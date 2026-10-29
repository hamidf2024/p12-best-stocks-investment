p='build_v2.py'; t=open(p).read()
def rep(a,b):
    global t
    assert a in t, a[:70]; t=t.replace(a,b)
rep("R = json.load(open('/tmp/outputs/model_results.json'))\nfor r in R: r['ens_pct'] = round(r['ens'] * 100)",
"R = json.load(open('/tmp/outputs/model_results_final.json'))\nMLR = json.load(open('/tmp/outputs/ml/ml_results.json'))\nfor r in R:\n    r['ens'] = r['final']; r['ens_pct'] = round(r['final'] * 100)\n    r['risk'] = r['mlloss'] if r['mlloss'] is not None else r['loss']\nfmtp = lambda v: '-' if v is None else f'{v*100:.0f}%'")
rep('"Version 2: which stocks could double by October 2029? All 117 holdings categorized, financially evaluated and run through a doubling-prediction model."',
    '"Version 2.1: which stocks could double by October 2029? All 117 holdings categorized, financially evaluated, and scored by a machine-learning model trained and tested on 1967-2026 stock history, combined with a fundamentals model."')
rep('["Prediction model", "Ensemble of (1) a scenario simulation over each stock\'s bear/base/bull 3-year outcomes and (2) a fundamentals factor model (growth, valuation, financial strength, theme tailwind, downside risk). Output: probability of being at least 2x by Oct 2029."],',
    '["Prediction models", "(1) Trained ML model: gradient boosting + logistic regression trained on 66,010 historical cases (690 stocks, start dates 1967-2023), walk-forward tested on unseen years, calibrated. (2) Rules model: v1 scenarios + fundamentals factor score. Final P(2x) = 50/50 blend. The ML model also predicts the chance of losing half your money."],\n  ["What the testing showed", "On unseen years the ML model\'s top 10% of picks doubled 31-34% of the time vs an 18-22% base rate (about 1.6x better). Doubling is only weakly predictable (AUC 0.58-0.63); big losses are much more predictable (AUC 0.75)."],')
rep('f"Tier A quality doubling candidates: {cnt[\'A\']}. Tier B high upside / higher risk: {cnt[\'B\']}. Tier C possible: {cnt[\'C\']}. No stock exceeds ~66%; even the best is far from certain."',
    'f"Tier A (final P(2x) 30%+, FS 70+, ML loss risk 15% or less): {cnt[\'A\']}. Tier B (30%+, higher risk): {cnt[\'B\']}. Tier C (25-29%): {cnt[\'C\']}. The best final score is ~46%: no stock is close to a sure double."')
rep("The model cannot see the future: its probabilities come from analyst scenarios and judgment-weighted factors, not from a model trained on historical outcomes.",
    "The models cannot see the future. The ML model learned from past price behaviour only (no historical fundamentals were available), its training data lacks most delisted companies, and past patterns may not repeat.")
rep('P("Sorted by ensemble probability of a price at least 2x by October 2029. Row colour = tier (green A, yellow B, blue C). Financial columns come from the v1 dossiers (latest TTM) unless marked as a v2 addition.", NOTE)]',
    'P("Sorted by final P(2x by Oct 2029) = 50% trained ML model + 50% rules model. ML P(-50%) = trained model\'s chance the stock ends at half or less. Row colour = tier (green A, yellow B, blue C). Financials from the v1 dossiers unless marked v2.", NOTE)]')
rep('rows = [["#", "Ticker / company", "Category", "P(2x) ens.", "Scen. / Factor", "P(-50%)", "FS", "Rev CAGR", "Op mgn", "Price balance", "Driver to watch", "Main risk"]]',
    'rows = [["#", "Ticker / company", "Category", "Final P(2x)", "ML / Rules", "ML P(-50%)", "FS", "Rev growth", "Op mgn", "Price balance", "Driver to watch", "Main risk"]]')
rep('f"<b>{r[\'ens_pct\']}%</b>", f"{r[\'mc\']*100:.0f}% / {r[\'fp\']*100:.0f}%", f"{r[\'loss\']*100:.0f}%", r[\'fs\'],',
    'f"<b>{r[\'ens_pct\']}%</b>", f"{fmtp(r[\'ml\'])}{\'*\' if r[\'ml_imputed\'] else \'\'} / {r[\'rules\']*100:.0f}%", fmtp(r[\'mlloss\']), r[\'fs\'],')
rep('s += [P("Rev CAGR = two-year historical revenue CAGR from v1,', 's += [P("* = too little price history for the ML model; the universe median (20%) is used in the blend. Rev growth = two-year historical revenue CAGR from v1,')
rep("ax.axhline(40, color='#888', lw=0.8, ls='--')", "ax.axhline(30, color='#888', lw=0.8, ls='--')")
rep('ax.text(71, 66, "Tier A zone: P(2x) 40%+ and FS 70+", fontsize=7.5, color=\'#444\')', 'ax.text(71, 45, "Tier A zone: final P(2x) 30%+ and FS 70+", fontsize=7.5, color=\'#444\')')
rep('ax.set_ylabel("Model P(price 2x by Oct 2029), %"', 'ax.set_ylabel("Final P(price 2x by Oct 2029), %"')
rep('P("3. The doubling-prediction model", H1),', 'P("3. Rules model: scenarios + fundamentals (50% of the final score)", H1),')
rep('P("<b>Ensemble.</b> P(2x) = average of the two components. Tiers: <b>A</b> P 40%+, FS 70+, bear multiple 0.45+; <b>B</b> P 40%+ otherwise; <b>C</b> 30-39%; <b>D</b> 20-29%; <b>E</b> under 20%. Funds use component 1 only.", B)',
    'P("<b>Rules score</b> = average of the two components (funds use component 1 only). It is blended 50/50 with the trained ML model (section 4). Final tiers: <b>A</b> final P(2x) 30%+, FS 70+ and ML loss risk 15% or less; <b>B</b> 30%+ otherwise; <b>C</b> 25-29%; <b>D</b> 18-24%; <b>E</b> under 18%.", B)')
rep('["Limits", "No model trained on historical outcomes", "No historical price database is reachable from this environment. Weights are analyst choices, documented so you can change them."]]',
    '["Limits", "Weights are analyst choices", "This half cannot be back-tested because historical fundamentals were not available; the ML half (section 4) supplies the tested evidence."]]')
rep('["Universe average", f"{statistics.mean(r[\'ens\'] for r in R)*100:.0f}% mean P(2x)"', '["Universe average", f"{statistics.mean(r[\'rules\'] for r in R)*100:.0f}% mean rules P(2x)"')
ml_section = open('/tmp/outputs/ml_section.txt').read()
rep("# ---------------- Category pages ----------------", ml_section + "\n# ---------------- Category pages ----------------")
rep('rows = [["Ticker / company", "FS", "Rev CAGR", "Op mgn", "FCF mgn", "Net cash (debt)", "Share CAGR", "P/E", "P/FCF", "Price balance", "Bear/base/bull", "Scen.", "Factor (DPS)", "P(2x)", "Tier"]]',
    'rows = [["Ticker / company", "FS", "Rev CAGR", "Op mgn", "FCF mgn", "Net cash (debt)", "Share CAGR", "P/E", "P/FCF", "Price balance", "Bear/base/bull", "Rules P(2x)", "ML P(2x)", "ML P(-50%)", "Final P(2x)", "Tier"]]')
rep('f"{r[\'bear\']}/{r[\'base\']}/{r[\'bull\']}", f"{r[\'mc\']*100:.0f}%", f"{r[\'fp\']*100:.0f}% ({r[\'dps\']:.0f})", f"<b>{r[\'ens_pct\']}%</b>", r[\'tier\'][0]])',
    'f"{r[\'bear\']}/{r[\'base\']}/{r[\'bull\']}", f"{r[\'rules\']*100:.0f}%", fmtp(r[\'ml\']) + (\'*\' if r[\'ml_imputed\'] else \'\'), fmtp(r[\'mlloss\']), f"<b>{r[\'ens_pct\']}%</b>", r[\'tier\'][0]])')
rep("[W-7.35*inch, 0.3*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.8*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.7*inch, 0.75*inch, 0.4*inch, 0.65*inch, 0.45*inch, 0.3*inch]",
    "[W-7.85*inch, 0.3*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.8*inch, 0.5*inch, 0.45*inch, 0.45*inch, 0.7*inch, 0.75*inch, 0.45*inch, 0.45*inch, 0.5*inch, 0.5*inch, 0.3*inch]")
rep("Scen. = scenario-simulation P(2x); Factor = fundamentals model P(2x) with its score; P(2x) = ensemble.", "Rules = scenarios + fundamentals model; ML = trained model (* = too little history, median used); Final = 50/50 blend.")
rep('rows = [["Ticker", "Fund", "Bear / base / bull", "P(2x)", "P(-50%)", "Tier"]]', 'rows = [["Ticker", "Fund", "Bear / base / bull", "Final P(2x)", "ML P(-50%)", "Tier"]]')
rep('f"<b>{r[\'ens_pct\']}%</b>", f"{r[\'loss\']*100:.0f}%", r[\'tier\']])', 'f"<b>{r[\'ens_pct\']}%</b>", fmtp(r[\'mlloss\']), r[\'tier\']])')
rep('f"{r[\'ens_pct\']}%", f"{r[\'loss\']*100:.0f}%", r[\'fs\'] if', 'f"{r[\'ens_pct\']}%", f"{r[\'risk\']*100:.0f}%", r[\'fs\'] if')
rep('"Appendix A. Full ranking of all 117 investments by doubling probability"', '"Appendix A. Full ranking of all 117 investments by final doubling probability"')
open(p,'w').write(t); print('patched')
