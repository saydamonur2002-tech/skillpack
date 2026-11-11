# Learning path: IAU 2006 frame-bias and precession matrix from TT

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Connect frames and dates
State the GCRS input and mean-of-date output frames, TT timescale and matrix-on-column-vector convention before performing arithmetic.

## 2. Reconstruct the angles
Evaluate the four upstream polynomials at the published epoch. Keep arcseconds-to-radians conversion explicit and compare mean obliquity to the separate source routine.

## 3. Audit rotation order
Multiply the four axis rotations by hand for a small example. Explain why changing signs, transposing or reordering the factors can yield an orthogonal but wrong reference-frame transform.

## 4. Validate beyond appearance
Check every published matrix entry, then R*R^T≈I and det(R)≈1. Explain why orthogonality alone cannot validate the epoch, conventions or IAU coefficients.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
