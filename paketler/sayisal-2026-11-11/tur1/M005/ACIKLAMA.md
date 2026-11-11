# M005 — Sabit pusula yönlü rota hesabı

## Ne işe yarar?

Küre üzerinde pusula yönü sabit tutulan bir rotanın mesafesini ve yönünü hesaplar.

## Hangi girdileri alır?

İki noktanın enlem/boylamı ve isteğe bağlı küre yarıçapı. Yarıçap verilmezse 6.371.000 metre kullanılır.

## Ne üretir?

Sabit yön açısı ve rota mesafesi.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/chrisveness/geodesy); sabit kaynak sürümü: `3e9fdd35b71dd86cee12383eccdf000ad6741e9d`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **MIT**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Genellikle en kısa rota değildir. Kutupları kabul etmez; elipsoit modeli veya manyetik sapma düzeltmesi yoktur. Seyir için kullanım onayı değildir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 23 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 24 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
