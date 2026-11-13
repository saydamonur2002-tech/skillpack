# idna-encode — Alan adını ASCII'ye çevirme

## Ne işe yarar?
Türkçe/Almanca gibi harfler içeren alan adını (ör. `münchen`) IDNA 2008 kuralıyla ASCII (punycode) biçimine çevirir: `xn--mnchen-3ya`.

## Girdi / çıktı
`{"input": "münchen"}` → `{"result": "xn--mnchen-3ya"}`

## Kaynak ve lisans
[idna](https://github.com/kjd/idna) 3.20, **BSD-3-Clause** (`references/LICENSE.txt`). Kütüphane pakete gömülü değildir; `pip install idna` gerekir.

## Sınırlar
Çevrimdışı. Girdi metin olmalı. IDNA 2003 değil 2008 kuralları. Testler kendi kendini sınar; bağımsız bir doğrulama kaynağı yoktur (`truth_level: sozlesme`).
