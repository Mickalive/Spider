"""EXP-PHYSICS-37992957068 EXECUTE orchestrator.

Phases:
  --collect   verify frozen inputs, non-network treatment-liveness trace, live oracles,
              then collect the frozen 57-endpoint universe with the frozen 4 arms.
  --analyze   offline: synthetic controls (PC/NC), LOSO CV skill + clustered bootstrap,
              Q4 separability, scheduler economy, branch decision.
  --synthetic quick dry-run of the synthetic controls only (calibration / smoke test).

Writes raw/*.json(l) during --collect and derived/*.json during --analyze.
Never edits frozen inputs.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import random
import sys
import time
import traceback

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exp_37992957068_lib as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.join(os.path.dirname(HERE), "experiments", L.EXPERIMENT_ID)
RAW_DIR = os.path.join(EXP_DIR, "raw")
DERIVED_DIR = os.path.join(EXP_DIR, "derived")
FREEZE_PATH = os.path.join(EXP_DIR, "freeze.json")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_frozen():
    with open(FREEZE_PATH) as f:
        freeze = json.load(f)
    out = {"declared": freeze["hashes"], "actual": {}, "match": {}}
    ok = True
    for name, declared in freeze["hashes"].items():
        p = os.path.join(EXP_DIR, name)
        actual = sha256_file(p)
        out["actual"][name] = actual
        out["match"][name] = (actual == declared)
        ok = ok and (actual == declared)
    out["all_match"] = ok
    out["freeze_sha256"] = sha256_file(FREEZE_PATH)
    return out


# ---------------------------------------------------------------------------
# Treatment liveness (non-network)
# ---------------------------------------------------------------------------

def policy_trace():
    """Prove A_ADAPT returns a defined action for every intrinsic class and always
    terminates within J_MAX. Non-network; recorded as a measurement prerequisite."""
    trace = []
    for cls in L.ALL_CLASSES:
        action, wait, fresh = L.adapt_action(cls, None)
        trace.append({"input_class": cls, "action": action, "wait_s": wait,
                      "fresh_jar": fresh, "defined": action in ("stop", "retry",
                                                                "retry_once_fresh")})
    # termination: simulate worst-case 429 loop with no CLEAN, honoring J_MAX
    seq = []
    j = 0
    guard = 0
    last_cls = L.CLASS_RATE_LIMIT_429
    while j < L.J_MAX and guard < 20:
        action, wait, fresh = L.adapt_action(last_cls, None)
        seq.append({"j": j, "class": last_cls, "action": action, "wait_s": wait})
        if action.startswith("retry"):
            j += 1
        else:
            break
        guard += 1
    terminates = j >= L.J_MAX or seq[-1]["action"] == "stop"
    return {
        "per_class": trace,
        "worst_case_429_sequence_requests": j,
        "terminates_within_J_max": bool(terminates),
        "all_classes_defined": all(t["defined"] for t in trace),
        "J_MAX": L.J_MAX,
    }


# ---------------------------------------------------------------------------
# Live oracles
# ---------------------------------------------------------------------------

ORACLE_EXPECT = {
    "https://httpbin.org/status/403": {L.CLASS_BLOCK_403_CHALLENGE, L.CLASS_UNAVAILABLE_403},
    "https://httpbin.org/status/429": {L.CLASS_RATE_LIMIT_429},
    "https://no-such-host.invalid/": {L.CLASS_TRANSPORT_ERROR},
    "https://httpbin.org/status/200": {L.CLASS_CLEAN},
    "https://httpbin.org/uuid": {L.CLASS_CLEAN},
}
ORACLE_GROUP = {
    "https://httpbin.org/status/403": "PC_BARRIER_ORACLE",
    "https://httpbin.org/status/429": "PC_BARRIER_ORACLE",
    "https://no-such-host.invalid/": "PC_BARRIER_ORACLE",
    "https://httpbin.org/status/200": "NC_CLEAN_ORACLE",
    "https://httpbin.org/uuid": "NC_CLEAN_ORACLE",
}


def run_oracles():
    out = []
    opener = L._new_opener()
    for url, expected in ORACLE_EXPECT.items():
        for k in range(2):
            status, headers, body, error, elapsed_ms = L._fetch(opener, url, L.HTTP_TIMEOUT_S)
            marker = L.body_marker_matched(body)
            cls = L.classify(status, error, headers.get("cf-mitigated"), marker)
            out.append({
                "group": ORACLE_GROUP[url],
                "url": url,
                "expected": sorted(expected),
                "observed": cls,
                "status": status,
                "error": error,
                "passed": cls in expected,
            })
    return out


# ---------------------------------------------------------------------------
# Arm assignment (frozen block randomization)
# ---------------------------------------------------------------------------

def arm_assignment():
    rng = random.Random(L.SEED_ASSIGNMENT)
    assignment = {}
    for ep in L.ENDPOINTS:
        arms = (["A_RETRY"] * 3 + ["A_RETRY_SPACED"] * 3
                + ["A_FRESH"] * 3 + ["A_ADAPT"] * 3)
        rng.shuffle(arms)
        assignment[ep] = arms
    return assignment


def collect():
    os.makedirs(RAW_DIR, exist_ok=True)
    meta = {"experiment_id": L.EXPERIMENT_ID, "verify_frozen": verify_frozen()}
    with open(os.path.join(RAW_DIR, "frozen_verify.json"), "w") as f:
        json.dump(meta["verify_frozen"], f, indent=2)

    meta["policy_trace"] = policy_trace()
    with open(os.path.join(RAW_DIR, "policy_trace.json"), "w") as f:
        json.dump(meta["policy_trace"], f, indent=2)

    meta["oracles"] = run_oracles()
    with open(os.path.join(RAW_DIR, "oracles.json"), "w") as f:
        json.dump(meta["oracles"], f, indent=2)
    meta["oracles_all_pass"] = all(o["passed"] for o in meta["oracles"])

    assignment = arm_assignment()
    with open(os.path.join(RAW_DIR, "arm_assignment.json"), "w") as f:
        json.dump(assignment, f, indent=2)

    t_start = time.time()
    all_records = []
    endpoint_records = {}

    def do_endpoint(ep):
        recs = []
        for si, arm in enumerate(assignment[ep]):
            recs.extend(L.run_episode(ep, arm, si))
        return ep, recs

    max_workers = int(os.environ.get("SPIDER_PHYS_WORKERS", "8"))
    with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(do_endpoint, ep): ep for ep in L.ENDPOINTS}
        for fut in cf.as_completed(futs):
            ep = futs[fut]
            try:
                ep_name, recs = fut.result()
                endpoint_records[ep_name] = recs
            except Exception as e:
                endpoint_records[ep] = {"__error__": f"{type(e).__name__}: {e}"}
                print(f"[collect] endpoint failed {ep}: {e}", file=sys.stderr)
    for ep in L.ENDPOINTS:
        recs = endpoint_records.get(ep, [])
        if isinstance(recs, dict):
            continue
        all_records.extend(recs)

    with open(os.path.join(RAW_DIR, "collection.jsonl"), "w") as f:
        for r in all_records:
            f.write(json.dumps(r, sort_keys=True) + "\n")

    status_hist = {}
    class_hist = {}
    for r in all_records:
        status_hist[str(r["status"])] = status_hist.get(str(r["status"]), 0) + 1
        class_hist[r["intrinsic_class"]] = class_hist.get(r["intrinsic_class"], 0) + 1
    meta["n_planned_gets"] = len(L.ENDPOINTS) * L.SESSIONS_PER_ENDPOINT * L.J_MAX
    meta["n_requests"] = len(all_records)
    meta["status_histogram"] = status_hist
    meta["class_histogram"] = class_hist
    meta["wall_clock_s"] = round(time.time() - t_start, 1)
    meta["max_workers"] = max_workers
    with open(os.path.join(RAW_DIR, "collection_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[collect] {len(all_records)} requests, wall {meta['wall_clock_s']}s")
    print(f"[collect] class histogram {class_hist}")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def build_rows(records):
    ep_idx = {e: i for i, e in enumerate(L.ENDPOINTS)}
    by_session = {}
    for r in records:
        by_session.setdefault((r["endpoint"], r["session_idx"]), []).append(r)
    rows = []
    for (ep, si), recs in by_session.items():
        recs = sorted(recs, key=lambda r: r["j"])
        for t, cur in enumerate(recs):
            f = L._row_features(recs[:t], cur, ep_idx[ep], len(L.ENDPOINTS))
            f["y"] = 1 if L.is_barrier(cur["intrinsic_class"]) else 0
            f["intrinsic_class"] = cur["intrinsic_class"]
            f["prev_class"] = recs[t - 1]["intrinsic_class"] if t > 0 else None
            f["session"] = L.session_id(ep, si)
            f["domain"] = cur["domain"]
            f["endpoint"] = ep
            rows.append(f)
    return rows


def build_episodes(records):
    by_session = {}
    for r in records:
        by_session.setdefault((r["endpoint"], r["session_idx"]), []).append(r)
    episodes = []
    for (ep, si), recs in by_session.items():
        recs = sorted(recs, key=lambda r: r["j"])
        m = L.episode_metrics(recs)
        m.update({"endpoint": ep, "domain": recs[0]["domain"],
                  "arm": recs[0]["arm"], "session_idx": si})
        episodes.append(m)
    return episodes


def analyze():
    os.makedirs(DERIVED_DIR, exist_ok=True)
    with open(os.path.join(RAW_DIR, "collection.jsonl")) as f:
        records = [json.loads(line) for line in f if line.strip()]
    with open(os.path.join(RAW_DIR, "collection_meta.json")) as f:
        meta = json.load(f)
    with open(os.path.join(RAW_DIR, "oracles.json")) as f:
        oracles = json.load(f)

    rows = build_rows(records)
    episodes = build_episodes(records)
    n_endpoints = len(L.ENDPOINTS)

    # ---- primary + secondary prediction metrics ----
    core = L.run_analysis_core(rows, n_endpoints, n_resamples_ci=L.BOOTSTRAP_N,
                               seed=L.SEED_BOOTSTRAP)
    # endpoint-identity ablation named in spec.stable_identifiers.models (reported diagnostic)
    core_noid = L.run_analysis_core(rows, n_endpoints, n_resamples_ci=L.BOOTSTRAP_N,
                                    seed=L.SEED_BOOTSTRAP, feature_names=L.M_NOID_FEATURES)
    onset_idx = [i for i, r in enumerate(rows)
                 if r["prev_class"] == L.CLASS_CLEAN and L.is_barrier(r["intrinsic_class"])]
    recovery_idx = [i for i, r in enumerate(rows)
                    if r["prev_class"] in L.BARRIER_SET and r["intrinsic_class"] == L.CLASS_CLEAN]
    # transition skill: recompute predictions restricted to event rows
    trans = _transition_skills(rows, n_endpoints, onset_idx, recovery_idx)

    sep = L.separability_skill(rows, n_endpoints, n_resamples_ci=L.BOOTSTRAP_N,
                               seed=L.SEED_BOOTSTRAP)

    # ---- scheduler stratum ----
    barrier_endpoints = sorted({r["endpoint"] for r in records
                                if L.is_barrier(r["intrinsic_class"])})
    scheduler = L.scheduler_economy(episodes, barrier_endpoints,
                                    n_resamples_ci=L.BOOTSTRAP_N, seed=L.SEED_BOOTSTRAP)
    full_pool_sched = L.scheduler_economy(episodes, L.ENDPOINTS,
                                          n_resamples_ci=1000, seed=L.SEED_BOOTSTRAP)

    # ---- measurement-invalid conditions ----
    invalid = {}
    invalid["network_unreachable"] = (meta["n_requests"] == 0
                                      or meta["class_histogram"].get(L.CLASS_TRANSPORT_ERROR, 0)
                                      / max(meta["n_requests"], 1) > 0.80)
    invalid["pc_barrier_oracle_misclassified"] = any(
        (not o["passed"]) for o in oracles if o["group"] == "PC_BARRIER_ORACLE")
    invalid["nc_clean_oracle_misclassified"] = any(
        (not o["passed"]) for o in oracles if o["group"] == "NC_CLEAN_ORACLE")
    invalid["fewer_than_3_barrier_exposed_endpoints"] = len(barrier_endpoints) < L.MIN_BARRIER_EXPOSED_ENDPOINTS
    invalid["fewer_than_30_scheduler_barrier_events"] = scheduler["n_stratum_barrier_events"] < L.MIN_SCHEDULER_BARRIER_EVENTS

    # ---- synthetic controls ----
    pc = _synthetic_pc()
    nc = _synthetic_nc()
    invalid["pc_synthetic_power_below_0_80"] = pc["power"] < L.PC_POWER_MIN
    invalid["nc_synthetic_false_positive_above_0_05"] = nc["false_positive_rate"] > L.NC_FP_MAX
    # classifier reproducibility: re-derive the intrinsic class from the stored raw
    # fields (status, error, cf_mitigated, challenge_marker_matched) for EVERY record.
    nonrepro = 0
    nonrepro_examples = []
    for r in records:
        back = L.classify(r["status"], r["error"], r["cf_mitigated"],
                          r.get("challenge_marker_matched"))
        if back != r["intrinsic_class"]:
            nonrepro += 1
            if len(nonrepro_examples) < 5:
                nonrepro_examples.append({"endpoint": r["endpoint"], "j": r["j"],
                                          "stored": r["intrinsic_class"], "recomputed": back})
    invalid["classifier_not_reproducible"] = nonrepro > 0
    meta["classifier_recomputation_mismatches"] = nonrepro
    meta["classifier_recomputation_examples"] = nonrepro_examples

    metrics = {
        "SKILL_LL": core["SKILL_LL"],
        "SKILL_LL_CI95": [core["LO"], core["HI"]],
        "SKILL_LL_NOID": core_noid["SKILL_LL"],
        "SKILL_LL_NOID_CI95": [core_noid["LO"], core_noid["HI"]],
        "SKILL_BA": core["SKILL_BA"],
        "logloss": core["logloss"],
        "balanced_accuracy": core["balanced_accuracy"],
        "n_rows_primary": core["n_rows"],
        "ONSET_SKILL_LL": trans["ONSET"]["skill"],
        "ONSET_CI95": [trans["ONSET"]["lo"], trans["ONSET"]["hi"]],
        "ONSET_n": len(onset_idx),
        "RECOVERY_SKILL_LL": trans["RECOVERY"]["skill"],
        "RECOVERY_CI95": [trans["RECOVERY"]["lo"], trans["RECOVERY"]["hi"]],
        "RECOVERY_n": len(recovery_idx),
        "SEPARABILITY_SKILL_LL": sep.get("SKILL_LL"),
        "SEPARABILITY_CI95": [sep.get("LO"), sep.get("HI")],
        "SEPARABILITY_n": sep.get("n_rows"),
        "d_Req": scheduler["d_Req"],
        "d_Req_CI95": [scheduler["d_Req_ci_lo"], scheduler["d_Req_ci_hi"]],
        "d_Succ": scheduler["d_Succ"],
        "ADAPT_abs_requests": scheduler["ADAPT_abs_requests"],
        "RETRY_abs_requests": scheduler["RETRY_abs_requests"],
        "ADAPT_success": scheduler["ADAPT_success"],
        "RETRY_success": scheduler["RETRY_success"],
        "endpoint_no_barrier_success": scheduler["endpoint_no_barrier_success"],
        "n_barrier_exposed_endpoints": len(barrier_endpoints),
        "n_scheduler_barrier_events": scheduler["n_stratum_barrier_events"],
        "n_sessions": len(episodes),
        "n_requests": meta["n_requests"],
        "class_histogram": meta["class_histogram"],
        "status_histogram": meta["status_histogram"],
    }

    branch = L.decide_branch(
        core["SKILL_LL"], core["LO"], core["HI"],
        scheduler["d_Req"], scheduler["d_Req_ci_hi"] if scheduler["d_Req_ci_hi"] is not None else 1.0,
        scheduler["d_Succ"], scheduler["ADAPT_success"], scheduler["endpoint_no_barrier_success"],
    )

    controls = {
        "PC_SYNTHETIC_DYNAMICS": pc,
        "NC_SYNTHETIC_MEMORYLESS": nc,
        "PC_BARRIER_ORACLE": {
            "requests": [o for o in oracles if o["group"] == "PC_BARRIER_ORACLE"],
            "pass": not invalid["pc_barrier_oracle_misclassified"],
        },
        "NC_CLEAN_ORACLE": {
            "requests": [o for o in oracles if o["group"] == "NC_CLEAN_ORACLE"],
            "pass": not invalid["nc_clean_oracle_misclassified"],
        },
    }

    measurement_invalid = any(invalid[k] for k in invalid if k != "classifier_not_reproducible")
    # classifier reproducibility flag handled explicitly
    if invalid["classifier_not_reproducible"]:
        measurement_invalid = True

    derived = {
        "experiment_id": L.EXPERIMENT_ID,
        "metrics": metrics,
        "core": core,
        "core_noid": core_noid,
        "controls": controls,
        "branch": branch,
        "measurement_invalid_conditions": invalid,
        "measurement_invalid": bool(measurement_invalid),
        "barrier_exposed_endpoints": barrier_endpoints,
        "scheduler_stratum": scheduler,
        "full_pool_scheduler": full_pool_sched,
        "transition_detail": trans,
        "separability_detail": sep,
        "collection_meta": meta,
    }
    with open(os.path.join(DERIVED_DIR, "metrics.json"), "w") as f:
        json.dump(derived, f, indent=2)
    print("[analyze] SKILL_LL", core["SKILL_LL"], "CI", [core["LO"], core["HI"]])
    print("[analyze] d_Req", scheduler["d_Req"], "d_Succ", scheduler["d_Succ"])
    print("[analyze] branch", branch["branch"], "invalid", measurement_invalid)
    return derived


def _transition_skills(rows, n_endpoints, onset_idx, recovery_idx):
    y = np.array([r["y"] for r in rows], dtype=float)
    X, _ = L.build_design(L.M_HISTORY_FEATURES, rows, n_endpoints)
    sessions = sorted({r["session"] for r in rows})
    s2i = {}
    for i, r in enumerate(rows):
        s2i.setdefault(r["session"], []).append(i)
    pred = L._loso_by_session(rows, X, y, sessions, s2i)
    # rate-only + nulls
    Xr, _ = L.build_design(L.RATE_ONLY_FEATURES, rows, 1)
    pred_rate = L._loso_by_session(rows, Xr, y, sessions, s2i)
    nulls = {"B_RATE_ONLY": pred_rate}
    for kind in ("B_CONSTANT", "B_ENDPOINT_CONST", "B_MEMORY_PERSIST"):
        p = [None] * len(rows)
        for s in sessions:
            te = s2i[s]
            tr = [i for i in range(len(rows)) if i not in set(te)]
            trr = [rows[i] for i in tr]
            ter = [rows[i] for i in te]
            if kind == "B_CONSTANT":
                pp = L.predict_constant(trr, ter)
            elif kind == "B_ENDPOINT_CONST":
                pp = L.predict_endpoint_const(trr, ter)
            else:
                pp = L.predict_memory_persist(trr, ter)
            for k, i in enumerate(te):
                p[i] = pp[k]
        nulls[kind] = p
    out = {}
    for name, idx in (("ONSET", onset_idx), ("RECOVERY", recovery_idx)):
        if not idx:
            out[name] = {"skill": None, "lo": None, "hi": None, "n": 0,
                         "note": "no events of this class in the run"}
            continue
        sk, lo, hi, _ = L.skill_and_ci(rows, pred, nulls,
                                       [r["domain"] for r in rows], restricted_idx=idx,
                                       n_resamples=min(2000, L.BOOTSTRAP_N),
                                       seed=L.SEED_BOOTSTRAP)
        out[name] = {"skill": sk, "lo": lo, "hi": hi, "n": len(idx)}
    return out


def _synthetic_pc():
    R = 200
    n_ep = L.SYNTH_ENDPOINTS
    hits = 0
    skills = []
    los = []
    for r in range(R):
        rng = random.Random(L.SEED_PC_SYNTHETIC + r)
        seqs = L.gen_pc_sequences(rng, L.SYNTH_SEQUENCES, L.SYNTH_SEQ_LEN, n_ep)
        res = L.run_synthetic_control(seqs, n_ep, n_resamples_ci=500, seed=L.SEED_BOOTSTRAP)
        skills.append(res["SKILL_LL"])
        los.append(res["LO"])
        if res["LO"] > 0:
            hits += 1
    return {"replications": R, "power": hits / R, "hits": hits,
            "mean_SKILL_LL": sum(skills) / len(skills),
            "min_SKILL_LL": min(skills), "max_SKILL_LL": max(skills),
            "min_CI_lower": min(los), "gate": L.PC_POWER_MIN,
            "pass": (hits / R) >= L.PC_POWER_MIN,
            "plant": {"a": L.PC_PLANT_A, "b": L.PC_PLANT_B, "c": L.PC_PLANT_C},
            "synthetic_endpoints": n_ep}


def _synthetic_nc():
    R = 200
    n_ep = L.SYNTH_ENDPOINTS
    hits = 0
    skills = []
    los = []
    for r in range(R):
        rng = random.Random(L.SEED_NC_SYNTHETIC + r)
        seqs = L.gen_nc_sequences(rng, L.SYNTH_SEQUENCES, L.SYNTH_SEQ_LEN, n_ep)
        res = L.run_synthetic_control(seqs, n_ep, n_resamples_ci=500, seed=L.SEED_BOOTSTRAP)
        skills.append(res["SKILL_LL"])
        los.append(res["LO"])
        if res["LO"] > 0:
            hits += 1
    return {"replications": R, "false_positive_rate": hits / R, "hits": hits,
            "mean_SKILL_LL": sum(skills) / len(skills),
            "min_SKILL_LL": min(skills), "max_SKILL_LL": max(skills),
            "max_CI_lower": max(los), "gate": L.NC_FP_MAX,
            "pass": (hits / R) <= L.NC_FP_MAX,
            "synthetic_endpoints": n_ep}


def synthetic_smoke():
    rng = random.Random(L.SEED_PC_SYNTHETIC)
    seqs = L.gen_pc_sequences(rng, 114, 6, 57)
    pc = L.run_synthetic_control(seqs, 57, n_resamples_ci=300, seed=L.SEED_BOOTSTRAP)
    rng2 = random.Random(L.SEED_NC_SYNTHETIC)
    seqs2 = L.gen_nc_sequences(rng2, 114, 6, 57)
    nc = L.run_synthetic_control(seqs2, 57, n_resamples_ci=300, seed=L.SEED_BOOTSTRAP)
    print("PC SKILL_LL", pc["SKILL_LL"], "CI", [pc["LO"], pc["HI"]])
    print("NC SKILL_LL", nc["SKILL_LL"], "CI", [nc["LO"], nc["HI"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--synthetic", action="store_true")
    args = ap.parse_args()
    if args.synthetic:
        synthetic_smoke()
        return
    if args.collect:
        collect()
    if args.analyze:
        analyze()
    if not (args.collect or args.analyze):
        ap.error("choose --collect, --analyze or --synthetic")


if __name__ == "__main__":
    main()
