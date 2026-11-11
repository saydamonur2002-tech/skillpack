---
name: m009
description: "Computes an image center of mass from pixel intensities, optionally excluding a boolean mask. Returns x (column), y (row), and the included signed intensity sum."
---

# Masked image center of mass

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Computes an image center of mass from pixel intensities, optionally excluding a boolean mask. Returns x (column), y (row), and the included signed intensity sum.

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
    "m009": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M009/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m009` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

Rectangular 2D finite real data, at most 64 rows/columns and 4096 pixels. No image file reading, background estimation, PSF fitting, segmentation, nonfinite-value masking or units. Signed intensities are accepted and can place a centroid outside the image. Absolute included total below 1e-30 is an error.

Ports the 2D finite/masked branch of centroid_com: sum(index*data)/sum(data), reversed to x,y order. Upstream undefined NaN output for near-zero total becomes a structured error. Nonfinite pixels are rejected, not automatically masked.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
