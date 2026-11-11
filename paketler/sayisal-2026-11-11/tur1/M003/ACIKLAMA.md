# M003 — Dünya elipsoidi üzerinde mesafe

## Ne işe yarar?

İki koordinat arasındaki yüzey mesafesini ve başlangıç/bitiş yönlerini WGS84 Dünya modeliyle hesaplar.

## Hangi girdileri alır?

İki noktanın enlem ve boylamı; ondalık derece olarak.

## Ne üretir?

Metre cinsinden mesafe ve başlangıç/bitiş yön açıları.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/chrisveness/geodesy); sabit kaynak sürümü: `3e9fdd35b71dd86cee12383eccdf000ad6741e9d`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **MIT**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Yükseklik ve farklı koordinat sistemine dönüşüm içermez. Dünyanın neredeyse karşı tarafındaki noktalar için yöntem yakınsamayabilir; bu durumda başka bir sonucu doğruymuş gibi vermek yerine hata döndürür.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 39 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 40 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
