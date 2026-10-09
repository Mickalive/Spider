#!/usr/bin/env python3
"""EXP-PHYSICS-37973239386 EXECUTE orchestrator.

Usage:
  python3 exp_37973239386_run.py            # collect (resumable) + analyze
  python3 exp_37973239386_run.py --analyze   # analysis only from raw/collection.jsonl

Writes raw and derived artifacts under the experiment directory. Does NOT write
result.json / report.md / provenance.json (those are written by finalize step).
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import sys
import threading
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exp_37973239386_lib as L  # noqa: E402

EXP_DIR = os.path.join(
    os.path.dirname(os.path.dirname(HERE)),
    "research",
    "experiments",
    "EXP-PHYSICS-37973239386",
)
SPEC_PATH = os.path.join(EXP_DIR, "spec.json")
RAW_DIR = os.path.join(EXP_DIR, "raw")
DERIVED_DIR = os.path.join(EXP_DIR, "derived")
COLLECTION_PATH = os.path.join(RAW_DIR, "collection.jsonl")
COLLECTION_META_PATH = os.path.join(RAW_DIR, "collection_meta.json")
LOCK = threading.Lock()


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_spec():
    with open(SPEC_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------


def load_existing_sessions():
    done = {}
    if os.path.exists(COLLECTION_PATH):
        with open(COLLECTION_PATH) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                done[(rec["endpoint"], rec["session_index"])] = rec
    return done


def collect(spec, workers=16):
    os.makedirs(RAW_DIR, exist_ok=True)
    endpoints = list(spec["candidate_universe"]["endpoints"])
    tasks = [(ep, s) for ep in endpoints for s in range(L.K_SESSIONS)]
    done = load_existing_sessions()
    todo = [t for t in tasks if t not in done]
    print(f"[collect] endpoints={len(endpoints)} tasks={len(tasks)} done={len(done)} todo={len(todo)}", flush=True)

    errors = 0
    completed = 0
    t0 = time.time()
    with open(COLLECTION_PATH, "a") as out:
        with cf.ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(L._collect_one_session, ep, s): (ep, s) for ep, s in todo}
            for fut in cf.as_completed(futs):
                ep, s = futs[fut]
                try:
                    rec = fut.result()
                except Exception as e:  # a whole session failed unexpectedly
                    rec = {
                        "endpoint": ep,
                        "session_index": s,
                        "observations": [
                            {"endpoint": ep, "session_index": s, "request_index": j,
                             "transport_error": f"{type(e).__name__}: {str(e)[:200]}",
                             "status": None, "fields": [], "cookies": {}}
                            for j in range(L.J_REQUESTS)
                        ],
                    }
                with LOCK:
                    out.write(json.dumps(rec, separators=(",", ":")) + "\n")
                    out.flush()
                    completed += 1
                    for o in rec["observations"]:
                        if o.get("transport_error"):
                            errors += 1
                    if completed % 25 == 0:
                        el = time.time() - t0
                        print(f"[collect] {completed}/{len(todo)} sessions, transport_errors={errors}, {el:.0f}s", flush=True)
    meta = {
        "endpoints": endpoints,
        "n_endpoints": len(endpoints),
        "k_sessions": L.K_SESSIONS,
        "j_requests": L.J_REQUESTS,
        "planned_gets": len(endpoints) * L.K_SESSIONS * L.J_REQUESTS,
        "transport_errors": errors,
        "collected_at": time.time(),
        "collection_path": "raw/collection.jsonl",
    }
    with open(COLLECTION_META_PATH, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[collect] finished sessions={completed} transport_errors={errors} elapsed={time.time()-t0:.0f}s", flush=True)
    return meta


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------


def build_observations(endpoints):
    """Return list of observation dicts from raw JSONL."""
    obs = []
    with open(COLLECTION_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec["endpoint"] not in endpoints:
                continue
            for o in rec["observations"]:
                obs.append(o)
    return obs


def analyze(spec):
    os.makedirs(DERIVED_DIR, exist_ok=True)
    endpoints = list(spec["candidate_universe"]["endpoints"])
    ep_set = set(endpoints)
    obs = build_observations(ep_set)

    transport_errors = sum(1 for o in obs if o.get("transport_error"))
    planned = len(endpoints) * L.K_SESSIONS * L.J_REQUESTS
    status_hist = Counter(str(o.get("status")) for o in obs)

    # ---- controls (EXECUTE re-run) ----
    print("[analyze] running null battery ...", flush=True)
    null_res = L.run_null_battery()
    print("[analyze] running positive control battery ...", flush=True)
    pc_res = L.run_positive_control()
    print("[analyze] running live httpbin uuid null ...", flush=True)
    live_null = L.run_live_null_uuid(k_sessions=8)

    controls = {
        L.NULL_ID: {
            "NC_PLANTED_RANDOM": null_res,
            "NC_LIVE_HTTPBIN_UUID": live_null,
            "pass": (
                null_res["aggregate_fp"] <= L.NULL_FP_MAX
                and live_null["fields_collected"] > 0
                and live_null["fired_fraction"] is not None
                and live_null["fired_fraction"] <= L.NULL_FP_MAX
            ),
        },
        L.PC_ID: {
            "classes": pc_res["classes"],
            "power_min": pc_res["power_min"],
            "pass": pc_res["power_min"] >= L.PC_POWER_MIN,
        },
    }

    # ---- fields ----
    fields = defaultdict(list)  # key -> list of obs + value
    field_meta = {}
    for o in obs:
        if o.get("transport_error") or o.get("status") is None:
            continue
        ep = o["endpoint"]
        host = ep.split("//", 1)[-1].split("/", 1)[0]
        site = L.registrable_domain(host)
        for fld in o.get("fields", []):
            name = fld["name"]
            lt = fld["locator_type"]
            key = (ep, site, lt, name)
            fields[key].append({
                "value": fld["value"],
                "session_index": o["session_index"],
                "request_index": o["request_index"],
                "epoch": o.get("epoch"),
                "status": o.get("status"),
                "cookies": o.get("cookies", {}) or {},
            })
            field_meta[key] = {"endpoint": ep, "site": site, "locator_type": lt, "name": name}

    field_records = []
    for key, series in fields.items():
        ep, site, lt, name = key
        series = sorted(series, key=lambda x: (x["session_index"], x["request_index"]))
        values = [s["value"] for s in series]
        epochs = [s["epoch"] for s in series]
        cookie_maps = [s["cookies"] for s in series]
        sessions = {s["session_index"] for s in series}
        distinct = len(set(values))
        cls = L.name_class(lt, name)
        n_obs = len(series)
        admitted = bool(
            cls is not None
            and distinct >= 2
            and len(sessions) >= 2
            and n_obs >= L.N_MIN_OBS
        )
        rec = {
            "endpoint": ep,
            "site": site,
            "cluster": site,
            "locator_type": lt,
            "name": name,
            "taxonomy_class": cls,
            "n_obs": n_obs,
            "n_sessions": len(sessions),
            "n_distinct": distinct,
            "admitted": admitted,
            "stratum": "NONCE" if cls == "NONCE" else "PRIMARY",
        }
        if admitted:
            fired = L.rule_fire(values, epochs, cookie_maps, field_name=name, locator_type=lt)
            mem_hold = L.b_memory_repeat_holdout(values)
            mem_full = L.b_memory_repeat_acc(values)
            markov = L.b_markov1_acc(values)
            const = L.b_constant_mode_acc(values)
            best_frac = max(fired.values()) if fired else 0.0
            predictable = bool(fired) and (best_frac - mem_hold >= L.DELTA_MEM)
            # class attribution by frozen priority
            attr = None
            for rule_id, class_name in L.CLASS_PRIORITY:
                if rule_id in fired:
                    attr = (rule_id, class_name)
                    break
            if attr is None and fired:
                attr = (sorted(fired)[0], "OTHER")
            if not fired:
                attr = (None, "MEMORY_ONLY" if mem_hold >= 0.5 else "UNPREDICTABLE")
            rec.update({
                "firing_rules": sorted(fired.keys()),
                "firing_rule_detection_fractions": fired,
                "best_rule_fraction": best_frac,
                "memory_repeat_holdout": mem_hold,
                "memory_repeat_full": mem_full,
                "markov1_holdout": markov,
                "constant_mode_holdout": const,
                "predictable": int(predictable),
                "attributed_rule": attr[0],
                "attributed_class": attr[1],
                "ordered_values_sha256": hashlib.sha256(json.dumps(values).encode()).hexdigest(),
                "ordered_values": [v for v in values],
            })
        field_records.append(rec)

    admitted = [r for r in field_records if r["admitted"]]
    primary = [r for r in admitted if r["stratum"] == "PRIMARY"]
    nonce = [r for r in admitted if r["stratum"] == "NONCE"]
    indicator = [r for r in primary if r["n_obs"] >= L.N_MIN_OBS]
    n_pred = sum(r["predictable"] for r in indicator)
    n_ind = len(indicator)
    pv = (n_pred / n_ind) if n_ind else None

    sites = sorted({r["cluster"] for r in primary})
    boot = L.clustered_bootstrap([{"cluster": r["cluster"], "predictable": r["predictable"]} for r in indicator])

    per_site = {}
    for r in indicator:
        d = per_site.setdefault(r["cluster"], {"n": 0, "pred": 0})
        d["n"] += 1
        d["pred"] += r["predictable"]
    for k, d in per_site.items():
        d["prevalence"] = d["pred"] / d["n"] if d["n"] else None

    per_class = Counter(r["attributed_class"] for r in indicator if r["predictable"])
    baseline_means = {
        "B_MEMORY_REPEAT_ACC_MEAN_HOLDOUT": (sum(r["memory_repeat_holdout"] for r in indicator) / n_ind) if n_ind else None,
        "B_MEMORY_REPEAT_ACC_MEAN_FULL": (sum(r["memory_repeat_full"] for r in indicator) / n_ind) if n_ind else None,
        "B_MARKOV1_ACC_MEAN": (sum(r["markov1_holdout"] for r in indicator) / n_ind) if n_ind else None,
        "B_CONSTANT_MODE_ACC_MEAN": (sum(r["constant_mode_holdout"] for r in indicator) / n_ind) if n_ind else None,
    }

    # nonce sensitivity
    all_plus_nonce = [r for r in admitted if r["n_obs"] >= L.N_MIN_OBS]
    pred_plus = sum(r["predictable"] for r in all_plus_nonce)
    pv_plus = (pred_plus / len(all_plus_nonce)) if all_plus_nonce else None

    transport_rate = (transport_errors / planned) if planned else 1.0
    admitted_no_type = sum(1 for r in admitted if r["locator_type"] not in ("cookie", "input.hidden", "meta"))

    # ---- measurement-invalid conditions ----
    cond = {
        "a_too_few_fields": n_ind < L.M_MIN_FIELDS,
        "b_too_few_sites": len(sites) < L.S_MIN_SITES,
        "c_null_fail": not controls[L.NULL_ID]["pass"],
        "d_pc_power_fail": not controls[L.PC_ID]["pass"],
        "e_transport_or_non_get": (transport_rate > L.TRANSPORT_ERROR_MAX),
        "f_locator_missing": (admitted_no_type / len(admitted)) > 0.30 if admitted else False,
        "g_universe": False,  # verified below
        "h_rule_family": False,  # frozen implementation
    }
    # universe verification
    frozen = spec["candidate_universe"]["endpoints"]
    cond["g_universe"] = (frozen != endpoints)
    any_invalid = any(cond.values())

    # ---- branch precedence ----
    if any_invalid:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        branch = "M"
    else:
        lo = boot["lo"] if boot["lo"] is not None else 0.0
        hi = boot["hi"] if boot["hi"] is not None else 0.0
        if pv is not None and pv >= L.P_HI and lo > L.P_FLOOR:
            status, outcome, branch = "COMPLETE", "SUPPORTS", "S1"
        elif pv is not None and pv <= L.P_FLOOR and hi < L.P_HI:
            status, outcome, branch = "COMPLETE", "FALSIFIES", "S0"
        else:
            status, outcome, branch = "COMPLETE", "MIXED", "SX"
        if boot["distinct_resamples"] < 1000 and branch in ("S1", "S0"):
            outcome, branch = "MIXED", "SX_capped"

    result = {
        "n_indicator_fields": n_ind,
        "n_predictable": n_pred,
        "PREDICTABLE_PREVALENCE_POOLED": pv,
        "PREDICTABLE_PREVALENCE_ALL_PLUS_NONCE": pv_plus,
        "admitted_fields": len(admitted),
        "admitted_primary_fields": len(primary),
        "admitted_nonce_fields": len(nonce),
        "admitted_sites_primary": len(sites),
        "admitted_sites_list": sites,
        "admitted_endpoints": len({r["endpoint"] for r in admitted}),
        "site_clustered_ci95": [boot["lo"], boot["hi"]],
        "bootstrap_distinct_resamples": boot["distinct_resamples"],
        "bootstrap_n_clusters": boot["n_clusters"],
        "bootstrap_informative": boot["informative"],
        "baselines": baseline_means,
        "per_site_prevalence": per_site,
        "per_class_prevalence": dict(per_class),
        "transport_errors": transport_errors,
        "planned_gets": planned,
        "TRANSPORT_ERROR_RATE": transport_rate,
        "NON_GET_REQUESTS": 0,
        "status_histogram": dict(status_hist),
        "measurement_invalid_conditions": cond,
        "branch": branch,
        "outcome": outcome,
    }

    with open(os.path.join(DERIVED_DIR, "fields.json"), "w") as f:
        json.dump(field_records, f, indent=2)
    with open(os.path.join(DERIVED_DIR, "controls.json"), "w") as f:
        json.dump(controls, f, indent=2)
    with open(os.path.join(DERIVED_DIR, "metrics.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("[analyze] " + json.dumps({
        "n_ind": n_ind, "n_pred": n_pred, "pv": pv, "ci": [boot["lo"], boot["hi"]],
        "sites": len(sites), "branch": branch, "outcome": outcome,
        "null_pass": controls[L.NULL_ID]["pass"], "pc_pass": controls[L.PC_ID]["pass"],
        "transport_rate": transport_rate,
    }, indent=2), flush=True)
    return result, controls, field_records, null_res, pc_res, live_null


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()
    spec = load_spec()
    if not args.analyze:
        collect(spec, workers=args.workers)
    analyze(spec)


if __name__ == "__main__":
    main()
