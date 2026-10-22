# Evaluator guide — Week 2: Fashion data acquisition & preprocessing

This repository provides both a detailed Week 2 Word report and **executed preprocessing code with numeric, reproducible evidence**. It addresses Week 1 feedback about the need to display concrete analysis and actual code rather than only a strategy.

**Start at:** [README](README.md) → [preprocessing source](src/preprocess.py) → [data quality audit](data/processed/quality_audit.json) → [tests](tests/test_pipeline.py).

## Actual demonstrator, not just a proposal

1. [Raw synthetic apparel transactions](data/raw/synthetic_fashion_orders.csv) — 163 input rows, malformed dates/prices, duplicate line IDs, missing customer, return records, mixed labels.
2. [Cleaned sales CSV](data/processed/clean_sales.csv) — 147 rows, standardized fields and engineered features.
3. [Returns CSV](data/processed/returns.csv) — 2 valid returns separated from sales.
4. [Quarantined rows and reason codes](data/processed/quarantine.csv) — 14 rejected input records, each traceable to its raw CSV line.
5. [Quality audit](data/processed/quality_audit.json) — SHA-256, missingness, reason counts and 163 = 147 + 2 + 14 reconciliation.
6. [Weekly lag features](data/processed/weekly_features.csv) — time-aware feature engineering without look-ahead leakage.
7. [Eleven tested assertions](tests/test_pipeline.py) — duplicate handling, schema validation, discounts, returns, reconciliation and lag features.
8. [Structured data dictionary](DATA_DICTIONARY.md) and [source acquisition guide](README.md).

**Run it:** `pip install -r requirements.txt`, then `python run_pipeline.py`, then `python -m unittest discover -s tests -v`.

All numbers are **synthetic demonstration outputs** and are not represented as company business performance. External sources, licenses/access controls, source limitations and concrete acquisition steps are described separately in the report.
