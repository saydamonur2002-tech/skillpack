"""Runs networkx 3.6.1 astar_path / dijkstra_path on the same graphs; no network."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _nx_common import nx,mapdata,graph,sums
out=[]
for p in json.load(sys.stdin):
    prof=p.get('profile','car');opt=p.get('optimize','time');alg=p.get('algorithm','astar')
    coords,adj,G=graph(p['dataset'],prof,opt)
    vmax=max(d['length_m']/d['time_s'] for _,_,d in G.edges(data=True))
    def h(u,v):
        d=mapdata.haversine(coords[u][0],coords[u][1],coords[v][0],coords[v][1]);return d if opt=='distance' else d/vmax
    stops=[p['origin']]+p.get('via',[])+[p['destination']];vs=[]
    for i,s in enumerate(stops):vs.append(mapdata.snap(coords,adj,s['lat'],s['lon'],'in' if i==len(stops)-1 else 'out',p.get('max_snap_m',300))[0])
    path=[]
    for a,b in zip(vs,vs[1:]):
        leg=[a] if a==b else (nx.dijkstra_path(G,a,b,weight='weight') if alg=='dijkstra' else nx.astar_path(G,a,b,heuristic=h,weight='weight'))
        path+=leg if not path else leg[1:]
    L,T=sums(G,path)
    out.append({'vertex_path':path,'distance_m':round(L,1),'duration_s':round(T,1)})
sys.stdout.write(json.dumps(out))
