"""Week 6: reproducible executive evidence pack combining Weeks 1–5.

Aggregations are evidence-backed. Scenario business recommendations are proposed
experiments, NOT causal claims or observed changes in store performance.
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def _json(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def wape(actual,pred):
    a=np.asarray(actual,dtype=float);p=np.asarray(pred,dtype=float)
    if len(a)!=len(p) or not len(a) or np.isnan(a).any() or np.isnan(p).any() or a.sum()<=0:
        raise ValueError('WAPE requires same-length finite arrays and positive actual total')
    return 100*float(np.abs(a-p).sum())/float(a.sum())


def create_brief(root:Path)->dict:
    root=Path(root);refs=root/'data/reference';out=root/'outputs';assets=root/'assets'
    out.mkdir(parents=True,exist_ok=True);assets.mkdir(parents=True,exist_ok=True)
    w1=_json(refs/'week1_external_indicators.json')
    w2c=_json(refs/'week2_real_catalog_audit.json')
    w2=_json(refs/'week2_quality_audit.json')
    w3=_json(refs/'week3_eda_findings.json')
    w4=_json(refs/'week4_forecast_findings.json')
    hold=pd.read_csv(refs/'untouched_2026_holdout.csv',parse_dates=['date'])
    score=pd.read_csv(refs/'model_scorecard_overall.csv')
    fred=pd.read_csv(root/'data/raw/fred_clothing_store_sales_2019_2026_08.csv',parse_dates=['date'])
    if len(fred)!=92 or len(hold)!=8:raise ValueError('Historical and test period unexpected: check source provenance')
    if not (hold.date.max()==pd.Timestamp('2026-08-01') and hold.date.min()==pd.Timestamp('2026-01-01')):raise ValueError('Holdout dates shifted')
    chosen=wape(hold.actual_usd_million,hold.selected_model_forecast)
    baseline=wape(hold.actual_usd_million,hold.seasonal_naive_forecast)
    bias=float((hold.selected_model_forecast-hold.actual_usd_million).mean())
    peak_idx=(hold.actual_usd_million-hold.selected_model_forecast).abs().idxmax()
    dom=fred[fred.date.dt.year.between(2021,2025)]
    dec=float(dom.loc[dom.date.dt.month.eq(12),'clothing_stores_usd_million'].median())
    feb=float(dom.loc[dom.date.dt.month.eq(2),'clothing_stores_usd_million'].median())
    season=round(dec/feb,2)
    rows=[
      {'week':'1','evidence':'India public internet access / urban share','observed':f"Internet use {w1['internet_users_pct_2020']}% to {w1['internet_users_pct_2025']}% (2020–2025)", 'decision':'Explore digital-reach pilot; do not infer apparel conversion','validation':'Local consented channel conversion A/B test','caveat':'Macro correlation is not fashion sales'},
      {'week':'2','evidence':'Public fashion catalog integrity','observed':f"{w2c['input_collections']} collections; {w2c['missing_collection_images']} missing images, {w2c['missing_seo_descriptions']} missing SEO summaries", 'decision':'Create catalog completeness SLA and review counts','validation':'Monthly media coverage / exception-resolution rates','caveat':'Overlapping collection counts not unique products'},
      {'week':'2/5','evidence':'Synthetic apparel transaction stress test','observed':f"{w2['raw_rows']} input, {w2['clean_sales_rows']} sales, {w2['clean_returns_rows']} returns, {w2['quarantined_rows']} quarantine",'decision':'Block invalid financial rows; separate returns','validation':'100% reconciled rows; zero accepted duplicate line ids','caveat':'Synthetic fixture, not actual business transactions'},
      {'week':'3','evidence':'U.S. Census clothing-store monthly sales','observed':f"{w3['n_months']} months; Dec/Feb seasonal median {season:.2f}x",'decision':'Test seasonality as a planning prior, not as local reorder quantity','validation':'Local same-month unit-sales comparison over >=2 years','caveat':'National USD values not SKU-level units'},
      {'week':'4','evidence':'Forecast holdout and model comparison','observed':f"WAPE {chosen:.2f}% selected vs {baseline:.2f}% naive (eight 2026 months)",'decision':'Pilot forecasts with monitoring before any automated buying','validation':'Repeat rolling-origin holdouts, bias, and by-category WAPE','caveat':'Short holdout; potential revisions/drift'},
    ]
    pd.DataFrame(rows).to_csv(out/'evidence_to_action_matrix.csv',index=False)
    priorities=[
      {'rank':1,'initiative':'Deploy schema and duplicate gates','owner':'Data analyst + data steward','metric':'Accepted rows valid / unique','target':'100% critical checks; 0 duplicate accepted keys','timeframe':'Weeks 1–2','go_no_go':'No release if reconciliation fails'},
      {'rank':2,'initiative':'Remediate missing catalog images/SEO','owner':'Merchandising catalog owner','metric':'Missing image URLs and SEO summaries','target':'Resolve 3 image and 1 SEO exceptions from snapshot','timeframe':'Weeks 2–3','go_no_go':'Human sign-off; do not invent assets'},
      {'rank':3,'initiative':'Trial season-aware forecasts','owner':'Demand planning + analyst','metric':'Holdout WAPE and bias vs seasonal naive','target':'Show repeated improvement across category/time tests','timeframe':'Weeks 3–5','go_no_go':'Do not automate replenishment on national aggregate'},
      {'rank':4,'initiative':'Consent-based digital pilot','owner':'Marketing + privacy lead','metric':'Incremental contribution per exposed group','target':'Pre-register and evaluate lift against holdout','timeframe':'Weeks 4–6','go_no_go':'No personalized targeting without lawful basis'},
    ]
    pd.DataFrame(priorities).to_csv(out/'prioritized_decision_plan.csv',index=False)
    model_scores=pd.DataFrame([
        {'model':'Selected seasonal trend','holdout_wape_pct':round(chosen,2),'mean_signed_error_usd_million':round(bias,2),'n_holdout':len(hold)},
        {'model':'Seasonal naive','holdout_wape_pct':round(baseline,2),'mean_signed_error_usd_million':round(float((hold.seasonal_naive_forecast-hold.actual_usd_million).mean()),2),'n_holdout':len(hold)}
    ])
    model_scores.to_csv(out/'recomputed_holdout_metrics.csv',index=False)
    findings={
      'scope':'Final synthesis of previously prepared demonstrations and frozen public datasets; no private employer data',
      'week1_observed_internet_access_increase_pp':round(w1['internet_users_pct_2025']-w1['internet_users_pct_2020'],2),
      'week2_real_catalog_missing_images':w2c['missing_collection_images'],
      'week2_synthetic_reconciliation_pct':round(100*(w2['clean_sales_rows']+w2['clean_returns_rows']+w2['quarantined_rows'])/w2['raw_rows'],2),
      'week3_clothing_months':len(fred),
      'week3_dec_to_feb_ratio':season,
      'week4_selected_backtest_wape_pct':w4['backtest_WAPE_pct'],
      'week4_holdout_wape_pct':round(chosen,2),
      'week4_seasonal_naive_holdout_wape_pct':round(baseline,2),
      'week4_holdout_improvement_pp':round(baseline-chosen,2),
      'week4_holdout_mean_signed_error_usd_million':round(bias,2),
      'week4_largest_holdout_absolute_error_usd_million':round(float(abs(hold.loc[peak_idx,'actual_usd_million']-hold.loc[peak_idx,'selected_model_forecast'])),1),
      'week4_largest_holdout_error_month':hold.loc[peak_idx,'date'].strftime('%Y-%m'),
      'distinction':'Observed values and historical model tests are evidence; scenario interventions are unmeasured proposals.',
      'scope_limitation':'U.S. national store sales cannot measure India store-level units, margins, conversion, or causal effects.'
    }
    (out/'executive_findings.json').write_text(json.dumps(findings,indent=2),encoding='utf-8')
    # Reports deliberately separate observed and scenario information.
    plt.figure(figsize=(9.5,3.6))
    plt.plot(fred.date,fred.clothing_stores_usd_million,color='#1A6075',linewidth=1.45)
    plt.axvspan(pd.Timestamp('2020-03-01'),pd.Timestamp('2020-06-01'),color='#DEA073',alpha=.25,label='Pandemic shock window')
    plt.title('Evidence: observed clothing-store sales (U.S., not seasonally adjusted)')
    plt.ylabel('Nominal USD millions');plt.legend(frameon=False);plt.tight_layout()
    plt.savefig(assets/'01_observed_market_series.png',dpi=180);plt.close()
    plt.figure(figsize=(9.5,3.6));plt.plot(hold.date,hold.actual_usd_million,marker='o',color='#1B566E',label='Observed 2026')
    plt.plot(hold.date,hold.selected_model_forecast,marker='s',linestyle='--',color='#9A6239',label='Selected model (out-of-sample)')
    plt.plot(hold.date,hold.seasonal_naive_forecast,linestyle=':',color='#9FABB3',label='Seasonal naive')
    plt.title('Evidence: untouched eight-month holdout, not forward predictions');plt.ylabel('USD millions');plt.legend(frameon=False)
    plt.xticks(rotation=25);plt.tight_layout();plt.savefig(assets/'02_holdout_comparison.png',dpi=180);plt.close()
    plt.figure(figsize=(7.5,3.6));b=plt.barh(['Selected seasonal trend','Seasonal naive'],[chosen,baseline],color=['#1B6574','#9FABB3'])
    for bar in b:plt.text(bar.get_width()+.08,bar.get_y()+bar.get_height()/2,f'{bar.get_width():.2f}%',va='center')
    plt.xlabel('WAPE (%) — lower is better');plt.title('Measured forecast accuracy on Jan–Aug 2026')
    plt.xlim(0,7);plt.tight_layout();plt.savefig(assets/'03_measured_model_accuracy.png',dpi=180);plt.close()
    plt.figure(figsize=(9.8,3.8));labels=['Product data quality','Seasonality validation','Forecast pilot','Consent-based marketing'];phase=[1,2,3,4]
    for y,(label,n) in enumerate(zip(labels,phase)):plt.barh(y,n,left=0,color=['#1C6B79','#557D8F','#B7804F','#799A88'][y],alpha=.85)
    plt.yticks(range(len(labels)),labels);plt.xlabel('Priority order (not predicted financial benefit)');plt.title('Action plan prioritizes auditability before automation');plt.xlim(0,5);plt.tight_layout()
    plt.savefig(assets/'04_action_sequence.png',dpi=180);plt.close()
    return findings

if __name__=='__main__':
    print(json.dumps(create_brief(Path(__file__).resolve().parents[1]),indent=2))
