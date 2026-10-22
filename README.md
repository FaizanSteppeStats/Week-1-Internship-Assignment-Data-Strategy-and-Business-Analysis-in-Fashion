# Week 1 — Data Strategy and Business Analysis in Fashion

**[EVALUATOR: START HERE](EVALUATOR_START_HERE.md)**

This is the **improved October 22, 2026 evidence pack** addressing prior feedback about missing numerical analysis and difficult-to-find Python source. It includes reproducible synthetic data, runnable scripts, forecast/KPI comparisons, inventory decisions, RFM segmentation and an improved text version of the Word report.

## Open immediately

- **[Revised full report, readable online](Week1_Fashion_Data_Strategy_Improved_Report.md)** — expanded analysis and worked examples.
- **[Runnable analysis entry point](run_analysis.py)** — one command.
- **[Worked case-study Python source](src/case_study_analysis.py)** and **[original demand-modelling source](src/fashion_strategy_demo.py)**.
- **[Interactive notebook](Week1_Fashion_Case_Study.ipynb)** — executes charts and result tables.
- **[Numeric results](outputs/case_study_summary.json)**, **[forecast results](outputs/case_forecast_by_category.csv)**, **[inventory decisions](outputs/case_reorder_ranked.csv)**, and **[customer segmentation](outputs/case_segment_shares.csv)**.
- **[Validation test](tests/test_case_study.py)**.

### Example findings (all synthetic)

| Measure | Result |
|---|---:|
| SKUs / SKU-weeks | 16 / 1,248 |
| Simulated units sold | 34,131 |
| Baseline forecast WAPE | 19.09% |
| Blend forecast WAPE | 18.86% |
| SKU-week holdout observations | 153 |
| Replenishment review | 11 SKUs, 149 units |
| Simulated customers | 520 |

The forecast improvement of 0.23 percentage points is modest and **not significant evidence for deployment**; the blended forecast worsened T-shirt performance. Analysis and gross sales are synthetic examples, not verified company results.

## Run locally

```bash
pip install -r requirements.txt
python run_analysis.py
python -m unittest discover -s tests -v
```

No private company data or API keys are required. Original input data are located in `data/`; generated tables and metrics appear in `outputs/`.

**Word report note:** `Week1_Fashion_Data_Strategy_Report.docx` is the **original** DOCX already in the repository. The revised full report is shown in [GitHub-readable format](Week1_Fashion_Data_Strategy_Improved_Report.md). The revised 12-page `.docx` should be uploaded as the portal attachment. No company sales or personal data were used.
