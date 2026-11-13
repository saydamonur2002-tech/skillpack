#!/usr/bin/env python3
"""Sound-effect synthesis (port of ZzFX buildSamples, randomness off) and game presets. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math,hashlib
from array import array
NAMES=['volume','randomness','frequency','attack','sustain','release','shape','shapeCurve','slide','deltaSlide','pitchJump','pitchJumpTime','repeatTime','noise','modulation','bitCrush','delay','sustainVolume','decay','tremolo','filter']
DEFAULTS=[1,.05,220,0,0,.1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0]
# Skillpack game presets (original parameter choices; 'wasted' is the upstream README "Game Over" example).
PRESETS={
 'horn':[.8,.02,415,.01,.22,.06,5,.6,0,0,0,0,0,0,0,0,0,.9,.02,0,0],
 'crash':[.8,.1,90,.005,.08,.45,4,2.2,-2,0,0,0,0,1.6,0,.2,0,.6,.06,0,0],
 'siren':[.5,0,700,.05,1.1,.1,0,1,4,0,0,0,.35,0,0,0,0,1,0,0,0],
 'pickup':[1,.05,1675,0,.06,.24,1,1.82,0,0,837,.06,0,0,0,0,0,1,0,0,0],
 'cash':[1,.05,1400,.01,.04,.18,1,1.5,0,0,600,.04,.09,0,0,0,0,1,0,0,0],
 'mission_complete':[1,.02,523,.02,.3,.4,1,1.2,0,0,262,.12,.24,0,0,0,.08,1,.05,0,0],
 'wasted':[1,.05,925,.04,.3,.6,1,.3,0,6.27,-184,.09,.17,0,0,0,0,1,0,0,0],
 'engine':[.4,0,55,.02,.3,.05,2,1,0,0,0,0,.05,.1,8,0,0,.8,0,.3,600]}
def f32(x):return array('f',[x])[0]
def jround(x):return math.floor(x+0.5)       # JavaScript Math.round
def jsign(v):return -1 if v<0 else 1
def toint(x):return int(x)                    # x|0 for the bounded non-negative values used here
def build(P,sample_rate=44100):
    volume,randomness,frequency,attack,sustain,release,shape,shapeCurve,slide,deltaSlide,pitchJump,pitchJumpTime,repeatTime,noise,modulation,bitCrush,delay,sustainVolume,decay,tremolo,filt=P
    sr=sample_rate;PI2=math.pi*2
    slide*=500*PI2/sr/sr;startSlide=slide
    frequency*=(1+randomness*2*0-randomness*0)*PI2/sr;startFrequency=frequency   # randomness disabled for determinism
    modOffset=0;repeat=0;crush=0;jump=1;t=0.0;i=0;s=0.0
    quality=2;w=PI2*abs(filt)*2/sr;cos=math.cos(w);alpha=math.sin(w)/2/quality
    a0=1+alpha;a1=-2*cos/a0;a2=(1-alpha)/a0;b0=(1+jsign(filt)*cos)/2/a0;b1=-(jsign(filt)+cos)/a0;b2=b0
    x2=x1=y2=y1=0.0
    attack=attack*sr or 9
    decay*=sr;sustain*=sr;release*=sr;delay*=sr
    deltaSlide*=500*PI2/sr**3;modulation*=PI2/sr;pitchJump*=PI2/sr;pitchJumpTime*=sr;repeatTime=toint(repeatTime*sr)
    length=toint(attack+decay+sustain+release+delay)
    b=array('f',bytes(4*max(length,0)))
    k=toint(bitCrush*100)
    while i<length:
        crush+=1
        if k==0 or crush%k==0:
            if shape>4:s=1 if math.fmod(t/PI2,1)<shapeCurve/2 else -1
            elif shape>3:s=math.sin(t**3)
            elif shape>2:s=max(min(math.tan(t),1),-1)
            elif shape>1:s=1-math.fmod(math.fmod(2*t/PI2,2)+2,2)
            elif shape:s=1-4*abs(jround(t/PI2)-t/PI2)
            else:s=math.sin(t)
            env=(i/attack if i<attack else 1-((i-attack)/decay)*(1-sustainVolume) if i<attack+decay else sustainVolume if i<attack+decay+sustain
                 else (length-i-delay)/release*sustainVolume if i<length-delay else 0)
            s=((1-tremolo+tremolo*math.sin(PI2*i/repeatTime)) if repeatTime else 1)*(s if shape>4 else jsign(s)*abs(s)**shapeCurve)*env
            if delay:s=s/2+(0 if delay>i else (1 if i<length-delay else (length-i)/delay)*b[toint(i-delay)]/2/volume)
            if filt:
                y=b2*x2+b1*x1+b0*s-a2*y2-a1*y1
                x2=x1;x1=s;y2=y1;y1=y;s=y
        slide+=deltaSlide;frequency+=slide
        f=frequency*math.cos(modulation*modOffset);modOffset+=1
        t+=f+f*noise*(math.fmod(i*i*PI2,2)-1)
        if jump:
            jump+=1
            if jump>pitchJumpTime:frequency+=pitchJump;startFrequency+=pitchJump;jump=0
        if repeatTime:
            repeat+=1
            if repeat%repeatTime==0:frequency=startFrequency;slide=startSlide;jump=jump or 1
        b[i]=s*volume;i+=1
    return b
def params_of(p):
    if 'preset' in p:
        if 'params' in p:raise ValueError("give either 'preset' or 'params', not both")
        return list(PRESETS[p['preset']])
    if 'params' not in p:raise ValueError("give 'preset' or 'params'")
    raw=p['params']
    return [DEFAULTS[j] if j>=len(raw) or raw[j] is None else raw[j] for j in range(21)]
def describe(P,head):
    if P[0]<=0 and P[16]:raise ValueError('volume must be > 0 when delay is used')
    dur=((P[3]*44100 or 9)+P[18]*44100+P[4]*44100+P[5]*44100+P[16]*44100)/44100
    if dur>5:raise ValueError('sound longer than 5 seconds')
    b=build(P)
    n=len(b);peak=max((abs(x) for x in b),default=0.0);rms=math.sqrt(sum(x*x for x in b)/n) if n else 0.0
    q=array('h',(max(-32768,min(32767,int(round(x*32767)))) for x in b))
    idx=[j*(n//16) for j in range(16)] if n>=16 else list(range(n))
    return {'params':P,'named':dict(zip(NAMES,P)),'sample_rate':44100,'sample_count':n,'duration_s':n/44100,'peak':peak,'rms':rms,
            'samples_head':list(b[:head]),'samples_at':{str(j):b[j] for j in idx},'int16_sha256':hashlib.sha256(q.tobytes()).hexdigest(),
            'js_call':'zzfx(...'+repr(P).replace(' ','')+')','clipping':peak>1}
def calculate(p):
    if p['operation']=='list_presets':return {'operation':'list_presets','presets':{k:v for k,v in PRESETS.items()},'parameter_names':NAMES,'defaults':DEFAULTS}
    if p['operation']=='bank':
        names=p.get('names',sorted(PRESETS))
        out={}
        for n in names:
            d=describe(PRESETS[n],0);out[n]={'params':PRESETS[n],'duration_s':d['duration_s'],'peak':d['peak'],'clipping':d['clipping']}
        return {'operation':'bank','sounds':out,'any_clipping':any(v['clipping'] for v in out.values()),'longest_s':max(v['duration_s'] for v in out.values())}
    return dict(describe(params_of(p),p.get('samples_head',8)),operation='build')
if __name__=='__main__':raise SystemExit(cli(calculate))
