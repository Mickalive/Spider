"""Cycle 32670239235 analysis — matched method comparison + curve + calibration.

Reads a run2/run2b results JSON and emits compact analysis:
  - per-target x per-method table (primary endpoints);
  - paired deltas fragment-vs-{cold,trajectory,graph} with task-grouped
    bootstrap CIs (seeded RNG, resample targets, B=10000);
  - inheritance ledger stream (>=20 sequential executions) summary;
  - addressing retrieval quality (content-support rate, unknown rate,
    route-source provenance mix);
  - prospective calibration reliability (exploratory).
No aggregate claim is made without its per-task rows.
"""
import json, random, sys

B = 10000
SEED = 20260823
METHODS = ["cold", "trajectory", "graph", "fragment"]


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def paired_bootstrap_delta(per_task_a, per_task_b, seed=SEED):
    """CI for mean(a-b) resampling TARGETS (the exchangeable unit)."""
    diffs = [a - b for a, b in zip(per_task_a, per_task_b)]
    rng = random.Random(seed)
    boots = []
    n = len(diffs)
    if n == 0:
        return None
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        boots.append(mean([diffs[i] for i in idx]))
    boots.sort()
    lo, hi = boots[int(0.025 * B)], boots[int(0.975 * B)]
    return {"mean_diff": round(mean(diffs), 3),
            "ci95": [round(lo, 3), round(hi, 3)],
            "n_targets": n, "per_task_diffs": [round(d, 1) for d in diffs]}


def analyze(path_in, path_out):
    r = json.load(open(path_in))
    out = {"source": path_in.split("/")[-1], "variant": r.get("variant"),
           "cycle": r["cycle"], "commit": r["commit"]}

    # ---- primary table ----
    table = {}
    by = {}
    for rec in r["target_runs"]:
        by.setdefault(rec["task"], {}).setdefault(rec["method"], []).append(rec)
    tasks = sorted(by)
    for task in tasks:
        row = {}
        for meth, recs in by[task].items():
            m = recs[0]["metrics"]
            diag = recs[0].get("retrieval_diag", {})
            row[meth] = {
                "status": recs[0]["status"],
                "success": int(recs[0]["status"] == "success"),
                "actions": m["actions"], "novel": m["novel"],
                "reused": m["reused"], "failed": m["failed"],
                "recoveries": m["recoveries"], "loads": m["loads"],
                "subgoals_ok": m["subgoals_ok"],
                "subgoals_total": m["subgoals_total"],
                "decision_points": m["decision_points"],
                "wall_ms": m["wall_ms"],
                "retrieval_ms": diag.get("retrieval_ms"),
                "unknown_lookups": diag.get("unknown")}
        table[task] = row
    out["per_target_table"] = table

    # ---- aggregates + paired deltas vs fragment ----
    def series(meth, key):
        vals = []
        for task in tasks:
            recs = by[task].get(meth)
            if recs:
                if key == "success":
                    vals.append(int(recs[0]["status"] == "success"))
                else:
                    vals.append(recs[0]["metrics"][key])
        return vals

    agg = {}
    for meth in METHODS:
        agg[meth] = {
            "novel_actions_mean": round(mean(series(meth, "novel")), 2),
            "actions_mean": round(mean(series(meth, "actions")), 2),
            "reused_mean": round(mean(series(meth, "reused")), 2),
            "success_rate": round(mean(series(meth, "success")), 3),
            "recoveries_total": sum(series(meth, "recoveries")),
            "wall_s_mean": round(mean(series(meth, "wall_ms")) / 1000, 1)}
    out["aggregate"] = agg
    deltas = {}
    for meth in ("cold", "trajectory", "graph"):
        deltas[f"fragment_minus_{meth}__novel_actions"] = \
            paired_bootstrap_delta(series("fragment", "novel"),
                                   series(meth, "novel"))
        deltas[f"fragment_minus_{meth}__success"] = \
            paired_bootstrap_delta(series("fragment", "success"),
                                   series(meth, "success"))
    out["paired_deltas"] = deltas

    # ---- inheritance ledger / cost-vs-knowledge stream ----
    ledger = r["ledger"]
    stream = []
    reuse_by_gen = {}
    for e in ledger:
        stream.append({k: e[k] for k in
                       ("i", "phase", "gen", "agent", "task", "condition",
                        "status", "actions", "novel", "reused",
                        "store")})
        g = reuse_by_gen.setdefault(e["gen"], {"novel": [], "reused": [],
                                               "n": 0})
        g["novel"].append(e["novel"]); g["reused"].append(e["reused"])
        g["n"] += 1
    out["ledger_stream_len"] = len(ledger)
    out["generations"] = {str(g): {"n_tasks": v["n"],
                                   "mean_novel": round(mean(v["novel"]), 2),
                                   "mean_reused": round(mean(v["reused"]), 2)}
                          for g, v in sorted(reuse_by_gen.items())}
    out["stream"] = stream

    # ---- retrieval diagnostics across all fragment-method runs ----
    lookups = []
    for rec in r["target_runs"]:
        if rec["method"] != "fragment":
            continue
        for l in rec.get("retrieval_diag", {}).get("lookups", []):
            top = l.get("top_candidates") or []
            lookups.append({
                "task": rec["task"], "subgoal_prov": l["subgoal_prov"],
                "kws": l["kws"], "route_found": l["route_found"],
                "unknown": l.get("unknown"),
                "top_sig": top[0]["goal_sig"] if top else None,
                "top_score": top[0]["score"] if top else None,
                "content_hits": top[0]["content_hits"] if top else None,
                "ms": l["ms"]})
    found = [l for l in lookups if l["route_found"]]
    out["addressing_quality"] = {
        "n_lookups": len(lookups),
        "route_found_rate": round(len(found) / max(1, len(lookups)), 3),
        "unknown_rate": round(
            sum(1 for l in lookups if l.get("unknown")) /
            max(1, len(lookups)), 3),
        "mean_retrieval_ms_per_lookup": round(
            mean([l["ms"] for l in lookups]), 3)}

    # ---- prospective calibration (exploratory) ----
    rows = r["calibration_rows"]
    by_conf = {}
    pairs = []
    for c in rows:
        if c["outcome"] == "error":
            continue
        b = round(c["conf_before"], 2)
        bucket = "<0.5" if b < 0.5 else ("0.5-0.75" if b <= 0.75 else ">0.75")
        by_conf.setdefault(bucket, []).append(1 if c["outcome"] == "success"
                                              else 0)
        try:
            pairs.append((float(c["conf_before"]),
                          1.0 if c["outcome"] == "success" else 0.0))
        except Exception:
            pass
    out["calibration"] = {
        "n_rounds_total": len(rows),
        "empirical_success_by_confidence_bucket": {
            k: {"n": len(v), "rate": round(mean(v), 3)}
            for k, v in sorted(by_conf.items())}}
    if len(pairs) >= 5 and len(set(p[0] for p in pairs)) > 1:
        xs = [p[0] for p in pairs]; ys = [p[1] for p in pairs]
        mx, my = mean(xs), mean(ys)
        cov = sum((x - mx) * (y - my) for x, y in pairs)
        var = (sum((x - mx) ** 2 for x in xs) *
               sum((y - my) ** 2 for y in ys)) ** 0.5
        pearson = cov / var if var else float("nan")
        brier = mean([(x - y) ** 2 for x, y in pairs])
        out["calibration"]["pearson_conf_vs_outcome"] = round(pearson, 3)
        out["calibration"]["brier_if_conf_as_prob"] = round(brier, 4)

    json.dump(out, open(path_out, "w"), indent=1)
    # console summary
    print(f"== {out['source']} variant={out.get('variant')} ==")
    for meth in METHODS:
        print(f"{meth:11s}", agg[meth])
    for k, v in deltas.items():
        print(k, v["mean_diff"], v["ci95"])
    print("generations:", out["generations"])
    print("addressing:", out["addressing_quality"])
    print("calibration:", out.get("calibration"))
    return out


if __name__ == "__main__":
    analyze(sys.argv[1], sys.argv[2])
