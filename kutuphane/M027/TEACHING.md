# Learning path: Spherical area of GeoJSON polygons (m², hectares, km²)

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Area on a sphere
Compare the 0.01 degree square area with a flat estimate 0.01*111320 * 0.01*111320*cos(41 deg) and explain the difference.

## 2. Holes
Run the hole case and check that the result equals outer minus hole areas from ring_signed_areas_m2.

## 3. Orientation
Reverse a ring and show the signed area flips; explain why polygon area uses absolute values.

## 4. Accuracy
Compare the Illinois area with an official figure and discuss sphere versus ellipsoid.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
