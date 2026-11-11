import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

def test_robust_translation_and_scale_equivariance():
    data=[1,3,5,500,2];base=run({'data':data})['result'];shift=run({'data':[x+100 for x in data]})['result'];scaled=run({'data':[3*x for x in data]})['result']
    assert shift['location']==pytest.approx(base['location']+100);assert shift['midvariance']==pytest.approx(base['midvariance'])
    assert scaled['location']==pytest.approx(3*base['location']);assert scaled['scale']==pytest.approx(3*base['scale'])

def test_mostly_constant_matches_upstream_mad_zero_branch():
    r=run({'data':[1,1,1,100]});assert r['ok'];close(r['result'],{'location':1,'midvariance':0,'scale':0},0)

def test_scale_square_is_midvariance():
    r=run({'data':[1,3,5,500,2]});assert r['ok'];assert r['result']['scale']**2==pytest.approx(r['result']['midvariance'])

def test_nonpositive_tuning_rejected():assert not run({'data':[1,2,3],'location_c':0})['ok']
