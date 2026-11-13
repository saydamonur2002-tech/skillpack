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

INPUT_SCHEMA={'type': 'object', 'properties': {'events': {'type': 'array', 'items': {'type': 'object', 'properties': {'time': {'type': 'number', 'minimum': 0}, 'motion': {'enum': ['on', 'off']}}, 'required': ['time', 'motion'], 'additionalProperties': False}, 'minItems': 0, 'maxItems': 10000}, 'wait_seconds': {'type': 'number', 'minimum': 0, 'maximum': 3600}, 'until': {'type': 'number', 'minimum': 0}}, 'required': ['events', 'wait_seconds', 'until'], 'additionalProperties': False}

def run(d):
    until=d['until'];wait=d['wait_seconds'];deadline=None;last=-1;plans=[];active=False
    for event in d['events']:
        t=event['time']
        if t<last or t>until:raise ValueError('ordered events within replay horizon required')
        if deadline is not None and deadline<=t:
            plans.append({'time':deadline,'action':'turn_off'});deadline=None;active=False
        if event['motion']=='on':
            plans.append({'time':t,'action':'turn_on'});active=True;deadline=None
        elif active:deadline=t+wait
        last=t
    if deadline is not None and deadline<=until:plans.append({'time':deadline,'action':'turn_off'})
    return {'planned_actions':plans}



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
