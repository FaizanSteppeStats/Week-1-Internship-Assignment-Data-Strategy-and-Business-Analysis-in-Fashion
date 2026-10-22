"""Optional online acquisition of a licensed public World Bank textile indicator.

Actual retrieval requires internet access; project still runs fully offline.
Source: https://data.worldbank.org/indicator/NV.MNF.TXTL.ZS.UN
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request
import pandas as pd

INDICATOR='NV.MNF.TXTL.ZS.UN'
BASE='https://api.worldbank.org/v2/country/IND/indicator/'+INDICATOR

def fetch(out_dir:Path,year_start:int=2000,year_end:int=2023):
    out_dir=Path(out_dir);out_dir.mkdir(parents=True,exist_ok=True)
    query=urllib.parse.urlencode({'format':'json','date':f'{year_start}:{year_end}','per_page':1000})
    url=BASE+'?'+query
    req=urllib.request.Request(url,headers={'User-Agent':'Fashion-Week2-Teaching-Project/1.0'})
    with urllib.request.urlopen(req,timeout=30) as response:raw=response.read()
    data=json.loads(raw)
    if not isinstance(data,list) or len(data)!=2:raise ValueError('Unexpected World Bank response structure')
    metadata,records=data
    if int(metadata.get('pages',1))!=1:raise ValueError('More than one page; increase page size or paginate')
    (out_dir/'india_textiles_worldbank_raw.json').write_bytes(raw)
    rows=[]
    for v in records:
        rows.append({'country':v.get('country',{}).get('value'), 'year':v.get('date'),
            'value_pct_mfg':v.get('value'),'indicator':v.get('indicator',{}).get('id')})
    df=pd.DataFrame(rows);df.to_csv(out_dir/'india_textiles_worldbank.csv',index=False)
    audit={'source_url':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),
        'raw_sha256':hashlib.sha256(raw).hexdigest(),'records':len(df),
        'nonnull_values':int(df.value_pct_mfg.notna().sum()),
        'source_label':'World Bank WDI: textiles and clothing share in manufacturing value added',
        'license_note':'Check source attribution requirements; World Bank indicator page lists CC BY 4.0',
        'limitation':'Macro indicator, not daily fashion sales or consumer-level observations'}
    (out_dir/'india_textiles_worldbank_provenance.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    return audit

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('data/external'))
    a=p.parse_args();print(json.dumps(fetch(a.out),indent=2))
