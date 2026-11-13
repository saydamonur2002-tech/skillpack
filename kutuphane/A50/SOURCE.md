# Source record: A50

Origin: https://github.com/ninjasphere/go-castv2/blob/master/PacketStream.go
Revision/version: `c628dcf318eee67f396e13d6a8ec53d2925c93e3`
Distribution: **public-ok**
Selected source: `upstream/PacketStream.go` lines 1-66.
Pinned source URL: https://raw.githubusercontent.com/ninjasphere/go-castv2/c628dcf318eee67f396e13d6a8ec53d2925c93e3/PacketStream.go

One complete frame only. Protocol buffers and device control excluded. Hardened length and truncation checks.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
