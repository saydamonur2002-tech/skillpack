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

INPUT_SCHEMA={'type': 'object', 'properties': {'arguments': {'type': 'object'}, 'parameters': {'type': 'array', 'items': {'type': 'object'}, 'minItems': 0, 'maxItems': 10000}}, 'required': ['arguments', 'parameters'], 'additionalProperties': False}

def run(d):
    from jsonschema import Draft202012Validator
    args=d['arguments'];params=d['parameters'];names=set();errors=[]
    for p in params:
        if set(p)-{'name','in','required','schema'} or p.get('in') not in ['query','path']:raise ValueError('unsupported parameter feature')
        n=p['name'];names.add(n);schema=p['schema']
        if set(schema)-{'type','enum','minimum','maximum','minLength','maxLength'}:raise ValueError('unsupported schema feature')
        Draft202012Validator.check_schema(schema)
        if n not in args:
            if p.get('required',False) or p['in']=='path':errors.append(n+': required')
        elif not Draft202012Validator(schema).is_valid(args[n]):errors.append(n+': invalid')
    errors.extend(k+': unexpected' for k in sorted(set(args)-names))
    return {'valid':not errors,'errors':errors}



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
