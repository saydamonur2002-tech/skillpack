# Learning path: Spherical great-circle distance and bearings

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Draw a great circle and derive the haversine central angle.

## 2. Separate the dimensionless central angle from radius times angle, which has length units.

## 3. Compute the initial and final forward bearings; compare against the upstream Cambridge/Paris fixture.

## 4. Compare this pack with M003 on the same coordinates and explain the model difference; never quietly interchange the two results.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
