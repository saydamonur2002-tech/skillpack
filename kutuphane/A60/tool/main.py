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

INPUT_SCHEMA={'type': 'object', 'properties': {'template': {'type': 'object'}, 'values': {'type': 'object'}}, 'required': ['template', 'values'], 'additionalProperties': False}

def run(d):
    t=d['template'];values=d['values'];params=t.get('params',{})
    if set(values)-set(params):raise ValueError('unknown value')
    for k,p in params.items():
        if set(p)-{'type','optional','description'}:raise ValueError('unsupported parameter feature')
        if k not in values:
            if p.get('optional',False):continue
            raise ValueError('missing '+k)
        typ=p['type'];v=values[k]
        if typ=='integer':valid=type(v) is int
        elif typ=='boolean':valid=type(v) is bool
        elif typ in ['string','uuid','dateTime']:valid=isinstance(v,str)
        elif typ=='decimal':valid=type(v) in [int,float]
        else:raise ValueError('unsupported type')
        if not valid:raise ValueError('wrong type for '+k)
    def sub(x):
        if isinstance(x,list):return [sub(v) for v in x]
        if isinstance(x,dict):return {k:sub(v) for k,v in x.items()}
        if not isinstance(x,str):return x
        m=re.fullmatch(r'\{\{\{(\w+)\}\}\}',x)
        if m:return values[m[1]]
        def replace(m):
            v=values[m[1]]
            if not isinstance(v,(str,int,float,bool)):raise ValueError('nonscalar substitution')
            return str(v)
        return re.sub(r'\{\{\{(\w+)\}\}\}',replace,x)
    return {'json':sub(t['hydrated'])}



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
