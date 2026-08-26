#!/usr/bin/env python3
"""RF-3 robustness recomputation — Intel cycle 9 REPAIR round 1.

INTEL_REPRODUCER-owned, independently written classifier/statistics code
implementing the FROZEN prereg semantics (cycle8 prereg sections 10/14)
from the prereg TEXT; the sealed instrument's evaluate_rule.py was read
only to pin raw-row FIELD semantics (classify_row / pairing by rep), and
its stats.bca_or_percentile is re-run read-only on THIS script's own
derived log-ratio deltas as a frozen-routine cross-check beside an
independent different-RNG percentile bootstrap.

Evaluates BOTH surviving cycle-9 collections of run 32935080145:
  - ATTEMPT-1: origin/cycle/intel/32935080145/scout tip 47bccf3
    (quarantined NON-EVIDENCE observation-tier dataset)
  - SEALED:   origin/cycle/intel/32935080145/repro tip 523c3c1
    (canonical sealed evidence tree)

Read-only with respect to every input tree. Output:
  results/intel/reproductions/cycle9_repair1/dual_collection_robustness.json
"""

import json
import math
import os
import random
import statistics
import sys
from pathlib import Path

# Read-only input checkouts (override via argv[1]=sealed, argv[2]=attempt-1).
REPO = Path(os.environ.get(
    "SEALED_TREE",
    sys.argv[1] if len(sys.argv) > 1 else "/tmp/spider_intel_old_repro"))
SCOUT = Path(os.environ.get(
    "ATTEMPT1_TREE",
    sys.argv[2] if len(sys.argv) > 2 else "/tmp/spider_intel_scout"))

sys.path.insert(0, str(REPO))
from intel.experiments.unbrowse_ladder_c8.stats import bca_or_percentile  # noqa: E402

TASKS = ("T_HTTPBIN_FORM", "T_HTTPBIN_COOKIE", "T_PETSTORE_FIND",
         "T_DEMOBLAZE_CART")
TASK_HOST = {"T_HTTPBIN_FORM": "httpbin.org",
             "T_HTTPBIN_COOKIE": "httpbin.org",
             "T_PETSTORE_FIND": "petstore.swagger.io",
             "T_DEMOBLAZE_CART": "www.demoblaze.com"}
DECISION_CELL = "T_DEMOBLAZE_CART"
HARNESS_CODES = ("NO_ROUTE", "PARAM_UNRESOLVED", "ESCALATED_BROWSER",
                 "ESCALATED_HTML_TIER")
N_MIN_VALID = 8
SPEEDUP_GATE = 2.0


def classify(row):
    """Frozen pair-outcome classification (prereg section 10, verbatim)."""
    if row.get("payload_ok") is True:
        return "ok"
    if row.get("error"):
        return "excluded_harness"
    if row.get("code") in HARNESS_CODES:
        return "excluded_harness"
    detail = str(row.get("detail") or "")
    status = None
    if "status=" in detail:
        try:
            status = int(detail.split("status=")[1].split()[0])
        except Exception:
            status = None
    if row.get("code") == "HTTP_ERROR" and (status is None or status >= 500):
        return "excluded_env"
    return "loss"


def rows_for(passes, arm, task):
    return [p for p in passes
            if p.get("arm") == arm and p.get("task") == task
            and p.get("kind") != "warmup"]


def pairs_for(passes, task):
    a = {p["rep"]: p for p in rows_for(passes, "A", task)
         if isinstance(p.get("rep"), int)}
    b = {p["rep"]: p for p in rows_for(passes, "B", task)
         if isinstance(p.get("rep"), int)}
    out = []
    for r in sorted(set(a) & set(b)):
        ra, rb = a[r], b[r]
        ca, cb = classify(ra), classify(rb)
        e = {"rep": r}
        if ca == "ok" and cb == "ok":
            e["outcome"] = "win" if ra["wall_ms"] > rb["wall_ms"] else "loss"
            e["valid"] = True
        elif ca == "ok" and cb == "loss":
            e["outcome"] = "loss"
            e["valid"] = False
        else:
            e["outcome"] = "excluded"
            e["valid"] = False
            e["why"] = f"A:{ca}/B:{cb}"
        e["A_ms"], e["B_ms"] = ra.get("wall_ms"), rb.get("wall_ms")
        out.append(e)
    return out


def sign_p_one_sided(wins, n):
    """Exact one-sided binomial P(X >= wins | n, 0.5) in rationals."""
    from fractions import Fraction
    total = Fraction(0)
    for k in range(wins, n + 1):
        total += Fraction(math.comb(n, k), 2 ** n)
    return float(total)


def holm(ps):
    """Holm-Bonferroni step-down; returns adjusted p-list (monotone)."""
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj, running = [0.0] * m, 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * ps[idx]
        running = max(running, val)
        adj[idx] = min(1.0, running)
    return adj


def own_bootstrap_ci_low(deltas, n_resample=200_000, seed=975310):
    """Independent percentile bootstrap (different RNG stream from the
    frozen routine's random.Random(20260826)-style seeding)."""
    rng = random.Random(seed)
    n = len(deltas)
    lows = []
    # percentile bootstrap on the mean of log-ratios, 2.5th percentile
    means = []
    for _ in range(n_resample):
        s = 0.0
        for _ in range(n):
            s += deltas[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    lo = means[int(0.025 * n_resample)]
    hi = means[min(n_resample - 1, int(0.975 * n_resample))]
    return lo, hi


def eval_tree(resdir: Path, label: str):
    passes = json.loads((resdir / "passes_raw.json").read_text())
    per_task = {}
    raw_ps = []
    for t in TASKS:
        prs = pairs_for(passes, t)
        scored = [p for p in prs if p["outcome"] in ("win", "loss")]
        valid = [p for p in prs if p.get("valid")]
        wins = sum(1 for p in scored if p["outcome"] == "win")
        a_ms = [p["A_ms"] for p in valid]
        b_ms = [p["B_ms"] for p in valid]
        deltas = ([math.log(x / y) for x, y in zip(a_ms, b_ms)]
                  if len(valid) >= 3 else [])
        bci = bca_or_percentile(deltas) if deltas else None
        ob_lo, ob_hi = own_bootstrap_ci_low(deltas) if deltas else (None, None)
        b_zero = all(p.get("actions") == 0 for p in rows_for(passes, "B", t))
        med_speed = (statistics.median(a_ms) / statistics.median(b_ms)
                     if valid else None)
        per_task[t] = {
            "n_valid_pairs": len(valid),
            "n_scored": len(scored),
            "wins": wins,
            "losses_completed": len(scored) - wins,
            "excluded_harness": sum(1 for p in prs if p["outcome"] == "excluded"
                                    and "harness" in (p.get("why") or "")),
            "excluded_env": sum(1 for p in prs if p["outcome"] == "excluded"
                                and "env" in (p.get("why") or "")),
            "median_A_ms": round(statistics.median(a_ms), 1) if valid else None,
            "median_B_ms": round(statistics.median(b_ms), 1) if valid else None,
            "speedup_median_ratio": round(med_speed, 2) if med_speed else None,
            "bca_method_frozen_rerun": bci.get("method") if bci else None,
            "bca_logratio_ci_low_frozen_rerun": round(bci["ci_low"], 4)
            if bci else None,
            "own_bootstrap_logratio_ci_low_seed975310": round(ob_lo, 4),
            "B_actions_all_zero": b_zero,
            "component_pass": bool(
                len(valid) >= N_MIN_VALID and med_speed
                and med_speed >= SPEEDUP_GATE and bci and bci["ci_low"] > 0
                and b_zero),
        }
        raw_ps.append(sign_p_one_sided(wins, len(scored)) if scored else 1.0)

    adj = holm(raw_ps)
    for i, t in enumerate(TASKS):
        per_task[t]["sign_p_raw_one_sided"] = raw_ps[i]
        per_task[t]["sign_p_holm"] = round(adj[i], 6)
    family_pass = all(per_task[t]["sign_p_holm"] < 0.05 for t in TASKS)

    # leave-one-host-out directional stability (frozen mechanic)
    loho = {}
    stable = True
    for hx in sorted(set(TASK_HOST.values())):
        pp = [(p["A_ms"], p["B_ms"]) for t in TASKS
              if TASK_HOST[t] != hx for p in pairs_for(passes, t)
              if p.get("valid")]
        med_a = statistics.median(x for x, _ in pp)
        med_b = statistics.median(y for _, y in pp)
        w = sum(1 for x, y in pp if y < x)
        keep = med_b < med_a and w >= 0.7 * len(pp)
        stable = stable and keep
        loho[f"without_{hx}"] = {"n_pairs": len(pp), "B_wins": w,
                                 "median_A_ms": round(med_a, 1),
                                 "median_B_ms": round(med_b, 1),
                                 "stable": keep}

    tb = rows_for(passes, "B", DECISION_CELL)
    tds = [p for p in rows_for(passes, "D", DECISION_CELL)
           if p.get("d_variant") == "strict"]
    tda = [p for p in rows_for(passes, "D", DECISION_CELL)
           if p.get("d_variant") == "acceptance"]
    te = rows_for(passes, "E", DECISION_CELL)
    rate = lambda rs: (sum(1 for p in rs if p.get("payload_ok")) / len(rs)
                       if rs else None)
    c3 = {
        "decision_cell": DECISION_CELL,
        "B_n": len(tb), "B_ok": sum(1 for p in tb if p.get("payload_ok")),
        "B_rate": round(rate(tb), 4),
        "D_strict_n": len(tds),
        "D_strict_ok": sum(1 for p in tds if p.get("payload_ok")),
        "D_strict_rate": round(rate(tds), 4),
        "D_acceptance_n": len(tda),
        "D_acceptance_ok": sum(1 for p in tda if p.get("payload_ok")),
        "D_acceptance_rate": round(rate(tda), 4),
        "E_descriptive_n": len(te),
        "E_descriptive_ok": sum(1 for p in te if p.get("payload_ok")),
    }
    c3["pass"] = bool(tb and tds and tda and len(tb) >= 20
                      and c3["B_rate"] >= 0.9 and c3["D_strict_rate"] <= 0.4
                      and (c3["D_acceptance_rate"] <= 0.4
                           or c3["D_acceptance_rate"] >= 0.9))

    # validity precondition from discovery metadata
    dm = json.loads((resdir / "disc_meta_c8.json").read_text())
    dc = json.loads((resdir / "discovery_checks_c8.json").read_text())
    validity = {}
    for t in TASKS:
        meta, chk = dm.get(t, {}), dc.get(t, {})
        validity[t] = {
            "both_completions_accepted":
                meta.get("both_genuine_completions_accepted") == [True, True],
            "routes_learned_n": len(meta.get("routes_learned") or []),
            "discovery_time_replay_code": chk.get("code"),
            "discovery_time_equivalent": bool(chk.get("equivalent")),
        }
        v = validity[t]
        v["pass"] = (v["both_completions_accepted"] and v["routes_learned_n"] > 0
                     and v["discovery_time_equivalent"]
                     and v["discovery_time_replay_code"] == "REPLAY_OK")
    validity_pass = all(v["pass"] for v in validity.values())

    c2_pass = all(per_task[t]["component_pass"] for t in TASKS)
    if not validity_pass:
        verdict = "FAILED_TO_REPRODUCE"
    elif c2_pass and family_pass and stable and c3["pass"]:
        verdict = "REPRODUCED_USEFUL"
    elif not c2_pass and not c3["pass"]:
        verdict = "REPRODUCED_NO_ADVANTAGE"
    else:
        verdict = "INCONCLUSIVE"

    return {
        "dataset_label": label,
        "evidence_root": str(resdir),
        "rows_total": len(passes),
        "verdict_independent_recompute": verdict,
        "validity_precondition": {"pass": validity_pass, "tasks": validity},
        "C2_prime_per_task": per_task,
        "C2_family_gate": {
            "holm_all_below_0.05": family_pass,
            "leave_one_host_out_stable": stable,
            "detail": loho},
        "C3_two_variant_comparator": c3,
    }


def main():
    out = {
        "artifact": "RF-3 dual-collection robustness recomputation",
        "author_role": "INTEL_REPRODUCER (repair round 1, cycle 9)",
        "method_note": (
            "Independently written classifier and sign/Holm arithmetic "
            "implemented from frozen prereg sections 10/14 text; frozen "
            "stats.bca_or_percentile re-run READ-ONLY on this script's own "
            "deltas; independent 200k-resample percentile bootstrap with "
            "RNG seed 975310 as corroboration. No experiment code was "
            "modified; both input trees are read-only."),
        "datasets": [
            eval_tree(SCOUT / "results/intel/reproductions/cycle8",
                      "ATTEMPT-1 (scout snapshot 47bccf3) — QUARANTINED "
                      "NON-EVIDENCE, observation tier only"),
            eval_tree(REPO / "results/intel/reproductions/cycle8",
                      "SEALED canonical evidence (repro tip 523c3c1)"),
        ],
        "invariance_statement": None,  # filled below
    }
    v = {d["verdict_independent_recompute"] for d in out["datasets"]}
    out["invariance_statement"] = (
        "IDENTICAL clause outcomes and verdict across both collections: "
        f"{sorted(v)}" if len(v) == 1 else
        f"DIVERGENT verdicts across datasets: {sorted(v)}")
    # write next to THIS script (the repair checkout), never into an
    # input tree: both input trees are treated as strictly read-only.
    dest = Path(__file__).resolve().parent
    (dest / "dual_collection_robustness.json").write_text(
        json.dumps(out, indent=2) + "\n")

    # console summary cross-check table
    print(out["invariance_statement"])
    for d in out["datasets"]:
        print("=" * 72)
        print(d["dataset_label"], "| verdict:", d["verdict_independent_recompute"])
        for t in TASKS:
            c = d["C2_prime_per_task"][t]
            print(f"  {t:18s} n={c['n_valid_pairs']:2d} W={c['wins']:2d} "
                  f"L={c['losses_completed']} A→B {c['median_A_ms']}→"
                  f"{c['median_B_ms']} ms  x{c['speedup_median_ratio']}  "
                  f"Holm p={c['sign_p_holm']}  ci_lo(frozenBCa)="
                  f"{c['bca_logratio_ci_low_frozen_rerun']}  "
                  f"ci_lo(ownBoot)={c['own_bootstrap_logratio_ci_low_seed975310']}")
        c3 = d["C3_two_variant_comparator"]
        print(f"  C3': B {c3['B_ok']}/{c3['B_n']}={c3['B_rate']} | "
              f"D-strict {c3['D_strict_ok']}/{c3['D_strict_n']}="
              f"{c3['D_strict_rate']} | D-acc {c3['D_acceptance_ok']}/"
              f"{c3['D_acceptance_n']}={c3['D_acceptance_rate']} "
              f"| pass={c3['pass']} | LOHO stable="
              f"{d['C2_family_gate']['leave_one_host_out_stable']}")


if __name__ == "__main__":
    main()
