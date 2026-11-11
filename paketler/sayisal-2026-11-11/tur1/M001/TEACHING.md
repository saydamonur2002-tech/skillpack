# Learning path: Consistent-end cubic spline and derivatives

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Plot the knot pairs and distinguish interpolation from regression.

## 2. Fit the cubic through the first four knots and compute its endpoint second derivative; repeat at the right.

## 3. Enforce C2 continuity by solving the tridiagonal system, then evaluate each cubic and its derivatives.

## 4. Reproduce the upstream linear/extrapolation fixture and sine error bound. Finally compare consistent versus natural endpoints; explain why extrapolation is not a forecast.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
