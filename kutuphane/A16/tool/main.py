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

INPUT_SCHEMA={'type': 'object', 'properties': {'csv': {'type': 'string', 'maxLength': 100000}}, 'required': ['csv'], 'additionalProperties': False}

def run(d):
    import csv,io
    rows=list(csv.reader(io.StringIO(d['csv'])))
    if not rows:raise ValueError('empty CSV')
    fields=rows[0]
    left={'left_'+j for j in ['s0','s1','e0','e1','w0','w1','w2']}
    right={'right_'+j for j in ['s0','s1','e0','e1','w0','w1','w2']}
    if len(fields)!=17 or fields[0]!='time' or fields[8]!='left_gripper' or fields[16]!='right_gripper' or set(fields[1:8])!=left or set(fields[9:16])!=right:raise ValueError('expected recorder joint and gripper header')
    last=None
    for row in rows[1:]:
        if len(row)!=len(fields):raise ValueError('column count')
        nums=[float(x) for x in row]
        if not all(math.isfinite(x) for x in nums):raise ValueError('nonfinite')
        if last is not None and nums[0]<=last:raise ValueError('time must increase')
        last=nums[0]
    return {'rows':len(rows)-1,'fields':fields}



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
