# docs/deney/

[ALTYAPI_ENVANTERI.md](../ALTYAPI_ENVANTERI.md) içindeki ilk denemenin betikleri ve örnek paketi. Bunlar ölçüm betikleridir; referans uygulama (`cli/`) değildir.

- `depo-koli-ayirma/` — taslak Bölüm 4.3'teki örneğin küçültülmüş hâli. Yalnız sentetik veri içerir. `skillpack.yaml` taslak alanların küçük bir alt kümesidir; şema henüz yok.
- `beceri_olcumu.py` — aynı görevi becerisiz ve beceriyle küçük yerel modelde çalıştırır, doğruluğu deterministik referansla karşılaştırır.
- `iptal_tatbikati.py` — yerel bir TUF deposunda iptal listesi yayımlar; imzasız değişiklik, geri sarma ve dondurma saldırılarını dener.
- `ince_ayar.py` — betiğin etiketlediği sentetik kolilerle küçük modele LoRA ince ayarı yapar; öncesini ve sonrasını ölçer. Ek gereksinim: `torch`, `transformers`, `peft`.

```sh
pip install skills-ref "tuf>=7" "securesystemslib[crypto]" llama-cpp-python
agentskills validate depo-koli-ayirma
python iptal_tatbikati.py
python beceri_olcumu.py <model.gguf> 20
```

Model dosyası depoya konmaz. Denemede Qwen2.5 1.5B ve 7B Instruct (GGUF, Q4_K_M) kullanıldı.
