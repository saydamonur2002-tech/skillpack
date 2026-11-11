# Reproducible native C reference check

Run `python3 reference/verify_native.py` from this pack with GCC available. It performs no network reads, compiles only the included pinned upstream C evidence into a temporary shared library, calls it via ctypes, checks every frozen reference and removes the temporary library. Numerical execution does not import the Python technique port.

The exact compiler command is assembled visibly in verify_native.py: gcc -shared -fPIC -O2 -ffp-contract=off, local include paths, source files and -lm. C translation units were executed on the box during mining; this is not the complete upstream test suite.

All required original ERFA C dependencies and headers are included unchanged. Native differential fixtures and literal upstream t_erfa_c assertions are separately labelled in tests/references.json.

## Sources and fixture interpretation

The literal t_era00 fixture is (2400000.5,54388.0) -> 0.4022837240028158102 radians, tolerance 1e-12. Additional split, reversed-part and negative-offset references were generated with the exact pinned original C functions.

The exact commit, full-file and delivered-excerpt SHA-256 values are in manifest.json and SOURCE.md. All legal notices must accompany source redistribution.
