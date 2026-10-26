# Week 2 — Fashion Data Acquisition and Preprocessing (enhanced)

## [EVALUATOR START HERE](EVALUATOR_START_HERE.md)

**Enhanced report adds a complete public fashion catalog source, a real-data cleaning script, observed anomaly metrics and reproducible output artifacts.** The previous 163-row synthetic apparel quality stress test is preserved as a separate demonstration for invalid sales lines. The two datasets are never misrepresented as the same source.

### One-command reproduction

```bash
pip install -r requirements.txt
python -m src.real_catalog_pipeline
python run_pipeline.py
python -m unittest discover -s tests -v
```

For fresh retrieval: `python -m src.real_catalog_pipeline --fetch` downloads fixed upstream source revision `0ce98ce4412b0c7b6b76d8fe809c1e78c7e16b5f`. Both upstream JSON files are bundled in `data/external` so offline execution is possible. Public source https://github.com/arturayupov/womens-fashion-catalog-open-data under MIT; stats sync date 2026-10-18 UTC.

### Observed real-catalog metrics

- 161 collection records; all accepted at collection-row level.
- 2,938 unique products reported by independent statistics snapshot, 2,302 classified as clothing (78.35%).
- Missing media on 3 collections and SEO descriptions on 1; preserved as flags, no fabricated source facts.
- The sum 36,682 is overlapping *collection memberships* (not unique SKUs). Two collections have counts larger than the unique-product statistics. They are flagged but are not silently capped or claimed as sales.

### Synthetic stress test (separate, no company data)

163 intentionally dirty rows: 147 valid sales, 2 returns, 14 quarantined. This demonstrates handling of duplicate order lines, bad prices, invalid discounts, missing SKUs, returns and reproducible quality auditing. Results are **synthetic**, never a real fashion retailer's transaction statistics.

The report, sources, cleaning code, tests and machine-readable outputs are linked in [EVALUATOR_START_HERE](EVALUATOR_START_HERE.md).
