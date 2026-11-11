---
name: m001
description: "One-dimensional cubic spline with second derivatives fixed by the first/last four-point interpolating cubics; optional natural endpoints. Returns value, first and second derivatives, including explicit polynomial extrapolation."
---

# Consistent-end cubic spline and derivatives

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

One-dimensional cubic spline with second derivatives fixed by the first/last four-point interpolating cubics; optional natural endpoints. Returns value, first and second derivatives, including explicit polynomial extrapolation.

Read manifest.json for the strict JSON schema. Additional fields, nonfinite numbers and duplicate JSON keys are rejected. Exactly one request object is read from stdin and one JSON result is written to stdout. Success is `{ "ok": true, "result": {...} }`; failure is `{ "ok": false, "error": {"code": "...", "message": "..."} }` and CLI exit code 2.

## Run

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tool/main.py < example.json
```

Dependency installation needs package availability; dependencies are not bundled. Calculations require no network access once installed.

## MCP connection

```json
{
  "mcpServers": {
    "m001": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M001/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m001` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

At least four strictly increasing finite knots, at most 256 knots and 512 query points. No smoothing, uncertainty estimate or multidimensional interpolation. Extrapolation evaluates the outer cubic and can be misleading.

The endpoint condition and interpolating spline are preserved. Upstream solves a banded coefficient system with LAPACK; this port solves the algebraically equivalent tridiagonal second-derivative system and a scaled four-point endpoint solve. Natural endpoints expose upstream bctype=1 with zero second derivatives. No LAPACK dependency.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
