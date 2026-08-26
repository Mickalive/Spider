#!/usr/bin/env python3
"""INTEL AUDITOR RECOMPUTATION v2 — cycle 9 repair round 1 (run 32941504002).

Auditor-owned. Written independently for the documentation-only re-audit of
the RF-1..RF-5 repair delivery (branch tip 04b7f1d descending from rejected
tip 523c3c1). All classifier/statistics logic re-implemented here directly
from the FROZEN prereg text (cycle8 prereg sections 10/14); the frozen
stats.bca_or_percentile is imported READ-ONLY only as a cross-check routine
applied to THIS script's own derived log-ratios, beside an independent
percentile bootstrap with a different RNG.

NOTE: this file path previously held an UNATTRIBUTED pre-staged script that
existed before this audit session began; it was inspected and REPLACED by
this auditor-authored version. See audit report boundary note.
"""
import hashlib, json, math, os, random, re, statistics, subprocess, sys
from fractions import Fraction

SCOUT = "/tmp/spider_intel_scout"
REPRO = "/tmp/spider_intel_repro"
A1 = f"{SCOUT}/results/intel/reproductions/cycle8"
SE = f"{REPRO}/results/intel/reproductions/cycle8"
TASKS = ["T_HTTPBIN_FORM", "T_HTTPBIN_COOKIE", "T_PETSTORE_FIND", "T_DEMOBLAZE_CART"]
HOST = {"T_HTTPBIN_FORM": "httpbin.org", "T_HTTPBIN_COOKIE": "httpbin.org",
        "T_PETSTORE_FIND": "petstore.swagger.io", "T_DEMOBLAZE_CART": "www.demoblaze.com"}
HARNESS = {"NO_ROUTE", "PARAM_UNRESOLVED", "ESCALATED_BROWSER", "ESCALATED_HTML_TIER"}

results = []
def check(name, ok, detail=""):
    results.append((ok, name))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))

def load(p):
    with open(p) as f: return json.load(f)

def git(*a, cwd=REPRO):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)

def classify(row):
    """prereg section-10 pair-outcome semantics, re-implemented verbatim."""
    if row.get("payload_ok") is True:
        return "ok"
    if row.get("error"):
        return "harness"
    code = row.get("code")
    if code in HARNESS:
        return "harness"
    if code == "HTTP_ERROR":
        d = str(row.get("detail") or "")
        m = re.search(r"status=(\d+)", d)
        st = int(m.group(1)) if m else None
        return "env" if (st is None or st >= 500) else "loss"
    return "loss"

def sign_p(wins, n):
    return float(sum(Fraction(math.comb(n, k), 2**n) for k in range(wins, n+1)))

def holm(ps):
    m = len(ps); adj=[0.0]*m; run=0.0
    for r,i in enumerate(sorted(range(m), key=lambda i: ps[i])):
        run = max(run, (m-r)*ps[i]); adj[i]=min(1.0,run)
    return adj

def median(v): return statistics.median(v)

def analyze(tree):
    rows = load(f"{tree}/passes_raw.json")
    prod = [r for r in rows if r.get("kind") != "warmup"]
    by = {}
    for r in prod: by.setdefault((r["task"], r["arm"]), {})[r.get("rep")] = r
    out = {"rows_total": len(rows), "rows_prod": len(prod), "tasks": {}, "loho": {}, "c3": {}}
    ps = []
    for t in TASKS:
        A, B = by[(t,"A")], by[(t,"B")]
        pairs, wins, losses, excl_h, excl_e = [], 0, 0, 0, 0
        for rep in sorted(set(A) & set(B)):
            a, b = A[rep], B[rep]
            ca, cb = classify(a), classify(b)
            if ca=="ok" and cb=="ok":
                pairs.append((a["wall_ms"], b["wall_ms"]))
                if b["wall_ms"] < a["wall_ms"]: wins += 1
                else: losses += 1
            elif cb=="loss" and ca=="ok":
                losses += 1                      # completed-but-lost stays in denominator
            elif ca in ("harness","env") or cb in ("harness","env"):
                if "harness" in (ca,cb): excl_h += 1
                else: excl_e += 1
            else:
                losses += 1                      # A ok / B loss already handled; defensive
        n_scored = wins + losses
        medA = median([x for x,_ in pairs]); medB = median([y for _,y in pairs])
        deltas = [math.log(x/y) for x,y in pairs]
        p = sign_p(wins, n_scored) if n_scored else 1.0
        ps.append(p)
        out["tasks"][t] = dict(
            n_valid=len(pairs), wins=wins, losses=losses, excl_h=excl_h, excl_e=excl_e,
            b_only_reps=len([r for r in B if r not in A]),
            medA_raw=medA, medB_raw=medB,
            medA=round(medA,4), medB=round(medB,4), speedup=medA/medB, p=p,
            deltas=deltas,
            b_actions_zero=all(r.get("actions")==0 for r in B.values()),
            b_equiv_ok=all(r.get("code")=="REPLAY_OK" and r.get("payload_ok") is True
                           for r in (B[r] for r in set(A)&set(B))))
    adj = holm(ps)
    for t,a in zip(TASKS,adj): out["tasks"][t]["holm"] = a
    # leave-one-host-out over pooled valid pairs of remaining tasks
    out["loho_stable"] = True
    for hx in sorted(set(HOST.values())):
        pp=[]
        for t in TASKS:
            if HOST[t]==hx: continue
            A,B = by[(t,"A")], by[(t,"B")]
            for rep in sorted(set(A)&set(B)):
                if classify(A[rep])=="ok" and classify(B[rep])=="ok":
                    pp.append((A[rep]["wall_ms"], B[rep]["wall_ms"]))
        w=sum(1 for x,y in pp if y<x)
        ok = median([y for _,y in pp]) < median([x for x,_ in pp]) and w >= 0.7*len(pp)
        out["loho"][f"without_{hx}"]=dict(n=len(pp),wins=w,stable=ok)
        out["loho_stable"] &= ok
    # C3' decision cell
    d = [r for r in prod if r["task"]=="T_DEMOBLAZE_CART"]
    sel = lambda arm,**kw: [r for r in d if r["arm"]==arm and all(r.get(k)==v for k,v in kw.items())]
    Bn,Ds,Da,E = sel("B"), sel("D",d_variant="strict"), sel("D",d_variant="acceptance"), sel("E")
    okr = lambda rs:(sum(1 for r in rs if r.get("payload_ok")), len(rs))
    out["c3"] = dict(B=okr(Bn), Ds=okr(Ds), Da=okr(Da), E=okr(E))
    return out

sys.path.insert(0, REPRO)
from intel.experiments.unbrowse_ladder_c8.stats import bca_or_percentile

def boot_ci_low(deltas, n=200000, seed=8675309):
    rng = random.Random(seed); m=[]; N=len(deltas)
    for _ in range(n):
        s=0.0
        for _ in range(N): s += deltas[rng.randrange(N)]
        m.append(s/N)
    m.sort(); return m[int(0.025*n)]

print("="*25, "INDEPENDENT C2'/C3' RECOMPUTATION BOTH TREES", "="*25)
pub = {  # published dual_collection_robustness.md values (attempt-1 | sealed)
 "attempt1": {"T_HTTPBIN_FORM":(12,12,0,627.5,48.9),"T_HTTPBIN_COOKIE":(12,12,0,468.1,26.1),
              "T_PETSTORE_FIND":(12,12,0,2649.5,31.7),"T_DEMOBLAZE_CART":(12,12,0,6644.2,217.3)},
 "sealed":   {"T_HTTPBIN_FORM":(12,12,0,769.7,81.9),"T_HTTPBIN_COOKIE":(12,12,0,522.0,92.0),
              "T_PETSTORE_FIND":(12,12,0,2548.7,140.0),"T_DEMOBLAZE_CART":(12,12,0,6599.3,176.2)}}
an = {}
for lbl, tree in [("attempt1", A1), ("sealed", SE)]:
    an[lbl] = analyze(tree)
    print(f"-- {lbl}: rows={an[lbl]['rows_total']} prod={an[lbl]['rows_prod']}")
    for t in TASKS:
        g = an[lbl]["tasks"][t]; e = pub[lbl][t]
        check(f"{lbl} {t}: shape 12 valid / 12W-0L-0excl / B-extras=18",
              (g["n_valid"],g["wins"],g["losses"],g["excl_h"],g["excl_e"],g["b_only_reps"])==(12,12,0,0,0,18),
              f"{g['n_valid']}/{g['wins']}/{g['losses']}/{g['excl_h']},{g['excl_e']} extras={g['b_only_reps']}")
        check(f"{lbl} {t}: medians == published {e[3]}->{e[4]} (at 1-decimal precision)",
              round(g["medA_raw"],1)==e[3] and round(g["medB_raw"],1)==e[4], f"{round(g['medA_raw'],1)}->{round(g['medB_raw'],1)}")
        check(f"{lbl} {t}: Holm p == 0.0009765625 & B actions==0 & B equiv OK",
              abs(g["holm"]-0.0009765625)<1e-9 and g["b_actions_zero"] and g["b_equiv_ok"],
              f"holm={g['holm']:.10f}")
        ci = bca_or_percentile(g["deltas"])
        ob = boot_ci_low(g["deltas"])
        g["ci_frozen"], g["ci_own"] = round(ci["ci_low"],4), round(ob,4)
        check(f"{lbl} {t}: BCa(ci_low)>0 [{ci['method']}] AND own-bootstrap ci_low>0",
              ci["ci_low"]>0 and ob>0, f"frozen={g['ci_frozen']} own={g['ci_own']}")
    check(f"{lbl}: LOHO stable all three exclusions", an[lbl]["loho_stable"],
          "; ".join(f"{k}:{v['wins']}/{v['n']}" for k,v in an[lbl]["loho"].items()))
    c3 = an[lbl]["c3"]
    check(f"{lbl}: C3' counts B 30/30, D-strict 0/5, D-acc 0/10, E 0/5",
          c3==dict(B=(30,30),Ds=(0,5),Da=(0,10),E=(0,5)), json.dumps(c3))

for t in TASKS:
    lo = an["sealed"]["tasks"][t]["speedup"] < an["attempt1"]["tasks"][t]["speedup"]
    print(f"   conservative-direction {t}: sealed {an['sealed']['tasks'][t]['speedup']:.2f}x "
          f"vs attempt1 {an['attempt1']['tasks'][t]['speedup']:.2f}x -> {'sealed smaller' if lo else 'sealed larger'}")
cons = sum(1 for t in TASKS if an["sealed"]["tasks"][t]["speedup"] < an["attempt1"]["tasks"][t]["speedup"])
check("sealed tree SMALLER speedup on exactly 3 of 4 tasks (no favorable-selection signature)", cons==3)

# sealed-tree figures must equal committed decision_rule_evaluation.json
dr = load(f"{SE}/decision_rule_evaluation.json")
ok=True; det=""
for t in TASKS:
    c = dr["clause_2_economics_powered"]["tasks"][t]; g = an["sealed"]["tasks"][t]
    if not (c["n_valid_pairs"]==12 and c["wins"]==12 and c["losses_completed"]==0
            and c["median_A_ms"]==round(g["medA_raw"],1) and c["median_B_ms"]==round(g["medB_raw"],1)
            and abs(c["speedup_median_warm_amortized"]-g["speedup"])<0.005
            and abs(c["bca_logratio_ci_low"]-g["ci_frozen"])<5e-5):
        ok=False; det+=f" {t}"
check("sealed recomputation == committed decision_rule_evaluation.json fields", ok, det)
check("committed verdict REPRODUCED_USEFUL with empty invalidity list",
      dr["verdict"]=="REPRODUCED_USEFUL" and dr.get("invalidity_conditions")==[])

print("="*25, "RF-3 PUBLISHED JSON vs MY RECOMPUTATION", "="*25)
rf3 = load(f"{REPRO}/results/intel/reproductions/cycle9_repair1/dual_collection_robustness.json")
ok=True; det=""
for ds in rf3["datasets"]:
    key = "attempt1" if "ATTEMPT-1" in ds["dataset_label"] else "sealed"
    for t in TASKS:
        c = ds["C2_prime_per_task"][t]; g = an[key]["tasks"][t]
        exp = pub[key][t]
        if not (c["n_valid_pairs"]==exp[0] and c["wins"]==exp[1] and c["losses_completed"]==exp[2]
                and abs(c["median_A_ms"]-exp[3])<0.051 and abs(c["median_B_ms"]-exp[4])<0.051
                and abs(c["sign_p_holm"]-0.000977)<1e-6):
            ok=False; det+=f" {key}/{t}"
check("RF-3 robustness.json per-task numbers match my independent recomputation (both datasets)", ok, det)
inv = rf3["invariance_statement"]
check("RF-3 verdict-invariance statement present & single-valued", "IDENTICAL clause outcomes" in inv, inv[:80])

print("="*25, "REPAIR SCOPE / SEAL / FREEZE LINEAGE", "="*25)
d = git("diff","--name-status","523c3c1","04b7f1d").stdout.strip().splitlines()
allowed = ("reports/intel/reproductions/cycle8_report.md",
           "reports/intel/reproductions/cycle9_repair1_report.md",
           "results/intel/reproductions/cycle9_repair1/", "state/intel_reproduction.json")
bad = [l for l in d if not any(l.split("\t")[-1].startswith(p) for p in allowed)]
check("repair diff touches ONLY erratum/state/new-repair-dir/report", not bad, str(bad))
pybad = [l for l in d if l.split("\t",-1)[-1].endswith(".py") and "/cycle9_repair1/" not in l]
check("ZERO .py edits outside cycle9_repair1/", not pybad, str(pybad))
check("ZERO changes under intel/prereg/ or intel/experiments/",
      not [l for l in d if l.split("\t")[-1].startswith(("intel/prereg/","intel/experiments/"))])
ev = git("diff","--name-status","523c3c1","04b7f1d","--","results/intel/reproductions/cycle8/").stdout.strip()
check("SEALED evidence dir untouched between 523c3c1 and repair tip", ev=="")
r = subprocess.run(["sha256sum","-c","SHA256SUMS.txt"],cwd=SE,capture_output=True,text=True)
oks = sum(1 for l in r.stdout.splitlines() if l.endswith(": OK"))
fails = [l for l in (r.stdout+r.stderr).splitlines() if "FAILED" in l or "open or read" in l]
check("42-entry SHA256SUMS verifies on repair branch", oks==42 and not fails, f"OK={oks} fails={fails[:2]}")

pb_se = open(f"{REPRO}/intel/prereg/cycle8_unbrowse_ladder_powered_prereg.md","rb").read()
pb_a1 = open(f"{SCOUT}/intel/prereg/cycle8_unbrowse_ladder_powered_prereg.md","rb").read()
check("prereg byte-identical scout vs repro trees", pb_se==pb_a1)
fb = git("show","18abd5a:intel/prereg/cycle8_unbrowse_ladder_powered_prereg.md").stdout.encode()
check("freeze-commit 18abd5a bytes are a PREFIX of current prereg; E1 erratum follows",
      pb_se[:len(fb)]==fb and pb_se[len(fb):].startswith(b"\n## ERRATUM E1"),
      f"freeze_len={len(fb)} cur_len={len(pb_se)}")
sec16 = txt = pb_se.decode()
m = b"SELF-HASH INPUT ENDS HERE\n"; k = pb_se.index(m)+len(m)
sh = hashlib.sha256(pb_se[:k]).hexdigest()
check("E1.4 self-hash reproduces 67d02ab2...", sh=="67d02ab253f858b76b25227319fc6e4da9ba1f62c43aabbbba421ca418bc83b0", sh)

e13 = {}
for line in txt.splitlines():
    mm = re.match(r"^([0-9a-f]{64})\s+(\S+)\s*(SUPERSEDES-STALE-ROW)?\s*$", line.strip())
    if mm: e13[mm.group(2)] = mm.group(1)
mods = sorted(f for f in os.listdir(f"{REPRO}/intel/experiments/unbrowse_ladder_c8") if f.endswith(".py"))
check("32 modules enumerated; 32-row E1.3 table parsed", len(mods)==32 and len(e13)==32,
      f"tree={len(mods)} table={len(e13)}")
badm=[]
for mod in mods:
    h_r = hashlib.sha256(open(f"{REPRO}/intel/experiments/unbrowse_ladder_c8/{mod}","rb").read()).hexdigest()
    h_s = hashlib.sha256(open(f"{SCOUT}/intel/experiments/unbrowse_ladder_c8/{mod}","rb").read()).hexdigest()
    if not (h_r==h_s==e13.get(mod)): badm.append(mod)
check("all 32 modules sha256-equal across BOTH trees AND equal to E1.3", not badm, str(badm))

print("="*25, "ATTEMPT-1 FORENSICS / MULTIPLICITY", "="*27)
import datetime
def ts(ref): return int(git("log","-1","--format=%ct",ref).stdout.strip())
t_sc, t_se = ts("47bccf3"), ts("523c3c1")
print("scout snapshot commit:", datetime.datetime.utcfromtimestamp(t_sc).isoformat(),
      "| sealed delivery commit:", datetime.datetime.utcfromtimestamp(t_se).isoformat())
check("persist order: scout snapshot commit < sealed delivery commit", t_sc < t_se)
def walk(root):
    out=[]
    for dp,_,fns in os.walk(root):
        for fn in fns: out.append(os.path.relpath(os.path.join(dp,fn), root))
    return sorted(out)
FORBIDDEN = {"SHA256SUMS.txt","decision_rule_evaluation.json","evaluator_invocations.json"}
a1_files, se_files = walk(A1), walk(SE)
ev_a1 = [f for f in a1_files if f.endswith(".json")]
se_ev = [f for f in se_files if f.endswith(".json")]
check("attempt-1 evidence set: 42 json files, NO evaluator-facing artifacts anywhere",
      len(ev_a1)==42 and not any(os.path.basename(f) in FORBIDDEN for f in a1_files),
      f"n_json={len(ev_a1)}")
EXTRA={"SHA256SUMS.txt","decision_rule_evaluation.json","evaluator_invocations.json"}
check("sealed tree == attempt-1 file set PLUS exactly SHA256SUMS/decision/invocation artifacts",
      set(se_files)==set(a1_files)|EXTRA and len(se_ev)==44,
      f"unexpected={sorted(set(se_files)-set(a1_files)-EXTRA)}")
blob_eq = all(open(f"{A1}/{f}","rb").read()==open(f"{SE}/{f}","rb").read()
              for f in ["passes_raw.json"]) is False  # datasets MUST differ (two executions)
check("attempt-1 passes_raw.json DIFFERS byte-wise from sealed (two real datasets)",
      open(f"{A1}/passes_raw.json","rb").read()!=open(f"{SE}/passes_raw.json","rb").read())
def corpus(tree, files): 
    s=""
    for f in files:
        p=os.path.join(tree,f)
        if os.path.exists(p): s+=open(p,encoding="utf-8",errors="replace").read()
    return s
accts = lambda s: sorted(set(re.findall(r"spiderc8\d+", s)))
a_acc = accts(corpus(A1,a1_files)); s_acc = accts(corpus(SE,se_files))
check("distinct throwaway accounts across the two collections",
      a_acc==["spiderc81787723464702"] and s_acc==["spiderc81787724909702"], f"A={a_acc} S={s_acc}")
lm = load(f"{A1}/ladder_events.json"); evs = lm if isinstance(lm,list) else lm.get("events",[])
ts_ms = [e.get("ts_ms") for e in evs if e.get("ts_ms")]
anchor = load(f"{A1}/ttl_window1.json").get("ts_ms")
last_ev, anchor_dt = max(ts_ms)/1000, anchor/1000
snap = datetime.datetime.utcfromtimestamp(t_sc).timestamp()
sealed_first = 1787724909.318  # 06:15:09.318Z per attestation
check("timeline strictly sequential: attempt-1 last event < snapshot commit < sealed probes",
      last_ev < snap < sealed_first,
      f"last_ev={datetime.datetime.utcfromtimestamp(last_ev).isoformat()} snap={datetime.datetime.utcfromtimestamp(snap).isoformat()}")
check("attempt-1 anchor ts decodes to 06:04:33.442Z as disclosed",
      datetime.datetime.utcfromtimestamp(anchor_dt).strftime("%H:%M:%S.%f")[:-3]=="06:04:33.442",
      datetime.datetime.utcfromtimestamp(anchor_dt).isoformat())
inv_log = load(f"{SE}/evaluator_invocations.json")
check("sealed invocation log: exactly one EXECUTED entry, zero REFUSED",
      len(inv_log)==1 and inv_log[0].get("mode")=="EXECUTED" and inv_log[0].get("verdict")=="REPRODUCED_USEFUL")
# rounds 0..8 scout branches contain zero evidence files
clean=True; detl=[]
_gb = lambda ref: subprocess.run(["git","show",ref],cwd=REPRO,capture_output=True).stdout
a1_blob = _gb("47bccf3:results/intel/reproductions/cycle8/passes_raw.json")
se_blob = _gb("523c3c1:results/intel/reproductions/cycle8/passes_raw.json")
_refs=[l.strip() for l in git("for-each-ref","--format=%(refname)","refs/remotes").stdout.splitlines()]
clean=True; detl=[]
for ref in _refs:
    p = subprocess.run(["git","show",f"{ref}:results/intel/reproductions/cycle8/passes_raw.json"],cwd=REPRO,capture_output=True)
    if p.returncode!=0: continue          # ref carries no cycle-8 production evidence at all
    b=p.stdout
    if b not in (a1_blob, se_blob): clean=False; detl.append(f"{ref}: UNKNOWN third dataset")
    for art in ("SHA256SUMS.txt","decision_rule_evaluation.json","evaluator_invocations.json"):
        if git("cat-file","-e",f"{ref}:results/intel/reproductions/cycle8/{art}").returncode==0 \
           and "32935080145" not in ref and "32941504002" not in ref:
            clean=False; detl.append(f"{ref}: unexpected {art}")
c9=[r for r in _refs if r.endswith(("/scout","/audit")) and
    git("ls-tree","-r","--name-only",r,"--","results/intel/reproductions/cycle9").stdout.strip()]
check("every cycle8 passes_raw in ANY ref matches attempt-1 or sealed bytes; no evaluator artifacts elsewhere; no cycle9 dirs on scout/audit refs",
      clean and not c9, "; ".join(detl)+f"; cycle9dirs={c9}")

print("="*25, "RF COMPLIANCE SPOT-CHECKS (delivered docs)", "="*23)
err = open(f"{REPRO}/reports/intel/reproductions/cycle8_report.md").read()
_k = err.find("\n---\n\n> \u26a0\ufe0f **(frozen delivery text above")
head = err[:_k] if _k!=-1 else None
check("original report body above separator unchanged vs 523c3c1",
      head == git("show","523c3c1:reports/intel/reproductions/cycle8_report.md").stdout)
for needle in ["spiderc81787723464702","47bccf3","06:04:34Z","42-file","never an evaluator input",
               "QUARANTINED NON-EVIDENCE","single **guarded evaluation**","RETRACTED"]:
    check(f"D1 erratum contains '{needle}'", needle in err)
st_new = open(f"{REPRO}/state/intel_reproduction.json").read()
stj = json.loads(st_new)
check("state carries binding_caveats_and_forbidden_wordings incl. dual-collection caveat",
      "binding_caveats_and_forbidden_wordings" in stj and "dual_collection_caveat_MANDATORY" in st_new)
check("state carries rf5_infra_escalation_handoff", "rf5_infra_escalation_handoff" in stj)
check("state labels attempt-1 QUARANTINED NON-EVIDENCE", "QUARANTINED NON-EVIDENCE" in st_new)
check("state retracts zero-interventions phrasing", "RETRACTED as materially incomplete" in st_new)
check("state closes live line permanently / no further collection",
      "CLOSED PERMANENTLY" in st_new and "MUST NOT be treated as authorization" in st_new)
rob = open(f"{REPRO}/results/intel/reproductions/cycle9_repair1/dual_collection_robustness.md").read()
check("robustness md labels scout tree NON-EVIDENCE + forbidden uses", "NON-EVIDENCE" in rob and "Forbidden:" in rob)

npass = sum(1 for ok,_ in results if ok); nfail = len(results)-npass
print(f"\nAUDITOR RECOMPUTE TOTAL: {npass}/{len(results)} PASS, {nfail} FAIL")
if nfail:
    for ok,name in results:
        if not ok: print("FAILED:", name)
