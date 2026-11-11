# Kaynak ve paketleme notu

## Kaynak

Waters, T. R., Putz-Anderson, V., Garg, A. *Applications Manual for the Revised NIOSH Lifting Equation.* DHHS (NIOSH) Publication No. 94-110, Ocak 1994. CDC Stacks kaydı: https://stacks.cdc.gov/view/cdc/5434 (kayıtta "Public Domain" işaretli). 11 Kasım 2026'da okundu.

Pakete alınan bölümler:

| Kılavuzda | Pakette |
|---|---|
| Bölüm 1.3: RWL = LC × HM × VM × DM × AM × FM × CM; LC = 23 kg | `params.lc_kg`, `sinir` adımı |
| HM = 25/H; H ≤ 25 cm ise 1,0; H > 63 cm ise 0 | `carpanlar` adımı, ilk tehlike kuralı |
| VM = 1 − 0,003·\|V − 75\|; V > 175 cm ise 0 | `carpanlar` adımı, ikinci tehlike kuralı |
| DM = 0,82 + 4,5/D; D < 25 cm ise 25 cm; D en çok 175 cm | `carpanlar` adımı, `d_cm` üst sınırı |
| AM = 1 − 0,0032·A; A > 135° ise 0 | `carpanlar` adımı, üçüncü tehlike kuralı |
| Tablo 5: sıklık çarpanı (18 satır × 6 sütun) | altı `fm_*` tablosu |
| Tablo 7: kavrama çarpanı | `cm_alt`, `cm_ust` |
| Bölüm 1.4: LI = yük / RWL; LI > 1,0 bir bölüm çalışan için artan risk; LI > 3,0 hemen hemen bütün çalışanlar için artan risk | `karar` adımı |

## Kılavuzdan sapmalar

1. **Sıklıkta ara değer yok.** Kılavuz, tablodaki iki satır arasına düşen sıklık için doğrusal ara değer ister. Akış profili ara değer hesabı taşımadığı için paket yalnız tablodaki satırları kabul eder ve kullanıcıdan bir üstteki satırı seçmesini ister. Sonuç kılavuzdakinden küçük ya da ona eşit bir sınır verir (temkinli taraf).
2. **Tek nokta.** Kılavuz, varışta denetim gerekiyorsa sınırı hem başlangıçta hem varışta hesaplayıp küçüğünü alır. Paket tek bir noktayı değerlendirir; iki nokta için iki kez çalıştırılır.
3. **Tek görev.** Çok görevli işler için bileşik kaldırma indeksi (CLI) pakette yoktur.
4. **Süre sınıfı kullanıcıdan alınır.** Kılavuz süre sınıfını çalışma ve dinlenme sürelerinin oranından çıkarır. 2021 baskısı bu oranda bir düzeltme yapmıştır (1,2 yerine 1,0); o baskının tam metni bu derlemede okunamadı. Formüller ve çarpanlar iki baskıda aynıdır (CDC Stacks kaydı 110725).
5. **Sonuç eşlemesi.** "Uygun / riskli / çok riskli" adları ve mesajların Türkçe metni paketleyene aittir; eşikler (1,0 ve 3,0) kılavuzdandır.

## Kılavuzun örnekleriyle karşılaştırma

Kılavuzun örnekleri inç ve libreyle çözülmüştür. Paket metrik formülü kullanır; 25 cm ile 10 inç (25,4 cm) aynı olmadığı için metrik sınır yaklaşık %3–4 daha küçük çıkar.

| Örnek | Kılavuz RWL | Paket RWL | Kılavuz LI | Paket LI |
|---|---|---|---|---|
| Örnek 1 başlangıç (pres makarası) | 16.3 lb (7.39 kg) | 7.13 kg | 2.7 | 2.8 |
| Örnek 1 varış | 14.5 lb (6.58 kg) | 6.28 kg | 3.0 | 3.18 |
| Örnek 2 başlangıç (kâğıt rulosu) | 28.0 lb (12.7 kg) | 12.31 kg | 1.3 | 1.29 |
| Örnek 2 varış | 18.1 lb (8.21 kg) | 8.01 kg | 1.9 | 1.98 |
| Örnek 3 başlangıç (torba, 45 derece dönüş) | 18.9 lb (8.57 kg) | 8.23 kg | 2.1 | 2.2 |

Beş örneğin beşinde de paket, kılavuzla aynı risk sınıfına varır.

## Onay

Bu paketi bir iş güvenliği uzmanı ya da ergonomist gözden geçirmemiştir. Sayılar kaynaktan aktarılmıştır; sahada kullanmadan önce yetkin bir kişi tarafından denetlenmelidir. Denklem tek kişiyle, iki elle, sarsmadan yapılan kaldırmalar içindir; kılavuzun Bölüm 1.2'deki diğer kısıtları geçerlidir.
