# Source record: A16

Origin: https://github.com/RethinkRobotics/baxter_examples/blob/master/src/baxter_examples/recorder.py
Revision/version: `033756294b59f038869d97e59b5d9b28fe64d9e5`
Distribution: **public-ok**
Selected source: `upstream/src/baxter_examples/recorder.py` lines 103-145.
Pinned source URL: https://raw.githubusercontent.com/RethinkRobotics/baxter_examples/033756294b59f038869d97e59b5d9b28fe64d9e5/src/baxter_examples/recorder.py

CSV format validator for 14 joint columns plus both gripper columns; recorder and playback code are not executed. Input time units seconds, joints radians. Preserves both gripper columns and accepts joint ordering within each arm.

Implementation kind: new-format-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
