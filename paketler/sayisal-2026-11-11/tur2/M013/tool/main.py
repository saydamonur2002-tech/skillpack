#!/usr/bin/env python3
"""Fehlberg 7(8) fixed-step affine linear ODE propagation. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
C=[0,2/27,1/9,1/6,5/12,1/2,5/6,1/6,2/3,1/3,1,0,1]
A=[[],[2/27],[1/36,1/12],[1/24,0,1/8],[5/12,0,-25/16,25/16],[1/20,0,0,1/4,1/5],[-25/108,0,0,125/108,-65/27,125/54],[31/300,0,0,0,61/225,-2/9,13/900],[2,0,0,-53/6,704/45,-107/9,67/90,3],[-91/108,0,0,23/108,-976/135,311/54,-19/60,17/6,-1/12],[2383/4100,0,0,-341/164,4496/1025,-301/82,2133/4100,45/82,45/164,18/41],[3/205,0,0,0,0,-6/41,-3/205,-3/41,3/41,6/41],[-1777/4100,0,0,-341/164,4496/1025,-289/82,2193/4100,51/82,33/164,12/41,0,1]]
W=[0,0,0,0,0,34/105,9/35,9/35,9/280,9/280,0,41/840,41/840]

def step(matrix,bias,t,y,h):
    if h==0:return y[:],[0.0]*len(y)
    k=[]
    for row in A:
        z=[y[j]+h*sum(row[i]*k[i][j] for i in range(len(row))) for j in range(len(y))]
        dy=[sum(a*v for a,v in zip(r,z))+b for r,b in zip(matrix,bias)]
        if not all(math.isfinite(v) for v in dy):raise ValueError('ODE stages overflowed; reduce interval or use a suitable solver')
        k.append(dy)
    yf=[y[j]+h*sum(W[i]*k[i][j] for i in range(13)) for j in range(len(y))]
    terr=[(41/840)*(k[0][j]+k[10][j]-k[11][j]-k[12][j]) for j in range(len(y))]
    return yf,terr

def calculate(p):
    n=len(p['initial']);matrix=p['matrix'];bias=p.get('bias',[0.0]*n)
    if len(matrix)!=n or any(len(row)!=n for row in matrix) or len(bias)!=n:raise ValueError('Matrix, initial state and bias dimensions must agree')
    y=p['initial'][:];count=p['steps'];t0=p['t0'];t1=p['t1'];h=(t1-t0)/count;terr=[0.0]*n
    for i in range(count):y,terr=step(matrix,bias,t0+i*h,y,h)
    return {'state':y,'last_error_indicator':terr,'last_local_error_estimate':[h*v for v in terr],'step_size':h,'steps':count,'evaluations':0 if h==0 else 13*count}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
