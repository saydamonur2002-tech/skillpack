import hashlib,json,os,re
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];PACKS=sorted(ROOT.glob('G[0-9][0-9][0-9]'))
ALLOWED={'MIT','BSD-2-Clause','BSD-3-Clause','Apache-2.0','ISC','PSF-2.0'}
EMAIL=re.compile(rb'[A-Za-z0-9._%+-]+@(?!example\.(?:com|org|net)\b)[A-Za-z0-9.-]+\.(?:com|org|net|io|dev|edu|gov|tr|co|uk|de|fr|eu|me|info|ca)\b')
FORBIDDEN=[p.encode() for p in os.environ.get('EKSTRA_IZ','').split('|') if p]  # kişiye özel ifadeler dosyaya yazılmaz; çalıştırırken EKSTRA_IZ ile verilir
TELEMETRY=[b'sendBeacon',b'google-analytics',b'gtag(',b'XMLHttpRequest',b'navigator.geolocation']
SKIP_DIRS={'__pycache__','.pytest_cache','.venv','wheels'}
def text_files(base):
    for f in base.rglob('*'):
        if f.is_file() and not SKIP_DIRS&set(f.parts) and f.suffix not in('.whl','.zip','.png'):yield f
def verbatim(pack):
    v=set()
    def walk(o):
        if isinstance(o,dict):
            for k,x in o.items():
                if k in('sha256','license_sha256') and isinstance(x,str):v.add(x)
                else:walk(x)
        elif isinstance(o,list):
            for x in o:walk(x)
    walk(json.loads((pack/'manifest.json').read_text())['provenance']);return v
def test_pack_identifiers():assert [p.name for p in PACKS]==['G%03d'%i for i in range(1,13)]
@pytest.mark.parametrize('pack',PACKS,ids=lambda p:p.name)
def test_required_artifacts_and_no_contact_strings(pack):
    m=json.loads((pack/'manifest.json').read_text())
    req=['manifest.json','SKILL.md','TEACHING.md','SOURCE.md','NOTICE','LICENSE','REFERENCE_RUN.md','example.json','requirements.txt','requirements-test.txt','pytest.ini','tool/main.py','tool/runtime.py','mcp/server.py','tests/references.json','FILES.sha256']
    if m['provenance']['source_kind']=='github':req+=['reference/verify_upstream.py','reference/harness.json']
    for n in req:assert (pack/n).is_file(),n
    vb=verbatim(pack)
    for f in text_files(pack):
        raw=f.read_bytes()
        if hashlib.sha256(raw).hexdigest() in vb or 'upstream' in f.parts or f.parent.name=='licenses':continue
        assert not EMAIL.search(raw),str(f.relative_to(ROOT))
def test_no_personal_identity_civil_service_or_telemetry():
    for f in text_files(ROOT):
        if 'upstream' in f.parts or f.parent.name=='licenses' or f.name=='test_release_audit.py':continue
        low=f.read_bytes().lower()
        for t in FORBIDDEN:assert t not in low,(str(f.relative_to(ROOT)),t)
        if f.suffix in('.js','.html','.py') and f.relative_to(ROOT).as_posix()!='G012/tool/main.py':  # main.py holds the deny-list itself
            for t in TELEMETRY:assert t.lower() not in low,(str(f.relative_to(ROOT)),t)
@pytest.mark.parametrize('pack',PACKS,ids=lambda p:p.name)
def test_files_sha256(pack):
    for line in (pack/'FILES.sha256').read_text().splitlines():
        d,n=line.split('  ',1);assert hashlib.sha256((pack/n).read_bytes()).hexdigest()==d,n
def test_licenses_author_and_usta_pending():
    for pack in PACKS:
        m=json.loads((pack/'manifest.json').read_text())
        assert m['license'] in ALLOWED and m['provenance']['license_spdx']==m['license'] and m['author']=='Skillpack contributors'
        for x in m['provenance']['additional_licenses']:assert x['license_spdx'] in ALLOWED
        lic=(pack/'LICENSE').read_bytes().upper();assert b'GNU GENERAL PUBLIC' not in lic and b'LESSER GENERAL' not in lic
        assert m['audit']['usta_approval']['status']=='pending' and m['audit']['usta_approval']['approved_by'] is None
        assert m['data']['network']=='none' and m['data']['telemetry']=='none'
        sk=(pack/'SKILL.md').read_text();assert sk.startswith('---\nname: '+m['mcp']['server_name']+'\ndescription: ')
        assert 'usta_approval: pending' in sk
        for f in (pack/'tool').rglob('*.py'):
            t=f.read_text()
            for tok in ['eval(','exec(','urllib','requests','socket','subprocess','http.client','logging']:assert tok not in t,(f,tok)
        assert 'transport="stdio"' in (pack/'mcp'/'server.py').read_text()
        assert set((pack/'requirements.txt').read_text().split())<={'jsonschema==4.26.0','mcp==1.30.0'}
def test_catalog_config_and_flow_match():
    cat=json.loads((ROOT/'catalog.json').read_text());assert [e['id'] for e in cat['entries']]==[p.name for p in PACKS]
    cfg=json.loads((ROOT/'claude_desktop_config.json').read_text())['mcpServers'];assert len(cfg)==12
    for e in cat['entries']:
        m=json.loads((ROOT/e['manifest']).read_text());assert m['mcp']['server_name']==e['mcp_server'] and e['mcp_server'] in cfg
    flow=json.loads((ROOT/'flows'/'oyun-kur.flow.json').read_text())
    used={s['skill'] for s in flow['steps']};assert used=={p.name for p in PACKS}
@pytest.mark.skipif(not (ROOT/'wheels').is_dir(),reason='wheels/ bu depoda yer almaz (boyut ve üçüncü taraf ikili dosyalar); bağımlılıklar requirements-*.txt içindeki sabit sürümlerle kurulur')
def test_offline_requirements_cover_runtime():
    off={l.strip() for l in (ROOT/'requirements-offline.txt').read_text().splitlines() if l.strip() and not l.startswith('#')}
    for r in ['jsonschema==4.26.0','mcp==1.30.0','pytest==9.2.0']:assert r in off
    whl=[f.name.lower() for f in (ROOT/'wheels').glob('*.whl')]
    for r in off:
        name=r.split('==')[0].replace('-','_').lower();assert any(w.startswith(name+'-') for w in whl),r
def test_generated_html_blocked_by_builder_denylist():
    src=(ROOT/'G012'/'tool'/'main.py').read_text()
    for t in ['sendBeacon','XMLHttpRequest']:assert t in src
