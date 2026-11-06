# Data sources for the research program

As of November 6, 2026. Each source was checked for reachability and coverage. Prices are from vendor pages or
comparison articles and should be re-checked before buying. "Browser" means the cloud workspace and the Mac shell are
blocked by the network allowlist, so the download runs in Chrome (same-origin fetch on that site).

## Verified free sources (ready to use)

| Source | What it gives | Coverage (verified) | Access | Used by |
| --- | --- | --- | --- | --- |
| SEC EDGAR XBRL API (`data.sec.gov/api/xbrl/companyfacts`, `/frames`) | Reported fundamentals (revenue, income, cash, debt, shares) with the **filing date** of each value, so features can be point-in-time | 2009 onward (XBRL era); about 500+ concepts per large filer (Apple: 512) | Free, no key; SEC asks for a descriptive User-Agent and max 10 requests/s. Browser | R-01, R-04 |
| FRED (St. Louis Fed) | Macro series for the regime gate | DGS10 10-yr yield 1962-01 to 2026-11-04; BAA10Y credit spread 1986-01 to 2026-11-04; UNRATE 1948-; CPIAUCSL 1947- | Free CSV (`fredgraph.csv?id=`). Browser | R-02 |
| Ken French Data Library | Fama-French 5 factors and momentum, monthly | 1963- (FF5), 1926- (momentum) | Free zip. Browser | R-02, R-04 (risk adjustment) |
| Yahoo Finance chart API | Monthly total-return prices for listed stocks and ETFs | Decades for survivors; **delisted names mostly missing** | Free, unofficial. Browser | EXP-000, R-06 |
| fja05680/sp500 (GitHub) | S&P 500 membership history | 1996- | Free, reachable from the workspace | Universe, R-05 |
| Shiller data (GitHub mirror) | S&P level, dividends, earnings, CPI | 1871- | Free | Market features |

## Delisted companies (R-05): needs a paid source

Free sources do not cover the 444 delisted S&P 500 members the current model is missing. Choices, best value first:

| Source | Delisted coverage | Fundamentals | Cost (check vendor) | Note |
| --- | --- | --- | --- | --- |
| Sharadar via Nasdaq Data Link (SEP prices + SF1 fundamentals + S&P 500 constituents) | Active **and delisted**, 20,000+ US companies | Yes, point-in-time | Personal license, about $50-150/month for the bundle | Best single fit: fixes R-01, R-04 and R-05 together |
| EODHD | 26,000+ delisted US tickers, mostly from Jan 2000 | Limited for delisted | Included in all paid plans (from about $20-80/month) | Cheapest; prices only |
| Norgate Data | Complete US delisted archive, S&P 500 / Russell membership flags by day | No | Annual subscription, Windows app | Strong for survivorship-free universes; Windows only |
| CRSP via WRDS | The academic standard, 1925- | With Compustat | University access only | Use if a university login is available |

Recommendation: one month of the Sharadar bundle, download once, then cancel. Stay within its personal license (no redistribution, so
raw files stay out of the public repository; only derived results are published).

## Alpaca: verdict

- Stock history only from 2016; the free Basic plan uses the IEX feed (about 2.5% of volume), 200 calls/min; full SIP
  data is Algo Trader Plus, $99/month. Delisted coverage partial, no fundamentals.
- **Not suitable for training the 36-month model.** Useful for R-06 live tracking and paper trading. Needs your own API keys (entered by you, never by Claude).

## Not yet covered

- Analyst estimate revisions (I/B/E/S, Zacks, FactSet): paid only; deferred.
- Point-in-time fundamentals before 2009: Sharadar (1998-) or Compustat (WRDS).

## Sources

- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- FRED: https://fred.stlouisfed.org
- Ken French Data Library: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- S&P 500 history: https://github.com/fja05680/sp500
- Sharadar on QuantRocket: https://www.quantrocket.com/pricing/data/sharadar
- EODHD delisted data: https://eodhd.com/financial-apis/landing-delisted/
- Norgate Data toolkit: https://concretumgroup.substack.com/p/the-complete-norgate-data-toolkit
- Alpaca vs other vendors: https://marketparquet.com/vs/alpaca
