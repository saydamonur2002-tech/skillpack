#!/usr/bin/env python3
"""QUADPACK 21-point Gauss–Kronrod panel and error diagnostics. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli
import math,sys
X=[.995657163025808080735527280689003,.973906528517171720077964012084452,.930157491355708226001207180059508,.865063366688984510732096688423493,.780817726586416897063717578345042,.679409568299024406234327365114874,.562757134668604683339000992726694,.433395394129247190799265943165784,.294392862701460198131126603103866,.148874338981631210884826001129720,0.0]
WG=[.066671344308688137593568809893332,.149451349150580593145776339657697,.219086362515982043995534934228163,.269266719309996355091226921569469,.295524224714752870173892994651338]
WK=[.011694638867371874278064396062192,.032558162307964727478818972459390,.054755896574351996031381300244580,.075039674810919952767043140916190,.093125454583697605535065465083366,.109387158802297641899210590325805,.123491976262065851077958109831074,.134709217311473325928054001771707,.142775938577060080797094273138717,.147739104901338491374841515972068,.149445554002916905664936468398821]

def calculate(p):
    kind=p['function'];a=p['a'];b=p['b']
    def f(x):
        if kind=='polynomial':
            y=0.0
            for c in p['coefficients']:y=y*x+c
        elif kind=='bessel_integrand':y=math.cos(p['order']*x-p['argument']*math.sin(x))/math.pi
        else:y={'sin':math.sin,'cos':math.cos,'exp':math.exp}[kind](x)
        if not math.isfinite(y):raise ValueError('Non-finite integrand')
        return y
    if a==b:return {'value':0.0,'estimated_absolute_error':0.0,'gauss10_value':0.0,'resabs':0.0,'resasc':0.0,'evaluations':0}
    center=.5*(a+b);h=.5*(b-a);dh=abs(h);fc=f(center);resg=0.0;resk=WK[10]*fc;resabs=abs(resk);fv1=[0.0]*10;fv2=[0.0]*10
    for j in list(range(1,10,2))+list(range(0,10,2)):
        absc=h*X[j];v1=f(center-absc);v2=f(center+absc);fv1[j]=v1;fv2[j]=v2;s=v1+v2
        if j%2==1:resg+=WG[j//2]*s
        resk+=WK[j]*s;resabs+=WK[j]*(abs(v1)+abs(v2))
    mean=resk*.5;resasc=WK[10]*abs(fc-mean)
    for j in range(10):resasc+=WK[j]*(abs(fv1[j]-mean)+abs(fv2[j]-mean))
    result=resk*h;resabs*=dh;resasc*=dh;error=abs((resk-resg)*h)
    if resasc!=0 and error!=0:error=resasc*min(1.0,(200*error/resasc)**1.5)
    if resabs>sys.float_info.min/(50*sys.float_info.epsilon):error=max(50*sys.float_info.epsilon*resabs,error)
    return {'value':result,'estimated_absolute_error':error,'gauss10_value':resg*h,'resabs':resabs,'resasc':resasc,'evaluations':21}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
