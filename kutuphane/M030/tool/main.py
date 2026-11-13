#!/usr/bin/env python3
"""Offline road routing (A*/Dijkstra) with distance, time and street list. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
from heapq import heappush,heappop
from itertools import count
import mapdata

def astar_path(adj,source,target,heuristic):
    """Port of networkx astar_path (networkx 3.6.1, algorithms/shortest_paths/astar.py); cutoff omitted."""
    c=count();queue=[(0,next(c),source,0,None)];enqueued={};explored={}
    while queue:
        _,__,curnode,dist,parent=heappop(queue)
        if curnode==target:
            path=[curnode];node=parent
            while node is not None:path.append(node);node=explored[node]
            path.reverse();return path
        if curnode in explored:
            if explored[curnode] is None:continue
            qcost,h=enqueued[curnode]
            if qcost<dist:continue
        explored[curnode]=parent
        for neighbor,w in adj[curnode].items():
            cost=w['weight']
            ncost=dist+cost
            if neighbor in enqueued:
                qcost,h=enqueued[neighbor]
                if qcost<=ncost:continue
            else:h=heuristic(neighbor,target)
            enqueued[neighbor]=ncost,h
            heappush(queue,(ncost+h,next(c),neighbor,ncost,curnode))
    raise ValueError('NO_PATH: target not reachable from source with this profile (one-way streets, access rules or a disconnected road piece)')

def _segments(coords,adj,path):
    segs=[];L=T=0.0
    for a,b in zip(path,path[1:]):
        e=adj[a][b];L+=e['length_m'];T+=e['time_s'];nm=e['name'] or '(unnamed '+str(e['highway'])+')'
        if segs and segs[-1]['name']==nm:segs[-1]['distance_m']+=e['length_m'];segs[-1]['duration_s']+=e['time_s']
        else:segs.append({'name':nm,'highway':e['highway'],'distance_m':e['length_m'],'duration_s':e['time_s']})
    for s in segs:s['distance_m']=round(s['distance_m'],1);s['duration_s']=round(s['duration_s'],1)
    return segs,L,T

def calculate(p):
    profile=p.get('profile','car');opt=p.get('optimize','time');alg=p.get('algorithm','astar');max_snap=p.get('max_snap_m',300)
    coords,adj,info=mapdata.build_graph(p['dataset'],profile,opt)
    vmax=max((e['length_m']/e['time_s'] for a in adj for e in a.values()),default=1.0)
    def heuristic(u,v):
        if alg=='dijkstra':return 0
        d=mapdata.haversine(coords[u][0],coords[u][1],coords[v][0],coords[v][1])
        return d if opt=='distance' else d/vmax
    stops=[p['origin']]+p.get('via',[])+[p['destination']];snapped=[];path=[]
    for i,s in enumerate(stops):
        need='out' if i==0 else ('in' if i==len(stops)-1 else 'out')
        v,d=mapdata.snap(coords,adj,s['lat'],s['lon'],need,max_snap)
        snapped.append({'input':{'lat':s['lat'],'lon':s['lon']},'vertex':v,'snapped':{'lat':coords[v][0],'lon':coords[v][1]},'snap_distance_m':round(d,1)})
    for a,b in zip(snapped,snapped[1:]):
        leg=astar_path(adj,a['vertex'],b['vertex'],heuristic) if a['vertex']!=b['vertex'] else [a['vertex']]
        path+=leg if not path else leg[1:]
    segs,L,T=_segments(coords,adj,path)
    line=[[round(coords[v][1],7),round(coords[v][0],7)] for v in path]
    feature={'type':'Feature','properties':{'kind':'route','profile':profile,'optimize':opt,'distance_m':round(L,1),'duration_s':round(T,1)},'geometry':{'type':'LineString','coordinates':line if len(line)>1 else line*2}}
    return {'profile':profile,'optimize':opt,'algorithm':alg,'distance_m':round(L,1),'duration_s':round(T,1),'duration_min':round(T/60,1),
            'vertex_path':path,'stops':snapped,'segments':segs,'feature':feature,
            'dataset':{'file':info['file'],'attribution':info['attribution'],'license':info['license'],'vertices':info['vertices'],'directed_edges':info['directed_edges']},
            'assumptions':'Free-flow speeds from road class or numeric maxspeed; no live traffic, turn costs, signals or time-of-day rules.'}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
