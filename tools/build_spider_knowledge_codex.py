#!/usr/bin/env python3
from __future__ import annotations
import datetime as dt, hashlib, json, os, re, subprocess, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path.cwd(); OUT=ROOT/'SPIDER_CODEX_ULTIME.md'
REPO=os.getenv('GITHUB_REPOSITORY','Mickalive/Spider'); TOKEN=os.getenv('GITHUB_TOKEN','')
MAX=90*1024*1024; EXT={'.md','.json','.txt','.csv','.tsv','.yaml','.yml','.log'}
RESEARCH_LANES={'graph','physics','intel','runtime','product','frontier'}; LANES=RESEARCH_LANES|{'audit','cto'}
ROLE_ORDER={'charter_question':0,'prereg_protocol':1,'result_measurement':2,'report_verdict':3,'audit_gate':4,'state_provenance':5,'context_input':6}
LANE_ORDER={'graph':0,'physics':1,'intel':2,'runtime':3,'product':4,'frontier':5,'audit':6,'cto':7,'cross-lane':8,'unknown':9}
K=re.compile(r'(charter|question|mission|prereg|registration|protocol|method|design|plan|freeze|seal|baseline|power|result|report|audit|gate|verdict|metric|benchmark|measurement|finding|experiment|hypothesis|evidence|evaluation|falsification|claim|ledger|outcome|score|test|manifest|state|decision|limitation|provenance|receipt|handoff|taxonomy|registry)',re.I)
NOISE=re.compile(r'(watchdog|supervisor|control plane|run evidence curator|repo hygiene|publisher|evidence handoff|model router|model health|reaper|purge|maintenance|archive)',re.I)
SUBWF=re.compile(r'(graph|physics|intel|runtime|product|frontier|critical cto council|research lane|engineering loop|failure review|beta)',re.I)
VERDICT=re.compile(r'\b(PASS|FAIL(?:ED)?|FALSIFIED|VALIDATED_USEFUL|REPRODUCED_USEFUL|MEASUREMENT_INVALID|VALID_INCONCLUSIVE|INCONCLUSIVE|BLOCKED(?:_UNRUN)?|FLOOR_VOID|REJECTED|PROMISING|PRODUCT_CANDIDATE|WATCH|DORMANT|UNKNOWN|ACCEPTED|REVISE|SITE_BOUND|SCALING_HOLDS)\b',re.I)
ID_PATTERNS=[re.compile(x,re.I) for x in [r'\bWP[-_ ]?\d+[A-Z]?(?:[-_ ]?R\d+)?\b',r'\bG[-_]?H\d+\b',r'\bPB[-_]?\d+\b',r'\bPH[-_]?\d+\b',r'\bPW[-_][A-Z0-9-]+\b',r'\bR\d+(?:[-_]\d+){1,2}\b',r'\bCYCLE[_-]\d{8,}\b']]
METRIC_KEY=re.compile(r'(metric|score|accuracy|acc|mean|median|rate|ratio|speedup|latency|token|action|success|failure|count|total|sample|\bn\b|p_value|pvalue|confidence|ci|effect|delta|coverage|floor|ceiling|verdict|status|conclusion)',re.I)

def sh(*a,check=True):
    p=subprocess.run(a,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and p.returncode:raise RuntimeError(f"{' '.join(a)}\n{p.stderr}")
    return p.stdout

def api(url):
    q=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    if TOKEN:q.add_header('Authorization',f'Bearer {TOKEN}')
    with urllib.request.urlopen(q,timeout=60) as r:return json.load(r)

def action_runs():
    out=[]; page=1
    while True:
        b=api(f'https://api.github.com/repos/{REPO}/actions/runs?per_page=100&page={page}').get('workflow_runs',[])
        if not b:break
        out+=b
        if len(b)<100:break
        page+=1
        if page>100:raise RuntimeError('refusing silent Actions truncation')
    return out

def refs():
    rows=[]
    for line in sh('git','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin','refs/tags').splitlines():
        if line.endswith('/HEAD') or ' ' not in line:continue
        r,o=line.split(' ',1); rows.append((r,o))
    return rows

def lane_for_path(p):
    q=p.replace('\\','/').lower(); parts=q.split('/')
    if parts and parts[0] in RESEARCH_LANES:return parts[0]
    if len(parts)>=2 and parts[0] in {'reports','results','state','directives'} and parts[1] in LANES:return parts[1]
    if len(parts)>=3 and parts[0]=='data' and parts[1]=='manifests' and parts[2] in LANES:return parts[2]
    for lane in ('frontier','intel','physics','graph','runtime','product','audit','cto'):
        if re.search(rf'(^|[/_.-]){lane}([/_.-]|$)',q):return lane
    return 'cross-lane'

def role_for_path(p):
    q=p.replace('\\','/').lower(); name=Path(q).name
    if '/audit/' in q or re.search(r'(^|[_\-.])(audit|gate)([_\-.]|$)',name):return 'audit_gate'
    if q.startswith('results/'):return 'result_measurement'
    if q.startswith('reports/'):return 'report_verdict'
    if '/charters/' in q or 'charter' in name or re.fullmatch(r'cto_v\d+\.json',name):return 'charter_question'
    if any(x in q for x in ('/prereg/','/protocol/','/method/')) or re.search(r'(prereg|registration|protocol|method|design|freeze|seal|baseline|power|plan)',name):return 'prereg_protocol'
    if re.search(r'(result|metric|measurement|benchmark|evaluation|score|outcome)',name):return 'result_measurement'
    if re.search(r'(report|verdict|finding|falsif|claim|decision|handoff)',name):return 'report_verdict'
    if q.startswith(('state/','data/manifests/','evidence/')) or re.search(r'(manifest|ledger|provenance|receipt|evidence|state)',name):return 'state_provenance'
    return 'context_input'

def wanted_path(p):
    p=p.replace('\\','/'); low=p.lower(); parts=low.split('/')
    if Path(p).suffix.lower() not in EXT:return False
    if low.startswith(('.github/','.opencode/','tools/','archive/','evidence/run-memory/')) or p in {'SPIDER_CODEX_ULTIME.md','SPIDER_ULTIMATE_CODEX.md'}:return False
    if parts and parts[0] in RESEARCH_LANES:return True
    if low.startswith('results/'):return p!='results/CATALOG.json'
    if low.startswith('reports/'):return len(parts)>2 and parts[1] in LANES
    if low.startswith('state/'):return len(parts)>2 and parts[1] in LANES
    if low.startswith('data/manifests/'):return True
    if low.startswith('evidence/frontier-one-shot/'):return True
    if low.startswith(('docs/','directives/')):return bool(K.search(p))
    return False

def blob(oid):
    b=subprocess.check_output(['git','cat-file','blob',oid],cwd=ROOT)
    try:return b,b.decode('utf-8')
    except UnicodeDecodeError:return b,None

def final_tip_blobs(refrows):
    bytree={}; out=defaultdict(lambda:{'paths':set(),'refs':set(),'aliases':set()})
    for ref,_ in refrows:
        tree=sh('git','rev-parse',f'{ref}^{{tree}}',check=False).strip()
        if not tree:continue
        if tree not in bytree:
            items=[]
            for line in sh('git','ls-tree','-r',tree,check=False).splitlines():
                if '\t' not in line:continue
                meta,p=line.split('\t',1); a=meta.split()
                if len(a)>=3 and a[1]=='blob' and wanted_path(p):items.append((a[2],p))
            bytree[tree]=items
        for oid,p in bytree[tree]:out[oid]['paths'].add(p);out[oid]['refs'].add(ref)
    # Whitespace-equivalent files collapse too; exact SHA aliases remain recorded.
    fpmap={}; compact={}
    for oid,info in out.items():
        raw,text=blob(oid)
        if text is None:fp='BIN:'+oid
        else:
            norm='\n'.join(x.rstrip() for x in text.replace('\r\n','\n').replace('\r','\n').split('\n')).strip()+'\n'
            fp='TXT:'+hashlib.sha256(norm.encode()).hexdigest()
        if fp not in fpmap:
            fpmap[fp]=oid;compact[oid]={'paths':set(info['paths']),'refs':set(info['refs']),'aliases':{oid}}
        else:
            c=fpmap[fp];compact[c]['paths']|=info['paths'];compact[c]['refs']|=info['refs'];compact[c]['aliases'].add(oid)
    return compact

def normalized_meta(paths):
    lanes=sorted({lane_for_path(x) for x in paths},key=lambda x:(LANE_ORDER.get(x,99),x)); roles=sorted({role_for_path(x) for x in paths},key=lambda x:(ROLE_ORDER.get(x,99),x))
    return (lanes[0] if lanes else 'unknown',roles[0] if roles else 'context_input',lanes,roles)

def extract_ids(paths,text):
    s='\n'.join(paths)+'\n'+(text[:250000] if text else '')
    ids=[]
    for pat in ID_PATTERNS:
        for m in pat.findall(s):
            x=re.sub(r'[ _]+','-',m.upper()).replace('G-H','G-H').replace('CYCLE-','CYCLE_')
            if x not in ids:ids.append(x)
    for p in paths:
        q=p.replace('\\','/'); parts=q.split('/')
        if parts and parts[0].lower()=='frontier' and len(parts)>1:
            x='FRONTIER:'+parts[1]
            if x not in ids:ids.append(x)
        if len(parts)>2 and parts[0].lower() in {'reports','results'} and parts[1].lower()=='frontier':
            x='FRONTIER:'+parts[2]
            if x not in ids:ids.append(x)
    return ids[:12]

def extract_metrics(path,text):
    if not text or Path(path).suffix.lower()!='.json' or len(text)>2_000_000:return {}
    try:o=json.loads(text)
    except Exception:return {}
    out={}
    def walk(x,prefix='',depth=0):
        if depth>5 or len(out)>=50:return
        if isinstance(x,dict):
            for k,v in x.items():walk(v,f'{prefix}.{k}' if prefix else str(k),depth+1)
        elif isinstance(x,list):
            if len(x)<=12 and all(isinstance(v,(str,int,float,bool,type(None))) for v in x) and METRIC_KEY.search(prefix):out[prefix]=x
        elif isinstance(x,(str,int,float,bool,type(None))) and METRIC_KEY.search(prefix):
            if not isinstance(x,str) or len(x)<=180:out[prefix]=x
    walk(o);return out

def artifact_rows(bs):
    rows=[]
    for oid,info in bs.items():
        paths=sorted(info['paths']); raw,text=blob(oid); lane,role,lanes,roles=normalized_meta(paths); primary=paths[0]
        ids=extract_ids(paths,text or ''); verdicts=[]
        if text:
            for v in VERDICT.findall(text[:300000]):
                u=v.upper().replace(' ','_')
                if u not in verdicts:verdicts.append(u)
        rows.append({'sha':oid,'aliases':sorted(info['aliases']- {oid}),'lane':lane,'role':role,'lanes':lanes,'roles':roles,'paths':paths,'ref_count':len(info['refs']),'bytes':len(raw),'experiment_ids':ids,'verdicts':verdicts[:16],'metrics':extract_metrics(primary,text)})
    rows.sort(key=lambda r:(LANE_ORDER.get(r['lane'],99),ROLE_ORDER.get(r['role'],99),r['paths'][0],r['sha']))
    return rows

def experiment_key(row):
    ids=[x for x in row['experiment_ids'] if not x.startswith('CYCLE_')]
    if ids:return ids[0]
    if row['experiment_ids']:return row['experiment_ids'][0]
    p=row['paths'][0].replace('\\','/'); parts=p.split('/'); lane=row['lane']
    if lane=='frontier':
        for i,x in enumerate(parts[:-1]):
            if x.lower()=='frontier':return f'FRONTIER:{parts[i+1]}'
    stem=re.sub(r'[^a-z0-9]+','-',Path(p).stem.lower()).strip('-')
    stem=re.sub(r'(^|-)\d{8,}($|-)','-',stem).strip('-')
    return f'{lane}:{stem or "context"}'

def groups(rows):
    g=defaultdict(lambda:{'lane':'','roles':Counter(),'shas':[],'verdicts':set()})
    for r in rows:
        k=experiment_key(r); x=g[k]; x['lane']=r['lane'];x['roles'][r['role']]+=1;x['shas'].append(r['sha']);x['verdicts'].update(r['verdicts'])
    return g

def coverage_checks(rows):
    paths={p for r in rows for p in r['paths']}; checks={
      'frontier_charter':any(p.startswith('frontier/') and '/charters/' in p.lower() for p in paths),
      'frontier_prereg':any(p.startswith('frontier/') and 'prereg' in p.lower() for p in paths),
      'frontier_report':any(p.startswith('reports/frontier/') for p in paths),
      'intel_namespace':any(p.startswith('intel/') for p in paths),
      'intel_report':any(p.startswith('reports/intel/') for p in paths),
      'physics_report':any(p.startswith('reports/physics/') for p in paths),
      'graph_report':any(p.startswith('reports/graph/') for p in paths),
      'runtime_report':any(p.startswith('reports/runtime/') for p in paths)}
    miss=[k for k,v in checks.items() if not v]
    if miss:raise RuntimeError('normalized Codex coverage missing: '+', '.join(miss))
    return checks

def snapshot_run_ids(refrows):
    ids=set()
    for r,_ in refrows:
        for m in re.findall(r'/(\d{8,})(?:/|$)',r):ids.add(int(m))
    return ids

def orphan_run_memories(snapshot_ids):
    kept=[]; excluded=0
    for l in sh('git','ls-tree','-r','origin/main','evidence/run-memory/runs',check=False).splitlines():
        try:meta,p=l.split('\t',1);oid=meta.split()[2]
        except Exception:continue
        m=re.search(r'(\d+)\.json$',p);rid=int(m.group(1)) if m else 0
        raw,t=blob(oid)
        if t is None:excluded+=1;continue
        try:r=json.loads(t)
        except Exception:excluded+=1;continue
        wf=str(r.get('workflow_name') or r.get('workflow') or r.get('source_workflow') or '');cls=str(r.get('class') or r.get('evidence_class') or r.get('kind') or '').upper()
        substantive=bool(SUBWF.search(wf) or re.search(r'(result|negative|falsif|measurement|blocked|inconclusive|invalid|product|runtime|graph|physics|intel|frontier|cto|benchmark|claim)',t,re.I))
        if not substantive or (cls in {'OPERATIONAL','INFRA','DUPLICATE','MAINTENANCE','OPERATIONAL_DIAGNOSTIC'} and not SUBWF.search(wf)):excluded+=1;continue
        if rid in snapshot_ids:excluded+=1;continue
        kept.append((rid,oid,p,r))
    kept.sort();return kept,excluded

def fence(t):
    n=3
    for m in re.finditer(r'~+',t):n=max(n,len(m.group())+1)
    return '~'*n

HIST='''## 1. Historical experiments preserved from before the autonomous GitHub lanes

### WP-000 — mechanics-only
- TASKS: 200
- SITES: 56
- RULE DIM-ACC: 0.6595
- RULE EXACT: 0.1603
- NN DIM-ACC: 0.5761
Claim ceiling: early mechanics-only evidence; not proof of universal Web physics.

### WP-001 — robustness over 100 splits
- Splits: 100
- RULE – SHUFFLE DIM: +0.0505
- empirical 95% interval: [+0.0249, +0.0756]
Claim ceiling: rule advantage over shuffle persisted under this protocol.

### WP-002 — raw next-state route
- Status: BLOCKED
- raw_dump unavailable because access depended on Globus / university login.
- Infrastructure/data-access block, not negative scientific evidence.
- Historical audit: WP002_RAW_AUDIT.json.

### WP-002B — WebWorldData true next-state
- TRAJECTORIES: 300
- TRANSITIONS: 901
- REPEATED TRAJECTORY HOLDOUTS: 100
- TRUE NEXT-STATE: YES
- WEBSITE HOLDOUT CLAIM: NO
- MEAN RULE DIM-ACC: 0.6238
- MEAN NN DIM-ACC: 0.6295
- MEAN SHUFFLE DIM-ACC: 0.5706
- RULE - SHUFFLE DIM: mean +0.0532 | median +0.0523 | empirical 95% [+0.0363, +0.0710]
Claim ceiling: true next-state evidence on this dataset/subset; no website-holdout claim.

### Mind2Web V0.40
- VALID: 176
- HARD: 66
- NOVEL: 149/176 (0.8466)
- HARD NOVEL: 56/66 (0.8485)
- RETRIEVAL: 47/176 (0.267)

### Mind2Web V0.50 — falsification gate
- RAW TASKS: 1009
- ACTION EXTRACTION: 3843/6766 (0.568)
- PLAN FOUND: 176/176 (1)
- EXACT HUMAN ROUTE: 6/176 (0.0341)
- SAME OPERATIONS (ANY ORDER): 40/176 (0.2273)
- HARD EXACT HUMAN ROUTE: 4/66 (0.0606)
- HARD SAME OPERATIONS: 19/66 (0.2879)
- OPERATION MICRO-F1: 0.7893
- MEAN LCS / HUMAN ROUTE: 0.5178
- CAUSALLY LINKED COMPOSITION: 23/176 (0.1307)
- STRICT CAUSAL CHAIN: 4/176 (0.0227)
- HARD CAUSAL COMPOSITION: 15/66 (0.2273)
- GT ROUTES WITH ANY CAUSAL DEPENDENCY: 16/176 (0.0909)
Claim ceiling: falsification-oriented evidence; strict causal-composition support is sparse.

Binding rule: positive, negative, BLOCKED, invalid and inconclusive outcomes remain visible. Infrastructure/model failures are not scientific evidence.
'''
LESSONS='''## 2. Product/research architecture lessons established by pre-2.0

1. Immutable work-request identity: bind execution and audit to request ID + content hash.
2. Explicit write sets: never stage injected control-plane/evidence files with broad `git add -A`.
3. Transactional inheritance: publication and consumption must be atomic or hash-pinned.
4. Per-item recovery: quarantine bad artifacts without discarding valid siblings.
5. Workflow success is not epistemic success: route on explicit scientific verdicts.
6. Measurement validity precedes scientific interpretation: invalid instruments cannot falsify hypotheses.
7. Product is the terminal objective, but research claims must be resolved before product claims are promoted.
'''

def main():
    sh('git','fetch','origin','+refs/heads/*:refs/remotes/origin/*','+refs/tags/*:refs/tags/*','--force','--prune')
    rr=refs();bs=final_tip_blobs(rr);rows=artifact_rows(bs);checks=coverage_checks(rows);g=groups(rows);snap=snapshot_run_ids(rr);mem,excluded=orphan_run_memories(snap);ars=action_runs();wf=Counter(str(r.get('name') or '') for r in ars)
    parts=['# SPIDER CODEX ULTIME — CANONICAL KNOWLEDGE BASE\n\n',f'Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}\n\n',
      'Single canonical SPIDER knowledge file. Pre-2.0 research has been normalized here so legacy GitHub Actions runs and orchestration can be deleted.\n\n',
      '**Anti-redundancy rule:** the corpus is the union of the FINAL tree state of every reachable branch/tag snapshot, not every intermediate Git revision. Identical Git blobs are stored once; whitespace-equivalent text blobs are also collapsed. Per-run memory is reproduced only when no durable run snapshot exists. Actions logs are handled separately only for gaps with neither snapshot nor retained run-memory.\n\n',
      '**Normalization rule:** every scientific artifact is assigned the same lane/role schema: charter/question → prereg/protocol → result/measurement → report/verdict → audit/gate → state/provenance/context. Generated labels and metric extraction are navigation aids only; the retained source artifact remains authoritative.\n\n',HIST,'\n',LESSONS,
      '\n## 3. Normalized experiment/result manifest\n\n',
      f'- refs scanned: **{len(rr)}**\n- unique final-state scientific/data contents: **{len(rows)}**\n- orphan substantive run-memory records required as gap-fill: **{len(mem)}**\n- redundant/operational/run-memory records excluded: **{excluded}**\n- live Actions runs inventoried before deletion: **{len(ars)}**\n\n',
      'Coverage assertions: '+', '.join(f'{k}=PASS' for k in sorted(checks))+'.\n\n',
      '### 3.1 Experiments/campaigns grouped into one common schema\n\n| Experiment/campaign | Lane | Charter | Protocol | Result | Report | Audit | State/context | Verdict tokens |\n|---|---|---:|---:|---:|---:|---:|---:|---|\n']
    for k,x in sorted(g.items(),key=lambda kv:(LANE_ORDER.get(kv[1]['lane'],99),kv[0])):
        c=x['roles'];v=', '.join(sorted(x['verdicts']))[:160]
        parts.append(f"| {k.replace('|','/')} | {x['lane']} | {c['charter_question']} | {c['prereg_protocol']} | {c['result_measurement']} | {c['report_verdict']} | {c['audit_gate']} | {c['state_provenance']+c['context_input']} | {v} |\n")
    parts+=['\n### 3.2 Machine-readable artifact manifest\n\n```json\n',json.dumps(rows,ensure_ascii=False,separators=(',',':')),'\n```\n\n### 3.3 Legacy workflow-family counts — inventory only\n\n| Workflow | Runs |\n|---|---:|\n']
    for n,c in sorted(wf.items(),key=lambda x:(-x[1],x[0])):parts.append(f"| {n.replace('|','/')} | {c} |\n")
    parts+=['\n## 4. Normalized verbatim scientific/data corpus from final ref snapshots\n\n']
    for i,r in enumerate(rows,1):
        raw,t=blob(r['sha']);parts+=[f"### 4.{i} — {r['lane']} / {r['role']} — `{r['sha']}`\n\n",'Experiment IDs: '+(', '.join(f'`{x}`' for x in r['experiment_ids']) if r['experiment_ids'] else 'none auto-detected')+'\n\n','Historical path(s): '+', '.join(f'`{p}`' for p in r['paths'])+f"\n\nBytes: {len(raw)}\n\n"]
        if r['aliases']:parts.append('Whitespace-equivalent SHA alias(es): '+', '.join(f'`{x}`' for x in r['aliases'])+'\n\n')
        if t is None:parts.append('Non-UTF8 blob retained by SHA in Git snapshot provenance.\n\n');continue
        f=fence(t);parts.append(f+'\n'+t+('' if t.endswith('\n') else '\n')+f+'\n\n')
    parts+=['\n## 5. Orphan substantive run-memory gap-fill only\n\n','These records are reproduced only when no durable cycle/lab snapshot for the run exists; everything else is omitted here as redundant with section 4.\n\n']
    for i,(rid,oid,p,r) in enumerate(mem,1):
        t=json.dumps(r,ensure_ascii=False,indent=2);f=fence(t);parts+=[f"### 5.{i} — run `{rid}` — blob `{oid}`\n\nPath: `{p}`\n\n",f+'\n'+t+'\n'+f+'\n\n']
    d=sh('git','show','origin/main:evidence/run-memory/DELETED_RUNS_RECOVERY.json',check=False) or 'Recovery aggregate unavailable.\n';f=fence(d)
    parts+=['\n## 6. Previously deleted-run recovery assessment — verbatim\n\n',f+'\n'+d+('' if d.endswith('\n') else '\n')+f+'\n']
    out=''.join(parts).encode('utf-8')
    if len(out)>=MAX:raise RuntimeError(f'Codex {len(out)} bytes exceeds hard limit; refusing truncation')
    OUT.write_bytes(out)
    print(json.dumps({'bytes':len(out),'refs_scanned':len(rr),'unique_final_contents':len(rows),'orphan_run_memory':len(mem),'excluded_run_memory':excluded,'actions_runs':len(ars),'experiment_groups':len(g)},indent=2))
if __name__=='__main__':main()
