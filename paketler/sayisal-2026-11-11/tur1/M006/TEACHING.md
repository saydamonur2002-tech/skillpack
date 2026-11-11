# Learning path: Robust biweight location, midvariance and scale

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Compute the sample median and median absolute deviation by hand.

## 2. Form u=(x-M)/(c*MAD), reject absolute u >=1 and derive the location weights.

## 3. Compute the scale numerator and denominator, and compare total versus retained n.

## 4. Reproduce [1,3,5,500,2] -> location 2.7456117 and midvariance 2.9238456, then explain why these robust estimates are not automatic anomaly or safety decisions.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
