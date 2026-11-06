"""Week 4: transparent leakage-free model evaluation for FRED clothing-store sales.
All models predict NOMINAL US USD-million MONTHLY national sales, not retailer SKU demand.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
ROOT=Path(__file__).resolve().parents[1]

def features(idx):
    idx=pd.DatetimeIndex(idx)
    t=(idx.year-2019)*12+(idx.month-1)
    m=idx.month
    return pd.DataFrame({'time_months':t,'sin1':np.sin(2*np.pi*m/12),'cos1':np.cos(2*np.pi*m/12),'sin2':np.sin(4*np.pi*m/12),'cos2':np.cos(4*np.pi*m/12),'is_dec':(m==12).astype(float),'is_jan':(m==1).astype(float)},index=idx)

def train_predict(history,dates,model):
    """Every prediction is from data earlier than first forecast date; full horizon is fixed."""
    history=history.sort_index();dates=pd.DatetimeIndex(dates)
    assert len(history)>24 and dates.min()>history.index.max(), 'temporal leakage or short history'
    y=history.astype(float)
    if model=='seasonal_naive':return pd.Series([float(y.loc[d-pd.DateOffset(years=1)]) for d in dates],index=dates)
    if model=='seasonal_trend':
        vals=[]
        for d in dates:
            base=float(y.loc[d-pd.DateOffset(years=1)])
            prev=float(y.loc[d-pd.DateOffset(years=2)])
            vals.append(max(0,base+0.5*(base-prev)))
        return pd.Series(vals,index=dates)
    if model=='ridge_fourier':
        # Exclude COVID structural shock; fit 2021+ only. Model weights chosen in advance, no tuning on holdout.
        subset=y.loc[y.index>=pd.Timestamp('2021-01-01')]
        reg=make_pipeline(StandardScaler(),Ridge(alpha=50.0))
        reg.fit(features(subset.index),subset.to_numpy())
        return pd.Series(np.maximum(0,reg.predict(features(dates))),index=dates)
    raise ValueError('unknown model')

def wape(y,p):
    y=np.asarray(y,dtype=float);p=np.asarray(p,dtype=float)
    return float(np.abs(y-p).sum()/np.abs(y).sum()*100)

def run(root=ROOT):
    root=Path(root)
    df=pd.read_csv(root/'data/fred_clothing_store_sales_2019_2026_08.csv',parse_dates=['date']).set_index('date').sort_index()
    y=df.clothing_stores_usd_million.astype(float)
    assert len(y)==92 and y.index.max()==pd.Timestamp('2026-08-01')
    models=['seasonal_naive','seasonal_trend','ridge_fourier']
    # Pseudo-out-of-sample expanding folds. Each fold forecasts 12 months at once, avoiding next-month actual peeking.
    folds=[('2024',pd.Timestamp('2024-01-01'),12),('2025',pd.Timestamp('2025-01-01'),12)]
    back=[]
    for label,start,h in folds:
        hist=y.loc[:start-pd.DateOffset(months=1)]
        ix=pd.date_range(start,periods=h,freq='MS')
        for model in models:
            p=train_predict(hist,ix,model)
            for d,pred in p.items():back.append({'fold':label,'date':d,'model':model,'actual_usd_million':float(y[d]),'forecast_usd_million':float(pred),'abs_error':abs(float(y[d])-float(pred))})
    b=pd.DataFrame(back);b.to_csv(root/'outputs/rolling_origin_backtest.csv',index=False)
    tbl=[]
    for (fold,model),d in b.groupby(['fold','model']):
        tbl.append({'fold':fold,'model':model,'WAPE_pct':round(wape(d.actual_usd_million,d.forecast_usd_million),2),'MAE_usd_million':round(float(d.abs_error.mean()),2),'bias_usd_million':round(float((d.forecast_usd_million-d.actual_usd_million).mean()),2)})
    scores=pd.DataFrame(tbl);scores.to_csv(root/'outputs/model_scorecard_by_fold.csv',index=False)
    overall=[]
    for model,d in b.groupby('model'):
        overall.append({'model':model,'WAPE_pct':round(wape(d.actual_usd_million,d.forecast_usd_million),2),'MAE_usd_million':round(float(d.abs_error.mean()),2),'bias_usd_million':round(float((d.forecast_usd_million-d.actual_usd_million).mean()),2)})
    summary=pd.DataFrame(overall).sort_values('WAPE_pct');summary.to_csv(root/'outputs/model_scorecard_overall.csv',index=False)
    winner=summary.iloc[0]['model']
    # untouched holdout 2026 Jan-Aug: winner is chosen ONLY from 2024+2025 backtests.
    hold_ix=pd.date_range('2026-01-01',periods=8,freq='MS')
    hist=y.loc[:'2025-12-01']
    preds=train_predict(hist,hold_ix,winner)
    baseline=train_predict(hist,hold_ix,'seasonal_naive')
    hold=pd.DataFrame({'date':hold_ix,'actual_usd_million':y.reindex(hold_ix).values,'selected_model_forecast':preds.values,'seasonal_naive_forecast':baseline.values})
    hold['selected_absolute_error']=(hold.actual_usd_million-hold.selected_model_forecast).abs()
    hold.to_csv(root/'outputs/untouched_2026_holdout.csv',index=False)
    hold_score=wape(hold.actual_usd_million,hold.selected_model_forecast)
    baseline_hold=wape(hold.actual_usd_million,hold.seasonal_naive_forecast)
    # Scenario only: future Sept 2026–Aug 2027, after latest published observation Aug 2026.
    future_ix=pd.date_range('2026-09-01',periods=12,freq='MS')
    # Seasonal trend requires 2024–25 values; ridge can use all observed 2021 onward. Forecast all 12 months from Aug 2026.
    fut=train_predict(y,future_ix,winner)
    # Conservative descriptive range from holdout absolute percentage errors, no calibrated PI claimed.
    ape=(hold.selected_absolute_error/hold.actual_usd_million).to_numpy()
    margin=max(0.10,float(np.quantile(ape,.80)))
    fut_df=pd.DataFrame({'month':future_ix,'point_forecast_usd_million':fut.values,
        'illustrative_lower_not_95pi':np.maximum(0,fut.values*(1-margin)),
        'illustrative_upper_not_95pi':fut.values*(1+margin)})
    fut_df.to_csv(root/'outputs/forward_forecast_scenarios.csv',index=False)
    result={'data':'Observed US clothing store sales, FRED MRTSSM4481USN','target':'National monthly nominal USD million, NSA','model_selection_method':'2024 and 2025 rolling-origin fixed 12-month folds','untouched_holdout':'2026 Jan-Aug','chosen_model':str(winner),'backtest_WAPE_pct':float(summary.iloc[0].WAPE_pct),'holdout_WAPE_pct':round(hold_score,2),'holdout_seasonal_naive_WAPE_pct':round(baseline_hold,2),'forecast_horizon':'Sep 2026–Aug 2027','illustrative_band_80pct_absolute_percentage_error':round(margin*100,2),'interval_warning':'Illustrative stress bands from 2026 holdout, NOT statistically calibrated prediction intervals; may fail if regime changes.','scope':'US sector aggregate, not SKU-level fashion demand or India-specific retail prediction.','future_warning':'Forward forecasts are model scenarios, not observed future sales.'}
    (root/'outputs/forecast_findings.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    plt.rcParams.update({'figure.dpi':140,'font.size':9})
    fig,ax=plt.subplots(figsize=(9,4));ax.bar(summary.model,summary.WAPE_pct);ax.set(ylabel='WAPE (%), smaller is better',title='Chronological 2024–25 validation — model comparison');ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(root/'assets/01_model_comparison.png',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,4.3));ax.plot(hold.date,hold.actual_usd_million,'o-',label='Observed 2026 Jan–Aug');ax.plot(hold.date,hold.selected_model_forecast,'s--',label='Selected model (trained through 2025)');ax.plot(hold.date,hold.seasonal_naive_forecast,':',label='Seasonal naive');ax.set(title='True out-of-time holdout, 2026 Jan–Aug',ylabel='Nominal USD millions',xlabel='Month');ax.grid(alpha=.2);ax.legend(frameon=False);fig.tight_layout();fig.savefig(root/'assets/02_2026_holdout.png',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(10.2,4.4));recent=y.loc['2024-01-01':];ax.plot(recent.index,recent.values,label='Observed through Aug 2026',lw=1.7);ax.plot(fut_df.month,fut_df.point_forecast_usd_million,'--',label='Forward scenario, not actuals');ax.fill_between(fut_df.month,fut_df.illustrative_lower_not_95pi,fut_df.illustrative_upper_not_95pi,alpha=.16,label='Illustrative stress range (not 95% PI)');ax.set(title='Forward market scenario: Sep 2026–Aug 2027',ylabel='Nominal USD millions',xlabel='Month');ax.grid(alpha=.2);ax.legend(frameon=False);fig.tight_layout();fig.savefig(root/'assets/03_future_scenarios.png',bbox_inches='tight');plt.close(fig)
    print(json.dumps(result,indent=2));return result
if __name__=='__main__':run()
