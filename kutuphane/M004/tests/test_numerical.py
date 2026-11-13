import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

def test_distance_symmetry_and_radius_scaling():
    p={'lat1':52.205,'lon1':.119,'lat2':48.857,'lon2':2.351};a=run(p)['result']['distance_m'];b=run({'lat1':p['lat2'],'lon1':p['lon2'],'lat2':p['lat1'],'lon2':p['lon1']})['result']['distance_m']
    assert a==pytest.approx(b);assert run(dict(p,radius_m=12742000))['result']['distance_m']==pytest.approx(2*a)

@pytest.mark.parametrize('lon2',[0,180])
def test_undefined_bearings_are_null(lon2):
    r=run({'lat1':0,'lon1':0,'lat2':0,'lon2':lon2});assert r['ok'];assert r['result']['initial_bearing_deg'] is None

def test_zero_radius_rejected():assert not run({'lat1':0,'lon1':0,'lat2':1,'lon2':1,'radius_m':0})['ok']
