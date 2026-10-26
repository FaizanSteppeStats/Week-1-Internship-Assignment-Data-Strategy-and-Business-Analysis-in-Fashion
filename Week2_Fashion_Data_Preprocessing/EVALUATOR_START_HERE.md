# Week 2 — Evaluator: START HERE (improved real-data submission)

**NEW: observed public fashion retail data, alongside a separate deterministic synthetic stress test.**

1. **[Enhanced 10-page Word report](Week2_Data_Acquisition_and_Preprocessing_Report.docx)** — actual collection and unique-product counts, charts, cleaning decisions, source attributions and proposed joins.
2. **[Real fashion source dataset](data/external/livostyle_collections.json)** + [stats source](data/external/livostyle_stats.json) — MIT licensed Livostyle public dataset, pinned upstream revision `0ce98ce4412b0c7b6b76d8fe809c1e78c7e16b5f` (18 Oct 2026 source sync).
3. **[Real preprocessing Python](src/real_catalog_pipeline.py)** — validates counts, IDs and UTC timestamps; cleans HTML and SEO; preserves optional missing image fields; flags inconsistent membership totals. Run `python -m src.real_catalog_pipeline`.
4. **[Real-data audit](outputs/real_catalog/real_catalog_quality_audit.json)** and [cleaned source table](outputs/real_catalog/real_collections_clean.csv).
5. **[Real category distribution](outputs/real_catalog/real_product_category_shares.csv)** and [catalog anomalies](outputs/real_catalog/real_top_collections.csv).
6. **[Synthetic quality fixture](data/raw/synthetic_fashion_orders.csv)** + [pipeline](run_pipeline.py) + [audit](data/processed/quality_audit.json). Real catalog is NOT sales data. Do not mix their metrics.
7. **[Real-dataset unit tests](tests/test_real_catalog_pipeline.py)** and original 11 tests. 21 tests passed locally.

## Key observed real-world outputs

| Observed field | Result |
|---|---:|
| Fashion collections | 161 |
| Unique products, in source stats | 2,938 |
| Missing image URLs | 3 |
| Missing SEO descriptions | 1 |
| Collections above unique product count | 2 |
| Sum of overlapping collection memberships (NOT unique) | 36,682 |
| Clothing share of unique product categories | 78.35% |

## Repeat

```bash
python -m pip install -r requirements.txt
python -m src.real_catalog_pipeline
python run_pipeline.py
python -m unittest discover -s tests -v
```

Data source: https://github.com/arturayupov/womens-fashion-catalog-open-data (MIT license, source revision pinned). **Catalog has no sales, orders, stock or consumer behavior observations.** Previous evaluated score is not evidence of a guaranteed new score.
