# skillpack v0.1-taslak — spesifikasyon

Durum: taslak. Bu belge, depodaki referans çalıştırıcının (`cli/`) uyguladığı kuralları tanımlar. Belgede yazıp çalıştırıcıda olmayan bir kural yoktur; çalıştırıcıda olmayan konular Bölüm 13'te "kapsam dışı" olarak listelenir.

Lisans: CC-BY-4.0.

## 1. Amaç ve temel ilke

Bir ustanın tekniğini, genel amaçlı bir yerel dil modelinin **uygulayabileceği** bir pakete çevirmek.

Temel ilke şudur: **niş işte model karar vermez.** Kararı paketteki akış verir; akışı çalıştırıcı yürütür. Modelin görevi yalnız iki şeydir:

1. Kullanıcının cümlesinden hangi paketin istendiğini seçmek.
2. Kullanıcının açıkça söylediği değerleri (sayı, evet/hayır, seçenek) çıkarmak.

Model hesap yapmaz, eşik karşılaştırmaz, sonuç mesajı yazmaz, eylem başlatmaz. Bu sınır Bölüm 9'da kurallaştırılır.

Bu belgede **ZORUNLU**, **YASAK** ve **ÖNERİLİR** sözcükleri uygunluk koşullarını belirtir.

## 2. Dayanılan standartlar

Yeni bir şey icat edilmeden kullanılanlar:

| Konu | Standart | Bu belgede nerede |
|---|---|---|
| Paket dizini ve `SKILL.md` | Agent Skills | Bölüm 4 |
| Manifest ve akış dosya biçimi | YAML 1.2'nin JSON ile uyumlu alt kümesi | Bölüm 5, 6 |
| Şema dili | JSON Schema 2020-12 | `cli/skillpack/schemas/` |
| Paket sürümü | Semantic Versioning 2.0.0 | Bölüm 5 |
| Dosya özeti | SHA-256 (FIPS 180-4) | Bölüm 10 |
| İmza | Ed25519 (RFC 8032) | Bölüm 10 |
| Anahtar dosyası | PEM; özel anahtar PKCS#8, açık anahtar SubjectPublicKeyInfo | Bölüm 10 |
| İmzalanan baytlar | JSON, RFC 8785 (JCS) ile aynı çıktı (Bölüm 10.2'deki kısıtla) | Bölüm 10 |
| Lisans kimliği | SPDX | Bölüm 5 |
| Dil etiketi | BCP 47 | Bölüm 5 |
| Tarih | ISO 8601 | Bölüm 8, 11 |
| Modelin çıktısını kısıtlama | JSON Schema ile yapılandırılmış çıktı (ör. Ollama `format`) | Bölüm 9 |

Bu belgenin eklediği tek yeni biçim **akış profilidir** (Bölüm 6): ustanın tekniğini adım adım tanımlayan bildirimsel dosya.

## 3. Terimler

- **Paket:** tek bir tekniği taşıyan dizin.
- **Akış:** tekniğin adımları. Veridir, kod değildir.
- **Çalıştırıcı:** paketi doğrulayan, akışı yürüten program.
- **Ev sahibi (host):** çalıştırıcının insana soru sorduğu, sensör okuduğu ve eylem yaptığı arayüz.
- **Yönlendirici:** kullanıcının cümlesinden paketi seçen bileşen. Dil modeli burada, yalnız burada kullanılır.
- **Usta:** tekniğin sahibi olan insan (fabrika ustası, esnaf, öğretmen).

## 4. Paket yapısı

```text
<ad>/
├── SKILL.md                 # Agent Skills ön bilgisi + İngilizce prosedür özeti
├── skillpack.yaml           # manifest
├── flow.yaml                # akış (adı manifestte verilir)
├── tests/cases.yaml         # kabul testleri ve yönlendirme örnekleri
├── provenance/approvals.json  # insan onay kayıtları
└── skillpack.sig.json       # imza paketi (imzalamayla üretilir)
```

Kurallar:

- Dizin adı, manifestteki `name` ve `SKILL.md` içindeki `name` aynı olmak ZORUNDADIR.
- Her paket geçerli bir Agent Skills dizinidir. `SKILL.md` ön bilgisinde `name` ve `description` ZORUNLUDUR; `metadata` altında `skillpack-spec: "0.1-taslak"` ve `skillpack-manifest: "skillpack.yaml"` ZORUNLUDUR.
- `description` İngilizce yazılır ve "ne yapar, ne zaman kullanılır" sorularını cevaplar. Yönlendirici modele gösterilen metin budur.
- Dosya yolları yalnız `A-Z a-z 0-9 . _ -` ve `/` içerebilir. Sembolik bağ YASAKTIR.
- Pakette çalıştırılabilir kod bulunması bu sürümde anlamsızdır: çalıştırıcı paketten kod yürütmez.

## 5. Manifest (`skillpack.yaml`)

Şema: `cli/skillpack/schemas/skillpack.schema.json`.

| Alan | Zorunlu | Açıklama |
|---|---|---|
| `skillpack` | Evet | Spesifikasyon sürümü. Bu belge için `"0.1-taslak"`. |
| `name` | Evet | Küçük harf, rakam, tire; en çok 64 karakter. |
| `version` | Evet | SemVer `MAJOR.MINOR.PATCH`. |
| `publisher.display` | Evet | Görünen ad. Takma ad olabilir. |
| `publisher.org_role` | Evet | `bireysel`, `isveren-adina` ya da `kurum`. |
| `domain` | Evet | `sector`, `task`, `lang` (BCP 47 listesi). |
| `components` | Evet | `procedure: SKILL.md`, `flow`, `tests` dosya yolları. Yollar paket dışına çıkamaz. |
| `runtime.llm_role` | Hayır | Verilirse `route-only` olmak zorundadır. |
| `runtime.model_class` | Hayır | Bilgi amaçlı model sınıfı listesi. |
| `routing.title` | Evet | Kullanıcıya gösterilen kısa ad. |
| `routing.triggers` | Evet | Modelsiz yönlendirme için anahtar ifadeler. |
| `capabilities.tools` | Evet | Akışın kullanabileceği eylemler: `host:notify`, `host:record`. Boş liste olabilir. |
| `capabilities.sensors` | Hayır | Akışın okuyabileceği sensör adları. |
| `capabilities.network` | Evet | Bu sürümde yalnız `none` kabul edilir. |
| `capabilities.cloud_egress.allowed` | Evet | Bu sürümde yalnız `false` kabul edilir. |
| `human_in_loop.mode` | Evet | `suggest`, `approve-each`, `approve-batch` (Bölüm 7.3). |
| `privacy.raw_customer_data` | Evet | `false` olmak zorundadır. |
| `privacy.examples` | Evet | `anonymized` ya da `synthetic`. |
| `license.spdx` | Evet | SPDX kimliği ya da `LicenseRef-...`. |
| `provenance.approvals` | Evet | Onay kaydı dosyasının yolu. |

Sürümleme: MAJOR, sonuç kümesi ya da girdiler uyumsuz değiştiğinde veya `capabilities` genişlediğinde artar; MINOR, geriye uyumlu yeni kural ya da sonuç eklendiğinde; PATCH, düzeltme ve ek testte.

Doğrulayıcı bilinmeyen üst düzey alanları uyarıyla geçer. `skillpack` alanı tanımadığı bir değer taşıyan paketi reddeder.

**Beyan edilmeyen yetki yoktur.** Akış, `capabilities.tools` içinde olmayan bir eylemi ya da `capabilities.sensors` içinde olmayan bir sensörü kullanırsa paket geçersizdir.

## 6. Akış profili (`flow.yaml`)

Şema: `cli/skillpack/schemas/flow.schema.json`. Akış beş bölümden oluşur.

```yaml
flow: "0.1"
params:      # ustanın sayıları
inputs:      # insandan ya da sensörden alınacak değerler
tables:      # arama tabloları (isteğe bağlı)
steps:       # adımlar
outcomes:    # olası sonuçlar ve mesajları
on_unknown:  # cevap alınamazsa varılacak sonuç
```

### 6.1 Parametreler

`params`, ad → sayı, dizge ya da mantıksal değer eşlemesidir. Ustanın eşikleri burada durur; kural ifadelerine sayı gömmek yerine parametre adı kullanmak ÖNERİLİR. Böylece usta mantığa dokunmadan sayıyı değiştirir.

### 6.2 Girdiler

Her girdinin `type` ve `prompt` alanı ZORUNLUDUR.

| Tür | Kabul edilen cevap | Ek alanlar |
|---|---|---|
| `number` | Sayı; ondalık ayracı nokta ya da virgül | `min`, `max`, `unit` |
| `integer` | Tam sayı | `min`, `max`, `unit` |
| `bool` | evet / hayır | — |
| `choice` | Seçeneklerden biri ya da sıra numarası | `choices` (zorunlu) |

`hint`, ölçümün nasıl yapılacağını anlatır. `sensor`, değerin önce okunacağı sensörün adıdır.

Serbest metin girdisi **yoktur**. Karar, sayılabilir ya da sınıflanabilir gözleme dayanmak zorundadır; ustanın "kıvamına bakarım" dediği şey bir `choice` ya da `bool` sorusuna indirgenmeden pakete giremez.

### 6.3 Tablolar

- `map`: anahtar → değer. Anahtar tabloda yoksa akış hatayla durur.
- `range`: satırlar `below` değerine göre artan sıradadır; anahtar ilk `below` değerinden küçük olduğu satırın değerini alır. Son satır `below` taşımaz ve geri kalanı kapsar.

### 6.4 Adımlar

Her adımın bir `id` değeri ve aşağıdakilerden **tam olarak biri** vardır.

| Adım | İş |
|---|---|
| `ask: <girdi>` | Girdiyi edinir (Bölüm 7.2). |
| `compute: {ad: ifade}` | İfadeyi hesaplar, sonucu ada bağlar. |
| `lookup: {table, key, into}` | Tablodan değer arar. |
| `decide: [kurallar]` | İlk doğru kuralı uygular. |
| `say: "metin"` | İnsana talimat ya da bilgi gösterir. |
| `act: {action, text}` | Eylem önerir ya da onayla yapar (Bölüm 7.3). |
| `finish: <sonuç>` | Akışı bu sonuçla bitirir. |

`decide` kuralı `when: <ifade>` ya da `else: true` taşır; hedefi `goto: <adım>`, `finish: <sonuç>` ya da `continue: true` değerlerinden tam olarak biridir. **Son kural `else` olmak ZORUNDADIR.** Bu, ustanın düşünmediği bir durumun sessizce geçmesini engeller.

Son adım `finish` olmak ya da bütün dalları `goto`/`finish` ile biten bir `decide` olmak ZORUNDADIR.

### 6.5 İfade dili

`when`, `compute` ve `lookup.key` ifadeleri şu yapılarla sınırlıdır:

- Sabitler: sayı, tek ya da çift tırnaklı dizge, `true`, `false`.
- Adlar: parametre, girdi ya da daha önce hesaplanmış değer.
- Aritmetik: `+ - * / %`, tekli `-`.
- Karşılaştırma: `== != < <= > >=`, `in`, `not in`; zincirleme (`0 < x < 10`) geçerlidir.
- Mantık: `and`, `or`, `not`.
- Liste sabiti: `[a, b]` (yalnız `in` için).
- Fonksiyonlar: `min`, `max`, `abs`, `round`.

Öznitelik erişimi, indeksleme, atama, döngü, koşullu ifade, üs alma ve başka fonksiyon çağrısı YASAKTIR. İfade en çok 300 karakterdir. Çalıştırıcı ifadeyi genel amaçlı bir değerlendiriciye (`eval`) vermez; sözdizim ağacını yorumlar.

Parametre, girdi ve hesaplanan değer adları tek bir ad uzayını paylaşır; çakışma paketi geçersiz kılar.

### 6.6 Sonuçlar

Her sonucun `verdict` ve `message` alanı vardır.

| `verdict` | Anlamı |
|---|---|
| `ok` | Uygun, devam. |
| `warn` | Dikkat; iş sürer ama bir şey yapılmalı. |
| `stop` | Dur; iş bu haliyle sürmemeli. |
| `escalate` | Paket bu durumu çözemiyor; ustaya sor. |

`message`, kullanıcıya gösterilecek metindir ve usta tarafından yazılır. `{ad}` yer tutucuları çalıştırıcı tarafından doldurulur. `on_unknown`, `verdict` değeri `escalate` olan bir sonuca işaret etmek ZORUNDADIR; bu sonucun mesajında `{missing}` cevapsız kalan sorunun metnini verir.

## 7. Yürütme kuralları

### 7.1 Belirlenimcilik

Aynı paket ve aynı girdilerle çalıştırıcı aynı sonucu, aynı mesajı ve aynı izi üretmek ZORUNDADIR. Yürütme sırasında model çağrısı, ağ erişimi, saat ya da rastgelelik kullanılmaz.

Adımlar yazıldıkları sırayla yürür. Bir çalıştırmada en çok 200 adım yürütülür; aşılırsa akış hatayla durur.

### 7.2 Girdinin edinilmesi

Bir `ask` adımı değeri şu sırayla arar:

1. Yönlendiricinin konuşmadan çıkardığı değer. Kaynak model ise değer, kullanılmadan önce insana gösterilip onaylatılmak ZORUNDADIR. Onaylanmazsa atılır.
2. Girdide `sensor` varsa sensör okuması.
3. İnsana soru. Geçersiz cevapta soru yinelenir; üç denemeden sonra cevap "bilinmiyor" sayılır.

Her değer, kaynağı ne olursa olsun, girdinin türü ve `min`/`max` sınırlarıyla denetlenir. Sınır dışı değer kullanılmaz.

Cevap alınamazsa akış **tahmin yürütmez**: `on_unknown` sonucuyla biter.

### 7.3 Eylemler ve insan onayı

Çalıştırıcı iki eylem ilkeli sağlar: `notify` (insana bildirim) ve `record` (kayıt defterine yazma).

| `human_in_loop.mode` | `act` adımının davranışı |
|---|---|
| `suggest` | Eylem yapılmaz; sonuçta "öneri" olarak listelenir. |
| `approve-each` | Her eylem için insana sorulur; onaylanırsa yapılır, onaylanmazsa öneri olarak kalır. |
| `approve-batch` | Bu sürümde `approve-each` gibi davranır. |

İnsan onayı olmadan hiçbir eylem yapılmaz.

### 7.4 Sonuç ve iz

Çalıştırıcı her çalıştırmada şunları döndürür: paket adı ve sürümü, sonuç kimliği, `verdict`, mesaj, edinilen ve hesaplanan değerler, önerilen ve yapılan eylemler ve **iz**. İz; her girdinin değerini ve kaynağını (insan, sensör, model+onay), her hesabı, her tablo aramasını ve tetiklenen her kuralı sırayla listeler. İz, "bu sonuca neden varıldı" sorusunun cevabıdır.

## 8. Kabul testleri ve insan onayı

`tests/cases.yaml` iki liste taşır:

```yaml
cases:
  - name: tam sınırda
    inputs: {core_temp_c: 4, ...}     # verilmeyen girdi "bilinmiyor" sayılır
    sensors: {bearing_temp_c: 45}     # isteğe bağlı
    expect: {outcome: kabul, verdict: ok, values: {limit_c: 4}}
routing:
  - utterance: "Tedarikçi tavuk getirdi, kabul edeyim mi?"
```

- En az bir vaka ZORUNLUDUR. Her sonucun en az bir vakayla sınanması ve her eşiğin tam sınır değerinde sınanması ÖNERİLİR; doğrulayıcı sınanmayan sonuç için uyarı verir.
- Vakalar sentetik ya da anonimleştirilmiş olmak ZORUNDADIR. Doğrulayıcı e-posta, telefon, IBAN ve 11 haneli numara kalıplarını tarar ve uyarı verir. Bu tarama yardımcıdır, garanti değildir.
- `routing` örnekleri, yönlendiricinin bu paketi seçmesi gereken cümlelerdir.

`provenance/approvals.json` en az bir onay taşır. Her onayda `approver` (takma ad olabilir), `role`, `date` ve `version` ZORUNLUDUR; paketin güncel sürümü için en az bir onay bulunmalıdır. Onay, ustanın "kuralları okudum, benim yaptığım iş budur" beyanıdır.

İmzalama aracı, doğrulamadan ya da kabul testlerinden geçmeyen paketi imzalamaz.

## 9. Modelin sınırı (yönlendirme)

Yönlendirici iki aşamada çalışır ve her aşamada modelin çıktısı bir JSON şemasıyla kısıtlanır.

1. **Seçim.** Modele yüklü paketlerin adları ve `description` metinleri verilir. Çıktı şeması, `skill` alanını yüklü paket adları ve `none` değeriyle sınırlar. Model var olmayan bir paket adı üretemez.
2. **Çıkarma.** Modele seçilen paketin girdileri verilir. Çıktı şeması her girdiyi kendi türüyle ya da `null` ile sınırlar. Modele "yalnız açıkça söyleneni doldur, gerisine `null` yaz" talimatı verilir.

Kurallar:

- Modelin çıkardığı her değer Bölüm 7.2'ye göre insana onaylatılır.
- Model yanıt vermezse ya da geçersiz yanıt verirse çalıştırıcı modelsiz yönlendirmeye (`routing.triggers`) düşmek ZORUNDADIR. Paketler modelsiz de kullanılabilir.
- Modelsiz yönlendirme eşitlik ya da eşleşmeme durumunda seçim yapmaz; kullanıcıya yüklü paketleri listeler.
- Sonuç mesajı modele yeniden yazdırılmaz. Kullanıcı ustanın yazdığı metni görür.
- Model yereldir. Referans çalıştırıcı model isteğini sistemdeki vekil sunucu ayarlarını yok sayarak gönderir.

Yalnız `SKILL.md` okuyan bir ajan (çalıştırıcısı olmayan) paketi yine kullanabilir; ancak bu durumda belirlenimcilik ve onay güvenceleri geçerli değildir. `SKILL.md` gövdesi bu yüzden modele "kendin karar verme, akışı çalıştırıcıyla yürüt" der.

## 10. İmza

### 10.1 Anahtarlar

İmza Ed25519'dur. Özel anahtar yalnız yayıncıda durur. Çalıştırıcı yalnız açık anahtarları, güvenilenler dizininde (`<anahtar-kimliği>.pem`) taşır. Anahtar kimliği, ham açık anahtarın SHA-256 özetinin ilk 16 onaltılık hanesidir.

Simetrik yöntemler (HMAC gibi) YASAKTIR: doğrulayan tarafın imza üretebildiği bir düzen imza değildir.

### 10.2 İmzalanan içerik

1. İmza dosyası dışındaki her dosyanın SHA-256 özeti alınır: `yol → "sha256:<onaltılık>"`.
2. Şu nesne kurulur: `{"checksums": {...}, "name": ..., "skillpack": "0.1-taslak", "version": ...}`.
3. Nesne kanonik JSON'a çevrilir: anahtarlar sıralı, boşluksuz, UTF-8. Nesne yalnız dizge içerdiği ve yollar Bölüm 4'teki karakter kümesiyle sınırlı olduğu için çıktı RFC 8785 ile aynıdır.
4. Bu baytlar Ed25519 ile imzalanır. **Paket kimliği**, aynı baytların SHA-256 özetidir (`sha256:...`). Aynı içerik her yerde aynı kimliği taşır.

`skillpack.sig.json` alanları: `skillpack`, `algorithm` (`ed25519`), `key_id`, `pack_id`, `name`, `version`, `checksums`, `signature` (Base64).

### 10.3 Doğrulama

Çalıştırıcı bir paketi yüklemeden önce sırayla şunları denetler; herhangi biri düşerse paket yüklenmez:

1. İmza dosyası var ve okunabiliyor.
2. Spesifikasyon ana sürümü ve imza algoritması destekleniyor.
3. Diskteki dosya kümesi ve özetleri imzadakilerle birebir aynı (fazla, eksik ya da değişmiş dosya yok).
4. İmzadaki ad ve sürüm manifesttekiyle aynı.
5. Paket kimliği yeniden hesaplanan değerle aynı.
6. `key_id` güvenilenler dizininde var.
7. İmza geçerli.
8. Paket kimliği ve anahtar kimliği iptal listesinde yok (Bölüm 11).
9. Paket Bölüm 4–8 kurallarından geçiyor.

Depo her istekte yeniden taranır. Çalışırken eklenen imzalı paket bir sonraki istekte kullanılabilir; değiştirilen, silinen ya da iptal edilen paket bir sonraki istekte düşer.

## 11. İptal

İptal listesi bir JSON dosyasıdır. Şema: `cli/skillpack/schemas/revocations.schema.json`.

```json
{
  "revocations": "0.1-taslak",
  "revoked": [
    {"pack_id": "sha256:...", "reason": "yanlis-beyan", "date": "2026-11-10"},
    {"key_id": "e3d6cd1f2ecd0220", "reason": "guvenlik-acigi", "date": "2026-11-10"}
  ]
}
```

Gerekçe kodları: `zararli`, `guvenlik-acigi`, `lisans-ihlali`, `yanlis-beyan`, `yayinci-talebi`. Bir anahtarın iptali, o anahtarla imzalanmış bütün paketleri düşürür. Okunamayan iptal listesi verildiğinde çalıştırıcı paketi yüklemez.

## 12. Uygunluk

**Uygun paket**, `skillpack validate` komutundan hatasız geçen, kabul testlerinin tamamı geçen ve imzası doğrulanan pakettir.

**Uygun çalıştırıcı** şunları sağlar:

1. Bölüm 10.3'teki denetimlerden geçmeyen paketi yüklemez.
2. Akışı Bölüm 6 ve 7'ye göre, belirlenimci olarak yürütür.
3. Paketten kod yürütmez; ifadeleri Bölüm 6.5'teki alt kümeyle sınırlar.
4. Beyan edilmeyen eylem ya da sensörü kullandırmaz.
5. İnsan onayı olmadan eylem yapmaz.
6. Modeli yalnız Bölüm 9'daki iki iş için kullanır ve modelsiz çalışabilir.
7. Her sonuçla birlikte izi verir.

## 13. Kapsam dışı ve bilinen sınırlar

Bu sürümde **yoktur**; teknik taslaktaki (`docs/TEKNIK_PROJE_v0.1.md`) hedefler olarak durur:

- Sigstore ile anahtarsız imza, şeffaflık günlüğü, TUF tarzı imzalı ve zaman damgalı iptal listesi. Bu sürümde iptal listesi imzasız yerel dosyadır; listeyi değiştirebilen biri iptali kaldırabilir.
- Paket arşivi, dağıtım, aynalar (`pack`, `publish`).
- Fiziksel profil (`robot_profile.yaml`), gösterim verisi, politika ağırlıkları.
- Ağ, bulut ve dosya sistemi yetkileri; MCP araçları.
- `budget` alanı (model yürütmede kullanılmadığı için bu profilde harcama yoktur).
- Köken beyanı (SLSA/in-toto), anonimleştirme raporu.
- Onay kaydının onaylayanın kendi anahtarıyla imzalanması. Bu sürümde onay, yayıncının imzasının kapsadığı bir beyandır; onaylayanın kimliği kriptografik olarak kanıtlanmaz.

Teknik taslaktan bilinçli sapmalar:

- Özetler ve imza manifestin içinde değil, ayrı `skillpack.sig.json` dosyasındadır. Gerekçe: imzalama manifesti yeniden yazmaz, ustanın dosyası olduğu gibi kalır.
- `components.flow`, `routing` ve `runtime.llm_role` alanları eklendi.

Tasarımın sınırları:

- Akış profili **karar ağırlıklı** teknikleri taşır: kontrol, teşhis, kabul/ret, sıradaki adımı seçme. El becerisi (kaynak, sıva, bıçak kullanımı) bu profille taşınmaz.
- Paket, ustanın öngördüğü durumları kapsar. Öngörülmeyen durumda doğru davranış `else` dalı ve `escalate` sonucudur; paket doğaçlama yapmaz.
- Biçim garantisi doğruluk garantisi değildir. Yönlendirici yanlış paketi seçebilir; bu yüzden çalıştırıcı seçilen paketin adını kullanıcıya gösterir ve çıkarılan değerleri onaylatır.
