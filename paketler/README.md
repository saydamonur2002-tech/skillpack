# Sayısal modüller

Burada **20 bağımsız hesap aracı** ve 3 küçük beceri paketi (tablonun sonunda) vardır. İki grup birbirinin yerine geçmez: ilk grup M001–M010, ikinci grup M011–M020.

Bunlar `manifest.json` ile çalışan komut satırı ve stdio MCP araçlarıdır. `examples/` altındaki `skillpack.yaml` akış paketleriyle aynı biçimde değildir; o çalıştırıcı bunları paket olarak yüklemez.

Her modülün yanında sade bir `ACIKLAMA.md` durur. Lisans metinleri ve kaynak bildirimleri modülün içinde durur; bu dizin onların yerine geçmez.

| Modül | Ne işe yarar? | Kaynak | Lisans | Test |
|---|---|---|---|---|
| [M001 — Kübik eğriyle ara değer ve türev](sayisal-2026-11-11/tur1/M001/ACIKLAMA.md) | Ölçülmüş noktalardan düzgün bir eğri kurar; istenen noktada değeri, eğimi ve eğimdeki değişimi verir. Aralık dışını da uçtaki eğriyle cevaplar. | [fortran-utils](https://github.com/certik/fortran-utils) | MIT | Grup 261 geçti · kayıt 23 |
| [M002 — Düzensiz ölçümlerden türev hesabı](sayisal-2026-11-11/tur1/M002/ACIKLAMA.md) | Eşit aralıklı olmayan noktalarda türev ağırlıkları üretir. Ölçüm değerleri verilirse tek bir türev tahmini de verir. | [numdifftools](https://github.com/pbrod/numdifftools) | BSD-3-Clause | Grup 261 geçti · kayıt 28 |
| [M003 — Dünya elipsoidi üzerinde mesafe](sayisal-2026-11-11/tur1/M003/ACIKLAMA.md) | İki koordinat arasındaki yüzey mesafesini ve başlangıç/bitiş yönlerini WGS84 Dünya modeliyle hesaplar. | [geodesy](https://github.com/chrisveness/geodesy) | MIT | Grup 261 geçti · kayıt 40 |
| [M004 — Küre üzerinde kısa yüzey yolu](sayisal-2026-11-11/tur1/M004/ACIKLAMA.md) | Dünyayı küre kabul ederek iki koordinat arasındaki büyük çember mesafesini ve yönleri hesaplar. | [geodesy](https://github.com/chrisveness/geodesy) | MIT | Grup 261 geçti · kayıt 22 |
| [M005 — Sabit pusula yönlü rota hesabı](sayisal-2026-11-11/tur1/M005/ACIKLAMA.md) | Küre üzerinde pusula yönü sabit tutulan bir rotanın mesafesini ve yönünü hesaplar. | [geodesy](https://github.com/chrisveness/geodesy) | MIT | Grup 261 geçti · kayıt 24 |
| [M006 — Uç değerlerden daha az etkilenen özet](sayisal-2026-11-11/tur1/M006/ACIKLAMA.md) | Aşırı yüksek veya düşük gözlemlerin etkisini azaltarak bir sayı dizisinin merkezini ve yayılımını hesaplar. | [astropy](https://github.com/astropy/astropy) | BSD-3-Clause | Grup 261 geçti · kayıt 22 |
| [M007 — Medyan çevresindeki yayılım](sayisal-2026-11-11/tur1/M007/ACIKLAMA.md) | Bir sayı dizisinin ortancasını ve bu ortancadan tipik uzaklığını hesaplar. | [astropy](https://github.com/astropy/astropy) | BSD-3-Clause | Grup 261 geçti · kayıt 21 |
| [M008 — Sinyali kaba yapı ve ayrıntıya ayırma](sayisal-2026-11-11/tur1/M008/ACIKLAMA.md) | Çift uzunluklu bir sayı dizisini Haar yöntemiyle yavaş değişen ana parça ve ayrıntıya ayırır, sonra yeniden kurar. | [PyWavelets](https://github.com/PyWavelets/pywt) | MIT | Grup 261 geçti · kayıt 20 |
| [M009 — Piksel ağırlık merkezini bulma](sayisal-2026-11-11/tur1/M009/ACIKLAMA.md) | Sayısal piksel tablosunun ağırlık merkezini bulur. Seçilen pikseller dışarıda bırakılabilir. Görüntü dosyası açmaz. | [photutils](https://github.com/astropy/photutils) | BSD-3-Clause | Grup 261 geçti · kayıt 35 |
| [M010 — Bağlantı ağının Laplasyen tablosu](sayisal-2026-11-11/tur1/M010/ACIKLAMA.md) | Ağırlıklı bağlantı tablosunu birleşik ya da normalleştirilmiş Laplasyen tabloya çevirir. Yönlü bağlar ortalanır. | [pygsp](https://github.com/epfl-lts2/pygsp) | BSD-3-Clause | Grup 261 geçti · kayıt 24 |
| [M011 — Polinomun bir kökünü bulma](sayisal-2026-11-11/tur2/M011/ACIKLAMA.md) | İşaret değiştiren bir aralıkta polinomun bir gerçek kökünü Brent yöntemiyle arar. | [SciPy](https://github.com/scipy/scipy) | BSD-3-Clause | Grup 324 geçti · kayıt 28 |
| [M012 — Sınırlı aralıkta integral tahmini](sayisal-2026-11-11/tur2/M012/ACIKLAMA.md) | Listedeki düzgün bir fonksiyonun iki sınır arasındaki integralini, aralığı bölmeden, tek hesap paneliyle yaklaşık bulur. | [SciPy](https://github.com/scipy/scipy) | BSD-3-Clause | Grup 324 geçti · kayıt 29 |
| [M013 — Doğrusal sistemin zamanla ilerlemesi](sayisal-2026-11-11/tur2/M013/ACIKLAMA.md) | Doğrusal bir sistemin başlangıç durumundan, sabit adımlarla, seçilen sonraki zamandaki durumunu hesaplar. | [Fortran Astrodynamics Toolkit](https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit) | BSD-3-Clause | Grup 324 geçti · kayıt 23 |
| [M014 — Tamamlanmamış gamma değerleri](sayisal-2026-11-11/tur2/M014/ACIKLAMA.md) | İstatistikte kullanılan düzenlenmiş tamamlanmamış gamma fonksiyonunun alt ve üst kuyruk değerlerini hesaplar. | [SciPy](https://github.com/scipy/scipy) | BSD-3-Clause | Grup 324 geçti · kayıt 42 |
| [M015 — Tamamlanmamış beta değeri](sayisal-2026-11-11/tur2/M015/ACIKLAMA.md) | İstatistikte kullanılan düzenlenmiş tamamlanmamış beta integralini hesaplar. | [SciPy](https://github.com/scipy/scipy) | BSD-3-Clause | Grup 324 geçti · kayıt 39 |
| [M016 — Kare doğrusal denklem sistemini çözme](sayisal-2026-11-11/tur2/M016/ACIKLAMA.md) | Birbirine bağlı kare doğrusal denklemlerin bilinmeyenlerini satır değiştirmeli LU yöntemiyle çözer. | [OpenBLAS](https://github.com/OpenMathLib/OpenBLAS) | BSD-3-Clause | Grup 324 geçti · kayıt 23 |
| [M017 — Üç köşegenli denklem sistemini çözme](sayisal-2026-11-11/tur2/M017/ACIKLAMA.md) | Yalnızca ana köşegen ve yanındaki iki köşegende katsayı bulunan doğrusal sistemi çözer. | [OpenBLAS](https://github.com/OpenMathLib/OpenBLAS) | BSD-3-Clause | Grup 324 geçti · kayıt 22 |
| [M018 — Takvim tarihini Jülyen güne çevirme](sayisal-2026-11-11/tur2/M018/ACIKLAMA.md) | Gregoryen takvim gününü, saat olmadan gece yarısı kabul ederek, Jülyen gün ve değiştirilmiş Jülyen gün sayılarına çevirir. | [ERFA](https://github.com/liberfa/erfa) | BSD-3-Clause | Grup 324 geçti · kayıt 28 |
| [M019 — Dünya dönüş açısını hesaplama](sayisal-2026-11-11/tur2/M019/ACIKLAMA.md) | UT1 zaman ölçeğindeki iki parçalı Jülyen tarihten Dünya’nın dönüş açısını IAU 2000 modeline göre hesaplar. | [ERFA](https://github.com/liberfa/erfa) | BSD-3-Clause | Grup 324 geçti · kayıt 31 |
| [M020 — Astronomik eksen dönüşümünü hesaplama](sayisal-2026-11-11/tur2/M020/ACIKLAMA.md) | TT zaman ölçeğindeki iki parçalı Jülyen tarihten gök eksenlerinin başlangıç farkı ve presesyon matrisini hesaplar. | [ERFA](https://github.com/liberfa/erfa) | BSD-3-Clause | Grup 324 geçti · kayıt 27 |
| [idna-encode — Alan adını ASCII'ye çevirme](beceri-paketleri-2026-11-13/idna-encode/ACIKLAMA.md) | Unicode alan adını IDNA 2008 ile punycode'a çevirir. | [idna](https://github.com/kjd/idna) | BSD-3-Clause | 2 test geçti |
| [chain-runner — Paketleri art arda çalıştırma](beceri-paketleri-2026-11-13/chain-runner/ACIKLAMA.md) | Paketleri sırayla çalıştırır, çıktıyı sonrakine aktarır. | Özgün (oturum üretimi) | Apache-2.0 | 1 test geçti |
| [skillpack-orchestrator — Paket iskelet/doğrulama/ZIP](beceri-paketleri-2026-11-13/skillpack-orchestrator/ACIKLAMA.md) | Paket iskeleti kurar, temel denetler, deterministik ZIP üretir. | Özgün (oturum üretimi) | Apache-2.0 | 1 test geçti |

## Test sütunu ne demek?

11 Kasım 2026’da her iki grup bu depoda yeniden çalıştırıldı. Python 3.12. İlk grup **261 geçti**, ikinci grup **324 geçti**. Hata ve atlama yok. İkinci grubun yerel C kontrolleri GCC ile de geçti.

«Kayıt», teslimdeki modül sayısıdır. İlk grupta bu sayı, modül klasöründeki testlere bir gerçek MCP oturumunu ekler. İkinci grupta kayıt, yalnız modül klasöründeki testlerdir; 32 ortak test (MCP, süre sınırı, yerel C, yayın denetimi) grup toplamının içindedir, tek bir modüle yazılmaz.

Kaynak projelerin tam test takımları ve özgün Fortran programları çalıştırılmaz. Ayrıntı her grubun `MINING_REPORT.md` dosyasındadır.

## Nasıl çalıştırılır?

İlk grup, `sayisal-2026-11-11/tur1` klasöründe:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m pytest -q
```

İkinci grup, `sayisal-2026-11-11/tur2` klasöründe:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r M011/requirements-test.txt
.venv/bin/python -m pytest -q
```

İkinci grubun sekiz yerel C kontrolü GCC ister. GCC yoksa o sekiz test atlanır; diğer testler çalışır. Hesapların kendisi NumPy, SciPy veya Fortran istemez. Kurulum için `jsonschema`, `mcp` ve `pytest` gerekir. Bu sürümler ana deponun `mcp>=2` kurulumundan ayrı tutulmalıdır; CI’de ayrı bir iş olarak koşarlar.

Tek bir modülün örneği, o modülün klasöründe `python tool/main.py < example.json` ile denenebilir. MCP ayarı modülün `SKILL.md` dosyasındadır.

## Düzen

| Klasör | İçerik |
|---|---|
| `sayisal-2026-11-11/tur1/` | M001–M010, grubun kendi testleri ve raporları |
| `sayisal-2026-11-11/tur2/` | M011–M020, grubun kendi testleri ve raporları |
| `sayisal-2026-11-11/butunluk/` | Aktarmadan önce doğrulanan arşiv özetleri |

Aynı adlı raporlar (`README.md`, `MINING_REPORT.md`, `catalog.json`) iki grupta ayrı durur; biri diğerinin üzerine yazılmaz.

Arşiv dosyaları depoda tekrar tutulmaz. Özetler açılmadan önce tuttu. Ayrıntı: [bütünlük notu](sayisal-2026-11-11/butunluk/README.md).

Eski RESEARCH-ONLY arşivi bu teslimde yoktu. Bitmiş modül değildir, eklenmedi. `kaldirma-siniri-niosh` ve `isi-indeksi-nws` bu iki arşivde yoktur.
