import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

def test_upstream_sine_error_bound():
    x=[math.pi*i/4 for i in range(5)];q=[math.pi*i/99 for i in range(100)]
    r=run({'x':x,'y':[math.sin(t) for t in x],'query':q})
    assert r['ok'];assert max(abs(v-math.sin(t)) for v,t in zip(r['result']['values'],q))<.012

def test_upstream_quadratic_extrapolation_and_derivatives():
    x=[i/10 for i in range(11)];q=[-10,10]
    r=run({'x':x,'y':[t*t for t in x],'query':q});assert r['ok'],r
    close(r['result'],{'values':[100,100],'first_derivatives':[-20,20],'second_derivatives':[2,2]},1e-10)

def test_upstream_sine_extrapolation_bounds():
    x=[math.pi*i/20 for i in range(11)];q=[-math.pi/2,3*math.pi/4]
    r=run({'x':x,'y':[math.sin(t) for t in x],'query':q});assert r['ok'],r
    for field,fn,tol in [('values',math.sin,.05),('first_derivatives',math.cos,.2),('second_derivatives',lambda z:-math.sin(z),.52)]:
        assert max(abs(a-fn(b)) for a,b in zip(r['result'][field],q))<tol

def test_natural_boundary_zero_second_derivative():
    r=run({'x':[0,1,2,3],'y':[0,2,1,5],'query':[0,3],'boundary':'natural'});assert r['ok']
    close(r['result']['second_derivatives'],[0,0],1e-12)

@pytest.mark.parametrize('p',[{'x':[0,1,1,3],'y':[0,1,2,3],'query':[1]},{'x':[0,1,2,3],'y':[0,1,2,3,4],'query':[1]}])
def test_bad_knots_rejected(p):assert not run(p)['ok']
