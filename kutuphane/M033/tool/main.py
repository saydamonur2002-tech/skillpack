#!/usr/bin/env python3
"""Nearby places: nearest-N and within-radius search by category. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
from decimal import Decimal,ROUND_HALF_UP
import mapdata

def _to_fixed(x,n):
    """JavaScript Number.prototype.toFixed for finite non-negative x (exact binary value, ties to the larger n)."""
    return float(Decimal(x).quantize(Decimal(1).scaleb(-n),rounding=ROUND_HALF_UP))

def get_distance(s_lat,s_lon,e_lat,e_lon,accuracy=1,precision=0):
    """Port of geolib v2.0.24 getDistance (Vincenty inverse on WGS-84), elevation ignored."""
    a=6378137;b=6356752.314245;f=1/298.257223563
    L=math.radians(e_lon-s_lon)
    U1=math.atan((1-f)*math.tan(math.radians(s_lat)));U2=math.atan((1-f)*math.tan(math.radians(e_lat)))
    sinU1=math.sin(U1);cosU1=math.cos(U1);sinU2=math.sin(U2);cosU2=math.cos(U2)
    lam=L;it=100
    while True:
        sinL=math.sin(lam);cosL=math.cos(lam)
        sinSigma=math.sqrt((cosU2*sinL)*(cosU2*sinL)+(cosU1*sinU2-sinU1*cosU2*cosL)*(cosU1*sinU2-sinU1*cosU2*cosL))
        if sinSigma==0:return 0
        cosSigma=sinU1*sinU2+cosU1*cosU2*cosL;sigma=math.atan2(sinSigma,cosSigma)
        sinAlpha=cosU1*cosU2*sinL/sinSigma;cosSqAlpha=1-sinAlpha*sinAlpha
        cos2SigmaM=cosSigma-2*sinU1*sinU2/cosSqAlpha if cosSqAlpha!=0 else 0.0
        C=f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha))
        lamP=lam
        lam=L+(1-C)*f*sinAlpha*(sigma+C*sinSigma*(cos2SigmaM+C*cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)))
        it-=1
        if not (abs(lam-lamP)>1e-12 and it>0):break
    if it==0:raise ValueError('Vincenty formula failed to converge (nearly antipodal points)')
    uSq=cosSqAlpha*(a*a-b*b)/(b*b)
    A=1+uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)))
    B=uSq/1024*(256+uSq*(-128+uSq*(74-47*uSq)))
    dS=B*sinSigma*(cos2SigmaM+B/4*(cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)-B/6*cos2SigmaM*(-3+4*sinSigma*sinSigma)*(-3+4*cos2SigmaM*cos2SigmaM)))
    d=_to_fixed(b*A*(sigma-dS),precision)
    v=math.floor(d*10**precision/accuracy+0.5)*accuracy/10**precision
    return int(v) if precision==0 else v

def calculate(p):
    op=p['operation'];pl,info=mapdata.places(p['dataset'])
    ds={'file':info['file'],'attribution':info['attribution'],'license':info['license'],'records':len(pl)}
    c=p['center'];lat=c['lat'];lon=c['lon'];radius=p.get('radius_m',1000)
    cats,aliases=mapdata.resolve_categories(p.get('categories',[]));cs=set(cats)
    sub=p.get('name_contains');subn=sub.lower() if sub else None
    # geolib orderByDistance: getDistance(center, place) with default accuracy 1 m / precision 0, stable ascending sort
    rows=[]
    for i,x in enumerate(pl):
        if cs and x['category'] not in cs:continue
        if subn and subn not in x['name'].lower():continue
        if op=='nearby' and not cs and x['category']=='street' and not p.get('include_streets',False):continue
        rows.append((get_distance(lat,lon,x['lat'],x['lon']),i,x))
    rows.sort(key=lambda r:r[0])
    inside=[r for r in rows if r[0]<=radius]
    if op=='categories':
        counts={}
        for d,i,x in inside:counts[x['category']]=counts.get(x['category'],0)+1
        top=sorted(counts.items(),key=lambda kv:(-kv[1],kv[0]))
        return {'operation':op,'center':c,'radius_m':radius,'categories':[{'category':k,'count':v} for k,v in top],'dataset':ds}
    lim=p.get('limit',10)
    out=[]
    for d,i,x in inside[:lim]:
        r={'name':x['name'],'category':x['category'],'lat':x['lat'],'lon':x['lon'],'distance_m':d,'id':x['id']}
        for k in ('addr:street','addr:housenumber','opening_hours'):
            if k in x['props']:r[k]=x['props'][k]
        out.append(r)
    feature={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'kind':'poi','name':r['name'],'category':r['category'],'distance_m':r['distance_m']},'geometry':{'type':'Point','coordinates':[r['lon'],r['lat']]}} for r in out]}
    return {'operation':op,'center':c,'radius_m':radius,'categories_used':aliases,'found_within_radius':len(inside),'results':out,'features':feature,'dataset':ds,
            'note':'Straight-line WGS-84 distance rounded to whole metres (inclusive radius), not walking distance; opening hours are copied from data and not evaluated.'}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
