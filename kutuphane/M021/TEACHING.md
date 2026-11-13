# Learning path: Polyline simplification with radial pre-filter and Ramer-Douglas-Peucker

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Squared distances
Compute by hand the squared distance from point (1, 1) to segment (0, 0)-(2, 0) and to segment (0, 0)-(0.5, 0). Note the clamp when the projection parameter t leaves [0, 1].

## 2. Radial pre-filter
Walk the ZIG example with tolerance 1 and mark which points are dropped because they are within tolerance of the previously kept point. Explain why the last point is always kept.

## 3. Douglas-Peucker recursion
Draw the first and last point, find the farthest intermediate point, and split. Compare your hand trace with kept_indices for highest_quality=true.

## 4. Quality versus speed
Run the 1k fixture with and without highest_quality and compare output_count. Explain why tolerance is in input units and what happens with latitude/longitude degrees.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
