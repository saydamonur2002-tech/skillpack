# oyun/: 2B şehir oyununu kuran 12 beceri ve 19 adımlık akış

Basit grafikli, yukarıdan bakışlı, tek HTML dosyasında çalışan 2B bir şehir oyununu **12 küçük beceri ve bir akış dosyasıyla** kurar. Her beceri bir açık kaynak projeden ya da özgün koddan çıkarılmış tek işlevdir (şehir üretici, araç fiziği, çarpışma, yol bulma, NPC yönlendirme, arananlık, görev, ekonomi, kayıt, ses, oyun döngüsü, HTML üretici). Akış dosyası (`flows/oyun-kur.flow.json`) hangi adımda hangi aracın hangi girdiyle çağrılacağını söyler; `flows/run_flow.py` bunu modelsiz çalıştırır.

> **Beklentiyi ayarlayalım:** Bu, 2B, düz renkli karolu küçük bir şehirdir (40×30 harita). "GTA 5" ölçeğinde bir oyun **değildir**. Paketler ve oyun **usta/oyun tasarımcısı onayı taşımaz** (durum: `tested-awaiting-usta-approval`). Ön sürümdür.

## Paketler

| No | Beceri | Kaynak (lisans) |
|---|---|---|
| G001 | Sabit adımlı oyun döngüsü | IceCreamYou/MainLoop.js (MIT) |
| G002 | Şehir haritası üretici | özgün (MIT) |
| G003 | Araç fiziği | AtsushiSakai/PythonRobotics (MIT) |
| G004 | Çarpışma testi | jriecken/sat-js (MIT) |
| G005 | Yol bulma | brean/python-pathfinding (MIT) |
| G006 | NPC yönlendirme | Mugen87/yuka (MIT) |
| G007 | Arananlık seviyesi | özgün (MIT) |
| G008 | Görev sistemi | özgün (MIT) |
| G009 | Ekonomi ve envanter | özgün (MIT) |
| G010 | Kayıt ve yükleme | özgün (MIT) |
| G011 | Ses efekti | KilledByAPixel/ZzFX (MIT) |
| G012 | HTML oyun üretici | özgün (MIT) |

Her paket kendi `SKILL.md`, `manifest.json`, `LICENSE`/`NOTICE`, `upstream/` (kaynak kopyası), `tool/` (JSON girdi/çıktılı CLI), `mcp/` (isteğe bağlı MCP girişi) ve `tests/` klasörünü taşır. Lisans dizini: [`LICENSE_INDEX.md`](LICENSE_INDEX.md).

## Çalıştırma

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-test.txt     # jsonschema==4.26.0, mcp==1.30.0, pytest==9.2.0
.venv/bin/python flows/run_flow.py --out oyun_cikti   # 19 adım; ağ gerekmez
# sonra oyun_cikti/index.html dosyasını tarayıcıda açın (WASD/oklar, boşluk el freni, K/L kaydet/yükle)
```

Hazır bir çıktı: [`ornek/index.html`](ornek/index.html) (33.964 bayt). Not: `BENIOKU.md` ve `requirements-offline.txt` çevrimdışı kurulum için `wheels/` klasörünü anlatır; bu klasör **depoda yer almaz** (boyut ve üçüncü taraf ikili dosyalar), yukarıdaki pip komutunu kullanın.

## Ne doğrulandı (13 Kasım 2026, Linux, Python 3.13, ağ kapalı)

- **Akış 19/19 adım çalıştı** ve ürettiği `index.html`, `ornek/index.html` ile **bayt bayt aynı** (SHA-256 `64d18d868b8da12f80eeeaf4c007a12a70566cd3c2523b20e8cadf2378b143fc`).
- Testler: **384 geçti**, 1 atlandı (`wheels/` testi, klasör depoda yok), **1 başarısız** (aşağıda).
- Bu sonuçlar bir kurulum ve belirlenimcilik kanıtıdır; oyunun "eğlenceli" ya da "doğru" olduğunun kanıtı değildir.

## Bilinen sorun ve sınırlar

- **G011 isteğe bağlı kaynak yeniden çalıştırma testi başarısız** (`tests/test_upstream_references.py::test_upstream_rerun[G011]`): Node.js v22.23.4 ile kaynağı yeniden koşturunca `rms` değeri tolerans 1×10⁻¹²'yi **2,0×10⁻¹²** aşıyor (kayan nokta farkı, Node/V8 sürümüne bağlı olabilir). Paketin kendi zorunlu testleri geçiyor. Node PATH'te yoksa bu test atlanır.
- Yalnız Linux'ta denendi; Windows ve macOS denenmedi.
- `tests/test_release_audit.py` kişiye özel yasaklı ifadeleri dosyada tutmaz; çalıştırırken `EKSTRA_IZ` ortam değişkeniyle verilir.
- Bu akışı bir modelin yürütmesinin token maliyeti ve davranışı için: [`docs/deney/oyun-akisi-deneyi.md`](../docs/deney/oyun-akisi-deneyi.md) (her hücre tek koşu).
