# Skillpack System Standard

Source document: SKILLPACK_SISTEMI.md (13 Kasım 2026, taslak).

## One-sentence definition

Format and production method that turns single functions from open-source projects into small, offline, tested "skill" packages with recorded source and license, and enables reliable connection between them.

Platform değil; format + doğrulama yöntemi + örnek paketler.

## Package structure

```
<beceri-adi>/
  SKILL.md          # kullanım kılavuzu + YAML frontmatter (name, description)
  manifest.json     # künye: kaynak, commit, SHA, lisans, truth_level, izinler
  scripts/main.py   # ince betik: kurulu kütüphanedeki TEK işlevi çağırır
  tests/            # testler + vektör kökenleri yazılı
  references/       # kaynak dosya kopyası (kanıt) + TAM lisans metni
  schema/           # (önerilen) girdi/çıktı JSON şemaları
```

## Call contract

stdin: `{"input": ...}`  
stdout: `{"result": ...}`  
Error: JSON object + non-zero exit code.

No network required at runtime. Library must be installed (pinned version).

## Truth levels

| Level | Meaning |
|---|---|
| `bagimsiz` | Results compared against independent oracle (standard test vectors or another library) |
| `kismi` | Independent comparison exists but narrow scope |
| `sozlesme` | Only own tests |

Self-testing against own library is NOT `bagimsiz`.

## Control pipeline (draft v0.1.1)

States: PASS · FAIL · UNAVAILABLE · SKIP

| # | Control |
|---|---|
| C01 | Agent Skills format validation |
| C02 | Source reality (SHA / PyPI match) |
| C03 | License reality (full text, SPDX) |
| C04 | Functional tests (network off) |
| C05 | Vector origins documented |
| C06 | Independent comparison |
| C07 | Quality (Ruff, version-pinned rules; do not touch source copy) |
| C08 | Deterministic zip |
| C09 | Network-free execution |
| C10 | Personal trace scan |
| C11 | Environment record |

Second-environment rule: re-run UNAVAILABLE controls elsewhere; package hash must match.

## Roles

- Production: strong model once
- Independent verification: separate environment + tools
- Runtime: small model or pure script
- Approval: human/institution only

## What it is not

- Not a platform or marketplace
- Not an approval body
- Not a way to make the model "smarter"; it removes precise work from the model and gives it to code
- Not a proven standard yet

See original document for measured results, risks, and next steps.
