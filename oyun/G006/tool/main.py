#!/usr/bin/env python3
"""Steering behaviours seek / flee / arrive / pursuit and vehicle integration (2D port of Yuka). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
def length(v):return math.sqrt(v[0]*v[0]+v[1]*v[1])
def normalize(v):
    d=length(v) or 1
    return (v[0]/d,v[1]/d)
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def scale(v,s):return (v[0]*s,v[1]*s)
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def seek(veh,target):
    d=scale(normalize(sub(target,veh['pos'])),veh['max_speed'])
    return sub(d,veh['vel'])
def flee(veh,target,panic):
    dx=veh['pos'][0]-target[0];dy=veh['pos'][1]-target[1]
    if dx*dx+dy*dy<=panic*panic:
        d=normalize(sub(veh['pos'],target))
        if d[0]*d[0]+d[1]*d[1]==0:d=(0.0,1.0)
        d=scale(d,veh['max_speed'])
        return sub(d,veh['vel'])
    return (0.0,0.0)
def arrive(veh,target,decel,tol):
    disp=sub(target,veh['pos']);dist=length(disp)
    if dist>tol:
        speed=min(dist/decel,veh['max_speed'])
        d=scale(disp,speed/dist)
    else:d=(0.0,0.0)
    return sub(d,veh['vel'])
def pursuit(veh,ev,pf):
    disp=sub(ev['pos'],veh['pos'])
    ahead=dot(disp,veh['dir'])>0
    facing=dot(veh['dir'],ev['dir'])<-0.95
    if ahead and facing:return seek(veh,ev['pos'])
    t=length(disp)/(veh['max_speed']+length(ev['vel']))*pf
    pred=(ev['pos'][0]+ev['vel'][0]*t,ev['pos'][1]+ev['vel'][1]*t)
    return seek(veh,pred)
def heading(vx,vy,h):
    if h is not None:return (math.sin(h),math.cos(h))   # yuka forward is +z; 2D (x,y)=(x,z)
    if vx*vx+vy*vy>1e-8:return normalize((vx,vy))
    return (0.0,1.0)
def accumulate(f,max_force):
    # SteeringManager._accumulate with a single behaviour of weight 1
    if max_force<=0:return (0.0,0.0)
    m=length(f)
    if m>max_force:f=normalize(f);f=scale(f,max_force)
    return f
def calculate(p):
    v=p['vehicle'];prm=p.get('params',{});b=p['behavior']
    veh={'pos':(float(v['x']),float(v['y'])),'vel':(float(v.get('vx',0)),float(v.get('vy',0))),'max_speed':v.get('max_speed',1),'max_force':v.get('max_force',100),'mass':v.get('mass',1)}
    veh['dir']=heading(veh['vel'][0],veh['vel'][1],v.get('heading'))
    if b=='pursuit':
        if 'evader' not in p:raise ValueError("pursuit needs 'evader'")
        e=p['evader'];ev={'pos':(float(e['x']),float(e['y'])),'vel':(float(e.get('vx',0)),float(e.get('vy',0)))};ev['dir']=heading(ev['vel'][0],ev['vel'][1],e.get('heading'))
    elif 'target' not in p:raise ValueError("this behavior needs 'target'")
    else:tgt=(float(p['target']['x']),float(p['target']['y']))
    dt=p.get('dt_s',1/60);every=p.get('record_every',1);traj=[];mind=None
    for i in range(1,p.get('steps',1)+1):
        if b=='seek':f=seek(veh,tgt)
        elif b=='flee':f=flee(veh,tgt,prm.get('panic_distance',10))
        elif b=='arrive':f=arrive(veh,tgt,prm.get('deceleration',3),prm.get('tolerance',0))
        else:f=pursuit(veh,ev,prm.get('prediction_factor',1))
        f=accumulate(f,veh['max_force'])
        acc=(f[0]/veh['mass'],f[1]/veh['mass'])
        vel=(veh['vel'][0]+acc[0]*dt,veh['vel'][1]+acc[1]*dt)
        if vel[0]*vel[0]+vel[1]*vel[1]>veh['max_speed']*veh['max_speed']:vel=scale(normalize(vel),veh['max_speed'])
        disp=(vel[0]*dt,vel[1]*dt);veh['vel']=vel
        newpos=(veh['pos'][0]+disp[0],veh['pos'][1]+disp[1])
        if vel[0]*vel[0]+vel[1]*vel[1]>1e-8:veh['dir']=normalize(sub(newpos,veh['pos']))
        veh['pos']=newpos
        if b=='pursuit':
            ev['pos']=(ev['pos'][0]+ev['vel'][0]*dt,ev['pos'][1]+ev['vel'][1]*dt)
            other=ev['pos']
        else:other=tgt
        d=length(sub(other,veh['pos']));mind=d if mind is None else min(mind,d)
        if i%every==0:traj.append({'step':i,'x':veh['pos'][0],'y':veh['pos'][1],'vx':vel[0],'vy':vel[1],'distance':d})
    fin={'x':veh['pos'][0],'y':veh['pos'][1],'vx':veh['vel'][0],'vy':veh['vel'][1],'speed':length(veh['vel'])}
    return {'operation':'simulate','behavior':b,'steps':p.get('steps',1),'final':fin,'trajectory':traj,'min_distance':mind,
            'caught':(mind is not None and mind<=p.get('catch_radius',-1))}
if __name__=='__main__':raise SystemExit(cli(calculate))
