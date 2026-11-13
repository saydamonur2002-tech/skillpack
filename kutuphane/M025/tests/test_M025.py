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


LITERAL_CHECKS=[(0, 'geohash', 'ww8p1r4t8'), (1, 'geohash', 'wte'), (3, 'clockwise_from_north', ['dqcjw', 'dqcjx', 'dqcjr', 'dqcjp', 'dqcjn', 'dqcjj', 'dqcjm', 'dqcjt']), (4, 'clockwise_from_north', ['dqcjw', 'dqcjx', 'dqcjr', 'dqcjp', 'dqcjn', 'dqcjj', 'dqcjm', 'dqcjt']), (5, 'clockwise_from_north', ['21208', '21209', '21203', '21201', '21200', 'rcrbp', 'rcrbr', 'rcrbx'])]

def test_upstream_literals():
    for idx,key,value in LITERAL_CHECKS:
        assert run(REFS[idx]['input'])['result'][key]==value

def test_upstream_decode_tolerance():
    r=run({'operation':'decode','geohash':'ww8p1r4t8'})['result']
    assert abs(r['latitude']-37.8324)<1e-4 and abs(r['longitude']-112.5584)<1e-4

def test_single_char_neighbours_literal():
    nb=run({'operation':'neighbors','geohash':'r'})['result']['neighbors']
    assert (nb['northeast'],nb['east'],nb['southeast'])==('8','2','0')

def test_encode_decode_consistency():
    for lat,lon in [(0.1,0.1),(-33.9,151.2),(64.1,-21.9)]:
        h=core({'operation':'encode','latitude':lat,'longitude':lon,'length':10})['geohash']
        b=core({'operation':'decode','geohash':h})['bbox'];assert b[0]<=lat<=b[2] and b[1]<=lon<=b[3]

@pytest.mark.parametrize('p',[{'operation':'decode','geohash':'abc'},{'operation':'decode','geohash':'ww8','latitude':1},{'operation':'encode','latitude':1},{'operation':'encode','latitude':91,'longitude':0}])
def test_rejections(p):assert run(p)['ok'] is False
