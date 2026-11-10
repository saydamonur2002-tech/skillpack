# F1 açık kaynak bileşenleri

F1 çekirdeği için benimsenen hazır araçlar. Bu liste bir kurulum betiği değildir. Doğrulayıcı, imza ve simülasyon bu depoda henüz çalışmıyor. Faz durumu: ⬜ Başlamadı.

Okuma tarihi: 10 Kasım 2026. Bağlantıların hepsi bu tarihte açıldı.

Kaynak etiketleri teknik taslaktaki gibidir: `[VERİ]` birincil sayfa, `[VEKİL]` aktarım, `[VARSAYIM]` tasarım seçimi, `[EKSİK]` doğrulanmadı.

## Benimsenenler

| Bileşen | Lisans | Bağlantı | Rol |
|---|---|---|---|
| Agent Skills spesifikasyonu | Kod ve spesifikasyon katkısı Apache-2.0; belge CC-BY-4.0 `[VERİ]` | [agentskills.io/specification](https://agentskills.io/specification), [depo](https://github.com/agentskills/agentskills) | `SKILL.md` ön bilgisi. Zorunlu alanlar `name` ve `description`. `metadata` dizge→dizge |
| NVIDIA skill kartı | Depo Apache-2.0 `[VERİ]` | [skill-cards](https://docs.nvidia.com/skills/skill-cards), [NVIDIA/skills](https://github.com/NVIDIA/skills) | İmza öncesi kartın hangi soruları taşıyacağına referans. NVIDIA kök sertifikası bu pakette kullanılmaz |
| OpenSSF model-signing | Apache-2.0 `[VERİ]` | [sigstore/model-transparency](https://github.com/sigstore/model-transparency) | Dizin imzası için referans (`model-signing`, OMS). `skill.oms.sig` üretmek F1 kodu ister; bu PR üretmez |
| MCP Registry `server.schema.json` | Yeni katkı Apache-2.0, belge CC-BY-4.0; eski MIT katkıları duruyor `[VERİ]` | [şema 2025-12-11](https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json), [depo](https://github.com/modelcontextprotocol/registry) | İlerideki paket indeksi için şema referansı. Şema dosyası bu depoya kopyalanmadı |
| python-jsonschema | MIT `[VERİ]` | [depo](https://github.com/python-jsonschema/jsonschema) | `validate` için JSON Schema motoru |
| check-jsonschema | Apache-2.0 `[VERİ]` | [depo](https://github.com/python-jsonschema/check-jsonschema) | Şema dosyasını komut satırından denetlemek |
| sigstore-python | Apache-2.0 `[VERİ]` | [depo](https://github.com/sigstore/sigstore-python) | `sign` / `verify` için Sigstore istemcisi. Bu PR imza üretmez |
| in-toto attestation | Apache-2.0 `[VERİ]` | [depo](https://github.com/in-toto/attestation) | Köken beyanının (provenance) biçimi |
| SLSA şartnamesi | Community Specification License 1.0 `[VERİ]` | [LICENSE.md](https://github.com/slsa-framework/slsa/blob/main/LICENSE.md), [slsa.dev](https://slsa.dev/) | Köken düzeylerinin adı. Şartname metni Apache-2.0 değildir. Metin bu depoya kopyalanmadı |
| ORAS | Apache-2.0 `[VERİ]` | [depo](https://github.com/oras-project/oras) | İsteğe bağlı `publish`. Go CLI'dir; `requirements-f1.txt` içine pip satırı konmadı |
| python-tuf | Güncel LICENSE Apache-2.0 `[VERİ]` | [depo](https://github.com/theupdateframework/python-tuf) | İptal listesi dağıtımı F4'te. F1'de kurulmaz. İkinci bir MIT metni bu LICENSE dosyasında görülmedi `[EKSİK]` |
| Presidio | MIT `[VERİ]` | [depo](https://github.com/microsoft/presidio) | Metin PII taraması. Aşağıdaki Türkiye notuna bakın |
| Faker `tr_TR` | MIT `[VERİ]` | [depo](https://github.com/joke2k/faker), [tr_TR](https://faker.readthedocs.io/en/master/locales/tr_TR.html) | Sentetik kişisel veri. Gerçek kayıt yok |
| MuJoCo | Apache-2.0 `[VERİ]` | [depo](https://github.com/google-deepmind/mujoco) | Simülasyon. Bu iskelet simülasyon çalıştırmaz |
| Gazebo gz-sim | Apache-2.0 `[VERİ]` | [depo](https://github.com/gazebosim/gz-sim) | MuJoCo yerine seçilebilecek simülatör. pip paketi değil |
| LeRobotDataset v3 / lerobot | Apache-2.0 `[VERİ]` | [biçim](https://huggingface.co/docs/lerobot/lerobot-dataset-v3), [depo](https://github.com/huggingface/lerobot) | Kayıt biçimi (Parquet + MP4). Örnekte video veya Parquet yok |

`[VARSAYIM]`: F1'de önce MuJoCo, gz-sim yedek simülatör olarak durur. İkisi de bu PR'da kurulmaz.

### Presidio: Türkiye ve yüz

Açılacak metin türleri: `TR_NATIONAL_ID`, `TR_LICENSE_PLATE`, `TR_PHONE_NUMBER`, IBAN (`IBAN_CODE`) ve e-posta (`EMAIL_ADDRESS`). Türkiye tanıyan üç tanıyıcı varsayılan olarak kapalıdır; F1 kodu yazılırken açıkça açılır `[VERİ]` (Presidio `default_recognizers.yaml` ve değişiklik günlüğü).

Yüz algılama yok. `presidio-image-redactor` bağımlılık değildir. Görüntüde yüz varsa araç yalnız uyarı yazar; yüzü bulduğu iddiası taşımaz `[VARSAYIM]`.

## Kullanılmayanlar

Bu paketlere ve veri kümelerine bağımlılık yok. Dosyaları bu depoda yoktur.

| Ad | Neden | Bağlantı |
|---|---|---|
| tr-pii-detect | PolyForm Noncommercial 1.0.0 `[VERİ]` | [depo](https://github.com/fevziegeyurtsevenler/tr-pii-detect) |
| SCD | CC BY-NC-SA 4.0 deniyor. Bu okumada birincil sayfa sabitlemedi `[EKSİK]` | bağlantı yazılmadı |
| GraspNet-1Billion | Ticari olmayan paylaşım. HF kartı ekibin CC BY-NC-SA 4.0 beyanını aktarır `[VEKİL]`. graspnet.net açıldı; lisans cümlesi o HTML'de yoktu `[EKSİK]` | [proje](https://graspnet.net/), [HF kartı](https://huggingface.co/datasets/DravenALG/GraspNet-1Billion) |
| MetaGraspNet | CC BY-NC-SA 3.0 `[VERİ]` | [depo](https://github.com/maximiliangilles/MetaGraspNet) |
| AgiBot World | CC BY-NC-SA 4.0 `[VERİ]` | [HF](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Beta) |
| Fourier ActionNet | Veri CC BY-NC-SA 4.0; eğitim kodu Apache-2.0 `[VERİ]` | [action-net.org](https://action-net.org/) |
| Galaxea Open-World | CC BY-NC-SA 4.0 `[VERİ]` | [HF](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset) |
| 1X | Ham robot videosu CC BY-NC-SA 4.0 `[VERİ]`. Token dizisi Apache-2.0 `[VERİ]`. İkisi de koli ayırma paketine girmez | [duyuru](https://www.1x.tech/discover/1x-world-model-sampling-challenge), [1xgpt](https://github.com/1x-technologies/1xgpt) |
| Common Voice | Yeniden barındırma yok. Resmî indirme sayfası açıldı `[VERİ]` | [commonvoice.mozilla.org/en/datasets](https://commonvoice.mozilla.org/en/datasets) |
| Instacart market siparişleri | 2017 blogu bu ortamda 403 verdi. Bağlantı yazılmadı `[EKSİK]` | — |
| M5 | Birincil sayfa bu okumada sabitlemedi `[EKSİK]` | bağlantı yazılmadı |
| TRI `lbm_eval` / PickAndPlaceBox | Depo kodu Apache-2.0 `[VERİ]`. PickAndPlaceBox veri lisansının koddan ayrı olup olmadığı netleşmedi `[EKSİK]`. Veri gömülmez | [lbm_eval](https://github.com/ToyotaResearchInstitute/lbm_eval) |

Pip sürümleri: [requirements-f1.txt](../requirements-f1.txt).
