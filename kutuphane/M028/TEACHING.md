# Learning path: Destination point, bearing, midpoint and cross-track distance on a sphere

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Haversine by hand
Compute Cambridge to Paris with a calculator and compare with 404279 m.

## 2. Initial versus final bearing
Explain why the bearing changes along a great circle (156.2 versus 157.9 degrees).

## 3. Destination point
Walk 1 km south-east from the Kadikoy pier and check the result on a map.

## 4. Cross-track sign
Use the cross-track case and explain what a negative value means relative to the path direction.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
