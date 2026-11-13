import json,shutil,subprocess,sys
from importlib import metadata
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
RUNNERS=sorted(ROOT.glob('G*/reference/verify_upstream.py'))

def missing(req):
    if req.startswith('node'):return None if shutil.which('node') else req
    name,_,ver=req.partition('==')
    try:v=metadata.version(name)
    except metadata.PackageNotFoundError:return req
    return req if ver and v!=ver else None

@pytest.mark.parametrize('runner',RUNNERS,ids=lambda p:p.parents[1].name)
def test_upstream_rerun(runner):
    """Optional: re-executes the pinned upstream on every reference input. Skipped when the upstream oracle packages are not installed (they are not needed at runtime)."""
    h=json.loads((runner.parent/'harness.json').read_text())
    if h['runner']=='node' and shutil.which('node') is None:pytest.skip('Optional upstream rerun requires Node.js')
    gaps=[r for r in h.get('python_requirements',[]) if missing(r)]
    if gaps:pytest.skip('Optional upstream rerun requires '+', '.join(gaps))
    result=subprocess.run([sys.executable,str(runner)],cwd=runner.parents[1],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
    assert result.returncode==0,result.stderr.decode()+result.stdout.decode()
    assert 'upstream reference rerun passed' in result.stdout.decode()
