# Source record: B49

Origin: https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/converters/fromZigbee.ts
Revision/version: `f46c6d88f0eaceaf25dca7dba0dda797d2dc281e`
Distribution: **public-ok**
Selected source: `upstream/src/converters/fromZigbee.ts` lines 1-2162.
Pinned source URL: https://raw.githubusercontent.com/Koenkk/zigbee-herdsman-converters/f46c6d88f0eaceaf25dca7dba0dda797d2dc281e/src/converters/fromZigbee.ts

Port of temperature and percentage scaling only; metadata override supplied explicitly. No arbitrary device model detection, voltage estimation or Zigbee transport.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
