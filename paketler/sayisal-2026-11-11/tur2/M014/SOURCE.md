# Source audit

Upstream: https://github.com/scipy/scipy

Pinned commit: `fcdc3d7b7c1b950d874ac3e890cccde3e2de1c6c`

Observed stars: 15206; repository created 2011. Repository age is not a claim that every line has the same age.

License: BSD-3-Clause, inspected in the actual selected source tree. All original text is in LICENSE, upstream/UPSTREAM_LICENSE and any LICENSES/ files.

## Original copyright

Copyright (c) 2001, 2002 Enthought, Inc.
Copyright (c) 2003-2012 SciPy Developers.
Copyright 1985, 1987 by Stephen L. Moshier
 * Copyright 1985, 1987 by Stephen L. Moshier
  Copyright 1984, 1995, 2000 by Stephen L. Moshier
Copyright (c) 2003-2016 SciPy Developers.

## Faithfulness and changes

Ports the v0.15.1 C igam.c algorithm (source identifies Cephes April 1987), including branch selection, MAXLOG guard, fraction renormalization by 2^52 and series convergence at MACHEP=2^-53. Python math.lgamma substitutes for the separate Cephes lgam implementation; iteration caps are explicit new safety bounds. The old source carries its original copyright but only a platform include and algorithm body are redistributed as compilable evidence; a nonlegal postal-contact line is omitted. Full SciPy BSD text and the separately pinned explicit Cephes BSD author-permission block are preserved. No claim of bit-identical full-Cephes behavior.

## Reference values

Native reference values were produced by the pinned original C body with the documented libm-lgamma/platform shim. Independent published literal anchors are from later v0.19.1 test_basic.py (including P(10,.05)=2.5715803516000736e-20); the distinct source/test/license commits are explicitly recorded. The inverse fixture P(50,11) is honestly labelled a derived forward check.

Frozen references are in tests/references.json. Origins distinguish literal upstream fixtures, native-generated differential values, cross-library analytic formulas and supplementary mathematical properties. No unsupported digit guarantee or full-upstream-suite claim is made.

## Evidence and exact source pins

- [scipy/special/cephes/igam.c](https://github.com/scipy/scipy/blob/fcdc3d7b7c1b950d874ac3e890cccde3e2de1c6c/scipy/special/cephes/igam.c) — original LF lines 86-EOF; delivered SHA-256 `2e38666d72c04cdc34013cff944d7a6a4ace8cce657df3ef16f9b74e368878b5`; full original SHA-256 `f756039d2d968694eb34a11a7634967919a64e13264f97a234b968a4c83d8515`.
- [scipy/special/cephes/igam.c](https://github.com/scipy/scipy/blob/fcdc3d7b7c1b950d874ac3e890cccde3e2de1c6c/scipy/special/cephes/igam.c) — original LF lines 1-82; delivered SHA-256 `ff966978c03d4e434f783c1b24404a1627d93d011db7534254c8ebf737059f22`; full original SHA-256 `f756039d2d968694eb34a11a7634967919a64e13264f97a234b968a4c83d8515`.
- [scipy/special/tests/test_basic.py](https://github.com/scipy/scipy/blob/03b1092cf0e0bdebcbe98a44d289208a1e597416/scipy/special/tests/test_basic.py) — original LF lines 1850-1895; delivered SHA-256 `a24e29e48239bbaaaf7c622a9d130b3933127a94a95355696aa0041b60e67fd3`; full original SHA-256 `299245f565438e2de3860b54109c17224f18d9582c07c82cfbc82cf19c78f084`.
- [LICENSES_bundled.txt](https://github.com/scipy/scipy/blob/92d2a8592782ee19a1161d0bf3fc2241ba78bb63/LICENSES_bundled.txt) — original LF lines 94-128; delivered SHA-256 `c3255036952d180c1e855cb2e50be8c2c528db580a9632a070820887a7997e2a`; full original SHA-256 `2ef7ab02d0a5f17837658d11761ef9892c38276714bed3338ed145bd2cf9865b`.

## Additional license provenance

[
  {
    "path": "LICENSES/CEPHES_BSD_PERMISSION.txt",
    "upstream_url": "https://github.com/scipy/scipy/blob/92d2a8592782ee19a1161d0bf3fc2241ba78bb63/LICENSES_bundled.txt",
    "commit": "92d2a8592782ee19a1161d0bf3fc2241ba78bb63",
    "scope": "original LF lines 94-128",
    "sha256": "c3255036952d180c1e855cb2e50be8c2c528db580a9632a070820887a7997e2a"
  },
  {
    "path": "LICENSES/SCIPY_VALIDATION_LICENSE",
    "upstream_url": "https://github.com/scipy/scipy/blob/03b1092cf0e0bdebcbe98a44d289208a1e597416/LICENSE.txt",
    "commit": "03b1092cf0e0bdebcbe98a44d289208a1e597416",
    "scope": "original LF lines 1-EOF",
    "sha256": "142b6deb0132be1adba8d9ba9f9027629f5a9573be3a829ed8a53733473ae0a1"
  }
]

## Observed legacy partition discrepancy

At a=x=1000 the native original-C/shim P and Q sum differs from 1 by about -5.9e-14 because both branches are evaluated independently. The supplementary partition tolerance is 3e-12, consistent with the declared differential tolerance, rather than silently renormalizing the algorithm to force an identity. This is not a blanket relative-error guarantee for extreme tails.
