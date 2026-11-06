# EVALUATOR — Week 4 — Predictive Analytics and Forecasting in Fashion

Real national apparel retail series, 3 candidate forecast methods, strictly chronological 2024/2025 annual-origin folds and a sealed January–August 2026 holdout.

**Open the report:** [Week4_Fashion_Predictive_Analytics_Forecasting_Report.docx](Week4_Fashion_Predictive_Analytics_Forecasting_Report.docx)

**Inspect the Python:** [src/forecast.py](src/forecast.py)

**Reproduce:** `pip install -r requirements.txt`, `python run_analysis.py`, `python -m unittest discover -s tests -v`.

**Verify outputs:** outputs/model_scorecard_overall.csv, outputs/model_scorecard_by_fold.csv, outputs/untouched_2026_holdout.csv, outputs/forward_forecast_scenarios.csv, outputs/forecast_findings.json, and three PNGs in assets/

The primary dataset is a frozen 15 October 2026 FRED table of real published U.S. national clothing sales. No synthetic outcomes are presented as actual company results; interpretation is sector-level, not an Indian shop forecast.
