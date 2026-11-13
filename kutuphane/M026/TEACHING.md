# Learning path: Point-in-polygon, bounding box and centre of a polygon

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Ray casting by hand
Draw the square case and a horizontal-in-longitude ray: count edge crossings for an inside and an outside point and confirm odd/even.

## 2. Holes
Run the hole case: explain why the point in the hole is outside even though it is inside the outer ring.

## 3. Concave shapes and centres
Use the L-shaped polygon: show that the centre of bounds can sit outside the polygon, then verify with contains.

## 4. Edges are ambiguous
Test a point exactly on an edge and explain why a planar ray test is not a survey-grade boundary decision.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
