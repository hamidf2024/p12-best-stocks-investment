const ML=require('./core.js');
let seed=1; const rnd=()=>{seed=(seed*16807)%2147483647; return seed/2147483647}; const gauss=()=>Math.sqrt(-2*Math.log(rnd()))*Math.cos(2*Math.PI*rnd());
const months=[]; for(let i=ML.mIdx('1970-01');i<=ML.mIdx('2026-10');i++) months.push(ML.idxM(i));
const MKT={m:months,p:[]}; let v=100; for(const m of months){v*=Math.exp(0.007+0.04*gauss()); MKT.p.push(v)}
const PX={}; for(let k=0;k<300;k++){ const st=Math.floor(rnd()*300); const q=0.002+0.01*rnd(); let x=10, ps=[], ms=[]; let mom=0;
 for(let i=st;i<months.length;i++){ const r=q+0.09*gauss()+0.15*mom/12; mom=0.92*mom+r; x*=Math.exp(r); ps.push(x); ms.push(months[i]); } PX['T'+k]={m:ms,p:ps}; }
let t0=Date.now(); const D=ML.buildDataset(PX,MKT,3); console.log('rows',D.X.length,'pos',D.y.reduce((a,b)=>a+b)/D.y.length, (Date.now()-t0)+'ms');
const tr=[],te=[]; D.meta.forEach((m,i)=> (m[1]<=ML.mIdx('2005-12')?tr:m[1]>=ML.mIdx('2009-01')?te:null)?.push(i));
const sel=(ix)=>({X:ix.map(i=>D.X[i]),y:ix.map(i=>D.y[i])}); const A=sel(tr),B=sel(te);
t0=Date.now(); const g=ML.trainGBM(A.X,A.y,{rounds:150}); console.log('gbm train', Date.now()-t0,'ms');
const pg=ML.predictGBM(g,B.X); const l=ML.trainLR(A.X,A.y,200); const pl=ML.predictLR(l,B.X);
console.log('test AUC gbm',ML.auc(pg,B.y).toFixed(3),'lr',ML.auc(pl,B.y).toFixed(3),'base',(B.y.reduce((a,b)=>a+b)/B.y.length).toFixed(3),'top10 gbm',ML.topK(pg,B.y,.1).toFixed(3));
console.log(ML.importance(g,ML.FEAT.length).map((v,j)=>ML.FEAT[j]+':'+v.toFixed(2)).join(' '));
const L=ML.latestFeatures(PX,MKT,['T1','T2']); console.log(Object.values(L).map(f=>f&&f.length));
