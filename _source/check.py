import os, re, sys
from html.parser import HTMLParser
D = sys.argv[1]
files = {f for f in os.listdir(D)}
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.ids=set()
    def handle_starttag(s, t, a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        for k in ('href','src'):
            if k in a and a[k]: s.links.append(a[k])
pages={}
for f in files:
    if f.endswith('.html'):
        p=P(); p.feed(open(os.path.join(D,f),encoding='utf-8').read()); pages[f]=p
bad=[]
for f,p in pages.items():
    for l in p.links:
        if l.startswith(('http','mailto:')): continue
        path,_,frag=l.partition('#')
        path=path.lstrip('/') or ('index.html' if l.startswith('/') else f)
        if path not in files: bad.append((f,l,'missing file')); continue
        if frag and path in pages and frag not in pages[path].ids: bad.append((f,l,'missing anchor'))
print('broken:',len(bad))
for b in sorted(set(bad)): print(b)
# French typography: space before ? ! in fr pages text
fr=[f for f in pages if open(os.path.join(D,f),encoding='utf-8').read().find('lang="fr-CA"')>0]
for f in fr:
    t=open(os.path.join(D,f),encoding='utf-8').read()
    t=re.sub(r'<[^>]+>',' ',t)
    for m in re.finditer(r'\w ([?!;])',t): print('FR spacing',f,repr(t[m.start()-15:m.end()]))
    for m in re.finditer(r'\w:(?=\s)',t): print('FR colon',f,repr(t[m.start()-15:m.end()+5]))
