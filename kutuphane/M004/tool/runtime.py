"""Shared template copied into each standalone pack; Python stdlib plus jsonschema."""
import json, math, signal, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
MAX_BYTES=65536

def fail(message, code="INVALID_INPUT"):
    return {"ok":False,"error":{"code":code,"message":str(message)[:500]}}

def finite(v, depth=0):
    if depth>30: raise ValueError("JSON nesting exceeds 30 levels")
    if isinstance(v,float) and not math.isfinite(v): raise ValueError("Non-finite number")
    if isinstance(v,dict):
        for x in v.values(): finite(x,depth+1)
    if isinstance(v,list):
        for x in v: finite(x,depth+1)

def validate(v):
    finite(v)
    if len(json.dumps(v,allow_nan=False,separators=(",",":"),ensure_ascii=False).encode())>MAX_BYTES:
        raise ValueError("Input exceeds 65536 bytes")
    spec=json.loads((ROOT/"manifest.json").read_text())
    Draft202012Validator(spec["inputs"]).validate(v)
    return v

def pairs(xs):
    d={}
    for k,v in xs:
        if k in d: raise ValueError("Duplicate JSON key: "+k)
        d[k]=v
    return d

def reject_constant(x): raise ValueError("Invalid JSON number: "+x)

def cli(calculate):
    def alarm(*_): raise TimeoutError("Calculation exceeded 10 seconds")
    signal.signal(signal.SIGALRM,alarm);signal.alarm(10)
    try:
        raw=sys.stdin.buffer.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES: raise ValueError("Input exceeds 65536 bytes")
        value=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=reject_constant)
        result=calculate(validate(value));finite(result)
        answer={"ok":True,"result":result}
    except TimeoutError as e: answer=fail(e,"TIMEOUT")
    except Exception as e: answer=fail(e)
    finally: signal.alarm(0)
    sys.stdout.write(json.dumps(answer,allow_nan=False,separators=(",",":"))+"\n")
    return 0 if answer["ok"] else 2
