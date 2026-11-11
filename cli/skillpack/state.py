"""Kurulu paketlerin kaydı: geri sarma ve yayıncı değişimine karşı koruma.

İmza, bir paketin kimden geldiğini söyler; ama eski ve hatalı bir sürüm de aynı
anahtarla imzalıdır. Bu kayıt, her paket adının en son kabul edilen sürümünü ve
onu imzalayan anahtarı tutar (ilk görüşte güven):

- daha düşük sürüm reddedilir (geri sarma),
- aynı sürümün farklı içeriği reddedilir (yayımlanmış sürüm değişmez),
- başka bir anahtarla imzalanmış aynı adlı paket reddedilir (ad gaspı).

Bilerek geri dönmek ya da yayıncı değiştirmek için kayıt `forget` ile silinir.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

_VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)")


class StateError(Exception):
    pass


def version_key(version: str) -> tuple[int, int, int] | None:
    match = _VERSION.match(version)
    return tuple(int(part) for part in match.groups()) if match else None  # type: ignore[return-value]


class InstallState:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _load(self) -> dict[str, dict[str, Any]]:
        try:
            data = json.loads(self.path.read_text("utf-8"))
        except FileNotFoundError:
            return {}
        except (OSError, json.JSONDecodeError) as exc:
            raise StateError(f"kurulum kaydı okunamadı ({self.path}): {exc}") from exc
        packs = data.get("packs") if isinstance(data, dict) else None
        if not isinstance(packs, dict):
            raise StateError(f"kurulum kaydı bozuk ({self.path})")
        return packs

    def _save(self, packs: dict[str, dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_name(self.path.name + ".tmp")
        temporary.write_text(
            json.dumps({"packs": packs}, indent=2, ensure_ascii=False, sort_keys=True) + "\n", "utf-8"
        )
        os.replace(temporary, self.path)

    def admit(self, name: str, version: str, key_id: str, pack_id: str) -> str | None:
        """Paketi kayda göre sınar. Kabulse kaydı günceller ve `None` döner; değilse gerekçeyi."""
        packs = self._load()
        seen = packs.get(name)
        if seen is not None:
            if seen["key_id"] != key_id:
                return (
                    f"yayıncı anahtarı değişmiş (kayıtlı {seen['key_id']}, gelen {key_id}); "
                    "bilerek değiştiyse 'skillpack forget' ile kaydı silin"
                )
            old, new = version_key(seen["version"]), version_key(version)
            if old is None or new is None:
                if seen["version"] != version:
                    return f"sürüm karşılaştırılamıyor (kayıtlı {seen['version']}, gelen {version})"
            elif new < old:
                return f"eski sürüme geri sarma (kayıtlı {seen['version']}, gelen {version})"
            if seen["version"] == version and seen["pack_id"] != pack_id:
                return f"{version} sürümünün içeriği değişmiş; yayımlanmış sürüm değiştirilemez"
            if seen["version"] == version:
                return None
        packs[name] = {"version": version, "key_id": key_id, "pack_id": pack_id}
        self._save(packs)
        return None

    def forget(self, name: str) -> bool:
        packs = self._load()
        if name not in packs:
            return False
        del packs[name]
        self._save(packs)
        return True

    def entries(self) -> dict[str, dict[str, Any]]:
        return self._load()
