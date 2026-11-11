# Yerel Beceri Paketi (skillpack)

## Adım Şablonu ve Mekanizma (v0.1-taslak)

> Bu bölüm bir **taslaktır**. Şablon boştur; hiçbir değeri gerçek bir uzman onaylamamıştır.
> Mevcut referans çalıştırıcı (`cli/`) bu şablonun tüm alanlarını henüz uygulamaz; aşağıda "Uygulama durumu"na bakın.

### Temel ilke

**Model bir şey öğrenmez, sadece çevirir.** Tekniğin bilgisi modelin içinde değil, pakettedir.

```
İnsan  ⇄  Yerel LLM (tercüman)  ⇄  MCP (bağlantı)  ⇄  DİKEY TEKNİK PAKETİ (merkez)  ⇄  Uygulamalar/makineler (çevre)
```

- **Merkez:** tekniğin adımları, ölçütleri, sınırları, testleri, kökeni.
- **Çevre:** işi fiilen yapan yazılım ve makineler. Değiştirilebilir; aynı arayüzü sunan her biri takılabilir.
- **LLM:** insanın söylediğini yapılandırılmış değere çevirir, sonucu anlatır. Karar vermez.

### Üç dosya

| Dosya | Ne tutar | Kim değiştirir |
|---|---|---|
| [`sablon/adim.sablon.yaml`](sablon/adim.sablon.yaml) | Tekniğin tek bir adımı: amaç, girdi, ön koşul, tehlike, işlem, etki, doğrulama, bağlayıcı, LLM sınırı, test, köken | Usta / paket yazarı |
| [`sablon/profil.sablon.yaml`](sablon/profil.sablon.yaml) | İşletmeye özel değerler (örn. azami ağırlık 25 kg) ve değişiklik kaydı | İşletme, onayla |
| [`sablon/paket.sablon.yaml`](sablon/paket.sablon.yaml) | Adımların sırası, gereken arayüzler, kılavuz, imza | Paket yazarı |

### Bir adım nasıl çalışır

1. **Girdileri topla.** Öncelik sabittir: `sensör > kayıt > insan > LLM`. Alttaki kaynak üsttekini asla ezemez. Sensör verisi `tazelik_sn`'den eskiyse kullanılmaz.
2. **Sert sınırı kontrol et.** Değer fiziksel/yasal sınırın dışındaysa reddedilir. Profil bu sınırı genişletemez.
3. **Tehlike kurallarına bak.** Eksik veri olsa bile önce bunlar değerlendirilir. Bilinen tek bir tehlike `dur` için yeterlidir; "bilinmiyor"a düşmez.
4. **Ön koşulları kontrol et.** Sağlanmazsa adım başlamaz (`bekle`, `sor` veya `dur`).
5. **İşlemi yürüt.** Hesap, tablo veya karar; kesin koddur, tahmin değildir.
6. **Bağlayıcıyı çağır.** Varsayılan izin `oneri`dir: sistem önerir, insan onaylar.
7. **Doğrula.** Aracın "başardım" demesi yetmez; ölçümle `basarili / basarisiz / bilinmiyor` ayrılır.
8. **Başarısızsa** tanımlı yol izlenir: tekrar, geri al, dur veya insana sor.

### Profil değişikliği nasıl yapılır

```
"Kutular artık 25 kg"  →  LLM öneri yazar (max_agirlik: 25)
                       →  Şema kontrolü (sert sınır içinde mi?)
                       →  İnsan onayı
                       →  Testler yeniden koşar
                       →  Değişiklik kaydına yazılır, profil sürümü artar
```
Kod değişmez. Testlerden biri düşerse değişiklik uygulanmaz.

### Dikey işlere nasıl uyarlanır

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
4. Her adıma en az bir normal, bir sınır, bir tehlike testi yaz.
5. Bağlayıcıyı arayüz adıyla yaz; hangi yazılımın takılacağı sahada seçilir.
6. Usta onaylamadan paket `DEMO` etiketiyle yüklenir.

### Uygulama durumu (dürüst not)

| Özellik | Durum |
|---|---|
| Akış, tablo, karar, test, Ed25519 imza, MCP sunucusu | Mevcut çalıştırıcıda **var** |
| Kaynak önceliği (sensör > LLM), tazelik kontrolü | **Yok** — şu an LLM argümanı sensör değerini ezebiliyor |
| Eksik veride önce tehlike kuralı | **Yok** — bilinen tehlike "bilinmiyor"a düşebiliyor |
| Amaç / ön koşul / etki / doğrulama alanları | **Yok** — bu şablonla tanımlandı |
| Profil – sert sınır ayrımı, onaylı değişiklik akışı | **Yok** |
| Bağlayıcı arayüzleri | **Yok** |
| Boş beklentili testin reddi | **Yok** — şu an geçiyor sayılıyor |

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

Çalışan: paket doğrulama, kabul testleri, Ed25519 imza ve doğrulama, yerel iptal listesi, belirlenimci akış yürütme, insan onaylı eylem, paketleri araç olarak sunan MCP sunucusu (dosya tabanlı sensör bağı ve kayıt defteriyle), terminalde anahtar kelime ve Ollama yönlendiricisi.

Henüz yok: Sigstore ve şeffaflık günlüğü, imzalı iptal listesi (TUF), dağıtım, fiziksel profil, öğretme döngüsü arayüzü. MCP sunucusu resmî MCP Python istemcisiyle sınandı, ama gerçek bir yerel modelin araçları doğru çağırıp çağırmadığı ölçülmedi; Ollama yönlendiricisi de yalnız Ollama yanıt biçimini taklit eden bir test sunucusuyla sınandı. Ayrıntı: spesifikasyon Bölüm 13 ve [ROADMAP.md](ROADMAP.md).

Uzun vadeli hedefler: [docs/TEKNIK_PROJE_v0.1.md](docs/TEKNIK_PROJE_v0.1.md) (9 Kasım 2026, tartışma taslağı) ve [docs/PROJE_DEVAMI.md](docs/PROJE_DEVAMI.md).

## Depo yapısı

| Klasör | İçerik | Durum |
|---|---|---|
| `spec/` | skillpack v0.1-taslak spesifikasyonu | 🚧 Taslak |
| `cli/` | Referans çalıştırıcı (Python): `init`, `validate`, `test`, `keygen`, `sign`, `verify`, `list`, `run`, `ask`, `serve` (MCP), `route-test`; JSON şemaları | 🚧 MVP |
| `examples/` | Üç imzalı örnek paket ve güvenilen açık anahtar | 🚧 Örnek (usta onayı yok) |
| `schemas/` | Şemaların yerini gösterir (`cli/skillpack/schemas/`) | 🚧 MVP alt kümesi |
| `docs/` | Yöntem belgesi, teknik taslak, tartışma notları | Taslak |
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

Öneren bir kamu görevlisidir. 657 sayılı Devlet Memurları Kanunu md. 28 çerçevesinde proje açık standart ve açık kaynak katkısı olarak kurgulanmıştır. Bu not hukuki görüş değildir. Gelir, lisans devri veya vakıf görevi gibi adımlardan önce bağlı olunan kurumun personel biriminden ve bir avukattan yazılı görüş alınması F0 fazının çıkış ölçütüdür. Ayrıntı: teknik taslak, Bölüm 14.

Katkılar hoş gelir. Henüz katkı rehberi yazılmadı (F0 / F6). Şimdilik bir issue açmak veya taslağa yorum bırakmak yeterlidir. En değerli katkı, kendi işini bilen birinin yazdığı ve onayladığı gerçek bir pakettir.
