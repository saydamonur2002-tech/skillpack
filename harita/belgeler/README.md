# Map skillpacks (2026-11-12)

Fifteen single-tool, offline MCP skill packs that together give an LLM client the core functions of a simple street map: geocoding, reverse geocoding, routing, travel-time matrices and isochrones, nearby search, geometry helpers and SVG map rendering. Code computes; the model chooses the tool and explains; a human approves. Turkish user guide: `README_TR.md`.

| Pack | Server name | Function | Upstream (pinned) | License |
|---|---|---|---|---|
| M026 | poligon-icinde-mi | Point in polygon, bounds, centre | manuelbieh/geolib v2.0.24 | MIT |
| M027 | alan-hesapla | Spherical polygon area | mapbox/geojson-area | BSD-2-Clause |
| M028 | yon-ve-varis-noktasi | Bearing, destination, midpoint, cross-track, compass (EN/TR) | chrisveness/geodesy | MIT |
| M029 | harita-karosu | Slippy-map tile math | mapbox/tilebelt v1.0.1 | MIT |
| M030 | rota | Offline routing (A*/Dijkstra) car/walk/bike, via points, turn list, GeoJSON | networkx 3.6.1 (+ geodesy) | BSD-3-Clause |
| M031 | sure-matrisi-izokron | Duration/distance matrix ≤25×25, isochrone ≤60 min | networkx 3.6.1 (+ geodesy) | BSD-3-Clause |
| M032 | yer-ara | Geocode search / reverse, Turkish folding, Jaro-Winkler | jamesturk/jellyfish (+ geodesy) | MIT |
| M033 | yakindakiler | Nearby POIs by category with Turkish aliases (Vincenty distances) | manuelbieh/geolib v2.0.24 | MIT |
| M034 | harita-ciz | SVG map renderer, Web-Mercator project/unproject, optional basemap | mapbox/sphericalmercator v1.1.0 (+ simplify-js) | BSD-3-Clause |
| M003 | mesafe-vincenty | Ellipsoidal (Vincenty) distance | chrisveness/geodesy | MIT |
| M004 | mesafe-buyuk-daire | Great-circle distance/bearing | chrisveness/geodesy | MIT |
| M005 | loksodrom | Rhumb-line distance/bearing | chrisveness/geodesy | MIT |
| M021 | cizgi-sadelestir | Ramer–Douglas–Peucker simplification | mourner/simplify-js | BSD-2-Clause |
| M024 | polyline-kodla | Encoded polyline encode/decode | mapbox/polyline | BSD-3-Clause |
| M025 | geohash | Geohash encode/decode/neighbours | sunng87/node-geohash | MIT |

M003–M005, M021, M024 and M025 are reused unchanged from earlier rounds.

## Layout

- `Mxxx/` — one pack each: `manifest.json` (provenance, commit pin, budgets, MCP metadata), `SKILL.md`, `TEACHING.md`, `tool/` (deterministic JSON CLI), `mcp/server.py` (FastMCP, stdio, exactly one tool, 64 KB input, 10 s timeout with child kill), `tests/`, `upstream/` (byte-identical upstream files + license), `reference/` (optional rerun against the real upstream code), `FILES.sha256`.
- `map_data/` — demo dataset `demo_kadikoy` (OpenStreetMap extract, ~2.5 × 2.8 km of Kadıköy). **© OpenStreetMap contributors, ODbL 1.0**, licensed separately from the code.
- `examples/` — `demo_chain.py` (geocode → route → nearby → render) and its outputs; `example_route.png`.
- `claude_desktop_config.json` — registration snippet for all 15 servers (replace `/MUTLAK/YOL` placeholders).
- `catalog.json`, `LICENSE_INDEX.md`, `TEST_RESULTS.json`, `tests/` (cross-pack: real MCP stdio, watchdog/kill, release audit, upstream reruns, demo end-to-end).

## Data access model

Data packs (M030–M034) take a dataset **name**, never a path. Names resolve only inside `SKILLPACK_MAP_DATA` (or `../map_data`). Accepted layers: `name_roads.geojson`, `name_places.geojson|.csv`, `name_areas.geojson`, `name.osm`; 64 MiB per file. Only M034 writes, and only when `save_name` is given and `SKILLPACK_MAP_OUTPUT` is set; it never overwrites. No network access, telemetry or API keys anywhere.

## Running tests

```
python3 -m venv .venv && .venv/bin/pip install -r requirements-test.txt
.venv/bin/python -m pytest
```

Upstream reruns need Node.js for the JavaScript upstreams and skip cleanly without it.

## Limitations

Free-flow speeds only (no live traffic), no turn restrictions, public transport or ferries; no satellite imagery, street view, opening-hours evaluation or reviews. The isochrone returns reachable road segments, not a hull polygon. `.osm` inputs are parsed on every call, so large areas should be converted to GeoJSON to stay within the 10 s budget. The demo extract is a 2026-11-12 snapshot and may be incomplete.
