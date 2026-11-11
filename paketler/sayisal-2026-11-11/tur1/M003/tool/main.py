#!/usr/bin/env python3
"""WGS84 Vincenty inverse geodesic. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def calculate(p):
    a=6378137.0;b=6356752.314245;f=1/298.257223563
    phi1,phi2=map(math.radians,[p["lat1"],p["lat2"]]);L=math.radians((p["lon2"]-p["lon1"]+180)%360-180)
    if p["lat1"]==p["lat2"] and (L==0 or abs(p["lat1"])==90):
        return {"distance_m":0.0,"initial_bearing_deg":None,"final_bearing_deg":None}
    tan1=(1-f)*math.tan(phi1);cos1=1/math.sqrt(1+tan1*tan1);sin1=tan1*cos1
    tan2=(1-f)*math.tan(phi2);cos2=1/math.sqrt(1+tan2*tan2);sin2=tan2*cos2
    antipodal=abs(L)>math.pi/2 or abs(phi2-phi1)>math.pi/2
    lam=L;sigma=math.pi if antipodal else 0.0;sins=0.0;coss=-1.0 if antipodal else 1.0;cos2m=1.0;cos2alpha=1.0
    for iteration in range(1000):
        sinl=math.sin(lam);cosl=math.cos(lam)
        sinsq=(cos2*sinl)**2+(cos1*sin2-sin1*cos2*cosl)**2
        if abs(sinsq)<1e-24:break
        sins=math.sqrt(sinsq);coss=sin1*sin2+cos1*cos2*cosl;sigma=math.atan2(sins,coss)
        sinalpha=cos1*cos2*sinl/sins;cos2alpha=1-sinalpha*sinalpha
        cos2m=coss-2*sin1*sin2/cos2alpha if cos2alpha!=0 else 0.0
        C=f/16*cos2alpha*(4+f*(4-3*cos2alpha));old=lam
        lam=L+(1-C)*f*sinalpha*(sigma+C*sins*(cos2m+C*coss*(-1+2*cos2m*cos2m)))
        check=abs(lam)-math.pi if antipodal else abs(lam)
        if check>math.pi:raise ValueError("Vincenty failed to converge")
        if abs(lam-old)<=1e-12:break
    else:raise ValueError("Vincenty failed to converge after 1000 iterations")
    u=cos2alpha*(a*a-b*b)/(b*b)
    A=1+u/16384*(4096+u*(-768+u*(320-175*u)));B=u/1024*(256+u*(-128+u*(74-47*u)))
    ds=B*sins*(cos2m+B/4*(coss*(-1+2*cos2m*cos2m)-B/6*cos2m*(-3+4*sins*sins)*(-3+4*cos2m*cos2m)))
    distance=b*A*(sigma-ds)
    alpha1=0 if abs(sinsq)<2.220446049250313e-16 else math.atan2(cos2*sinl,cos1*sin2-sin1*cos2*cosl)
    alpha2=math.pi if abs(sinsq)<2.220446049250313e-16 else math.atan2(cos1*sinl,-sin1*cos2+cos1*sin2*cosl)
    return {"distance_m":round(distance,3),"initial_bearing_deg":None if abs(distance)<2.220446049250313e-16 else round(math.degrees(alpha1)%360,7),"final_bearing_deg":None if abs(distance)<2.220446049250313e-16 else round(math.degrees(alpha2)%360,7)}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
