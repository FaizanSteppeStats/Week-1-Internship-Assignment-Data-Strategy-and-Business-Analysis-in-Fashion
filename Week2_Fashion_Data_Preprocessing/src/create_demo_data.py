"""Generate deterministic synthetic fashion orders with deliberate quality defects.

Not sourced from an employer or online vendor. NOT real consumer data.
"""
import csv
from pathlib import Path
import random

FIELDS = ['order_id','line_id','order_timestamp','sku','category','size','quantity','unit_price_inr','discount_pct','customer_id','channel','color','return_flag']


def make_demo(path: Path, seed: int = 2026, n: int = 160):
    rng = random.Random(seed)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows=[]
    categories=[('TSHIRT','TS'),('DENIM','DN'),('KURTA','KR'),('ACTIVE','AC')]
    for i in range(n):
        cat,prefix=categories[i%4]
        size = ['S','M','L','XL'][i%4]
        unit={'TSHIRT':699,'DENIM':1899,'KURTA':1299,'ACTIVE':999}[cat]
        d=(i%27)+1
        row={
            'order_id':f'ORD-{(i//2)+1001}', 'line_id':f'LN-{i+1:04d}',
            'order_timestamp':f'2026-09-{d:02d} {10+i%10:02d}:{i%60:02d}:00',
            'sku':f'{prefix}-{(i%7)+1:02d}-{size}', 'category':cat, 'size':size,
            'quantity':rng.choice([1,1,1,2,3]), 'unit_price_inr':str(unit),
            'discount_pct':rng.choice(['0','10','0.15','5%']),
            'customer_id':f'C{(i%58)+1:04d}', 'channel':rng.choice(['Online','Store','Marketplace']),
            'color':rng.choice(['Black','Blue','White']), 'return_flag':'N'
        }
        rows.append(row)
    # controlled imperfections (all indexes are distinct except explicit duplicates)
    rows[3]['size']=' medium '
    rows[7]['size']='xxxl'
    rows[11]['category']=' tees '
    rows[15]['channel']='web'
    rows[18]['color']=' navy '
    rows[19]['unit_price_inr']='₹1,899.00'
    rows[23]['discount_pct']=''
    rows[31]['discount_pct']='bad discount'
    rows[33]['customer_id']=''
    rows[35]['customer_id']=''
    rows[39]['quantity']='0'
    rows[43]['unit_price_inr']=''
    rows[47]['sku']=''
    rows[51]['order_timestamp']='31/09/2026'
    rows[55]['quantity']='-2';rows[55]['return_flag']='Y'
    rows[59]['return_flag']='Y';rows[59]['quantity']='1'
    rows[63]['return_flag']='Y';rows[63]['quantity']='-1'
    rows[67]['unit_price_inr']='-99'
    rows[71]['discount_pct']='130%'
    rows[73]['color']=''
    rows[75]['size']=''
    rows[79]['category']=''
    rows[83]['order_id']=''
    rows[87]['discount_pct']='15'
    rows[89]['quantity']='two'
    rows[91]['unit_price_inr']='1,299.00'
    rows[93]['channel']='MOBILE APP'
    rows[95]['order_timestamp']='2026-10-01 23:15:00'  # outside September window, valid observation
    rows.append(dict(rows[5]))  # byte-for-byte duplicate
    rows.append(dict(rows[42]))  # byte-for-byte duplicate
    conflict=dict(rows[9]);conflict['unit_price_inr']='2999';rows.append(conflict)  # same line_id, contradictory price
    # Legitimate two-line order already occurs frequently. Duplicate order_id is not a duplicate line.
    with path.open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)
    return len(rows)

if __name__ == '__main__':
    p=Path(__file__).resolve().parents[1]/'data'/'raw'/'synthetic_fashion_orders.csv'
    print(f'Generated {make_demo(p)} SYNTHETIC raw rows at {p}')
