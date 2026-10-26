"""Reproduce the real, MIT-licensed Livostyle catalog quality case study.

Run after cloning the GitHub repository (snapshots in data/external/), or use
--fetch to obtain the pinned upstream source revision. No keys are required.
Never merge overlapping collection membership counts as unique SKU totals.
"""
from __future__ import annotations
import argparse, collections, hashlib, html, json, re, urllib.request, math
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import pandas as pd

SOURCE_COMMIT = "0ce98ce4412b0c7b6b76d8fe809c1e78c7e16b5f"
SOURCE_REPO = "arturayupov/womens-fashion-catalog-open-data"
BASE = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/data"
FILES = {"collections":"livostyle_collections.json", "stats":"livostyle_stats.json"}

class PlainText(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self, value): self.parts.append(value)
    def value(self): return ' '.join(' '.join(self.parts).split())

def strip_markup(raw):
    p=PlainText(); p.feed(raw if isinstance(raw,str) else '')
    return html.unescape(p.value())

def fetch_pinned_snapshot(directory: Path):
    directory.mkdir(parents=True,exist_ok=True)
    for name,filename in FILES.items():
        url=BASE+'/collections.json' if name=='collections' else BASE+'/stats.json'
        request=urllib.request.Request(url,headers={'User-Agent':'Week2-Fashion-Study/1.0'})
        with urllib.request.urlopen(request,timeout=35) as response:
            body=response.read()
        json.loads(body.decode('utf-8'))
        (directory/filename).write_bytes(body)

def run_case(source_dir:Path, dest_dir:Path):
    source_dir,dest_dir=Path(source_dir),Path(dest_dir)
    raw_c=(source_dir/FILES['collections']).read_bytes()
    raw_s=(source_dir/FILES['stats']).read_bytes()
    collections_data=json.loads(raw_c)
    stats=json.loads(raw_s)
    if not isinstance(collections_data,list) or not isinstance(stats,dict):
        raise ValueError('Source schema mismatch')
    required={'id','handle','title','products_count','updated_at'}
    if any(not isinstance(r,dict) or not required.issubset(r) for r in collections_data):
        raise ValueError('Missing required catalog fields')
    expected=int(stats['total_collections'])
    total_products=int(stats['total_products'])
    missing_image=sum(not str(r.get('image_url') or '').strip() for r in collections_data)
    missing_seo=sum(not str((r.get('seo') or {}).get('description') or '').strip() for r in collections_data)
    existing=set(); cleaned=[]; quarantined=[]; dupes=0; invalid_count=0
    for idx,r in enumerate(collections_data):
        handle=str(r.get('handle') or '').strip().lower()
        raw_id=str(r.get('id') or '').strip()
        if not handle or not raw_id:
            quarantined.append({'source_row':idx+1,'reason':'missing_key'}); continue
        if raw_id in existing:
            dupes+=1; quarantined.append({'source_row':idx+1,'reason':'duplicate_collection_id'});continue
        try:
            num=int(r['products_count'])
            if num<0 or float(r['products_count'])!=num: raise ValueError()
            updated=pd.to_datetime(r['updated_at'],utc=True,errors='raise')
        except Exception:
            invalid_count+=1;quarantined.append({'source_row':idx+1,'reason':'invalid_count_or_timestamp'});continue
        existing.add(raw_id)
        desc=strip_markup(r.get('description_html',''))
        seo=(r.get('seo') or {}).get('description')
        fallback=not bool(str(seo or '').strip())
        processed=(str(seo).strip() if not fallback else desc[:160] if desc else '')
        cleaned.append({'collection_id':raw_id,'handle':handle,'title':str(r['title']).strip(),
        'products_count':num,'updated_at_utc':updated.isoformat(),
        'image_missing':not bool(str(r.get('image_url') or '').strip()),
        'seo_description_fallback':fallback,'seo_description_final':processed,
        'description_plaintext':desc,'description_word_count':len(desc.split()),
        'product_count_gt_unique_total':num>total_products,'log1p_collection_count':round(math.log1p(num),6)})
    df=pd.DataFrame(cleaned).sort_values(['collection_id'],kind='stable')
    categories=[]
    for label,n in stats['products_by_category'].items():
        hierarchy=str(label).split(' > ')
        group=hierarchy[1] if len(hierarchy)>1 else 'Other'
        categories.append({'full_category':label,'category_group':group,'distinct_products':int(n)})
    cat=pd.DataFrame(categories)
    groups=cat.groupby('category_group',as_index=False)['distinct_products'].sum().sort_values('distinct_products',ascending=False)
    groups['catalog_share_pct']=(100*groups.distinct_products/total_products).round(2)
    cat_sum=int(cat.distinct_products.sum())
    if cat_sum!=total_products:
        raise ValueError('Category category totals are inconsistent with unique product total')
    dest_dir.mkdir(parents=True,exist_ok=True)
    df.to_csv(dest_dir/'real_collections_clean.csv',index=False)
    groups.to_csv(dest_dir/'real_product_category_shares.csv',index=False)
    cat.to_csv(dest_dir/'real_product_category_detail.csv',index=False)
    pd.DataFrame(quarantined,columns=['source_row','reason']).to_csv(dest_dir/'real_collections_quarantine.csv',index=False)
    top=df.sort_values('products_count',ascending=False).head(12)[['title','products_count','product_count_gt_unique_total']]
    top.to_csv(dest_dir/'real_top_collections.csv',index=False)
    audit={
    'data_origin':'REAL PUBLIC RETAIL FASHION CATALOG; NOT SYNTHETIC',
    'catalog_last_synced_utc':stats['last_synced'], 'source_repo':SOURCE_REPO,
    'source_commit':SOURCE_COMMIT,'raw_file_sha256':{'collections':hashlib.sha256(raw_c).hexdigest(),'stats':hashlib.sha256(raw_s).hexdigest()},
    'input_collections':len(collections_data),'valid_collection_rows':len(df),'quarantined_rows':len(quarantined),
    'duplicate_collection_ids':dupes,'invalid_count_or_timestamp':invalid_count,
    'missing_collection_images':missing_image,'missing_seo_descriptions':missing_seo,
    'seo_descriptions_derived_from_html':int(df.seo_description_fallback.sum()),
    'collections_count_exceeding_unique_skus':int(df.product_count_gt_unique_total.sum()),
    'unique_products_source_stats':total_products,'sum_of_all_collection_memberships_not_distinct_skus':int(df.products_count.sum()),
    'product_category_totals_sum':cat_sum,'product_category_groups':int(len(groups)),
    'products_with_reviews':int(stats['products_with_reviews']),
    'review_coverage_pct':round(100*stats['products_with_reviews']/total_products,2),
    'caveat':'Collection memberships can overlap and include values inconsistent with the stats snapshot. Do not count them as unique products, sales or inventory.'}
    (dest_dir/'real_catalog_quality_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    return audit

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,default=Path('data/external'))
    ap.add_argument('--output',type=Path,default=Path('outputs/real_catalog'))
    ap.add_argument('--fetch',action='store_true',help='Download pinned MIT upstream dataset; only needed when local snapshots absent')
    opt=ap.parse_args()
    if opt.fetch: fetch_pinned_snapshot(opt.source)
    print(json.dumps(run_case(opt.source,opt.output),indent=2))
