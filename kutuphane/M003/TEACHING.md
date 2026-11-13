# Learning path: WGS84 Vincenty inverse geodesic

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Distinguish a sphere from the WGS84 ellipsoid and identify a, b and flattening.

## 2. Compute reduced latitudes, iterate auxiliary longitude and examine the convergence criterion.

## 3. Recover arc correction, distance and the two forward azimuths; understand that final bearing is not the reverse bearing.

## 4. Reproduce the upstream 969954.166 m example, the antimeridian case and a known non-convergent near-antipodal case. Explain why no answer is safer than an unannounced fallback.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
