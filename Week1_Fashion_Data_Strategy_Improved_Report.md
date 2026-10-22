# REVISED WEEK 1 REPORT — FASHION DATA STRATEGY & BUSINESS ANALYSIS

**Updated 22 October 2026.** This is the GitHub-readable text version of the improved 12-page report. Some diagram formatting is not preserved in the text conversion. The `.docx` in this repository is the original submission; upload the separately provided improved `.docx` to the internship portal. All worked numerical examples use synthetic demonstration data, not a real retailer.



---

## PARSED TEXT FOR PAGE: 1 / 12



RESEARCH + IMPLEMENTATION BLUEPRINT




Fashion Data
Strategy & Business
Analysis
Connecting demand, inventory, trend signals and customer value
for apparel and textile businesses.




 ASSIGNMENT                           PERIOD                                 SUBMISSION
 Junior Data Science Analyst — Week
                                      13 Oct – 19 Oct 2026                   Revised 22 Oct 2026
 1
 Internship: Coimbatore, Tamil Nadu   13 Oct – 24 Nov 2026                   Word report + code evidence


DOCUMENT PURPOSE
An independently executable six-week plan that identifies strategic questions, measurable KPIs, public data
sources, modelling approaches, responsible-use safeguards, resources, and assessment criteria. The companion
GitHub-ready project provides reproducible sample analyses using synthetic data—not claims about any
employer.


Report version 1.1 | Expanded quantitative evidence     |    Prepared for academic evaluation      |   Public-data-
first



---

## PARSED TEXT FOR PAGE: 2 / 12



                                                                            FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY




Executive summary
Apparel businesses face a recurring tension: buying or making enough of the right product, size and colour
while limiting unsold stock, markdowns and avoidable resource use. In 2026, the State of Fashion research
highlights changing consumer preferences, trade volatility and AI-enabled operating improvements [1]. Tamil
Nadu’s integrated textile and knitwear ecosystem makes these questions particularly relevant to a Coimbatore-
centred learning case [2][3].

This report recommends starting with three practical decision systems: (1) size-level sales forecasting and
reorder review, (2) early detection of apparel search-interest changes, and (3) permission-aware customer
segmentation and campaign testing. A fourth, longer-horizon workstream connects return reasons, product
attributes and traceability to circularity. The proposed first milestone is a reproducible proof of concept; not an
enterprise data platform.

Because no internal company files are assumed available, the independent demonstration uses synthetic orders
and sales, public research, downloadable Google Trends samples, and sources that are clearly marked as
conditional or third-party licensed. Actual business improvements must be validated on authorised real data
before decisions are automated.

 PRIORITY                                  MANAGEMENT QUESTION                       FIRST DECISION OUTPUT
                                           Which SKU / size is at risk of missing    Weekly SKU demand scorecard and
 01 Demand & stock
                                           demand or becoming aged stock?            reorder review queue
                                           Which garment types or colours            Trends watchlist, not an automatic
 02 Trend intelligence
                                           show sustained emerging interest?         buy signal
                                           Who may benefit from useful,              Aggregate customer groups and
 03 Customer growth
                                           relevant outreach?                        controlled campaign test
                                           Where are returns and material            Reason-code quality checks and
 04 Circularity (phase 2)
                                           losses concentrated?                      traceability checklist


Status: strategic plan plus demonstration only. No internal company access, live retailer forecast or claimed revenue
improvement is assumed.



1. Sector context and business case
1.1 Why analytics matters in fashion
Fashion differs from generic retail because many variants of one style compete for constrained stock; collection
life cycles are short; preferences change across seasons, occasions and regions; and unsold merchandise loses
value as new assortments arrive. A useful data strategy must therefore operate at style–colour–size–channel–
week granularity while preserving an aggregated view for managers.

The 2026 McKinsey/Business of Fashion outlook identifies technology adoption, shifting consumer priorities
and trade uncertainty as strategic pressures [1]. For the regional context, the Tamil Nadu Department of
Handlooms describes a substantial knitwear and garment industry around Tiruppur and an interlinked textile
value chain [2]. A 2026 Tamil Nadu circular-textile pathway emphasises traceability, resource efficiency and
better coordination along the chain [3]. These observations justify the business problem; they do not supply a
measured baseline for a particular company.

1.2 Decision hierarchy
 DECISION HORIZON                          USE CASE                                  INFORMATION REQUIRED
                                           Reallocate sizes, identify stockouts,     Available-to-sell units, sell-through,
 Daily / weekly
                                           launch small replenishment review         lead times, recent sales
                                                                                     Forecast errors, promotion effects,
                                           Adjust category allocation, discount
 Monthly                                                                             gross margin, incremental campaign
                                           depth and acquisition mix
                                                                                     lift




                                      Independent learning report • 22 Oct 2026 | Page 2



---

## PARSED TEXT FOR PAGE: 3 / 12



                                                                           FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



 DECISION HORIZON                      USE CASE                                   INFORMATION REQUIRED
                                       Review assortment gaps, supplier           Historical cohort demand, return
 Seasonal / quarterly                  exposure and waste-reduction               reasons, supplier data, traceability
                                       actions                                    evidence




2. Objectives, hypotheses and research questions
 OBJECTIVE / PRIORITY                  TESTABLE BUSINESS QUESTION                 HYPOTHESIS / DECISION RULE
                                       Can a transparent SKU-level                Use walk-forward tests. Promote
 A. Improve demand planning |          baseline forecast outperform or            only if error reduction is stable
 Highest                               match naive recent-sales estimates         across categories and stockout
                                       on unseen weeks?                           artefacts are monitored.
                                                                                  Rank reorder candidates; require
                                       Which SKUs need review given
 B. Reduce inventory friction |                                                   human confirmation until costs and
                                       forecast demand, on-hand stock,
 Highest                                                                          lead-time distributions are
                                       lead time and service risk?
                                                                                  available.
                                       Do persistent search changes lead          Compare search indices with lagged
 C. Detect emerging trends |
                                       category demand by two to eight            category sales; retain a signal only
 Medium
                                       weeks?                                     when it beats a sales-only baseline.
                                                                                  Randomised holdout, report
                                       Do permission-aware RFM
 D. Improve marketing efficiency |                                                incremental conversions and gross
                                       audiences respond better than
 Medium                                                                           contribution, not click-through
                                       undifferentiated campaigns?
                                                                                  alone.
                                                                                  Start with coded return reasons and
                                       Which product attributes or
 E. Enable circularity | Longer                                                   credible material-provenance fields;
                                       suppliers correlate with avoidable
 term                                                                             do not infer sustainability from a
                                       returns and waste?
                                                                                  marketing label.


Scope assumption: a hypothetical small/midsize apparel retailer or brand connected to the Tamil Nadu textile
ecosystem. Manufacturer-only businesses can substitute finished-goods demand with purchase orders, fabric
yield, defect rate and on-time-in-full shipments.


3. KPI framework: definitions, baselines and success gates
Every KPI needs a single formula, consistent reporting grain, a baseline period, a data steward and a response
action. Proposed targets below are pilot thresholds, not measured current performance or guaranteed gains.

 KPI                                   DEFINITION / UNIT                          PILOT DECISION THRESHOLD
                                       SKU–week rows with valid date, SKU,
                                                                                  At least 95% completeness; duplicate
 Data completeness                     units and price / required SKU–week
                                                                                  key below 1%; flag exceptions
                                       rows
                                       100 × sum(|actual − forecast|) /           Stretch goal: at least 10% relative
 Forecast WAPE                         sum(actual), for nonzero actual total;     WAPE reduction versus naive baseline
                                       percent                                    on out-of-time test
                                       SKU–store–day observations with
                                                                                  Target +3 percentage points only after
 In-stock rate                         sellable stock / all eligible SKU–store–
                                                                                  reliable daily stock data exists
                                       day observations
                                       Net units sold / (opening units +          Track by collection and age;
 Sell-through                          received units) for defined cohort;        investigate slow movers, no universal
                                       percent                                    target
                                       Units (or value) older than locally        Pilot goal: reduce aged-stock value
 Aged-stock share                      chosen collection-age threshold / total    10% relative after matched cohort
                                       units (or value)                           measurement
                                       Returned units / shipped units on          Report by reason and size; first
 Return rate
                                       aligned order cohort; percent              objective is reliable reason coding




                                  Independent learning report • 22 Oct 2026 | Page 3



---

## PARSED TEXT FOR PAGE: 4 / 12



                                                                               FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



 KPI                                       DEFINITION / UNIT                          PILOT DECISION THRESHOLD
                                                                                      Run holdout test; scale only if lift
                                           (Treatment conversion rate − control
 Incremental campaign lift                                                            exceeds noise and contribution covers
                                           conversion rate) and gross margin lift
                                                                                      spend
                                           Customer acquisition cost =
                                                                                      Secondary guardrail; never treat clicks
 Attribution / cost                        attributable acquisition spend / new
                                                                                      or attributed ROAS as causal lift
                                           customers


WAPE is undefined when total actual demand is zero. Low-demand SKUs should be evaluated in aggregated groups as well as
individually. Stockouts censor observed sales, so sales alone can understate true demand.


Target ownership and frequency
An analyst should issue weekly demand / data-quality scorecards and a monthly customer-learning summary.
In a future company pilot, merchandising owns stock decisions, marketing owns campaign design, operations
validates lead times, and an appointed data steward signs off on definitions. In the internship demonstration,
the student plays the analyst and documents these roles without requiring company participation.


4. Data inventory: public-first and future company inputs
 SOURCE / ACCESS                           WHAT IT CONTRIBUTES                        LIMITATION / SAFE USE
                                           Relative search interest by term, date     Normalised 0–100, not search volume
 Google Trends / manual CSV export
                                           and geography; examples: cotton            or direct purchase intent;
 [4][5]
                                           kurta, oversized T-shirt                   time/location comparisons need care.
                                           Cluster background, value chain,
 Tamil Nadu public textile sources                                                    Sector context only; cannot substitute
                                           circularity priorities and policy
 [2][3]                                                                               for local store transaction data.
                                           context
                                           Past temperature or rainfall features      Free service is non-commercial; check
 Open-Meteo archive [6][7]                 to test weather-sensitive category         current terms and commercial licence
                                           hypotheses                                 before business deployment.
                                                                                      Account and rules acceptance
                                           Fashion article metadata and time-
                                                                                      required; large download,
 H&M Kaggle competition [8]                stamped purchases for separate
                                                                                      competition-specific licence; do not
                                           methodology experimentation
                                                                                      redistribute.
                                           General transaction structure,
                                                                                      Not an apparel dataset; historic UK gift
 UCI Online Retail [9]                     cancellation handling and RFM
                                                                                      retailer; transfer learning only.
                                           teaching example
                                           Complete offline reproducibility of
                                                                                      Demonstrates code mechanics only; no
 Locally generated synthetic CSVs          forecast, reorder and customer-
                                                                                      commercial conclusions.
                                           segmentation examples
                                           POS, e-commerce orders, stock              Not accessible in this task; require
 Future authorised company data /
                                           snapshot, receipts, returns,               permission, security, business
 conditional
                                           promotions, cost and consent               definitions and privacy review.



Minimum analytical data schema
The recommended fact table key is (week_start, SKU, sales_channel, location) with `units_sold`, `units_returned`,
`selling_price`, `promotion_flag`, `in_stock_exposure`, `beginning_inventory`, `receipts` and `inventory_on_hand`.
A product dimension maps SKU to style, category, size, colour, fabric, season and supplier. Future marketing
tables should contain pseudonymised customer IDs, consent flags, event timestamps and campaign costs, stored
separately from directly identifying details.

Validation rules: reject negative non-return sales, invalid dates and impossible sizes; deduplicate the declared
composite key; reconcile sales plus returns with order-line evidence; distinguish cancellations from fulfilled
orders; store currency and tax treatment; flag impossible inventory balances; capture snapshot dates; and log
missingness by channel and category. Use ISO dates and UTF-8 consistently.




                                     Independent learning report • 22 Oct 2026 | Page 4



---

## PARSED TEXT FOR PAGE: 5 / 12



                                                                         FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY




5. Analytics and business-action design
5.1 Inventory optimisation and demand forecasting
1.   Prepare weekly item-level sales, stock availability, returns, promotions and any order cancellations. Split
     chronologically; retain the most recent 12 weeks for evaluation.
2.   Benchmark seasonal-naive (same period in prior cycle) or rolling-four-week mean against transparent
     candidates: 4/8-week blend, exponential smoothing or category pooling when sparse.
3.   Compare WAPE by category and by full portfolio; inspect systematic bias, high-demand items, promotions,
     newly launched styles and weeks with stockouts. Do not apply a random train/test split.
4.   Build a decision queue: reorder point = expected demand during supplier lead time + safety stock. Include
     minimum order quantity, supplier capacity, margin, obsolescence risk and return-adjusted demand as data
     becomes available.
5.   Human reviewer approves a small trial; track realised fill rate, stock value and forecast drift weekly. Stop
     automatic proposals if missing stock data or abnormal trends make the recommendation unreliable.
Action example: if a size is trending up but has limited sellable stock, review allocation and replenish
cautiously; if an end-of-season style has weak sell-through and excess stock, test smaller markdowns before
ordering more. Estimated lost sales should be treated as an assumption unless customer demand beyond stock
limits can be observed.

5.2 Trends and assortment intelligence
Create a stable dictionary of apparel terms grouped by category, fit, fabric, colour and occasion; export
comparable weekly Google Trends series for India or relevant cities [4][5]. Standardise geography and window
before comparing terms. Apply four-week smoothing and track sustained changes rather than one-off spikes.
Combine search indices with seasonality, holidays, weather (where terms allow) and product lead times. Back-
test lag correlations on prior weeks and compare against a sales-only baseline before assigning a “watch” or
“validate” status.

Output: a 10–20-term watchlist with direction, confidence, time window, source link and owner. Example
question: does interest in cotton kurtas rise ahead of demand in a given region? The search index can generate
an investigation; it cannot alone justify supplier orders or infer absolute market size.

5.3 Customer marketing and retention
With consented, authorised transaction records, compute recency, frequency and monetary value. Create
understandable groups such as loyal repeat buyers, reactivation candidates and growth-potential buyers; test
cross-selling or useful product information through channels customers have chosen. Use a randomised
holdout and measure incremental conversions, attributable gross margin and opt-outs. Report results
separately from platform-reported return on ad spend (ROAS), which can over-attribute sales. Avoid profiling
protected or sensitive characteristics and do not purchase dubious identity datasets.

5.4 Returns, responsible sourcing and circularity
As a future extension, normalise return reasons (fit, quality, damaged, style mismatch), and link them to size
guide, garment attributes and production batch when authorised. The 2026 Tamil Nadu circular-textile
pathway calls attention to traceability and resource efficiency [3]. A responsible analytics objective is therefore
verifiable lower waste and clearer provenance, not unsubstantiated sustainability scores.


6. Technical demonstration and honest interpretation
The companion GitHub-ready code repository contains reproducible Python, a README, two automated tests
and generated CSV/PNG outputs. It creates 78 weekly periods for 16 imaginary SKUs and 520 imaginary




                                   Independent learning report • 22 Oct 2026 | Page 5



---

## PARSED TEXT FOR PAGE: 6 / 12



                                                                            FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



customers; it does not download, scrape or reveal business records. The forecast evaluation uses the final 12
weeks, expands the training history one week at a time and excludes flagged stockout test weeks.

 SYNTHETIC DEMONSTRATION
                                           OBSERVED OUTPUT                          WHAT IT MEANS / DOES NOT MEAN
 MEASURE
                                                                                    Baseline error on fictional uncensored
 Four-week moving mean WAPE                19.09%
                                                                                    holdout sales only
                                                                                    A small synthetic difference; not proof
 4/8-week blend WAPE                       18.86%
                                                                                    of real-world superiority
                                                                                    Eligible observations after excluding
 Evaluated SKU–weeks                       153
                                                                                    flagged test stockouts
                                                                                    Illustrative reorder screening with
 Replenishment review list                 11 of 16 SKUs
                                                                                    invented on-hand quantities
                                                                                    Demonstrates segmentation logic, not
 RFM customer coverage                     520 simulated customers
                                                                                    campaign uplift




Figure 1. Forecast-model comparison on generated sample data (seed = 42). Both methods are tested on fictional sales only.
Source: included Python project.

Interpretation: the blend edges the simple baseline on this seed, but the difference is small and neither passes
the proposed 10% relative improvement threshold. A responsible project would retain the simpler baseline or
continue testing rather than imply a demonstrated business gain. Past training-period stockouts can still
depress observed demand; the example does not model price elasticity, supply constraints or causal
promotions.

6.1 Worked case study: design and validation boundary
The following tables and figures are computed from the executable Python files accompanying this report. A
deterministic seed creates 78 weekly observations per SKU for 16 fictional apparel SKUs (4 categories × 2
colours × 2 sizes), totalling 1,248 SKU-weeks, plus 2,374 fictional order records from 520 customers. All amounts
are INR and all outcomes are SYNTHETIC; they are evidence that the analytical method runs, not evidence that
a real brand earned or saved money.

Data-quality and exposure check: 34,131 units are marked as sold with a notional listed-price gross value of INR
51,174,969. 1,986 units are recorded as returned (5.8% of sold units), and 214 of 1,248 SKU-weeks (17.1%) are
stockout-flagged. Listed-price gross value is NOT recognised/net revenue or margin: it is before returns and any
realised discounts. Stockout-flagged sales are censored, not true demand.




                                     Independent learning report • 22 Oct 2026 | Page 6



---

## PARSED TEXT FOR PAGE: 7 / 12



                                                                              FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



6.2 Concrete category analysis: sales, stockouts and returns
 Apparel category         Units sold                Listed-price gross        Stockout SKU-weeks        Return-unit rate
                                                    value (INR)


 ACTIVE                   6,173                     9,253,327                 55/312                    5.99%

 DENIM                    6,960                     16,001,040                45/312                    5.95%

 KURTA                    8,312                     15,784,488                62/312                    5.50%

 TSHIRT                   12,686                    10,136,114                52/312                    5.87%

Business interpretation: synthetic T-shirts contribute the most units (12,686), while denim generates high listed-
price value because of its higher price point. Kurta shows the highest stockout-flagged SKU-weeks (62 out of
312). A merchandising analyst would investigate these categories first, but should not infer the cause of a
stockout from this table alone; supplier delays, distribution, assortment and promotions require separate
evidence.

6.3 Forecast experiment: actual calculations and cautious decisions
Experiment design: the last 12 calendar weeks are reserved as an out-of-time test; the model predicts each SKU-
week only from preceding weeks. Forecast rows with stockout flags are excluded from the test because
observed sales may understate demand. That leaves 153 evaluated SKU-weeks and 39 excluded test SKU-weeks.
WAPE = 100 × SUM(|actual units − predicted units|) / SUM(actual units) over the included rows.

 Category                 Evaluated SKU-            4-week WAPE               4/8-week blend            Change (pp)
                          weeks                                               WAPE


 ACTIVE                   33                        21.18%                    20.99%                    +0.19

 DENIM                    42                        23.24%                    22.74%                    +0.49

 KURTA                    39                        16.94%                    16.27%                    +0.67

 TSHIRT                   39                        17.03%                    17.26%                    -0.23

Positive percentage-point change means the blend has lower error. Weighted across all evaluated rows, the
four-week baseline WAPE is 19.09% and the four-/eight-week blend WAPE is 18.86%, an absolute difference of
only 0.23 percentage points (about 1.2% relative reduction in error). The blend loses on T-shirts: 17.26% versus
17.03% baseline. A simple paired resampling of the 12 test weeks gives an illustrative 95% range of −0.36 to
+0.83 percentage points for the blend improvement; it crosses zero. Therefore the result is not robust evidence
to replace the baseline, and it is not a production claim.




            Figure 2. Forecast error by apparel category and prioritized replenishment reviews; all values synthetic.




                                       Independent learning report • 22 Oct 2026 | Page 7



---

## PARSED TEXT FOR PAGE: 8 / 12



                                                                          FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



Recommended decision: retain the four-week mean as a transparent champion until a longer external holdout
shows consistent reduction in stockout-adjusted error by product family. Add promotion, price, calendar,
returns, local weather and availability features only after establishing data provenance. A production
dashboard would display SKU-week actuals, predictions, WAPE, bias and 80%/95% prediction intervals.

6.4 Inventory use case: worked reorder-point calculation
Rule (illustrative): reorder point = ceiling[2 × mean weekly units over 8 weeks + 1.65 × sample standard
deviation of last 8 weeks × √2]. The two-week lead time and safety multiplier of 1.65 are assumed, not sourced
from an actual supplier. Review units = MAX(0, reorder point − simulated on-hand). This does not include open
purchase orders, shelf minimums, pack sizes, or desired order-up-to coverage.

 SKU                          2-week reorder point            Demo on-hand                 Units for human review


 TSHIRT-BLACK-L               79                              49                           30

 TSHIRT-NAVY-L                80                              55                           25

 DENIM-NAVY-L                 58                              36                           22

 DENIM-BLACK-L                48                              29                           19

 KURTA-NAVY-L                 60                              44                           16

Worked SKU example: TSHIRT-BLACK-L averages approximately 29.0 units/week. Two weeks of expected sales
are about 58 units. Adding approximately 20 units of estimated safety stock gives a reorder point of 79 units
after ceiling the unrounded underlying calculations. With 49 fictional units on hand, the review gap is 79 − 49 =
30 units. Across all 16 SKUs, 11 receive REVIEW flags, totalling 149 illustrative units; that total is NOT an
authorised purchase recommendation or a proven stockout reduction.

6.5 Trend signal and marketing example
Illustrative seasonal hypothesis: synthetic Kurta weekly SKU-level units averaged 22.25 in August–September
2025 and 29.69 in October–November 2025, a descriptive increase of 33.4%. This fits a plausible festive-season
hypothesis but does NOT establish causal demand growth: simulated promotions and stock availability differ
by period. Before acting, compare equivalent weeks across at least two years and validate against Google
Trends relative search indices, holiday dates, price and actual available-to-sell stock.

 RFM audience                 Customers                       Share of customers           Synthetic spend share


 Growth potential             191                             36.7%                        36.7%

 Loyal                        97                              18.7%                        29.3%

 Occasional                   103                             19.8%                        17.1%

 Reactivation candidate       129                             24.8%                        17.0%

Decision example: prioritise opt-in, permission-respecting retention experiments for 129 fictional reactivation
candidates rather than emailing all 520 customers indiscriminately. Assign a random holdout group and track
incremental conversion and gross margin after campaign cost and returns. RFM is descriptive segmentation; it
does not establish that an offer improves retention, revenue or lifetime value.

6.6 Reproducibility, limitations and evaluation checklist
Evidence chain: data/synthetic_weekly_sales.csv + data/synthetic_orders.csv → src/fashion_strategy_demo.py →
outputs/walk_forward_predictions.csv / forecast_scores.csv / replenishment_suggestions.csv /
rfm_segment_summary.csv → src/case_study_analysis.py → outputs/case_*.csv, case_study_summary.json,
case_study_decisions.png → Week1_Fashion_Case_Study.ipynb → report tables. An evaluator can open the
precomputed files without running code or reproduce them from the repository root.


                                    Independent learning report • 22 Oct 2026 | Page 8



---

## PARSED TEXT FOR PAGE: 9 / 12



                                                                            FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



Run: pip install -r requirements.txt; python src/fashion_strategy_demo.py; python src/case_study_analysis.py;
python -m unittest discover -s tests -v. No business accounts, credentials or internal company datasets are
required. Dependencies, sample data, generated outputs and tests are included at the root of the linked GitHub
repository.

Validity gates: (1) verify unique SKU × week keys; (2) remove no rows without explanation; (3) protect time-
series ordering; (4) distinguish stockout-censored observed sales from latent demand; (5) retain baseline if
change is within error uncertainty; (6) obtain real point-in-time inventory and product costs before making
purchase decisions; (7) run controlled consented marketing tests before claiming incremental results. The case
study is suitable as a training demonstration, not as statistical proof of a real apparel strategy.


7. Six-week implementation roadmap and resource plan
The roadmap aligns with the six-week internship period beginning Tuesday, 13 October 2026. Since the
submission window ends on 24 November, technical work is staged through 23 November with a final
review/upload checkpoint on 24 November. Actual assignment completion is not asserted by this plan.

 WEEK / DATES                           WORK PACKAGE                               OUTPUT + ACCEPTANCE GATE
                                        Research 2026 sector trends, frame         Strategy DOCX, question matrix, risk
 1 | 13–19 Oct                          decisions and assumptions; document        list and repository outline; evaluator
                                        public sources; define KPI dictionary.     can follow the plan.
                                        Acquire allowed public samples;
                                        create synthetic schema and                Data dictionary + clean example CSVs;
 2 | 20–26 Oct
                                        validations; document source               completeness and schema checks pass.
                                        permissions.
                                        Establish demand baselines, walk-
                                                                                   Forecast error table, code, method
 3 | 27 Oct–2 Nov                       forward tests, stockout flags and
                                                                                   note and human-review rubric.
                                        indicative reorder queue.
                                        Compare Google Trends terms by             Trend watchlist and a documented
 4 | 3–9 Nov                            stable windows; explore external           sales-only comparison; no “prediction”
                                        features and leakage.                      based solely on searches.
                                                                                   Customer group summary,
                                        Perform synthetic RFM and plan a
 5 | 10–16 Nov                                                                     randomised holdout design and
                                        privacy-aware marketing experiment.
                                                                                   contribution metric.
                                        Integrate charts, examine limitations,     Readable GitHub repository, validated
 6 | 17–23 Nov                          test scripts and prepare final             outputs, final report and assessment
                                        explanation.                               checklist.
                                                                                   Word document uploaded to
                                        Check filenames, document length and
 Close | 24 Nov                                                                    internship portal; real public GitHub
                                        upload requirements.
                                                                                   URL supplied if required.



Resources, effort and budget assumptions
Personnel: one junior analyst/student for approximately 8–10 hours per week (48–60 hours across six weeks),
with no compulsory company reviewer. Technology: Python 3, pandas, NumPy, Matplotlib, Word-compatible
DOCX tools, a free GitHub repository and locally generated CSVs. Baseline software cost is ₹0 for permitted
educational use on an existing computer; electricity, device, network, and any chosen paid services are
excluded. H&M data access is optional and subject to rules. Live commercial uses of an API or data feed require
a separate licence and budget check.

Dependencies: internet access for public reading/CSV exports, computer with Python, and permission to
publish code. If optional sites are unavailable, use included synthetic files. To move from demonstration to real
operations, the organisation would need to provide transaction and stock data, define replenishment authority,
and authorise data governance.




                                   Independent learning report • 22 Oct 2026 | Page 9



---

## PARSED TEXT FOR PAGE: 10 / 12



                                                                           FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



Decision gates
 GATE                                    PASS CONDITIONS                            IF NOT MET
                                         Key schema validates; sources and          Use synthetic schema and document
 Data ready                              licences recorded; no personal             gap; do not make operational
                                         identifiers exposed                        recommendations
                                         Out-of-time error, stockout exclusions     Keep transparent baseline; review
 Forecast ready
                                         and category performance reported          data and additional history
                                         Human owner, inventory and cost            Restrict output to educational ranking
 Pilot ready
                                         data, review trail and monitoring exist    only
                                         Consent and opt-out workflows;
                                                                                    Do not send campaigns or make causal
 Marketing ready                         randomised control and contribution
                                                                                    claims
                                         metric




8. Risks, mitigations and ethical safeguards
 CHALLENGE                               POTENTIAL FAILURE                          MITIGATION / OWNER
                                         Missing sizes or transactions produce      Validate grain, log missingness; analyst
 Data gaps and silos
                                         inaccurate demand                          pauses unreliable segments
                                                                                    Use stock availability/exposure; skip
                                         Observed sales understate actual desire
 Stockout censoring                                                                 censored validation points; operations
                                         to buy
                                                                                    review
                                                                                    Borrow category and similar-style priors;
 Cold-start styles                       New SKUs lack historical demand
                                                                                    lower confidence and order smaller
                                         Historic relationship breaks during        Rolling backtests, drift alerts and event
 Changing season and promotions
                                         festival or markdown                       annotations; merchandising review
                                         Future promotions used to predict past     Time-based splits, frozen holdout,
 Selection / leakage bias
                                         sales or test tuned repeatedly             timestamped feature availability
                                         Normalised Trends score confused with      Attribute source, compare same
 Misinterpreting search interest
                                         total shoppers                             windows; treat as leading hypothesis [5]
                                                                                    Minimise/pseudonymise data; opt-out
                                         Unconsented tracking or discriminatory
 Customer privacy and fairness                                                      and retention controls; marketing
                                         targeting
                                                                                    steward
                                         Attributed ROAS mistaken for               Randomised control, incremental gross
 Confounded campaigns
                                         incremental sales                          contribution and uncertainty interval
                                         Competition data or non-commercial API     Document terms; use synthetic fallback;
 Source licensing / costs
                                         used beyond permission                     procure commercial permissions [7][8]
                                         “Green” labels imply evidence that does    Collect traceability proof; show missing
 Unverified sustainability claims
                                         not exist                                  values; avoid unsupported scores




9. Evaluation, deliverables and conclusion
Evaluator-facing completion checklist
 EXPECTED DELIVERABLE                                           PROOF INCLUDED OR PLANNED
                                                                This DOCX: sector rationale, objectives, analytics logic,
 Detailed Word-format strategy, >200 words
                                                                governance and roadmap
                                                                Sections 2 and 3: explicit decisions, metric formulas and
 Business questions and KPIs
                                                                tentative gates
                                                                Section 4 and sources [1]–[9], including access and
 External research and data sources
                                                                licence caveats
                                                                Section 5: decision framework, validation plan and
 Inventory, forecasting and marketing analysis
                                                                limitations
                                                                Companion Python code, synthetic CSV, result charts,
 Executable technical evidence
                                                                README and passing tests
                                                                Sections 7 and 8, including dated phases, effort and
 Action plan, resources and mitigation
                                                                contingencies
 Submission description of at least 200 words                   Companion Submission_Description.txt ready to paste



                                    Independent learning report • 22 Oct 2026 | Page 10



---

## PARSED TEXT FOR PAGE: 11 / 12



                                                                       FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY



 EXPECTED DELIVERABLE                                      PROOF INCLUDED OR PLANNED
                                                           Repository files prepared; user must publish to GitHub
 GitHub URL for technical internship
                                                           to obtain genuine live URL


Conclusion. The recommended strategy is intentionally modest in technology but ambitious in decision clarity:
unify product-level definitions, measure forecast and stock outcomes, treat trend data as contextual evidence,
and test marketing actions incrementally. Its value lies in connecting repeatable measurement to operational
choices while keeping methodological uncertainty visible. A public-data-first demonstration can be completed
independently; a real business rollout should occur only after data access, ownership and decision rights are
established.




                                 Independent learning report • 22 Oct 2026 | Page 11



---

## PARSED TEXT FOR PAGE: 12 / 12



                                                                            FASHION DATA INTELLIGENCE / WEEK 1 STRATEGY




References and access notes
Source review date: 15 October 2026. Source titles and URLs are supplied for evaluator verification; external pages may
change. Background figures on older government pages should not be represented as October 2026 market observations.
[1] McKinsey & The Business of Fashion (17 Nov 2025). The State of Fashion 2026: When the Rules Change. Global industry
outlook. View original source
[2] Government of Tamil Nadu, Department of Handlooms. Textile sector background, knitwear / garment ecosystem and
Tiruppur context. View original source
[3] Government of Tamil Nadu / Tamil Nadu Green Climate Company (2026). Reweaving the Circular Transition: A
Pathway for Sustainable Circular Textiles in Tamil Nadu. View original source
[4] Google Trends Help. Export, embed and cite Trends data; export is available as CSV. View original source
[5] Google Trends Help. FAQ on normalised relative search-interest indices (0–100). View original source
[6] Open-Meteo. Historical Weather API data documentation. View original source
[7] Open-Meteo. Terms and licence distinction between educational/non-commercial free API and commercial use. View
original source
[8] H&M / Kaggle. Personalized Fashion Recommendations dataset; sign-in, competition terms and file sizes apply. View
original source
[9] UCI Machine Learning Repository. Online Retail benchmark: non-fashion transactional dataset for methods practice.
View original source



Appendix A. Transition from demonstration to a real pilot
An independent demonstration becomes a real decision-support tool only after the organisation supplies
permissioned data and identifies a person responsible for the outputs. The following handover checks prevent
a prototype from being mistaken for operational automation.

 REPLACE OR APPROVE                                             CONDITION FOR REAL-WORLD USE
                                                                Load authorised SKU–store–day sales, returns, stock and
 Synthetic demand and on-hand
                                                                product master data; reconcile inventory movements.
                                                                Use verified supplier lead-time history, minimum order
 Lead-time assumptions
                                                                quantities, purchase costs and review cycles.
                                                                Document permitted data uses, retention limits, customer
 Source licences and consent
                                                                contact choices and commercial feed terms.
                                                                Set a real baseline, evaluate the next 8–12 weeks out of time
 Performance thresholds
                                                                and record gross-margin / availability trade-offs.
                                                                Assign business approvers; keep an audit log and disable
 Human ownership
                                                                any decision automation on data-quality failure.


Reproducibility: run the repository command in README.md and compare outputs/kpi_summary.json with the technical-
demonstration values in Section 6. A different random seed will change all synthetic outcomes.




                                     Independent learning report • 22 Oct 2026 | Page 12