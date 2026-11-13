#!/usr/bin/env python3
"""Mission graph validation and mission state machine (goto, deliver, escape, collect). Original work, MIT."""
from runtime import cli
import math
def validate(ms):
    issues=[];ids=[m['id'] for m in ms];seen=set()
    for i in ids:
        if i in seen:issues.append('duplicate id: '+i)
        seen.add(i)
    for m in ms:
        for r in m.get('requires',[]):
            if r not in seen:issues.append(m['id']+' requires unknown mission '+r)
            if r==m['id']:issues.append(m['id']+' requires itself')
        if m['type']=='deliver' and 'pickup' not in m:issues.append(m['id']+': deliver needs pickup')
        if m['type'] in('goto','deliver') and 'target' not in m:issues.append(m['id']+': needs target')
    order=[];done=set();pending=[m for m in ms]
    while pending:
        nxt=[m for m in pending if all(r in done for r in m.get('requires',[]))]
        if not nxt:issues.append('dependency cycle among: '+', '.join(m['id'] for m in pending));break
        m=nxt[0];order.append(m['id']);done.add(m['id']);pending.remove(m)
    return {'valid':not issues,'issues':issues,'order':order,'total_reward':sum(m.get('reward',0) for m in ms),
            'start_missions':[m['id'] for m in ms if not m.get('requires')]}
def centre(t):return (t[0]+0.5,t[1]+0.5)
def near(pos,t,r):c=centre(t);return math.hypot(pos[0]-c[0],pos[1]-c[1])<=r
def simulate(ms,events):
    v=validate(ms)
    if not v['valid']:raise ValueError('mission graph invalid: '+'; '.join(v['issues'])[:300])
    by={m['id']:m for m in ms};st={m['id']:'locked' for m in ms};fails={m['id']:0 for m in ms}
    ctx={'active':None,'elapsed':0.0,'picked':False,'had_stars':False,'count':0}
    pos=None;stars=0;money=0;log=[];tx=[]
    def activate():
        for i in v['order']:
            if st[i] in('locked','available') and all(st[r]=='done' for r in by[i].get('requires',[])):
                st[i]='active';ctx.update(active=i,elapsed=0.0,picked=False,had_stars=stars>0,count=0);log.append({'mission':i,'status':'active'});return
        ctx['active']=None
    def finish(i):
        nonlocal money
        st[i]='done';r=by[i].get('reward',0);money+=r;tx.append({'type':'earn','amount':r,'reason':'mission '+i})
        log.append({'mission':i,'status':'done','reward':r});activate()
    activate()
    for e in events:
        if e['type']=='position':
            pos=(e['x'],e['y'])
            if 'stars' in e:stars=e['stars']
        elif e['type']=='tick':ctx['elapsed']+=e.get('dt',0)
        i=ctx['active']
        if i is None:continue
        m=by[i];lim=m.get('time_limit_s',0)
        if lim and ctx['elapsed']>lim:
            fails[i]+=1;log.append({'mission':i,'status':'failed','reason':'time limit'})
            ctx.update(elapsed=0.0,picked=False,count=0);log.append({'mission':i,'status':'active','retry':fails[i]});continue
        if stars>0:ctx['had_stars']=True
        r=m.get('radius',1.5);t=m['type']
        if t=='goto' and pos and near(pos,m['target'],r):finish(i)
        elif t=='deliver' and pos:
            if not ctx['picked'] and near(pos,m['pickup'],r):ctx['picked']=True;log.append({'mission':i,'status':'picked_up'})
            elif ctx['picked'] and near(pos,m['target'],r):finish(i)
        elif t=='escape' and ctx['had_stars'] and stars==0:finish(i)
        elif t=='collect' and e['type']=='collect':
            ctx['count']+=1
            if ctx['count']>=m.get('count',1):finish(i)
    return {'statuses':st,'active':ctx['active'],'money_earned':money,'failures':fails,'log':log,'transactions':tx,'all_done':all(s=='done' for s in st.values())}
def calculate(p):
    if p['operation']=='validate':return dict(validate(p['missions']),operation='validate',missions=p['missions'])
    return dict(simulate(p['missions'],p.get('events',[])),operation='simulate')
if __name__=='__main__':raise SystemExit(cli(calculate))
