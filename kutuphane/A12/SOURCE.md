# Source record: A12

Origin: https://github.com/sonos/nlu-benchmark
Revision/version: `b86ac7f1577868c42158d0dec77db50956046696`
Distribution: **public-ok**
Selected source: `upstream/README.md` lines 1-23.
Pinned source URL: https://raw.githubusercontent.com/sonos/nlu-benchmark/b86ac7f1577868c42158d0dec77db50956046696/README.md

New deterministic scorer, not an intent recognizer. Labels are explicit inputs; no training or judge model. For slot scoring, serialize canonical intent+slot labels before exact-match comparison. Source fixture coverage is stated in SOURCE.md.

Implementation kind: new-data-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
