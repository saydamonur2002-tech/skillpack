# Ustadan pakete: bir tekniği nasıl pakete çevirirsin

Bu belge yöntemi anlatır. Biçimin kuralları [spec/SKILLPACK_v0.1.md](../spec/SKILLPACK_v0.1.md) içindedir. Üç çalışan örnek [examples/](../examples/) altındadır: fabrika (rulman kontrolü), lokanta (mal kabul), okul (kazanım telafi kararı).

## Kim ne yapar

| Rol | İşi |
|---|---|
| Usta | Tekniği bilir. Kuralları ve sayıları onaylar. |
| Paketleyen | Ustayı izler, akışı yazar, testleri kurar. Usta ile aynı kişi olabilir. |
| Çalıştırıcı | Akışı yürütür. Karar buradadır. |
| Yerel model | Cümleden paketi seçer, söylenen değerleri çıkarır. Karar vermez. |

## Hangi teknik pakete girer

Girer: sonucu "evet / hayır / dikkat / dur" ya da "sıradaki adım şu" olan, gözleme ve eşiğe dayanan işler. Vardiya başı kontrolü, arıza ön teşhisi, mal kabul, kalite kontrol, bir ölçme sonucuna göre ne yapılacağına karar verme.

Girmez: el becerisi (kaynak dikişi, hamur açma), yaratıcı iş (menü tasarlamak, ders planı yazmak) ve her seferinde farklı muhakeme isteyen işler. Bunları pakete zorlamak, kötü çalışan bir paket üretir.

## Yedi adım

### 1. Tek bir karar seç

"Motor bakımı" bir teknik değil, yüz tekniktir. "Vardiya başında rulman çalışmaya uygun mu" tek bir karardır. Paket tek bir karara cevap verir.

### 2. İzle, sorma

Ustaya "nasıl yapıyorsun" diye sorarsan ders kitabı cevabı alırsın. İş yaparken izle ve üç şeyi not et: neye baktı, ne ölçtü, sonra ne yaptı. Anlattığı ile yaptığı ayrışırsa doğru olan yaptığıdır.

### 3. Dört sütunu doldur

| Gözlem | Eşik | Karar | Eylem |
|---|---|---|---|
| Rulman sıcaklığı − ortam sıcaklığı | 40 °C ve üstü | Dur | Bakımı çağır |
| Ürünün iç sıcaklığı | Sınırın 2 °C üstüne kadar | Şartlı kabul | Hemen soğut, bugün kullan |
| Doğru yapan / cevaplayan | %50'nin altı | Yeniden öğret | Konuyu sınıfça yeniden işle |

Dolduramadığın hücre, tekniğin henüz anlaşılmamış yeridir. Oraya dönüp ustayı yeniden izle.

### 4. Her sıfatı ölçüme bağla

"Fazla ısınmış", "bayat görünüyor", "çoğu yapamadı" pakete giremez. Her biri şu üçünden birine çevrilir:

- **Sayı:** "kaç derece", "kaç öğrenci". Nasıl ölçüleceğini `hint` alanına yaz.
- **Evet/hayır:** "normalden farklı ses var mı".
- **Seçenek:** "en sık hata hangisi: kavram yanılgısı, işlem hatası, soru anlaşılmadı, belirgin değil".

Çevrilemeyen gözlem insana bırakılır: akış soruyu sorar, cevabı insan verir. İnsan da bilmiyorsa akış "ustaya sor" sonucuna gider. Paket hiçbir zaman tahmin yürütmez.

### 5. Akışı yaz

`skillpack init <ad>` bir iskelet üretir. `flow.yaml` içinde:

- Ustanın sayılarını `params` altına koy. Kural ifadesine sayı gömme.
- En tehlikeli durumu ilk kurala yaz. Kurallar sırayla denenir; "dur" koşulu "dikkat" koşulundan önce gelmelidir.
- Her `decide` bir `else` ile biter. `else` dalını bilerek doldur: "hiçbiri değilse ne olur".
- Sonuç mesajını ustanın ağzıyla yaz. Kullanıcı bu metni olduğu gibi görür; model onu yeniden yazmaz.
- Mesajda ölçülen değeri göster (`{core_temp_c}`), yalnız hükmü değil. Kullanıcı neden o sonuca varıldığını görmelidir.

### 6. Ustanın vakalarıyla sına

`tests/cases.yaml` içine ustanın geçmişte karşılaştığı durumları yaz (adları, tarihleri, müşteri bilgisini çıkararak) ve her biri için ustanın o gün ne yaptığını `expect` alanına koy.

Mutlaka bulunması gerekenler:

- Her sonuç için en az bir vaka.
- Her eşik için **tam sınırda** bir vaka. "4 °C sınır" dendiğinde 4,0 kabul mü, ret mi? Ustalar bu soruya çoğu zaman ilk kez testte cevap verir.
- Bir "cevap yok" vakası.

`skillpack test <paket>` vakaları koşar. Kural ile ustanın yaptığı ayrışıyorsa ya kural eksiktir ya da ustanın söylemediği bir istisna vardır. İkisi de değerlidir.

### 7. Onaylat, imzala

Kuralları ustaya düz cümleyle geri oku. "Evet, ben böyle yaparım" dediğinde `provenance/approvals.json` dosyasına onayı yaz. Sonra:

```bash
skillpack keygen --out ~/usta.key --trust trust/     # bir kez
skillpack sign <paket> --key ~/usta.key
```

`sign`, doğrulamadan ya da testlerden geçmeyen paketi imzalamaz. İmzadan sonra pakette tek bir bayt değişirse çalıştırıcı paketi yüklemez.

## Sık yapılan hatalar

- **Çok geniş paket.** Beş kararı tek akışa sıkıştırmak. Beş paket yaz.
- **Modele iş bırakmak.** "Model duruma göre yorumlasın" dediğin her yer, belirlenimciliği kaybettiğin yerdir. Yorum gerekiyorsa o adım insana sorulur.
- **Sınırı sınamamak.** Hataların çoğu `>` ile `>=` arasındadır.
- **Eşiği başka yerden kopyalamak.** Örnek paketlerdeki sayılar örnektir. Gıda sıcaklığı, makine titreşimi gibi değerler işletmenin kendi planından ve ustanın kendisinden gelir.
- **Gerçek kişi verisi koymak.** Öğrenci adı, müşteri adı, telefon pakete girmez. Akış bunları sormaz; testler sentetiktir.
