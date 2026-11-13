# chain-runner — Paketleri art arda çalıştırma

## Ne işe yarar?
Sıralı bir paket listesini (a→b→c) çalıştırır; her paketin çıktısı bir sonrakinin girdisi olur. Her adımın girdi/çıktısı `trace` içinde döner.

## Önemli
Paketleri `SKILLPACK_PACKS_DIR` klasöründe (varsayılan `/workspace/skillpacks`) ad.zip ya da açık klasör olarak arar. Bu paket `scripts/main.py` + stdin JSON sözleşmesi olan paketlerle çalışır; `skillpack.yaml` akış paketlerini çalıştırmaz.

Yol ayarı bu depoya taşınırken eklendi (özgün sürümde yol sabitti). Güvenlik notu: paketin `main.py` dosyasını çalıştırır, yani yalnız güvendiğin paketleri zincire koy.

## Lisans
Apache-2.0.
