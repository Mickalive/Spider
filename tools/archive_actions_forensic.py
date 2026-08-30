#!/usr/bin/env python3
from __future__ import annotations
import io, json, os, re, subprocess, urllib.error, urllib.request, zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path.cwd(); OUT=ROOT/'SPIDER_CODEX_ULTIME.md'; PREV=Path('/tmp/SPIDER_CODEX_PREVIOUS.md')
REPO=os.getenv('GITHUB_REPOSITORY','Mickalive/Spider'); TOKEN=os.getenv('GITHUB_TOKEN',''); CURRENT=int(os.getenv('GITHUB_RUN_ID','0') or 0)
START='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_START -->'; END='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_END -->'
SIGNAL=re.compile(r'(error|exception|traceback|warn|fail|blocked|falsif|inconclusive|invalid|verdict|audit|metric|score|accuracy|speedup|median|mean|confidence|effect|claim|hypothesis|floor|ceiling|accept|reject|prereg|measurement|dataset|trajectory|transition|novel|causal|reuse|inherit|delta|freshness|witness|knowledge|timeout|permission|denied|rate.?limit|network|artifact|persist|receipt)',re.I)
FAILISH=re.compile(r'(error|exception|traceback|fail|timeout|permission|denied|rate.?limit|network|provider|checkout|persist|git)',re.I)
NOISE=re.compile(r'(current runner version|runner image|operating system|github_token permissions|secret source|prepare workflow directory|get action download info|node\.js 20 is deprecated|temporarily overriding home|safe directory|automatic garbage collection|setting up auth|fetching the repository|determining the checkout info|checking out the ref|post job cleanup|cleaning up orphan processes|\* \[new branch\]|\* \[new tag\]|from https://github\.com/|git config --global|git submodule foreach|actions/checkout@|syncing repository)',re.I)

def req(url,binary=False):
    q=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    if TOKEN:q.add_header('Authorization',f'Bearer {TOKEN}')
    try:
        with urllib.request.urlopen(q,timeout=90) as r:return r.read() if binary else json.load(r)
    except urllib.error.HTTPError as e:return b'' if binary else {'_error':f'HTTP {e.code}'}
    except Exception as e:return b'' if binary else {'_error':type(e).__name__}

def runs():
    out=[]; page=1
    while True:
        d=req(f'https://api.github.com/repos/{REPO}/actions/runs?per_page=100&page={page}')
        b=d.get('workflow_runs',[]) if isinstance(d,dict) else []
        if not b:break
        out+=b
        if len(b)<100:break
        page+=1
        if page>100:raise RuntimeError('refusing silent Actions truncation')
    return out

def refs_for(rid):
    p=subprocess.run(['git','for-each-ref','--format=%(refname)','refs/remotes/origin','refs/tags'],cwd=ROOT,text=True,stdout=subprocess.PIPE).stdout
    needle=f'/{rid}/'
    return [x for x in p.splitlines() if needle in x or x.endswith(f'/{rid}')]

def clean_line(s):
    s=re.sub(r'^\ufeff?\d{4}-\d\d-\d\dT[^ ]+Z\s+','',s.rstrip())
    s=re.sub(r'\x1b\[[0-9;]*m','',s)
    return s.strip()

def signature(s):
    s=clean_line(s)
    if FAILISH.search(s):
        s=re.sub(r'\b[0-9a-f]{20,40}\b','<SHA>',s,flags=re.I)
        s=re.sub(r'\b[0-9a-f]{8}-[0-9a-f-]{27,}\b','<UUID>',s,flags=re.I)
        s=re.sub(r'(?i)(run[_ -]?id[=: ]+)\d+',r'\1<RUN>',s)
        s=re.sub(r'(?<=/)\d{8,}(?=/|\b)','<RUN>',s)
    return s

def signal_lines(raw):
    try:z=zipfile.ZipFile(io.BytesIO(raw))
    except Exception:return []
    out=[]
    for name in sorted(z.namelist()):
        if name.endswith('/'):continue
        try:lines=z.read(name).decode('utf-8','replace').splitlines()
        except Exception:continue
        for line in lines:
            s=clean_line(line)
            if not s or NOISE.search(s) or not SIGNAL.search(s):continue
            out.append(s)
    return out

def live_record(r):
    rid=int(r['id']); jobs=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/jobs?per_page=100'); arts=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/artifacts?per_page=100'); raw=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/logs',binary=True)
    jrows=[]
    for j in (jobs.get('jobs',[]) if isinstance(jobs,dict) else []):
        steps=[{'name':s.get('name'),'conclusion':s.get('conclusion')} for s in j.get('steps',[]) if s.get('conclusion') not in (None,'success','skipped')]
        jrows.append({'name':j.get('name'),'conclusion':j.get('conclusion'),'non_success_steps':steps})
    arows=[{'name':a.get('name'),'size_in_bytes':a.get('size_in_bytes'),'expired':a.get('expired')} for a in (arts.get('artifacts',[]) if isinstance(arts,dict) else [])]
    meta={k:r.get(k) for k in ('id','name','display_title','run_number','run_attempt','event','conclusion','head_branch','head_sha','created_at')}
    meta['snapshot_refs']=refs_for(rid);meta['jobs']=jrows;meta['artifacts']=arows
    return {'meta':meta,'signals':signal_lines(raw)}

def parse_prior():
    records={}; receipt=''
    if not PREV.exists():return records,receipt
    t=PREV.read_text('utf-8',errors='replace')
    pat=re.compile(r'<!-- RUN_FORENSIC:(\d+):START -->.*?```json\n(.*?)\n```.*?```text\n(.*?)\n```.*?<!-- RUN_FORENSIC:\1:END -->',re.S)
    for m in pat.finditer(t):
        try:meta=json.loads(m.group(2))
        except Exception:continue
        rid=int(m.group(1)); records[rid]={'meta':meta,'signals':[x for x in m.group(3).splitlines() if x and not x.startswith('--- log:')]}
    # Already-compact previous appendix.
    m=re.search(r'<!-- COMPACT_FORENSIC_JSON_START -->\n(.*?)\n<!-- COMPACT_FORENSIC_JSON_END -->',t,re.S)
    if m:
        try:
            packed=json.loads(m.group(1))
            for row in packed.get('runs',[]):records[int(row['id'])]={'meta':row,'signals':[]}
        except Exception:pass
    m=re.search(r'<!-- FORENSIC_PRUNE_RECEIPT_START -->(.*?)<!-- FORENSIC_PRUNE_RECEIPT_END -->',t,re.S)
    if m:receipt='<!-- FORENSIC_PRUNE_RECEIPT_START -->'+m.group(1)+'<!-- FORENSIC_PRUNE_RECEIPT_END -->'
    return records,receipt

def compact_meta(m):
    jobs=m.get('jobs',[]); bad=[]
    for j in jobs:
        if j.get('conclusion') not in (None,'success','skipped') or j.get('non_success_steps'):
            bad.append({'job':j.get('name'),'conclusion':j.get('conclusion'),'steps':[s.get('name') for s in j.get('non_success_steps',[]) if s.get('name')]})
        elif 'steps' in j:
            ns=[s.get('name') for s in j.get('steps',[]) if s.get('conclusion') not in (None,'success','skipped')]
            if ns:bad.append({'job':j.get('name'),'conclusion':j.get('conclusion'),'steps':ns})
    arts=m.get('artifacts',[])
    return {'id':int(m.get('id',0)),'workflow':m.get('name'),'title':m.get('display_title'),'run_number':m.get('run_number'),'attempt':m.get('run_attempt'),'event':m.get('event'),'conclusion':m.get('conclusion'),'branch':m.get('head_branch'),'head_sha':m.get('head_sha'),'created_at':m.get('created_at'),'snapshot_refs':m.get('snapshot_refs',m.get('reachable_snapshot_refs',[])),'non_success':bad,'artifacts':[{'name':a.get('name'),'size':a.get('size_in_bytes'),'expired':a.get('expired')} for a in arts]}

def main():
    previous,receipt=parse_prior(); current=[r for r in runs() if int(r.get('id',0))!=CURRENT]; failures=[]; new=0
    for r in sorted(current,key=lambda x:int(x.get('id',0))):
        rid=int(r['id'])
        if rid in previous:continue
        try:previous[rid]=live_record(r);new+=1
        except Exception as e:failures.append({'run_id':rid,'error':f'{type(e).__name__}: {e}'})
    base=OUT.read_text('utf-8')
    if START in base:base=base.split(START,1)[0].rstrip()+'\n'
    canonical={clean_line(x) for x in base.splitlines() if clean_line(x)}
    rows=[]; groups=defaultdict(lambda:{'runs':set(),'example':''})
    for rid in sorted(previous):
        rows.append(compact_meta(previous[rid]['meta']))
        for line in previous[rid].get('signals',[]):
            c=clean_line(line)
            if not c or c in canonical or NOISE.search(c):continue
            key=signature(c)
            if not key or key in canonical:continue
            groups[key]['runs'].add(rid)
            if not groups[key]['example']:groups[key]['example']=c
    # Only preserve execution signal absent from the canonical scientific corpus; duplicates collapse to one signature.
    unique=[]
    for key,v in sorted(groups.items(),key=lambda kv:(-len(kv[1]['runs']),kv[0])):
        ids=sorted(v['runs']); unique.append({'signature':key,'example':v['example'],'run_count':len(ids),'run_ids':ids})
    packed={'schema':'SPIDER compact legacy Actions forensic v2','runs':rows,'unique_execution_signals':unique,'archival_failures':failures,'current_run_excluded':CURRENT}
    section=[START,'\n\n## 7. Compact legacy Actions forensic archive before run deletion\n\n',
      'This appendix contains only information that can disappear with deletion of legacy GitHub Actions runs and is not already carried by the verbatim scientific corpus. Every run keeps a compact provenance row (workflow, conclusion, branch/head SHA, timestamp, persisted snapshot refs, non-success jobs/steps and artifact names). Execution log lines already present in results/reports are omitted; repeated diagnostics are normalized and stored once with the complete set of run IDs that exhibited them. Hosted-runner setup, checkout/fetch chatter and other execution boilerplate are excluded.\n\n',
      f'- legacy_runs_covered: **{len(rows)}**\n- unique_nonredundant_execution_signatures: **{len(unique)}**\n- newly_read_live_runs_this_pass: **{new}**\n- archival_failures: **{len(failures)}**\n\n',
      '<!-- COMPACT_FORENSIC_JSON_START -->\n',json.dumps(packed,ensure_ascii=False,separators=(',',':')),'\n<!-- COMPACT_FORENSIC_JSON_END -->\n\n']
    if receipt:section+=[receipt,'\n\n']
    section+=[END,'\n']
    out=base+''.join(section)
    if len(out.encode('utf-8'))>=90*1024*1024:raise RuntimeError('compact forensic appendix exceeds Codex hard limit; refusing deletion')
    OUT.write_text(out,'utf-8')
    Path('/tmp/forensic_archive_status.json').write_text(json.dumps({'archived_ids':sorted(previous),'failures':failures,'new':new},indent=2),'utf-8')
    print(json.dumps({'legacy_runs_covered':len(rows),'unique_signatures':len(unique),'new':new,'failures':len(failures),'codex_bytes':len(out.encode('utf-8'))},indent=2))
if __name__=='__main__':main()
