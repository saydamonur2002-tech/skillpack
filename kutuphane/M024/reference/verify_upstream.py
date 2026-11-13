#!/usr/bin/env python3
"""Rerun the pinned upstream source on every frozen reference input; no network, no import of the Python port."""
import json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'reference'
REFS=json.loads((ROOT/'tests/references.json').read_text())
HARNESS=json.loads((R/'harness.json').read_text())
def compare(a,b,tol,where):
    if isinstance(b,dict):
        for k,v in b.items():
            assert k in a,(where,k);compare(a[k],v,tol,where+'.'+k)
    elif isinstance(b,list):
        assert isinstance(a,list) and len(a)==len(b),(where,a,b)
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,tol,where+'[%d]'%i)
    elif isinstance(b,bool) or b is None or isinstance(b,str):assert a==b,(where,a,b)
    else:assert abs(a-b)<=tol,(where,a,b,tol)
runner=HARNESS['runner']
exe=shutil.which('node') if runner=='node' else sys.executable
if exe is None:raise SystemExit('Node.js is required for this upstream rerun')
proc=subprocess.run([exe,str(R/HARNESS['script'])],input=json.dumps([r['input'] for r in REFS]).encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60,check=True)
outputs=json.loads(proc.stdout)
assert len(outputs)==len(REFS)
for i,(got,ref) in enumerate(zip(outputs,REFS)):compare(got,ref['expected_subset'],ref['absolute_tolerance'],'case%d'%i)
print('upstream reference rerun passed: %d cases via %s'%(len(REFS),runner))
