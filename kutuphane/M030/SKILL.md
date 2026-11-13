---
name: m030
description: Shortest or fastest route between two points (optionally through up to 8 via points) on a local road dataset, for car, walking or bike, using A* or Dijkstra. Returns distance, free-flow travel time, the street-by-street segments and a GeoJSON LineString ready for the map renderer. Answers "Kadıköy iskelesinden Moda'ya en kısa yol".
---

# Offline road routing (A*/Dijkstra) with distance, time and street list

Shortest or fastest route between two points (optionally through up to 8 via points) on a local road dataset, for car, walking or bike, using A* or Dijkstra. Returns distance, free-flow travel time, the street-by-street segments and a GeoJSON LineString ready for the map renderer. Answers "Kadıköy iskelesinden Moda'ya en kısa yol".

## When and how to use

Typical chain: M032 geocode the place names, then this tool with the two coordinates, then M034 to draw `result.feature`. Report distance and duration with the free-flow caveat, and name the dataset and attribution. Use only this bounded deterministic operation. Read manifest.json for the exact schema; do not guess missing data, coerce strings/booleans or invent reference values.

Exactly one JSON object is read from stdin; one JSON result is written to stdout. Success: `{ "ok": true, "result": {...} }`. Failure: `{ "ok": false, "error": {"code": "...", "message": "..."} }`, exit status 2. Duplicate keys, nonfinite values, extra properties and oversized input are rejected.

## Run

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
SKILLPACK_MAP_DATA=tests/fixtures .venv/bin/python tool/main.py < example.json
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m pytest tests
```

Dependencies must be available for installation; they are not vendored. The calculation itself uses only the Python standard library and no network.

## Map data

This pack reads local map files only. Datasets are chosen by **name**, never by path, inside one folder picked by the human: the `SKILLPACK_MAP_DATA` environment variable, or a `map_data` folder next to the pack. A bare name such as `demo_kadikoy` resolves to `demo_kadikoy_<layer>.geojson` (layers: roads, places, areas), then `.csv`, then `demo_kadikoy.osm`; a name with an extension is used as the file name. Accepted formats: GeoJSON (LineString roads with OSM-style `highway`, `oneway`, `maxspeed`, `name`, `access` properties; Point places with `name` and `category`), CSV places (`name,category,lat,lon`), or a small OSM XML extract (`.osm`, parsed on every call, so keep it small). Files above 64 MiB are refused. The demo dataset is OpenStreetMap data under ODbL 1.0 (© OpenStreetMap contributors) and ships separately from the code; tests use a synthetic CC0 grid in tests/fixtures.

## MCP

```json
{
  "mcpServers": {
    "m030": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M030/mcp/server.py"
      ],
      "env": {
        "SKILLPACK_MAP_DATA": "/ABSOLUTE/PATH/TO/map_data"
      }
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m030`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

Routing uses only the local road file: free-flow speeds by road class (car: motorway 90 ... residential 25, living street 10, service 15 km/h, or a numeric maxspeed tag), walking 5 km/h (steps 3), cycling 15 km/h (5 on footways that allow bicycles). One-way tags and roundabouts are respected for car and bike, ignored for walking; access=no/private roads are excluded. There is no live or historic traffic, no turn restrictions or turn costs, no traffic lights, ferries, public transport, elevation or time-of-day rules. Vertices are joined only where lines share an identical coordinate (7 decimals), as in OSM-derived exports; bridges/tunnels without shared nodes are not connected. Points are snapped to the nearest routable vertex (straight-line, default limit 300 m), which can be on the wrong side of a barrier. The whole file is read on every call; files above roughly 20 MB may not finish within the 10-second limit. Vertex numbers in the output are internal to one dataset load.

## Faithfulness

The search is a port of networkx 3.6.1 astar_path (counter tie-break, enqueued/explored bookkeeping, skip of stale queue entries); Dijkstra is the same function with a zero heuristic, as in upstream. The heuristic is straight-line haversine distance (divided by the fastest edge speed in the graph when optimizing time), so it never overestimates and A* returns an optimal path. Graph building, snapping, profiles and segment grouping are Skillpack code in tool/mapdata.py and tool/main.py, documented in SKILL.md.

## Evidence and human review

Fixture graphs are synthetic (CC0). Expected vertex paths, distances and durations were produced by the installed networkx 3.6.1 (astar_path or dijkstra_path) on a DiGraph built from the same Skillpack graph builder; the harness checks that the installed astar.py and weighted.py are byte-identical to the pinned upstream copies under upstream/. Graph construction is shared code, so only the search is independently compared.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI by Skillpack contributors; no upstream endorsement, formal verification or independent certification is implied.
