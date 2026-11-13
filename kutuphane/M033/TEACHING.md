# Learning path: Nearby places: nearest-N and within-radius search by category

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Ellipsoidal distance
Compare one result with M028 haversine distance and explain the small difference.

## 2. Stable ordering
Find two places at the same rounded distance and confirm they keep dataset order.

## 3. Aliases
Run with categories ["eczane"] and read categories_used.

## 4. What is not answered
Explain why opening_hours cannot be evaluated here and what data would be needed.

## Human check

Run `python tool/main.py < example.json` with `SKILLPACK_MAP_DATA=tests/fixtures` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
