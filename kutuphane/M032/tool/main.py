#!/usr/bin/env python3
"""Offline place search (geocode) and reverse geocode on a local places file. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
# --- Jaro-Winkler port (jamesturk/jellyfish _jellyfish.py, MIT); see M023 for the standalone pack ---
def _jaro_winkler(s1,s2,long_tolerance,winklerize):
    s1_len=len(s1);s2_len=len(s2)
    stats={'matches':0,'transpositions':0,'prefix_length':0,'long_tolerance_applied':False}
    if not s1_len or not s2_len:return 0.0,stats
    min_len=min(s1_len,s2_len);search_range=max(s1_len,s2_len)//2-1
    if search_range<0:search_range=0
    s1_flags=[False]*s1_len;s2_flags=[False]*s2_len;common=0
    for i,ch in enumerate(s1):
        low=max(0,i-search_range);hi=min(i+search_range,s2_len-1)
        for j in range(low,hi+1):
            if not s2_flags[j] and s2[j]==ch:
                s1_flags[i]=s2_flags[j]=True;common+=1;break
    stats['matches']=common
    if not common:return 0.0,stats
    k=trans=0
    for i,f in enumerate(s1_flags):
        if f:
            for j in range(k,s2_len):
                if s2_flags[j]:k=j+1;break
            if s1[i]!=s2[j]:trans+=1
    trans//=2;stats['transpositions']=trans
    c=float(common)
    weight=(c/s1_len+c/s2_len+(c-trans)/c)/3
    if winklerize and weight>0.7:
        j=min(min_len,4);i=0
        while i<j and s1[i]==s2[i]:i+=1
        stats['prefix_length']=i
        if i:weight+=i*0.1*(1.0-weight)
        if long_tolerance and min_len>4 and c>i+1 and 2*c>=min_len+i:
            weight+=(1.0-weight)*(float(c-i-1)/float(s1_len+s2_len-i*2+2));stats['long_tolerance_applied']=True
    return weight,stats

import unicodedata,re
import mapdata

def jaro_winkler(a,b):return _jaro_winkler(a,b,False,True)[0]

TR=str.maketrans({'İ':'i','I':'ı'})
FOLD=str.maketrans({'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u','â':'a','î':'i','û':'u'})
def normalize(s):
    """Turkish-aware lower case, Turkish letter folding, accents stripped, punctuation to spaces."""
    s=s.translate(TR).lower().translate(FOLD)
    s=''.join(ch for ch in unicodedata.normalize('NFKD',s) if not unicodedata.combining(ch))
    return ' '.join(re.sub(r'[^0-9a-z]+',' ',s).split())

def score(q,name):
    """max(JW(query, name), 0.95 * best JW(query, any window of the name with the query's token count))."""
    s=jaro_winkler(q,name);qt=q.split();nt=name.split();k=len(qt)
    if len(nt)>k:
        w=max(jaro_winkler(q,' '.join(nt[i:i+k])) for i in range(len(nt)-k+1))
        s=max(s,0.95*w)
    return s

PLACE_CATS={'city','town','village','suburb','quarter','neighbourhood','hamlet','locality','square'}

def _rec(p,extra):
    r={'name':p['name'],'category':p['category'],'lat':p['lat'],'lon':p['lon'],'id':p['id']}
    for k in ('addr:street','addr:housenumber','name:en'):
        if k in p['props']:r[k]=p['props'][k]
    r.update(extra);return r

def calculate(p):
    op=p['operation'];pl,info=mapdata.places(p['dataset']);ds={'file':info['file'],'attribution':info['attribution'],'license':info['license'],'records':len(pl)}
    cats,aliases=mapdata.resolve_categories(p.get('categories',[]));cats=set(cats)
    if op=='search':
        if 'query' not in p or 'lat' in p or 'lon' in p:raise ValueError('search requires query (near is optional)')
        q=normalize(p['query'])
        if not q:raise ValueError('query has no letters or digits')
        near=p.get('near');minimum=p.get('min_score',0.85);hits=[]
        for i,x in enumerate(pl):
            if cats and x['category'] not in cats:continue
            s=score(q,normalize(x['name']))
            if s<minimum:continue
            d=mapdata.haversine(near['lat'],near['lon'],x['lat'],x['lon']) if near else None
            hits.append((-s,d if d is not None else 0.0,i,x,s,d))
        hits.sort(key=lambda h:(h[0],h[1],h[2]))
        out=[_rec(x,{'score':round(s,4),**({'distance_m':round(d,1)} if d is not None else {})}) for _,_,_,x,s,d in hits[:p.get('limit',5)]]
        return {'operation':op,'query':p['query'],'normalized_query':q,'matches':out,'match_count':len(hits),'categories_used':aliases,'dataset':ds,
                'note':'Fuzzy name match on a local dataset; several places can share a name. Confirm the right one before routing.'}
    if 'lat' not in p or 'lon' not in p or 'query' in p or 'near' in p:raise ValueError('reverse requires lat and lon only')
    lat=p['lat'];lon=p['lon'];maxd=p.get('max_distance_m',500)
    def nearest(pred):
        best=None
        for i,x in enumerate(pl):
            if not pred(x):continue
            d=mapdata.haversine(lat,lon,x['lat'],x['lon'])
            if d<=maxd and (best is None or (d,i)<(best[0],best[1])):best=(d,i,x)
        return _rec(best[2],{'distance_m':round(best[0],1)}) if best else None
    pois=[]
    for i,x in enumerate(pl):
        if x['category']=='street' or x['category'] in PLACE_CATS or (cats and x['category'] not in cats):continue
        d=mapdata.haversine(lat,lon,x['lat'],x['lon'])
        if d<=maxd:pois.append((d,i,x))
    pois.sort(key=lambda t:(t[0],t[1]))
    return {'operation':op,'point':{'lat':lat,'lon':lon},'street':nearest(lambda x:x['category']=='street'),
            'area':nearest(lambda x:x['category'] in PLACE_CATS),
            'nearby':[_rec(x,{'distance_m':round(d,1)}) for d,i,x in pois[:p.get('limit',5)]],'dataset':ds,
            'note':'Street = nearest representative point of a named street; area = nearest named place point. Not an address-level geocoder.'}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
