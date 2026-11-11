# Learning path: IAU 2000 Earth rotation angle from split UT1 Julian date

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Understand UT1
Explain why Earth rotation follows UT1 and why the tool cannot silently substitute UTC or TT. Identify the missing external observations needed for that conversion.

## 2. Preserve the split
Evaluate a date split at J2000 and at MJD zero. Trace the sorted parts and fmod operations, especially for negative fractional parts.

## 3. Reproduce the reference
Calculate the upstream 54388-MJD fixture and compare the reported radians and degrees. Check the normalization interval without confusing it with a sidereal-time angle.

## 4. Define the boundary of the tool
List the missing polar-motion, precession, nutation and observer transformations needed for a full terrestrial-to-celestial coordinate pipeline. Do not imply this single angle supplies them.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
