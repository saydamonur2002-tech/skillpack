# M001 — Kübik eğriyle ara değer ve türev

## Ne işe yarar?

Ölçülmüş noktalardan düzgün bir eğri kurar. İstenen noktada değeri, eğimi ve eğimdeki değişimi verir. Ölçüm aralığının dışındaki bir sorguyu da uçtaki eğri parçasıyla cevaplar; bu uzatma yanıltıcı olabilir.

## Hangi girdileri alır?

Sıralı x noktaları, karşılık gelen y ölçümleri, hesaplanacak noktalar ve isteğe bağlı uç koşulu.

## Ne üretir?

Her sorgu noktasında değer, birinci türev ve ikinci türev.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/certik/fortran-utils); sabit kaynak sürümü: `b43bd24cd421509a5bc6d3b9c3eeae8ce856ed88`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **MIT**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

En az 4, en çok 256 ölçüm noktası ve 512 sorgu kabul eder. Gürültüyü temizlemez. Ölçüm aralığının dışına uzatılan eğri yanıltıcı olabilir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 22 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 23 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
