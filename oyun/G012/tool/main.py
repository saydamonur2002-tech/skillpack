#!/usr/bin/env python3
"""Builds one self-contained HTML5 canvas game file from the outputs of the other game skills. Original work, MIT."""
from runtime import cli
import hashlib,html,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
NOTICES=('MainLoop.js - Copyright (C) 2016 Isaac Sukin - MIT License.\nZzFX - Copyright (c) 2019 Frank Force - MIT License.\n\n'
 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), '
 'to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, '
 'and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n'
 'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n'
 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
 'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '
 'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')
DEF_VEHICLE={'wheelbase_m':0.9,'max_steer_deg':35,'accel':7.0,'brake':12.0,'reverse_accel':4.0,'drag':0.25,'max_v':11.0,'min_v':-4.0,'offroad_factor':0.55,'radius':0.38}
DEF_NPC={'ped_max_speed':1.1,'ped_max_force':6.0,'traffic_max_speed':3.5,'traffic_max_force':8.0,'police_max_speed':10.0,'police_max_force':30.0,
         'flee_panic_distance':3.0,'arrive_deceleration':2.0,'prediction_factor':1.0}
LOADS=re.compile(r'(?:\b(?:src|href|action|poster|data)\s*=\s*["\']?\s*(?:https?:)?//)|(?:url\(\s*["\']?\s*(?:https?:)?//)|@import|\bfetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon|EventSource|\bimport\s*\(',re.I)
URL=re.compile(r'https?://|(?<![:\w])//[a-z0-9.-]+\.[a-z]{2,}/',re.I)
def strip_header(js):
    js=js.lstrip()
    if js.startswith('/**'):js=js[js.index('*/')+2:].lstrip()
    return js
def check(doc):
    return {'loads_external_resources':bool(LOADS.search(doc)),'urls_found':URL.findall(doc)[:10]}
def calculate(p):
    m=p['map'];W,H=m['width'],m['height'];tiles=m['tiles']
    if len(tiles)!=H or any(len(r)!=W for r in tiles):raise ValueError('map.tiles does not match width/height')
    if any(set(r)-set('RSBP') for r in tiles):raise ValueError('map.tiles may only use R, S, B, P')
    def inside(t,name):
        if not(0<=t[0]<W and 0<=t[1]<H):raise ValueError(name+' is outside the map')
    pts=m['points']
    for k in('spawn','police_station','paint_shop'):inside(pts[k]['tile'],'points.'+k)
    for r in p['routes']['pedestrians']+p['routes']['traffic']:
        for t in r:inside(t,'route point')
    order=p['mission_order'];ids=[x['id'] for x in p['missions']]
    if sorted(order)!=sorted(ids):raise ValueError('mission_order must list every mission id exactly once (use G008 validate order)')
    for x in p['missions']:
        for k in('target','pickup'):
            if k in x:inside(x[k],'mission '+x['id']+' '+k)
    cat=p['economy']['catalog']
    for k in('paint_job','repair_kit'):
        if k not in cat:raise ValueError('economy.catalog needs '+k+' (use G009 catalog)')
    rules=p['wanted_rules']
    for k,n in(('star_thresholds',5),('cooldown_s',6),('police_units',6),('police_speed_factor',6),('search_radius_tiles',6)):
        if len(rules[k])!=n:raise ValueError('wanted_rules.'+k+' has the wrong length (use G007 rules)')
    cfg={'title':p['title'],'map':{'width':W,'height':H,'tiles':tiles,'seed':m.get('seed',0),'points':pts},
         'routes':{'pedestrians':p['routes']['pedestrians'],'traffic':p['routes']['traffic']},
         'vehicle':dict(DEF_VEHICLE,**p.get('vehicle',{})),'npc':dict(DEF_NPC,**p.get('npc',{})),'wanted_rules':rules,
         'missions':p['missions'],'mission_order':order,'economy':{'start_money':p['economy'].get('start_money',100),'cash_amount':p['economy'].get('cash_amount',50),'catalog':cat},
         'sounds':p.get('sounds',{}),'loop':{'timestep_ms':p.get('loop',{}).get('timestep_ms',1000/60)},
         'save':{'format':'skillpack-city-save','version':1},'render':{'tile_px':p.get('tile_px',32)}}
    cfg_json=json.dumps(cfg,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    tpl=(HERE/'game_template.html').read_text(encoding='utf-8')
    mainloop=strip_header((HERE/'vendor'/'mainloop.min.js').read_text(encoding='utf-8'))
    zzfx=(HERE/'vendor'/'ZzFXMicro.min.js').read_text(encoding='utf-8')
    runtime=(HERE/'game_runtime.js').read_text(encoding='utf-8')
    for part in (mainloop,zzfx,runtime):
        if '</script' in part.lower():raise ValueError('embedded script contains a closing script tag')
    doc=(tpl.replace('__NOTICES__',NOTICES).replace('__TITLE__',html.escape(p['title'])).replace('__CONFIG__',cfg_json)
         .replace('__MAINLOOP__',mainloop).replace('__ZZFX__',zzfx).replace('__RUNTIME__',runtime))
    chk=check(doc)
    if chk['loads_external_resources'] or chk['urls_found']:raise ValueError('generated HTML would reference an external URL')
    raw=doc.encode('utf-8')
    return {'operation':'build','html':doc if p.get('include_html',True) else '','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'self_contained':chk,'filename':'index.html','embedded':['MainLoop.js 1.0.4 (MIT)','ZzFXMicro 1.4.0 (MIT)','Skillpack city runtime (MIT)'],
            'summary':{'map':'%dx%d'%(W,H),'pedestrians':len(p['routes']['pedestrians']),'traffic':len(p['routes']['traffic']),'missions':len(ids),'sounds':sorted(p.get('sounds',{}))},
            'how_to_play':'Save html as index.html and open it in any modern browser (works offline).'}
if __name__=='__main__':raise SystemExit(cli(calculate))
