import re,sys,json
T=open(sys.argv[1]).read()
parts=re.split(r'\n(C\d{3}) \| (.+?) \| (\S+)\n',T)
D={}
for i in range(1,len(parts),4):
    cid,name,tk,body=parts[i],parts[i+1],parts[i+2],parts[i+3]
    if cid in D: continue
    body=body.split('FINANCIAL STRENGTH IS NOT A RETURN')[0]
    g=lambda pat: (re.search(pat,body,re.S).group(1) if re.search(pat,body,re.S) else '')
    flat=re.sub(r'\s+',' ',body)
    f=lambda pat: (re.search(pat,flat).group(1) if re.search(pat,flat) else '')
    row=lambda lab: re.search(r'\n\s*'+re.escape(lab)+r'\s+(\S+)',body)
    d=dict(cid=cid,name=name,tk=tk,
      theme=f(r'^(.+?) \| figures'),cur=f(r'figures in (millions|billions)? ?(\w+)') ,
      fs=f(r'FINANCIAL STRENGTH: (\d+)'),band=f(r'FINANCIAL STRENGTH: \d+/100 \| (\w+)'),
      rev=(row('Revenue').group(1) if row('Revenue') else ''),
      opm=(row('Operating margin').group(1) if row('Operating margin') else ''),
      cash=(row('Cash + short investments').group(1) if row('Cash + short investments') else ''),
      debt=(row('Total debt incl. leases*').group(1) if row('Total debt incl. leases*') else ''),
      fcf=(row('Free cash flow').group(1) if row('Free cash flow') else ''),
      cagr=f(r'revenue CAGR (-?[\d.]+%)'),cr=f(r'current ratio ([\d.]+x|N/\w)'),
      nde=f(r'net debt/EBITDA (-?[\d.]+x|N/\w)'),fcfm=f(r'FCF margin (-?[\d.]+%)'),
      dil=f(r'diluted-share CAGR (-?[\d.]+%)'),
      price=f(r'PRICE-FUNDAMENTALS BALANCE: ([A-Z\- ]+?) (?:P/E|EV|Bank|Reported|At|Not|[A-Z][a-z])'),
      pe=f(r'P/E (N/M|N/D|[\d,.]+x)'),pfcf=f(r'P/FCF (N/M|N/D|[\d,.]+x)'))
    d['cur']=re.search(r'figures in \w+ (\w+)',flat).group(1) if re.search(r'figures in \w+ (\w+)',flat) else ''
    D[cid]=d
json.dump(D,open(sys.argv[2],'w'),indent=0)
print(len(D))
for d in list(D.values()):
    print(d['cid'],d['tk'],d['fs'],d['cur'],'rev',d['rev'],'cagr',d['cagr'],'opm',d['opm'],'fcfm',d['fcfm'],'cash',d['cash'],'debt',d['debt'],'nde',d['nde'],'dil',d['dil'],'pe',d['pe'],'pfcf',d['pfcf'],'|',d['price'])
