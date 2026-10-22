"""Audited retail preprocessing; never silently discard invalid transactions.

Usage: python -m src.preprocess --input data/raw/synthetic_fashion_orders.csv --out data/processed
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED=['order_id','line_id','order_timestamp','sku','category','size','quantity','unit_price_inr','discount_pct','customer_id','channel','color','return_flag']
CATEGORIES={'TEES':'TSHIRT','TEE':'TSHIRT','T-SHIRT':'TSHIRT','TSHIRTS':'TSHIRT','TSHIRT':'TSHIRT','JEANS':'DENIM','DENIM':'DENIM','KURTA':'KURTA','ACTIVE':'ACTIVE','ACTIVEWEAR':'ACTIVE'}
SIZES={'SMALL':'S','S':'S','MEDIUM':'M','MD':'M','M':'M','LARGE':'L','L':'L','EXTRA LARGE':'XL','XL':'XL'}
CHANNELS={'WEB':'ONLINE','ONLINE':'ONLINE','MOBILE APP':'ONLINE','ECOM':'ONLINE','STORE':'STORE','RETAIL':'STORE','MARKETPLACE':'MARKETPLACE'}


def clean_text(value):
    if pd.isna(value):return ''
    return re.sub(r'\s+',' ',str(value).strip()).upper()


def parse_amount(value):
    val=clean_text(value).replace(',','').replace('₹','').replace('INR','').replace(' ','')
    return pd.to_numeric(val,errors='coerce') if val else np.nan


def parse_discount(value):
    """Return fraction: 10 -> 0.10, 0.10 -> 0.10, '10%' -> 0.10."""
    s=clean_text(value)
    if not s: return 0.0
    pct=s.endswith('%')
    s=s.rstrip('%')
    try:
        num=float(s)
    except (ValueError,TypeError):return np.nan
    if pct or num>1: num /= 100.0
    return num


def load_csv(path:Path)->pd.DataFrame:
    # dtype=str retains leading zeros for business identifiers.
    df=pd.read_csv(path,dtype='string',keep_default_na=False)
    absent=[k for k in REQUIRED if k not in df.columns]
    if absent: raise ValueError('Required columns missing: '+', '.join(absent))
    return df[REQUIRED].copy()


def process_csv(input_path:Path, out_dir:Path)->dict:
    input_path=Path(input_path);out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    raw=load_csv(input_path)
    digest=hashlib.sha256(input_path.read_bytes()).hexdigest()
    rows_before=len(raw)
    blank_counts={c:int(raw[c].map(lambda v:not bool(clean_text(v))).sum()) for c in REQUIRED}
    duplicate_exact=int(raw.duplicated().sum())
    d=raw.copy();d['source_row']=np.arange(2,len(raw)+2)  # CSV line number
    for c in ['order_id','line_id','sku','category','size','customer_id','channel','color','return_flag']:
        d[c]=d[c].map(clean_text)
    d['order_timestamp']=pd.to_datetime(d['order_timestamp'],errors='coerce',format='mixed',dayfirst=False,utc=True)
    d['quantity']=pd.to_numeric(d['quantity'],errors='coerce')
    d['unit_price_inr']=d['unit_price_inr'].map(parse_amount).astype(float)
    d['discount_pct']=d['discount_pct'].map(parse_discount).astype(float)
    d['category']=d['category'].map(lambda s:CATEGORIES.get(s,s))
    d['size']=d['size'].map(lambda s:SIZES.get(s,'UNKNOWN'))
    d['channel']=d['channel'].map(lambda s:CHANNELS.get(s,'UNKNOWN'))
    d['color']=d['color'].map(lambda s:s if s else 'UNKNOWN')
    d['customer_missing']=d['customer_id'].eq('')
    d.loc[d.customer_missing,'customer_id']='GUEST'
    d['return_flag']=d['return_flag'].isin(['Y','YES','TRUE','1'])
    # Separate original exact duplicate, and same line ID with competing payload.
    exact=raw.duplicated(keep='first').to_numpy()
    previous_seen={}
    reasons=[]
    for i,row in d.iterrows():
        errors=[]
        if exact[i]: errors.append('EXACT_DUPLICATE')
        lid=row['line_id']
        if lid and lid in previous_seen and not exact[i]:errors.append('CONFLICTING_LINE_ID')
        elif lid and lid not in previous_seen:previous_seen[lid]=i
        if not row['order_id']: errors.append('MISSING_ORDER_ID')
        if not lid: errors.append('MISSING_LINE_ID')
        if pd.isna(row['order_timestamp']): errors.append('INVALID_DATE')
        if not row['sku']: errors.append('MISSING_SKU')
        if not row['category']: errors.append('MISSING_CATEGORY')
        if pd.isna(row['quantity']) or row['quantity']==0 or row['quantity']%1!=0:errors.append('INVALID_QUANTITY')
        if pd.isna(row['unit_price_inr']) or row['unit_price_inr']<=0:errors.append('INVALID_PRICE')
        if pd.isna(row['discount_pct']) or row['discount_pct']<0 or row['discount_pct']>1:errors.append('INVALID_DISCOUNT')
        if pd.notna(row['quantity']) and row['quantity']<0 and not row['return_flag']:errors.append('UNFLAGGED_NEGATIVE_QUANTITY')
        if pd.notna(row['quantity']) and row['quantity']>0 and row['return_flag']:errors.append('RETURN_SIGN_MISMATCH')
        errors=list(dict.fromkeys(errors))
        reasons.append('|'.join(errors))
    d['rejection_reason']=reasons
    rejects=d[d.rejection_reason.ne('')].copy()
    good=d[d.rejection_reason.eq('')].copy()
    returns=good[good.return_flag].copy()
    sales=good[~good.return_flag].copy()
    for frame in [sales,returns]:
        frame['unit_count']=frame['quantity'].abs().astype('int64')
        frame['gross_value_inr']=(frame.unit_count*frame.unit_price_inr).round(2)
        frame['net_value_inr']=(frame.gross_value_inr*(1-frame.discount_pct)).round(2)
        frame['order_day']=frame.order_timestamp.dt.strftime('%Y-%m-%d')
        frame['year_week']=frame.order_timestamp.dt.strftime('%G-W%V')
        frame['month']=frame.order_timestamp.dt.month.astype('int64')
        frame['day_of_week']=frame.order_timestamp.dt.dayofweek.astype('int64')
        frame['is_weekend']=frame.day_of_week.isin([5,6])
        frame['size_unknown']=frame['size'].eq('UNKNOWN')
        frame.drop(columns=['rejection_reason'],inplace=True)
    sales=sales.sort_values(['order_timestamp','line_id']).reset_index(drop=True)
    returns=returns.sort_values(['order_timestamp','line_id']).reset_index(drop=True)
    # No leakage: customer features exclude GUEST and are computed on sales only.
    weekly=(sales.groupby(['year_week','category'],as_index=False)
      .agg(units_sold=('unit_count','sum'),revenue_inr=('net_value_inr','sum'),order_lines=('line_id','count'))
      .sort_values(['year_week','category']))
    # Longitudinal features lag one WEEK; current-week demand is never used to predict itself.
    weekly['lag_1_week_units']=weekly.groupby('category')['units_sold'].shift(1)
    weekly['rolling_2_week_mean_past']=weekly.groupby('category')['units_sold'].transform(lambda s:s.shift(1).rolling(2,min_periods=2).mean())
    customers=(sales[~sales.customer_missing].groupby('customer_id',as_index=False)
      .agg(order_lines=('line_id','count'),spend_inr=('net_value_inr','sum')))
    rejects=rejects[['source_row','order_id','line_id','sku','rejection_reason','quantity','unit_price_inr','discount_pct']]
    outputs={'clean_sales.csv':sales,'returns.csv':returns,'quarantine.csv':rejects,'weekly_features.csv':weekly,'customer_features.csv':customers}
    for name,frame in outputs.items():frame.to_csv(out_dir/name,index=False,float_format='%.2f')
    kept=len(sales)+len(returns)
    reject_reasons={}
    for r in rejects.rejection_reason:
        for why in r.split('|'):reject_reasons[why]=reject_reasons.get(why,0)+1
    result={'dataset':'Synthetic fashion apparel demo (NOT actual retailer transactions)',
        'input_file':str(input_path.name),'input_sha256':digest,'raw_rows':rows_before,
        'raw_blank_counts':blank_counts,'exact_duplicate_rows':duplicate_exact,
        'clean_sales_rows':len(sales),'clean_returns_rows':len(returns),'quarantined_rows':len(rejects),
        'retained_rows':kept,'rows_reconciled':bool(rows_before==kept+len(rejects)),
        'retention_pct':round(100*kept/rows_before,2),'quarantine_reason_counts':reject_reasons,
        'unknown_size_clean_rows':int(sales.size_unknown.sum()+returns.size_unknown.sum()),
        'missing_customer_id_retained_as_guest':int(sales.customer_missing.sum()+returns.customer_missing.sum()),
        'gross_sales_inr':round(float(sales.gross_value_inr.sum()),2),'net_sales_inr':round(float(sales.net_value_inr.sum()),2),
        'returned_units_separately_tracked':int(returns.unit_count.sum()),
        'customer_feature_rows':len(customers),'weekly_feature_rows':len(weekly),
        'rules':{'duplicates':'exact or conflicting line ID -> quarantine; same order ID with distinct lines retained',
        'missing_price':'quarantine; never invent revenue','missing_customer_id':'guest flag; exclude from individual customer metrics',
        'discount':'empty assumed no promotion (0); invalid >100% quarantined',
        'returns':'separate with negative signed quantity; not treated as demand',
        'time':'UTC; incoming timestamps assumed UTC for demonstrative data only',
        'outliers':'plausibility checks and quarantine, not blanket winsorization',
        'imputation':'no zero-fill on unknown numeric financial data'}}
    (out_dir/'quality_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    metric_rows=[
      ['Input rows',rows_before,kept],['Exact duplicate rows',duplicate_exact,0],
      ['Rows with missing order id',blank_counts['order_id'],0],
      ['Rows with missing SKU',blank_counts['sku'],0],
      ['Rows with missing customer id',blank_counts['customer_id'],result['missing_customer_id_retained_as_guest']],
      ['Rows quarantined',0,len(rejects)],['Rows with unknown size',0,result['unknown_size_clean_rows']]]
    pd.DataFrame(metric_rows,columns=['metric','before_or_raw_count','after_or_output_count']).to_csv(out_dir/'quality_comparison.csv',index=False)
    return result


def cli():
    p=argparse.ArgumentParser(description='Clean apparel order CSV with quarantine + audit trail.')
    p.add_argument('--input',type=Path,default=Path('data/raw/synthetic_fashion_orders.csv'))
    p.add_argument('--out',type=Path,default=Path('data/processed'))
    args=p.parse_args()
    print(json.dumps(process_csv(args.input,args.out),indent=2,ensure_ascii=False))

if __name__=='__main__': cli()
