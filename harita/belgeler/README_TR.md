# Harita becerileri

Bu klasör, Claude'a (Claude Desktop veya MCP destekleyen başka bir istemci) "basit bir Google Haritalar" gibi davranma yeteneği veren **15 küçük harita becerisi** içerir. İlke: **hesabı kod yapar, model hangi aracı kullanacağını seçip sonucu açıklar, insan onaylar.** Her beceri tek bir MCP aracıdır; tamamen yereldir (ağ yok, API anahtarı yok, telemetri yok), 64 KB girdi ve 10 saniye süre sınırı vardır.

## Hangi beceri ne yapar?

| Sunucu adı | Paket | Ne işe yarar | Örnek soru |
|---|---|---|---|
| `yer-ara` | M032 | Adres/yer arama (geocode) ve koordinattan adres bulma (reverse); Türkçe karakter ve yazım hatasına toleranslı | "Moda'yı bul" |
| `rota` | M030 | Arabayla/yürüyerek/bisikletle en kısa süreli rota, ara duraklar, adım adım yol tarifi | "İskeleden Moda'ya yürüyerek nasıl giderim?" |
| `sure-matrisi-izokron` | M031 | Çok nokta arası süre/mesafe tablosu (≤25×25) ve "X dakikada nereye ulaşırım" (izokron, ≤60 dk) | "10 dakikada yürüyerek nereye varırım?" |
| `yakindakiler` | M033 | Yakındaki eczane, kafe, ATM, okul vb. (Türkçe kategori adları çalışır) | "Bana en yakın 3 eczane" |
| `harita-ciz` | M034 | Rota/nokta/alanları SVG harita olarak çizer; istenirse demo altlık (yollar, binalar, parklar) ekler | "Bu rotayı haritada göster" |
| `poligon-icinde-mi` | M026 | Bir nokta bir alanın içinde mi, sınır kutusu, merkez | "Bu nokta Moda mahallesinin içinde mi?" |
| `alan-hesapla` | M027 | Çokgenin yüzölçümü (m², hektar, km²) | "Bu parkın alanı ne kadar?" |
| `yon-ve-varis-noktasi` | M028 | İki nokta arası yön (pusula: K, KD, D…), orta nokta, "şu yönde 500 m gidersem neredeyim" | "İskele Moda'nın hangi yönünde?" |
| `harita-karosu` | M029 | Harita karosu (z/x/y) hesapları, karo sınırları | "Bu nokta 16. zoomda hangi karoda?" |
| `mesafe-vincenty` | M003 | Elipsoid üzerinde hassas kuş uçuşu mesafe | "İki nokta arası kuş uçuşu kaç metre?" |
| `mesafe-buyuk-daire` | M004 | Küre üzerinde büyük daire mesafesi, başlangıç yönü | "İstanbul–Ankara kuş uçuşu" |
| `loksodrom` | M005 | Sabit pusula yönlü (rhumb) mesafe ve yön | "Sabit yönle gitsem kaç km?" |
| `cizgi-sadelestir` | M021 | Çok noktalı çizgiyi sadeleştirir (Ramer–Douglas–Peucker) | "Bu GPS izini sadeleştir" |
| `polyline-kodla` | M024 | Google tarzı encoded polyline kodla/çöz | "Bu polyline'ı koordinatlara çevir" |
| `geohash` | M025 | Geohash kodla/çöz, komşu hücreler | "Bu noktanın geohash'i ne?" |

Tipik zincir: **yer-ara → rota → yakindakiler → harita-ciz.** Claude bunu kendisi sıralar; siz yalnızca doğal dilde sorarsınız.

## Örnek komutlar (demo veri: Kadıköy)

Aşağıdakiler paketle gelen Kadıköy demo verisiyle doğrudan çalışır (`dataset: demo_kadikoy`):

1. "Kadıköy iskelesinden Moda'ya yürüyerek rota çıkar, kaç dakika sürer?"
2. "Bu rotayı altlıklı bir SVG harita olarak çiz ve kaydet."
3. "Bahariye Caddesi civarında 500 metre içindeki eczaneleri en yakından sırala."
4. "Moda sahiline en yakın 5 kafeyi göster, her birine yürüme süresini tablo yap."
5. "40.9856, 29.0306 koordinatında ne var? Hangi sokak, hangi mahalle?"
6. "Kadıköy iskelesinden 10 dakikalık yürüme mesafesinde nerelere ulaşırım? Haritada göster."
7. "İskeleden Moda'ya arabayla mı yürüyerek mi daha hızlı? İkisini karşılaştır."
8. "Rıhtım'dan başlayıp önce Altıyol'a uğrayıp sonra Moda'ya giden yürüyüş rotası yap."
9. "Yoğurtçu Parkı'nın alanı kaç hektar?"
10. "Kadıköy iskelesi Moda'nın hangi yönünde ve kuş uçuşu kaç metre?"

Yazım hataları sorun değildir ("kadikoy iskele", "eczne"); arama Türkçe harfleri katlayıp benzerliğe göre eşleştirir. Aynı adı taşıyan birden çok yer olabilir (ör. "Kadıköy iskele" kütüphane, karakol ve vapur iskelesini getirir); Claude `categories` filtresiyle (iskele, eczane, park, mahalle…) daraltabilir. Bulunan yer hâlâ belirsizse Claude adayları listeleyip sizden seçmenizi istemelidir.

> Demo veri yaklaşık 2,5 × 2,8 km'lik bir Kadıköy alanıdır (Rıhtım–Moda–Bahariye–Hasanpaşa). **"Kadıköy'den Beşiktaş'a"** gibi istekler için o bölgeyi kapsayan kendi OSM özetinizi eklemeniz gerekir. Vapur hatları rota ağına dahil değildir.

## Kurulum (Claude Desktop)

1. Klasörü bir yere çıkarın (örn. `C:\harita` veya `/home/ben/harita`). Paketler `M003.tar.gz` … `M034.tar.gz` ve `map_data.tar.gz` olarak ayrıdır; hepsini **aynı klasöre** açın.
2. Python 3.11+ ile sanal ortam kurun:
   ```
   python3 -m venv .venv
   .venv/bin/pip install -r requirements-test.txt
   ```
   (Windows'ta `.venv\Scripts\pip`.) Rota ve matris paketleri `networkx` kullanır; diğerleri yalnızca `mcp` ve `jsonschema` ister.
3. `claude_desktop_config.json` içindeki `/MUTLAK/YOL/...` yer tutucularını kendi tam yollarınızla değiştirip Claude Desktop ayarlarındaki dosyaya ekleyin. `SKILLPACK_MAP_DATA` veri klasörünü, `SKILLPACK_MAP_OUTPUT` haritaların kaydedileceği klasörü gösterir (bu klasörü siz oluşturun).
4. Claude Desktop'ı yeniden başlatın; araçlar listesinde 15 araç görünmelidir. İstemediğiniz becerileri config'ten silebilirsiniz.

İsteğe bağlı doğrulama: `.venv/bin/python -m pytest` (tüm testler).

## Kendi verinizi kullanmak

Veri kümeleri **ada göre** seçilir; araçlar asla rastgele dosya yolu kabul etmez. `SKILLPACK_MAP_DATA` klasörüne şu dosyalardan birini/birkaçını koyun:

- `ad_roads.geojson`, `ad_places.geojson`, `ad_areas.geojson` (GeoJSON, WGS84 lon/lat)
- `ad_places.csv` (sütunlar: `name,lat,lon,category`, isteğe bağlı `address`)
- `ad.osm` (OpenStreetMap XML; JOSM veya openstreetmap.org "Dışa aktar" ile küçük bir alan)

Sonra "**istanbul_avrupa** veri kümesinde Beşiktaş iskelesini bul" gibi sorabilirsiniz. Dosya sınırı 64 MiB'tir; `.osm` dosyaları her çağrıda yeniden okunur, bu yüzden büyük alanlarda GeoJSON'a çevirmek daha hızlıdır (10 saniye sınırı).

## SVG / GeoJSON nasıl görüntülenir?

- **SVG harita:** `harita-ciz` çıktısı SVG metnidir. Claude'da artifact olarak doğrudan görünür. `save_name` verirseniz `SKILLPACK_MAP_OUTPUT` klasörüne `.svg` olarak kaydedilir (var olan dosyanın üzerine yazmaz); herhangi bir tarayıcıda çift tıklayarak açın. PNG gerekirse tarayıcıdan ekran görüntüsü veya Inkscape ile dışa aktarın.
- **GeoJSON:** `rota` aracı `feature` alanında GeoJSON döndürür. QGIS (çevrimdışı) ile açabilir veya `harita-ciz`e verip çizdirebilirsiniz. geojson.io gibi web araçları da açar, ancak bu verinizi internete gönderir; paketlerin kendisi hiçbir zaman ağa çıkmaz.
- Örnek çıktı: `example_route.png` (Kadıköy iskelesi → Moda yürüyüş rotası, yakındaki eczaneler işaretli).

## Sınırlar (Google Haritalar ile farklar)

- **Canlı trafik yok:** süreler serbest akış hızlarıyla hesaplanır (araba yol tipine göre, varsa `maxspeed`; yaya 5 km/sa, merdivende 3; bisiklet 15 km/sa).
- **Dönüş yasakları, toplu taşıma, vapur, metrobüs, otobüs saatleri yok.** Tek yön ve erişim etiketleri dikkate alınır.
- **Uydu görüntüsü, sokak görünümü, 3B, fotoğraf, yorum, açık/kapalı saati yok.** Altlık yalnızca vektör çizimdir; deniz dolgu olarak boyanmaz.
- Demo veri küçük bir Kadıköy kesitidir ve 2026-11-12 tarihli OSM anlık görüntüsüdür; eksik ya da eski olabilir.
- Sonuçlar karar desteğidir; önemli yolculuklarda güncel bir kaynakla doğrulayın.

## Lisans

Kod: her paketin kendi `LICENSE`/`NOTICE` dosyası (MIT, BSD-2, BSD-3); özet `LICENSE_INDEX.md`. Demo veri: **© OpenStreetMap contributors**, ODbL 1.0 — koddan ayrı lisanslıdır, ayrıntı `map_data/README.md`. Bu veriden üretilen haritalarda atıf korunmalıdır (`harita-ciz` otomatik ekler).
