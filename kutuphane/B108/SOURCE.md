# Source record: B108

Origin: https://github.com/biolab-put/putemg_features/blob/master/features.py
Revision/version: `c2ada7c13b468771f93c0ccf96fd0091ed6eb195`
Distribution: **public-ok**
Selected source: `upstream/features.py` lines 197-297.
Pinned source URL: https://raw.githubusercontent.com/biolab-put/putemg_features/c2ada7c13b468771f93c0ccf96fd0091ed6eb195/features.py

Arithmetic from feature_rms and feature_mav only. Windowing rewritten with explicit full-window start indices (not pandas rolling index semantics). PyEEG imports and other features excluded; no NC dataset bundled.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
