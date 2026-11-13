# Reproducible upstream reference check

Run `python3 reference/verify_upstream.py` from this pack. It makes no network requests and never imports tool/main.py. It runs reference/upstream_harness.js (node) against the pinned upstream files in upstream/, feeds every input from tests/references.json and compares each field with the frozen expected_subset.

Requires: Node.js. This is a differential rerun of the pinned upstream code, not the complete upstream test suite.
