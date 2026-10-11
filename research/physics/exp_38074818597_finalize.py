"""EXP-PHYSICS-38074818597 EXECUTE finalize/analysis (Python 3.12 stdlib only).

Reads the raw evidence produced by exp_38074818597_run.py, recomputes every
frozen quantity, runs the offline synthetic controls, applies the EXACT frozen
branch rule, and writes:
  research/experiments/EXP-PHYSICS-38074818597/derived/metrics.json
  research/experiments/EXP-PHYSICS-38074818597/result.json
  research/experiments/EXP-PHYSICS-38074818597/report.md
  research/experiments/EXP-PHYSICS-38074818597/provenance.json

RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT -> INTERPRETATION are kept
distinct. No claim is promoted.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exp_38074818597_lib as L  # noqa: E402

EXP_ID = "EXP-PHYSICS-38074818597"
ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "research/experiments" / EXP_ID
EPS = 1e-6


def log(m):
    print(f"[finalize] {m}", flush=True)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


# --------------------------------------------------------------------------
# metric helpers
# --------------------------------------------------------------------------
def logloss_binary(y, p):
    n = len(y)
    total = 0.0
    for yi, pi in zip(y, p):
        pi = min(1 - EPS, max(EPS, pi))
        total += -(yi * math.log(pi) + (1 - yi) * math.log(1 - pi))
    return total / n if n else None


def accuracy_binary(y, p):
    if not y:
        return None
    return sum(1 for yi, pi in zip(y, p) if (1 if pi >= 0.5 else 0) == yi) / len(y)


def prevalence_ci_by_cluster(values_by_endpoint, domains, rng, resamples=10000):
    """Clustered bootstrap CI of the mean of a per-endpoint 0/1 value."""
    clusters = {}
    for i, d in enumerate(domains):
        clusters.setdefault(d, []).append(i)
    keys = list(clusters)
    m = len(keys)
    vals = []
    for _ in range(resamples):
        acc = []
        for _ in range(m):
            acc.extend(clusters[keys[rng.randrange(m)]])
        vals.append(sum(values_by_endpoint[i] for i in acc) / len(acc))
    vals.sort()
    def pct(q):
        pos = (len(vals) - 1) * q / 100.0
        f = int(math.floor(pos)); c = min(f + 1, len(vals) - 1)
        return vals[f] + (vals[c] - vals[f]) * (pos - f)
    return [pct(2.5), pct(97.5)]


def trend_slope(classes_by_sweep, offsets, endpoint_indices):
    """Least-squares slope of barrier prevalence vs rung offset (nats/sec units: /s)."""
    xs, ys = [], []
    for si, off in enumerate(offsets):
        b = [1 if classes_by_sweep[si][i] in L.BARRIER_SET else 0 for i in endpoint_indices]
        xs.append(off); ys.append(sum(b) / len(b))
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else 0.0


def clustered_slope_ci(classes_by_sweep, offsets, domains, rng, resamples=10000):
    clusters = {}
    for i, d in enumerate(domains):
        clusters.setdefault(d, []).append(i)
    keys = list(clusters); m = len(keys)
    vals = []
    for _ in range(resamples):
        idx = []
        for _ in range(m):
            idx.extend(clusters[keys[rng.randrange(m)]])
        vals.append(trend_slope(classes_by_sweep, offsets, idx))
    vals.sort()
    def pct(q):
        pos = (len(vals) - 1) * q / 100.0
        f = int(math.floor(pos)); c = min(f + 1, len(vals) - 1)
        return vals[f] + (vals[c] - vals[f]) * (pos - f)
    return [pct(2.5), pct(97.5)]


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    t_start = time.time()
    spec = L.load_spec(ROOT)
    endpoints = spec["frozen_universe"]["endpoints"]
    n = len(endpoints)
    offsets = spec["sweep_protocol"]["sweep_target_offsets_s"]
    delta_ref = spec["sweep_protocol"]["delta_ref_s"]
    stress = set(spec["strata"]["stratum_stress"]["endpoints"])
    seeds = spec["stable_identifiers"]["seeds"]
    thresholds = spec["decision_rule"]["thresholds_frozen"]

    raw = EXP / "raw"
    ambient = load_jsonl(raw / "ambient_collection.jsonl")
    oracles = load_jsonl(raw / "oracles.jsonl")
    induced = json.loads((raw / "induced_probe.json").read_text())
    meta = json.loads((raw / "collection_meta.json").read_text())

    # ---- classifier replay (recompute class from stored fields) ----
    mismatches = []
    for r in ambient + oracles:
        if L.classify_stored(r) != r["class"]:
            mismatches.append({"url": r.get("url"), "stored": r["class"], "recomputed": L.classify_stored(r)})
    classifier_reproducible = len(mismatches) == 0

    # ---- organize ambient classes ----
    n_sweeps = len(offsets)
    classes_by_sweep = [[None] * n for _ in range(n_sweeps)]
    counts_by_sweep = [{} for _ in range(n_sweeps)]
    seen = [set() for _ in range(n_sweeps)]
    for r in ambient:
        si = r["sweep_index"]; ei = r["endpoint_index"]
        classes_by_sweep[si][ei] = r["class"]
        seen[si].add(ei)
        counts_by_sweep[si][r["class"]] = counts_by_sweep[si].get(r["class"], 0) + 1
    anchor_complete = len(seen[0]) == n and all(c is not None for c in classes_by_sweep[0])
    all_sweeps_complete = all(len(seen[si]) == n for si in range(n_sweeps))
    delta_ref_actual = meta.get("delta_ref_actual_s")

    # ---- live oracle controls ----
    pc_oracle = [r for r in oracles if r.get("oracle") == "PC_ORACLE_BARRIER"]
    nc_oracle = [r for r in oracles if r.get("oracle") == "NC_CLEAN_ORACLE"]
    pc_oracle_ok = bool(pc_oracle) and all(r.get("oracle_ok") for r in pc_oracle)
    nc_oracle_ok = bool(nc_oracle) and all(r.get("class") == "CLEAN" for r in nc_oracle)

    # ---- T0 / delta_ref classes ----
    t0 = classes_by_sweep[0]
    tref = classes_by_sweep[n_sweeps - 1]
    intr_t0 = [1 if c in L.INTRINSIC_CLASSES else 0 for c in t0]
    intr_ref = [1 if c in L.INTRINSIC_CLASSES else 0 for c in tref]
    bar_t0 = [1 if c in L.BARRIER_SET else 0 for c in t0]
    bar_ref = [1 if c in L.BARRIER_SET else 0 for c in tref]
    n_t0_intrinsic = int(sum(intr_t0))
    n_t0_barrier = int(sum(bar_t0))
    f_b_obs = n_t0_barrier / n

    # ---- primary: STATIONARITY_SKILL + B_EXCHANGE + clustered bootstrap ----
    rng_perm = random.Random(seeds["permutation"])
    skill, p_perm = L.perm_test_binary(bar_t0, bar_ref, int(thresholds["permutations"]), rng_perm)
    rng_boot = random.Random(seeds["bootstrap"])
    ci = L.cluster_bootstrap_ci(bar_t0, bar_ref, endpoints, int(thresholds["bootstrap_resamples"]), rng_boot)
    stat_sig = (skill >= thresholds["delta_SKILL_nats"]) and (p_perm < thresholds["alpha"]) and (ci[0] is not None and ci[0] > 0)

    # ---- stationarity by rung ----
    skill_by_rung = {}
    for si in range(1, n_sweeps):
        b = [1 if classes_by_sweep[si][i] in L.BARRIER_SET else 0 for i in range(n)]
        skill_by_rung[offsets[si]] = L.mi_binary(bar_t0, b)

    # ---- no-stress replica ----
    nons = [i for i in range(n) if endpoints[i] not in stress]
    bar_t0_ns = [bar_t0[i] for i in nons]
    bar_ref_ns = [bar_ref[i] for i in nons]
    urls_ns = [endpoints[i] for i in nons]
    skill_ns, p_ns = L.perm_test_binary(bar_t0_ns, bar_ref_ns, int(thresholds["permutations"]), rng_perm)
    ci_ns = L.cluster_bootstrap_ci(bar_t0_ns, bar_ref_ns, urls_ns, int(thresholds["bootstrap_resamples"]), rng_boot)

    # ---- 6-class MI ----
    mi_class = L.mi_general(t0, tref)

    # ---- class persistence ----
    class_persistence = {}
    for c in L.ALL_CLASSES:
        denom = sum(1 for x in t0 if x == c)
        if denom:
            class_persistence[c] = sum(1 for x, y in zip(t0, tref) if x == c and y == c) / denom
    intrinsic_persistence_pooled = (
        sum(1 for x, y in zip(t0, tref) if x in L.INTRINSIC_CLASSES and y == x) / n_t0_intrinsic
        if n_t0_intrinsic else None
    )
    present_intrinsic_classes = [c for c in L.INTRINSIC_CLASSES if any(x == c for x in t0)]
    intrinsic_persistent = (n_t0_intrinsic >= thresholds["min_t0_intrinsic"]) and all(
        class_persistence.get(c, 0.0) >= thresholds["intrinsic_persistence_min"] for c in present_intrinsic_classes
    )

    # ---- denylist metrics ----
    denom_fa = n_t0_intrinsic
    denom_fr = n - n_t0_intrinsic
    fa = (sum(1 for x, y in zip(intr_t0, intr_ref) if x == 1 and y == 0) / denom_fa) if denom_fa else None
    fr = (sum(1 for x, y in zip(intr_t0, intr_ref) if x == 0 and y == 1) / denom_fr) if denom_fr else None
    denylist_valid = (fa is not None and fr is not None and fa <= thresholds["tau_FA"] and fr <= thresholds["tau_FR"])
    anybarrier_fa = (sum(1 for x, y in zip(bar_t0, bar_ref) if x == 1 and y == 0) / n_t0_barrier) if n_t0_barrier else None

    def rung_denylist_valid(si):
        ir = [1 if classes_by_sweep[si][i] in L.INTRINSIC_CLASSES else 0 for i in range(n)]
        a = (sum(1 for x, y in zip(intr_t0, ir) if x == 1 and y == 0) / denom_fa) if denom_fa else None
        b = (sum(1 for x, y in zip(intr_t0, ir) if x == 0 and y == 1) / denom_fr) if denom_fr else None
        return (a is not None and b is not None and a <= thresholds["tau_FA"] and b <= thresholds["tau_FR"]), a, b
    denylist_horizon = 0
    rung_valid_detail = {}
    contiguous = True
    for si in range(1, n_sweeps):
        v, a, b = rung_denylist_valid(si)
        rung_valid_detail[offsets[si]] = {"valid": v, "false_accept": a, "false_reject": b}
        if contiguous and v:
            denylist_horizon = offsets[si]
        else:
            contiguous = False

    # ---- secondary predictors / baselines on the barrier indicator at delta_ref ----
    b_constant = logloss_binary(bar_ref, [0.0] * n)
    b_marginal_p = (sum(bar_ref) / n)
    b_marginal = logloss_binary(bar_ref, [b_marginal_p] * n)
    anchor_transfer_bar = [1.0 if bar_t0[i] else 0.0 for i in range(n)]
    b_anchor_transfer = logloss_binary(bar_ref, anchor_transfer_bar)
    # DENYLIST_SKILL on the intrinsic indicator (denylist = intrinsic transfer)
    intr_anchor = [1.0 if intr_t0[i] else 0.0 for i in range(n)]
    l_const_intrinsic = logloss_binary(intr_ref, [0.0] * n)
    l_anchor_intrinsic = logloss_binary(intr_ref, intr_anchor)
    denylist_skill = (l_const_intrinsic - l_anchor_intrinsic) if (l_const_intrinsic is not None and l_anchor_intrinsic is not None) else None
    last_sweep_acc = None
    last_sweep_mi = None
    if all_sweeps_complete:
        pairs = 0; correct = 0
        for si in range(1, n_sweeps):
            for i in range(n):
                prev = 1 if classes_by_sweep[si - 1][i] in L.BARRIER_SET else 0
                cur = 1 if classes_by_sweep[si][i] in L.BARRIER_SET else 0
                pairs += 1; correct += (prev == cur)
        last_sweep_acc = correct / pairs if pairs else None
        last_sweep_mi = L.mi_binary(bar_t0, [1 if classes_by_sweep[1][i] in L.BARRIER_SET else 0 for i in range(n)])

    # ---- rate / class-conditional diagnostics ----
    rate_onset = 0
    rate_recovery = 0
    recovery_half_lives = []
    for ep in spec["strata"]["stratum_stress"]["endpoints"]:
        burst = induced["bursts"].get(ep, {})
        bclasses = burst.get("classes", [])
        t0_class = t0[endpoints.index(ep)]
        produced_429 = any(c == "RATE_LIMIT_429" for c in bclasses)
        if produced_429 and t0_class != "RATE_LIMIT_429":
            rate_onset += 1
        recs = induced["recovery"].get(ep, [])
        r60 = next((x for x in recs if x["nominal_delay_s"] == 60), None)
        if produced_429 and r60 is not None and r60["class"] != "RATE_LIMIT_429":
            rate_recovery += 1
        if produced_429:
            first = next((x["nominal_delay_s"] for x in recs if x["class"] != "RATE_LIMIT_429"), None)
            recovery_half_lives.append(180 if first is None else first)
    rate_recovery_half_life = None
    if recovery_half_lives:
        s = sorted(recovery_half_lives); m = len(s)
        rate_recovery_half_life = s[m // 2] if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2

    ambient_rate_onset = sum(1 for i in range(n) if t0[i] != "RATE_LIMIT_429" and any(classes_by_sweep[si][i] == "RATE_LIMIT_429" for si in range(1, n_sweeps)))
    ambient_rate_recovery = sum(1 for i in range(n) if t0[i] == "RATE_LIMIT_429" and any(classes_by_sweep[si][i] != "RATE_LIMIT_429" for si in range(1, n_sweeps)))
    class_conditional_transience = bool(rate_recovery > 0 or rate_onset > 0 or ambient_rate_onset > 0 or ambient_rate_recovery > 0)

    # ---- no-stress self-induction trend ----
    slope = trend_slope(classes_by_sweep, offsets, nons)
    rng_boot2 = random.Random(seeds["bootstrap"])
    domains_ns = [L.registrable_domain(endpoints[i]) for i in nons]
    slope_ci = clustered_slope_ci(classes_by_sweep, offsets, domains_ns, rng_boot2)
    slope_excludes_zero = (slope_ci[0] > 0) or (slope_ci[1] < 0)
    barrier_prevalence_by_rung_ns = {}
    for si, off in enumerate(offsets):
        b = [1 if classes_by_sweep[si][i] in L.BARRIER_SET else 0 for i in nons]
        barrier_prevalence_by_rung_ns[off] = sum(b) / len(b)

    # ---- synthetic controls ----
    log("running PC_SYNTHETIC_STATIONARY ...")
    rng_pc = random.Random(seeds["pc_synthetic"])
    pc98 = L.synthetic_power(rng_pc, L.PILOT_MARGINAL6, n, 0.98, 300, 500, 500, "PC98", log)
    rng_pc92 = random.Random(seeds["pc_synthetic"] + 1)
    pc92 = L.synthetic_power(rng_pc92, L.PILOT_MARGINAL6, n, 0.92, 300, 500, 500, "PC92", log)
    log("running NC_SYNTHETIC_EXCHANGEABLE ...")
    rng_nc = random.Random(seeds["nc_synthetic"])
    nc = L.synthetic_false_positive(rng_nc, L.PILOT_MARGINAL6, n, 300, 10000, "NC", log)
    pc_power = pc98["S1_fraction"]
    nc_fpr = nc["perm_sig_fraction"]

    # ---- measurement validity gates ----
    validity_failures = []
    if not classifier_reproducible:
        validity_failures.append("classifier replay mismatch")
    if not anchor_complete:
        validity_failures.append("anchor sweep incomplete")
    if not all_sweeps_complete:
        validity_failures.append("a ladder sweep is incomplete")
    if not pc_oracle_ok:
        validity_failures.append("PC_ORACLE_BARRIER misclassified")
    if not nc_oracle_ok:
        validity_failures.append("NC_CLEAN_ORACLE misclassified")
    if pc_power < thresholds["pc_power_min"]:
        validity_failures.append(f"PC power {pc_power} < {thresholds['pc_power_min']}")
    if nc_fpr > thresholds["nc_false_positive_max"]:
        validity_failures.append(f"NC false-positive {nc_fpr} > {thresholds['nc_false_positive_max']}")
    if n_t0_intrinsic < thresholds["min_t0_intrinsic"]:
        validity_failures.append(f"n_t0_intrinsic {n_t0_intrinsic} < {thresholds['min_t0_intrinsic']}")
    if n_t0_barrier < thresholds["min_t0_barrier"]:
        validity_failures.append(f"n_t0_barrier {n_t0_barrier} < {thresholds['min_t0_barrier']}")
    if delta_ref_actual is None or delta_ref_actual < thresholds["delta_ref_min_actual_s"]:
        validity_failures.append(f"delta_ref actual {delta_ref_actual} < {thresholds['delta_ref_min_actual_s']}")
    measurement_valid = len(validity_failures) == 0

    # ---- frozen branch ----
    change_classes = []
    if measurement_valid:
        if intrinsic_persistent and denylist_valid and stat_sig:
            branch = "S1_STATIONARY"
        else:
            branch = "S0_NON_STATIONARY"
            if not intrinsic_persistent:
                change_classes.append("intrinsic_break")
            if not denylist_valid:
                change_classes.append("intrinsic_denylist_violation")
            if not stat_sig:
                change_classes.append("no_anchor_information")
    else:
        branch = "MEASUREMENT_INVALID"

    outcome = "NOT_APPLICABLE" if not measurement_valid else ("SUPPORTS" if branch == "S1_STATIONARY" else "FALSIFIES")
    status = "COMPLETE" if measurement_valid else "MEASUREMENT_INVALID"

    # ---- metrics object ----
    metrics = {
        "STATIONARITY_SKILL": skill,
        "STATIONARITY_SKILL_B_EXCHANGE_p": p_perm,
        "STATIONARITY_SKILL_CI95": ci,
        "STATIONARITY_SKILL_BY_RUNG": skill_by_rung,
        "STATIONARITY_SKILL_NO_STRESS": skill_ns,
        "STATIONARITY_SKILL_NO_STRESS_B_EXCHANGE_p": p_ns,
        "STATIONARITY_SKILL_NO_STRESS_CI95": ci_ns,
        "MI_CLASS": mi_class,
        "CLASS_PERSISTENCE": class_persistence,
        "INTRINSIC_PERSISTENCE": intrinsic_persistence_pooled,
        "INTRINSIC_PERSISTENT": intrinsic_persistent,
        "present_intrinsic_classes": present_intrinsic_classes,
        "DENYLIST_FALSE_ACCEPT": fa,
        "DENYLIST_FALSE_REJECT": fr,
        "DENYLIST_INTRINSIC_VALID": denylist_valid,
        "DENYLIST_BY_RUNG": rung_valid_detail,
        "DENYLIST_HORIZON": denylist_horizon,
        "ANYBARRIER_FALSE_ACCEPT": anybarrier_fa,
        "DENYLIST_SKILL": denylist_skill,
        "DENYLIST_SKILL_definition": "logloss(nats/endpoint) of B_CONSTANT_USABLE(0) minus anchor intrinsic-transfer predictor on the delta_ref intrinsic indicator; positive = anchor denylist better",
        "RATE_ONSET_n": rate_onset,
        "RATE_RECOVERY_n": rate_recovery,
        "RATE_RECOVERY_HALF_LIFE_s": rate_recovery_half_life,
        "AMBIENT_RATE_ONSET_n": ambient_rate_onset,
        "AMBIENT_RATE_RECOVERY_n": ambient_rate_recovery,
        "CLASS_CONDITIONAL_TRANSIENCE": class_conditional_transience,
        "STATIONARITY_SKILL_NO_STRESS_TREND_slope_per_s": slope,
        "STATIONARITY_SKILL_NO_STRESS_TREND_CI95": slope_ci,
        "STATIONARITY_SKILL_NO_STRESS_TREND_excludes_zero": slope_excludes_zero,
        "barrier_prevalence_by_rung_no_stress": barrier_prevalence_by_rung_ns,
        "n_t0_intrinsic": n_t0_intrinsic,
        "n_t0_barrier": n_t0_barrier,
        "f_b_obs": f_b_obs,
        "POWER_AT_RHO98": pc_power,
        "POWER_AT_RHO92": pc92["S1_fraction"],
        "POWER_AT_RHO98_FIXED_ENDOWMENT": pc98["S1_fraction_given_n_t0_intrinsic_ge_3"],
        "POWER_AT_RHO92_FIXED_ENDOWMENT": pc92["S1_fraction_given_n_t0_intrinsic_ge_3"],
        "branch": branch,
        "change_evidence_classes": change_classes,
        "measurement_valid": measurement_valid,
        "class_counts_by_sweep": counts_by_sweep,
        "rung_actual_delta_s": meta.get("rung_actual_delta_s"),
        "delta_ref_actual_s": delta_ref_actual,
    }

    # ---- controls object ----
    controls = {
        "PC_SYNTHETIC_STATIONARY": {
            "expected": "S1 selection fraction >= 0.80 at rho=0.98",
            "observed": {"rho98": pc98, "rho92": pc92},
            "pass": bool(pc_power >= thresholds["pc_power_min"]),
        },
        "NC_SYNTHETIC_EXCHANGEABLE": {
            "expected": "B_EXCHANGE p<0.05 fraction <= 0.05",
            "observed": nc,
            "pass": bool(nc_fpr <= thresholds["nc_false_positive_max"]),
        },
        "PC_ORACLE_BARRIER": {
            "expected": "every oracle request classified into its expected class",
            "observed": [
                {"url": r["url"], "class": r["class"], "expected": r["expected_class"], "ok": r["oracle_ok"], "error": r["error"]}
                for r in pc_oracle
            ],
            "pass": bool(pc_oracle_ok),
        },
        "NC_CLEAN_ORACLE": {
            "expected": "all requests classify CLEAN",
            "observed": [{"url": r["url"], "class": r["class"], "error": r["error"]} for r in nc_oracle],
            "pass": bool(nc_oracle_ok),
        },
        "C_PROBE_SELF_INDUCTION": {
            "expected": "no hard pass/fail; report self-induction trend",
            "observed": {
                "barrier_prevalence_by_rung_no_stress": barrier_prevalence_by_rung_ns,
                "slope_per_s": slope,
                "slope_ci95": slope_ci,
                "slope_excludes_zero": slope_excludes_zero,
                "STATIONARITY_SKILL_NO_STRESS": skill_ns,
                "STATIONARITY_SKILL_NO_STRESS_p": p_ns,
            },
            "pass": None,
        },
        "B_EXCHANGE": {
            "expected": "primary strong null: anchor barrier indicator carries no info beyond marginal",
            "observed": {"p_value": p_perm, "permutations": int(thresholds["permutations"]), "seed": seeds["permutation"]},
            "pass": None,
        },
        "B_CONSTANT_USABLE": {"expected": "no-denylist floor (predict non-barrier)", "observed": {"logloss_nats": b_constant, "logloss_intrinsic": l_const_intrinsic}, "pass": None},
        "B_MARGINAL": {"expected": "constant-marginal diagnostic", "observed": {"logloss_nats": b_marginal, "marginal_p": b_marginal_p}, "pass": None},
        "B_LASTSWEEP": {"expected": "recent-memory diagnostic", "observed": {"accuracy": last_sweep_acc, "mi_prev_next": last_sweep_mi}, "pass": None},
    }

    # ---- artifacts ----
    artifacts = []
    for rel in ["raw/ambient_collection.jsonl", "raw/oracles.jsonl", "raw/induced_probe.json", "raw/collection_meta.json"]:
        p = EXP / rel
        if p.exists():
            artifacts.append({"path": f"research/experiments/{EXP_ID}/{rel}", "sha256": sha(p), "role": "raw"})
    for rel in ["derived/metrics.json"]:
        p = EXP / rel
        if p.exists():
            artifacts.append({"path": f"research/experiments/{EXP_ID}/{rel}", "sha256": sha(p), "role": "derived"})
    for p in [Path(__file__).resolve(), Path(__file__).resolve().parent / "exp_38074818597_lib.py", Path(__file__).resolve().parent / "exp_38074818597_run.py"]:
        if p.exists():
            artifacts.append({"path": str(p.relative_to(ROOT)), "sha256": sha(p), "role": "code"})

    # ---- observations ----
    observations = [
        {"id": "O1", "text": f"Anchor T0 ambient histogram: {counts_by_sweep[0]}", "evidence": "raw/ambient_collection.jsonl"},
        {"id": "O2", "text": f"delta_ref (nominal +{delta_ref}s) ambient histogram: {counts_by_sweep[n_sweeps-1]}", "evidence": "raw/ambient_collection.jsonl"},
        {"id": "O3", "text": f"All-rung ambient histograms: {counts_by_sweep}", "evidence": "raw/ambient_collection.jsonl"},
        {"id": "O4", "text": f"n_t0_intrinsic={n_t0_intrinsic}, n_t0_barrier={n_t0_barrier}, f_b_obs={f_b_obs:.4f}", "evidence": "derived/metrics.json"},
        {"id": "O5", "text": f"delta_ref actual delta = {delta_ref_actual}s; rung actual deltas = {meta.get('rung_actual_delta_s')}", "evidence": "raw/collection_meta.json"},
        {"id": "O6", "text": f"oracle classifications: PC={[ (r['url'],r['class']) for r in pc_oracle ]}, NC={[ (r['url'],r['class']) for r in nc_oracle ]}", "evidence": "raw/oracles.jsonl"},
        {"id": "O7", "text": f"induced bursts: { {ep: induced['bursts'][ep]['classes'] for ep in induced['bursts']} }", "evidence": "raw/induced_probe.json"},
        {"id": "O8", "text": f"induced recovery series: { {ep: [(x['nominal_delay_s'], x['class']) for x in induced['recovery'][ep]] for ep in induced['recovery']} }", "evidence": "raw/induced_probe.json"},
        {"id": "O9", "text": f"per-endpoint T0 vs delta_ref intrinsic transition: T0 intrinsic = {[endpoints[i] for i in range(n) if intr_t0[i]]}", "evidence": "raw/ambient_collection.jsonl"},
        {"id": "O10", "text": f"classifier replay mismatches = {len(mismatches)} / {len(ambient)+len(oracles)} requests", "evidence": "raw/ambient_collection.jsonl"},
    ]

    # ---- validity notes ----
    validity_notes = [
        "Single network vantage / single stdlib client / single ~{}s session; the source-vantage axis is a declared scope boundary (spec.scope_boundaries).".format(round(meta.get("wall_clock_s", 0))),
        "The denylist horizon is right-censored at delta_ref=1800 s; no information beyond the tested ladder is claimed.",
        "DENYLIST_FALSE_REJECT uses the frozen falsifier/prereg denominator |T0 non-intrinsic| (design_review N3 resolved in favour of falsifier/prereg over the conflicting decision_rule wording).",
        "DENYLIST_SKILL is reported on the intrinsic indicator (anchor intrinsic-transfer predictor vs constant non-intrinsic); the frozen name does not specify the smoothing, so clipping eps=1e-6 is used and the operational definition is recorded in metrics.",
        "PC_SYNTHETIC_STATIONARY uses the control's own literal perms_per_rep=500 and R=300 with a 500-resample clustered bootstrap for the CI clause (design_review N4 notes the 10000-permutation inconsistency in thresholds_frozen); the pass gate is the rho=0.98 S1 fraction.",
        "The induced-transience probe interleaves the 5 stress endpoints' recovery ladders at each nominal delay after each endpoint's own burst rather than serializing whole endpoints; Q3 is a reported refinement that never gates S1/S0.",
        "Body SHA-256 and the stored classifier prefix are the first 262144 bytes (the frozen match scope); a printable 8192-char prefix is stored for auditability.",
        "The pre-freeze census/calibration /tmp artifacts cited in spec/prereg are absent and are declared non-interpretation-dependencies (design_review N1/N2); EXECUTE re-derived all floors, controls and metrics from its own raw data.",
        "The pre-freeze census is outcome-adjacent pilot evidence on parent-inherited endpoints, not the frozen 4-sweep/1800 s measurement; it does not certify persistence at 1800 s (prereg validity threat 10).",
    ]

    unresolved = [
        "Does endpoint access-barrier persistence generalize beyond this frozen 57-endpoint pool, this single egress vantage and this ~30-minute window? The source-vantage axis is untested.",
        "Is the measured horizon censored: would the intrinsic denylist remain valid at delta > 1800 s?",
        "ONSET (CLEAN->intrinsic) at higher request rates or longer sequences remains untested outside the fixed 8-GET stress burst.",
        "The simultaneous role of protocol self-induction cannot be fully removed; C_PROBE_SELF_INDUCTION only bounds ambient barrier prevalence on the 52 non-stress endpoints.",
    ]
    if len(mismatches):
        unresolved.append(f"Classifier replay produced {len(mismatches)} mismatches: {mismatches[:5]}")

    # ---- write derived metrics ----
    derived = {
        "experiment_id": EXP_ID,
        "computed_at": now_iso(),
        "metrics": metrics,
        "controls": controls,
        "validity_failures": validity_failures,
        "measurement_valid": measurement_valid,
        "classifier_replay_mismatches": mismatches,
        "collection_meta": meta,
    }
    L.write_json(EXP / "derived/metrics.json", derived)
    artifacts.append({"path": f"research/experiments/{EXP_ID}/derived/metrics.json", "sha256": sha(EXP / "derived/metrics.json"), "role": "derived"})

    # ---- result.json ----
    result = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": "physics",
        "status": status,
        "outcome": outcome,
        "branch": branch,
        "claim_ids": spec["claim_ids"],
        "claim_ceiling": spec["decision_rule"]["claim_ceiling"],
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }
    L.write_json(EXP / "result.json", result)

    # ---- provenance.json ----
    request = json.loads((EXP / "request.json").read_text())
    provenance = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": "physics",
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "origin_github_run_id": request.get("origin_github_run_id"),
        "git_sha": os.environ.get("GITHUB_SHA") or _git(["rev-parse", "HEAD"]),
        "git_branch": _git(["branch", "--show-current"]),
        "base_sha": request.get("base_sha"),
        "recorded_at": now_iso(),
        "frozen_inputs": {
            "request.json": sha(EXP / "request.json"),
            "spec.json": sha(EXP / "spec.json"),
            "prereg.md": sha(EXP / "prereg.md"),
            "freeze.json": sha(EXP / "freeze.json"),
            "design_review.json": sha(EXP / "design_review.json"),
        },
        "frozen_artifact_hashes": json.loads((EXP / "freeze.json").read_text()).get("artifact_hashes", {}),
        "code": {
            "run_script": {"path": "research/physics/exp_38074818597_run.py", "sha256": sha(Path(__file__).resolve().parent / "exp_38074818597_run.py")},
            "finalize_script": {"path": "research/physics/exp_38074818597_finalize.py", "sha256": sha(Path(__file__).resolve())},
            "lib": {"path": "research/physics/exp_38074818597_lib.py", "sha256": sha(Path(__file__).resolve().parent / "exp_38074818597_lib.py")},
        },
        "dataset": {
            "type": "frozen_web_endpoint_universe",
            "n_endpoints": n,
            "source": spec["frozen_universe"]["source"],
            "endpoints_sha256": hashlib.sha256(json.dumps(endpoints).encode()).hexdigest(),
        },
        "raw_evidence": {a["path"]: a["sha256"] for a in artifacts if a["role"] == "raw"},
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "implementation": platform.python_implementation(),
            "numpy_imported": "numpy" in sys.modules,
        },
        "commands": [
            "python3 research/physics/exp_38074818597_run.py --seed 38074818597",
            "python3 research/physics/exp_38074818597_finalize.py",
        ],
        "seeds": seeds,
        "thresholds": thresholds,
    }
    L.write_json(EXP / "provenance.json", provenance)

    # ---- report.md ----
    write_report(spec, metrics, controls, observations, validity_notes, unresolved, validity_failures, meta, mismatches)

    log(f"FINAL branch={branch} status={status} outcome={outcome} valid={measurement_valid} failures={validity_failures}")
    log(f"finalize wall_clock={time.time()-t_start:.1f}s")


def _git(args):
    import subprocess
    try:
        return subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip()
    except Exception:
        return None


def write_report(spec, m, controls, observations, validity_notes, unresolved, validity_failures, meta, mismatches):
    def fmt(x):
        if isinstance(x, float):
            return f"{x:.6g}"
        return str(x)
    lines = []
    lines.append(f"# EXP-PHYSICS-38074818597 — EXECUTE report")
    lines.append("")
    lines.append(f"- Lane: **physics**; target claim **C-WEB-DYNAMICS** (no promotion).")
    lines.append(f"- Frozen branch: **{m['branch']}**; measurement valid: **{m['measurement_valid']}**.")
    if validity_failures:
        lines.append(f"- MEASUREMENT_INVALID failures: {validity_failures}")
    lines.append(f"- Anchor T0 histogram: `{m['class_counts_by_sweep'][0]}`")
    lines.append(f"- delta_ref histogram: `{m['class_counts_by_sweep'][-1]}`")
    lines.append(f"- n_t0_intrinsic={m['n_t0_intrinsic']}, n_t0_barrier={m['n_t0_barrier']}, f_b_obs={fmt(m['f_b_obs'])}")
    lines.append(f"- delta_ref actual = {fmt(m['delta_ref_actual_s'])} s; rung actual deltas = {m['rung_actual_delta_s']}")
    lines.append("")
    lines.append("## Primary quantities")
    lines.append("")
    lines.append(f"- STATIONARITY_SKILL = **{fmt(m['STATIONARITY_SKILL'])} nats**; B_EXCHANGE p = {fmt(m['STATIONARITY_SKILL_B_EXCHANGE_p'])}; clustered CI95 = {[fmt(c) for c in m['STATIONARITY_SKILL_CI95']]}")
    lines.append(f"- STATIONARITY_SKILL_BY_RUNG = { {k: round(v,6) for k,v in m['STATIONARITY_SKILL_BY_RUNG'].items()} }")
    lines.append(f"- STATIONARITY_SKILL_NO_STRESS = {fmt(m['STATIONARITY_SKILL_NO_STRESS'])} (p={fmt(m['STATIONARITY_SKILL_NO_STRESS_B_EXCHANGE_p'])})")
    lines.append(f"- MI_CLASS = {fmt(m['MI_CLASS'])}")
    lines.append(f"- CLASS_PERSISTENCE = { {k: round(v,4) for k,v in m['CLASS_PERSISTENCE'].items()} }")
    lines.append(f"- INTRINSIC_PERSISTENT = **{m['INTRINSIC_PERSISTENT']}** (pooled persistence {fmt(m['INTRINSIC_PERSISTENCE'])}, present classes {m['present_intrinsic_classes']})")
    lines.append(f"- DENYLIST_FALSE_ACCEPT = {fmt(m['DENYLIST_FALSE_ACCEPT'])}, DENYLIST_FALSE_REJECT = {fmt(m['DENYLIST_FALSE_REJECT'])}, DENYLIST_INTRINSIC_VALID = **{m['DENYLIST_INTRINSIC_VALID']}**")
    lines.append(f"- DENYLIST_HORIZON = {m['DENYLIST_HORIZON']} s; DENYLIST_BY_RUNG = {m['DENYLIST_BY_RUNG']}")
    lines.append(f"- ANYBARRIER_FALSE_ACCEPT = {fmt(m['ANYBARRIER_FALSE_ACCEPT'])}; DENYLIST_SKILL = {fmt(m['DENYLIST_SKILL'])} nats")
    lines.append(f"- rate diagnostics: RATE_ONSET_n={m['RATE_ONSET_n']}, RATE_RECOVERY_n={m['RATE_RECOVERY_n']}, RATE_RECOVERY_HALF_LIFE_s={fmt(m['RATE_RECOVERY_HALF_LIFE_s'])}, AMBIENT_RATE_ONSET_n={m['AMBIENT_RATE_ONSET_n']}, AMBIENT_RATE_RECOVERY_n={m['AMBIENT_RATE_RECOVERY_n']}, CLASS_CONDITIONAL_TRANSIENCE={m['CLASS_CONDITIONAL_TRANSIENCE']}")
    lines.append(f"- self-induction: no-stress barrier prevalence by rung = { {k: round(v,4) for k,v in m['barrier_prevalence_by_rung_no_stress'].items()} }, slope={fmt(m['STATIONARITY_SKILL_NO_STRESS_TREND_slope_per_s'])}/s, CI={[fmt(c) for c in m['STATIONARITY_SKILL_NO_STRESS_TREND_CI95']]}")
    lines.append("")
    lines.append("## Controls and baselines")
    lines.append("")
    for k, v in controls.items():
        lines.append(f"- **{k}**: pass={v['pass']}; expected: {v['expected']}")
    lines.append("")
    lines.append("## Branch decision (frozen rule)")
    lines.append("")
    lines.append(f"decision_rule: MEASUREMENT_INVALID first, then S1 if (INTRINSIC_PERSISTENT AND DENYLIST_INTRINSIC_VALID AND STAT_SIG), else S0.")
    lines.append(f"change evidence classes: {m['change_evidence_classes']}")
    lines.append("")
    lines.append("## Interpretation (bounded)")
    lines.append("")
    if m["branch"] == "S1_STATIONARY":
        lines.append("On this frozen pool/window and one egress vantage the intrinsic access-barrier state is consistent with stationarity at the tested timescales: intrinsic classes persisted, the intrinsic denylist remained valid through the tested horizon, and the anchor barrier indicator carried information beyond the exchangeable constant null. Product reading (bounded): a static intrinsic denylist built at one window remained valid through the measured horizon (>=1800 s, right-censored).")
    elif m["branch"] == "S0_NON_STATIONARY":
        lines.append("On this frozen pool/window the intrinsic access-barrier state is not stationary at the tested timescales under the frozen rule; the positive-evidence class(es) are reported in change_evidence_classes. Product reading (bounded): the endpoint intrinsic access decision is not amortizable through delta_ref here and the dead-end policy should re-observe before relying on a cached decision.")
    else:
        lines.append("The measurement transaction did not complete validly; the failure(s) are prerequisite/control failures, not a scientific negative.")
    lines.append("")
    lines.append("## Validity notes")
    lines.append("")
    for v in validity_notes:
        lines.append(f"- {v}")
    lines.append("")
    lines.append("## Unresolved")
    lines.append("")
    for u in unresolved:
        lines.append(f"- {u}")
    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"Run id `{os.environ.get('GITHUB_RUN_ID')}`; raw evidence under `raw/`; code hashes in `provenance.json`; classifier replay mismatches = {len(mismatches)}.")
    lines.append("")
    (EXP / "report.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
