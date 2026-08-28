#!/usr/bin/env python3
from __future__ import annotations
import datetime as dt, json, os, re, subprocess, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path.cwd(); OUT=ROOT/"SPIDER_CODEX_ULTIME.md"
REPO=os.getenv("GITHUB_REPOSITORY","Mickalive/Spider"); TOKEN=os.getenv("GITHUB_TOKEN","")
MAX=90*1024*1024; EXT={".md",".json",".txt",".csv",".tsv",".yaml",".yml",".log"}
LANES={"graph","physics","intel","runtime","product","frontier","audit","cto"}
K=re.compile(r"(charter|question|mission|prereg|registration|protocol|method|design|plan|freeze|seal|baseline|power|result|report|audit|gate|verdict|metric|benchmark|measurement|finding|experiment|hypothesis|evidence|evaluation|falsification|claim|ledger|outcome|score|test|manifest|state|decision|limitation|provenance|receipt|handoff|taxonomy|registry)",re.I)
NOISE=re.compile(r"(watchdog|supervisor|control plane|run evidence curator|repo hygiene|publisher|evidence handoff|model router|model health|reaper|purge|maintenance|archive)",re.I)
SUBWF=re.compile(r"(graph|physics|intel|runtime|product|frontier|critical cto council|research lane|engineering loop|failure review|beta)",re.I)

def sh(*a,check=True):
    p=subprocess.run(a,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and p.returncode: raise RuntimeError(f"{' '.join(a)}\n{p.stderr}")
    return p.stdout

def api(url):
    q=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
    if TOKEN:q.add_header("Authorization",f"Bearer {TOKEN}")
    with urllib.request.urlopen(q,timeout=60) as r:return json.load(r)

def action_runs():
    out=[]; page=1
    while True:
        b=api(f"https://api.github.com/repos/{REPO}/actions/runs?per_page=100&page={page}").get("workflow_runs",[])
        if not b:break
        out+=b
        if len(b)<100:break
        page+=1
        if page>100:raise RuntimeError("refusing silent Actions truncation")
    return out

ROLE_ORDER={"charter_question":0,"prereg_protocol":1,"result_measurement":2,"report_verdict":3,"audit_gate":4,"state_provenance":5,"context_input":6}
LANE_ORDER={"graph":0,"physics":1,"intel":2,"runtime":3,"product":4,"frontier":5,"audit":6,"cto":7,"cross-lane":8,"unknown":9}
RESEARCH_LANES={"graph","physics","intel","runtime","product","frontier"}

def lane_for_path(p):
    p=p.replace("\\","/").lower(); parts=p.split("/")
    if parts and parts[0] in RESEARCH_LANES:return parts[0]
    if len(parts)>=2 and parts[0] in {"reports","results","state","directives"} and parts[1] in LANES:return parts[1]
    if len(parts)>=3 and parts[0]=="data" and parts[1]=="manifests" and parts[2] in LANES:return parts[2]
    for lane in ("frontier","intel","physics","graph","runtime","product","audit","cto"):
        if re.search(rf"(^|[/_.-]){re.escape(lane)}([/_.-]|$)",p):return lane
    return "cross-lane"

def role_for_path(p):
    p=p.replace("\\","/").lower(); name=Path(p).name
    if "/audit/" in p or re.search(r"(^|[_\-.])(audit|gate)([_\-.]|$)",name):return "audit_gate"
    if p.startswith("results/"):return "result_measurement"
    if p.startswith("reports/"):return "report_verdict"
    if "/charters/" in p or "charter" in name or re.fullmatch(r"cto_v\d+\.json",name):return "charter_question"
    if any(x in p for x in ("/prereg/","/protocol/","/method/")) or re.search(r"(prereg|registration|protocol|method|design|freeze|seal|baseline|power|plan)",name):return "prereg_protocol"
    if re.search(r"(result|metric|measurement|benchmark|evaluation|score|outcome)",name):return "result_measurement"
    if re.search(r"(report|verdict|finding|falsif|claim|decision|handoff)",name):return "report_verdict"
    if p.startswith(("state/","data/manifests/","evidence/")) or re.search(r"(manifest|ledger|provenance|receipt|evidence|state)",name):return "state_provenance"
    return "context_input"

def wanted_path(p):
    p=p.replace("\\","/")
    if Path(p).suffix.lower() not in EXT:return False
    if p.startswith((".github/",".opencode/","tools/","archive/","evidence/run-memory/")) or p in {"SPIDER_CODEX_ULTIME.md","SPIDER_ULTIMATE_CODEX.md"}:return False
    parts=p.split("/")
    if parts and parts[0].lower() in RESEARCH_LANES:return True
    if p.startswith("results/"):return p!="results/CATALOG.json"
    if p.startswith("reports/"):return len(parts)>2 and parts[1].lower() in LANES
    if p.startswith("state/"):return len(parts)>2 and parts[1].lower() in LANES
    if p.startswith("data/manifests/"):return True
    if p.startswith("evidence/frontier-one-shot/"):return True
    if p.startswith(("docs/","directives/")):return bool(K.search(p))
    return False

def normalized_meta(paths):
    lanes=sorted({lane_for_path(x) for x in paths},key=lambda x:(LANE_ORDER.get(x,99),x))
    roles=sorted({role_for_path(x) for x in paths},key=lambda x:(ROLE_ORDER.get(x,99),x))
    return (lanes[0] if lanes else "unknown",roles[0] if roles else "context_input",lanes,roles)

def coverage_rows(bs):
    c=Counter()
    for paths in bs.values():
        _,_,lanes,roles=normalized_meta(paths)
        for lane in lanes:
            for role in roles:c[(lane,role)]+=1
    return c

def assert_normalized_coverage(bs):
    paths={p for ps in bs.values() for p in ps}
    checks={
      "frontier_charter":any(p.startswith("frontier/") and "/charters/" in p.lower() for p in paths),
      "frontier_prereg":any(p.startswith("frontier/") and "prereg" in p.lower() for p in paths),
      "frontier_report":any(p.startswith("reports/frontier/") for p in paths),
      "intel_namespace":any(p.startswith("intel/") for p in paths),
      "intel_report":any(p.startswith("reports/intel/") for p in paths),
      "physics_report":any(p.startswith("reports/physics/") for p in paths),
      "graph_report":any(p.startswith("reports/graph/") for p in paths),
      "runtime_report":any(p.startswith("reports/runtime/") for p in paths)}
    missing=[k for k,v in checks.items() if not v]
    if missing:raise RuntimeError("normalized Codex coverage missing: "+", ".join(missing))
    return checks

def blob(oid):
    b=subprocess.check_output(["git","cat-file","blob",oid],cwd=ROOT)
    try:return b,b.decode("utf-8")
    except UnicodeDecodeError:return b,None

def fence(t):
    n=3
    for m in re.finditer(r"~+",t):n=max(n,len(m.group())+1)
    return "~"*n

def substantive_blobs():
    d=defaultdict(set)
    for l in sh("git","rev-list","--objects","--all").splitlines():
        if " " not in l:continue
        oid,p=l.split(" ",1)
        if wanted_path(p):d[oid].add(p)
    proc=subprocess.Popen(["git","cat-file","--batch-check=%(objectname) %(objecttype)"],cwd=ROOT,text=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    assert proc.stdin and proc.stdout
    for oid in d:proc.stdin.write(oid+"\n")
    proc.stdin.close(); typ={}
    for l in proc.stdout:
        a=l.split()
        if len(a)>=2:typ[a[0]]=a[1]
    proc.wait()
    return {o:p for o,p in d.items() if typ.get(o)=="blob"}

def run_memories():
    kept=[]; excluded=0
    for l in sh("git","ls-tree","-r","origin/main","evidence/run-memory/runs",check=False).splitlines():
        try:meta,p=l.split("\t",1); oid=meta.split()[2]
        except:continue
        _,t=blob(oid)
        if t is None:excluded+=1;continue
        try:r=json.loads(t)
        except:excluded+=1;continue
        wf=str(r.get("workflow_name") or r.get("workflow") or r.get("source_workflow") or "")
        cls=str(r.get("class") or r.get("evidence_class") or r.get("kind") or "").upper()
        if NOISE.search(wf) and not re.search(r"(critical cto council|product engineering failure review)",wf,re.I):excluded+=1;continue
        if cls in {"OPERATIONAL","INFRA","DUPLICATE","MAINTENANCE","OPERATIONAL_DIAGNOSTIC"} and not SUBWF.search(wf):excluded+=1;continue
        if not SUBWF.search(wf) and not re.search(r"(result|negative|falsif|measurement|blocked|inconclusive|invalid|product|runtime|graph|physics|intel|frontier|cto|benchmark|claim)",t,re.I):excluded+=1;continue
        m=re.search(r"(\d+)\.json$",p)
        kept.append((int(m.group(1)) if m else 0,oid,p,r))
    kept.sort();return kept,excluded

HIST="""## 1. Historical experiments preserved from before the autonomous GitHub lanes

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
"""

LESSONS="""## 2. Product-architecture lessons established by pre-2.0

1. **Immutable work request identity.** Bind execution and audit to immutable `request_id` + content hash; stale Product requests were otherwise consumable.
2. **Explicit write sets.** `git add -A` could stage injected control-plane/evidence files; use explicit output/staging paths.
3. **Transactional inheritance.** Lane branches, `results/`, Product memory and CTO state could disagree; publication/consumption must be atomic or hash-pinned.
4. **Per-item recovery/publishing.** One bad artifact could fail an otherwise valid batch; quarantine bad items and persist good ones.
5. **Workflow success is not epistemic success.** Green Actions may mean REVISE/BLOCKED/INCONCLUSIVE/MEASUREMENT_INVALID; route on explicit gates.
6. **Product is the terminal objective.** Research is an instrument and exists only to resolve concrete product capability, reliability, transfer, economics or implementation uncertainty.
"""

def main():
    sh("git","fetch","origin","+refs/heads/*:refs/remotes/origin/*","+refs/tags/*:refs/tags/*","--force","--prune")
    refs=[l for l in sh("git","for-each-ref","--format=%(refname)","refs/remotes/origin","refs/tags").splitlines() if not l.endswith("/HEAD")]
    bs=substantive_blobs(); checks=assert_normalized_coverage(bs); role_counts=coverage_rows(bs); mem,excluded=run_memories(); ars=action_runs()
    wf=Counter(str(r.get("name") or "") for r in ars); sub=sum(1 for r in ars if SUBWF.search(str(r.get("name") or "")))
    parts=["# SPIDER CODEX ULTIME — KNOWLEDGE BASE BEFORE ARCHITECTURE 2.0\n\n",
      f"Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}\n\n",
      "This is the single canonical reading document for SPIDER knowledge accumulated from project start through the frozen pre-2.0 system. It reads the complete reachable Git history, including `main`, historical `lab/*` work branches, `cycle/*` branches, Frontier/Product/Runtime branches and tags. It writes to none of them.\n\n",
      "**Normalization rule:** every research namespace is treated symmetrically. Textual scientific/data artifacts under `graph/`, `physics/`, `intel/`, `runtime/`, `product/`, and `frontier/` are retained regardless of filename, alongside canonical results/reports/state/manifests. Frontier charters/preregistrations and Intel namespace inputs therefore cannot disappear merely because their filenames lack `result` or `report`.\n\n",
      "**Organization only:** generated lane/role labels never rewrite source evidence; every selected source artifact remains verbatim and SHA-deduplicated.\n\n",
      "**Excluded as useless execution noise:** watchdog ticks, no-op supervisors, routine heartbeats, provider/model retries, duplicate orchestration, curator/publisher/hygiene bookkeeping. The raw 42.7 MB forensic snapshot remains recoverable at commit `ffedfd81872f9dd05641378a4c37aaa48c2a2ddc`.\n\n",
      "**No shortening:** every selected substantive Git artifact and every selected substantive run-memory record is reproduced verbatim. Identical blobs are deduplicated by SHA with all historical paths retained.\n\n",
      HIST,"\n",LESSONS,
      "\n## 3. Coverage manifest and normalized lane/role map\n\n",
      f"- Reachable refs/branch heads scanned: **{len(refs)}**\n",
      f"- Unique substantive Git result/evidence blobs: **{len(bs)}**\n",
      f"- Current substantive per-run memories retained verbatim: **{len(mem)}**\n",
      f"- Current operational/non-substantive run-memory records excluded: **{excluded}**\n",
      f"- GitHub Actions run inventory: **{len(ars)}** total runs counted, **{sub}** in substantive workflow families; execution-only runs are not reproduced.\n",
      "- Deleted-run recovery is reproduced verbatim in section 6; its recorded boundary is 102 deleted runs: 98 `NONE_MATERIAL`, 4 old CTO Council runs `UNKNOWN`, 0 `MATERIAL_RISK`. The four unknowns remain explicit.\n",
      "\n### 3.1 Workflow-family counts (inventory, not knowledge)\n\n| Workflow | Runs |\n|---|---:|\n"]
    for n,c in sorted(wf.items(),key=lambda x:(-x[1],x[0])):parts.append(f"| {n.replace('|','/')} | {c} |\n")
    parts+=["\n### 3.2 Normalized unique-blob counts by lane and role\n\n","| Lane | Role | Unique blobs |\n|---|---|---:|\n"]
    for (lane,role),count in sorted(role_counts.items(),key=lambda x:(LANE_ORDER.get(x[0][0],99),ROLE_ORDER.get(x[0][1],99),x[0])):parts.append(f"| {lane} | {role} | {count} |\n")
    parts.append("\nNormalization assertions: "+", ".join(f"{k}=PASS" for k in sorted(checks))+".\n")
    parts+=["\n## 4. Normalized verbatim scientific/data corpus from complete reachable Git history\n\n"]
    items=[]
    for o,ps in bs.items():
        primary_lane,primary_role,lanes,roles=normalized_meta(ps)
        items.append((primary_lane,primary_role,sorted(ps)[0],o,sorted(ps),lanes,roles))
    items.sort(key=lambda x:(LANE_ORDER.get(x[0],99),ROLE_ORDER.get(x[1],99),x[2],x[3]))
    for i,(primary_lane,primary_role,_,o,paths,lanes,roles) in enumerate(items,1):
        raw,t=blob(o)
        parts+=[f"### 4.{i} — {primary_lane} / {primary_role} — blob `{o}`\n\n","Lane label(s): "+", ".join(f"`{x}`" for x in lanes)+"\n\n","Role label(s): "+", ".join(f"`{x}`" for x in roles)+"\n\n","Historical path(s): "+", ".join(f"`{p}`" for p in paths)+f"\n\nBytes: {len(raw)}\n\n"]
        if t is None:parts.append("Non-UTF8 content remains addressable by Git blob SHA.\n\n");continue
        f=fence(t);parts.append(f+"\n"+t+("" if t.endswith("\n") else "\n")+f+"\n\n")
    parts+=["\n## 5. Substantive per-run memories retained verbatim\n\n"]
    for i,(rid,o,p,r) in enumerate(mem,1):
        t=json.dumps(r,ensure_ascii=False,indent=2);f=fence(t)
        parts+=[f"### 5.{i} — run `{rid}` — blob `{o}`\n\nPath: `{p}`\n\n",f+"\n"+t+"\n"+f+"\n\n"]
    d=sh("git","show","origin/main:evidence/run-memory/DELETED_RUNS_RECOVERY.json",check=False) or "Recovery aggregate unavailable.\n"; f=fence(d)
    parts+=["\n## 6. Deleted-run recovery assessment — verbatim\n\n",f+"\n"+d+("" if d.endswith("\n") else "\n")+f+"\n"]
    out="".join(parts).encode("utf-8")
    if len(out)>=MAX:raise RuntimeError(f"Codex {len(out)} bytes exceeds hard limit; refusing truncation")
    OUT.write_bytes(out)
    print(json.dumps({"bytes":len(out),"refs_scanned":len(refs),"substantive_blobs":len(bs),"substantive_run_records":len(mem),"excluded_run_memory":excluded,"actions_runs":len(ars),"substantive_actions":sub},indent=2))
if __name__=="__main__":main()
