"""Yerel paket deposu.

Her çağrıda dizini yeniden tarar: çalışırken dizine atılan yeni paket bir sonraki
istekte kullanılabilir, silinen ya da iptal edilen paket bir sonraki istekte düşer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .pack import MANIFEST_FILE, Pack, validate_pack
from .signing import verify_pack


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
    ) -> None:
        self.packs_dir = packs_dir
        self.trust_dir = trust_dir
        self.revocations = revocations

    def scan(self) -> Scan:
        """Yalnız hem doğrulanan hem imzası geçen paketleri yükler."""
        result = Scan()
        if not self.packs_dir.is_dir():
            return result
        for path in sorted(self.packs_dir.iterdir()):
            if not (path / MANIFEST_FILE).is_file():
                continue
            verification = verify_pack(path, self.trust_dir, self.revocations)
            if not verification.ok:
                result.rejected.append(Rejected(path, verification.reasons))
                continue
            pack, report = validate_pack(path)
            if pack is None or not report.ok:
                result.rejected.append(Rejected(path, report.errors))
                continue
            result.packs[pack.name] = pack
            result.pack_ids[pack.name] = verification.pack_id or ""
        return result
