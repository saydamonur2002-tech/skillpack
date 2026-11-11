# M009 — Piksel ağırlık merkezini bulma

## Ne işe yarar?

Bir görüntünün sayısal piksel değerlerinden ağırlık merkezini bulur; seçilen pikseller dışarıda bırakılabilir.

## Hangi girdileri alır?

Dikdörtgen piksel değerleri tablosu ve isteğe bağlı dışlama maskesi.

## Ne üretir?

Merkezin sütun (x) ve satır (y) konumu ile hesaba katılan piksel değerleri toplamı.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/astropy/photutils); sabit kaynak sürümü: `0eb74eb4bc450c3d1476d26b774c0011c138bf49`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Görüntü dosyasını açmaz; sayısal tablo ister. En çok 64×64 piksel. Nesne tanıma, arka plan ayırma veya bölümleme yapmaz. Negatif değerler merkezi görüntünün dışına taşıyabilir; toplam mutlak değeri 1e-30 altında ise hata verir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 34 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 35 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
