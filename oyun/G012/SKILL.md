---
name: html-oyun-uret
description: Assembles the outputs of the other game skills (map, routes, car parameters, NPC/police parameters, wanted rules, missions, economy, sounds, loop step) into ONE offline HTML file with a canvas game: drive a car around the city, pedestrians and traffic follow precomputed routes, police pursue by wanted level, missions, cash, paint shop, sounds, save/load and touch buttons. The real-time loop runs in the browser (MainLoop.js); the model is not needed while playing.
license: MIT
metadata:
  author: Skillpack contributors
  version: "1.0.0"
  usta_approval: pending
---

# Self-contained HTML5 canvas game builder (top-down city driving game)

Assembles the outputs of the other game skills (map, routes, car parameters, NPC/police parameters, wanted rules, missions, economy, sounds, loop step) into ONE offline HTML file with a canvas game: drive a car around the city, pedestrians and traffic follow precomputed routes, police pursue by wanted level, missions, cash, paint shop, sounds, save/load and touch buttons. The real-time loop runs in the browser (MainLoop.js); the model is not needed while playing.

MCP server name: `html-oyun-uret`; tool: `skillpack_g012`.

## When and how to use

Call once at the end of the flow with the collected outputs (see flows/oyun-kur.flow.json for the exact mapping). The result.html string is the whole game; save it as index.html. Defaults are filled for vehicle and npc fields you leave out.

Read manifest.json for the exact schema; do not guess missing data, coerce types or invent values. Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2.

## Place in the game-building flow

Step 12 (HTML üret): the last skill call; the runner writes result.html to index.html, then verifies it (no external URLs, JavaScript syntax, a headless run of the game loop).

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
{"mcpServers": {"html-oyun-uret": {"command": "/ABSOLUTE/PATH/TO/.venv/bin/python", "args": ["/ABSOLUTE/PATH/TO/G012/mcp/server.py"]}}}
```

The FastMCP stdio server exposes exactly one tool, validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit and kills the child process after 10 seconds. It never logs arguments and has no network, shell or code-evaluation parameters.

## Scope and failure

Simple 2D graphics (coloured tiles and rectangles), no textures, no on-foot mode, no weapons, no multiplayer. NPC steering ignores walls except for push-out, so police can get stuck on corners. Real-time behaviour depends on the browser; audio starts only after the first key or touch (browser rule). Input max 64 KB, so maps above about 96x96 tiles do not fit.

## Faithfulness

Original builder and game runtime by Skillpack contributors. Embedded third-party code: MainLoop.js build/mainloop.min.js (MIT, leading comment with an author URL replaced by the full MIT notice in an HTML comment so the file has no URLs) and ZzFXMicro.min.js (MIT, wrapped in a function so the AudioContext is created only after a user gesture). The configuration JSON is embedded with <, > and & escaped. The runtime implements the formulas of G003 (car), G004 (circle vs box), G006 (seek/arrive/flee/pursuit), G007 (wanted), G008 (missions), G009 (integer money) and G010 (save envelope); tests/test_flow_e2e.py compares them with the Python tools.

## Evidence and human review

Original builder; references are structural (self-contained check, embedded parts, summary counts). Behaviour is checked end to end: the flow runner builds a game and Node.js runs it headless and compares the runtime formulas with G003, G004, G006 and G010.

Rule: the code decides, the model explains, the craftsman (usta: game designer and a playtester) approves. Usta approval status: **pending**. Read SOURCE.md and TEACHING.md. Preserve license and attribution notices in redistribution. Generated with AI by Skillpack contributors.
