---
name: koli-ayirma
description: Simülasyonda koliyi boyuta ve etiket sınıfına göre rampa önerir.
  Gerçek robot hareketi başlatmaz; hareket önerisi insan onayına kalır.
  Koli ayırma veya rampa önerisi istendiğinde kullan.
license: CC-BY-4.0
compatibility: Simülasyon yalnız. Birincil model alt sınırı 32B. MCP ve ROS çağrısı yok.
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
  skillpack-min-model-size: "32B"
---

# Koli ayırma

Bu metin bir taslaktır. Çalışan bir ayırıcı yoktur.

1. Koli boyutunu ve etiket sınıfını oku. Etiket yoksa veya okunamazsa insan kapısına yaz.
2. `references/kurallar.yaml` içindeki sırayı uygula. Çıktı bir öneridir: rampa, gerekçe, güven.
3. Gerçek hareket önerme. `mode` simülasyondur. Fiziksel komut ancak insan onayından sonra açılır; bu iskelet o kapıyı açmaz.
