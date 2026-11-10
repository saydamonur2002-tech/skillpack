# examples/

Üç çalışan örnek paket. Her biri doğrulanmış, kabul testlerinden geçmiş ve imzalanmıştır.

| Paket | Alan | Karar |
|---|---|---|
| [rulman-isi-titresim](rulman-isi-titresim/) | Fabrika | Rulman çalışmaya uygun mu: devam, izle, yağla, dur |
| [soguk-mal-kabul](soguk-mal-kabul/) | Lokanta | Gelen soğuk ürün kabul edilir mi: kabul, şartlı, kısa ömür, ret |
| [kazanim-telafi-karari](kazanim-telafi-karari/) | Okul | Ölçme sonrası sıradaki adım: ilerle, küçük grup, soruyu yenile, yeniden öğret |

## Önemli uyarı

**Bu paketler biçimi göstermek için yazıldı. İçlerindeki eşik değerleri örnektir ve hiçbir usta, şef ya da öğretmen tarafından onaylanmamıştır.** Onay kayıtları bunu açıkça yazar. Sıcaklık sınırları, titreşim değerleri ve başarı yüzdeleri sahada kullanılmadan önce işin sahibi tarafından kendi koşullarına göre belirlenmelidir.

Vakaların tamamı sentetiktir.

## İmza

`trust/` dizinindeki açık anahtar, bu örnekleri imzalayan gösterim anahtarına aittir. Özel anahtar depoda yoktur ve saklanmamıştır. Bir örneği değiştirirseniz imza geçersiz olur; kendi anahtarınızla yeniden imzalayın:

```bash
skillpack keygen --out ~/benim.key --trust examples/trust
skillpack sign examples/soguk-mal-kabul --key ~/benim.key
```

Kendi paketinizi yazmak için: [docs/USTADAN_PAKETE.md](../docs/USTADAN_PAKETE.md).

Teknik taslakta planlanan örnekler (depo stok sapması, ses kaydı düzeltme, koli ayırma simülasyonu) henüz yazılmadı.
