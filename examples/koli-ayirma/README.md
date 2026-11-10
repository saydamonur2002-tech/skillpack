# Koli ayırma (iskelet)

Tek F1 örneği budur. Depo stok tanısı ve ses düzeltme örnekleri ertelendi.

Bu dizin bir beceri paketi **iskeletidir**. Şema doğrulanmaz, imza yoktur, simülasyon koşmaz, yörünge dosyası yoktur. Durum: ⬜ Başlamadı.

## Ne var

- `SKILL.md` — Agent Skills ön bilgisi. `name` dizin adıyla aynıdır.
- `skillpack.yaml` — simülasyon modu, `raw_customer_data: false`, CC-BY-4.0, fiziksel profil yolu, verim alanları.
- `references/kurallar.yaml` — boyut ve etiket sınıfından rampaya. Gerçek hareket insan onayına bağlıdır ve kapalıdır.
- `physical/robot_profile.yaml` — boş profil.
- `tests/KABUL.md` — simülasyon kabul testinin tarifi.
- `examples/ornek_001.json` — sentetik, ölçüm değil.

## Model

Birincil modelin alt sınırı `32B` yazılır. Bu, [PR #9](https://github.com/saydamonur2002-tech/skillpack/pull/9) kararını izler. `main` üzerindeki teknik taslak Bölüm 2.3 hâlâ yaklaşık 8B der. 1,5B–8B burada birincil model değildir.

`tokens_per_task` ve `wh_per_task` boştur. Ölçüm yok `[EKSİK]`.

## Veri

Yörünge gömülmez. Açık ve pakete konabilir bir koli ayırma yörüngesi bulunamadı `[EKSİK]`. Yörünge ileride simülasyonda sentetik üretilecek `[VARSAYIM]`. Atıflar: [docs/F1_VERI_KAYNAKLARI.md](../../docs/F1_VERI_KAYNAKLARI.md). Araçlar: [docs/F1_ACIK_KAYNAKLAR.md](../../docs/F1_ACIK_KAYNAKLAR.md).
