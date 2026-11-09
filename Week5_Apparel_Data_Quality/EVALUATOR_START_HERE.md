# EVALUATOR — WEEK 5: OBSERVED EVIDENCE AND REPRODUCIBILITY

The earlier assessments requested **specific examples, less repetition, more detailed challenges and remedies, and claim-level data support**. This pack addresses those directly.

**Report:** [Week 5 Word report](Week5_Apparel_Data_Quality_Report.docx).

**Run:** [`run_analysis.py`](run_analysis.py) → [`src/quality_assessment.py`](src/quality_assessment.py) + [`src/retail_cleaner.py`](src/retail_cleaner.py).

**Evidence:** [`quality_evidence.json`](outputs/quality_evidence.json), [`quality_control_matrix.csv`](outputs/quality_control_matrix.csv), [rejection register](outputs/retail_issue_register.csv), [quarantined source rows](outputs/retail_processed/quarantine.csv), [real-data YoY review](outputs/fred_outlier_review.csv) and [three figures](assets/).

| Source type | Numeric result | Why it matters |
|---|---:|---|
| **Synthetic apparel order lines** | 163 = 147 accepted sales + 2 accepted returns + 14 quarantined | Every input line conserved; no silent omission |
| **Synthetic critical cells** | 99.63% raw populated → 100% accepted critical fields | Completeness defined with denominator |
| **Real public FRED clothing-sales observations** | 92 months; 0 missing target months or duplicated month keys | Time-series data gate is executable |
| **Real FRED Year-over-year outlier screen** | 16 flags for review | Major historical economic shocks must not be auto-deleted |
| **Automated tests** | 10 passed | Invalid discount, duplicate month and missing month scenarios covered |

Run offline: `python run_analysis.py && python -m unittest discover -s tests -v` after installing requirements. The 163 apparel transactions are **fabricated**; public real-world values come only from the frozen Census/FRED monthly series. No independent truth standard exists for the invented prices or actual employer sales, so the report does **not** claim measured factual accuracy.
