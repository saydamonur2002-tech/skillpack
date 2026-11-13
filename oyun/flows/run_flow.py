#!/usr/bin/env python3
"""Skill-independent flow runner: executes flows/oyun-kur.flow.json step by step, validates every step and writes index.html.

Each step calls one pack's tool/main.py through its stdin/stdout JSON contract (the same contract the MCP server uses).
No network. Usage: python3 flows/run_flow.py [--flow FILE] [--out DIR] [--set name=value ...] [--no-node]
Exit codes: 0 ok, 2 a skill returned an error, 3 a check failed (stop and ask), 4 final verification failed.
"""
import argparse,json,re,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(obj,path):
    cur=obj
    for part in path.split('.'):
        if part=='':continue
        if isinstance(cur,list):cur=cur[int(part)]
        elif isinstance(cur,dict):
            if part not in cur:raise KeyError(path)
            cur=cur[part]
        else:raise KeyError(path)
    return cur
def resolve(x,ctx,var):
    if isinstance(x,dict):
        if len(x)==1:
            (k,v),=x.items()
            if k=='$var':return get(var,v)
            if k=='$ref':return get(ctx,v)
            if k=='$tile_center_x':return get(ctx,v)[0]+0.5
            if k=='$tile_center_y':return get(ctx,v)[1]+0.5
            if k=='$concat':
                out=[]
                for part in v:out+=resolve(part,ctx,var)
                return out
            if k=='$range':return [round(v['start']+i*v['step'],6) for i in range(v['count'])]
            if k=='$pluck':
                src=get(ctx,v['from'])
                if isinstance(src,dict):return {n:it[v['field']] for n,it in src.items()}
                return [it[v['field']] for it in src]
        return {k:resolve(v,ctx,var) for k,v in x.items()}
    if isinstance(x,list):return [resolve(v,ctx,var) for v in x]
    return x
def check(value,op,want):
    if op=='==':return value==want
    if op=='!=':return value!=want
    if op=='<':return value<want
    if op=='<=':return value<=want
    if op=='>':return value>want
    if op=='>=':return value>=want
    if op=='len==':return len(value)==want
    if op=='len>=':return len(value)>=want
    raise ValueError('unknown check op '+op)
def call(skill,payload):
    raw=json.dumps(payload,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')
    if len(raw)>65536:return {'ok':False,'error':{'code':'INPUT_TOO_LARGE','message':'step input is %d bytes; the skill limit is 65536'%len(raw)}},len(raw)
    p=subprocess.run([sys.executable,str(ROOT/skill/'tool'/'main.py')],input=raw,capture_output=True,timeout=30)
    return json.loads(p.stdout.decode('utf-8')),len(raw)
URL=re.compile(r'https?://|\b(?:src|href)\s*=\s*["\']?//|@import|url\(\s*["\']?(?:https?:)?//',re.I)
def scripts(html):return [m.group(2) for m in re.finditer(r'<script([^>]*)>(.*?)</script>',html,re.S) if 'application/json' not in m.group(1)]
def verify(html_path,use_node):
    html=html_path.read_text(encoding='utf-8');rep={'bytes':len(html.encode()),'external_refs':URL.findall(html)}
    rep['self_contained']=not rep['external_refs']
    node=shutil.which('node') if use_node else None
    if node:
        ok=True
        with tempfile.TemporaryDirectory() as d:
            for i,s in enumerate(scripts(html)):
                f=Path(d)/('s%d.js'%i);f.write_text(s,encoding='utf-8')
                r=subprocess.run([node,'--check',str(f)],capture_output=True)
                ok=ok and r.returncode==0
        rep['js_syntax_ok']=ok
        r=subprocess.run([node,str(Path(__file__).with_name('headless_check.js')),str(html_path)],capture_output=True,timeout=120)
        rep['headless']=json.loads(r.stdout) if r.returncode==0 else {'ok':False,'error':r.stderr.decode()[-800:]}
    else:rep['js_syntax_ok']=None;rep['headless']={'ok':None,'note':'Node.js not found; open index.html in a browser to test'}
    rep['ok']=rep['self_contained'] and rep['js_syntax_ok'] is not False and rep['headless'].get('ok') is not False
    return rep
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument('--flow',default=str(Path(__file__).with_name('oyun-kur.flow.json')));ap.add_argument('--out',default='oyun_cikti')
    ap.add_argument('--set',action='append',default=[]);ap.add_argument('--no-node',action='store_true');ap.add_argument('--quiet',action='store_true')
    a=ap.parse_args(argv)
    flow=json.loads(Path(a.flow).read_text(encoding='utf-8'));var=flow['variables']
    for s in a.set:
        k,_,v=s.partition('=');var[k]=json.loads(v) if v[:1] in '0123456789-[{tf' else v
    out=Path(a.out);(out/'adimlar').mkdir(parents=True,exist_ok=True);ctx={};report={'flow':flow['name'],'steps':[]}
    say=(lambda *x:None) if a.quiet else print
    for n,st in enumerate(flow['steps'],1):
        payload=resolve(st['input'],ctx,var);res,size=call(st['skill'],payload)
        (out/'adimlar'/('%02d_%s.json'%(n,st['id']))).write_text(json.dumps({'skill':st['skill'],'input':payload,'output':res},ensure_ascii=False,indent=1)[:5_000_000],encoding='utf-8')
        entry={'n':n,'id':st['id'],'skill':st['skill'],'input_bytes':size,'ok':res.get('ok')}
        if not res.get('ok'):
            entry['error']=res.get('error');report['steps'].append(entry);report['stopped_at']=st['id']
            say('[%02d] %-16s %s HATA: %s'%(n,st['id'],st['skill'],res.get('error',{}).get('message')));say('DUR VE SOR: '+st.get('stop_and_ask_tr',''))
            (out/'akis_raporu.json').write_text(json.dumps(report,ensure_ascii=False,indent=1),encoding='utf-8');return 2
        ctx[st['id']]=res
        fails=[]
        for c in st.get('checks',[]):
            want=resolve(c['value'],ctx,var)
            try:val=get(res,c['path']);good=check(val,c['op'],want)
            except (KeyError,IndexError,TypeError):val=None;good=False
            if not good:fails.append({'path':c['path'],'op':c['op'],'want':want,'got':val,'why_tr':c.get('why_tr','')})
        entry['checks']=len(st.get('checks',[]));entry['failed']=fails;report['steps'].append(entry)
        say('[%02d] %-16s %s %s'%(n,st['id'],st['skill'],'tamam' if not fails else 'KONTROL BAŞARISIZ'))
        if fails:
            report['stopped_at']=st['id'];say('DUR VE SOR: '+st.get('stop_and_ask_tr',''))
            for f in fails:say('  - %s %s %r (bulunan %r) %s'%(f['path'],f['op'],f['want'],f['got'],f['why_tr']))
            (out/'akis_raporu.json').write_text(json.dumps(report,ensure_ascii=False,indent=1),encoding='utf-8');return 3
    html=ctx['html']['result']['html'];hp=out/'index.html';hp.write_text(html,encoding='utf-8')
    report['index_html']=str(hp);report['verification']=verify(hp,not a.no_node)
    (out/'akis_raporu.json').write_text(json.dumps(report,ensure_ascii=False,indent=1),encoding='utf-8')
    v=report['verification'];say('index.html: %d bayt, bağımsız=%s, js=%s, başsız deneme=%s'%(v['bytes'],v['self_contained'],v['js_syntax_ok'],v['headless'].get('ok')))
    return 0 if v['ok'] else 4
if __name__=='__main__':raise SystemExit(main())
