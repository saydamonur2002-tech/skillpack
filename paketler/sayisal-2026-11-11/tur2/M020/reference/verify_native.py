#!/usr/bin/env python3
"""Rebuild pinned C references locally; no network, Python numerical port or install."""
from pathlib import Path
import ctypes as C,json,subprocess,tempfile,math
ROOT=Path(__file__).resolve().parents[1];ID=json.loads((ROOT/'manifest.json').read_text())['id'];U=ROOT/'upstream';R=ROOT/'reference';D=C.c_double;I=C.c_int;DP=C.POINTER(D)
def compare(a,b,tol):
    if isinstance(b,dict):
        for k,v in b.items():compare(a[k],v,tol)
    elif isinstance(b,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):compare(x,y,tol)
    else:assert abs(a-b)<=tol,(a,b,tol)
with tempfile.TemporaryDirectory(prefix='skillpack-native-') as temporary:
    lib=Path(temporary)/'reference.so'
    if ID=='M011':files=[U/'scipy/optimize/Zeros/brentq.c'];inc=[U/'scipy/optimize/Zeros']
    elif ID in ['M014','M015']:files=[U/('scipy/special/cephes/'+('igam.c' if ID=='M014' else 'incbet.c')),R/'cephes_shim.c'];inc=[R]
    elif ID in ['M016','M017']:files=[U/('lapack-netlib/SRC/'+('dgetf2.c' if ID=='M016' else 'dgtsv.c')),R/'blas_shim.c'];inc=[]
    else:
        names={'M018':['cal2jd'],'M019':['era00','anp'],'M020':['pmat06','pfw06','obl06','fw2m','ir','rx','rz']}[ID]
        files=[U/('src/'+name+'.c') for name in names];inc=[U/'src']
    command=['gcc','-shared','-fPIC','-O2','-ffp-contract=off',*['-I'+str(p) for p in inc],*[str(p) for p in files],'-lm','-o',str(lib)]
    subprocess.run(command,check=True);native=C.CDLL(str(lib))
    CB=C.CFUNCTYPE(D,D,C.c_void_p)
    class Stats(C.Structure):_fields_=[('funcalls',I),('iterations',I),('error_num',I)]
    if ID=='M011':native.brentq.restype=D;native.brentq.argtypes=[CB,D,D,D,D,I,C.c_void_p,C.POINTER(Stats)]
    if ID=='M014':
        for name in ['igam','igamc']:getattr(native,name).restype=D;getattr(native,name).argtypes=[D,D]
    if ID=='M015':native.incbet.restype=D;native.incbet.argtypes=[D,D,D]
    if ID=='M018':native.eraCal2jd.restype=I;native.eraCal2jd.argtypes=[I,I,I,DP,DP]
    if ID=='M019':native.eraEra00.restype=D;native.eraEra00.argtypes=[D,D]
    if ID=='M020':native.eraPmat06.argtypes=[D,D,DP]
    refs=json.loads((ROOT/'tests/references.json').read_text())
    for ref in refs:
        p=ref['input']
        if ID=='M011':
            def fn(x,_):
                y=0.
                for c in p['coefficients']:y=y*x+c
                return y
            callback=CB(fn);stats=Stats();value=native.brentq(callback,p['a'],p['b'],p.get('xtol',2e-12),p.get('rtol',8.881784197001252e-16),p.get('max_iterations',200),None,C.byref(stats));assert stats.error_num==0
            result={'root':value,'iterations':stats.iterations,'evaluations':stats.funcalls}
        elif ID=='M014':result={'P':native.igam(p['shape'],p['x']),'Q':native.igamc(p['shape'],p['x'])}
        elif ID=='M015':result={'I':native.incbet(p['a'],p['b'],p['x'])}
        elif ID=='M016':
            n=len(p['rhs']);nn=I(n);a=(D*(n*n))(*[p['matrix'][i][j] for j in range(n) for i in range(n)]);piv=(I*n)();info=I()
            native.dgetf2_(C.byref(nn),C.byref(nn),a,C.byref(nn),piv,C.byref(info));assert info.value==0
            lu=[[a[i+j*n] for j in range(n)] for i in range(n)];b=p['rhs'][:]
            for i,j in enumerate(piv):b[i],b[j-1]=b[j-1],b[i]
            for i in range(n):
                for j in range(i):b[i]-=lu[i][j]*b[j]
            for i in range(n-1,-1,-1):
                for j in range(i+1,n):b[i]-=lu[i][j]*b[j]
                b[i]/=lu[i][i]
            result={'lu':lu,'pivots_1based':list(piv),'solution':b}
        elif ID=='M017':
            n=len(p['diagonal']);nn=I(n);nrhs=I(1);dl=(D*max(n-1,1))(*p['lower']);d=(D*n)(*p['diagonal']);du=(D*max(n-1,1))(*p['upper']);b=(D*n)(*p['rhs']);info=I()
            native.dgtsv_(C.byref(nn),C.byref(nrhs),dl,d,du,b,C.byref(nn),C.byref(info));assert info.value==0;result={'solution':list(b)}
        elif ID=='M018':
            a=D();b=D();assert native.eraCal2jd(p['year'],p['month'],p['day'],C.byref(a),C.byref(b))==0
            result={'jd_part1':a.value,'jd_part2':b.value,'mjd':b.value,'jd':a.value+b.value}
        elif ID=='M019':result={'angle_rad':native.eraEra00(p['jd1'],p['jd2'])}
        else:
            a=(D*9)();native.eraPmat06(p['jd1'],p['jd2'],a);result={'matrix':[[a[i*3+j] for j in range(3)] for i in range(3)]}
        compare(result,ref['expected_subset'],ref['absolute_tolerance'])
    print(ID+': native reference rerun passed ('+str(len(refs))+' cases)')
