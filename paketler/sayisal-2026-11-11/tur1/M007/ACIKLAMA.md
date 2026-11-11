# M007 — Medyan çevresindeki yayılım

## Ne işe yarar?

Bir veri dizisinin ortancasını ve bu ortancadan tipik uzaklığını hesaplar.

## Hangi girdileri alır?

Bir boyutlu, en çok 4096 sonlu sayı.

## Ne üretir?

Medyan, medyan mutlak sapma (MAD) ve normal dağılıma göre ölçeklenmiş MAD.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/astropy/astropy); sabit kaynak sürümü: `87cc16fbf125de08066606439a5c5e471c44647b`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Ölçeklenmiş değer ancak uygun dağılım varsayımıyla standart sapma tahmini sayılır. Eksik değerleri otomatik atmaz. Farklı değerler içeren bir dizide MAD yine sıfır olabilir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 20 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 21 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
