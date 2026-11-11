import hashlib,json,re
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];PACKS=sorted(ROOT.glob('M[0-9][0-9][0-9]'))

def test_ten_unique_new_identifiers():assert [p.name for p in PACKS]==['M%03d'%i for i in range(11,21)]

@pytest.mark.parametrize('pack',PACKS,ids=lambda p:p.name)
def test_required_artifacts_and_no_contact_strings(pack):
    required=['manifest.json','SKILL.md','TEACHING.md','SOURCE.md','NOTICE','LICENSE','REFERENCE_RUN.md','example.json','requirements.txt','requirements-test.txt','pytest.ini','tool/main.py','tool/runtime.py','mcp/server.py','tests/references.json']
    for name in required:assert (pack/name).is_file(),name
    pattern=re.compile(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    for f in pack.rglob('*'):
        if f.is_file() and '__pycache__' not in f.parts and '.pytest_cache' not in f.parts:
            assert not pattern.search(f.read_bytes()),str(f.relative_to(ROOT))

def test_selected_licenses_and_no_runtime_network():
    for pack in PACKS:
        m=json.loads((pack/'manifest.json').read_text());assert m['license']=='BSD-3-Clause'
        text=(pack/'tool/main.py').read_text()
        for token in ['eval(', 'exec(', 'urllib', 'requests', 'socket', 'subprocess']:assert token not in text
        assert "transport=\"stdio\"" in (pack/'mcp/server.py').read_text()
