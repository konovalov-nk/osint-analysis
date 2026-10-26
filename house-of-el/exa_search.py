import os, json, urllib.request, urllib.error, re, sys
key=os.environ.get('EXA_API_KEY','').strip()
if not key:
    try:
        for line in open(os.path.expanduser('~/.api-keys')):
            m=re.match(r'\s*(?:export\s+)?EXA_API_KEY\s*=\s*["\']?([^"\'\s]+)',line)
            if m: key=m.group(1); break
    except Exception as e: pass
if not key:
    print('NO KEY'); sys.exit(1)
print('key loaded, length',len(key))
queries=[
 ('general','"House of El" El PhD computer science geopolitical analyst'),
 ('footprint','"House of El: AI" OR "realhouseofel" OR "houseofel.net"'),
 ('book','"Six Eyes of Critical Thinking" Awake El'),
 ('critique','"House of El" AI avatar fake Reddit'),
 ('old','"House of El" El before June 2025'),
 ('proof','"You\'re Right - I\'m AI generated" "House of El"'),
 ('thesis','"El" "House of El" PhD thesis Denmark computer science'),
]
out={}
for name,q in queries:
    payload={'query':q,'type':'neural','numResults':5,'contents':{'text':{'maxCharacters':700},'highlights':{'numSentences':2}}}
    if name=='old': payload['endPublishedDate']='2025-06-01'
    req=urllib.request.Request('https://api.exa.ai/search',data=json.dumps(payload).encode(),headers={'x-api-key':key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=60) as r:
            d=json.load(r)
        out[name]=d
        print('\n===',name,q)
        for x in d.get('results',[]):
            print('-',x.get('title'))
            print('  ',x.get('url'))
            txt=(x.get('text') or '').replace('\n',' ')[:350]
            print('  ',txt)
    except urllib.error.HTTPError as e:
        print('\n===',name,'HTTP',e.code,e.read().decode()[:300])
    except Exception as e:
        print('\n===',name,'ERR',e)
json.dump(out,open('exa_results.json','w'),indent=1)
print('\nsaved exa_results.json')
