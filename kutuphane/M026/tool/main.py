#!/usr/bin/env python3
"""Point-in-polygon, bounding box and centre of a polygon. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def is_point_inside(lat,lon,ring):
    """Port of geolib v2.0.24 isPointInside (ray casting over longitude intervals); ring = [[lon,lat],...]."""
    c=False;l=len(ring);j=l-1
    for i in range(l):
        xi=ring[i][0];yi=ring[i][1];xj=ring[j][0];yj=ring[j][1]
        if ((xi<=lon and lon<xj) or (xj<=lon and lon<xi)) and (lat<(yj-yi)*(lon-xi)/(xj-xi)+yi):c=not c
        j=i
    return c

def _polys(g):
    t=g['type']
    if t=='Polygon':return [g['coordinates']]
    if t=='MultiPolygon':return g['coordinates']
    raise ValueError('geometry must be Polygon or MultiPolygon')

def _ring(r):
    # GeoJSON closes rings by repeating the first position; geolib expects an open ring.
    return r[:-1] if len(r)>1 and r[0]==r[-1] else r

def get_bounds(pts):
    """Port of geolib getBounds (no elevation)."""
    s={'maxLat':-math.inf,'minLat':math.inf,'maxLng':-math.inf,'minLng':math.inf}
    for lon,lat in pts:
        s['maxLat']=max(lat,s['maxLat']);s['minLat']=min(lat,s['minLat']);s['maxLng']=max(lon,s['maxLng']);s['minLng']=min(lon,s['minLng'])
    return s

def _js_round6(x):
    from decimal import Decimal,ROUND_HALF_UP
    return float(Decimal(x).quantize(Decimal('0.000001'),rounding=ROUND_HALF_UP)) if x>=0 else -float(Decimal(-x).quantize(Decimal('0.000001'),rounding=ROUND_HALF_UP))

def get_center(pts):
    """Port of geolib getCenter: mean of unit vectors; upstream returns toFixed(6) strings, returned here as numbers."""
    X=Y=Z=0.0
    for lon,lat in pts:
        la=math.radians(lat);lo=math.radians(lon)
        X+=math.cos(la)*math.cos(lo);Y+=math.cos(la)*math.sin(lo);Z+=math.sin(la)
    n=len(pts);X=X/n;Y=Y/n;Z=Z/n
    lon=math.atan2(Y,X);hyp=math.sqrt(X*X+Y*Y);lat=math.atan2(Z,hyp)
    return {'latitude':_js_round6(lat*(180/math.pi)),'longitude':_js_round6(lon*(180/math.pi))}

def calculate(p):
    op=p['operation'];g=p['geometry'];polys=_polys(g)
    for poly in polys:
        for r in poly:
            if len(_ring(r))<3:raise ValueError('each ring needs at least 3 distinct positions')
    outer=[tuple(c[:2]) for poly in polys for c in _ring(poly[0])]
    if op=='contains':
        if 'points' not in p:raise ValueError('contains requires points')
        res=[]
        for pt in p['points']:
            inside=False;which=None
            for k,poly in enumerate(polys):
                if is_point_inside(pt['lat'],pt['lon'],_ring(poly[0])) and not any(is_point_inside(pt['lat'],pt['lon'],_ring(h)) for h in poly[1:]):
                    inside=True;which=k;break
            res.append({'lat':pt['lat'],'lon':pt['lon'],'inside':inside,'polygon_index':which})
        return {'operation':op,'results':res,'inside_count':sum(r['inside'] for r in res),
                'note':'Planar ray casting on longitude/latitude; points exactly on an edge may fall either way.'}
    if 'points' in p:raise ValueError(op+' takes only geometry')
    b=get_bounds(outer)
    if op=='bbox':
        return {'operation':op,'bounds':b,'bbox':[b['minLng'],b['minLat'],b['maxLng'],b['maxLat']]}
    lat=b['minLat']+((b['maxLat']-b['minLat'])/2);lon=b['minLng']+((b['maxLng']-b['minLng'])/2)
    return {'operation':op,'center_of_bounds':{'latitude':_js_round6(lat),'longitude':_js_round6(lon)},'vertex_mean_center':get_center(outer),
            'note':'Both centres can fall outside a concave polygon; check with contains.'}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
