# Source audit

Upstream: https://github.com/astropy/astropy

Pinned commit: `87cc16fbf125de08066606439a5c5e471c44647b`

Observed stars: 5415; repository created 2011. This is repository age, not proof of 50-year-old source code.

License: BSD-3-Clause. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2011-2026, Astropy Developers

## Faithfulness and changes

Ports the finite one-dimensional default-M branches of biweight_location, biweight_midvariance and biweight_scale. Python scalar arithmetic replaces NumPy reductions. Undefined zero denominators are structured errors rather than non-finite results.

## Reference values

astropy/stats/tests/test_biweight.py:68-70, 251-257, plus constant-array tests; the 2.9238456 fixture is explicitly marked upstream as verified with R.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [astropy/stats/biweight.py](https://github.com/astropy/astropy/blob/87cc16fbf125de08066606439a5c5e471c44647b/astropy/stats/biweight.py) — SHA-256 `3d22a7264255bd75dff9ba1e0a84e477b7a240e9d6a5d28a68f1347dd7cad93e` (complete original file).
- [astropy/stats/tests/test_biweight.py](https://github.com/astropy/astropy/blob/87cc16fbf125de08066606439a5c5e471c44647b/astropy/stats/tests/test_biweight.py) — SHA-256 `15f642ca9b383e013c90fd6101800cd723cd6c3acf9dd2b73d6e54b78a2280ce` (complete original file).
