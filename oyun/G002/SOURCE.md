# Source and changes: Top-down tile city generator (roads, sidewalks, buildings, parks, points of interest)

Original work by Skillpack contributors (MIT). No third-party code.

## Design notes

Original algorithm by Skillpack contributors. Random numbers come from xorshift32 (G. Marsaglia, 'Xorshift RNGs', J. Stat. Software 8(14), 2003; shift triple 13,17,5) seeded with the given seed (0 replaced by 0x9E3779B9). Axis split: edge road, then blocks of random width, final road on the far edge. Road connectivity is verified by flood fill and reported.

## Reference values

tests/references.json holds frozen golden outputs of this original generator (regression only, not an external truth). Independent checks: the xorshift32 first output for seed 1 is 270369 (published sequence), and invariant tests check edge roads, block rings, connectivity, point placement and determinism.
