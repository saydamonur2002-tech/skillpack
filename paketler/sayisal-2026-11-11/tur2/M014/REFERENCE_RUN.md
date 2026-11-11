# Reproducible native C reference check

Run `python3 reference/verify_native.py` from this pack with GCC available. It performs no network reads, compiles only the included pinned upstream C evidence into a temporary shared library, calls it via ctypes, checks every frozen reference and removes the temporary library. Numerical execution does not import the Python technique port.

The exact compiler command is assembled visibly in verify_native.py: gcc -shared -fPIC -O2 -ffp-contract=off, local include paths, source files and -lm. C translation units were executed on the box during mining; this is not the complete upstream test suite.

The original C algorithm body is used with an explicit portable mconf/platform shim. lgam/beta/lbeta are replaced by system libm lgamma/exp, just as the Python adaptation uses math.lgamma. This verifies the original iteration logic, not bit-identical behavior of the entire Cephes gamma-function family. The independent published literal fixtures remain separately identified.

## Sources and fixture interpretation

Native reference values were produced by the pinned original C body with the documented libm-lgamma/platform shim. Independent published literal anchors are from later v0.19.1 test_basic.py (including P(10,.05)=2.5715803516000736e-20); the distinct source/test/license commits are explicitly recorded. The inverse fixture P(50,11) is honestly labelled a derived forward check.

The exact commit, full-file and delivered-excerpt SHA-256 values are in manifest.json and SOURCE.md. All legal notices must accompany source redistribution.
