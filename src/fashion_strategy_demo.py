"""Reproducible fashion analytics mini-demo: synthetic inputs, no private data.

Use cases: demand forecasting, illustrative reorder prioritisation, customer RFM.
Not a production ML service or validated estimate of actual retailer performance.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CATEGORIES = {
    'KURTA': (24, 1899),
    'TSHIRT': (35, 799),
    'DENIM': (21, 2299),
    'ACTIVE': (18, 1499),
}


def wape(actual, forecast) -> float:
    """Weighted absolute percentage error, in percent. NaN if demand totals zero."""
    a = np.asarray(actual, dtype=float)
    f = np.asarray(forecast, dtype=float)
    if a.shape != f.shape:
        raise ValueError('Actual and forecast must have identical shapes')
    if np.any(a < 0) or np.any(f < 0):
        raise ValueError('Unit demand/forecasts must be nonnegative')
    denominator = float(np.sum(np.abs(a)))
    return float(100 * np.sum(np.abs(a - f)) / denominator) if denominator > 0 else float('nan')


def generate_synthetic_data(data_dir: Path, seed: int = 42) -> None:
    """Generate 78 weeks of synthetic sales and 2,600 synthetic customer orders."""
    data_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    weeks = pd.date_range('2025-04-07', periods=78, freq='W-MON')
    rows = []
    for category, (base, price) in CATEGORIES.items():
        for color in ('NAVY', 'BLACK'):
            for size in ('M', 'L'):
                sku = f'{category}-{color}-{size}'
                multiplier = (1.12 if size == 'M' else .89) * (1.08 if color == 'NAVY' else .95)
                for i, d in enumerate(weeks):
                    promo = int(rng.random() < 0.16)
                    annual = 1 + .15 * math.sin(2 * math.pi * (d.dayofyear / 365.25))
                    festive = 1.36 if d.month in (10, 11) and category == 'KURTA' else 1.0
                    summer = 1.20 if d.month in (4, 5, 6) and category == 'TSHIRT' else 1.0
                    growth = 1 + i / 78 * .10
                    mean = base * multiplier * annual * festive * summer * growth * (1.30 if promo else 1)
                    potential_demand = int(rng.poisson(max(mean, 1)))
                    available = int(round(mean * rng.uniform(.73, 2.3)))
                    sold = min(available, potential_demand)
                    returns = int(rng.binomial(sold, .06))
                    rows.append((d, sku, category, color, size, promo, price, sold, returns,
                                 available, int(available < potential_demand)))
    sales = pd.DataFrame(rows, columns=[
        'week_start', 'sku', 'category', 'color', 'size', 'promotion_flag',
        'unit_price_inr', 'units_sold', 'returned_units', 'available_units', 'stockout_flag'])
    sales.to_csv(data_dir / 'synthetic_weekly_sales.csv', index=False, date_format='%Y-%m-%d')

    customers = [f'CUS{i:04d}' for i in range(1, 521)]
    order_rows = []
    for cid in customers:
        n = int(np.clip(rng.poisson(4.5), 1, 20))
        for _ in range(n):
            day = pd.Timestamp('2025-04-07') + pd.Timedelta(days=int(rng.integers(0, 539)))
            cat = str(rng.choice(list(CATEGORIES.keys())))
            base_price = CATEGORIES[cat][1]
            amount = round(base_price * float(rng.choice([.8, 1, 1.2, 1.75])), 2)
            order_rows.append((cid, day, cat, amount))
    orders = pd.DataFrame(order_rows, columns=['customer_id', 'order_date', 'category', 'order_value_inr'])
    orders.to_csv(data_dir / 'synthetic_orders.csv', index=False, date_format='%Y-%m-%d')


def evaluate_forecasts(sales: pd.DataFrame, holdout_weeks: int = 12):
    """Rolling one-step walk-forward. Exclude stockout test weeks; never fit on future."""
    df = sales.copy()
    df['week_start'] = pd.to_datetime(df['week_start'])
    dates = sorted(df['week_start'].unique())
    if len(dates) < holdout_weeks + 9:
        raise ValueError('Not enough weekly history for holdout')
    out = []
    test_weeks = set(dates[-holdout_weeks:])
    for sku, group in df.groupby('sku'):
        g = group.sort_values('week_start').reset_index(drop=True)
        for i in range(8, len(g)):
            record = g.iloc[i]
            if record['week_start'] not in test_weeks or int(record['stockout_flag']) == 1:
                continue
            previous = g.iloc[:i]['units_sold'].to_numpy(dtype=float)
            # Rolling base case versus blended short/medium-window demand estimate.
            baseline = float(previous[-4:].mean())
            candidate = float(.55 * previous[-4:].mean() + .45 * previous[-8:].mean())
            out.append((record['week_start'], sku, record['category'], float(record['units_sold']),
                        baseline, candidate))
    tests = pd.DataFrame(out, columns=['week_start', 'sku', 'category', 'actual', 'naive_4wk', 'blend_4_8wk'])
    if tests.empty:
        raise ValueError('No uncensored test weeks')
    scores = pd.DataFrame([{'model': name, 'wape_pct': round(wape(tests['actual'], tests[name]), 2),
                            'evaluated_sku_weeks': len(tests)} for name in ('naive_4wk', 'blend_4_8wk')])
    return tests, scores


def reorder_suggestions(sales: pd.DataFrame, lead_time_weeks: int = 2) -> pd.DataFrame:
    """Illustrative prioritisation. Stock snapshot is synthetic, not live on-hand."""
    df = sales.copy()
    df['week_start'] = pd.to_datetime(df['week_start'])
    rows = []
    for sku, g in df.groupby('sku'):
        g = g.sort_values('week_start')
        recent = g.tail(8)
        estimated_demand = float(recent['units_sold'].mean())
        variability = float(recent['units_sold'].std(ddof=1))
        # Simulate a warehouse snapshot, separate from weekly available-to-sell.
        seed_value = sum(ord(x) for x in sku)
        simulated_on_hand = int(round(estimated_demand * (1.4 + ((seed_value * 7) % 18) / 10)))
        safety_stock = 1.65 * variability * math.sqrt(lead_time_weeks)
        reorder_point = math.ceil(lead_time_weeks * estimated_demand + safety_stock)
        suggested_qty = max(0, reorder_point - simulated_on_hand)
        rows.append((sku, str(g['category'].iloc[0]), round(estimated_demand, 1),
                     simulated_on_hand, round(safety_stock, 1), reorder_point, suggested_qty,
                     'REVIEW' if suggested_qty > 0 else 'MONITOR'))
    return pd.DataFrame(rows, columns=['sku', 'category', 'avg_weekly_units_8wk', 'synthetic_on_hand',
                                       'safety_stock_units', 'reorder_point_units',
                                       'illustrative_replenishment_units', 'action'])


def customer_rfm(orders: pd.DataFrame, as_of: str = '2026-10-15'):
    df = orders.copy()
    df['order_date'] = pd.to_datetime(df['order_date'])
    cutoff = pd.Timestamp(as_of)
    if (df['order_date'] > cutoff).any():
        raise ValueError('Order data must not be dated after analysis cutoff')
    rfm = df.groupby('customer_id').agg(
        last_purchase=('order_date', 'max'),
        frequency=('order_date', 'size'),
        monetary_inr=('order_value_inr', 'sum')).reset_index()
    rfm['recency_days'] = (cutoff - rfm['last_purchase']).dt.days
    # Explicit decision rules rather than hidden clustering labels.
    rfm['segment'] = np.select([
        (rfm['frequency'] >= 6) & (rfm['recency_days'] <= 90),
        (rfm['recency_days'] > 180),
        (rfm['frequency'] >= 3) & (rfm['recency_days'] <= 120),
    ], ['Loyal', 'Reactivation candidate', 'Growth potential'], default='Occasional')
    summary = rfm.groupby('segment').agg(customers=('customer_id', 'count'),
        median_recency_days=('recency_days', 'median'), total_spend_inr=('monetary_inr', 'sum')).reset_index()
    return rfm, summary


def analyse(data_dir: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    sales = pd.read_csv(data_dir / 'synthetic_weekly_sales.csv')
    orders = pd.read_csv(data_dir / 'synthetic_orders.csv')
    tests, scores = evaluate_forecasts(sales)
    suggestions = reorder_suggestions(sales)
    rfm, segments = customer_rfm(orders)
    tests.to_csv(out_dir / 'walk_forward_predictions.csv', index=False)
    scores.to_csv(out_dir / 'forecast_scores.csv', index=False)
    suggestions.to_csv(out_dir / 'replenishment_suggestions.csv', index=False)
    rfm.to_csv(out_dir / 'customer_rfm.csv', index=False)
    segments.to_csv(out_dir / 'rfm_segment_summary.csv', index=False)
    summary = {
        'data_status': 'SYNTHETIC DEMONSTRATION - NOT COMPANY RESULTS',
        'sales_rows': int(len(sales)), 'unique_skus': int(sales['sku'].nunique()),
        'forecast_test_sku_weeks_uncensored': int(len(tests)),
        'stockout_test_rows_excluded': int((sales.assign(week_start=pd.to_datetime(sales['week_start']))
                                              .query('week_start >= "2026-07-13"')['stockout_flag'] == 1).sum()),
        'wape_pct': {r['model']: float(r['wape_pct']) for _, r in scores.iterrows()},
        'replenishment_review_skus': int((suggestions['action'] == 'REVIEW').sum()),
        'rfm_customer_count': int(len(rfm)),
        'note': 'Forecasts are illustrative and may be biased by past stockouts; no measured ROI, lift, or external validation.'
    }
    (out_dir / 'kpi_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

    plt.figure(figsize=(7.2, 3.5))
    bars = plt.bar(scores['model'], scores['wape_pct'])
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height()+.3,
                 f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=10)
    plt.ylabel('WAPE (%, lower is better)')
    plt.title('Synthetic demand demo: walk-forward forecast test')
    plt.ylim(0, max(scores['wape_pct'])*1.2)
    plt.tight_layout()
    plt.savefig(out_dir / 'forecast_comparison.png', dpi=160)
    plt.close()

    category_sales = sales.groupby('category')['units_sold'].sum().sort_values(ascending=False)
    plt.figure(figsize=(7.2, 3.5))
    plt.bar(category_sales.index, category_sales.values)
    plt.ylabel('Synthetic units sold')
    plt.title('Synthetic category-level sales distribution')
    plt.tight_layout()
    plt.savefig(out_dir / 'category_sales.png', dpi=160)
    plt.close()

    plt.figure(figsize=(7.2, 3.5))
    plt.bar(segments['segment'], segments['customers'])
    plt.ylabel('Synthetic customers')
    plt.title('Example RFM customer segments')
    plt.xticks(rotation=17, ha='right')
    plt.tight_layout()
    plt.savefig(out_dir / 'customer_segments.png', dpi=160)
    plt.close()
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--data-dir', type=Path, default=Path('data'))
    parser.add_argument('--output-dir', type=Path, default=Path('outputs'))
    args = parser.parse_args()
    generate_synthetic_data(args.data_dir, seed=args.seed)
    print(json.dumps(analyse(args.data_dir, args.output_dir), indent=2))


if __name__ == '__main__':
    main()
