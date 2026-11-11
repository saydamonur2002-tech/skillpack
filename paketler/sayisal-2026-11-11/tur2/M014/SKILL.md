---
name: m014
description: Evaluate regularized incomplete gamma P(shape,x) and Q(shape,x) using the classic 1987 power-series and scaled continued-fraction algorithms. Shape is positive and x nonnegative; outputs are dimensionless.
---

# Cephes regularized incomplete gamma lower and upper tails

Evaluate regularized incomplete gamma P(shape,x) and Q(shape,x) using the classic 1987 power-series and scaled continued-fraction algorithms. Shape is positive and x nonnegative; outputs are dimensionless.

## When and how to use

Use only this bounded mathematical operation. Read manifest.json for the exact schema; do not guess missing physical data, reinterpret a timescale, coerce strings/booleans or invent reference values. Coefficients, where present, are descending-degree order.

Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2. Duplicate keys, nonfinite values, extra properties and oversized input are rejected.

## Run

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tool/main.py < example.json
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m pytest tests
```

Dependencies must be available for installation; they are not vendored. Numerical calculation itself uses only Python standard-library math and no network.

## MCP

```json
{
  "mcpServers": {
    "m014": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M014/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m014`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

Legacy double-precision method, not a modern uniform-asymptotic implementation. Shape 1e-5..1000 and x 0..10000; extreme tails can underflow and subtraction can lose relative tail accuracy. This is a special-function primitive, not a fitted distribution, quantile solver or statistical significance recommendation. No arbitrary precision or blanket digit guarantee.

## Faithfulness

Ports the v0.15.1 C igam.c algorithm (source identifies Cephes April 1987), including branch selection, MAXLOG guard, fraction renormalization by 2^52 and series convergence at MACHEP=2^-53. Python math.lgamma substitutes for the separate Cephes lgam implementation; iteration caps are explicit new safety bounds. The old source carries its original copyright but only a platform include and algorithm body are redistributed as compilable evidence; a nonlegal postal-contact line is omitted. Full SciPy BSD text and the separately pinned explicit Cephes BSD author-permission block are preserved. No claim of bit-identical full-Cephes behavior.

## Evidence and human review

Native reference values were produced by the pinned original C body with the documented libm-lgamma/platform shim. Independent published literal anchors are from later v0.19.1 test_basic.py (including P(10,.05)=2.5715803516000736e-20); the distinct source/test/license commits are explicitly recorded. The inverse fixture P(50,11) is honestly labelled a derived forward check.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI; no upstream endorsement, formal verification or independent certification is implied.
