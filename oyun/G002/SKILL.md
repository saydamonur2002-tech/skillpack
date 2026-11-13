---
name: sehir-haritasi
description: Generates a repeatable 2D tile city from a seed: a grid of two-lane roads with edge ring roads, city blocks with a sidewalk ring and either a building or a park inside, plus a player spawn, police station, paint shop, mission landmarks, cash pickups, suggested pedestrian and traffic route requests, walk/drive cost tables and collision-check pairs for the spawn. Same seed, same city.
license: MIT
metadata:
  author: Skillpack contributors
  version: "1.0.0"
  usta_approval: pending
---

# Top-down tile city generator (roads, sidewalks, buildings, parks, points of interest)

Generates a repeatable 2D tile city from a seed: a grid of two-lane roads with edge ring roads, city blocks with a sidewalk ring and either a building or a park inside, plus a player spawn, police station, paint shop, mission landmarks, cash pickups, suggested pedestrian and traffic route requests, walk/drive cost tables and collision-check pairs for the spawn. Same seed, same city.

MCP server name: `sehir-haritasi`; tool: `skillpack_g002`.

## When and how to use

Give a seed and size in tiles (1 tile = 1 game unit, x = column, y = row downwards). Optional: road_width (2), block_min/block_max (4/7), park_ratio (0.2), landmarks (6), cash_pickups (5), ped_routes (6), traffic_routes (4). Feed tiles + walk_costs/drive_costs and the route pairs to G005, spawn_collision_pairs to G004, mission_targets to G008 and the whole map to G012.

Read manifest.json for the exact schema; do not guess missing data, coerce types or invent values. Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2.

## Place in the game-building flow

Step 1 (harita): the first call of the flow; every later step reads its tiles and points.

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
{"mcpServers": {"sehir-haritasi": {"command": "/ABSOLUTE/PATH/TO/.venv/bin/python", "args": ["/ABSOLUTE/PATH/TO/G002/mcp/server.py"]}}}
```

The FastMCP stdio server exposes exactly one tool, validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit and kills the child process after 10 seconds. It never logs arguments and has no network, shell or code-evaluation parameters.

## Scope and failure

Manhattan grid only (no curved roads, highways, rivers or bridges). The last block on each axis absorbs leftover space and can exceed block_max. One building per block. Points are placed by the seeded generator and are not guaranteed to be interesting; the designer may change the seed. Modulo bias in randint is accepted (game use only).

## Faithfulness

Original algorithm by Skillpack contributors. Random numbers come from xorshift32 (G. Marsaglia, 'Xorshift RNGs', J. Stat. Software 8(14), 2003; shift triple 13,17,5) seeded with the given seed (0 replaced by 0x9E3779B9). Axis split: edge road, then blocks of random width, final road on the far edge. Road connectivity is verified by flood fill and reported.

## Evidence and human review

tests/references.json holds frozen golden outputs of this original generator (regression only, not an external truth). Independent checks: the xorshift32 first output for seed 1 is 270369 (published sequence), and invariant tests check edge roads, block rings, connectivity, point placement and determinism.

Rule: the code decides, the model explains, the craftsman (usta: level designer) approves. Usta approval status: **pending**. Read SOURCE.md and TEACHING.md. Preserve license and attribution notices in redistribution. Generated with AI by Skillpack contributors.
