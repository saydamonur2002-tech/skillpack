# Learning path: Weighted graph combinatorial and normalized Laplacians

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Build weighted degrees from a small adjacency matrix and compute D-W by hand.

## 2. Normalize by inverse square-root degrees and explain the isolated-vertex convention.

## 3. Reproduce both directed and undirected example matrices from upstream docs.

## 4. Test symmetry and the combinatorial constant-vector nullspace, then explain that averaging a directed graph discards causal or flow direction.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
