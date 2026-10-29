import json, math, sys, statistics, collections
sys.path.insert(0, '/tmp/outputs')
from model_data import CATNAMES, THEME, ADJ, MAP
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

# reuse styled research notes (latest results / bull / bear) written earlier
src = open('/tmp/outputs/build_report.py').read().split('for c in CATS:\n    c["rows"]')[0]
src = src.replace('OUT = ', 'OLD_OUT = ')
g = {}; exec(src, g)
PICK = {}
for c in g['CATS']:
    for p in c['picks']:
        PICK[p[0]] = dict(latest=p[8], bull=p[9], bear=p[10])
PICK['RHM'] and PICK.setdefault('RNMBY', PICK['RHM'])
PICK.setdefault('BAESY', PICK.get('BAESY'))


EXTRA = {
 "APP": ("Op margin 77%, FCF margin 66%, revenue CAGR 72%; P/E ~20x (v1 'Supported') - rare mix of growth and a modest price.", "Ad-tech platform concentration and regulatory/short-seller scrutiny; e-commerce ad expansion must keep working."),
 "NU": ("Profitable Latin American digital bank: revenue CAGR 37%, P/E ~16x; base case assumes ~30%/yr earnings growth.", "Brazil/Mexico credit cycle and FX; bank-style leverage."),
 "SKHY": ("HBM leader (~50% share); P/E ~6.5x on peak earnings; memory sold out through 2029.", "Memory price reversal; Korean listing (ADR access limited)."),
 "PDD": ("P/E ~8x, net cash ~CNY450B, FCF margin ~25%; Temu international growth.", "China/US trade and delisting risk; governance transparency."),
 "NXT": ("Solar tracker leader, near-zero debt, P/E ~21x; utility-scale solar for data-center power.", "US tax-credit policy and interest rates."),
 "SOFI": ("Revenue CAGR 32%; base case assumes ~32%/yr earnings growth.", "Share count growing ~15%/yr; credit losses; demanding P/E ~31x."),
 "LYSDY": ("Largest rare-earth producer outside China; revenue CAGR 45%.", "Rare-earth price swings; P/FCF ~84x."),
 "QCOM": ("FS 92, P/E ~21x ('Supported'); edge-AI and PC chips.", "Smartphone dependence; Apple modem loss."),
 "FSLR": ("Op margin 34%, P/E ~11x; US-made thin-film modules.", "Earnings rely on tax credits; policy risk."),
 "ISRG": ("FS 97, net cash, recurring instrument revenue.", "Premium valuation (P/E ~54x) caps upside."),
 "TOYO": ("Revenue CAGR 162%, P/E ~1.6x on recent peak margins.", "Small Japanese/Vietnam solar cell maker; margins may normalize; dilution."),
 "KLAC": ("Process-control leader, op margin 42%.", "Chip-equipment cycle; P/FCF ~55x."),
 "AMSC": ("Grid/Navy power systems; revenue CAGR 43%, net cash.", "Small cap; share count +21%/yr."),
 "SYK": ("FS 87, steady 10%+ growth in med-tech robotics.", "Compounder profile: doubling needs a re-rating."),
 "LYSDY ": ("", ""),
}
for k,(a,b) in EXTRA.items():
    if a and k.strip() not in PICK: PICK[k.strip()] = dict(latest=a, bull=a, bear=b)

R = json.load(open('/tmp/outputs/model_results_final.json'))
MLR = json.load(open('/tmp/outputs/ml/ml_results.json'))
for r in R:
    r['ens'] = r['final']; r['ens_pct'] = round(r['final'] * 100)
    r['risk'] = r['mlloss'] if r['mlloss'] is not None else r['loss']
fmtp = lambda v: '-' if v is None else f'{v*100:.0f}%'
OUT = "/tmp/outputs/AI_War_Pandemic_Stock_Research_v2.1_ML_2026-10-29.pdf"
PS = landscape(letter); W = PS[0] - 1.0 * inch

NAVY = colors.HexColor("#14213D"); TEAL = colors.HexColor("#1F6F8B"); LIGHT = colors.HexColor("#EEF3F7")
TIERC = {"A": colors.HexColor("#D8EFD9"), "B": colors.HexColor("#FFF1CC"), "C": colors.HexColor("#E6EEF6"),
         "D": colors.white, "E": colors.HexColor("#F6E3E1")}
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=NAVY, fontSize=17, spaceAfter=5)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=TEAL, fontSize=12, spaceBefore=6, spaceAfter=3)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9, leading=12)
S = ParagraphStyle("S", parent=B, fontSize=7.2, leading=8.9)
SH = ParagraphStyle("SH", parent=S, textColor=colors.white, fontName="Helvetica-Bold")
NOTE = ParagraphStyle("N", parent=B, fontSize=7.8, leading=9.6, textColor=colors.HexColor("#555555"))
P = lambda t, st=B: Paragraph(str(t), st)

def tbl(rows, widths, tiers=None, head=True):
    data = [[P(c, SH if (head and i == 0) else S) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C4CE")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5),
          ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    for i in range(1, len(rows)):
        if tiers: st.append(("BACKGROUND", (0, i), (-1, i), TIERC[tiers[i - 1]]))
        elif i % 2 == 0: st.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(st)); return t

def pct(x, d=0):
    return "-" if x is None else f"{x:.{d}f}%"

def money(v, cur):
    if v is None or v == '': return "-"
    sgn = "+" if v >= 0 else "-"; a = abs(v)
    if cur in ("JPY", "KRW", "TWD", "CNY"):
        return f"{cur} {sgn}{a/1e3:,.0f}B" if a < 1e6 else f"{cur} {sgn}{a/1e6:,.1f}T"
    return f"{cur} {sgn}{a/1e3:,.1f}B" if a >= 1000 else f"{cur} {sgn}{a:,.0f}M"

def deco(cv, doc):
    cv.saveState(); cv.setFillColor(NAVY); cv.rect(0, PS[1] - 20, PS[0], 20, fill=1, stroke=0)
    cv.setFillColor(colors.white); cv.setFont("Helvetica-Bold", 8)
    cv.drawString(0.5 * inch, PS[1] - 14, "AI, War & Pandemic-Resilience Stock Research  |  v2.1: 3-Year Doubling Focus + trained ML model  |  Oct 29, 2026")
    cv.setFillColor(colors.HexColor("#666666")); cv.setFont("Helvetica", 6.8)
    cv.drawString(0.5 * inch, 0.32 * inch, "Research and education only, not personalized investment advice. Model probabilities are judgment-based estimates, not guarantees. Verify prices and filings before acting.")
    cv.drawRightString(PS[0] - 0.5 * inch, 0.32 * inch, f"Page {doc.page}"); cv.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=PS, leftMargin=0.5 * inch, rightMargin=0.5 * inch, topMargin=0.48 * inch,
                        bottomMargin=0.5 * inch, title="AI, War & Pandemic-Resilience Stock Research v2", author="Research lead: Claude")
s = []
ranked = sorted(R, key=lambda r: -r['ens'])
stocks = [r for r in ranked if r['cat'] != 13]
cnt = collections.Counter(r['tier'][0] for r in R)

# ---------------- Cover ----------------
s += [Spacer(1, 0.5 * inch), P("AI, War &amp; Pandemic-Resilience Stock Research", ParagraphStyle("T", parent=H1, fontSize=26, leading=31)),
      P("Version 2.1: which stocks could double by October 2029? All 117 holdings categorized, financially evaluated, and scored by a machine-learning model trained and tested on 1967-2026 stock history, combined with a fundamentals model.", ParagraphStyle("st", parent=B, fontSize=12, leading=15, textColor=TEAL)),
      Spacer(1, 8), P("As of October 29, 2026. Supersedes expanded_stock_research_109_investments_2026-10-28.pdf (v1, 273 pages), which was fully reviewed: all 100 company financial dossiers (C001-C100), 9 funds and all 3-year scenario models (P01-P64, N01-N25, E01-E20).", B), Spacer(1, 10)]
s.append(tbl([["Goal", "Answer in one line"],
  ["Main goal", "Find stocks with a high chance of at least doubling in 3 years. A double needs ~26% compound annual price gain, which the S&P 500 achieved in only 3 of 48 three-year windows (6%)."],
  ["Universe", f"117 investments = 100 v1 companies + 8 v2 additions (MSFT, PLTR, CEG, PANW, TMO, ABT, GILD, MRNA) + 9 funds, sorted into 12 categories (10 for the AI, war and pandemic themes, 11 solar and renewables, 12 fintech and consumer) plus a fund group."],
  ["Prediction models", "(1) Trained ML model: gradient boosting + logistic regression trained on 66,010 historical cases (690 stocks, start dates 1967-2023), walk-forward tested on unseen years, calibrated. (2) Rules model: v1 scenarios + fundamentals factor score. Final P(2x) = 50/50 blend. The ML model also predicts the chance of losing half your money."],
  ["What the testing showed", "On unseen years the ML model's top 10% of picks doubled 31-34% of the time vs an 18-22% base rate (about 1.6x better). Doubling is only weakly predictable (AUC 0.58-0.63); big losses are much more predictable (AUC 0.75)."],
  ["Result", f"Tier A (final P(2x) 30%+, FS 70+, ML loss risk 15% or less): {cnt['A']}. Tier B (30%+, higher risk): {cnt['B']}. Tier C (25-29%): {cnt['C']}. The best final score is ~46%: no stock is close to a sure double."],
  ["Top 5 by model", ", ".join(f"{r['tk']} ({r['ens_pct']}%)" for r in stocks[:5])]],
  [1.4 * inch, W - 1.4 * inch]))
s += [Spacer(1, 10), P("<b>Disclaimer.</b> Research and education, not personalized advice; the author is not a licensed financial advisor. The models cannot see the future. The ML model learned from past price behaviour only (no historical fundamentals were available), its training data lacks most delisted companies, and past patterns may not repeat. Size positions to your own risk tolerance; consider a licensed advisor.", NOTE), PageBreak()]

# ---------------- Doubling leaderboard ----------------
s += [P("1. Doubling leaderboard: the 25 highest-probability stocks", H1),
      P("Sorted by final P(2x by Oct 2029) = 50% trained ML model + 50% rules model. ML P(-50%) = trained model's chance the stock ends at half or less. Row colour = tier (green A, yellow B, blue C). Financials from the v1 dossiers unless marked v2.", NOTE)]
rows = [["#", "Ticker / company", "Category", "Final P(2x)", "ML / Rules", "ML P(-50%)", "FS", "Rev growth", "Op mgn", "Price balance", "Driver to watch", "Main risk"]]
tiers = []
for i, r in enumerate(stocks[:25], 1):
    pk = PICK.get(r['tk'])
    drv = pk['bull'] if pk else (r.get('note') or f"Revenue CAGR {pct(r.get('cagr'))}, op margin {pct(r.get('opm'))}")
    rsk = pk['bear'] if pk else ("Base case needs " + ("growth to persist" if (r.get('cagr') or 0) > 15 else "a re-rating"))
    rows.append([i, f"<b>{r['tk']}</b><br/>{r['name']}", CATNAMES[r['cat']].split(':')[0] if r['cat'] < 11 else CATNAMES[r['cat']].split(':')[0],
                 f"<b>{r['ens_pct']}%</b>", f"{fmtp(r['ml'])}{'*' if r['ml_imputed'] else ''} / {r['rules']*100:.0f}%", fmtp(r['mlloss']), r['fs'],
                 pct(r.get('gused') if r['tk'] in ('NVDA','AVGO','TSM','AMD','MU','GOOGL','VRT','GEV','PLTR') else r.get('cagr')),
                 pct(r.get('opm')), r['price'].title(), drv, rsk])
    tiers.append(r['tier'][0])
s.append(tbl(rows, [0.25*inch, 1.15*inch, 1.15*inch, 0.5*inch, 0.6*inch, 0.45*inch, 0.3*inch, 0.5*inch, 0.45*inch, 0.75*inch, 1.9*inch, W-8.0*inch], tiers))
s += [P("* = too little price history for the ML model; the universe median (20%) is used in the blend. Rev growth = two-year historical revenue CAGR from v1, replaced by latest-quarter y/y growth where Q2/Q3 2026 results were reviewed (NVDA, AVGO, TSM, AMD, MU, GOOGL, VRT, GEV, PLTR).", NOTE), PageBreak()]

# ---------------- Category overview + chart ----------------
s += [P("2. Twelve categories at a glance", H1)]
rows = [["#", "Category", "Theme", "Holdings", "Avg P(2x)", "Best doubling candidate", "Tier A/B names"]]
for c in range(1, 14):
    rs = sorted([r for r in R if r['cat'] == c], key=lambda r: -r['ens'])
    ab = [r['tk'] for r in rs if r['tier'][0] in 'AB']
    rows.append([c if c <= 12 else "F", CATNAMES[c], THEME[c], len(rs),
                 f"{statistics.mean(r['ens'] for r in rs)*100:.0f}%", f"{rs[0]['tk']} ({rs[0]['ens_pct']}%)", ", ".join(ab) or "-"])
s.append(tbl(rows, [0.35*inch, 3.0*inch, 1.2*inch, 0.6*inch, 0.65*inch, 1.5*inch, W-7.3*inch]))

fig, ax = plt.subplots(figsize=(10, 3.9), dpi=170)
grp = {"AI (cats 1-6)": ([1,2,3,4,5,6], "#2C6FBB"), "War & resources (7-9)": ([7,8,9], "#C0392B"),
       "Pandemic & biotech (10)": ([10], "#2E8B57"), "Solar & fintech (11-12)": ([11,12], "#9A9A9A")}
for lab, (cs, col) in grp.items():
    pts = [r for r in stocks if r['cat'] in cs]
    ax.scatter([r['fs'] for r in pts], [r['ens']*100 for r in pts], s=26, c=col, alpha=0.85, label=lab, edgecolors='white', linewidths=0.5)
for r in stocks[:14]:
    ax.annotate(r['tk'], (r['fs'], r['ens']*100), xytext=(4, 2), textcoords='offset points', fontsize=7, color='#222')
ax.axhline(30, color='#888', lw=0.8, ls='--'); ax.axvline(70, color='#888', lw=0.8, ls='--')
ax.text(71, 45, "Tier A zone: final P(2x) 30%+ and FS 70+", fontsize=7.5, color='#444')
ax.set_xlabel("Financial Strength (0-100, v1 rubric)", fontsize=8.5); ax.set_ylabel("Final P(price 2x by Oct 2029), %", fontsize=8.5)
ax.set_title("Few stocks combine a strong balance sheet with high doubling odds", fontsize=10, loc='left')
ax.tick_params(labelsize=7.5); ax.spines[['top', 'right']].set_visible(False); ax.legend(fontsize=7, frameon=False, loc='lower left')
plt.tight_layout(); plt.savefig('/tmp/outputs/fs_vs_p2x.png'); plt.close()
s += [Spacer(1, 6), Image('/tmp/outputs/fs_vs_p2x.png', width=W*0.86, height=W*0.86*0.39), PageBreak()]

# ---------------- Model method ----------------
def mcsig(sig):
    Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return {r['tk']: sum(w * (1 - Phi((math.log(2) - math.log(x)) / sig)) for w, x in zip((.25, .5, .25), (r['bear'], r['base'], r['bull']))) for r in R}
lo, hi = mcsig(0.18), mcsig(0.35)
s += [P("3. Rules model: scenarios + fundamentals (50% of the final score)", H1),
      P("<b>Component 1: scenario simulation.</b> Each stock has bear / base / bull 3-year price multiples (v1 analyst scenarios, weights 25/50/25). Each scenario is treated as a lognormal outcome with 25% log-volatility, and the model sums the probability mass above 2.0x. Results reported after v1's Oct 27 cutoff adjust the multiples (table below).", B),
      P("<b>Component 2: fundamentals factor model (Doubling Potential Score, 0-100).</b> Growth engine 30 pts (revenue growth 40%+ = 30, 25%+ = 25, 15%+ = 19, 8%+ = 12, 0%+ = 6). Valuation headroom 20 (v1 Price-Fundamentals Balance: Supported 18, Conditional 14, Demanding 7-10, Not established 5). Financial strength 20 (FS / 5). Theme tailwind 15 (AI compute 15 ... pandemic 8). Downside risk 15 (from the bear multiple; -3 if share count grows &gt;10%/yr). The score maps to probability with a capped logistic: P = 0.65 / (1 + e<super>-(DPS-68)/9</super>), so a score of 50 is ~8%, 68 is ~33% and 85 is ~56%.", B),
      P("<b>Rules score</b> = average of the two components (funds use component 1 only). It is blended 50/50 with the trained ML model (section 4). Final tiers: <b>A</b> final P(2x) 30%+, FS 70+ and ML loss risk 15% or less; <b>B</b> 30%+ otherwise; <b>C</b> 25-29%; <b>D</b> 18-24%; <b>E</b> under 18%.", B), Spacer(1, 4)]
rows = [["Check", "Result", "What it means"],
 ["Agreement with v1", "Correlation 0.69 between v2 ensemble and v1 2x illustrations", "The independent factor view broadly confirms v1 but re-ranks names where financials disagree with scenarios (e.g., SOFI and ARRY fall, TSM, MU, SK hynix and MSFT rise)."],
 ["Universe average", f"{statistics.mean(r['rules'] for r in R)*100:.0f}% mean rules P(2x)", "Higher than the market base rate because the list is pre-screened for growth themes; treat absolute levels as optimistic and the ranking as the more useful output."],
 ["Volatility sensitivity", f"Top-10 average {statistics.mean(lo[r['tk']] for r in stocks[:10])*100:.0f}% at 18% vol vs {statistics.mean(hi[r['tk']] for r in stocks[:10])*100:.0f}% at 35% vol (scenario part)", "Rankings are stable; absolute odds shift by a few points with the volatility assumption."],
 ["Limits", "Weights are analyst choices", "This half cannot be back-tested because historical fundamentals were not available; the ML half (section 4) supplies the tested evidence."]]
s.append(tbl(rows, [1.5*inch, 3.0*inch, W-4.5*inch]))
s += [Spacer(1, 6), P("Post-cutoff adjustments applied to scenario multiples", H2)]
rows = [["Ticker", "Multiplier", "Evidence"]] + [[k, f"x{v[0]:.2f}", v[1]] for k, v in ADJ.items()]
s += [tbl(rows, [0.8*inch, 0.8*inch, W-1.6*inch]), PageBreak()]

# ---------------- Trained ML model ----------------
fd = MLR['folds']; oos = MLR['oos']; dd = MLR['data']
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.2), dpi=170)
dec = oos['dec']; xs = list(range(1, 11))
a1.bar([x - 0.2 for x in xs], [d[0]*100 for d in dec], 0.4, color='#9DB7D5', label='Predicted')
a1.bar([x + 0.2 for x in xs], [d[1]*100 for d in dec], 0.4, color='#1F4E79', label='Actually doubled')
a1.axhline(oos['base']*100, color='#888', lw=0.8, ls='--'); a1.text(0.6, oos['base']*100 + 0.8, f"base rate {oos['base']*100:.0f}%", fontsize=7, color='#555')
a1.set_xticks(xs); a1.set_xlabel('Model score decile (1 = lowest, 10 = highest)', fontsize=8); a1.set_ylabel('% of cases', fontsize=8)
a1.set_title('Out-of-sample: higher scores doubled more often', fontsize=9, loc='left'); a1.legend(fontsize=7, frameon=False); a1.tick_params(labelsize=7)
imp = MLR['imp'][:9]; NAMES = {'vol36':'Volatility (3y)','age':'Years listed','mktTrend120':'Market vs 10y trend','mkt36':'Market 3y return','mktVol12':'Market volatility','vol12':'Volatility (1y)','mkt12':'Market 1y return','mom60':'5y momentum','mom36':'3y momentum'}
a2.barh([NAMES.get(k, k) for k, v in imp][::-1], [v*100 for k, v in imp][::-1], color='#1F6F8B')
a2.set_xlabel('Share of model split gain (%)', fontsize=8); a2.set_title('What the boosted-tree model relies on', fontsize=9, loc='left'); a2.tick_params(labelsize=7)
for a in (a1, a2): a.spines[['top', 'right']].set_visible(False)
plt.tight_layout(); plt.savefig('/tmp/outputs/ml_charts.png'); plt.close()
s += [P("4. Trained machine-learning model (50% of the final score)", H1),
      P(f"<b>Data.</b> Monthly total-return prices (Yahoo Finance) for every company in the S&amp;P 500 at any time since 1996 ({dd['universe']} tickers; {dd['fetched_ok']} with data, {dd['delisted_missing']} delisted names unavailable) plus our 117 holdings, and market history back to 1955 (Shiller S&amp;P series). Each example is a stock on a date; the label is whether its price was at least 2x 36 months later. {dd['rows60']:,} examples from {dd['stocks']} stocks, start dates {dd['firstYear']}-{dd['lastYear']}; {dd['pos60']*100:.1f}% doubled.", B),
      P("<b>Features (17, all known at the time).</b> Stock momentum over 3, 12, 36 and 60 months; volatility (1y, 3y); drawdown from 3-year high; biggest monthly gain; price vs 5-year average; years listed; beta; return vs market; market 1y and 3y return, market vs its 10-year trend, market volatility.", B),
      P("<b>Models.</b> Gradient-boosted decision trees (120 depth-2 trees, histogram splits) and L2 logistic regression, averaged, then calibrated (Platt scaling on out-of-sample predictions). A second pair trained on 36-month windows scores recent listings (CEG, NXT, NU, TOYO and others). A companion model with the same features predicts a 50%+ loss.", B),
      P("<b>Testing: walk-forward, never on data the model has seen.</b> Each test period starts 3 years after training ends, so no training label overlaps a test date.", B)]
rows = [["Test period", "Base rate (doubled)", "AUC trees / blend", "Top 10% picks doubled", "Top 5% doubled", "Bottom 20% doubled", "Brier blend vs base"]]
for f in fd: rows.append([f['name'], f"{f['base']*100:.0f}%", f"{f['aucG']:.2f} / {f['aucE']:.2f}", f"{f['top10']*100:.0f}%", f"{f['top5']*100:.0f}%", f"{f['bot20']*100:.0f}%", f"{f['brierE']:.3f} vs {f['brierB']:.3f}"])
s += [tbl(rows, [2.6*inch, 1.0*inch, 1.1*inch, 1.2*inch, 1.0*inch, 1.2*inch, W-8.1*inch]), Spacer(1, 4),
      Image('/tmp/outputs/ml_charts.png', width=W*0.9, height=W*0.9*0.32),
      P(f"<b>Reading the results.</b> AUC 0.5 is a coin flip and 1.0 is perfect; 0.58-0.63 means the model separates future doublers from the rest modestly but consistently, in three different eras. Big losses are far more predictable (loss model AUC {MLR['loss_model']['auc60']:.2f}). The model learned mostly that young, volatile stocks double more often, and that doubles become rarer after strong 3-year market runs. Today the S&amp;P 500 is ~85% above its level 3 years ago and well above its 10-year trend, so the model scores almost every stock below its historical base rate.", B),
      P("<b>Known biases.</b> Survivorship: most delisted companies are missing, which inflates doubling rates and understates loss rates. No fundamentals or valuation: free historical fundamentals were not reachable, so the rules half covers them. The 1967-1985 period has few stocks. Foreign listings are measured in local currency.", NOTE), PageBreak()]

# ---------------- Category pages ----------------
INTRO = {
 1: "Accelerators and leading-edge foundry. Nvidia guided its October quarter to $108B; TSMC guided Q4 to roughly +58% y/y and says the AI demand-supply gap is still large.",
 2: "Memory and chipmaking tools. SK hynix says DRAM/HBM is sold out through 2029; memory margins are at cycle peaks, which raises both the upside and the cyclical risk.",
 3: "Cloud platforms and AI-native platforms. Growth is accelerating (Google Cloud +103%, Azure +48%) but Alphabet and Meta posted negative free cash flow in Q3 2026.",
 4: "Robots, surgical systems, machine vision, autonomy. Strong balance sheets, but most names are priced for steady compounding rather than a 3-year double.",
 5: "Power generation, grid and cooling for data centers. The deepest order books in the universe: GE Vernova backlog ~$197B, Vertiv organic orders more than doubled.",
 6: "AI decision software and cybersecurity. Record quarters at CrowdStrike and Palo Alto; valuations are the main obstacle to a double.",
 7: "US primes and defense electronics. Record backlogs (RTX $340B, LMT $292B) but low growth and modest multiples make doubling unlikely; these are ballast, not rockets.",
 8: "Drones, munitions and European rearmament. Big theme, weak 2026 share prices (RHM -35%, AVAV/KTOS ~-48% YTD) and cash-burn or dilution risk.",
 9: "Uranium, nuclear fuel and critical minerals tied to both war supply chains and AI power. Many small names fund growth with new shares.",
 10: "Pandemic response capacity (tools, diagnostics, antivirals, vaccines) plus AI drug discovery. WHO still rates H5N1 public risk as low; clinical-stage names are binary.",
 11: "The 20-company solar/renewable section from v1 (17 here; GEV, NEE and AMSC moved to Category 5). Demand depends on subsidies and rates more than on AI, war or pandemics.",
 12: "Names from v1 outside the three themes. Included because several (NU, SOFI, PDD) have high model doubling odds.",
 13: "Funds provide diversified exposure; the model uses scenarios only (no corporate balance sheet).",
}
for c in range(1, 14):
    rs = sorted([r for r in R if r['cat'] == c], key=lambda r: -r['ens'])
    s += [P(f"{'Category ' + str(c) if c <= 12 else ''} {CATNAMES[c]}".strip(), H1), P(INTRO[c], B), Spacer(1, 3)]
    if c == 13:
        rows = [["Ticker", "Fund", "Bear / base / bull", "Final P(2x)", "ML P(-50%)", "Tier"]]
        for r in rs: rows.append([f"<b>{r['tk']}</b>", r['name'], f"{r['bear']} / {r['base']} / {r['bull']}", f"<b>{r['ens_pct']}%</b>", fmtp(r['mlloss']), r['tier']])
        s += [tbl(rows, [0.6*inch, 3.2*inch, 1.3*inch, 0.6*inch, 0.6*inch, W-6.3*inch], [r['tier'][0] for r in rs]), PageBreak()]
        continue
    rows = [["Ticker / company", "FS", "Rev CAGR", "Op mgn", "FCF mgn", "Net cash (debt)", "Share CAGR", "P/E", "P/FCF", "Price balance", "Bear/base/bull", "Rules P(2x)", "ML P(2x)", "ML P(-50%)", "Final P(2x)", "Tier"]]
    for r in rs:
        rows.append([f"<b>{r['tk']}</b> {r['name']}" + (" <i>(v2 add.)</i>" if r['src'] == 'v2 addition' else ""),
                     r['fs'], pct(r.get('cagr'), 1), pct(r.get('opm'), 1), pct(r.get('fcfm'), 1), money(r.get('netcash'), r.get('cur')),
                     pct(r.get('dil'), 1), r.get('pe_s') or '-', r.get('pfcf_s') or '-', r['price'].title(),
                     f"{r['bear']}/{r['base']}/{r['bull']}", f"{r['rules']*100:.0f}%", fmtp(r['ml']) + ('*' if r['ml_imputed'] else ''), fmtp(r['mlloss']), f"<b>{r['ens_pct']}%</b>", r['tier'][0]])
    s.append(tbl(rows, [W-7.85*inch, 0.3*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.8*inch, 0.5*inch, 0.45*inch, 0.45*inch, 0.7*inch, 0.75*inch, 0.45*inch, 0.45*inch, 0.5*inch, 0.5*inch, 0.3*inch], [r['tier'][0] for r in rs]))
    notes = [r for r in rs if PICK.get(r['tk']) or r.get('note')][:5]
    if notes:
        s += [P("Latest results and the doubling case for key names", H2)]
        rr = [["Ticker", "Latest reported (cited period)", "What gets it to 2x", "What stops it"]]
        for r in notes:
            pk = PICK.get(r['tk'])
            rr.append([f"<b>{r['tk']}</b>", pk['latest'] if pk else r['note'], pk['bull'] if pk else "-", pk['bear'] if pk else "-"])
        s.append(tbl(rr, [0.6*inch, 4.2*inch, (W-4.8*inch)/2, (W-4.8*inch)/2]))
    s += [P("FS = v1 Financial Strength 0-100 (v2 additions estimated with the same rubric). Net cash and margins are latest TTM in the issuer's statement currency. Rules = scenarios + fundamentals model; ML = trained model (* = too little history, median used); Final = 50/50 blend.", NOTE), PageBreak()]

# ---------------- Appendix: full ranking ----------------
s += [P("Appendix A. Full ranking of all 117 investments by final doubling probability", H1)]
rows = [["#", "Ticker", "Name", "Category", "P(2x)", "P(-50%)", "FS", "Tier", "#", "Ticker", "Name", "Category", "P(2x)", "P(-50%)", "FS", "Tier"]]
half = math.ceil(len(ranked) / 2)
short = lambda c: (str(c) if c <= 12 else "Fund")
for i in range(half):
    row = []
    for j in (i, i + half):
        if j < len(ranked):
            r = ranked[j]; row += [j + 1, r['tk'], r['name'][:24], short(r['cat']), f"{r['ens_pct']}%", f"{r['risk']*100:.0f}%", r['fs'] if r['fs'] is not None else "-", r['tier'][0]]
        else: row += [""] * 8
    rows.append(row)
cw = [0.3*inch, 0.5*inch, 1.45*inch, 0.45*inch, 0.4*inch, 0.45*inch, 0.3*inch, 0.3*inch]
s += [tbl(rows, cw + cw), P("Category: 1-10 theme categories; 11 solar and renewables; 12 fintech and consumer; Fund = theme funds.", NOTE), PageBreak()]

# ---------------- Appendix B: v1 -> v2 ----------------
s += [P("Appendix B. How the v1 report was re-categorized", H1),
      P("v1 had nine sections built up over successive requests: six strategic themes (55 companies + 9 funds), a 25-company screen, and a 20-company solar/renewable extension. v2 places each holding in exactly one category.", B)]
rows = [["v1 section", "v2 destination"],
 ["1. Physical AI and robotics (ISRG, FANUC, Keyence, ROK, TER, Yaskawa, SYM) + robotics additions (TSLA, CGNX, NOVT, SYK, DE, OUST, AUR, VPG, FFR, EMR)", "Cat 4 Physical AI & Robotics (TER moved to Cat 2)"],
 ["2. Chips and semiconductors + AMD, QCOM, AMBA", "Cat 1 (compute/foundry) and Cat 2 (memory/equipment)"],
 ["3. Rare and critical materials + FCX, USAR, UUUU, CCJ, BWXT", "Cat 9 Strategic Resources"],
 ["4. Biotech and AI + REGN, ABCL, ADPT", "Cat 10 Biotech, Pandemic & AI Drug Discovery"],
 ["5. Defense + CACI", "Cat 7 US primes; BAE and Rheinmetall to Cat 8"],
 ["6. Defense robotics and autonomy + RCAT, ONDS", "Cat 8 (AVAV, KTOS, ESLT, RCAT, ONDS); TDY, CW, HII, DRS to Cat 7"],
 ["25-company screen: GOOGL, AMZN, META, APP", "Cat 3 Hyperscalers & AI Platforms (+ MSFT added)"],
 ["25-company screen: VRT, ETN; renewables: GEV, NEE, AMSC", "Cat 5 AI Power (+ CEG added)"],
 ["25-company screen: CRWD, ZS", "Cat 6 AI Software & Cyber (+ PLTR, PANW added)"],
 ["Renewables: NXT, FSLR, ENPH, SHLS, ARRY, FLNC, RUN, ENLT, ELVA, TOYO, CSIQ, SEDG, BLDP, TURB, WAVE, PBK, BRNX", "Category 11 Solar & Renewables"],
 ["25-company screen: NU, SOFI, TBBK, MELI, PDD, CELH, LULU", "Category 12 Fintech & Consumer"],
 ["9 funds: SOXX, XSD, SMH, REMX, EART, BOT, KOID, BOTT, THNQ", "Fund group"],
 ["New in v2: MSFT, PLTR, CEG, PANW, TMO, ABT, GILD, MRNA", "Cats 3, 5, 6, 10 (estimated FS; full dossiers in v2.1)"]]
s += [tbl(rows, [5.5*inch, W-5.5*inch]), Spacer(1, 6),
      P("<b>What v2 changes in v1's conclusions.</b> v1 found no company with a validated &gt;60% doubling probability and placed NU (~61%) and APP (~60%) at the top. v2 agrees on the top names but promotes TSM, SK hynix, MU, GOOGL and MSFT, where financial strength and recent results are stronger than the scenario alone implies, and demotes SOFI, ARRY and TBBK, whose fundamentals score lower. v1's caveat stands: a probability, however modelled, is not a guarantee.", B), PageBreak()]

# ---------------- Appendix C: sources ----------------
s += [P("Appendix C. Sources", H1), P("v1 financial data: Stock Analysis standardized statements (S&P Global Market Intelligence / Fiscal.ai) as cited in the v1 dossiers, reviewed Oct 28, 2026. v2 updates: company releases and SEC filings, accessed Oct 29, 2026.", B)]
full=open('/tmp/outputs/build_report.py').read(); seg=full[full.index('src = ['):]; seg=seg[:seg.index(']\n')+2]; gg={}; exec(seg, gg); srcs=gg['src']
s.append(tbl([["Source", "URL (https://)"]] + [[a, b] for a, b in srcs], [2.6*inch, W-2.6*inch]))
doc.build(s, onFirstPage=deco, onLaterPages=deco)
print("built", OUT)
