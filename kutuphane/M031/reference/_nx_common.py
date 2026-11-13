# Shared by the networkx reference harnesses. networkx itself is imported from the installed package,
# which must be the pinned release; its source files are checked byte-for-byte against upstream/ copies.
import hashlib,importlib,json,os,sys
from pathlib import Path
PACK=Path(__file__).resolve().parents[1]
os.environ.setdefault('SKILLPACK_MAP_DATA',str(PACK/'tests'/'fixtures'))
import networkx as nx
PIN='3.6.1'
if nx.__version__!=PIN:raise SystemExit('networkx %s required for the reference rerun, found %s'%(PIN,nx.__version__))
for rel in ('networkx/algorithms/shortest_paths/astar.py','networkx/algorithms/shortest_paths/weighted.py'):
    installed=Path(nx.__file__).resolve().parents[1]/rel
    if hashlib.sha256(installed.read_bytes()).hexdigest()!=hashlib.sha256((PACK/'upstream'/rel).read_bytes()).hexdigest():
        raise SystemExit('installed '+rel+' differs from the pinned upstream copy')
# Skillpack's own dataset loader and graph builder (not the ported search) are shared with the tool.
sys.path.insert(0,str(PACK/'tool'))
mapdata=importlib.import_module('mapdata')
def graph(dataset,profile,optimize):
    coords,adj,info=mapdata.build_graph(dataset,profile,optimize)
    G=nx.DiGraph();G.add_nodes_from(range(len(coords)))
    for u,a in enumerate(adj):
        for v,e in a.items():G.add_edge(u,v,weight=e['weight'],length_m=e['length_m'],time_s=e['time_s'])
    return coords,adj,G
def sums(G,path):
    L=sum(G[u][v]['length_m'] for u,v in zip(path,path[1:]));T=sum(G[u][v]['time_s'] for u,v in zip(path,path[1:]))
    return L,T
