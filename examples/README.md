# examples/

Beş çalışan örnek paket. Her biri doğrulanmış, kabul testlerinden geçmiş ve imzalanmıştır. İlk üçü sentetik örnektir; son ikisi açık kamu verisinden derlenmiştir.

| Paket | Alan | Karar |
|---|---|---|
| [rulman-isi-titresim](rulman-isi-titresim/) | Fabrika | Rulman çalışmaya uygun mu: devam, izle, yağla, dur |
| [soguk-mal-kabul](soguk-mal-kabul/) | Lokanta | Gelen soğuk ürün kabul edilir mi: kabul, şartlı, kısa ömür, ret |
| [kazanim-telafi-karari](kazanim-telafi-karari/) | Okul | Ölçme sonrası sıradaki adım: ilerle, küçük grup, soruyu yenile, yeniden öğret |
| [kaldirma-siniri-niosh](kaldirma-siniri-niosh/) | İş güvenliği | Elle kaldırma: önerilen ağırlık sınırı ve kaldırma indeksi (NIOSH 94-110, kamu malı). Kılavuzun beş çözülmüş örneğiyle karşılaştırıldı |
| [isi-indeksi-nws](isi-indeksi-nws/) | İş güvenliği | Isı indeksi ve NWS sınıfı (NWS denklemi, kamu malı). NWS sayfasındaki iki örnekle karşılaştırıldı |

## Önemli uyarı

**İlk üç paket biçimi göstermek için yazıldı; son ikisi kaynaklarını `provenance/KAYNAK.md` dosyasında gösterir ama hiçbiri insan onayı taşımaz. İçlerindeki eşik değerleri örnektir ve hiçbir usta, şef ya da öğretmen tarafından onaylanmamıştır.** Onay kayıtları bunu açıkça yazar. Sıcaklık sınırları, titreşim değerleri ve başarı yüzdeleri sahada kullanılmadan önce işin sahibi tarafından kendi koşullarına göre belirlenmelidir.

Vakaların tamamı sentetiktir.

## İmza

`trust/` dizinindeki açık anahtar, bu örnekleri imzalayan gösterim anahtarına aittir. Özel anahtar depoda yoktur ve saklanmamıştır. Bir örneği değiştirirseniz imza geçersiz olur; kendi anahtarınızla yeniden imzalayın:

```bash
skillpack keygen --out ~/benim.key --trust examples/trust
skillpack sign examples/soguk-mal-kabul --key ~/benim.key
```

Kendi paketinizi yazmak için: [docs/USTADAN_PAKETE.md](../docs/USTADAN_PAKETE.md).

Teknik taslakta planlanan örnekler (depo stok sapması, ses kaydı düzeltme, koli ayırma simülasyonu) henüz yazılmadı.
