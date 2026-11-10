# Kabul testleri (yalnız tarif)

Bu dosya koşulmaz. Simülasyon ve doğrulayıcı yoktur.

Beklenen, `references/kurallar.yaml` ile aynı masadır:

| Girdi | Beklenen rampa | Not |
|---|---|---|
| küçük, etiket A | rampa-1 | |
| küçük, etiket B | insan | Küçük kural yalnız A içindir |
| orta, etiket A veya B | rampa-2 | Orta kural etiket harfine bakmaz |
| büyük, etiket okunmuş | rampa-3 | Etiket yoksa üstteki kural insana gider |
| etiket yok | insan | Bu kural listedeki ilk kuraldır |
| hareket komutu | reddedilir | `mode: simulation-only`. Onay kapısı kapalıdır |

Geçiş kapısı, bu satırlar bir simülasyon sahnesinde insan onayı olmadan kol hareket ettirmeden tekrar edilene kadardır. O sahne yazılmadı.
