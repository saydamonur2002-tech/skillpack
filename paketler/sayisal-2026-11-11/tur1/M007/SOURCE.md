# Source audit

Upstream: https://github.com/astropy/astropy

Pinned commit: `87cc16fbf125de08066606439a5c5e471c44647b`

Observed stars: 5415; repository created 2011. This is repository age, not proof of 50-year-old source code.

License: BSD-3-Clause. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2011-2026, Astropy Developers

## Faithfulness and changes

Ports the finite one-dimensional default-median behavior of median_absolute_deviation and mad_std. Rejects invalid input rather than omitting it.

## Reference values

astropy/stats/tests/test_funcs.py:27-31 (389.5), 67-68 (1); funcs.py:938-940 contains the exact Gaussian scaling constant.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [astropy/stats/funcs.py](https://github.com/astropy/astropy/blob/87cc16fbf125de08066606439a5c5e471c44647b/astropy/stats/funcs.py) — SHA-256 `17b3c8b52993b0e0bd4a3e089a5931379fec2d50e2fc86eb9ef17db97e769418` (complete original file).
- [astropy/stats/tests/test_funcs.py](https://github.com/astropy/astropy/blob/87cc16fbf125de08066606439a5c5e471c44647b/astropy/stats/tests/test_funcs.py) — SHA-256 `091bcaf5774f45b3f4bb3a4ec4d3bfdcf9a45763cd22216ff57e9799572a5875` (complete original file).
