# Altyapı envanteri ve ilk deneme sonuçları

- Tarih: 10 Kasım 2026
- Kapsam: teknik taslağın ([TEKNIK_PROJE_v0.1.md](TEKNIK_PROJE_v0.1.md)) Tablo 15'te saydığı katmanlar için ücretsiz ve açık kaynak parçaların taranması ve bir kısmının gerçekten çalıştırılması.
- Durum: keşif notu. Bu belge uygulama kodu değildir; F1 başlamış sayılmaz.

Kaynak etiketleri teknik taslaktakiyle aynıdır. Bu belgede `[VERİ]` iki anlama gelir: GitHub / Hugging Face kaydından 10 Kasım 2026'da okunan bilgi, ya da bu denemede bizzat ölçülen sonuç. Çalıştırılmayan her şey açıkça "denenmedi" diye yazılmıştır.

## 1. Kısa sonuç

Paketleme, imza, iptal ve simülasyon halkaları hazır açık kaynak parçalarla çalışıyor; bunlar için sıfırdan altyapı yazmaya gerek yok `[VERİ]`.

Zayıf halka modeldir. Küçük yerel model, öncelik sıralı iş kurallarını kendi başına güvenilir uygulayamadı: 7B sınıfı model 20 kolinin 13'ünü doğru atadı, aynı işi yapan deterministik betik 20'sini `[VERİ]`. Örneklem küçüktür (Bölüm 4.3); sonuç bir işarettir, kanıt değildir.

## 2. Deneme ortamı

| Öğe | Değer |
|---|---|
| Makine | 4 çekirdek CPU, 15 GB bellek, GPU yok (bulut konteyneri) |
| Python | 3.12 |
| Paket sürümleri | `skills-ref` 0.1.1, `model-signing` 1.1.1, `sigstore` 4.5.1, `tuf` 7.0.1, `securesystemslib` 1.6.0, `mujoco` 4.0.0, `mcp` 2.3.0, `llama-cpp-python` 0.3.36 |
| Modeller | Qwen2.5 1.5B Instruct ve Qwen2.5 7B Instruct, GGUF Q4_K_M |
| Örnek paket | [deney/depo-koli-ayirma/](deney/depo-koli-ayirma/) (taslak Bölüm 4.3'teki örneğin küçültülmüş hâli) |

Referans donanım (taslak Bölüm 2.3, tek 24–48 GB GPU) bu denemede yoktu. Buradaki hız sayıları o hedefle karşılaştırılamaz.

## 3. Çalıştırılan halkalar

**Tablo E1. Denenen parçalar ve sonuç** `[VERİ]`

| Halka | Parça | Lisans | Ne denendi | Sonuç |
|---|---|---|---|---|
| Biçim doğrulama | `skills-ref` (`agentskills` komutu) | Apache-2.0 | Geçerli paket; yanlış dizin adı; `metadata` içinde iç içe yapı; bilinmeyen üst düzey alan | Geçerli paket kabul edildi, diğer üçü reddedildi |
| Kanonik arşiv | GNU `tar` + SHA-256 | GPL (araç) | Aynı içerikten iki ayrı zamanda arşiv üretmek | İki özet aynı çıktı |
| Dizin imzası, anahtarlı | OpenSSF `model-signing` | Apache-2.0 | İmzala ve doğrula; bir kuralı değiştir; pakete dosya ekle; yanlış açık anahtar | Temiz paket doğrulandı, üç bozma da reddedildi |
| Anahtarsız imza doğrulama | Sigstore kamu örneği + `pypi-attestations` | Apache-2.0 | Yayımlanmış bir paketin kanıtını kamu günlüğüne karşı doğrulamak; yanlış kimlik; 1 bayt bozulmuş dosya | Doğru olan kabul edildi, diğer ikisi reddedildi |
| İptal listesi | `python-tuf` | Apache-2.0 / MIT | 3 istemciye iptal yaymak; imzasız değişiklik; geri sarma; dondurma | İptal 3 istemcide görüldü, üç saldırı reddedildi |
| Simülasyon | MuJoCo | Apache-2.0 | Başsız (ekransız) koli itme kabul testi | Test geçti; 5 sn'lik simülasyon yaklaşık 15 ms sürdü |
| Yerel model | `llama.cpp` (`llama-cpp-python`) | MIT | Qwen2.5 1.5B ve 7B'yi CPU'da çalıştırmak | Çalıştı; doğruluk Bölüm 4'te |

Notlar:

- `skills-ref` sonucu, taslak Bölüm 4.1'deki kararı doğrular: zengin yapı `SKILL.md` ön bilgisine konamaz, ayrı `skillpack.yaml` dosyası gerekir.
- `model-signing` imzası Sigstore paket biçiminde (`application/vnd.dev.sigstore.bundle.v0.3+json`) bir in-toto beyanıdır ve her dosyanın SHA-256 özetini taşır. Bu, taslaktaki `checksums` + `signatures` alanlarının yaptığı işle örtüşür.
- Anahtarsız kipte yalnız **doğrulama** denendi. İmzalama, tarayıcıdan ya da CI'dan OIDC kimliği ister; bu ortamda yapılamadı.
- İptal tatbikatı tek makinede, yerel ağ üzerinde yapıldı. Yayılma süresi ölçümü (taslak Bölüm 12) bundan çıkmaz.
- Tekrar çalıştırmak için: [deney/iptal_tatbikati.py](deney/iptal_tatbikati.py).

## 4. Yerel modelle kural uygulama ölçümü

### 4.1 Düzenek

Görev: bir koliyi beş kurala göre rampaya atamak. Kurallar sıralıdır, ilk eşleşen geçerlidir (geçersiz barkod → insan; 25 kg üstü → ağır; hedef IST → 3; kırılacak → 5; aksi hâlde → 1). 20 sentetik koli, sabit rastgele tohum, sıcaklık 0, çıktı JSON'a zorlandı. Doğru cevap aynı kuralları uygulayan birkaç satırlık betikten gelir. Betik: [deney/beceri_olcumu.py](deney/beceri_olcumu.py).

### 4.2 Sonuç

**Tablo E2. 20 kolide doğru atama** `[VERİ]`

| Karar veren | Doğru | Girdi / çıktı (token/görev) | Süre (sn/görev, CPU) |
|---|---|---|---|
| Qwen2.5 1.5B, becerisiz | 0/20 | 93 / 35 | 3,3 |
| Qwen2.5 1.5B, beceriyle | 4/20 | 269 / 19 | 2,2 |
| Qwen2.5 7B, beceriyle | 13/20 | 269 / 15 | 5,2 |
| Qwen2.5 7B, beceriyle, önce gerekçe yazdırılarak | 12/20 | 308 / 74 | 20,6 |
| Deterministik betik (referans) | 20/20 | — | — |

- "Becerisiz" satırı beklenen bir sıfırdır: kurallar verilmediği için model onları bilemez. Bu satır becerinin gerekli olduğunu gösterir, yeterli olduğunu değil.
- 7B'nin ilk turdaki 7 hatasının hepsi öncelik hatasıdır: üstteki kural eşleştiği hâlde alttaki uygulanmıştır (ör. 40 kg'lık IST kolisine "ağır" yerine "rampa 3").
- Gerekçe yazdırmak sonucu iyileştirmedi; model kuralları değerlendirmek yerine metnini tekrar etti. Bu, kullanılan istemin zayıflığı da olabilir.

### 4.3 Sınırlar

- 20 örnek, tek görev, tek istem, tek nicemleme (Q4_K_M). Güven aralığı hesaplanmadı.
- GPU yok; hızlar referans donanımı temsil etmez.
- Daha büyük model, daha iyi istem ya da araç çağırma kipi denenmedi `[EKSİK]`.

### 4.4 Taslak için çıkarım

Taslak Bölüm 13, "kuralların deterministik kısmını betiklere taşımak" maddesini bir risk azaltma yolu olarak anar. Bu ölçüm, maddenin varsayılan tasarım kuralı olmasını destekler `[VARSAYIM]`: kural motoru kararı verir; model girdiyi yapılandırır, tanı kartını yazar ve öğretme döngüsünde taslak kural önerir. Bu öneri ek ölçümle sınanmalıdır ([EK_TEST_ISTEMI.md](EK_TEST_ISTEMI.md)).

## 5. Envanter: canlı parçalar

GitHub kayıtları 10 Kasım 2026'da okundu `[VERİ]`. "Denendi" sütunu bu çalışmayı gösterir. Bir parçanın ne işe yaradığına dair açıklamalar, denenmeyen satırlarda proje belgelerinden değil genel bilgiden gelir `[VEKİL]`.

**Tablo E3. Katmanlara göre açık kaynak parçalar**

| Katman | Depo | Lisans | Son itme | Denendi mi |
|---|---|---|---|---|
| Beceri biçimi | `agentskills/agentskills` | Apache-2.0 | 2026-11-04 | Evet (`skills-ref`) |
| İmza | `sigstore/sigstore-python` | Apache-2.0 `[VEKİL]` | 2026-11-05 | Evet (doğrulama) |
| İmza | `sigstore/cosign` | Apache-2.0 | 2026-11-09 | Hayır |
| Dizin imzası | `sigstore/model-transparency` | Apache-2.0 | 2026-11-09 | Evet (`model-signing`) |
| Dizin imzası, spesifikasyon | `ossf/model-signing-spec` | Apache-2.0 | 2026-09-18 | Hayır |
| Şeffaflık günlüğü | `sigstore/rekor` | Apache-2.0 | 2026-11-09 | Dolaylı (kamu örneği) |
| Şeffaflık günlüğü | `transparency-dev/tessera` | Apache-2.0 | 2026-11-09 | Hayır |
| Şeffaflık günlüğü | `google/trillian` | Apache-2.0 | 2026-11-02 | Hayır |
| İptal / güncelleme | `theupdateframework/python-tuf` | Apache-2.0 | 2026-11-09 | Evet |
| TUF deposu işletme | `theupdateframework/tuf-on-ci` | belirtilmemiş | 2026-11-09 | Hayır |
| TUF deposu işletme | `repository-service-tuf/repository-service-tuf` | MIT | 2026-11-09 | Hayır |
| Köken | `in-toto/attestation`, `in-toto/in-toto` | belirtilmemiş | 2026-10-28, 2026-08-27 | Dolaylı (imza içinde) |
| Köken | `slsa-framework/slsa-github-generator` | Apache-2.0 | 2026-08-07 | Hayır |
| Çevrim dışı imza | `jedisct1/minisign` | ISC | 2026-10-11 | Hayır |
| Dağıtım | `oras-project/oras` | Apache-2.0 | 2026-11-10 | Hayır |
| Dağıtım | `ipfs/kubo` | belirtilmemiş | 2026-11-01 | Hayır |
| Dağıtım | `n0-computer/iroh` | Apache-2.0 | 2026-11-10 | Hayır |
| Model çalıştırma | `ggml-org/llama.cpp` | MIT | 2026-11-10 | Evet |
| Model çalıştırma | `ollama/ollama` | MIT | 2026-11-10 | Hayır |
| Ses anlatımı | `ggml-org/whisper.cpp` | MIT | 2026-11-10 | Hayır |
| Gösterim yakalama | `OpenAdaptAI/OpenAdapt` | MIT | 2026-11-10 | Hayır |
| Araç protokolü | `modelcontextprotocol/python-sdk` | MIT | 2026-11-05 | Yalnız kuruldu |
| Ajan protokolü | `a2aproject/A2A` | Apache-2.0 | 2026-11-05 | Hayır |
| İzin uygulama | `open-policy-agent/opa` | Apache-2.0 | 2026-11-10 | Hayır |
| İzin uygulama | `cedar-policy/cedar` | Apache-2.0 | 2026-11-09 | Hayır |
| Sandbox | `containers/bubblewrap` | belirtilmemiş | 2026-10-14 | Hayır |
| Robot verisi | `huggingface/lerobot` | Apache-2.0 | 2026-11-10 | Hayır |
| Veri dönüştürme | `Tavish9/any4lerobot` | MIT | 2026-11-06 | Hayır |
| Simülasyon | `google-deepmind/mujoco` | Apache-2.0 | 2026-11-10 | Evet |
| Simülasyon | `gazebosim/gz-sim` | Apache-2.0 | 2026-11-08 | Hayır |
| Robot ara katmanı | `ros2/ros2` | belirtilmemiş | 2026-11-04 | Hayır |
| Endüstriyel veri | `open62541/open62541` | MPL-2.0 | 2026-11-10 | Hayır |
| Endüstriyel veri | `FreeOpcUa/opcua-asyncio` | LGPL-3.0 | 2026-11-04 | Hayır |
| Gizlilik (DP) | `meta-pytorch/opacus` | Apache-2.0 | 2026-09-24 | Hayır |
| PII tarama | `data-privacy-stack/presidio` | MIT | 2026-11-08 | Hayır |
| Şema denetimi | `python-jsonschema/check-jsonschema` | belirtilmemiş | 2026-11-08 | Hayır |

"Belirtilmemiş": GitHub'ın lisans alanı tek bir tanımlayıcı döndürmedi; lisans dosyası ayrıca okunmalıdır `[EKSİK]`. Copyleft içeren satırlar (LGPL-3.0, MPL-2.0) Apache-2.0 referans kodla birlikte dağıtılmadan önce lisans uyumu açısından incelenmelidir `[EKSİK]`.

## 6. Envanter: duran ya da arşivlenmiş projeler

Bu projeler çalıştırılmadı. Değerleri hazır kod olmaktan çok, alınacak derstedir `[VEKİL]`.

**Tablo E4. Arşivlenmiş ya da bakımı durmuş projeler**

| Depo | Lisans | Durum `[VERİ]` | Projeye olası katkısı `[VEKİL]` |
|---|---|---|---|
| `MycroftAI/mycroft-core` | Apache-2.0 | Arşivlendi; son itme 2024-09-08 | Beceri paketi ve beceri mağazası denemesi. Canlı devamı: `OpenVoiceOS/ovos-core` (Apache-2.0, 2026-11-02) |
| `notaryproject/notary` | Apache-2.0 | Arşivlendi; son itme 2024-08-07 | TUF'un geniş çaplı ilk uygulamalarından; anahtar yönetimi yükü üzerine ders |
| `google-research/rlds` | Apache-2.0 | Arşivlendi; son itme 2024-09-26 | Open X-Embodiment'in veri biçimi; dönüştürücü yazılırken biçim tanımı |
| `snipsco/snips-nlu` | Apache-2.0 | Arşivli değil; son itme 2023-05-22 | Çevrim dışı niyet sınıflama; yönlendiricinin kural katmanı için fikir |
| `RethinkRobotics/intera_sdk` | Apache-2.0 | Arşivli değil; son itme 2023-08-17 | Göstererek öğretme yapan robotun SDK'sı |
| `anki/vector-python-sdk` | belirtilmemiş | Arşivli değil; son itme 2023-01-17 | Tüketici robotu SDK'sı; lisans okunmadan kullanılmamalı |

Bakımı durmuş koda bağımlılık kurmak güvenlik riskidir (taslak Tablo 14, tedarik zinciri satırı). Bu projelerden kod alınacaksa sabitlenmiş bir kopya ve lisans incelemesi gerekir.

## 7. Taslağa yansıtılması önerilen düzeltmeler

Teknik taslağa bu çalışmada dokunulmadı. Aşağıdakiler öneridir.

1. **Bölüm 6 ve Tablo 1, "beceri paketi için imza örneği bulunamadı `[EKSİK]`".** OpenSSF `model-signing` dizin ağaçlarını dosya başına özetle imzalar ve bir beceri dizininde çalıştı `[VERİ]`. Boşluk "imza aracı yok" değil, "beceri ekosistemine bağlanmamış ve iptal listesi yok" olarak daraltılabilir.
2. **Tablo 4, telefon katmanı "~1–3B".** Qwen2.5 3B Instruct Apache-2.0 değildir; Hugging Face kaydında lisansı `qwen-research` olarak görünür. 0.5B, 1.5B, 7B ve 14B Apache-2.0'dır `[VERİ]` (Hugging Face model kayıtları, 2026-11-10).
3. **Bölüm 13, deterministik betik maddesi.** Bölüm 4.4'teki çıkarım.
4. **Bölüm 6.4, dağıtım.** Paketlerin OCI kayıtlarından (`oras`) dağıtılması, ayna ve indeks biçimini sıfırdan tanımlamaya bir seçenek olarak değerlendirilebilir. Denenmedi `[EKSİK]`.

## 8. Kurulumda karşılaşılan pürüzler

- `model-signing` 1.1.1, `pyOpenSSL` olmadan başlamadı; ayrıca kurmak gerekti `[VERİ]`.
- `model-signing` komut satırı seçenekleri alt çizgilidir (`--private_key`, `--public_key`).
- `python-tuf` 7.x'te istemci kurucusu `bootstrap` parametresini zorunlu tutar; eski örnekler olduğu gibi çalışmaz `[VERİ]`.
- `skills-ref` paketinin komut adı `agentskills`'tir.
- Resmî `Qwen/Qwen2.5-7B-Instruct-GGUF` deposunda Q4_K_M tek dosya değildir; denemede `bartowski/Qwen2.5-7B-Instruct-GGUF` deposundaki tek dosyalı sürüm kullanıldı. Üçüncü taraf bir dönüştürmedir.

## 9. Yapılamayanlar

- `web.archive.org` deneme ortamından erişilemedi; web arşivi taranmadı `[EKSİK]`.
- Anahtarsız imzalama (OIDC), iki ayrı makine arasında doğrulama, IPFS, LeRobot, ROS 2, Gazebo, OPC UA, Opacus, Presidio ve GPU ölçümleri denenmedi `[EKSİK]`.
- Görev başına Wh ölçülmedi `[EKSİK]`.
