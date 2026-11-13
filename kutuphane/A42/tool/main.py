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

INPUT_SCHEMA={'type': 'object', 'properties': {'resource': {'type': 'object'}}, 'required': ['resource'], 'additionalProperties': False}

def run(d):
    p=d['resource']
    if p.get('resourceType')!='Patient':raise ValueError('only Patient supported')
    if set(p)-{'resourceType','id','active','gender','birthDate'}:raise ValueError('unsupported field')
    for k in ['id','gender','birthDate']:
        if k in p and not isinstance(p[k],str):raise ValueError(k+' must be a string')
    if 'active' in p and type(p['active']) is not bool:raise ValueError('active must be boolean')
    if 'gender' in p and p['gender'] not in ['male','female','other','unknown']:raise ValueError('invalid administrative gender')
    if 'birthDate' in p and not re.fullmatch(r'\d{4}(-\d{2}(-\d{2})?)?',p['birthDate']):raise ValueError('FHIR date lexical form')
    return {'resource':p,'scope':'Patient scalar subset only'}



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
