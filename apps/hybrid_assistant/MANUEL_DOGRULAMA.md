# Telefonda kısa kontrol (0.2.0)

Uygulamayı silmeden üstüne kur. Ana ekran açıkken:

1. Pil yüzdesi, şarj türü (AC / USB / kablosuz), pil sıcaklığı °C ve güç tasarrufu kartlarda görünür.
2. Durum satırında boş / toplam depolama yazar.
3. Sistem sağlığı kutusunda ısı durumu ve bellek kullanım yüzdesi görünür.
4. **Durumu yenile** ölçümü ve yerel kuralı yeniden çalıştırır. Logda `kural:`, kısıt varsa `kısıt:`, yedek varsa `yedek:` satırı vardır.
5. Isı orta ve üzeri, pil 40 °C ve üzeri, güç tasarrufu, pil %20 altı ve şarj yok, ya da düşük bellek varken `bunu neden yaptın` buluta gitmez.
6. Bu koşullar yokken aynı cümle onay sorar. Onaydan sonra buluta yalnız sayılar gider.
7. Öneri düğmeleri güç tasarrufu, ekran veya depolama ayarını açar. Sayfa yoksa uygulama kapanmaz, "Bu telefonda bu sayfa yok" der.
