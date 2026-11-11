---
name: m004
description: "Haversine central angle and spherical great-circle distance, with forward initial/final bearings and an explicit positive sphere radius. This is a spherical model, not a WGS84 ellipsoidal result."
---

# Spherical great-circle distance and bearings

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Haversine central angle and spherical great-circle distance, with forward initial/final bearings and an explicit positive sphere radius. This is a spherical model, not a WGS84 ellipsoidal result.

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
    "m004": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M004/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m004` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

Decimal-degree coordinates; default radius 6371000 m. Real Earth distances differ from the spherical approximation. Undefined bearings at coincident or exactly antipodal points are null. No geocoding, terrain, route planning or live navigation.

Ports distanceTo, initialBearingTo and finalBearingTo. Haversine is clamped into [0,1] against floating-point excursions. Undefined coincident/antipodal bearings are explicitly null. The radius is in metres in this adapter.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
