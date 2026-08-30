#!/usr/bin/env python3
from __future__ import annotations
import io,json,os,re,subprocess,urllib.error,urllib.request,zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path.cwd(); OUT=ROOT/'SPIDER_CODEX_ULTIME.md'; PREV=Path('/tmp/SPIDER_CODEX_PREVIOUS.md')
REPO=os.getenv('GITHUB_REPOSITORY','Mickalive/Spider'); TOKEN=os.getenv('GITHUB_TOKEN',''); CURRENT=int(os.getenv('GITHUB_RUN_ID','0') or 0)
START='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_START -->'; END='<!-- SPIDER_LEGACY_ACTIONS_FORENSIC_END -->'
SIGNAL=re.compile(r'(error|exception|traceback|fail|blocked|invalid|inconclusive|falsif|verdict|metric|score|accuracy|speedup|median|mean|confidence|effect|claim|hypothesis|measurement|dataset|trajectory|transition|novel|causal|reuse|inherit|delta|freshness|witness|timeout|permission|denied|rate.?limit|network|provider)',re.I)
NOISE=re.compile(r'(runner image|operating system|github_token permissions|prepare workflow|checkout@|fetching the repository|safe directory|post job cleanup|cleaning up orphan|new branch|new tag|syncing repository)',re.I)
SUBWF=re.compile(r'(graph|physics|intel|runtime|product|frontier|critical cto council|research lane|engineering loop|failure review|beta)',re.I)

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

def run_memory_ids():
    ids=set(); s=subprocess.run(['git','ls-tree','-r','origin/main','evidence/run-memory/runs'],cwd=ROOT,text=True,stdout=subprocess.PIPE).stdout
    for line in s.splitlines():
        try:p=line.split('\t',1)[1]
        except Exception:continue
        m=re.search(r'/(\d+)\.json$',p)
        if m:ids.add(int(m.group(1)))
    return ids

def all_refs():
    return subprocess.run(['git','for-each-ref','--format=%(refname)','refs/remotes/origin','refs/tags'],cwd=ROOT,text=True,stdout=subprocess.PIPE).stdout.splitlines()

def refs_for(rid,refs):
    needle=f'/{rid}/'; end=f'/{rid}'
    return [x for x in refs if needle in x or x.endswith(end)]

def clean(s):
    s=re.sub(r'^\ufeff?\d{4}-\d\d-\d\dT[^ ]+Z\s+','',s.rstrip()); s=re.sub(r'\x1b\[[0-9;]*m','',s)
    return s.strip()

def sig(s):
    s=clean(s); s=re.sub(r'\b[0-9a-f]{20,40}\b','<SHA>',s,flags=re.I); s=re.sub(r'\b[0-9a-f]{8}-[0-9a-f-]{27,}\b','<UUID>',s,flags=re.I); s=re.sub(r'(?i)(run[_ -]?id[=: ]+)\d+',r'\1<RUN>',s)
    return s

def signal_lines(raw):
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

def non_success_steps(rid,conclusion):
    if conclusion in (None,'success','skipped'):return []
    jobs=req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/jobs?per_page=100'); bad=[]
    for j in (jobs.get('jobs',[]) if isinstance(jobs,dict) else []):
        steps=[s.get('name') for s in j.get('steps',[]) if s.get('conclusion') not in (None,'success','skipped')]
        if j.get('conclusion') not in (None,'success','skipped') or steps:bad.append({'job':j.get('name'),'conclusion':j.get('conclusion'),'steps':steps})
    return bad

def live_record(r,mem_ids,refs):
    rid=int(r['id']); snap=refs_for(rid,refs); has_mem=rid in mem_ids; conclusion=r.get('conclusion')
    meta={'id':rid,'conclusion':conclusion,'head_sha':r.get('head_sha'),'snapshot_refs':snap,'run_memory':has_mem,'non_success':non_success_steps(rid,conclusion)}
    signals=[]
    # Only a substantive run with neither durable run-memory nor Git snapshot can lose unique scientific information on deletion.
    if not has_mem and not snap and SUBWF.search(str(r.get('name') or '')):
        signals=signal_lines(req(f'https://api.github.com/repos/{REPO}/actions/runs/{rid}/logs',binary=True))
    return {'meta':meta,'signals':signals}

def parse_previous():
    rec={}; receipt=''
    if not PREV.exists():return rec,receipt
    t=PREV.read_text('utf-8',errors='replace')
    m=re.search(r'<!-- COMPACT_FORENSIC_JSON_START -->\n(.*?)\n<!-- COMPACT_FORENSIC_JSON_END -->',t,re.S)
    if m:
        try:
            d=json.loads(m.group(1))
            for row in d.get('runs',[]):rec[int(row['id'])]={'meta':row,'signals':[]}
            for key in ('unique_uncovered_execution_signals','unique_execution_signals'):
                for g in d.get(key,[]):
                    for rid in g.get('run_ids',[]):rec.setdefault(int(rid),{'meta':{'id':int(rid)},'signals':[]})['signals'].append(g.get('example') or g.get('signature') or '')
        except Exception:pass
    m=re.search(r'<!-- FORENSIC_PRUNE_RECEIPT_START -->(.*?)<!-- FORENSIC_PRUNE_RECEIPT_END -->',t,re.S)
    if m:receipt='<!-- FORENSIC_PRUNE_RECEIPT_START -->'+m.group(1)+'<!-- FORENSIC_PRUNE_RECEIPT_END -->'
    return rec,receipt

def main():
    mem_ids=run_memory_ids(); refs=all_refs(); rec,receipt=parse_previous(); failures=[]; new=0
    current=[x for x in all_runs() if int(x.get('id',0))!=CURRENT]
    for r in sorted(current,key=lambda x:int(x.get('id',0))):
        rid=int(r['id'])
        if rid in rec:continue
        try:rec[rid]=live_record(r,mem_ids,refs);new+=1
        except Exception as e:failures.append({'run_id':rid,'error':f'{type(e).__name__}: {e}'})
    base=OUT.read_text('utf-8'); base=base.split(START,1)[0].rstrip()+'\n' if START in base else base
    canon={clean(x) for x in base.splitlines() if clean(x)}; groups=defaultdict(lambda:{'ids':set(),'example':''}); rows=[]
    for rid in sorted(rec):
        m=rec[rid]['meta']; rows.append({'id':rid,'conclusion':m.get('conclusion'),'head_sha':m.get('head_sha'),'snapshot_refs':m.get('snapshot_refs',[]),'run_memory':bool(m.get('run_memory')),'non_success':m.get('non_success',[])})
        for line in rec[rid].get('signals',[]):
            x=clean(line)
            if not x or x in canon or NOISE.search(x):continue
            k=sig(x)
            if not k or k in canon:continue
            groups[k]['ids'].add(rid); groups[k]['example']=groups[k]['example'] or x
    unique=[{'signature':k,'example':v['example'],'run_count':len(v['ids']),'run_ids':sorted(v['ids'])} for k,v in sorted(groups.items(),key=lambda kv:(-len(kv[1]['ids']),kv[0]))]
    uncovered=sum(1 for r in rows if not r['run_memory'] and not r['snapshot_refs'])
    packed={'schema':'SPIDER compact deletion ledger v5','runs':rows,'unique_uncovered_execution_signals':unique,'uncovered_runs_without_memory_or_snapshot':uncovered,'archival_failures':failures,'current_run_excluded':CURRENT}
    sec=START+'\n\n## 7. Compact legacy Actions deletion ledger\n\nPurpose: make every pre-2.0 Actions run deletable without duplicating the scientific corpus. Section 3 preserves workflow-family inventory; section 4 preserves substantive Git artifacts by SHA; section 5 preserves substantive run-memory. This ledger stores only the minimal run→evidence bridge needed after deletion: run ID, conclusion, immutable head SHA, durable snapshot refs, whether a run-memory exists, and failing job/step names. Raw log signal is read only for substantive runs with neither run-memory nor Git snapshot, then normalized and deduplicated across runs.\n\n'+f'- legacy_runs_covered: **{len(rows)}**\n- runs_without_memory_or_snapshot: **{uncovered}**\n- unique_nonredundant_uncovered_signatures: **{len(unique)}**\n- archival_failures: **{len(failures)}**\n\n<!-- COMPACT_FORENSIC_JSON_START -->\n'+json.dumps(packed,ensure_ascii=False,separators=(',',':'))+'\n<!-- COMPACT_FORENSIC_JSON_END -->\n\n'
    if receipt:sec+=receipt+'\n\n'
    sec+=END+'\n'; out=base+sec
    if len(out.encode())>=90*1024*1024:raise RuntimeError('Codex hard limit exceeded')
    OUT.write_text(out,'utf-8'); Path('/tmp/forensic_archive_status.json').write_text(json.dumps({'archived_ids':sorted(rec),'failures':failures,'new':new},indent=2),'utf-8')
    print(json.dumps({'legacy_runs_covered':len(rows),'uncovered':uncovered,'unique_signatures':len(unique),'new':new,'failures':len(failures),'codex_bytes':len(out.encode())},indent=2))
if __name__=='__main__':main()
