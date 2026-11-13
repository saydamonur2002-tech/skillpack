#!/usr/bin/env python3
"""Execute the pinned python-pathfinding A* (upstream/pathfinding) on every reference input; never imports tool/main.py."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'upstream'))
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement as D
from pathfinding.finder.a_star import AStarFinder
out=[]
for p in json.loads(sys.stdin.read()):
    costs=p.get('costs',{'.':1,'#':0});m=[[costs[c] for c in r] for r in p['grid']];g=Grid(matrix=m)
    f=AStarFinder(diagonal_movement=getattr(D,p.get('diagonal','never')),weight=p.get('heuristic_weight',1),time_limit=60,max_runs=p.get('max_runs',200000))
    res=[]
    for q in p['queries']:
        g.cleanup();path,runs=f.find_path(g.node(*q['start']),g.node(*q['end']),g)
        pts=[[n.x,n.y] for n in path]
        res.append({'found':bool(pts),'path':pts,'steps':max(len(pts)-1,0),'cost':float(g.node(*q['end']).g) if pts else None,'runs':runs})
    out.append({'width':len(m[0]),'height':len(m),'count':len(res),'found_all':all(r['found'] for r in res),'results':res})
print(json.dumps(out))
