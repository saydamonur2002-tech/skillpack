#!/usr/bin/env python3
"""Spherical great-circle distance and bearings. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    phi1,phi2=map(math.radians,[p["lat1"],p["lat2"]]);dl=math.radians(p["lon2"]-p["lon1"]);dp=phi2-phi1
    h=math.sin(dp/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    h=max(0.0,min(1.0,h));arc=2*math.atan2(math.sqrt(h),math.sqrt(1-h))
    distance=p.get("radius_m",6371000.0)*arc
    if arc<1e-15 or abs(arc-math.pi)<1e-15:initial=final=None
    else:
        initial=math.degrees(math.atan2(math.sin(dl)*math.cos(phi2),math.cos(phi1)*math.sin(phi2)-math.sin(phi1)*math.cos(phi2)*math.cos(dl)))%360
        reverse=math.degrees(math.atan2(-math.sin(dl)*math.cos(phi1),math.cos(phi2)*math.sin(phi1)-math.sin(phi2)*math.cos(phi1)*math.cos(dl)))%360
        final=(reverse+180)%360
    return {"distance_m":distance,"initial_bearing_deg":initial,"final_bearing_deg":final,"central_angle_rad":arc}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
