# Source record: A42

Origin: https://github.com/babylonhealth/lit-fhir
Revision/version: `9791e0aef2552507f465e6326ed60e66a277f1f9`
Distribution: **public-ok**
Selected source: `upstream/hl7/src/main/scala/com/babylonhealth/lit/hl7/model/Patient.scala` lines 1-639.
Pinned source URL: https://raw.githubusercontent.com/babylonhealth/lit-fhir/9791e0aef2552507f465e6326ed60e66a277f1f9/hl7/src/main/scala/com/babylonhealth/lit/hl7/model/Patient.scala

New structural port of selected Patient scalar fields. Not full FHIR R4, date calendar validity, profiles, terminology or clinical validation. Synthetic inputs only.

Implementation kind: schema-rule. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
