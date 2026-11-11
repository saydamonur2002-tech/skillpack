#!/usr/bin/env python3
"""One-level orthonormal Haar analysis and reconstruction. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    xs=p["data"]
    if len(xs)%2:raise ValueError("Even sample count required; no implicit padding")
    k=math.sqrt(0.5)
    approx=[(a+b)*k for a,b in zip(xs[::2],xs[1::2])]
    detail=[(a-b)*k for a,b in zip(xs[::2],xs[1::2])]
    low=[];high=[];reconstructed=[]
    for a,d in zip(approx,detail):
        low.extend([a*k,a*k]);high.extend([d*k,-d*k]);reconstructed.extend([(a+d)*k,(a-d)*k])
    return {"approximation":approx,"detail":detail,"lowpass_reconstruction":low,"highpass_reconstruction":high,"reconstructed":reconstructed}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
