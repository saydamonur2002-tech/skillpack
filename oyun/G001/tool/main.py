#!/usr/bin/env python3
"""Fixed-timestep game loop scheduler (port of MainLoop.js animate()). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
MAX_VALUE=1.7976931348623157e308
def calculate(p):
    T=p['frame_timestamps_ms']
    if any(b<a for a,b in zip(T,T[1:])):raise ValueError('frame_timestamps_ms must be non-decreasing')
    ts=p.get('timestep_ms',1000/60)
    mfps=p.get('max_fps')
    min_delay=0.0 if mfps is None else 1000/mfps
    fps_alpha=0.9;fps_interval=1000
    fps=60;frame_delta=0.0
    # start(): first rAF callback draws once and resets the clocks
    last=T[0];last_fps_update=T[0];frames_since=0
    frames=[{'t':T[0],'ran':True,'updates':0,'alpha':1,'fps':60,'panic':False,'start':True}]
    total=0;discarded=0.0
    for t in T[1:]:
        if t<last+min_delay:
            frames.append({'t':t,'ran':False,'updates':0,'alpha':None,'fps':None,'panic':False,'start':False});continue
        frame_delta+=t-last;last=t
        if t>last_fps_update+fps_interval:
            fps=fps_alpha*frames_since*1000/(t-last_fps_update)+(1-fps_alpha)*fps
            last_fps_update=t;frames_since=0
        frames_since+=1
        n=0;panic=False
        while frame_delta>=ts:
            total+=1;frame_delta-=ts;n+=1
            if n>=240:panic=True;break
        alpha=frame_delta/ts
        if panic and p.get('discard_on_panic',False):discarded+=frame_delta;frame_delta=0.0
        frames.append({'t':t,'ran':True,'updates':n,'alpha':alpha,'fps':fps,'panic':panic,'start':False})
    out={'operation':'schedule','timestep_ms':ts,'frames':frames,'total_updates':total,'simulated_ms':total*ts,'discarded_ms':discarded,
         'panic_frames':sum(1 for f in frames if f['panic']),'max_updates_in_one_frame':max(f['updates'] for f in frames)}
    if not p.get('include_frames',True):out['frames']=[]
    return out
if __name__=='__main__':raise SystemExit(cli(calculate))
