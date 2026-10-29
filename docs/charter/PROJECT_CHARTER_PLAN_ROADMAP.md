# AI, War & Pandemic-Resilience Stock Research — Project Charter, Plan & Roadmap

Oct 29, 2026 · @Tony

## Executive summary

This project builds and maintains a ranked, evidence-based watchlist of public companies positioned for three structural forces as of late October 2026: the AI infrastructure buildout, a multi-theatre war environment (Iran, Russia-Ukraine, Indo-Pacific build-up), and the risk of a next global pandemic. The output is a categorized research report (PDF) covering 12 investment categories, refreshed quarterly against company filings.

The starting point is the prior ChatGPT research, which grew to a 109-investment PDF with Financial Strength (0–100) and Price–Fundamentals Balance scores. That report was organized by sector request rather than by theme, its doubling percentages were unvalidated, and ChatGPT itself said balance-sheet coverage was inconsistent. This project re-categorizes those holdings into 12 categories, refreshes figures with Q3 2026 results, and adds a consistent scoring model.

Market backdrop at launch: the S&P 500 closed at 7,744 on Oct 28, 2026, near records, with the 10-year Treasury above 5%, the Fed funds rate at 3.75–4.00% after a September hike, oil above $100, and US midterm elections on Nov 3. AI fundamentals remain very strong (Nvidia guided $108B for its October quarter; TSMC guided Q4 to about +58% y/y), but hyperscaler free cash flow is under strain and defense stocks have de-rated despite record backlogs.

**Important:** this is research and education, not personalized investment advice. Claude is not a licensed financial advisor. Scores are judgment-based screens, not return forecasts. Verify prices and filings before acting, size positions to your own risk tolerance, and consider a licensed advisor.

## Project charter

| Item | Definition |
| --- | --- |
| Project name | AI, War & Pandemic-Resilience Stock Research (P-AIWP) |
| Sponsor / decision owner | You (the investor) |
| Research lead | Claude (analysis, data refresh, report production) |
| Start date | Oct 29, 2026 |
| Baseline report | expanded\_stock\_research\_109\_investments\_2026-10-28.pdf (ChatGPT) |
| Review cadence | Monthly watchlist check; full refresh after each earnings season |

**Purpose.** Identify the strongest listed companies in 12 categories that benefit from AI adoption, sustained high defense spending, and pandemic preparedness, and keep that view current as evidence changes.

**Objectives**

1. Define 12 investment categories without overlap: 10 covering the AI, war and pandemic themes, plus 11 Solar & Renewables and 12 Fintech & Consumer.
2. Select 3–5 leaders per category using one transparent 100-point scoring model.
3. Re-categorize all 109 investments from the baseline PDF into the new structure, keeping prior Financial Strength and Price–Fundamentals Balance scores where still valid.
4. Refresh every top pick with its latest quarterly results (Q3 2026 season) and cite the filing.
5. Publish an updated PDF report plus this charter, plan and roadmap.

**In scope:** US-listed equities (NYSE, Nasdaq) and major foreign leaders available as ADRs or on home exchanges; theme ETFs as diversification alternatives; fundamentals, valuation, catalysts and risks.

**Out of scope:** personalized allocation advice, options and leverage strategies, trade execution, tax planning, private companies (e.g., pre-IPO AI labs).

**Deliverables**

| # | Deliverable | Format | Status |
| --- | --- | --- | --- |
| D1 | Project charter, plan and roadmap | This doc | Done |
| D2 | 12-category framework + scoring models | This doc, section 3 | Done |
| D3 | Updated categorized research report | PDF | Done (v2.1 with trained ML model, 24 pages) |
| D4 | Quarterly refresh of scores and catalysts | PDF revision | Recurring |

**Success criteria**

- Every top pick has a cited source dated within the last 120 days.
- Each of the 109 baseline holdings is assigned to exactly one of the 12 categories (or the fund group).
- Scores are reproducible: another reader applying the rubric lands within ±10 points.
- The report states the bear case for every top pick, not only the bull case.

**Constraints:** public information only; prices move daily, so valuation figures are as of the report date; some non-US defense leaders (Rheinmetall, BAE) are not on US exchanges.

**Assumptions:** AI capex stays elevated through 2027 (hyperscalers guide group capex above $1 trillion next year); NATO's 5%-of-GDP-by-2035 target holds; H5N1 remains a low-probability, high-impact human pandemic risk.

## Investment framework: 12 categories and scoring model

The project's main goal is to find stocks with a high chance of at least doubling by October 2029, which needs about 26% compound annual price gain. All 117 holdings (100 from v1, 8 v2 additions, 9 funds) sit in 12 categories (1–10 for the AI, war and pandemic themes, 11 Solar & Renewables, 12 Fintech & Consumer) plus a fund group, and each gets a model probability of a 2x outcome.

| # | Category | Theme | Holdings | Best doubling candidate (final P 2x) |
| --- | --- | --- | --- | --- |
| 1 | AI semiconductors: compute & foundry | AI | NVDA, AVGO, TSM, AMD, QCOM, AMBA | NVDA (36%) |
| 2 | AI memory & semiconductor equipment | AI | MU, SK hynix, ASML, KLAC, TER | SK hynix (33%) |
| 3 | Hyperscalers & AI platforms | AI | GOOGL, AMZN, META, MSFT, APP | APP (46%) |
| 4 | Physical AI & robotics | AI | ISRG, SYK, SYM, TSLA, FANUC, Keyence + 10 more | SYM (27%) |
| 5 | AI power & data-center infrastructure | AI + energy security | VRT, GEV, ETN, CEG, NEE, AMSC | VRT (37%) |
| 6 | AI software & cybersecurity | AI + cyber war | PLTR, CRWD, PANW, ZS | PLTR (28%) |
| 7 | US defense primes & defense electronics | War | LMT, RTX, NOC, GD, LHX, CACI, DRS + 3 more | CW (22%) |
| 8 | Defense tech, drones & allied rearmament | War | AVAV, KTOS, RCAT, ONDS, Rheinmetall, BAE, Elbit | ONDS (27%) |
| 9 | Strategic resources: nuclear fuel & critical minerals | War + AI power | CCJ, BWXT, MP, Lynas, FCX + 7 more | Lynas (29%) |
| 10 | Biotech, pandemic preparedness & AI drug discovery | Pandemic | REGN, TMO, ABT, GILD, MRNA, TEM + 7 more | REGN (23%) |
| 11 | Solar & renewables | Energy transition | NXT, FSLR, ENPH, ARRY, ENLT, TOYO + 11 more | NXT (34%) |
| 12 | Fintech & consumer (outside the three themes) | Outside themes | NU, SOFI, TBBK, MELI, PDD, CELH, LULU | NU (40%) |

**Doubling-prediction model (ensemble)**

| Component | How it works | Weight in rules model |
| --- | --- | --- |
| Scenario simulation | Bear / base / bull 3-year price multiples (v1 scenarios, 25/50/25), each a lognormal with 25% volatility; adjusted for Q3 results after v1's cutoff | 50% |
| Fundamentals factor model | Doubling Potential Score: growth 30, valuation headroom 20, financial strength 20, theme tailwind 15, downside risk 15; mapped to probability with a capped logistic | 50% |
| Tiers | Applied to the final score (50% rules + 50% trained ML model). A: 30%+, FS 70+, ML loss risk 15% or less · B: 30%+ otherwise · C: 25–29% · D: 18–24% · E: under 18% | — |

**Update (v2.1): trained machine-learning model.** The rules model is now blended 50/50 with a model trained on 66,010 historical cases (690 stocks, 1967–2023 start dates, Yahoo Finance monthly prices). In walk-forward tests on unseen years, its top 10% of picks doubled 31–34% of the time versus an 18–22% base rate (AUC 0.58–0.63); a companion model predicts 50%+ losses (AUC 0.75). Final leaders: APP 46%, NU 40%, VRT 37%, NVDA 36%, AVGO 35%.

Six names reach Tier A on the final score (30%+ chance of doubling, Financial Strength 70+, loss risk 15% or less): NU 40% (Category 12), NVDA 36%, AVGO 35%, TSM 32%, PDD 32% (Category 12) and GOOGL 31%. The highest scores with higher risk are APP 46%, VRT 37% and NXT 34% (Category 11). Read the ranking as more reliable than the absolute percentages.

## Project plan

The work runs in five phases; phases 1–3 finish with the first report, and phases 4–5 repeat every quarter.

1. **Discovery and baseline (week 1).** Import the 109-investment PDF; extract each ticker, prior scores and notes; flag stale data.
   - Gate G1: every baseline row parsed and assigned an ID.
2. **Framework and categorization (week 1).** Fix the 12 categories and the scoring models; map each baseline holding to one category or the fund group.
   - Gate G2: no holding in two categories; legacy list explained.
3. **Deep research and scoring (weeks 1–2).** Pull Q2/Q3 2026 results from SEC filings and company releases; score top candidates; write bull, base and bear cases.
   - Gate G3: every top pick has a filing citation under 120 days old.
4. **Report production (week 2).** Build the categorized PDF: summary tables per category, company pages, risk matrix, appendix of all holdings.
   - Gate G4: page-by-page visual check; numbers re-checked against sources.
5. **Monitoring and refresh (ongoing).** Track catalysts, re-score after each earnings season, log changes.
   - Gate G5: change log published with each revision.

**Roles**

| Activity | You (sponsor) | Claude (research lead) |
| --- | --- | --- |
| Approve categories and rubric | Decide | Propose |
| Data gathering and scoring | Review | Do |
| Position sizing and trades | Decide and do | Not involved |
| Quarterly refresh trigger | Request | Do |
| Final sign-off on report | Approve | Deliver |

**Open items for you**

- [ ] Attach the baseline PDF (ChatGPT's share page blocks file access) so all 109 rows carry over exactly.
- [ ] Confirm whether non-US listings (Rheinmetall, BAE) are investable in your brokerage account.
- [ ] Choose a review day each month.

## Roadmap

The first report ships in Phase 1 (now through Dec 31, 2026); each later quarter re-scores the list after earnings season and closes with a published revision.

&#91;embedded content: 12-month roadmap · 4 phases, 4 gates\]

Phase 1 is highlighted because it is underway; dates for Phases 2–4 move with each company's reporting calendar.

## Risk register

The biggest risk to this watchlist is concentration: categories 1–6 all depend on the same AI capex cycle, so a capex pause would hit half the list at once.

| Risk | Likelihood | Impact | Hits categories | Early signal | Mitigation |
| --- | --- | --- | --- | --- | --- |
| AI capex slowdown or "payback" sell-off | Medium | High | 1–6 | Alphabet FCF negative $9.1B in Q3; Microsoft trimmed capex to $170B | Cap AI categories at a set share of the watchlist; favor names with backlog (GEV, VRT) and cash (MSFT) |
| Higher-for-longer rates | Medium | High | 1, 3, 4, 5 | 10-yr above 5%; Fed hiked in Sept, December hike priced | Weight the price–fundamentals factor; avoid 100x+ P/E names |
| Memory price reversal | Medium | High | 2 | DRAM contract prices; SK hynix supply commentary | Treat MU's \~6x forward P/E as cyclical, not cheap |
| Taiwan Strait crisis | Low | Very high | 1, 2 | PLA exercises, export-control news | TSM is single-point risk; pair with ASML / US fabs |
| Defense budget cuts after Nov 3 midterms | Medium | Medium | 7, 8 | House control result; FY27 appropriations | Prefer backlog-heavy primes (LMT $292B, RTX $340B) over program-dependent names |
| Ceasefire or peace deals (Iran, Ukraine) | Low–Medium | Medium | 7, 8, 9 | Negotiation headlines | Backlogs take years to burn; restocking continues after wars |
| Pandemic never arrives | High | Low–Medium | 10 | WHO still rates H5N1 public risk low | Choose companies that grow without a pandemic (TMO, ABT, GILD) |
| Single-binary biotech events | Medium | High | 10 | Trial readouts, FDA actions | Size MRNA-type names small; it rose 600%+ in 2026 on one trial |
| Export controls on chips | Medium | Medium | 1, 2 | Commerce rules | Nvidia already guides with zero China data-center revenue |
| Data and AI-tool error in this research | Medium | Medium | All | Figures that conflict across sources | Cite primary filings; re-check before any decision |

## Governance, review rules and KPIs

A holding moves only on evidence written into the change log, never on price action alone.

**Review rules**

- **Upgrade** to top pick: score reaches 70+ and the latest quarter beat and raised guidance.
- **Downgrade** to watch: score falls below 60, guidance cut, or the thesis-defining contract or trial fails.
- **Remove**: fraud, restatement, going-concern warning, or the company leaves the theme.
- **Theme check** each quarter: if a theme's driver weakens (e.g., hyperscaler capex guidance falls two quarters in a row), cut that category's weight in the report.
- **Diversification guide**: keep any single category to a stated cap of the watchlist so no one theme dominates; ETFs (e.g., ITA for US defense, CIBR-type cyber funds) are listed as lower-risk alternatives.

**Delivery workflow (standing rule from the sponsor, Oct 29, 2026).** After completing any request in this project, Claude finishes in this order:

1. **Local GitHub folder first:** save all relevant information and data to `~/Documents/GitHub/p12-best-stocks-investment` (reports, docs, data, scripts, results, chat notes), updating `README.md`, `CHANGELOG.md` and the checksum manifest.
2. **Website section second:** update the related part of the live page source, `website/project-12.html`, in the same folder.
3. **GitHub and website, automatic:** the sponsor commits and pushes the folder to [hamidf2024/p12-best-stocks-investment](https://github.com/hamidf2024/p12-best-stocks-investment) with GitHub Desktop; the workflow `sync-website.yml` then publishes the page to hamidf2024.github.io/stocks-investment/project-12.html.

A request is not complete until all three steps are done, or a step that could not be done is reported with the reason.

**KPIs for the project**

| KPI | Target |
| --- | --- |
| Top picks with filing cited within 120 days | 100% |
| Baseline holdings categorized | 109 of 109 |
| Report refresh after earnings season | Within 3 weeks of the last top-pick report |
| Bear case written per top pick | 100% |
| Watchlist vs S&P 500 (tracking only, not a promise) | Reported each quarter |

## Sources

- [Baseline ChatGPT conversation](https://chatgpt.com/share/6ae35a35-c880-83e8-aea8-858d8aafa7b6)
- [NVIDIA Q2 FY2027 results (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm)
- [Nvidia Q2 takeaways and $108B guide (CNBC)](https://www.cnbc.com/2026/08/26/nvidia-nvda-earnings-report-q2-2027-live-updates.html)
- [Broadcom Q3 FY2026 results (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/0001730168/000173016826000076/avgo-08022026x8kxex99.htm)
- [TSMC Q3 2026 results (SEC 6-K)](https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000726/a3q26e_withguidancexfinal.htm)
- [ASML Q3 2026 presentation (SEC 6-K)](https://www.sec.gov/Archives/edgar/data/0000937966/000162828026065813/a2026_10x14xpresentation.htm)
- [Micron valuation and FQ4 2026 results](https://www.top1markets.com/news/micron-stock-memory-supercycle-hbm-valuation)
- [Alphabet Q3 2026 results (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm)
- [Hyperscaler capex and FCF, Oct 29 2026 (CNBC)](https://www.cnbc.com/2026/10/29/microsoft-google-ai-capex-estimates.html)
- [Palantir Q2 2026 results and guidance (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/0001321655/000132165526000039/a2026q2ex991pressrelease.htm)
- [GE Vernova Q3 2026 results (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/0001996810/000199681026000162/gev3q2026form8-k10282026.pdf)
- [Vertiv Q3 2026 results (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/0001674101/000162828026067707/q32026exhibit991vrt10282026.htm)
- [CrowdStrike Q2 FY2027 results](https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-reports-second-quarter-fiscal-year-2027-financial)
- [RTX Q3 2026 results (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/0000101829/000010182926000030/a2026-10x208xkerexhibit99.htm)
- [Defense earnings week, Oct 21 2026 (Nasdaq)](https://www.nasdaq.com/press-release/defense-earnings-week-opens-three-raised-forecasts-and-two-record-backlogs-2026-10-21)
- [Lockheed guidance raise (24/7 Wall St.)](https://247wallst.com/investing/2026/10/22/lockheed-martin-rises-9-as-record-backlog-lifts-outlook-rtx-gains-2-northrop-grumman-advances-3/)
- [Rearmament cash flow and Rheinmetall (MarketScreener)](https://www.marketscreener.com/news/who-gets-paid-to-rearm-the-west-ce785cdfde8cf026)
- [Drone stocks year-to-date (24/7 Wall St.)](https://247wallst.com/investing/2026/10/14/ondas-retreats-6-despite-regna-ai-launch-with-palantir-aerovironment-drops-3-kratos-slips/)
- [Cameco quote page (StockAnalysis)](https://stockanalysis.com/stocks/ccj/)
- [Thermo Fisher Q3 2026 results (Nasdaq)](https://www.nasdaq.com/press-release/thermo-fisher-scientific-reports-third-quarter-2026-results-2026-10-21)
- [Abbott Q3 2026 results](https://finance.yahoo.com/healthcare/articles/abbott-reports-third-quarter-2026-113000842.html)
- [Moderna 2026 rally (Motley Fool)](https://www.fool.com/investing/2026/10/21/not-lilly-not-johnson-johnson-this-stock-will-be-t/)
- [WHO avian influenza weekly update, Oct 9 2026](https://cdn.who.int/media/docs/default-source/wpro---documents/emergency/surveillance/avian-influenza/ai_20261009.pdf)
- [S&P 500 close and Fed decision, Oct 28 2026](https://www.bbntimes.com/global-economy/s-p-500-rises-to-7-743-98-for-a-third-straight-gain-as-the-fed-holds-rates-in-a-split-10-2-vote-and-oracle-surges-11)
- [Geopolitical risk assessment, October 2026](https://tatsuikeda.substack.com/p/geopolitical-risk-assessment-october)
