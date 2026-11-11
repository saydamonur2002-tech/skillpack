# Kaynak ve paketleme notu

## Kaynaklar

11 Kasım 2026'da okundu.

1. NWS Weather Prediction Center, *The Heat Index Equation*: https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml (sayfa son değişikliği 12 Mayıs 2022).
2. NWS Amarillo, *What is the heat index?*: https://www.weather.gov/ama/heatindex
3. NWS sorumluluk reddi: https://www.weather.gov/disclaimer — NWS web sayfalarındaki bilgi, aksi belirtilmedikçe kamu malıdır; NWS'nin adını onay ya da ortaklık izlenimi verecek biçimde kullanmak yasaktır. Bu paket NWS tarafından hazırlanmamış ve onaylanmamıştır.

| Kaynakta | Pakette |
|---|---|
| Basit formül: HI = 0,5 × {T + 61,0 + [(T − 68,0) × 1,2] + (RH × 0,094)}; sonuç T ile ortalanır | `basit` adımı |
| Ortalama 80 °F ya da üstündeyse tam denklem (Rothfusz regresyonu, dokuz katsayı) | `esik`, `tam_denklem` |
| RH < %13 ve T 80–112 °F: [(13 − RH)/4] × √{[17 − \|T − 95\|]/17} çıkarılır | `kuru_mu`, `kuru_duzeltme` |
| RH > %85 ve T 80–87 °F: [(RH − 85)/10] × [(87 − T)/5] eklenir | `nemli_mi`, `nemli_duzeltme` |
| Sınıflar: Caution 80–90 °F, Extreme Caution 90–103 °F, Danger 103–124 °F, Extreme Danger 125 °F ve üstü | `params`, `karar` |
| "Doğrudan güneşte ısı indeksi 15 °F'a kadar artabilir"; çizelge gölge içindir | `gunes_eki_f`, `gunes_ekle` |

## Paketleyenin yorumları

Bunlar kaynakta yazmaz; değiştirmek isteyen `flow.yaml` içinde değiştirir.

1. **Sınıf sınırları.** Kaynakta 90 °F iki sınıfta da geçer ve 124 ile 125 °F arası boştur. Paket alt sınırı dahil, üst sınırı hariç sayar: 80 ≤ dikkat < 90 ≤ çok dikkat < 103 ≤ tehlike < 125 ≤ aşırı tehlike.
2. **Düzeltme aralıklarının uçları.** "80 ile 112 arası" ve "80 ile 87 arası" uçlar dahil alınmıştır.
3. **Güneş.** Kaynak "15 °F'a kadar" der. Paket güneşte tam 15 °F ekler, yani en kötü durumu alır.
4. **Hüküm eşlemesi.** Yalnız "aşırı tehlike" sınıfı `stop` hükmüne bağlanmıştır; "tehlike" sınıfı `warn` kalır. NWS sınıfları işi durdurma kuralı değildir; çalışma düzeni için iş güvenliği mevzuatına bakılmalıdır.
5. **Türkçe sınıf adları ve mesajlar** paketleyenin çevirisidir.

## Sınırlar

- Kaynağa göre denklemin hatası ±1,3 °F'tır ve denklem, dayandığı verinin kapsamı dışındaki aşırı sıcaklık ve nem değerlerinde geçerli değildir. Paket girdiyi −10 ile 60 °C arasında kabul eder ama bu aralığın tamamında geçerlilik iddia etmez.
- Isı indeksi rüzgârı, giysiyi, iş yükünü ve kişinin sağlık durumunu hesaba katmaz.

## Doğrulama

NWS sayfasındaki iki örnek paketle yeniden hesaplandı: 100 °F ve %55 nem için 124 °F, 100 °F ve %15 nem için 96 °F. İkisi de kaynakla aynı çıktı.

## Onay

Bu paketi bir meteorolog ya da iş sağlığı uzmanı gözden geçirmemiştir.
