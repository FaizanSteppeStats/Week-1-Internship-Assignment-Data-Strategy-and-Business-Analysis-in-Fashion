"""Generate fixture, preprocess, emit audit and chart in one command."""
from pathlib import Path
import json
from src.create_demo_data import make_demo
from src.preprocess import process_csv
from src.visualize import make_chart

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    print('SYNTHETIC FASHION DATA ONLY -- NO REAL COMPANY RECORDS')
    count=make_demo(root/'data/raw/synthetic_fashion_orders.csv')
    audit=process_csv(root/'data/raw/synthetic_fashion_orders.csv',root/'data/processed')
    make_chart(root/'data/processed',root/'assets/quality_breakdown.png')
    print('Raw rows:',count,' | clean sales:',audit['clean_sales_rows'],
          '| returns:',audit['clean_returns_rows'],'| quarantined:',audit['quarantined_rows'])
    print('Full audit: data/processed/quality_audit.json')
