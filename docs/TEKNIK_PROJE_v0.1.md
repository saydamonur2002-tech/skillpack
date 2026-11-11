# Yerel Beceri Paketi

**Yerel sunucuda öğretilen, açık, taşınabilir ve imzalı ajan becerileri için bir standart, güven altyapısı ve referans uygulama önerisi**

Teknik Proje Dokümanı — Taslak v0.1

Agent Skills (`SKILL.md`) için fiziksel gösterim/politika uzantısı, merkezsiz dağıtım, vakıf imzası ve iptal listesi, telefon ↔ yerel sunucu ↔ bulut yönlendirmesi

- Tarih: 9 Kasım 2026
- Güncelleme: 10 Kasım 2026 (Bölüm 2.3 eklendi; önceki bölümlerin anlamı aynıdır)
- Öneren: gülümse (bireysel katkıcı; açık kaynak / vakıf modeli)
- Hazırlık desteği: Grok Bot
- Hedef okur: teknik değerlendiriciler, Linux Foundation AAIF çalışma grupları, hibe değerlendiricileri

Kaynak etiketleri:

- `[VERİ]` birincil/doğrulanmış kaynak
- `[VEKİL]` ikincil kaynak veya yaklaşık gösterge
- `[VARSAYIM]` tasarım/ekip varsayımı
- `[HESAP]` dosyalardaki hesap çıktısı veya bu dokümanda gösterilen aritmetik
- `[EKSİK]` bulunamadı / doğrulanmadı

**Durum:** tartışma taslağı. Bu doküman bir şirket ya da ürün planı değildir; açık standart ve açık kaynak katkı önerisidir. Belirtilen hiçbir kuruluşla resmî ilişki yoktur.

Bu dosya, 9 Kasım 2026 tarihli taslağın temiz Markdown dönüşümüdür. Anlam, rakamlar ve kaynak etiketleri korunmuştur.

---

## İçindekiler

- [Özet](#özet)
- [1. Problem ve boşluk](#1-problem-ve-boşluk)
- [2. Hedefler ve hedef olmayanlar](#2-hedefler-ve-hedef-olmayanlar)
  - [2.3 Tasarım hedefleri (üç çerçeve)](#23-tasarım-hedefleri-üç-çerçeve)
- [3. Sistem mimarisi](#3-sistem-mimarisi)
- [4. Beceri paketi spesifikasyonu (taslak "skillpack" v0.1)](#4-beceri-paketi-spesifikasyonu-taslak-skillpack-v01)
- [5. Öğretme döngüsü](#5-öğretme-döngüsü)
- [6. Dağıtım ve güven](#6-dağıtım-ve-güven)
- [7. Yönetişim](#7-yönetişim)
- [8. Üzerine kurulabilecek iş modelleri ve yaratıcı sahipliği](#8-üzerine-kurulabilecek-iş-modelleri-ve-yaratıcı-sahipliği)
- [9. Güvenlik ve gizlilik tehdit modeli](#9-güvenlik-ve-gizlilik-tehdit-modeli)
- [10. Referans uygulama planı](#10-referans-uygulama-planı)
- [11. Yol haritası](#11-yol-haritası)
- [12. Başarı ölçütleri](#12-başarı-ölçütleri)
- [13. Riskler ve açık sorular](#13-riskler-ve-açık-sorular)
- [Ek A. Sözlük](#ek-a-sözlük)
- [Ek B. Kaynaklar](#ek-b-kaynaklar)

---

## Özet

Bu doküman, bir iş akışını ya da beceriyi kendi işyerindeki yerel bir sunucuda yapay zekâ ajanlarına öğreten herkesin (fabrika ustası, depo operatörü, fotoğraf/ses düzenleyici, sağlık teknisyeni) bu bilgiyi açık, taşınabilir ve imzalı bir "beceri paketi" olarak dışa aktarabilmesini, paylaşabilmesini ya da lisanslayabilmesini sağlayacak bir standart ve referans uygulama önerir.

Ajan becerileri için açık bir metin formatı artık var: Agent Skills (`SKILL.md`), 2026-10-22 `[VERİ]` tarihinde Linux Foundation bünyesindeki Agentic AI Foundation'a (AAIF) bağışlandı (Anthropic: Agent Skills AAIF bağışı). AAIF ise 2025-12-09 `[VERİ]` tarihinde MCP, AGENTS.md ve goose bağışlarıyla kuruldu (LF AAIF duyurusu). Bu proje mevcut standardın yerine geçmeyi değil, onun üzerine dört eksik katman eklemeyi hedefler:

- **Fiziksel uzantı:** prosedür + kurallar + araç çağrıları ile robot gösterim/politika verisini (ör. depoda koli ayırma) tek pakette birleştiren, LeRobotDataset / Open X-Embodiment, ROS 2 ve OPC UA ile hizalı bir profil.
- **Güven altyapısı:** Sigstore/SLSA/TUF yöntemlerini beceri paketlerine uyarlayan imza, şeffaflık günlüğü ve iptal listesi; dağıtım merkezi sunucu yerine aynalar ve P2P ile.
- **Öğretme döngüsü:** geliştirici olmayan bir ustanın gösterimini yerel sunucuda kurallara damıtan, sandbox/simülasyonda test eden ve insan onayından sonra paketleyen bir akış.
- **Taşınabilirlik ve yönlendirme:** n8n/Make/UiPath gibi tek ürüne kilitli şablonların aksine çalışma zamanından bağımsız paket; telefon ↔ yerel sunucu ↔ isteğe bağlı bulut arasında izin bilgili yönlendirme.

Tasarım duruşu muhafazakârdır: ajanlar tanı ve öneri üretir, kararı insan verir; ham müşteri verisi pakete girmez; bulut varsayılan olarak kapalıdır. Doküman bir ürün ya da pazar iddiası taşımaz. Bir spesifikasyon taslağı, bir tehdit modeli, bir yönetişim seçenek analizi ve göreli aylarla tanımlanmış bir referans uygulama planı sunar. Benimseme, gelir ve performans için ölçülmüş veri yoktur; bu boşluklar `[EKSİK]` olarak işaretlenmiştir.

**Okuma notu.** Sayılar yalnız `/workspace/nis_pazar_hesabi/` altındaki tarama dosyalarından ve bu dokümanda bağlantısı verilen kaynaklardan alınmıştır. Anthropic'in 1M skill, ~280M kurulum ve >70 platform rakamları şirketin kendi beyanıdır `[VERİ]` (kaynak kurumun iddiası olarak). Pazar büyüklüğü rakamları tanım farkları nedeniyle birbirleriyle doğrudan karşılaştırılamaz `[VEKİL]`.

---

## 1. Problem ve boşluk

### 1.1 Sahadaki problem

Küçük işletmelerde ve sahada çalışan ustalarda değerli bir örtük bilgi var: bir makinenin arızasını sesinden ayırt etmek, depoda koliyi hangi sırayla ayıracağını bilmek, bir ses kaydını belli bir standarda getirmek, bir cihazın kalibrasyon adımlarını doğru sırayla uygulamak. Bu bilgi bugün genellikle kişiyle birlikte gider; belgelenmez, aktarılması zordur ve ölçeklenmez.

Yapay zekâ benimsenmesinde ana engel teknoloji değil uzmanlıktır. AB'de 10+ çalışanlı işletmelerin %19,95'i `[VERİ]` 2025'te yapay zekâ kullanıyor (küçük işletmelerde %17 `[VERİ]`, orta ölçekte %30,36 `[VERİ]`). Kullanmayı düşünüp kullanmayanların %70,89'u `[VERİ]` gerekçe olarak "uzmanlık eksikliği"ni gösteriyor (Eurostat: işletmelerde yapay zekâ). Türkiye için aktarılan oran %7,4–7,5 `[VEKİL]` civarında; TÜİK birincil bülteni bu çalışmada doğrulanmadı `[EKSİK]`. Bu tablo "hazır, doğrulanmış, yerel çalışan beceri paketi" fikrine bir talep sinyali verir. Ama ödeme isteğini ya da benimsemeyi kanıtlamaz `[EKSİK]`.

Büyük otomasyon platformları bu ölçeğe genellikle inmez. Şablon ve bot pazarları var ama her biri kendi çalışma zamanına bağlı. Robot öğrenme dünyasında açık veri setleri hızla büyüyor ama prosedür, iş kuralı, izin ve sertifikasyon bilgisinden kopuk.

### 1.2 Ne değişti: standart katman kısmen kapandı

2025–2026'da tarafsız vakıf ve açık beceri formatı boşluğu büyük ölçüde kapandı. Bu proje bu zemini veri kabul eder ve tekrar icat etmez. Agent Skills spesifikasyonu bir beceriyi `SKILL.md` (YAML ön bilgi + Markdown talimat) ile isteğe bağlı `scripts/`, `references/`, `assets/` klasörlerinden oluşan bir dizin olarak tanımlar. Ön bilgide zorunlu alanlar `name` ve `description`; isteğe bağlı alanlar `license`, `compatibility`, `metadata` (dizge→dizge eşlemesi) ve deneysel `allowed-tools`. Spesifikasyonda imza, köken, iptal, fiziksel veri ya da donanım profili alanı yok `[VERİ]` (spesifikasyon metni, 2026-11 okuması).

### 1.3 Kanıt tablosu

**Tablo 1. Boşluğu gösteren kanıtlar**

| Bulgu | Değer | Etiket / kaynak | Projeye anlamı |
|---|---|---|---|
| AAIF kuruluşu (LF altında) | 2025-12-09 | `[VERİ]` LF AAIF duyurusu | Tarafsız ev mevcut; yeni vakıf zorunlu değil |
| MCP sunucu sayısı (LF duyurusu) | >10.000 | `[VERİ]` LF AAIF duyurusu | Araç katmanı standartlaştı |
| Resmî MCP kayıt satırı (farklı sayım) | 55.773 | `[VEKİL]` kayıt dökümü, 2026-11-03 | Kapsam farklı; büyüklük göstergesi |
| AGENTS.md benimseyen proje | >60.000 | `[VERİ]` LF AAIF duyurusu | Metin tabanlı ajan talimatı yaygın |
| Agent Skills → AAIF | 2026-10-22 | `[VERİ]` Anthropic: Agent Skills AAIF bağışı | Genişletilecek temel format |
| Yayınlanan skill / kurulum / platform | 1M / ~280M / >70 | `[VERİ]` Anthropic: Agent Skills AAIF bağışı (şirket beyanı) | Dağıtım ölçeği var; güven katmanı yok |
| Spesifikasyonda imza/iptal alanı | yok | `[VERİ]` Agent Skills spesifikasyonu | Boşluk B2 |
| LeRobot etiketli veri seti (resmî hesap dışı) | 81.881 | `[VERİ]` LeRobot HF sayımı, 2026-10-23 | Fiziksel veri bol |
| Örneklemde kullanılabilir pay | ~%38 (GA %33–43) | `[VERİ]` LeRobot HF sayımı | Kalite sorunu → test ve sertifikasyon ihtiyacı |
| Open X-Embodiment | 22 robot · 527 skill · 160.266 görev | `[VERİ]` Open X-Embodiment makalesi | Araştırma formatı; prosedür/kural/izin yok |
| n8n şablon sayısı | 5.191 (2025-09) → ~13.653 (2026-10) | `[VERİ]` n8n 5k şablon duyurusu / `[VEKİL]` şablon pazarı karşılaştırması (dartzdabz) | Talep var; platforma kilitli (B4) |
| Make şablonu / UiPath listing | >7.000 / >1.450 | `[VEKİL]` şablon pazarı karşılaştırması (dartzdabz) / UiPath Marketplace belgeleri | Merkezi, tek ürünlü dükkânlar |
| Model deposu tedarik zinciri saldırıları | belgelenmiş | `[VERİ]` Acronis: HF ve OpenClaw tedarik zinciri saldırıları; CSA: zararlı model depoları notu (PDF) | İmza + iptal şart (B2) |
| Sigstore/SLSA paket kayıtlarında | yaygınlaşıyor | `[VEKİL]` Paket kayıtlarında imza ve beyanlar (nesbitt.io, 2026-10) | Yöntem hazır; beceri ekosistemine bağlanmamış |
| Beceri paketi için iptal listesi ürünü | bulunamadı | `[EKSİK]` | Doğrudan hedef |
| Telefon + yerel + bulut + dikey/yatay ajan tek paket | A·B·C·D· satırı yok | `[VERİ]` platform taraması (bosluk.md) | B5 (yönlendirme) |

Kaynak: `beceri_standardi/veri_tablosu.csv`, `kaynaklar.csv`; `platform_tarama/bosluk.md`

### 1.4 En yakın paylaşılan "beceri" benzerleri

**Tablo 2. Mevcut paylaşım sistemleri ve eksikleri**

| Sistem | Ne paylaşılır | Taşınır mı | Yerel/bulut | Yönetişim | Eksik olan |
|---|---|---|---|---|---|
| Agent Skills | SKILL.md + script/ref/asset | Evet (açık spec) | Çoğu bulut ajanı; yerel mümkün | AAIF (2026-10) | İmza, iptal, fiziksel profil, izin modeli |
| MCP | Araç/bağlantı sunucuları | Protokol taşınır | Her ikisi | AAIF | Beceri/prosedür paketi değil |
| LeRobot / HF Hub | Robot veri seti / politika | Ortak format | Hub merkezi | HF topluluğu | Prosedür, kural, sertifikasyon |
| Open X-Embodiment | Çoklu robot verisi | Araştırma formatı | Lab/bulut | Konsorsiyum | Saha prosedürü, lisans/izin |
| n8n / Make / Zapier | Workflow şablonu | Hayır | Bulut / self-host | Şirket | Taşınabilirlik, imza |
| UiPath Marketplace | RPA bot/listing | UiPath içi | Kurumsal | UiPath | Açıklık, mikro ölçek |
| Ollama kütüphanesi | Model ailesi (~270 `[VEKİL]`) | Model taşınır | Yerel | Şirket | Beceri katmanı yok |

Kaynak: `beceri_standardi/ozet.md` `[VERİ]`/`[VEKİL]`

### 1.5 Boşluk tanımı

Bu çalışmanın hedeflediği boşluk beş maddeye indirgenebilir. Her biri ayrı ayrı kısmen çözülmüş durumda; birlikte çözen açık bir yapı bulunamadı `[VERİ]`/`[VEKİL]`:

- **B1 — Fiziksel + prosedürel birleşik paket:** gösterim/politika verisi, adımlar, iş kuralları ve araç çağrılarını tek bir imzalı birimde taşıyan format yok.
- **B2 — Merkezsiz pazar + vakıf imzası/iptal:** mevcut dükkânlar merkezi (GitHub, HF, UiPath, n8n); beceri paketleri için şeffaflık günlüğü ve iptal listesi yok.
- **B3 — Usta öğretme döngüsü → mikro lisans:** geliştirici olmayan birinin öğrettiği beceriyi pakete ve küçük ölçekli paylaşıma dönüştüren kanal yok.
- **B4 — Gerçek taşınabilirlik:** şablonlar tek çalışma zamanına kilitli.
- **B5 — İzin bilgili kenar–yerel–bulut yönlendirmesi:** telefon, yerel sunucu ve bulut arasında hangi verinin nereye gidebileceğini paket düzeyinde beyan eden bir model yok.

---

## 2. Hedefler ve hedef olmayanlar

### 2.1 Hedefler

**Tablo 3. Hedefler**

| Kod | Hedef | Doğrulanabilir çıktı |
|---|---|---|
| H1 | Agent Skills ile geriye uyumlu bir "beceri paketi" uzantısı (skillpack) tanımlamak | Spesifikasyon taslağı + JSON Schema + doğrulayıcı CLI |
| H2 | Fiziksel gösterim/politika verisini paketin isteğe bağlı bileşeni yapmak | LeRobotDataset'e referans veren `physical/` profili + örnek paket |
| H3 | İmza, köken, şeffaflık günlüğü ve iptal listesi | Sigstore tabanlı imzalama + iptal listesi formatı + doğrulama kitaplığı |
| H4 | Merkezi sunucusuz dağıtım | İçerik adresli ayna/P2P indeks formatı; en az iki bağımsız ayna |
| H5 | Geliştirici olmayan kullanıcı için yerel öğretme döngüsü | Yakala → damıt → test → onay → paketle akışının çalışan prototipi |
| H6 | İzin bilgili katmanlar arası yönlendirme | İzin beyanını uygulayan yönlendirici referans uygulaması |
| H7 | Yönetişim önerisi | AAIF'e çalışma grubu / alt proje önerisi metni |

### 2.2 Hedef olmayanlar

- Yeni bir ajan çerçevesi, yeni bir model ya da yeni bir araç protokolü yazmak (MCP, A2A ve mevcut çalışma zamanları kullanılır).
- Otonom karar ve eylem. Ajanlar tanı ve öneri üretir; kaynak sistemde kayıt değiştiren ya da fiziksel hareket başlatan her adım insan onayına bağlıdır. Fiziksel robotlarda güvenlik işlevleri (acil stop, güvenlik PLC'si) paketin kontrolünde değildir.
- Merkezi bir pazar yeri işletmek ya da ödeme aracısı olmak. Standart fiyat ve lisans alanı tanımlar; ödeme altyapısı kapsam dışıdır.
- Ham müşteri ya da hasta verisi paylaşımı. Paket yalnız damıtılmış kurallar ve anonimleştirilmiş örnekler taşır.
- Klinik teşhis, tıbbi cihaz işlevi ya da düzenlenmiş güvenlik işlevi sertifikasyonu. Sağlık alanında kapsam idari/teknik iş akışlarıyla sınırlıdır.
- Bir şirket kurmak. Proje açık kaynak / vakıf modeliyle ilerler.

### 2.3 Tasarım hedefleri (üç çerçeve)

Bölüm 2.1'deki H1–H7, standardın üretilecek çıktılarıdır. Bu alt bölüm, bir paketin **standart profile** girebilmesi için üç çerçeveyi sabitler. Model boyutu, tok/s ve güç bandı öneridir `[VARSAYIM]`. Enerji kazancının kendisi henüz ölçülmedi `[EKSİK]`. Telefon, Mac mini sınıfı yerel sunucu ve isteğe bağlı buluttan oluşan tipik katman donanımı Bölüm 3.1'de durur. Buradaki referans, standart profilin ölçüm tezgâhıdır.

**1. Orta segment donanımda çalışabilirlik.** Paket, tek bir orta segment GPU sunucusunda çalışabilmelidir. Referans donanım: 24–48 GB belleğe sahip tek GPU (RTX 4090 / 5090 veya L40S sınıfı), kart gücü kabaca 300–500 W `[VARSAYIM]`. Her paket, birlikte çalıştığı asgari model boyutunu beyan eder. Beceri uygulamasının hedefi yaklaşık 8B sınıfı bir açık modeldir `[VARSAYIM]`. Etkileşimli kullanım için önerilen alt hız yaklaşık 40 tok/s'tir `[VARSAYIM]`. 70B ve üzeri yoğun modellerde sınır muhakemesi (frontier) yerel kapsamın dışındadır; bu işler isteğe bağlı bulut katmanına gider (Bölüm 3.1, Katman 3).

**Tablo 3a. Referans kartta tek kullanıcılı üretim hızı (decode)**

| Kurulum | Hız | Etiket / kaynak |
|---|---|---|
| Llama 3.1 8B, RTX 4090 24 GB, llama.cpp GGUF Q4_K_M, batch 1 | 148 tok/s | `[VERİ]` [quantized.uk ölçümleri](https://quantized.uk/benchmarks/) |
| Aynı kart ve model, vLLM AWQ INT4 | 218 tok/s | `[VERİ]` quantized.uk |
| Aynı kart ve model, ExLlamaV2 EXL2 4,65 bpw | 235 tok/s | `[VERİ]` quantized.uk |
| Llama 3.1 8B, RTX 4090, llama.cpp / vLLM (Temmuz 2026) | 162 / 185 tok/s | `[VERİ]` [Plugsky yerel çıkarım ölçümü](https://plugsky.com/local-inference-benchmark) |
| Qwen2.5 32B / Qwen3 32B, RTX 4090, llama.cpp Q4_K_M | 44 / 42 tok/s | `[VERİ]` quantized.uk |
| Qwen 2.5 32B, RTX 4090, vLLM AWQ INT4, batch 1 | 65 tok/s | `[VEKİL]` [GigaGPU ölçümü](https://gigagpu.com/rtx-4090-24gb-qwen-32b-benchmark/) (barındırıcının kendi sayfası, Mayıs 2026) |
| Llama 3.3 70B Q4, RTX 4090 24 GB, Ollama | 5,1 tok/s | `[VERİ]` Plugsky |
| Llama 3 70B Q4_K_M, tek 48 GB kart (A6000 14,6; L40S 15,3; RTX 6000 Ada 18,4 tok/s) | yaklaşık 15–18 tok/s | `[VEKİL]` [GPU-Benchmarks-on-LLM-Inference](https://github.com/XiongjieDai/GPU-Benchmarks-on-LLM-Inference) (llama.cpp, Llama 3; 2026 yeniden ölçümü değil) |

quantized.uk satırları 4-bit civarıdır (Q4_K_M, AWQ INT4, EXL2 yaklaşık 4,65 bpw), tek dizidir ve üretim hızıdır; ön-doldurma (prefill) ayrı raporlanmaz `[VERİ]`. Plugsky aynı kartta Llama 3.1 8B için llama.cpp 162 tok/s ve vLLM 185 tok/s verir; tepe bellek yaklaşık 5,8–5,9 GB'dır `[VERİ]`. Sayfanın genel yöntem satırı GPU ölçümlerini FP16 diye yazar, 8B satırı nicemlemeyi ayrıca belirtmez. Kayıtlı bellek 4-bit ile uyumludur `[VEKİL]`. 70B Q4, 24 GB'ta 5,1 tok/s ile yaklaşık 40 tok/s etkileşim önerisinin altındadır `[VERİ]` / `[VARSAYIM]`. 48 GB sınıfı tek kartta (A6000, L40S, RTX 6000 Ada) llama.cpp ölçümü yaklaşık 15–18 tok/s'tir; bu, 10–20 tok/s vekil bandının içindedir `[VEKİL]`. İki hız da etkileşim önerisinin altındadır. ≥70B yoğun model yerel standart profilin dışında kalır ve isteğe bağlı bulut katmanına gider.

8B satırları (148–235 tok/s), yaklaşık 40 tok/s önerisinin birkaç kat üstündedir `[HESAP]`. Yaklaşık 32B yoğun model 42–65 tok/s ile eşiğin kıyısındadır: alt uç quantized.uk llama.cpp (42 ve 44) `[VERİ]`, üst uç barındırıcı AWQ ölçümü (65) `[VEKİL]`. Beceri uygulamasının hedefi bu yüzden yaklaşık 8B'de tutulur `[VARSAYIM]`.

**2. Enerji verimliliği.** Bu çerçeve bir watt tavanı koymaz. Birincil ölçü, 1.000 token başına enerji değil, **tamamlanan görev başına** Wh ve token'dır. Paket, aynı görevin iki ölçümünü raporlamalıdır: (a) becerisiz genel bir ajan, (b) paketlenmiş beceri, küçük bir yerel modelin üzerinde. Raporda token, süre ve tahmini Wh bulunur.

Yerel 8B decode için sabit 400 W `[VARSAYIM]` (300–500 W bandının içi) ve yalnız üretim hızı alındığında:

Wh/1000 decode token = P / (3,6 × tok/s) `[HESAP]`.

- 148 tok/s → 400 / (3,6 × 148) ≈ 0,75 Wh/1000
- 218 tok/s (vLLM, quantized.uk) → ≈ 0,51 Wh/1000
- 185 tok/s (vLLM, Plugsky) → ≈ 0,60 Wh/1000

vLLM aralığı yaklaşık 0,51–0,60 Wh/1000 decode token'dır `[HESAP]`. Hesap, duvar gücü çarpı üretim süresidir. Boşta güç, veri merkezi ek yükü (PUE), ön-doldurma ve yarım kalan görev bu sayının dışındadır.

Aşağıdaki sayılar başka ölçüm sınırlarına aittir. Görev başına tasarruf bunlardan çıkmaz:

- Google, medyan Gemini Apps metin istemi için 0,24 Wh verir. Sınır tam yığındır (hızlandırıcı, ana makine, boşta kapasite, PUE); ölçüm Mayıs 2025'tir `[VERİ]` ([Google Cloud blogu](https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference/), [arXiv:2508.15734](https://arxiv.org/abs/2508.15734)).
- Sam Altman, ortalama bir ChatGPT sorgusu için yaklaşık 0,34 Wh yazar. Yöntem yayımlanmamıştır `[VEKİL]` ([The Gentle Singularity](https://blog.samaltman.com/the-gentle-singularity)).
- Ajan görevleri tek turdan çok daha fazla token yer. OpenHands ve SWE-bench Verified çalışması, ajanik kodlama görevlerinin tipik tek turlu muhakemeden yaklaşık 3500 kat, çok turlu sohbetten yaklaşık 1200 kat fazla token tükettiğini yazar. Fark, her turda yeniden gönderilen girdi bağlamındadır `[VERİ]` ([arXiv:2604.22750](https://arxiv.org/abs/2604.22750)).
- Artificial Analysis Coding Agent Index'te GitHub Copilot Fusion görev başına yaklaşık 7,2M token kullanır `[VERİ]` ([AA yazısı](https://artificialanalysis.ai/articles/github-copilot-fusion-orchestrates-anthropic-and-openai-models-to-balance-performance-and-cost)). Karşılaştırma sayfası Fusion (max) için 7,34M token/görev listeler `[VERİ]` ([Claude Code ve Copilot karşılaştırması](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-github-copilot)).

Ajan izi ön-doldurma ağırlıklıdır: aynı bağlam her turda yeniden okunur. 0,75 Wh/1000 sayısı yalnız decode'dur. Görev başına Wh, bu cetvelden türetilemez. Becerinin enerji kazandırdığı bir hipotezdir ve ölçülmedi `[EKSİK]`. Ölçüm düzeneği (benchmark harness) yol haritasında F2'dedir ([ROADMAP.md](../ROADMAP.md)).

İsteğe bağlı alanlar, Agent Skills `metadata` alanının dizge→dizge kuralıyla ve Bölüm 4.1'deki ek dosya tercihiyle uyumludur. Kanonik yer, `skillpack.yaml` içinde `runtime` ile yan yana duran isteğe bağlı `efficiency` bloğudur. Değerler dizgedir; aynı dizgeler istenirse `metadata`'ya kopyalanır. Zorunlu iki anahtar (`skillpack-spec`, `skillpack-manifest`) durur. Alan adları taslaktır `[VARSAYIM]`.

```yaml
efficiency:                              # isteğe bağlı; Bölüm 2.3
  min_model_size: "8B"                   # asgari açık model
  tokens_per_task: ""                    # ölçülmüş girdi+çıktı, dizge
  wh_per_task: ""                        # ölçülmüş tahmini Wh/görev, dizge
  method: ""                             # donanım, çalışma zamanı, nicemleme, görev
```

Yalnız `SKILL.md` okuyan bir ajana göstermek için aynı dizgeler:

```yaml
metadata:
  skillpack-min-model-size: "8B"
  skillpack-tokens-per-task: ""
  skillpack-wh-per-task: ""
  skillpack-measure-method: ""
```

**3. Açık model ve gündelik hayat etkisi.** Paket, ağırlıkları indirilebilen bir açık modelde çalışmalıdır. Ham veri yerelde kalır, çalışma çevrim dışı olabilir, token başına ücret yoktur. Usta (fabrika ustası, teknisyen) bir kez öğretir; başkası paketi yeniden kullanır (Bölüm 5). Bulut isteğe bağlıdır ve varsayılan kapalıdır (Bölüm 2.2 ve 3.3).

Dürüst sınır: açık ağırlıklı modeller, sınır modellerin gerisindedir. 10 Kasım 2026 okumasında Artificial Analysis Intelligence Index'te en yüksek kapalı model Claude Fable 5.2 (Max) 65, en iyi açık ağırlık Kimi K3.1 Pro 46'dır `[VERİ]` ([Fable 5.2](https://artificialanalysis.ai/models/claude-fable-5-2), [Kimi K3.1 Pro](https://artificialanalysis.ai/models/kimi-k3-1-pro)). Kimi K3.1 Pro 2,8T toplam ve 104B etkin parametrelidir; referans donanıma sığmaz `[VERİ]` (aynı model sayfası). Yerel boyutta skor yaklaşık 20'dir: AA ana sayfası Nanbeige4.3-33B için 20 yazar `[VERİ]` ([artificialanalysis.ai](https://artificialanalysis.ai/), 5 Kasım 2026 duyurusu, 10 Kasım 2026 okundu). 7 Kasım 2026 tarihli ikinci el okuma, Qwen3.8 27B (Xhigh) için 20,1 ve Nanbeige4.3-33B için 20,4 aktarır `[VEKİL]` ([GPUwerk](https://gpuwerk.com/blog/open-weight-model-leaderboard/)). Yeni ya da zor görev buluta gider. Tekrar eden görev yerelde, paketlenmiş beceriyle kalır.

**Birleşik kabul ölçütü.** Bir beceri, aşağıdaki üçünü birlikte sağladığında standart profile girer:

1. Referans donanımda çalışır ve asgari model boyutunu beyan eder.
2. Aynı görevin ölçülmüş verim karşılaştırmasını raporlar: becerisiz genel ajan ve paketlenmiş beceri, küçük yerel model; token, süre, tahmini Wh.
3. Açık ağırlıklı bir modelde çalışır; ham veri sahadan çıkmaz.

Üç madde birlikte standart profilin tanımıdır. Bulut katmanı bu ölçütün yerine konmaz; yeni ve zor iş için isteğe bağlı kanal olarak durur. Eşikler öneridir `[VARSAYIM]`. İkinci maddenin göstereceği tasarruf henüz yoktur `[EKSİK]`.

---

## 3. Sistem mimarisi

Mimari, önceki "Yerel Tanı Sistemi" çalışmasının (salt-okur bağlayıcılar, mini sunucuda tek işlevli dikey ajanlar, kural tabanlı hafif yönlendirici, tanı kartı + insan onayı) genelleştirilmiş hâlidir. Yeni olan iki şey var: becerilerin yerelde öğretilip paket olarak dışa aktarılması ve telefon katmanı + merkezsiz güven/dağıtım katmanı.

**Şekil 1.** Üç katmanlı mimari: telefon/kenar, yerel sunucu (koordinatör, dikey ajanlar, beceri çalışma zamanı, araçlar, robot hücresi, paket deposu), isteğe bağlı bulut ve merkezsiz güven/dağıtım katmanı.

### 3.1 Üç katman

**Tablo 4. Katmanlar ve sorumluluklar**

| Katman | Tipik donanım | Model | Rol | Veri sınırı |
|---|---|---|---|---|
| 1. Telefon / kenar | Akıllı telefon, tablet, endüstriyel el terminali | Küçük açık model, ~1–3B `[VARSAYIM]` | Saha arayüzü (ses, foto, kısa soru), gösterim yakalama, basit niyet sınıflama; çevrim dışı çalışabilir | Ham veriyi yalnız yerel sunucuya gönderir |
| 2. Yerel sunucu | Mini sunucu; ör. Mac mini 24GB sınıfı (~$999 `[VEKİL]`) | Açık ağırlıklı ~7–14B, Q4 (ör. Qwen2.5, Apache-2.0) | Koordinatör, dikey ajanlar, beceri çalışma zamanı, öğretme döngüsü, paket deposu, MCP araçları, robot arayüzü | Ham veri ve gösterimler burada kalır |
| 3. Bulut (isteğe bağlı) | Kullanıcının kendi aboneliği | Genel amaçlı büyük model | Yalnız genel zekâ gerektiren işler (genel yazım, araştırma) | Varsayılan kapalı; yalnız izinli, anonim özet |

Kaynak: `platform_tarama/bosluk.md`; rapor (Bölüm 4.3–4.4); `mini_sunucu/ozet.csv`

Önceki çalışmadaki vekil ölçümlere göre Mac mini M4'te Qwen2.5 7B ~22,2 token/s, 14B ~11,6 token/s `[VEKİL]` üretiyor. Gerçek iş yüküyle sahada ölçülmedi `[EKSİK]`. Tek işlevli ajanlar kısa, yapılandırılmış çıktı ürettiği için bu hızların yeterli olacağı bir `[VARSAYIM]`; referans uygulamada ilk ölçülecek konulardan biridir (Bölüm 12). Standart profilin ölçüm tezgâhı ayrıdır: tek 24–48 GB GPU sunucusu ve yaklaşık 8B beceri hedefi Bölüm 2.3'tedir. Bu tablodaki Mac mini sınıfı, saha için daha hafif bir yerel örnektir.

### 3.2 Ajan hiyerarşisi

- **Dikey alan ajanları:** her biri tek bir alana (ör. depo koli ayırma, CNC bakım tanısı, podcast ses düzeltme, cihaz kalibrasyon kontrol listesi) bakar ve o alanın beceri paketlerini yükler. Kapsam dar, girdi/çıktı şeması tanımlıdır.
- **Yatay koordinatör / yönlendirici:** gelen olayı ya da isteği doğru dikey ajana gönderir, katmanlar arası devri yönetir, izin beyanlarını uygular. Önce kural tabanlı eşleştirme yapar; eşleşme yoksa yerel LLM ile sınıflar; güven düşükse insana devreder. Önceki simülasyonda kural tabanlı yönlendirme için yanlış yönlendirme %2, insana devir %10 alınmıştı `[VARSAYIM]`; bu oranlar ölçülmedi.
- **Ajanlar arası iletişim:** ajan–araç için MCP, ajan–ajan için A2A (ikisi de açık protokol: Model Context Protocol, A2A protokolü). Serbest çoklu ajan diyaloğu varsayılan değildir: önceki sentetik simülasyonda benzer tasarruf için yaklaşık 12 kat daha fazla token harcandı `[VARSAYIM]` (rapor, Bölüm 1).

### 3.3 Yönlendirici ve izin modeli

Yönlendirme kararı üç girdiye dayanır: (1) isteğin türü, (2) yüklü paketin izin beyanı (Bölüm 4.6), (3) yerel politika (işletme yöneticisinin ayarları). Kurallar şunlar:

- **Yerelde kalma önceliği:** veri sınıfı `kisisel`, `musteri` veya `gizli` olan hiçbir girdi Katman 3'e gönderilmez. Bu kural paket beyanıyla gevşetilemez; yalnız yerel yönetici açıkça izin verebilir.
- **Yetenek eşleşmesi:** bir paket yalnız beyan ettiği araçları (`allowed-tools` + skillpack izinleri) çağırabilir; çalışma zamanı beyan dışı çağrıyı reddeder ve kaydeder.
- **Eskalasyon:** telefon → yerel sunucu, model güveni eşik altında kalırsa ya da gereken araç telefonda yoksa. Yerel sunucu → bulut, yalnız paket `cloud: optional` beyan etmiş ve kullanıcı o oturum için onaylamışsa; giden içerik bir anonimleştirme filtresinden geçer.
- **Fiziksel eylem kapısı:** `physical` profilli paketlerde her hareket komutu, hücrenin güvenlik katmanının (güvenlik PLC'si, alan tarayıcı) üstünde ve onun izin verdiği zarf içinde çalışır. İlk sürümde varsayılan mod öneri/simülasyon; gerçek hareket insan onayıyla açılır.

### 3.4 Veri akışı

**Tablo 5. Veri akışları ve sınırlar**

| Akış | Kaynak → hedef | Ne taşınır | Ne taşınmaz |
|---|---|---|---|
| Kullanım | Telefon → yerel sunucu → dikey ajan | İstek, bağlam, ilgili salt-okur kayıt referansı | — |
| Tanı çıktısı | Dikey ajan → kullanıcı | Tanı kartı: sorun, olası neden, kanıt, öneri, güven düzeyi | Otomatik eylem |
| Öğretme | Telefon/kamera/ekran → yerel sunucu | Ham gösterim (kullanıcı izniyle) | Ham gösterim dışarı çıkmaz |
| Paket yayımlama | Yerel sunucu → aynalar/P2P | Damıtılmış kurallar, anonim örnekler, isteğe bağlı politika ağırlıkları, imza, köken | Müşteri verisi, ham kayıt |
| Paket edinme | Aynalar/P2P → yerel depo | Paket + imza + günlük kanıtı + iptal listesi | — |
| Bulut (ops.) | Yerel sunucu → bulut | İzinli, anonimleştirilmiş özet | Kişisel/müşteri/gizli sınıf |
| Denetim izi | Tüm bileşenler → yerel günlük | Paket sürümü, karar, kanıt, onaylayan, süre | — |

---

## 4. Beceri paketi spesifikasyonu (taslak "skillpack" v0.1)

### 4.1 Tasarım ilkeleri

- **Geriye uyumluluk:** her skillpack geçerli bir Agent Skills dizinidir. Yalnız `SKILL.md` okuyan bir ajan da paketi kullanabilir; uzantılar bilinmiyorsa yok sayılır.
- **Ön bilgiyi kirletmeden ek dosya:** Agent Skills `metadata` alanı yalnız dizge→dizge eşlemesine izin verdiği için `[VERİ]` (Agent Skills spesifikasyonu) zengin yapı ayrı bir `skillpack.yaml` dosyasında tutulur. `SKILL.md` içinde yalnız bu dosyaya işaret eden iki anahtar bulunur.
- **İçerik adresleme:** her dosya SHA-256 özetiyle `checksums` listesine girer; paket kimliği, kanonik arşivin özetidir. Aynalar arasında aynı içerik aynı kimliği taşır.
- **Beyan edilmeyen yetki yoktur:** araç, ağ, dosya, cihaz ve bulut erişimi açıkça beyan edilir; çalışma zamanı beyanı uygular.
- **Veri minimizasyonu:** pakette ham müşteri verisi yer alamaz; örnekler anonimleştirilmiş ya da sentetiktir.

### 4.2 Klasör yapısı örneği

```text
depo-koli-ayirma/                 # dizin adı = name (Agent Skills kuralı)
├── SKILL.md                      # Agent Skills ön bilgi + talimatlar (zorunlu)
├── skillpack.yaml                # skillpack uzantı manifesti (bu öneri)
├── LICENSE.txt                   # lisans metni (SPDX kimliği manifestte)
├── scripts/                      # deterministik yardımcılar (ör. barkod doğrulama)
│   └── koli_sinifla.py
├── references/
│   ├── KURALLAR.md               # damıtılmış iş kuralları (insan okunur)
│   └── kurallar.yaml             # aynı kurallar, makine okunur
├── assets/
│   └── etiket_sablonu.json
├── examples/                     # yalnız anonim/sentetik girdi-çıktı örnekleri
│   ├── ornek_001.json
│   └── ornek_002.json
├── tests/                        # sandbox/simülasyon kabul testleri
│   ├── test_kurallar.yaml
│   └── sim/senaryo_karisik_koli.yaml
├── physical/                     # isteğe bağlı: robot profili
│   ├── robot_profile.yaml        # donanım, eklemler, sensörler, güvenlik zarfı
│   ├── dataset/                  # LeRobotDataset biçiminde gösterim (veya harici referans)
│   └── policy/                   # isteğe bağlı politika ağırlıkları + model kartı
└── provenance/
    ├── slsa.intoto.jsonl         # öğretme/derleme köken beyanı
    ├── anon_rapor.json           # anonimleştirme yöntemi ve kalan risk
    └── approvals.json            # insan onay kayıtları (takma adlı)
```

### 4.3 Örnek manifest: SKILL.md uzantısı

Aşağıdaki `SKILL.md`, Agent Skills spesifikasyonuna göre geçerlidir. Uzantı yalnız `metadata` içindeki iki dizge anahtarıdır:

```yaml
---
name: depo-koli-ayirma
description: Depoda karışık gelen kolileri etikete, ağırlığa ve hedef rampaya göre
  sınıflandırır; robot hücresi varsa ayırma sırasını önerir. Koli ayırma, rampa atama
  veya hatalı etiket tespiti istendiğinde kullan.
license: LicenseRef-Skillpack-Ticari-1.0. LICENSE.txt dosyasına bakın
compatibility: Yerel sunucu; MCP WMS salt-okur bağlayıcı; isteğe bağlı ROS 2
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
allowed-tools: Read mcp__wms__stok_oku mcp__wms__siparis_oku
---
# Depo koli ayırma
1. Koli etiketini oku; barkod geçersizse insana devret.
2. references/kurallar.yaml içindeki rampa kurallarını sırayla uygula.
3. Çıktı: tanı kartı (koli, önerilen rampa, gerekçe, güven). Eylemi operatör onaylar.
```

Uzantı manifesti (`skillpack.yaml`). Alan adları taslaktır:

```yaml
skillpack: "0.1-taslak"
id: "sha256:<kanonik-arsiv-ozeti>"               # içerik adresli kimlik
name: depo-koli-ayirma
version: "1.2.0"                          # SemVer (bkz. 4.5)
publisher:
  display: "Usta A. (takma ad)"
  identity: "oidc:https://kimlik.ornek.org|kullanici-123" # Sigstore/Fulcio kimliği
  org_role: "bireysel"                     # bireysel | isveren-adina | kurum
domain: { sector: lojistik, task: koli-ayirma, lang: [tr, en] }
components:
  procedure: SKILL.md
  rules: references/kurallar.yaml
  tests: tests/
  examples: examples/
  physical: physical/robot_profile.yaml          # isteğe bağlı
runtime:
  min_context_tokens: 8192
  model_class: ["local-7b-14b", "edge-1b-3b:limited"]
  tiers: { edge: limited, local: full, cloud: optional }
capabilities:                            # beyan edilmeyen yetki yok
  tools: ["mcp:wms/stok_oku:read", "mcp:wms/siparis_oku:read"]
  network: none                            # none | local | allowlist:[...]
  filesystem: { read: ["./"], write: ["./.cache"] }
  devices: ["camera:optional", "ros2:/cell1/*:suggest"] # suggest | act-with-approval
  data_classes_in: [operasyonel]
  cloud_egress: { allowed: false }
human_in_loop:
  mode: suggest                             # suggest | approve-each | approve-batch
  physical_motion: approve-each
privacy:
  raw_customer_data: false                     # zorunlu false
  examples: anonymized                         # anonymized | synthetic
  anonymization: { method: "alan-silme+genelleme", report: provenance/anon_rapor.json }
  differential_privacy: { applied: false }      # politika eğitimi için isteğe bağlı (epsilon, delta)
license:
  spdx: "LicenseRef-Skillpack-Ticari-1.0"
  terms: "LICENSE.txt"
  pricing: { model: "tek-seferlik", note: "ödeme standart dışı" } # free | tek-seferlik | abonelik
  rights_holders: [{ who: "Usta A.", share: "bilgi-amacli" }]
provenance:
  taught_on: "yerel-sunucu"
  base_models: ["qwen2.5-7b-instruct-q4 (Apache-2.0)"]
  slsa: provenance/slsa.intoto.jsonl
  approvals: provenance/approvals.json
  derived_from: []                         # türetilmiş paket ise üst paket kimlikleri
checksums: { "SKILL.md": "sha256:...", "references/kurallar.yaml": "sha256:..." }
signatures:
  - { type: sigstore-bundle, ref: "skillpack.sigstore.json" }
certification: { level: none }               # none | topluluk | vakif-dogrulanmis
```

> Örnekteki `LicenseRef-Skillpack-Ticari-1.0` ve `pricing` alanları, standardın üçüncü tarafların kendi paketlerinde lisans beyanı yapabilmesi için tanımladığı taslak alanlardır. Bu depo ve standart çalışması ticari değildir; ödeme altyapısı kapsam dışıdır (Bölüm 2.2, 7.1 ve 8).

### 4.4 Manifest alanları

**Tablo 6. skillpack.yaml alanları (taslak)**

| Alan | Zorunlu | Açıklama |
|---|---|---|
| skillpack, id, name, version | Evet | Spesifikasyon sürümü, içerik özetli kimlik, Agent Skills adıyla aynı ad, SemVer sürüm |
| publisher | Evet | Görünen ad (takma ad olabilir), doğrulanabilir imza kimliği, `org_role` (bireysel / işveren adına / kurum); sahiplik tartışmaları için (Bölüm 8.3) |
| domain | Evet | Sektör, görev, dil; keşif ve yönlendirme için |
| components | Evet | Prosedür, kurallar, testler, örnekler, isteğe bağlı fiziksel profil |
| runtime | Evet | Asgari bağlam, model sınıfı, katman uygunluğu (edge/local/cloud) |
| efficiency | Hayır | İsteğe bağlı dizgeler: asgari model boyutu, ölçülmüş token/görev, Wh/görev, ölçüm yöntemi (Bölüm 2.3). Aynı dizgeler `metadata` anahtarı olarak tekrarlanabilir |
| capabilities | Evet | Araçlar, ağ, dosya sistemi, cihazlar, girdi veri sınıfları, bulut çıkışı |
| human_in_loop | Evet | Öneri / tek tek onay / toplu onay; fiziksel hareket için ayrı kural |
| privacy | Evet | `raw_customer_data: false` zorunlu; örnek türü; anonimleştirme raporu; isteğe bağlı diferansiyel gizlilik parametreleri |
| license | Evet | SPDX kimliği veya LicenseRef; koşullar dosyası; fiyat modeli ve hak sahipleri (bilgi amaçlı) |
| provenance | Evet | Öğretildiği ortam, temel modeller ve lisansları, SLSA/in-toto beyanı, onay kayıtları, türetme zinciri |
| checksums, signatures | Evet | Dosya özetleri ve Sigstore paketi |
| certification | Hayır | Topluluk ya da vakıf doğrulama düzeyi (Bölüm 6.5) |

### 4.5 Sürümleme

- **SemVer:** MAJOR = kural/çıktı şeması uyumsuz değişti ya da yetki genişledi; MINOR = geriye uyumlu yeni kural/örnek; PATCH = düzeltme, ek test.
- Yetki genişlemesi her zaman MAJOR'dır ve yerel depoda otomatik güncellenmez; kullanıcı yeni izinleri onaylar.
- **Değişmezlik:** yayımlanmış bir sürümün içeriği değişmez; düzeltme yeni sürümdür. Geri çekme iptal listesiyle yapılır (Bölüm 6.3).
- Spesifikasyon sürümü (`skillpack`) paket sürümünden bağımsızdır. Doğrulayıcı bilinmeyen alanları uyarıyla geçer, bilinmeyen MAJOR spesifikasyonu reddeder.

### 4.6 Yetenek ve izin beyanları

**Tablo 7. İzin sınıfları**

| Sınıf | Değerler | Çalışma zamanı davranışı |
|---|---|---|
| tools | `mcp:<sunucu>/<araç>:read\|write` | Yalnız listelenen araçlar; write ilk sürümde her çağrıda insan onayı |
| network | none \| local \| allowlist | Varsayılan none; allowlist alan adları kullanıcıya gösterilir |
| filesystem | okuma/yazma yolları | Paket dizini dışına yazma yok (sandbox) |
| devices | camera, mic, ros2 konu/servis, opcua düğüm | `suggest` (yalnız öneri) veya `act-with-approval` |
| data_classes_in | operasyonel, kisisel, musteri, gizli | Kişisel/müşteri/gizli girdiler Katman 3'e çıkmaz |
| cloud_egress | allowed + amaç | Kullanıcı oturum bazında onaylar; giden içerik anonimleştirme filtresinden geçer |

### 4.7 Donanım ve robot profili

Fiziksel bileşen isteğe bağlıdır ve yeni bir veri formatı icat etmez. Gösterim verisi için birincil hedef LeRobotDataset biçimidir (Parquet + MP4/görüntü `[VERİ]`; LeRobotDataset belgeleri, LeRobot deposu). Open X-Embodiment'in kullandığı RLDS biçimi için referans uygulamada bir dönüştürücü yer alır (Open X-Embodiment makalesi). `robot_profile.yaml` şunları beyan eder:

- **Gövde:** robot tipi (kol, mobil, tutucu), serbestlik derecesi, eklem sınırları, uç efektör, kalibrasyon referansı; varsa URDF dosyası.
- **Sensörler:** kamera konumları/çözünürlükleri, kuvvet-tork, barkod okuyucu.
- **Arayüz:** ROS 2 konu/servis adları ve mesaj tipleri (ROS 2 belgeleri); PLC/hücre verisi için OPC UA düğüm kimlikleri (OPC UA (OPC Foundation)).
- **Güvenlik zarfı:** hız/kuvvet sınırları, yasak bölgeler, gereken güvenlik donanımı. Bu zarf bilgilendiricidir; uyumluluk sahadaki güvenlik sisteminin ve yetkin kişinin sorumluluğundadır. ISO 10218, ISO/TS 15066 ve AB Makine Tüzüğü 2023/1230 gibi çerçevelerin uygulanabilirliği ayrıca teknik/hukuki inceleme ister `[EKSİK]`.
- **Politika:** isteğe bağlı ağırlıklar + model kartı (eğitim verisi özeti, değerlendirme, bilinen başarısızlıklar). Ağırlıklar farklı bir robota taşınabilirliği garanti etmez; profil uyumsuzsa çalışma zamanı paketi yalnız procedure modunda yükler.

### 4.8 Köken ve lisans

Köken beyanı SLSA ve in-toto biçimini izler: paketin hangi yerel ortamda, hangi temel modellerle, hangi gösterimlerden (yalnız özetleri) ve kimlerin onayıyla üretildiği. Lisans alanı SPDX lisans listesi kimliği ya da `LicenseRef-` kullanır. Açık paketler için Apache-2.0 (kod/kural) ve CC-BY-4.0 (veri), üçüncü tarafların ticari paketleri için standart bir "Skillpack ticari lisans" şablonu önerilir; şablonun hukuki metni hazırlanmadı `[EKSİK]`. Temel model lisansları (ör. Qwen2.5 için Apache-2.0 `[VEKİL]`) manifestte açıkça listelenir. Türetilmiş politika ağırlıklarının lisans uyumu, doğrulayıcının uyarı verdiği bir kontroldür.

### 4.9 Gizlilik kuralları

- **Ham müşteri verisi yok:** `raw_customer_data: false` zorunlu. Doğrulayıcı örneklerde kişisel veri kalıplarını (T.C. kimlik no, telefon, e-posta, IBAN, plaka, yüz görüntüsü) tarar ve uyarı verir. Bu tarama yardımcıdır, garanti değildir.
- **Anonimleştirilmiş ya da sentetik örnekler:** alan silme, genelleme, takma adlandırma; görüntüde yüz/etiket bulanıklaştırma. Yöntem ve kalan risk `anon_rapor.json` içinde beyan edilir.
- **İsteğe bağlı diferansiyel gizlilik:** paket politika ağırlıkları ya da öğrenilmiş istatistikler içeriyorsa eğitim DP-SGD ile yapılabilir (ör. Opacus (diferansiyel gizlilik)); (ε, δ) değerleri beyan edilir. DP yalnız istatistiksel bir sınır sağlar; fayda kaybı göreve göre değişir ve bu çalışmada ölçülmedi `[EKSİK]`.
- **Neden gerekli:** paylaşılan eğitim verisinden üyelik çıkarımı saldırıları belgelenmiştir `[VERİ]` (Üyelik çıkarımı saldırıları anketi (arXiv)). KVKK/GDPR açısından hukuki analiz yapılmadı `[EKSİK]`.

---

## 5. Öğretme döngüsü

Hedef kullanıcı yazılım geliştirici değildir. Döngü, ustanın bildiği işi gösterip anlatmasını ve sistemin bunu doğrulanabilir kurallara çevirmesini sağlar. Tüm adımlar yerel sunucuda çalışır.

**Şekil 2.** Öğretme döngüsü: yakala → damıt → sandbox/simülasyon testi → insan onayı → paketle ve imzala; başarısızlıkta damıtmaya dönüş.

**Tablo 8. Öğretme döngüsü aşamaları**

| Aşama | Girdi | İşlem | Çıktı | Geçiş kapısı |
|---|---|---|---|---|
| 1. Yakalama | Ekran kaydı, ses anlatımı, kamera; robotta teleoperasyon/kinestetik gösterim | Kullanıcı izniyle kayıt; telefon veya yerel istasyon; hassas alanlar yakalama sırasında maskelenir | Ham gösterim (yalnız yerelde) | Görev başına asgari gösterim sayısı (pilotla belirlenecek `[EKSİK]`) |
| 2. Damıtma | Ham gösterim + anlatım | Yerel LLM adımları, karar noktalarını ve araç çağrılarını çıkarır; kurallar `kurallar.yaml` olarak yazılır; usta soruları yanıtlar (etkileşimli) | Taslak `SKILL.md`, kurallar, örnekler; robotta LeRobotDataset bölümleri | Her kural en az bir kanıt gösterimine bağlı |
| 3. Test | Taslak paket | Kayıtlı gösterimleri tekrar oynatma; kenar durumları; robotta Gazebo / MuJoCo simülasyonu; beyan dışı araç çağrısı denetimi | Test raporu (geçen/kalan, hata türleri) | Kabul testlerinin tamamı geçer; başarısızlar açıkça listelenir |
| 4. İnsan onayı | Test raporu + fark raporu | Usta ve (varsa) işyeri sorumlusu kuralları okur, düzeltir, onaylar; sahiplik/`org_role` beyanı | `approvals.json` | İşyerinde iki kişi kuralı önerilir |
| 5. Paketleme | Onaylı içerik | Anonimleştirme + PII taraması, manifest, köken beyanı, Sigstore imzası, günlüğe kayıt | İmzalı skillpack | Doğrulayıcı hatasız geçer |

**Gerçekçilik notu.** 7–14B sınıfı modellerin karmaşık gösterimlerden güvenilir kural çıkarma başarısı ölçülmedi `[EKSİK]`. Bu yüzden döngü, modeli "kural yazan" değil "taslak öneren" konumunda tutar; nihai kuralı insan onaylar. Robot politikalarında öğrenme verimliliği görevden göreve büyük fark gösterir. LeRobot ekosistemindeki veri setlerinin örneklemde yalnız ~%38'inin `[VERİ]` kullanılabilir bulunması (LeRobot HF sayımı), test ve sertifikasyon aşamasının neden zorunlu olduğunu gösterir.

---

## 6. Dağıtım ve güven

Hedef, merkezi bir dükkâna bağımlı olmadan şu sorulara cevap verebilmek: "Bu paketi kim yaptı, değiştirildi mi, geri çekildi mi?" Yöntemlerin çoğu yazılım paketi dünyasında var: Sigstore, SLSA, The Update Framework (TUF), in-toto. Bunların npm/PyPI/Maven gibi kayıtlarda yaygınlaştığı aktarılıyor `[VEKİL]` (Paket kayıtlarında imza ve beyanlar (nesbitt.io, 2026-10)). Beceri paketlerine uygulanmış bir örnek bulunamadı `[EKSİK]`.

### 6.1 İmzalama

- **Anahtarsız imza (varsayılan):** yayıncı OIDC kimliğiyle kısa ömürlü sertifika alır (Sigstore Fulcio modeli); imza şeffaflık günlüğüne yazılır. Uzun ömürlü anahtar yönetimi gerektirmez.
- **Anahtarlı imza (çevrim dışı/kurum):** hava boşluklu sahalar için donanım anahtarıyla imza; açık anahtar yayıncı kaydında.
- **Vakıf karşı imzası:** sertifikasyon düzeyi olan paketlerde vakfın ikinci imzası. Vakıf yalnız doğrulama sürecinin yapıldığını imzalar; paketin her koşulda güvenli olduğunu garanti etmez.

### 6.2 Şeffaflık günlüğü

Her yayın ve her iptal, yalnız eklemeli (append-only) bir Merkle günlüğüne yazılır (Sigstore şeffaflık günlüğü (Rekor)). İstemci, paketi kabul etmeden önce günlük kapsama kanıtını doğrular. Böylece sessizce değiştirilmiş paket ya da yalnız belirli kullanıcılara gösterilen sürüm tespit edilebilir. Vakıf kendi günlüğünü işletebilir ya da kamuya açık Sigstore örneğini kullanabilir; ikisinin işletme maliyeti ve hizmet düzeyi karşılaştırılmadı `[EKSİK]`.

### 6.3 İptal listesi

- **Format:** imzalı, sürümlü, zaman damgalı liste. Satırlar paket kimliği (özet), sürüm aralığı, gerekçe kodu (zararlı, güvenlik açığı, lisans ihlali, yanlış beyan, yayıncı talebi), ciddiyet ve tarih içerir.
- **Dağıtım:** TUF tarzı rol ayrımı (kök, zaman damgası, anlık görüntü, hedefler). Küçük ve sık güncellenen zaman damgası dosyası, eski listenin "dondurulmasına" karşı korur.
- **İstemci davranışı:** yerel depo listeyi periyodik çeker (aralık yerel politikadır; öneri: çevrimiçiyken günlük `[VARSAYIM]`). İptal edilen paket devre dışı kalır, kullanıcıya gerekçe gösterilir. Çevrim dışı sahalarda liste USB/aynayla taşınır ve son senkron tarihi arayüzde görünür.
- **Yetki:** iptal yalnız vakfın güvenlik ekibi rolüyle ya da yayıncının kendi geri çekme talebiyle yapılır; süreç ve itiraz yolu yönetişim belgesinde tanımlanır.

### 6.4 Aynalar ve P2P

Paketler içerik adresli olduğu için nereden indirildiği güveni etkilemez; güven imzadan ve günlükten gelir. Dağıtım kanalları: statik HTTP aynaları (üniversite, kamu kurumu, topluluk), IPFS ve BitTorrent BEP 3 gibi P2P ağlar, kurum içi aynalar, çevrim dışı medya. İndeks dosyası (paket kimliği → ad, sürüm, yayıncı, alan) da imzalıdır ve aynalanır. Merkezsiz dağıtımın beceri paketi ölçeğinde üretim kanıtı yok `[EKSİK]`; pilot en az iki bağımsız ayna ve bir P2P kanalıyla başlar.

### 6.5 İtibar ve sertifikasyon

**Tablo 9. Sertifikasyon düzeyleri (taslak)**

| Düzey | Kim verir | Ne anlama gelir | Ne anlama gelmez |
|---|---|---|---|
| none | — | İmzalı; yayıncı kimliği doğrulanabilir | İçerik incelenmedi |
| topluluk | En az iki bağımsız doğrulayıcı (yeniden üretilebilir test çalıştırma) | Testler bağımsız ortamda geçti; izin beyanı içerikle tutarlı | Saha güvenliği, hukuki uygunluk |
| vakif-dogrulanmis | Vakıf sertifikasyon programı (maliyet karşılayan bir ücret olabilir) | Belgelenmiş inceleme listesi uygulandı; fiziksel profilde simülasyon testleri yapıldı | Sahada her koşulda güvenli çalışma garantisi |

İtibar sinyalleri (indirme sayısı, kullanıcı geri bildirimi, olay raporları) yerel istemcilerden isteğe bağlı ve anonim toplanabilir. Sahte itibar (Sybil) riskine karşı sinyaller imzalı kimliklere bağlanır ve tek başına sertifikasyonun yerine geçmez.

---

## 7. Yönetişim

### 7.1 Vakfın rolü

- Spesifikasyonu ve JSON şemalarını açık bir süreçle sürdürmek (öneri → taslak → kabul; uyumluluk test seti).
- Kök anahtarları ve iptal listesini işletmek; güvenlik ekibi ve olay müdahale süreci.
- Sertifikasyon programı ve doğrulayıcı akreditasyonu.
- Referans uygulamaların (doğrulayıcı, yerel depo, yönlendirici) bakımını koordine etmek.
- Ticari faaliyet yapmamak: pazar yeri işletmemek, ödemeye aracılık etmemek. Tarafsızlık bunu gerektirir.

### 7.2 Seçenekler

**Tablo 10. Yönetişim seçenekleri**

| Seçenek | Artılar | Eksiler |
|---|---|---|
| A. AAIF içinde çalışma grubu / alt proje (önerilen hedef) | Agent Skills ve MCP ile aynı çatı; mevcut hukuki/finansal altyapı; benimseyen platformlara doğrudan erişim; tekrar icat yok | Kabul AAIF süreçlerine ve önceliklerine bağlı; büyük üyelerin ağırlığı; fiziksel/robot alanı AAIF'in odağı dışında kalabilir |
| B. Yeni LF projesi / bağımsız vakıf | Tam odak (fiziksel + saha); kendi yönetişim kuralları | Kuruluş ve sürdürme maliyeti; Agent Skills'ten parçalanma riski; finansman yükü |
| C. Vakıfsız topluluk projesi (GitHub org) | Hızlı başlangıç, sıfır maliyet | Kök anahtar ve iptal için tarafsız güven yok; kurumsal benimseme zor |
| D. Mevcut vakıflara dağıtık katkı (OpenSSF + ROS/OPC toplulukları) | İmza yöntemi OpenSSF'te, robot arayüzleri kendi topluluklarında gelişir | Tek bir "skillpack" kimliği oluşmaz; koordinasyon zor |

**Öneri:** C ile başlamak (spesifikasyon taslağı + referans kod), olgunlaşınca A'ya geçmek. Yani AAIF bünyesinde, Agent Skills'in "skillpack: fiziksel profil ve güven" uzantısı için bir çalışma grubu önermek. İmza kısmında OpenSSF, robot kısmında ROS ve LeRobot topluluklarıyla iş birliği yapılır. AAIF'in çalışma grubu açma süreci ve kriterleri bu çalışmada doğrulanmadı `[EKSİK]` (AAIF sitesi).

### 7.3 Üyelik ve finansman emsalleri

**Tablo 11. Vakıf finansman emsalleri**

| Gösterge | Değer | Etiket / kaynak |
|---|---|---|
| Linux Foundation 2025 gelir tahmini | ~$311,3M | `[VEKİL]` Phoronix: LF 2025 raporu özeti |
| LF 2025 gider / üyelik+bağış | ~$299M / $133M | `[VEKİL]` Phoronix: LF 2025 raporu özeti |
| LF üye sayısı | 2.126 | `[VERİ]` LF 2025 Yıllık Raporu (PDF) |
| LF proje topluluğu | ~1.500 | `[VERİ]` LF 2025 Yıllık Raporu (PDF) |
| LF AI & Data | 76 proje · 52K katkıcı (2025-05) | `[VERİ]` LF AI & Data Insights |
| AAIF Platinum üyeler (kuruluşta) | AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI | `[VERİ]` LF AAIF duyurusu |

Kaynak: `beceri_standardi/veri_tablosu.csv`, `kaynaklar.csv`

LF modelinde gelir ağırlıklı olarak üyelik, proje hizmetleri, eğitim ve etkinliklerden gelir `[VEKİL]`. Bu proje için gerçekçi finansman yolları: (1) AAIF'in mevcut bütçesi içinde çalışma grubu, (2) açık kaynak güvenliği ve dijital altyapı hibeleri, (3) yalnız maliyet karşılayan sertifikasyon ücretleri. Hibe programlarının uygunluk koşulları taranmadı `[EKSİK]`. Üyelik kademeleri için: LF üyelik sayfası.

---

## 8. Üzerine kurulabilecek iş modelleri ve yaratıcı sahipliği

Standart ve vakıf ticari değildir. Aşağıdaki modeller üçüncü tarafların (ustalar, entegratörler, kooperatifler, şirketler) standart üzerinde yapabilecekleridir. Hiçbirinin gelir potansiyeli ölçülmedi `[EKSİK]`. Bu bölüm, bu deponun bir ticari ürün veya şirket planı olduğu anlamına gelmez.

### 8.1 Modeller

**Tablo 12. Standart üzerinde (üçüncü taraf) iş modelleri**

| Model | Kim | Açıklama | Emsal / not |
|---|---|---|---|
| Ücretsiz açık paket | Usta, topluluk, kamu | Apache-2.0 / CC-BY; itibar ve görünürlük | Agent Skills ekosistemi; n8n topluluk şablonları |
| Ücretli paket (lisans) | Usta, küçük atölye | Tek seferlik veya abonelik; lisans manifestte, ödeme dış kanalda | UiPath partner marketplace; n8n/Make kısmi yaratıcı satışı (gelir kırılımı `[EKSİK]`) |
| Destek ve uyarlama | Entegratör / mini-servis | Paketi işletmeye kurma, bağlayıcı ayarı, eğitim | Önceki çalışmada başa baş 47 müşteri `[HESAP]` (mini_sunucu; şirket varsayımlarıyla) |
| Sertifikasyon hizmeti | Akredite doğrulayıcı | Paket inceleme, simülasyon testleri | Vakıf düzeyinde maliyet karşılama |
| Kurumsal dağıtım | Yazılım şirketi | Desteklenen yerel depo, filo yönetimi | Red Hat emsali: IBM Hybrid Cloud (Red Hat) 2025 geliri $7,327B `[VERİ]` (IBM SEC dosyası) |

Red Hat emsali, açık yazılım üzerine abonelik/destek gelirinin mümkün olduğunu gösterir. Bu ölçeğin beceri paketlerine aktarılabileceğine dair kanıt yoktur; emsal yalnız iş modelinin türünü gösterir.

### 8.2 Mikro ölçek

Projenin ana tezi, büyük araçların inmediği mikro ölçektir (tek usta, küçük atölye). Küresel ~196M mikro işletme `[VEKİL]` ve Türkiye'de ~3,93M KOBİ (girişimlerin %99,6'sı) `[VEKİL]` aktarılıyor. Bu sayılar pazar büyüklüğü değil, yalnız ölçek bağlamıdır. Mikro paylaşımda temel engeller işlem maliyeti, lisansı uygulatmanın zorluğu (paket kopyalanabilir) ve destek beklentisidir. Standart lisansı uygulatmaz; yalnız beyan eder ve iptal/itibar yoluyla ihlali görünür kılar. DRM önerilmez, çünkü açık ve taşınabilir tasarımla çelişir.

### 8.3 Yaratıcı sahipliği: çalışan mı, işveren mi?

Bir ustanın işyerinde öğrettiği becerinin kime ait olduğu, standardın çözemeyeceği ama beyan altına alabileceği bir sorundur:

**Tablo 13. Sahiplik senaryoları (hukuki görüş değildir)**

| Durum | Olası sahiplik eğilimi | Standardın katkısı |
|---|---|---|
| Usta kendi zamanında, kendi bilgisiyle, genel bir beceriyi öğretir | Usta (ülke hukukuna ve sözleşmeye bağlı) | `org_role: bireysel` + işveren verisi kullanılmadığı beyanı |
| Usta işyerinde, iş süresinde, işyeri sistem/verisiyle öğretir | Çoğu hukukta işveren ağırlıklı. Türkiye'de FSEK md.18, çalışan ve memurların işlerini görürken meydana getirdikleri eserlerde hakları çalıştırana bağlar `[VEKİL]` (5846 sayılı FSEK) | `org_role: isveren-adina` + işveren imzası (iki imza) |
| Beceri işverene özgü ticari sır içerir (müşteri listesi, tarif, süreç parametresi) | Ticari sır koruması (AB: AB Ticari Sırlar Direktifi 2016/943; Türkiye'de ayrı bir ticari sır kanunu yok, haksız rekabet ve sözleşme hükümleri uygulanır `[VEKİL]`) | Doğrulayıcı uyarısı + yayın öncesi "gizli bilgi yok" beyanı; yine de hukuki değerlendirme gerekir |
| Paylaşım (usta + işveren) | Sözleşmeye bağlı | Manifestte çoklu hak sahibi ve pay beyanı (bilgi amaçlı) |

**Hukuki uyarı.** Bu bölüm hukuki görüş değildir. Çalışan bilgisi, ticari sır ve eser sahipliği ülkeden ülkeye değişir. Bu çalışmada avukat görüşü alınmadı `[EKSİK]`. Standart yalnız beyan ve köken alanları sunar; beyanın doğruluğundan yayıncı sorumludur.

---

## 9. Güvenlik ve gizlilik tehdit modeli

Model deposu tedarik zinciri saldırıları belgelenmiştir `[VERİ]` (Acronis: HF ve OpenClaw tedarik zinciri saldırıları; CSA: zararlı model depoları notu (PDF)). Beceri paketleri metin talimat + betik + isteğe bağlı model ağırlığı içerdiği için saldırı yüzeyi hem yazılım paketlerini hem model depolarını kapsar.

**Tablo 14. Tehdit modeli**

| Tehdit | Örnek | Etki | Önlem | Kalan risk |
|---|---|---|---|---|
| Zararlı paket | Betikte veri sızdırma; kötü niyetli kural | Veri kaybı, yanlış iş kararı | İmza + günlük; izin beyanı + sandbox; ağ varsayılan kapalı; iptal listesi; topluluk incelemesi | İmzalı ama kötü niyetli yayıncı; ilk tespitte gecikme |
| Talimat/araç zehirleme (prompt injection) | SKILL.md ya da örnekte gizli talimat; MCP araç açıklamasında yönlendirme | Beyan dışı araç çağrısı denemesi, yanlış öneri | Çalışma zamanı beyan dışı çağrıyı reddeder; araç açıklamaları özetle sabitlenir; yazma işlemlerinde insan onayı | Beyan içi araçlarla yanlış yönlendirme |
| Zararlı model ağırlığı | Güvensiz serileştirme (pickle) ile kod çalıştırma | Sunucunun ele geçirilmesi | Yalnız safetensors/GGUF gibi güvenli formatlar; doğrulayıcı diğerlerini reddeder | Formatın kendisindeki açıklar |
| Tedarik zinciri / bağımlılık | Betik bağımlılığının ele geçirilmesi | Kod çalıştırma | Bağımlılık sabitleme + özet; SBOM; çevrim dışı paketleme | Yeni açıklar |
| Üyelik çıkarımı / veri sızıntısı | Politika ağırlıklarından eğitim örneği çıkarımı (Üyelik çıkarımı saldırıları anketi (arXiv)) | Müşteri/işyeri bilgisinin ifşası | Ham veri yok; anonim örnek; isteğe bağlı DP; PII taraması | Anonimleştirmenin tersine çevrilmesi; DP kullanılmayan paketler |
| Fiziksel robot güvenliği | Yanlış politika, profil uyumsuzluğu, sensör hatası | Yaralanma, ekipman hasarı | Varsayılan öneri/simülasyon modu; güvenlik PLC önceliği; hareket başına onay; profil uyumsuzsa fiziksel mod kapalı | Saha güvenlik sisteminin eksikliği; insan hatası |
| İptal listesinin engellenmesi / dondurulması | Saldırganın eski listeyi sunması | İptal edilmiş paket çalışmaya devam eder | TUF tarzı zaman damgası rolü; son senkron yaşı uyarısı | Uzun süre çevrim dışı sahalar |
| Sahte itibar / taklit ad | Benzer adlı paket (typosquatting), sahte yorum | Yanlış paket kurulumu | Doğrulanmış yayıncı kimliği; ad benzerliği uyarısı; itibarın imzalı kimliğe bağlanması | Sosyal mühendislik |
| Kök anahtarın ele geçirilmesi | Vakıf anahtarının çalınması | Sahte sertifikasyon | Çoklu imza eşiği; çevrim dışı kök; anahtar rotasyonu | Kurumsal operasyon hatası |
| Sorumluluk belirsizliği | Paket öneri verdi, insan uyguladı, zarar doğdu | Hukuki uyuşmazlık | "Öneri, karar değil" duruşu; denetim izi; lisansta garanti reddi; sertifikasyonun sınırlarının açık yazılması | Ülke hukukuna göre sorumluluk dağılımı `[EKSİK]` |

---

## 10. Referans uygulama planı

### 10.1 Açık kaynak bileşenler

**Tablo 15. Referans uygulamada kullanılacak açık bileşenler**

| Katman | Bileşen | Rol |
|---|---|---|
| Model çalıştırma | Ollama, llama.cpp | Yerel çıkarım (GGUF, Q4) |
| Model | Qwen2.5 deposu 7B/14B (Apache-2.0 `[VEKİL]`); telefon için 1–3B sınıfı | Damıtma, tanı açıklaması, yönlendirme yedeği |
| Araç/ajan protokolü | Model Context Protocol, A2A protokolü | Araç bağlayıcıları, ajanlar arası devir |
| Beceri formatı | Agent Skills spesifikasyonu + Agent Skills GitHub organizasyonu | Temel format; doğrulayıcı (skills-ref) genişletilir |
| Robot verisi/politika | LeRobot deposu, ROS 2 belgeleri | Gösterim kaydı, veri seti, politika eğitimi; robot arayüzü |
| Endüstriyel veri | OPC UA (OPC Foundation) | PLC/hücre durumunu salt-okur almak |
| Simülasyon | Gazebo, MuJoCo | Fiziksel paket testleri |
| İmza/köken/güncelleme | Sigstore, SLSA, in-toto, The Update Framework (TUF) | İmza, şeffaflık günlüğü, köken, iptal dağıtımı |
| Dağıtım | IPFS, HTTP aynaları | İçerik adresli dağıtım |
| Gizlilik | Opacus (diferansiyel gizlilik) | İsteğe bağlı DP eğitimi |

### 10.2 Yazılacak bileşenler

- **skillpack CLI:** `init`, `validate`, `pack`, `sign`, `verify`, `publish`, `revoke-check`.
- JSON Schema dosyaları (`skillpack.yaml`, `robot_profile.yaml`, iptal listesi, indeks).
- Yerel depo servisi: paket indirme, doğrulama, iptal senkronu, izin onay arayüzü.
- Yönlendirici: kural tabanlı eşleştirme + yerel LLM yedeği + izin uygulama + denetim izi.
- Öğretme istasyonu: ekran/ses/kamera yakalama, ustaya sade bir damıtma arayüzü, test çalıştırıcı, onay ekranı.
- Telefon istemcisi (ince): yakalama, soru-cevap, tanı kartı görüntüleme.

### 10.3 MVP kapsamı

**Tablo 16. MVP kapsamı**

| Kapsamda | Kapsam dışı (MVP) |
|---|---|
| Spesifikasyon v0.1 + şemalar + doğrulayıcı | Ödeme / pazar yeri arayüzü |
| Sigstore ile imza + doğrulama; basit iptal listesi (TUF rollerinin asgari alt kümesi) | Vakıf sertifikasyon programı |
| Tek yerel sunucu + tek telefon istemcisi; Ollama + Qwen2.5 7B | Çoklu saha filo yönetimi |
| İki dijital örnek beceri (ör. depo stok sapması tanısı, ses kaydı düzeltme iş akışı) | Gerçek robotta hareket (yalnız simülasyon + öneri) |
| Bir fiziksel örnek: koli ayırma, LeRobotDataset + simülasyon testi | Diferansiyel gizlilikli eğitim (yalnız arayüz) |
| İki bağımsız HTTP aynası + bir IPFS kanalı | Bulut katmanı (yalnız kapalı/açık anahtarı) |

---

## 11. Yol haritası

Süreler göreli aylarla verilmiştir (A0 = başlangıç). Gönüllü/hibe destekli bir ekibin hızı bilinmediği için tüm süreler `[VARSAYIM]` niteliğindedir.

Görev düzeyinde ayrıntılı ve "Başlamadı" işaretli plan bu depodaki [ROADMAP.md](../ROADMAP.md) dosyasındadır.

**Tablo 17. Faz planı**

| Faz | Süre | Kilometre taşları | Çıkış ölçütü |
|---|---|---|---|
| F0 — Hazırlık | A0–A2 | Spesifikasyon taslağı v0.1 yayımı; geri bildirim çağrısı; hukuki ön görüş | En az bir dış teknik inceleme; yazılı hukuki görüş alındı |
| F1 — Çekirdek | A2–A6 | Şemalar + doğrulayıcı CLI; Sigstore imza/doğrulama; iki dijital örnek paket | Paket uçtan uca imzalanıp başka bir makinede doğrulanıyor |
| F2 — Yerel çalışma | A5–A9 | Yerel depo + yönlendirici + izin uygulama; telefon istemcisi; öğretme döngüsü prototipi; görev başına verim düzeneği (Bölüm 2.3) | Geliştirici olmayan bir usta, yardımla bir beceriyi paketleyebiliyor |
| F3 — Fiziksel profil | A8–A12 | `robot_profile` şeması; LeRobotDataset bağlantısı; koli ayırma simülasyon testi | Fiziksel paket simülasyonda kabul testlerini geçiyor |
| F4 — Dağıtım ve iptal | A10–A14 | İndeks formatı; aynalar + IPFS; iptal listesi + TUF rolleri; iptal tatbikatı | Bir test paketinin iptali tüm pilot istemcilerde tespit ediliyor |
| F5 — Pilot | A12–A18 | 2–3 gönüllü pilot saha; Bölüm 12'deki ölçümler | Ölçüm raporu; olay kayıtları |
| F6 — Yönetişim | A12–A24 | AAIF çalışma grubu önerisi; spesifikasyon v1.0 adayı | Öneri değerlendirmeye alındı (sonuç belirsiz) |

---

## 12. Başarı ölçütleri

Hedef değerler bilinçli olarak sayı içermiyor, çünkü taban ölçümü yok. İlk pilotta taban ölçülür, hedefler sonra belirlenir `[EKSİK]`. Bir paketin standart profile girmesi Bölüm 2.3'teki üçlü kabul ölçütüyle önerilir. Buradaki liste, projenin pilot başarı ölçütleridir. Eşikler `[VARSAYIM]`; görev başına enerji kazancı `[EKSİK]`.

**Tablo 18. Başarı ölçütleri**

| Alan | Ölçüt | Nasıl ölçülür |
|---|---|---|
| Spesifikasyon | Bağımsız uygulama sayısı (doğrulayıcıyı geçen üçüncü taraf çalışma zamanı) | Uyumluluk test seti sonuçları |
| Taşınabilirlik | Aynı paketin değişiklik olmadan çalıştığı çalışma zamanı sayısı | Çapraz test matrisi |
| Güven | İmza doğrulama başarısı; iptalin istemcilere yayılma süresi | Tatbikat ölçümü |
| Öğretme | Geliştirici olmayan kullanıcının paketleme süresi; dış yardım ihtiyacı | Pilot gözlemi, görev süresi |
| Kalite | Kabul testi geçme oranı; sahada tanı kartlarının onay/düzeltme/red oranı | Yerel denetim izi |
| Performans | Yerel sunucuda gecikme (p50/p95), token/s, bellek | Referans donanımda ölçüm |
| Gizlilik | PII taramasında yakalanan/kaçan örnek; DP kullanılan paket payı | Kırmızı takım testi |
| Güvenlik | Kırmızı takım bulguları; olay sayısı ve kapanma süresi | Güvenlik süreç kayıtları |
| Topluluk | Katkıcı, yayıncı ve ayna sayısı | Depo istatistikleri |
| Ekonomik (dolaylı) | Lisans beyanlı paket var mı; yaratıcıların gönüllü bildirdiği gözlem (bu proje gelir toplamaz) | Anonim anket |

---

## 13. Riskler ve açık sorular

**Tablo 19. Riskler (olasılıklar nitel; ölçülmedi)**

| Risk | Olasılık / etki | Azaltma |
|---|---|---|
| Agent Skills sürdürücüleri benzer uzantıyı kendileri yapar ya da reddeder | Belirsiz / yüksek | Erken iletişim; uzantıyı ayrık dosyada tutmak; gerekirse doğrudan upstream katkı |
| Benimseme olmaz (yayıncı çıkmaz) | Belirsiz / yüksek | Gerçek pilot ihtiyacından doğan paketler; ücretsiz örnek paketler |
| Yerel 7–14B modeller damıtmada yetersiz kalır | Belirsiz / orta | İnsan onaylı taslak modu; kuralların deterministik kısmını betiklere taşımak |
| Fiziksel paket kaynaklı kaza | Düşük–orta / çok yüksek | Varsayılan öneri modu; güvenlik PLC önceliği; sertifikasyon sınırlarının açık yazılması |
| Ticari sır / çalışan bilgisi uyuşmazlığı | Orta / orta | `org_role` beyanı, iki imza, hukuki şablonlar |
| Zararlı paket kampanyası | Orta / yüksek | İptal tatbikatları, güvenlik ekibi, ağ varsayılan kapalı |
| Gönüllü kapasite ve finansman eksikliği | Yüksek / yüksek | Küçük MVP; hibe; vakıf çatısı |
| Parçalanma (birden çok rakip uzantı) | Orta / orta | AAIF çatısı altında birleştirme |

**Açık sorular**

- Agent Skills topluluğu fiziksel/robot uzantısını kapsam içinde görüyor mu? `[EKSİK]`
- Beceri paketleri için şeffaflık günlüğünü kim işletmeli; kamuya açık Sigstore örneği yeterli mi? `[EKSİK]`
- Robot politikaları farklı donanımlar arasında ne ölçüde taşınabilir; profil eşleştirme kuralları ne olmalı? `[EKSİK]`
- Lisans uygulatma olmadan sürdürülebilir bir mikro yaratıcı katkısı mümkün mü? `[EKSİK]`
- Türkiye'de çalışan bilgisi ve ticari sır için hukuki çerçeve `[EKSİK]`
- Sertifikasyonun vakıf için sorumluluk doğurup doğurmadığı; sigorta/sorumluluk sınırı `[EKSİK]`
- Telefon katmanında hangi model sınıfının pratikte yeterli olduğu `[EKSİK]`

---

## Ek A. Sözlük

**Tablo 20. Sözlük**

| Terim | Açıklama |
|---|---|
| Beceri (skill) | Bir ajanın belirli bir işi yapmasını sağlayan talimat, kural, betik ve kaynak bütünü |
| Beceri paketi (skillpack) | Bu önerideki uzantı: Agent Skills dizini + `skillpack.yaml` + imza/köken (+ isteğe bağlı fiziksel profil) |
| Agent Skills / SKILL.md | AAIF'e bağışlanan açık beceri formatı |
| AAIF | Agentic AI Foundation; Linux Foundation bünyesindeki ajanik yapay zekâ vakfı |
| MCP | Model Context Protocol; ajan–araç bağlantı protokolü |
| A2A | Agent2Agent; ajanlar arası iletişim protokolü |
| Dikey / yatay ajan | Tek alana odaklı ajan / alanlar arası yönlendirme ve koordinasyon yapan ajan |
| Gösterim (demonstration) | Bir işin insan tarafından yapılarak kaydedilmesi (ekran, ses, kamera, teleoperasyon) |
| Politika (policy) | Robotun gözlemden eyleme eşleme yapan öğrenilmiş modeli |
| LeRobotDataset | Hugging Face LeRobot'un robot veri formatı (Parquet + MP4/görüntü) |
| RLDS / Open X-Embodiment | Çoklu robot veri seti girişimi ve kullandığı veri biçimi |
| ROS 2 / OPC UA | Robot yazılım ara katmanı / endüstriyel veri iletişim standardı |
| Sigstore / Rekor / Fulcio | Anahtarsız imza altyapısı / şeffaflık günlüğü / kısa ömürlü sertifika otoritesi |
| SLSA / in-toto | Yazılım tedarik zinciri köken düzeyleri / beyan formatı |
| TUF | The Update Framework; rol ayrımlı güvenli güncelleme ve meta veri dağıtımı |
| İptal listesi | Geri çekilmiş paketlerin imzalı listesi |
| Diferansiyel gizlilik (DP) | Tek bir kaydın sonuca etkisini istatistiksel olarak sınırlayan yöntem; (ε, δ) parametreleri |
| Üyelik çıkarımı | Bir kaydın eğitim verisinde olup olmadığını modelden tahmin etme saldırısı |
| Tanı kartı | Sorun + olası neden + kanıt + öneri + güven; kararı insan verir |
| SPDX | Standart lisans tanımlayıcı listesi |

---

## Ek B. Kaynaklar

Proje dosyaları: `beceri_standardi/` (`ozet.md`, `veri_tablosu.csv`, `kaynaklar.csv`), `platform_tarama/` (`ozet.md`, `bosluk.md`, `oyuncular.csv`), `sektor_tarama/ozet.md`, `PROJE_NOTU.md`, `rapor/Yerel_Tani_Sistemi_Raporu.pdf`, `mini_sunucu/ozet.csv`.

### B.1 Tarama dosyalarındaki kaynaklar (`beceri_standardi/kaynaklar.csv`)

**Tablo 21. Tarama kaynakları**

| # | Kaynak | Tarih / dönem | Etiket |
|---|---|---|---|
| 1 | LF AAIF kuruluş duyurusu | 2025-12-09 | `[VERİ]` |
| 2 | Anthropic MCP bağışı + AAIF | 2025-12-09 | `[VERİ]` |
| 3 | OpenAI AGENTS.md bağışı | 2025-12-09 | `[VERİ]` |
| 4 | AAIF about | 2026-11 okuma | `[VERİ]` |
| 5 | Anthropic Agent Skills AAIF bağışı | 2026-10-22 | `[VERİ]` |
| 6 | Agent Skills specification | 2026-11 okuma | `[VERİ]` |
| 7 | LF 2025 Annual Report (Phoronix özeti) | 2025 | `[VEKİL]` |
| 8 | LF 2025 Annual Report PDF | 2025 | `[VERİ]` |
| 9 | LF AI & Data Insights | 2025-05 | `[VERİ]` |
| 10 | IBM SEC Hybrid Cloud Red Hat | 2025 | `[VERİ]` |
| 11 | LeRobot HF census | 2026-10-23 | `[VERİ]` |
| 12 | Open X-Embodiment paper | 2023+ | `[VERİ]` |
| 13 | LeRobot models HF | 2026-11 okuma | `[VERİ]` |
| 14 | Voxel51 LeRobot guide | 2026-11 | `[VEKİL]` |
| 15 | n8n 5k templates | 2025-09-04 | `[VERİ]` |
| 16 | Template marketplace karşılaştırması | 2026-10-25 | `[VEKİL]` |
| 17 | UiPath Marketplace intro | 2026 okuma | `[VEKİL]` |
| 18 | UiPath FY2026 gelir (Quantumrun derleme) | FY2026 (31 Ocak 2026 bitiş) | `[VEKİL]` |
| 19 | RPA boyut aralığı (üç firma) | 2026 | `[VEKİL]` |
| 20 | Dataintelo dar RPA | 2025–2034 | `[VEKİL]` |
| 21 | Edge AI IDC/eenews | 2025–2028 | `[VEKİL]` |
| 22 | Edge AI Research and Markets | 2025–2026 | `[VEKİL]` |
| 23 | Eurostat AI in enterprises | 2025 | `[VERİ]` |
| 24 | TÜİK KOBİ 2024 (TV5 aktarım) | 2024 | `[VEKİL]` |
| 25 | TÜİK AI kullanım (Cumhuriyet) | 2025 | `[VEKİL]` |
| 26 | OECD TR AI (Dünya) | 2025 civarı | `[VEKİL]` |
| 27 | Statista global SME | 2023 | `[VEKİL]` |
| 28 | Caribou mikro işletme | 2023 | `[VEKİL]` |
| 29 | HF/OpenClaw supply chain | 2026 | `[VERİ]` |
| 30 | CSA malicious AI model repos | 2026-05 | `[VERİ]` |
| 31 | Membership inference survey | 2025 | `[VERİ]` |
| 32 | Sigstore/SLSA package signing | 2026-10 | `[VEKİL]` |
| 33 | OpenSSF 2025 Annual Report | 2025-12 | `[VERİ]` |
| 34 | HF open models summer 2026 blog | 2026 yaz | `[VEKİL]` |
| 35 | MCP registry 55773 | 2026-11-03 | `[VEKİL]` |
| 36 | Ollama library count | 2026-11-07 | `[VEKİL]` |

### B.2 Bu dokümanda ayrıca kullanılan kaynaklar

**Tablo 22. Ek kaynaklar (erişim: 2026-11-09)**

| # | Kaynak |
|---|---|
| 1 | Agent Skills spesifikasyonu (alan tanımları) |
| 2 | Agent Skills GitHub organizasyonu |
| 3 | AAIF sitesi |
| 4 | LeRobot deposu |
| 5 | LeRobotDataset belgeleri |
| 6 | Open X-Embodiment proje sayfası |
| 7 | ROS 2 belgeleri |
| 8 | OPC UA (OPC Foundation) |
| 9 | Model Context Protocol |
| 10 | A2A protokolü |
| 11 | Ollama |
| 12 | llama.cpp |
| 13 | Qwen2.5 deposu |
| 14 | Sigstore |
| 15 | Sigstore şeffaflık günlüğü |
| 16 | SLSA |
| 17 | in-toto |
| 18 | The Update Framework |
| 19 | OpenSSF |
| 20 | IPFS |
| 21 | BitTorrent BEP 3 |
| 22 | Gazebo |
| 23 | MuJoCo |
| 24 | Opacus |
| 25 | SPDX lisans listesi |
| 26 | LF üyelik sayfası |
| 27 | CNCF (vakıf emsali) |
| 28 | AB Ticari Sırlar Direktifi 2016/943 |
| 29 | AB Makine Tüzüğü 2023/1230 |
| 31 | 5846 sayılı Fikir ve Sanat Eserleri Kanunu |

### B.3 Bölüm 2.3 ile eklenen kaynaklar

Bağlantılar 10 Kasım 2026'da açıldı. Açılmayan bağlantı yoktur. İkinci el satırlar `[VEKİL]` olarak durur.

**Tablo 23. Tasarım hedefleri kaynakları (erişim: 2026-11-10)**

| # | Kaynak | Tarih / okuma | Etiket |
|---|---|---|---|
| 1 | [quantized.uk ölçümleri](https://quantized.uk/benchmarks/) — RTX 4090, Llama 3.1 8B ve ~32B | sayfa okuması 2026-11-10 | `[VERİ]` |
| 2 | [Plugsky yerel çıkarım ölçümü](https://plugsky.com/local-inference-benchmark) — Temmuz 2026 | sayfa okuması 2026-11-10 | `[VERİ]` |
| 3 | [GigaGPU, Qwen 2.5 32B AWQ](https://gigagpu.com/rtx-4090-24gb-qwen-32b-benchmark/) | Mayıs 2026; barındırıcı ölçümü | `[VEKİL]` |
| 4 | [GPU-Benchmarks-on-LLM-Inference](https://github.com/XiongjieDai/GPU-Benchmarks-on-LLM-Inference) — Llama 3, 48 GB | llama.cpp tablosu; 2026 yeniden ölçümü değil | `[VEKİL]` |
| 5 | [Google: AI çıkarımının çevresel etkisi](https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference/) ve [arXiv:2508.15734](https://arxiv.org/abs/2508.15734) | blog 2025-08-21; makale medyan 0,24 Wh | `[VERİ]` |
| 6 | [Sam Altman, The Gentle Singularity](https://blog.samaltman.com/the-gentle-singularity) — ortalama sorgu 0,34 Wh | şirket beyanı, yöntem yok | `[VEKİL]` |
| 7 | [arXiv:2604.22750](https://arxiv.org/abs/2604.22750) — OpenHands, SWE-bench Verified, token katları | HTML v3 okuması 2026-11-10 | `[VERİ]` |
| 8 | [AA: Copilot Fusion](https://artificialanalysis.ai/articles/github-copilot-fusion-orchestrates-anthropic-and-openai-models-to-balance-performance-and-cost) ve [karşılaştırma sayfası](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-github-copilot) | ~7,2M ve 7,34M token/görev | `[VERİ]` |
| 9 | [AA: Claude Fable 5.2](https://artificialanalysis.ai/models/claude-fable-5-2) ve [Kimi K3.1 Pro](https://artificialanalysis.ai/models/kimi-k3-1-pro); [AA ana sayfası](https://artificialanalysis.ai/) | okuma 2026-11-10; 65 ve 46, Nanbeige4.3-33B 20 | `[VERİ]` |
| 10 | [GPUwerk açık ağırlık özeti](https://gpuwerk.com/blog/open-weight-model-leaderboard/) — 27B / 33B ≈ 20 | 7 Kasım 2026 okuması | `[VEKİL]` |

Not: Kaynak tablosundaki bazı rakamlar ikinci el aktarımdır (`[VEKİL]`). Birincil belgeyle doğrulanmadıkça karar girdisi olarak kullanılmamalıdır.
