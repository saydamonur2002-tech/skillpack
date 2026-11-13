#!/usr/bin/env python3
"""Execute pinned PythonRobotics State.update on each reference input. Needs numpy; plotting/spline imports are stubbed."""
import json,math,sys,types,importlib.util
from pathlib import Path
UP=Path(__file__).resolve().parents[1]/'upstream'
for name in ('matplotlib','matplotlib.pyplot','scipy','scipy.spatial','scipy.spatial.transform','PathPlanning','PathPlanning.CubicSpline','PathPlanning.CubicSpline.cubic_spline_planner'):
    m=types.ModuleType(name);m.Rotation=None;m.cubic_spline_planner=None;sys.modules[name]=m
spec=importlib.util.spec_from_file_location('utils.angle',UP/'utils'/'angle.py');ang=importlib.util.module_from_spec(spec);spec.loader.exec_module(ang)
sys.modules['utils']=types.ModuleType('utils');sys.modules['utils'].angle=ang;sys.modules['utils.angle']=ang
spec=importlib.util.spec_from_file_location('stanley',UP/'PathTracking'/'stanley_control'/'stanley_control.py');sc=importlib.util.module_from_spec(spec);spec.loader.exec_module(sc)
import numpy as np
out=[]
for p in json.loads(sys.stdin.read()):
    prm=dict({'wheelbase_m':2.9,'max_steer_deg':30.0,'dt_s':0.1},**p.get('params',{}))
    sc.L=prm['wheelbase_m'];sc.dt=prm['dt_s'];sc.max_steer=np.radians(prm['max_steer_deg'])
    st=sc.State(**{k:float(p['state'][k]) for k in ('x','y','yaw','v')})
    lim=p.get('speed_limits');every=p.get('record_every',1);n=0;traj=[];dist=0.0;vmax=abs(st.v)
    for c in p['controls']:
        for _ in range(c.get('repeat',1)):
            dist+=abs(float(st.v))*sc.dt
            st.update(c['acceleration'],np.radians(c['steer_deg']))
            if lim:st.v=min(max(float(st.v),lim['min_v']),lim['max_v'])
            n+=1;vmax=max(vmax,abs(float(st.v)))
            if n%every==0:traj.append({'x':float(st.x),'y':float(st.y),'yaw':float(st.yaw),'v':float(st.v),'step':n})
    out.append({'steps':n,'final':{'x':float(st.x),'y':float(st.y),'yaw':float(st.yaw),'v':float(st.v)},'trajectory':traj,'distance_m':dist,'max_abs_speed':vmax})
print(json.dumps(out))
