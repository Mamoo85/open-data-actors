"""Refresh data/pricing.json from the live Apify actor pricingInfos. Needs APIFY_TOKEN env or --token-file.
Public-API only: GET /v2/acts?my=true then /v2/acts/{id}. Usage: python scripts/refresh_pricing.py [tokenfile]"""
import json,os,sys,urllib.request,datetime
tf=sys.argv[1] if len(sys.argv)>1 else None
tok=os.environ.get('APIFY_TOKEN') or (open(tf).read().strip().split('=',1)[-1].strip('"\' \n') if tf else '')
H={'Authorization':'Bearer '+tok}
def g(u): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2/'+u,headers=H),timeout=30))['data']
out={'generated':datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec='seconds')+'Z','source':'Apify API actor pricingInfos','actors':[]}
for a in g('acts?my=true&limit=100')['items']:
    d=g('acts/'+a['id'])
    if not d.get('isPublic'): continue
    pi=(d.get('pricingInfos') or [None])[-1]
    row={'slug':d['name'],'username':d['username'],'title':d.get('title') or d['name'],'url':f"https://apify.com/{d['username']}/{d['name']}",'model':None,'events':{},'monthly':None,'trial':None}
    if pi:
        row['model']=pi['pricingModel']
        if pi['pricingModel']=='PAY_PER_EVENT':
            for k,v in pi['pricingPerEvent']['actorChargeEvents'].items():
                if 'eventPriceUsd' in v: row['events'][k]={'title':v.get('eventTitle',k),'usd':v['eventPriceUsd']}
                elif 'eventTieredPricingUsd' in v: row['events'][k]={'title':v.get('eventTitle',k),'tiers':v['eventTieredPricingUsd']}
        elif pi['pricingModel']=='FLAT_PRICE_PER_MONTH': row['monthly']=pi.get('pricePerUnitUsd'); row['trial']=pi.get('trialMinutes')
        elif pi['pricingModel']=='PRICE_PER_DATASET_ITEM': row['events']['result']={'title':'Dataset item','usd':pi.get('pricePerUnitUsd')}
    out['actors'].append(row)
json.dump(out,open(os.path.join(os.path.dirname(__file__),'..','data','pricing.json'),'w'),indent=1)
print(len(out['actors']),'public actors')
