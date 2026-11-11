#!/usr/bin/env python3
"""Median absolute deviation and Gaussian scale. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import statistics

def calculate(p):
    xs=p["data"];center=statistics.median(xs);mad=statistics.median([abs(v-center) for v in xs])
    return {"median":center,"mad":mad,"gaussian_scaled_mad":mad*1.482602218505602}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
