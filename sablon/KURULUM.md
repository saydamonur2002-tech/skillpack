# Paketin kurulumu (v0.1-taslak)

> Bu metin bir **taslaktır**. Mevcut referans çalıştırıcı (`cli/`) bu kontrollerin çoğunu henüz uygulamaz; aşağıda ve [README.md](README.md) içindeki "Uygulama durumu"na bakın.
> Paket, modele gösterilmeden önce bir uygulama gibi cihaza (yerel sunucuya) kurulur. Kurulmamış veya kontrolden geçmemiş paket MCP'de görünmez.

## Nerede kurulur

Ana model (32B) yerel sunucudadır. Teknik paketleri de orada kurulur ve yürütülür. Telefon arayüz, varsa kendi sensörleri ve küçük yardımcı model (1,5B–8B) içindir. Bulut varsayılan olarak kapalıdır; ancak insan açıkça onaylarsa kullanılır.

## Kurulum sırası

Aşağıdaki adımlardan **biri bile düşerse paket kurulmaz** ve MCP'ye çıkarılmaz.

1. **İmza ve iptal.** İmza geçerli midir? Anahtar güvenilen listede midir? Paket veya anahtar iptal listesinde midir? İmzasız, bozuk veya iptal edilmiş paket kurulmaz.
2. **Şema.** Dosya yapısı ve alan türleri şemaya uyar mı? Beklenen dosyalar (`paket.yaml`, adımlar, kurallar, profil, donanım, testler, kılavuz, imza) yerinde midir?
3. **Sert sınır ve tehlike dolu mu?** `kurallar/sert_sinirlar.yaml` ve `kurallar/tehlike.yaml` boş bırakılmışsa paket kurulmaz. Dayanak bilinmiyorsa gerçek madde uydurulmaz; `[VARSAYIM]` yazılmış olmalıdır.
4. **Testler bu cihazda geçer mi?** Paketin kendi testleri, bu cihazın donanımıyla koşulur. Bir test düşerse kurulum durur. **Beklenen alanı boş olan test geçersizdir; geçti sayılmaz** ve kurulumu düşürür.
5. **Gereken arayüzler var mı?** `paket.yaml` içindeki `gereken_arayuzler`, bu cihazın `donanim.yaml` dosyasında ve fiilen bağlı görünmelidir. Eksik bir ağırlık sensörü veya kaldırıcı varsa paket kurulmaz.
6. **Profil sert sınırı aşmıyor mu?** İşletme kendi profilini girer (örneğin azami 25 kg). Değer sert sınırın (örnek 30 kg) dışındaysa, veya bir test bu yüzden düşüyorsa, değişiklik uygulanmaz ve kurulum tamamlanmaz.
7. **Kayıt, sürüm, geri dönüş.** Kurulan paket "kurulu" listesine adı, sürümü ve imzasıyla yazılır. Bir önceki sürüm geri dönüş için saklanır.

## Ancak şimdi MCP

Kurulum bu yedi kontrolü geçtikten sonra paket, modelin önüne **tek bir araç** olarak çıkar. Model paketin iç dosyalarını gezmez; sadece bu aracı çağırabilir. Çağrı gelince adımları paket yürütür, model sonucu insana anlatır.

## Anlam katmanı

MCP'nin modele gösterdiği araç tarifi, yalnız parametre listesi olamaz. Aşağıdaki anlam katmanı bulunmalıdır; yoksa model aracı "var ama ne yaptığı belirsiz" görür ve doğru eşleyemez:

| Alan | Modele ne anlatır | Kaynak |
|---|---|---|
| **amaç** | Bu teknik neyi başarır | `paket.yaml` / adımların `amac` alanı |
| **ön koşul** | Başlamadan önce ne doğru olmalı | adımların `on_kosullar` alanı |
| **etki** | Bitince dünyada ne değişmiş olmalı | adımların `etki` alanı |
| **donanım** | Cihazda hangi arayüzler var, ne yapabilir | `donanim.yaml` |
| **mevcut durum** | Şu an hangi ön koşullar sağlanmış | `donanim.yaml` içindeki `durum` |

Model bu tarifi okuyup insanın isteğini doğru adıma eşler. Yanlış sıra seçerse paket ön koşul kontrolünde onu durdurur. Model planı okur ve sırayı anlatır; yürütmez ve karar vermez.

## Kısa akış

```
yükle → imza+iptal → şema → sınır/tehlike dolu mu → testler geçer mi
     → arayüzler var mı → profil sınır içinde mi → kaydet + sürüm
     → (ancak şimdi) MCP'de tek araç olarak görün
```
