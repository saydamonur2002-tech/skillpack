#!/usr/bin/env python3
"""Spherical area of GeoJSON polygons (m², hectares, km²). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
WGS84_RADIUS=6378137  # value of RADIUS in the wgs84 npm module used by geojson-area

def rad(x):return x*math.pi/180

def _closed(c):return len(c)>1 and c[0][0]==c[-1][0] and c[0][1]==c[-1][1]

def ring_area(coords):
    """Port of mapbox/geojson-area ringArea (Chamberlain & Duquette 2007). Positive when clockwise."""
    area=0.0;n=len(coords)-1 if _closed(coords) else len(coords)
    if n>2:
        for i in range(n):
            if i==n-2:lo,mi,up=n-2,n-1,0
            elif i==n-1:lo,mi,up=n-1,0,1
            else:lo,mi,up=i,i+1,i+2
            p1=coords[lo];p2=coords[mi];p3=coords[up]
            area+=(rad(p3[0])-rad(p1[0]))*math.sin(rad(p2[1]))
        area=area*WGS84_RADIUS*WGS84_RADIUS/2
    return area

def polygon_area(coords):
    a=0.0
    if coords:
        a+=abs(ring_area(coords[0]))
        for r in coords[1:]:a-=abs(ring_area(r))
    return a

def geometry(g):
    t=g['type']
    if t=='Polygon':return polygon_area(g['coordinates'])
    if t=='MultiPolygon':
        a=0.0
        for c in g['coordinates']:a+=polygon_area(c)
        return a
    if t in ('Point','MultiPoint','LineString','MultiLineString'):return 0
    if t=='GeometryCollection':
        a=0.0
        for x in g['geometries']:a+=geometry(x)
        return a
    raise ValueError('unsupported geometry type')

def _rings(g):
    t=g['type']
    if t=='Polygon':return [g['coordinates']]
    if t=='MultiPolygon':return g['coordinates']
    if t=='GeometryCollection':return [p for x in g['geometries'] for p in _rings(x)]
    return []

def _check(g,depth=0):
    t=g.get('type')
    if t=='GeometryCollection':
        if depth>2 or not isinstance(g.get('geometries'),list):raise ValueError('bad GeometryCollection')
        for x in g['geometries']:_check(x,depth+1)
        return
    lv={'Point':0,'MultiPoint':1,'LineString':1,'MultiLineString':2,'Polygon':2,'MultiPolygon':3}.get(t)
    if lv is None:raise ValueError('unsupported geometry type')
    def walk(c,l):
        if l==0:
            if not (isinstance(c,list) and 2<=len(c)<=3 and all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in c)):raise ValueError('positions must be [lon, lat]')
            if not (-180<=c[0]<=180 and -90<=c[1]<=90):raise ValueError('position out of range')
            return
        if not isinstance(c,list):raise ValueError('coordinates nesting does not match the geometry type')
        for x in c:walk(x,l-1)
    walk(g.get('coordinates'),lv)

def calculate(p):
    g=p['geometry'];_check(g)
    if p['operation']=='ring':
        if g['type']!='LineString':raise ValueError('ring takes a LineString of the ring positions')
        a=ring_area(g['coordinates']);return {'operation':'ring','signed_area_m2':a,'orientation':'clockwise' if a>0 else ('counterclockwise' if a<0 else 'degenerate')}
    a=geometry(g)
    rings=[[ring_area(r) for r in poly] for poly in _rings(g)]
    return {'operation':'area','area_m2':a,'area_ha':a/1e4,'area_km2':a/1e6,'ring_signed_areas_m2':rings,
            'note':'Spherical approximation on a sphere of radius 6378137 m; expect small differences from ellipsoidal GIS areas.'}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
