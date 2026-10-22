"""Optional documented acquisition/adapter for independently downloaded UCI Online Retail.

UCI Online Retail is general-gift retail data, NOT apparel. A fashion SKU/size is
not fabricated. Its transactions can demonstrate generic cleaning only.
Download: https://archive.ics.uci.edu/dataset/352/online+retail (CC BY 4.0)
"""
from pathlib import Path
import argparse
import pandas as pd


def convert_uci_excel(input_xlsx: Path, output_csv: Path) -> int:
    frame=pd.read_excel(input_xlsx,engine='openpyxl',dtype={'InvoiceNo':'string','StockCode':'string','CustomerID':'string'})
    names=['InvoiceNo','StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID','Country']
    missing=[c for c in names if c not in frame.columns]
    if missing:raise ValueError(f'UCI input missing columns: {missing}')
    n=len(frame)
    # Preserve distinct original rows even when fields match; UCI can contain repeated purchased items.
    converted=pd.DataFrame({
        'order_id':frame.InvoiceNo.astype('string'),
        'line_id': ['UCI-'+str(i+1).zfill(8) for i in range(n)],
        'order_timestamp':pd.to_datetime(frame.InvoiceDate,errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S'),
        'sku':frame.StockCode.astype('string'),
        'category':'GENERAL_RETAIL', 'size':'UNKNOWN',
        'quantity':frame.Quantity,'unit_price_gbp':frame.UnitPrice, # Currency preserved: GBP, NOT rupees.
        'discount_pct':'0','customer_id':frame.CustomerID,
        'channel':'UNKNOWN','color':'UNKNOWN',
        'return_flag':frame.InvoiceNo.astype(str).str.upper().str.startswith('C') | (frame.Quantity<0)})
    # This adapter creates a source-aware staging table. It is not directly compatible
    # with the synthetic INR teaching pipeline until a distinct GBP schema is used.
    output_csv=Path(output_csv);output_csv.parent.mkdir(parents=True,exist_ok=True)
    converted['return_flag']=converted.return_flag.map({True:'Y',False:'N'})
    converted.to_csv(output_csv,index=False)
    (output_csv.with_suffix('.currency.txt')).write_text('SOURCE CURRENCY: GBP. The table uses unit_price_gbp. It must NOT be passed to the INR fashion demo pipeline without a separate GBP-aware schema. UCI is gift retail, not fashion.\n',encoding='utf-8')
    return n

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input_xlsx',type=Path);p.add_argument('output_csv',type=Path)
    a=p.parse_args();print(f'Adapted {convert_uci_excel(a.input_xlsx,a.output_csv)} UCI source rows; check currency note.')
