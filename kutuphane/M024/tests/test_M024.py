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


LITERAL_STRINGS=[(0, 'encoded', '_p~iF~ps|U_ulLnnqC_mqNvxq`@'), (1, 'coordinates', [[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]]), (2, 'coordinates', [[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]]), (3, 'coordinates', [[39, -120], [41, -121], [43, -126]]), (4, 'encoded', '_izlhA~rlgdF_{geC~ywl@_kwzCn`{nI'), (5, 'encoded', 'mAnFC@CH'), (6, 'encoded', '_p~iF~ps|U_ulLnnqC_mqNvxq`@'), (7, 'encoded', '?A?@'), (8, 'encoded', 'ss`{E~kbkTeAQw@J'), (9, 'encoded', ''), (10, 'coordinates', [])]

def test_upstream_literals():
    for idx,key,value in LITERAL_STRINGS:
        assert run(REFS[idx]['input'])['result'][key]==value

def test_identity_roundtrips():
    for coords,prec in [([[35.6,-82.55],[35.59985,-82.55015],[35.6,-82.55]],5),([[179.1234567895121,-179.1245965456112]],13)]:
        e=core({'operation':'encode','coordinates':coords,'precision':prec})['encoded']
        assert core({'operation':'decode','encoded':e,'precision':prec})['coordinates']==coords
    s='_chxEn`zvN\\\\]]'
    c=core({'operation':'decode','encoded':s})['coordinates']
    assert core({'operation':'encode','coordinates':c})['encoded']==s

def test_negative_value_survives():
    e=core({'operation':'encode','coordinates':[[-107.3741825,0]],'precision':7})['encoded']
    assert core({'operation':'decode','encoded':e,'precision':7})['coordinates'][0][0]<0

@pytest.mark.parametrize('p',[{'operation':'decode','encoded':'_p~iF~ps|U_'},{'operation':'decode','encoded':'abc '},{'operation':'encode'},{'operation':'decode','encoded':'??','coordinates':[]}])
def test_strict_rejections(p):assert run(p)['ok'] is False
