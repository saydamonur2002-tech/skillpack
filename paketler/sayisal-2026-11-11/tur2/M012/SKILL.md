---
name: m012
description: Integrate one bounded polynomial or enumerated smooth function over a finite interval using the original 10/21 Gauss–Kronrod pair. Return value, absolute error estimate, Gauss-10 result, resabs, resasc and evaluation count.
---

# QUADPACK 21-point Gauss–Kronrod panel and error diagnostics

Integrate one bounded polynomial or enumerated smooth function over a finite interval using the original 10/21 Gauss–Kronrod pair. Return value, absolute error estimate, Gauss-10 result, resabs, resasc and evaluation count.

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
    "m012": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M012/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m012`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

Exactly one panel: no adaptive subdivision, infinite bounds, singularity detection or QAGS/QAGI implementation. The error estimate is heuristic and may underestimate aliased/narrow features. sin/cos/exp use radians/dimensionless x. bessel_integrand is cos(order*x-argument*sin(x))/pi; it only represents the conventional Bessel integral on [0,pi]. Overflow is an error. Zero-width intervals return zero without sampling.

## Faithfulness

Faithful double-precision DQK21 abscissae and weights, even/odd node evaluation order, Gauss comparison, absolute integral, mean-deviation integral, resasc-based error rescaling and 50*machine-epsilon roundoff floor. The upstream prologue dates the Fortran routine to 1980 with a 1983 revision. Only a safe finite set of integrands replaces Fortran callbacks; this does not port the full adaptive QUADPACK driver. Original Fortran was not compiled in this environment.

## Evidence and human review

The upstream quadpack test asserts sin integral=2 and the n=2,z=1.8 Bessel integral=0.30614353532540296487. Those are driver-level published fixtures, applied here to a smooth single panel with declared tolerances. Supplemental polynomial expectations are analytically integrated, not upstream literal gold.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI; no upstream endorsement, formal verification or independent certification is implied.
