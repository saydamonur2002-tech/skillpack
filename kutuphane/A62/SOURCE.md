# Source record: A62

Origin: https://github.com/babylonhealth/simba
Revision/version: `3a133d492c903024db37ac9e1ef1ac7d5714f788`
Distribution: **public-ok**
Selected source: `upstream/simba/similarities/geometry.py` lines 6-15.
Pinned source URL: https://raw.githubusercontent.com/babylonhealth/simba/3a133d492c903024db37ac9e1ef1ac7d5714f788/simba/similarities/geometry.py

Port of avg_cosine mean-vector preprocessing only; no embeddings, Jaccard, batch search or learned model.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
