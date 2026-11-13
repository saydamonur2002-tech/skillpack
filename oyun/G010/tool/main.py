#!/usr/bin/env python3
"""Versioned save/load envelope for the city game state: canonical JSON + FNV-1a 32 checksum. Original work, MIT."""
from runtime import cli
import json,math
FORMAT='skillpack-city-save';VERSION=1
def q(v):
    if isinstance(v,bool) or v is None or isinstance(v,str):return v
    if isinstance(v,int):return v
    if isinstance(v,float):
        r=math.floor(v*1000+0.5)/1000
        return int(r) if r==int(r) else r
    if isinstance(v,dict):return {k:q(x) for k,x in v.items()}
    return [q(x) for x in v]
def canonical(state):return json.dumps(q(state),sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def fnv1a32(data):
    h=0x811c9dc5
    for b in data:h=((h^b)*0x01000193)&0xFFFFFFFF
    return h
def checksum(s):return 'fnv1a32:%08x'%fnv1a32(s.encode('utf-8'))
def calculate(p):
    if p['operation']=='checksum':return {'operation':'checksum','text_bytes':len(p['text'].encode()),'checksum':checksum(p['text'])}
    if p['operation']=='save':
        c=canonical(p['state'])
        env={'format':FORMAT,'version':VERSION,'checksum':checksum(c),'state':json.loads(c)}
        return {'operation':'save','envelope':env,'canonical_state':c,'bytes':len(c.encode())}
    env=p['envelope']
    if env.get('format')!=FORMAT:raise ValueError('not a city save (format field)')
    if env.get('version')!=VERSION:raise ValueError('unsupported save version; this tool reads version 1')
    c=canonical(env['state'])
    if checksum(c)!=env.get('checksum'):return {'operation':'load','valid':False,'reason':'checksum mismatch: the save was changed or damaged','state':None}
    return {'operation':'load','valid':True,'reason':'ok','state':json.loads(c)}
if __name__=='__main__':raise SystemExit(cli(calculate))
