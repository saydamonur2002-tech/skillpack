#!/usr/bin/env python3
"""Polyline simplification with radial pre-filter and Ramer-Douglas-Peucker. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
def _sq_dist(p1,p2):
    dx=p1[0]-p2[0];dy=p1[1]-p2[1]
    return dx*dx+dy*dy

def _sq_seg_dist(p,p1,p2):
    x=p1[0];y=p1[1];dx=p2[0]-x;dy=p2[1]-y
    if dx!=0 or dy!=0:
        t=((p[0]-x)*dx+(p[1]-y)*dy)/(dx*dx+dy*dy)
        if t>1:x=p2[0];y=p2[1]
        elif t>0:x+=dx*t;y+=dy*t
    dx=p[0]-x;dy=p[1]-y
    return dx*dx+dy*dy

def _radial(points,idx,sq_tol):
    prev=idx[0];keep=[prev];point=prev
    for k in idx[1:]:
        point=k
        if _sq_dist(points[k],points[prev])>sq_tol:keep.append(k);prev=k
    if prev!=point:keep.append(point)
    return keep

def _douglas_peucker(points,idx,sq_tol):
    # Explicit-stack, in-order equivalent of upstream recursive simplifyDPStep.
    last=len(idx)-1;out=[idx[0]];stack=[('span',0,last)]
    while stack:
        item=stack.pop()
        if item[0]=='emit':out.append(idx[item[1]]);continue
        _,first,end=item;max_sq=sq_tol;index=None
        for i in range(first+1,end):
            d=_sq_seg_dist(points[idx[i]],points[idx[first]],points[idx[end]])
            if d>max_sq:index=i;max_sq=d
        if max_sq>sq_tol:
            if end-index>1:stack.append(('span',index,end))
            stack.append(('emit',index))
            if index-first>1:stack.append(('span',first,index))
    out.append(idx[last])
    return out

def calculate(p):
    points=[(float(a),float(b)) for a,b in p['points']]
    tol=p.get('tolerance',1);hq=p.get('highest_quality',False)
    if len(points)<=2:
        idx=list(range(len(points)))
    else:
        sq=tol*tol;idx=list(range(len(points)))
        if not hq:idx=_radial(points,idx,sq)
        idx=_douglas_peucker(points,idx,sq)
    return {'points':[list(p['points'][i]) for i in idx],'kept_indices':idx,'input_count':len(points),'output_count':len(idx)}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
