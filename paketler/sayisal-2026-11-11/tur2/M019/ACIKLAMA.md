# M019 — Dünya dönüş açısını hesaplama

## Ne işe yarar?

UT1 zaman ölçeğinde verilmiş iki parçalı Jülyen tarihten Dünya’nın dönüş açısını IAU 2000 modeline göre hesaplar. Takvim saati veya UTC kabul etmez.

## Hangi girdileri alır?

UT1 zaman ölçeğinde, iki parçalı Jülyen tarih (jd1, jd2).

## Ne üretir?

0–2π aralığında radyan ve derece olarak Dünya dönüş açısı.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/liberfa/erfa); sabit kaynak sürümü: `1a8044cde5b7763295d472a6443387239127c6c8`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

UTC tarihini UT1 yerine kullanmak yanlıştır. UT1-UTC farkını veya IERS verisini getirmez; kutup hareketi ve tam Dünya yönelim dönüşümü içermez. Sayısal sınır kontrolü, zaman ölçeğinin doğru girildiğini kanıtlamaz.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 31 test vardır; teslim kaydı da 31 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
