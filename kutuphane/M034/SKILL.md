---
name: m034
description: Draw points, routes, isochrones and polygons as a self-contained SVG map in Web Mercator (no tiles, no network), optionally over the roads, parks, water and coastline of a local dataset, with labels, A/B markers, scale bar, north arrow and OpenStreetMap attribution. Returns the SVG text and the GeoJSON; can also save both to the configured output folder. Also converts lon/lat to web-map pixels and back.
---

# Static map renderer: GeoJSON to SVG (with optional offline road basemap)

Draw points, routes, isochrones and polygons as a self-contained SVG map in Web Mercator (no tiles, no network), optionally over the roads, parks, water and coastline of a local dataset, with labels, A/B markers, scale bar, north arrow and OpenStreetMap attribution. Returns the SVG text and the GeoJSON; can also save both to the configured output folder. Also converts lon/lat to web-map pixels and back.

## When and how to use

Pass result.feature from M030/M031 and result.features from M033 (plus start/end points) as features, set basemap to the dataset name, and show the returned SVG to the user (for example as an artifact) or open the saved file in a browser. Use only this bounded deterministic operation. Read manifest.json for the exact schema; do not guess missing data, coerce strings/booleans or invent reference values.

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
    "m034": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M034/mcp/server.py"
      ],
      "env": {
        "SKILLPACK_MAP_DATA": "/ABSOLUTE/PATH/TO/map_data",
        "SKILLPACK_MAP_OUTPUT": "/ABSOLUTE/PATH/TO/map_output"
      }
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m034`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters; the only file write is the optional save_name output described below. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

A static schematic map, not a tiled web map: no satellite or aerial imagery, terrain, buildings, street view, live traffic or interactive panning. The basemap draws roads, parks/water areas and coastline from the local dataset only; open sea is not filled, so coasts appear as lines. Very large views drop footways/service roads (more than 3500 roads) and refuse SVGs above 900 kB. Labels are drawn without collision avoidance. Fit-to-view uses a fractional zoom up to 19.5. Saving writes only two new files named by save_name into SKILLPACK_MAP_OUTPUT and refuses to overwrite.

## Faithfulness

Projection is a port of sphericalmercator v1.1.0 px and ll (256-pixel tiles), including the separate integer-zoom branch with cached per-zoom constants and Math.round, the sin clamp at plus/minus 0.9999 and the upper clamp at the world size. Polylines are simplified in pixel space with the simplify-js port from M021 (tolerance 0.7 px basemap, 0.4 px features). Fit-to-view, styling, labels, scale bar and file saving are Skillpack code; render always uses the fractional branch.

## Evidence and human review

px and ll inputs and their literal expectations are from upstream test/sphericalmercator.test.js. All full outputs were generated by executing pinned upstream sphericalmercator.js in Node, not this port; supplementary cases are labelled. The SVG renderer has no upstream counterpart and is covered by structural, determinism, escaping and file-safety tests.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI by Skillpack contributors; no upstream endorsement, formal verification or independent certification is implied.
