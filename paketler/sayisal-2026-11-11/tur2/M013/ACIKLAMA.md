# M013 — Doğrusal sistemin zamanla ilerlemesi

## Ne işe yarar?

Doğrusal bir sistemin başlangıç durumundan belirli bir sonraki zamandaki durumunu sayısal olarak hesaplar.

## Hangi girdileri alır?

Sistemi tanımlayan matris, başlangıç durumu, isteğe bağlı sabit etki, başlangıç/bitiş zamanı ve adım sayısı.

## Ne üretir?

Son durum, son adımın ham hata göstergesi ve zaman adımıyla ölçeklenmiş yerel durum hata göstergesi.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit); sabit kaynak sürümü: `3cf0a0a8ba2abf8bc4995c6da5b6abae07b45a0a`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Yalnızca 1–8 boyutlu, zamandan bağımsız doğrusal/sabit etkili sistemler; en çok 10.000 sabit adım. Otomatik adım ayarı, katı sistem çözümü veya toplam hata garantisi yoktur. Birimler tutarlı olmalıdır; ham gösterge doğrudan durum hatası değildir.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ikinci grup yeniden çalıştırıldı: **324 test geçti**, hata ve atlama yok (Python 3.12; GCC ile yerel C kontrolleri de geçti). Bu modülün klasöründe 23 test vardır; teslim kaydı da 23 testtir. Grubun ek 32 testi modüllerin MCP oturumları, süre sınırı, yerel C kontrolü ve yayın denetimidir.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
