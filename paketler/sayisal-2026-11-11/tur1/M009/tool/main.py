#!/usr/bin/env python3
"""Masked image center of mass. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
def calculate(p):
    data=p["data"];ny=len(data);nx=len(data[0]);mask=p.get("mask")
    if any(len(r)!=nx for r in data):raise ValueError("Image must be rectangular")
    if nx*ny>4096:raise ValueError("At most 4096 pixels")
    if mask is not None and (len(mask)!=ny or any(len(r)!=nx for r in mask)):raise ValueError("mask shape differs from image")
    total=sx=sy=0.0
    for y,row in enumerate(data):
        for x,v in enumerate(row):
            if mask is None or not mask[y][x]:total+=v;sx+=x*v;sy+=y*v
    if abs(total)<1e-30:raise ValueError("Centroid undefined: absolute total below 1e-30")
    return {"x":sx/total,"y":sy/total,"total":total}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
