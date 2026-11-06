# Project 12 Research Program: finding better models for the 3-year doubling goal

Version 1.0 · Nov 6, 2026 · Owner: Hamid (sponsor) · Research lead: Claude
Built from the ChatGPT "Develop New AI Architecture" conversation (two development paths, five factors) and adapted
to Project 12. The structure is reusable for any financial market (stocks, Forex, options): only the settings in
section 7 change.

## 1. Research goal

Find a model that ranks stocks by their chance of **at least doubling within 36 months** better than our current
model, while flagging stocks likely to **lose half**. Better means a fair, out-of-sample improvement on the metrics
below, not a better-looking backtest.

## 2. Current baseline (EXP-000, frozen Oct 29, 2026)

| Item | Value |
| --- | --- |
| Model | 50% rules model (scenarios + fundamentals score) + 50% trained ML (gradient-boosted trees + logistic regression, calibrated) |
| Training data | 66,010 cases, 690 S&P 500 stocks, start dates 1967–2023, 17 price/market features |
| Doubling AUC (walk-forward, 3 eras) | 0.58 / 0.60 / 0.63 |
| Top-10% hit rate vs base rate | 31–34% vs 18–22% (~1.6x) |
| Loss model (P halves) AUC | 0.75 |
| Known weaknesses | Survivorship bias (444 delisted names missing); no point-in-time fundamentals; rules half not back-tested; weights hand-set |

Every new model is compared against EXP-000 on the same data, splits and budget.

## 3. Two development paths

**Path A, original design:** start from a problem in our data and invent a mechanism to solve it.
**Path B, combine strengths:** benchmark existing model families, document pros and cons, and build a combination
that keeps each one's strengths. Both paths share one evaluation protocol (section 5), so results are comparable.

| Factor | Path A: original design | Path B: combine existing strengths |
| --- | --- | --- |
| 1. Define success | Same goal, metrics, risk limits, data and compute budget for both paths (section 4) | Same, plus practical limits on adapting existing models (licensing, data each one needs) |
| 2. Build a baseline | EXP-000 plus simple baselines: momentum rank, low-volatility rank, random | Benchmark each candidate family on our task; record strengths and weaknesses (section 6) |
| 3. Hypothesis | A mechanism aimed at a specific failure, e.g. "doubles cluster after market drawdowns, so condition stock signals on market regime" | A specific combination that covers individual weaknesses, e.g. "price-based ML + point-in-time quality fundamentals" |
| 4. One change at a time | Add each mechanism alone; measure its contribution (ablation) | Add or remove each borrowed component alone; compare to its source models and a simple average |
| 5. Refine and scale | Keep mechanisms that help across eras; enlarge data or model only when evidence supports it | Drop components that add nothing; scale the combinations that survive |

Originality is checked in both paths: an idea developed independently may already be published, and a combination
needs evidence of a real added contribution.

## 4. Definition of success (factor 1)

| Metric | Why | Promotion threshold vs EXP-000 |
| --- | --- | --- |
| Doubling AUC, each walk-forward era | Ranking quality | +0.02 or more in at least 2 of 3 eras, no era worse by more than 0.01 |
| Top-decile hit rate / base rate | What we actually use: the best-ranked names | Higher in at least 2 of 3 eras |
| Brier score and calibration curve | Percentages shown on the site must mean what they say | Not worse |
| Loss-model AUC | Avoiding halving | Not worse |
| Basket test: equal-weight top decile, rebalanced yearly, vs S&P 500 | Turns predictions into an investable result | Higher 3-year return with max drawdown no worse than 10 points deeper |
| Compute and data cost | Must run on free or owned data and a laptop/GPU | Documented |

A result that meets thresholds on the validation eras still has to pass the untouched holdout (section 5).

## 5. Shared evaluation protocol (factor 4, both paths)

1. **Point-in-time data only.** Every feature uses information available on the prediction date (filing dates, not
   fiscal period ends). Labels look 36 months ahead.
2. **Walk-forward splits with a 36-month embargo** between training end and test start, so no label overlaps.
   Eras: test 2001–05, 2009–14, 2016–23 (same as EXP-000).
3. **Untouched holdout.** Predictions made on Oct 29, 2026 are logged and scored in Oct 2029 (true live test). For
   faster feedback, a historical holdout era is chosen before experiments start and opened only once per frozen design.
4. **Survivorship.** Results are reported with and without delisted companies once delisted data is available.
5. **Multiple testing.** Every experiment is logged in `experiments.csv`, including failures. Report how many
   variants were tried; prefer improvements that hold in every era over the single best run.
6. **Repeatability.** At least 3 random seeds per model; report the spread.
7. **Costs.** Basket tests include 0.10% per trade (stocks); Forex/options settings in section 7.

## 6. Path B candidate model families (initial review)

| Family | Strengths | Weaknesses for our goal | Use in Project 12 |
| --- | --- | --- | --- |
| Gradient-boosted trees (current) | Strong on tabular data, fast, interpretable | Needs good features; no time structure | Keep as baseline component |
| Factor models (momentum, value, quality, low volatility) | Decades of evidence, simple, transparent | Factors weaken once crowded; linear | Features and simple baselines |
| Earnings-revision / analyst signals | Historically predictive of medium-term returns | Data is mostly paid; short horizon | Optional if a data source is found |
| Time-series Transformers (e.g. PatchTST, Temporal Fusion Transformer) | Learn patterns across long price histories; TFT handles mixed inputs | Data-hungry; easy to overfit monthly data | Path A/B experiment on long histories |
| Survival / time-to-event models | Predict *when* a stock doubles, use partial outcomes from recent listings | Less common in finance; needs careful censoring | Path A candidate: time-to-2x |
| Commercial scores (Zacks Rank, Seeking Alpha Quant, Danelfin) | Track records published by vendors | Closed methods; mostly short horizons | External benchmark only (see COMPETITIVE_ANALYSIS.md) |

## 7. Reusable settings for other markets

| Setting | Stocks (Project 12) | Forex | Options |
| --- | --- | --- | --- |
| Target | P(price ≥ 2x in 36 months), P(≤ 0.5x) | P(move ≥ k·ATR in horizon) | P(position return ≥ target) or expected value after premium |
| Horizon | 36 months, monthly data | Minutes to weeks | Days to expiry |
| Costs | 0.10% per trade | Spread + swap | Bid–ask, commissions, early-assignment risk |
| Main leakage risks | Restated fundamentals, survivorship | Timezone/session alignment | Implied-volatility surface timing |

## 8. Decision gates

| Gate | Passes when | Decision |
| --- | --- | --- |
| R1 Plan | Experiment card filled: hypothesis, single change, metrics, budget | Approve to run |
| R2 Validation | Thresholds in section 4 met on validation eras with 3 seeds | Freeze design |
| R3 Holdout | Frozen design holds on the holdout | Candidate for production |
| R4 Adoption | Sponsor approves; report and website switch to the new model, change logged | Becomes new baseline (EXP-000 archived) |

## 9. Research backlog (first cycle)

| ID | Path | Hypothesis | Data needed | Status |
| --- | --- | --- | --- | --- |
| R-01 | B | Adding point-in-time fundamentals (growth, margins, leverage, share dilution from SEC XBRL filings) to the ML model raises top-decile hit rate | SEC EDGAR company facts (free) | Planned |
| R-02 | A | A regime gate (market drawdown and valuation level) that changes how stock signals are weighted improves AUC in every era | Existing data | Planned |
| R-03 | A | A survival model of time-to-2x uses recent listings better and improves calibration | Existing data | Planned |
| R-04 | B | Replacing hand-set rules weights with weights learned on back-testable proxies improves the blend | R-01 data | Planned |
| R-05 | Both | Delisted companies reduce measured doubling odds; quantify survivorship bias | Delisted price history (source to find) | Data search |
| R-06 | Both | Live tracking: score the Oct 2026 predictions each quarter | Prices only | Running |

Data for every item: `DATA_SOURCES.md` (added 2026-11-06).

## 10. Cycle and roles

A research cycle takes about 4–6 weeks: plan (gate R1) → run and log experiments → validation review (R2) → holdout (R3)
→ adoption decision (R4). Claude designs, runs and logs experiments and writes the results; the sponsor approves gates.
After each cycle the workflow rule applies: local folder → GitHub → website (Research section).

## Files

- `experiments.csv`: registry of every experiment (append-only)
- `templates/EXPERIMENT_CARD.md`: fill one per experiment before running it
- `templates/MODEL_REVIEW.md`: Path B pros/cons review of an existing model
- `templates/GATE_REVIEW.md`: decision record for gates R2–R4

This is research, not investment advice. No model guarantees returns.
