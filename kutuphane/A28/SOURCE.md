# Source record: A28

Origin: https://github.com/argoverse/av2-api/blob/main/src/av2/datasets/motion_forecasting/eval/metrics.py
Revision/version: `b7321d1f71f6ce0ecdd151f4f2b648338c191edd`
Distribution: **public-ok**
Selected source: `upstream/src/av2/datasets/motion_forecasting/eval/metrics.py` lines 1-308.
Pinned source URL: https://raw.githubusercontent.com/argoverse/av2-api/b7321d1f71f6ce0ecdd151f4f2b648338c191edd/src/av2/datasets/motion_forecasting/eval/metrics.py

Single unmasked trajectory metric only. Multiple modes, probability ranking and AV2 datasets excluded.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
