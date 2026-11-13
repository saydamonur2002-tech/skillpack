# Source record: A61

Origin: https://github.com/babylonhealth/corrsim
Revision/version: `1d172055d0009d0f4f0c5ad7d6a3d1045da01889`
Distribution: **public-ok**
Selected source: `upstream/similarity/correlation.py` lines 20-97.
Pinned source URL: https://raw.githubusercontent.com/babylonhealth/corrsim/1d172055d0009d0f4f0c5ad7d6a3d1045da01889/similarity/correlation.py

Preserves upstream mean-over-word-vectors preprocessing, not plain arbitrary flattened-vector correlation. No embeddings supplied. Constant vectors explicitly rejected.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
