#!/usr/bin/env python3
"""Deterministic top-down tile city generator (roads, sidewalks, buildings, parks, points of interest). Original work, MIT."""
from runtime import cli
from collections import deque
LEGEND={'R':'road (drivable)','S':'sidewalk (walkable, drivable slowly)','B':'building (solid)','P':'park (walkable)'}
class Rng:
    """xorshift32 (Marsaglia 2003): x^=x<<13; x^=x>>17; x^=x<<5 (mod 2^32)."""
    def __init__(s,seed):s.x=(seed&0xFFFFFFFF) or 0x9E3779B9
    def next(s):
        x=s.x;x^=(x<<13)&0xFFFFFFFF;x^=x>>17;x^=(x<<5)&0xFFFFFFFF;s.x=x;return x
    def randint(s,a,b):return a+s.next()%(b-a+1)
def split(n,rw,bmin,bmax,rng):
    """Road start indices along one axis; roads on both edges, blocks of bmin..bmax between."""
    roads=[0];pos=rw
    while True:
        rem=n-pos
        w=rng.randint(bmin,bmax)
        if rem-(w+rw)<bmin+rw:w=rem-rw
        roads.append(pos+w);pos+=w+rw
        if pos>=n:break
    return roads
def generate(p):
    W,H=p['width'],p['height'];rw=p.get('road_width',2);bmin=p.get('block_min',4);bmax=p.get('block_max',7)
    if bmin>bmax:raise ValueError('block_min must be <= block_max')
    if min(W,H)<2*rw+bmin:raise ValueError('map too small for one block between edge roads')
    rng=Rng(p['seed'])
    xs=split(W,rw,bmin,bmax,rng);ys=split(H,rw,bmin,bmax,rng)
    rc={x+i for x in xs for i in range(rw)};rr={y+i for y in ys for i in range(rw)}
    g=[['R' if (x in rc or y in rr) else '?' for x in range(W)] for y in range(H)]
    blocks=[];ratio=int(round(p.get('park_ratio',0.2)*1000))
    for j in range(len(ys)-1):
        for i in range(len(xs)-1):
            x0,x1=xs[i]+rw,xs[i+1]-1;y0,y1=ys[j]+rw,ys[j+1]-1
            kind='park' if rng.next()%1000<ratio else 'building'
            for y in range(y0,y1+1):
                for x in range(x0,x1+1):
                    ring=x in(x0,x1) or y in(y0,y1)
                    g[y][x]='S' if ring else ('P' if kind=='park' else 'B')
            blocks.append({'x':x0,'y':y0,'w':x1-x0+1,'h':y1-y0+1,'kind':kind})
    tiles=[''.join(r) for r in g]
    def T(x,y):return tiles[y][x] if 0<=x<W and 0<=y<H else None
    road=[(x,y) for y in range(H) for x in range(W) if tiles[y][x]=='R']
    curb=[(x,y) for y in range(H) for x in range(W) if tiles[y][x]=='S' and any(T(x+dx,y+dy)=='R' for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
    def pick(pool,used):
        for _ in range(64):
            c=pool[rng.next()%len(pool)]
            if c not in used:used.add(c);return c
        raise ValueError('not enough free tiles for the requested points')
    cx,cy=W/2,H/2
    spawn=min(road,key=lambda c:((c[0]+.5-cx)**2+(c[1]+.5-cy)**2,c[1],c[0]))
    used={spawn}
    def access(c):
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            if T(c[0]+dx,c[1]+dy)=='R':return [c[0]+dx,c[1]+dy]
    def pt(c,kind):return {'kind':kind,'tile':[c[0],c[1]],'x':c[0]+.5,'y':c[1]+.5,'road_access':access(c) if kind!='cash' and kind!='spawn' else [c[0],c[1]]}
    pts={'spawn':pt(spawn,'spawn'),'police_station':pt(pick(curb,used),'police_station'),'paint_shop':pt(pick(curb,used),'paint_shop'),
         'landmarks':[pt(pick(curb,used),'landmark') for _ in range(p.get('landmarks',6))],
         'cash':[pt(pick(road,used),'cash') for _ in range(p.get('cash_pickups',5))]}
    walk=[c for c in ((x,y) for y in range(H) for x in range(W)) if tiles[c[1]][c[0]] in 'SP']
    inter=[(x,y) for x in xs for y in ys]
    ped=[];tr=[]
    for _ in range(p.get('ped_routes',6)):
        a=walk[rng.next()%len(walk)];b=walk[rng.next()%len(walk)]
        if a!=b:ped.append({'start':[a[0],a[1]],'end':[b[0],b[1]]})
    for _ in range(p.get('traffic_routes',4)):
        a=inter[rng.next()%len(inter)];b=inter[rng.next()%len(inter)]
        if a!=b:tr.append({'start':[a[0],a[1]],'end':[b[0],b[1]]})
    # road connectivity check (4-neighbour flood fill)
    seen={spawn};q=deque([spawn])
    while q:
        x,y=q.popleft()
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            n=(x+dx,y+dy)
            if T(*n)=='R' and n not in seen:seen.add(n);q.append(n)
    sx,sy=spawn
    near=[{'a':{'type':'circle','x':sx+.5,'y':sy+.5,'r':0.45},'b':{'type':'box','x':x,'y':y,'w':1,'h':1}}
          for y in range(max(0,sy-3),min(H,sy+4)) for x in range(max(0,sx-3),min(W,sx+4)) if tiles[y][x]=='B']
    if not near:near=[{'a':{'type':'circle','x':sx+.5,'y':sy+.5,'r':0.45},'b':{'type':'box','x':-10,'y':-10,'w':1,'h':1}}]
    counts={k:sum(r.count(k) for r in tiles) for k in LEGEND}
    return {'operation':'generate','seed':p['seed'],'width':W,'height':H,'tiles':tiles,'legend':LEGEND,'road_cols':xs,'road_rows':ys,'road_width':rw,
            'blocks':blocks,'counts':counts,'points':pts,'road_connected':len(seen)==len(road),
            'walk_costs':{'R':3,'S':1,'P':1,'B':0},'drive_costs':{'R':1,'S':0,'P':0,'B':0},
            'ped_route_pairs':ped,'traffic_route_pairs':tr,'mission_targets':[l['road_access'] for l in pts['landmarks']],
            'spawn_collision_pairs':near[:64],'solid':'B','tile_size_units':1}
def calculate(p):return generate(p)
if __name__=='__main__':raise SystemExit(cli(calculate))
