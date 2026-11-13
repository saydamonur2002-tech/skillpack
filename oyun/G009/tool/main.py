#!/usr/bin/env python3
"""Wallet, shop catalog and inventory ledger with integer money. Original work, MIT."""
from runtime import cli
import copy
CATALOG={'repair_kit':{'price':150,'sell':60,'max':3,'stored':True,'effect':'repair vehicle +50'},
         'snack':{'price':20,'sell':0,'max':5,'stored':True,'effect':'health +25'},
         'fuel_can':{'price':40,'sell':10,'max':2,'stored':True,'effect':'refuel'},
         'paint_job':{'price':500,'sell':0,'max':0,'stored':False,'effect':'clear wanted level (paint shop, see G007)'},
         'package':{'price':0,'sell':0,'max':1,'stored':True,'effect':'mission item'}}
MAX_MONEY=10**9
def calculate(p):
    cat=copy.deepcopy(CATALOG);cat.update(p.get('catalog',{}))
    if p['operation']=='catalog':return {'operation':'catalog','catalog':cat,'currency':'game dollars (integer)'}
    money=p.get('wallet',{}).get('money',0);inv={k:v for k,v in p.get('inventory',{}).items() if v}
    for k,v in inv.items():
        if k not in cat:raise ValueError('inventory has an item that is not in the catalog')
    mode=p.get('mode','per_transaction');ledger=[]
    start=(money,dict(inv))
    for n,t in enumerate(p['transactions']):
        ty=t['type'];it=t.get('item');q=t.get('qty',1);why=None;delta=0
        if ty in('buy','sell','pickup','use','drop') and it not in cat:why='unknown item'
        elif ty=='earn':delta=t.get('amount',0)
        elif ty=='spend':
            delta=-t.get('amount',0)
            if money+delta<0:why='insufficient money'
        elif ty=='buy':
            c=cat[it];delta=-c['price']*q
            if money+delta<0:why='insufficient money'
            elif c['stored'] and inv.get(it,0)+q>c['max']:why='inventory limit'
        elif ty=='sell':
            c=cat[it];delta=c['sell']*q
            if not c['stored'] or inv.get(it,0)<q:why='not enough items'
            elif c['sell']<=0:why='item cannot be sold'
        elif ty=='pickup':
            if inv.get(it,0)+q>cat[it]['max']:why='inventory limit'
        elif ty in('use','drop'):
            if inv.get(it,0)<q:why='not enough items'
        if why is None and money+delta>MAX_MONEY:why='money limit'
        if why:
            ledger.append({'index':n,'type':ty,'status':'rejected','reason':why,'balance_after':money})
            if mode=='all_or_nothing':
                return {'operation':'apply','committed':False,'money':start[0],'inventory':start[1],'ledger':ledger,'rejected':1,'effects':[]}
            continue
        money+=delta
        if ty in('buy','pickup') and cat[it]['stored']:inv[it]=inv.get(it,0)+q
        if ty in('sell','use','drop'):inv[it]-=q
        e={'index':n,'type':ty,'status':'applied','delta':delta,'balance_after':money}
        if it:e['item']=it;e['qty']=q
        if ty in('use',) or (ty=='buy' and not cat[it]['stored']):e['effect']=cat[it]['effect']
        if t.get('reason'):e['reason']=t['reason']
        ledger.append(e)
    inv={k:v for k,v in sorted(inv.items()) if v}
    return {'operation':'apply','committed':True,'money':money,'inventory':inv,'ledger':ledger,'rejected':sum(1 for l in ledger if l['status']=='rejected'),
            'effects':[l['effect'] for l in ledger if 'effect' in l]}
if __name__=='__main__':raise SystemExit(cli(calculate))
