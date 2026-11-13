---
name: aranma-seviyesi
description: Turns crimes into 'heat' and heat into 0-5 wanted stars, decays heat only after the player has been out of police sight for a star-dependent cooldown, lets a paint shop clear the level when police are not watching, and maps stars to police units, police speed factor and search radius. Returns a timeline for a list of events and the full rule table for the game.
license: MIT
metadata:
  author: Skillpack contributors
  version: "1.0.0"
  usta_approval: pending
---

# Wanted level (0-5 stars) and police response rules

Turns crimes into 'heat' and heat into 0-5 wanted stars, decays heat only after the player has been out of police sight for a star-dependent cooldown, lets a paint shop clear the level when police are not watching, and maps stars to police units, police speed factor and search radius. Returns a timeline for a list of events and the full rule table for the game.

MCP server name: `aranma-seviyesi`; tool: `skillpack_g007`.

## When and how to use

operation=rules returns the table the game will use (with optional overrides). operation=simulate replays events: crimes add heat (x witness_multiplier when witnessed), tick {dt} advances time out of sight, seen_by_police resets the out-of-sight clock, paint_shop clears stars only when unseen for paint_shop_min_unseen_s, busted/wasted reset.

Read manifest.json for the exact schema; do not guess missing data, coerce types or invent values. Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2.

## Place in the game-building flow

Step 5 (aranma kuralları): fix the rule table and replay a sample chase to confirm stars rise and fall as intended; the rules object goes into the HTML (G012), whose runtime applies the same rules each frame.

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
{"mcpServers": {"aranma-seviyesi": {"command": "/ABSOLUTE/PATH/TO/.venv/bin/python", "args": ["/ABSOLUTE/PATH/TO/G007/mcp/server.py"]}}}
```

The FastMCP stdio server exposes exactly one tool, validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit and kills the child process after 10 seconds. It never logs arguments and has no network, shell or code-evaluation parameters.

## Scope and failure

Illustrative game-design defaults, not tuned by playtesting. Stars rise immediately with heat and fall only through out-of-sight decay or reset events. No separate police, army or helicopter tiers. Line-of-sight is decided by the game runtime (distance within search radius), not here.

## Faithfulness

Original rules by Skillpack contributors, inspired by the general wanted-level idea of open-world games; no game code or data was copied. stars = number of thresholds reached; on decay stars = min(stars, level(heat)). Decay only counts the part of a tick that lies after the cooldown.

## Evidence and human review

tests/references.json cases were derived by hand from the default table (each origin shows the arithmetic).

Rule: the code decides, the model explains, the craftsman (usta: game designer (difficulty)) approves. Usta approval status: **pending**. Read SOURCE.md and TEACHING.md. Preserve license and attribution notices in redistribution. Generated with AI by Skillpack contributors.
