// Core ML pipeline: features, labels, gradient boosting, logistic regression, metrics.
// Works on window.PX = {ticker: {m: ['YYYY-MM',...], p: [adjclose,...]}} and window.MKT = {m:[], p:[]}
var ML = (function () {
  const H = 36; // forward horizon in months
  const FEAT = ['mom3', 'mom12', 'mom12x1', 'mom36', 'mom60', 'vol12', 'vol36', 'dd36', 'maxret12', 'trend60',
                'age', 'beta36', 'rel12', 'mkt12', 'mkt36', 'mktTrend120', 'mktVol12'];
  function mIdx(m) { return (+m.slice(0, 4)) * 12 + (+m.slice(5, 7)) - 1; }
  function idxM(i) { const y = Math.floor(i / 12), mo = i % 12 + 1; return y + '-' + String(mo).padStart(2, '0'); }
  function std(a) { const n = a.length; if (n < 2) return NaN; let m = 0; for (const x of a) m += x; m /= n; let v = 0; for (const x of a) v += (x - m) ** 2; return Math.sqrt(v / (n - 1)); }

  function marketSeries(MKT) {
    const base = mIdx(MKT.m[0]); const lp = MKT.p.map(Math.log);
    const ret = lp.map((x, i) => i ? x - lp[i - 1] : 0);
    return { base, lp, ret };
  }

  // Build a dense monthly log-price array for one ticker (forward-fill gaps up to 2 months; otherwise break)
  function dense(s) {
    const base = mIdx(s.m[0]), last = mIdx(s.m[s.m.length - 1]);
    const lp = new Array(last - base + 1).fill(NaN);
    for (let i = 0; i < s.m.length; i++) { const v = s.p[i]; if (v > 0 && isFinite(v)) lp[mIdx(s.m[i]) - base] = Math.log(v); }
    for (let i = 1; i < lp.length; i++) if (isNaN(lp[i]) && !isNaN(lp[i - 1]) && (i < 2 || !isNaN(lp[i - 2]))) lp[i] = lp[i - 1];
    return { base, lp };
  }

  function featuresAt(d, t, M, firstValid, L) {
    L = L || 60; const lp = d.lp; if (t < L) return null;
    for (let k = t - L; k <= t; k++) if (isNaN(lp[k])) return null;
    const r = []; for (let k = t - 35; k <= t; k++) r.push(lp[k] - lp[k - 1]);
    const r12 = r.slice(-12);
    let mx = -1e9; for (let k = t - 36; k <= t; k++) mx = Math.max(mx, lp[k]);
    let avg = 0; for (let k = t - L + 1; k <= t; k++) avg += Math.exp(lp[k] - lp[t]); avg /= L;
    const gi = d.base + t - M.base; // global month index into market
    if (gi < 120 || gi >= M.lp.length) return null;
    const mr = []; for (let k = gi - 35; k <= gi; k++) mr.push(M.ret[k]);
    let mm = 0, sm = 0; for (let i = 0; i < 36; i++) { mm += mr[i]; sm += r[i]; } mm /= 36; sm /= 36;
    let cov = 0, vm = 0; for (let i = 0; i < 36; i++) { cov += (r[i] - sm) * (mr[i] - mm); vm += (mr[i] - mm) ** 2; }
    let mavg = 0; for (let k = gi - 119; k <= gi; k++) mavg += Math.exp(M.lp[k] - M.lp[gi]); mavg /= 120;
    const mom12 = lp[t] - lp[t - 12], mkt12 = M.lp[gi] - M.lp[gi - 12];
    return [lp[t] - lp[t - 3], mom12, lp[t - 1] - lp[t - 12], lp[t] - lp[t - 36], lp[t] - lp[t - L],
            std(r12) * Math.sqrt(12), std(r) * Math.sqrt(12), lp[t] - mx, Math.max(...r12), -Math.log(avg),
            Math.log(1 + (t - firstValid) / 12), vm > 0 ? cov / vm : 1, mom12 - mkt12, mkt12, M.lp[gi] - M.lp[gi - 36],
            -Math.log(mavg), std(mr.slice(-12)) * Math.sqrt(12)];
  }

  function buildDataset(PX, MKT, step, L) {
    L = L || 60;
    const M = marketSeries(MKT); const X = [], y = [], meta = [];
    for (const tk in PX) {
      const s = PX[tk]; if (!s || s.m.length < 100) continue;
      const d = dense(s); let first = 0; while (first < d.lp.length && isNaN(d.lp[first])) first++;
      for (let t = L; t + H < d.lp.length; t += step) {
        if (isNaN(d.lp[t + H])) continue;
        const f = featuresAt(d, t, M, first, L); if (!f || f.some(v => !isFinite(v))) continue;
        X.push(f); y.push(d.lp[t + H] - d.lp[t] >= Math.log(2) ? 1 : 0); meta.push([tk, d.base + t]);
      }
    }
    return { X, y, meta };
  }
  function latestFeatures(PX, MKT, tickers, L) {
    L = L || 60;
    const M = marketSeries(MKT); const out = {};
    for (const tk of tickers) {
      const s = PX[tk]; if (!s || s.m.length < L + 1) { out[tk] = null; continue; }
      const d = dense(s); let first = 0; while (isNaN(d.lp[first])) first++;
      const t = d.lp.length - 1; const f = featuresAt(d, t, M, first, L);
      out[tk] = f && f.every(v => isFinite(v)) ? f : null;
    }
    return out;
  }

  // ---------- Histogram gradient boosting (binary logloss) ----------
  function makeBins(X, nb) {
    const p = X[0].length, edges = [];
    for (let j = 0; j < p; j++) {
      const col = X.map(r => r[j]).sort((a, b) => a - b); const e = [];
      for (let b = 1; b < nb; b++) e.push(col[Math.floor(b * col.length / nb)]);
      edges.push([...new Set(e)]);
    }
    return edges;
  }
  function binX(X, edges) {
    return X.map(r => r.map((v, j) => { const e = edges[j]; let lo = 0, hi = e.length; while (lo < hi) { const mid = (lo + hi) >> 1; if (v > e[mid]) lo = mid + 1; else hi = mid; } return lo; }));
  }
  function trainGBM(X, y, opt) {
    opt = Object.assign({ rounds: 250, lr: 0.05, depth: 3, nb: 32, minLeaf: 200, lambda: 5, sub: 0.7, seed: 7 }, opt || {});
    const n = X.length, p = X[0].length; const edges = makeBins(X, opt.nb); const B = binX(X, edges);
    const ybar = y.reduce((a, b) => a + b, 0) / n; const f0 = Math.log(ybar / (1 - ybar));
    const F = new Float64Array(n).fill(f0); const trees = []; let seed = opt.seed;
    const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
    const gain = (G, Hh) => G * G / (Hh + opt.lambda);
    for (let it = 0; it < opt.rounds; it++) {
      const g = new Float64Array(n), h = new Float64Array(n);
      for (let i = 0; i < n; i++) { const pr = 1 / (1 + Math.exp(-F[i])); g[i] = pr - y[i]; h[i] = Math.max(pr * (1 - pr), 1e-6); }
      let idx = []; for (let i = 0; i < n; i++) if (rnd() < opt.sub) idx.push(i);
      const tree = build(idx, 0);
      trees.push(tree);
      for (let i = 0; i < n; i++) F[i] += opt.lr * predTree(tree, B[i]);
      function build(ids, dep) {
        let G = 0, Hs = 0; for (const i of ids) { G += g[i]; Hs += h[i]; }
        const leaf = { v: -G / (Hs + opt.lambda) };
        if (dep >= opt.depth || ids.length < 2 * opt.minLeaf) return leaf;
        let best = null;
        for (let j = 0; j < p; j++) {
          const nbj = edges[j].length + 1; const gh = new Float64Array(nbj), hh = new Float64Array(nbj), cc = new Int32Array(nbj);
          for (const i of ids) { const b = B[i][j]; gh[b] += g[i]; hh[b] += h[i]; cc[b]++; }
          let gl = 0, hl = 0, cl = 0;
          for (let b = 0; b < nbj - 1; b++) {
            gl += gh[b]; hl += hh[b]; cl += cc[b];
            if (cl < opt.minLeaf || ids.length - cl < opt.minLeaf) continue;
            const sc = gain(gl, hl) + gain(G - gl, Hs - hl) - gain(G, Hs);
            if (!best || sc > best.sc) best = { sc, j, b };
          }
        }
        if (!best || best.sc <= 0) return leaf;
        const L = [], R = []; for (const i of ids) (B[i][best.j] <= best.b ? L : R).push(i);
        return { j: best.j, b: best.b, l: build(L, dep + 1), r: build(R, dep + 1), sc: best.sc };
      }
    }
    return { trees, f0, lr: opt.lr, edges };
  }
  function predTree(t, xb) { while (t.l) t = xb[t.j] <= t.b ? t.l : t.r; return t.v; }
  function predictGBM(m, X) {
    const B = binX(X, m.edges);
    return B.map(xb => { let f = m.f0; for (const t of m.trees) f += m.lr * predTree(t, xb); return 1 / (1 + Math.exp(-f)); });
  }
  function importance(m, p) {
    const imp = new Array(p).fill(0);
    const walk = t => { if (!t.l) return; imp[t.j] += t.sc; walk(t.l); walk(t.r); };
    m.trees.forEach(walk); const s = imp.reduce((a, b) => a + b, 0); return imp.map(v => v / s);
  }

  // ---------- Logistic regression (standardized, L2, full-batch GD) ----------
  function trainLR(X, y, iters, l2) {
    iters = iters || 400; l2 = l2 || 1e-3; const n = X.length, p = X[0].length;
    const mu = new Array(p).fill(0), sd = new Array(p).fill(0);
    for (const r of X) r.forEach((v, j) => mu[j] += v / n); for (const r of X) r.forEach((v, j) => sd[j] += (v - mu[j]) ** 2 / n);
    for (let j = 0; j < p; j++) sd[j] = Math.sqrt(sd[j]) || 1;
    const Z = X.map(r => r.map((v, j) => Math.max(-5, Math.min(5, (v - mu[j]) / sd[j]))));
    let w = new Array(p).fill(0), b = 0;
    for (let it = 0; it < iters; it++) {
      const gw = new Array(p).fill(0); let gb = 0;
      for (let i = 0; i < n; i++) { let z = b; for (let j = 0; j < p; j++) z += w[j] * Z[i][j]; const e = 1 / (1 + Math.exp(-z)) - y[i]; gb += e; for (let j = 0; j < p; j++) gw[j] += e * Z[i][j]; }
      b -= 0.5 * gb / n; for (let j = 0; j < p; j++) w[j] -= 0.5 * (gw[j] / n + l2 * w[j]);
    }
    return { w, b, mu, sd };
  }
  function predictLR(m, X) { return X.map(r => { let z = m.b; r.forEach((v, j) => z += m.w[j] * Math.max(-5, Math.min(5, (v - m.mu[j]) / m.sd[j]))); return 1 / (1 + Math.exp(-z)); }); }

  // ---------- Metrics ----------
  function auc(p, y) {
    const o = p.map((v, i) => [v, y[i]]).sort((a, b) => a[0] - b[0]); let rank = 0, sp = 0, np = 0, nn = 0;
    for (let i = 0; i < o.length; i++) { rank = i + 1; if (o[i][1]) { sp += rank; np++; } else nn++; }
    return (sp - np * (np + 1) / 2) / (np * nn);
  }
  function topK(p, y, frac) { const o = p.map((v, i) => [v, y[i]]).sort((a, b) => b[0] - a[0]); const k = Math.max(1, Math.floor(o.length * frac)); let s = 0; for (let i = 0; i < k; i++) s += o[i][1]; return s / k; }
  function deciles(p, y) { const o = p.map((v, i) => [v, y[i]]).sort((a, b) => a[0] - b[0]); const out = []; for (let d = 0; d < 10; d++) { const a = Math.floor(d * o.length / 10), b = Math.floor((d + 1) * o.length / 10); let sp = 0, sy = 0; for (let i = a; i < b; i++) { sp += o[i][0]; sy += o[i][1]; } out.push([+(sp / (b - a)).toFixed(3), +(sy / (b - a)).toFixed(3)]); } return out; }
  function brier(p, y) { let s = 0; for (let i = 0; i < p.length; i++) s += (p[i] - y[i]) ** 2; return s / p.length; }
  return { FEAT, H, mIdx, idxM, buildDataset, latestFeatures, trainGBM, predictGBM, importance, trainLR, predictLR, auc, topK, deciles, brier };
})();
if (typeof module !== 'undefined') module.exports = ML;
