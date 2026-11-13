# Source record: B54

Origin: https://github.com/fluttercommunity/plus_plugins/tree/main/packages/battery_plus/battery_plus
Revision/version: `907994b0e52c2c11ae2f2ccc08d0658e1c73dbaf`
Distribution: **public-ok**
Selected source: `upstream/packages/battery_plus/battery_plus/lib/battery_plus.dart` lines 1-56.
Pinned source URL: https://raw.githubusercontent.com/fluttercommunity/plus_plugins/907994b0e52c2c11ae2f2ccc08d0658e1c73dbaf/packages/battery_plus/battery_plus/lib/battery_plus.dart

New Linux sysfs implementation of the mobile API result contract. Probe reads capacity/status only. Battery health, cycle count and remaining runtime excluded. Live values vary; pure run(snapshot) is deterministic.

Implementation kind: linux-port. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
