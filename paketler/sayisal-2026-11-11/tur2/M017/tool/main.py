#!/usr/bin/env python3
"""Linear-time partial-pivot tridiagonal system solve. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    d=list(p['diagonal']);dl=list(p['lower']);du=list(p['upper']);b=list(p['rhs']);n=len(d);piv=[]
    if len(dl)!=n-1 or len(du)!=n-1 or len(b)!=n:raise ValueError('Diagonal lengths must be n, n-1, n-1 and rhs length n')
    for i in range(n-1):
        if abs(d[i])>=abs(dl[i]):
            if d[i]==0:raise ValueError('Singular tridiagonal matrix at pivot '+str(i+1))
            factor=dl[i]/d[i];d[i+1]-=factor*du[i];b[i+1]-=factor*b[i];piv.append(i+1)
            if i<n-2:dl[i]=0.0
        else:
            factor=d[i]/dl[i];d[i]=dl[i];temp=d[i+1];d[i+1]=du[i]-factor*temp
            if i<n-2:dl[i]=du[i+1];du[i+1]=-factor*du[i+1]
            du[i]=temp;temp=b[i];b[i]=b[i+1];b[i+1]=temp-factor*b[i+1];piv.append(i+2)
    if d[-1]==0:raise ValueError('Singular tridiagonal matrix at final pivot')
    b[-1]/=d[-1]
    if n>1:b[-2]=(b[-2]-du[-1]*b[-1])/d[-2]
    for i in range(n-3,-1,-1):b[i]=(b[i]-du[i]*b[i+1]-dl[i]*b[i+2])/d[i]
    if not all(math.isfinite(v) for v in b):raise ValueError('Tridiagonal solve produced a non-finite solution')
    residual=0.0
    for i in range(n):
        value=p['diagonal'][i]*b[i]
        if i>0:value+=p['lower'][i-1]*b[i-1]
        if i<n-1:value+=p['upper'][i]*b[i+1]
        residual=max(residual,abs(value-p['rhs'][i]))
    return {'solution':b,'elimination_pivots_1based':piv,'residual_inf':residual}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
