# Source audit

Upstream: https://github.com/chrisveness/geodesy

Pinned commit: `3e9fdd35b71dd86cee12383eccdf000ad6741e9d`

Observed stars: 1228; repository created 2014. This is repository age, not proof of 50-year-old source code.

License: MIT. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2014 Chris Veness

## Faithfulness and changes

Ports distanceTo, initialBearingTo and finalBearingTo. Haversine is clamped into [0,1] against floating-point excursions. Undefined coincident/antipodal bearings are explicitly null. The radius is in metres in this adapter.

## Reference values

test/latlon-spherical-tests.js:34-35, 138-144. The fixture rounded values have the same precision here, not invented extra digits.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [latlon-spherical.js](https://github.com/chrisveness/geodesy/blob/3e9fdd35b71dd86cee12383eccdf000ad6741e9d/latlon-spherical.js) — SHA-256 `97b8a730869bc33a0ac2b474556c89bc37c93f4fe0a3989b8a76eb06c55f6a6e` (complete original file).
- [test/latlon-spherical-tests.js](https://github.com/chrisveness/geodesy/blob/3e9fdd35b71dd86cee12383eccdf000ad6741e9d/test/latlon-spherical-tests.js) — SHA-256 `c3a38b126242202f1a8bc1a0656fd73e6ecf7e1bd2e0f0f02f353fd730c37e19` (complete original file).
