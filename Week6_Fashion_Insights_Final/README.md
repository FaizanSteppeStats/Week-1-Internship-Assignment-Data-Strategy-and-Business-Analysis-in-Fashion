# Week 6 — Reporting, Evaluation and Presentation of Fashion Data Insights

**[EVALUATOR: START HERE](EVALUATOR_START_HERE.md)** | **[Final Word report](Week6_Fashion_Final_Reporting_and_Evaluation_Report.docx)**

This is the final narrative and evaluation artifact integrating public-data strategy, retail data cleaning, real-time-series EDA, benchmarked forecasts, controlled data-quality evidence and specific decisions.

## Core evaluated results

- **Observed national clothing-store sales**: 92 months, January 2019–August 2026, U.S. Census via FRED, vintage 15 October 2026. Median December/February seasonal factor **1.90×** for 2021–25.
- **Held-out forecast**: on the same eight Jan–Aug 2026 months, seasonal-trend WAPE **2.66%**, seasonal-naïve WAPE **5.69%**. Model-selection WAPE (2024–25) was **4.72%**. Average selected signed error **−484.38 million USD** (underprediction).
- **Observed real catalog**: 161 collections, three missing collection image URLs and one missing SEO description in the pinned Week 2 source.
- **Synthetic quality stress-test**: 163 records → 147 sales + 2 returns + 14 quarantine (these are NOT genuine business transactions).
- **World Bank India macro indicators**: observed 2020–25 internet-user share increased 26.59 percentage points; this does NOT establish garment conversion or sales.

## Reproduce the final evidence pack

```bash
python -m pip install -r requirements.txt
python run_analysis.py
python -m unittest discover -s tests -v
```

The scripts read frozen Weeks 1–4 summaries, recompute Week 4 holdout errors from **individual rows**, generate the **evidence-to-action matrix**, a **go/no-go priority plan** and four charts.

Outputs: [`executive_findings.json`](outputs/executive_findings.json), [`evidence_to_action_matrix.csv`](outputs/evidence_to_action_matrix.csv), [`recomputed_holdout_metrics.csv`](outputs/recomputed_holdout_metrics.csv), [`prioritized_decision_plan.csv`](outputs/prioritized_decision_plan.csv) and [`assets/`](assets/).

The project **does not** claim to retrain every prior model: to rerun the original week-specific models, use [Week 3](../Week3_Fashion_Trend_EDA/) and [Week 4](../Week4_Fashion_Forecasting/). Week 6 independently reproduces the *evaluation* and presentation evidence from the stored original predictions.

The U.S. national nominal sales series is *not* an Indian business or local SKU-level demand, and forward scenarios should never be presented as observed revenue. Recommendations are proposed, unmeasured pilots.
