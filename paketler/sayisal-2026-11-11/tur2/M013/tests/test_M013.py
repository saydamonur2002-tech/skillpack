import hashlib,json,math,subprocess,sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
PACK=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((PACK/'manifest.json').read_text())
EXAMPLE=json.loads((PACK/'example.json').read_text())
REFS=json.loads((PACK/'tests'/'references.json').read_text())

def run_raw(raw):
    proc=subprocess.run([sys.executable,str(PACK/'tool'/'main.py')],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=12)
    assert proc.stderr==b'',proc.stderr.decode(errors='replace')
    assert proc.stdout.count(b'\n')==1
    value=json.loads(proc.stdout);Draft202012Validator(MANIFEST['outputs']).validate(value)
    assert proc.returncode==(0 if value['ok'] else 2)
    return value

def run(value):return run_raw(json.dumps(value,separators=(',',':'),allow_nan=False).encode())

def close(got,expected,tol):
    if isinstance(expected,dict):
        for k,v in expected.items():assert k in got;close(got[k],v,tol)
    elif isinstance(expected,list):
        assert len(got)==len(expected)
        for a,b in zip(got,expected):close(a,b,tol)
    elif expected is None:assert got is None
    elif isinstance(expected,bool):assert got is expected
    elif isinstance(expected,(int,float)):assert got==pytest.approx(expected,rel=0,abs=tol)
    else:assert got==expected

@pytest.mark.parametrize('reference',REFS,ids=lambda r:r['origin'][:30])
def test_upstream_reference(reference):
    reply=run(reference['input']);assert reply['ok'],reply
    close(reply['result'],reference['expected_subset'],reference['absolute_tolerance'])

def test_manifest_and_provenance():
    Draft202012Validator.check_schema(MANIFEST['inputs']);Draft202012Validator.check_schema(MANIFEST['outputs'])
    prov=MANIFEST['provenance'];assert prov['stars_at_mining']>=100;assert prov['repository_created_year']<2015
    assert len(prov['commit'])==40
    assert MANIFEST['license'] in ['MIT','BSD-3-Clause']
    assert hashlib.sha256((PACK/'LICENSE').read_bytes()).hexdigest()==prov['license_sha256']
    for e in prov['evidence']:assert hashlib.sha256((PACK/'upstream'/e['path']).read_bytes()).hexdigest()==e['sha256']
    for extra in prov.get('additional_licenses',[]):assert hashlib.sha256((PACK/extra['path']).read_bytes()).hexdigest()==extra['sha256']
    for line in prov['copyright_lines_verbatim']:assert line in (PACK/'NOTICE').read_text()
    assert MANIFEST['budget']['max_input_bytes']==65536
    assert MANIFEST['budget']['timeout_seconds']==10

def test_example_repeatable():assert run(EXAMPLE)==run(EXAMPLE)

def test_missing_input_rejected():assert run({})['ok'] is False

def test_additional_field_rejected():assert run(dict(EXAMPLE,unknown_field=0))['ok'] is False

@pytest.mark.parametrize('bad',[True,'3',None])
def test_no_type_coercion(bad):
    p=dict(EXAMPLE);p[MANIFEST['inputs']['required'][0]]=bad
    assert run(p)['ok'] is False

@pytest.mark.parametrize('literal',['NaN','Infinity','-Infinity'])
def test_nonfinite_json_rejected(literal):assert run_raw(('{"x":'+literal+'}').encode())['ok'] is False

def test_duplicate_json_keys_rejected():assert run_raw(b'{"x":1,"x":2}')['ok'] is False

def test_invalid_json_rejected():assert run_raw(b'{not json}')['ok'] is False

def test_byte_ceiling():
    assert run_raw(b' '*65537+b'{}')['ok'] is False
    raw=json.dumps(EXAMPLE,separators=(',',':')).encode()
    assert len(raw)<65536
    assert run_raw(raw+b' '*(65536-len(raw)))['ok'] is True

def test_array_root_rejected():assert run_raw(b'[]')['ok'] is False


# Supplementary properties do not replace pinned-source numerical references.
def core(p):
    import importlib.util
    sys.path.insert(0,str(PACK/'tool'))
    spec=importlib.util.spec_from_file_location('numerical_'+PACK.name,PACK/'tool/main.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.calculate(p)

def test_halving_fixed_steps_improves_analytic_solution():
    p={'matrix':[[-1,-5],[1,1]],'initial':[0,2],'t0':0,'t1':1,'steps':2}
    expected=[-5*math.sin(2),2*math.cos(2)+math.sin(2)];coarse=core(p)['state'];fine=core(dict(p,steps=4))['state']
    ec=max(abs(a-b) for a,b in zip(coarse,expected));ef=max(abs(a-b) for a,b in zip(fine,expected));assert ef<ec/30

def test_raw_indicator_and_h_scaled_adapter():
    p={'matrix':[[1]],'initial':[1],'t0':0,'t1':.5,'steps':1};r=core(p)
    assert r['last_local_error_estimate'][0]==.5*r['last_error_indicator'][0]
    # Reconstruct the distinct embedded endpoint from the source tableau.
    import importlib.util
    spec=importlib.util.spec_from_file_location('rk_core',PACK/'tool/main.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);k=[]
    for row in m.A:k.append(1+.5*sum(row[i]*k[i] for i in range(len(row))))
    alternate=1+.5*(41/840*(k[0]+k[10])+34/105*k[5]+9/35*(k[6]+k[7])+9/280*(k[8]+k[9]))
    assert alternate-r['state'][0]==pytest.approx(r['last_local_error_estimate'][0],abs=5e-16)

def test_zero_interval_and_dimensions():
    r=core({'matrix':[[1]],'initial':[3],'t0':2,'t1':2,'steps':10})
    assert r['state']==[3];assert r['last_error_indicator']==[0];assert r['evaluations']==0
    assert not run({'matrix':[[1,2]],'initial':[1],'t0':0,'t1':1,'steps':1})['ok']
