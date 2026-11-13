import hashlib,json,math,os,subprocess,sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
PACK=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((PACK/'manifest.json').read_text())
EXAMPLE=json.loads((PACK/'example.json').read_text())
REFS=json.loads((PACK/'tests'/'references.json').read_text())
FIX=PACK/'tests'/'fixtures'
ENV=dict(os.environ,SKILLPACK_MAP_DATA=str(FIX))
ENV.pop('SKILLPACK_MAP_OUTPUT',None)

def run_raw(raw,env=None):
    proc=subprocess.run([sys.executable,str(PACK/'tool'/'main.py')],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=12,env=env or ENV)
    assert proc.stderr==b'',proc.stderr.decode(errors='replace')
    assert proc.stdout.count(b'\n')==1
    value=json.loads(proc.stdout);Draft202012Validator(MANIFEST['outputs']).validate(value)
    assert proc.returncode==(0 if value['ok'] else 2)
    return value

def run(value,env=None):return run_raw(json.dumps(value,separators=(',',':'),allow_nan=False,ensure_ascii=False).encode(),env)

def close(got,expected,tol):
    if isinstance(expected,dict):
        for k,v in expected.items():assert k in got,k;close(got[k],v,tol)
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
    for extra in prov.get('additional_licenses',[]):
        assert extra['license_spdx'] in ['MIT','BSD-2-Clause','BSD-3-Clause']
        assert hashlib.sha256((PACK/extra['path']).read_bytes()).hexdigest()==extra['sha256']
        for e in extra['evidence']:assert hashlib.sha256((PACK/'upstream'/e['path']).read_bytes()).hexdigest()==e['sha256']
        for line in extra['copyright_lines_verbatim']:assert line in (PACK/'NOTICE').read_text()
    for line in prov['copyright_lines_verbatim']:assert line in (PACK/'NOTICE').read_text()
    assert MANIFEST['budget']['max_input_bytes']==65536
    assert MANIFEST['budget']['timeout_seconds']==10

def test_example_repeatable():
    assert EXAMPLE==REFS[0]['input']
    assert run(EXAMPLE)==run(EXAMPLE)

def test_missing_input_rejected():assert run({})['ok'] is False

def test_additional_field_rejected():assert run(dict(EXAMPLE,unknown_field=0))['ok'] is False

@pytest.mark.parametrize('bad',[True,'3',None,7])
def test_no_type_coercion(bad):
    p=dict(EXAMPLE);p['operation']=bad
    assert run(p)['ok'] is False

@pytest.mark.parametrize('literal',['NaN','Infinity','-Infinity'])
def test_nonfinite_json_rejected(literal):assert run_raw(('{"x":'+literal+'}').encode())['ok'] is False

def test_duplicate_json_keys_rejected():assert run_raw(b'{"x":1,"x":2}')['ok'] is False

def test_invalid_json_rejected():assert run_raw(b'{not json}')['ok'] is False

def test_byte_ceiling():
    assert run_raw(b' '*65537+b'{}')['ok'] is False
    raw=json.dumps(EXAMPLE,separators=(',',':'),ensure_ascii=False).encode()
    assert len(raw)<65536
    assert run_raw(raw+b' '*(65536-len(raw)))['ok'] is True

def test_array_root_rejected():assert run_raw(b'[]')['ok'] is False

def test_no_network_imports():
    for f in (PACK/'tool').glob('*.py'):
        t=f.read_text()
        for token in ['urllib','requests','socket','http.client','subprocess','eval(','exec(']:assert token not in t,(f.name,token)

# Supplementary properties do not replace pinned-source numerical references.
def core(p):
    import importlib.util
    os.environ['SKILLPACK_MAP_DATA']=str(FIX)
    sys.path.insert(0,str(PACK/'tool'))
    spec=importlib.util.spec_from_file_location('numerical_'+PACK.name,PACK/'tool/main.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.calculate(p)


def test_upstream_display_literals():
    d=run(REFS[0]['input'])['result'];assert (round(d['lat'],4),round(d['lon'],4))==(51.5136,-0.0983)
    b=run(REFS[1]['input'])['result'];assert (round(b['initial_bearing_deg'],1),round(b['final_bearing_deg'],1))==(156.2,157.9)
    assert round(run(REFS[2]['input'])['result']['initial_bearing_deg'],1)==337.9
    c=run(REFS[3]['input'])['result'];assert c['initial_bearing_deg'] is None and c['final_bearing_deg'] is None
    m=run(REFS[4]['input'])['result'];assert (round(m['lat'],4),round(m['lon'],4))==(50.5363,1.2746)
    assert round(run(REFS[5]['input'])['result']['distance_m'])==404279
    assert round(run(REFS[6]['input'])['result']['distance_m'],1)==251.2
    assert round(run(REFS[7]['input'])['result']['cross_track_m'],1)==-307.5

def test_compass_labels():
    assert run(REFS[1]['input'])['result']['compass']=={'en':'SSE','tr':'GGD'}

def test_destination_then_bearing_roundtrip():
    s={'lat':40.993,'lon':29.023};d=core({'operation':'destination','from':s,'distance_m':800,'bearing_deg':60})
    b=core({'operation':'bearing','from':s,'to':{'lat':d['lat'],'lon':d['lon']}});assert abs(b['initial_bearing_deg']-60)<1e-6
    r=core({'operation':'distance','from':s,'to':{'lat':d['lat'],'lon':d['lon']}});assert abs(r['distance_m']-800)<1e-6

@pytest.mark.parametrize('p',[{'operation':'destination','from':{'lat':0,'lon':0},'distance_m':10},{'operation':'bearing','from':{'lat':0,'lon':0}},{'operation':'cross_track','from':{'lat':0,'lon':0},'to':{'lat':1,'lon':1}},{'operation':'distance','from':{'lat':91,'lon':0},'to':{'lat':0,'lon':0}},{'operation':'destination','from':{'lat':0,'lon':0},'distance_m':-1,'bearing_deg':0}])
def test_rejections(p):assert run(p)['ok'] is False
