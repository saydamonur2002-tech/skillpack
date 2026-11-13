"""Recheck all unchanged JSON CLIs using the existing first successful vector."""
from pathlib import Path
import datetime,json,os,subprocess,sys
from mcp_checks import equal
from jsonschema import Draft7Validator
ROOT=Path(__file__).resolve().parent.parent
results=[]
for p in sorted(ROOT.glob('[AB]*/manifest.json')):
 m=json.loads(p.read_text());pack=p.parent
 vector=next(v for v in json.loads((pack/'tests/vectors.json').read_text()) if not v.get('error'))
 env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONNOUSERSITE']='1'
 process=subprocess.run([sys.executable,str(pack/'tool/main.py')],input=json.dumps(vector['input']),text=True,capture_output=True,timeout=90,cwd=ROOT,env=env)
 record={'id':m['id'],'passed':False,'returncode':process.returncode,'stderr':process.stderr[-1000:]}
 try:
  output=json.loads(process.stdout);record['response']=output
  assert process.returncode==0 and output['ok'] is True
  Draft7Validator(m['outputs']).validate(output)
  equal(output['result'],vector['result'],m['id'])
  record['passed']=True
 except Exception as exc:record['error']=str(exc)
 results.append(record)
report={'checked_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).isoformat(),'time_zone':'Europe/Istanbul','tools':results}
(ROOT/'CLI_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print('CLI checks:',sum(r['passed'] for r in results),'passed;',sum(not r['passed'] for r in results),'failed')
sys.exit(0 if all(r['passed'] for r in results) and len(results)==75 else 1)
