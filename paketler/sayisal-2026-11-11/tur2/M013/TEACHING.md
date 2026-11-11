# Learning path: Fehlberg 7(8) fixed-step affine linear ODE propagation

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Understand a tableau
Map each b coefficient in the Fortran source onto a row of A in the port. Show which prior derivative vectors each stage is allowed to use.

## 2. Check an exact solution
For matrix=[[-1,-5],[1,1]], y(0)=[0,2], differentiate the published y(t)=[-5*sin(2t),2*cos(2t)+sin(2t)] and verify y'=A*y before running the solver.

## 3. Audit the units of error
The original terr is a combination of derivatives, not states: multiply by h to compare embedded state formulas. Explain why the last local indicator cannot bound accumulated global error.

## 4. Observe convergence safely
Halve a fixed step on the analytic system and compare state error. Try reversed time and a zero interval. Identify when stiffness or overflow requires a different solver instead of increasing confidence in an unvalidated estimate.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
