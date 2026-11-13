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

INPUT_SCHEMA={'type': 'object', 'properties': {'text': {'type': 'string', 'maxLength': 100000}, 'vocabulary': {'type': 'object', 'additionalProperties': {'type': 'array', 'items': {'type': 'string', 'maxLength': 100000}, 'minItems': 0, 'maxItems': 10000}}, 'required': {'type': 'array', 'items': {'type': 'string', 'maxLength': 100000}, 'minItems': 1, 'maxItems': 10000}}, 'required': ['text', 'vocabulary', 'required'], 'additionalProperties': False}

def run(d):
    from adapt.intent import IntentBuilder
    from adapt.engine import IntentDeterminationEngine
    e=IntentDeterminationEngine()
    for entity,words in sorted(d['vocabulary'].items()):
        for word in sorted(words):e.register_entity(word,entity)
    b=IntentBuilder('FixedIntent')
    for name in d['required']:b.require(name)
    e.register_intent_parser(b.build())
    out=[]
    for x in e.determine_intent(d['text']):
        if x.get('confidence',0)>0:out.append({'intent':x['intent_type'],'slots':{k:x[k] for k in d['required'] if k in x}})
    return {'matches':out}



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
