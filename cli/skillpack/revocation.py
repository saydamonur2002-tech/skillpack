"""İmzalı iptal listesi: The Update Framework (TUF) ile dağıtım ve eşitleme.

İptal listesi düz bir dosyayken onu değiştirebilen biri iptali kaldırabilir, eski
bir listeyi yeniden sunabilir ya da güncellemeyi sessizce durdurabilir. TUF bu
üçünü de kapatır: liste imzalıdır, sürüm geri gidemez, zaman damgasının süresi
dolunca eski liste kabul edilmez. Uygulama python-tuf'tur (Apache-2.0 / MIT).

İstemci yalnız kök meta verisine (`root.json`) güvenir; onu ilk kurulumda elden
alır. Kaynak bir HTTP(S) adresi ya da yerel bir dizin (USB, ağ paylaşımı) olabilir.

`publish` küçük kurulumlar ve testler içindir: dört rolün anahtarını tek dizinde,
şifresiz tutar. Gerçek bir yayında kök anahtarı çevrim dışı tutulmalı ve roller
ayrı kişilerde olmalıdır (ör. tuf-on-ci).
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import unquote, urlparse

TARGET = "revocations.json"
STAMP = "sync.json"
ROLES = ("root", "targets", "snapshot", "timestamp")
LIST_VERSION = "0.1-taslak"


class RevocationError(Exception):
    pass


def _tuf():
    try:
        import tuf.api.metadata  # noqa: F401
        import tuf.ngclient  # noqa: F401
    except ImportError as exc:  # pragma: no cover - kurulum ortamına bağlı
        raise RevocationError(
            "imzalı iptal listesi için TUF gerekli: pip install 'skillpack[tuf]'"
        ) from exc


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------- istemci


@dataclass
class Cached:
    """Yerel önbellekteki son doğrulanmış liste."""

    path: Path
    synced_at: datetime
    source: str

    def age(self) -> timedelta:
        return _now() - self.synced_at


def _file_fetcher():
    from tuf.api.exceptions import DownloadHTTPError
    from tuf.ngclient.fetcher import FetcherInterface

    class FileFetcher(FetcherInterface):
        """`file://` adreslerini okur: çevrim dışı sahada liste USB ile taşınabilir."""

        def _fetch(self, url: str) -> Iterator[bytes]:
            path = Path(unquote(urlparse(url).path))
            if not path.is_file():
                raise DownloadHTTPError(f"dosya yok: {path}", 404)
            return iter([path.read_bytes()])

    return FileFetcher()


def _locations(source: str) -> tuple[str, str, Any]:
    """Kaynaktan meta veri ve hedef adreslerini ve gerekiyorsa dosya okuyucuyu üretir."""
    if "://" in source and not source.startswith("file://"):
        base = source.rstrip("/")
        return f"{base}/metadata/", f"{base}/targets/", None
    root = Path(unquote(urlparse(source).path) if source.startswith("file://") else source).resolve()
    if not root.is_dir():
        raise RevocationError(f"iptal deposu dizini yok: {root}")
    return f"{root.as_uri()}/metadata/", f"{root.as_uri()}/targets/", _file_fetcher()


def sync(source: str, trusted_root: Path, cache: Path) -> Cached:
    """Listeyi kaynaktan çeker, TUF kurallarıyla doğrular ve önbelleğe yazar.

    Doğrulama düşerse önbellek değişmez ve hata fırlatılır.
    """
    _tuf()
    from tuf.api.exceptions import DownloadError, RepositoryError
    from tuf.ngclient import Updater, UpdaterConfig

    try:
        bootstrap = trusted_root.read_bytes()
    except OSError as exc:
        raise RevocationError(f"güvenilen kök okunamadı: {exc}") from exc
    metadata_url, targets_url, fetcher = _locations(source)
    metadata_dir = cache / "metadata"
    incoming = cache / "incoming"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(incoming, ignore_errors=True)
    incoming.mkdir(parents=True)
    try:
        updater = Updater(
            str(metadata_dir), metadata_url, str(incoming), targets_url,
            fetcher=fetcher, config=UpdaterConfig(prefix_targets_with_hash=False),
            bootstrap=bootstrap,
        )
        updater.refresh()
        info = updater.get_targetinfo(TARGET)
        if info is None:
            raise RevocationError(f"depoda {TARGET} yok")
        downloaded = Path(updater.download_target(info))
        entries = _read_list(downloaded)
    except (RepositoryError, DownloadError, OSError) as exc:
        raise RevocationError(f"iptal listesi doğrulanamadı: {type(exc).__name__}: {exc}") from exc
    finally:
        if not (incoming / TARGET).is_file():
            shutil.rmtree(incoming, ignore_errors=True)
    del entries
    (incoming / TARGET).replace(cache / TARGET)
    shutil.rmtree(incoming, ignore_errors=True)
    stamp = {"synced_at": _now().isoformat(timespec="seconds"), "source": source}
    (cache / STAMP).write_text(json.dumps(stamp, ensure_ascii=False) + "\n", "utf-8")
    return cached(cache)


def cached(cache: Path) -> Cached:
    try:
        stamp = json.loads((cache / STAMP).read_text("utf-8"))
        synced_at = datetime.fromisoformat(stamp["synced_at"])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise RevocationError(
            f"iptal önbelleği boş ya da bozuk ({cache}); önce 'skillpack revocations sync' çalıştırın"
        ) from exc
    if not (cache / TARGET).is_file():
        raise RevocationError(f"iptal önbelleğinde {TARGET} yok ({cache})")
    return Cached(cache / TARGET, synced_at, str(stamp.get("source", "")))


def _read_list(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RevocationError(f"iptal listesi okunamadı: {exc}") from exc
    revoked = data.get("revoked") if isinstance(data, dict) else None
    if not isinstance(revoked, list):
        raise RevocationError("iptal listesi 'revoked' dizisi içermeli")
    return revoked


# ---------------------------------------------------------------- yayıncı


def _load_signer(path: Path):
    from cryptography.hazmat.primitives import serialization
    from securesystemslib.signer import CryptoSigner

    return CryptoSigner(serialization.load_pem_private_key(path.read_bytes(), password=None))


def _new_signer(path: Path):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private = Ed25519PrivateKey.generate()
    path.write_bytes(
        private.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    path.chmod(0o600)
    return _load_signer(path)


def publish(
    repo: Path,
    keys: Path,
    add: list[dict[str, Any]] | None = None,
    timestamp_days: float = 7,
    now: datetime | None = None,
) -> dict[str, Any]:
    """İptal deposunu oluşturur ya da günceller ve yeniden imzalar.

    `add` boşsa yalnız zaman damgası tazelenir: yayıncı listeyi düzenli olarak
    yeniden imzalamazsa istemciler `timestamp_days` sonra listeyi bayat sayar.
    """
    _tuf()
    from tuf.api.metadata import (
        Metadata, MetaFile, Root, Snapshot, TargetFile, Targets, Timestamp,
    )
    from tuf.api.serialization.json import JSONSerializer

    now = now or _now()
    serializer = JSONSerializer(compact=False)
    metadata_dir, targets_dir = repo / "metadata", repo / "targets"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    targets_dir.mkdir(parents=True, exist_ok=True)
    keys.mkdir(parents=True, exist_ok=True)

    fresh = not (metadata_dir / "root.json").is_file()
    if fresh:
        signers = {role: _new_signer(keys / f"{role}.pem") for role in ROLES}
        root = Root(expires=now + timedelta(days=365), consistent_snapshot=False)
        for role, signer in signers.items():
            root.add_key(signer.public_key, role)
        root_md = Metadata(root)
        root_md.sign(signers["root"])
        root_md.to_file(str(metadata_dir / "1.root.json"), serializer)
        shutil.copyfile(metadata_dir / "1.root.json", metadata_dir / "root.json")
        md = {
            "targets": Metadata(Targets(version=1, expires=now)),
            "snapshot": Metadata(Snapshot(version=1, expires=now)),
            "timestamp": Metadata(Timestamp(version=1, expires=now)),
        }
        entries: list[dict[str, Any]] = []
    else:
        try:
            signers = {role: _load_signer(keys / f"{role}.pem") for role in ROLES[1:]}
            md = {role: Metadata.from_file(str(metadata_dir / f"{role}.json")) for role in ROLES[1:]}
        except (OSError, ValueError) as exc:
            raise RevocationError(f"iptal deposu ya da anahtarları okunamadı: {exc}") from exc
        entries = _read_list(targets_dir / TARGET)

    changed = fresh
    for entry in add or []:
        if entry not in entries:
            entries.append(entry)
            changed = True

    if changed:
        document = {
            "revocations": LIST_VERSION,
            "updated_at": now.isoformat(timespec="seconds"),
            "revoked": entries,
        }
        (targets_dir / TARGET).write_text(
            json.dumps(document, indent=2, ensure_ascii=False) + "\n", "utf-8"
        )
        targets = md["targets"].signed
        targets.version += 0 if fresh else 1
        targets.expires = now + timedelta(days=365)
        targets.targets[TARGET] = TargetFile.from_file(TARGET, str(targets_dir / TARGET))
        snapshot = md["snapshot"].signed
        snapshot.version += 0 if fresh else 1
        snapshot.expires = now + timedelta(days=365)
        snapshot.meta["targets.json"] = MetaFile(targets.version)
    timestamp = md["timestamp"].signed
    timestamp.version += 0 if fresh else 1
    timestamp.expires = now + timedelta(days=timestamp_days)
    timestamp.snapshot_meta = MetaFile(md["snapshot"].signed.version)

    for role in ("targets", "snapshot", "timestamp"):
        if role != "timestamp" and not changed:
            continue
        md[role].signatures.clear()
        md[role].sign(signers[role])
        md[role].to_file(str(metadata_dir / f"{role}.json"), serializer)
    return {
        "created": fresh,
        "entries": len(entries),
        "list_version": md["targets"].signed.version,
        "timestamp_version": timestamp.version,
        "timestamp_expires": timestamp.expires.isoformat(timespec="seconds"),
        "trusted_root": str(metadata_dir / "1.root.json"),
    }
