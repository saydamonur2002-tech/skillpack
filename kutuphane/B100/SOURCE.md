# Source record: B100

Origin: https://github.com/pvlib/pvlib-python
Revision/version: `c5de586d73bbb8875a4e87468894e7b34871a575`
Distribution: **public-ok**
Selected source: `upstream/pvlib/solarposition.py` lines 1-1530.
Pinned source URL: https://raw.githubusercontent.com/pvlib/pvlib-python/c5de586d73bbb8875a4e87468894e7b34871a575/pvlib/solarposition.py

Pinned pvlib 0.16.1 SPA numpy implementation, geometric elevation and azimuth. Pressure/altitude defaults; no weather source, forecast or measured sunlight. Known-answer tolerance 0.01 degrees.

Implementation kind: runtime-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
