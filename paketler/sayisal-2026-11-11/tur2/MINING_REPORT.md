# Mining report — Round 2

Date: 2026-11-11 (Europe/Istanbul). Ten standalone packs M011–M020. No existing repository or Round-1 pack was modified. Public GitHub search/metadata and pinned raw source were read without login or GitHub writes.

## Delivered packs

| Pack | Technique | Upstream repo | Stars observed | Created year | License | Pack tests | Status |
|---|---|---|---:|---:|---|---:|---|
| M011 | Bracketed polynomial roots with safeguarded Brent interpolation | https://github.com/scipy/scipy | 15206 | 2011 | BSD-3-Clause | 28 | PASS |
| M012 | QUADPACK 21-point Gauss–Kronrod panel and error diagnostics | https://github.com/scipy/scipy | 15206 | 2011 | BSD-3-Clause | 29 | PASS |
| M013 | Fehlberg 7(8) fixed-step affine linear ODE propagation | https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit | 214 | 2014 | BSD-3-Clause | 23 | PASS |
| M014 | Cephes regularized incomplete gamma lower and upper tails | https://github.com/scipy/scipy | 15206 | 2011 | BSD-3-Clause | 42 | PASS |
| M015 | Cephes regularized incomplete beta with symmetry and dual fractions | https://github.com/scipy/scipy | 15206 | 2011 | BSD-3-Clause | 39 | PASS |
| M016 | Unblocked partial-pivot LU factorization and dense linear solve | https://github.com/OpenMathLib/OpenBLAS | 7680 | 2011 | BSD-3-Clause | 23 | PASS |
| M017 | Linear-time partial-pivot tridiagonal system solve | https://github.com/OpenMathLib/OpenBLAS | 7680 | 2011 | BSD-3-Clause | 22 | PASS |
| M018 | Proleptic Gregorian date to two-part Julian date and MJD | https://github.com/liberfa/erfa | 181 | 2013 | BSD-3-Clause | 28 | PASS |
| M019 | IAU 2000 Earth rotation angle from split UT1 Julian date | https://github.com/liberfa/erfa | 181 | 2013 | BSD-3-Clause | 31 | PASS |
| M020 | IAU 2006 frame-bias and precession matrix from TT | https://github.com/liberfa/erfa | 181 | 2013 | BSD-3-Clause | 27 | PASS |

Star counts are an observation during this round, not a promise of current counts. Metadata uses the canonical OpenMathLib/OpenBLAS repository (the old xianyi alias redirects there). FAT and ERFA had GitHub NOASSERTION classifications; their actual complete BSD-style three-clause licenses were manually inspected instead of relying on that metadata.

## Reproducible test gate

**324 passed; 0 failed, 0 errors, 0 skipped.** 292 per-pack tests plus 32 cross-pack tests: ten real stdio MCP sessions, two watchdog/kill-reap checks, eight native-source recompilation checks and twelve release/privacy checks. The CLI tests execute real JSON subprocesses; inputs are not merely passed to imported functions.

- 76 frozen numeric reference cases; 65 were also rerun through included original C sources.
- Native checks compile exact pinned C bodies/translations into temporary libraries. Native helpers explain any scalar BLAS or libm substitutions; they never import the technique port.
- Tested with Python 3.13.5, jsonschema 4.26.0, mcp 1.30.0, pytest 9.2.0. Production numerical cores use Python standard-library math only.
- Run `python -m pytest -q` from the extracted root after installing M011/requirements-test.txt; GCC is needed for the eight optional native recompile tests. Every MCP server exposes exactly one advertised tool, validates schema/finite numbers, bounds argument JSON to 65536 UTF-8 bytes and kills/reaps a calculation after 10 seconds. CLI raw input has the same byte ceiling and a real POSIX 10-second alarm.

## Reference honesty and limits

- M011: original C Brent solver executed; upstream polynomial fixtures and additional generated C references. Endpoint statistics are made deterministic.
- M012: complete original 1980/1983 DQK21 panel logic ported, including error rescaling and roundoff floor. Published upstream sine/Bessel driver expectations plus exact analytic polynomial/exp checks. **One panel, not adaptive QUADPACK/QAGS. Original Fortran not compiled.**
- M013: complete 13-stage Fehlberg tableau and xf combination ported for bounded affine linear systems. Primary FAT test prints examples without asserted gold; numeric state references are a separately pinned SciPy analytic test model and supplemental exact solutions. **No native Fortran reference, no full adaptive controller and no global-error bound.** The source raw terr lacks h; both raw and explicitly derived h-scaled local fields are exposed rather than silently changing it.
- M014/M015: classic Cephes 1987/1995 algorithms from older SciPy pins. Published literal regressions are distinguished from generated native-C values. libm lgamma/beta normalization is a documented substitution; no claim of bit-identical complete-Cephes behavior. Legacy tails can underflow/cancel; at a=x=1000 original-C gamma P+Q differs from 1 by about -5.9e-14, retained and documented rather than normalized away.
- M016/M017: exact upstream LAPACK generated C translations executed. The available upstream random DGESV example has no fixed golden solution: generated matrices/factors are labelled generated, not attributed as upstream literal tests. Native DGETF2 factors and pivot arrays plus independent reconstruction/known-solution checks validate the dense wrapper. DGTSV supplies the complete native tridiagonal solve. Original Fortran binaries were not executed.
- M018–M020: literal original ERFA C test assertions plus complete native C pipeline reference executions. M018 rejects invalid days; M019 requires UT1, M020 requires TT. No UTC/timescale service, IERS data fetch or complete apparent-place claim.

The system had no Fortran compiler. A standard package-manager attempt failed because the package network was unavailable; no login, network bypass or unverified binary substitute was used. No complete upstream library test suite was run, and no formal certification is claimed. Repo creation year is verified, but algorithm lineage does not imply that every source line is decades old.

## Exact primary pins

- M011: https://github.com/scipy/scipy @ `92d2a8592782ee19a1161d0bf3fc2241ba78bb63`.
- M012: https://github.com/scipy/scipy @ `92d2a8592782ee19a1161d0bf3fc2241ba78bb63`.
- M013: https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit @ `3cf0a0a8ba2abf8bc4995c6da5b6abae07b45a0a`.
- M014: https://github.com/scipy/scipy @ `fcdc3d7b7c1b950d874ac3e890cccde3e2de1c6c`.
- M015: https://github.com/scipy/scipy @ `03b1092cf0e0bdebcbe98a44d289208a1e597416`.
- M016: https://github.com/OpenMathLib/OpenBLAS @ `6c303de7bc061ccec5a417e3b419a0d5551e4ff6`.
- M017: https://github.com/OpenMathLib/OpenBLAS @ `6c303de7bc061ccec5a417e3b419a0d5551e4ff6`.
- M018: https://github.com/liberfa/erfa @ `1a8044cde5b7763295d472a6443387239127c6c8`.
- M019: https://github.com/liberfa/erfa @ `1a8044cde5b7763295d472a6443387239127c6c8`.
- M020: https://github.com/liberfa/erfa @ `1a8044cde5b7763295d472a6443387239127c6c8`.

Additional test/license commits and every source-file/excerpt hash are in each manifest.json and SOURCE.md. In particular, Cephes explicit author-permitted BSD text is preserved from a separately pinned SciPy LICENSES_bundled.txt block, not incorrectly described as a file present in the historical source tag.

## Exclusions and scope choices

| Candidate / topic | Reason |
|---|---|
| mborgerding/kissfft | Repository was created in 2017, despite older algorithm/source history; fails pre-2015 repository rule. |
| FFTW/fftw3 | GPL-2.0, not permitted. |
| xiahouzuoxin/fft; alexbw/iPhoneFFT | No clear repository license; excluded. |
| attractivechaos/klib | Mandatory license copyright contains a contact string incompatible with the contact-free delivery rule; excluded rather than deleting that notice. |
| Most newer dedicated Fortran root/quadrature libraries | Repositories created in/after 2015; excluded. |
| Full FFT, QAGS and generic adaptive ODE packages | Not forced into this batch without complete faithful bounded ports and independently checked references. No FFT accuracy/coverage claim. |
| Existing catalog / Round-1 techniques | Reviewed and excluded as duplicates. See DUPLICATE_REVIEW.md for source-catalog hashes and scope distinctions. |

## Contents, legal notices and integrity

Every pack contains manifest.json, English LLM-facing SKILL.md, deterministic JSON CLI, strict input schema, pytest references/properties, one-tool FastMCP stdio server, TEACHING.md, SOURCE.md, REFERENCE_RUN.md, complete LICENSE/NOTICE, pinned upstream evidence and FILES.sha256. Native-verified packs also contain an offline rerun helper. No runtime downloaded binary, email address or project-owner identity/contact data is included. Required public upstream author/copyright attribution is retained verbatim because the licenses require it. No sharing permissions were broadened.

The archive has deterministic file order, zero timestamps and neutral uid/gid/user/group metadata. SHA256SUMS is an outer checksum list (excluded from its own archive to avoid circularity). If the archive exceeds 8 MiB it must be split; otherwise one archive is used. Hashes establish integrity, not publisher authentication. The extracted-archive gate is recorded separately in ARCHIVE_VERIFICATION.txt after extraction.
