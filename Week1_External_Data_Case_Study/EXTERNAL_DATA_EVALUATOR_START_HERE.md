# WEEK 1 — NEW EVIDENCE RESPONSE TO SUBMISSION #166037

The evaluator asked for **specific examples of external data sources integrated into the strategy**, with concrete, measurable case studies. This public evidence pack adds both.

## Open these artifacts

1. [Expanded 14-page Word report](../Week1_Fashion_Strategy_External_Evidence_Enhanced.docx) — includes Appendix B: verified external-data join, quantitative comparison, sources, visual and marketing test design.
2. [Actual source records](data/external/worldbank_india_2020_2025.csv) — 12 **observed** figures from 2 World Bank indicators, not generated values.
3. [Joined observations](outputs/joined_india_external_market_indicators.csv) — complete 2020–2025 country-year join.
4. [Reproducible source code](src/worldbank_market_integration.py) — optional API refresh, numeric validation, missing/duplicate rejection, year-aligned join, chart and illustrative case.
5. [Machine-readable results](outputs/external_case_findings.json) and [chart](outputs/worldbank_india_2020_2025.png).
6. [Five passing tests](tests/test_worldbank_integration.py).

## Measured versus hypothetical

**Verified public statistics:** World Bank India Internet usage increased from **43.41% in 2020** to **70.00% in 2025** (+**26.59 percentage points**); the urban population share rose from **34.13%** to **35.69%** (+**1.56 points**). Country-year join has 6 complete rows, 2 measures each.

**Assumed fashion marketing example:** 20,000 ad impressions × 2.5% CTR = 500 clicks × 4% conversion = 20 orders × ₹1,800 AOV = ₹36,000 revenue; ₹12,000 assumed spend gives **3.0× illustrative ROAS**. This is an *unmeasured planning scenario*, not achieved performance.

**Decision:** Run a limited, controlled mobile-first apparel landing-page pilot; measure actual regional conversion, return-adjusted gross revenue and incremental profitability before scaling. National Internet adoption does not establish fashion demand, Coimbatore purchase rates, causality or ROI.

## Reproduce offline

```bash
pip install pandas matplotlib
python src/worldbank_market_integration.py
python -m unittest discover -s tests -v
```

Append `--refresh` to download the source directly via the World Bank API (requires network), replacing the saved snapshot. No employer data required.
