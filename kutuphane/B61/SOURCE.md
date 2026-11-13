# Source record: B61

Origin: https://github.com/giampaolo/psutil
Revision/version: `42a7b5963698393a37cbde60d5aac3c63f56bb03`
Distribution: **public-ok**
Selected source: `upstream/psutil/__init__.py` lines 1-2912.
Pinned source URL: https://raw.githubusercontent.com/giampaolo/psutil/42a7b5963698393a37cbde60d5aac3c63f56bb03/psutil/__init__.py

Calculation contract port for explicit sampled counters; not a live psutil binding. Disk denominator is total capacity, not psutil reserved-space-adjusted user percentage. No process control or performance diagnosis.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
