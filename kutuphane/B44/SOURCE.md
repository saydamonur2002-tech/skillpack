# Source record: B44

Origin: https://github.com/home-assistant/core/blob/dev/homeassistant/util/unit_conversion.py
Revision/version: `d9115f3e0492aa94b06edb439ab1ebcd594b4738`
Distribution: **public-ok**
Selected source: `upstream/homeassistant/util/unit_conversion.py` lines 783-883.
Pinned source URL: https://raw.githubusercontent.com/home-assistant/core/d9115f3e0492aa94b06edb439ab1ebcd594b4738/homeassistant/util/unit_conversion.py

C/F/K only; absolute and delta distinguished, below-absolute-zero inputs additionally rejected. No whole Home Assistant runtime.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
