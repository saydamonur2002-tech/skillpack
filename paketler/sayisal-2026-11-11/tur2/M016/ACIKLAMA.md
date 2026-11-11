# M016 — Kare doğrusal denklem sistemini çözme

## Ne işe yarar?

Birbirine bağlı doğrusal denklemlerin bilinmeyenlerini, satır değiştirmeli LU yöntemiyle çözer.

## Hangi girdileri alır?

1–64 boyutlu gerçek kare katsayı matrisi ve tek sağ taraf vektörü.

## Ne üretir?

Çözüm vektörü, LU ayrıştırması, satır seçimi indeksleri, artık normu ve ölçeklenmiş geri hata.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/OpenMathLib/OpenBLAS); sabit kaynak sürümü: `6c303de7bc061ccec5a417e3b419a0d5551e4ff6`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Seyrek matris, çoklu sağ taraf veya en küçük kareler çözümü yoktur. Sıfır pivot hata verir. Küçük artık, kötü koşullu bir problemde doğruya çok yakın çözüm garantisi değildir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 23 test vardır; teslim kaydı da 23 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
