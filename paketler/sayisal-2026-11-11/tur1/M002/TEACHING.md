# Learning path: Fornberg arbitrary-grid finite-difference weights

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Derive the three-point central first difference from Taylor expansions.

## 2. Use the five-point upstream matrix to check the moments of each derivative row.

## 3. Follow the recurrence as a new node is added; check that old weights are read before replacement.

## 4. Evaluate a derivative from sampled data, then perturb sample values and describe the noise amplification. Do not present interpolation exactness as a numerical error guarantee.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
