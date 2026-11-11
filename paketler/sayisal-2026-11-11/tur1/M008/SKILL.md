---
name: m008
description: "One-level real Haar/db1 transform for even-length vectors: approximation/detail coefficients, separate low/high reconstructions and full reconstruction. No implicit boundary padding."
---

# One-level orthonormal Haar analysis and reconstruction

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

One-level real Haar/db1 transform for even-length vectors: approximation/detail coefficients, separate low/high reconstructions and full reconstruction. No implicit boundary padding.

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
    "m008": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M008/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m008` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

Real, even-length samples only (2..4096). No complex values, multilevel transform, padding mode, wavelet selection, denoising policy or automatic threshold. Haar detail signs and coefficient order follow PyWavelets.

Ports the two-tap db1 analysis/reconstruction equations using sqrt(0.5). For even lengths these do not require boundary extension. The upstream complex fixture is explicitly adapted to real components; this is not claimed to be an unchanged real upstream fixture.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
