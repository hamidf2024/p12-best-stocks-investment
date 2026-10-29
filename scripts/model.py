import json, math, sys
sys.path.insert(0, '/tmp/outputs')
from model_data import *
D = json.load(open(sys.argv[1]))
byTk = {d['tk']: d for d in D.values()}
alias = {"TSM": "TSM", "SKHY": "SKHY"}
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
SIG = 0.25  # within-scenario log-volatility of the 3-year terminal multiple
W = (0.25, 0.50, 0.25)

def num(s):
    try: return float(str(s).replace(',', '').replace('%', '').replace('x', ''))
    except: return None

def mc(b, m, u):
    p2 = sum(w * (1 - Phi((math.log(2) - math.log(x)) / SIG)) for w, x in zip(W, (b, m, u)))
    pl = sum(w * Phi((math.log(0.5) - math.log(x)) / SIG) for w, x in zip(W, (b, m, u)))
    med_log = sum(w * math.log(x) for w, x in zip(W, (b, m, u)))
    return p2, pl, math.exp(med_log)

def growth_pts(g):
    if g is None: return 8
    return 30 if g >= 40 else 25 if g >= 25 else 19 if g >= 15 else 12 if g >= 8 else 6 if g >= 0 else 2

def val_pts(label, pe):
    label = (label or '').upper()
    if 'SUPPORTED' in label: return 18
    if 'CONDITIONAL' in label: return 14
    if 'DEMANDING' in label: return 10 if (pe is not None and pe < 30) else 7
    if 'FUNDING' in label: return 5
    return 5

def risk_pts(bear, dil):
    r = 15 if bear >= 0.65 else 12 if bear >= 0.55 else 9 if bear >= 0.45 else 6 if bear >= 0.35 else 4 if bear >= 0.25 else 2
    if dil is not None and dil > 10: r -= 3
    return max(r, 0)

def factor_p(dps):
    return 0.65 / (1 + math.exp(-(dps - 68) / 9))

def tier(p, fs, bear):
    if p >= 0.40 and (fs or 0) >= 70 and bear >= 0.45: return "A - Quality doubling candidate"
    if p >= 0.40: return "B - High upside, higher risk"
    if p >= 0.30: return "C - Possible, needs strong execution"
    if p >= 0.20: return "D - Compounder, doubling unlikely"
    return "E - Low doubling odds / speculative"

out = []
for tk, (cat, v1p, sc) in MAP.items():
    b, m, u = sc
    adjnote = ''
    if tk in ADJ:
        f, adjnote = ADJ[tk]; b, m, u = b * f, m * f, u * f
    p2, pl, med = mc(b, m, u)
    rec = dict(tk=tk, cat=cat, v1=v1p, bear=round(b, 2), base=round(m, 2), bull=round(u, 2), mc=p2, loss=pl, med=med, adj=adjnote)
    if cat == 13:
        rec.update(name=FUNDNAMES[tk], fs=None, src='Fund')
        rec['dps'] = None; rec['fp'] = None; rec['ens'] = p2
    else:
        if tk in NEW:
            n = NEW[tk]; rec.update(name=n['name'], fs=n['fs'], cagr=n['cagr'], opm=n['opm'], fcfm=n['fcfm'], price=n['price'],
                                    pe_s=n['pe'], pfcf_s='', netcash='', dil=None, cur='USD', src='v2 addition', note=n['note'], cid='new')
            pe = None
        else:
            d = byTk[tk]
            cash, debt = num(d['cash']), num(d['debt'])
            rev, fcf = num(d['rev']), num(d['fcf'])
            fcfm = num(d['fcfm']) if d['fcfm'] else (round(100 * fcf / rev, 1) if (fcf is not None and rev) else None)
            rec.update(name=d['name'], fs=int(d['fs']), cagr=num(d['cagr']), opm=num(d['opm']), fcfm=fcfm, price=d['price'].title(),
                       pe_s=d['pe'] or 'N/M', pfcf_s=d['pfcf'] or 'N/M', dil=num(d['dil']), cur=d['cur'], cid=d['cid'], src='v1 dossier',
                       netcash=(cash - debt) if (cash is not None and debt is not None) else None, note='')
            pe = num(d['pe'])
        g = FWD.get(tk, rec['cagr'])
        gp = growth_pts(g); vp = val_pts(rec['price'], pe); fsp = rec['fs'] / 5
        tw = TAILWIND[cat]; rp = risk_pts(b, rec.get('dil'))
        dps = gp + vp + fsp + tw + rp
        rec.update(gp=gp, vp=vp, fsp=round(fsp, 1), tw=tw, rp=rp, dps=round(dps, 1), fp=factor_p(dps), gused=g)
        rec['ens'] = 0.5 * p2 + 0.5 * rec['fp']
    rec['tier'] = tier(rec['ens'], rec.get('fs') if rec.get('fs') is not None else 75, b)
    out.append(rec)
json.dump(out, open('/tmp/outputs/model_results.json', 'w'), indent=0)
out.sort(key=lambda r: -r['ens'])
print(len(out))
for r in out[:40]:
    print(f"{r['tk']:6} c{r['cat']:2} ens {r['ens']*100:4.0f}% mc {r['mc']*100:4.0f}% fp {(r['fp'] or 0)*100:4.0f}% dps {r['dps']} fs {r.get('fs')} v1 {r['v1']} loss {r['loss']*100:3.0f}% {r['tier']}")
import collections
print(collections.Counter(r['tier'][0] for r in out))
