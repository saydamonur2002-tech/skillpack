# Learning path: Mercator rhumb-line distance and constant bearing

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Draw a straight line on a Mercator map and identify its constant compass bearing.

## 2. Compute the logarithmic latitude difference and stretch factor q.

## 3. Explain the east-west 0/0 limit and the short antimeridian longitude branch.

## 4. Reproduce the upstream Dover/Calais example; contrast rhumb distance with M004 great-circle distance and identify when a constant bearing is useful.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
