# Learning path: Top-down tile city generator (roads, sidewalks, buildings, parks, points of interest)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Seed
Generate seed 2026 twice and compare: identical. Change the seed by 1 and compare again.

## 2. Blocks
Find a block in the tiles and point out its sidewalk ring and the building or park inside.

## 3. Points
Check that every landmark has road_access next to it so a car can stop there.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that the city size, block size and park share give a fun drive (not too empty, not a maze) and that landmarks are spread out.
