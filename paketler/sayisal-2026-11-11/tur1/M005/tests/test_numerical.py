import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

def test_upstream_bearing_at_original_precision():
    r=run({'lat1':51.127,'lon1':1.338,'lat2':50.964,'lon2':1.853});assert r['ok'];assert r['result']['bearing_deg']==pytest.approx(116.7,abs=.05)

def test_upstream_antimeridian_equivalence():
    a=run({'lat1':1,'lon1':-179,'lat2':1,'lon2':179})['result']['distance_m'];b=run({'lat1':1,'lon1':1,'lat2':1,'lon2':-1})['result']['distance_m'];assert a==pytest.approx(b,abs=1e-6)

def test_upstream_east_west_limit():
    r=run({'lat1':1,'lon1':-1,'lat2':1,'lon2':1});assert r['ok'];assert r['result']['distance_m']==pytest.approx(222400,abs=50)

@pytest.mark.parametrize('lat',[-90,90])
def test_poles_explicitly_rejected(lat):assert not run({'lat1':lat,'lon1':0,'lat2':0,'lon2':1})['ok']

def test_coincident_bearing_null():
    r=run({'lat1':51.127,'lon1':1.338,'lat2':51.127,'lon2':1.338});assert r['ok'];assert r['result']['bearing_deg'] is None
