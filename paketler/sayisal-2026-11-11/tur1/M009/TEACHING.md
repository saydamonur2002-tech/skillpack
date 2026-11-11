# Learning path: Masked image center of mass

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Define row/column indices and distinguish x,y output from array row,column order.

## 2. Compute zeroth and first intensity moments, then divide to obtain center of mass.

## 3. Mask one large contaminated pixel and reproduce the upstream Gaussian-center tolerance.

## 4. Explain background bias, truncated-image bias and why this estimator is not a fitted source position or a detector.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
