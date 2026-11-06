# Week 3 — EDA and Visualization in Fashion Trends

**Evaluator: begin with [EVALUATOR_START_HERE.md](EVALUATOR_START_HERE.md).**

Real U.S. Census retail dataset (92 monthly records), five charts, robust outlier screen, seasonality, distribution, correlated nested series, practical limitations.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run_analysis.py
python -m unittest discover -s tests -v
```

## Checkable evidence

- **Word report:** [Week3_Fashion_EDA_and_Visualization_Report.docx](Week3_Fashion_EDA_and_Visualization_Report.docx)
- **Source and data dictionary:** [data/SOURCE_PROVENANCE.json](data/SOURCE_PROVENANCE.json) and [source CSV](data/fred_clothing_store_sales_2019_2026_08.csv)
- **Analysis code:** [src/eda.py](src/eda.py)
- **Outputs:** outputs/eda_findings.json, outputs/annual_summary.csv, outputs/seasonality_by_month.csv, outputs/robust_outliers_yoy.csv, and five PNGs in assets/
- **Tests:** tests/

## Data scope and provenance

Real U.S. Census Bureau monthly national retail sales delivered via FRED. Sources: https://fred.stlouisfed.org/data/MRTSSM4481USN and https://fred.stlouisfed.org/data/MRTSSM448USN; release snapshot 15 October 2026; observations through August 2026 only. Currency is millions of nominal USD, not seasonally adjusted. This dataset does not contain local Indian retail transactions, SKU trends, product colors or consumer identities. Any forward forecasts are projections, not observed future outcomes.
