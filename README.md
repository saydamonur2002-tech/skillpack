# Yerel Beceri Paketi (skillpack)

Yerel sunucuda öğretilen, açık, taşınabilir ve imzalı ajan becerileri için bir **açık standart taslağı**. Mevcut [Agent Skills](https://github.com/agentskills) (`SKILL.md`) formatının yerine geçmez; onun üzerine dört katman eklemeyi önerir:

- **Fiziksel uzantı** — prosedür, iş kuralları ve araç çağrılarını, isteğe bağlı robot gösterim/politika verisiyle (ör. LeRobotDataset, ROS 2, OPC UA) tek pakette birleştirmek
- **Güven altyapısı** — imza, şeffaflık günlüğü ve iptal listesi (Sigstore, SLSA, TUF yöntemlerinin beceri paketlerine uyarlanması); dağıtımın aynalar ve P2P ile yapılması
- **Öğretme döngüsü** — geliştirici olmayan bir ustanın gösterimini yerelde kurallara damıtmak, test etmek, insan onayından sonra paketlemek
- **Taşınabilirlik ve yönlendirme** — çalışma zamanından bağımsız paket; telefon ↔ yerel sunucu ↔ isteğe bağlı bulut arasında izin bilgili yönlendirme

Tasarım duruşu muhafazakârdır: ajanlar tanı ve öneri üretir, kararı insan verir; ham müşteri verisi pakete girmez; bulut varsayılan olarak kapalıdır.

Tasarım hedefleri üç çerçevede toplanır: orta segment donanımda çalışabilirlik, görev başına enerji verimliliği ve açık modelle gündelik hayat etkisi. Kabul ölçütü teknik taslağın [Bölüm 2.3](docs/TEKNIK_PROJE_v0.1.md#23-tasarım-hedefleri-üç-çerçeve) başlığındadır.

Bu depo bir şirket, ürün veya pazar yeri değildir. Ticari olmayan, bireysel bir açık kaynak / açık standart katkısıdır.

## Durum

**⬜ Başlamadı / taslak**

Hiçbir faz henüz başlamadı. Güncel plan ve görev listeleri [ROADMAP.md](ROADMAP.md) dosyasındadır. Her faz ayrıca bir GitHub issue olarak da izlenir (`başlamadı` etiketi).

Teknik taslak: [docs/TEKNIK_PROJE_v0.1.md](docs/TEKNIK_PROJE_v0.1.md) (9 Kasım 2026, tartışma taslağı).

## Depo yapısı

| Klasör | İçerik | Durum |
|---|---|---|
| `spec/` | skillpack v0.1 spesifikasyon taslağı | ⬜ Başlamadı |
| `schemas/` | JSON Schema dosyaları (`skillpack.yaml`, `robot_profile.yaml`, iptal listesi, indeks) | ⬜ Başlamadı |
| `examples/` | Örnek beceri paketleri | ⬜ Başlamadı |
| `cli/` | Doğrulayıcı ve paketleyici CLI (`init`, `validate`, `pack`, `sign`, `verify`, `publish`, `revoke-check`) | ⬜ Başlamadı |
| `docs/` | Teknik proje taslağı ve belgeler | Taslak metin mevcut; uygulama başlamadı |

## Yol haritası (özet)

Süreler göreli aylardır (A0 = başlangıç) ve [VARSAYIM] niteliğindedir. Ayrıntılı görevler için [ROADMAP.md](ROADMAP.md).

| Faz | Süre | Durum |
|---|---|---|
| F0 — Hazırlık | A0–A2 | ⬜ Başlamadı |
| F1 — Çekirdek | A2–A6 | ⬜ Başlamadı |
| F2 — Yerel çalışma | A5–A9 | ⬜ Başlamadı |
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

Katkılar hoş gelir. Henüz katkı rehberi yazılmadı (F0 / F6). Şimdilik bir issue açmak veya taslağa yorum bırakmak yeterlidir.
