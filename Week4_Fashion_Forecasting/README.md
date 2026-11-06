# Week 4 — Predictive Analytics and Forecasting in Fashion

**Evaluator: begin with [EVALUATOR_START_HERE.md](EVALUATOR_START_HERE.md).**

Real national apparel retail series, 3 candidate forecast methods, strictly chronological 2024/2025 annual-origin folds and a sealed January–August 2026 holdout.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run_analysis.py
python -m unittest discover -s tests -v
```

## Checkable evidence

- **Word report:** [Week4_Fashion_Predictive_Analytics_Forecasting_Report.docx](Week4_Fashion_Predictive_Analytics_Forecasting_Report.docx)
- **Source and data dictionary:** [data/SOURCE_PROVENANCE.json](data/SOURCE_PROVENANCE.json) and [source CSV](data/fred_clothing_store_sales_2019_2026_08.csv)
- **Analysis code:** [src/forecast.py](src/forecast.py)
- **Outputs:** outputs/model_scorecard_overall.csv, outputs/model_scorecard_by_fold.csv, outputs/untouched_2026_holdout.csv, outputs/forward_forecast_scenarios.csv, outputs/forecast_findings.json, and three PNGs in assets/
- **Tests:** tests/

## Data scope and provenance

Real U.S. Census Bureau monthly national retail sales delivered via FRED. Sources: https://fred.stlouisfed.org/data/MRTSSM4481USN and https://fred.stlouisfed.org/data/MRTSSM448USN; release snapshot 15 October 2026; observations through August 2026 only. Currency is millions of nominal USD, not seasonally adjusted. This dataset does not contain local Indian retail transactions, SKU trends, product colors or consumer identities. Any forward forecasts are projections, not observed future outcomes.
