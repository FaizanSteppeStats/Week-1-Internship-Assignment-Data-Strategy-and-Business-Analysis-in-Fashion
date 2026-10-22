# EVALUATOR — START HERE

**Week 1: Data Strategy and Business Analysis in Fashion — revised evidence pack (22 Oct 2026)**

The earlier evaluator feedback requested **numerical analysis** and **visible Python source**. Both are now directly linked below.

1. **[Improved report — readable in GitHub](Week1_Fashion_Data_Strategy_Improved_Report.md)**: text of the revised 12-page Word report, including concrete examples, KPIs and limitations. Submit the separate improved .docx to the internship portal. The .docx in this repository is the older version.
2. **[Run the full analysis](run_analysis.py)** in one command: `python run_analysis.py`.
3. **[Core case study](src/case_study_analysis.py)**: category sales, forecast comparison, stock replenishment, RFM segment proportions and uncertainty estimates.
4. **[Original generation and model code](src/fashion_strategy_demo.py)**: fixed-seed data, chronological evaluation and original outputs.
5. **[Notebook](Week1_Fashion_Case_Study.ipynb)**: open/run cells for tables and chart; clear outputs also linked below.
6. **[Results overview](outputs/case_study_summary.json)** / [category forecasts](outputs/case_forecast_by_category.csv) / [replenishment](outputs/case_reorder_ranked.csv) / [customer segmentation](outputs/case_segment_shares.csv).
7. **[Automated test](tests/test_case_study.py)**: verify the evidence tables and row counts.

### Selected reproducible results

| Evidence (synthetic illustration only) | Value |
|---|---:|
| Product / weekly observation count | 16 SKUs / 1,248 SKU-weeks |
| Synthetic units sold | 34,131 |
| Baseline versus blend WAPE | 19.09% vs 18.86% |
| Change in overall forecast WAPE | 0.23 percentage points |
| Holdout observations | 153 (39 stockout observations excluded) |
| SKUs flagged for replenishment review | 11 |
| Replenishment units to review | 149 |
| Synthetic customers segmented | 520 |

**Limitation:** The blend performed worse for T-shirts; the paired-week resampling interval includes zero. No actual retailer outcomes or measured campaign uplift are claimed.

### To reproduce

```bash
pip install -r requirements.txt
python run_analysis.py
python -m unittest discover -s tests -v
```
