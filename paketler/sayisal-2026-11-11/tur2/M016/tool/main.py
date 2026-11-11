#!/usr/bin/env python3
"""Unblocked partial-pivot LU factorization and dense linear solve. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    source=p['matrix'];rhs=p['rhs'];n=len(source)
    if any(len(r)!=n for r in source) or len(rhs)!=n:raise ValueError('Require a square matrix and matching rhs')
    a=[list(r) for r in source];b=list(rhs);piv=[]
    for j in range(n):
        jp=max(range(j,n),key=lambda i:abs(a[i][j]));piv.append(jp+1)
        if a[jp][j]==0:raise ValueError('Singular matrix: zero pivot at column '+str(j+1))
        if jp!=j:a[j],a[jp]=a[jp],a[j];b[j],b[jp]=b[jp],b[j]
        for i in range(j+1,n):a[i][j]/=a[j][j]
        for k in range(j+1,n):
            for i in range(j+1,n):a[i][k]-=a[i][j]*a[j][k]
    for i in range(n):
        for j in range(i):b[i]-=a[i][j]*b[j]
    x=[0.0]*n
    for i in range(n-1,-1,-1):
        value=b[i]
        for j in range(i+1,n):value-=a[i][j]*x[j]
        x[i]=value/a[i][i]
    if not all(math.isfinite(v) for v in x):raise ValueError('Linear solve produced a non-finite solution')
    residual=max(abs(sum(v*z for v,z in zip(row,x))-r) for row,r in zip(source,rhs));denom=max(sum(abs(v) for v in row) for row in source)*max(abs(v) for v in x)+max(abs(v) for v in rhs)
    return {'solution':x,'pivots_1based':piv,'lu':a,'residual_inf':residual,'scaled_backward_error':residual/denom if denom else 0.0}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
