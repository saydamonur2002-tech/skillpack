# Learning path: Bracketed polynomial roots with safeguarded Brent interpolation

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Establish the mathematical bracket
Evaluate the polynomial at both endpoints. Show why opposite signs plus continuity imply at least one real root, but do not imply uniqueness.

## 2. Trace the safeguards
Hand-trace a secant step, an inverse-quadratic proposal and a rejected interpolation that forces bisection. Compare source variables xpre/xcur/xblk to the Python port, especially the sequential C swap.

## 3. Read tolerances as intervals
Run x^2-1 on [0.5,sqrt(3)] and then reverse the endpoints. Compare root error and polynomial residual: they have different units and neither is a condition-number estimate.

## 4. Probe failure deliberately
Try x^2+1 on [-1,1] and a one-iteration budget. Explain why an explicit failure is preferable to silently returning the last iterate.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
