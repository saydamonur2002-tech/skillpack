# M011 — Polinomun bir kökünü bulma

## Ne işe yarar?

Verilen aralıkta bir polinomun sıfır olduğu noktayı Brent yöntemiyle arar.

## Hangi girdileri alır?

Azalan derece sırasıyla polinom katsayıları, iki aralık ucu ve isteğe bağlı tolerans/tekrar sınırı.

## Ne üretir?

Bulunan kök, polinomun bu noktadaki değeri, tekrar sayısı ve değerlendirme sayısı.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/scipy/scipy); sabit kaynak sürümü: `92d2a8592782ee19a1161d0bf3fc2241ba78bb63`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

En çok 20. derece. Uçta tam sıfır bulunması dışında işaret değiştiren bir aralık gerekir. Bütün kökleri veya karmaşık kökleri bulmaz. Yaklaşımın bitmesi, tam sıfır veya sınırsız doğruluk garantisi değildir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 28 test vardır; teslim kaydı da 28 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
