# Source record: A59

Origin: https://github.com/babylonhealth/hmrb
Revision/version: `a8c5903ac0265e50ca3c4f626f1f7ef78cf07803`
Distribution: **public-ok**
Selected source: `upstream/hmrb/core.py` lines 1-258.
Pinned source URL: https://raw.githubusercontent.com/babylonhealth/hmrb/a8c5903ac0265e50ca3c4f626f1f7ef78cf07803/hmrb/core.py

Pinned hmrb 1.2.1 runtime, external span matching only. Callbacks prohibited; no clinical data or model. Python regex fallback, not adversarial-regex hardened.

Implementation kind: runtime-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
