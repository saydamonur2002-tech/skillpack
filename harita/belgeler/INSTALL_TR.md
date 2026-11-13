# Kurulum (tek arşiv)

Bu ZIP, 15 harita becerisini, Kadıköy demo verisini, ortak testleri, örnek haritayı ve çevrimdışı kurulum için Python tekerleklerini (wheels) birlikte içerir. İnternet gerekmez.

## 1. Arşivi açın

ZIP'i bir klasöre çıkarın. İçinde `map_packs_2026-11-12` adında bir klasör oluşur. Bundan sonraki komutları o klasörde çalıştırın.

Linux / macOS:

```
cd map_packs_2026-11-12
python3 -m venv .venv
.venv/bin/pip install --no-index --find-links wheels --no-deps --disable-pip-version-check -r requirements-offline.txt
```

Windows:

```
cd map_packs_2026-11-12
python -m venv .venv
.venv\Scripts\pip install --no-index --find-links wheels --no-deps --disable-pip-version-check -r requirements-offline.txt
```

`--no-deps` şarttır: MCP paketi JWT imzası için `cryptography` ister, o tekerlek ~4,7 MB olduğu için bu arşive konmadı. Yerel (stdio) kullanım ve testler onsuz çalışır.

**Python 3.13, Linux x86_64** bu arşivle tamamen çevrimdışı kurulur. Windows, macOS veya başka bir Python sürümünde `pydantic-core` ile `rpds-py` tekerlekleri bu arşivde yoktur; bir kez internetle şunu eklemeniz gerekir:

```
pip install pydantic-core==2.50.4 rpds-py==2026.9.1
```

Windows'ta MCP ayrıca `pywin32` ister; o da bu arşivde yoktur (`pip install pywin32`).

## 2. Claude Desktop ayarı

`claude_desktop_config.json` içindeki `/MUTLAK/YOL/map_packs_2026-11-12` yer tutucusunu, bu klasörün **tam yolu** ile değiştirin (Windows'ta örn. `C:/harita/map_packs_2026-11-12`). `SKILLPACK_MAP_OUTPUT` için bir çıktı klasörü oluşturun (örn. `harita_cikti`) ve yolunu da güncelleyin.

JSON'u Claude Desktop ayarlarındaki MCP yapılandırmasına yapıştırıp Claude Desktop'ı yeniden başlatın. Araç listesinde 15 araç görünmelidir.

## 3. Örnek komut

Claude'a şunu yazın:

> Kadıköy iskelesinden Moda'ya yürüyerek rota çıkar, kaç dakika sürer? Sonra altlıklı bir SVG harita olarak çiz.

Diğer örnekler `README_TR.md` içindedir.

## İsteğe bağlı doğrulama

```
.venv/bin/python -m pytest
```

(Windows'ta `.venv\Scripts\python -m pytest`.)

## Bu arşive konmayan tekerlekler

Boyutu 9 MB'ın altında tutmak için şunlar çıkarıldı:

- `cryptography` (MCP'nin `pyjwt[crypto]` bağımlılığı; stdio için gerekmez)
- `cffi` ve `pycparser` (yalnızca cryptography için)
- `networkx` (M030/M031 içindeki yol bulma zaten pakete aktarıldı; yalnızca isteğe bağlı üst akım doğrulaması kullanır)
- `pydantic-core` / `rpds-py` için Linux x86_64 + CPython 3.13 dışındaki platform tekerlekleri

Ayrıntılı beceri listesi, sınırlar ve lisans özeti: `README_TR.md`, `LICENSE_INDEX.md`.
