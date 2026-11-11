# M014 — Tamamlanmamış gamma değerleri

## Ne işe yarar?

İstatistiksel hesaplarda kullanılan düzenlenmiş tamamlanmamış gamma fonksiyonunun alt ve üst kuyruk değerlerini hesaplar.

## Hangi girdileri alır?

Pozitif şekil parametresi (1e-5–1000) ve negatif olmayan x değeri (0–10.000).

## Ne üretir?

Boyutsuz P(shape,x) ve Q(shape,x) değerleri.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/scipy/scipy); sabit kaynak sürümü: `fcdc3d7b7c1b950d874ac3e890cccde3e2de1c6c`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Klasik çift duyarlıklı yöntemdir; uç kuyruklarda hassasiyet kaybı veya sayısal sıfıra yuvarlanma olabilir. Dağılım uydurmaz, ters fonksiyon çözmez ve istatistiksel karar vermez.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 42 test vardır; teslim kaydı da 42 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
