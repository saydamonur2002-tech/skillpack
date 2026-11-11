#!/usr/bin/env python3
"""IAU 2000 Earth rotation angle from split UT1 Julian date. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    d1,d2=sorted([p['jd1'],p['jd2']]);t=d1+(d2-2451545.0);f=math.fmod(d1,1.0)+math.fmod(d2,1.0)
    angle=math.fmod(2*math.pi*(f+.7790572732640+.00273781191135448*t),2*math.pi)
    if angle<0:angle+=2*math.pi
    return {'angle_rad':angle,'angle_deg':angle*180/math.pi}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
