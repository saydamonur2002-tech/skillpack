# skillpack-orchestrator — Paket iskeleti, doğrulama, deterministik ZIP

## Ne işe yarar?
`manifest.json` + `scripts/main.py` biçimindeki paketler için üç komut verir: `scaffold` (iskelet), `validate` (temel denetim), `zip` (aynı girdiden aynı baytlı ZIP). Stdin'e `{"command": "help"}` gibi JSON verilir.

## Sınırlar
`validate` kontrol listesinin yalnız bir alt kümesini uygular (`references/controls.md`). SKILL.md'deki Grok/Google Drive aktarım akışı bu depoda uygulanmış değildir; yalnız belgedir. Bu araç ana deponun imzalı `skillpack.yaml` doğrulamasının yerine geçmez.

## Lisans
Apache-2.0.
