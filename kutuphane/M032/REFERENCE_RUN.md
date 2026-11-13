# Reproducible upstream reference check

Run `python3 reference/verify_upstream.py` from this pack. It performs no network reads and never imports the ported formula or search in tool/main.py. Instead Python runs reference/upstream_harness.py against the pinned upstream code, feeds every input from tests/references.json and compares each output field exactly (absolute tolerance 0) with the frozen expected_subset. The pack tests compare the Python port with the same values using the per-case tolerance stored in references.json.

This is a differential rerun of the pinned upstream code, not the complete upstream test suite.

## Sources and fixture interpretation

Fixture places are synthetic (CC0). Expected matches, scores, counts and reverse results were produced by reference/upstream_harness.py: an independent re-implementation of the documented ranking that calls the pinned upstream jellyfish pure-Python jaro_winkler_similarity and Skillpack's shared file loader, without importing the port. jellyfish fixtures themselves are covered by pack M023.

The exact commit and file SHA-256 values are in manifest.json and SOURCE.md. All legal notices must accompany source redistribution.
