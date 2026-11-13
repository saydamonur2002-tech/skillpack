# Source record: A60

Origin: https://github.com/babylonhealth/fhir-hydrant
Revision/version: `0f1651136958d3f50dc48fd6bcb3058838b6b9e4`
Distribution: **public-ok**
Selected source: `upstream/docs/templates.md` lines 1-1002.
Pinned source URL: https://raw.githubusercontent.com/babylonhealth/fhir-hydrant/0f1651136958d3f50dc48fd6bcb3058838b6b9e4/docs/templates.md

Independent implementation of documented scalar triple-brace mapping. No Scala runtime, repeated parameters, inheritance, dehydrate, external terminology or full FHIR validity. Optional absent parameters cannot be referenced.

Implementation kind: new-format-adapter. New adapters and ports are explicitly distinguished from upstream runtime wrappers. Source files are reference snapshots, not automatically executable. No model weights or external services are required.

## Evidence
`ACQUISITION.json` records fetched paths, hashes and failed URL attempts. Full source LICENSE and NOTICE were retained when present. If a separate LICENSE was absent, the manifest remains private-only; metadata claims are not silently treated as a redistribution license. Content snapshots are hashed when a source has no git revision.

## Testing boundary
Tests are local deterministic known-answer/synthetic vectors, plus selected upstream fixtures. Passing is not full upstream conformance, real sensor calibration, hardware validation or a security certification. Tests were authored in this run unless an individual vector cites upstream provenance. The final test report is in `../TEST_RESULTS.json`.
