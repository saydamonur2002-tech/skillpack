#!/usr/bin/env python3
"""Weighted graph combinatorial and normalized Laplacians. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    w=p["adjacency"];n=len(w)
    if any(len(row)!=n for row in w):raise ValueError("Adjacency must be square")
    # Same average symmetrization used by upstream for directed graphs.
    W=[[(w[i][j]+w[j][i])/2 for j in range(n)] for i in range(n)];degree=[sum(row) for row in W]
    mode=p.get("kind","combinatorial");L=[]
    for i in range(n):
        row=[]
        for j in range(n):
            if mode=="combinatorial":v=(degree[i] if i==j else 0)-W[i][j]
            elif degree[i]==0 or degree[j]==0:v=0.0
            else:v=(1.0 if i==j else 0.0)-W[i][j]/math.sqrt(degree[i]*degree[j])
            row.append(v)
        L.append(row)
    return {"laplacian":L,"weighted_degree":degree,"directed_input":any(w[i][j]!=w[j][i] for i in range(n) for j in range(n))}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
