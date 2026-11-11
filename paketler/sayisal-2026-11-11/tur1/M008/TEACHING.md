# Learning path: One-level orthonormal Haar analysis and reconstruction

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Compute pair sum/difference divided by sqrt(2), explaining orthonormal normalization.

## 2. Reconstruct each pair from its approximation and detail coefficients.

## 3. Compare separate low/high reconstructions with the upstream real-component fixture and verify they sum to the input.

## 4. Check energy preservation on a synthetic vector, and explain why perfect reconstruction alone does not establish a useful denoising threshold.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
