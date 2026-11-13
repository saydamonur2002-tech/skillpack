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

INPUT_SCHEMA={'type': 'object', 'properties': {'memory_total': {'type': 'number', 'minimum': 1}, 'memory_available': {'type': 'number', 'minimum': 0}, 'disk_total': {'type': 'number', 'minimum': 1}, 'disk_free': {'type': 'number', 'minimum': 0}, 'cpu_busy_delta': {'type': 'number', 'minimum': 0}, 'cpu_total_delta': {'type': 'number', 'minimum': 1e-09}}, 'required': ['memory_total', 'memory_available', 'disk_total', 'disk_free', 'cpu_busy_delta', 'cpu_total_delta'], 'additionalProperties': False}

def run(d):
    if d['memory_available']>d['memory_total'] or d['disk_free']>d['disk_total'] or d['cpu_busy_delta']>d['cpu_total_delta']:raise ValueError('inconsistent counters')
    return {'memory_used_percent':100*(d['memory_total']-d['memory_available'])/d['memory_total'],'disk_used_percent':100*(d['disk_total']-d['disk_free'])/d['disk_total'],'cpu_percent':100*d['cpu_busy_delta']/d['cpu_total_delta']}



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
