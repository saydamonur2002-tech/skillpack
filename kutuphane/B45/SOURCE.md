# Source record: B45

Origin: https://github.com/OHF-Voice/intents
Revision/version: `583d1bc1f39b16b2b20be39ac3b37820fc233aa5`
Distribution: **public-ok**
Selected source: `upstream/sentences/tr/HassClimateGetTemperature/default.yaml` lines 1-11.
Pinned source URL: https://raw.githubusercontent.com/OHF-Voice/intents/583d1bc1f39b16b2b20be39ac3b37820fc233aa5/sentences/tr/HassClimateGetTemperature/default.yaml

Uses upstream default read-only TR/EN sentence grammars through Hassil 3.12.1. No entity device lookup or action dispatch. Output is intent recognition only, not a fabricated temperature value.

Implementation kind: runtime-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
