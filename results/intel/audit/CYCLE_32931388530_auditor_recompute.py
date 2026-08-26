#!/usr/bin/env python3
"""Cycle-8 repair-round-3 auditor recomputation (run 32931388530).

Read-only. Re-executes every check the round-3 audit performed on the
persisted reproduction branch cycle/intel/32931388530/repro (= ca97212)
against its base 937c7a5 (round-1 tip) and freeze commit 18abd5a.
Run from anywhere; requires the Spider repo worktrees:
  REPO  = audit checkout (this file's repo)
  REPRO = /tmp/spider_intel_repro (mounted reproduction workspace)

Exit code 0 iff ALL CHECKS PASS.
"""
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout
from math import comb

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPRO = "/tmp/spider_intel_repro"
C8 = "intel/experiments/unbrowse_ladder_c8"
PREREG = "intel/prereg/cycle8_unbrowse_ladder_powered_prereg.md"
SEP = b"--- (frozen text above; errata only below) ---\n"
TIP = "ca972128f7d8c3d406881823d1753224bfe6a9c2"
R1 = "937c7a5"
R0 = "18abd5a"
BASE = "7a8182d"
SELF_HASH_EXPECTED = "67d02ab253f858b76b25227319fc6e4da9ba1f62c43aabbbba421ca418bc83b0"
FULL_HASH_EXPECTED = "e82140e31ef6920dbaf1b9a38c94c48a94758e6e33eae2bb8f1ab7b38dbb948a"
SCHEDULE_HASH = "276132df2f6a57a466d3b84d918e03acc177c10d2e82f745d028f9f02c4efbb8"

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def git(rev, path=None, cwd=REPRO):
    cmd = ["git", "show", rev if path is None else f"{rev}:{path}"]
    return subprocess.run(cmd, capture_output=True, cwd=cwd).stdout


# 1. Lineage ---------------------------------------------------------------
tip = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                     cwd=REPRO).stdout.decode().strip()
check("repro-worktree-HEAD==persisted-tip", tip == TIP, tip)
remote = subprocess.run(["git", "rev-parse", "origin/cycle/intel/32931388530/repro"],
                        capture_output=True, cwd=REPRO).stdout.decode().strip()
check("persisted-branch-tip==worktree", remote == TIP, remote)
anc = subprocess.run(["git", "merge-base", "--is-ancestor", R1, TIP],
                     capture_output=True, cwd=REPRO).returncode == 0
check("descends-from-round1-tip-937c7a5", anc)
anc0 = subprocess.run(["git", "merge-base", "--is-ancestor", R0, TIP],
                      capture_output=True, cwd=REPRO).returncode == 0
check("contains-freeze-commit-18abd5a", anc0)

# 2. Delivery scope: exactly 4 files, zero code ----------------------------
ns = subprocess.run(["git", "diff", "--name-status", f"{R1}..{TIP}"],
                    capture_output=True, cwd=REPRO).stdout.decode().splitlines()
paths = sorted(l.split("\t", 1)[1] for l in ns)
expected_paths = sorted([
    PREREG,
    "results/intel/reproductions/cycle8/pre_freeze_phase0/round3_gate_rerun.json",
    "results/intel/reproductions/cycle8_repair3_delivery_note.md",
    "state/intel_reproduction.json"])
check("delivery-touches-exactly-4-files", paths == expected_paths, str(paths))
check("zero-code-files-touched",
      not any(p.endswith(".py") for p in paths))

# 3. Prereg frozen-region byte invariance ----------------------------------
cur = open(os.path.join(REPRO, PREREG), "rb").read()
old = git(R0, PREREG)


def split_frozen(b):
    i = b.index(SEP) + len(SEP)
    return b[:i], b[i:]


cur_f, cur_e = split_frozen(cur)
old_f, old_e = split_frozen(old)
r1_f, r1_e = split_frozen(git(R1, PREREG))
check("frozen-text-byte-identical-to-freeze-commit", cur_f == old_f)
check("frozen-text-byte-identical-to-round1-tip", cur_f == r1_f)
check("round0-errata-section-was-empty", old_e.strip() == b"")
check("current-errata-nonempty", len(cur_e.strip()) > 1000)

# 4. E1.3 refreshed table vs working tree + superseded rows ----------------
prereg_txt = cur.decode()
rows = re.findall(r"^([0-9a-f]{64})  (\S+?)(?:  SUPERSEDES-STALE-ROW)?$",
                  prereg_txt.split("--- (frozen text above")[1], re.M)
e13 = {}
for hsh, name in rows:
    e13[name] = hsh
check("e13-lists-32-modules", len(e13) == 32, str(len(e13)))
mismatch = [n for n, hsh in e13.items()
            if hashlib.sha256(open(os.path.join(REPRO, C8, n), "rb").read()).hexdigest() != hsh]
check("all-32-module-hashes-match-working-tree", not mismatch, str(mismatch))
s16 = {}
for hsh, name in re.findall(r"^([0-9a-f]{64})  (\S+)$",
                            old.decode().split("--- (frozen text above")[0], re.M):
    s16[name] = hsh
changed = sorted(n for n in s16 if s16[n] != e13[n])
check("exactly-five-superseded-rows",
      changed == sorted(["evaluate_rule.py", "phase0_fixtures.py", "run_all.py",
                         "selftest.py", "tasks_hosts.py"]), str(changed))
prov_old = {"evaluate_rule.py": "241dc64dc65952900f6538cf871526876a7bf7cd6327ca770d1541f17bf8dcea",
            "phase0_fixtures.py": "a9e288f4862d03b674ace4d384d4392102ea5ff4621e0865ba497f5de8e1db8c",
            "run_all.py": "7df2e5f90fa81a3e2593978cc0eff86b4358875c46d6213d2e8623103aab0171",
            "selftest.py": "53b818a30eee5f31f8691ee66e64c96519ca900210764085d9cb3dabbab9b1f7",
            "tasks_hosts.py": "3c69c4cc684cf142a80af4a5f72627a41ddc2431471ee2fafd6c7011c9a2500f"}
check("superseded-old-values-recorded-truthfully",
      all(s16[k] == v for k, v in prov_old.items()))
other27 = all(s16[n] == e13[n] for n in s16 if n not in prov_old)
check("other-27-rows-byte-identical-values", other27)

# 5. E1.4 self-hash ---------------------------------------------------------
marker = b"SELF-HASH INPUT ENDS HERE\n"
i = cur.index(marker) + len(marker)
self_hash = hashlib.sha256(cur[:i]).hexdigest()
full_hash = hashlib.sha256(cur).hexdigest()
check("e14-self-hash-reproduces", self_hash == SELF_HASH_EXPECTED, self_hash)
check("full-file-hash-matches-state-claim", full_hash == FULL_HASH_EXPECTED, full_hash)
state = json.load(open(os.path.join(REPRO, "state/intel_reproduction.json")))
check("state-prereg-sha256==e14-self-hash",
      state["preregistration"]["sha256"] == self_hash)

# 6. Code untouched since round-1 tip --------------------------------------
diffs = []
for f in sorted(os.listdir(os.path.join(REPRO, C8))):
    if not f.endswith(".py"):
        continue
    if open(os.path.join(REPRO, C8, f), "rb").read() != git(R1, f"{C8}/{f}"):
        diffs.append(f)
check("all-32-modules-byte-identical-to-937c7a5", not diffs, str(diffs))

# 7. c7-lineage provenance truth (RFIX-D) ----------------------------------
c7dir, c8dir = "intel/experiments/unbrowse_ladder_c7", C8
f7 = {f for f in os.listdir(os.path.join(REPRO, c7dir)) if f.endswith(".py")}
f8 = {f for f in os.listdir(os.path.join(REPRO, c8dir)) if f.endswith(".py")}
common = sorted(f7 & f8)
new = sorted(f8 - f7)


def h(p):
    return hashlib.sha256(open(os.path.join(REPRO, p), "rb").read()).hexdigest()


verbatim = [f for f in common if h(f"{c7dir}/{f}") == h(f"{c8dir}/{f}")]
changedmod = sorted(set(common) - set(verbatim))
lin = state["c7_lineage_provenance"]
check("common-modules==24", len(common) == lin["common_modules_c7_c8"] == 24)
check("verbatim-count-and-set-truthful",
      len(verbatim) == 16 and sorted(lin["byte_verbatim_vs_c7"]["modules"]) == sorted(verbatim))
check("modified-set-truthful",
      sorted(changedmod) == sorted(
          ["eval_guard.py", "evaluate_rule.py", "extract.py", "run_all.py",
           "selftest.py", "specgen.py", "stats.py", "tasks_hosts.py"]))
a7, a8 = git(R1, f"{c7dir}/eval_guard.py"), open(os.path.join(REPRO, f"{c8dir}/eval_guard.py")).read()
t7, t8 = ast.parse(a7), ast.parse(a8)
body_equal = ast.dump(ast.Module(body=t7.body[1:], type_ignores=())) == \
             ast.dump(ast.Module(body=t8.body[1:], type_ignores=()))
check("eval_guard-delta-docstring-only", body_equal)
check("new-modules-count-and-set-truthful",
      len(new) == 8 and sorted(lin["new_phase0_tooling_modules"]["modules"]) == new)
check("verdict-proposed-null-and-status-pending", state["verdict_proposed"] is None
      and "PENDING" in state["status"])

# 8. Zero condition-level outcomes -----------------------------------------
evdir = os.path.join(REPRO, "results/intel/reproductions/cycle8")
found = sorted(os.path.relpath(os.path.join(r, f), evdir)
               for r, _d, fs in os.walk(evdir) for f in fs)
allowed = sorted(["pre_freeze_phase0/repair1_gate_rerun.json",
                  "pre_freeze_phase0/repair1_rf3_bite_proof.json",
                  "pre_freeze_phase0/round3_gate_rerun.json",
                  "pre_freeze_phase0/soak_samples.json",
                  "pre_freeze_phase0/spare_screening.json"])
check("cycle8-results-dir-contains-only-5-noncevidence-phase0-files", found == allowed, str(found))
bad = [p for p in found if re.search(r"(passes_raw|ladder_events|ttl_window|SHA256SUMS|decision_rule_evaluation)", p, re.I)]
check("no-outcome-shaped-filename-anywhere", not bad, str(bad))
check("phase0-dir-has-exactly-5-files-not-6-as-delivery-note-says", len(allowed) == 5)

# 9. Sealed schedule continuity ---------------------------------------------
sys.path.insert(0, REPRO)
from intel.experiments.unbrowse_ladder_c8 import schedule  # noqa: E402
obj = schedule.build_schedule()
raw = obj if isinstance(obj, bytes) else json.dumps(obj, sort_keys=True,
                                                   separators=(",", ":")).encode()
check("sealed-schedule-hash-regenerates",
      hashlib.sha256(raw).hexdigest() == SCHEDULE_HASH)

# 10. Power tables byte stability + first-principles arithmetic -------------
sys.path.insert(0, REPRO)
from intel.experiments.unbrowse_ladder_c8 import power_tables  # noqa: E402
buf = io.StringIO()
with redirect_stdout(buf):
    try:
        power_tables.main()
    except SystemExit:
        pass
out = buf.getvalue().strip()
emb = ("CONVENTION PINNED:" + prereg_txt.split("CONVENTION PINNED:", 1)[1].split("```")[0]).strip()
check("power-tables-byte-stable-vs-prereg-embedding", out == emb)


def sign_p(wins, n):
    return sum(comb(n, k) for k in range(wins, n + 1)) / 2 ** n


def holm(ps):
    m = len(ps)
    idx = sorted(range(m), key=lambda i: ps[i])
    adj = [0] * m
    prev = 0.0
    for rank, i2 in enumerate(idx):
        v = min(1.0, (m - rank) * ps[i2])
        prev = max(prev, v)
        adj[i2] = prev
    return adj


ok_t1 = True
for n in [5, 6, 7, 8, 9, 10, 11, 12]:
    adj_max = max(holm([sign_p(n, n)] * 4))
    exp = 4 * 2 ** -n
    ok_t1 &= abs(adj_max - exp) < 1e-9
    ok_t1 &= (adj_max < 0.05) == (n >= 7)
check("table1-first-principles-min-adjusted-p", ok_t1)
spot = [(8, [0, 0, 0, 0], True, .015625), (8, [1, 0, 0, 0], True, .035156),
        (8, [1, 1, 0, 0], False, None), (12, [2, 2, 1, 1], True, .038574),
        (12, [3, 0, 0, 0], False, .072998), (12, [1, 0, 0, 0], True, .003174),
        (10, [1, 1, 1, 1], True, .042969), (10, [2, 0, 0, 0], False, .054688),
        (9, [1, 1, 0, 0], True, .039062), (11, [3, 0, 0, 0], False, .113281),
        (12, [0, 0, 0, 0], True, .000977)]
ok_t2 = True
for n, lv, exp_pass, exp_p in spot:
    ps = [sign_p(n - l, n) for l in sorted(lv, reverse=True)]
    a = holm(ps)
    got_pass = all(x < 0.05 for x in a)
    ok_t2 &= got_pass == exp_pass and (exp_p is None or abs(max(a) - exp_p) < 5e-4)
check("table2-eleven-spot-checks-first-principles", ok_t2)

# 11. Clock-gate arithmetic from committed anchors --------------------------
for cyc, f, elig in [("c6", "results/intel/reproductions/cycle6/ttl_window1.json", 1787781930749),
                     ("c7", "results/intel/reproductions/cycle7/ttl_window1.json", 1787790608665)]:
    d = json.load(open(os.path.join(REPRO, f)))
    check(f"{c7dir and cyc}-window2-eligibility-anchor-plus-24h",
          d["ts_ms"] + 86_400_000 == elig, f"{d['ts_ms']}+86400000")

# 12. Scout candidate byte-sync ---------------------------------------------
cand = open(os.path.join(REPRO, "state/intel_candidate.json"), "rb").read()
scout_branch = git("1914d8e14cfd1bde394e2b6ea46fc673717038cb", "state/intel_candidate.json")
mounted = open("/tmp/spider_intel_scout/state/intel_candidate.json", "rb").read()
check("candidate-sha256==claimed", hashlib.sha256(cand).hexdigest() ==
      "7f55e9a838f272a6ef3c9ee2ddac75c2aea25712268acbd283f8f514fd1bc9b1")
check("candidate-byte-identical-across-scout-branch-mounted-scout-repro",
      cand == scout_branch == mounted)

# 13. Tampering scope vs accepted lane base ---------------------------------
ns_all = subprocess.run(["git", "diff", "--name-status", f"{BASE}..{TIP}"],
                        capture_output=True, cwd=REPRO).stdout.decode().splitlines()
outside = [l for l in ns_all
           if not re.search(r"(unbrowse_ladder_c8/|prereg/cycle8|reproductions/cycle8|"
                            r"cycle8_repair3_delivery_note|state/intel_reproduction\.json|"
                            r"state/intel_candidate\.json)", l)]
check("no-changes-outside-cycle8-surface-since-base", not outside, str(outside))

# ---------------------------------------------------------------------------
failed = [(n, d) for n, okk, d in results if not okk]
for n, okk, d in results:
    print(("PASS " if okk else "FAIL ") + n + ("" if okk else f"   [{d}]"))
print(f"\n{len(results) - len(failed)}/{len(results)} CHECKS PASS")
sys.exit(1 if failed else 0)
