# Week 2 — Fashion data acquisition & preprocessing techniques

**Junior Data Science Analyst Internship | Reproducible technical submission**

> **Evaluator: begin with [EVALUATOR_START_HERE.md](EVALUATOR_START_HERE.md).**
> All demo orders are deliberately **SYNTHETIC**. Real public source datasets are documented with acquisition links, restrictions and provenance instructions.

## Evidence first: actual executed demo

| Reconciliation measure | Reproduced result |
|---|---:|
| Raw rows | 163 |
| Clean positive sales | 147 |
| Valid returns routed to separate file | 2 |
| Quarantined problematic rows | 14 |
| Retained for controlled analyses | 149 (91.41%) |
| Exact duplicates identified | 2 |
| Missing customer IDs retained as `GUEST` | 2 |
| Clean rows with unknown size preserved | 2 |
| Unit tests | 11 passed |

Exact artifacts: [quality audit](data/processed/quality_audit.json) · [rejected rows](data/processed/quarantine.csv) · [cleaned sales](data/processed/clean_sales.csv) · [weekly features](data/processed/weekly_features.csv).

## One-command reproduction

```bash
python -m pip install -r requirements.txt
python run_pipeline.py
python -m unittest discover -s tests -v
```

The pipeline recreates the source fixture with seed 2026, validates and cleans rows, quarantines rather than silently deleting violations, generates time-safe lag features and a chart in `assets/`.

## Code map

- [src/create_demo_data.py](src/create_demo_data.py) — deterministic noisy apparel dataset with intentional errors.
- [src/preprocess.py](src/preprocess.py) — business rules, parse types, required checks, duplicate policy, split sales vs returns, build features, emit SHA-256 audit log.
- [src/visualize.py](src/visualize.py) — quality outcome chart.
- [src/uci_adapter.py](src/uci_adapter.py) — optional real UCI general retail workbook staging to a **GBP-denominated schema**; not apparel-specific and not fed into synthetic INR metrics.
- [src/fetch_worldbank.py](src/fetch_worldbank.py) — OPTIONAL internet-connected World Bank India textile indicator acquisition with source metadata/sha256. Not executed in offline demo.
- [tests/test_pipeline.py](tests/test_pipeline.py) — 11 reproducible tests.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — fields, business constraints, caveats.

## Real data acquisition (optional, non-demo)

- UCI Online Retail (general gift retail, **not fashion-specific**): https://archive.ics.uci.edu/dataset/352/online+retail. Site lists **CC BY 4.0** and 541,909 transactions. Download `Online Retail.xlsx` independently, then run:
  `python -m src.uci_adapter 'Online Retail.xlsx' data/external/uci_transactions_gbp.csv`.
  This creates a separate GBP staging table. **Do not label it as fashion transactions or rupee revenue.**
- H&M competition (fashion-specific): https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data. Login/rule acceptance necessary; reuse governed by competition terms; raw data excluded.
- Google Trends: https://trends.google.com/trends/ — manually export CSV, retain search term, geography and time period; normalized 0–100 is relative search interest, **not sales**.
- Open-Meteo historical weather: https://open-meteo.com/en/docs/historical-weather-api — API supports historical weather for contextual feature joins.
- India textile production: https://sikkim.data.gov.in/catalog/production-textile-products-india — dated official production dataset; check update coverage and reuse terms.
- World Bank industry structure: https://data.worldbank.org/indicator/NV.MNF.TXTL.ZS.UN — textiles/clothing share of manufacturing value added (not SKU data); `python -m src.fetch_worldbank --out data/external` (requires internet).
- Open Supply Hub: https://info.opensupplyhub.org/resources/how-to-search — production facility data; account/download rules apply.

## Limitations

A controlled fixture demonstrates *how* cleaning works, not empirical trends in India. An operational implementation must obtain permissioned product/sales feeds, define currency/timezone conventions, review data contracts, avoid customer-level personal identifiers in public repositories, and validate on holdout data. Downloadable external datasets are **not** silently bundled or falsely described as executed.
