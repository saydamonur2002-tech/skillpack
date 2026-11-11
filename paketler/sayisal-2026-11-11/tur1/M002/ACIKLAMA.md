# M002 — Düzensiz ölçümlerden türev hesabı

## Ne işe yarar?

Eşit aralıklı olmayan ölçüm noktalarında değişim hızını hesaplamak için gereken ağırlıkları üretir. Ölçüm değerleri de verilirse bu ağırlıklarla tek bir türev tahmini verir.

## Hangi girdileri alır?

Birbirinden farklı ölçüm konumları; isteğe bağlı hesap noktası, türev derecesi ve ölçüm değerleri.

## Ne üretir?

İstenen dereceye kadarki türev ağırlıkları; ölçüm değerleri verilirse türev tahmini.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/pbrod/numdifftools); sabit kaynak sürümü: `54ba279ca9915cbd4fa07ccb2f959b82815950f1`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

En çok 25 nokta ve 0–8 türev derecesi; derece nokta sayısından küçük olmalıdır. Birbirine çok yakın noktalar gürültü ve yuvarlama hatasını büyütür. Güvenilir hata sınırı vermez.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 27 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 28 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
