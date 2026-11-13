#!/usr/bin/env python3
"""2D collision tests (port of SAT.js: circle/circle, polygon/circle, circle/polygon, polygon/polygon). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
MAX=1.7976931348623157e308
class Poly:
    def __init__(s,x,y,points,angle=0.0):
        pts=[list(map(float,p)) for p in points]
        i=0
        while i<len(pts):                       # setPoints(): drop consecutive duplicates
            p1=pts[i];p2=pts[i+1] if i<len(pts)-1 else pts[0]
            if p1 is not p2 and p1[0]==p2[0] and p1[1]==p2[1]:pts.pop(i);continue
            i+=1
        s.pos=(float(x),float(y));s.calc=[];s.edges=[];s.normals=[]
        for px,py in pts:
            if angle!=0:px,py=px*math.cos(angle)-py*math.sin(angle),px*math.sin(angle)+py*math.cos(angle)
            s.calc.append((px,py))
        n=len(s.calc)
        for i in range(n):
            p1=s.calc[i];p2=s.calc[i+1] if i<n-1 else s.calc[0]
            e=(p2[0]-p1[0],p2[1]-p1[1]);s.edges.append(e)
            s.normals.append(norm((e[1],-e[0])))
def norm(v):
    d=math.sqrt(v[0]*v[0]+v[1]*v[1])
    return (v[0]/d,v[1]/d) if d>0 else v
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def new_resp():return {'aInB':True,'bInA':True,'overlap':MAX,'n':(0.0,0.0)}
def flatten(points,normal):
    mn=MAX;mx=-MAX
    for p in points:
        d=dot(p,normal)
        if d<mn:mn=d
        if d>mx:mx=d
    return [mn,mx]
def separating(apos,bpos,ap,bp,axis,r):
    off=(bpos[0]-apos[0],bpos[1]-apos[1]);po=dot(off,axis)
    A=flatten(ap,axis);Bv=flatten(bp,axis);Bv[0]+=po;Bv[1]+=po
    if A[0]>Bv[1] or Bv[0]>A[1]:return True
    if A[0]<Bv[0]:
        r['aInB']=False
        if A[1]<Bv[1]:ov=A[1]-Bv[0];r['bInA']=False
        else:o1=A[1]-Bv[0];o2=Bv[1]-A[0];ov=o1 if o1<o2 else -o2
    else:
        r['bInA']=False
        if A[1]>Bv[1]:ov=A[0]-Bv[1];r['aInB']=False
        else:o1=A[1]-Bv[0];o2=Bv[1]-A[0];ov=o1 if o1<o2 else -o2
    if abs(ov)<r['overlap']:
        r['overlap']=abs(ov);r['n']=axis if ov>=0 else (-axis[0],-axis[1])
    return False
def voronoi(line,point):
    l2=dot(line,line);dp=dot(point,line)
    return -1 if dp<0 else (1 if dp>l2 else 0)
def circle_circle(a,b,r):
    d=(b['x']-a['x'],b['y']-a['y']);tr=a['r']+b['r'];d2=dot(d,d)
    if d2>tr*tr:return False
    dist=math.sqrt(d2);r['overlap']=tr-dist;r['n']=norm(d)
    r['aInB']=a['r']<=b['r'] and dist<=b['r']-a['r'];r['bInA']=b['r']<=a['r'] and dist<=a['r']-b['r']
    return True
def poly_circle(P,c,r):
    cp=(c['x']-P.pos[0],c['y']-P.pos[1]);rad=c['r'];r2=rad*rad;pts=P.calc;n=len(pts)
    for i in range(n):
        nx=0 if i==n-1 else i+1;pv=n-1 if i==0 else i-1
        ov=0;on=None
        edge=P.edges[i];pt=(cp[0]-pts[i][0],cp[1]-pts[i][1])
        if dot(pt,pt)>r2:r['aInB']=False
        reg=voronoi(edge,pt)
        if reg==-1:
            edge=P.edges[pv];pt2=(cp[0]-pts[pv][0],cp[1]-pts[pv][1])
            if voronoi(edge,pt2)==1:
                dist=math.sqrt(dot(pt,pt))
                if dist>rad:return False
                r['bInA']=False;on=norm(pt);ov=rad-dist
        elif reg==1:
            edge=P.edges[nx];pt=(cp[0]-pts[nx][0],cp[1]-pts[nx][1])
            if voronoi(edge,pt)==-1:
                dist=math.sqrt(dot(pt,pt))
                if dist>rad:return False
                r['bInA']=False;on=norm(pt);ov=rad-dist
        else:
            normal=norm((edge[1],-edge[0]));dist=dot(pt,normal)
            if dist>0 and abs(dist)>rad:return False
            on=normal;ov=rad-dist
            if dist>=0 or ov<2*rad:r['bInA']=False
        if on is not None and abs(ov)<abs(r['overlap']):r['overlap']=ov;r['n']=on
    return True
def poly_poly(A,Bp,r):
    for ax in A.normals:
        if separating(A.pos,Bp.pos,A.calc,Bp.calc,ax,r):return False
    for ax in Bp.normals:
        if separating(A.pos,Bp.pos,A.calc,Bp.calc,ax,r):return False
    return True
def to_poly(s):
    if s['type']=='box':return Poly(s['x'],s['y'],[[0,0],[s['w'],0],[s['w'],s['h']],[0,s['h']]])
    pts=s['points'];area=0.0;n=len(pts)
    for i in range(n):x1,y1=pts[i];x2,y2=pts[(i+1)%n];area+=x1*y2-x2*y1
    if area<=0:raise ValueError('polygon points must be counter-clockwise (positive signed area, y up) and non-degenerate')
    for i in range(n):
        a,b,c=pts[i],pts[(i+1)%n],pts[(i+2)%n]
        if (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])<0:raise ValueError('polygon must be convex')
    return Poly(s['x'],s['y'],pts,s.get('angle',0.0))
def test(a,b):
    r=new_resp()
    ca=a['type']=='circle';cb=b['type']=='circle'
    if ca and cb:hit=circle_circle(a,b,r)
    elif cb:hit=poly_circle(to_poly(a),b,r)
    elif ca:
        hit=poly_circle(to_poly(b),a,r)
        if hit:r['n']=(-r['n'][0],-r['n'][1]);r['aInB'],r['bInA']=r['bInA'],r['aInB']
    else:hit=poly_poly(to_poly(a),to_poly(b),r)
    if not hit:return {'collides':False,'overlap':None,'overlap_n':None,'overlap_v':None,'a_in_b':None,'b_in_a':None,'push_a':None}
    n=r['n'];o=r['overlap'];v=[n[0]*o,n[1]*o]
    return {'collides':True,'overlap':o,'overlap_n':[n[0],n[1]],'overlap_v':v,'a_in_b':r['aInB'],'b_in_a':r['bInA'],'push_a':[-v[0],-v[1]]}
def calculate(p):
    res=[test(x['a'],x['b']) for x in p['pairs']]
    return {'operation':'test','count':len(res),'colliding':sum(1 for x in res if x['collides']),'results':res}
if __name__=='__main__':raise SystemExit(cli(calculate))
