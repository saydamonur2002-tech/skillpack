# Learning path: A* path finding on a tile grid (python-pathfinding)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Manhattan A*
Trace the small maze by hand: why does the path go around the wall at column 3?

## 2. Costs
Change R from 3 to 1 for pedestrians and see them cut across roads.

## 3. Unreachable
Read the found=false answer and decide whether the map or the mission is wrong.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that pedestrians stay on sidewalks and parks, cars stay on roads, and the cost for pedestrians crossing a road is acceptable.
