# M018 — Takvim tarihini Jülyen güne çevirme

## Ne işe yarar?

Bir Gregoryen takvim gününü, saat olmadan gece yarısı kabul ederek, astronomide kullanılan Jülyen gün ve değiştirilmiş Jülyen gün sayılarına dönüştürür.

## Hangi girdileri alır?

Yıl (-4799–9999), ay ve geçerli gün; astronomik yıl numaralamasıyla.

## Ne üretir?

Gece yarısına karşılık gelen iki parçalı Jülyen tarih, MJD ve kolaylık için toplam JD.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/liberfa/erfa); sabit kaynak sürümü: `1a8044cde5b7763295d472a6443387239127c6c8`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Saat dilimi veya UTC/TT/UT1 dönüşümü yapmaz. Astronomik yıl sıfırı vardır; tarihsel MÖ etiketleriyle aynı değildir. İş günü/tatil hesabı yoktur. Hassas sonraki hesaplarda iki tarih parçası korunmalıdır.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 28 test vardır; teslim kaydı da 28 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
