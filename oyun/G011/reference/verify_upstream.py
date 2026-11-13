#!/usr/bin/env python3
"""Rerun the pinned upstream code on every frozen reference input; no network, never imports tool/main.py."""
import json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'reference'
REFS=json.loads((ROOT/'tests/references.json').read_text(encoding='utf-8'))
HARNESS=json.loads((R/'harness.json').read_text())
def compare(a,b,tol,where):
    if isinstance(b,dict):
        for k,v in b.items():
            assert k in a,(where,k);compare(a[k],v,tol,where+'.'+k)
    elif isinstance(b,list):
        assert isinstance(a,list) and len(a)==len(b),(where,a,b)
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,tol,where+'[%d]'%i)
    elif isinstance(b,bool) or b is None or isinstance(b,str):assert a==b,(where,a,b)
    else:assert abs(a-b)<=tol*max(1.0,abs(b)),(where,a,b,tol)
runner=HARNESS['runner']
exe=shutil.which('node') if runner=='node' else sys.executable
if exe is None:raise SystemExit('Node.js is required for this upstream rerun')
env=dict(os.environ,SKILLPACK_FILES_DIR=str(ROOT/'tests'/'fixtures'))
proc=subprocess.run([exe,str(R/HARNESS['script'])],input=json.dumps([r['input'] for r in REFS],ensure_ascii=False).encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300,env=env,cwd=str(ROOT))
if proc.returncode!=0:raise SystemExit(proc.stderr.decode())
outputs=json.loads(proc.stdout)
assert len(outputs)==len(REFS)
# Frozen values came from this same rerun; allow only last-bit drift across platforms/library builds.
for i,(got,ref) in enumerate(zip(outputs,REFS)):compare(got,ref['expected_subset'],1e-12,'case%d'%i)
print('upstream reference rerun passed: %d cases via %s'%(len(REFS),runner))
