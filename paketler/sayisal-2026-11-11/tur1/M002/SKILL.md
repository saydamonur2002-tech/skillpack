---
name: m002
description: "Computes finite-difference weights of every derivative order up to the requested order on distinct, arbitrarily spaced real nodes. Optional sampled values are combined into one derivative estimate."
---

# Fornberg arbitrary-grid finite-difference weights

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Computes finite-difference weights of every derivative order up to the requested order on distinct, arbitrarily spaced real nodes. Optional sampled values are combined into one derivative estimate.

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
    "m002": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M002/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m002` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

At most 25 distinct real nodes, derivative order 0..8 and smaller than node count. No function strings, arbitrary code, complex nodes, adaptive step-size selection or trustworthy error bound. Clustered nodes amplify noise and roundoff.

Scalar-list port of fd_weights_all / _fd_weights_all, preserving the recurrence and update ordering. Only real numbers are supported; SciPy/NumPy are not runtime dependencies.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
