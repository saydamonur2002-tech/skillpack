---
name: m031
description: Many-to-many travel times and road distances between up to 25 origins and 25 destinations on a local road dataset (car, walk or bike), or an isochrone: every road segment reachable from one point within N minutes, returned as GeoJSON MultiLineString with its extent and farthest point. Answers "which of these three pharmacies is closest by walking?" and "where can I walk in 10 minutes?".
---

# Travel-time/distance matrix and isochrone (reachable roads within N minutes)

Many-to-many travel times and road distances between up to 25 origins and 25 destinations on a local road dataset (car, walk or bike), or an isochrone: every road segment reachable from one point within N minutes, returned as GeoJSON MultiLineString with its extent and farthest point. Answers "which of these three pharmacies is closest by walking?" and "where can I walk in 10 minutes?".

## When and how to use

Use matrix to rank candidate places (for example nearby pharmacies from M033) by real road time instead of straight-line distance; use isochrone and draw result.feature with M034. Use only this bounded deterministic operation. Read manifest.json for the exact schema; do not guess missing data, coerce strings/booleans or invent reference values.

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
    "m031": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M031/mcp/server.py"
      ],
      "env": {
        "SKILLPACK_MAP_DATA": "/ABSOLUTE/PATH/TO/map_data"
      }
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m031`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

Routing uses only the local road file: free-flow speeds by road class (car: motorway 90 ... residential 25, living street 10, service 15 km/h, or a numeric maxspeed tag), walking 5 km/h (steps 3), cycling 15 km/h (5 on footways that allow bicycles). One-way tags and roundabouts are respected for car and bike, ignored for walking; access=no/private roads are excluded. There is no live or historic traffic, no turn restrictions or turn costs, no traffic lights, ferries, public transport, elevation or time-of-day rules. Vertices are joined only where lines share an identical coordinate (7 decimals), as in OSM-derived exports; bridges/tunnels without shared nodes are not connected. Points are snapped to the nearest routable vertex (straight-line, default limit 300 m), which can be on the wrong side of a barrier. The whole file is read on every call; files above roughly 20 MB may not finish within the 10-second limit. Matrix cells report the distance and time along the path that minimises the chosen metric; null means unreachable. The isochrone lists whole road segments whose both ends are reachable (partial segments at the edge are omitted) and is not a smoothed area; at most 12000 segments are returned, and max_minutes is capped at 60.

## Faithfulness

Single-source Dijkstra is a port of networkx 3.6.1 _dijkstra_multisource with a predecessor dict (as used by dijkstra_predecessor_and_distance): counter tie-break, cutoff pruning and the record of equal-cost predecessors; paths follow the first recorded predecessor, as the harness does. Snapping, profiles and segment listing are Skillpack code (tool/mapdata.py, tool/main.py).

## Evidence and human review

Fixture graphs are synthetic (CC0). Expected matrices and isochrone counts were produced by installed networkx 3.6.1 dijkstra_predecessor_and_distance on a DiGraph built from the same Skillpack graph builder; the harness checks that installed astar.py and weighted.py are byte-identical to the pinned upstream copies. Graph construction is shared code, so only the search is independently compared.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI by Skillpack contributors; no upstream endorsement, formal verification or independent certification is implied.
