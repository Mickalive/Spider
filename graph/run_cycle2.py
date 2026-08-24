"""SPIDER TEAM GRAPH — cycle 32670239235 experiment driver.

Phases:
  P0 preflight live sites.
  P1 PRODUCTION: agentG explores 10 tasks cold on a fresh store (writes
     states/transitions/fragments/trajectories; reads disabled by policy).
  P2 Store isolation: physical copies so all four memory methods start from
     byte-identical knowledge. Cold control gets an empty store with reads
     disabled.
  P3 BLIND TARGETS: each of 5 held-out composites executed by every method
     (fresh browser session per run; per-target method order randomized with
     a fixed seed). The consumer never receives hand-selected fragment IDs;
     addressing is content-derived and UNKNOWN stays UNKNOWN (explore).
  P4 INHERITANCE LEDGER / COST CURVE: ordered execution log over the
     producer stream + fragment-method target stream + a replay-validation
     pass, giving >=20 sequential agents/tasks against growing knowledge.
  P5 PROSPECTIVE CALIBRATION: frozen-confidence fragments are revalidated
     R=2 times each in fresh sessions; outcomes are recorded WITHOUT
     feeding back into the store (no contamination of the evaluated score).

Preregistered primary endpoints (frozen before any target run):
  - mean novel actions per composite target (inheritance cost), per method;
  - composite success rate per method;
  - addressing UNKNOWN rate and content-support rate (fragment method);
  - retrieval overhead ms per subgoal.
Exploratory (labeled as such): calibration reliability table.
"""
import hashlib, json, os, random, shutil, subprocess, sys, time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.browser import Session
from graph.store import Store, target_sig, now
from graph.explorer import Explorer, NO_EFFECT_EXEMPT
from graph.consumer import StrategyConsumer
from graph import tasks2 as T

CYCLE = "32670239235"
VARIANT = "run2c"
# Disclosed corrections relative to recorded provenance artifacts:
#   run2  (results/graph/run2_cycle32670239235_20260823_235851.json)
#   run2b (results/graph/run2b_cycle32670239235_20260824_005039.json)
#   C1 keyword hits scaled 3x->6x so keyword hits outrank generic priors
#      (run2: polluted pager fragment whose first step was a logo click);
#   C2 product-page acceptance excludes global listing pages (run2:
#      /catalogue/page-2.html satisfied 'page-2');
#   C3 href tokens weighted below visible text/aria (run2b: empty-text
#      carousel links with keyword-bearing hrefs outranked the true
#      navigation link; production 'fiction' task landed on an unrelated
#      product page via its slug substring);
#   C4 structural URL-path predicates for books category/product/pager and
#      quotes tag pagination replace raw substring acceptance (run2/run2b:
#      'science-fiction' satisfied 'fiction'; homepage global pager
#      satisfied 'page-2');
#   C5 route distillation at fragment acquisition: saved steps are the
#      accepted path reconstructed over the subgoal's own recorded
#      transition edges (fills/presses interleaved chronologically), so
#      exploratory detour clicks no longer enter fragments;
#   C6 generic crawler recovery: on dead-end or churn (no new structural
#      state for 6 actions) return deterministically to the task entry
#      region (charged load+novel). Replaces browser-history back(), which
#      after a replay walks the replay path rather than site structure.
#      Available identically in ALL conditions including cold.
#   NO change to addressing gates/weights (frozen), budgets, methods,
#      corpus routes, or analysis endpoints.
CHANGES_VS_RUN2 = ["C1-keyword-prior-scale", "C2-product-accept-guard",
                   "C3-href-weight-below-text", "C4-structural-url-predicates",
                   "C5-route-distillation", "C6-deterministic-hub-recovery"]
SEED = 20260823
WORKDIR = "/tmp/opencode/cycle2"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "graph")
METHODS = ["cold", "trajectory", "graph", "fragment"]
CAL_ROUNDS = 2
CAL_MAX_FRAGMENTS = 20
REPLAY_VALIDATION_TASKS = ["Q_login", "I_login", "B_travel_first_book",
                           "I_checkboxes_check_first", "I_status_200"]


def git_sha():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True).strip()[:12]
    except Exception:
        return "unknown"


def preflight():
    up = {}
    with Session() as s:
        for name, url in T.SITES.items():
            try:
                snap = s.goto(url, name)
                up[name] = bool(snap["elements"])
            except Exception as e:
                up[name] = False
                print(f"[preflight] {name} DOWN: {e}")
    return up


def ledger_append(ledger, i, phase, gen, agent, task_id, cond, m, status,
                  stats):
    ledger.append({
        "i": i, "phase": phase, "gen": gen, "agent": agent,
        "task": task_id, "condition": cond, "status": status,
        "actions": m.get("actions", 0), "novel": m.get("novel", 0),
        "reused": m.get("reused", 0), "failed": m.get("failed", 0),
        "recoveries": m.get("recoveries", 0),
        "loads": m.get("loads", 0),
        "decision_points": m.get("decision_points", 0),
        "wall_ms": m.get("wall_ms", 0),
        "subgoals_ok": m.get("subgoals_ok", 0),
        "subgoals_total": m.get("subgoals_total", 0),
        "store": stats})


def run_one(store_cls_kwargs, strategy, condition, agent, task_id, task,
            ledger, ctr, phase, gen):
    store = Store(**store_cls_kwargs)
    # "cold" is Explorer + read-gated store; other strategies share one
    # consumer shell with identical replay/fallback machinery.
    if strategy in ("none", "cold"):
        exp = Explorer(store, policy=agent[-1])
    else:
        exp = StrategyConsumer(store, policy=agent[-1], strategy=strategy)
    # persist trajectory records into THIS store (each method stream keeps
    # its own memory; production builds the baseline corpus)
    def _hook(event, **kw):
        if event == "trajectory":
            store.save_trajectory(kw["task_id"], kw["site"],
                                  kw["profile_tokens"], kw["steps"])
    exp.hook = _hook
    t_start = time.time()
    err = None
    with Session() as sess:
        try:
            m = exp.run_task(sess, task, condition, task_id)
            status = ("success" if m["subgoals_ok"] == m["subgoals_total"]
                      else "partial")
        except Exception as e:
            import traceback; traceback.print_exc()
            m, status = dict(getattr(exp, "m", {})), f"error:{type(e).__name__}"
            err = str(e)[:200]
    diag = getattr(exp, "diag", {})
    st = store.stats()
    store.log_run(agent, task_id, condition, {**m, "status": status})
    ledger_append(ledger, next(ctr), phase, gen, agent, task_id, condition,
                  m, status, st)
    rec = {"task": task_id, "method": strategy, "condition": condition,
           "agent": agent, "status": status, "metrics": m,
           "store_after": st,
           "run_wall_ms": int((time.time() - t_start) * 1000)}
    if diag:
        rec["retrieval_diag"] = {
            "n_lookups": diag.get("n_lookups", 0),
            "retrieval_ms": round(diag.get("retrieval_ms", 0.0), 1),
            "unknown": diag.get("unknown", 0),
            "lookups": diag.get("lookups", [])}
    if err:
        rec["error"] = err
    store.db.close()
    return rec


def main():
    os.makedirs(WORKDIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = random.Random(SEED)
    alive = preflight()
    print("[preflight]", alive)

    prod_path = f"{WORKDIR}/prod.db"
    for p in list(os.listdir(WORKDIR)):
        if p.endswith(".db"):
            os.remove(os.path.join(WORKDIR, p))

    ledger, ctr = [], iter(range(1, 10 ** 6))
    production_runs, target_runs, replay_runs = [], [], []

    # ---------------- P1 production ----------------
    print("\n=== P1: production (agentG cold) ===")
    prod_store_kwargs = {"path": prod_path, "allow_reads": False}
    for tid, task in T.PRODUCTION_TASKS.items():
        if not alive[task["site"]]:
            continue
        rec = run_one(prod_store_kwargs, "none", "cold", "agentG", tid, task,
                      ledger, ctr, "production", 1)
        production_runs.append(rec)
        print(f"prod {tid:32s} {rec['status']:8s} "
              f"act={rec['metrics'].get('actions',0):3d} "
              f"novel={rec['metrics'].get('novel',0):3d} "
              f"{rec['metrics'].get('wall_ms',0)/1000:6.1f}s | {rec['store_after']}")

    # checkpoint WAL so physical copies are complete
    chk = Store(prod_path)
    chk.db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    chk.db.commit(); chk.db.close()

    # ---------------- P2 store isolation ----------------
    paths = {}
    for meth in METHODS:
        if meth == "cold":
            paths[meth] = f"{WORKDIR}/cold.db"
        else:
            dst = f"{WORKDIR}/{meth}.db"
            shutil.copyfile(prod_path, dst)
            paths[meth] = dst
    # materialize the cold store now (schema only; reads stay disabled)
    _c = Store(paths["cold"], allow_reads=False)
    _c.db.close()
    print("[stores]", {k: os.path.getsize(v) for k, v in paths.items()})

    # ---------------- P3 blind targets ----------------
    print("\n=== P3: blind composite targets ===")
    for tid, task in T.TARGET_TASKS.items():
        if not alive[task["site"]]:
            continue
        order = rng.sample(METHODS, len(METHODS))
        print(f"-- {tid} order={order}")
        for meth in order:
            kw = {"path": paths[meth]}
            if meth == "cold":
                kw["allow_reads"] = False
            rec = run_one(kw, meth, "blind", "agentB", tid, task,
                          ledger, ctr, "target", 2)
            rec["method_order"] = order
            target_runs.append(rec)
            mm = rec["metrics"]
            rd = rec.get("retrieval_diag", {})
            print(f"tgt {meth:10s} {tid:34s} {rec['status']:8s} "
                  f"act={mm.get('actions',0):3d} reused={mm.get('reused',0):3d} "
                  f"novel={mm.get('novel',0):3d} unk={rd.get('unknown','-')} "
                  f"| {rec['store_after']}")

    # ---------------- P4 replay validation on the inheritance stream ------
    print("\n=== P4: replay validation (agentB, fragment store stream) ===")
    frag_kwargs = {"path": paths["fragment"]}
    for tid in REPLAY_VALIDATION_TASKS:
        task = T.PRODUCTION_TASKS[tid]
        if not alive[task["site"]]:
            continue
        rec = run_one(frag_kwargs, "none", "replay", "agentB", tid, task,
                      ledger, ctr, "replay_validation", 3)
        replay_runs.append(rec)
        print(f"replay {tid:32s} {rec['status']:8s} "
              f"act={rec['metrics'].get('actions',0):3d} "
              f"reused={rec['metrics'].get('reused',0):3d}")

    # ---------------- P5 prospective calibration ----------------
    print("\n=== P5: prospective fragment calibration ===")
    shutil.copyfile(prod_path, f"{WORKDIR}/calib.db")
    calib = Store(f"{WORKDIR}/calib.db")
    groups = {}
    for f in calib.iter_fragments():
        k = (f["goal_sig"], f["site"])
        groups.setdefault(k, f)
    crows = []
    calibrated = 0
    for (gsig, site), f in sorted(groups.items()):
        if f["success_count"] < 1 or not f["steps"]:
            continue
        if calibrated >= CAL_MAX_FRAGMENTS:
            break
        entry_url = (f.get("meta") or {}).get("entry_url") or \
            T.SITES.get(site, "").rstrip("/") + "/"
        conf_before = Store.confidence(f["success_count"], f["failure_count"],
                                       f["last_validated"])
        for r in range(CAL_ROUNDS):
            ok_all = True
            try:
                with Session() as s:
                    snap = s.goto(entry_url, site)
                    cur = snap
                    for step in f["steps"]:
                        hits = [e["i"] for e in cur["elements"]
                                if target_sig(e) == step["target_sig"]
                                and e["enabled"]]
                        if not hits:
                            ok_all = False; break
                        act = {"kind": step["kind"], "target": hits[0],
                               "target_sig": step["target_sig"],
                               "value": step.get("value", "")}
                        prev_fp = calib.fingerprint(cur)
                        post = s.act(cur, act)
                        cur = post
                        if not post["last_action"].get("ok"):
                            ok_all = False; break
                        if post["last_action"].get("ok") and \
                                step["kind"] not in NO_EFFECT_EXEMPT and \
                                calib.fingerprint(post) == prev_fp:
                            ok_all = False; break
            except Exception as e:
                ok_all = False
                crows.append({"goal_sig_prov": gsig, "site": site,
                              "round": r, "conf_before": conf_before,
                              "outcome": "error", "error": str(e)[:120],
                              "entry_url": entry_url})
                continue
            crows.append({"goal_sig_prov": gsig, "site": site,
                          "round": r, "conf_before": conf_before,
                          "outcome": "success" if ok_all else "fail",
                          "n_steps": len(f["steps"]),
                          "entry_url": entry_url})
        calibrated += 1
    print(f"[calibration] fragments={calibrated} rows={len(crows)}")

    result = {
        "cycle": CYCLE,
        "variant": VARIANT,
        "changes_vs_run2": CHANGES_VS_RUN2,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "commit": git_sha(),
        "seed": SEED,
        "preregistered": {
            "tau": addressing_tau(), "content_w": 1.0, "prov_w": 0.4,
            "min_content_hits": 1, "traj_min_hits": 1,
            "bfs_max_depth": 3, "bfs_frontier_cap": 60, "conf_min": 0.35,
            "primary_endpoints": [
                "mean novel actions per composite target per method",
                "composite success rate per method",
                "addressing unknown rate (fragment method)",
                "retrieval overhead ms per lookup"],
            "exploratory": ["prospective confidence reliability"]},
        "preflight": alive,
        "config": {"methods": METHODS, "cal_rounds": CAL_ROUNDS,
                   "cal_max_fragments": CAL_MAX_FRAGMENTS},
        "ledger": ledger,
        "production_runs": production_runs,
        "target_runs": target_runs,
        "replay_runs": replay_runs,
        "calibration_rows": crows,
        "store_final": Store(paths["fragment"]).stats(),
    }
    out = os.path.join(
        RESULTS_DIR,
        f"{VARIANT}_cycle{CYCLE}_{time.strftime('%Y%m%d_%H%M%S')}.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=1)
    print("\nwrote", out)


def addressing_tau():
    from graph.addressing import TAU
    return TAU


if __name__ == "__main__":
    main()
