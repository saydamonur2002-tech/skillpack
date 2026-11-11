import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

def test_energy_conservation_and_roundtrip():
    import random
    rng=random.Random(20261111);data=[rng.uniform(-100,100) for _ in range(32)];r=run({'data':data});assert r['ok'];z=r['result']
    assert sum(x*x for x in data)==pytest.approx(sum(x*x for x in z['approximation']+z['detail']),rel=1e-14)
    close(z['reconstructed'],data,1e-12)

def test_detail_sign_matches_pair_difference():
    r=run({'data':[1,3]});assert r['ok'];assert r['result']['detail'][0]==pytest.approx(-math.sqrt(2))

def test_odd_length_explicitly_rejected():assert not run({'data':[1,2,3]})['ok']
