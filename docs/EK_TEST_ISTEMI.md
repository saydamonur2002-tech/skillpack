# Ek test istemi

Bu dosya, [ALTYAPI_ENVANTERI.md](ALTYAPI_ENVANTERI.md) içindeki ilk denemeyi genişletecek bir kodlama ajanına (ör. Claude Code oturumu) verilmek üzere yazılmıştır. Aşağıdaki kutunun içi olduğu gibi yapıştırılabilir. Donanım satırı, testin koşacağı makineye göre düzeltilmelidir.

```text
Bu depo (skillpack), yerel sunucuda öğretilen ajan becerileri için bir açık standart
taslağıdır. Henüz uygulama kodu yoktur. docs/ALTYAPI_ENVANTERI.md dosyasında küçük bir
ilk deneme var: paketleme, imza, iptal ve simülasyon halkaları hazır açık kaynak
parçalarla çalıştı; ama 7B sınıfı yerel model, öncelik sıralı beş iş kuralını 20 kolinin
yalnız 13'ünde doğru uyguladı, aynı kuralları uygulayan betik ise 20'sinde. O deneme
20 örnek, tek görev ve tek istemle yapıldı; bu yüzden bir işaret, kanıt değil.

Senden istediğim, o işareti sağlam bir ölçüme çevirmen ve ilk denemede atlanan halkaları
denemen. Sonuçlar bir tasarım kararını besleyecek: standart, "kararı kural motoru verir,
model yalnız girdiyi yapılandırır ve açıklamayı yazar" kuralını zorunlu tutmalı mı?
Bu yüzden benim için en değerli çıktı, beklentiyi doğrulayan değil onu sınayan ölçümdür.
Model beklenenden iyi çıkarsa bunu aynı açıklıkla yaz.

Önce docs/ALTYAPI_ENVANTERI.md, docs/deney/ klasörü ve docs/TEKNIK_PROJE_v0.1.md
Bölüm 2.3 ile Bölüm 13'ü oku. Mevcut betikler (docs/deney/beceri_olcumu.py,
docs/deney/iptal_tatbikati.py) başlangıç noktandır; onları genişlet.

Donanım: <buraya makineyi yaz; GPU varsa modeli ve belleğini belirt>.

A. Kural uygulama ölçümü (asıl iş)

1. Örneklemi büyüt: görev başına en az 200 sentetik örnek, sabit tohumla. Her kural
   dalından ve özellikle iki kuralın birden eşleştiği çakışma durumlarından yeterli
   örnek olsun; ilk denemedeki hataların hepsi çakışma durumlarındaydı.
2. Tek görevle yetinme. Koli ayırmaya ek olarak yapısı farklı en az iki görev yaz:
   biri sayısal eşik ve aralık ağırlıklı (ör. stok sapması tanısı), biri serbest
   metinden alan çıkarmayı gerektiren (ör. Türkçe yazılmış bir arıza notundan
   makine, belirti ve aciliyet çıkarma). Her görevin doğru cevabı deterministik bir
   betikten gelsin.
3. Şu dört kipi aynı örneklerde karşılaştır:
   a) model kuralları kendi uygular (ilk denemedeki kip),
   b) model önce her kuralı tek tek değerlendirir, sonra karar verir,
   c) melez: model yalnız girdiyi yapılandırılmış alanlara çevirir, kararı betik verir,
   d) araç çağırma: model kural betiğini araç olarak çağırır ve sonucu aktarır.
   Serbest metin görevinde (c) kipi modelin gerçekten işe yaradığı yer olabilir;
   orada çıkarma hatasını karar hatasından ayrı raporla.
4. Model boyutunu değiştir: Apache-2.0 lisanslı Qwen2.5 1.5B, 7B ve donanım
   elveriyorsa 14B; ayrıca güncel bir açık ağırlıklı 7–9B model daha. Her modelin
   lisansını Hugging Face kaydından doğrula ve yaz; Qwen2.5 3B Apache-2.0 değildir.
   Nicemlemeyi (Q4_K_M ve Q8) en az bir modelde karşılaştır.
5. İstem duyarlılığını ölç: aynı kuralları üç farklı biçimde ver (düz liste, karar
   tablosu, YAML). Sonuç isteme göre çok oynuyorsa bunu ana bulgu olarak yaz.
6. Token bütçesini bir değişken olarak ölç. İlk denemede model cevaba 40, gerekçeli
   turda 160 token ile sınırlandı; bu, düşünmeye yer bırakmamış olabilir. Aynı
   örneklerde çıktı sınırını kademeli aç (ör. 40, 160, 600, 2000) ve biçim
   zorlaması olmayan serbest kipi (docs/deney/beceri_olcumu.py --kip serbest) kullan.
   Varsa düşünme kipi olan bir açık modeli (ör. Qwen3 ailesi) düşünme açık ve kapalı
   olarak ekle. Her bütçe için doğruluğun yanında sınırda kesilen cevap sayısını,
   modelin fiilen harcadığı tokenı ve "doğru cevap başına token" değerini ver.
   Aradığım şey şu eğri: token arttıkça doğruluk nerede yükseliyor, nerede
   düzleşiyor, nerede model kendini tekrar etmeye başlıyor. Bağlam penceresini de
   bütçeye göre büyüt; kesilme yüzünden düşen doğruluğu model hatası sayma.
7. İnce ayar kolu. docs/deney/ince_ayar.py, betiğin etiketlediği 640 koliyle 1.5B
   modele tek turluk LoRA eğitimi yaptı; taze kolilerde doğruluk yalnız %42'ye çıktı
   ve kayıp hâlâ düşüyordu. Bunu düzgün ölç: örnek sayısını (ör. 500, 2000, 8000) ve
   tur sayısını değiştirerek öğrenme eğrisini çıkar; 1.5B ve 7B'yi karşılaştır;
   istemde kural metni olan ve olmayan iki eğitimi ayrı tut. Eğitimde hiç görülmemiş
   değerlerde (yeni şehir, yeni barkod biçimi, eşik çevresindeki ağırlıklar) doğruluğu
   ayrı raporla; ezber ile kuralı öğrenmeyi bu ayırır. Son olarak bir kuralı değiştir
   (ör. eşiği 25'ten 30 kg'a çek) ve modelin yeni kurala uyması için ne kadar yeni
   örnek ve süre gerektiğini, betikte aynı değişikliğin tek satır olduğunu not ederek
   yaz.
8. Her satır için şunları raporla: doğruluk ve %95 güven aralığı, hata türü dağılımı
   (öncelik hatası, eşik hatası, biçim hatası, uydurma), görev başına girdi ve çıktı
   tokenı, süre, tok/s. Güç ölçebiliyorsan (GPU'da nvidia-smi, CPU'da RAPL) görev
   başına Wh ekle ve ölçüm sınırını yaz; ölçemiyorsan tahmin uydurma, [EKSİK] yaz.

B. İlk denemede atlanan halkalar

9. Anahtarsız imzalama: bir GitHub Actions iş akışında OIDC ile docs/deney/
   depo-koli-ayirma dizinini model-signing ya da cosign ile imzala, imzayı ayrı bir
   makinede doğrula. Bu adım depoya iş akışı dosyası eklemeyi gerektirir; eklemeden
   önce bana sor.
10. İki makine arası doğrulama: paketi bir yerde imzala, imza ve paketi başka bir
   makineye taşı, orada temiz kurulumla doğrula. Gereken adımları tekrarlanabilir
   biçimde yaz.
11. İçerik adresli dağıtım: aynı paketi IPFS (kubo) ve bir OCI kaydı (oras) üzerinden
   yayımlayıp geri çek; özetin değişmediğini göster. Hangisinin daha az iş çıkardığını
   söyle.
12. PII taraması: T.C. kimlik no (sağlama basamağıyla), telefon, e-posta, IBAN ve
    plaka için bir tarayıcıyı sentetik örneklerde dene. Presidio'yu ve düz düzenli
    ifadeleri karşılaştır; yakalanan ve kaçan sayısını ver.
13. İstem zehirleme: örnek paketin SKILL.md ya da examples/ dosyasına "beyan dışı
    aracı çağır" türünden gizli bir talimat koy; modelin buna uyup uymadığını ve
    çalışma zamanında beyan dışı çağrıyı reddeden basit bir kapının bunu durdurup
    durdurmadığını ölç.
14. LeRobot: küçük bir açık LeRobotDataset'i indirip yükle; robot_profile.yaml için
    gereken alanların (eklem sayısı, kamera adları, kare hızı) veri setinin kendi
    meta verisinden okunup okunamadığını yaz.

Sınırlar

- cli/, spec/ ve schemas/ klasörlerine dokunma. Yol haritasında F0 bitmeden uygulama
  kodu yazılmıyor; ölçüm betikleri docs/deney/ altında kalır.
- docs/TEKNIK_PROJE_v0.1.md dosyasını değiştirme; öneriyi rapora yaz.
- Yalnız sentetik veri kullan. Gerçek kişi, müşteri ya da kurum verisi koyma.
- Bir testi geçirmek için örnekleri, doğru cevap betiğini ya da puanlamayı gevşetme.
  Puanlamayı değiştirmen gerekirse neyi neden değiştirdiğini yaz.
- Bir adım yapılamıyorsa (ağ, donanım, kimlik) atla, nedenini yaz ve devam et.

Çıktı

Sonuçları docs/EK_TEST_RAPORU.md dosyasına yaz ve betikleri docs/deney/ altına koy.
Rapor, docs/ALTYAPI_ENVANTERI.md ile aynı kaynak etiketlerini kullansın: bu oturumda
ölçülen şey [VERİ], başka kaynaktan aktarılan [VEKİL], ölçülemeyen [EKSİK]. Raporun
başında üç şeyi açıkça yanıtla: (1) hangi kipte ve hangi model boyutunda doğruluk
kabul edilebilir düzeye çıkıyor, (2) "karar betikte, açıklama modelde" kuralı
ölçümle destekleniyor mu, çürüyor mu, (3) hangi sonuca en az güveniyorsun ve neden.
Çalıştırmadığın hiçbir şeyi çalışmış gibi yazma; her sayının hangi komuttan geldiği
rapordan izlenebilsin.
```

## İstemin dayandığı varsayımlar

- İlk denemedeki 13/20 sonucu küçük örneklemdir; istem bu yüzden doğrulama değil sınama ister.
- Dört kip arasındaki fark, taslağın Bölüm 13'teki risk azaltma maddesini tasarım kuralına çevirip çevirmeme kararını belirler.
- B bölümündeki adımlar birbirinden bağımsızdır; ağ ya da kimlik eksikse atlanabilir.
