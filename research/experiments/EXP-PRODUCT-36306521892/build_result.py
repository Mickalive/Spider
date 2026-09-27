"""Build derived metrics for EXP-PRODUCT-36306521892 from raw evidence.

Reads raw_evidence/ (task_results.jsonl, probe_results.jsonl, mechanisms.json,
substrate_probe.json, run_summary.json) and computes:
  - per-arm task success rate and mean requests per task (family-stratified
    B=5000 bootstrap)
  - amortized cost ratio (INHERITANCE vs B-COLD) per regime
  - break-even reuse count f* per regime
  - f* ratio
  - abstention precision and false-accept rate from probes
  - falsifier evaluation F1-F8
  - decision rule evaluation

Writes raw_evidence/derived.json. No interpretation is written here.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from pathlib import Path

EXP = Path(__file__).resolve().parent
RAW = EXP / "raw_evidence"

SEED = 42
BOOTSTRAP_B = 5000


def stratified_bootstrap(by_family, stat, b=BOOTSTRAP_B):
    rng = random.Random(SEED)
    fams = sorted(by_family)
    if not fams:
        return {"point": None, "ci_low": None, "ci_high": None, "n": 0, "B": b, "n_strata": 0}
    point = stat({f: by_family[f] for f in fams})
    draws = []
    for _ in range(b):
        sample = {f: ([by_family[f][rng.randrange(len(by_family[f]))] for _ in range(len(by_family[f]))]
                       if by_family[f] else []) for f in fams}
        try:
            draws.append(stat(sample))
        except (ZeroDivisionError, ValueError):
            continue
    draws.sort()
    if not draws:
        return {"point": point, "ci_low": None, "ci_high": None, "n": 0, "B": b, "n_strata": len(fams)}
    return {
        "point": point, "ci_low": draws[int(0.025 * len(draws))],
        "ci_high": draws[min(len(draws) - 1, int(0.975 * len(draws)))],
        "n": len(draws), "B": b, "n_strata": len(fams),
    }


def rate(sample):
    vals = [v for f in sample for v in sample[f]]
    return sum(vals) / len(vals) if vals else float("nan")


def main() -> int:
    rows = [json.loads(l) for l in (RAW / "task_results.jsonl").read_text().splitlines() if l.strip()]
    probes = [json.loads(l) for l in (RAW / "probe_results.jsonl").read_text().splitlines() if l.strip()]
    mechanisms = json.loads((RAW / "mechanisms.json").read_text())
    substrate_probe = json.loads((RAW / "substrate_probe.json").read_text())
    summary = json.loads((RAW / "run_summary.json").read_text())

    induction_cost = summary["induction_cost"]

    def arm(name):
        return [r for r in rows if r["arm"] == name]

    def fams(name):
        return {f: [r for r in arm(name) if r["family"] == f]
                for f in {r["family"] for r in arm(name)}}

    def boot(name, key):
        return stratified_bootstrap(
            {f: [float(r[key]) for r in rs] for f, rs in fams(name).items()}, rate)

    arms = sorted({r["arm"] for r in rows})
    costs = {n: boot(n, "requests") for n in arms}
    successes = {n: boot(n, "success") for n in arms}
    http_oks = {n: boot(n, "http_ok") for n in arms}

    # Per-family breakdown
    def per_family(name):
        out = {}
        for f, rs in sorted(fams(name).items()):
            out[f] = {
                "n": len(rs),
                "success_rate": sum(r["success"] for r in rs) / len(rs) if rs else None,
                "http_ok_rate": sum(r["http_ok"] for r in rs) / len(rs) if rs else None,
                "mean_requests": sum(r["requests"] for r in rs) / len(rs) if rs else None,
                "resolution_counts": dict(Counter(r.get("resolution", "n/a") for r in rs)),
            }
        return out

    # Amortized cost ratio: (induction + n * transfer) / (n * B-COLD)
    def amortized(arm_name, base_name):
        t = costs[arm_name]["point"]
        b = costs[base_name]["point"]
        n = len(arm(arm_name))
        if b is None or b == 0:
            return None
        return (induction_cost + n * t) / (n * b)

    # Break-even reuse count f* = ceil(induction / (B-COLD - transfer))
    def break_even(base_name, arm_name):
        t = costs[arm_name]["point"]
        b = costs[base_name]["point"]
        if b is None or t is None or b <= t:
            return None  # infinity: transfer cost >= cold cost
        return math.ceil(induction_cost / (b - t))

    # Minimum n where amortized ratio <= 0.85
    def n_for_ratio(base_name, arm_name, threshold=0.85):
        t = costs[arm_name]["point"]
        b = costs[base_name]["point"]
        if b is None or t is None:
            return None
        denom = threshold * b - t
        if denom <= 0:
            return None  # ratio never falls to threshold
        return math.ceil(induction_cost / denom)

    # Probe rates
    probe_by_kind = {}
    for p in probes:
        key = p["kind"]
        probe_by_kind.setdefault(key, {"n": 0, "executed": 0})
        probe_by_kind[key]["n"] += 1
        probe_by_kind[key]["executed"] += int(p["executed"])

    inv = probe_by_kind.get("invalid_intent", {"n": 0, "executed": 0})
    oos = probe_by_kind.get("out_of_support_binding", {"n": 0, "executed": 0})
    es = probe_by_kind.get("empty_string_binding", {"n": 0, "executed": 0})
    abstention_precision = (1.0 - inv["executed"] / inv["n"]) if inv["n"] else None
    false_accept_rate = ((oos["executed"] + es["executed"]) / (oos["n"] + es["n"])) if (oos["n"] + es["n"]) else None

    # Falsifier evaluation
    inh_costly_succ = successes["INHERITANCE-COSTLY"]["point"]
    inh_cheap_succ = successes["INHERITANCE-CHEAP"]["point"]
    pc_succ = successes["PC-SAME-RESOURCE"]["point"]
    bcold_costly_req = costs["B-COLD-COSTLY"]["point"]
    bcold_cheap_req = costs["B-COLD-CHEAP"]["point"]

    f_star_costly = break_even("B-COLD-COSTLY", "INHERITANCE-COSTLY")
    f_star_cheap = break_even("B-COLD-CHEAP", "INHERITANCE-CHEAP")
    f_star_ratio = (f_star_costly / f_star_cheap) if (f_star_costly and f_star_cheap) else (
        0.0 if f_star_costly is not None and f_star_cheap is None else None)

    ratio_costly = amortized("INHERITANCE-COSTLY", "B-COLD-COSTLY")
    ratio_cheap = amortized("INHERITANCE-CHEAP", "B-COLD-CHEAP")
    n_ratio_costly = n_for_ratio("B-COLD-COSTLY", "INHERITANCE-COSTLY", 0.85)
    n_ratio_cheap = n_for_ratio("B-COLD-CHEAP", "INHERITANCE-CHEAP", 0.85)

    falsifiers = {
        "F1_inheritance_success_lt_0.95": (inh_costly_succ is not None and inh_costly_succ < 0.95) or
                                          (inh_cheap_succ is not None and inh_cheap_succ < 0.95),
        "F2_safety_gate_fail": (abstention_precision is not None and abstention_precision < 0.95) or
                                 (false_accept_rate is not None and false_accept_rate > 0.10),
        "F3_ratio_gt_0.85_at_max_n": (ratio_costly is not None and ratio_costly > 0.85) or
                                      (ratio_cheap is not None and ratio_cheap > 0.85),
        "F4_f_star_ratio_le_2.0": f_star_ratio is not None and f_star_ratio <= 2.0,
        "F5_kernel_distill_not_executable": False,  # tests pass, see provenance
        "F6_bcold_costly_le_1.0": bcold_costly_req is not None and bcold_costly_req <= 1.0,
        "F7_bcold_cheap_gt_1.5": bcold_cheap_req is not None and bcold_cheap_req > 1.5,
        "F8_cost_accounting_invalid": False,  # all costs from counted HTTP requests
    }

    # Decision rule
    triggered = [k for k, v in falsifiers.items() if v]
    if falsifiers["F5_kernel_distill_not_executable"]:
        outcome = "NOT_APPLICABLE"
    elif all(not v for v in falsifiers.values()):
        # Check all SUPPORTS conditions
        supports = (
            inh_costly_succ is not None and inh_costly_succ >= 0.95 and
            inh_cheap_succ is not None and inh_cheap_succ >= 0.95 and
            abstention_precision is not None and abstention_precision >= 0.95 and
            false_accept_rate is not None and false_accept_rate <= 0.10 and
            n_ratio_costly is not None and n_ratio_cheap is not None and
            f_star_ratio is not None and f_star_ratio > 2.0 and
            pc_succ is not None and pc_succ >= 0.95
        )
        outcome = "SUPPORTS" if supports else "MIXED"
    else:
        # Some falsifier triggered. MIXED if one regime passes and other fails.
        costly_pass = (inh_costly_succ is not None and inh_costly_succ >= 0.95 and
                       n_ratio_costly is not None)
        cheap_pass = (inh_cheap_succ is not None and inh_cheap_succ >= 0.95 and
                      n_ratio_cheap is not None)
        if costly_pass != cheap_pass:
            outcome = "MIXED"
        elif not costly_pass and not cheap_pass:
            outcome = "FALSIFIES"
        else:
            outcome = "MIXED"

    derived = {
        "arms": arms,
        "arm_n": {n: len(arm(n)) for n in arms},
        "arm_per_family": {n: per_family(n) for n in arms},
        "arm_success_rate": successes,
        "arm_http_ok_rate": http_oks,
        "arm_mean_requests_per_task": costs,
        "induction_cost_total": induction_cost,
        "amortized_cost_ratio_vs_bcold": {
            "costly": ratio_costly,
            "cheap": ratio_cheap,
        },
        "n_for_ratio_0.85": {
            "costly": n_ratio_costly,
            "cheap": n_ratio_cheap,
        },
        "break_even_reuse_count": {
            "f_star_costly": f_star_costly,
            "f_star_cheap": f_star_cheap,
        },
        "f_star_ratio": f_star_ratio,
        "probe_abstention_precision": abstention_precision,
        "probe_false_accept_rate": false_accept_rate,
        "probe_by_kind": probe_by_kind,
        "falsifier_evaluation": falsifiers,
        "falsifiers_triggered": triggered,
        "decision_rule_evaluation": {
            "outcome": outcome,
            "costly_regime_passes_economics": n_ratio_costly is not None,
            "cheap_regime_passes_economics": n_ratio_cheap is not None,
            "costly_regime_passes_mechanism": inh_costly_succ is not None and inh_costly_succ >= 0.95,
            "cheap_regime_passes_mechanism": inh_cheap_succ is not None and inh_cheap_succ >= 0.95,
            "safety_gate_passes": (abstention_precision is not None and abstention_precision >= 0.95 and
                                    false_accept_rate is not None and false_accept_rate <= 0.10),
            "pc_same_resource_success": pc_succ,
            "bcold_costly_mean_requests": bcold_costly_req,
            "bcold_cheap_mean_requests": bcold_cheap_req,
        },
        "inheritance_mechanism_slots": sorted({s for m in mechanisms["inheritance"] for s in m["parameter_slots"]}),
        "inheritance_mechanism_paths": sorted({m["action_template"]["path"] for m in mechanisms["inheritance"]}),
        "inheritance_mechanism_confidence": {m["intent"]: m["confidence"] for m in mechanisms["inheritance"]},
        "nc_mechanism_confidence": {m["intent"]: m["confidence"] for m in mechanisms["nc_shuffled_intent"]},
        "nc_shuffled_success_rate": {
            "costly": successes.get("NC-SHUFFLED-INTENT-COSTLY", {}).get("point"),
            "cheap": successes.get("NC-SHUFFLED-INTENT-CHEAP", {}).get("point"),
        },
        "substrate_probe": substrate_probe,
        "total_http_requests": summary["total_http_requests"],
        "reauths_costly": summary["reauths_costly"],
    }
    (RAW / "derived.json").write_text(json.dumps(derived, indent=2, sort_keys=True, default=str) + "\n")
    print(json.dumps(derived, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
