# Yerel Beceri Paketi (skillpack)

> **Vizyon:** Ustanın tekniğini, mikro ölçekte, kod yazmadan bir makineye veya robota aktaran basit bir kurulum ve onun açık standardı. Beceri ve tarif katmanları mevcut standartlara (OPC UA, PackML, ISA-88, MTP) uyumlanır; asıl katkı eksik olan **anlatım mekanizmasıdır**: tekniğin ustadan çıkarılması ve modele anlatılması. Ayrıntı: [`VIZYON.md`](VIZYON.md)

## Açık kaynak işlev paketleri (`kutuphane/`)

Açık kaynak projelerdeki tek işlevlerden çıkarılmış, internetsiz çalışan ve kaynağı/lisansı kayıtlı **46 beceri paketi** (harita, hesap, doğrulama, cihaz protokolü, dil). Hepsi kendi testlerinden geçti (ağ kapalı, 670 test); bir kısmı bağımsız karşılaştırmayla doğrulandı, çoğu yalnızca sözleşme testli. **Hiçbiri onaylı değildir.** Doğruluk düzeyleri, bilinen sınırlar ve bu ön sürümde bulunmayan 7 paket: [`kutuphane/README.md`](kutuphane/README.md).

## Adım Şablonu ve Mekanizma (v0.1-taslak)

> Bu bölüm bir **taslaktır**. Şablon ve örnek, gerçek bir uzman onayı taşımaz. Örnek paket `DEMO` etiketlidir.
> Mevcut referans çalıştırıcı (`cli/`) bu alanları henüz uygulamaz; "Uygulama durumu"na bakın. Ayrıntı: [`sablon/README.md`](sablon/README.md), kurulum: [`sablon/KURULUM.md`](sablon/KURULUM.md).

**Model bir şey öğrenmez, sadece çevirir.** Tekniğin bilgisi modelin içinde değil, pakettedir.

```
İnsan  ⇄  Yerel LLM (tercüman)  ⇄  MCP (bağlantı)  ⇄  DİKEY TEKNİK PAKETİ (merkez)  ⇄  Uygulamalar/makineler (çevre)
```

Ana model (32B) yerel sunucudadır; paketler orada kurulur. Telefon arayüz ve küçük yardımcı model (1,5B–8B) içindir. Bulut yalnız insan onayıyla. LLM karar vermez, sensörü ezmez, sert sınırı değiştirmez, eylem başlatmaz.

### Paket klasörü

Boş iskelet: [`sablon/iskelet/`](sablon/iskelet/). Dolu örnek (kutu kaldırma, DEMO): [`sablon/ornek-kutu-kaldirma/`](sablon/ornek-kutu-kaldirma/).

```text
<paket>/
├─ paket.yaml                 # kimlik, alan, adımların sırası, gereken arayüzler
├─ adimlar/                   # her adım ayrı dosya
├─ kurallar/                  # sert_sinirlar.yaml (değişmez) + tehlike.yaml
├─ profil.yaml                # işletmeye özel, değişebilir
├─ donanim.yaml               # cihaz yeteneği + anlık durum (anlam katmanı)
├─ veri/                      # referans tablolar (CSV); ham müşteri verisi yok
├─ testler/                   # normal, sınır, tehlike; boş beklenti = geçersiz
├─ sorular/                   # paketleme oyunu: soru + tuzak senaryosu
├─ SKILL.md                   # LLM kılavuzu (yalnız çeviri)
└─ imza.json
```

`donanim.yaml` modelin okuduğu tariftir: her cihaz bir arayüz kimliğiyle anılır (ör. `sensor.agirlik.v1`, `kaldirici.v1`); tür, ölçüm aralığı, hassasiyet, tazelik, yapabildikleri, sınır, yerel bağlantı ve anlık durumu yazar. `durum` hangi ön koşulların sağlandığını gösterir.

MCP araç tarifi yalnız parametre listesi olamaz: modele **amaç, ön koşul, etki, donanım ve mevcut durum** birlikte verilir. Model bu tarifi okuyup isteği eşler; yürütmez.

### Kurulum, sonra MCP

Paket bir uygulama gibi yerel sunucuya yüklenir. Sıra: imza + iptal, şema, sert sınır / tehlike dolu mu, testler bu cihazda geçer mi, gereken arayüzler `donanim.yaml`'da var mı, profil sert sınırı aşmıyor mu, kayıt + sürüm + geri dönüş. **Ancak bunlar geçtikten sonra** paket MCP'de tek bir araç olarak görünür. Kurulu olmayan paket model tarafından görülmez. Ayrıntı: [`sablon/KURULUM.md`](sablon/KURULUM.md).

### Bir adım nasıl çalışır

1. **Girdileri topla.** Öncelik sabittir: `sensör > kayıt > insan > LLM`. Alttaki kaynak üsttekini asla ezemez. Sensör verisi `tazelik_sn`'den eskiyse kullanılmaz.
2. **Sert sınırı kontrol et.** Değer fiziksel/yasal sınırın dışındaysa reddedilir. Profil bu sınırı genişletemez.
3. **Tehlike kurallarına bak.** Eksik veri olsa bile önce bunlar değerlendirilir. Bilinen tek bir tehlike `dur` için yeterlidir; "bilinmiyor"a düşmez.
4. **Ön koşulları kontrol et.** Sağlanmazsa adım başlamaz (`bekle`, `sor` veya `dur`).
5. **İşlemi yürüt.** Hesap, tablo veya karar; kesin koddur, tahmin değildir.
6. **Bağlayıcıyı çağır.** Varsayılan izin `oneri`dir: sistem önerir, insan onaylar.
7. **Doğrula.** Aracın "başardım" demesi yetmez; ölçümle `basarili / basarisiz / bilinmiyor` ayrılır.
8. **Başarısızsa** tanımlı yol izlenir: tekrar, geri al, dur veya insana sor.

Profil değişikliği: LLM önerir, şema sert sınırı kontrol eder, insan onaylar, testler yeniden koşar. Kod değişmez.

### Uygulama durumu (dürüst not)

| Özellik | Durum |
|---|---|
| Akış, tablo, karar, test, Ed25519 imza, MCP sunucusu | Mevcut çalıştırıcıda **var** |
| Kaynak önceliği (sensör > LLM), tazelik kontrolü | **Var** — sensör okuması model değerinden önce gelir; `max_age_s` beyan edilmişse bayat okuma kullanılmaz. `kayıt` kaynağı yok |
| Eksik veride önce tehlike kuralı | **Var** — `flow.yaml` içindeki `hazards` bölümüyle; üç örnek paket bunu henüz beyan etmiyor |
| İmzalı iptal listesi, geri sarma koruması | **Var** — TUF ile (`skillpack revocations`), kurulum kaydı ile (`--state`) |
| Modelin aktardığı değerin kullanıcıya onaylatılması (MCP) | **Var** — istemci girdi istemeyi destekliyorsa; yoksa uyarılı sonuç |
| Amaç / ön koşul / etki / doğrulama alanları | **Yok** — bu şablonla tanımlandı |
| Profil – sert sınır ayrımı, onaylı değişiklik akışı | **Yok** — yalnız şablonda |
| Bağlayıcı arayüzleri | **Yok** |
| Boş beklentili testin reddi | **Var** — beklentisiz test paketi geçersiz kılar |
| Donanım tarifi ve anlam katmanı (`donanim.yaml`, MCP amaç/ön koşul/etki/durum) | **Yok** — yalnız şablonda |
| Kurulum kontrolleri ve MCP'den önce kurulum | **Yok** — yalnız [`sablon/KURULUM.md`](sablon/KURULUM.md)'de |
| `sorular/` paketleme oyunu | **Yok** — yalnız şablonda |
| Adımların ayrı dosya, kural / profil / veri ayrımı (iskelet biçimi) | **Yok** — yalnız şablonda |

Bu şablon bir **sözleşme taslağıdır**; çalıştırıcının bunu uygulaması sonraki iştir.

---

Yerel sunucuda öğretilen, açık, taşınabilir ve imzalı ajan becerileri için bir **açık standart taslağı**. Mevcut [Agent Skills](https://github.com/agentskills) (`SKILL.md`) formatının yerine geçmez; onun üzerine dört katman eklemeyi önerir:

- **Fiziksel uzantı** — prosedür, iş kuralları ve araç çağrılarını, isteğe bağlı robot gösterim/politika verisiyle (ör. LeRobotDataset, ROS 2, OPC UA) tek pakette birleştirmek
- **Güven altyapısı** — imza, şeffaflık günlüğü ve iptal listesi (Sigstore, SLSA, TUF yöntemlerinin beceri paketlerine uyarlanması); dağıtımın aynalar ve P2P ile yapılması
- **Öğretme döngüsü** — geliştirici olmayan bir ustanın gösterimini yerelde kurallara damıtmak, test etmek, insan onayından sonra paketlemek
- **Taşınabilirlik ve yönlendirme** — çalışma zamanından bağımsız paket; telefon ↔ yerel sunucu ↔ isteğe bağlı bulut arasında izin bilgili yönlendirme

Tasarım duruşu muhafazakârdır: ajanlar tanı ve öneri üretir, kararı insan verir; ham müşteri verisi pakete girmez; bulut varsayılan olarak kapalıdır.

Tasarım hedefleri üç çerçevede toplanır: orta segment donanımda çalışabilirlik, görev başına enerji verimliliği ve açık modelle gündelik hayat etkisi. Kabul ölçütü teknik taslağın [Bölüm 2.3](docs/TEKNIK_PROJE_v0.1.md#23-tasarım-hedefleri-üç-çerçeve) başlığındadır.

Bu depo bir şirket, ürün veya pazar yeri değildir. Ticari olmayan, bireysel bir açık kaynak / açık standart katkısıdır.

## Ne çalışıyor

Bir ustanın tekniği bir **pakete** çevrilir; yerel bir dil modeli bu paketi **uygular**. Niş işte model karar vermez: kararı paketteki akış verir, akışı çalıştırıcı yürütür. Modelin işi yalnız kullanıcının cümlesinden doğru paketi seçmek ve söylenen değerleri çıkarmaktır.

Mimari merkez ve çevre biçimindedir. Bağlantı standardı MCP'dir (Model Context Protocol):

```text
        MERKEZ                  MCP                     ÇEVRE
  yerel modeli çalıştıran   ◄────────►   skillpack sunucusu
  uygulama                                 ├─ dikey teknik: rulman kontrolü ──► sensör
  (kullanıcıyla konuşur)                   ├─ dikey teknik: soğuk mal kabul ──► kayıt defteri
                                           └─ dikey teknik: kazanım telafisi
```

Merkez genel araçlar yerine dikey teknikleri görür. Model bir tekniği çağırır; teknik eksik ölçümü geri sorar, sonra hükmü verir:

```text
"Tedarikçi tavuk getirdi, 6,5 derece ölçtüm"
  → araç: soguk-mal-kabul {product: tavuk, core_temp_c: 6.5}
  ← eksik: "Ambalaj yırtık, ezik, şişmiş ya da sızdırıyor mu?"
  → ... {package_damaged: false, days_to_expiry: 5}
  ← [DUR] Reddedin. tavuk: 6,5 °C (sınır 4 °C) ...   + kullanılan değerler
```

Depo kökünde deneyin (Python 3.10+):

```bash
pip install -e "cli/[mcp]"
skillpack list
skillpack ask "Tedarikçi tavuk getirdi, kabul edeyim mi?"   # MCP'siz, doğrudan terminalde
skillpack serve                                              # MCP sunucusu (stdio)
```

MCP destekleyen bir uygulamaya bağlamak için: [cli/README.md](cli/README.md#mcp-sunucusu).

Üç örnek paket vardır: fabrika (rulman kontrolü), lokanta (soğuk mal kabul), okul (kazanım telafi kararı). Eşik değerleri örnektir; gerçek bir usta onayı taşımazlar ([examples/README.md](examples/README.md)).

| Belge | İçerik |
|---|---|
| [spec/SKILLPACK_v0.1.md](spec/SKILLPACK_v0.1.md) | Standart: paket yapısı, akış profili, modelin sınırı, imza, iptal, uygunluk, MCP bağlaması |
| [docs/USTADAN_PAKETE.md](docs/USTADAN_PAKETE.md) | Yöntem: bir tekniği yedi adımda pakete çevirmek |
| [cli/README.md](cli/README.md) | Çalıştırıcının komutları ve yapısı |

## Durum

**🚧 MVP çalışıyor; standart taslak aşamasında.**

Çalışan: paket doğrulama, kabul testleri, Ed25519 imza ve doğrulama, TUF ile imzalı iptal listesi (kurcalama, geri sarma ve dondurma reddedilir), geri sarma ve yayıncı değişimine karşı kurulum kaydı, belirlenimci akış yürütme, sabit kaynak önceliği ve sensör tazeliği, tehlike kuralları, insan onaylı eylem, paketleri araç olarak sunan MCP sunucusu (dosya tabanlı sensör bağı, kayıt defteri ve değerlerin kullanıcıya doğrudan onaylatılmasıyla), terminalde anahtar kelime ve Ollama yönlendiricisi.

Henüz yok: Sigstore ve şeffaflık günlüğü, paketlerin dağıtımı, paket adlarını yayıncılara bağlayan imzalı indeks, fiziksel profil, öğretme döngüsü arayüzü. Üç örnek paket yeni `hazards` ve `max_age_s` alanlarını kullanmıyor; eklenince yayıncı anahtarıyla yeniden imzalanmaları gerekir. MCP sunucusu resmî MCP Python istemcisiyle sınandı, ama gerçek bir yerel modelin araçları doğru çağırıp çağırmadığı ölçülmedi; Ollama yönlendiricisi de yalnız Ollama yanıt biçimini taklit eden bir test sunucusuyla sınandı. Ayrıntı: spesifikasyon Bölüm 13 ve [ROADMAP.md](ROADMAP.md).

Uzun vadeli hedefler: [docs/TEKNIK_PROJE_v0.1.md](docs/TEKNIK_PROJE_v0.1.md) (9 Kasım 2026, tartışma taslağı) ve [docs/PROJE_DEVAMI.md](docs/PROJE_DEVAMI.md).

## Depo yapısı

| Klasör | İçerik | Durum |
|---|---|---|
| `spec/` | skillpack v0.1-taslak spesifikasyonu | 🚧 Taslak |
| `cli/` | Referans çalıştırıcı (Python): `init`, `validate`, `test`, `keygen`, `sign`, `verify`, `list`, `run`, `ask`, `serve` (MCP), `route-test`; JSON şemaları | 🚧 MVP |
| `examples/` | Üç imzalı örnek paket ve güvenilen açık anahtar | 🚧 Örnek (usta onayı yok) |
| `schemas/` | Şemaların yerini gösterir (`cli/skillpack/schemas/`) | 🚧 MVP alt kümesi |
| `docs/` | Yöntem belgesi, teknik taslak, tartışma notları | Taslak |
| `sablon/` | Adım şablonu, boş iskelet, kutu kaldırma örneği (DEMO), kurulum sırası | 🚧 Taslak (çalıştırıcı uygulamıyor) |
| `apps/hybrid_assistant` | Erken deneme: Flutter + Firebase AI Logic ile telefon pili/ısı asistanı. skillpack biçimini kullanmaz | 🧪 Deneme |

## Yol haritası (özet)

Süreler göreli aylardır (A0 = başlangıç) ve [VARSAYIM] niteliğindedir. Ayrıntılı görevler için [ROADMAP.md](ROADMAP.md).

| Faz | Süre | Durum |
|---|---|---|
| F0 — Hazırlık | A0–A2 | 🚧 Başladı (spesifikasyon taslağı) |
| F1 — Çekirdek | A2–A6 | 🚧 Başladı |
| F2 — Yerel çalışma | A5–A9 | 🚧 Başladı (yönlendirici, yerel depo) |
| F3 — Fiziksel profil | A8–A12 | ⬜ Başlamadı |
| F4 — Dağıtım ve iptal | A10–A14 | ⬜ Başlamadı |
| F5 — Pilot | A12–A18 | ⬜ Başlamadı |
| F6 — Yönetişim | A12–A24 | ⬜ Başlamadı |

Önerilen sıra: önce topluluk projesi (bu depo), olgunlaşınca Linux Foundation bünyesindeki AAIF'e çalışma grubu önerisi.

## Lisans

- **Kod** (CLI, şemalar, referans uygulama): [Apache License 2.0](LICENSE)
- **Spesifikasyon metni ve veri** (taslak belge, örnek paket içerikleri, yol haritası): [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)

## Katkı ve hukuki not

Proje **ticari değildir**. Şirket, ürün, pazar yeri veya ücretli hizmet olarak yürütülmez.

Çalışma mesai dışında, kurum bilgisayarı ve kurum kaynakları kullanılmadan, kurumla ilgili gizli bilgi konulmadan yürütülür.

Katkılar hoş gelir. Henüz katkı rehberi yazılmadı (F0 / F6). Şimdilik bir issue açmak veya taslağa yorum bırakmak yeterlidir. En değerli katkı, kendi işini bilen birinin yazdığı ve onayladığı gerçek bir pakettir.
