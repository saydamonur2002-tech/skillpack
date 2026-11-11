---
name: m013
description: Propagate y'=matrix*y+bias between explicit times using bounded fixed steps and the 13-stage Fehlberg 7(8) tableau. Return the upstream xf combination and raw last-step error indicator plus its h-scaled local-state interpretation.
---

# Fehlberg 7(8) fixed-step affine linear ODE propagation

Propagate y'=matrix*y+bias between explicit times using bounded fixed steps and the 13-stage Fehlberg 7(8) tableau. Return the upstream xf combination and raw last-step error indicator plus its h-scaled local-state interpretation.

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
    "m013": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M013/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m013`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

Autonomous affine linear systems only, dimension 1..8 and at most 10000 fixed steps. Not RK45, not a complete adaptive integrator, no stiffness handling, events, dense output, spacecraft model or global-error certificate. Keep physical units consistent between matrix, bias, times and state. Overflow is rejected. The raw upstream terr omits h; treating it as a state error would be dimensionally wrong.

## Faithfulness

Preserves all 13 stages and the exact upstream xf weights; returns last_error_indicator=(41/840)*(f0+f10-f11-f12) exactly as the Fortran routine does, WITHOUT h. last_local_error_estimate=h*last_error_indicator is an explicitly derived adapter field, not an upstream output and not a global error bound. Adds a fixed-step loop and limits the callback to matrix*y+bias. The source cites Fehlberg NASA 1968; this is a modern Fortran implementation of that classic formula, not a claim that the repository contains 1968 source. No Fortran compiler was available, so the original Fortran binary was not executed.

## Evidence and human review

Primary upstream embedded test prints orbital examples but supplies no asserted golden trajectory. State fixtures instead come from the explicitly pinned BSD SciPy test_ivp.py fun_linear/sol_linear analytic solution, a different upstream validation source. Scalar exponential, zero and constant-derivative cases are supplementary analytic checks. Neither RKF78 raw terr nor a full adaptive controller has an independent native-Fortran reference here.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI; no upstream endorsement, formal verification or independent certification is implied.
