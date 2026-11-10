---
name: depo-koli-ayirma
description: Depoda karışık gelen kolileri etikete, ağırlığa ve hedef rampaya göre sınıflandırır; robot hücresi varsa ayırma sırasını önerir. Koli ayırma, rampa atama veya hatalı etiket tespiti istendiğinde kullan.
license: Apache-2.0
compatibility: Yerel sunucu; MCP WMS salt-okur bağlayıcı; isteğe bağlı ROS 2
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
allowed-tools: Read mcp__wms__stok_oku mcp__wms__siparis_oku
---
# Depo koli ayırma
1. Koli etiketini oku; barkod geçersizse insana devret.
2. references/kurallar.yaml içindeki rampa kurallarını sırayla uygula.
3. Çıktı: tanı kartı (koli, önerilen rampa, gerekçe, güven). Eylemi operatör onaylar.
