---
name: kayit-yukle
description: Saves the city game state (player car, money, inventory, wanted level, missions, picked-up cash) as a versioned envelope with a canonical JSON form (sorted keys, numbers rounded to 3 decimals) and an FNV-1a 32-bit checksum, and loads it back, refusing saves of another format or version and reporting damaged or edited saves. The browser game writes the same envelope to localStorage.
license: MIT
metadata:
  author: Skillpack contributors
  version: "1.0.0"
  usta_approval: pending
---

# Save and load game state (versioned JSON envelope with FNV-1a checksum)

Saves the city game state (player car, money, inventory, wanted level, missions, picked-up cash) as a versioned envelope with a canonical JSON form (sorted keys, numbers rounded to 3 decimals) and an FNV-1a 32-bit checksum, and loads it back, refusing saves of another format or version and reporting damaged or edited saves. The browser game writes the same envelope to localStorage.

MCP server name: `kayit-yukle`; tool: `skillpack_g010`.

## When and how to use

save {state} returns envelope + canonical_state; load {envelope} returns valid and the state; checksum {text} returns the FNV-1a 32 checksum of any text (to compare with the browser).

Read manifest.json for the exact schema; do not guess missing data, coerce types or invent values. Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2.

## Place in the game-building flow

Step 10 (kayıt biçimi): save the starting state of the game to fix the save format; the end-to-end test saves from the browser runtime and loads it with this tool to prove both sides agree.

## Run

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tool/main.py < example.json
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m pytest tests
```

## MCP

```json
{"mcpServers": {"kayit-yukle": {"command": "/ABSOLUTE/PATH/TO/.venv/bin/python", "args": ["/ABSOLUTE/PATH/TO/G010/mcp/server.py"]}}}
```

The FastMCP stdio server exposes exactly one tool, validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit and kills the child process after 10 seconds. It never logs arguments and has no network, shell or code-evaluation parameters.

## Scope and failure

The checksum detects accidental damage and casual edits, not tampering by a determined player (FNV-1a is not cryptographic). Only format version 1 exists; there is no migration yet. Numbers are rounded to 3 decimals on save.

## Faithfulness

Original format by Skillpack contributors. FNV-1a 32 (Fowler-Noll-Vo; offset basis 2166136261, prime 16777619) over the UTF-8 bytes of the canonical JSON. Rounding uses floor(x*1000+0.5)/1000 in both Python and JavaScript, and integral values are written as integers, so Python json and JavaScript JSON.stringify produce the same text.

## Evidence and human review

FNV-1a cases are published test vectors (empty string, 'a', 'foobar'); the canonical form case was written by hand from the rules.

Rule: the code decides, the model explains, the craftsman (usta: game programmer) approves. Usta approval status: **pending**. Read SOURCE.md and TEACHING.md. Preserve license and attribution notices in redistribution. Generated with AI by Skillpack contributors.
