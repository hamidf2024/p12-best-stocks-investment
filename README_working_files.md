# p12 — Best Stocks for Investment (AI, War & Pandemic Resilience)

Research project to find stocks with a high chance of **at least doubling within 3 years (by Oct 2029)** across
three structural themes: the AI buildout, a multi-theatre war environment, and the risk of a next global pandemic.

As of **October 29, 2026**. Research and education only, not personalized investment advice.

## Main deliverable

| File | What it is |
| --- | --- |
| `reports/AI_War_Pandemic_Stock_Research_v2.1_ML_2026-10-29.pdf` | 24-page report: 117 holdings in 12 categories, financials, rules model + trained ML model, doubling leaderboard |
| `docs/Project_Charter_Plan_Roadmap.pdf` | Project charter, plan, roadmap, risk register, governance ([live doc](https://claude.ai/artifact/J8rDrPfFf5inPMEuanPE3W)) |
| `source/expanded_stock_research_109_investments_2026-10-28.pdf` | Baseline v1 report (ChatGPT, 273 pages, 109 investments) |

## Categories (12 + funds)

| # | Category | Theme | Holdings | Leader (final P 2x) |
| --- | --- | --- | --- | --- |
| 1 | AI semiconductors: compute & foundry | AI | 6 | NVDA 36% |
| 2 | AI memory & semiconductor equipment | AI | 5 | SK hynix 33% |
| 3 | Hyperscalers & AI platforms | AI | 5 | APP 46% |
| 4 | Physical AI & robotics | AI | 16 | SYM 27% |
| 5 | AI power & data-center infrastructure | AI + energy | 6 | VRT 37% |
| 6 | AI software & cybersecurity | AI + cyber | 4 | PLTR 28% |
| 7 | US defense primes & defense electronics | War | 10 | CW 22% |
| 8 | Defense tech, drones & allied rearmament | War | 7 | ONDS 27% |
| 9 | Strategic resources: nuclear fuel & critical minerals | War + AI power | 12 | Lynas 29% |
| 10 | Biotech, pandemic preparedness & AI drug discovery | Pandemic | 13 | REGN 23% |
| 11 | Solar & renewables | Energy transition | 17 | NXT 34% |
| 12 | Fintech & consumer (outside the three themes) | Outside themes | 7 | NU 40% |
| F | Theme funds (ETFs / closed-end) | Diversified | 9 | SMH 27% |

## Models

**Final P(2x) = 50% rules model + 50% trained ML model.**

- **Rules model** (`scripts/model.py`, `scripts/model_data.py`): v1 bear/base/bull scenarios simulated as lognormals,
  plus a fundamentals factor score (growth 30, valuation 20, financial strength 20, theme tailwind 15, downside risk 15).
- **Trained ML model** (`scripts/ml/core.js`): gradient-boosted trees + logistic regression, calibrated.
  - Data: Yahoo Finance monthly total-return prices for every S&P 500 member since 1996 (765 available; 444 delisted
    names missing) plus Shiller market history; 66,010 examples from 690 stocks, start dates 1967–2023.
  - Label: price at least 2x after 36 months. 17 price/market features.
  - Walk-forward tests on unseen years: top 10% of picks doubled 31–34% vs an 18–22% base rate (AUC 0.58–0.63).
    Companion model for a 50%+ loss: AUC 0.75.
  - The pipeline ran in a browser (Yahoo blocks server access); `core.js` is plain JS and also runs in Node
    (`scripts/ml/test.js` is the synthetic-data check).

## Folder layout

```
reports/   final PDF report and charts
docs/      project charter, plan and roadmap
source/    baseline v1 PDF from ChatGPT
scripts/   report builders, rules model, v1 PDF parsers, ML pipeline (scripts/ml)
data/
  v1_extracted/  text and parsed dossiers from the v1 PDF (100 companies)
  model/         rules-model and final blended results per holding (JSON)
  ml/            ML results, S&P 500 membership history, Shiller market series
```

## Rebuild the report

```
pip install reportlab matplotlib pypdf
python scripts/model.py data/v1_extracted/dossiers.json   # rules model -> model_results.json
python scripts/build_v2.py                                # writes the PDF
```
Scripts expect their inputs under `/tmp/outputs` (paths from the build session); adjust the paths at the top of each
script to this folder.

## Known limits

- Survivorship bias in the ML data (delisted companies missing) makes doubling odds look higher and loss odds look
  lower than reality.
- No historical fundamentals were available for training; the rules half covers fundamentals but is not back-tested.
- Probabilities are estimates, not guarantees. Verify prices and filings before acting.
