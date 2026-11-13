# game_pack_2026-11-12: Basit arayüzlü 2B açık şehir oyunu skill paketi

GTA tarzı (yukarıdan bakışlı, 2B, basit grafikli) bir şehir oyununu kuran 12 skill bu pakette. Her skill bağımsızdır. Her biri şunları içerir:
- JSON girdi/çıktılı deterministik Python CLI
- tek araçlı FastMCP stdio sunucusu (64 KB girdi sınırı, 10 sn zaman aşımı)
- pytest testleri
- `SKILL.md`, `TEACHING.md`, `LICENSE`/`NOTICE`

Hepsini tek bir sistem olarak çalıştıran, skill'den bağımsız akış dosyası `flows/oyun-kur.flow.json`. Türkçe açıklaması `flows/AKIS.md` içinde.

**İlke:** kod karar verir, model açıklar, usta onaylar. Usta onayı **bekliyor**.

## Hızlı başlangıç

```
python3 -m venv .venv
.venv/bin/pip install --no-index --find-links wheels --no-deps -r requirements-offline.txt
.venv/bin/python flows/run_flow.py --out oyun_cikti
```

Sonra `oyun_cikti/index.html` dosyasını tarayıcıda açın. İnternet gerekmez.

Kontroller:
- WASD / oklar: sür
- Boşluk: el freni
- K / L: kaydet / yükle
- Dokunmatik ekranda pad çıkar

Ses ilk tuşa basınca başlar. Hazır bir örnek `ornek/index.html` içinde.

## Testler

```
.venv/bin/python -m pytest
```

Şunları çalıştırır:
- bütün paket testleri
- gerçek stdio MCP testleri
- upstream referans testleri (`node` ve `numpy` gerekir; yoksa atlanır)
- uçtan uca akış testi

## Notlar

- `wheels/` klasöründeki tekerlekler Linux x86_64 ve CPython 3.13 içindir. Başka platformda bağlantılı kurulum yapın: `pip install -r requirements-test.txt`.
- Paket telemetri içermez ve ağa erişmez.
- Lisanslar `LICENSE_INDEX.md` içinde.
- MCP istemci örneği `claude_desktop_config.json` içinde. `/MUTLAK/YOL` kısmını kendi yolunuzla değiştirin.
