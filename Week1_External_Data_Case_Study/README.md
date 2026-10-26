# Week 1 external data integration — empirical appendix

This **supplement** addresses evaluator feedback on Submission #166037 (Week 1). It combines **two actual World Bank indicators for India** by country and year, computes a descriptive historical trend, and maps the finding to a proposed fashion-marketing experiment. It does not claim the data prove fashion sales, customer reach, campaign ROI, or that marketing spend should automatically increase.

## What is genuinely external?

- [World Bank Internet usage: IT.NET.USER.ZS](https://api.worldbank.org/v2/country/IND/indicator/IT.NET.USER.ZS?format=json)
- [World Bank urban-population proportion: SP.URB.TOTL.IN.ZS](https://api.worldbank.org/v2/country/IND/indicator/SP.URB.TOTL.IN.ZS?format=json)
- Archived observations for 2020–2025 appear in `data/external/worldbank_india_2020_2025.csv`; source last updated 2026-07-13 at retrieval time. Online `--refresh` queries the source directly and updates the snapshot.
- `outputs/joined_india_external_market_indicators.csv` proves the key-based join; `outputs/external_case_findings.json` separates observed data from assumptions. `outputs/worldbank_india_2020_2025.png` charts both observed series.

## Reproduce

```bash
pip install pandas matplotlib
python src/worldbank_market_integration.py
python -m unittest discover -s tests -v
python src/worldbank_market_integration.py --refresh  # optional network download
```

2020–2025 India Internet usage grew from **43.41% to 70.00%** (+26.59 percentage points); the national urban population share grew from **34.13% to 35.69%** (+1.56 points). These are *national context indicators*, not apparel purchase measurements, and they cannot identify Coimbatore-specific conversions. A proposed mobile-first apparel advertising pilot uses completely assumed inputs: 20,000 impressions, 2.5% CTR, 4% purchase conversion, ₹1,800 basket, ₹12,000 ad spend; this gives 500 clicks, 20 orders, ₹36,000 attributed gross sales and **3.0× illustrative ROAS**. No incremental uplift is claimed. The *decision* is to A/B test a mobile-first campaign while measuring actual retail conversion and geography-specific performance.

### Responsible use

Do not multiply country-wide Internet usage by urbanisation rate as though the two populations were independent. Do not equate Internet use with e-commerce or fashion purchases. Annual indicators alone cannot predict weekly SKU-level inventory. Do not describe scenario assumptions as sourced data.
