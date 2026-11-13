#!/usr/bin/env python3
"""Slippy-map tile math: lon/lat to z/x/y, tile bounds, quadkeys, parent and children. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
D2R=math.pi/180;R2D=180/math.pi

def tile2lon(x,z):return x/math.pow(2,z)*360-180

def tile2lat(y,z):
    n=math.pi-2*math.pi*y/math.pow(2,z)
    return R2D*math.atan(0.5*(math.exp(n)-math.exp(-n)))

def tile_to_bbox(t):
    return [tile2lon(t[0],t[2]),tile2lat(t[1]+1,t[2]),tile2lon(t[0]+1,t[2]),tile2lat(t[1],t[2])]

def tile_to_geojson(t):
    b=tile_to_bbox(t)
    return {'type':'Polygon','coordinates':[[[b[0],b[1]],[b[0],b[3]],[b[2],b[3]],[b[2],b[1]],[b[0],b[1]]]]}

def point_to_tile_fraction(lon,lat,z):
    s=math.sin(lat*D2R);z2=math.pow(2,z)
    x=z2*(lon/360+0.5);y=z2*(0.5-0.25*math.log((1+s)/(1-s))/math.pi)
    return [x,y,z]

def point_to_tile(lon,lat,z):
    t=point_to_tile_fraction(lon,lat,z);return [math.floor(t[0]),math.floor(t[1]),z]

def get_children(t):
    return [[t[0]*2,t[1]*2,t[2]+1],[t[0]*2+1,t[1]*2,t[2]+1],[t[0]*2+1,t[1]*2+1,t[2]+1],[t[0]*2,t[1]*2+1,t[2]+1]]

def get_parent(t):
    # upstream branches reduce to integer halving for non-negative integer tiles
    if t[0]%2==0 and t[1]%2==0:return [t[0]//2,t[1]//2,t[2]-1]
    if t[0]%2==0:return [t[0]//2,(t[1]-1)//2,t[2]-1]
    if t[1]%2==0:return [(t[0]-1)//2,t[1]//2,t[2]-1]
    return [(t[0]-1)//2,(t[1]-1)//2,t[2]-1]

def tile_to_quadkey(t):
    s=''
    for z in range(t[2],0,-1):
        b=0;mask=1<<(z-1)
        if t[0]&mask:b+=1
        if t[1]&mask:b+=2
        s+=str(b)
    return s

def quadkey_to_tile(q):
    x=y=0;z=len(q)
    for i in range(z,0,-1):
        mask=1<<(i-1);ch=q[z-i]
        if ch=='1':x|=mask
        elif ch=='2':y|=mask
        elif ch=='3':x|=mask;y|=mask
    return [x,y,z]

def _i32(v):
    v&=0xFFFFFFFF
    return v-0x100000000 if v&0x80000000 else v

def _get_bbox_zoom(b):
    for z in range(28):
        mask=_i32(1<<(32-(z+1)))
        if (_i32(b[0])&mask)!=(_i32(b[2])&mask) or (_i32(b[1])&mask)!=(_i32(b[3])&mask):return z
    return 28

def bbox_to_tile(bb):
    mn=point_to_tile(bb[0],bb[1],32);mx=point_to_tile(bb[2],bb[3],32)
    b=[mn[0],mn[1],mx[0],mx[1]];z=_get_bbox_zoom(b)
    if z==0:return [0,0,0]
    # JavaScript >>> converts to uint32 first
    return [(b[0]&0xFFFFFFFF)>>(32-z),(b[1]&0xFFFFFFFF)>>(32-z),z]

def _tile(p):
    t=p.get('tile')
    if t is None:raise ValueError('this operation requires tile [x, y, z]')
    x,y,z=t
    if x>=2**z or y>=2**z:raise ValueError('tile x and y must be below 2^z')
    return t

def calculate(p):
    op=p['operation']
    if op in ('point_to_tile','point_to_tile_fraction'):
        if 'lon' not in p or 'lat' not in p or 'zoom' not in p:raise ValueError(op+' requires lon, lat and zoom')
        f=point_to_tile if op=='point_to_tile' else point_to_tile_fraction
        r={'operation':op,'tile':f(p['lon'],p['lat'],p['zoom'])}
        if op=='point_to_tile':r['quadkey']=tile_to_quadkey(r['tile']);r['path']='%d/%d/%d'%(r['tile'][2],r['tile'][0],r['tile'][1])
        return r
    if op=='quadkey_to_tile':
        if 'quadkey' not in p:raise ValueError('quadkey_to_tile requires quadkey')
        return {'operation':op,'tile':quadkey_to_tile(p['quadkey'])}
    if op=='bbox_to_tile':
        if 'bbox' not in p:raise ValueError('bbox_to_tile requires bbox [w, s, e, n]')
        return {'operation':op,'tile':bbox_to_tile(p['bbox'])}
    t=_tile(p)
    if op=='tile_to_bbox':return {'operation':op,'bbox':tile_to_bbox(t)}
    if op=='tile_to_geojson':return {'operation':op,'geometry':tile_to_geojson(t)}
    if op=='tile_to_quadkey':return {'operation':op,'quadkey':tile_to_quadkey(t)}
    if op=='children':return {'operation':op,'tiles':get_children(t)}
    if t[2]==0:raise ValueError('zoom 0 tile has no parent or siblings')
    if op=='parent':return {'operation':op,'tile':get_parent(t)}
    return {'operation':op,'tiles':get_children(get_parent(t))}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
