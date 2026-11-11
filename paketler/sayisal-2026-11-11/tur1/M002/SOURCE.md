# Source audit

Upstream: https://github.com/pbrod/numdifftools

Pinned commit: `54ba279ca9915cbd4fa07ccb2f959b82815950f1`

Observed stars: 283; repository created 2014. This is repository age, not proof of 50-year-old source code.

License: BSD-3-Clause. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2009-2026, Per A. Brodtkorb, John D'Errico

## Faithfulness and changes

Scalar-list port of fd_weights_all / _fd_weights_all, preserving the recurrence and update ordering. Only real numbers are supported; SciPy/NumPy are not runtime dependencies.

## Reference values

src/numdifftools/tests/test_fornberg.py:50-60 provides the complete five-point derivative coefficient matrix; fornberg.py:22-34 provides additional central weights.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [src/numdifftools/fornberg.py](https://github.com/pbrod/numdifftools/blob/54ba279ca9915cbd4fa07ccb2f959b82815950f1/src/numdifftools/fornberg.py) — SHA-256 `4c5852aa17c664f35c88661ed8e17395d605e05da691c1e162cd0cff419ad336` (complete original file).
- [src/numdifftools/tests/test_fornberg.py](https://github.com/pbrod/numdifftools/blob/54ba279ca9915cbd4fa07ccb2f959b82815950f1/src/numdifftools/tests/test_fornberg.py) — SHA-256 `af099b39570039e514ed3476799650de9cd3b290f4b2f78ca507808a9d5f88ca` (complete original file).
