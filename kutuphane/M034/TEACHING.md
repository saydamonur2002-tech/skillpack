# Learning path: Static map renderer: GeoJSON to SVG (with optional offline road basemap)

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Web Mercator pixels
Compute px for (-179, 85) at zoom 9 by hand and compare with [364, 215].

## 2. Integer versus fractional zoom
Explain why zoom 9 rounds to whole pixels but 8.6574 does not.

## 3. Simplification
Render the demo route and count path points before and after simplification.

## 4. Reading the SVG
Open the SVG in a text editor: find the basemap, route, marker and attribution layers.

## Human check

Run `python tool/main.py < example.json` with `SKILLPACK_MAP_DATA=tests/fixtures` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
