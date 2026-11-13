# kutuphane/: açık kaynak işlevlerinden çıkarılmış beceri paketleri

Bu klasör, açık kaynak projelerdeki tek işlevleri **internetsiz çalışan, testli, kaynağı ve lisansı kayıtlı** küçük paketlere çeviren 46 beceriyi içerir. Her paket `upstream/` altında kaynak projenin kopyasını, `LICENSE` ve `NOTICE` dosyalarını, `manifest.json` içinde kaynak adresi ve sürümünü taşır.

> **Durum: ön sürüm.** Paketlerin çoğu yalnızca kendi testlerinden geçti (aşağıdaki doğruluk düzeyleri). Hiçbiri bir kurum ya da uzman tarafından **onaylanmadı**. Hesapları, kaynağın kendi tanımına göre doğru kabul edilir; sağlık, güvenlik, hukuk, finans gibi kararların tek dayanağı yapılmamalıdır. Yapay zekâ (Claude) yardımıyla üretildi; üretim, kaynak ve lisans kayıtları paketlerin içindedir.

## Doğruluk düzeyleri

| Düzey | Anlamı | Paket sayısı |
|---|---|---|
| bağımsız doğrulandı | Sonuçlar, paketten bağımsız bir yolla (başka kütüphane ya da resmî kaynak) karşılaştırıldı ve tuttu | 7 |
| kısmen doğrulandı | Bir bölümü bağımsız karşılaştırıldı | 1 |
| sözleşme testli | Yalnızca paketin kendi bilinen-cevap testleri ve şema/hata/belirlenimcilik testleri geçti | 38 |

Düzey, paketin `manifest.json` ve katalogdaki `kanit` alanında açıklanır. "Sözleşme testli", çıktının doğru olduğunun **kanıtı değildir**.

## Paketler

### Ayrıştırma ve dönüştürme

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| A44 | Süre ifadesini saniyeye çevirme | sözleşme testli | Apache-2.0 | 5 |
| A60 | FHIR şablon doldurma | sözleşme testli | Apache-2.0 | 5 |

### Cihaz ve protokol

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| A15 | Baxter SDK sürüm uyumu | sözleşme testli | BSD-3-Clause | 5 |
| A4 | Daikin klima sensör yanıtı çözücü | sözleşme testli | MIT | 6 |
| A50 | Cast V2 mesaj çözücü | sözleşme testli | MIT | 7 |
| B49 | Zigbee sıcaklık ve pil çözücü | sözleşme testli | MIT | 6 |
| B50 | Xiaomi sıcaklık aralık filtresi | sözleşme testli | Apache-2.0 | 6 |
| B53 | SHT3x CRC denetimli çözücü | sözleşme testli | BSD-3-Clause | 7 |
| B54 | Linux pil durumu | sözleşme testli | BSD-3-Clause | 7 |

### Dil ve niyet

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| A12 | Niyet tanıma puanlayıcı | sözleşme testli | CC0-1.0 | 5 |
| A59 | Öznitelik dilbilgisi eşleşmeleri | sözleşme testli | Apache-2.0 | 6 |
| A6 | Niyet gereksinimleri (Adapt) | sözleşme testli | Apache-2.0 | 5 |
| B45 | Sıcaklık cümlesi dilbilgisi (TR/EN) | sözleşme testli | CC-BY-4.0 | 5 |

### Doğrulama ve denetim

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| A16 | Baxter eklem kaydı doğrulayıcı | sözleşme testli | BSD-3-Clause | 6 |
| A42 | FHIR hasta kaydı yapı denetimi | sözleşme testli | Apache-2.0 | 6 |
| A54 | Baxter montaj durumu doğrulayıcı | sözleşme testli | BSD-3-Clause | 5 |
| A63 | ACL bit denetçisi | sözleşme testli | Apache-2.0 | 6 |
| A64 | CRC-32 sağlama toplamı | sözleşme testli | Apache-2.0 | 7 |
| B71 | OpenAPI parametre kuralları | sözleşme testli | Apache-2.0 | 5 |
| B72 | AsyncAPI sensör yükü sözleşmesi | sözleşme testli | Apache-2.0 | 5 |

### Harita ve konum

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| M003 | Vincenty elipsoid mesafesi | sözleşme testli | MIT | 39 |
| M004 | Büyük daire mesafesi | sözleşme testli | MIT | 21 |
| M005 | Loksodrom (sabit pusula yönü) | sözleşme testli | MIT | 23 |
| M021 | Çizgi sadeleştirme | sözleşme testli | BSD-2-Clause | 28 |
| M024 | Polyline kodlama | sözleşme testli | BSD-3-Clause | 37 |
| M025 | Geohash | sözleşme testli | MIT | 34 |
| M026 | Nokta alanın içinde mi? | bağımsız doğrulandı | MIT | 33 |
| M027 | Çokgen alanı | bağımsız doğrulandı | BSD-2-Clause | 34 |
| M028 | Varış noktası ve yön | bağımsız doğrulandı | MIT | 35 |
| M029 | Harita karesi (z/x/y) | bağımsız doğrulandı | MIT | 40 |
| M030 | Çevrimdışı yol rotası | bağımsız doğrulandı | BSD-3-Clause | 37 |
| M031 | Süre/mesafe matrisi ve izokron | sözleşme testli | BSD-3-Clause | 32 |
| M032 | Yer arama ve ters geokodlama | bağımsız doğrulandı | MIT | 35 |
| M033 | Yakındaki yerler | bağımsız doğrulandı | MIT | 31 |
| M034 | Statik harita çizimi (SVG) | kısmen doğrulandı | BSD-3-Clause | 35 |

### Hesap ve dönüşüm

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| A61 | Korelasyon (Pearson/Spearman) | sözleşme testli | Apache-2.0 | 5 |
| A62 | Kosinüs benzerliği | sözleşme testli | Apache-2.0 | 6 |
| A65 | Dairesel tampon yeniden oynatma | sözleşme testli | Apache-2.0 | 6 |
| B44 | Sıcaklık dönüştürücü | sözleşme testli | Apache-2.0 | 6 |
| B61 | Sistem sayaç aritmetiği | sözleşme testli | BSD-3-Clause | 5 |
| B73 | QUDT sıcaklık dönüşümü | sözleşme testli | CC-BY-4.0 | 6 |

### Kural ve karar

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| B46 | Hareket-ışık otomasyonu (oynatma) | sözleşme testli | Apache-2.0 | 5 |

### Mühendislik ve bilim

| No | Beceri | Doğruluk | Lisans | Test |
|---|---|---|---|---|
| A28 | Yörünge hatası (ADE/FDE) | sözleşme testli | MIT | 6 |
| A57 | Lazer taramayı noktalara çevirme | sözleşme testli | BSD-3-Clause | 4 |
| B100 | Güneş konumu | sözleşme testli | BSD-3-Clause | 5 |
| B108 | EMG RMS ve MAV | sözleşme testli | MIT | 7 |

Ayrıntılı kayıtlar: [`katalog.json`](katalog.json).

## Yapı

```text
<NO>/                  her paket
  SKILL.md             kullanım kılavuzu
  manifest.json        kimlik, girdi/çıktı şemaları, kaynak, lisans, dağıtım etiketi
  tool/                tek işlevli, JSON girdi/çıktılı çalıştırılabilir kod
  mcp/                 isteğe bağlı MCP giriş noktası
  tests/               bilinen-cevap vektörleri ve testler
  upstream/            kaynak projenin kopyası (kanıt)
  LICENSE, NOTICE      kaynağın lisansı ve bildirimleri
_mcp/                  paketlerin ortak MCP çalışma zamanı ve test yardımcıları
```

## Çalıştırma ve test

Python 3.11+ gerekir. Haritalı `M…` paketleri kendi `requirements.txt` dosyalarındaki sabit sürümleri ister. `A…`/`B…` paketleri için sabit sürümler [`requirements-ab.txt`](requirements-ab.txt) içindedir. Testler ağsız ortamda çalışacak şekilde yazılmıştır.

**Son doğrulama (13 Kasım 2026):** 46 paketin tamamı, bu klasördeki konumlarında ve ağ kapalı ortamda geçti (toplam 670 test). Haritalı `M…` paketleri kendi `requirements.txt` sürümleriyle, `A…`/`B…` paketleri `requirements-ab.txt` sürümleriyle çalıştırıldı; Node gerekmedi. Bu bir kurulum kanıtıdır, doğruluk kanıtı değildir (bkz. doğruluk düzeyleri).

```bash
cd kutuphane/M004 && python -m pytest -q          # harita paketi
cd kutuphane/A64  && python -m pytest -q tests    # A/B paketi (MCP testi için mcp==1.30.0 gerekir)
```

Bir paketi doğrudan çağırmak: `echo '<girdi JSON>' | python tool/main.py` (girdi biçimi paketin `manifest.json` şemasında).

## Bilinen sınırlar

- **Yalnız Linux'ta test edildi** (Python 3.13); Windows ve macOS denenmedi.
- **Paket dışı çalışma zamanı gerektirenler çıkarıldı.** Aşağıdaki 7 paket bu ön sürümde yoktur, çünkü testleri temiz bir kopyada çalışmadı (Node modülü ya da ikili dosya gerekiyor, bu depoda kurulum betiği yok):
- `B62`: opa ikilisi gerekir (paket dışı çalışma zamanı)
- `B63`: Node modülü json-rules-engine gerekir
- `B64`: Node modülü (JSON Schema doğrulayıcı) gerekir; temiz ortamda testler geçmedi
- `B65`: Node modülü ajv gerekir
- `B66`: Node modülü eslint gerekir
- `B67`: ruff ikili dosyasının paket dışı yolu gerekir
- `B85`: sandbox araçları gerekir
- Sözleşme testli paketler için çıktıların bağımsız doğruluğu ölçülmedi.
- Kaynak commit/sürüm kayıtları paket içindeki `manifest.json` ve `SOURCE.md` dosyalarındadır; lisanslar kaynak projenin kendi kaydıyla eşleştirilmiştir (tarih: 12 Kasım 2026).
- Her paketin lisansı kendi `LICENSE` dosyasındadır; bu depodaki Apache-2.0 yalnızca depoya özgü özgün içeriğe uygulanır, `upstream/` altındaki üçüncü taraf içeriğin lisansını değiştirmez.
