# Source record: A4

Origin: https://github.com/ninjasphere/go-daikin-ac
Revision/version: `0d10d6d291ae5b701ce03b88258ea8bd23139b32`
Distribution: **public-ok**
Selected source: `upstream/baseDaikin.go` lines 1-189.
Pinned source URL: https://raw.githubusercontent.com/ninjasphere/go-daikin-ac/0d10d6d291ae5b701ce03b88258ea8bd23139b32/baseDaikin.go

SensorState.ParseWirelessValues only. Missing or invalid fields are now errors, not silent zero values. No networking or device writes.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
