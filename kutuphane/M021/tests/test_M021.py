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
    assert MANIFEST['license'] in ['MIT','BSD-2-Clause','BSD-3-Clause']
    assert hashlib.sha256((PACK/'LICENSE').read_bytes()).hexdigest()==prov['license_sha256']
    for e in prov['evidence']:assert hashlib.sha256((PACK/'upstream'/e['path']).read_bytes()).hexdigest()==e['sha256']
    for extra in prov.get('additional_licenses',[]):assert hashlib.sha256((PACK/extra['path']).read_bytes()).hexdigest()==extra['sha256']
    for line in prov['copyright_lines_verbatim']:assert line in (PACK/'NOTICE').read_text()
    assert MANIFEST['budget']['max_input_bytes']==65536
    assert MANIFEST['budget']['timeout_seconds']==10

def test_example_repeatable():
    assert EXAMPLE==REFS[0]['input']
    assert run(EXAMPLE)==run(EXAMPLE)

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


LITERAL_CHECKS=[(0, 'points', [[224.55, 250.15], [267.76, 213.81], [296.91, 155.64], [330.33, 137.57], [409.52, 141.14], [439.6, 119.74], [486.51, 106.75], [529.57, 127.86], [539.27, 147.24], [617.74, 159.86], [629.55, 194.6], [671.55, 222.55], [727.81, 213.36], [739.94, 204.77], [769.98, 208.42], [779.6, 216.87], [800.24, 214.62], [820.77, 236.17], [859.88, 255.49], [865.21, 268.53], [857.95, 280.3], [867.79, 306.17], [859.87, 311.37], [854.54, 335.4], [860.92, 343], [849.84, 359.59], [854.56, 365.53], [844.09, 371.89], [839.57, 390.4], [848.4, 407.55], [839.51, 432.76], [853.97, 471.15], [866.36, 480.77]])]

def test_upstream_literal_simplified_array():
    for idx,key,value in LITERAL_CHECKS:
        assert run(REFS[idx]['input'])['result'][key]==value
    assert run(REFS[6]['input'])['result']['points']==[[1,2]]
    assert run(REFS[7]['input'])['result']['points']==[]

def test_kept_indices_are_increasing_and_endpoints_kept():
    for ref in REFS:
        idx=core(ref['input'])['kept_indices']
        assert idx==sorted(set(idx))
        if len(ref['input']['points'])>2:assert idx[0]==0 and idx[-1]==len(ref['input']['points'])-1

def test_deep_input_no_recursion_error():
    pts=[[i,(i%2)*1000.0] for i in range(1500)]
    assert core({'points':pts,'tolerance':0.1,'highest_quality':True})['output_count']==1500

@pytest.mark.parametrize('p',[{'points':[[1,2,3]]},{'points':[[0,0]],'tolerance':-1},{'points':[['1',2]]}])
def test_bad_points_rejected(p):assert run(p)['ok'] is False
