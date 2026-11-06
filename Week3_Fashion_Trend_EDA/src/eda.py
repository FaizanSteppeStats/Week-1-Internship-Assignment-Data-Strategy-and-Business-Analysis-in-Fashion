"""Week 3: reproducible EDA of U.S. Census/FRED clothing-store monthly sales.
Source data frozen as of Oct 15 2026. Nominal USD millions; not seasonally adjusted.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]

def run(root=ROOT):
    root=Path(root)
    df=pd.read_csv(root/'data/fred_clothing_store_sales_2019_2026_08.csv',parse_dates=['date'])
    df=df.sort_values('date').reset_index(drop=True)
    assert df.date.is_unique # unique monthly observations
    assert df.date.dt.to_period('M').diff().dropna().apply(lambda x:x.n==1).all()
    assert (df.clothing_stores_usd_million>0).all()
    df['year']=df.date.dt.year;df['month']=df.date.dt.month
    df['year_over_year_pct']=df.clothing_stores_usd_million.pct_change(12)*100
    df['yearly_mean']=df.groupby('year').clothing_stores_usd_million.transform('mean')
    df['deviation_from_annual_mean_pct']=100*(df.clothing_stores_usd_million/df.yearly_mean-1)
    z=df[df.year.between(2021,2025)]
    med=z.groupby('month').clothing_stores_usd_million.median().rename('five_year_median_usd_million').reset_index()
    med['seasonal_index_vs_overall_median']=med.five_year_median_usd_million/z.clothing_stores_usd_million.median()
    df.to_csv(root/'outputs/eda_monthly_features.csv',index=False)
    med.to_csv(root/'outputs/seasonality_by_month.csv',index=False)
    # Outliers: median absolute deviation in YoY changes, including COVID shutdown.
    yoy=df.dropna(subset=['year_over_year_pct']).copy()
    center=yoy.year_over_year_pct.median();mad=np.median(np.abs(yoy.year_over_year_pct-center))
    denom=max(1e-9,1.4826*mad)
    yoy['robust_yoy_score']=(yoy.year_over_year_pct-center)/denom
    outliers=yoy.loc[yoy.robust_yoy_score.abs()>3.5,['date','clothing_stores_usd_million','year_over_year_pct','robust_yoy_score']]
    outliers.to_csv(root/'outputs/robust_outliers_yoy.csv',index=False)
    # Correlation in levels is not causation, and may be driven by trends and seasonality.
    common=df.dropna(subset=['clothing_accessory_stores_usd_million']).copy()
    corr_levels=common[['clothing_stores_usd_million','clothing_accessory_stores_usd_million']].corr().iloc[0,1]
    common['a_yoy']=common.clothing_accessory_stores_usd_million.pct_change(12)
    common['c_yoy']=common.clothing_stores_usd_million.pct_change(12)
    corr_yoy=common[['a_yoy','c_yoy']].corr().iloc[0,1]
    annual=df[df.year.between(2021,2025)].groupby('year').clothing_stores_usd_million.agg(['sum','mean','median','std']).round(2)
    annual.to_csv(root/'outputs/annual_summary.csv')
    # Charts, intentionally including a 2020 shutdown exception.
    plt.rcParams.update({'figure.dpi':140,'font.size':9})
    fig,ax=plt.subplots(figsize=(10.2,4))
    ax.plot(df.date,df.clothing_stores_usd_million,linewidth=1.7,label='Monthly nominal sales')
    ax.plot(df.date,df.clothing_stores_usd_million.rolling(12,min_periods=12).mean(),linewidth=2.3,label='12-month trailing average')
    ax.axvspan(pd.Timestamp('2020-03-01'),pd.Timestamp('2020-05-01'),alpha=.14,label='Early COVID disruption')
    ax.set(title='US clothing-store sales, 2019 to Aug 2026',ylabel='USD millions (NSA)',xlabel='Observation month');ax.legend(frameon=False,loc='upper left');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(root/'assets/01_sales_trend.png',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9.5,4))
    ax.bar(med.month,med.five_year_median_usd_million)
    ax.set_xticks(range(1,13),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']);ax.set(title='Typical monthly clothing sales (2021–25 median)',ylabel='USD millions',xlabel='Calendar month');ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(root/'assets/02_seasonal_bar.png',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4))
    years=[2021,2022,2023,2024,2025]
    ax.boxplot([df.loc[df.year==y,'clothing_stores_usd_million'] for y in years],tick_labels=years,showfliers=True)
    ax.set(title='Within-year variation and outliers in monthly sales',xlabel='Year',ylabel='USD millions');ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(root/'assets/03_year_boxplot.png',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(6.8,5.2));ax.scatter(common.clothing_stores_usd_million,common.clothing_accessory_stores_usd_million,alpha=.65)
    ax.set(title='Related retail series (shared trends; not causal)',xlabel='Clothing stores (USD m)',ylabel='Clothing + accessories stores (USD m)');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(root/'assets/04_series_scatter.png',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.2,4.2));shares=annual['sum']/annual['sum'].sum();ax.pie(shares,labels=[str(y) for y in annual.index],autopct='%.1f%%',startangle=85)
    ax.set_title('Share of combined 2021–25 clothing-store revenue by year\n(yearly total, not product share)');fig.tight_layout();fig.savefig(root/'assets/05_yearly_share_pie.png',bbox_inches='tight');plt.close(fig)
    stats={'source':'Real U.S. Census monthly clothing-store sales via FRED, frozen 2026-10-15','n_months':int(len(df)),'first_month':str(df.date.min().date()),'last_month':str(df.date.max().date()),'months_in_2021_2025':int(len(z)),'missing_clothing':int(df.clothing_stores_usd_million.isna().sum()),'zero_or_negative_clothing':int((df.clothing_stores_usd_million<=0).sum()),'avg_2021_2025':round(float(z.clothing_stores_usd_million.mean()),2),'median_december_2021_2025':float(med.loc[med.month==12,'five_year_median_usd_million'].iloc[0]),'median_february_2021_2025':float(med.loc[med.month==2,'five_year_median_usd_million'].iloc[0]),'dec_to_feb_multiple':round(float(med.loc[med.month==12,'five_year_median_usd_million'].iloc[0]/med.loc[med.month==2,'five_year_median_usd_million'].iloc[0]),2),'level_correlation_clothing_accessory':round(float(corr_levels),4),'yoy_change_correlation':round(float(corr_yoy),4),'outliers_mad_3_5':int(len(outliers)),'apr_2020':int(df.loc[df.date==pd.Timestamp('2020-04-01'),'clothing_stores_usd_million'].iloc[0]),'apr_2019':int(df.loc[df.date==pd.Timestamp('2019-04-01'),'clothing_stores_usd_million'].iloc[0]),'data_caution':'Nominal NSA national retail sales not product searches or local demand. 2026 has only January–August; never compare its sum with full calendar years.'}
    (root/'outputs/eda_findings.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
    print(json.dumps(stats,indent=2));return stats
if __name__=='__main__':run()
