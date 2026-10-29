# Universe: 100 v1 companies (C-ids) + 8 v2 additions + 9 funds.
# scen = (bear, base, bull) 3-year price multiples. v1 = original 2x illustration (%).
CATNAMES = {
 1: "AI Semiconductors: Compute & Foundry",
 2: "AI Memory & Semiconductor Equipment",
 3: "Hyperscalers & AI Platforms",
 4: "Physical AI & Robotics",
 5: "AI Power & Data-Center Infrastructure",
 6: "AI Software & Cybersecurity",
 7: "US Defense Primes & Defense Electronics",
 8: "Defense Tech, Drones & Allied Rearmament",
 9: "Strategic Resources: Nuclear Fuel & Critical Minerals",
 10: "Biotech, Pandemic Preparedness & AI Drug Discovery",
 11: "Solar & Renewables",
 12: "Fintech & Consumer (outside the 3 themes)",
 13: "Theme Funds (ETFs / closed-end)",
}
THEME = {1: "AI", 2: "AI", 3: "AI", 4: "AI", 5: "AI + energy security", 6: "AI + cyber war",
         7: "War", 8: "War", 9: "War + AI power", 10: "Pandemic", 11: "Energy transition",
         12: "Outside themes", 13: "Diversified"}
TAILWIND = {1: 15, 2: 14, 3: 12, 4: 11, 5: 14, 6: 12, 7: 9, 8: 11, 9: 11, 10: 8, 11: 7, 12: 8, 13: 10}

# ticker -> (cat, v1 2x %, (bear, base, bull))
MAP = {
 # Cat 1
 "NVDA": (1, 50, (0.55, 2.10, 3.75)), "AVGO": (1, 45, (0.55, 1.95, 3.45)), "TSM": (1, 40, (0.60, 1.75, 2.90)),
 "AMD": (1, 37, (0.40, 1.63, 3.40)), "QCOM": (1, 34, (0.60, 1.60, 2.80)), "AMBA": (1, 30, (0.35, 1.35, 3.10)),
 # Cat 2
 "MU": (2, 35, (0.45, 1.55, 3.00)), "SKHY": (2, 35, (0.50, 1.60, 3.00)), "ASML": (2, 35, (0.60, 1.65, 2.80)),
 "KLAC": (2, 30, (0.60, 1.55, 2.60)), "TER": (2, 35, (0.60, 1.65, 2.90)),
 # Cat 3
 "GOOGL": (3, 35, (0.65, 1.65, 2.70)), "AMZN": (3, 40, (0.60, 1.75, 2.95)), "META": (3, 44, (0.60, 1.86, 3.20)),
 "APP": (3, 60, (0.45, 3.10, 5.50)), "MSFT": (3, None, (0.65, 1.55, 2.40)),
 # Cat 4
 "ISRG": (4, 35, (0.75, 1.65, 2.65)), "FANUY": (4, 25, (0.65, 1.45, 2.35)), "KYCCF": (4, 30, (0.70, 1.50, 2.45)),
 "ROK": (4, 20, (0.65, 1.40, 2.25)), "YASKY": (4, 25, (0.60, 1.40, 2.35)), "SYM": (4, 35, (0.40, 1.65, 3.30)),
 "TSLA": (4, 30, (0.25, 1.20, 3.50)), "CGNX": (4, 30, (0.55, 1.50, 2.70)), "NOVT": (4, 24, (0.60, 1.28, 2.40)),
 "SYK": (4, 30, (0.70, 1.60, 2.60)), "DE": (4, 20, (0.55, 1.30, 2.25)), "OUST": (4, 35, (0.25, 1.60, 3.80)),
 "AUR": (4, 30, (0.15, 1.25, 4.00)), "VPG": (4, 30, (0.35, 1.35, 3.25)), "FFR": (4, 15, (0.05, 0.55, 3.50)),
 "EMR": (4, 20, (0.70, 1.40, 2.20)),
 # Cat 5
 "VRT": (5, 46, (0.50, 1.97, 3.80)), "GEV": (5, 31, (0.50, 1.50, 2.70)), "ETN": (5, 31, (0.65, 1.55, 2.70)),
 "NEE": (5, 13, (0.70, 1.27, 2.00)), "AMSC": (5, 32, (0.40, 1.50, 3.00)), "CEG": (5, None, (0.55, 1.60, 2.80)),
 # Cat 6
 "CRWD": (6, 14, (0.25, 0.85, 2.00)), "ZS": (6, 30, (0.45, 1.35, 2.80)), "PLTR": (6, None, (0.35, 1.20, 3.00)),
 "PANW": (6, None, (0.55, 1.45, 2.50)),
 # Cat 7
 "LMT": (7, 20, (0.65, 1.35, 2.15)), "RTX": (7, 25, (0.65, 1.45, 2.30)), "NOC": (7, 15, (0.65, 1.35, 2.10)),
 "GD": (7, 15, (0.70, 1.35, 2.05)), "LHX": (7, 20, (0.65, 1.40, 2.25)), "HII": (7, 25, (0.55, 1.40, 2.50)),
 "CACI": (7, 34, (0.60, 1.65, 2.65)), "TDY": (7, 20, (0.70, 1.40, 2.20)), "CW": (7, 25, (0.65, 1.45, 2.35)),
 "DRS": (7, 30, (0.60, 1.55, 2.65)),
 # Cat 8
 "AVAV": (8, 35, (0.40, 1.75, 3.50)), "KTOS": (8, 35, (0.35, 1.55, 3.60)), "RCAT": (8, 38, (0.20, 1.80, 4.50)),
 "ONDS": (8, 37, (0.25, 1.65, 4.20)), "RNMBY": (8, 45, (0.45, 1.90, 3.75)), "BAESY": (8, 25, (0.65, 1.40, 2.30)),
 "ESLT": (8, 25, (0.40, 1.30, 2.70)),
 # Cat 9
 "CCJ": (9, 31, (0.45, 1.45, 3.00)), "BWXT": (9, 27, (0.65, 1.43, 2.50)), "UUUU": (9, 30, (0.25, 1.40, 3.50)),
 "MP": (9, 35, (0.30, 1.50, 3.50)), "USAR": (9, 35, (0.20, 1.40, 3.75)), "LYSDY": (9, 35, (0.45, 1.65, 3.20)),
 "ALB": (9, 35, (0.45, 1.55, 3.10)), "NOPMF": (9, 35, (0.50, 1.60, 2.90)), "MTRN": (9, 25, (0.65, 1.40, 2.25)),
 "ATI": (9, 25, (0.60, 1.45, 2.45)), "ALM": (9, 30, (0.25, 1.30, 3.25)), "FCX": (9, 34, (0.45, 1.57, 3.00)),
 # Cat 10
 "REGN": (10, 30, (0.65, 1.55, 2.55)), "ABCL": (10, 30, (0.15, 1.40, 4.00)), "ADPT": (10, 29, (0.30, 1.30, 3.10)),
 "TEM": (10, 35, (0.35, 1.70, 3.60)), "SDGR": (10, 30, (0.30, 1.40, 3.25)), "3696": (10, 30, (0.20, 1.50, 4.00)),
 "RXRX": (10, 30, (0.15, 1.35, 4.25)), "GENB": (10, 30, (0.15, 1.30, 4.00)), "ABSI": (10, 30, (0.12, 1.25, 4.25)),
 "TMO": (10, None, (0.70, 1.35, 2.00)), "ABT": (10, None, (0.75, 1.30, 1.85)), "GILD": (10, None, (0.70, 1.35, 2.00)),
 "MRNA": (10, None, (0.20, 0.90, 3.00)),
 # Category 11
 "NXT": (11, 44, (0.55, 1.97, 3.10)), "FSLR": (11, 38, (0.40, 1.71, 3.20)), "ENPH": (11, 38, (0.35, 1.60, 3.80)),
 "SHLS": (11, 38, (0.40, 1.71, 3.20)), "ARRY": (11, 46, (0.30, 2.25, 4.00)), "FLNC": (11, 37, (0.18, 1.60, 4.50)),
 "RUN": (11, 29, (0.15, 1.10, 3.50)), "ENLT": (11, 37, (0.45, 1.75, 3.40)), "ELVA": (11, 34, (0.35, 1.50, 3.50)),
 "TOYO": (11, 37, (0.15, 1.60, 5.00)), "CSIQ": (11, 33, (0.25, 1.30, 4.00)), "SEDG": (11, 33, (0.25, 1.35, 3.40)),
 "BLDP": (11, 28, (0.25, 1.15, 3.50)), "TURB": (11, 32, (0.12, 1.10, 4.00)), "WAVE": (11, 26, (0.10, 0.90, 4.00)),
 "PBK": (11, 13, (0.03, 0.65, 3.00)), "BRNX": (11, 14, (0.01, 0.40, 3.00)),
 # Category 12
 "NU": (12, 61, (0.65, 2.57, 4.20)), "SOFI": (12, 50, (0.40, 2.52, 4.30)), "TBBK": (12, 45, (0.45, 1.91, 3.20)),
 "MELI": (12, 40, (0.55, 1.71, 3.40)), "PDD": (12, 41, (0.35, 1.75, 3.30)), "CELH": (12, 36, (0.40, 1.63, 3.20)),
 "LULU": (12, 27, (0.45, 1.31, 2.70)),
 # Funds
 "SOXX": (13, 35, (0.60, 1.60, 2.75)), "XSD": (13, 30, (0.55, 1.50, 2.65)), "SMH": (13, 40, (0.55, 1.70, 3.00)),
 "REMX": (13, 30, (0.45, 1.40, 2.90)), "EART": (13, 30, (0.50, 1.40, 2.75)), "BOT": (13, 25, (0.20, 1.05, 3.50)),
 "KOID": (13, 30, (0.50, 1.50, 2.90)), "BOTT": (13, 30, (0.55, 1.45, 2.70)), "THNQ": (13, 30, (0.55, 1.50, 2.70)),
}
FUNDNAMES = {"SOXX": "iShares Semiconductor ETF", "XSD": "SPDR S&P Semiconductor ETF", "SMH": "VanEck Semiconductor ETF",
  "REMX": "VanEck Rare Earth & Strategic Metals ETF", "EART": "Critical Materials ETF (ex-DMAT)", "BOT": "RoboStrategy (closed-end)",
  "KOID": "KraneShares Humanoid Robotics & Physical AI ETF", "BOTT": "Themes Humanoid Robotics ETF", "THNQ": "ROBO Global Artificial Intelligence ETF"}

# v2 additions (no v1 dossier): approximate fundamentals from Oct 2026 releases; FS estimated with v1 rubric.
NEW = {
 "MSFT": dict(name="Microsoft", fs=92, cagr=16.0, opm=46.8, fcfm=None, price="CONDITIONAL", pe="~30x", note="FY26 rev >$331B (+18%), op income >$155B; FCF positive while peers negative"),
 "PLTR": dict(name="Palantir Technologies", fs=86, cagr=60.0, opm=60.0, fcfm=56.0, price="DEMANDING", pe="~120x+ fwd", note="FY26 guide $8.15B (+82%); adj op inc $4.89B; adj FCF $4.5-4.7B"),
 "CEG": dict(name="Constellation Energy", fs=65, cagr=None, opm=None, fcfm=None, price="CONDITIONAL", pe="~27x", note="Largest US nuclear fleet; hyperscaler power deals; Q3 pending"),
 "PANW": dict(name="Palo Alto Networks", fs=70, cagr=15.0, opm=None, fcfm=None, price="DEMANDING", pe="high", note="Record fiscal Q4; ~$18B backlog"),
 "TMO": dict(name="Thermo Fisher Scientific", fs=80, cagr=4.0, opm=24.5, fcfm=None, price="CONDITIONAL", pe="~22x fwd", note="Q3 rev $12.14B (+9%); FY guide raised to $47.7-48.2B"),
 "ABT": dict(name="Abbott Laboratories", fs=82, cagr=6.0, opm=None, fcfm=None, price="CONDITIONAL", pe="~25x fwd", note="Q3 sales +14.5% (7% comparable); diagnostics +46.7% incl. Exact Sciences"),
 "GILD": dict(name="Gilead Sciences", fs=78, cagr=6.0, opm=None, fcfm=None, price="SUPPORTED", pe="~15x fwd", note="Q2 rev $7.8B (+10%); no major LOE until 2036"),
 "MRNA": dict(name="Moderna", fs=38, cagr=-20.0, opm=None, fcfm=None, price="NOT ESTABLISHED", pe="loss", note="+600% in 2026 on cancer-vaccine data; H1 rev $534M, net loss $2.1B"),
}

# Post-v1-cutoff evidence adjustments to the base multiple (documented).
ADJ = {
 "VRT": (1.07, "Q3 (Oct 28): organic orders >100% y/y; FY guide +$650M"),
 "GEV": (1.08, "Q3 (Oct 28): backlog $176B -> ~$197B; orders +96%"),
 "GOOGL": (1.06, "Shares -10% on Oct 29 lowers entry; offset by negative FCF"),
 "META": (0.97, "Negative FCF (-$2.1B) and capex raise"),
 "RNMBY": (0.95, "Operating FCF -$1.81B in H1; -35% YTD on program cancellation"),
 "AVAV": (0.95, "Restatement and $1.5B SCAR backlog reversal"),
}
# Forward growth overrides (latest quarter y/y revenue growth, from Q2/Q3 2026 filings) used in the factor model.
FWD = {"NVDA": 106, "AVGO": 86, "TSM": 41, "AMD": 50, "MU": 379, "GOOGL": 25, "VRT": 61, "GEV": 25,
       "CRWD": 26, "RTX": 11, "LMT": 11, "NOC": 7, "TMO": 9, "PLTR": 93}
