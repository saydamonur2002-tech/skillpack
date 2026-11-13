#!/usr/bin/env python3
"""Travel-time/distance matrix and isochrone (reachable roads within N minutes). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
from heapq import heappush,heappop
from itertools import count
import mapdata

def dijkstra_pred(adj,source,cutoff=None):
    """Port of networkx _dijkstra_multisource with a pred dict (networkx 3.6.1, weighted.py), single source, no target."""
    pred={source:[]};dist={};seen={source:0};c=count();fringe=[];heappush(fringe,(0,next(c),source))
    while fringe:
        (dist_v,_,v)=heappop(fringe)
        if v in dist:continue
        dist[v]=dist_v
        for u,e in adj[v].items():
            cost=e['weight'];vu_dist=dist_v+cost
            if cutoff is not None and vu_dist>cutoff:continue
            if u in dist:
                u_dist=dist[u]
                if vu_dist<u_dist:raise ValueError('Contradictory paths found: negative weights?')
                elif vu_dist==u_dist:pred[u].append(v)
            elif u not in seen or vu_dist<seen[u]:
                seen[u]=vu_dist;heappush(fringe,(vu_dist,next(c),u));pred[u]=[v]
            elif vu_dist==seen[u]:pred[u].append(v)
    return pred,dist

def _other(adj,pred,src,dst):
    L=T=0.0;v=dst
    while v!=src:
        u=pred[v][0];e=adj[u][v];L+=e['length_m'];T+=e['time_s'];v=u
    return L,T

def calculate(p):
    op=p['operation'];profile=p.get('profile','car');opt=p.get('optimize','time');max_snap=p.get('max_snap_m',300)
    coords,adj,info=mapdata.build_graph(p['dataset'],profile,opt)
    ds={'file':info['file'],'attribution':info['attribution'],'license':info['license'],'vertices':info['vertices']}
    if op=='matrix':
        if 'origins' not in p or 'destinations' not in p or 'origin' in p or 'max_minutes' in p:raise ValueError('matrix requires origins and destinations only')
        os_=[mapdata.snap(coords,adj,s['lat'],s['lon'],'out',max_snap) for s in p['origins']]
        ds_=[mapdata.snap(coords,adj,s['lat'],s['lon'],'in',max_snap) for s in p['destinations']]
        D=[];T=[]
        for o,_ in os_:
            pred,dist=dijkstra_pred(adj,o);rd=[];rt=[]
            for d,_ in ds_:
                if d not in dist:rd.append(None);rt.append(None);continue
                L,t=_other(adj,pred,o,d);rd.append(round(L,1));rt.append(round(t,1))
            D.append(rd);T.append(rt)
        return {'operation':op,'profile':profile,'optimize':opt,'distances_m':D,'durations_s':T,
                'origin_snaps_m':[round(x[1],1) for x in os_],'destination_snaps_m':[round(x[1],1) for x in ds_],
                'origin_vertices':[x[0] for x in os_],'destination_vertices':[x[0] for x in ds_],'dataset':ds,
                'note':'null means unreachable. Each cell follows the path that minimises the optimize metric.'}
    if 'origin' not in p or 'max_minutes' not in p or 'origins' in p or 'destinations' in p:raise ValueError('isochrone requires origin and max_minutes only')
    if opt!='time':raise ValueError('isochrone uses optimize=time')
    o,sd=mapdata.snap(coords,adj,p['origin']['lat'],p['origin']['lon'],'out',max_snap);cut=p['max_minutes']*60.0
    pred,dist=dijkstra_pred(adj,o,cut)
    lines=[];total=0.0
    for u in dist:
        for v,e in adj[u].items():
            if v in dist and (u<v or u not in adj[v]):
                lines.append([[round(coords[u][1],6),round(coords[u][0],6)],[round(coords[v][1],6),round(coords[v][0],6)]]);total+=e['length_m']
    if len(lines)>12000:raise ValueError('Reachable network too large to return (%d segments); use a smaller max_minutes'%len(lines))
    la=[coords[v][0] for v in dist];lo=[coords[v][1] for v in dist]
    far=max(dist,key=lambda v:(dist[v],-v))
    feature={'type':'Feature','properties':{'kind':'isochrone','profile':profile,'max_minutes':p['max_minutes']},'geometry':{'type':'MultiLineString','coordinates':lines}}
    return {'operation':op,'profile':profile,'max_minutes':p['max_minutes'],'origin_vertex':o,'origin_snap_m':round(sd,1),
            'reachable_vertices':len(dist),'reachable_segments':len(lines),'reachable_road_length_m':round(total,1),
            'bbox':[min(lo),min(la),max(lo),max(la)],'farthest':{'lat':coords[far][0],'lon':coords[far][1],'minutes':round(dist[far]/60,2)},
            'feature':feature,'dataset':ds,'assumptions':'Free-flow speeds; reachable road segments are returned instead of a smoothed polygon.'}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
