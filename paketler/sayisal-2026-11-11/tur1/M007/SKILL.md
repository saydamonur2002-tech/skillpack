---
name: m007
description: "Computes the median, median absolute deviation (MAD), and MAD multiplied by the upstream Gaussian consistency constant 1.482602218505602."
---

# Median absolute deviation and Gaussian scale

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Computes the median, median absolute deviation (MAD), and MAD multiplied by the upstream Gaussian consistency constant 1.482602218505602.

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
    "m007": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M007/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m007` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

One finite vector of at most 4096 values; no axes, masks, missing-value omission or units. The Gaussian-scaled value estimates standard deviation only under an appropriate distributional model. MAD can be zero for non-constant discrete data.

Ports the finite one-dimensional default-median behavior of median_absolute_deviation and mad_std. Rejects invalid input rather than omitting it.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
