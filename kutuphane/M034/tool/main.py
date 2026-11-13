#!/usr/bin/env python3
"""Static map renderer: GeoJSON to SVG (with optional offline road basemap). See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
# --- simplify-js port (mourner/simplify-js, BSD-2-Clause); see M021 for the standalone pack ---
def _sq_dist(p1,p2):
    dx=p1[0]-p2[0];dy=p1[1]-p2[1]
    return dx*dx+dy*dy

def _sq_seg_dist(p,p1,p2):
    x=p1[0];y=p1[1];dx=p2[0]-x;dy=p2[1]-y
    if dx!=0 or dy!=0:
        t=((p[0]-x)*dx+(p[1]-y)*dy)/(dx*dx+dy*dy)
        if t>1:x=p2[0];y=p2[1]
        elif t>0:x+=dx*t;y+=dy*t
    dx=p[0]-x;dy=p[1]-y
    return dx*dx+dy*dy

def _radial(points,idx,sq_tol):
    prev=idx[0];keep=[prev];point=prev
    for k in idx[1:]:
        point=k
        if _sq_dist(points[k],points[prev])>sq_tol:keep.append(k);prev=k
    if prev!=point:keep.append(point)
    return keep

def _douglas_peucker(points,idx,sq_tol):
    # Explicit-stack, in-order equivalent of upstream recursive simplifyDPStep.
    last=len(idx)-1;out=[idx[0]];stack=[('span',0,last)]
    while stack:
        item=stack.pop()
        if item[0]=='emit':out.append(idx[item[1]]);continue
        _,first,end=item;max_sq=sq_tol;index=None
        for i in range(first+1,end):
            d=_sq_seg_dist(points[idx[i]],points[idx[first]],points[idx[end]])
            if d>max_sq:index=i;max_sq=d
        if max_sq>sq_tol:
            if end-index>1:stack.append(('span',index,end))
            stack.append(('emit',index))
            if index-first>1:stack.append(('span',first,index))
    out.append(idx[last])
    return out

def simplify(points,tol,hq=False):
    if len(points)<=2:return list(points)
    sq=tol*tol;idx=list(range(len(points)))
    if not hq:idx=_radial(points,idx,sq)
    idx=_douglas_peucker(points,idx,sq)
    return [points[i] for i in idx]

# --- sphericalmercator px/ll port (mapbox/sphericalmercator v1.1.0, BSD-3-Clause) ---
import math,os,re,json
from pathlib import Path
EPSLN=1.0e-10;D2R=math.pi/180;R2D=180/math.pi;A=6378137.0;SIZE=256
_CACHE={}
def _cache(size):
    if size not in _CACHE:
        c={'Bc':[],'Cc':[],'zc':[],'Ac':[]};s=size
        for d in range(30):
            c['Bc'].append(s/360);c['Cc'].append(s/(2*math.pi));c['zc'].append(s/2);c['Ac'].append(s);s*=2
        _CACHE[size]=c
    return _CACHE[size]

def _is_float(z):return z%1!=0

def _js_round(x):return math.floor(x+0.5)

def px(ll,zoom,size=SIZE):
    if _is_float(zoom):
        s=size*math.pow(2,zoom);d=s/2;bc=s/360;cc=s/(2*math.pi);ac=s
        f=min(max(math.sin(D2R*ll[1]),-0.9999),0.9999)
        x=d+ll[0]*bc;y=d+0.5*math.log((1+f)/(1-f))*-cc
        if x>ac:x=ac
        if y>ac:y=ac
        return [x,y]
    c=_cache(size);z=int(zoom);d=c['zc'][z]
    f=min(max(math.sin(D2R*ll[1]),-0.9999),0.9999)
    x=_js_round(d+ll[0]*c['Bc'][z]);y=_js_round(d+0.5*math.log((1+f)/(1-f))*(-c['Cc'][z]))
    if x>c['Ac'][z]:x=c['Ac'][z]
    if y>c['Ac'][z]:y=c['Ac'][z]
    return [x,y]

def ll(p,zoom,size=SIZE):
    if _is_float(zoom):
        s=size*math.pow(2,zoom);bc=s/360;cc=s/(2*math.pi);zc=s/2
        g=(p[1]-zc)/-cc;lon=(p[0]-zc)/bc;lat=R2D*(2*math.atan(math.exp(g))-0.5*math.pi);return [lon,lat]
    c=_cache(size);z=int(zoom)
    g=(p[1]-c['zc'][z])/(-c['Cc'][z]);lon=(p[0]-c['zc'][z])/c['Bc'][z];lat=R2D*(2*math.atan(math.exp(g))-0.5*math.pi)
    return [lon,lat]

# --- Skillpack static SVG map renderer (no network, no tiles) ---
import mapdata
from xml.sax.saxutils import escape
ROAD_STYLE={'motorway':(5,'#e892a2'),'trunk':(4.5,'#f9b29c'),'primary':(4,'#fcd6a4'),'secondary':(3.5,'#f7fabf'),'tertiary':(3,'#ffffff'),
 'unclassified':(2.2,'#ffffff'),'residential':(2.2,'#ffffff'),'living_street':(2,'#ededed'),'road':(2,'#ffffff'),'service':(1.4,'#ffffff'),
 'pedestrian':(2,'#dddde8'),'footway':(0.9,'#f4a582'),'path':(0.9,'#f4a582'),'steps':(1.2,'#f4a582'),'cycleway':(0.9,'#7aa7e0'),'track':(1,'#c9a87c'),'corridor':(0.8,'#cccccc')}
MINOR={'footway','path','steps','cycleway','track','corridor','service'}
AREA_FILL={'park':'#c8facc','garden':'#cdebb0','playground':'#dffce2','pitch':'#aae0cb','grass':'#cdebb0','cemetery':'#aacbaf','forest':'#add19e','wood':'#add19e',
 'water':'#aad3df','stadium':'#dffce2','hospital':'#ffe8e8','university':'#ffffe5','school':'#ffffe5','recreation_ground':'#dffce2','beach':'#fff1ba','pier':'#e8e8e8'}
POINT_STYLE={'start':('#1e8e3e','A'),'end':('#d93025','B'),'via':('#f9ab00',''),'poi':('#e8710a',''),'center':('#1a73e8','')}
NAME_RE=re.compile(r'^[A-Za-z0-9_-]{1,64}$')
MAX_SVG=900000

def _feats(x):
    if isinstance(x,list):fs=x
    elif x.get('type')=='FeatureCollection':fs=x.get('features',[])
    elif x.get('type')=='Feature':fs=[x]
    else:fs=[{'type':'Feature','properties':{},'geometry':x}]
    out=[]
    for f in fs:
        if f.get('type')=='FeatureCollection':out+=_feats(f);continue
        if not isinstance(f,dict) or f.get('type')!='Feature' or not isinstance(f.get('geometry'),dict):raise ValueError('features must be GeoJSON Feature objects')
        out.append(f)
    return out

def _positions(g):
    t=g.get('type');c=g.get('coordinates')
    if t=='Point':return [c]
    if t in ('MultiPoint','LineString'):return c
    if t in ('MultiLineString','Polygon'):return [q for r in c for q in r]
    if t=='MultiPolygon':return [q for poly in c for r in poly for q in r]
    raise ValueError('unsupported geometry type '+str(t))

def _num(v):
    if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v):raise ValueError('coordinates must be finite numbers')
    return float(v)

def _check(g):
    for q in _positions(g):
        if not isinstance(q,list) or len(q)<2:raise ValueError('position must be [lon, lat]')
        lon=_num(q[0]);lat=_num(q[1])
        if not (-180<=lon<=180 and -85.06<=lat<=85.06):raise ValueError('position out of range (lon -180..180, lat -85.06..85.06)')

def _fmt(v):return ('%.1f'%v).rstrip('0').rstrip('.')

def _path(pts,closed=False):
    return 'M'+' L'.join(_fmt(x)+' '+_fmt(y) for x,y in pts)+(' Z' if closed else '')

def calculate(p):
    op=p['operation']
    if op=='project':
        if 'points' not in p or 'zoom' not in p:raise ValueError('project requires points and zoom')
        z=p['zoom'];out=[px([q['lon'],q['lat']],z) for q in p['points']]
        back=[ll(xy,z) for xy in out]
        return {'operation':op,'zoom':z,'tile_size':SIZE,'branch':'fractional' if _is_float(z) else 'integer-rounded','pixels':out,'lonlat_roundtrip':back}
    if op=='unproject':
        if 'pixels' not in p or 'zoom' not in p:raise ValueError('unproject requires pixels and zoom')
        return {'operation':op,'zoom':p['zoom'],'tile_size':SIZE,'lonlat':[ll(xy,p['zoom']) for xy in p['pixels']]}
    if 'points' in p or 'pixels' in p or 'zoom' in p:raise ValueError('render takes features/bbox, not points, pixels or zoom')
    W=p.get('width',900);H=p.get('height',650);pad=p.get('padding',40);title=p.get('title')
    feats=_feats(p.get('features',{'type':'FeatureCollection','features':[]}))
    for f in feats:_check(f['geometry'])
    if len(feats)>2000:raise ValueError('at most 2000 features')
    if 'bbox' in p:
        w,s,e,n=p['bbox']
        if not (w<e and s<n):raise ValueError('bbox must be [west, south, east, north] with west<east and south<north')
    else:
        pts=[q for f in feats for q in _positions(f['geometry'])]
        if not pts:raise ValueError('give features or a bbox')
        w=min(q[0] for q in pts);e=max(q[0] for q in pts);s=min(q[1] for q in pts);n=max(q[1] for q in pts)
    if e-w<0.002:c=(w+e)/2;w,e=c-0.001,c+0.001
    if n-s<0.0015:c=(s+n)/2;s,n=c-0.00075,c+0.00075
    if not (w<e and s<n):raise ValueError('bbox must be [west, south, east, north] with west<east and south<north')
    top=38 if title else 0
    a0=px([w,n],0.5);b0=px([e,s],0.5)
    zoom=0.5+min(math.log2((W-2*pad)/(b0[0]-a0[0])),math.log2((H-2*pad-top)/(b0[1]-a0[1])))
    zoom=min(zoom,19.5)
    if not _is_float(zoom):zoom+=1e-9
    tl=px([w,n],zoom);br=px([e,s],zoom)
    ox=(W-(br[0]-tl[0]))/2-tl[0];oy=top+(H-top-(br[1]-tl[1]))/2-tl[1]
    def P(c):q=px([c[0],c[1]],zoom);return (q[0]+ox,q[1]+oy)
    vw,vn=ll([-ox,top-oy],zoom);ve,vs=ll([W-ox,H-oy],zoom)
    view=[vw,vs,ve,vn]
    def visible(coords):
        xs=[c[0] for c in coords];ys=[c[1] for c in coords]
        return not (max(xs)<view[0] or min(xs)>view[2] or max(ys)<view[1] or min(ys)>view[3])
    layers=[];attribution=set();basemap_info=None
    if p.get('basemap'):
        roads,ri=mapdata.load_layer(p['basemap'],'roads')
        try:areas,ai=mapdata.load_layer(p['basemap'],'areas')
        except ValueError:areas,ai=[],{}
        for i in (ri,ai):
            if i.get('attribution'):attribution.add(i['attribution'])
        vis=[f for f in roads if (f.get('geometry') or {}).get('type')=='LineString' and visible(f['geometry']['coordinates'])]
        drop_minor=len(vis)>3500
        if drop_minor:vis=[f for f in vis if f['properties'].get('highway') not in MINOR]
        g=['<g id="basemap-areas">']
        for f in areas:
            gm=f.get('geometry') or {};cat=(f.get('properties') or {}).get('category')
            if gm.get('type')=='Polygon' and visible(gm['coordinates'][0]):
                d=' '.join(_path(simplify([P(c) for c in r],0.7),True) for r in gm['coordinates'])
                g.append('<path d="%s" fill="%s" fill-rule="evenodd" stroke="none"/>'%(d,AREA_FILL.get(cat,'#e8e8e8')))
            elif gm.get('type')=='LineString' and cat=='coastline' and visible(gm['coordinates']):
                g.append('<path d="%s" fill="none" stroke="#6fa8dc" stroke-width="2"/>'%_path(simplify([P(c) for c in gm['coordinates']],0.7)))
        g.append('</g>')
        order=sorted(vis,key=lambda f:-ROAD_STYLE.get(f['properties'].get('highway'),(1,''))[0])
        cas=['<g id="basemap-road-casing" stroke="#bbbbbb" fill="none" stroke-linecap="round" stroke-linejoin="round">'];top_=['<g id="basemap-roads" fill="none" stroke-linecap="round" stroke-linejoin="round">']
        for f in reversed(order):
            hw=f['properties'].get('highway');wd,col=ROAD_STYLE.get(hw,(1,'#ffffff'))
            d=_path(simplify([P(c) for c in f['geometry']['coordinates']],0.7))
            if hw not in MINOR:cas.append('<path d="%s" stroke-width="%s"/>'%(d,_fmt(wd+1.2)))
            dash=' stroke-dasharray="2 2"' if hw in ('footway','path','steps','cycleway','track') else ''
            top_.append('<path d="%s" stroke="%s" stroke-width="%s"%s/>'%(d,col,_fmt(wd),dash))
        cas.append('</g>');top_.append('</g>')
        layers+=g+cas+top_
        basemap_info={'dataset':p['basemap'],'roads_drawn':len(vis),'minor_roads_dropped':drop_minor}
    polys=[];lines=[];points=[];labels=[]
    for f in feats:
        g=f['geometry'];pr=f.get('properties') or {};t=g['type'];kind=pr.get('kind')
        if pr.get('attribution'):attribution.add(str(pr['attribution']))
        if t in ('Polygon','MultiPolygon'):
            fill=pr.get('fill','#1a73e8');stroke=pr.get('stroke','#1a73e8')
            for poly in (g['coordinates'] if t=='MultiPolygon' else [g['coordinates']]):
                d=' '.join(_path([P(c) for c in r],True) for r in poly)
                polys.append('<path d="%s" fill="%s" fill-opacity="%s" fill-rule="evenodd" stroke="%s" stroke-width="2"/>'%(d,escape(str(fill)),_fmt(float(pr.get('fill-opacity',0.2))),escape(str(stroke))))
        elif t in ('LineString','MultiLineString'):
            parts=g['coordinates'] if t=='MultiLineString' else [g['coordinates']]
            col=pr.get('stroke','#8e24aa' if kind=='isochrone' else '#1a73e8');wd=float(pr.get('stroke-width',2.5 if kind=='isochrone' else 5))
            d=' '.join(_path(simplify([P(c) for c in part],0.4)) for part in parts if len(part)>=2)
            if not d:continue
            if kind!='isochrone':lines.append('<path d="%s" fill="none" stroke="#ffffff" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>'%(d,_fmt(wd+3)))
            lines.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.95"/>'%(d,escape(str(col)),_fmt(wd)))
        else:
            col,letter=POINT_STYLE.get(kind,('#e8710a',''));col=pr.get('marker-color',col);letter=str(pr.get('marker-symbol',letter))[:2]
            for c in (g['coordinates'] if t=='MultiPoint' else [g['coordinates']]):
                x,y=P(c);r=9 if letter else 6
                points.append('<circle cx="%s" cy="%s" r="%d" fill="%s" stroke="#ffffff" stroke-width="2"/>'%(_fmt(x),_fmt(y),r,escape(str(col))))
                if letter:points.append('<text x="%s" y="%s" font-size="11" font-weight="bold" text-anchor="middle" fill="#ffffff">%s</text>'%(_fmt(x),_fmt(y+4),escape(letter)))
                nm=pr.get('label',pr.get('name'))
                if nm:labels.append('<text x="%s" y="%s" font-size="12" class="lbl">%s</text>'%(_fmt(x+r+3),_fmt(y+4),escape(str(nm)[:60])))
    mpp=math.cos(math.radians((view[1]+view[3])/2))*2*math.pi*A/(SIZE*math.pow(2,zoom))
    nice=[5,10,20,25,50,100,200,250,500,1000,2000,2500,5000,10000,20000,50000,100000]
    sb=max([v for v in nice if v/mpp<=140] or [5]);sbpx=sb/mpp;sbl=('%d km'%(sb//1000)) if sb>=1000 else ('%d m'%sb)
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="DejaVu Sans, Arial, sans-serif">'%(W,H,W,H),
         '<style>.lbl{fill:#202124;paint-order:stroke;stroke:#ffffff;stroke-width:3px;stroke-linejoin:round}</style>',
         '<defs><clipPath id="frame"><rect x="0" y="%d" width="%d" height="%d"/></clipPath></defs>'%(top,W,H-top),
         '<rect width="%d" height="%d" fill="#f2efe9"/>'%(W,H),'<g clip-path="url(#frame)">']+layers+polys+lines+points+labels+['</g>']
    if title:out.append('<rect width="%d" height="%d" fill="#ffffff"/><text x="12" y="25" font-size="17" font-weight="bold" fill="#202124">%s</text>'%(W,top,escape(str(title)[:120])))
    out.append('<g transform="translate(14,%d)"><rect x="-6" y="-16" width="%s" height="26" fill="#ffffff" fill-opacity="0.85"/><path d="M0 0 h%s" stroke="#202124" stroke-width="3"/><text x="%s" y="-4" font-size="11" fill="#202124">%s</text></g>'%(H-14,_fmt(sbpx+50),_fmt(sbpx),_fmt(sbpx+6),sbl))
    out.append('<g transform="translate(%d,%d)"><path d="M0 -14 L7 6 L0 1 L-7 6 Z" fill="#202124"/><text x="0" y="20" font-size="11" text-anchor="middle" fill="#202124">N</text></g>'%(W-24,top+26))
    if attribution:
        txt=escape(' | '.join(sorted(attribution)))
        out.append('<text x="%d" y="%d" font-size="10" text-anchor="end" class="lbl">%s</text>'%(W-8,H-8,txt))
    out.append('</svg>')
    svg='\n'.join(out)
    if len(svg.encode())>MAX_SVG:raise ValueError('SVG would exceed 900 kB; zoom in (smaller bbox) or omit the basemap')
    fc={'type':'FeatureCollection','features':feats}
    res={'operation':op,'svg':svg,'svg_bytes':len(svg.encode()),'view':{'bbox':[round(v,7) for v in view],'zoom':round(zoom,4),'width':W,'height':H,'meters_per_pixel':round(mpp,3)},
         'feature_count':len(feats),'basemap':basemap_info,'attribution':sorted(attribution),'saved':None}
    if p.get('save_name'):
        nm=p['save_name']
        if not NAME_RE.match(nm):raise ValueError('save_name must be 1-64 letters, digits, _ or -')
        od=os.environ.get('SKILLPACK_MAP_OUTPUT')
        if not od or not Path(od).is_dir():raise ValueError('Saving needs SKILLPACK_MAP_OUTPUT set to an existing folder')
        d=Path(od).resolve();fs=d/(nm+'.svg');fg=d/(nm+'.geojson')
        if fs.exists() or fg.exists():raise ValueError('Refusing to overwrite an existing file: '+nm)
        fs.write_text(svg,encoding='utf-8');fg.write_text(json.dumps(fc,ensure_ascii=False),encoding='utf-8')
        res['saved']={'svg':fs.name,'geojson':fg.name,'folder':'SKILLPACK_MAP_OUTPUT'}
    if p.get('include_geojson',True):res['geojson']=fc
    return res

if __name__=="__main__":
    raise SystemExit(cli(calculate))
