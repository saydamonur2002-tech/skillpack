# Source audit

Upstream: https://github.com/astropy/photutils

Pinned commit: `0eb74eb4bc450c3d1476d26b774c0011c138bf49`

Observed stars: 316; repository created 2011. This is repository age, not proof of 50-year-old source code.

License: BSD-3-Clause. Full original text is in LICENSE and upstream/UPSTREAM_LICENSE.

## Original copyright

Copyright (c) 2011-2026, Photutils Developers

## Faithfulness and changes

Ports the 2D finite/masked branch of centroid_com: sum(index*data)/sum(data), reversed to x,y order. Upstream undefined NaN output for near-zero total becomes a structured error. Nonfinite pixels are rejected, not automatically masked.

## Reference values

photutils/centroids/tests/test_core.py:56-82 checks centers (25.7,26.2) for 8 Gaussian parameter combinations and their masked versions. helpers.py defines the Gaussian source model.

Expected values are frozen in tests/references.json. The origin field distinguishes original fixtures from adaptations and supplementary properties. No fabricated benchmark accuracy or unsupported precision is claimed.

## Evidence

- [photutils/centroids/core.py](https://github.com/astropy/photutils/blob/0eb74eb4bc450c3d1476d26b774c0011c138bf49/photutils/centroids/core.py) — SHA-256 `88098f5455d9fe5875c3634192fe0397ea913b90769929c330e7b48a0ebccad2` (complete original file).
- [photutils/centroids/tests/test_core.py](https://github.com/astropy/photutils/blob/0eb74eb4bc450c3d1476d26b774c0011c138bf49/photutils/centroids/tests/test_core.py) — SHA-256 `f4f829b315dcae3a3eebf3f58f0c1fe72dfa571fe510d86212543467a163c6b1` (complete original file).
- [photutils/centroids/tests/helpers.py](https://github.com/astropy/photutils/blob/0eb74eb4bc450c3d1476d26b774c0011c138bf49/photutils/centroids/tests/helpers.py) — SHA-256 `0706a8e97018994d24c8e65c57accc373b0502bbfb946848a80903ce4268fc2d` (complete original file).
