"""Generate website/index.html from the project data.
Usage (from the repo root):  python website/build_site.py [path/to/model_results_final.json] [path/to/ml_results.json]
"""
import json, sys, html, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "model", "model_results_final.json")
MLF = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "model", "ml_results.json")
REPO = "https://github.com/hamidf2024/p12-best-stocks-investment"
RAW = REPO + "/raw/main/"

CAT = {1: ("AI semiconductors: compute & foundry", "AI"), 2: ("AI memory & chip equipment", "AI"),
       3: ("Hyperscalers & AI platforms", "AI"), 4: ("Physical AI & robotics", "AI"),
       5: ("AI power & data-center infrastructure", "AI + energy"), 6: ("AI software & cybersecurity", "AI + cyber"),
       7: ("US defense primes & electronics", "War"), 8: ("Defense tech, drones & rearmament", "War"),
       9: ("Nuclear fuel & critical minerals", "War + AI power"), 10: ("Biotech & pandemic preparedness", "Pandemic"),
       11: ("Solar & renewables", "Energy transition"), 12: ("Fintech & consumer", "Outside themes"),
       13: ("Theme funds (ETFs)", "Diversified")}

R = json.load(open(RES)); ML = json.load(open(MLF))
e = html.escape
pct = lambda v: "–" if v is None else f"{v*100:.0f}%"
ranked = sorted(R, key=lambda r: -r["final"])
stocks = [r for r in ranked if r["cat"] != 13]

def tier_badge(t):
    k = t[0]
    return f'<span class="tier t{k}" title="{e(t)}">{k}</span>'

rows = "\n".join(
    f'<tr><td class="num">{i}</td><td><b>{e(r["tk"])}</b><span class="sub">{e(r["name"])}</span></td>'
    f'<td>{e(CAT[r["cat"]][0])}</td><td class="num strong">{pct(r["final"])}</td>'
    f'<td class="num">{pct(r["ml"])}{"*" if r.get("ml_imputed") else ""}</td><td class="num">{pct(r["rules"])}</td>'
    f'<td class="num">{pct(r["mlloss"])}</td><td class="num">{r.get("fs") if r.get("fs") is not None else "–"}</td>'
    f'<td>{tier_badge(r["tier"])}</td></tr>'
    for i, r in enumerate(stocks[:20], 1))

cards = []
for c in range(1, 14):
    rs = sorted([r for r in R if r["cat"] == c], key=lambda r: -r["final"])
    chips = " ".join(f'<span class="chip">{e(r["tk"])} <small>{pct(r["final"])}</small></span>' for r in rs)
    cards.append(f'<article class="card"><div class="cardhead"><span class="catnum">{c if c <= 12 else "F"}</span>'
                 f'<div><h3>{e(CAT[c][0])}</h3><p class="theme">{e(CAT[c][1])} · {len(rs)} holdings · avg {pct(statistics.mean(r["final"] for r in rs))}</p></div></div>'
                 f'<div class="chips">{chips}</div></article>')
cards = "\n".join(cards)

folds = "\n".join(
    f'<tr><td>{e(f["name"])}</td><td class="num">{f["base"]*100:.0f}%</td><td class="num">{f["aucE"]:.2f}</td>'
    f'<td class="num strong">{f["top10"]*100:.0f}%</td><td class="num">{f["bot20"]*100:.0f}%</td></tr>' for f in ML["folds"])
dec = ML["oos"]["dec"]; mx = max(max(d) for d in dec)
bars = "\n".join(
    f'<div class="bar"><div class="b pred" style="height:{d[0]/mx*100:.0f}%" title="Predicted {d[0]*100:.0f}%"></div>'
    f'<div class="b act" style="height:{d[1]/mx*100:.0f}%" title="Actually doubled {d[1]*100:.0f}%"></div><span>{i}</span></div>'
    for i, d in enumerate(dec, 1))
tierA = ", ".join(r["tk"] for r in stocks if r["tier"][0] == "A")
dd = ML["data"]

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Best Stocks to Double by 2029</title>
<meta name="description" content="Project 12: 117 stocks across AI, war and pandemic themes, scored for their chance of doubling by October 2029 with a trained, walk-forward-tested model.">
<style>
:root{{--bg:#f7f8fa;--surface:#fff;--ink:#14213d;--muted:#5b6475;--line:#e3e7ee;--accent:#1f6f8b;--accent2:#9db7d5;
--a:#d8efd9;--b:#fff1cc;--c:#e6eef6;--d:#f1f2f4;--e:#f6e3e1;--ak:#1e6b2f;--bk:#8a5a00;--ck:#1f4e79;--dk:#555;--ek:#9b2c22}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0f141c;--surface:#171e29;--ink:#e8edf5;--muted:#9aa6b8;--line:#2a3442;--accent:#5fb3cf;--accent2:#35587a;
--a:#1d3a24;--b:#3d3216;--c:#1c2d40;--d:#222a35;--e:#3f2220;--ak:#9be0a9;--bk:#f2c66b;--ck:#9cc4ec;--dk:#b5bdc9;--ek:#f2a39a}}}}
:root[data-theme="dark"]{{--bg:#0f141c;--surface:#171e29;--ink:#e8edf5;--muted:#9aa6b8;--line:#2a3442;--accent:#5fb3cf;--accent2:#35587a;
--a:#1d3a24;--b:#3d3216;--c:#1c2d40;--d:#222a35;--e:#3f2220;--ak:#9be0a9;--bk:#f2c66b;--ck:#9cc4ec;--dk:#b5bdc9;--ek:#f2a39a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:0 16px 64px}}header.hero{{padding:56px 0 28px}}
.eyebrow{{color:var(--accent);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:12px}}
h1{{font-size:clamp(28px,5vw,44px);line-height:1.1;margin:8px 0 12px}}h2{{font-size:22px;margin:44px 0 6px}}h3{{font-size:15px;margin:0}}
.lead{{font-size:17px;color:var(--muted);max-width:760px}}.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-top:24px}}
.kpi{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}.kpi b{{display:block;font-size:26px}}.kpi span{{color:var(--muted);font-size:13px}}
.note{{color:var(--muted);font-size:13px}}.tablewrap{{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:12px;margin-top:12px}}
table{{border-collapse:collapse;width:100%;min-width:640px}}th,td{{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{font-size:12px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.04em}}tr:last-child td{{border-bottom:0}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}.strong{{font-weight:700}}.sub{{display:block;color:var(--muted);font-size:12px}}
.tier{{display:inline-block;min-width:24px;text-align:center;border-radius:6px;font-weight:700;font-size:12px;padding:2px 6px}}
.tA{{background:var(--a);color:var(--ak)}}.tB{{background:var(--b);color:var(--bk)}}.tC{{background:var(--c);color:var(--ck)}}.tD{{background:var(--d);color:var(--dk)}}.tE{{background:var(--e);color:var(--ek)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:12px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px}}.cardhead{{display:flex;gap:12px;align-items:flex-start}}
.catnum{{flex:none;width:32px;height:32px;border-radius:8px;background:var(--accent);color:#fff;display:grid;place-items:center;font-weight:700}}
.theme{{margin:2px 0 0;color:var(--muted);font-size:12.5px}}.chips{{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}}
.chip{{border:1px solid var(--line);border-radius:999px;padding:2px 9px;font-size:12.5px}}.chip small{{color:var(--muted)}}
.chart{{display:flex;align-items:flex-end;gap:10px;height:180px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 16px 28px;margin-top:12px}}
.bar{{flex:1;height:100%;display:flex;align-items:flex-end;gap:3px;position:relative}}.bar span{{position:absolute;bottom:-20px;left:0;right:0;text-align:center;font-size:11px;color:var(--muted)}}
.b{{flex:1;border-radius:3px 3px 0 0}}.pred{{background:var(--accent2)}}.act{{background:var(--accent)}}
.legend{{display:flex;gap:16px;font-size:12.5px;color:var(--muted);margin-top:8px}}.sw{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:middle}}
.links{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:12px}}
.links a{{display:block;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;color:var(--ink);text-decoration:none}}
.links a:hover{{border-color:var(--accent)}}.links a b{{display:block}}.links a span{{color:var(--muted);font-size:13px}}
.toc{{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}}.toc a{{border:1px solid var(--line);border-radius:999px;padding:4px 12px;font-size:13px;color:var(--ink);text-decoration:none;background:var(--surface)}}.toc a:hover{{border-color:var(--accent);color:var(--accent)}}
section{{scroll-margin-top:16px}}html{{scroll-behavior:smooth}}
footer{{margin-top:48px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);padding-top:16px}}
</style></head><body><main>
<header class="hero"><div class="eyebrow">Project 12 · Last updated October 29, 2026</div>
<h1>Which stocks could double by 2029?</h1>
<p class="lead">117 holdings across AI, a world at war and the risk of the next pandemic, sorted into 12 categories and scored for their chance of at least doubling within three years. Scores blend a fundamentals model with a machine-learning model trained on stock history from 1967 to 2026.</p>
<div class="kpis"><div class="kpi"><b>{pct(stocks[0]["final"])}</b><span>Highest chance of doubling ({e(stocks[0]["tk"])})</span></div>
<div class="kpi"><b>{len(tierA.split(", "))}</b><span>Tier A names: {e(tierA)}</span></div>
<div class="kpi"><b>{dd["rows60"]:,}</b><span>historical cases the model learned from ({dd["stocks"]} stocks)</span></div>
<div class="kpi"><b>~1.6x</b><span>better than chance at picking doublers in tests on unseen years</span></div></div>
<nav class="toc" aria-label="Sections"><a href="#leaderboard">Leaderboard</a><a href="#categories">12 categories</a><a href="#model">Model tests</a><a href="#downloads">Downloads</a></nav></header>

<section id="leaderboard"><h2>Doubling leaderboard</h2><p class="note">Top 20 stocks by final chance of being at least 2x by October 2029. Final = 50% trained ML model + 50% rules model. Loss risk = ML chance of ending at half or less. FS = Financial Strength (0-100). * too little history; universe median used.</p>
<div class="tablewrap"><table><thead><tr><th class="num">#</th><th>Stock</th><th>Category</th><th class="num">Final</th><th class="num">ML</th><th class="num">Rules</th><th class="num">Loss risk</th><th class="num">FS</th><th>Tier</th></tr></thead><tbody>
{rows}
</tbody></table></div>
<p class="note">Tiers: <span class="tier tA">A</span> 30%+ with FS 70+ and loss risk 15% or less · <span class="tier tB">B</span> 30%+, higher risk · <span class="tier tC">C</span> 25–29% · <span class="tier tD">D</span> 18–24% · <span class="tier tE">E</span> under 18%.</p></section>

<section id="categories"><h2>12 categories</h2><p class="note">Every holding sits in exactly one category, by what drives most of its revenue. Percentages are each stock's final chance of doubling.</p>
<div class="grid">{cards}</div></section>

<section id="model"><h2>How well the model predicts</h2><p class="note">Walk-forward tests: each model trained only on earlier years and was scored on later years it never saw.</p>
<div class="tablewrap"><table><thead><tr><th>Test period</th><th class="num">Base rate</th><th class="num">AUC</th><th class="num">Top 10% doubled</th><th class="num">Bottom 20% doubled</th></tr></thead><tbody>{folds}</tbody></table></div>
<div class="chart" role="img" aria-label="Out-of-sample doubling rate by model score decile">{bars}</div>
<div class="legend"><span><i class="sw" style="background:var(--accent2)"></i>Predicted</span><span><i class="sw" style="background:var(--accent)"></i>Actually doubled</span><span>by model score decile (1 = lowest)</span></div>
<p class="note">Doubling is only modestly predictable (AUC 0.58–0.63); big losses are far more predictable (AUC {ML["loss_model"]["auc60"]:.2f}). Training data lacks most delisted companies, so true odds are somewhat lower than shown.</p></section>

<section id="downloads"><h2>Downloads</h2><div class="links">
<a href="{RAW}reports/AI_War_Pandemic_Stock_Research_v2.1_ML_2026-10-29.pdf"><b>Full report (PDF, 24 pages)</b><span>All 117 holdings, financials, both models</span></a>
<a href="{RAW}docs/charter/PROJECT_CHARTER_PLAN_ROADMAP.pdf"><b>Project charter, plan and roadmap</b><span>Scope, phases, risks, governance</span></a>
<a href="{REPO}/blob/main/results/RESULTS_SUMMARY.md"><b>Results summary</b><span>Tiers, top picks, test metrics</span></a>
<a href="{REPO}"><b>GitHub repository</b><span>Code, data and version history</span></a></div></section>

<footer>Research and education only, not personalized investment advice. Probabilities are model estimates, not guarantees; verify prices and filings before acting. Data: Yahoo Finance, SEC filings, company releases, Shiller S&amp;P series. Generated by website/build_site.py.</footer>
</main></body></html>"""
open(os.path.join(HERE, "index.html"), "w").write(page)
print("wrote", os.path.join(HERE, "index.html"), len(page))
