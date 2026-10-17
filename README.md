# Fashion Data Strategy | Junior Data Science Analyst Internship, Week 1

**Scope:** a documented, implementable data strategy for apparel, textiles and fashion, with a runnable offline demo of demand forecasting, inventory prioritisation and customer segmentation.

**Data transparency:** all files in `data/` and `outputs/` are generated from **synthetic data** with a fixed random seed. No real fashion brand, customer, store or manufacturing performance is asserted. The demonstration is **not a validated business deployment**. An actual pilot would need transaction histories, true inventory snapshots, product master data, cost information and permission to use any personal data.

## Repo contents

- `src/fashion_strategy_demo.py`: generates 78 weeks of sales for 16 fictitious SKUs, then runs transparent baseline/candidate forecasts, indicative reorder calculations and RFM segmentation of 520 fictitious customers.
- `tests/test_metrics.py`: unit and integration checks.
- `data/`: synthetic input CSVs.
- `outputs/`: example output CSVs, PNG charts, and a summary JSON.
- `Week1_Fashion_Data_Strategy_Report.docx`: assessment report.
- `Submission_Description.txt`: report description (over 200 words).

## Run the code

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/fashion_strategy_demo.py
python -m unittest discover -s tests -v
```

The script overwrites its synthetic files for a reproducible baseline. The default seed is 42. All output files are written relative to the working directory. For another reproducible sample, run `python src/fashion_strategy_demo.py --seed 91`.

## How the analytics work

1. **Demand:** expanding-history, rolling one-step predictions for each SKU on the final 12 weeks, skipping test weeks flagged as stockouts. Compare an uncomplicated four-week mean with a 55/45 blend of four- and eight-week means using WAPE. The forecasts use only weeks before the prediction date. Excluding out-of-stock weeks avoids treating censored test sales as full demand; training may still be censored, a limitation to correct before deployment.
2. **Replenishment:** `reorder point = lead-time demand + 1.65 x rolling sample std dev x sqrt(lead-time weeks)`. The on-hand balances are **artificial demo values**, and the suggested quantity is `max(0, reorder point - demo on-hand)`. This is a simplified first pass (not a service-level guarantee, purchasing order, or lead-time distribution model).
3. **Marketing:** recency, frequency and monetary (RFM) grouping with clear rule-based segments to explain potential campaign audiences. Any experiments should assess incremental outcomes with a control group, permission and unsubscribe safeguards; aggregate RFM is not incremental lift.

## Methodology and caveats

- Real sales can be censored by out-of-stocks and impacted by returns, holidays, prices, promotions and channel mix. These are not fully disentangled here.
- Synthetic results cannot substantiate financial benefits, forecast accuracy for a real retailer, ROI or target achievement.
- Forecast champion selection should be based on out-of-time holdout performance and stability, not just synthetic WAPE. Never randomly split time series or tune on the test period.
- Google Trends is a *relative index* and is not a substitute for actual sales volume; respect source terms and attribution. H&M Kaggle competition data requires login and acceptance of the competition rules; do not copy its restricted files into this repository.
- There is no real customer personal data in this project. For live operations, restrict access, pseudonymise identifiers and set a retention policy.

## Data-source research links

- [BoF/McKinsey, State of Fashion 2026](https://www.mckinsey.com/industries/retail/our-insights/state-of-fashion)
- [Tamil Nadu Department of Handlooms textile sector](https://www.tnhandlooms.tn.gov.in/english/sectortext?t=1)
- [Tamil Nadu circular textile transition report (2026)](https://tngcc.tn.gov.in/wp-content/uploads/2026/07/Reweaving-the-Circular-Transition-A-Pathway-for-Sustainable-Circular-Textiles-in-Tamil-Nadu.pdf)
- [H&M Personalized Fashion Recommendations competition](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data)
- [Google Trends: export and cite data](https://support.google.com/trends/answer/4365538?hl=en)
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- [UCI Online Retail (general retail, not apparel-specific)](https://archive.ics.uci.edu/dataset/352/online+retail)

## Suggested GitHub publishing steps

Sign into GitHub, create a **public** repository such as `fashion-data-strategy-week1`, and upload the files at the root of this folder (or use `git init`, `git add .`, `git commit -m "Week 1 fashion data strategy"` and push to a GitHub remote). Copy the live repository URL into the internship form. Do **not** enter an example or invented URL. Make sure the Word report is also uploaded to the internship portal directly.
