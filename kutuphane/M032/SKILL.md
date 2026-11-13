---
name: m032
description: Find places by name in a local places dataset with Turkish-aware fuzzy matching (Jaro-Winkler; İ/ı, ş, ğ, ç, ö, ü folded), optionally filtered by category and ranked by distance to a reference point; or reverse geocode a coordinate to the nearest named street, nearest named area (mahalle/quarter) and nearby places. Answers "Moda Eczanesi nerede?" and "bu nokta hangi sokakta?".
---

# Offline place search (geocode) and reverse geocode on a local places file

Find places by name in a local places dataset with Turkish-aware fuzzy matching (Jaro-Winkler; İ/ı, ş, ğ, ç, ö, ü folded), optionally filtered by category and ranked by distance to a reference point; or reverse geocode a coordinate to the nearest named street, nearest named area (mahalle/quarter) and nearby places. Answers "Moda Eczanesi nerede?" and "bu nokta hangi sokakta?".

## When and how to use

Search first, show the top candidates, and pass the confirmed coordinates to M030/M031/M034. Use reverse to describe a clicked or computed point. Use only this bounded deterministic operation. Read manifest.json for the exact schema; do not guess missing data, coerce strings/booleans or invent reference values.

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
    "m032": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M032/mcp/server.py"
      ],
      "env": {
        "SKILLPACK_MAP_DATA": "/ABSOLUTE/PATH/TO/map_data"
      }
    }
  }
}
```

The official FastMCP stdio server exposes exactly `skillpack_m032`. It validates the advertised input schema, enforces a 65536-byte UTF-8 JSON limit, runs one fixed local script at a time and kills/reaps it after 10 seconds. There are no expression-code, arbitrary path, shell or network parameters. This is not a security sandbox for hostile code or a statement about the hosting AI client privacy settings.

## Scope and failure

Name lookup in the local file only: no house-number interpolation, no postal addresses, no spelling suggestions beyond Jaro-Winkler similarity, and no ranking by popularity. Several places can share a name (chains, stops); always show the candidates with category and coordinates and let the human pick. Score = max(JW(query, name), 0.95 x best JW over name word windows of the query length) after Turkish folding; default threshold 0.85. Reverse geocoding returns the nearest representative point of a named street and the nearest named place point (quarter, neighbourhood, square ...), not a containing polygon, within max_distance_m (default 500). Category words may be Turkish or English (eczane -> pharmacy).

## Faithfulness

Jaro-Winkler is the M023 port of jellyfish _jellyfish.py _jaro_winkler (winklerize on, long_tolerance off), unchanged. Distances use the haversine formula in the same operation order as geodesy latlon-spherical distanceTo (R = 6371 km). Normalisation, word-window scoring, category aliases and tie-breaking (score, distance to near point, file order) are Skillpack rules documented here.

## Evidence and human review

Fixture places are synthetic (CC0). Expected matches, scores, counts and reverse results were produced by reference/upstream_harness.py: an independent re-implementation of the documented ranking that calls the pinned upstream jellyfish pure-Python jaro_winkler_similarity and Skillpack's shared file loader, without importing the port. jellyfish fixtures themselves are covered by pack M023.

Read SOURCE.md and TEACHING.md. Cite the exact origin of any reference; do not describe a generated fixture as an original upstream test. Preserve license and attribution notices in redistribution. This adaptation and documentation were generated with AI by Skillpack contributors; no upstream endorsement, formal verification or independent certification is implied.
