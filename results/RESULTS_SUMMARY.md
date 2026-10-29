# Results summary — Project 12 (v2.1, 29 Oct 2026)

**Question:** which stocks have the best chance of at least doubling by October 2029?
A double needs about 26% compound annual price gain. The S&P 500 managed that in only 3 of 48 three-year windows (6%).

**Universe:** 117 investments = 100 companies from ChatGPT's v1 report + 8 v2 additions (MSFT, PLTR, CEG, PANW, TMO, ABT, GILD, MRNA) + 9 funds, in 12 categories plus a fund group.

## How each stock is scored

Final P(2x) = 50% trained ML model + 50% rules model (v1 scenarios + financial score, FS 0–100).

| ML model | Value |
|---|---|
| Algorithms | Gradient boosting + logistic regression, calibrated (`model/core.js`) |
| Training cases | 66,010 five-year windows (71,530 three-year), 690 stocks, start years 1967–2023 |
| Features | 17 price-history features (volatility, momentum, drawdown, beta, stock age, market trend) |
| Walk-forward test (unseen years) | Top 10% doubled 30.5% / 33.6% / 30.7% of the time vs base rates 22.0% / 21.7% / 18.4% (folds 2001–05, 2009–14, 2016–23) |
| Ranking power | AUC 0.58–0.63 for doubling (weak); 0.75 for losing half (much stronger) |
| Known limits | No historical fundamentals; 444 of 1,209 candidate tickers (mostly delisted) unavailable → survivorship bias |

## Tiers

| Tier | Rule | Stocks |
|---|---|---|
| **A** (6) | Final P(2x) ≥ 30%, FS ≥ 70, ML loss risk ≤ 15% | NU, NVDA, AVGO, TSM, PDD, GOOGL |
| **B** (8) | Final P(2x) ≥ 30%, higher risk | APP, VRT, SKHY (SK hynix), MU, AMD, NXT, TOYO, SOFI |
| **C** (17) | Final P(2x) 25–29% | e.g. QCOM, FSLR, Lynas, META, AMSC, ARRY, PLTR, SYM, MSFT, ONDS |

## Top 10 by final P(2x)

| # | Ticker | Category | Final P(2x) | ML P(−50%) |
|---|---|---|---|---|
| 1 | APP | Hyperscalers & AI Platforms | 46% | 31% |
| 2 | NU | Fintech & Consumer | 40% | 8% |
| 3 | VRT | AI Power & Data-Center | 37% | 21% |
| 4 | NVDA | AI Semiconductors | 36% | 9% |
| 5 | AVGO | AI Semiconductors | 35% | 13% |
| 6 | NXT | Solar & Renewables | 34% | 20% |
| 7 | SKHY | AI Memory & Equipment | 33% | 41% |
| 8 | SOFI | Fintech & Consumer | 33% | 15% |
| 9 | TSM | AI Semiconductors | 32% | 8% |
| 10 | MU | AI Memory & Equipment | 32% | 36% |

The best score is about 46%: no stock is close to a sure double.

## 12 categories

| # | Category | Theme | Holdings | Avg P(2x) | Best candidate |
|---|---|---|---|---|---|
| 1 | AI Semiconductors: Compute & Foundry | AI | 6 | 31% | NVDA 36% |
| 2 | AI Memory & Semiconductor Equipment | AI | 5 | 28% | SK hynix 33% |
| 3 | Hyperscalers & AI Platforms | AI | 5 | 31% | APP 46% |
| 4 | Physical AI & Robotics | AI | 16 | 20% | SYM 27% |
| 5 | AI Power & Data-Center Infrastructure | AI + energy security | 6 | 26% | VRT 37% |
| 6 | AI Software & Cybersecurity | AI + cyber war | 4 | 22% | PLTR 28% |
| 7 | US Defense Primes & Defense Electronics | War | 10 | 19% | CW 22% |
| 8 | Defense Tech, Drones & Allied Rearmament | War | 7 | 22% | ONDS 27% |
| 9 | Strategic Resources: Nuclear Fuel & Critical Minerals | War + AI power | 12 | 21% | Lynas 29% |
| 10 | Biotech, Pandemic Preparedness & AI Drug Discovery | Pandemic | 13 | 19% | REGN 23% |
| 11 | Solar & Renewables | Energy transition | 17 | 23% | NXT 34% |
| 12 | Fintech & Consumer (outside the 3 themes) | Outside themes | 7 | 28% | NU 40% |

Source: `reports/AI_War_Pandemic_Stock_Research_v2.1_ML_2026-10-29.pdf` (24 pages). Research and education only, not investment advice.
