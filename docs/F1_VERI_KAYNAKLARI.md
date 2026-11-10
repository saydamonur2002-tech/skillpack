# F1 veri kaynakları — koli ayırma

Tek örnek koli ayırmadır. Veri bu depoya konmaz. Aşağıdaki kümeler bağlantı ve atıfla anılır. Yörünge dosyası, video, mesh ve ağırlık yoktur.

Okuma tarihi: 10 Kasım 2026. Yazılan bağlantılar bu tarihte açıldı.

## Açık boşluk

Açık, pakete konabilir bir **koli ayırma robot yörüngesi** veri kümesi bulunamadı `[EKSİK]`. Aşağıdakiler algı, mesh veya başka bir görevin biçimidir. Bu örneğin yörüngesi, yazıldığında simülasyonda sentetik üretilecektir `[VARSAYIM]`. Bu PR o yörüngeyi üretmez.

## Bağlantılı kaynaklar (gömülü değil)

| Kaynak | Lisans | Ne işe yarar | Ne değildir |
|---|---|---|---|
| [ARMBench](https://www.armbench.com/) (Amazon) | CC BY 4.0 `[VERİ]` | Depo nesnesi algısı için atıf | Koli ayırma yörüngesi değil |
| [LOCO](https://github.com/tum-fml/loco) (TUM FML) | CC0-1.0 `[VERİ]` | Lojistik sahne görüntüsü | Robot yörüngesi değil |
| [OCID](https://researchdata.tuwien.at/records/pcbjd-4wa12) (TU Wien) | CC BY 4.0 `[VERİ]` | Kapalı ortamda dağınık nesne, RGB-D. Nesneler arasında YCB örnekleri var | Ayırma yörüngesi değil |
| [YCB model seti](https://ycb-benchmarks.s3.amazonaws.com/index.html) | Veri CC BY 4.0 `[VERİ]` | Simülasyonda kutu mesh'i için atıf. Kod MIT `[VERİ]` | Bu depoda mesh yok |
| [DROID](https://droid-dataset.github.io/) | Veri kümesi CC BY 4.0 `[VERİ]` ([makale](https://arxiv.org/abs/2403.12945)) | Çok görevli robot kaydının biçim referansı | Koli ayırma paketi değil; dosya indirilmez |
| [PhysicalAI-GR00T-Tuned-Tasks](https://huggingface.co/datasets/nvidia/PhysicalAI-GR00T-Tuned-Tasks) (NVIDIA) | CC BY 4.0 `[VERİ]` | Isaac içinde sentetik görev ve LeRobot biçimine dönüşüm referansı. Boru sıralama ve somun dökme var | Koli ayırma yörüngesi değil; gömülmez |

Atıf, paketi kullananın bu sayfalardaki istendiği künyeyi koruması demektir. Bu depo veriyi yeniden lisanslamaz.

## Robotik şirketler

Kapanmış ya da dağılmış gruplar: Kindred, Covariant, Vicarious, Everyday Robots, Kinema, Fetch, Rethink. Bu isimler için yayımlanmış ve pakete konabilir bir koli ayırma yörüngesi bu taramada bulunamadı `[EKSİK]`.

Etkin yayımlar içinde bu listenin izin veren (permissive) ve depoya bağlanabilen parçası Amazon ARMBench'tir `[VERİ]`. O da algı kümesidir, yörünge arşivi değildir. AgiBot World, Fourier ActionNet, Galaxea ve 1X ham videosu CC BY-NC-SA 4.0 olduğu için kullanılmaz. Ayrıntı: [F1_ACIK_KAYNAKLAR.md](F1_ACIK_KAYNAKLAR.md).

## Bu örnekte olan

`examples/koli-ayirma/` kural ve beyan taşır. Sentetik bir girdi-çıktı örneği vardır; o örnek ölçüm değildir. Simülasyon kabul testi metindir, koşmaz.
