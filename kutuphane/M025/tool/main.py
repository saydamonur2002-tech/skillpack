#!/usr/bin/env python3
"""Geohash encode, decode with bounding box, and eight neighbours. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
BASE32='0123456789bcdefghjkmnpqrstuvwxyz'
DICT={c:i for i,c in enumerate(BASE32)}
DIRS=[('north',1,0),('northeast',1,1),('east',0,1),('southeast',-1,1),('south',-1,0),('southwest',-1,-1),('west',0,-1),('northwest',1,-1)]

def encode(lat,lon,n):
    chars=[];bits=0;total=0;hv=0;max_lat=90;min_lat=-90;max_lon=180;min_lon=-180
    while len(chars)<n:
        if total%2==0:
            mid=(max_lon+min_lon)/2
            if lon>mid:hv=(hv<<1)+1;min_lon=mid
            else:hv=hv<<1;max_lon=mid
        else:
            mid=(max_lat+min_lat)/2
            if lat>mid:hv=(hv<<1)+1;min_lat=mid
            else:hv=hv<<1;max_lat=mid
        bits+=1;total+=1
        if bits==5:chars.append(BASE32[hv]);bits=0;hv=0
    return ''.join(chars)

def decode_bbox(h):
    is_lon=True;max_lat=90;min_lat=-90;max_lon=180;min_lon=-180
    for pos,ch in enumerate(h):
        v=DICT.get(ch.lower())
        if v is None:raise ValueError('Invalid geohash character at offset %d'%pos)
        for b in range(4,-1,-1):
            bit=(v>>b)&1
            if is_lon:
                mid=(max_lon+min_lon)/2
                if bit==1:min_lon=mid
                else:max_lon=mid
            else:
                mid=(max_lat+min_lat)/2
                if bit==1:min_lat=mid
                else:max_lat=mid
            is_lon=not is_lon
    return [min_lat,min_lon,max_lat,max_lon]

def decode(h):
    b=decode_bbox(h);lat=(b[0]+b[2])/2;lon=(b[1]+b[3])/2
    return {'latitude':lat,'longitude':lon,'error':{'latitude':b[2]-lat,'longitude':b[3]-lon},'bbox':b}

def _valid_lon(lon):
    if lon>180:return -180+math.fmod(lon,180)
    if lon<-180:return 180+math.fmod(lon,180)
    return lon

def _valid_lat(lat):return 90 if lat>90 else (-90 if lat<-90 else lat)

def neighbors(h):
    d=decode(h);lat=d['latitude'];lon=d['longitude'];le=d['error']['latitude']*2;oe=d['error']['longitude']*2
    return {name:encode(_valid_lat(lat+a*le),_valid_lon(lon+b*oe),len(h)) for name,a,b in DIRS}

def calculate(p):
    op=p['operation']
    if op=='encode':
        if 'latitude' not in p or 'longitude' not in p or 'geohash' in p:raise ValueError('encode requires latitude and longitude and no geohash')
        n=p.get('length',9);return {'operation':op,'geohash':encode(p['latitude'],p['longitude'],n),'length':n}
    if 'geohash' not in p or 'latitude' in p or 'longitude' in p or 'length' in p:raise ValueError(op+' requires geohash only')
    h=p['geohash']
    if op=='decode':
        r=decode(h);r.update({'operation':op,'geohash':h.lower()});return r
    decode_bbox(h);nb=neighbors(h)
    return {'operation':op,'geohash':h.lower(),'neighbors':nb,'clockwise_from_north':[nb[n] for n,_,_ in DIRS]}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
