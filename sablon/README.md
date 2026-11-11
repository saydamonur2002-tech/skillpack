# Adım Şablonu ve Mekanizma (v0.1-taslak)

> Bu bölüm bir **taslaktır**. Şablon ve örnek, gerçek bir uzman onayı taşımaz. Örnek paket `DEMO` etiketlidir.
> Mevcut referans çalıştırıcı (`cli/`) bu şablonun alanlarını henüz uygulamaz; aşağıda "Uygulama durumu"na bakın.

## Temel ilke

**Model bir şey öğrenmez, sadece çevirir.** Tekniğin bilgisi modelin içinde değil, pakettedir.

```
İnsan  ⇄  Yerel LLM (tercüman)  ⇄  MCP (bağlantı)  ⇄  DİKEY TEKNİK PAKETİ (merkez)  ⇄  Uygulamalar/makineler (çevre)
```

- **Merkez:** tekniğin adımları, ölçütleri, sınırları, testleri, kökeni.
- **Çevre:** işi fiilen yapan yazılım ve makineler. Değiştirilebilir; aynı arayüzü sunan her biri takılabilir.
- **LLM:** insanın söylediğini yapılandırılmış değere çevirir, sonucu anlatır. Karar vermez, sensörü ezmez, sert sınırı değiştirmez, eylem başlatmaz.
- **Ana model (32B)** yerel sunucudadır; paketler orada kurulur. Telefon arayüz ve küçük yardımcı model (1,5B–8B) içindir. Bulut yalnız insan onayıyla.

## Paket klasörü

Her dikey teknik tek bir klasördür. Boş iskelet: [`iskelet/`](iskelet/). Dolu örnek (kutu kaldırma, DEMO): [`ornek-kutu-kaldirma/`](ornek-kutu-kaldirma/). Kurulum sırası: [`KURULUM.md`](KURULUM.md).

```text
<paket>/
├─ paket.yaml                 # kimlik, alan, adımların sırası, gereken arayüzler
├─ adimlar/                   # her adım ayrı dosya
│   └─ 01-....yaml
├─ kurallar/
│   ├─ sert_sinirlar.yaml     # değişmez sınırlar (yasa, fizik, cihaz etiketi)
│   └─ tehlike.yaml           # "görünce dur" kuralları
├─ profil.yaml                # işletmeye özel, değişebilir değerler
├─ donanim.yaml               # cihaz yeteneği + anlık durum (anlam katmanı)
├─ veri/                      # referans tablolar (CSV); ham müşteri verisi yok
├─ testler/                   # normal, sınır, tehlike; boş beklenti = geçersiz
├─ sorular/                   # paketleme oyunu: soru + tuzak senaryosu
├─ SKILL.md                   # LLM kılavuzu (yalnız çeviri)
└─ imza.json                  # Ed25519 imza + onaylayan + dayanak
```

Alanların tek tek açıklaması, durağan şablon dosyalarında durur: [`adim.sablon.yaml`](adim.sablon.yaml), [`profil.sablon.yaml`](profil.sablon.yaml), [`paket.sablon.yaml`](paket.sablon.yaml).

Kural değişmez, profil değişir, veri referanstır, test kanıttır. Her biri farklı izinle değişir.

## Donanım ve anlam katmanı

`donanim.yaml` modelin okuduğu tariftir: her cihaz bir arayüz kimliğiyle (`sensor.agirlik.v1`, `kaldirici.v1` gibi) anılır; türü (sensör / eylemci / yazılım), ölçüm aralığı, hassasiyet, birim, tazelik, yapabildikleri, sınırı, bağlantısı (yerel) ve anlık durumu yazılır. Aynı arayüzü sunan başka bir makine takılabilir.

`durum` bölümü, şu an hangi ön koşulların sağlandığını gösterir. Model burayı okuyarak "şimdi ne yapılabilir"i görür; karar vermez.

MCP araç tarifi yalnız parametre listesi olamaz. Modele **amaç, ön koşul, etki, donanım ve mevcut durum** birlikte verilmelidir. Ayrıntı: [`KURULUM.md`](KURULUM.md#anlam-katmanı).

## Kurulum, sonra MCP

Paket bir uygulama gibi yerel sunucuya yüklenir. Sıra sabittir: imza + iptal, şema, sert sınır / tehlike dolu mu, testler bu cihazda geçer mi, gereken arayüzler `donanim.yaml`'da var mı, profil sert sınırı aşmıyor mu, kayıt + sürüm + geri dönüş. **Ancak bunlar geçtikten sonra** paket MCP'de tek bir araç olarak görünür. Kurulu olmayan paket model tarafından görülmez. Ayrıntı: [`KURULUM.md`](KURULUM.md).

## Bir adım nasıl çalışır

1. **Girdileri topla.** Öncelik sabittir: `sensör > kayıt > insan > LLM`. Alttaki kaynak üsttekini asla ezemez. Sensör verisi `tazelik_sn`'den eskiyse kullanılmaz.
2. **Sert sınırı kontrol et.** Değer fiziksel/yasal sınırın dışındaysa reddedilir. Profil bu sınırı genişletemez.
3. **Tehlike kurallarına bak.** Eksik veri olsa bile önce bunlar değerlendirilir. Bilinen tek bir tehlike `dur` için yeterlidir; "bilinmiyor"a düşmez.
4. **Ön koşulları kontrol et.** Sağlanmazsa adım başlamaz (`bekle`, `sor` veya `dur`).
5. **İşlemi yürüt.** Hesap, tablo veya karar; kesin koddur, tahmin değildir.
6. **Bağlayıcıyı çağır.** Varsayılan izin `oneri`dir: sistem önerir, insan onaylar.
7. **Doğrula.** Aracın "başardım" demesi yetmez; ölçümle `basarili / basarisiz / bilinmiyor` ayrılır.
8. **Başarısızsa** tanımlı yol izlenir: tekrar, geri al, dur veya insana sor.

## Profil değişikliği nasıl yapılır

```
"Kutular artık 25 kg"  →  LLM öneri yazar (max_agirlik: 25)
                       →  Şema kontrolü (sert sınır içinde mi?)
                       →  İnsan onayı
                       →  Testler yeniden koşar
                       →  Değişiklik kaydına yazılır, profil sürümü artar
```
Kod değişmez. Testlerden biri düşerse değişiklik uygulanmaz.

## Paketleme oyunu

Usta kod yazmaz. `sorular/` içindeki her alan bir karttır: soruya cevap verilir, tuzak senaryosu çözülünce test kendiliğinden yazılır. Tehlike veya doğrulama boşsa kart kırmızı kalır. Bu, tekniği paketlemenin kendisidir; paketin süsü değildir. Sert sınır, tehlike kuralı ve gerçek eylem izni oyunun dışında kalır.

## Dikey işlere nasıl uyarlanır

Şablon aynı kalır; her sektör sadece içini doldurur.

| Alan | Örnek adım | Girdi / sensör | Tehlike kuralı | Bağlayıcı arayüz | Doğrulama |
|---|---|---|---|---|---|
| Depo / robotik | Kutu kaldır | ağırlık sensörü, kavrama durumu | ağırlık > azami ⇒ dur | `kaldirici.v1` | yükseklik sensörü ±2 cm |
| Mutfak | Soğuk mal kabul | saplama termometre, SKT | ambalaj hasarlı ⇒ ret | `kayit_defteri.v1` | teslim fişi notu |
| Fabrika bakım | Rulman kontrol | ısı, titreşim | ısı ≥ sınır ⇒ dur | `bakim_emri.v1` | ölçüm tekrarı |
| Telefon | Pil koruma | pil %, sıcaklık, termal durum | sıcaklık ≥ 40 °C ⇒ bulutu kapat | `android_sistem.v1` | sonraki ölçüm |
| Hastane | Randevu dağıtımı | doluluk, bekleme süresi | acil işaret ⇒ insana | `randevu_sistemi.v1` | atama kaydı |
| Okul | Kazanım telafi | sınav puanı, devam | — | `not_sistemi.v1` | sonraki ölçme |

Uyarlama sırası:
1. Tekniği bilen kişiyle işi **küçük adımlara** böl.
2. Her adım için şablonu doldur; özellikle **tehlike** ve **doğrulama** alanlarını boş bırakma.
3. Değişen değerleri **profile**, değişmez sınırları **sert_sinir**'a ayır.
4. Her adıma en az bir normal, bir sınır, bir tehlike testi yaz. Boş beklentili test geçersizdir.
5. Bağlayıcıyı arayüz adıyla yaz; hangi yazılımın takılacağı sahada seçilir.
6. Usta onaylamadan paket `DEMO` etiketiyle yüklenir.

## Uygulama durumu (dürüst not)

| Özellik | Durum |
|---|---|
| Akış, tablo, karar, test, Ed25519 imza, MCP sunucusu | Mevcut çalıştırıcıda **var** |
| Kaynak önceliği (sensör > LLM), tazelik kontrolü | **Var** — `flow.yaml` biçiminde (`sensor`, `max_age_s`); `kayıt` kaynağı yok |
| Eksik veride önce tehlike kuralı | **Var** — `flow.yaml` içindeki `hazards` bölümüyle |
| Amaç / ön koşul / etki / doğrulama alanları | **Yok** — bu şablonla tanımlandı |
| Profil – sert sınır ayrımı, onaylı değişiklik akışı | **Yok** — yalnız şablonda |
| Bağlayıcı arayüzleri | **Yok** |
| Boş beklentili testin reddi | **Var** |
| Donanım tarifi ve anlam katmanı (`donanim.yaml`, MCP amaç/ön koşul/etki/durum) | **Yok** — yalnız şablonda |
| Kurulum kontrolleri (imza+iptal sırası, arayüz var mı, sürüm geri dönüşü) ve MCP'den önce kurulum | **Yok** — yalnız [`KURULUM.md`](KURULUM.md)'de |
| `sorular/` paketleme oyunu | **Yok** — yalnız şablonda |
| Adımların ayrı dosya, kural / profil / veri ayrımı (iskelet biçimi) | **Yok** — yalnız şablonda |

"Var" yazan satırlar çalıştırıcının kendi biçiminde (`flow.yaml`, [spec/SKILLPACK_v0.1.md](../spec/SKILLPACK_v0.1.md) Bölüm 6.7 ve 7.2) uygulanmıştır; bu şablonun Türkçe alan adlarıyla (`tazelik_sn`, `tehlike`) değil.

Bu şablon bir **sözleşme taslağıdır**; çalıştırıcının bunu uygulaması sonraki iştir.
