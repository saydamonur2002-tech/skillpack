# Source record: A57

Origin: https://github.com/ros-perception/laser_geometry
Revision/version: `47954dc5454a443b5b0a5ea5bd23315f1bc505ab`
Distribution: **public-ok**
Selected source: `upstream/src/laser_geometry.cpp` lines 1-413.
Pinned source URL: https://raw.githubusercontent.com/ros-perception/laser_geometry/47954dc5454a443b5b0a5ea5bd23315f1bc505ab/src/laser_geometry.cpp

Range maximum is exclusive to match selected implementation. Null explicitly marks unavailable readings; JSON NaN/Inf rejected. No transforms, network or live scan.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
