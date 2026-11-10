# Yerel Beceri Paketi (skillpack)

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

```text
"Tedarikçi tavuk getirdi, kabul edeyim mi?"
        │
        ▼
  yönlendirici (yerel model ya da anahtar kelime)  →  paket: soguk-mal-kabul
        │
        ▼
  çalıştırıcı: imzayı doğrular, akışı yürütür, eksik ölçümü insana sorar
        │
        ▼
  [DUR] Reddedin. tavuk: 6,5 °C (sınır 4 °C) ...   + gerekçe izi
```

Depo kökünde deneyin (Python 3.10+):

```bash
pip install -e cli/
skillpack list
skillpack ask "Tedarikçi tavuk getirdi, kabul edeyim mi?"
```

Üç örnek paket vardır: fabrika (rulman kontrolü), lokanta (soğuk mal kabul), okul (kazanım telafi kararı). Eşik değerleri örnektir; gerçek bir usta onayı taşımazlar ([examples/README.md](examples/README.md)).

| Belge | İçerik |
|---|---|
| [spec/SKILLPACK_v0.1.md](spec/SKILLPACK_v0.1.md) | Standart: paket yapısı, akış profili, modelin sınırı, imza, iptal, uygunluk |
| [docs/USTADAN_PAKETE.md](docs/USTADAN_PAKETE.md) | Yöntem: bir tekniği yedi adımda pakete çevirmek |
| [cli/README.md](cli/README.md) | Çalıştırıcının komutları ve yapısı |

## Durum

**🚧 MVP çalışıyor; standart taslak aşamasında.**

Çalışan: paket doğrulama, kabul testleri, Ed25519 imza ve doğrulama, yerel iptal listesi, belirlenimci akış yürütme, insan onaylı eylem, anahtar kelime ve Ollama yönlendiricisi.

Henüz yok: Sigstore ve şeffaflık günlüğü, imzalı iptal listesi (TUF), dağıtım, fiziksel profil, öğretme döngüsü arayüzü. Ollama yönlendiricisi gerçek bir modelle değil, Ollama yanıt biçimini taklit eden bir test sunucusuyla sınandı. Ayrıntı: spesifikasyon Bölüm 13 ve [ROADMAP.md](ROADMAP.md).

Uzun vadeli hedefler: [docs/TEKNIK_PROJE_v0.1.md](docs/TEKNIK_PROJE_v0.1.md) (9 Kasım 2026, tartışma taslağı) ve [docs/PROJE_DEVAMI.md](docs/PROJE_DEVAMI.md).

## Depo yapısı

| Klasör | İçerik | Durum |
|---|---|---|
| `spec/` | skillpack v0.1-taslak spesifikasyonu | 🚧 Taslak |
| `cli/` | Referans çalıştırıcı (Python): `init`, `validate`, `test`, `keygen`, `sign`, `verify`, `list`, `run`, `ask`, `route-test`; JSON şemaları | 🚧 MVP |
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
