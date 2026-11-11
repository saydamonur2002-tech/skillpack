# M015 — Tamamlanmamış beta değeri

## Ne işe yarar?

İstatistiksel hesaplarda kullanılan düzenlenmiş tamamlanmamış beta integralini hesaplar.

## Hangi girdileri alır?

a ve b şekil parametreleri (1e-4–1000), x (0–1).

## Ne üretir?

Düzenlenmiş tamamlanmamış beta değeri I_x(a,b).

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/scipy/scipy); sabit kaynak sürümü: `03b1092cf0e0bdebcbe98a44d289208a1e597416`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Çift duyarlıkla çalışır; uç değerlere yakın hassasiyet kaybı olabilir. Ters beta, parametre uydurma veya istatistiksel karar motoru değildir. 300 kesir tekrarında yakınsamazsa açık hata verir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 39 test vardır; teslim kaydı da 39 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
