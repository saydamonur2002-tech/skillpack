#!/usr/bin/env python3
"""IAU 2006 frame-bias and precession matrix from TT. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def poly(t,cs):
    y=cs[-1]
    for c in cs[-2::-1]:y=c+y*t
    return y*math.pi/(180*3600)

def calculate(p):
    t=((p['jd1']-2451545.0)+p['jd2'])/36525.0
    gamb=poly(t,[-.052928,10.556378,.4932044,-.00031238,-.000002788,.0000000260])
    phib=poly(t,[84381.412819,-46.811016,.0511268,.00053289,-.000000440,-.0000000176])
    psib=poly(t,[-.041775,5038.481484,1.5584175,-.00018522,-.000026452,-.0000000148])
    epsa=poly(t,[84381.406,-46.836769,-.0001831,.00200340,-.000000576,-.0000000434])
    r=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]
    def rotate(angle,i,j):
        c=math.cos(angle);s=math.sin(angle);ri=r[i][:];rj=r[j][:]
        r[i]=[c*a+s*b for a,b in zip(ri,rj)];r[j]=[-s*a+c*b for a,b in zip(ri,rj)]
    rotate(gamb,0,1);rotate(phib,1,2);rotate(-psib,0,1);rotate(-epsa,1,2)
    return {'matrix':r,'gamb_rad':gamb,'phib_rad':phib,'psib_rad':psib,'epsa_rad':epsa,'julian_centuries_tt':t}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
