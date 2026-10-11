"""EXP-PHYSICS-38074818597 EXECUTE collection runner (Python 3.12 stdlib only).

Executes the frozen sweep protocol live:
  1. live oracle controls (PC_ORACLE_BARRIER, NC_CLEAN_ORACLE);
  2. ambient ladder sweeps anchored at T0 with nominal revisits +300/+900/+1800 s;
  3. the induced-transience probe on stratum_stress after the 1800 s rung.

Writes RAW EVIDENCE only:
  research/experiments/EXP-PHYSICS-38074818597/raw/oracles.jsonl
  research/experiments/EXP-PHYSICS-38074818597/raw/ambient_collection.jsonl
  research/experiments/EXP-PHYSICS-38074818597/raw/induced_probe.json
  research/experiments/EXP-PHYSICS-38074818597/raw/collection_meta.json

No interpretation is written here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
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


def log(msg):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", flush=True)


def verify_freeze():
    freeze = json.loads((EXP / "freeze.json").read_text())
    bad = []
    for name, expected in freeze["hashes"].items():
        got = hashlib.sha256((EXP / name).read_bytes()).hexdigest()
        if got != expected:
            bad.append((name, got, expected))
    if bad:
        raise SystemExit(f"FROZEN FILE HASH MISMATCH: {bad}")
    for rel, expected in freeze.get("artifact_hashes", {}).items():
        p = ROOT / rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            raise SystemExit(f"FROZEN ARTIFACT MISMATCH: {rel}")
    log("freeze integrity OK")


def run_oracles(spec, opener):
    pc = spec["positive_control"]["PC_ORACLE_BARRIER"]
    nc = spec["null_control"]["NC_CLEAN_ORACLE"]
    per = int(pc["literal_design_values"]["per_host_requests"])
    expected = {
        "https://httpbin.org/status/429": "RATE_LIMIT_429",
        "https://httpbingo.org/status/429": "RATE_LIMIT_429",
        "https://no-such-host.invalid/": "TRANSPORT_ERROR",
        "https://httpbin.org/status/403": "UNAVAILABLE_403",
        "https://httpbin.org/status/200": "CLEAN",
        "https://httpbin.org/uuid": "CLEAN",
        "https://example.com/": "CLEAN",
    }
    rows = []
    for host in pc["literal_design_values"]["hosts"] + nc["literal_design_values"]["hosts"]:
        for k in range(per):
            rec = L.fetch(opener, host)
            rec["oracle"] = "PC_ORACLE_BARRIER" if host in pc["literal_design_values"]["hosts"] else "NC_CLEAN_ORACLE"
            rec["oracle_rep"] = k
            rec["expected_class"] = expected.get(host)
            rec["oracle_ok"] = (rec["class"] == expected.get(host))
            rows.append(rec)
            log(f"oracle {host} rep{k} -> {rec['class']} (expected {expected.get(host)}) err={rec['error']}")
    L.append_jsonl(EXP / "raw/oracles.jsonl", rows)
    return rows


def run_ambient(spec, seed):
    endpoints = spec["frozen_universe"]["endpoints"]
    offsets = spec["sweep_protocol"]["sweep_target_offsets_s"]
    gap = 0.30
    rows = []
    rung_starts = {}
    t0 = None
    for si, off in enumerate(offsets):
        if si == 0:
            t0 = time.time()
        target = t0 + off
        target = t0 + off
        while True:
            now = time.time()
            if target <= now:
                break
            log(f"waiting {target-now:.1f}s until nominal rung +{off}s")
            time.sleep(min(20.0, target - now))
        rung_start = time.time()
        rung_starts[si] = rung_start
        rng = random.Random(seed + si)
        order = rng.sample(range(len(endpoints)), len(endpoints))
        log(f"=== sweep {si} rung +{off}s start (actual +{rung_start-t0:.1f}s) ===")
        last_log = time.time()
        for pos, idx in enumerate(order):
            url = endpoints[idx]
            opener = L.build_opener()  # fresh cookie jar per observation
            rec = L.fetch(opener, url)
            rec.update({
                "sweep_index": si,
                "nominal_rung_s": off,
                "order_pos": pos,
                "endpoint_index": idx,
                "actual_offset_s": rec["t_start"] - t0,
            })
            rows.append(rec)
            now = time.time()
            if pos % 10 == 0 or rec["class"] not in ("CLEAN",) or (now - last_log) > 15:
                log(f"  sweep{si} [{pos+1}/{len(order)}] {url} -> {rec['class']} ({rec['elapsed_ms']:.0f}ms)")
                last_log = now
            L.append_jsonl(EXP / "raw/ambient_collection.jsonl", [rec])
            if pos < len(order) - 1:
                time.sleep(gap)
        log(f"=== sweep {si} done at +{time.time()-t0:.1f}s ===")
    return rows, rung_starts, t0


def run_induced(spec):
    stress = spec["strata"]["stratum_stress"]["endpoints"]
    b_stress = 8
    gap = 0.15
    delays = [2, 5, 15, 60, 180]
    result = {"bursts": {}, "recovery": {}, "rungs": delays}
    burst_t0 = {}
    for ep in stress:
        opener = L.build_opener()
        recs = []
        t_burst = time.time()
        log(f"induced burst on {ep}")
        for b in range(b_stress):
            rec = L.fetch(opener, ep)
            rec["burst_pos"] = b
            recs.append(rec)
            if b < b_stress - 1:
                time.sleep(gap)
        load_rank = max(L.SEVERITY_RANK.get(r["class"], -1) for r in recs)
        load_class = [c for c, r in L.SEVERITY_RANK.items() if r == load_rank][0]
        burst_t0[ep] = t_burst
        result["bursts"][ep] = {
            "burst_t0": t_burst,
            "classes": [r["class"] for r in recs],
            "load_rank": load_rank,
            "load_class": load_class,
            "records": recs,
        }
        log(f"  load_class={load_class} classes={[r['class'] for r in recs]}")
    for d in delays:
        for ep in stress:
            target = burst_t0[ep] + d
            while True:
                now = time.time()
                if target <= now:
                    break
                log(f"  induced wait {target-now:.1f}s before recovery d={d}s for {ep}")
                time.sleep(min(20.0, target - now))
            rec = L.fetch(L.build_opener(), ep)
            result["recovery"].setdefault(ep, []).append({
                "nominal_delay_s": d,
                "actual_delay_s": rec["t_start"] - burst_t0[ep],
                "class": rec["class"],
                "record": rec,
            })
            log(f"  recovery {ep} d={d}s -> {rec['class']} (actual {rec['t_start']-burst_t0[ep]:.1f}s)")
    L.write_json(EXP / "raw/induced_probe.json", result)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=38074818597)
    args = ap.parse_args()

    verify_freeze()
    spec = L.load_spec(ROOT)
    (EXP / "raw").mkdir(parents=True, exist_ok=True)
    # fresh raw files for this run
    for name in ("oracles.jsonl", "ambient_collection.jsonl"):
        p = EXP / "raw" / name
        if p.exists():
            p.unlink()

    log(f"code sha256={L.sha256_file(__file__)} lib sha256={L.sha256_file(Path(__file__).parent/'exp_38074818597_lib.py')}")
    log(f"spec sha256={L.sha256_file(EXP/'spec.json')}")

    t_begin = time.time()
    opener = L.build_opener()
    oracle_rows = run_oracles(spec, opener)
    t_oracles_done = time.time()

    ambient_rows, rung_starts, t0 = run_ambient(spec, args.seed)
    t_ambient_done = time.time()

    induced = run_induced(spec)
    t_end = time.time()

    meta = {
        "experiment_id": EXP_ID,
        "seed_probe_order": args.seed,
        "seed_permutation": spec["stable_identifiers"]["seeds"]["permutation"],
        "seed_bootstrap": spec["stable_identifiers"]["seeds"]["bootstrap"],
        "spec_sha256": L.sha256_file(EXP / "spec.json"),
        "run_code_sha256": L.sha256_file(__file__),
        "lib_code_sha256": L.sha256_file(Path(__file__).parent / "exp_38074818597_lib.py"),
        "t0_unix": t0,
        "t_begin_unix": t_begin,
        "t_oracles_done_unix": t_oracles_done,
        "t_ambient_done_unix": t_ambient_done,
        "t_end_unix": t_end,
        "rung_start_unix": {str(k): v for k, v in rung_starts.items()},
        "rung_actual_delta_s": {str(si): (v - t0) for si, v in rung_starts.items()},
        "delta_ref_actual_s": rung_starts[max(rung_starts)] - t0,
        "n_endpoints": len(spec["frozen_universe"]["endpoints"]),
        "n_ambient_records": len(ambient_rows),
        "n_oracle_records": len(oracle_rows),
        "wall_clock_s": t_end - t_begin,
        "wall_clock_cap_minutes": spec["sweep_protocol"]["wall_clock_cap_minutes"],
    }
    L.write_json(EXP / "raw/collection_meta.json", meta)
    log(f"collection complete wall_clock={meta['wall_clock_s']:.1f}s delta_ref_actual={meta['delta_ref_actual_s']:.1f}s")


if __name__ == "__main__":
    main()
