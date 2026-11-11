---
name: m019
description: Compute the IAU 2000 Earth Rotation Angle in radians [0,2*pi) and degrees from an explicitly supplied two-part UT1 Julian Date, preserving the original ERFA split-date arithmetic and normalization.
---

# IAU 2000 Earth rotation angle from split UT1 Julian date

Compute the IAU 2000 Earth Rotation Angle in radians [0,2*pi) and degrees from an explicitly supplied two-part UT1 Julian Date, preserving the original ERFA split-date arithmetic and normalization.

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
    "m019": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M019/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m019`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

Inputs MUST be UT1, not an assumed UTC timestamp. No UT1-UTC lookup, IERS data, polar motion, sidereal-time model, nutation, observer coordinates or full Earth-orientation transform. The schema only bounds numerical values; it cannot prove a timescale label is correct. Very remote epochs can lose numerical/model accuracy despite being inside the arithmetic bounds.

## Faithfulness

Ports eraEra00 with ordering of the two date parts, t=d1+(d2-J2000), fractional parts using C-style fmod, the exact IAU constants and eraAnp normalization. Degrees are a derived convenience output. This is a separate Earth-rotation primitive, not a generic 3D rotation pack and not the earlier solar-position algorithm. Full ERFA source notices remain intact.

## Evidence and human review

The literal t_era00 fixture is (2400000.5,54388.0) -> 0.4022837240028158102 radians, tolerance 1e-12. Additional split, reversed-part and negative-offset references were generated with the exact pinned original C functions.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI; no upstream endorsement, formal verification or independent certification is implied.
