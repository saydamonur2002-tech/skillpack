import hashlib,json,math,os,subprocess,sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
PACK=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((PACK/'manifest.json').read_text(encoding='utf-8'))
EXAMPLE=json.loads((PACK/'example.json').read_text(encoding='utf-8'))
REFS=json.loads((PACK/'tests'/'references.json').read_text(encoding='utf-8'))
ENV=dict(os.environ)
for _k in ('SKILLPACK_TIMEOUT_SECONDS','SKILLPACK_MAX_FILE_MB','SKILLPACK_FILES_DIR'):ENV.pop(_k,None)
ALLOWED={'MIT','BSD-2-Clause','BSD-3-Clause','Apache-2.0','ISC','PSF-2.0'}

def run_raw(raw,env=None):
    proc=subprocess.run([sys.executable,str(PACK/'tool'/'main.py')],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,env=env or ENV)
    assert proc.stderr==b'',proc.stderr.decode(errors='replace')
    assert proc.stdout.count(b'\n')==1
    value=json.loads(proc.stdout.decode('utf-8'));Draft202012Validator(MANIFEST['outputs']).validate(value)
    assert proc.returncode==(0 if value['ok'] else 2)
    return value

def run(value,env=None):return run_raw(json.dumps(value,separators=(',',':'),allow_nan=False,ensure_ascii=False).encode(),env)

def close(got,expected,tol,rel=0.0):
    if isinstance(expected,dict):
        assert isinstance(got,dict),(got,expected)
        for k,v in expected.items():assert k in got,k;close(got[k],v,tol,rel)
    elif isinstance(expected,list):
        assert isinstance(got,list) and len(got)==len(expected),(got,expected)
        for a,b in zip(got,expected):close(a,b,tol,rel)
    elif expected is None:assert got is None
    elif isinstance(expected,bool):assert got is expected
    elif isinstance(expected,(int,float)):assert not isinstance(got,bool) and got==pytest.approx(expected,rel=rel,abs=tol)
    else:assert got==expected

@pytest.mark.parametrize('reference',REFS,ids=lambda r:r['origin'][:40])
def test_reference(reference):
    reply=run(reference['input']);assert reply['ok'],reply
    close(reply['result'],reference['expected_subset'],reference['absolute_tolerance'],reference.get('relative_tolerance',0.0))

def test_manifest_and_provenance():
    Draft202012Validator.check_schema(MANIFEST['inputs']);Draft202012Validator.check_schema(MANIFEST['outputs'])
    prov=MANIFEST['provenance'];assert MANIFEST['license'] in ALLOWED
    notice=(PACK/'NOTICE').read_text(encoding='utf-8')
    for u in [prov]+prov.get('additional_licenses',[]):
        assert u['license_spdx'] in ALLOWED
        assert hashlib.sha256((PACK/u['license_path']).read_bytes()).hexdigest()==u['license_sha256']
        if u['source_kind']=='github':
            assert len(u['commit'])==40 and all(c in '0123456789abcdef' for c in u['commit'])
            for e in u['evidence']:assert hashlib.sha256((PACK/'upstream'/e['path']).read_bytes()).hexdigest()==e['sha256']
        else:
            assert u['source_kind']=='original' and u['evidence']==[]
        for line in u['copyright_lines_verbatim']:assert line in notice and line in (PACK/u['license_path']).read_text(encoding='utf-8')
    assert MANIFEST['budget']['max_input_bytes']==65536
    assert MANIFEST['budget']['timeout_seconds']==10
    assert MANIFEST['data']['network']=='none' and MANIFEST['data']['telemetry']=='none'
    assert MANIFEST['audit']['usta_approval']['status']=='pending' and MANIFEST['audit']['usta_approval']['approved_by'] is None

def test_example_repeatable():
    assert EXAMPLE==REFS[0]['input']
    assert run(EXAMPLE)==run(EXAMPLE)

def test_missing_input_rejected():assert run({})['ok'] is False

def test_additional_field_rejected():assert run(dict(EXAMPLE,unknown_field=0))['ok'] is False

@pytest.mark.parametrize('bad',[True,3.5,None,[]])
def test_no_type_coercion(bad):
    key=MANIFEST['inputs']['required'][0];p=dict(EXAMPLE);p[key]=bad
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

def test_rejection_message_never_echoes_values():
    secret='ZZQX'+'7'*20
    key=MANIFEST['inputs']['required'][0];p=dict(EXAMPLE);p[key]=secret
    reply=run(p)
    if reply['ok'] is False:assert secret not in json.dumps(reply,ensure_ascii=False)

def test_no_network_or_code_execution_in_tool():
    for f in (PACK/'tool').rglob('*.py'):
        t=f.read_text(encoding='utf-8')
        for token in ['urllib','requests','socket','http.client','subprocess','eval(','exec(','pickle','logging']:assert token not in t,(f.name,token)

def core(p):
    import importlib.util
    sys.path.insert(0,str(PACK/'tool'))
    spec=importlib.util.spec_from_file_location('core_'+PACK.name,PACK/'tool/main.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.calculate(p)

# ---- pack-specific tests below ----

def test_vendored_files_match_upstream():
    for f in (PACK/'tool'/'pathfinding').rglob('*.py'):
        assert f.read_bytes()==(PACK/'upstream'/f.relative_to(PACK/'tool')).read_bytes(),f

def test_blocked_or_outside_rejected():
    assert run({'operation':'find_path','grid':['.#'],'queries':[{'start':[0,0],'end':[1,0]}]})['ok'] is False
    assert run({'operation':'find_path','grid':['..'],'queries':[{'start':[0,0],'end':[5,0]}]})['ok'] is False
    assert run({'operation':'find_path','grid':['.x'],'queries':[{'start':[0,0],'end':[0,0]}]})['ok'] is False

def test_path_is_contiguous():
    r=run(EXAMPLE)['result']['results'][0]
    for (a,b),(c,d) in zip(r['path'],r['path'][1:]):assert abs(a-c)+abs(b-d)==1
