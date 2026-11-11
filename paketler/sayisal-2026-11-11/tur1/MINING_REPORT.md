# Mining report — tested standalone release

Completed: 2026-11-11 20:26 Europe/Istanbul (UTC+3).

**10 completed packs; 261 tests passed; zero failures, errors or skips.** The previous research-only delivery is superseded by `mined-packs-2026-11-11.tar.gz`.

## Selection and provenance

Seven distinct public GitHub repositories supplied ten deliberately bounded techniques. Every selected repository has at least 100 stars in the read-only search snapshot and was created before 2015. The root license texts and relevant file headers were inspected, original copyright lines retained, and exact upstream commits pinned. MIT/BSD-3-Clause only. Source evidence and SHA-256 hashes are present in each pack.

| Pack id | Technique | Upstream repository | Stars | Created year | License | Tests incl. real MCP | Status |
|---|---|---|---:|---:|---|---:|---|
| M001 | Consistent-end cubic spline and derivatives | https://github.com/certik/fortran-utils | 229 | 2012 | MIT | 23 | tested |
| M002 | Fornberg arbitrary-grid finite-difference weights | https://github.com/pbrod/numdifftools | 283 | 2014 | BSD-3-Clause | 28 | tested |
| M003 | WGS84 Vincenty inverse geodesic | https://github.com/chrisveness/geodesy | 1228 | 2014 | MIT | 40 | tested |
| M004 | Spherical great-circle distance and bearings | https://github.com/chrisveness/geodesy | 1228 | 2014 | MIT | 22 | tested |
| M005 | Mercator rhumb-line distance and constant bearing | https://github.com/chrisveness/geodesy | 1228 | 2014 | MIT | 24 | tested |
| M006 | Robust biweight location, midvariance and scale | https://github.com/astropy/astropy | 5415 | 2011 | BSD-3-Clause | 22 | tested |
| M007 | Median absolute deviation and Gaussian scale | https://github.com/astropy/astropy | 5415 | 2011 | BSD-3-Clause | 21 | tested |
| M008 | One-level orthonormal Haar analysis and reconstruction | https://github.com/PyWavelets/pywt | 2413 | 2013 | MIT | 20 | tested |
| M009 | Masked image center of mass | https://github.com/astropy/photutils | 316 | 2011 | BSD-3-Clause | 35 | tested |
| M010 | Weighted graph combinatorial and normalized Laplacians | https://github.com/epfl-lts2/pygsp | 551 | 2014 | BSD-3-Clause | 24 | tested |

The table accounts for 259 pack-associated tests. Two additional shared tests exercise the real ten-second CLI watchdog and the MCP timeout kill/reap branch, making **261 total**. The latter uses a shortened test-only wait to exercise cleanup, while asserting that production requested a 10-second timeout.

## What each pack contains

- `manifest.json`, strict input schema and provenance; English `SKILL.md` and `TEACHING.md`.
- Standard-library numerical Python core, deterministic JSON CLI, `example.json`, tests and source-derived reference fixtures.
- Official FastMCP server over stdio with exactly one tool, no HTTP listener, a 65536-byte argument/input ceiling, schema/type/nonfinite checks, and a ten-second child-process kill deadline.
- Original `LICENSE`, `NOTICE`, pinned `SOURCE.md`, preserved upstream evidence, and file checksums.
- Exact top-level runtime dependency versions. Numerical code requires no NumPy/SciPy or external executables. Installation needs the stated Python packages; the calculation itself does not access the network.

## Tests and reference honesty

`TEST_RESULTS.xml` records the passing suite. Tests cover original or explicitly adapted upstream numerical fixtures, additional mathematical properties, degenerate inputs, strict validation, repeatability, UTF-8 byte bounds, malformed/duplicate/nonfinite JSON, and real MCP initialization/list/call/error exchanges for all ten servers.

Expected numbers are not fabricated. Original reference files are included and `tests/references.json` states each fixture's origin and tolerance. Important adaptations:
- Haar fixtures take the real components of explicit upstream complex partial-reconstruction arrays, using the real-linear filter; this is stated, not passed off as an unchanged upstream real fixture.
- Photutils fixtures reproduce its analytic sampled Gaussian, dimensions, parameters, mask and expected center/tolerance without importing Astropy at runtime.
- Spline tests reuse the upstream linear values, sine tolerance and polynomial value/derivative assertions. The port uses an equivalent second-derivative system rather than upstream LAPACK storage.
- Extra analytic/property tests are supplementary evidence, not invented upstream fixture values.

The full original library suites, compiled Fortran code and independent scientific certification were not run. Passing this bounded test suite is not proof of every upstream feature or all numerical edge cases.

## Scope and intentional differences

M001 has consistent or zero-second-derivative natural endpoints, not smoothing. M002 computes weights, not adaptive differentiation or a certified error bound. M003 is WGS84 surface-only and can fail near antipodes; non-convergence is an error, undefined bearings are null, and physically equivalent coordinate representations are normalized. M004 and M005 are explicitly spherical models, not ellipsoidal navigation substitutes. M006/M007 are finite one-dimensional robust estimators without automatic missing-data handling. M008 is even-length, one-level real Haar only. M009 uses supplied intensities and mask, not background estimation or source fitting. M010 averages directed adjacency, deliberately losing direction. Undefined nonfinite results become structured errors or documented nulls.

## Duplicate screening

Compared proposed techniques with the existing 114-entry catalog (including five shared runtimes). Existing temperature, CRC, RMS/MAV, angular difference, solar position, geometry-transform, financial and industrial-decision packs were not duplicated. M003/M004/M005 are intentionally distinct geodesic models: ellipsoidal shortest surface path, spherical great circle, and spherical constant-bearing loxodrome. MAD is also usable independently of the biweight estimator that internally employs it.

## Deferred candidates

- `clawpack/pyclaw`: selected limiter-file attribution contains email addresses; skipped rather than remove required notices or place addresses in this batch.
- `wavebitscientific/datetime-fortran`: calendar subset was too small and close to existing calendar/day-count coverage to justify a pack in this quality-focused batch.
- `lvandeve/jmat`: deferred complex/special-function work rather than claim a hurried high-precision port.
- `jleinonen/pytmatrix`, `timduly4/pyglow`: larger scientific models and embedded-code provenance require additional audit; not packaged.
- `nigma/pywt`: migrated repository; used maintained `PyWavelets/pywt` instead.
- `astropy/astroquery`: remote-data-access focus, unsuitable for the requested offline deterministic calculator.

No GPL/LGPL/AGPL or unclear-license source was incorporated. Repository creation date is not a claim that these source files are 50 years old; the durable techniques and their modern mirrors have separate ages. Original upstream legal attributions remain intact; no private project-owner identity details or email addresses were inserted. Documentation and adaptation were AI-generated; project concept and direction belong to the project designer. No upstream endorsement is implied.

## Delivery and safety

The archive is below 8 MB, so splitting is unnecessary. `SHA256SUMS` verifies the archive and report, while per-pack `FILES.sha256` verifies the contents. No existing user repository was modified, cloned or pushed. No forks, stars, issues, account login or credential access occurred. The earlier research-only archive is obsolete, not the installable release; it is retained as historical context rather than silently deleted.
