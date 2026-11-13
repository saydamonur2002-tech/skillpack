# Demo map data: Kadıköy (Istanbul) — ODbL

**© OpenStreetMap contributors.** This folder contains data from OpenStreetMap, available under the
Open Database License 1.0 (ODbL): https://www.openstreetmap.org/copyright — full text in `LICENSE-ODbL-1.0.txt`.
The code packs (M003–M034) are under their own permissive licenses; this data is licensed separately and is NOT covered by them.

## What is here

| File | Content | Features |
|---|---|---:|
| demo_kadikoy_roads.geojson | Road/path LineStrings with OSM tags highway, name, oneway, maxspeed, junction, access, foot, bicycle, motor_vehicle | 2093 |
| demo_kadikoy_places.geojson | Named POIs (amenity, shop, tourism, leisure, healthcare, public transport, place …) as Points, plus one representative point per named street (category "street") | 3078 |
| demo_kadikoy_areas.geojson | Parks, gardens, water, cemeteries, schools, hospitals, piers (Polygons) and coastline (LineStrings) | 333 |

- Extract area: longitude 29.015–29.045, latitude 40.975–41.000 (Kadıköy centre, Moda, Yeldeğirmeni, Söğütlüçeşme, part of Fenerbahçe), roughly 2.5 km × 2.8 km. Ways crossing the edge are kept whole.
- Source: OpenStreetMap API 0.6 `/map` calls on 12 small bounding boxes, 2026-11-12 (Europe/Istanbul). Converted with a small script that keeps only the tags listed above; coordinates rounded to 7 decimals; street points and way centroids are derived values.
- Not included: buildings, house numbers as searchable addresses, turn restrictions, relations (multipolygons, routes), public-transport timetables, ferries as routable links, sea polygons.

## Attribution when you show results

Any map, route or list made from this data must credit **"© OpenStreetMap contributors"** (the renderer M034 adds this automatically when a basemap is used).
If you publicly share a modified version of the database itself, ODbL share-alike applies to that database. Produced works (images, routes) need attribution only.

## Using your own data

Put your own files in this folder (or point `SKILLPACK_MAP_DATA` at another folder) and pass their name as `dataset`:
`myarea_roads.geojson`, `myarea_places.geojson` / `myarea_places.csv` (`name,category,lat,lon`), `myarea_areas.geojson`, or a small `myarea.osm` XML extract. OSM-derived files you add stay under ODbL.
