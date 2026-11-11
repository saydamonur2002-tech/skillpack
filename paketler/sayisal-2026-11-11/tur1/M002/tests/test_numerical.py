import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

@pytest.mark.parametrize('order,nodes,weights',[(1,[-1,0,1],[-.5,0,.5]),(2,[-1,0,1],[1,-2,1]),(1,list(range(-3,4)),[-1/60,9/60,-45/60,0,45/60,-9/60,1/60]),(2,list(range(-3,4)),[2/180,-27/180,270/180,-490/180,270/180,-27/180,2/180])])
def test_upstream_central_weight_tables(order,nodes,weights):
    r=run({'nodes':nodes,'order':order});assert r['ok'];close(r['result']['weights'],weights,1e-14)

def test_upstream_exp_derivative_doctest():
    x=[(-1+i*.5)*.001 for i in range(5)]
    r=run({'nodes':x,'order':1,'values':[math.exp(t) for t in x]});assert r['ok']
    assert r['result']['derivative']==pytest.approx(1,abs=1e-8)

@pytest.mark.parametrize('p',[{'nodes':[0,0,1]},{'nodes':[0,1],'order':2},{'nodes':[0,1,2],'values':[0,1]}])
def test_degenerate_inputs_rejected(p):assert not run(p)['ok']
