# Project 12 — Best Stocks for Investment (AI, War & Pandemic Resilience)

Private archive of Claude Project 12, "Project 12: Best Stocks for investment" (29 Oct 2026).

**Goal (owner):** find stocks with a high chance of **doubling in value within 3 years** (by Oct 2029),
across categories driven by AI, a world at war, and the risk of the next global virus.

**Status:** v2.1 report delivered 29 Oct 2026. 117 holdings in 12 categories, scored by a trained ML
model (walk-forward tested) blended 50/50 with a fundamentals model. Tier A: NU, NVDA, AVGO, TSM, PDD, GOOGL.
Top score: APP at 46% — no stock is close to a sure double. Research only, not investment advice.

## What's here

```
docs/
  charter/PROJECT_CHARTER_PLAN_ROADMAP.md / .docx / .pdf   charter, 5-phase plan, roadmap, risk register, KPIs (Claude Doc export)
  COMPETITIVE_ANALYSIS.md     benchmark vs Zacks, Seeking Alpha Quant, Danelfin, Motley Fool, Morningstar, theme ETFs
reports/
  AI_War_Pandemic_Stock_Research_v2.1_ML_2026-10-29.pdf    FINAL report (24 pages)
  version-history/
    ..._v2.1_ML_2026-10-29_legacy-watchlists-A-B.pdf       v2.1 before categories A/B were renumbered 11/12
    ..._v2_2026-10-29.pdf                                   v2 (rules model only, before the ML model)
model/
  core.js, ml_results.json, README.md                       ML pipeline and its results/test metrics
results/
  RESULTS_SUMMARY.md          tiers, top 10, 12 categories, model test results
sources/
  chatgpt_v1_expanded_stock_research_109_investments_2026-10-28.pdf   ChatGPT's 273-page v1 report (input)
  chatgpt_conversation_excerpts.md                                    captured fragments of the ChatGPT chat
chats/
  claude_chat_transcript.md   the Claude conversation in this project
  raw/claude-export-p12.json.gz   full export incl. every tool input/output
project/
  project_metadata.json       project info, Claude Doc link, source links
website/
  index.html, project-12.html  project web page (self-contained; same content, two names)
  build_site.py               regenerates the page from data/model + model/ml_results.json
  README.md                   how to update and publish
data/model/
  model_results_final.json    every holding: category, financials, rules/ML/final P(2x), loss risk, tier
.github/workflows/pages.yml   optional GitHub Pages deploy of website/ (enable: Settings -> Pages -> GitHub Actions)
CHANGELOG.md                  dated list of changes
WORKFLOW_RULES.md             standing rule: local folder -> GitHub -> website after every request
MANIFEST.sha256               SHA-256 of every file (verify with: sha256sum -c MANIFEST.sha256)
```

## Working rule

After every request: save to the local GitHub folder first, then to this GitHub repo, then update the website.
See `WORKFLOW_RULES.md` and the charter's Governance section.

## Links

- Claude Doc (charter, plan, roadmap): https://claude.ai/artifact/J8rDrPfFf5inPMEuanPE3W
- Source ChatGPT conversation: https://chatgpt.com/share/6ae35a35-c880-83e8-aea8-858d8aafa7b6
- Website page: https://hamidf2024.github.io/stocks-investment/project-12.html
