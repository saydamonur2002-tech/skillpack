#!/usr/bin/env python3
"""Fornberg arbitrary-grid finite-difference weights. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
def calculate(p):
    x=p["nodes"]; x0=p.get("at",0.0); n=p.get("order",1); m=len(x)
    if n>=m:raise ValueError("order must be smaller than node count")
    if len(set(x))!=m:raise ValueError("nodes must be distinct")
    w=[[0.0]*(n+1) for _ in x];w[0][0]=1.0
    c1=1.0;c4=x[0]-x0
    for i in range(1,m):
        js=range(min(i,n)+1);c2=1.0;c5=c4;c4=x[i]-x0
        for v in range(i):
            c3=x[i]-x[v];c2*=c3
            c6=[j*w[v][j-1] if j else 0.0 for j in js]
            c7=[w[v][j] for j in js]
            for j in js:w[v][j]=(c4*c7[j]-c6[j])/c3
        for j in js:w[i][j]=c1*(c6[j]-c5*c7[j])/c2
        c1=c2
    all_weights=[[w[i][j] for i in range(m)] for j in range(n+1)]
    out={"weights":all_weights[n],"all_weights":all_weights}
    if "values" in p:
        if len(p["values"])!=m:raise ValueError("values must match nodes")
        out["derivative"]=sum(a*b for a,b in zip(all_weights[n],p["values"]))
    return out

if __name__=="__main__":
    raise SystemExit(cli(calculate))
