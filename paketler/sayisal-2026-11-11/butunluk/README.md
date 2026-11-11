# Bütünlük notu

Modüller buraya alınmadan önce iki arşivin SHA-256 değerleri kontrol edildi. Arşivlerin kendisi depoda yok; çalışan kopya `tur1/` ve `tur2/` altındadır.

| Grup | Arşiv | SHA-256 | Sonuç |
|---|---|---|---|
| tur1, M001–M010 | `mined-packs-2026-11-11.tar.gz` | `ed3de23530d446e4eb9c39ca08674fabaf1e95882dfbc47720e88a5e69a0b64f` | eşleşti |
| tur2, M011–M020 | `mined-packs-2026-11-11b.tar.gz` | `102a9ecdf3854852b49e2a0c54f41e6201bd9d3aec5901261d1dcfbecc0e8604` | eşleşti |

İkinci grubun dış `SHA256SUMS` listesindeki `catalog.json`, aktarım klasörünün kökünde ayrı durmuyordu. Arşivin içindeki `catalog.json` aynı özeti verdi: `123e51d204d703ea00b869ee569a3d121c2ec168da60b478da13cdaad06f0b89`.

Her modülün `FILES.sha256` listesi açılmış dosyalarla karşılaştırıldı: 428 kayıt, fark yok. Türkçe `ACIKLAMA.md` bu listelere eklenmedi; özgün özetler aynı kaldı.

`tur1/EXTRACTED_RELEASE_TEST_RESULTS.xml`, ilk grubun arşivindeki `TEST_RESULTS.xml` ile aynı 261 testi gösterir. Ayrım yalnız koşunun süresi ve zaman damgasıdır. İkisi de sıfır hata, sıfır atlama kaydeder.

Eski RESEARCH-ONLY arşivi bu teslimde yoktu. Aday listesidir, çalışan modül olarak eklenmedi.
