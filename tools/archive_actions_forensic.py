#!/usr/bin/env python3
from __future__ import annotations
import io, json, os, re, subprocess, urllib.error, urllib.request, zipfile
from pathlib import Path

ROOT=Path.cwd(); OUT=ROOT/'SPIDER_CODEX_ULTIME.md'; PREV=Path('/tmp/SPIDER_CODEX_PREVIOUS.md')
REPO=os.getenv('GITHUB_REPOSITORY','Mickalive/Spider'); TOKEN=os.getenv('GITHUB_TOKEN',''); CURRENT=int(os.getenv('GITHUB_RUN_ID','0') or 0)
START='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_START -->'; END='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_END -->'
RS='<!-- RUN_FORENSIC:{rid}:START -->'; RE='<!-- RUN_FORENSIC:{rid}:END -->'
SIGNAL=re.compile(r'(error|exception|traceback|warn|fail|blocked|pass|falsif|inconclusive|invalid|result|verdict|audit|metric|score|accuracy|speedup|median|mean|confidence|\bp\s*[=<>]|effect|claim|evidence|hypothesis|floor|ceiling|accept|reject|prereg|measurement|dataset|trajectory|transition|novel|causal|reuse|inherit|delta|freshness|witness|knowledge|physics|graph|intel|runtime|product|frontier|timeout|permission|denied|artifact|persist|receipt)',re.I)
NOISE=re.compile(r'(current runner version|runner image|operating system|github_token permissions|secret source|prepare workflow directory|get action download info|node\.js 20 is deprecated|temporarily overriding home|safe directory|disabling automatic garbage collection|setting up auth|fetching the repository|determining the checkout info|checking out the ref|post job cleanup|cleaning up orphan processes|\* \[new branch\]|\* \[new tag\]|from https://github\.com/|git config --global|git submodule foreach|actions/checkout@|syncing repository)',re.I)

def req(url, binary=False):
    q=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    if TOKEN:q.add_header('Authorization',f'Bearer {TOKEN}')
    try:
        with urllib.request.urlopen(q,timeout=90) as r:return r.read() if binary else json.load(r)
    except urllib.error.HTTPError as e:
        return {'_error':f'HTTP {e.code}'} if not binary else b''
    except Exception as e:
        return {'_error':type(e).__name__} if not binary else b''

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

def prior_records():
    if not PREV.exists():return {},''
    t=PREV.read_text('utf-8',errors='replace')
    records={}
    pat=re.compile(r'<!-- RUN_FORENSIC:(\d+):START -->(.*?)<!-- RUN_FORENSIC:\1:END -->',re.S)
    for m in pat.finditer(t):records[int(m.group(1))]=m.group(0)
    receipt=''
    m=re.search(r'<!-- FORENSIC_PRUNE_RECEIPT_START -->(.*?)<!-- FORENSIC_PRUNE_RECEIPT_END -->',t,re.S)
    if m:receipt='<!-- FORENSIC_PRUNE_RECEIPT_START -->'+m.group(1)+'<!-- FORENSIC_PRUNE_RECEIPT_END -->'
    return records,receipt

def strip_ts(s):
    return re.sub(r'^\ufeff?\d{4}-\d\d-\d\dT[^ ]+Z\s+','',s.rstrip())

def signal_excerpt(raw):
    try:z=zipfile.ZipFile(io.BytesIO(raw))
    except Exception:return 'Run log ZIP unavailable or unreadable.'
    kept=[]; seen=set()
    for name in sorted(z.namelist()):
        if name.endswith('/'):continue
        try:lines=z.read(name).decode('utf-8','replace').splitlines()
        except Exception:continue
        hit=set()
        for i,line in enumerate(lines):
            s=strip_ts(line)
            if NOISE.search(s):continue
            if SIGNAL.search(s):
                hit.update(range(max(0,i-1),min(len(lines),i+2)))
        if not hit:continue
        kept.append(f'--- log: {name} ---')
        for i in sorted(hit):
            s=strip_ts(lines[i])
            if NOISE.search(s):continue
            key=(name,s)
            if key in seen:continue
            seen.add(key); kept.append(s)
    return '\n'.join(kept) if kept else 'No non-boilerplate scientific/diagnostic signal lines found; job/step metadata and Git snapshots remain recorded.'

def record(r):
    rid=int(r['id']); jobs=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/jobs?per_page=100')
    arts=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/artifacts?per_page=100')
    raw=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/logs',binary=True)
    jrows=[]
    for j in (jobs.get('jobs',[]) if isinstance(jobs,dict) else []):
        steps=[{'number':s.get('number'),'name':s.get('name'),'status':s.get('status'),'conclusion':s.get('conclusion')} for s in j.get('steps',[])]
        jrows.append({'id':j.get('id'),'name':j.get('name'),'status':j.get('status'),'conclusion':j.get('conclusion'),'started_at':j.get('started_at'),'completed_at':j.get('completed_at'),'steps':steps})
    arows=[{'id':a.get('id'),'name':a.get('name'),'size_in_bytes':a.get('size_in_bytes'),'expired':a.get('expired'),'created_at':a.get('created_at')} for a in (arts.get('artifacts',[]) if isinstance(arts,dict) else [])]
    meta={k:r.get(k) for k in ('id','name','display_title','run_number','run_attempt','event','status','conclusion','head_branch','head_sha','created_at','updated_at','run_started_at','html_url')}
    meta['reachable_snapshot_refs']=refs_for(rid); meta['jobs']=jrows; meta['artifacts']=arows
    ex=signal_excerpt(raw)
    return f"{RS.format(rid=rid)}\n### Legacy run `{rid}` — {str(r.get('name') or '').replace(chr(10),' ')}\n\n```json\n{json.dumps(meta,ensure_ascii=False,indent=2)}\n```\n\n#### Preserved scientific/diagnostic execution signal\n\n```text\n{ex}\n```\n{RE.format(rid=rid)}"

def main():
    old,receipt=prior_records(); current=[r for r in runs() if int(r.get('id',0))!=CURRENT]
    new=0; failures=[]
    for r in sorted(current,key=lambda x:int(x.get('id',0))):
        rid=int(r['id'])
        if rid in old:continue
        try:old[rid]=record(r); new+=1
        except Exception as e:
            failures.append({'run_id':rid,'error':f'{type(e).__name__}: {e}'})
    base=OUT.read_text('utf-8')
    if START in base:base=base.split(START,1)[0].rstrip()+'\n'
    section=[START,'\n\n## 7. Legacy GitHub Actions forensic archive before run deletion\n\n',
      'Purpose: preserve the information value of legacy Actions runs inside this same canonical Codex before deleting the GitHub run objects. Generated Git result/report/audit artifacts are already preserved verbatim in section 4. This appendix therefore retains the complementary execution evidence that can disappear with a run: run metadata, immutable head SHA, reachable snapshot refs, job/step conclusions, artifact inventory, and non-boilerplate scientific/error/diagnostic log signal. Routine hosted-runner setup, checkout chatter and repeated branch-fetch noise are deliberately excluded because they carry no SPIDER scientific or forensic information.\n\n',
      f'- forensic_records_archived: **{len(old)}**\n- newly_archived_this_pass: **{new}**\n- archival_failures: **{len(failures)}**\n- current_run_intentionally_not_archived: **{CURRENT}**\n\n']
    if failures:section+=['Archival failures (these runs MUST NOT be deleted):\n\n```json\n',json.dumps(failures,indent=2),'\n```\n\n']
    for rid in sorted(old):section+=[old[rid],'\n\n']
    if receipt:section+=[receipt,'\n\n']
    section+=[END,'\n']
    out=base+''.join(section)
    if len(out.encode('utf-8'))>=90*1024*1024:raise RuntimeError('forensic appendix would exceed Codex hard limit; refusing any deletion')
    OUT.write_text(out,'utf-8')
    Path('/tmp/forensic_archive_status.json').write_text(json.dumps({'archived_ids':sorted(old),'failures':failures,'new':new},indent=2),'utf-8')
    print(json.dumps({'forensic_records_archived':len(old),'new':new,'failures':len(failures),'codex_bytes':len(out.encode('utf-8'))},indent=2))
if __name__=='__main__':main()
