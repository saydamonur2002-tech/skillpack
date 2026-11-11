#!/usr/bin/env python3
"""Cephes regularized incomplete gamma lower and upper tails. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
EPS=1.1102230246251565e-16
MAXLOG=709.782712893384
BIG=4.503599627370496e15
BINV=2.220446049250313e-16

def lower(a,x):
    if x==0:return 0.0
    if x>1 and x>a:return 1-upper(a,x)
    ax=a*math.log(x)-x-math.lgamma(a)
    if ax < -MAXLOG:return 0.0
    r=a;c=ans=1.0
    for _ in range(100000):
        r+=1;c*=x/r;ans+=c
        if c/ans<=EPS:return ans*math.exp(ax)/a
    raise ValueError('Gamma power series failed to converge')

def upper(a,x):
    if x<1 or x<a:return 1-lower(a,x)
    ax=a*math.log(x)-x-math.lgamma(a)
    if ax < -MAXLOG:return 0.0
    y=1-a;z=x+y+1;c=0.0;pkm2=1.0;qkm2=x;pkm1=x+1;qkm1=z*x;ans=pkm1/qkm1
    for _ in range(100000):
        c+=1;y+=1;z+=2;yc=y*c;pk=pkm1*z-pkm2*yc;qk=qkm1*z-qkm2*yc
        if qk!=0:
            r=pk/qk;t=abs((ans-r)/r);ans=r
        else:t=1.0
        pkm2,pkm1=pkm1,pk;qkm2,qkm1=qkm1,qk
        if abs(pk)>BIG:pkm2*=BINV;pkm1*=BINV;qkm2*=BINV;qkm1*=BINV
        if t<=EPS:return ans*math.exp(ax)
    raise ValueError('Gamma continued fraction failed to converge')

def calculate(p):return {'P':lower(p['shape'],p['x']),'Q':upper(p['shape'],p['x'])}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
