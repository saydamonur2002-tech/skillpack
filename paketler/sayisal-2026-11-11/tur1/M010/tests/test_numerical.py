import importlib.util,json,math
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location("local_test_helpers_"+Path(__file__).parents[1].name,Path(__file__).with_name("test_pack.py"))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
run=h.run;close=h.close;REFS=h.REFS

def test_isolated_normalized_vertex():
    r=run({'adjacency':[[0,1,0],[1,0,0],[0,0,0]],'kind':'normalized'});assert r['ok'];close(r['result']['laplacian'],[[1,-1,0],[-1,1,0],[0,0,0]],0)

def test_combinatorial_nullspace_and_symmetry():
    r=run({'adjacency':[[0,2,0],[2,0,1],[0,0,0]]});assert r['ok'];L=r['result']['laplacian'];assert r['result']['directed_input'] is True
    assert all(abs(sum(row))<1e-14 for row in L);assert all(L[i][j]==L[j][i] for i in range(3) for j in range(3))

def test_self_loop_handling():
    r=run({'adjacency':[[2]]});assert r['ok'];close(r['result']['laplacian'],[[0]],0)
    r=run({'adjacency':[[2]],'kind':'normalized'});assert r['ok'];close(r['result']['laplacian'],[[0]],0)

@pytest.mark.parametrize('p',[{'adjacency':[[0,1],[1]]},{'adjacency':[[0,-1],[-1,0]]}])
def test_bad_graph_rejected(p):assert not run(p)['ok']
