#!/usr/bin/env python3
"""Deterministic local tool. No model-generated decisions."""
import json,math,re,sys
from pathlib import Path
PACK=Path(__file__).resolve().parents[1]
ROOT=PACK.parent
sys.path.insert(0,str(ROOT/'_vendor'))

def node_run(d):
    import subprocess
    p=subprocess.run(['node',str(PACK/'tool/runner.cjs')],input=json.dumps(d),text=True,capture_output=True,timeout=8)
    if p.returncode:raise ValueError(p.stderr[:300] or 'Node runtime failed')
    return json.loads(p.stdout)

INPUT_SCHEMA={'type': 'object', 'properties': {'capacity': {'type': 'integer', 'minimum': 1, 'maximum': 10000}, 'operations': {'type': 'array', 'items': {'type': 'object', 'properties': {'op': {'enum': ['write', 'read']}, 'data': {'type': 'array', 'items': {'type': 'integer', 'minimum': 0, 'maximum': 255}, 'minItems': 0, 'maxItems': 10000}, 'count': {'type': 'integer', 'minimum': 0}}, 'required': ['op'], 'additionalProperties': False}, 'minItems': 0, 'maxItems': 10000}}, 'required': ['capacity', 'operations'], 'additionalProperties': False}

def run(d):
    q=[];out=[]
    for op in d['operations']:
        if op['op']=='write':
            b=op.get('data',[])
            if len(q)+len(b)>d['capacity']:raise ValueError('buffer full')
            q.extend(b)
        else:
            n=op.get('count',0)
            if n>len(q):raise ValueError('buffer empty')
            out.append(q[:n]);del q[:n]
    return {'reads':out,'remaining':q}



def finite(x):
    if isinstance(x,float) and not math.isfinite(x):raise ValueError('nonfinite JSON value')
    if isinstance(x,dict):
        for v in x.values():finite(v)
    elif isinstance(x,list):
        for v in x:finite(v)

def handle(d):
    try:
        from jsonschema import Draft7Validator
        finite(d)
        Draft7Validator(INPUT_SCHEMA).validate(d)
        result=run(d);finite(result)
        return {'ok':True,'result':result}
    except Exception as e:
        return {'ok':False,'error':{'code':'INVALID_INPUT_OR_RUNTIME','message':str(e)[:400]}}

if __name__=='__main__':
    try:
        raw=sys.stdin.buffer.read(1048577)
        if len(raw)>1048576:raise ValueError('input exceeds 1 MiB')
        data=json.loads(raw,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
        if isinstance(data,dict) and data.get('probe') is True:
            if set(data)!={'probe'}:raise ValueError('probe cannot be combined with snapshot fields')
            if 'probe' not in globals():raise ValueError('probe unsupported')
            data=probe()
        print(json.dumps(handle(data),allow_nan=False,ensure_ascii=False))
    except Exception as e:print(json.dumps({'ok':False,'error':{'code':'INVALID_JSON_OR_PROBE','message':str(e)[:400]}}))
