import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

def test_even_length_and_negative_values():
    r=run({'data':[-5,-3,-1,1]});assert r['ok'];close(r['result'],{'median':-2,'mad':2},0)

def test_translation_equivariance():
    a=run({'data':[1,2,3,9]})['result'];b=run({'data':[101,102,103,109]})['result'];assert a['mad']==b['mad'];assert b['median']==a['median']+100

def test_zero_mad_is_not_constant_claim():
    r=run({'data':[1,1,1,100]});assert r['ok'];assert r['result']['mad']==0
