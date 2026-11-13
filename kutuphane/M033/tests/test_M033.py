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


def test_sorted_and_within_radius():
    r=run(REFS[2]['input'])['result']['results'];d=[x['distance_m'] for x in r]
    assert d==sorted(d) and all(x<=5000 for x in d)
    assert all(x['category'] in ('cafe','pharmacy') for x in r)

def test_turkish_alias_matches_english():
    a=core({'operation':'nearby','dataset':'grid','center':{'lat':41.001,'lon':29.001},'radius_m':300,'categories':['eczane']})
    b=core({'operation':'nearby','dataset':'grid','center':{'lat':41.001,'lon':29.001},'radius_m':300,'categories':['pharmacy']})
    assert a['results']==b['results'] and a['categories_used']=={'eczane':['pharmacy']}

def test_features_for_renderer():
    f=run(REFS[0]['input'])['result']['features'];assert f['type']=='FeatureCollection' and all(x['geometry']['type']=='Point' for x in f['features'])

def test_upstream_distance_literals():
    # literals from upstream tests/geolib.test.js getDistance()
    import importlib.util;sys.path.insert(0,str(PACK/'tool'))
    spec=importlib.util.spec_from_file_location('nb',PACK/'tool/main.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    assert m.get_distance(52.518611,13.408056,51.519475,7.46694444)==422592
    assert m.get_distance(52.518611,13.408056,51.519475,7.46694444,100)==422600
    assert m.get_distance(37.774514,-122.418079,51.519475,7.46694444)==8980260
    assert m.get_distance(41.72977,-111.77621999999997,41.73198,-111.77636999999999)==246
    assert m.get_distance(41.72977,-111.77621999999997,41.73198,-111.77636999999999,1,3)==245.777

def test_csv_dataset():
    r=core({'operation':'nearby','dataset':'poi_list.csv','center':{'lat':41.003,'lon':29.001},'radius_m':1000})
    assert [x['name'] for x in r['results']]==['Kuzey Eczanesi','Güney Kafe']

@pytest.mark.parametrize('p',[{'operation':'nearby','dataset':'grid'},{'operation':'nearby','dataset':'grid','center':{'lat':41.0,'lon':29.0},'radius_m':0},{'operation':'nearby','dataset':'grid','center':{'lat':41.0,'lon':29.0},'limit':101}])
def test_rejections(p):assert run(p)['ok'] is False
