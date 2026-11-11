# Source audit

Upstream: https://github.com/scipy/scipy

Pinned commit: `92d2a8592782ee19a1161d0bf3fc2241ba78bb63`

Observed stars: 15206; repository created 2011. Repository age is not a claim that every line has the same age.

License: BSD-3-Clause, inspected in the actual selected source tree. All original text is in LICENSE, upstream/UPSTREAM_LICENSE and any LICENSES/ files.

## Original copyright

Copyright (c) 2001-2002 Enthought, Inc. 2003-2024, SciPy Developers.

## Faithfulness and changes

Faithful double-precision DQK21 abscissae and weights, even/odd node evaluation order, Gauss comparison, absolute integral, mean-deviation integral, resasc-based error rescaling and 50*machine-epsilon roundoff floor. The upstream prologue dates the Fortran routine to 1980 with a 1983 revision. Only a safe finite set of integrands replaces Fortran callbacks; this does not port the full adaptive QUADPACK driver. Original Fortran was not compiled in this environment.

## Reference values

The upstream quadpack test asserts sin integral=2 and the n=2,z=1.8 Bessel integral=0.30614353532540296487. Those are driver-level published fixtures, applied here to a smooth single panel with declared tolerances. Supplemental polynomial expectations are analytically integrated, not upstream literal gold.

Frozen references are in tests/references.json. Origins distinguish literal upstream fixtures, native-generated differential values, cross-library analytic formulas and supplementary mathematical properties. No unsupported digit guarantee or full-upstream-suite claim is made.

## Evidence and exact source pins

- [scipy/integrate/quadpack/dqk21.f](https://github.com/scipy/scipy/blob/92d2a8592782ee19a1161d0bf3fc2241ba78bb63/scipy/integrate/quadpack/dqk21.f) — original LF lines 1-EOF; delivered SHA-256 `7ffccab6a409c1c01c2ad651279e46097242a4ba8ef0f1d6c77a06a597e292fd`; full original SHA-256 `7ffccab6a409c1c01c2ad651279e46097242a4ba8ef0f1d6c77a06a597e292fd`.
- [scipy/integrate/tests/test_quadpack.py](https://github.com/scipy/scipy/blob/92d2a8592782ee19a1161d0bf3fc2241ba78bb63/scipy/integrate/tests/test_quadpack.py) — original LF lines 85-140; delivered SHA-256 `0867a4478e6176f4a0e9790b731cd092049db7cf5ebe12117d23388ac15eec45`; full original SHA-256 `0849d806a78030ec60222d990cc66ce713b24ba4997cf9543f305934595a44ee`.

## Additional license provenance

[]
