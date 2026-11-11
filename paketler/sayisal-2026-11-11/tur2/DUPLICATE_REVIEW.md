# Duplicate-technique review

Reviewed the 114-entry original catalog (including five shared runtimes) and the ten Round-1 packs. No source repository or existing pack was changed.

- pazar_repo/catalog.json: SHA-256 `8eaf48248109207f7451430c53faa2a6c838dbcbdeb69516bbff36eaedf3f229`; 114 entries.
- mined_packs_2026-11-11/catalog.json: SHA-256 `43b411c14e77615824f9851b1c6ddab2013f56b84669808df9458408220cdefa`; 10 entries.

## Scope distinctions

- M011 exposes a general bracketed polynomial-root kernel, not the existing financial cash-flow IRR workflow.
- M016 is standalone pivoted dense LU; M017 is pivoted band elimination with second-superdiagonal fill, not M001 spline internal non-pivot Thomas elimination.
- M018 is astronomical proleptic-calendar to split JD/MJD, not F4 financial day counts or holiday/business-day adjustment.
- M019 is the UT1 IAU Earth-rotation model, not solar position or a generic angular-distance rule.
- M020 is the TT IAU bias-precession model, not a generic coordinate rotation helper.
- No new spline, geodesic, robust median/biweight, Haar, centroid, finite-difference-weight or graph-Laplacian pack was created.
