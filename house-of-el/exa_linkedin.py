import os,json,urllib.request,urllib.error,re
key=os.environ.get('EXA_API_KEY','').strip()
if not key:
    for line in open(os.path.expanduser('~/.api-keys')):
        m=re.match(r'\s*(?:export\s+)?EXA_API_KEY\s*=\s*["\']?([^"\'\s]+)',line)
        if m: key=m.group(1); break
def post(path,payload):
    req=urllib.request.Request('https://api.exa.ai'+path,data=json.dumps(payload).encode(),headers={'x-api-key':key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=90) as r: return json.load(r)
# contents
try:
    d=post('/contents',{'urls':['https://www.linkedin.com/in/elena-m-5341b1a3'],'text':{'maxCharacters':3000}})
    print('=== CONTENTS')
    for x in d.get('results',[]):
        print(x.get('url'),x.get('title'))
        print((x.get('text') or '')[:3000])
    for x in d.get('statuses',[]): print('STATUS',x)
except Exception as e: print('CONTENTS ERR',e)
# searches
for q in ['"Elena M." "House of El" LinkedIn','"Elena M" PhD Denmark London data science LinkedIn']:
    try:
        d=post('/search',{'query':q,'type':'neural','numResults':5,'contents':{'text':{'maxCharacters':800},'highlights':{'numSentences':2}}})
        print('\n=== SEARCH',q)
        for x in d.get('results',[]):
            print('-',x.get('title'),'|',x.get('url'))
            for h in (x.get('highlights') or [])[:2]: print('  >',h.replace('\n',' ')[:300])
            print('  ',(x.get('text') or '').replace('\n',' ')[:300])
    except Exception as e: print('SEARCH ERR',q,e)
