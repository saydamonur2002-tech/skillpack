# Source audit

Upstream: https://github.com/chrisveness/geodesy

Pinned commit: `3e9fdd35b71dd86cee12383eccdf000ad6741e9d`

Observed stars: 1228; repository created 2014. This is repository age, not proof of 50-year-old source code.

License: MIT. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2014 Chris Veness

## Faithfulness and changes

Port of inverse() and the upstream public distance/bearing rounding, including the equatorial and exactly antipodal branches and 1000-iteration guard. Non-convergence becomes an error instead of upstream public-method NaN. Undefined coincident bearings become null.

## Reference values

test/latlon-ellipsoidal-vincenty-tests.js:22-24, 65-71, 92-100, 103-122, 127-142.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [latlon-ellipsoidal-vincenty.js](https://github.com/chrisveness/geodesy/blob/3e9fdd35b71dd86cee12383eccdf000ad6741e9d/latlon-ellipsoidal-vincenty.js) — SHA-256 `c2cb115d2ce6076de144d4592ff85e01d842b37e4b9e893a279579e8b25e8cf8` (complete original file).
- [latlon-ellipsoidal.js](https://github.com/chrisveness/geodesy/blob/3e9fdd35b71dd86cee12383eccdf000ad6741e9d/latlon-ellipsoidal.js) — SHA-256 `cc6570213065b7f82e3b04e70df278df5c18e43f9ccb86928e62aa109f42aabd` (complete original file).
- [test/latlon-ellipsoidal-vincenty-tests.js](https://github.com/chrisveness/geodesy/blob/3e9fdd35b71dd86cee12383eccdf000ad6741e9d/test/latlon-ellipsoidal-vincenty-tests.js) — SHA-256 `b9e7163e016ca586e1d46b5fc266651a669862c36891e8b9c38aca053850918e` (complete original file).

Adapter hardening: longitude difference is normalized to [-180,180), and physically coincident poles / equivalent antimeridian representations are detected before iteration. This deliberately avoids representation-sensitive degeneracies rather than reproducing them.
