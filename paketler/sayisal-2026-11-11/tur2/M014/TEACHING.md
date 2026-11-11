# Learning path: Cephes regularized incomplete gamma lower and upper tails

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Define normalization
Write the lower and upper integrals divided by Gamma(a). Verify the boundary P(a,0)=0 and P+Q=1, but understand that this identity alone cannot verify either tail.

## 2. Choose the stable branch
Trace why a power series is used on the left and a continued fraction on the right. Find the intermediate ax=a*log(x)-x-lgamma(a).

## 3. Control dynamic range
Explain fraction renormalization and the underflow guard. Compare absolute and relative tolerance on the published 10,.05 tiny-tail fixture; an absolute tolerance of 1e-10 would be meaningless there.

## 4. Interpret honestly
Vary a and x near the branch boundary, inspect complements and compare the pinned C fixtures. Explain when this old algorithm is unsuitable for extreme-tail inference.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
