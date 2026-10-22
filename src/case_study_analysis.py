"""Reproducible fashion case-study evidence (ALL DATA ARE SYNTHETIC)."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def calculate_case_study(root: Path) -> dict:
    root=Path(root)
    data=root / "data"
    out=root / "outputs"
    out.mkdir(parents=True,exist_ok=True)
    sales=pd.read_csv(data / "synthetic_weekly_sales.csv")
    predictions=pd.read_csv(out / "walk_forward_predictions.csv")
    reorder=pd.read_csv(out / "replenishment_suggestions.csv")
    segments=pd.read_csv(out / "rfm_segment_summary.csv")
    orders=pd.read_csv(data / "synthetic_orders.csv")

    sales['gross_value_inr']=sales['units_sold']*sales['unit_price_inr']
    grouped=sales.groupby('category',sort=True).agg(
        sku_weeks=('sku','size'),units_sold=('units_sold','sum'),
        gross_value_inr=('gross_value_inr','sum'),
        returned_units=('returned_units','sum'),
        stockout_sku_weeks=('stockout_flag','sum'))
    grouped['stockout_sku_week_pct']=(100*grouped['stockout_sku_weeks']/grouped['sku_weeks']).round(2)
    grouped['return_units_pct']=(100*grouped['returned_units']/grouped['units_sold']).round(2)
    grouped.reset_index().to_csv(out/'case_category_kpis.csv',index=False)

    forecast_rows=[]
    for cat,g in predictions.groupby('category',sort=True):
        den=float(g['actual'].sum())
        w1=100*float((g['actual']-g['naive_4wk']).abs().sum())/den
        w2=100*float((g['actual']-g['blend_4_8wk']).abs().sum())/den
        forecast_rows.append({'category':cat,'evaluated_sku_weeks':len(g),
           'wape_baseline_pct':round(w1,2),'wape_blend_pct':round(w2,2),
           'improvement_percentage_points':round(w1-w2,2),
           'lower_error_model':'blend_4_8wk' if w2<w1 else 'naive_4wk'})
    scores=pd.DataFrame(forecast_rows)
    scores.to_csv(out/'case_forecast_by_category.csv',index=False)

    rank=reorder[['sku','category','avg_weekly_units_8wk','synthetic_on_hand',
        'reorder_point_units','illustrative_replenishment_units','action']].sort_values(
        'illustrative_replenishment_units',ascending=False).reset_index(drop=True)
    rank.to_csv(out/'case_reorder_ranked.csv',index=False)

    count=int(segments['customers'].sum())
    segments['customer_pct']=(100*segments['customers']/count).round(1)
    segments['spend_share_pct']=(100*segments['total_spend_inr']/segments['total_spend_inr'].sum()).round(1)
    segments.to_csv(out/'case_segment_shares.csv',index=False)

    # Resample held-out weeks as paired units; descriptive interval only.
    rng=np.random.default_rng(2026)
    weeks=sorted(predictions.week_start.unique())
    draws=[]
    for i in range(2000):
        sample=rng.choice(weeks,size=len(weeks),replace=True)
        sub=pd.concat([predictions.loc[predictions.week_start==w] for w in sample],ignore_index=True)
        den=float(sub.actual.sum())
        b=100*(sub.actual-sub.naive_4wk).abs().sum()/den
        m=100*(sub.actual-sub.blend_4_8wk).abs().sum()/den
        draws.append(b-m)
    bounds=np.quantile(draws,[.025,.975])
    (out/'case_bootstrap_interval.json').write_text(json.dumps({
       'method':'2000 paired resamples of held-out weeks; descriptive synthetic estimate',
       'wape_improvement_lower_pp':round(float(bounds[0]),3),
       'wape_improvement_upper_pp':round(float(bounds[1]),3)},indent=2),encoding='utf-8')

    baseline=100*float((predictions.actual-predictions.naive_4wk).abs().sum())/float(predictions.actual.sum())
    blend=100*float((predictions.actual-predictions.blend_4_8wk).abs().sum())/float(predictions.actual.sum())
    result={'data_type':'SYNTHETIC - NEVER REAL COMPANY DATA',
       'sku_weeks':int(len(sales)),'sku_count':int(sales.sku.nunique()),
       'orders':int(len(orders)),'customers':int(orders.customer_id.nunique()),
       'units_sold':int(sales.units_sold.sum()),
       'gross_merchandise_value_inr':int(sales.gross_value_inr.sum()),
       'total_stockout_sku_weeks':int(sales.stockout_flag.sum()),
       'total_returned_units':int(sales.returned_units.sum()),
       'holdout_sku_weeks_used':int(len(predictions)),
       'holdout_sku_weeks_excluded_due_to_stockout':int(len(sales.sku.unique())*12-len(predictions)),
       'overall_baseline_wape_pct':round(baseline,2),
       'overall_blend_wape_pct':round(blend,2),
       'overall_improvement_pp':round(baseline-blend,2),
       'wape_improvement_95pct_resampled_interval_pp':[round(float(x),3) for x in bounds],
       'sku_reorder_reviews':int((reorder.action=='REVIEW').sum()),
       'illustrative_total_reorder_units':int(reorder.illustrative_replenishment_units.sum()),
       'disclaimer':'Historical and financial results are fictional. No incremental marketing impact measured.'}
    (out/'case_study_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

    fig,axes=plt.subplots(1,2,figsize=(10.5,3.65),gridspec_kw={'width_ratios':[1.2,1]})
    cats=scores.category.tolist();x=np.arange(len(cats));width=.36
    axes[0].bar(x-width/2,scores.wape_baseline_pct,width,label='4-week baseline',color='#90A9C7')
    axes[0].bar(x+width/2,scores.wape_blend_pct,width,label='4/8-week blend',color='#145B6C')
    axes[0].set_xticks(x,cats);axes[0].set_ylabel('WAPE (%) - lower is better')
    axes[0].set_title('Holdout error by category',fontweight='bold',fontsize=11)
    axes[0].legend(frameon=False,fontsize=8)
    axes[0].set_ylim(0,27)
    top=rank.head(5).iloc[::-1]
    axes[1].barh(top.sku,top.illustrative_replenishment_units,color='#B77838')
    axes[1].set_xlabel('Illustrative reorder units')
    axes[1].set_title('Top reorder reviews',fontweight='bold',fontsize=11)
    axes[1].set_xlim(0,max(top.illustrative_replenishment_units)+6)
    for i,v in enumerate(top.illustrative_replenishment_units):
        axes[1].text(v+.5,i,str(int(v)),va='center',fontsize=8)
    for ax in axes:ax.spines[['top','right']].set_visible(False)
    fig.suptitle('SYNTHETIC CASE STUDY | not actual retailer results',fontsize=10,color='#666666',y=1.02)
    fig.tight_layout()
    fig.savefig(out/'case_study_decisions.png',dpi=175,bbox_inches='tight')
    plt.close(fig)
    return result

if __name__=='__main__':
    print(json.dumps(calculate_case_study(Path(__file__).resolve().parents[1]),indent=2))
