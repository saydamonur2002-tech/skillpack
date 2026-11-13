# Learning path: Slippy-map tile math: lon/lat to z/x/y, tile bounds, quadkeys, parent and children

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Tile grid
At zoom z the world is 2^z by 2^z tiles. Compute the Moda tile at zoom 16 by hand from the fractional position.

## 2. Mercator stretch
Compare tile heights in degrees near the equator and at 60 degrees north using tile_to_bbox.

## 3. Quadkeys
Convert [11, 3, 8] to 00001033 digit by digit (x bit + 2 * y bit).

## 4. Covering tile
Explain why the Kadikoy box maps to one tile and why a box crossing 0,0 needs zoom 0.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
