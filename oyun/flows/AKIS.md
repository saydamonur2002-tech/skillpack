# Oyun kurma akışı (`flows/oyun-kur.flow.json`)

Bu akış hiçbir skill'e bağlı değildir. Hangi adımın hangi aracı hangi girdiyle çağıracağını tek başına söyler. Akışı `run_flow.py` (veya bir model, ya da MCP üzerinden bir insan) aynı sırayla yürütebilir.

**İlke:** kodu karar verir, model açıklar, usta onaylar. Model hiçbir sayıyı uydurmaz; her sayı bir aracın JSON çıktısından gelir.

**Token bütçesi:** token yalnızca kurulumda harcanır (19 araç çağrısı). Ortaya çıkan `index.html` tarayıcıda kendi JavaScript döngüsüyle çalışır; oyun sırasında hiçbir model ya da ağ çağrısı yapılmaz.

## Çalıştırma

```
python3 flows/run_flow.py --out oyun_cikti        # tohum 2026, 40x30 harita
python3 flows/run_flow.py --out o2 --set seed=7   # başka şehir
```

Çıktılar:
- `oyun_cikti/adimlar/NN_<adim>.json`: her adımın tam girdisi ve çıktısı (denetim izi)
- `oyun_cikti/akis_raporu.json`: özet, kontroller, süreler
- `oyun_cikti/index.html`: oynanabilir oyun, tek dosya

Çıkış kodları:
- 0: tamam
- 2: bir skill hata verdi
- 3: bir kontrol tuttu ve akış "DUR VE SOR" durumunda kaldı
- 4: son doğrulama başarısız

## Çözümleyiciler

Bir adım, önceki adımların çıktılarını şu işaretlerle kullanır:
- `$var`: değişken
- `$ref`: `adim.result.yol` biçiminde önceki adımın çıktısı
- `$tile_center_x/y`: kare merkezi
- `$pluck`: listeden alan seçer
- `$concat`: birleştirir
- `$range`: sayı aralığı

Bir referans çözülemezse akış durur. Varsayılan değer uydurulmaz.

## Adım sırası

| # | Adım | Skill (MCP sunucusu) | Ne yapar | Durdurma koşulu (kontrol tutmazsa DUR VE SOR) |
|---|---|---|---|---|
| 1 | harita | G002 sehir-haritasi | Tohumdan yol/kaldırım/bina/park karoları; doğuş, karakol, boyacı, para, simge noktaları ve rota çiftleri | Yollar bağlı değil; bina < 50 |
| 2 | yaya_rotalari | G005 yol-bulma | Yaya rotalarını yürünebilir maliyetlerle A* ile bulur | Bir rota bulunamadı |
| 3 | trafik_rotalari | G005 yol-bulma | Trafik araçlarının yol üstü rotaları | Bir rota yoldan çıkıyor ya da yok |
| 4 | arac_ayari | G003 arac-fizigi | 3 saniyelik gaz provasıyla bisiklet modeli | Azami hıza ulaşılmadı ya da sınır aşıldı |
| 5 | polis_yakalar | G006 npc-yonlendirme | Takip davranışı: yavaş oyuncu yakalanır | Yakalanmıyor (polis işe yaramaz) |
| 6 | polis_kacis | G006 npc-yonlendirme | Hızlı oyuncu kaçabilir | Kaçış imkânsız (oyun adil değil) |
| 7 | yaya_durus | G006 npc-yonlendirme | Yaklaşma davranışı: yaya hedefte durur | Yaya titriyor ya da geçip gidiyor |
| 8 | aranma | G007 aranma-seviyesi | Suç → ısı → yıldız; soğuma; boyacı | Suç yıldız vermiyor ya da boyacı silmiyor |
| 9 | gorev_dogrula | G008 gorev-sistemi | 5 görevlik zincirin (M1–M5) yapısı ve sırası | Geçersiz zincir ya da sıra 5 değil |
| 10 | gorev_erisim | G005 yol-bulma | Her görev hedefine sürüş yolu | Ulaşılamayan hedef var |
| 11 | gorev_prova | G008 gorev-sistemi | Görevleri süre sınırlarıyla oynatır | Bitirilemeyen görev var |
| 12 | katalog | G009 ekonomi-envanter | Fiyat kataloğu (tamir kiti, boya, yakıt…) | Boya fiyatı yok |
| 13 | ekonomi_prova | G009 ekonomi-envanter | Ödüllerle alışveriş provası, tam sayı defteri | Reddedilen işlem var (ekonomi dengesiz) |
| 14 | sesler | G011 ses-efekti | ZzFX ses bankası (8 ses) | Kırpılma var ya da ses > 2 sn |
| 15 | dongu | G001 oyun-dongusu | Sabit adımlı döngü provası | Panik ya da karede > 2 güncelleme |
| 16 | dongu_takilma | G001 oyun-dongusu | Sekme takılması benzetimi | Panik tetiklenmedi (koruma çalışmıyor) |
| 17 | kayit | G010 kayit-yukle | Kayıt zarfı ve sağlama toplamı (FNV-1a) | Kayıt ≥ 4096 bayt |
| 18 | carpisma | G004 carpisma-testi | Doğuş noktası binaların içinde mi (SAT) | Çarpışan doğuş var |
| 19 | html | G012 html-oyun-uret | Bütün sonuçları tek dosyalık HTML oyuna gömer | Dış kaynak ya da URL bulundu |

## Adımlardan sonra (`after_tr`)

1. `result.html` dosyası `index.html` olarak yazılır.
2. Bağımsızlık kontrolü yapılır: dosyada `http(s)://` ya da dış kaynak yüklemesi olmamalı.
3. Her `<script>` bloğu `node --check` ile denetlenir (Node kuruluysa).
4. Başsız deneme (`headless_check.js`) yapılır: oyun 10 saniye boyunca gaz basılı oynatılır. Araba hareket etmeli ve hata çıkmamalı.
5. Usta onayı gerekir. Usta oyunu oynar; kontrolleri, görev dengesini ve polis dengesini onaylar. Durum şu an: **bekliyor**.

## DUR VE SOR

Bir kontrol tutmazsa `run_flow.py` 3 koduyla durur. Hangi kontrolün neden tutmadığı `akis_raporu.json` içine Türkçe olarak yazılır. Model bu durumda sayıları değiştirip yeniden denemez. Kullanıcıya ya da ustaya sorar: tohum mu değişsin, değişken mi değişsin?
