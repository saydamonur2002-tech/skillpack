# Source record: A64

Origin: https://github.com/google/pebble/blob/main/src/libutil/crc32.c
Revision/version: `4051c5bb97377f1215bbd26094c1a157532c55fe`
Distribution: **public-ok**
Selected source: `upstream/src/libutil/crc32.c` lines 17-51.
Pinned source URL: https://raw.githubusercontent.com/google/pebble/4051c5bb97377f1215bbd26094c1a157532c55fe/src/libutil/crc32.c

Port of reflected polynomial computation. CRC is not a signature or authentication.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
