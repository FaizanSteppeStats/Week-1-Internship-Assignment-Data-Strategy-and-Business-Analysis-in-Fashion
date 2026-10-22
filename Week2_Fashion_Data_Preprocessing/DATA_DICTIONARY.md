# Week 2 — Data dictionary and decision rules

**Source:** deterministic, made-up sample fashion orders. It is **not** an employer or published customer dataset.

| Column | Source meaning / type | Decision |
|---|---|---|
| `order_id` | String order reference | Required; never use alone as a deduplication key because orders can have multiple lines |
| `line_id` | Unique order-line key | Required; exact row duplicates quarantined, conflicting duplicate line IDs quarantined |
| `order_timestamp` | Transaction clock | Parsed to UTC; invalid times quarantined. Synthetic source assumed UTC, not a real local timezone |
| `sku` | Apparel item ID | Required; preserve leading zeros; missing quarantined |
| `category` | Product family | Synonyms mapped; unresolved blank quarantined, unknown nonblank retained with explicit category |
| `size` | Apparel size | Normalize S/M/L/XL; unknown becomes `UNKNOWN` + indicator |
| `quantity` | Sold or returned units | Integer; positive sales, negative returns if flagged; mismatches quarantined |
| `unit_price_inr` | **Synthetic INR** unit selling price | Required positive numeric; no invented values |
| `discount_pct` | Discount; input may be 15, 0.15, or 15% | Normalize to 0–1; explicit blank treated as 0 by demonstration assumption |
| `customer_id` | Fictional shopper ID | Missing becomes GUEST; excluded from individual customer features |
| `channel` | Shop/store/app/marketplace | Standardize names; UNKNOWN when other |
| `color` | Item colour | Case/space normalize; UNKNOWN where blank |
| `return_flag` | Return or sale | Separate valid returns from positive sales |

## Output files

- `data/processed/clean_sales.csv`: valid positive sales with `unit_count`, `gross_value_inr`, `net_value_inr`, `order_day`, `year_week`, and flag columns.
- `data/processed/returns.csv`: negative signed-quantity records, retained for return analytics but **not** netted invisibly into sales.
- `data/processed/quarantine.csv`: failing row, CSV source line, machine-readable rejection reason(s).
- `data/processed/weekly_features.csv`: weekly/category units and lagged features computed using **past weeks only**.
- `data/processed/customer_features.csv`: order-line counts/spend by known, non-GUEST IDs.
- `data/processed/quality_audit.json`: SHA-256 source checksum, counts, reconciliation, reasons and policy assumptions.
- `data/processed/quality_comparison.csv`: demonstrative before/after quality indicators.

## Quality policies

- Do not deduplicate by `order_id` alone; fashion orders contain multiple SKUs/sizes.
- Do not impute missing price or SKU: quarantine until investigated.
- Missing discount means **no promotion** only for this controlled teaching fixture; a real feed needs a contract.
- Keep source returns distinct; cancellation is not positive demand.
- Unknown categories/sizes may be analytically meaningful. Preserve unknown flags.
- Do not fit scalers or category encoders on the validation/test split; fit on train only.
- World Bank macro data and Google Trends search interest must never be interpreted as observed SKU sales.
- The optional UCI adapter keeps prices as `unit_price_gbp`; UCI gift retail is a **methodological comparison, not fashion sales**.
