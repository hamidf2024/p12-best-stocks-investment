import re,sys,json
L=open(sys.argv[1]).read().split('\n')
theme=None;out=[]
for i,l in enumerate(L):
    m=re.search(r'(Investment summary|summary) \| (.+?)$',l.strip())
    if m and len(l.strip())<120: theme=m.group(2).strip()
    m=re.match(r'^\s{1,4}(\d+)\.\s+(\S.*?)\s{2,}',l)
    if m and re.search(r'[~<>]\s?\d+%',l):
        p=re.search(r'([~<>]\s?\d+%)',l).group(1)
        tk=L[i+1].split()[0] if L[i+1].strip() else ''
        val=re.search(r'(\d+\.?\d*x)',l); 
        loss=''
        for k in range(i,i+5):
            mm=re.search(r'50% loss:\s*([~<>]?\s?\d+%)',L[k])
            if mm: loss=mm.group(1);break
        gv=re.search(r'\b(HIGH|Cyclical|Quality|Speculative|Moderate|Defensive|Medium|Steady|Volatile|Turnaround|Distressed|Low)\b',l[60:])
        out.append(dict(theme=theme,rank=m.group(1),name=m.group(2),tk=tk,p2x=p,loss=loss,val=val.group(1) if val else '',gv=gv.group(1) if gv else ''))
json.dump(out,open(sys.argv[2],'w'),indent=0)
print(len(out))
seen={}
for o in out: seen.setdefault(o['tk'],o)
print(len(seen))
for o in seen.values(): print(o['theme'][:40],'|',o['tk'],'|',o['name'][:28],'|',o['p2x'],o['loss'],o['val'],o['gv'])
