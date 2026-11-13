# Source record: B53

Origin: https://github.com/Sensirion/embedded-sht/blob/master/sht3x/sht3x.c
Revision/version: `94967774f25985bf65356bad3689fec4e8fef2b8`
Distribution: **public-ok**
Selected source: `upstream/sht3x/sht3x.c` lines 256-270.
Pinned source URL: https://raw.githubusercontent.com/Sensirion/embedded-sht/94967774f25985bf65356bad3689fec4e8fef2b8/sht3x/sht3x.c

Preserves upstream /65536 fixed-point arithmetic, not the datasheet /65535 floating approximation. Read errors abort before conversion. CRC-8 polynomial 0x31, init 0xff. No I2C operations.

Implementation kind: ported-core. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.

## Shared CRC provenance
`upstream-common/REVISION.json` pins the exact embedded-common gitlink used by the selected SHT source. `upstream-common/sensirion_common.c` contains the CRC-8 polynomial/update rule, with its own BSD-3-Clause LICENSE. The tool exposes only byte CRC/decode, never bus-write helpers.
