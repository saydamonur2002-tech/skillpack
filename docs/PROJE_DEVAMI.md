# Proje devamı

10 Kasım 2026 tartışma notlarının düzenlenmiş hali. Metin tartışma notudur. `spec/`, `schemas/`, `cli/` ve teknik proje taslağı ayrı durur. Fazlar (F0–F6) [ROADMAP.md](../ROADMAP.md) dosyasındadır.

Sayılar, kaynak nottaki kurala göre aksi belirtilmedikçe **tahmin** veya **varsayımdır**; ölçüm değildir. Sentetik simülasyon ayrıca işaretlenir. Bu dosyaya yeni sayı veya yeni kaynak eklenmemiştir.

## 1. Somut çıktı yolu (MVP)

Dar bir iş seçilir. İşin kuralı bellidir ve ekran üzerinden yürür.

İlke: karar betikte, açıklama modelde. Ön test notu (**tahmin**, ölçüm değildir): 7B model, 5 öncelikli kuralda 13/20; deterministik betik 20/20.

Araç tek komutla ilerler: yakala, damıt, test et, onayla, paketle ve imzala. Paket başka bir makinede doğrulanır ve kullanılır.

Saha denemesi küçük tutulur: 1 gerçek usta, 1 gerçek iş yeri, 1 hafta kullanım. Bakılacak şey zaman kazancıdır.

Yayımlanacaklar: kod, örnek paket, ölçüm ve demo videosu. Agent Skills topluluğuna bir uzantı önerisi götürülür.

Kaba süre 4–8 haftadır (**tahmin**). Altyapı notu da **tahmin**dir: ayda yaklaşık 15 € VPS, gerekirse saatlik GPU.

## 2. Geri bildirim ve test kimden gelir

Sıra kabaca şöyledir:

1. Açık kaynak topluluğu (Agent Skills Discussions).
2. Gerçek kullanıcı: esnaf veya atölye.
3. Üniversite: tez veya proje.
4. En son, firmaların geliştirici ilişkileri ekibi. Onlara demo ve ölçümle gidilir.

## 3. Kapanan firmalardan açık varlıklar

Ön eleme sayfası: [kapanan firmalardan açık varlıklar](https://cursor.com/canvas/store-5c1ca32d-96cc-42d1-abab-9abdc881dcaf/3fdb6ee8-87ea-4dce-a1b0-7828abef561f).

Notlardaki sayım (**tahmin** / ön eleme özeti, bu depoda yeniden sayılmadı):

- 43 aday.
- 19 firma veya proje kökeni.
- 8 kategori: Robotik 11, Ses 8, Ofis/altyapı 6, Lojistik 5, Kodlama 5, IoT 4, Sağlık 2, Siber güvenlik 2.
- 15 kayıt elendi: lisans belirsiz veya kısıtlı 7, yalnız varlık satışı 4, aslında batmamış veya kanıt eksik 4.
- Toplam 58.

İlk üç aday: Mycroft devamı / Adapt (niyet ayrıştırıcı), Grapl analizörleri, Ninja Sphere sensör köprüsü (go-ninja / go-zigbee).

Puanlar ön eleme **tahminidir**.

## 4. Sektörel etki (tahmin)

Sıra tartışma notundaki tahmindir. Ölçülmüş etki değildir.

1. IoT ve soğuk zincir (en hızlı etki beklenen alan).
2. Esnaf ve ustalık bilgisinin taşınması (en özgün alan).
3. Lojistik ve depo.
4. Siber güvenlik: imzalı ve iptal edilebilir kural.
5. Yazılım ekip kuralları.
6. Ofis ve idari belge işleri. Veri yerelde kalır.
7. Sağlık. Yavaş ilerlenir. Kapsam yalnız şema ve kayıt doğrulamadır.
8. Eğitim.

## 5. Cihaz katmanları

### Telefon

32B model (4-bit, yaklaşık 16 GB ağırlık) üst segmentte yaklaşık 2027–2028, orta segmentte yaklaşık 2029–2031 döneminde beklenir. Bu aralık **tahmindir**.

Bugün pratik olan 1–4B model ve bir beceri paketidir (**tahmin**). Android tarafında adı geçen çalıştırma yolları: Gemini Nano / AICore, MLC, llama.cpp, LiteRT-LM.

### Laptop ve masaüstü

7–14B modeller bu katmanda rahat çalışır (**tahmin**).

Yerel modelin kazancı erişimdir. Sistemi sürekli görür ve bunu token harcamadan yapar. Buluta yalnız özet gider. Token kullanımı düşer.

Örnek beceriler:

- Oyun / performans modu.
- Servis ve telemetri yükü izleme.

Bu örnekler yalnız resmî Windows ayarlarını kullanır. Sistem dosyası silinmez. Hile karşıtı yazılıma ve oyun belleğine dokunulmaz. Her değişiklik geri alınabilir.

### Beyaz eşya

Cihazın kendisinde LLM yoktur. Donanım mikrodenetleyicidir. Kural kısmı cihazda durur. LLM evdeki merkezdedir: Home Assistant ve Ollama, mini PC veya Raspberry Pi 5. Dış buluta yalnız zor durumda gidilir.

## 6. Hedef ürün mimarisi

İlk demo için dört parça önerilir:

1. **Arayüz.** Telefon uygulaması veya web panel. Panel Home Assistant üzerindedir.
2. **Sesli komut.** openWakeWord, Whisper ve Piper (HA Assist).
3. **Yüklenebilir beceriler.** İmzalı, insan onaylı ve iptal edilebilir `SKILL.md` paketleri. Projenin katkısı bu katmandır.
4. **Cihaz, yerel ve bulut ağı.** Zigbee, Wi-Fi veya Matter ile ev merkezine gelinir. Ev merkezi yerel modeli çalıştırır. Gerekirse dış buluta yalnız özet gider.

Yeni yazılacak parça: beceri paketleri ve bu paketleri yükleyen küçük bir eklenti.

İlk beceri: buzdolabı sıcaklık takibi.

## 7. Yerel ve bulut işbirliği

Üç rol konuşuldu:

- **Bulut kontrol eder.** Belirsiz veya riskli durumda devreye girer.
- **Bulut paket yazar.** Bu, önerilen yoldur. Akış: kural, örnek ve test; sonra insan onayı; sonra paket güncellemesi.
- **Bulut öğretir.** LoRA ile damıtma. Sağlayıcının şartları kontrol edilir. Gemini, kendi çıktılarıyla model eğitimini kısıtlar.

### Simülasyon (sentetik)

Sayfa: [yerel–bulut simülasyonu](https://cursor.com/canvas/store-5c1ca32d-96cc-42d1-abab-9abdc881dcaf/a1cd97fb-dcd6-4717-88fb-245a24c24c0b).

1.000 sorgu. **Sentetiktir. Ölçüm değildir.** Karşılaştırma: yalnız yerel, sonra paket + Gemini (8. hafta).

| Ölçü | Yalnız yerel | Paket + Gemini (8. hafta) | Etiket |
|---|---|---|---|
| Doğruluk | %68,4 | %92,9 | sentetik |
| Ortalama yanıt | 10,5 sn | 7,55 sn | sentetik |
| İlk token | 2,5 sn | 3,09 sn | sentetik |
| Bulut çağrısı | %23 | %13,6 | varsayım |
| Enerji | 31,5 J/sorgu | 22,1 J/sorgu | varsayım |

Aynı sentetik çalışmada 1.000 sorgu yaklaşık 0,049 ABD dolarıdır (sentetik, ölçüm değildir).

## 8. Benzer projeler ve boşluk

Adı geçen çalışmalar: Google AI Edge Gallery (telefonda `SKILL.md`), Layla, PocketPal, Maid, ChatterUI, MLC LLM, llama.cpp, LiteRT-LM, ExecuTorch, Qualcomm GenieX, Firebase Hybrid inference, Apple PCC, Samsung Galaxy AI, RouteLLM, Hybrid LLM (ICLR 2024), Minions, FrugalGPT, Android AppFunctions, Nexa Octopus v2, PromptSign (`SKILL.md` imza ve iptal), Amazon Alexa Skills.

Alexa Skills bulutta ve kapalıdır. Bilgi paketi değildir. Komut kısayoludur.

Boşluk: imzalı, iptal edilebilir ve insan onaylı paketler ile zorluk yönlendiricisi ve bulut-öğretmen döngüsü bir arada durmuyor.

Öneri: AI Edge Gallery, Home Assistant veya PromptSign üstüne kurmak.

## 9. Tasarım kararları ve öneriler

Bu bölüm öneridir. Şema, CLI ve teknik taslak bu önerilerle değişmez.

### 9.1 LLM'ye giden içerik İngilizce yazılır

`SKILL.md`, kurallar, örnekler, testler ve istemler İngilizce yazılır. Kullanıcıya dönük dil ikincildir.

### 9.2 İsteğe bağlı `budget` alanı (token sınırı)

Pakete isteğe bağlı bir token sınırı alanı konması önerilir. Örnek değerler tartışma notundandır. Ölçülmüş limit değildir.

```yaml
budget:
  skill_max_tokens: 2000
  local_max_output: 300
  cloud_max_tokens_per_day: 5000
  on_exceed: ask_user
```

Alanlar:

- `skill_max_tokens` — beceri içeriğinin token üst sınırı.
- `local_max_output` — yerel model çıktısının üst sınırı.
- `cloud_max_tokens_per_day` — bir günde buluta giden token üst sınırı.
- `on_exceed` — sınır aşılınca ne yapılır. Örnek değer `ask_user`: kullanıcıya sorulur.

### 9.3 Açık ve ticari olmayan duruş

Proje ticari değildir. Ücret veya satış yoktur. Kod tarafı Apache-2.0 çizgisinde açık lisansla durur. İleride bir vakıf çatısı düşünülebilir.

### 9.4 Patent ve önceki teknik

Patent, fikre değil uygulamaya bakar. Bileşenler açık tutulur. Tarihli açık yayın, önceki teknik (prior art) kaydıdır. Firmaların özel teknikleri birebir kopyalanmaz.

## 10. Sonraki adım

İlk demo üç parçadan oluşur: Home Assistant, Ollama ve bir imzalı beceri. Beceri buzdolabı sıcaklığını izler.

Aday olarak duran ikinci beceri: Windows üzerinde oyun / performans modu. Kurallar Bölüm 5'tedir. Yalnız resmî ayarlar, silme yok, hile karşıtı yazılıma ve oyun belleğine dokunma yok, her değişiklik geri alınabilir.

İş listesi [ROADMAP.md](../ROADMAP.md) içindeki "Proje devamı" bölümündedir.
