# Source audit

Upstream: https://github.com/certik/fortran-utils

Pinned commit: `b43bd24cd421509a5bc6d3b9c3eeae8ce856ed88`

Observed stars: 229; repository created 2012. This is repository age, not proof of 50-year-old source code.

License: MIT. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2012 Ondřej Čertík

## Faithfulness and changes

The endpoint condition and interpolating spline are preserved. Upstream solves a banded coefficient system with LAPACK; this port solves the algebraically equivalent tridiagonal second-derivative system and a scaled four-point endpoint solve. Natural endpoints expose upstream bctype=1 with zero second derivatives. No LAPACK dependency.

## Reference values

tests/splines/test_splines.f90:15-27 (linear values and sine tolerance), and the x**2 endpoint/derivative assertions later in that file.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [src/splines.f90](https://github.com/certik/fortran-utils/blob/b43bd24cd421509a5bc6d3b9c3eeae8ce856ed88/src/splines.f90) — SHA-256 `63a2ebb10cbe8a6d382e6f7bb62e5add4207b0fb5d52706173477c6a109bcccf` (complete original file).
- [tests/splines/test_splines.f90](https://github.com/certik/fortran-utils/blob/b43bd24cd421509a5bc6d3b9c3eeae8ce856ed88/tests/splines/test_splines.f90) — SHA-256 `5d73abffc21ee712d9148543495eff354b7cbe015379583d48cbfc21cc00b96b` (complete original file).
