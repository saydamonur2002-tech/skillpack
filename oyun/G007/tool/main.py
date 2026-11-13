#!/usr/bin/env python3
"""Wanted level ("stars") and police response rules for a top-down city game. Original rule table, MIT."""
from runtime import cli
import copy
RULES={'heat':{'steal_car':15,'hit_vehicle':10,'hit_pedestrian':35,'hit_police':60,'run_red_light':5},
       'witness_multiplier':2,
       'star_thresholds':[20,60,120,200,320],
       'cooldown_s':[0,8,12,16,20,25],
       'decay_per_s':10,
       'paint_shop_min_unseen_s':3,
       'police_units':[0,1,2,3,5,7],
       'police_speed_factor':[0,0.85,0.95,1.05,1.15,1.25],
       'search_radius_tiles':[0,8,12,16,20,26],
       'max_heat':400}
def merged(over):
    r=copy.deepcopy(RULES)
    for k,v in (over or {}).items():
        if k=='heat':r['heat'].update(v)
        else:r[k]=v
    th=r['star_thresholds']
    if any(b<=a for a,b in zip(th,th[1:])):raise ValueError('star_thresholds must be strictly increasing')
    return r
def level(h,th):return sum(1 for t in th if h>=t)
def view(s,r,ev,note):
    st=s['stars']
    return {'event':ev,'stars':st,'heat':s['heat'],'seconds_unseen':s['unseen'],'police_units':r['police_units'][st],
            'police_speed_factor':r['police_speed_factor'][st],'search_radius_tiles':r['search_radius_tiles'][st],'note':note}
def calculate(p):
    r=merged(p.get('rules'))
    if p['operation']=='rules':return {'operation':'rules','rules':r}
    s0=p.get('state',{})
    s={'stars':s0.get('stars',0),'heat':float(s0.get('heat',0)),'unseen':float(s0.get('seconds_unseen',0))}
    th=r['star_thresholds'];timeline=[]
    for e in p['events']:
        t=e['type'];note='ok'
        if t in r['heat']:
            add=r['heat'][t]*(r['witness_multiplier'] if e.get('witnessed') else 1)
            s['heat']=min(r['max_heat'],s['heat']+add);s['stars']=max(s['stars'],level(s['heat'],th))
            if e.get('witnessed'):s['unseen']=0.0
            note='+%g heat'%add
        elif t=='tick':
            dt=e.get('dt',0);before=s['unseen'];s['unseen']+=dt;cd=r['cooldown_s'][s['stars']]
            if s['stars']>0 and s['unseen']>=cd:
                over=min(dt,s['unseen']-max(cd,before)) if before<cd else dt
                s['heat']=max(0.0,s['heat']-r['decay_per_s']*over)
                s['stars']=min(s['stars'],level(s['heat'],th))
                note='decay %g s'%over
            else:note='no decay'
        elif t=='seen_by_police':s['unseen']=0.0;note='police see the player'
        elif t=='paint_shop':
            if s['stars']==0:note='nothing to clear'
            elif s['unseen']>=r['paint_shop_min_unseen_s']:s['heat']=0.0;s['stars']=0;note='cleared'
            else:note='rejected: police are watching'
        elif t in('busted','wasted'):s['heat']=0.0;s['stars']=0;s['unseen']=0.0;note='reset'
        timeline.append(view(s,r,t,note))
    return {'operation':'simulate','final':view(s,r,'final','final'),'timeline':timeline,'rules':r}
if __name__=='__main__':raise SystemExit(cli(calculate))
