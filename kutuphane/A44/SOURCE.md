# Source record: A44

Origin: https://github.com/MycroftAI/lingua-franca
Revision/version: `5bfd75fe5996fd364102a0eec3f714c9ddc9275c`
Distribution: **public-ok**
Selected source: `upstream/lingua_franca/lang/parse_en.py` lines 1-1496.
Pinned source URL: https://raw.githubusercontent.com/MycroftAI/lingua-franca/5bfd75fe5996fd364102a0eec3f714c9ddc9275c/lingua_franca/lang/parse_en.py

English only. Pinned lingua-franca 0.4.3 runtime; no time-of-day, date, wall clock or locale inference.

Implementation kind: runtime-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
