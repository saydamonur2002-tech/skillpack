# Yol haritası

Süreler göreli aylarla verilmiştir (A0 = başlangıç). Gönüllü veya hibe destekli bir ekibin hızı bilinmediği için tüm süreler **[VARSAYIM]** niteliğindedir. Kaynak: teknik taslak Bölüm 10–12 ve 14, [docs/TEKNIK_PROJE_v0.1.md](docs/TEKNIK_PROJE_v0.1.md).

Her fazın durumu bu belgede ve ilgili GitHub issue'sunda tutulur. Görev kutuları işlendikçe işaretlenir.

## Durum özeti

| Faz | Süre | Amaç (kısa) | Durum |
|---|---|---|---|
| [F0 — Hazırlık](#f0--hazırlık-a0a2) | A0–A2 | Taslağı yayımlamak, geri bildirim ve hukuki ön görüş almak | ⬜ Başlamadı |
| [F1 — Çekirdek](#f1--çekirdek-a2a6) | A2–A6 | Şemalar, doğrulayıcı CLI, imza ve iki dijital örnek paket | ⬜ Başlamadı |
| [F2 — Yerel çalışma](#f2--yerel-çalışma-a5a9) | A5–A9 | Yerel depo, yönlendirici, telefon istemcisi, öğretme döngüsü | ⬜ Başlamadı |
| [F3 — Fiziksel profil](#f3--fiziksel-profil-a8a12) | A8–A12 | Robot profili, LeRobotDataset, koli ayırma simülasyonu | ⬜ Başlamadı |
| [F4 — Dağıtım ve iptal](#f4--dağıtım-ve-iptal-a10a14) | A10–A14 | Aynalar, IPFS, iptal listesi, TUF, iptal tatbikatı | ⬜ Başlamadı |
| [F5 — Pilot](#f5--pilot-a12a18) | A12–A18 | 2–3 gönüllü saha, Bölüm 12 ölçümleri | ⬜ Başlamadı |
| [F6 — Yönetişim](#f6--yönetişim-a12a24) | A12–A24 | AAIF çalışma grubu önerisi, spesifikasyon v1.0 adayı | ⬜ Başlamadı |

---

## F0 — Hazırlık (A0–A2)

**Durum:** ⬜ Başlamadı

**Amaç:** Spesifikasyon taslağı v0.1'i yayımlamak, geri bildirim çağırmak ve kamu görevlisi statüsü için yazılı hukuki ön görüş almak. Uygulama kodu bu fazda hedef değildir; kurallar ve izin netleşmeden F1'e geçilmez.

### Görevler

Hukuki ön görüş (Bölüm 14):

- [ ] Personel birimine gidecek yazılı görüş talebi dilekçesini hazırlamak
- [ ] Avukat için kısa brifing notu yazmak (projenin ticari olmadığı, mesai dışı / kurum kaynağı kullanılmadan yürütüleceği, FSEK kapsamında eser katkısı olduğu)
- [ ] Bağlı olunan kurumun personel biriminden yazılı görüş almak
- [ ] Bağımsız bir avukattan yazılı hukuki görüş almak
- [ ] Görüş sonuçlarını bu depoya ticari sır veya kurum bilgisi koymadan, yalnızca izin verilen özetle kaydetmek

Spesifikasyon taslağı v0.1:

- [ ] `spec/` altında skillpack v0.1 taslağını yazmak (tasarım ilkeleri, klasör yapısı, `SKILL.md` uzantısı, `skillpack.yaml` alanları)
- [ ] Agent Skills ile geriye uyumluluk kurallarını açıkça belgelemek (yalnız `SKILL.md` okuyan bir ajanın paketi kullanabilmesi)
- [ ] Sürümleme, izin beyanları, gizlilik kuralları ve köken/lisans alanlarını taslakta tanımlamak
- [ ] Kod için Apache-2.0, spesifikasyon metni ve veri için CC-BY-4.0 notunu netleştirmek
- [ ] Taslağı bu depoda yayımlamak ve sürüm etiketini (`v0.1-taslak`) kararlaştırmak

Geri bildirim:

- [ ] Kısa bir geri bildirim çağrısı metni yayımlamak (ne istendiği, nereye yazılacağı)
- [ ] En az bir dış teknik uzmandan inceleme veya yazılı yorum almak
- [ ] Açık soruları izleme listesine almak (Agent Skills kapsamı, şeffaflık günlüğü işletimi, memur katkısı çerçevesi vb.; teknik taslak Bölüm 13)

### Çıkış ölçütü

En az bir dış teknik inceleme alınmıştır; yazılı hukuki görüş alınmıştır.

---

## F1 — Çekirdek (A2–A6)

**Durum:** ⬜ Başlamadı

**Amaç:** Paketin kurallara uyup uymadığını kontrol eden, onu imzalayan ve doğrulayan çekirdeği ortaya çıkarmak. İlk elle tutulur çıktı buradadır. İki basit dijital örnek paket de bu fazda hazırlanır.

### Görevler

JSON şemaları:

- [ ] `skillpack.yaml` için JSON Schema yazmak
- [ ] İptal listesi için basit bir JSON Schema taslağı yazmak (olgunlaşma F4'te)
- [ ] Paket indeksi için JSON Schema taslağı yazmak (olgunlaşma F4'te)
- [ ] `robot_profile.yaml` için iskelet şema yazmak (olgunlaşma F3'te)

CLI komutları (her biri ayrı iş):

- [ ] `skillpack init` — yeni paket iskeleti (klasör yapısı, `SKILL.md`, `skillpack.yaml`)
- [ ] `skillpack validate` — şema, zorunlu alanlar, geriye uyumluluk ve temel kural denetimi
- [ ] `skillpack pack` — kanonik arşiv, SHA-256 özetleri, içerik adresli paket kimliği
- [ ] `skillpack sign` — Sigstore (anahtarsız / OIDC) ile imzalama
- [ ] `skillpack verify` — imza, özet ve (varsa) şeffaflık günlüğü kanıtını doğrulama
- [ ] `skillpack publish` — paketi dağıtım hedefine (önce yerel dizin veya basit HTTP) yayımlama
- [ ] `skillpack revoke-check` — iptal listesine bakma (basit liste; TUF F4'te)

Güven ve gizlilik yardımcıları:

- [ ] PII tarama yardımcısı eklemek (T.C. kimlik no, telefon, e-posta, IBAN, plaka; yüz görüntüsü uyarısı). Tarama yardımcıtır, garanti değildir.
- [ ] `raw_customer_data: false` kuralını doğrulayıcıda zorunlu kılmak
- [ ] Bilinmeyen alanları uyarıyla geçme, bilinmeyen MAJOR spesifikasyonu reddetme davranışını yazmak

Örnek paketler:

- [ ] Dijital örnek paket 1: depo stok sapması tanısı (anonim/sentetik örnekler, kabul testleri)
- [ ] Dijital örnek paket 2: ses kaydı düzeltme iş akışı (anonim/sentetik örnekler, kabul testleri)
- [ ] Her iki örneği `validate` + `pack` + `sign` + `verify` zincirinden geçirmek

Uçtan uca kanıt:

- [ ] Bir paketi bir bilgisayarda imzalayıp başka bir bilgisayarda doğrulayan tekrarlanabilir bir test belgelemek

### Çıkış ölçütü

Bir paket uçtan uca imzalanıp başka bir makinede doğrulanabiliyor.

---

## F2 — Yerel çalışma (A5–A9)

**Durum:** ⬜ Başlamadı

**Amaç:** Mini sunucuda çalışan yerel sistemi kurmak: model, paket deposu, izin uygulayan yönlendirici, ince telefon istemcisi ve öğretme döngüsü prototipi. Hedef, yazılımcı olmayan bir ustanın yardımla bir beceriyi paketleyebilmesidir.

### Görevler

Yerel ortam:

- [ ] Mini sunucuya Ollama (veya llama.cpp) kurulumunu belgelemek
- [ ] Qwen2.5 7B (Q4, Apache-2.0) modelini kurmak ve ilk gecikme / token/s / bellek ölçümünü almak (Bölüm 12; taban henüz yok)
- [ ] Kurulumun kurum kaynağı kullanmadan, kişisel/gönüllü donanımda yapıldığını netleştirmek

Yerel depo servisi:

- [ ] Paket indirme ve yerel saklama
- [ ] İndirilen paketin imza ve özet doğrulaması
- [ ] İptal listesi senkronu (basit periyodik çekme)
- [ ] İzin onay arayüzü (yeni veya genişleyen yetkiler otomatik uygulanmaz)

Yönlendirici:

- [ ] Kural tabanlı eşleştirme (istek türü → dikey ajan / paket)
- [ ] Eşleşme yoksa veya güven düşükse yerel LLM ile yedek sınıflama
- [ ] İzin beyanını uygulama (beyan dışı araç çağrısını reddetme ve kaydetme)
- [ ] Katmanlar arası kural: kişisel/müşteri/gizli verinin buluta gitmemesi; bulut varsayılan kapalı
- [ ] Denetim izi: paket sürümü, karar, kanıt, onaylayan, süre

Telefon istemcisi (ince):

- [ ] Gösterim yakalama (ses, fotoğraf, ekran; kullanıcı izniyle)
- [ ] Kısa soru-cevap / saha arayüzü
- [ ] Tanı kartı görüntüleme (sorun, olası neden, kanıt, öneri, güven; otomatik eylem yok)

Öğretme döngüsü prototipi:

- [ ] Yakala — kayıt ve (gerekiyorsa) maskeleme
- [ ] Damıt — yerel modelin taslak `SKILL.md` / `kurallar.yaml` önermesi; her kural en az bir kanıta bağlı
- [ ] Test et — kayıtlı gösterimleri tekrar oynatma, kabul testleri, beyan dışı araç çağrısı denetimi
- [ ] Onayla — ustanın (ve varsa ikinci kişinin) kuralları okuyup onaylaması (`approvals.json`)
- [ ] Paketle — anonimleştirme, PII taraması, köken beyanı, imza

Kullanılabilirlik kanıtı:

- [ ] Geliştirici olmayan bir ustanın yardımla bir beceriyi paketlediği bir deneme yapmak ve süreyi / dış yardım ihtiyacını not etmek

### Çıkış ölçütü

Geliştirici olmayan bir usta, yardımla bir beceriyi paketleyebiliyor.

---

## F3 — Fiziksel profil (A8–A12)

**Durum:** ⬜ Başlamadı

**Amaç:** İsteğe bağlı fiziksel uzantıyı tanımlamak ve koli ayırma örneğini **yalnız simülasyonda** kabul testlerinden geçirmek. MVP kapsamında gerçek robot hareket ettirilmez.

### Görevler

Şema ve profil:

- [ ] `robot_profile.yaml` şemasını olgunlaştırmak (gövde, serbestlik derecesi, eklem sınırları, uç efektör, kalibrasyon, varsa URDF)
- [ ] Sensör beyanları (kamera, kuvvet-tork, barkod okuyucu)
- [ ] ROS 2 konu/servis adları ve mesaj tipleri
- [ ] OPC UA düğüm kimlikleri (PLC/hücre durumu, salt-okur)
- [ ] Güvenlik zarfı alanları (hız/kuvvet sınırları, yasak bölgeler, gereken güvenlik donanımı). Zarf bilgilendiricidir; saha güvenliği paketin kontrolünde değildir.
- [ ] ISO 10218, ISO/TS 15066 ve ilgili çerçevelerin uygulanabilirliği için ayrıca inceleme notu açmak **[EKSİK]**

Veri bağlantısı:

- [ ] LeRobotDataset biçimine referans veya gömülü `physical/dataset/` bağlantısını tanımlamak
- [ ] Open X-Embodiment / RLDS biçimi için bir dönüştürücü yazmak
- [ ] İsteğe bağlı politika ağırlıkları + model kartı alanlarını tanımlamak (safetensors/GGUF dışı formatları reddetmek)

Örnek ve test:

- [ ] Koli ayırma örnek fiziksel paketini hazırlamak (prosedür + kurallar + `robot_profile` + simülasyon testleri)
- [ ] Gazebo veya MuJoCo üzerinde kabul testlerini yazmak ve çalıştırmak
- [ ] Varsayılan çalışma kipini öneri/simülasyon yapmak; gerçek hareket kapısını insan onayına bağlamak (kapı bu fazda simülasyonla sınanır, saha hareketi açılmaz)
- [ ] Profil uyumsuzsa paketin yalnız `procedure` kipinde yüklenmesini uygulamak
- [ ] Kapsam sınırını belgelemek: gerçek robotta hareket MVP dışında kalır

### Çıkış ölçütü

Fiziksel paket simülasyonda kabul testlerini geçiyor.

---

## F4 — Dağıtım ve iptal (A10–A14)

**Durum:** ⬜ Başlamadı

**Amaç:** Paketleri tek bir merkeze bağlı olmadan dağıtmak ve bozuk bir paketin geri çekilebildiğini göstermek. Güven imzadan ve günlükten gelir; indirme kaynağı güveni belirlemez.

### Görevler

İndeks ve aynalar:

- [ ] İmzalı paket indeksi formatını tamamlamak (kimlik → ad, sürüm, yayıncı, alan)
- [ ] En az iki bağımsız HTTP aynası kurmak veya anlaşmak (üniversite, kamu, topluluk; ticari dükkân değil)
- [ ] Bir IPFS kanalı eklemek
- [ ] Çevrim dışı medya / USB ile taşıma yolunu belgelemek

İptal listesi ve TUF:

- [ ] İmzalı, sürümlü, zaman damgalı iptal listesi formatını tamamlamak (paket kimliği, sürüm aralığı, gerekçe kodu, ciddiyet, tarih)
- [ ] TUF tarzı rol ayrımını kurmak (kök, zaman damgası, anlık görüntü, hedefler)
- [ ] İstemcinin listeyi periyodik çekmesini yazmak (çevrimiçiyken günlük çekme önerisi [VARSAYIM]; aralık yerel politikadır)
- [ ] İptal edilen paketi devre dışı bırakıp kullanıcıya gerekçe göstermek
- [ ] Çevrim dışı sahalarda son senkron tarihini arayüzde göstermek

Tatbikat:

- [ ] Bir test paketini yayımlayıp ardından geri çekmek
- [ ] Tüm pilot istemcilerin (ve aynaların) iptali tespit ettiğini ölçerek göstermek
- [ ] İptal yetkisini ve itiraz yolunu yönetişim taslağına not etmek (vakıf güvenlik rolü veya yayıncının kendi talebi; olgunlaşma F6)

### Çıkış ölçütü

Bir test paketinin iptali tüm pilot istemcilerde tespit ediliyor.

---

## F5 — Pilot (A12–A18)

**Durum:** ⬜ Başlamadı

**Amaç:** 2–3 gönüllü iş yerinde sistemi denemek, Bölüm 12'deki alanlarda taban ölçümü almak ve olayları kaydetmek. Hedef sayılar bilinçli olarak baştan konmaz; taban ölçüldükten sonra belirlenir **[EKSİK]**.

### Görevler

Hazırlık:

- [ ] 2–3 gönüllü pilot saha seçmek (yazılı onam; kurum kaynağı ve gizli bilgi kullanılmaz)
- [ ] Pilot kapsamında hangi paketlerin kullanılacağını ve hangi verinin yerelde kalacağını yazılı olarak netleştirmek
- [ ] Ölçüm planını Bölüm 12'ye göre yazmak (taban ölçümü, sonra hedef)

Ölçümler (her biri ayrı izlenir):

- [ ] Spesifikasyon: doğrulayıcıyı geçen bağımsız / üçüncü taraf uygulama sayısı
- [ ] Taşınabilirlik: aynı paketin değişiklik olmadan çalıştığı çalışma zamanı sayısı (çapraz test matrisi)
- [ ] Güven: imza doğrulama başarısı; iptalin istemcilere yayılma süresi (tatbikat)
- [ ] Öğretme: geliştirici olmayan kullanıcının paketleme süresi ve dış yardım ihtiyacı
- [ ] Kalite: kabul testi geçme oranı; tanı kartlarının onay / düzeltme / red oranı
- [ ] Performans: yerel sunucuda gecikme (p50/p95), token/s, bellek
- [ ] Gizlilik: PII taramasında yakalanan / kaçan örnek; DP kullanılan paket payı (MVP'de DP yalnız arayüz olabilir)
- [ ] Güvenlik: kırmızı takım bulguları; olay sayısı ve kapanma süresi
- [ ] Topluluk: katkıcı, yayıncı ve ayna sayısı
- [ ] Dolaylı ekonomik gözlem (isteğe bağlı, gönüllü, anonim): lisans beyanı olan paket var mı? Bu proje gelir toplamaz.

Rapor:

- [ ] Olay kayıtlarını tutmak
- [ ] Ölçüm raporunu yayımlamak
- [ ] Taban ölçüldükten sonra hedef değerleri önerip yol haritasını güncellemek

### Çıkış ölçütü

Ölçüm raporu ve olay kayıtları yayımlanmıştır.

---

## F6 — Yönetişim (A12–A24)

**Durum:** ⬜ Başlamadı

**Amaç:** Projeyi olgun bir topluluk çalışması olarak sürdürmek ve Linux Foundation bünyesindeki AAIF'e, Agent Skills'in "skillpack: fiziksel profil ve güven" uzantısı için bir çalışma grubu / alt proje önermek. Sonuç belirsizdir; hedef, önerinin değerlendirmeye alınmasıdır.

### Görevler

Topluluk projesi:

- [ ] `KATKI.md` ve davranış kurallarını yazmak
- [ ] Spesifikasyon değişiklik sürecini tanımlamak (öneri → taslak → kabul)
- [ ] Uyumluluk test setinin bakımını planlamak

AAIF'e giden yol:

- [ ] AAIF'in çalışma grubu açma sürecini ve kriterlerini birincil kaynaktan doğrulamak **[EKSİK]**
- [ ] AAIF çalışma grubu / alt proje önerisi metnini yazmak
- [ ] İmza tarafında OpenSSF, robot tarafında ROS ve LeRobot topluluklarıyla iş birliği notları hazırlamak
- [ ] Öneriyi sunmak ve sürecin değerlendirmeye alınıp alınmadığını kaydetmek (kabul sonucu bu fazın başarısı değildir)

Spesifikasyon v1.0 adayı:

- [ ] Pilot ve dış inceleme notlarını taslağa işlemek
- [ ] Spesifikasyon v1.0 adayını yayımlamak
- [ ] Uyumluluk test setini v1.0 adayıyla hizalamak
- [ ] Vakıf rolünün sınırlarını belgelemek: spesifikasyon, kök/iptal, referans uygulama koordinasyonu; pazar yeri işletmemek, ödemeye aracılık etmemek

### Çıkış ölçütü

AAIF önerisi değerlendirmeye alındı (sonucun ne olacağı belirsizdir).

---

## Başarı ölçütleri (hatırlatma)

Hedef değerler bilinçli olarak sayı içermez; çünkü taban ölçümü yoktur. İlk pilotta (F5) taban ölçülür, hedefler sonra belirlenir **[EKSİK]**. Ölçüt listesi teknik taslak Bölüm 12'dedir.

## Hukuki duruş (hatırlatma)

Bu proje ticari değildir, şirket veya ürün planı değildir. F0'ın hukuki görüşü alınmadan gelir, lisans devri veya vakıf görevi gibi adımlara geçilmez. Ayrıntı: teknik taslak Bölüm 14.
