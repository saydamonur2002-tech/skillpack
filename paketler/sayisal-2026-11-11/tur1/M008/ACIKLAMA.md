# M008 — Sinyali kaba yapı ve ayrıntıya ayırma

## Ne işe yarar?

Bir sayı dizisini Haar yöntemiyle yavaş değişen ana parça ve ayrıntı parçasına ayırır, ardından yeniden oluşturur.

## Hangi girdileri alır?

Uzunluğu çift olan, 2–4096 elemanlı gerçek sayı dizisi.

## Ne üretir?

Yaklaşım/ayrıntı katsayıları, düşük/yüksek frekans bileşenleri ve yeniden oluşturulan dizi.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/PyWavelets/pywt); sabit kaynak sürümü: `7b9e57ed639e7f87490a5bcb31f7b6c088d19031`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **MIT**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Tek seviyelidir. Otomatik gürültü temizleme veya eşik seçimi yapmaz; tek uzunluk, karmaşık sayı ve otomatik kenar doldurma desteklemez.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 19 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 20 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
