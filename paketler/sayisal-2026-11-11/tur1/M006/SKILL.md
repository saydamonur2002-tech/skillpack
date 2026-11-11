---
name: m006
description: "Computes one-dimensional biweight location and midvariance/scale using median absolute deviation, with explicit tuning constants and the upstream optional reduced sample-size definition."
---

# Robust biweight location, midvariance and scale

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Computes one-dimensional biweight location and midvariance/scale using median absolute deviation, with explicit tuning constants and the upstream optional reduced sample-size definition.

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
    "m006": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M006/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m006` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

One finite real vector only, maximum 4096 observations. No axes, masking, NaN omission, measurement units, confidence intervals or multivariate covariance. A zero MAD returns the median and zero variance, as upstream does; this does not prove an absence of variation.

Ports the finite one-dimensional default-M branches of biweight_location, biweight_midvariance and biweight_scale. Python scalar arithmetic replaces NumPy reductions. Undefined zero denominators are structured errors rather than non-finite results.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
