import importlib.util,json,math
from pathlib import Path
import pytest
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('tool_'+P.name,P/'tool/main.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CASES=json.loads((P/'tests/vectors.json').read_text())
def equal(a,b):
    if isinstance(b,(int,float)) and not isinstance(b,bool):
        assert isinstance(a,(int,float)) and math.isclose(a,b,rel_tol=1e-6,abs_tol=0.01 if P.name=='B100' else 1e-8)
    elif isinstance(b,dict):
        assert isinstance(a,dict) and set(a)==set(b)
        for k in b:equal(a[k],b[k])
    elif isinstance(b,list):
        assert isinstance(a,list) and len(a)==len(b)
        for x,y in zip(a,b):equal(x,y)
    else:assert a==b
@pytest.mark.parametrize('v',CASES)
def test_vector(v):
    out=m.handle(v['input'])
    from jsonschema import Draft7Validator
    Draft7Validator(json.loads((P/'manifest.json').read_text())['outputs']).validate(out)
    if v.get('error'):assert out['ok'] is False,out
    else:
        assert out['ok'] is True,out
        equal(out['result'],v['result'])
def test_reject_nonfinite():
    assert m.handle({'unexpected':float('nan')})['ok'] is False
def test_reject_nonobject():
    assert m.handle([])['ok'] is False
