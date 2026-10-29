from reportlab.lib.pagesizes import letter
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

OUT = "/tmp/outputs/AI_War_Pandemic_Stock_Research_v2_2026-10-29.pdf"
NAVY = colors.HexColor("#14213D"); TEAL = colors.HexColor("#1F6F8B"); LIGHT = colors.HexColor("#EEF3F7")
GOOD = colors.HexColor("#2E7D32"); WARN = colors.HexColor("#B26A00"); BAD = colors.HexColor("#B3261E")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=NAVY, fontSize=18, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=TEAL, fontSize=13, spaceBefore=8, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9.2, leading=12.2)
S = ParagraphStyle("S", parent=B, fontSize=7.8, leading=9.8)
SH = ParagraphStyle("SH", parent=S, textColor=colors.white, fontName="Helvetica-Bold")
NOTE = ParagraphStyle("N", parent=B, fontSize=8, leading=10, textColor=colors.HexColor("#555555"))

def P(t, st=B): return Paragraph(t, st)

def tbl(rows, widths, head=True, zebra=True):
    data = [[P(str(c), SH if (head and i == 0) else S) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4CE")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    if zebra:
        for i in range(1, len(rows)):
            if i % 2 == 0: st.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(st)); return t

def rating(total):
    return "Top pick" if total >= 80 else "Core" if total >= 70 else "Watch" if total >= 60 else "Speculative"

def balance(v):
    return ("Cheap vs fundamentals" if v >= 13 else "Roughly balanced" if v >= 10
            else "Priced for growth" if v >= 7 else "Stretched / speculative")

# ---------- data: (ticker, company, listing, theme, fin, growth, valuation, risk, latest, bull, bear) ----------
CATS = [
 dict(n=1, name="AI Accelerators & Foundry", theme="AI",
  thesis="Every AI model runs on accelerators fabricated at the leading edge. Demand still exceeds supply: Nvidia guided its October quarter to $108B (+/-2%) with zero China data-center revenue assumed, and TSMC said the AI demand-supply gap remains large.",
  picks=[
   ("NVDA","NVIDIA","Nasdaq",25,24,19,10,10,"Q2 FY27 (May-Jul 2026): revenue $96.2B (+106% y/y); Data Center $89.0B (+117%); GM 75.0%. Q3 guide $108B. Reports Nov 17.","Rubin ramp + sovereign/enterprise 'ACIE' demand (+138% y/y) keep beats coming.","Top two direct customers were 22% and 14% of FY26 revenue; any hyperscaler capex pause hits first."),
   ("AVGO","Broadcom","Nasdaq",25,23,19,8,10,"Q3 FY26 (May-Aug 2026): revenue $29.6B (+86%); AI semis $16.7B (+221%); FCF $13.7B. Q4 guide $34.8B; AI $21.7B.","Custom XPUs for six frontier labs; mgmt outlines ~$115B AI revenue in FY27.","Customer concentration in a few AI labs; gross margin dilution from XPU mix (75%, -210 bp q/q)."),
   ("TSM","TSMC (ADR)","NYSE",23,25,17,12,7,"Q3 2026: revenue $46.72B (+41.2% y/y USD); GM 66.4%; net income +68.7%; HPC 68% of sales. Q4 guide $52.3-54.3B.","Sole supplier of 2nm/3nm at scale; pricing power through 2028.","Taiwan Strait geopolitical tail risk; N2 ramp costs pressure margins."),
   ("AMD","Advanced Micro Devices","Nasdaq",22,20,16,9,9,"Q2 2026: revenue $11.54B (+50%); Data Center $6.7B (+107%, 58% of sales). Q3 guide ~$13.0B. Anthropic deal up to 2 GW of MI450.","Second-source GPU winner; mgmt expects Data Center revenue to more than double in 2027.","Software (ROCm) gap vs CUDA; higher capex weighed on shares after Q2."),
  ],
  catalysts="AMD Q3 (early Nov); NVDA Q3 FY27 Nov 17; AVGO Q4 (Dec); TSMC monthly sales (10th of each month).",
  risks="Export controls; AI capex digestion; memory cost inflation trimming GPU margins (Nvidia guided 74.0% GM)."),
 dict(n=2, name="AI Memory & Chip Equipment", theme="AI",
  thesis="High-bandwidth memory is the tightest link in the AI supply chain. SK hynix said on Oct 28 that DRAM/HBM output is effectively sold out through 2029, and memory pricing has pushed Micron's gross margin above 80%. Lithography (ASML) sets the pace of new capacity.",
  picks=[
   ("MU","Micron Technology","Nasdaq",24,24,20,10,6,"FQ4 FY26 (Jun-Aug 2026): revenue $54.23B (+379%); adj GM ~87%; FY26 revenue $133.2B. FQ1 guide $61.5B, EPS $38.15. Closed $983.23 on Oct 28 (~6x run-rate EPS).","Sold-out HBM/DRAM through 2029 sustains super-normal margins; only US-based memory maker.","Memory is cyclical: a 40% price drop would compress EPS sharply; analyst targets range $361-$3,000."),
   ("ASML","ASML Holding (ADR)","Nasdaq",20,23,13,10,10,"Q3 2026: net sales EUR11.7B; net income EUR5.0B; GM 57.5%. FY26 guide EUR44-45B. ~EUR4.1B buyback in Q3.","EUV/High-NA monopoly; every new 2nm fab needs it.","China export limits; lumpy system orders; slower growth than chip designers."),
  ],
  catalysts="Micron FQ1 FY27 (mid/late Dec); Sandisk results Oct 29; ASML Q4 (Jan 2027).",
  risks="Capacity additions by 2028 could end the shortage; customer double-ordering."),
 dict(n=3, name="Hyperscalers & AI Cloud", theme="AI",
  thesis="Cloud growth is accelerating (Google Cloud +103%, Azure +48%), but the bill is visible: Alphabet posted negative free cash flow of $9.07B in Q3 and Meta negative $2.12B. Favor platforms that fund AI from cash flow.",
  picks=[
   ("MSFT","Microsoft","Nasdaq",22,25,15,11,12,"FQ1 FY27 (Jul-Sep 2026): Azure +48%; capex forecast trimmed to $170B; generated ~$19B positive FCF while peers went negative. FY26 revenue >$331B.","Self-funded AI buildout; 30M+ paid M365 Copilot seats (Jul).","Capex re-accelerates in H1 2027 on component costs; OpenAI-related exposure."),
   ("GOOGL","Alphabet","Nasdaq",23,20,17,11,9,"Q3 2026: revenue $127.6B (+25%); Google Cloud $30.7B (+103%); op margin 31.8%; FCF -$9.07B. 2026 capex $195-205B, 'significant increase' in 2027. Shares fell ~10% Oct 29.","Full-stack AI (TPUs, Gemini) with Search still growing; TPU sales to third parties.","Second straight negative-FCF quarter; equity-stake gains/losses (SpaceX, Anthropic) add volatility."),
   ("AMZN","Amazon","Nasdaq",21,17,13,10,9,"Q3 results due after close Oct 29, 2026. 2026 capex guide ~$220B, the largest; trailing capex ran above operating cash flow.","AWS re-acceleration on AI infrastructure demand.","Highest capex burden in the group; memory cost inflation flagged."),
   ("META","Meta Platforms","Nasdaq",18,18,14,10,8,"Q3 2026 (Oct 21): FCF -$2.12B; 2026 capex guide raised at the low end to $135-145B.","AI-driven ad targeting lifts monetization.","No cloud business to resell capacity; payback depends on ads alone."),
  ],
  catalysts="Amazon Q3 (Oct 29); 2027 capex guidance with Q4 reports (late Jan/early Feb 2027).",
  risks="Group capex expected above $1 trillion in 2027; any revenue shortfall exposes depreciation burden."),
 dict(n=4, name="AI Software & Decision Platforms", theme="AI + Defense",
  thesis="Software that turns models into operational decisions. Palantir sits on both the AI and defense themes: its AIP platform runs US military command systems and its US commercial business is growing well over 100%.",
  picks=[
   ("PLTR","Palantir Technologies","Nasdaq",24,23,20,3,8,"Q2 2026: revenue $1.935B (+93%); FY26 guide raised to $8.150-8.158B; US commercial >$3.424B (+134%); adj FCF guide $4.5-4.7B. Q3 guide $2.16B; reports Nov 2. Market cap ~$473B.","Rule-of-40 far above peers; defense 'operating system' position.","~120x+ forward earnings leaves no room for a miss; political/ICE controversy; short sellers active."),
  ],
  catalysts="Q3 results Nov 2, 2026; FY27 defense budget (drone/AI lines).",
  risks="Valuation compression if rates rise further; government contract timing."),
 dict(n=5, name="AI Power & Data-Center Infrastructure", theme="AI + Energy security",
  thesis="Power and cooling are now the binding constraint on AI data centers. Order books are the strongest in this list: GE Vernova's backlog jumped from $176B to ~$197B in one quarter, and Vertiv's organic orders more than doubled.",
  picks=[
   ("GEV","GE Vernova","NYSE",23,22,18,9,11,"Q3 2026 (Oct 28): orders $29.3B (+96% organic); backlog ~$197B, expected >$200B in Q4; gas power backlog + slots 122 GW; $9B Trench acquisition.","Multi-year sold-out gas turbines + grid equipment; services backlog $93B.","Wind segment drag; execution on capacity expansion; premium multiple."),
   ("VRT","Vertiv Holdings","NYSE",25,21,20,7,9,"Q3 2026 (Oct 28): sales $4.313B (+61%, 55% organic); adj op margin 25.2%; organic orders >100% y/y. FY26 guide raised $650M to $14.65B; adj EPS $7.15.","Liquid cooling + power for every Nvidia rack generation.","~50x+ earnings; revenue slips on multiphase projects (Q2)."),
   ("CEG","Constellation Energy","Nasdaq",21,20,13,11,11,"Largest US nuclear fleet; Oct 6, 2026 Google collaboration to add 890 MW to PJM; long-term power deals with hyperscalers.","24/7 carbon-free power is scarce; contracts lock in price.","Power-price regulation in PJM; reactor outages. (Q3 figures to refresh.)"),
  ],
  catalysts="Constellation Q3 (early Nov); Vertiv/GEV order updates; PJM capacity auction.",
  risks="If AI capex slows, orders (not backlog) fall first; tariff costs on equipment."),
 dict(n=6, name="Cybersecurity", theme="AI + War (cyber front)",
  thesis="AI agents widen the attack surface and state actors in active conflicts target infrastructure. Gartner projects ~$244B of security spend in 2026; CrowdStrike and Palo Alto both posted record quarters and raised guidance.",
  picks=[
   ("CRWD","CrowdStrike","Nasdaq",22,20,16,7,11,"Q2 FY27 (May-Jul 2026): revenue $1.47B (+26%); ending ARR $5.84B (+25%); record net new ARR $333M (+51%); FCF $377M. FY27 revenue guide $5.99-6.01B.","Falcon Flex ARR >$2.29B (+101%); AI detection & response module ramping.","Shares already +120% since Q2; 'priced for perfection' sell-offs on good prints."),
   ("PANW","Palo Alto Networks","Nasdaq",21,21,13,8,12,"Best quarter in its history (fiscal Q4, Jul 2026); ~$18B backlog; platformization strategy. (FQ1 FY27 due mid-Nov.)","Broadest platform; identity + AI security cross-sell.","Integration risk from acquisitions; competition from cloud vendors' own tools."),
  ],
  catalysts="CRWD Q3 FY27 (early Dec); PANW FQ1 FY27 (mid-Nov).",
  risks="High multiples; budget fatigue if economy slows."),
 dict(n=7, name="US Defense Primes & Missile Defense", theme="War",
  thesis="Record backlogs from missile and air-defense demand (Iran war, Ukraine Patriot shortage). Yet the S&P Aerospace & Defense index was ~-3% YTD on Oct 26 and ITA fell ~18% from Aug to Oct on fears of a Democratic Congress cutting budgets. Valuations (~16-17x forward) are modest.",
  picks=[
   ("LMT","Lockheed Martin","NYSE",22,21,12,14,12,"Q3 2026 (Oct 22): sales $20.7B (+11%); EPS $7.97; record backlog $292B. 2026 guide raised: revenue $80-82B, EPS $30.35-30.75, FCF ~ $8B. ~16x forward.","THAAD/PAC-3 interceptor restocking for years.","F-35 program cost pressure; budget risk after midterms."),
   ("RTX","RTX Corp","NYSE",21,21,14,12,12,"Q3 2026 (Oct 20): sales $25.0B (+11%, +12% organic); backlog $340B ($164B defense); $52B defense bookings in Q3 incl. Tomahawk $23B, AMRAAM $14.3B.","Defense + commercial aero mix; missile multiyear contracts.","GTF engine issues; undefinitized contract pricing."),
   ("NOC","Northrop Grumman","NYSE",20,19,10,13,9,"Q3 2026: sales $11.1B (+7%); EPS $7.89; book-to-bill 1.5x; backlog $109.6B. ~17x forward; ~34% below 52-week high on Oct 19.","B-21, Sentinel ICBM, space; cheapest re-rating candidate if budgets hold.","Most exposed to new-program delays under a split/Democratic Congress."),
  ],
  catalysts="Nov 3 midterm results; FY27 appropriations ($1.5T request); NATO orders.",
  risks="Ceasefires; continuing resolutions delaying new starts; fixed-price contract losses."),
 dict(n=8, name="Defense Tech, Drones & European Rearmament", theme="War",
  thesis="Wars in Ukraine and the Gulf proved cheap drones, counter-drone systems and munitions volume. NATO targets 5% of GDP by 2035 and the FY27 US request includes ~$75B for drones. But 2026 punished this group: Rheinmetall -34.7% YTD (Oct 21), AeroVironment and Kratos ~-48% YTD.",
  picks=[
   ("RHM","Rheinmetall (Frankfurt; ADR OTC)","XETRA",23,15,17,11,8,"H1 2026: sales +39%; operating margin 15.0% (from 12.1%); operating FCF -$1.81B. Shares -34.7% YTD to Oct 21; German F126 frigate cancellation hit sentiment.","Germany 3.5% of GDP core defense; ammunition and air-defense backlog.","Cash conversion is weak; not on US exchanges."),
   ("BAESY","BAE Systems (London; ADR OTC)","LSE",20,19,11,12,12,"Diversified UK/US prime with large US exposure (AUKUS, munitions). Latest results to be refreshed in v3.","Most US-exposed European prime; steadier than pure plays.","AUKUS/UK budget timing; FX."),
   ("AVAV","AeroVironment","Nasdaq",22,12,15,10,5,"FQ4 FY26: revenue $642M (more than doubled, incl. BlueHalo); funded backlog $1.2B. Down ~43-49% YTD after a restatement and $1.5B SCAR backlog reversal.","Switchblade + counter-UAS + low-cost laser export orders.","Accounting restatement; integration risk."),
   ("KTOS","Kratos Defense","Nasdaq",21,13,13,7,8,"2026 revenue guide $1.595-1.675B; XQ-58 Valkyrie in Marine Corps production; ~-48% YTD; very high P/E.","Collaborative combat aircraft and hypersonic test demand.","Thin margins; equity raises ($150M Mar 2026)."),
  ],
  catalysts="NATO procurement awards; US drone budget lines; Ukraine aid packages.",
  risks="Peace deal; European program cancellations; small-cap volatility."),
 dict(n=9, name="Strategic Resources: Nuclear Fuel & Critical Minerals", theme="War + AI power",
  thesis="War and AI power demand both raise the value of secure uranium and rare-earth supply. Long-term uranium hit $96.50/lb in Sept 2026, above its 2007 peak, while China dominates rare-earth magnets used in munitions.",
  picks=[
   ("CCJ","Cameco","NYSE",21,20,10,10,11,"Closed $83.84 Oct 28 (52-wk range $76.92-135.24; ~42% below record); 2026 delivery guide 29-32M lb; Q2 realized price $67.79/lb (+18%). Reports Oct 30.","Contract book reprices upward as old deals roll off; Westinghouse stake.","Rate-sensitive; deliberately lower 2026 volumes."),
   ("BWXT","BWX Technologies","NYSE",20,18,13,8,12,"Naval reactors + HALEU/TRISO fuel; ~18% revenue growth expected for 2026; ~38x forward earnings (mid-2026).","Sole-source US Navy nuclear supplier; SMR fuel.","Premium valuation; government program timing."),
   ("MP","MP Materials","NYSE",20,13,12,7,8,"Only fully integrated US rare-earth miner-to-magnet producer (Mountain Pass, CA).","National-security magnet supply; government-backed demand.","Chinese price competition; early-stage magnet ramp."),
  ],
  catalysts="Cameco Q3 Oct 30; US reactor restarts and SMR approvals; China export-control moves.",
  risks="Uranium spot volatility; policy reversals."),
 dict(n=10, name="Pandemic Preparedness: Diagnostics, Tools, Antivirals & Vaccines", theme="Pandemic",
  thesis="WHO still rates H5N1 public risk as low (1,003 human cases, 479 deaths since 2003; sporadic, no sustained human spread), but H5N1 reached Washington dairy cattle in Oct 2026. The best pandemic hedge is a company that grows without a pandemic and scales fast in one: testing, lab tools and antivirals. mRNA names are high-beta options.",
  picks=[
   ("TMO","Thermo Fisher Scientific","NYSE",18,24,11,12,14,"Q3 2026 (Oct 21): revenue $12.14B (+9%, 6% organic); adj EPS $6.68 (+15%); adj op margin 24.5%. FY guide raised to $47.7-48.2B, adj EPS $25.13-25.43.","Supplied PCR, sampling and bioproduction in COVID; same role in any outbreak.","Biotech funding cycle; China exposure."),
   ("ABT","Abbott Laboratories","NYSE",18,22,11,12,14,"Q3 2026 (Oct 21): sales +14.5% reported (+7.0% comparable); diagnostics +46.7% reported after Exact Sciences deal; adj EPS $1.42; FY EPS guide reaffirmed.","Rapid/molecular test scale (BinaxNOW-type capacity).","Integration of Exact Sciences; GAAP EPS dilution."),
   ("GILD","Gilead Sciences","Nasdaq",15,22,10,13,13,"Q2 2026: revenue $7.8B (+10%); HIV +12%; no major patent expiry until 2036; Veklury (COVID antiviral) shrinking. Q3 due Oct 29 after close.","Proven antiviral platform; cash flow funds pipeline.","Pandemic upside is small vs HIV core."),
   ("MRNA","Moderna","Nasdaq",17,10,15,3,4,"Up ~600% in 2026 (market cap ~$90B in Oct) after cancer-vaccine (intismeran) data and flu approval; H1 2026 revenue $534M, net loss $2.1B.","Fastest pandemic vaccine platform; oncology optionality.","Binary trial risk; heavy losses; outbreak headlines move it more than revenue does."),
  ],
  catalysts="GILD Q3 Oct 29; WHO monthly H5N1 assessments; flu season (Dec-Feb).",
  risks="Vaccine-policy hostility in the US; no pandemic = no windfall."),
]

for c in CATS:
    c["rows"] = []
    for p in c["picks"]:
        tk, co, ex, th, fin, gr, val, rk, latest, bull, bear = p
        tot = th + fin + gr + val + rk
        c["rows"].append(dict(tk=tk, co=co, ex=ex, th=th, fin=fin, gr=gr, val=val, rk=rk, tot=tot,
                               latest=latest, bull=bull, bear=bear))

def page_deco(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY); canvas.rect(0, letter[1] - 22, letter[0], 22, fill=1, stroke=0)
    canvas.setFillColor(colors.white); canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(0.6 * inch, letter[1] - 15, "AI, War & Pandemic-Resilience Stock Research  |  v2  |  Oct 29, 2026")
    canvas.setFillColor(colors.HexColor("#666666")); canvas.setFont("Helvetica", 7)
    canvas.drawString(0.6 * inch, 0.4 * inch, "Research and education only. Not personalized investment advice. Verify prices and filings before acting.")
    canvas.drawRightString(letter[0] - 0.6 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch,
                        topMargin=0.6*inch, bottomMargin=0.6*inch,
                        title="AI, War & Pandemic-Resilience Stock Research v2", author="Research lead: Claude")
W = letter[0] - 1.2 * inch
s = []

# ---- Cover ----
s += [Spacer(1, 1.2*inch), P("AI, War &amp; Pandemic-Resilience<br/>Stock Research", ParagraphStyle("T", parent=H1, fontSize=28, leading=34)),
      Spacer(1, 8), P("Version 2 — re-categorized into 10 investment themes and refreshed with Q3 2026 results", ParagraphStyle("st", parent=B, fontSize=12, textColor=TEAL)),
      Spacer(1, 14), P("As of October 29, 2026 (market data through Oct 28 close unless stated)", B),
      P("Supersedes: expanded_stock_research_109_investments_2026-10-28.pdf (v1, ChatGPT)", B),
      Spacer(1, 24)]
s.append(tbl([["What changed from v1", "Detail"],
  ["Structure", "v1 was organized by request (sector lists, then 20 solar/renewable names). v2 groups holdings into 10 themes tied to AI, war and pandemic risk."],
  ["Data", "Top picks refreshed with Q2/Q3 2026 filings and releases (SEC 8-K/6-K/10-Q, company IR)."],
  ["Scoring", "One 100-point rubric: theme 25, financial strength 25, growth 20, price-fundamentals balance 15, risk 15. Financial Strength (0-100) and Price-Fundamentals Balance from v1 are kept as columns."],
  ["Removed", "v1 'doubling probability' percentages: unvalidated and replaced by bull/bear cases."],
  ["Pending", "Row-level merge of all 109 v1 holdings (the v1 PDF could not be opened from the shared ChatGPT link). Appendix A gives the mapping rules; v2.1 will carry every row once the file is supplied."]],
  [1.5*inch, W-1.5*inch]))
s += [Spacer(1, 18), P("<b>Disclaimer.</b> This report is research and education, not personalized investment advice; the author is not a licensed financial advisor. Scores are judgment-based screens, not return forecasts. Markets can fall sharply; size any position to your own risk tolerance and consider a licensed advisor.", NOTE), PageBreak()]

# ---- Market backdrop ----
s += [P("1. Market backdrop and theme drivers", H1)]
s.append(tbl([["Driver", "Evidence (late Oct 2026)", "Read-through"],
 ["AI buildout", "Nvidia Q2 FY27 revenue $96.2B (+106%), Q3 guide $108B; TSMC Q3 +41% USD, Q4 guide ~+58%; Broadcom FY27 AI target ~$115B; SK hynix memory sold out through 2029.", "Demand still exceeds supply in chips, memory, power and cooling."],
 ["AI payback stress", "Alphabet Q3 FCF -$9.07B (shares -10%); Meta FCF -$2.12B; Microsoft cut capex forecast to $170B but stayed FCF-positive; group capex seen >$1T in 2027.", "Prefer suppliers with backlog and platforms that self-fund capex."],
 ["War environment", "Iran war in its seventh month; Ukraine PAC-3 stocks nearly exhausted; Russia-Ukraine front static; Indo-Pacific build-up continues. RTX backlog $340B, LMT $292B (records).", "Interceptors, munitions, drones and air defense are multi-year restocking stories."],
 ["Defense politics", "Midterms Nov 3; ITA fell ~18% Aug-Oct on Democratic-sweep pricing; FY27 request $1.5T incl. ~$75B drones; NATO 5% of GDP by 2035.", "Budget risk is priced in; primes trade ~16-17x forward."],
 ["Pandemic risk", "WHO: 1,003 human H5N1 cases (479 deaths) since 2003; public risk still low, no sustained human transmission; H5N1 in Washington dairy herds (Oct 8).", "Own pandemic optionality through companies that also grow in normal years."],
 ["Rates and valuation", "S&P 500 7,744 (Oct 28), ~1.3% below record; Fed held 3.75-4.00% (10-2 vote) after a Sept hike; 10-yr >5%; oil >$100.", "Long-duration, high-P/E names are most rate-sensitive."]],
 [1.15*inch, 3.85*inch, W-5.0*inch]))
s += [Spacer(1, 8), P("<b>Portfolio construction note.</b> Categories 1-6 share one driver (AI capex). A reader building a watchlist should cap the combined AI weight and hold war and pandemic categories as partial hedges; defense and diagnostics have historically had low correlation with AI semiconductors.", B), PageBreak()]

# ---- Summary table ----
s += [P("2. Summary: all scored companies by category", H1),
      P("Score = theme (25) + financial strength (25) + growth (20) + price-fundamentals balance (15) + risk (15). Financial Strength (0-100) = financial component x 4. Rating: 80+ Top pick, 70-79 Core, 60-69 Watch, &lt;60 Speculative.", NOTE), Spacer(1, 4)]
rows = [["#", "Category", "Ticker", "Company", "Score", "Fin. Strength", "Price-Fund. Balance", "Rating"]]
for c in CATS:
    for r in sorted(c["rows"], key=lambda r: -r["tot"]):
        rows.append([c["n"], c["name"], r["tk"], r["co"], r["tot"], r["fin"]*4, balance(r["val"]), rating(r["tot"])])
t = tbl(rows, [0.3*inch, 1.9*inch, 0.6*inch, 1.6*inch, 0.5*inch, 0.65*inch, 1.0*inch, W-6.55*inch])
s += [t, PageBreak()]

# ---- Top 10 overall ----
allr = [(c, r) for c in CATS for r in c["rows"]]
top = sorted(allr, key=lambda x: -x[1]["tot"])[:12]
s += [P("3. Highest-scoring names across all themes", H1),
      P("A ranked list is not a buy list: the top of it is dominated by AI, which is a single bet. The 'best per category' column shows a diversified alternative.", NOTE)]
rows = [["Rank", "Ticker", "Category", "Score", "Why it ranks"]]
for i, (c, r) in enumerate(top, 1):
    rows.append([i, r["tk"], c["name"], r["tot"], r["bull"]])
s.append(tbl(rows, [0.45*inch, 0.6*inch, 1.9*inch, 0.5*inch, W-3.45*inch]))
s += [Spacer(1, 10), P("Best-scoring name in each category", H2)]
rows = [["#", "Category", "Leader", "Score", "Runner-up"]]
for c in CATS:
    rs = sorted(c["rows"], key=lambda r: -r["tot"])
    rows.append([c["n"], c["name"], f'{rs[0]["tk"]} ({rs[0]["co"]})', rs[0]["tot"], f'{rs[1]["tk"]} ({rs[1]["tot"]})' if len(rs) > 1 else "-"])
s += [tbl(rows, [0.3*inch, 2.4*inch, 2.0*inch, 0.5*inch, W-5.2*inch]), PageBreak()]

# ---- Category pages ----
for c in CATS:
    blk = [P(f'Category {c["n"]}: {c["name"]}', H1), P(f'<b>Theme:</b> {c["theme"]}', NOTE), Spacer(1, 3), P(c["thesis"], B), Spacer(1, 6)]
    rows = [["Ticker", "Listing", "Latest results (cited period)", "Score", "Th/Fin/Gr/Val/Risk", "Balance", "Rating"]]
    for r in sorted(c["rows"], key=lambda r: -r["tot"]):
        rows.append([f'<b>{r["tk"]}</b><br/>{r["co"]}', r["ex"], r["latest"], f'<b>{r["tot"]}</b>',
                     f'{r["th"]}/{r["fin"]}/{r["gr"]}/{r["val"]}/{r["rk"]}', balance(r["val"]), rating(r["tot"])])
    blk.append(tbl(rows, [1.0*inch, 0.55*inch, 3.0*inch, 0.45*inch, 0.85*inch, 0.75*inch, W-6.6*inch]))
    blk += [Spacer(1, 6), P("Bull and bear case", H2)]
    rows = [["Ticker", "Bull case", "Bear case"]]
    for r in sorted(c["rows"], key=lambda r: -r["tot"]):
        rows.append([r["tk"], r["bull"], r["bear"]])
    blk.append(tbl(rows, [0.7*inch, (W-0.7*inch)/2, (W-0.7*inch)/2]))
    blk += [Spacer(1, 6), P(f'<b>Upcoming catalysts:</b> {c["catalysts"]}', B), P(f'<b>Category risks:</b> {c["risks"]}', B), PageBreak()]
    s += blk

# ---- Risk matrix ----
s += [P("4. Scenario matrix: how each category reacts", H1)]
sc = ["AI capex pause", "Rates up 100 bp", "Ceasefires", "Taiwan crisis", "H5N1 human spread", "Defense budget cut"]
m = {1:["--","-","0","--","-","0"],2:["--","-","0","--","-","0"],3:["-","-","0","-","-","0"],4:["-","--","-","+","0","-"],
     5:["-","-","0","-","0","0"],6:["-","-","0","+","0","0"],7:["0","0","-","++","0","--"],8:["0","-","--","+","0","-"],
     9:["-","-","-","+","0","0"],10:["0","0","0","0","++","0"]}
rows = [["#", "Category"] + sc]
for c in CATS: rows.append([c["n"], c["name"]] + m[c["n"]])
s.append(tbl(rows, [0.3*inch, 2.0*inch] + [(W-2.3*inch)/6]*6))
s += [P("Key: ++ strong benefit, + benefit, 0 little effect, - hurt, -- strongly hurt. Judgment-based; use to check that a watchlist is not exposed to one scenario everywhere.", NOTE), PageBreak()]

# ---- Appendix A ----
s += [P("Appendix A. Re-categorization of the v1 (109-investment) report", H1),
      P("The v1 PDF was produced in a ChatGPT conversation whose shared link does not allow file download, so v2 applies the rules below. Every v1 holding goes to exactly one of the 10 categories or to the Legacy Watchlist. A row-level table will be added in v2.1 once the v1 file is attached.", B), Spacer(1, 6)]
s.append(tbl([["v1 group / company type", "v2 destination", "Rule"],
 ["GPU, ASIC, foundry, networking chips", "Cat 1", "Revenue mainly from AI compute silicon"],
 ["Memory, chip equipment, EDA", "Cat 2", "Supplies capacity to Cat 1"],
 ["Mega-cap cloud and internet platforms", "Cat 3", "Owns AI data centers"],
 ["AI/data software, analytics", "Cat 4 (cyber names to Cat 6)", "Sells software, not hardware"],
 ["Utilities with nuclear/gas fleets; power, grid and cooling equipment", "Cat 5", "Sells power or power gear to data centers"],
 ["Security software", "Cat 6", "Endpoint, network, identity, cloud security"],
 ["US defense contractors", "Cat 7 (primes) or Cat 8 (small/drone)", "Prime = >$10B revenue"],
 ["Non-US defense", "Cat 8", "European/Asian rearmament"],
 ["Uranium, nuclear fuel, rare earths, lithium for defense", "Cat 9", "Strategic supply"],
 ["Vaccines, antivirals, diagnostics, lab tools", "Cat 10", "Pandemic response capacity"],
 ["Solar and renewable section (20 companies: 10 US, 10 non-US, e.g., First Solar FSLR, Nextpower NXT, Enlight ENLT, Turbo Energy)", "Legacy Watchlist - Clean Energy (adjacent to Cat 5)", "Solar/wind demand is driven by subsidies and rates more than by AI, war or pandemic; v1 itself found none supported its >60% doubling threshold. FSLR, NXT and ENLT remain the best-ranked names there."],
 ["Everything else (consumer, financial, unrelated)", "Legacy Watchlist - Other", "Kept for reference, not scored in v2"]],
 [2.4*inch, 1.7*inch, W-4.1*inch]))
s += [Spacer(1, 8), P("v1 issues carried forward as fixes", H2),
      P("1) v1 doubling percentages were 'unvalidated scenario estimates' per v1's author; removed. 2) v1 financial reviews covered companies unevenly; v2 cites a dated filing per top pick. 3) v1 Financial Strength (0-100) and Price-Fundamentals Balance columns are kept and re-computed for every scored company.", B), PageBreak()]

# ---- Appendix B sources ----
s += [P("Appendix B. Methodology and sources", H1),
      P("Figures come from company press releases and SEC filings where available, otherwise from named financial news sources, all accessed Oct 29, 2026. Prices move daily; re-check before use. Fiscal periods are labelled with calendar months.", B), Spacer(1, 6)]
src = [
 ("NVIDIA Q2 FY27 8-K", "sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm"),
 ("NVIDIA guidance (CNBC, Aug 26)", "cnbc.com/2026/08/26/nvidia-nvda-earnings-report-q2-2027-live-updates.html"),
 ("Broadcom Q3 FY26 8-K", "sec.gov/Archives/edgar/data/0001730168/000173016826000076/avgo-08022026x8kxex99.htm"),
 ("TSMC Q3 2026 6-K", "sec.gov/Archives/edgar/data/0001046179/000104617926000726/a3q26e_withguidancexfinal.htm"),
 ("AMD Q2 2026 (247wallst / S&P Global)", "247wallst.com/companies/amd/earnings/2026/Q2"),
 ("Micron FQ4 FY26 and valuation", "top1markets.com/news/micron-stock-memory-supercycle-hbm-valuation"),
 ("Micron price, SK hynix sold-out (FinanceFeeds)", "financefeeds.com/micron-stock-rises-5-5-as-sk-hynix-says-dram-and-hbm-sold-out-through-2029/"),
 ("ASML Q3 2026 6-K", "sec.gov/Archives/edgar/data/0000937966/000162828026065813/a2026_10x14xpresentation.htm"),
 ("Alphabet Q3 2026 8-K", "sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm"),
 ("Alphabet FCF and shares (CNBC, Oct 28)", "cnbc.com/2026/10/28/alphabet-googl-earnings-q3-2026.html"),
 ("Hyperscaler capex, Azure 48% (CNBC, Oct 29)", "cnbc.com/2026/10/29/microsoft-google-ai-capex-estimates.html"),
 ("Microsoft vs Alphabet FCF (24/7 Wall St, Oct 29)", "247wallst.com/investing/2026/10/29/alphabet-sinks-11-as-ai-spending-pushes-cash-flow-negative-again-microsoft-and-meta-edge-higher-amazon-slips/"),
 ("Palantir Q2 2026 8-K", "sec.gov/Archives/edgar/data/0001321655/000132165526000039/a2026q2ex991pressrelease.htm"),
 ("GE Vernova Q3 2026 8-K", "sec.gov/Archives/edgar/data/0001996810/000199681026000162/gev3q2026form8-k10282026.pdf"),
 ("GE Vernova Q3 call (Benzinga)", "benzinga.com/news/26/10/62652519/ge-vernova-q3-2026-earnings-call-transcript"),
 ("Vertiv Q3 2026 8-K", "sec.gov/Archives/edgar/data/0001674101/000162828026067707/q32026exhibit991vrt10282026.htm"),
 ("Constellation / Google 890 MW (Analytics Insight)", "analyticsinsight.net/artificial-intelligence/top-ai-infrastructure-stocks-in-2026-the-power-companies-behind-the-ai-boom"),
 ("CrowdStrike Q2 FY27 release", "ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-reports-second-quarter-fiscal-year-2027-financial"),
 ("Cyber stocks +120% since Q2 (Seoul Economic Daily)", "en.sedaily.com/finance/2026/10/28/cybersecurity-firms-emerge-as-core-ai-infrastructure"),
 ("Palo Alto backlog (GlobeInsights)", "globeinsights.net/cyber-shock-what-the-crowdstrike-and-palo-alto-plunge-really-means-for-ai-stocks/"),
 ("RTX Q3 2026 8-K and 10-Q", "sec.gov/Archives/edgar/data/0000101829/000010182926000031/rtx-20260930.htm"),
 ("Defense Q3 results (Nasdaq/PRN, Oct 21)", "nasdaq.com/press-release/defense-earnings-week-opens-three-raised-forecasts-and-two-record-backlogs-2026-10-21"),
 ("Lockheed guidance (24/7 Wall St, Oct 22)", "247wallst.com/investing/2026/10/22/lockheed-martin-rises-9-as-record-backlog-lifts-outlook-rtx-gains-2-northrop-grumman-advances-3/"),
 ("Defense election selloff (24/7 Wall St, Oct 20)", "247wallst.com/investing/2026/10/20/defense-stocks-are-tumbling-as-wall-street-bets-on-a-democratic-sweep/"),
 ("Rheinmetall and LMT cash flow (MarketScreener)", "marketscreener.com/news/who-gets-paid-to-rearm-the-west-ce785cdfde8cf026"),
 ("NATO 5% target; F126 cancellation (XTB)", "xtb.com/int/market-analysis/news-and-research/european-defence-stocks-in-panic-what-s-next-for-europe-s-rearmament-trade"),
 ("AeroVironment Q4 FY26 (CNBC)", "cnbc.com/2026/06/30/aerovironment-avav-stock-earnings-defense.html"),
 ("Drone stocks YTD (24/7 Wall St, Oct 14)", "247wallst.com/investing/2026/10/14/ondas-retreats-6-despite-regna-ai-launch-with-palantir-aerovironment-drops-3-kratos-slips/"),
 ("Kratos guidance (Parameter)", "parameter.io/top-defense-stocks-benefiting-from-americas-unmanned-warfare-revolution-aerovironment-avav-palantir-pltr-and-kratos/"),
 ("Cameco quote (StockAnalysis)", "stockanalysis.com/stocks/ccj/"),
 ("Cameco uranium price (Motley Fool, Oct 26)", "fool.com/investing/2026/10/26/cameco-stock-is-down-42-from-its-record-here-s-how-i-d-buy-it-around-its-oct-30-report/"),
 ("BWXT/Cameco valuation (Yahoo Finance)", "finance.yahoo.com/energy/articles/nuclear-energy-story-2026-3-175908876.html"),
 ("MP Materials (Motley Fool)", "fool.com/coverage/better-buy/2026/09/10/cameco-vs-mp-materials-which-crucial-renewable-energy-supplier-stock-is-a-better-buy-in-2026/"),
 ("Thermo Fisher Q3 2026", "nasdaq.com/press-release/thermo-fisher-scientific-reports-third-quarter-2026-results-2026-10-21"),
 ("Thermo Fisher guidance raise", "insiderfinance.io/news/thermo-fisher-q3-2026-results-raise-outlook"),
 ("Abbott Q3 2026", "finance.yahoo.com/healthcare/articles/abbott-reports-third-quarter-2026-113000842.html"),
 ("Gilead Q2 2026 (EMJ)", "emjreviews.com/?p=403608"),
 ("Moderna 2026 (Motley Fool, Oct 21)", "fool.com/investing/2026/10/21/not-lilly-not-johnson-johnson-this-stock-will-be-t/"),
 ("WHO avian influenza update, Oct 9 2026", "cdn.who.int/media/docs/default-source/wpro---documents/emergency/surveillance/avian-influenza/ai_20261009.pdf"),
 ("H5N1 by country (Mappr)", "mappr.co/bird-flu-h5n1-by-country/"),
 ("S&P 500 and Fed, Oct 28 (BBN Times)", "bbntimes.com/global-economy/s-p-500-rises-to-7-743-98-for-a-third-straight-gain-as-the-fed-holds-rates-in-a-split-10-2-vote-and-oracle-surges-11"),
 ("Geopolitical risk, Oct 2026 (Tatsu)", "tatsuikeda.substack.com/p/geopolitical-risk-assessment-october"),
 ("Baseline ChatGPT conversation", "chatgpt.com/share/6ae35a35-c880-83e8-aea8-858d8aafa7b6"),
]
s.append(tbl([["Source", "URL (https://)"]] + [[a, b] for a, b in src], [2.4*inch, W-2.4*inch]))

doc.build(s, onFirstPage=page_deco, onLaterPages=page_deco)
print("ok", OUT)
