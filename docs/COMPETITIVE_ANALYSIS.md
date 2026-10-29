# Benchmark — Project 12 (Best Stocks for Investment)

Prepared 2026-10-29. Purpose: compare Project 12's approach with the stock-rating services and
funds an investor could use instead, and list what to add next. Project 12 asks one question:
**which stocks have the best chance of at least doubling by October 2029?**

Vendor performance figures are each vendor's own claims (or a reviewer's summary of them). They
weren't independently tested here, and most measure something different from a 3-year double.

## 1. Competitive landscape

| Competitor | Type | Method | Reported performance (vendor's own figures) | Cost |
|---|---|---|---|---|
| **Zacks Rank** | Quant rating, 1–5 | Earnings-estimate revisions and EPS surprises only | #1 Strong Buys +23.82%/yr vs +11.58% for the S&P 500 since 1988 (equal-weighted, rebalanced monthly; the page also says "since 1998" in its FAQ) | Free rank; Zacks Premium paid |
| **Seeking Alpha Quant Ratings** | Quant rating, Strong Sell → Strong Buy | Value, growth, profitability, momentum and estimate-revision grades vs sector | Univ. of Kentucky study, 2016–2022: Strong Buys returned 1.92%/month equal-weighted (~25.6%/yr) and 1.48%/month value-weighted; alpha remained after Fama-French + momentum controls (as reported by Seeking Alpha) | Seeking Alpha Premium paid |
| **Danelfin AI Score** | ML rating, 1–10 | Thousands of technical, fundamental and sentiment features per stock; predicts beating the market over **3 months** | "Best Stocks" strategy +191% vs +118% for the S&P 500, Jan 2017–Aug 2023; 10/10 stocks +14.69% annualized alpha | Free tier; paid plans |
| **Motley Fool Stock Advisor** | Analyst picks | 2 new picks a month, buy-and-hold 5+ years | +993% vs +208% for the S&P 500 cumulative since 2002 (as of May 2026) | $199/yr ($99 first year) |
| **Morningstar** | Analyst ratings | Fair value, economic moat, uncertainty | Star ratings are a valuation signal, not a return forecast | Morningstar Investor paid |
| **Theme ETFs** (e.g. SMH semis, ITA defense, BOTZ robotics) | Passive funds | Hold the whole theme by index weight | Market return of each theme, minus a small fee | ~0.35–0.70%/yr expense ratio |

## 2. Where Project 12 stands

| Capability | Project 12 | Commercial services | Gap / edge |
|---|---|---|---|
| Target | P(stock at least doubles in 3 years), plus P(loses half) | Beat the market over 1–3 months (Zacks, Danelfin) or "buy" ratings | **Different and harder target**, matched to the owner's goal. Ratings don't say how likely a double is. |
| Model testing | Walk-forward on unseen years (3 folds, 2001–2023); top 10% doubled 31–34% vs 18–22% base rate; AUC 0.58–0.63; loss model AUC 0.75 | Long track records published by the vendors themselves | **Honest but short.** Ours is tested out-of-sample but hasn't been run live yet. |
| Training data | 66,010 cases, 690 stocks, 1967–2023; price history only | Decades of fundamentals, estimates and sentiment | **Behind.** No historical fundamentals; most delisted stocks missing (survivorship bias). |
| Fundamentals | Financial score (FS) per stock from v1 dossiers + v2 checks, 50/50 blend with ML | Fully automated, refreshed daily | **Behind on freshness**, ahead on hand-read context. |
| Theme coverage | 117 holdings in 12 categories built around AI, war and pandemic risk | Whole market; themes only via ETFs | **Ahead** for this specific thesis. |
| Risk view | Explicit P(−50%) per stock and a concentration warning (categories 1–6 share the AI capex cycle) | Ratings rarely show downside probability | **Ahead.** |
| Cost | Claude subscription only | ~$100–$500/yr per service | **Ahead.** |

## 3. Suggested additions (not yet started)

1. **Cross-check against ratings.** For every Tier A/B stock, record its Zacks Rank, Seeking Alpha Quant
   rating and Danelfin score at each quarterly refresh; flag any pick that all three rate Sell.
2. **ETF baseline.** Track SMH, ITA, BOTZ and the S&P 500 alongside the Tier A basket so the project
   can show whether stock picking beat simply owning the theme.
3. **Live paper track record.** Freeze the Oct 29, 2026 tiers and measure them every quarter to Oct 2029.
4. **Add historical fundamentals** (e.g. SEC XBRL data) to the ML features and include delisted stocks
   to cut survivorship bias.

## Sources

- Zacks Rank, about and performance — https://www.zacks.com/zrank/about_zrank_inds.php
- Seeking Alpha, University of Kentucky study summary — https://seekingalpha.com/article/4683185-university-of-kentucky-study-finds-seeking-alpha-quant-ratings-beat-the-market-sa-quant
- Danelfin, AI Score and strategy figures — https://danelfin.com/
- Motley Fool Stock Advisor review (StockAnalysis) — https://stockanalysis.com/article/motley-fool-stock-advisor-review/
