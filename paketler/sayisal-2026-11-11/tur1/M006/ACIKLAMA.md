# M006 — Uç değerlerden daha az etkilenen özet

## Ne işe yarar?

Aşırı yüksek veya düşük gözlemlerin etkisini azaltarak bir veri dizisinin merkezini ve yayılımını hesaplar.

## Hangi girdileri alır?

Bir boyutlu sayı dizisi ve isteğe bağlı merkez/yayılım ayarları. Ek bir anahtar, yayılım hesabında bütün diziyi mi yoksa merkeze yakın kalan gözlemleri mi sayacağını seçer.

## Ne üretir?

Biweight merkez, orta varyans ve ölçek değerleri.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/astropy/astropy); sabit kaynak sürümü: `87cc16fbf125de08066606439a5c5e471c44647b`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

En çok 4096 sonlu sayı; eksik veri atlama veya güven aralığı yoktur. MAD sıfırsa sıfır yayılım dönebilir; bu, bütün gözlemler aynı demek değildir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 21 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 22 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
