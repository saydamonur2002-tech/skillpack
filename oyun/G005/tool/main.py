#!/usr/bin/env python3
"""A* grid path finding using the vendored python-pathfinding core (MIT). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
DIAG={'never':DiagonalMovement.never,'always':DiagonalMovement.always,'if_at_most_one_obstacle':DiagonalMovement.if_at_most_one_obstacle,'only_when_no_obstacle':DiagonalMovement.only_when_no_obstacle}
def matrix(p):
    rows=p['grid'];w=len(rows[0])
    if any(len(r)!=w for r in rows):raise ValueError('grid rows must all have the same length')
    costs=p.get('costs',{'.':1,'#':0})
    for r in rows:
        for ch in r:
            if ch not in costs:raise ValueError('grid contains a character that has no entry in costs')
    return [[costs[ch] for ch in r] for r in rows],w,len(rows)
def calculate(p):
    m,w,h=matrix(p)
    grid=Grid(matrix=m)
    finder=AStarFinder(diagonal_movement=DIAG[p.get('diagonal','never')],weight=p.get('heuristic_weight',1),time_limit=8,max_runs=p.get('max_runs',200000))
    out=[]
    for q in p['queries']:
        (sx,sy),(ex,ey)=q['start'],q['end']
        for x,y,f in ((sx,sy,'start'),(ex,ey,'end')):
            if not(0<=x<w and 0<=y<h):raise ValueError(f+' is outside the grid')
            if m[y][x]<=0:raise ValueError(f+' is on a blocked cell')
        grid.cleanup()
        try:path,runs=finder.find_path(grid.node(sx,sy),grid.node(ex,ey),grid)
        except Exception as e:raise ValueError('search stopped: '+type(e).__name__) from None
        pts=[[n.x,n.y] for n in path]
        out.append({'found':bool(pts),'path':pts,'steps':max(len(pts)-1,0),'cost':float(grid.node(ex,ey).g) if pts else None,'runs':runs})
    return {'operation':'find_path','width':w,'height':h,'count':len(out),'found_all':all(r['found'] for r in out),'results':out}
if __name__=='__main__':raise SystemExit(cli(calculate))
