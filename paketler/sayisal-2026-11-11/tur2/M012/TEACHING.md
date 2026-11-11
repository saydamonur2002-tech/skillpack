# Learning path: QUADPACK 21-point Gauss–Kronrod panel and error diagnostics

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Build the nested rule
Locate every Gauss-10 node within the Kronrod-21 set. Explain why the extra evaluations can estimate error without evaluating a second disjoint rule.

## 2. Reproduce the diagnostics
Integrate sin(x) on [0,pi]. Compute resg, resk, resabs and resasc separately and find the roundoff floor in the Fortran source.

## 3. Distinguish estimate from guarantee
Use a high-degree polynomial or oscillatory integrand. A small pairwise difference can miss narrow or aliased structure: do not present a single-panel estimate as a certified bound.

## 4. Design the next algorithm
Describe, without claiming it is implemented, how a largest-error adaptive subdivision driver could reuse this panel kernel. Explain why QAGS additionally needs extrapolation and termination logic.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
