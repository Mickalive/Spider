#!/usr/bin/env python3
from __future__ import annotations
import io,json,os,re,subprocess,urllib.error,urllib.request,zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path.cwd(); OUT=ROOT/'SPIDER_CODEX_ULTIME.md'; PREV=Path('/tmp/SPIDER_CODEX_PREVIOUS.md')
REPO=os.getenv('GITHUB_REPOSITORY','Mickalive/Spider'); TOKEN=os.getenv('GITHUB_TOKEN',''); CURRENT=int(os.getenv('GITHUB_RUN_ID','0') or 0)
START='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_START -->'; END='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_END -->'
SIGNAL=re.compile(r'(error|exception|traceback|fail|blocked|invalid|inconclusive|timeout|permission|denied|rate.?limit|network|provider)',re.I)
NOISE=re.compile(r'(runner image|operating system|github_token permissions|prepare workflow|checkout@|fetching the repository|safe directory|post job cleanup|cleaning up orphan|new branch|new tag|syncing repository)',re.I)

def req(url,binary=False):
    q=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    if TOKEN:q.add_header('Authorization',f'Bearer {TOKEN}')
    try:
        with urllib.request.urlopen(q,timeout=90) as r:return r.read() if binary else json.load(r)
    except urllib.error.HTTPError as e:return b'' if binary else {'_error':f'HTTP {e.code}'}
    except Exception as e:return b'' if binary else {'_error':type(e).__name__}

def all_runs():
    out=[]; p=1
    while True:
        d=req(f'https://api.github.com/repos/{REPO}/actions/runs?per_page=100&page={p}'); b=d.get('workflow_runs',[]) if isinstance(d,dict) else []
        if not b:break
        out+=b
        if len(b)<100:break
        p+=1
        if p>100:raise RuntimeError('Actions pagination overflow')
    return out

def refs_for(rid):
    s=subprocess.run(['git','for-each-ref','--format=%(refname)','refs/remotes/origin','refs/tags'],cwd=ROOT,text=True,stdout=subprocess.PIPE).stdout
    return [x for x in s.splitlines() if f'/{rid}/' in x or x.endswith(f'/{rid}')]

def clean(s):
    s=re.sub(r'^\ufeff?\d{4}-\d\d-\d\dT[^ ]+Z\s+','',s.rstrip()); s=re.sub(r'\x1b\[[0-9;]*m','',s)
    return s.strip()

def sig(s):
    s=clean(s); s=re.sub(r'\b[0-9a-f]{20,40}\b','<SHA>',s,flags=re.I); s=re.sub(r'\b[0-9a-f]{8}-[0-9a-f-]{27,}\b','<UUID>',s,flags=re.I); s=re.sub(r'(?i)(run[_ -]?id[=: ]+)\d+',r'\1<RUN>',s)
    return s

def error_lines(raw):
    try:z=zipfile.ZipFile(io.BytesIO(raw))
    except Exception:return []
    out=[]
    for n in sorted(z.namelist()):
        if n.endswith('/'):continue
        try:ls=z.read(n).decode('utf-8','replace').splitlines()
        except Exception:continue
        for l in ls:
            x=clean(l)
            if x and SIGNAL.search(x) and not NOISE.search(x):out.append(x)
    return out

def read_live(r):
    rid=int(r['id']); refs=refs_for(rid); jobs=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/jobs?per_page=100'); arts=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/artifacts?per_page=100')
    bad=[]
    for j in (jobs.get('jobs',[]) if isinstance(jobs,dict) else []):
        steps=[s.get('name') for s in j.get('steps',[]) if s.get('conclusion') not in (None,'success','skipped')]
        if j.get('conclusion') not in (None,'success','skipped') or steps:bad.append({'job':j.get('name'),'conclusion':j.get('conclusion'),'steps':steps})
    meta={'id':rid,'workflow':r.get('name'),'title':r.get('display_title'),'run_number':r.get('run_number'),'attempt':r.get('run_attempt'),'event':r.get('event'),'conclusion':r.get('conclusion'),'branch':r.get('head_branch'),'head_sha':r.get('head_sha'),'created_at':r.get('created_at'),'snapshot_refs':refs,'non_success':bad,'artifacts':[{'name':a.get('name'),'size':a.get('size_in_bytes'),'expired':a.get('expired')} for a in (arts.get('artifacts',[]) if isinstance(arts,dict) else [])]}
    # Raw logs are redundant for successful runs and for failures with a durable Git snapshot.
    signals=[]
    if r.get('conclusion') not in ('success',None) and not refs:
        signals=error_lines(req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/logs',binary=True))
    return {'meta':meta,'signals':signals}

def parse_previous():
    rec={}; receipt=''
    if not PREV.exists():return rec,receipt
    t=PREV.read_text('utf-8',errors='replace')
    # Old verbose appendix, if one ever landed.
    p=re.compile(r'<!-- RUN_FORENSIC:(\d+):START -->.*?```json\n(.*?)\n```.*?```text\n(.*?)\n```.*?<!-- RUN_FORENSIC:\1:END -->',re.S)
    for m in p.finditer(t):
        try:meta=json.loads(m.group(2)); rid=int(m.group(1)); rec[rid]={'meta':meta,'signals':[x for x in m.group(3).splitlines() if x and not x.startswith('--- log:')]}
        except Exception:pass
    m=re.search(r'<!-- COMPACT_FORENSIC_JSON_START -->\n(.*?)\n<!-- COMPACT_FORENSIC_JSON_END -->',t,re.S)
    if m:
        try:
            d=json.loads(m.group(1))
            for row in d.get('runs',[]):rec[int(row['id'])]={'meta':row,'signals':[]}
            for g in d.get('unique_execution_signals',[]):
                for rid in g.get('run_ids',[]):rec.setdefault(int(rid),{'meta':{'id':int(rid)},'signals':[]})['signals'].append(g.get('example') or g.get('signature') or '')
        except Exception:pass
    m=re.search(r'<!-- FORENSIC_PRUNE_RECEIPT_START -->(.*?)<!-- FORENSIC_PRUNE_RECEIPT_END -->',t,re.S)
    if m:receipt='<!-- FORENSIC_PRUNE_RECEIPT_START -->'+m.group(1)+'<!-- FORENSIC_PRUNE_RECEIPT_END -->'
    return rec,receipt

def normalize_meta(m):
    if 'workflow' in m:return m
    jobs=m.get('jobs',[]); bad=[]
    for j in jobs:
        steps=[s.get('name') for s in j.get('steps',[]) if s.get('conclusion') not in (None,'success','skipped')]
        if j.get('conclusion') not in (None,'success','skipped') or steps:bad.append({'job':j.get('name'),'conclusion':j.get('conclusion'),'steps':steps})
    return {'id':int(m.get('id',0)),'workflow':m.get('name'),'title':m.get('display_title'),'run_number':m.get('run_number'),'attempt':m.get('run_attempt'),'event':m.get('event'),'conclusion':m.get('conclusion'),'branch':m.get('head_branch'),'head_sha':m.get('head_sha'),'created_at':m.get('created_at'),'snapshot_refs':m.get('snapshot_refs',m.get('reachable_snapshot_refs',[])),'non_success':bad,'artifacts':[{'name':a.get('name'),'size':a.get('size_in_bytes'),'expired':a.get('expired')} for a in m.get('artifacts',[])]}

def main():
    rec,receipt=parse_previous(); failures=[]; new=0
    for r in sorted([x for x in all_runs() if int(x.get('id',0))!=CURRENT],key=lambda x:int(x.get('id',0))):
        rid=int(r['id'])
        if rid in rec:continue
        try:rec[rid]=read_live(r);new+=1
        except Exception as e:failures.append({'run_id':rid,'error':f'{type(e).__name__}: {e}'})
    base=OUT.read_text('utf-8'); base=base.split(START,1)[0].rstrip()+'\n' if START in base else base
    canon={clean(x) for x in base.splitlines() if clean(x)}; groups=defaultdict(lambda:{'ids':set(),'example':''}); rows=[]
    for rid in sorted(rec):
        rows.append(normalize_meta(rec[rid]['meta']))
        for line in rec[rid].get('signals',[]):
            x=clean(line)
            if not x or x in canon or NOISE.search(x):continue
            k=sig(x)
            if k in canon:continue
            groups[k]['ids'].add(rid); groups[k]['example']=groups[k]['example'] or x
    unique=[{'signature':k,'example':v['example'],'run_count':len(v['ids']),'run_ids':sorted(v['ids'])} for k,v in sorted(groups.items(),key=lambda kv:(-len(kv[1]['ids']),kv[0]))]
    packed={'schema':'SPIDER compact legacy Actions forensic v3','runs':rows,'unique_execution_signals':unique,'archival_failures':failures,'current_run_excluded':CURRENT}
    sec=START+'\n\n## 7. Compact legacy Actions forensic archive before run deletion\n\nOnly information that can disappear with the Actions objects is retained. Scientific outputs already present in the verbatim corpus are never copied here. Successful runs contribute provenance metadata only. Failed runs with durable Git snapshots contribute provenance + failing job/step names only. Raw log error lines are retained solely for failed runs with no durable snapshot, then deduplicated by normalized signature.\n\n'+f'- legacy_runs_covered: **{len(rows)}**\n- unique_nonredundant_execution_signatures: **{len(unique)}**\n- newly_read_live_runs_this_pass: **{new}**\n- archival_failures: **{len(failures)}**\n\n<!-- COMPACT_FORENSIC_JSON_START -->\n'+json.dumps(packed,ensure_ascii=False,separators=(',',':'))+'\n<!-- COMPACT_FORENSIC_JSON_END -->\n\n'
    if receipt:sec+=receipt+'\n\n'
    sec+=END+'\n'; out=base+sec
    if len(out.encode())>=90*1024*1024:raise RuntimeError('Codex hard limit exceeded')
    OUT.write_text(out,'utf-8'); Path('/tmp/forensic_archive_status.json').write_text(json.dumps({'archived_ids':sorted(rec),'failures':failures,'new':new},indent=2),'utf-8')
    print(json.dumps({'legacy_runs_covered':len(rows),'unique_signatures':len(unique),'new':new,'failures':len(failures),'codex_bytes':len(out.encode())},indent=2))
if __name__=='__main__':main()
