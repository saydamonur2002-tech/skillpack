# Source record: A15

Origin: https://github.com/RethinkRobotics/baxter_interface/blob/master/src/baxter_interface/robot_enable.py
Revision/version: `aea70d96eb0fb0a99084dcb02d467785dde8fe52`
Distribution: **public-ok**
Selected source: `upstream/src/baxter_interface/settings.py` lines 1-41.
Pinned source URL: https://raw.githubusercontent.com/RethinkRobotics/baxter_interface/aea70d96eb0fb0a99084dcb02d467785dde8fe52/src/baxter_interface/settings.py

Historical settings.py mapping only; does not allow enabling or moving hardware. Version strings must match exactly.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
