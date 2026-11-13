# Source record: B46

Origin: https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/blueprints/motion_light.yaml
Revision/version: `d9115f3e0492aa94b06edb439ab1ebcd594b4738`
Distribution: **public-ok**
Selected source: `upstream/homeassistant/components/automation/blueprints/motion_light.yaml` lines 1-58.
Pinned source URL: https://raw.githubusercontent.com/home-assistant/core/d9115f3e0492aa94b06edb439ab1ebcd594b4738/homeassistant/components/automation/blueprints/motion_light.yaml

Deterministic simulation of restart, wait-for-off and delay. Deadline is processed before an event at the same timestamp; this tie rule is explicit. No lights are operated.

Implementation kind: ported-rule. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
