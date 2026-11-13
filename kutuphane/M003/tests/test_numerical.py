import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

@pytest.mark.parametrize('lat1,lon1,lat2,lon2',[(30,30,60,60),(60,60,30,30),(30,60,60,30),(60,30,30,60),(30,-30,60,-60),(60,-60,30,-30),(30,-60,60,-30),(60,-30,30,-60),(-30,-30,-60,-60),(-60,-60,-30,-30),(-30,-60,-60,-30),(-60,-30,-30,-60),(-30,30,-60,60),(-60,60,-30,30),(-30,60,-60,30),(-60,30,-30,60)])
def test_upstream_all_quadrants(lat1,lon1,lat2,lon2):
    r=run(dict(lat1=lat1,lon1=lon1,lat2=lat2,lon2=lon2));assert r['ok'],r
    assert r['result']['distance_m']==pytest.approx(4015703.021,abs=1e-6)

@pytest.mark.parametrize('lat2,lon2',[(.5,179.7),(-5.1,179.4)])
def test_upstream_nonconvergence(lat2,lon2):
    r=run({'lat1':0 if lat2==.5 else 5,'lon1':0,'lat2':lat2,'lon2':lon2});assert not r['ok']
    assert 'converge' in r['error']['message']

@pytest.mark.parametrize('lat1,lon1,lat2,lon2',[(0,180,0,-180),(90,-80,90,70)])
def test_equivalent_coordinate_adapter_hardening(lat1,lon1,lat2,lon2):
    r=run(dict(lat1=lat1,lon1=lon1,lat2=lat2,lon2=lon2));assert r['ok'];close(r['result'],{'distance_m':0,'initial_bearing_deg':None,'final_bearing_deg':None},0)
