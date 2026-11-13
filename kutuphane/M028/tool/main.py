#!/usr/bin/env python3
"""Destination point, bearing, midpoint and cross-track distance on a sphere. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math
R_DEFAULT=6371e3

def to_rad(x):return x*math.pi/180
def to_deg(x):return x*180/math.pi

def _jsmod(a,n):return math.fmod(a,n)

def wrap90(d):
    if -90<=d<=90:return d
    x=d;a=90;p=360
    return 4*a/p*abs(_jsmod(_jsmod(x-p/4,p)+p,p)-p/2)-a

def wrap180(d):
    if -180<=d<=180:return d
    x=d;a=180;p=360
    return _jsmod(_jsmod(2*a*x/p-p/2,p)+p,p)-a

def wrap360(d):
    if 0<=d<360:return d
    x=d;a=180;p=360
    return _jsmod(_jsmod(2*a*x/p,p)+p,p)

def distance(lat1,lon1,lat2,lon2,R):
    f1=to_rad(lat1);l1=to_rad(lon1);f2=to_rad(lat2);l2=to_rad(lon2);df=f2-f1;dl=l2-l1
    a=math.sin(df/2)*math.sin(df/2)+math.cos(f1)*math.cos(f2)*math.sin(dl/2)*math.sin(dl/2)
    return R*(2*math.atan2(math.sqrt(a),math.sqrt(1-a)))

EPS=2.220446049250313e-16
def equals(a1,o1,a2,o2):return abs(a1-a2)<=EPS and abs(o1-o2)<=EPS

def initial_bearing(lat1,lon1,lat2,lon2):
    if equals(lat1,lon1,lat2,lon2):return None
    f1=to_rad(lat1);f2=to_rad(lat2);dl=to_rad(lon2-lon1)
    x=math.cos(f1)*math.sin(f2)-math.sin(f1)*math.cos(f2)*math.cos(dl);y=math.sin(dl)*math.cos(f2)
    return wrap360(to_deg(math.atan2(y,x)))

def final_bearing(lat1,lon1,lat2,lon2):
    b=initial_bearing(lat2,lon2,lat1,lon1)
    return None if b is None else wrap360(b+180)

def midpoint(lat1,lon1,lat2,lon2):
    f1=to_rad(lat1);l1=to_rad(lon1);f2=to_rad(lat2);dl=to_rad(lon2-lon1)
    A=(math.cos(f1),0,math.sin(f1));B=(math.cos(f2)*math.cos(dl),math.cos(f2)*math.sin(dl),math.sin(f2))
    C=(A[0]+B[0],A[1]+B[1],A[2]+B[2])
    fm=math.atan2(C[2],math.sqrt(C[0]*C[0]+C[1]*C[1]));lm=l1+math.atan2(C[1],C[0])
    return wrap90(to_deg(fm)),wrap180(to_deg(lm))

def destination(lat,lon,dist,brng,R):
    d=dist/R;t=to_rad(brng);f1=to_rad(lat);l1=to_rad(lon)
    s2=math.sin(f1)*math.cos(d)+math.cos(f1)*math.sin(d)*math.cos(t);f2=math.asin(s2)
    y=math.sin(t)*math.sin(d)*math.cos(f1);x=math.cos(d)-math.sin(f1)*s2;l2=l1+math.atan2(y,x)
    return wrap90(to_deg(f2)),wrap180(to_deg(l2))

def cross_track(lat,lon,s_lat,s_lon,e_lat,e_lon,R):
    if equals(lat,lon,s_lat,s_lon):return 0
    d13=distance(s_lat,s_lon,lat,lon,R)/R;t13=to_rad(initial_bearing(s_lat,s_lon,lat,lon));t12=to_rad(initial_bearing(s_lat,s_lon,e_lat,e_lon))
    return math.asin(math.sin(d13)*math.sin(t13-t12))*R

POINTS16=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
TR16=['K','KKD','KD','DKD','D','DGD','GD','GGD','G','GGB','GB','BGB','B','BKB','KB','KKB']
def compass(b):
    if b is None:return None
    i=int(math.floor(b/22.5+0.5))%16
    return {'en':POINTS16[i],'tr':TR16[i]}

def calculate(p):
    op=p['operation'];R=p.get('radius_m',R_DEFAULT);a=p['from'];la=a['lat'];lo=a['lon']
    if op=='destination':
        if 'distance_m' not in p or 'bearing_deg' not in p or 'to' in p:raise ValueError('destination requires from, distance_m and bearing_deg')
        lat,lon=destination(la,lo,p['distance_m'],p['bearing_deg'],R);return {'operation':op,'lat':lat,'lon':lon}
    if 'to' not in p or 'distance_m' in p or 'bearing_deg' in p:raise ValueError(op+' requires from and to')
    b=p['to'];lb=b['lat'];ob=b['lon']
    if op=='bearing':
        ib=initial_bearing(la,lo,lb,ob);fb=final_bearing(la,lo,lb,ob)
        return {'operation':op,'initial_bearing_deg':ib,'final_bearing_deg':fb,'compass':compass(ib),'note':'null for coincident points'}
    if op=='midpoint':
        lat,lon=midpoint(la,lo,lb,ob);return {'operation':op,'lat':lat,'lon':lon}
    if op=='distance':
        return {'operation':op,'distance_m':distance(la,lo,lb,ob,R),'model':'sphere, haversine'}
    if 'point' not in p:raise ValueError('cross_track requires point, from and to')
    q=p['point']
    return {'operation':op,'cross_track_m':cross_track(q['lat'],q['lon'],la,lo,lb,ob,R),'note':'negative = left of the path from->to'}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
