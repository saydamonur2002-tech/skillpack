#!/usr/bin/env python3
"""Bracketed polynomial roots with safeguarded Brent interpolation. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    coeff=p['coefficients'];a=p['a'];b=p['b'];xtol=p.get('xtol',2e-12);rtol=p.get('rtol',8.881784197001252e-16);limit=p.get('max_iterations',200)
    def f(x):
        y=0.0
        for c in coeff:y=y*x+c
        if not math.isfinite(y):raise ValueError('Polynomial evaluation overflowed')
        return y
    xpre=a;xcur=b;xblk=fblk=spre=scur=0.0;fpre=f(xpre);fcur=f(xcur);calls=2
    if fpre==0:return {'root':a,'residual':0.0,'iterations':0,'evaluations':calls}
    if fcur==0:return {'root':b,'residual':0.0,'iterations':0,'evaluations':calls}
    if (fpre<0)==(fcur<0):raise ValueError('Endpoints must bracket a sign change')
    for i in range(limit):
        if fpre!=0 and fcur!=0 and (fpre<0)!=(fcur<0):xblk=xpre;fblk=fpre;spre=scur=xcur-xpre
        if abs(fblk)<abs(fcur):xpre,xcur,xblk=xcur,xblk,xcur;fpre,fcur,fblk=fcur,fblk,fcur
        delta=(xtol+rtol*abs(xcur))/2;sbis=(xblk-xcur)/2
        if fcur==0 or abs(sbis)<delta:return {'root':xcur,'residual':fcur,'iterations':i+1,'evaluations':calls}
        if abs(spre)>delta and abs(fcur)<abs(fpre):
            try:
                if xpre==xblk:stry=-fcur*(xcur-xpre)/(fcur-fpre)
                else:
                    dpre=(fpre-fcur)/(xpre-xcur);dblk=(fblk-fcur)/(xblk-xcur)
                    stry=-fcur*(fblk*dblk-fpre*dpre)/(dblk*dpre*(fblk-fpre))
            except (ZeroDivisionError,OverflowError):stry=math.inf
            if 2*abs(stry)<min(abs(spre),3*abs(sbis)-delta):spre=scur;scur=stry
            else:spre=scur=sbis
        else:spre=scur=sbis
        xpre=xcur;fpre=fcur;xcur+=scur if abs(scur)>delta else (delta if sbis>0 else -delta)
        fcur=f(xcur);calls+=1
    raise ValueError('Brent solver did not converge within max_iterations')

if __name__=="__main__":
    raise SystemExit(cli(calculate))
