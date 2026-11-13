# Source record: A6

Origin: https://github.com/MycroftAI/adapt
Revision/version: `06b98f8d5e525601a763103ad572b8ae615655a5`
Distribution: **public-ok**
Selected source: `upstream/adapt/intent.py` lines 1-305.
Pinned source URL: https://raw.githubusercontent.com/MycroftAI/adapt/06b98f8d5e525601a763103ad572b8ae615655a5/adapt/intent.py

Uses pinned adapt-parser 1.0.0 runtime. Fixed input vocabulary, no regex registrations, no actions. Confidence is upstream scoring, not a calibrated probability.

Implementation kind: runtime-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
