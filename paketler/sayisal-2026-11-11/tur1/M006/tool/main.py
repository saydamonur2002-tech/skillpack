#!/usr/bin/env python3
"""Robust biweight location, midvariance and scale. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math,statistics

def calculate(p):
    xs=p["data"];M=statistics.median(xs);d=[x-M for x in xs];mad=statistics.median([abs(v) for v in d])
    if mad==0:return {"median":M,"mad":mad,"location":M,"midvariance":0.0,"scale":0.0}
    c=p.get("location_c",6.0);terms=[(v,(v/(c*mad))**2) for v in d if abs(v/(c*mad))<1]
    total=sum((1-u)**2 for _,u in terms)
    if total==0:raise ValueError("No retained location observations")
    loc=M+sum(v*(1-u)**2 for v,u in terms)/total
    c=p.get("scale_c",9.0);terms=[(v,(v/(c*mad))**2) for v in d if abs(v/(c*mad))<1]
    n=len(terms) if p.get("modify_sample_size",False) else len(xs)
    denominator=sum((1-u)*(1-5*u) for _,u in terms)**2
    if denominator==0:raise ValueError("Biweight scale denominator is zero")
    variance=n*sum(v*v*(1-u)**4 for v,u in terms)/denominator
    return {"median":M,"mad":mad,"location":loc,"midvariance":variance,"scale":math.sqrt(variance)}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
