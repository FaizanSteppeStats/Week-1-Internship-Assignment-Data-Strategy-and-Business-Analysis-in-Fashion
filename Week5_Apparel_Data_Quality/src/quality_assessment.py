"""Week 5 reproducible data-quality assessment.

Two independent datasets are evaluated:
* explicitly SYNTHETIC apparel transaction stress-test, with labelled corrections;
* real public U.S. Census clothing-store sales via FRED, frozen at 2026-10-15.
This script does NOT assert measured ground-truth accuracy or alter real outliers.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .retail_cleaner import process_csv, load_csv

CRITICAL = ['order_id', 'sku', 'quantity', 'unit_price_inr', 'order_timestamp']
FRED_COLUMN = 'clothing_stores_usd_million'


def inspect_fred(path: Path) -> tuple[dict, pd.DataFrame]:
    """Validate source schema, target and cadence; flag—not delete—YoY shocks."""
    df = pd.read_csv(path, dtype={'date': str})
    for c in ['date', FRED_COLUMN, 'source_vintage', 'adjustment']:
        if c not in df: raise ValueError(f'Missing public-series field: {c}')
    dates = pd.to_datetime(df['date'], errors='coerce')
    target = pd.to_numeric(df[FRED_COLUMN], errors='coerce')
    n = len(df)
    bad_date = int(dates.isna().sum())
    duplicate_months = int(dates[dates.notna()].duplicated().sum())
    bad_level = int((target.isna() | (target <= 0)).sum())
    not_month_start = int(((dates.dt.day != 1) & dates.notna()).sum())
    d = df.assign(date=dates, target=target).sort_values('date').reset_index(drop=True)
    expected = pd.date_range(d.date.min(), d.date.max(), freq='MS') if not bad_date else pd.DatetimeIndex([])
    gaps = [str(x.date()) for x in expected.difference(d.date)]
    d['yoy_pct'] = (100 * (d.target / d.target.shift(12) - 1)).round(2)
    finite = d['yoy_pct'].dropna()
    med = float(finite.median())
    mad = float((finite - med).abs().median())
    scale = 1.4826 * mad if mad > 0 else np.nan
    d['robust_z_yoy'] = (d.yoy_pct - med) / scale
    d['review_outlier_yoy'] = d.robust_z_yoy.abs() > 3.5
    metrics = {
        'origin': 'OBSERVED PUBLIC U.S. CENSUS / FRED SERIES; NOT A LOCAL FASHION RETAILER',
        'series': 'MRTSSM4481USN',
        'source_url': 'https://fred.stlouisfed.org/series/MRTSSM4481USN',
        'source_vintage': sorted(df.source_vintage.astype(str).unique().tolist()),
        'raw_sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        'monthly_rows': n, 'first_month': d.date.min().strftime('%Y-%m'),
        'last_month': d.date.max().strftime('%Y-%m'),
        'missing_target_months': len(gaps), 'missing_target_month_labels': gaps,
        'invalid_target_values': bad_level, 'invalid_dates': bad_date,
        'duplicate_months': duplicate_months, 'not_first_of_month_dates': not_month_start,
        'additional_accessory_series_missing_rows': int(d.clothing_accessory_stores_usd_million.isna().sum()) if 'clothing_accessory_stores_usd_million' in d else None,
        'yoy_robust_z_review_flags': int(d.review_outlier_yoy.sum()),
        'apr_2020_sales_usd_million': float(d.loc[d.date == pd.Timestamp('2020-04-01'), 'target'].iloc[0]),
        'apr_2019_sales_usd_million': float(d.loc[d.date == pd.Timestamp('2019-04-01'), 'target'].iloc[0]),
        'quality_release_rule': 'Pass observed-series completeness, uniqueness, schema and positive-target checks; review shock flags as genuine historical events, never auto-delete',
        'passed_structural_gates': bool(not (gaps or bad_date or duplicate_months or bad_level or not_month_start)),
        'accuracy_verified_against_independent_ground_truth': False,
        'warning': 'Nominal U.S. monthly aggregate; economic shocks and data revisions matter. FRED values may change at later vintages.'
    }
    return metrics, d


def run_quality(root: Path) -> dict:
    root = Path(root)
    outputs = root / 'outputs'
    assets = root / 'assets'
    outputs.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)
    synthetic_path = root / 'data/raw/synthetic_fashion_orders.csv'
    raw = load_csv(synthetic_path)
    raw_blanks = int(raw[CRITICAL].apply(lambda s: s.astype(str).str.strip().eq('').sum()).sum())
    total_critical = len(raw) * len(CRITICAL)
    a = process_csv(synthetic_path, outputs / 'retail_processed')
    clean = pd.read_csv(outputs / 'retail_processed/clean_sales.csv')
    returns = pd.read_csv(outputs / 'retail_processed/returns.csv')
    quarantine = pd.read_csv(outputs / 'retail_processed/quarantine.csv')
    joined = pd.concat([clean, returns], ignore_index=True)
    accepted_empty_critical = int(joined[CRITICAL].isna().sum().sum())
    critical_valid_pct = 100 * (total_critical - raw_blanks) / total_critical
    out_rows = len(joined)
    if out_rows != len(raw) - len(quarantine): raise AssertionError('Row conservation violated')
    if joined.line_id.duplicated().any(): raise AssertionError('Duplicate accepted line ID')
    if (clean.quantity <= 0).any() or (returns.quantity >= 0).any():
        raise AssertionError('Signed sales/returns rule broken')
    if (clean.net_value_inr < 0).any(): raise AssertionError('Negative net sales amount')
    if accepted_empty_critical: raise AssertionError('Missing required accepted values')
    fm, detail = inspect_fred(root/'data/external/fred_clothing_store_sales_2019_2026_08.csv')
    detail[['date','target','yoy_pct','robust_z_yoy','review_outlier_yoy']].to_csv(outputs/'fred_outlier_review.csv',index=False)
    issue_rows = [{'issue': k, 'rows': int(v), 'action': 'Quarantine for correction/replay'} for k,v in sorted(a['quarantine_reason_counts'].items(),key=lambda kv:(-kv[1],kv[0]))]
    pd.DataFrame(issue_rows).to_csv(outputs/'retail_issue_register.csv',index=False)
    rows = [
        ['Completeness: five critical fields',round(critical_valid_pct,2),100.0,'% of populated critical cells', 'Pass after correction'],
        ['Structural validity / acceptance',round(100*a['retained_rows']/a['raw_rows'],2),100.0,'% of input records passing', 'Quarantine failures; no blind deletion'],
        ['Exact-duplicate input rows',a['exact_duplicate_rows'],0,'rows','Quarantine exact duplicates'],
        ['Accepted line-id collisions',int(joined.line_id.duplicated().sum()),0,'rows','Block release if >0'],
        ['Missing customer identifiers',a['raw_blank_counts']['customer_id'],0,'rows','Retain as guest, exclude personal features'],
        ['FRED missing months',fm['missing_target_months'],0,'months','Block forecast data release'],
        ['FRED unusual YoY changes',fm['yoy_robust_z_review_flags'],None,'flags','Review historical causes; do not auto-impute'],
    ]
    pd.DataFrame(rows,columns=['check','before','target_or_after','unit','decision']).to_csv(outputs/'quality_control_matrix.csv',index=False)
    result = {'synthetic_case':{
        'source_type':'SYNTHETIC 163-row apparel cleaning fixture',
        'raw_rows':a['raw_rows'],'accepted_sales':a['clean_sales_rows'],
        'accepted_returns':a['clean_returns_rows'],'quarantined_rows':a['quarantined_rows'],
        'record_conservation':a['rows_reconciled'], 'accepted_pct':a['retention_pct'],
        'raw_populated_critical_field_pct':round(critical_valid_pct,2),
        'accepted_populated_critical_field_pct':round(100*(len(joined)*len(CRITICAL)-accepted_empty_critical)/(len(joined)*len(CRITICAL)),2),
        'raw_exact_duplicate_rows':a['exact_duplicate_rows'],
        'accepted_unique_line_ids':bool(joined.line_id.is_unique),
        'guest_customer_rows':a['missing_customer_id_retained_as_guest'],
        'net_sales_inr_synthetic':a['net_sales_inr'],
        'gross_sales_inr_synthetic':a['gross_sales_inr'],
        'return_units_separated':a['returned_units_separately_tracked'],
        'quarantine_reason_counts':a['quarantine_reason_counts']},
        'public_series_case':fm,
        'release_status':'CONDITIONALLY PASS: only accepted sales/returns and validated monthly target are analysis-ready; quarantined transaction rows need steward review',
        'quality_accuracy_caveat':'These checks prove specified validity/consistency properties, not independent truth of prices, products or national estimates.',
        'monitoring_proposal':{'critical_keys':'100% accepted rows','monthly_series_completeness':'100% expected month starts','duplicate_line_ids':'0 accepted','source_vintage':'record each run','rejected_records':'quarantine with reason; track trend weekly','real_outliers':'review, not automatically removed'}
    }
    (outputs/'quality_evidence.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    # Clear, independent visualizations.
    plt.figure(figsize=(9,3.5))
    names=['Accepted sales','Valid returns','Quarantined']; values=[a['clean_sales_rows'],a['clean_returns_rows'],a['quarantined_rows']]
    bars=plt.barh(names[::-1],values[::-1],color=['#C88552','#6C9DA9','#19556C'][::-1])
    plt.xlabel('Source rows (synthetic)');plt.title('All 163 transaction rows are accounted for')
    for bar in bars:plt.text(bar.get_width()+1,bar.get_y()+bar.get_height()/2,str(int(bar.get_width())),va='center')
    plt.xlim(0,165);plt.tight_layout();plt.savefig(assets/'01_row_reconciliation.png',dpi=170);plt.close()
    issues=pd.DataFrame(issue_rows).sort_values(['rows','issue'],ascending=[True,True])
    plt.figure(figsize=(9.2,4.8));plt.barh(issues.issue,issues.rows,color='#A65F4D')
    plt.title('Why rows are quarantined — synthetic apparel example');plt.xlabel('Issue occurrences (some rows may have multiple)')
    plt.tight_layout();plt.savefig(assets/'02_quarantine_reasons.png',dpi=170);plt.close()
    plt.figure(figsize=(10,3.7));plt.plot(detail.date,detail.yoy_pct,color='#1C5777',linewidth=1.6,label='YoY change (%)')
    flagged=detail[detail.review_outlier_yoy]
    plt.scatter(flagged.date,flagged.yoy_pct,color='#B65E4B',s=25,label='Review, not delete',zorder=3)
    plt.axhline(0,color='#777',linewidth=.8);plt.title('Observed public clothing-store sales: economic shocks flagged')
    plt.ylabel('YoY change (%)');plt.legend(frameon=False);plt.tight_layout()
    plt.savefig(assets/'03_real_series_anomaly_review.png',dpi=170);plt.close()
    return result

if __name__=='__main__':
    r=run_quality(Path(__file__).resolve().parents[1]);print(json.dumps(r,indent=2,ensure_ascii=False))
