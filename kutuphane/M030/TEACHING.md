# Learning path: Offline road routing (A*/Dijkstra) with distance, time and street list

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Graph from lines
Open tests/fixtures/grid_roads.geojson and draw the 4 x 4 grid; mark the one-way streets.

## 2. Dijkstra by hand
Run the Dijkstra case and verify the first three settled vertices by hand.

## 3. Why A* is still exact
Explain why haversine distance divided by the top speed never overestimates travel time.

## 4. Profiles
Compare car, walk and bike routes for the one-way case and explain each difference.

## Human check

Run `python tool/main.py < example.json` with `SKILLPACK_MAP_DATA=tests/fixtures` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
