# skillpack v0.1-taslak — spesifikasyon

Durum: taslak. Bu belge, depodaki referans çalıştırıcının (`cli/`) uyguladığı kuralları tanımlar. Belgede yazıp çalıştırıcıda olmayan bir kural yoktur; çalıştırıcıda olmayan konular Bölüm 13'te "kapsam dışı" olarak listelenir.

Lisans: CC-BY-4.0.

## 1. Amaç ve temel ilke

Bir ustanın tekniğini, genel amaçlı bir yerel dil modelinin **uygulayabileceği** bir pakete çevirmek.

Temel ilke şudur: **niş işte model karar vermez.** Kararı paketteki akış verir; akışı çalıştırıcı yürütür. Modelin görevi yalnız iki şeydir:

1. Kullanıcının cümlesinden hangi paketin istendiğini seçmek.
2. Kullanıcının açıkça söylediği değerleri (sayı, evet/hayır, seçenek) çıkarmak.

Model hesap yapmaz, eşik karşılaştırmaz, sonuç mesajı yazmaz, eylem başlatmaz. Bu sınır Bölüm 9'da kurallaştırılır.

Mimari **merkez ve çevre** biçimindedir. Merkezde yerel modeli çalıştıran uygulama durur. Çevrede dikey teknikler (paketler) ve onlara bağlı yazılımlar (sensörler, kayıt defteri) durur. İkisini bağlayan standart Model Context Protocol'dür (MCP): her paket merkeze bir araç olarak görünür (Bölüm 14).

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
| Merkez ile çevre arasındaki bağlantı | Model Context Protocol (MCP), stdio taşıması | Bölüm 14 |

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

Şema: `cli/skillpack/schemas/flow.schema.json`. Akış beş zorunlu bölümden ve isteğe bağlı tehlike kurallarından oluşur.

Dosyalar YAML'dır ve sürprizsiz bir alt kümeyle okunur: yalnız `true` ve `false` mantıksal değerdir, yalnız ondalık yazım sayıdır. `1:30`, `no`, `yes`, `012` ve tarih görünümlü değerler **metin** kalır; tür şemaya uymuyorsa paket reddedilir. Aynı eşlemede yinelenen anahtar hatadır. Gerekçe: yaygın YAML 1.1 okuyucuları bu değerleri sessizce başka bir şeye çevirir (`1:30` → 90, `no` → false) ve ustanın yazdığı eşik fark edilmeden değişir.

```yaml
flow: "0.1"
params:      # ustanın sayıları
inputs:      # insandan ya da sensörden alınacak değerler
tables:      # arama tabloları (isteğe bağlı)
hazards:     # tehlike kuralları (isteğe bağlı, Bölüm 6.7)
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

`hint`, ölçümün nasıl yapılacağını anlatır. `sensor`, değerin önce okunacağı sensörün adıdır. `max_age_s`, sensör okumasının en çok kaç saniyelik olabileceğini söyler; yalnız `sensor` ile birlikte kullanılır. Sensör bağlı bir girdide `max_age_s` beyan etmek ÖNERİLİR: beyan edilmezse bayat bir okuma da kullanılır.

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

- Sabitler: sayı, tek ya da çift tırnaklı metin, `true`, `false`.
- Adlar: parametre, girdi ya da daha önce hesaplanmış değer.
- Aritmetik: `+ - * / %`, tekli `-`.
- Karşılaştırma: `== != < <= > >=`, `in`, `not in`; zincirleme (`0 < x < 10`) geçerlidir.
- Mantık: `and`, `or`, `not`.
- Fonksiyonlar: `min`, `max`, `abs`, `round`, `sqrt`.

Öznitelik erişimi, indeksleme, atama, döngü, koşullu ifade, üs alma ve başka fonksiyon çağrısı YASAKTIR. İfade en çok 300 karakter ve 100 sözdizim düğümüdür. Çalıştırıcı ifadeyi genel amaçlı bir değerlendiriciye (`eval`) vermez; sözdizim ağacını yorumlar.

Sözdizimi Python'unkine benzer, ama **anlam bu bölümde tanımlıdır** ve hiçbir programlama dilinin davranışına bırakılmaz. Farklı dillerde yazılmış çalıştırıcılar aynı ifadeye aynı sonucu vermek ZORUNDADIR.

Üç değer türü vardır: sayı, metin, mantıksal. Türler birbirine dönüşmez.

| Yapı | İşlenen | Sonuç ve kural |
|---|---|---|
| `+ - * / %`, tekli `-` | sayı | Sayı. `/` her zaman ondalık böler (`7 / 2` = 3,5). `%` sonucu bölenin işaretini taşır. Sıfıra bölme hatadır. |
| `< <= > >=` | sayı | Mantıksal. |
| `== !=` | aynı türden iki değer | Mantıksal. Farklı türleri karşılaştırmak hatadır. |
| `in`, `not in` | sol: tek değer; sağ: sabitlerden oluşan `[...]` listesi | Mantıksal. Listede aynı türden eşit bir değer aranır. Metin içinde metin arama yoktur. |
| `and`, `or`, `not` | mantıksal | Mantıksal. Sayı ya da metin koşul yerine geçmez. `and`/`or` soldan sağa değerlendirilir ve sonuç belli olunca durur. |
| `min`, `max` | iki ya da daha çok sayı | Sayı. |
| `abs(x)` | sayı | Sayı. |
| `sqrt(x)` | sıfır ya da artı sayı | Karekök. Eksi sayı hatadır. |
| `round(x)` | sayı | En yakın tam sayı; tam yarımda **sıfırdan uzağa** yuvarlanır (2,5 → 3; -2,5 → -3). |
| `round(x, n)` | sayı; `n` 0–6 arası sabit tam sayı | `n` ondalık basamağa, aynı kuralla (2,675 → 2,68). |

Liste yalnız `in` işlecinin sağında kullanılabilir. Tür kuralına uymayan ifade hatadır; akış o noktada durur. Her sabit ve her ara sonuç sonlu olmak ve mutlak değeri 10¹⁵'i aşmamak ZORUNDADIR; aşan ifade hatadır.

`decide` kuralının `when` ifadesi mantıksal değer vermek ZORUNDADIR.

Sayılar ikili kayan noktadır; `0.1 + 0.2 == 0.3` yanlıştır. Ondalık değerleri eşitlikle sınamak yerine aralıkla sınamak (`abs(a - b) < 0.01`) ÖNERİLİR.

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

### 6.7 Tehlike kuralları

`hazards`, akıştaki sıradan bağımsız olarak geçerli olan "bunu görürsen dur" kurallarının listesidir.

```yaml
hazards:
  - when: "package_damaged or days_to_expiry < 0"
    finish: ret
    note: "Hasarlı ya da tarihi geçmiş ürün alınmaz."
```

- `finish`, `verdict` değeri `stop` olan bir sonuca işaret etmek ZORUNDADIR.
- O sonucun mesajındaki yer tutucular yalnız kuralın kullandığı adlar ve parametreler olabilir; kural, diğer değerler henüz bilinmezken de ateşleyebilir.
- Kurallar akış başlamadan önce ve değer üreten her adımdan (`ask`, `compute`, `lookup`) sonra yazıldıkları sırayla sınanır. İlk doğru kural akışı bitirir.
- Değerlendirme **üç değerlidir**: bir ad henüz bilinmiyorsa ona bağlı alt ifade "bilinmiyor"dur. `a or b` içinde `a` doğruysa `b` bilinmese de sonuç doğrudur; `a and b` içinde `a` yanlışsa sonuç yanlıştır. Kural yalnız sonucu kesin doğru olduğunda ateşler.
- Henüz sorulmamış bir girdi için çalıştırıcı yalnız eldeki kaynaklara bakar: sensör okuması ve konuşmadan gelen değer. Tehlike kuralı için insana soru sorulmaz ve konuşmadan gelen değer onay beklemeden kullanılır; yanlış bir "dur", kaçırılmış bir "dur"dan daha az zararlıdır.

Amaç: eksik veri, bilinen bir tehlikeyi örtmemelidir. Tehlike kuralı olmayan bir akışta tek bir cevapsız soru, o ana kadar görülen dur koşulunu `on_unknown` sonucuna düşürebilir. Dur sonucu olan bir pakette `hazards` beyan etmek ÖNERİLİR; doğrulayıcı eksikliği öneri olarak bildirir.

## 7. Yürütme kuralları

### 7.1 Belirlenimcilik

Aynı paket ve aynı girdilerle çalıştırıcı aynı sonucu, aynı mesajı ve aynı izi üretmek ZORUNDADIR. Yürütme sırasında model çağrısı, ağ erişimi, saat ya da rastgelelik kullanılmaz.

Adımlar yazıldıkları sırayla yürür. Bir çalıştırmada en çok 200 adım yürütülür; aşılırsa akış hatayla durur.

### 7.2 Girdinin edinilmesi

Kaynak önceliği sabittir: **sensör, sonra konuşmadan gelen değer, sonra insana soru**. Alttaki kaynak üsttekini ezemez. Bir `ask` adımı değeri şu sırayla arar:

1. Girdide `sensor` varsa sensör okuması. Okuma geçerli ve tazeyse kullanılır. Aynı girdi için konuşmadan farklı bir değer gelmişse o değer kullanılmaz ve ize `override` kaydı düşülür.
2. Konuşmadan gelen değer (yönlendiricinin çıkardığı ya da istemcinin verdiği). Kaynak model ise değer, kullanılmadan önce insana gösterilip onaylatılmak ZORUNDADIR. Onaylanmazsa atılır.
3. İnsana soru. Geçersiz cevapta soru yinelenir; üç denemeden sonra cevap "bilinmiyor" sayılır.

Tazelik: girdi `max_age_s` beyan ediyorsa, bundan eski ya da yaşı bilinmeyen okuma kullanılmaz; çalıştırıcı bir sonraki kaynağa geçer ve reddi ize yazar. Bir sensör bir çalıştırmada en çok bir kez okunur.

Her değer, kaynağı ne olursa olsun, girdinin türü ve `min`/`max` sınırlarıyla denetlenir. Sınır dışı değer kullanılmaz.

Cevap alınamazsa akış **tahmin yürütmez**: `on_unknown` sonucuyla biter. Bundan önce tehlike kuralları sınanmıştır (Bölüm 6.7).

### 7.3 Eylemler ve insan onayı

Çalıştırıcı iki eylem ilkeli sağlar: `notify` (insana bildirim) ve `record` (kayıt defterine yazma).

| `human_in_loop.mode` | `act` adımının davranışı |
|---|---|
| `suggest` | Eylem yapılmaz; sonuçta "öneri" olarak listelenir. |
| `approve-each` | Her eylem için insana sorulur; onaylanırsa yapılır, onaylanmazsa öneri olarak kalır. |
| `approve-batch` | Bu sürümde `approve-each` gibi davranır. |

İnsan onayı olmadan hiçbir eylem yapılmaz.

### 7.4 Sonuç ve iz

Çalıştırıcı her çalıştırmada şunları döndürür: paket adı ve sürümü, sonuç kimliği, `verdict`, mesaj, edinilen ve hesaplanan değerler, önerilen ve yapılan eylemler ve **iz**. İz; her girdinin değerini ve kaynağını (insan, sensör, model+onay), reddedilen sensör okumalarını, sensörün ezdiği değerleri, her hesabı, her tablo aramasını ve tetiklenen her kuralı (tehlike kuralları dahil) sırayla listeler. İz, "bu sonuca neden varıldı" sorusunun cevabıdır.

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

### 9.1 Ajan yürütme modu (model sıralayıcı) — deneysel öneri

Bazı istemciler akışı belirlenimci çalıştırıcıya bütün olarak vermek yerine bir modelin adım adım yürütmesine izin verir. Bu mod, Bölüm 9'daki "model yalnız seçer ve çıkarır" sınırını genişletir ve aşağıdaki kurallarla güvenceye alınır. **Bu bölüm bir ön ölçüme dayanır** (docs/deney/oyun-akisi-deneyi.md: bir akış, iki model, her koşul tek çalıştırma); kesin kanıt değil, deneysel bir öneridir.

1. **Girdiyi çalıştırıcı kurar.** Her adımın girdisini ve önceki adımların çıktılarının taşınmasını (`$ref`, `$var` ve benzerleri) çalıştırıcı yapar. Model adım girdisi üretmez ve sayı, alan ya da tohum yazamaz. Ölçümde büyük ve iç içe girdiyi elle kurmak küçük modeli (Haiku) 19. adımda başarısız etti (18/19); aynı iş araca verilince iki model de 19/19 tamamladı ve token maliyetleri yaklaşık eşitlendi (~71 bin).
2. **Model yalnız sırayı ve devam/dur kararını verir.** Modelin görevi sıradaki adımı çağırmak, kontrol özetini okumak ve durmak ya da devam etmek ile bunu insana açıklamaktır.
3. **Her adım kontrol ve durma koşulu taşır** (Bölüm 6.4). Çalıştırıcı kontrolleri kendisi değerlendirir ve sonucu modele özet olarak verir (geçti/geçmedi, beklenen ve bulunan değer, nedeni).
4. **Kontrol tutmazsa dur ve sor.** Model değeri değiştirip yeniden denemez; hangi kontrolün neden tutmadığını ve olası düzeltmeleri insana bildirir ve hangisinin uygulanacağını sorar.
5. **Çalıştırıcı, kontrolü başarısız adımdan sonra sonraki adımı reddetmelidir.** (Ön ölçümdeki yardımcı araç bunu uygulamıyordu; modeller ilerlemeyi seçmedi, ama güvence araca bağlanmadan modelin davranışına bırakılmamalıdır. Bu kural henüz denenmemiştir.)
6. **Büyük çıktılar modele gösterilmez.** Çıktı eşiğin üstündeyse çalıştırıcı onu dosyaya yazar, modele yalnız boyut ve özet verir.
7. **İz tamdır.** Her adımın girdisi, çıktısı ve kontrol sonucu Bölüm 7.4'teki izde yer alır; model beyanı iz yerine geçmez.

Sınır: Bu mod Bölüm 7.1'in belirlenimcilik güvencesini bozmaz (adımlar yine çalıştırıcıda çalışır), ama sıralama kararı modele bağlıdır; bu yüzden aynı girdiyle aynı sıranın yürütüleceği, modelsiz çalıştırıcıdaki gibi garanti edilmez.

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
8. Paket kimliği ve anahtar kimliği iptal listesinde yok (Bölüm 11). İmzalı iptal önbelleği kullanılıyorsa önbellek taze.
9. Paket Bölüm 4–8 kurallarından geçiyor.
10. Kurulum kaydı kullanılıyorsa paket kayıtla çelişmiyor (Bölüm 10.4).

Depo her istekte yeniden taranır. Çalışırken eklenen imzalı paket bir sonraki istekte kullanılabilir; değiştirilen, silinen ya da iptal edilen paket bir sonraki istekte düşer.

### 10.4 Kurulum kaydı: geri sarma ve yayıncı değişimi

İmza paketin kimden geldiğini söyler, ama eski ve hatalı bir sürüm de aynı anahtarla imzalıdır; güvenilen her anahtar da her paket adını imzalayabilir. Çalıştırıcı bu yüzden bir **kurulum kaydı** tutabilir (`--state dosya`). Kayıt her paket adı için son kabul edilen sürümü, paket kimliğini ve imzalayan anahtarı saklar (ilk görüşte güven). Kayıt kullanılırken:

- kayıtlıdan düşük sürüm reddedilir (geri sarma);
- aynı sürümün farklı içeriği reddedilir (yayımlanmış sürüm değişmez);
- kayıtlıdan farklı bir anahtarla imzalanmış aynı adlı paket reddedilir;
- okunamayan kayıt güvenmek için gerekçe değildir: paket yüklenmez.

Bilerek geri dönmek ya da yayıncı değiştirmek için kayıt silinir (`skillpack forget <ad> --state dosya`). Sürümler `ANA.ALT.YAMA` sayılarıyla karşılaştırılır.

Kayıt yerel bir dosyadır ve imzasızdır; dosyayı değiştirebilen biri korumayı kaldırabilir. Paket adlarını yayıncılara bağlayan imzalı bir indeks bu sürümde yoktur.

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

### 11.1 İmzalı dağıtım

Liste düz bir dosya olarak verildiğinde (`--revocations`) onu değiştirebilen biri iptali kaldırabilir. Bu kullanım yalnız deneme içindir. Asıl yol, listenin The Update Framework (TUF) ile dağıtılmasıdır; referans çalıştırıcı python-tuf kullanır.

- İptal deposu dört rol taşır: kök, hedefler, anlık görüntü, zaman damgası. Liste, `revocations.json` adlı hedef dosyadır.
- İstemci yalnız kök meta verisine güvenir ve onu ilk kurulumda **elden** alır.
- `skillpack revocations sync --source <adres ya da dizin> --root <kök> --cache <dizin>` listeyi çeker, doğrular ve önbelleğe yazar. Kaynak bir HTTP(S) adresi ya da yerel bir dizin olabilir; çevrim dışı sahada depo taşınabilir bellekle getirilir.
- Doğrulama düşerse önbellek değişmez. İmzasız değişiklik, eski bir listenin yeniden sunulması (geri sarma) ve süresi dolmuş zaman damgası (dondurma) reddedilir.
- Çalıştırıcı önbelleği `--revocation-cache <dizin>` ile kullanır. Son başarılı eşitleme `--revocation-max-age-days` değerinden (varsayılan 7) eskiyse **hiçbir paket yüklenmez**: iptal edilmiş bir paketi bilmeden çalıştırmaktansa durmak yeğdir. Uzun süre çevrim dışı kalan saha bu sınırı kendi politikasına göre büyütür; `0` sınırı kaldırır.
- Yayıncı zaman damgasını süresi dolmadan yeniden imzalamak ZORUNDADIR (`skillpack revocations publish` kayıt eklemeden çağrıldığında yalnız bunu yapar).

`skillpack revocations publish` küçük kurulumlar ve denemeler içindir: dört rolün anahtarını tek dizinde ve şifresiz tutar. Gerçek bir yayında kök anahtarı çevrim dışı tutulmalı ve roller ayrılmalıdır.

## 12. Uygunluk

**Uygun paket**, `skillpack validate` komutundan hatasız geçen, kabul testlerinin tamamı geçen ve imzası doğrulanan pakettir.

**Uygun çalıştırıcı** şunları sağlar:

1. Bölüm 10.3'teki denetimlerden geçmeyen paketi yüklemez.
2. Akışı Bölüm 6 ve 7'ye göre, belirlenimci olarak yürütür.
3. Paketten kod yürütmez; ifadeleri Bölüm 6.5'teki alt kümeyle sınırlar.
4. Beyan edilmeyen eylem ya da sensörü kullandırmaz.
5. İnsan onayı olmadan eylem yapmaz.
6. Modeli yalnız Bölüm 9'daki iki iş için kullanır ve modelsiz çalışabilir.
6a. Kaynak önceliğini, tazelik sınırını ve tehlike kurallarını Bölüm 6.7 ve 7.2'ye göre uygular.
7. Her sonuçla birlikte izi verir.
8. Ajan yürütme modunu (Bölüm 9.1) sunuyorsa, 9.1'in 1–7. maddelerini uygular.

## 13. Kapsam dışı ve bilinen sınırlar

Bu sürümde **yoktur**; teknik taslaktaki (`docs/TEKNIK_PROJE_v0.1.md`) hedefler olarak durur:

- Sigstore ile anahtarsız imza ve şeffaflık günlüğü. İptal listesi TUF ile imzalı dağıtılır (Bölüm 11.1), ama paketlerin kendisi TUF hedefi değildir ve iptal deposunun rol anahtarlarını ayıran bir yayın süreci tanımlı değildir.
- Paket adlarını yayıncılara bağlayan imzalı indeks. Kurulum kaydı (Bölüm 10.4) yereldir ve ilk görüşte güvene dayanır.
- Girdilerde birim denetimi ve dönüşümü: `unit` yalnız etikettir.
- Paket arşivi, dağıtım, aynalar (`pack`, `publish`).
- Fiziksel profil (`robot_profile.yaml`), gösterim verisi, politika ağırlıkları.
- Ağ, bulut ve dosya sistemi yetkileri. Paketin başka MCP sunucularındaki araçları çağırması (paketler MCP üzerinden sunulur, ama kendileri MCP aracı çağırmaz).
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

## 14. MCP bağlaması: merkez ve çevre

### 14.1 Mimari

```text
                 MERKEZ                                   ÇEVRE
  ┌───────────────────────────────┐        ┌──────────────────────────────────┐
  │ yerel modeli çalıştıran       │  MCP   │ skillpack sunucusu               │
  │ uygulama (MCP istemcisi)      │◄──────►│  ├─ paket: rulman-isi-titresim   │──► sensör bağı
  │                               │ stdio  │  ├─ paket: soguk-mal-kabul       │──► kayıt defteri
  │ kullanıcıyla konuşur          │        │  └─ paket: kazanim-telafi-karari │
  └───────────────────────────────┘        └──────────────────────────────────┘
```

Merkez, MCP konuşan herhangi bir istemcidir; hangi modeli çalıştırdığı bu standardın konusu değildir. Çevre, `skillpack serve` komutuyla başlatılan sunucudur. Sunucu genel amaçlı araç (dosya oku, komut çalıştır) sunmaz; yalnız dikey teknikleri sunar.

### 14.2 Paketin araca eşlenmesi

Depodaki her geçerli ve imzası doğrulanmış paket bir MCP aracıdır.

| Araç alanı | Kaynak |
|---|---|
| `name` | Paketin `name` değeri |
| `title` | `routing.title` |
| `description` | `SKILL.md` içindeki `description` + modelin sınırını bildiren sabit cümle |
| `inputSchema` | Akıştaki `inputs` |

`inputSchema` kuralları: her girdi bir özelliktir; **hiçbiri zorunlu değildir**; her özellik kendi türünün yanında `null` kabul eder; `min`/`max` değerleri `minimum`/`maximum` olarak, seçenekler `enum` olarak yazılır; tanımsız özellik kabul edilmez.

Araç listesi her istekte depodan yeniden üretilir. Bölüm 10.3'ten geçmeyen paket listede görünmez ve çağrılamaz.

### 14.3 Çağrı kuralları

Çağrı **durumsuzdur**: her çağrıda akış baştan, verilen argümanlarla yürütülür. Sunucu oturum tutmaz; aynı argümanlar aynı cevabı verir.

| Durum | Cevap |
|---|---|
| Bir girdi eksik ve bağlı sensörden de okunamıyor | `status: needs_input` ve `ask` (sorulacak sorunun adı, metni, türü, birimi, seçenekleri). Hata değildir. |
| Verilen değer türüne ya da sınırına uymuyor | `status: needs_input`, `ask` ve `rejected` (hangi değer, neden). Değer kullanılmaz. |
| Bir girdi `null` | Kullanıcı bilmiyor demektir; akış `on_unknown` sonucuna gider. |
| Bütün gerekli girdiler var | `status: done` ve Bölüm 7.4'teki sonucun tamamı. |
| Paket yok, reddedilmiş ya da tanımsız argüman var | Araç hatası (`isError`). |

İstemci `needs_input` cevabında soruyu kullanıcıya sorar ve aracı önceki argümanlara yenisini ekleyerek yeniden çağırır. Sunucu eksik değeri hiçbir durumda kendisi doldurmaz.

Cevap hem yapılandırılmış içerik hem düz metin taşır. Düz metnin ilk satırı hüküm ve ustanın mesajıdır; ardından önerilen eylemler, kullanılan bütün değerler ve paketin adı ile sürümü gelir.

### 14.4 MCP üzerinden değişen güvenceler

- **Eylem yapılmaz.** Sunucu insana doğrudan soramadığı için `human_in_loop.mode` ne olursa olsun `act` adımları yalnız öneri olarak döner.
- **Değerler kullanıcıya doğrudan onaylatılır, istemci destekliyorsa.** Sunucu, bir değerin kullanıcıdan mı modelden mi geldiğini bilemez; bu yüzden istemcinin aktardığı her değeri onaysız sayar. Hüküm böyle değerlere dayanıyorsa sunucu, MCP'nin girdi isteme mekanizmasıyla (elicitation) değerleri kullanıcıya gösterir. Bu soru modelden geçmez. Kullanıcı onaylarsa hüküm döner (`confirmed_by_user: true`). Onaylamazsa hüküm **verilmez**: cevap `status: not_confirmed` olur ve kayıt defterine yazılmaz. Sensörden gelen değerler onay gerektirmez.
- **İstemci girdi istemeyi desteklemiyorsa** hüküm yine döner, ama `confirmed_by_user: false` ve `unconfirmed_inputs` alanlarıyla ve metinde açık bir uyarıyla. Sonuç metni her değerin kaynağını da yazar.
- **Mesajın değişmeden gösterilmesi istemciye kalır.** Sunucu bunu araç açıklamasında ve sunucu talimatında ister, ama zorlayamaz.

Bu güvencelerin tamamı gerekiyorsa paket, doğrudan çalıştırıcıyla (`skillpack ask`, `skillpack run`) kullanılır.

### 14.5 Bağlı yazılımlar

Çevredeki yazılımlar sunucuya iki yoldan bağlanır:

- **Sensör bağı.** `--sensor ad=dosya`: adı geçen sensörün güncel değeri bir dosyadan okunur. Başka bir yazılım (ölçüm cihazının programı, ev otomasyonu) bu dosyayı günceller. Dosyanın son yazılma anı ölçümün anı sayılır ve `max_age_s` buna göre uygulanır. Sensör okuması istemcinin verdiği değerden önce gelir (Bölüm 7.2); ezilen değer sonuç metninde belirtilir. Paket yalnız `capabilities.sensors` içinde beyan ettiği sensörü okuyabilir.
- **Kayıt defteri.** `--journal dosya`: tamamlanan her çalıştırma (zaman, paket, sürüm, sonuç, değerler, değerlerin kaynağı, kullanıcı onayı) JSON Lines biçiminde eklenir. Başka bir yazılım bu dosyayı okuyabilir.

Bu sürümde bağ yalnız dosya üzerindendir. Ağ üzerinden bağ (ör. bir ev otomasyonu sunucusu) ve paketin başka bir uygulamada eylem başlatması yoktur.

### 14.6 Sınırlar

- Taşıma yalnız stdio'dur.
- Eksik girdinin sorulması, MCP'nin kendi girdi isteme mekanizmasıyla değil, araç cevabındaki `needs_input` durumuyla yapılır. Gerekçe: her istemci bu mekanizmayı desteklemez; düz araç cevabını hepsi okur. Değerlerin onayı ise bu mekanizmayla yapılır (Bölüm 14.4), çünkü onayın modelden geçmemesi gerekir.
- Değer onayı, 2026-07-28 protokol sürümündeki "girdi gerekli" sonucuyla resmî SDK istemcisine karşı sınandı. Daha eski protokol sürümlerindeki sunucudan istemciye istek yolu yazıldı ama sınanmadı.
- Referans sunucu resmî MCP Python SDK'sının istemcisiyle sınandı. Gerçek bir yerel modelin aracı doğru argümanlarla çağırıp çağırmadığı ölçülmedi.

