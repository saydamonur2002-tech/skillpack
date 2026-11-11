# Learning path: Proleptic Gregorian date to two-part Julian date and MJD

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Learn the numbering conventions
Contrast astronomical year 0 with historical BC numbering, and proleptic Gregorian rules with actual local adoption dates.

## 2. Derive the split
Explain JD=djm0+djm and why ERFA returns 2400000.5 separately. Reproduce the literal 2003-06-01 fixture with integer arithmetic.

## 3. Audit integer semantics
Compute (month-14)/12 in C and Python for January and March. Show why replacing every division by Python floor division would be wrong.

## 4. Keep timescales separate
Try invalid century leap days and valid year-zero February 29. Explain why a midnight calendar JD alone does not provide UT1, TT, a timezone or leap-second handling.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
