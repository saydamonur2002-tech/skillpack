"""End to end: run the skill-independent flow, check the generated index.html, and compare the browser runtime formulas with the Python skills."""
import json,math,re,shutil,subprocess,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
NODE=shutil.which('node')
def tool(pid,payload):
    p=subprocess.run([sys.executable,str(ROOT/pid/'tool'/'main.py')],input=json.dumps(payload).encode(),capture_output=True,timeout=60)
    r=json.loads(p.stdout);assert r['ok'],r;return r['result']
@pytest.fixture(scope='module')
def built(tmp_path_factory):
    out=tmp_path_factory.mktemp('oyun')
    p=subprocess.run([sys.executable,str(ROOT/'flows'/'run_flow.py'),'--out',str(out),'--quiet']+([] if NODE else ['--no-node']),capture_output=True,timeout=300)
    assert p.returncode==0,p.stdout.decode()+p.stderr.decode()
    return out
def test_flow_runs_every_step(built):
    rep=json.loads((built/'akis_raporu.json').read_text())
    flow=json.loads((ROOT/'flows'/'oyun-kur.flow.json').read_text())
    assert [s['id'] for s in rep['steps']]==[s['id'] for s in flow['steps']]
    assert all(s['ok'] and not s['failed'] for s in rep['steps'])
    assert all(s['input_bytes']<65536 for s in rep['steps'])
def test_index_html_self_contained(built):
    h=(built/'index.html').read_text()
    assert 'http://' not in h and 'https://' not in h and not re.search(r'\b(src|href)\s*=',h)
    assert '<canvas id="game">' in h and 'MainLoop' in h
    v=json.loads((built/'akis_raporu.json').read_text())['verification'];assert v['ok'] and v['self_contained']
@pytest.mark.skipif(NODE is None,reason='Node.js not installed')
def test_headless_game_loop(built):
    v=json.loads((built/'akis_raporu.json').read_text())['verification']
    assert v['js_syntax_ok'] is True
    h=v['headless'];assert h['ok'] and h['errors']==0 and h['moved']>1 and h['mainloop_present'] and h['load_error'] is None
@pytest.mark.skipif(NODE is None,reason='Node.js not installed')
def test_runtime_formulas_match_skills(built):
    flow=json.loads((ROOT/'flows'/'oyun-kur.flow.json').read_text());V=flow['variables']['vehicle'];dt=flow['variables']['timestep_ms']/1000
    car=[{'acceleration':7,'steer_deg':0,'repeat':60},{'acceleration':0,'steer_deg':20,'repeat':45},{'acceleration':-3,'steer_deg':-50,'repeat':30}]
    boxes=[[1.2,0.5,0.38,0,0],[1.25,1.2,0.38,0,0],[0.5,-0.2,0.38,0,0],[0.3,0.45,0.38,0,0],[2.5,2.5,0.38,0,0]]
    pursuit={'vehicle':{'x':0,'y':0,'vx':0,'vy':1,'max_speed':8.5,'max_force':30},'evader':{'x':12,'y':6,'vx':5,'vy':0},'steps':240}
    fnv=['','a','foobar','Görev: Şehir']
    p=subprocess.run([NODE,str(ROOT/'tests'/'js_formulas.js'),str(built/'index.html')],input=json.dumps({'car':car,'boxes':boxes,'pursuit':pursuit,'fnv':fnv}).encode(),capture_output=True,timeout=60)
    assert p.returncode==0,p.stderr.decode();js=json.loads(p.stdout)
    py=tool('G003',{'operation':'simulate','state':{'x':0,'y':0,'yaw':0,'v':0},'params':{'wheelbase_m':V['wheelbase_m'],'max_steer_deg':V['max_steer_deg'],'dt_s':dt},'controls':car})['final']
    for k in('x','y','yaw','v'):assert js['car'][k]==pytest.approx(py[k],abs=1e-9)
    col=tool('G004',{'operation':'test','pairs':[{'a':{'type':'circle','x':b[0],'y':b[1],'r':b[2]},'b':{'type':'box','x':b[3],'y':b[4],'w':1,'h':1}} for b in boxes]})['results']
    for j,s in zip(js['boxes'],col):
        if s['collides']:assert j==pytest.approx(s['push_a'],abs=1e-9)
        else:assert j is None
    pr=tool('G006',dict(pursuit,operation='simulate',behavior='pursuit',dt_s=dt,steps=240))['final']
    for k in('x','y','vx','vy'):assert js['pursuit'][k]==pytest.approx(pr[k],abs=1e-7)
    env=json.loads(js['envelope']);ld=tool('G010',{'operation':'load','envelope':env});assert ld['valid'] is True and ld['state']['money']==777
    assert tool('G010',{'operation':'save','state':env['state']})['envelope']['checksum']==env['checksum']
    for t,h in zip(fnv,js['fnv']):assert tool('G010',{'operation':'checksum','text':t})['checksum']=='fnv1a32:'+h
def test_flow_stops_and_asks_on_failed_check(tmp_path):
    flow=json.loads((ROOT/'flows'/'oyun-kur.flow.json').read_text())
    flow['steps'][0]['checks'].append({'path':'result.counts.B','op':'>=','value':100000,'why_tr':'test'})
    f=tmp_path/'bozuk.flow.json';f.write_text(json.dumps(flow,ensure_ascii=False))
    p=subprocess.run([sys.executable,str(ROOT/'flows'/'run_flow.py'),'--flow',str(f),'--out',str(tmp_path/'o'),'--no-node'],capture_output=True,timeout=120)
    assert p.returncode==3 and 'DUR VE SOR' in p.stdout.decode()
