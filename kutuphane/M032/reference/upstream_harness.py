"""Runs the pinned upstream jellyfish pure-Python jaro_winkler_similarity inside an independent re-implementation
of the documented search/reverse rules; dataset reading uses Skillpack's shared loader; no network."""
import importlib,importlib.util,json,os,re,sys,unicodedata,warnings
from pathlib import Path
warnings.simplefilter('ignore',DeprecationWarning)
PACK=Path(__file__).resolve().parents[1]
os.environ.setdefault('SKILLPACK_MAP_DATA',str(PACK/'tests'/'fixtures'))
spec=importlib.util.spec_from_file_location('upstream_jellyfish',PACK/'upstream'/'python'/'jellyfish'/'_jellyfish.py')
jf=importlib.util.module_from_spec(spec);spec.loader.exec_module(jf)
sys.path.insert(0,str(PACK/'tool'));mapdata=importlib.import_module('mapdata')
def norm(s):
    s=s.replace('İ','i').replace('I','ı').lower()
    for a,b in zip('çğıöşüâîû','cgiosuaiu'):s=s.replace(a,b)
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
    return ' '.join(re.sub(r'[^0-9a-z]+',' ',s).split())
def score(q,n):
    s=jf.jaro_winkler_similarity(q,n);k=len(q.split());t=n.split()
    if len(t)>k:s=max(s,0.95*max(jf.jaro_winkler_similarity(q,' '.join(t[i:i+k])) for i in range(len(t)-k+1)))
    return s
AREA={'city','town','village','suburb','quarter','neighbourhood','hamlet','locality','square'}
out=[]
for p in json.load(sys.stdin):
    pl,_=mapdata.places(p['dataset']);cats=set(p.get('categories',[]))
    if p['operation']=='search':
        q=norm(p['query']);near=p.get('near');hits=[]
        for i,x in enumerate(pl):
            if cats and x['category'] not in cats:continue
            s=score(q,norm(x['name']))
            if s<p.get('min_score',0.85):continue
            d=mapdata.haversine(near['lat'],near['lon'],x['lat'],x['lon']) if near else 0.0
            hits.append((-s,d,i))
        hits.sort()
        out.append({'match_count':len(hits),'matches':[{'name':pl[i]['name'],'score':round(-s,4)} for s,d,i in hits[:p.get('limit',5)]]})
    else:
        lat,lon,maxd=p['lat'],p['lon'],p.get('max_distance_m',500)
        def best(f):
            c=sorted((mapdata.haversine(lat,lon,x['lat'],x['lon']),i) for i,x in enumerate(pl) if f(x))
            c=[t for t in c if t[0]<=maxd]
            return {'name':pl[c[0][1]]['name'],'distance_m':round(c[0][0],1)} if c else None
        pois=sorted((mapdata.haversine(lat,lon,x['lat'],x['lon']),i) for i,x in enumerate(pl) if x['category']!='street' and x['category'] not in AREA and (not cats or x['category'] in cats))
        pois=[t for t in pois if t[0]<=maxd][:p.get('limit',5)]
        out.append({'street':best(lambda x:x['category']=='street'),'area':best(lambda x:x['category'] in AREA),'nearby':[{'name':pl[i]['name'],'distance_m':round(d,1)} for d,i in pois]})
sys.stdout.write(json.dumps(out))
