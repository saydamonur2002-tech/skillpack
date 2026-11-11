#!/usr/bin/env python3
"""Cephes regularized incomplete beta with symmetry and dual fractions. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
EPS=1.1102230246251565e-16
BIG=4.503599627370496e15
BINV=2.220446049250313e-16
MAXLOG=709.782712893384
MINLOG=-745.1332191019411
MAXGAM=171.62437695630273

def lbeta(a,b):return math.lgamma(a)+math.lgamma(b)-math.lgamma(a+b)

def fraction(a,b,x,second=False):
    k1=a;k2=b-1 if second else a+b;k3=a;k4=a+1;k5=1.0;k6=a+b if second else b-1;k7=a+1;k8=a+2
    pkm2=0.0;qkm2=pkm1=qkm1=ans=r=1.0;z=x/(1-x) if second else x
    for n in range(300):
        xk=-z*k1*k2/(k3*k4);pk=pkm1+pkm2*xk;qk=qkm1+qkm2*xk;pkm2,pkm1=pkm1,pk;qkm2,qkm1=qkm1,qk
        xk=z*k5*k6/(k7*k8);pk=pkm1+pkm2*xk;qk=qkm1+qkm2*xk;pkm2,pkm1=pkm1,pk;qkm2,qkm1=qkm1,qk
        if qk!=0:r=pk/qk
        if r!=0:t=abs((ans-r)/r);ans=r
        else:t=1.0
        if t<3*EPS:return ans
        k1+=1;k2+=-1 if second else 1;k3+=2;k4+=2;k5+=1;k6+=1 if second else -1;k7+=2;k8+=2
        if abs(qk)+abs(pk)>BIG:pkm2*=BINV;pkm1*=BINV;qkm2*=BINV;qkm1*=BINV
        if abs(qk)<BINV or abs(pk)<BINV:pkm2*=BIG;pkm1*=BIG;qkm2*=BIG;qkm1*=BIG
    raise ValueError('Beta continued fraction did not converge in 300 iterations')

def pseries(a,b,x):
    ai=1/a;u=(1-b)*x;v=u/(a+1);t1=v;t=u;n=2.0;s=0.0;z=EPS*ai
    for _ in range(100000):
        if abs(v)<=z:break
        u=(n-b)*x/n;t*=u;v=t/(a+n);s+=v;n+=1
    else:raise ValueError('Beta power series failed to converge')
    s+=t1;s+=ai;u=a*math.log(x)
    if a+b<MAXGAM and abs(u)<MAXLOG:return s*math.exp(-lbeta(a,b))*x**a
    t=-lbeta(a,b)+u+math.log(s)
    return 0.0 if t<MINLOG else math.exp(t)

def incomplete(a,b,x):
    if x==0:return 0.0
    if x==1:return 1.0
    if b*x<=1 and x<=.95:return pseries(a,b,x)
    flag=x>a/(a+b)
    if flag:a,b,x,xc=b,a,1-x,x
    else:xc=1-x
    if flag and b*x<=1 and x<=.95:t=pseries(a,b,x)
    else:
        w=fraction(a,b,x) if x*(a+b-2)-(a-1)<0 else fraction(a,b,x,True)/xc
        y=a*math.log(x);t=b*math.log(xc)
        if a+b<MAXGAM and abs(y)<MAXLOG and abs(t)<MAXLOG:t=xc**b*x**a/a*w*math.exp(-lbeta(a,b))
        else:
            y+=t-lbeta(a,b);y+=math.log(w/a);t=0.0 if y<MINLOG else math.exp(y)
    return (1-EPS if t<=EPS else 1-t) if flag else t

def calculate(p):return {'I':incomplete(p['a'],p['b'],p['x'])}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
