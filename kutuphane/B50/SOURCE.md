# Source record: B50

Origin: https://github.com/zigpy/zha-device-handlers/blob/master/zhaquirks/xiaomi/__init__.py
Revision/version: `b07fa76876e081d48744968f9fb806e7f1fee0ee`
Distribution: **public-ok**
Selected source: `upstream/zhaquirks/xiaomi/__init__.py` lines 654-754.
Pinned source URL: https://raw.githubusercontent.com/zigpy/zha-device-handlers/b07fa76876e081d48744968f9fb806e7f1fee0ee/zhaquirks/xiaomi/__init__.py

Range rule of selected Xiaomi TemperatureMeasurementCluster only. Declared family gate is not automatic model identification.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
