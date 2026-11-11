# Source audit

Upstream: https://github.com/liberfa/erfa

Pinned commit: `1a8044cde5b7763295d472a6443387239127c6c8`

Observed stars: 181; repository created 2013. Repository age is not a claim that every line has the same age.

License: BSD-3-Clause, inspected in the actual selected source tree. All original text is in LICENSE, upstream/UPSTREAM_LICENSE and any LICENSES/ files.

## Original copyright

Copyright (C) 2013-2021, NumFOCUS Foundation.
**  Copyright (C) 2013-2023, NumFOCUS Foundation.

## Faithfulness and changes

Ports eraEra00 with ordering of the two date parts, t=d1+(d2-J2000), fractional parts using C-style fmod, the exact IAU constants and eraAnp normalization. Degrees are a derived convenience output. This is a separate Earth-rotation primitive, not a generic 3D rotation pack and not the earlier solar-position algorithm. Full ERFA source notices remain intact.

## Reference values

The literal t_era00 fixture is (2400000.5,54388.0) -> 0.4022837240028158102 radians, tolerance 1e-12. Additional split, reversed-part and negative-offset references were generated with the exact pinned original C functions.

Frozen references are in tests/references.json. Origins distinguish literal upstream fixtures, native-generated differential values, cross-library analytic formulas and supplementary mathematical properties. No unsupported digit guarantee or full-upstream-suite claim is made.

## Evidence and exact source pins

- [src/era00.c](https://github.com/liberfa/erfa/blob/1a8044cde5b7763295d472a6443387239127c6c8/src/era00.c) — original LF lines 1-EOF; delivered SHA-256 `91c092c322d070305ba02873005bcb03110d7c26674fbdc7105477c50543ffb5`; full original SHA-256 `91c092c322d070305ba02873005bcb03110d7c26674fbdc7105477c50543ffb5`.
- [src/anp.c](https://github.com/liberfa/erfa/blob/1a8044cde5b7763295d472a6443387239127c6c8/src/anp.c) — original LF lines 1-EOF; delivered SHA-256 `41f132914547ce4137edf024bc809fd7dfed3e0f5ff5b38f22313c884e8978e3`; full original SHA-256 `41f132914547ce4137edf024bc809fd7dfed3e0f5ff5b38f22313c884e8978e3`.
- [src/t_erfa_c.c](https://github.com/liberfa/erfa/blob/1a8044cde5b7763295d472a6443387239127c6c8/src/t_erfa_c.c) — original LF lines 3613-3636; delivered SHA-256 `bde4352a823f8ed4cc16c1c69485f82ede42a2de6182ba197d933210603793f3`; full original SHA-256 `8a92d0099c48df31ca566bea881c19497dc295dba58dba7136cc2f8443c31f15`.

## Additional license provenance

[]

Native compile header: [erfa.h](https://github.com/liberfa/erfa/blob/1a8044cde5b7763295d472a6443387239127c6c8/src/erfa.h) — complete original file, SHA-256 `9549553b95ca2fbbcdcabcc69d82fb3cdd376c28b03c2793200138ff55727088`.

Native compile header: [erfam.h](https://github.com/liberfa/erfa/blob/1a8044cde5b7763295d472a6443387239127c6c8/src/erfam.h) — complete original file, SHA-256 `0da6313033aacf9c64533a7e74be49ecda97b4aaa87e134f98287e4ff279886f`.
