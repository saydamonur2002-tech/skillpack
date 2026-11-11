# Source audit

Upstream: https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit

Pinned commit: `3cf0a0a8ba2abf8bc4995c6da5b6abae07b45a0a`

Observed stars: 214; repository created 2014. Repository age is not a claim that every line has the same age.

License: BSD-3-Clause, inspected in the actual selected source tree. All original text is in LICENSE, upstream/UPSTREAM_LICENSE and any LICENSES/ files.

## Original copyright

Copyright (c) 2014-2025, Jacob Williams
Copyright (c) 2001-2002 Enthought, Inc. 2003-2024, SciPy Developers.

## Faithfulness and changes

Preserves all 13 stages and the exact upstream xf weights; returns last_error_indicator=(41/840)*(f0+f10-f11-f12) exactly as the Fortran routine does, WITHOUT h. last_local_error_estimate=h*last_error_indicator is an explicitly derived adapter field, not an upstream output and not a global error bound. Adds a fixed-step loop and limits the callback to matrix*y+bias. The source cites Fehlberg NASA 1968; this is a modern Fortran implementation of that classic formula, not a claim that the repository contains 1968 source. No Fortran compiler was available, so the original Fortran binary was not executed.

## Reference values

Primary upstream embedded test prints orbital examples but supplies no asserted golden trajectory. State fixtures instead come from the explicitly pinned BSD SciPy test_ivp.py fun_linear/sol_linear analytic solution, a different upstream validation source. Scalar exponential, zero and constant-derivative cases are supplementary analytic checks. Neither RKF78 raw terr nor a full adaptive controller has an independent native-Fortran reference here.

Frozen references are in tests/references.json. Origins distinguish literal upstream fixtures, native-generated differential values, cross-library analytic formulas and supplementary mathematical properties. No unsupported digit guarantee or full-upstream-suite claim is made.

## Evidence and exact source pins

- [src/rk_module_variable_step.f90](https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit/blob/3cf0a0a8ba2abf8bc4995c6da5b6abae07b45a0a/src/rk_module_variable_step.f90) — original LF lines 819-944; delivered SHA-256 `f718702f7c1a61dc7ffc0f23295df88ac4c8b50a6c342350cc34d541ec015726`; full original SHA-256 `f79e6214802e9b060fef03403301042dc15a5bf871171e963d68ef111161c26d`.
- [scipy/integrate/_ivp/tests/test_ivp.py](https://github.com/scipy/scipy/blob/92d2a8592782ee19a1161d0bf3fc2241ba78bb63/scipy/integrate/_ivp/tests/test_ivp.py) — original LF lines 15-29; delivered SHA-256 `64e40bb533c64a6fbb8eb83078c38592cf684c806ba5ca3d26b18a01b1558dec`; full original SHA-256 `d3ab40163ba28225bc29d0a689496c217d8ffc5cf71079a208b0361484e5ce30`.

## Additional license provenance

[
  {
    "path": "LICENSES/SCIPY_VALIDATION_LICENSE",
    "upstream_url": "https://github.com/scipy/scipy/blob/92d2a8592782ee19a1161d0bf3fc2241ba78bb63/LICENSE.txt",
    "commit": "92d2a8592782ee19a1161d0bf3fc2241ba78bb63",
    "scope": "original LF lines 1-EOF",
    "sha256": "c29fb8e5936f33237a8b15256b4c6e93037f05bbf58c3d7b5755aede4c200173"
  }
]
