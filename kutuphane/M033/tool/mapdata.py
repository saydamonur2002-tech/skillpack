"""Skillpack local map-data access (shared by the map packs). Offline only: no network, no writes.

Datasets are looked up by NAME only (no paths) inside one directory chosen by the human:
  1. the SKILLPACK_MAP_DATA environment variable, if set; otherwise
  2. a sibling folder named map_data next to this pack.
A name with an extension (.geojson, .json, .csv, .osm) is used as a file name; a bare name such as
"demo_kadikoy" is resolved to "<name>_<layer>.geojson", then "<name>_<layer>.csv", then "<name>.osm".
"""
import csv,json,math,os,re
import xml.etree.ElementTree as ET
from pathlib import Path
PACK=Path(__file__).resolve().parents[1]
NAME_RE=re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$')
EXTS=('.geojson','.json','.csv','.osm')
MAX_FILE_BYTES=64*1024*1024
EARTH_R=6371e3  # mean radius used by chrisveness/geodesy latlon-spherical distanceTo

def data_dir():
    env=os.environ.get('SKILLPACK_MAP_DATA')
    d=Path(env).expanduser() if env else PACK.parent/'map_data'
    if not d.is_dir():raise ValueError('Map data folder not found: set SKILLPACK_MAP_DATA or create map_data next to the pack')
    return d.resolve()

def dataset_path(name,layer):
    if not NAME_RE.match(name) or '..' in name:raise ValueError('Dataset must be a plain file or dataset name without folders')
    d=data_dir()
    cands=[name] if name.lower().endswith(EXTS) else [name+'_'+layer+'.geojson',name+'_'+layer+'.csv',name+'.osm']
    for c in cands:
        p=(d/c).resolve()
        if p.parent!=d:raise ValueError('Dataset must stay inside the map data folder')
        if p.is_file():
            if p.stat().st_size>MAX_FILE_BYTES:raise ValueError('Dataset file exceeds 64 MiB')
            return p
    raise ValueError('Dataset not found for layer %s: %s'%(layer,', '.join(cands)))

def haversine(lat1,lon1,lat2,lon2,radius=EARTH_R):
    """Haversine distance; same operation order as geodesy latlon-spherical distanceTo (MIT, Chris Veness)."""
    p1=math.radians(lat1);l1=math.radians(lon1);p2=math.radians(lat2);l2=math.radians(lon2)
    dp=p2-p1;dl=l2-l1
    a=math.sin(dp/2)*math.sin(dp/2)+math.cos(p1)*math.cos(p2)*math.sin(dl/2)*math.sin(dl/2)
    return radius*(2*math.atan2(math.sqrt(a),math.sqrt(1-a)))

# ---------- readers ----------
def _features_geojson(p):
    d=json.loads(p.read_text(encoding='utf-8'))
    if d.get('type')=='FeatureCollection':feats=d.get('features',[])
    elif d.get('type')=='Feature':feats=[d]
    else:raise ValueError('GeoJSON must be a FeatureCollection or Feature')
    meta=d.get('metadata') or {}
    return feats,meta

def _features_csv(p):
    feats=[]
    with p.open(newline='',encoding='utf-8-sig') as f:
        r=csv.DictReader(f);cols={c.lower():c for c in (r.fieldnames or [])}
        lat=cols.get('lat') or cols.get('latitude');lon=cols.get('lon') or cols.get('lng') or cols.get('longitude')
        if not lat or not lon or 'name' not in cols:raise ValueError('CSV needs name, lat and lon columns')
        for i,row in enumerate(r):
            props={k:v for k,v in row.items() if k not in (lat,lon) and v not in (None,'')}
            props.setdefault('osm_id','csv/%d'%(i+1))
            feats.append({'type':'Feature','properties':props,'geometry':{'type':'Point','coordinates':[float(row[lon]),float(row[lat])]}})
    return feats,{}

ROAD={'motorway','motorway_link','trunk','trunk_link','primary','primary_link','secondary','secondary_link','tertiary','tertiary_link','unclassified','residential','living_street','service','pedestrian','footway','path','steps','cycleway','track','road','corridor'}
CATKEYS=['amenity','shop','tourism','leisure','healthcare','historic','railway','public_transport','place','office','craft','man_made']
def osm_category(t):
    for k in CATKEYS:
        if k in t and t[k] not in ('yes','no'):
            if k=='railway' and t[k] not in ('station','halt','tram_stop','subway_entrance'):continue
            if k=='public_transport' and t[k] not in ('station','stop_position','platform'):continue
            return k,t[k]
    if t.get('highway')=='bus_stop':return 'highway','bus_stop'
    return None

def _features_osm(p,layer):
    nodes={};ways=[];ntags=[]
    for _,el in ET.iterparse(p,events=('end',)):
        if el.tag=='node':
            i=int(el.get('id'));nodes[i]=(float(el.get('lon')),float(el.get('lat')))
            t={c.get('k'):c.get('v') for c in el if c.tag=='tag'}
            if t:ntags.append((i,t))
            el.clear()
        elif el.tag=='way':
            ways.append((int(el.get('id')),[int(c.get('ref')) for c in el if c.tag=='nd'],{c.get('k'):c.get('v') for c in el if c.tag=='tag'}));el.clear()
        elif el.tag=='relation':el.clear()
    feats=[]
    if layer=='roads':
        for wid,nd,t in ways:
            if t.get('highway') not in ROAD or t.get('area')=='yes' or len(nd)<2 or not all(n in nodes for n in nd):continue
            props={'osm_id':'way/%d'%wid,'highway':t['highway']}
            for k in ('name','oneway','maxspeed','junction','access','foot','motor_vehicle','bicycle'):
                if k in t:props[k]=t[k]
            feats.append({'type':'Feature','properties':props,'geometry':{'type':'LineString','coordinates':[list(nodes[n]) for n in nd]}})
    elif layer=='places':
        def add(osm,t,lon,lat):
            c=osm_category(t)
            if c and 'name' in t:feats.append({'type':'Feature','properties':{'osm_id':osm,'name':t['name'],'kind':c[0],'category':c[1]},'geometry':{'type':'Point','coordinates':[lon,lat]}})
        for i,t in ntags:add('node/%d'%i,t,*nodes[i])
        for wid,nd,t in ways:
            pts=[nodes[n] for n in nd if n in nodes]
            if 'highway' in t or len(pts)!=len(nd) or not pts:continue
            if len(pts)>1 and nd[0]==nd[-1]:pts=pts[:-1]
            add('way/%d'%wid,t,sum(q[0] for q in pts)/len(pts),sum(q[1] for q in pts)/len(pts))
    else:
        for wid,nd,t in ways:
            if len(nd)>=4 and nd[0]==nd[-1] and all(n in nodes for n in nd) and any(k in t for k in ('leisure','landuse','natural')):
                props={'osm_id':'way/%d'%wid,'kind':'area','category':t.get('leisure') or t.get('landuse') or t.get('natural')}
                if 'name' in t:props['name']=t['name']
                feats.append({'type':'Feature','properties':props,'geometry':{'type':'Polygon','coordinates':[[list(nodes[n]) for n in nd]]}})
    return feats,{}

def load_layer(name,layer):
    p=dataset_path(name,layer);s=p.suffix.lower()
    if s in ('.geojson','.json'):feats,meta=_features_geojson(p)
    elif s=='.csv':feats,meta=_features_csv(p)
    else:feats,meta=_features_osm(p,layer)
    return feats,{'file':p.name,'attribution':meta.get('attribution'),'license':meta.get('license')}

def places(name):
    feats,info=load_layer(name,'places');out=[]
    for f in feats:
        g=f.get('geometry') or {};pr=f.get('properties') or {}
        if g.get('type')!='Point' or not pr.get('name'):continue
        lon,lat=g['coordinates'][:2]
        out.append({'name':str(pr['name']),'category':str(pr.get('category','unknown')),'kind':str(pr.get('kind','')),'id':str(pr.get('osm_id','')),'lat':float(lat),'lon':float(lon),'props':pr})
    return out,info

# ---------- road graph ----------
CAR_SPEED={'motorway':90,'motorway_link':45,'trunk':70,'trunk_link':35,'primary':50,'primary_link':30,'secondary':40,'secondary_link':25,'tertiary':35,'tertiary_link':20,'unclassified':30,'residential':25,'living_street':10,'service':15,'road':25}
WALK_EXCLUDE={'motorway','motorway_link','trunk','trunk_link'}
BIKE_EXCLUDE={'motorway','motorway_link','trunk','trunk_link','steps'}
PROFILES=('car','walk','bike')

def _speed_kmh(props,profile):
    hw=props.get('highway')
    if profile=='walk':return 3.0 if hw=='steps' else 5.0
    if profile=='bike':return 5.0 if hw in ('footway','pedestrian') else 15.0
    ms=str(props.get('maxspeed','')).strip()
    if ms.isdigit() and 5<=int(ms)<=150:return float(ms)
    return float(CAR_SPEED[hw])

def _allowed(props,profile):
    hw=props.get('highway');acc=props.get('access')
    if profile=='car':
        if hw not in CAR_SPEED:return False
        if acc in ('no','private') or props.get('motor_vehicle') in ('no','private'):return False
        return True
    if hw not in ROAD:return False
    if profile=='walk':
        if hw in WALK_EXCLUDE or props.get('foot') in ('no','private'):return False
        return not (acc in ('no','private') and props.get('foot') not in ('yes','designated'))
    if hw in BIKE_EXCLUDE or props.get('bicycle') in ('no','private'):return False
    if hw in ('footway','pedestrian') and props.get('bicycle') not in ('yes','designated'):return False
    return not (acc in ('no','private') and props.get('bicycle') not in ('yes','designated'))

def _direction(props,profile):
    if profile=='walk':return 0
    ow=str(props.get('oneway','')).lower()
    if ow in ('yes','true','1'):return 1
    if ow=='-1':return -1
    if ow=='no':return 0
    if props.get('junction') in ('roundabout','circular') or props.get('highway') in ('motorway','motorway_link'):return 1
    return 0

def build_graph(name,profile,optimize):
    """Return (coords, adj, edges, info). adj[u] is an insertion-ordered dict {v: edge}; edge has length_m, time_s, weight, name, highway.
    Vertices are LineString positions keyed by coordinates rounded to 7 decimals, so lines connect where they share a vertex."""
    if profile not in PROFILES:raise ValueError('profile must be car, walk or bike')
    feats,info=load_layer(name,'roads')
    key={};coords=[];adj=[]
    def vid(c):
        k=(round(c[0],7),round(c[1],7))
        if k not in key:key[k]=len(coords);coords.append((c[1],c[0]));adj.append({})
        return key[k]
    for f in feats:
        g=f.get('geometry') or {};pr=f.get('properties') or {}
        if g.get('type')!='LineString' or not _allowed(pr,profile):continue
        sp=_speed_kmh(pr,profile)/3.6;d=_direction(pr,profile);ids=[vid(c) for c in g['coordinates']]
        for a,b in zip(ids,ids[1:]):
            if a==b:continue
            L=haversine(coords[a][0],coords[a][1],coords[b][0],coords[b][1]);T=L/sp
            e={'length_m':L,'time_s':T,'weight':T if optimize=='time' else L,'name':pr.get('name'),'highway':pr.get('highway')}
            for u,v in ((a,b),(b,a)) if d==0 else (((a,b),) if d==1 else ((b,a),)):
                old=adj[u].get(v)
                if old is None or e['weight']<old['weight']:adj[u][v]=e
    if not coords:raise ValueError('No routable roads for this profile in the dataset')
    info.update({'vertices':len(coords),'directed_edges':sum(len(a) for a in adj),'profile':profile,'optimize':optimize})
    return coords,adj,info

def snap(coords,adj,lat,lon,need,max_m):
    """Nearest vertex with an outgoing (need='out') or incoming (need='in') edge; ties keep the lower index."""
    has_in=None
    if need=='in':
        has_in=set()
        for a in adj:has_in.update(a.keys())
    best=None;bd=None
    for i,(la,lo) in enumerate(coords):
        if need=='out' and not adj[i]:continue
        if need=='in' and i not in has_in:continue
        d=haversine(lat,lon,la,lo)
        if bd is None or d<bd:best=i;bd=d
    if best is None:raise ValueError('No routable vertex found')
    if bd>max_m:raise ValueError('Nearest road is %.0f m away (limit %.0f m); the point is probably outside the dataset'%(bd,max_m))
    return best,bd

# Turkish/English everyday words -> OpenStreetMap category values used in the places layer.
CATEGORY_ALIASES={
 'eczane':['pharmacy'],'kafe':['cafe'],'kahve':['cafe','coffee'],'restoran':['restaurant'],'lokanta':['restaurant'],
 'yemek':['restaurant','fast_food'],'fast food':['fast_food'],'banka':['bank'],'atm':['atm'],'bankamatik':['atm'],
 'hastane':['hospital'],'klinik':['clinic'],'doktor':['doctors','clinic'],'dis':['dentist'],'disci':['dentist'],
 'okul':['school'],'universite':['university'],'kutuphane':['library'],'market':['supermarket','convenience'],
 'supermarket':['supermarket'],'bakkal':['convenience'],'firin':['bakery'],'pastane':['pastry','bakery'],
 'otel':['hotel','hostel','guest_house'],'iskele':['ferry_terminal'],'vapur':['ferry_terminal'],
 'durak':['bus_stop','stop_position','platform','tram_stop'],'otobus duragi':['bus_stop','stop_position','platform'],
 'tramvay':['tram_stop'],'metro':['station','subway_entrance'],'istasyon':['station'],'park':['park'],
 'cami':['place_of_worship'],'ibadethane':['place_of_worship'],'polis':['police'],'karakol':['police'],
 'postane':['post_office'],'kargo':['post_office'],'benzinlik':['fuel'],'akaryakit':['fuel'],'otopark':['parking'],
 'sinema':['cinema'],'tiyatro':['theatre'],'muze':['museum'],'bar':['bar','pub'],'meyhane':['pub','bar'],
 'kuafor':['hairdresser'],'berber':['hairdresser'],'kitapci':['books'],'giyim':['clothes'],'taksi':['taxi'],
 'veteriner':['veterinary'],'tuvalet':['toilets'],'cesme':['drinking_water'],'sokak':['street'],'cadde':['street'],
 'mahalle':['quarter','neighbourhood','suburb']}

def resolve_categories(values):
    """Map each requested category through CATEGORY_ALIASES (after Turkish folding); unknown words are kept as given."""
    out=[];used={}
    TRL=str.maketrans({'İ':'i','I':'ı','ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u'})
    for v in values:
        k=' '.join(v.translate(TRL).lower().translate(TRL).replace('_',' ').split())
        cands=[k,re.sub(r'(ler|lar)$','',k),re.sub(r'(leri|lari|si|i)$','',k)]
        cats=next((CATEGORY_ALIASES[c] for c in cands if c in CATEGORY_ALIASES),[v])
        used[v]=cats
        for c in cats:
            if c not in out:out.append(c)
    return out,used
