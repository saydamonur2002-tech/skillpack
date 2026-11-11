import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

@pytest.mark.parametrize('index',range(8))
def test_upstream_masked_gaussian(index):
    p=json.loads(json.dumps(REFS[index]['input']));ny=len(p['data']);nx=len(p['data'][0]);p['data'][15][11]=1e5;p['mask']=[[False]*nx for _ in range(ny)];p['mask'][15][11]=True
    r=run(p);assert r['ok'],r;close(r['result'],{'x':25.7,'y':26.2},.001)

@pytest.mark.parametrize('p',[{'data':[[0,0],[0,0]]},{'data':[[1,-1]]},{'data':[[1,2],[3]]},{'data':[[1,2],[3,4]],'mask':[[False]]}])
def test_undefined_or_bad_image_rejected(p):assert not run(p)['ok']
