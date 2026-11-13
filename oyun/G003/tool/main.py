#!/usr/bin/env python3
"""Kinematic bicycle model (port of PythonRobotics stanley_control.State.update). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
DEFAULTS={'wheelbase_m':2.9,'max_steer_deg':30.0,'dt_s':0.1}
def angle_mod(x):
    # upstream utils/angle.py angle_mod(): (x + pi) % (2 pi) - pi  (Python/numpy floor modulo)
    return (x+math.pi)%(2*math.pi)-math.pi
def step(s,acc,delta,L,max_steer,dt):
    delta=min(max(delta,-max_steer),max_steer)          # np.clip
    x=s['x']+s['v']*math.cos(s['yaw'])*dt
    y=s['y']+s['v']*math.sin(s['yaw'])*dt
    yaw=angle_mod(s['yaw']+s['v']/L*math.tan(delta)*dt)
    v=s['v']+acc*dt
    return {'x':x,'y':y,'yaw':yaw,'v':v}
def calculate(p):
    prm=dict(DEFAULTS,**p.get('params',{}))
    L=prm['wheelbase_m'];dt=prm['dt_s'];max_steer=math.radians(prm['max_steer_deg'])
    lim=p.get('speed_limits')
    if lim and lim['min_v']>lim['max_v']:raise ValueError("speed_limits: min_v must be <= max_v")
    total=sum(c.get('repeat',1) for c in p['controls'])
    if total>5000:raise ValueError('controls expand to more than 5000 steps')
    every=p.get('record_every',1)
    s={k:float(p['state'][k]) for k in ('x','y','yaw','v')}
    traj=[];dist=0.0;vmax=abs(s['v']);n=0
    for c in p['controls']:
        acc=c['acceleration'];delta=math.radians(c['steer_deg'])
        for _ in range(c.get('repeat',1)):
            dist+=abs(s['v'])*dt
            s=step(s,acc,delta,L,max_steer,dt)
            if lim:s['v']=min(max(s['v'],lim['min_v']),lim['max_v'])
            n+=1;vmax=max(vmax,abs(s['v']))
            if n%every==0:traj.append(dict(s,step=n))
    for k,v in s.items():
        if not math.isfinite(v):raise ValueError('state became non-finite')
    return {'operation':'simulate','steps':n,'final':s,'trajectory':traj,'distance_m':dist,'max_abs_speed':vmax,
            'params':{'wheelbase_m':L,'max_steer_deg':prm['max_steer_deg'],'dt_s':dt},
            'model':'x+=v cos(yaw) dt; y+=v sin(yaw) dt; yaw=wrap(yaw+v/L tan(clip(delta)) dt); v+=a dt'}
if __name__=='__main__':raise SystemExit(cli(calculate))
