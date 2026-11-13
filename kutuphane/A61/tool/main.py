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

INPUT_SCHEMA={'type': 'object', 'properties': {'a': {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 2, 'maxItems': 10000}, 'minItems': 1, 'maxItems': 10000}, 'b': {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 2, 'maxItems': 10000}, 'minItems': 1, 'maxItems': 10000}, 'method': {'enum': ['pearson', 'spearman']}}, 'required': ['a', 'b', 'method'], 'additionalProperties': False}

def run(d):
    import numpy as np
    from scipy.stats import pearsonr,spearmanr
    a,b=np.asarray(d['a'],dtype=float),np.asarray(d['b'],dtype=float)
    if a.ndim!=2 or b.ndim!=2 or a.shape[1]!=b.shape[1]:raise ValueError('embedding dimension mismatch')
    x,y=a.mean(axis=0),b.mean(axis=0)
    if np.ptp(x)==0 or np.ptp(y)==0:raise ValueError('constant mean vector')
    score=(pearsonr if d['method']=='pearson' else spearmanr)(x,y).statistic
    return {'correlation':float(score)}



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
