# Week 5 — Data Quality Assessment and Error Handling in Apparel Data

**[EVALUATOR: START HERE](EVALUATOR_START_HERE.md)** | **[Complete Word report](Week5_Apparel_Data_Quality_Report.docx)**

The deliverable is a technical, auditable **data-quality and incident-handling framework** for the fashion and textile domain. It is **not** a claim about any employer's internal sales or an independently verified data-accuracy rate.

## Two independently identified evidence sets

1. **SYNTHETIC apparel order-line stress test (163 rows)** — controlled injected issues; 147 accepted sales, 2 valid returns, 14 quarantined; 100% source-row reconciliation; 10 automated tests.
2. **OBSERVED, PUBLIC clothing-store series (92 months)** — Census Bureau/FRED `MRTSSM4481USN`, Jan 2019–Aug 2026, vintage 15 Oct 2026; 0 missing target months, 0 duplicates; 16 robust year-on-year review flags, never auto-deleted.

The public source is nominal **U.S. dollars, millions, not seasonally adjusted**; it cannot establish the accuracy of Indian retailer inventory. The 163 transaction rows and their INR values are **synthetic**.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run_analysis.py
python -m unittest discover -s tests -v
```

Outputs include [`quality_evidence.json`](outputs/quality_evidence.json), [`quality_control_matrix.csv`](outputs/quality_control_matrix.csv), [`retail_issue_register.csv`](outputs/retail_issue_register.csv), [`quarantine.csv`](outputs/retail_processed/quarantine.csv), [`fred_outlier_review.csv`](outputs/fred_outlier_review.csv) and three original charts in [`assets/`](assets/). The raw synthetic CSV and frozen external CSV are included to reproduce offline.

## Important methodological boundary

Completeness/validity, line-ID uniqueness, and reconciliation are measurable from these files. **Accuracy** requires independent ledger or source-truth checks and is not established by passing validation. U.S. national clothing-store sales are *not* a company-specific price, forecast, SKU or actual stock dataset.

**Public source:** U.S. Census Bureau via [FRED MRTSSM4481USN](https://fred.stlouisfed.org/series/MRTSSM4481USN); snapshots may be revised after the 15 Oct 2026 vintage.
