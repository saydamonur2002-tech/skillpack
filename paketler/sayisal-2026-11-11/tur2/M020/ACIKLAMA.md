# M020 — Astronomik eksen dönüşümünü hesaplama

## Ne işe yarar?

TT zaman ölçeğindeki iki parçalı Jülyen tarihten, ortalama gök eksenleri için başlangıç çerçevesi farkı ile presesyon dönüşüm matrisini hesaplar. Takvim saati kabul etmez.

## Hangi girdileri alır?

TT zaman ölçeğinde, iki parçalı Jülyen tarih (jd1, jd2).

## Ne üretir?

GCRS sütun vektörlerinden tarih anının ortalama ekvator çerçevesine 3×3 dönüşüm matrisi, dört Fukushima–Williams açısı ve J2000’den Jülyen yüzyıl sayısı.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/liberfa/erfa); sabit kaynak sürümü: `1a8044cde5b7763295d472a6443387239127c6c8`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

UTC veya UT1 yerine TT gerektirir. Nutasyon, ışık sapması, Dünya dönüşü ve tam görünen konum hesabı yoktur. Çok geniş sayısal tarih sınırı, modelin her dönemde geçerli olduğunu göstermez.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 27 test vardır; teslim kaydı da 27 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
