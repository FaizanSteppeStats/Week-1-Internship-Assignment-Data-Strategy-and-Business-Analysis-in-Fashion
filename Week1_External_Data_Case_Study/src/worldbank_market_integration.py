"""Reproducible real external-data join plus an explicitly assumed fashion marketing scenario.

World Bank indicator data: https://api.worldbank.org/v2/country/IND/indicator/IT.NET.USER.ZS?format=json
and https://api.worldbank.org/v2/country/IND/indicator/SP.URB.TOTL.IN.ZS?format=json

Run without network with audited snapshot. Use --refresh to download fresh indicators.

WARNING: No fashion sales or business causal effect are inferred from these national statistics.
"""
import argparse
import json
from pathlib import Path
from urllib.request import urlopen, Request

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

INDICATORS = {
    'IT.NET.USER.ZS': 'internet_users_pct',
    'SP.URB.TOTL.IN.ZS': 'urban_population_pct',
}


def fetch_worldbank_india(year_start=2020, year_end=2025):
    """Read first API page for 2020-25; explicit country, year and indicator identifiers."""
    rows=[]
    for code in INDICATORS:
        url = f'https://api.worldbank.org/v2/country/IND/indicator/{code}?format=json&date={year_start}:{year_end}&per_page=100'
        req=Request(url, headers={'User-Agent':'Fashion-Data-Strategy-Educational/1.0'})
        with urlopen(req, timeout=30) as response:
            meta, observations=json.load(response)
        if meta.get('pages',1)!=1:
            raise ValueError('Unexpected API pagination; review download before proceeding')
        for item in observations:
            rows.append({'country':item['countryiso3code'], 'year':int(item['date']),
                         'indicator_code':code,'indicator_name':item['indicator']['value'],
                         'value_pct':item['value'], 'source_url':url,
                         'source_lastupdated':meta.get('lastupdated','unavailable')})
    return pd.DataFrame(rows)


def integrate(df):
    """Clean, validate, align two independently sourced indicators by (country, year)."""
    needed={'country','year','indicator_code','value_pct'}
    if not needed.issubset(df.columns):
        raise ValueError(f'Missing fields: {needed - set(df.columns)}')
    x=df.copy()
    x['country']=x['country'].astype(str).str.strip().str.upper()
    x['year']=pd.to_numeric(x['year'],errors='raise').astype(int)
    x['value_pct']=pd.to_numeric(x['value_pct'],errors='coerce')
    x=x.loc[(x['country']=='IND')&(x['year'].between(2020,2025))]
    x=x.loc[x['indicator_code'].isin(INDICATORS)]
    if x[['country','year','indicator_code']].duplicated().any():
        raise ValueError('Duplicate country-year-indicator key')
    if x['value_pct'].isna().any() or not x['value_pct'].between(0,100).all():
        raise ValueError('Missing or impossible percentage values; quarantine not impute')
    wide=x.pivot(index=['country','year'],columns='indicator_code',values='value_pct').reset_index()
    wide=wide.rename(columns=INDICATORS).sort_values('year')
    if len(wide)!=6 or wide[list(INDICATORS.values())].isna().any().any():
        raise ValueError('Unmatched or missing year(s); cannot do a complete inner join')
    wide.columns.name=None
    return wide


def make_outputs(root, refresh=False):
    root=Path(root)
    snapshot=root/'data/external/worldbank_india_2020_2025.csv'
    if refresh:
        fetched=fetch_worldbank_india()
        fetched.to_csv(snapshot,index=False)
    raw=pd.read_csv(snapshot)
    clean=integrate(raw)
    out=root/'outputs'; out.mkdir(exist_ok=True,parents=True)
    clean.to_csv(out/'joined_india_external_market_indicators.csv',index=False,float_format='%.8f')
    s=clean.set_index('year')
    metrics={
        'data_provenance': 'OBSERVED World Bank indicators, not synthetic fashion transactions',
        'country':'India','period':'2020-2025','years_joined':int(len(clean)),
        'internet_users_pct_2020':round(float(s.loc[2020,'internet_users_pct']),2),
        'internet_users_pct_2025':round(float(s.loc[2025,'internet_users_pct']),2),
        'internet_change_percentage_points':round(float(s.loc[2025,'internet_users_pct']-s.loc[2020,'internet_users_pct']),2),
        'urban_population_pct_2020':round(float(s.loc[2020,'urban_population_pct']),2),
        'urban_population_pct_2025':round(float(s.loc[2025,'urban_population_pct']),2),
        'urban_change_percentage_points':round(float(s.loc[2025,'urban_population_pct']-s.loc[2020,'urban_population_pct']),2),
    }
    # Marketing calculation uses Assumptions, not data-derived results.
    assumptions={'ad_impressions':20000,'ctr':0.025,'conversion_rate':0.04,
                 'order_value_inr':1800,'advertising_cost_inr':12000}
    clicks=int(assumptions['ad_impressions']*assumptions['ctr'])
    orders=int(clicks*assumptions['conversion_rate'])
    revenue=orders*assumptions['order_value_inr']
    scenario={'type':'ILLUSTRATIVE ASSUMPTIONS - NOT MEASURED',**assumptions,'clicks':clicks,
              'orders':orders,'revenue_inr':revenue,'roas':round(revenue/assumptions['advertising_cost_inr'],2)}
    (out/'external_case_findings.json').write_text(json.dumps({'observed_external_indicators':metrics,'hypothetical_fashion_scenario':scenario},indent=2),encoding='utf-8')
    fig,ax=plt.subplots(figsize=(9,4.5))
    ax.plot(clean.year,clean.internet_users_pct,marker='o',linewidth=2.2,label='Internet users (% population)')
    ax.plot(clean.year,clean.urban_population_pct,marker='s',linewidth=2.2,label='Urban population (% population)')
    ax.set_xlabel('Year');ax.set_ylabel('Share of Indian population (%)');ax.set_ylim(25,75)
    ax.set_xticks(clean.year);ax.set_title('India: two observed public indicators, joined by year (World Bank)')
    ax.legend(frameon=False,loc='upper left');ax.spines[['top','right']].set_visible(False)
    fig.tight_layout();fig.savefig(out/'worldbank_india_2020_2025.png',dpi=160);plt.close(fig)
    return metrics, scenario

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--refresh',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    observed,illustration=make_outputs(root,refresh=args.refresh)
    print(json.dumps({'observed':observed,'illustrative':illustration},indent=2))
