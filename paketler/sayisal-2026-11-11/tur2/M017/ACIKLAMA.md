# M017 — Üç köşegenli denklem sistemini çözme

## Ne işe yarar?

Yalnızca ana köşegen ve yanındaki iki köşegende katsayı bulunan doğrusal sistemleri çözer.

## Hangi girdileri alır?

Ana/alt/üst köşegen dizileri ve tek sağ taraf vektörü.

## Ne üretir?

Çözüm, eleme sırasındaki satır değiştirme kararları ve artık normu.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/OpenMathLib/OpenBLAS); sabit kaynak sürümü: `6c303de7bc061ccec5a417e3b419a0d5551e4ff6`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

1–512 bilinmeyen. Döngüsel köşe katsayıları ve genel bantlı matrisler desteklenmez. Sıfır pivot hata verir; koşulluluk veya çözüm doğruluğu sertifikası vermez.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 22 test vardır; teslim kaydı da 22 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
