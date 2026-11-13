# harita/: harita becerileri için belgeler ve açık veri örneği

15 harita becerisinin (M003–M034: mesafe, yön, çokgen, geohash, çevrimdışı yol rotası, çizim…) **kodu ve testleri** [`../kutuphane/`](../kutuphane/) altında `M…` klasörlerindedir. Bu klasör onların paket dışı belgelerini ve küçük bir açık veri örneğini içerir.

| Yol | İçerik |
|---|---|
| `belgeler/` | Dağıtım belgeleri: `README.md`, `README_TR.md`, `INSTALL_TR.md`, `LICENSE_INDEX.md`, `TEST_RESULTS.json`, `catalog.json` ve kurulum dosyaları. **ZIP dağıtımı için yazılmıştır**; `wheels/`, `map_data/` ve `examples/` gibi bu depoda bulunmayan klasörlerden söz edebilir |
| `ornek-veri/` | Kadıköy'den **yol ve alan** verisi (GeoJSON), ODbL lisansı ve atıf dosyası |

## Veri lisansı (önemli)

`ornek-veri/` içindeki veriler **© OpenStreetMap katkıcıları**, **Açık Veri Tabanı Lisansı (ODbL) 1.0** altındadır (`LICENSE-ODbL-1.0.txt`, `ATTRIBUTION.txt`). Beceri kodları kendi izin verici lisanslarındadır; bu veri ayrı lisanslıdır ve onlarca kapsanmaz. Sonuçları gösterirken atıf zorunludur.

## Bilerek yayınlanmayanlar

- **Yer (POI) verisi** (`places`): OpenStreetMap'te işletme ve **kişi adları** (ör. serbest meslek sahibi kişilerin adları) içerdiği için yayınlanmadı. Bu yüzden arama (`M032`) ve yakındaki yerler (`M033`) için hazır demo veri ve demo zinciri bu depoda **yoktur**.
- **Büyük OSM çıkarımları** (yaklaşık 314 MB): GitHub dosya sınırı ve boyut nedeniyle.
- **`wheels/` ve `.venv`**: üçüncü taraf ikili dosyalar.

## Ne doğrulandı

Harita becerilerinin 15'i de `kutuphane/` içinde, depodaki konumunda ve ağ kapalı ortamda geçti (bkz. [`../kutuphane/README.md`](../kutuphane/README.md)). Bu belgeler ve veri örneği için ayrı bir test koşulmadı.
