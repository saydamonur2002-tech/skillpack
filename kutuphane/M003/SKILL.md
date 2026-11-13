---
name: m003
description: "Solves the WGS84 ellipsoidal inverse geodesic using Vincenty iteration: surface distance in metres and forward initial/final bearings. Reports non-convergence rather than substituting a spherical answer."
---

# WGS84 Vincenty inverse geodesic

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Solves the WGS84 ellipsoidal inverse geodesic using Vincenty iteration: surface distance in metres and forward initial/final bearings. Reports non-convergence rather than substituting a spherical answer.

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
    "m003": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M003/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m003` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

WGS84 surface points only; decimal degrees, no altitude, datum conversion or other ellipsoids. Vincenty can fail near antipodes; this returns a structured error. Coincident bearings are null, not JSON NaN. Distance is rounded to millimetres and bearings to 7 decimals as upstream public methods do.

Port of inverse() and the upstream public distance/bearing rounding, including the equatorial and exactly antipodal branches and 1000-iteration guard. Non-convergence becomes an error instead of upstream public-method NaN. Undefined coincident bearings become null.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.

Adapter hardening: longitude difference is normalized to [-180,180), and physically coincident poles / equivalent antimeridian representations are detected before iteration. This deliberately avoids representation-sensitive degeneracies rather than reproducing them.
