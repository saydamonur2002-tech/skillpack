# Learning path: Unblocked partial-pivot LU factorization and dense linear solve

## Prerequisites

Real arithmetic, algebra and JSON; basic calculus for integration/ODE/special functions and linear algebra for matrix packs. Read the input units and assumptions first.

## 1. Connect elimination to factors
Hand-factor a small matrix, recording multipliers below the diagonal. Explain why the packed output stores unit-diagonal L and upper U in the same array.

## 2. Understand pivot permutations
Force an initial row swap with a zero diagonal entry. Apply the returned 1-based swaps in order and verify that the resulting P*A equals L*U.

## 3. Separate factorization from solve
Apply the same swaps to b, then perform forward and backward substitution. Read the generated native-reference harness so factorization gold is not confused with an upstream asserted solution.

## 4. Assess conditioning carefully
Compute residual and scaled backward error. Give an ill-conditioned example where a small residual says little about the accuracy of x; this pack deliberately makes no condition-number claim.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream excerpt; identify whether it is literal, native-generated, analytic or a cross-library check. Explain every returned field and one rejection case. Human review is required for consequential use.
