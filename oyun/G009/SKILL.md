---
name: ekonomi-envanter
description: Applies earn, spend, buy, sell, pickup, use and drop transactions to an integer wallet and an item inventory with per-item limits, either one by one (rejected ones are skipped with a reason) or all-or-nothing, and returns the ledger with the balance after each step and the effects the game must apply (repair, health, clear wanted level).
license: MIT
metadata:
  author: Skillpack contributors
  version: "1.0.0"
  usta_approval: pending
---

# Game economy: wallet, shop catalog and inventory ledger

Applies earn, spend, buy, sell, pickup, use and drop transactions to an integer wallet and an item inventory with per-item limits, either one by one (rejected ones are skipped with a reason) or all-or-nothing, and returns the ledger with the balance after each step and the effects the game must apply (repair, health, clear wanted level).

MCP server name: `ekonomi-envanter`; tool: `skillpack_g009`.

## When and how to use

operation=catalog returns the shop table (defaults plus overrides). operation=apply needs transactions; money is whole game dollars (no decimals, never negative). Missions (G008) produce earn transactions; the paint_job service maps to the G007 paint_shop event.

Read manifest.json for the exact schema; do not guess missing data, coerce types or invent values. Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2.

## Place in the game-building flow

Step 7 (ekonomi): set the starting money and shop catalog, replay mission rewards and a few purchases to check prices make sense; the catalog and start money go into the HTML (G012).

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
{"mcpServers": {"ekonomi-envanter": {"command": "/ABSOLUTE/PATH/TO/.venv/bin/python", "args": ["/ABSOLUTE/PATH/TO/G009/mcp/server.py"]}}}
```

The FastMCP stdio server exposes exactly one tool, validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit and kills the child process after 10 seconds. It never logs arguments and has no network, shell or code-evaluation parameters.

## Scope and failure

Single currency, integer amounts, no interest, theft or taxes. Effects are labels for the game to apply; this tool does not change health or wanted level itself. Illustrative prices.

## Faithfulness

Original ledger by Skillpack contributors. Checks run before any change; all_or_nothing stops at the first rejection and returns the starting wallet and inventory. Money is capped at 1e9.

## Evidence and human review

tests/references.json cases were derived by hand (arithmetic in each origin).

Rule: the code decides, the model explains, the craftsman (usta: game designer (economy)) approves. Usta approval status: **pending**. Read SOURCE.md and TEACHING.md. Preserve license and attribution notices in redistribution. Generated with AI by Skillpack contributors.
