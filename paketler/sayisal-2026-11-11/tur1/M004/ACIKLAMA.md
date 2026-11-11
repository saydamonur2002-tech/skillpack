# M004 — Küre üzerinde kısa yüzey yolu

## Ne işe yarar?

Dünyayı küre kabul ederek iki koordinat arasındaki büyük çember mesafesini ve yönleri hesaplar.

## Hangi girdileri alır?

İki noktanın enlem/boylamı ve isteğe bağlı küre yarıçapı; varsayılan yarıçap 6.371.000 metre.

## Ne üretir?

Merkez açısı, yüzey mesafesi ve başlangıç/bitiş yön açıları.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/chrisveness/geodesy); sabit kaynak sürümü: `3e9fdd35b71dd86cee12383eccdf000ad6741e9d`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **MIT**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Gerçek Dünya elipsoidi yerine küresel yaklaşım kullanır. Arazi, yol ağı veya canlı navigasyon sağlamaz. Aynı ya da tam karşıt noktaların tanımsız yönleri boş değer olarak döner.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 21 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 22 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
