import shutil,subprocess,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
RUNNERS=sorted(ROOT.glob('M*/reference/verify_native.py'))
@pytest.mark.parametrize('runner',RUNNERS,ids=lambda p:p.parents[1].name)
def test_native_upstream_rerun(runner):
    if shutil.which('gcc') is None:pytest.skip('Optional native-reference rerun requires GCC; frozen numerical tests do not')
    result=subprocess.run([sys.executable,str(runner)],cwd=runner.parents[1],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
    assert result.returncode==0,result.stderr.decode()+result.stdout.decode()
    assert 'native reference rerun passed' in result.stdout.decode()
