# Vizyon

## Tek cümle

**Ustanın tekniğini, mikro ölçekte, kod yazmadan bir makineye veya robota aktaran basit bir kurulum ve onun açık standardı.**

## Ne yapmıyoruz

- Yeni bir robot yapmıyoruz.
- Yeni bir dil modeli eğitmiyoruz. Model bir şey öğrenmez, sadece çevirir (LoRA veya damıtma ile beceri aktarımı yanlış kurgu olarak bırakıldı).
- Motor kontrolü, hareket planlama ve güvenlik katmanlarını yeniden yazmıyoruz. Bunlar makinenin kendi yazılımında kalır.

## Ne yapıyoruz

Var olan üç şeyi tek, sade bir standartta birleştiriyoruz:

| Katman | İçerik | Karşılık geldiği mevcut yapı | Durum |
|---|---|---|---|
| **Beceri** | Makinenin yapabildiği tekil işler (tart, kavra, kaldır) | OPC UA beceri modeli, PackML, davranış ağaçları | Var; uyumlanır, sınır çizilir |
| **Tarif** | Adım sırası, ön koşul, tehlike kuralı, doğrulama, yerel profil | ISA-88, MTP / POL | Var; uyumlanır, sınır çizilir |
| **Anlatım mekanizması** | Tekniğin ustadan çıkarılması ve modele anlatılması | AAS yetenek tanımı (yarım) | **Yok, asıl katkı burası** |

## Eksik olan taraf: anlatım mekanizması

1. **Ustadan çıkarma yöntemi:** Kod bilmeyen ustanın bilgisini adım, tehlike, doğrulama ve teste çeviren soru akışı (oyunlaştırılabilir; tuzak senaryoları teste dönüşür).
2. **Modele anlatma biçimi:** Her aracın amacı, ön koşulu, etkisi, donanımı ve mevcut durumu modelin okuyabileceği ortak biçimde.
3. **Tek kaynak:** Tarif, kılavuz ve testler aynı paketten üretilir, birbirinden kopmaz.
4. **Yerel değişiklik ve kanıt:** "Kutular artık 25 kg" gibi değişiklik onayla, testle, kayıtla yapılır; sonuç ölçümle kanıtlanır.

## Mimari

```
İnsan ⇄ Yerel LLM (32B, yerel sunucu; telefonda küçük yardımcı) ⇄ MCP ⇄ DİKEY TEKNİK PAKETİ ⇄ Uygulamalar / makineler
```

Paket önce uygulama gibi **kurulur** (imza, şema, test, donanım arayüzü, profil kontrolü); MCP ancak ondan sonra paketi modele araç olarak açar.

## Modüler uygulama ve tekniğin yayılması

- **Modüler:** Çekirdek sabit; teknik paketleri ve donanım bağlayıcıları takılıp çıkarılır.
- **Serbestleşme ve çoğalma:** İmzalı paket kopyalanabilir, paylaşılabilir, başka işletme kendi profiliyle uyarlar. Ustanın emeği "yazan / onaylayan" kaydıyla görünür kalır.
- **Ticarileşme:** Standart açık kalır; üzerinde paketleme, kurulum ve onay hizmetleri başkaları tarafından yapılabilir.

## Doğabilecek iş kolu

- **Teknik paketleyici:** Ustayla oturup tekniği pakete çeviren kişi.
- **Yerel kurulumcu:** Sensör, makine ve sunucuyu bağlayan entegratör.
- **Paket deposu / onay hizmeti:** İmza, test ve iptal listesi.

## Bu deponun rolü

Bu depo ticari değildir. Rolü açık standardı ve ücretsiz referans uygulamayı koymaktır. Ticarileşme, isteyen başkaları tarafından bu standart üzerinde yapılır.

## Dürüst durum

- Şablon ve örnek paket taslaktır; gerçek usta onayı yoktur.
- Ustadan çıkarma yöntemi (soru akışı) sahada denenmedi.
- Referans çalıştırıcı yeni biçimin tüm alanlarını henüz uygulamıyor.
