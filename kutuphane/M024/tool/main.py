#!/usr/bin/env python3
"""Encoded polyline algorithm format encode and decode. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math

def _round(v):
    return math.floor(abs(v)+0.5)*(1 if v>=0 else -1)

def _enc(cur,prev,factor):
    cur=_round(cur*factor);prev=_round(prev*factor);c=int((cur-prev)*2)
    if c<0:c=-c-1
    out=[]
    while c>=0x20:out.append(chr((0x20|(c&0x1f))+63));c>>=5
    out.append(chr(c+63));return ''.join(out)

def encode(coords,precision):
    if not coords:return ''
    factor=float(10**precision);out=[_enc(coords[0][0],0,factor),_enc(coords[0][1],0,factor)]
    for i in range(1,len(coords)):
        a=coords[i];b=coords[i-1];out.append(_enc(a[0],b[0],factor));out.append(_enc(a[1],b[1],factor))
    return ''.join(out)

def decode(s,precision):
    factor=float(10**precision);index=0;lat=lng=0;coords=[];n=len(s)
    for pos,ch in enumerate(s):
        if not 63<=ord(ch)<=126:raise ValueError('Character outside polyline range 63..126 at offset %d'%pos)
    def value():
        nonlocal index
        result=0;shift=0
        while True:
            if index>=n:raise ValueError('Truncated polyline value')
            b=ord(s[index])-63;index+=1;result|=(b&0x1f)<<shift;shift+=5
            if shift>60:raise ValueError('Polyline value too long')
            if b<0x20:break
        return (-result-1)//2 if result&1 else result//2
    while index<n:
        dlat=value();dlng=value();lat+=dlat;lng+=dlng
        if abs(lat)>2**53 or abs(lng)>2**53:raise ValueError('Accumulated value exceeds exact float range')
        coords.append([lat/factor,lng/factor])
    return coords

def calculate(p):
    op=p['operation'];prec=p.get('precision',5)
    if op=='encode':
        if 'coordinates' not in p or 'encoded' in p:raise ValueError('encode requires coordinates and no encoded field')
        for c in p['coordinates']:
            if abs(_round(c[0]*10.0**prec))>2**52 or abs(_round(c[1]*10.0**prec))>2**52:raise ValueError('Scaled coordinate exceeds exact range')
        return {'operation':op,'precision':prec,'encoded':encode(p['coordinates'],prec),'point_count':len(p['coordinates'])}
    if 'encoded' not in p or 'coordinates' in p:raise ValueError('decode requires encoded and no coordinates field')
    coords=decode(p['encoded'],prec)
    return {'operation':op,'precision':prec,'coordinates':coords,'point_count':len(coords)}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
