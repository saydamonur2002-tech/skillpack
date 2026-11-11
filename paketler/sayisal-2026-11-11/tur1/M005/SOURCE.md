# Source audit

Upstream: https://github.com/chrisveness/geodesy

Pinned commit: `3e9fdd35b71dd86cee12383eccdf000ad6741e9d`

Observed stars: 1228; repository created 2014. This is repository age, not proof of 50-year-old source code.

License: MIT. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2014 Chris Veness

## Faithfulness and changes

Ports rhumbDistanceTo and rhumbBearingTo with the exact upstream 10e-12 Mercator tolerance. Poles are explicitly rejected rather than relying on non-finite logarithms. Coincident NaN bearing becomes null.

## Reference values

test/latlon-spherical-tests.js:44-45 and 279-290. Distance fixtures are rounded metres; the bearing fixture is rounded to 0.1 degree.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [latlon-spherical.js](https://github.com/chrisveness/geodesy/blob/3e9fdd35b71dd86cee12383eccdf000ad6741e9d/latlon-spherical.js) — SHA-256 `97b8a730869bc33a0ac2b474556c89bc37c93f4fe0a3989b8a76eb06c55f6a6e` (complete original file).
- [test/latlon-spherical-tests.js](https://github.com/chrisveness/geodesy/blob/3e9fdd35b71dd86cee12383eccdf000ad6741e9d/test/latlon-spherical-tests.js) — SHA-256 `c3a38b126242202f1a8bc1a0656fd73e6ecf7e1bd2e0f0f02f353fd730c37e19` (complete original file).
