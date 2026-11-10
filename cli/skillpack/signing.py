"""İçerik özeti, Ed25519 imza, doğrulama ve iptal denetimi.

İmza asimetriktir: imzalayan özel anahtar yalnız yayıncıdadır, çalıştırıcı
yalnız açık anahtarı taşır. Açık anahtarı ele geçiren biri paket imzalayamaz.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from . import SPEC_VERSION
from .pack import MANIFEST_FILE, SIGNATURE_FILE, PackError, load_pack

# Kanonik biçimin RFC 8785 ile aynı çıktıyı vermesi için yollar bu kümeyle sınırlıdır.
_SAFE_PATH = re.compile(r"^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$")


class SigningError(Exception):
    pass


@dataclass
class Verification:
    ok: bool
    pack_id: str | None = None
    key_id: str | None = None
    reasons: list[str] = field(default_factory=list)


def checksums(root: Path) -> dict[str, str]:
    """Paketteki her dosyanın SHA-256 özeti (imza dosyası hariç)."""
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise SigningError(f"sembolik bağ pakete giremez: {relative}")
        if path.is_dir() or relative == SIGNATURE_FILE:
            continue
        if not _SAFE_PATH.match(relative):
            raise SigningError(
                f"dosya yolu yalnız A-Z a-z 0-9 . _ - / içerebilir: {relative}"
            )
        result[relative] = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def canonical(data: Any) -> bytes:
    """Anahtarları sıralı, boşluksuz, UTF-8 JSON."""
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _payload(name: str, version: str, sums: dict[str, str]) -> bytes:
    return canonical(
        {"checksums": sums, "name": name, "skillpack": SPEC_VERSION, "version": version}
    )


def pack_id(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def key_id(public_key: Ed25519PublicKey) -> str:
    raw = public_key.public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    return hashlib.sha256(raw).hexdigest()[:16]


def generate_key(private_path: Path, trust_dir: Path) -> str:
    """Yeni anahtar çifti üretir. Özel anahtar şifresiz PEM olarak yazılır."""
    if private_path.exists():
        raise SigningError(f"dosya zaten var, üzerine yazılmadı: {private_path}")
    private = Ed25519PrivateKey.generate()
    private_path.write_bytes(
        private.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    private_path.chmod(0o600)
    public = private.public_key()
    identifier = key_id(public)
    trust_dir.mkdir(parents=True, exist_ok=True)
    (trust_dir / f"{identifier}.pem").write_bytes(
        public.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    return identifier


def load_private_key(path: Path) -> Ed25519PrivateKey:
    try:
        key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    except (OSError, ValueError, TypeError) as exc:
        raise SigningError(f"özel anahtar okunamadı: {exc}") from exc
    if not isinstance(key, Ed25519PrivateKey):
        raise SigningError("özel anahtar Ed25519 değil")
    return key


def load_trusted_keys(trust_dir: Path) -> dict[str, Ed25519PublicKey]:
    keys: dict[str, Ed25519PublicKey] = {}
    if not trust_dir.is_dir():
        return keys
    for path in sorted(trust_dir.glob("*.pem")):
        try:
            key = serialization.load_pem_public_key(path.read_bytes())
        except ValueError:
            continue
        if isinstance(key, Ed25519PublicKey):
            keys[key_id(key)] = key
    return keys


def sign_pack(root: Path, private_path: Path) -> dict[str, Any]:
    pack = load_pack(root)
    private = load_private_key(private_path)
    sums = checksums(root)
    payload = _payload(pack.name, pack.version, sums)
    bundle = {
        "skillpack": SPEC_VERSION,
        "algorithm": "ed25519",
        "key_id": key_id(private.public_key()),
        "pack_id": pack_id(payload),
        "name": pack.name,
        "version": pack.version,
        "checksums": sums,
        "signature": base64.b64encode(private.sign(payload)).decode("ascii"),
    }
    (root / SIGNATURE_FILE).write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", "utf-8"
    )
    return bundle


def load_revocations(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    try:
        data = json.loads(path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SigningError(f"iptal listesi okunamadı: {exc}") from exc
    revoked = data.get("revoked") if isinstance(data, dict) else None
    if not isinstance(revoked, list):
        raise SigningError("iptal listesi 'revoked' dizisi içermeli")
    return revoked


def verify_pack(
    root: Path, trust_dir: Path, revocations: Path | None = None
) -> Verification:
    """Paketi yüklemeden önce yapılan denetim. Herhangi biri düşerse paket reddedilir."""
    result = Verification(ok=False)
    try:
        bundle = json.loads((root / SIGNATURE_FILE).read_text("utf-8"))
    except FileNotFoundError:
        result.reasons.append("imza dosyası yok")
        return result
    except (OSError, json.JSONDecodeError) as exc:
        result.reasons.append(f"imza dosyası okunamadı: {exc}")
        return result
    if not isinstance(bundle, dict):
        result.reasons.append("imza dosyası bir nesne olmalı")
        return result

    major = str(bundle.get("skillpack", "")).split(".")[0]
    if major != SPEC_VERSION.split(".")[0]:
        result.reasons.append(f"desteklenmeyen spesifikasyon sürümü: {bundle.get('skillpack')}")
        return result
    if bundle.get("algorithm") != "ed25519":
        result.reasons.append(f"desteklenmeyen imza algoritması: {bundle.get('algorithm')}")
        return result

    try:
        pack = load_pack(root)
        actual = checksums(root)
    except (PackError, SigningError) as exc:
        result.reasons.append(str(exc))
        return result

    signed = bundle.get("checksums")
    if not isinstance(signed, dict):
        result.reasons.append("imza dosyasında checksums yok")
        return result
    for path in sorted(set(actual) - set(signed)):
        result.reasons.append(f"imzalanmamış dosya: {path}")
    for path in sorted(set(signed) - set(actual)):
        result.reasons.append(f"imzalı dosya eksik: {path}")
    for path in sorted(set(actual) & set(signed)):
        if actual[path] != signed[path]:
            result.reasons.append(f"dosya imzadan sonra değişmiş: {path}")
    if bundle.get("name") != pack.name or bundle.get("version") != pack.version:
        result.reasons.append(f"imzadaki ad/sürüm {MANIFEST_FILE} ile uyuşmuyor")
    if result.reasons:
        return result

    payload = _payload(pack.name, pack.version, actual)
    result.pack_id = pack_id(payload)
    result.key_id = str(bundle.get("key_id"))
    if bundle.get("pack_id") != result.pack_id:
        result.reasons.append("paket kimliği uyuşmuyor")
        return result

    public = load_trusted_keys(trust_dir).get(result.key_id)
    if public is None:
        result.reasons.append(f"imzalayan anahtar güvenilenler arasında değil: {result.key_id}")
        return result
    try:
        public.verify(base64.b64decode(str(bundle.get("signature", "")), validate=True), payload)
    except (InvalidSignature, ValueError):
        result.reasons.append("imza geçersiz")
        return result

    try:
        revoked = load_revocations(revocations)
    except SigningError as exc:
        result.reasons.append(str(exc))
        return result
    for entry in revoked:
        if not isinstance(entry, dict):
            continue
        if entry.get("pack_id") == result.pack_id:
            result.reasons.append(f"paket iptal edilmiş: {entry.get('reason', 'gerekçe yok')}")
        if entry.get("key_id") == result.key_id:
            result.reasons.append(f"imzalayan anahtar iptal edilmiş: {entry.get('reason', 'gerekçe yok')}")
    result.ok = not result.reasons
    return result
