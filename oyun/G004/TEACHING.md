# Learning path: 2D collision detection and push-out vector (SAT.js: circles, boxes, convex polygons)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Circles
Two radius-20 circles 30 apart overlap by 10: check overlap and overlap_n.

## 2. Corner regions
Move a circle around a box corner and see when the Voronoi corner case applies.

## 3. Push out
Apply push_a to A and run the test again: it should just touch.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that car/pedestrian radii and building boxes match the drawn sprites so hits look fair.
