# Learning path: Cephes regularized incomplete beta with symmetry and dual fractions

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Derive reflection
From the integral, prove I_x(a,b)=1-I_(1-x)(b,a). Explain why a reflected evaluation can avoid a poorly convergent region.

## 2. Trace all three expansions
Choose one input for the power series and one for each fraction. Compare the k1..k8 updates against incbet.c and locate the rescaling conditions.

## 3. Verify a difficult regression
Reproduce the upstream .0342,171,1e-10 value with the published tolerance. Explain why direct products of gamma functions can overflow even when the normalized answer is moderate.

## 4. Report bounded accuracy
Inspect x=0 and x=1, then approach both limits. Explain complement saturation, the iteration cap and why this tool must not invent a significance threshold.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
