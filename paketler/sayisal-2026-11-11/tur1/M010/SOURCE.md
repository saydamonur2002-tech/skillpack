# Source audit

Upstream: https://github.com/epfl-lts2/pygsp

Pinned commit: `4716b12c470c579e3f477f2d1c1d99752c73252d`

Observed stars: 551; repository created 2014. This is repository age, not proof of 50-year-old source code.

License: BSD-3-Clause. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2014, EPFL LTS2

## Faithfulness and changes

Ports Graph.compute_laplacian combinatorial and normalized formulas using dense Python lists, with directed mean-symmetrization and zero normalized diagonal for isolated vertices. Weighted degrees come from the symmetrized matrix.

## Reference values

pygsp/graphs/graph.py:545-577 contains four explicit directed/undirected Laplacian matrices. compute_laplacian:618-627 specifies isolated-node handling.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [pygsp/graphs/graph.py](https://github.com/epfl-lts2/pygsp/blob/4716b12c470c579e3f477f2d1c1d99752c73252d/pygsp/graphs/graph.py) — SHA-256 `1b1192f04b4663c1f2dfcdb27aea932e5028010e16d2ba70d8bb6a249120cac7` (complete original file).
