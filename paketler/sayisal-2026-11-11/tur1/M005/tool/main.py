#!/usr/bin/env python3
"""Mercator rhumb-line distance and constant bearing. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    phi1,phi2=map(math.radians,[p["lat1"],p["lat2"]]);dp=phi2-phi1;dl=math.radians(p["lon2"]-p["lon1"])
    if abs(dl)>math.pi:dl=-(2*math.pi-dl) if dl>0 else 2*math.pi+dl
    psi=math.log(math.tan(phi2/2+math.pi/4)/math.tan(phi1/2+math.pi/4))
    q=dp/psi if abs(psi)>1e-11 else math.cos(phi1)
    d=math.sqrt(dp*dp+q*q*dl*dl)*p.get("radius_m",6371000.0)
    bearing=None if dp==0 and abs(dl)<1e-15 else math.degrees(math.atan2(dl,psi))%360
    return {"distance_m":d,"bearing_deg":bearing}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
