# Adım Şablonu ve Mekanizma (v0.1-taslak)

> Bu bölüm bir **taslaktır**. Şablon boştur; hiçbir değeri gerçek bir uzman onaylamamıştır.
> Mevcut referans çalıştırıcı (`cli/`) bu şablonun tüm alanlarını henüz uygulamaz; aşağıda "Uygulama durumu"na bakın.

## Temel ilke

**Model bir şey öğrenmez, sadece çevirir.** Tekniğin bilgisi modelin içinde değil, pakettedir.

```
İnsan  ⇄  Yerel LLM (tercüman)  ⇄  MCP (bağlantı)  ⇄  DİKEY TEKNİK PAKETİ (merkez)  ⇄  Uygulamalar/makineler (çevre)
```

- **Merkez:** tekniğin adımları, ölçütleri, sınırları, testleri, kökeni.
- **Çevre:** işi fiilen yapan yazılım ve makineler. Değiştirilebilir; aynı arayüzü sunan her biri takılabilir.
- **LLM:** insanın söylediğini yapılandırılmış değere çevirir, sonucu anlatır. Karar vermez.

## Üç dosya

| Dosya | Ne tutar | Kim değiştirir |
|---|---|---|
| [`sablon/adim.sablon.yaml`](adim.sablon.yaml) | Tekniğin tek bir adımı: amaç, girdi, ön koşul, tehlike, işlem, etki, doğrulama, bağlayıcı, LLM sınırı, test, köken | Usta / paket yazarı |
| [`sablon/profil.sablon.yaml`](profil.sablon.yaml) | İşletmeye özel değerler (örn. azami ağırlık 25 kg) ve değişiklik kaydı | İşletme, onayla |
| [`sablon/paket.sablon.yaml`](paket.sablon.yaml) | Adımların sırası, gereken arayüzler, kılavuz, imza | Paket yazarı |

## Bir adım nasıl çalışır

1. **Girdileri topla.** Öncelik sabittir: `sensör > kayıt > insan > LLM`. Alttaki kaynak üsttekini asla ezemez. Sensör verisi `tazelik_sn`'den eskiyse kullanılmaz.
2. **Sert sınırı kontrol et.** Değer fiziksel/yasal sınırın dışındaysa reddedilir. Profil bu sınırı genişletemez.
3. **Tehlike kurallarına bak.** Eksik veri olsa bile önce bunlar değerlendirilir. Bilinen tek bir tehlike `dur` için yeterlidir; "bilinmiyor"a düşmez.
4. **Ön koşulları kontrol et.** Sağlanmazsa adım başlamaz (`bekle`, `sor` veya `dur`).
5. **İşlemi yürüt.** Hesap, tablo veya karar; kesin koddur, tahmin değildir.
6. **Bağlayıcıyı çağır.** Varsayılan izin `oneri`dir: sistem önerir, insan onaylar.
7. **Doğrula.** Aracın "başardım" demesi yetmez; ölçümle `basarili / basarisiz / bilinmiyor` ayrılır.
8. **Başarısızsa** tanımlı yol izlenir: tekrar, geri al, dur veya insana sor.

## Profil değişikliği nasıl yapılır

```
"Kutular artık 25 kg"  →  LLM öneri yazar (max_agirlik: 25)
                       →  Şema kontrolü (sert sınır içinde mi?)
                       →  İnsan onayı
                       →  Testler yeniden koşar
                       →  Değişiklik kaydına yazılır, profil sürümü artar
```
Kod değişmez. Testlerden biri düşerse değişiklik uygulanmaz.

## Dikey işlere nasıl uyarlanır

Şablon aynı kalır; her sektör sadece içini doldurur.

| Alan | Örnek adım | Girdi / sensör | Tehlike kuralı | Bağlayıcı arayüz | Doğrulama |
|---|---|---|---|---|---|
| Depo / robotik | Kutu kaldır | ağırlık sensörü, kavrama durumu | ağırlık > azami ⇒ dur | `kaldirici.v1` | yükseklik sensörü ±2 cm |
| Mutfak | Soğuk mal kabul | saplama termometre, SKT | ambalaj hasarlı ⇒ ret | `kayit_defteri.v1` | teslim fişi notu |
| Fabrika bakım | Rulman kontrol | ısı, titreşim | ısı ≥ sınır ⇒ dur | `bakim_emri.v1` | ölçüm tekrarı |
| Telefon | Pil koruma | pil %, sıcaklık, termal durum | sıcaklık ≥ 40 °C ⇒ bulutu kapat | `android_sistem.v1` | sonraki ölçüm |
| Hastane | Randevu dağıtımı | doluluk, bekleme süresi | acil işaret ⇒ insana | `randevu_sistemi.v1` | atama kaydı |
| Okul | Kazanım telafi | sınav puanı, devam | — | `not_sistemi.v1` | sonraki ölçme |

Uyarlama sırası:
1. Tekniği bilen kişiyle işi **küçük adımlara** böl.
2. Her adım için şablonu doldur; özellikle **tehlike** ve **doğrulama** alanlarını boş bırakma.
3. Değişen değerleri **profile**, değişmez sınırları **sert_sinir**'a ayır.
4. Her adıma en az bir normal, bir sınır, bir tehlike testi yaz.
5. Bağlayıcıyı arayüz adıyla yaz; hangi yazılımın takılacağı sahada seçilir.
6. Usta onaylamadan paket `DEMO` etiketiyle yüklenir.

## Uygulama durumu (dürüst not)

| Özellik | Durum |
|---|---|
| Akış, tablo, karar, test, Ed25519 imza, MCP sunucusu | Mevcut çalıştırıcıda **var** |
| Kaynak önceliği (sensör > LLM), tazelik kontrolü | **Yok** — şu an LLM argümanı sensör değerini ezebiliyor |
| Eksik veride önce tehlike kuralı | **Yok** — bilinen tehlike "bilinmiyor"a düşebiliyor |
| Amaç / ön koşul / etki / doğrulama alanları | **Yok** — bu şablonla tanımlandı |
| Profil – sert sınır ayrımı, onaylı değişiklik akışı | **Yok** |
| Bağlayıcı arayüzleri | **Yok** |
| Boş beklentili testin reddi | **Yok** — şu an geçiyor sayılıyor |

Bu şablon bir **sözleşme taslağıdır**; çalıştırıcının bunu uygulaması sonraki iştir.
