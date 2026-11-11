"""Yerel paket deposu.

Her çağrıda dizini yeniden tarar: çalışırken dizine atılan yeni paket bir sonraki
istekte kullanılabilir, silinen ya da iptal edilen paket bir sonraki istekte düşer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path

from .pack import MANIFEST_FILE, Pack, validate_pack
from .revocation import RevocationError, cached
from .signing import verify_pack
from .state import InstallState, StateError


@dataclass
class Rejected:
    path: Path
    reasons: list[str]


@dataclass
class Scan:
    packs: dict[str, Pack] = field(default_factory=dict)
    pack_ids: dict[str, str] = field(default_factory=dict)
    rejected: list[Rejected] = field(default_factory=list)


class Registry:
    def __init__(
        self,
        packs_dir: Path,
        trust_dir: Path,
        revocations: Path | None = None,
        revocation_cache: Path | None = None,
        revocation_max_age: timedelta | None = timedelta(days=7),
        state: InstallState | None = None,
    ) -> None:
        self.packs_dir = packs_dir
        self.trust_dir = trust_dir
        self.revocations = revocations
        self.revocation_cache = revocation_cache
        self.revocation_max_age = revocation_max_age
        self.state = state

    def _revocations(self) -> tuple[Path | None, str | None]:
        """Kullanılacak iptal listesi ve (varsa) hiçbir paketin yüklenmemesi için gerekçe.

        İmzalı önbellek verilmişse yalnız o kullanılır. Son eşitleme sınırdan eskiyse
        liste bayat sayılır: iptal edilmiş bir paketi bilmeden çalıştırmaktansa
        hiçbir paket yüklenmez.
        """
        if self.revocation_cache is None:
            return self.revocations, None
        try:
            entry = cached(self.revocation_cache)
        except RevocationError as exc:
            return None, str(exc)
        if self.revocation_max_age is not None and entry.age() > self.revocation_max_age:
            days = entry.age().total_seconds() / 86400
            limit = self.revocation_max_age.total_seconds() / 86400
            return None, (
                f"iptal listesi bayat: son eşitleme {days:.1f} gün önce (sınır {limit:g} gün); "
                "'skillpack revocations sync' çalıştırın"
            )
        return entry.path, None

    def scan(self) -> Scan:
        """Yalnız hem doğrulanan hem imzası geçen paketleri yükler."""
        result = Scan()
        if not self.packs_dir.is_dir():
            return result
        revocations, blocked = self._revocations()
        for path in sorted(self.packs_dir.iterdir()):
            if not (path / MANIFEST_FILE).is_file():
                continue
            if blocked:
                result.rejected.append(Rejected(path, [blocked]))
                continue
            verification = verify_pack(path, self.trust_dir, revocations)
            if not verification.ok:
                result.rejected.append(Rejected(path, verification.reasons))
                continue
            pack, report = validate_pack(path)
            if pack is None or not report.ok:
                result.rejected.append(Rejected(path, report.errors))
                continue
            if self.state is not None:
                try:
                    refusal = self.state.admit(
                        pack.name, pack.version, verification.key_id or "", verification.pack_id or ""
                    )
                except StateError as exc:
                    refusal = str(exc)
                if refusal:
                    result.rejected.append(Rejected(path, [refusal]))
                    continue
            result.packs[pack.name] = pack
            result.pack_ids[pack.name] = verification.pack_id or ""
        return result
