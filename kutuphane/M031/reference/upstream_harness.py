"""Runs networkx 3.6.1 dijkstra_predecessor_and_distance on the same graphs; no network."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _nx_common import nx,mapdata,graph,sums
out=[]
for p in json.load(sys.stdin):
    prof=p.get('profile','car');opt=p.get('optimize','time');ms=p.get('max_snap_m',300)
    coords,adj,G=graph(p['dataset'],prof,opt)
    def back(pred,o,d):
        path=[d]
        while path[-1]!=o:path.append(pred[path[-1]][0])
        return path[::-1]
    if p['operation']=='matrix':
        os_=[mapdata.snap(coords,adj,s['lat'],s['lon'],'out',ms)[0] for s in p['origins']]
        ds_=[mapdata.snap(coords,adj,s['lat'],s['lon'],'in',ms)[0] for s in p['destinations']]
        D=[];T=[]
        for o in os_:
            pred,dist=nx.dijkstra_predecessor_and_distance(G,o,weight='weight');rd=[];rt=[]
            for d in ds_:
                if d not in dist:rd.append(None);rt.append(None);continue
                L,t=sums(G,back(pred,o,d));rd.append(round(L,1));rt.append(round(t,1))
            D.append(rd);T.append(rt)
        out.append({'distances_m':D,'durations_s':T})
    else:
        o=mapdata.snap(coords,adj,p['origin']['lat'],p['origin']['lon'],'out',ms)[0]
        pred,dist=nx.dijkstra_predecessor_and_distance(G,o,cutoff=p['max_minutes']*60.0,weight='weight')
        segs=sum(1 for u in dist for v in G.successors(u) if v in dist and (u<v or not G.has_edge(v,u)))
        far=max(dist,key=lambda v:(dist[v],-v))
        out.append({'reachable_vertices':len(dist),'reachable_segments':segs,'farthest':{'lat':coords[far][0],'lon':coords[far][1],'minutes':round(dist[far]/60,2)}})
sys.stdout.write(json.dumps(out))
