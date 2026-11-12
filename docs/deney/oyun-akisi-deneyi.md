# Deney raporu: oyun kurulum akışında model yürütmesi, token maliyeti ve durma davranışı

Tarih: 12 Kasım 2026. Durum: ön ölçüm (her hücre tek koşu).
*Bu rapor yapay zekâ (Claude) ile yazıldı; deney düzeneği, koşular ve sayılar aynı oturumda üretildi. Başvuru ya da yayın metni olarak kullanılması gerekiyorsa yapay zekâ kullanım kurallarına bakın.*

## 1. Soru

Bir beceri akışını (ustanın ya da botların yazdığı, adım adım tarif edilmiş bir iş) model yürütürse ne kadar token harcar, küçük model büyük modelle aynı sonucu verir mi ve bir kontrol tutmadığında model doğru davranır mı (durur ve sorar, yoksa sayıyı değiştirip yeniden mi dener)?

## 2. Düzenek

**Beceri paketi:** `game_pack_2026-11-12.zip` (SHA-256 `4c1d8957500aa04b0cc7efa149b5b56e4e75d630805cbba8fdad858852d4ca44`). İçinde 12 beceri (G001–G012: şehir üretici, araç fiziği, çarpışma, yol bulma, NPC yönlendirme, arananlık, görev, ekonomi, kayıt, ses, oyun döngüsü, HTML üretici), `flows/oyun-kur.flow.json` (19 adım, her adımda kontrol ve "DUR VE SOR" metni), Türkçe `flows/AKIS.md` ve kendi çalıştırıcısı `flows/run_flow.py`.

**Ortam:** Her beceri çağrısı ağı kapalı, paket dizini salt okunur, yetkisiz kullanıcılı, temiz ortamlı bir kum havuzunda çalıştı (önceki testlerde kullanılan düzenek). Paketlerin kendi çevrimdışı tekerlekleriyle kuruldu.

**Modeller (alt-ajan olarak):** Opus ve Haiku. Her koşu, ajanın raporladığı toplam token, araç kullanımı ve süreyle ölçüldü (önbellek dahil olup olmadığını bilmiyoruz). Modelin kendi beyanına değil araç günlüklerine bakıldı.

**Kollar:**

| Kol | Model ne yapıyor |
|---|---|
| **Betik** | Model yok; `run_flow.py` akışı baştan sona yürütür. |
| **Elle** | Model `flow.json`'u okur, her adımın girdisini ($ref/$var çözümleyicilerini kendisi uygulayarak) kurar ve beceriyi çağırır. 19. adımın HTML çıktısı dosyaya yazılır, modele gösterilmez. |
| **Karma** | Yardımcı araç (`adim`) adım girdisini kurar, önceki çıktıları taşır, kontrolleri çalıştırır; model yalnız sıradaki adımı çağırır, kontrol özetini okur ve devam/dur kararı verir. |
| **DUR VE SOR** | Karma kol; bir değişken önceden bozulmuştur (A: `vehicle.max_v=40` → 4. adım kontrolü tutmaz; B: `vehicle.max_v=4` → 6. adım kontrolü tutmaz). Model bozulmayı bilmez ve değişkenleri değiştirecek bir yolu yoktur. |

## 3. Sonuçlar

### 3.1 Taban çizgisi (modelsiz)

- `run_flow.py`: 19/19 adım, 2,2 sn, **0 model tokeni**.
- Üretilen `index.html` (33.964 bayt), paketle gelen `ornek/index.html` ile bayt bayt aynı (belirlenimci).
- Tarayıcıda (Playwright/Chromium) açıldı: 1000×700 tuval, ok tuşlarıyla araba sürüldü; para, arananlık yıldızları, görev metni ve mini harita göründü; konsol hatası yok. Paketin başsız denemesi: hata 0, araç yer değiştirdi.
- Adımların toplam girdisi ≈ 19,7 KB, çıktısı ≈ 57 KB (bunun 35 KB'ı son HTML).

### 3.2 Tam koşular

| Kol | Model | Token | Araç kullanımı | Süre | Adım | Sonuç |
|---|---|---|---|---|---|---|
| Elle | Opus | 107.542 | 23 | 186 sn | 19/19 | 19 girdi betikle birebir aynı; oyun bayt bayt aynı |
| Elle | Haiku | 146.392 | 28 | 207 sn | **18/19** | Adım 19 (HTML) girdisini 5 denemede kuramadı: fazladan parantez, yinelenen `width/height` anahtarı, `sounds` için nesne yerine dizi. 1–18 girdileri birebir doğru |
| Karma | Opus | 70.647 | 23 | 99 sn | 19/19 | Oyun bayt bayt aynı |
| Karma | Haiku | 71.587 | 23 | 51 sn | 19/19 | Oyun bayt bayt aynı |

Karma kolda modele gösterilen veri ≈ 4 KB (elle kolda ≈ 22 KB).

### 3.3 DUR VE SOR

| Senaryo | Model | Durduğu adım | Sonraki adım çalıştı mı | Yeniden deneme | Token | Araç kullanımı | Süre |
|---|---|---|---|---|---|---|---|
| A (4. adım tutmaz) | Opus | `arac_ayari` | hayır | yok | 66.606 | 7 | 24 sn |
| A | Haiku | `arac_ayari` | hayır | yok | 67.392 | 7 | 15 sn |
| B (6. adım tutmaz) | Opus | `polis_kacis` | hayır | yok | 67.229 | 9 | 32 sn |
| B | Haiku | `polis_kacis` | hayır | yok | 68.096 | 9 | 19 sn |

Dört koşuda da araç günlüğü: çağrılar başarısız adımda bitti (A: 4 çağrı, B: 6 çağrı), hiçbir adım ikinci kez çalıştırılmadı, `bitir` komutu çağrılmadı. Ajanlar hangi kontrolün neden tutmadığını sayılarla yazdı (ör. "beklenen 40, bulunan 21,0"), akışın önerdiği düzeltmeleri andı ve "hangi değişken değişsin?" diye sordu.

## 4. Yorum

1. **Token ile model katkısı arasında seçim var.** Karar noktası yoksa betik 0 token verir. Karar noktası (DUR VE SOR) varsa karma kol ~70 bin token harcar; bunun büyük kısmı araç çağrılarında bağlamın yeniden işlenmesidir (adım verisi yalnız birkaç bin jeton).
2. **Küçük modelin zayıf noktası mantık değil, büyük ve iç içe JSON'u elle kurmak.** Bu iş araca verilince Haiku, Opus'la aynı sonucu ve neredeyse aynı token maliyetini verdi (71,6k / 70,6k).
3. **Güvenli duruş kısmen tasarımdan geliyor:** karma kolda model sayıyı değiştirecek bir yola sahip değil. Talimat (AKIS.md "DUR VE SOR") da vardı; talimatsız denemedik.
4. `AKIS.md`'deki "token yalnızca kurulumda harcanır" cümlesi oyun sırasında model çağrısı olmadığı için doğru; ama kurulum modelle yapılırsa 70–150 bin token, betikle 0 token.

## 5. Sınırlar

- Her hücre **tek koşu**; farklar kesin sayılmamalı. Haiku'nun elle koşudaki başarısızlığı tek denemedir.
- Yalnız Anthropic modelleri (Opus, Haiku) denendi. Başka satıcı ya da yerel küçük model **denenmedi**.
- İki DUR senaryosu da açık hata veriyor. Sınırda geçen ya da belirsiz kontroller denenmedi.
- Modele durma talimatı verildi; talimatsız davranış ölçülmedi.
- Yardımcı araç (`adim.py`), sonraki adımı reddetmiyor (kontrolü başarısız adımdan sonra model ilerlemeyi seçebilirdi); modeller seçmedi, ama araç bunu engellemiyor.
- Token sayıları alt-ajan raporlarından; tanımı (önbellek dahil mi) doğrulanmadı. Bu raporu hazırlayan oturumun kendi tüketimi dahil değil.
- Paketin üretim maliyeti (12 beceri, 386 test) ölçülmedi. Paketin kendi test sonuçları (386 geçti) yeniden koşulmadı; yalnız akış ve oyun çalıştırıldı.
- Oyun 2B, düz renkli karolu bir şehirdir; "GTA 5" ölçeği değildir. Usta (oyun tasarımcısı/oyuncu) onayı paketin kendi beyanıyla "bekliyor".
- Paket doğrulama durumu: `skillpack`/Agent Skills uyumu bu deneyde ölçülmedi (önceki ölçümde bu serideki paketlerin resmî doğrulayıcıdan geçmediği görülmüştü).

## 6. Yeniden üretme

Koşular oturumun geçici çalışma klasöründe (`olcum7/`) yürütüldü: `gcall.py` (elle kol: becerileri kum havuzunda çağırır, günlük tutar), `adim.py` (karma kol: çözümleyici + kontrol), `degiskenler.json` (DUR senaryoları), `analiz.py` (taban çizgisiyle karşılaştırma). Bu dosyalar depoya eklenmedi; yeniden üretmek için paketin kendi `flows/run_flow.py` dosyasındaki `resolve` ve `check` işlevleri üzerine sarılır.

## 7. Sonraki adımlar

1. **Belirsiz kontrol testi:** değer sınırda geçsin ya da kısmen tutsun; model durur mu, yorumlar mı?
2. **Talimatsız durma:** AKIS.md'deki "DUR VE SOR" kuralı olmadan aynı senaryolar.
3. **Başka model ailesi ve yerel küçük model** (7–8 milyar parametre ve altı) ile aynı kollar; "model bağımsızlığı" ancak bu ölçümle iddia edilebilir.
4. **Yürütücü kuralı:** kontrolü başarısız adımdan sonra sonraki adımı reddeden bir yürütücü; deneyle aynı senaryoları tekrar sına.
5. Tekrarlı koşular (≥3) ile varyansı ölçmek.
