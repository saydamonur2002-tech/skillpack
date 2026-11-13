---
name: gorev-sistemi
description: Checks a list of missions (unique ids, known prerequisites, no cycles, required fields) and gives the play order; replays position/tick/collect events through the mission state machine: one active mission at a time, reach-a-tile, pick-up-then-deliver, lose-the-police and collect-N missions, time limits with automatic retry, rewards and the money transactions to send to the economy.
license: MIT
metadata:
  author: Skillpack contributors
  version: "1.0.0"
  usta_approval: pending
---

# Mission chain validation and mission state machine (goto, deliver, escape, collect)

Checks a list of missions (unique ids, known prerequisites, no cycles, required fields) and gives the play order; replays position/tick/collect events through the mission state machine: one active mission at a time, reach-a-tile, pick-up-then-deliver, lose-the-police and collect-N missions, time limits with automatic retry, rewards and the money transactions to send to the economy.

MCP server name: `gorev-sistemi`; tool: `skillpack_g008`.

## When and how to use

validate first; stop if valid is false and show the issues. Targets and pickups are tiles; the tile centre (x+0.5, y+0.5) must be within radius (default 1.5 tiles). simulate replays a scripted play-through (positions, ticks, collect events) to prove the chain can be finished.

Read manifest.json for the exact schema; do not guess missing data, coerce types or invent values. Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2.

## Place in the game-building flow

Step 6 (görevler): build missions from the map landmarks (G002), validate the chain, check every target tile is reachable by car (G005 on the drive grid), and replay a scripted run; the validated list goes into the HTML (G012).

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
{"mcpServers": {"gorev-sistemi": {"command": "/ABSOLUTE/PATH/TO/.venv/bin/python", "args": ["/ABSOLUTE/PATH/TO/G008/mcp/server.py"]}}}
```

The FastMCP stdio server exposes exactly one tool, validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit and kills the child process after 10 seconds. It never logs arguments and has no network, shell or code-evaluation parameters.

## Scope and failure

One active mission at a time, strictly in validated order. No branching choices, cut-scenes or failure by damage. Escape completes when stars return to 0 after being above 0 during the mission. Collect counts collect events of any item.

## Faithfulness

Original state machine by Skillpack contributors. Order = repeated choice of the first mission (input order) whose prerequisites are done (stable topological order). Time-limit failure resets the mission timer and progress and counts a failure.

## Evidence and human review

tests/references.json cases were derived by hand (distances and sums are written in each origin).

Rule: the code decides, the model explains, the craftsman (usta: game designer (missions)) approves. Usta approval status: **pending**. Read SOURCE.md and TEACHING.md. Preserve license and attribution notices in redistribution. Generated with AI by Skillpack contributors.
