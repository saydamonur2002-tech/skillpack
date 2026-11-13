# Learning path: Geohash encode, decode with bounding box, and eight neighbours

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Bisection by hand
Encode latitude 32, longitude 117 to 15 bits: alternate longitude and latitude halving and write 1 for the upper half. Group into 5-bit symbols and confirm wte.

## 2. Cell, not point
Decode ww8p1r4t8 and read the error fields: the geohash names a rectangle, and the centre is only a representative.

## 3. Neighbours and wrap
List neighbours of 21202 and explain why the western ones start with r (longitude wrap across 180 degrees).

## 4. Prefix caution
Show two nearby points on either side of a cell boundary with different prefixes; explain why proximity searches use neighbours, not only prefixes.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
