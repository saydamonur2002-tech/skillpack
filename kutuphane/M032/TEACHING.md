# Learning path: Offline place search (geocode) and reverse geocode on a local places file

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Turkish folding
Normalise "GÜL ECZANESİ" by hand and confirm it equals the stored name after folding.

## 2. Jaro-Winkler
Compute JW("cinar kafe", "cinar kafe") and JW("eczane", "merkez eczanesi"); explain the prefix bonus.

## 3. Word windows
Show why "eczane" still finds "Şifa Eczanesi" with min_score 0.7.

## 4. Ambiguity
Use the two "Merkez Eczanesi" records and a near point to decide which one the user meant.

## Human check

Run `python tool/main.py < example.json` with `SKILLPACK_MAP_DATA=tests/fixtures` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
