# M012 — Sınırlı aralıkta integral tahmini

## Ne işe yarar?

Listeden seçilen düzgün bir fonksiyonun (polinom, sinüs, kosinüs, üstel fonksiyon veya Bessel hesabında kullanılan hazır eğri) iki sınır arasındaki integralini, aralığı bölmeden tek hesap paneliyle yaklaşık bulur.

## Hangi girdileri alır?

Polinom, sinüs, kosinüs, üstel fonksiyon veya Bessel hesabında kullanılan hazır eğri; alt ve üst sınırlar ile gereken katsayılar.

## Ne üretir?

İntegral tahmini, mutlak hata tahmini, daha kaba olan Gauss-10 tahmini, yardımcı büyüklükler ve fonksiyonun kaç kez hesaplandığı.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/scipy/scipy); sabit kaynak sürümü: `92d2a8592782ee19a1161d0bf3fc2241ba78bb63`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Tek 21 noktalı Gauss–Kronrod paneli kullanır; aralığı otomatik bölmez. Sonsuz aralık veya tekillik çözümü yoktur. Hata tahmini dar özellikleri kaçırabilir. Açısal fonksiyonlarda radyan kullanılır.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 29 test vardır; teslim kaydı da 29 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
