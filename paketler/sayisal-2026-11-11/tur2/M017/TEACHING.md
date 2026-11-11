# Learning path: Linear-time partial-pivot tridiagonal system solve

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Exploit the band
Write the three diagonal vectors as a dense matrix by hand and count the O(n) stored numbers. Contrast this with dense LU.

## 2. See why Thomas can fail
Use a nonsingular matrix with a zero first diagonal. Explain why a no-pivot recurrence divides by zero while DGTSV swaps adjacent equations.

## 3. Track the fill
Follow one swap and identify the second superdiagonal stored in the overwritten lower array. Verify all three terms in the backward-substitution recurrence.

## 4. Validate edge cases
Solve n=1 and n=2, then repeated-pivot systems. Reconstruct A*x-b without allocating a dense matrix and explain the limits of a residual check.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
