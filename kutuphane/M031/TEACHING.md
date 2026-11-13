# Learning path: Travel-time/distance matrix and isochrone (reachable roads within N minutes)

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Matrix from one Dijkstra per origin
Explain why one single-source run answers a whole row of the matrix.

## 2. Asymmetry
Compare car times A to B and B to A in the first case; explain the one-way streets.

## 3. Cutoff
Run the 2-minute walk and count the reached vertices by hand from 5 km/h.

## 4. Isochrone shape
Draw the reachable segments with M034 and discuss why the edge looks ragged.

## Human check

Run `python tool/main.py < example.json` with `SKILLPACK_MAP_DATA=tests/fixtures` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
