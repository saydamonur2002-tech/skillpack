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


def test_oneway_detour_longer_than_walk():
    car=run(REFS[2]['input'])['result'];walk=run(REFS[3]['input'])['result']
    assert car['distance_m']>walk['distance_m']
    assert walk['vertex_path']==sorted(walk['vertex_path'],reverse=True) or len(walk['vertex_path'])==4

def test_astar_equals_dijkstra_cost():
    for prof in ('car','walk','bike'):
        for a,b in [((0,0),(3,3)),((3,1),(0,1)),((3,0),(3,3)),((1,2),(2,0))]:
            p={'operation':'route','dataset':'grid','origin':{'lat':41+a[1]*0.001,'lon':29+a[0]*0.001},'destination':{'lat':41+b[1]*0.001,'lon':29+b[0]*0.001},'profile':prof}
            x=core(p);y=core(dict(p,algorithm='dijkstra'));assert x['duration_s']==pytest.approx(y['duration_s'],abs=0.05)

def test_feature_is_renderable_geojson():
    f=run(REFS[0]['input'])['result']['feature'];assert f['type']=='Feature' and f['geometry']['type']=='LineString' and len(f['geometry']['coordinates'])>=2

def test_segments_sum():
    r=run(REFS[0]['input'])['result'];assert sum(s['distance_m'] for s in r['segments'])==pytest.approx(r['distance_m'],abs=0.5)

def test_csv_and_geojson_names_resolved():
    assert run(REFS[8]['input'])['ok']

def test_data_folder_env_required(tmp_path):
    env=dict(ENV,SKILLPACK_MAP_DATA=str(tmp_path/'missing'));r=run(REFS[0]['input'],env)
    assert r['ok'] is False and 'Map data folder not found' in r['error']['message']

@pytest.mark.parametrize('p',[
  {'operation':'route','dataset':'grid','origin':{'lat':41.0,'lon':29.0},'destination':{'lat':41.0005,'lon':29.006}},
  {'operation':'route','dataset':'../grid','origin':{'lat':41.0,'lon':29.0},'destination':{'lat':41.003,'lon':29.003}},
  {'operation':'route','dataset':'grid','origin':{'lat':42.0,'lon':29.0},'destination':{'lat':41.003,'lon':29.003}},
  {'operation':'route','dataset':'nope','origin':{'lat':41.0,'lon':29.0},'destination':{'lat':41.003,'lon':29.003}},
  {'operation':'route','dataset':'grid','origin':{'lat':41.0,'lon':29.0},'destination':{'lat':41.003,'lon':29.003},'profile':'truck'}])
def test_rejections(p):assert run(p)['ok'] is False
