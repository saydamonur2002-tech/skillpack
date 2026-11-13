# Reproducible upstream reference check

Run `python3 reference/verify_upstream.py` from this pack. It performs no network reads and never imports the ported formula or search in tool/main.py. Instead Python runs reference/upstream_harness.py against the pinned upstream code, feeds every input from tests/references.json and compares each output field exactly (absolute tolerance 0) with the frozen expected_subset. The pack tests compare the Python port with the same values using the per-case tolerance stored in references.json.

Requires networkx==3.6.1 installed (see requirements-test.txt); the harness refuses any other version and checks the installed source files byte-for-byte against upstream/. This is a differential rerun of the pinned upstream code, not the complete upstream test suite.

## Sources and fixture interpretation

Fixture graphs are synthetic (CC0). Expected vertex paths, distances and durations were produced by the installed networkx 3.6.1 (astar_path or dijkstra_path) on a DiGraph built from the same Skillpack graph builder; the harness checks that the installed astar.py and weighted.py are byte-identical to the pinned upstream copies under upstream/. Graph construction is shared code, so only the search is independently compared.

The exact commit and file SHA-256 values are in manifest.json and SOURCE.md. All legal notices must accompany source redistribution.
