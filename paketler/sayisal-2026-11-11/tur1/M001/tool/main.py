#!/usr/bin/env python3
"""Consistent-end cubic spline and derivatives. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import bisect

def endpoint_second(x,y,at):
    # Same interpolating-cubic endpoint condition as upstream's 4x4 solve.
    h=max(abs(v-at) for v in x)
    z=[(v-at)/h for v in x]
    a=[[1.0,t,t*t,t*t*t,float(v)] for t,v in zip(z,y)]
    for k in range(4):
        row=max(range(k,4),key=lambda i:abs(a[i][k]));a[k],a[row]=a[row],a[k]
        if a[k][k]==0:raise ValueError("Singular endpoint polynomial")
        q=a[k][k];a[k]=[v/q for v in a[k]]
        for i in range(4):
            if i!=k:
                q=a[i][k];a[i]=[u-q*v for u,v in zip(a[i],a[k])]
    return 2*a[2][4]/(h*h)

def calculate(p):
    x=p["x"];y=p["y"];q=p["query"];n=len(x)
    if len(y)!=n:raise ValueError("x and y lengths differ")
    h=[x[i+1]-x[i] for i in range(n-1)]
    if any(t<=0 for t in h):raise ValueError("x must be strictly increasing")
    m=[0.0]*n
    if p.get("boundary","consistent")=="consistent":
        m[0]=endpoint_second(x[:4],y[:4],x[0]);m[-1]=endpoint_second(x[-4:],y[-4:],x[-1])
    diag=[2*(h[i-1]+h[i]) for i in range(1,n-1)]
    rhs=[6*((y[i+1]-y[i])/h[i]-(y[i]-y[i-1])/h[i-1]) for i in range(1,n-1)]
    rhs[0]-=h[0]*m[0];rhs[-1]-=h[-1]*m[-1]
    for k in range(1,n-2):
        ratio=h[k]/diag[k-1];diag[k]-=ratio*h[k];rhs[k]-=ratio*rhs[k-1]
    m[-2]=rhs[-1]/diag[-1]
    for k in range(n-4,-1,-1):m[k+1]=(rhs[k]-h[k+1]*m[k+2])/diag[k]
    vals=[];ders=[];seconds=[]
    for t in q:
        i=min(n-2,max(0,bisect.bisect_right(x,t)-1));s=h[i];a=(x[i+1]-t)/s;b=(t-x[i])/s
        vals.append(a*y[i]+b*y[i+1]+((a**3-a)*m[i]+(b**3-b)*m[i+1])*s*s/6)
        ders.append((y[i+1]-y[i])/s+s*((1-3*a*a)*m[i]+(3*b*b-1)*m[i+1])/6)
        seconds.append(a*m[i]+b*m[i+1])
    return {"values":vals,"first_derivatives":ders,"second_derivatives":seconds}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
