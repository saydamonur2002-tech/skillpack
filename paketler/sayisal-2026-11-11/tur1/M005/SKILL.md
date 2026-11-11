---
name: m005
description: "Computes spherical loxodrome distance and constant compass bearing using the Mercator stretch factor, including the east-west limiting case and shortest antimeridian crossing."
---

# Mercator rhumb-line distance and constant bearing

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Computes spherical loxodrome distance and constant compass bearing using the Mercator stretch factor, including the east-west limiting case and shortest antimeridian crossing.

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
    "m005": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M005/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m005` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

Spherical model with default 6371000 m radius; latitudes must be strictly between the poles. A rhumb line is generally not a shortest path. Coincident bearing is null. No ellipsoidal loxodrome, magnetic-declination correction or navigation authorization.

Ports rhumbDistanceTo and rhumbBearingTo with the exact upstream 10e-12 Mercator tolerance. Poles are explicitly rejected rather than relying on non-finite logarithms. Coincident NaN bearing becomes null.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
