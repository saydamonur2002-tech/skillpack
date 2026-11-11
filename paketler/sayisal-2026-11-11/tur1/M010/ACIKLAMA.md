# M010 — Bağlantı ağının Laplasyen tablosu

## Ne işe yarar?

Bir ağın ağırlıklı bağlantı tablosunu, bağlantı yapısını incelemede kullanılan Laplasyen tabloya çevirir. İki türden biri seçilir: birleşik tablo ya da normalleştirilmiş tablo.

## Hangi girdileri alır?

En çok 32 düğümlü, negatif olmayan kare bağlantı matrisi; isteğe bağlı normalleştirme türü.

## Ne üretir?

Kombinatoryal veya normalleştirilmiş graf Laplasyeni.

## Hangi kaynağa dayanır?

[Asıl proje](https://github.com/epfl-lts2/pygsp); sabit kaynak sürümü: `4716b12c470c579e3f477f2d1c1d99752c73252d`. Ayrıntılı kaynak kanıtları aynı modülün `SOURCE.md` ve `manifest.json` dosyalarındadır.

Lisans: **BSD-3-Clause**. Asıl `LICENSE`, `NOTICE` ve varsa `LICENSES/` içeriği korunmalıdır; bu açıklama onların yerine geçmez.

## Sınırları ve uyarıları

Yönlü bağlantıları ters yönleriyle ortalayarak simetrikleştirir; yön bilgisi kaybolur. Ağ öğrenmesi, özdeğer çözümü ve negatif bağlantı modeli içermez.

Bu bağımsız sayısal araç doğrudan makine kontrolü veya bağımsız güvenlik onayı değildir. `manifest.json` ile çalışan bir komut satırı ve stdio MCP aracıdır; ana deponun `skillpack.yaml` akış paketlerinden ayrıdır. SHA-256 bütünlüğü gösterir, imzalı yayıncı kimliği veya iptal kontrolü yerine geçmez.

## Test durumu

11 Kasım 2026’da bu depoda ilk grup yeniden çalıştırıldı: **261 test geçti**, hata ve atlama yok (Python 3.12). Bu modülün klasöründe 23 test vardır. Ortak MCP oturumuyla birlikte teslim kaydındaki sayı 24 olur. Grubun kalan iki testi, on saniyelik süre sınırı ve MCP’nin zaman aşımında işi durdurmasıdır.

Kaynak projenin tam test takımı ve özgün Fortran programı çalıştırılmaz.

`FILES.sha256` özgün dosyaların özetidir. Bu Türkçe açıklama o listenin parçası değildir.
