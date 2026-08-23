"""SPIDER TEAM GRAPH — Run 1: inheritance experiment driver.

Sequence: cold exploration builds the store; independent agents then
inherit. Measures first-agent vs later-agent cost on live websites.
"""
import json, os, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.browser import Session
from graph.store import Store
from graph.explorer import Explorer
from graph import tasks as T

DB = "/tmp/opencode/spider_graph.db"
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "graph",
                   f"run1_{time.strftime('%Y%m%d_%H%M%S')}.json")

SITE_BASES = {
    "books": "https://books.toscrape.com/",
    "quotes": "https://quotes.toscrape.com/",
    "internet": "https://the-internet.herokuapp.com/",
    "wikipedia": "https://en.wikipedia.org/wiki/Spider",
}


def preflight():
    up = {}
    with Session() as s:
        for name, url in SITE_BASES.items():
            try:
                snap = s.goto(url, name)
                up[name] = bool(snap["elements"])
            except Exception as e:
                up[name] = False
                print(f"[preflight] {name} DOWN: {e}")
    return up


def run_sequence(seq, store, alive):
    all_runs = []
    growth = []
    for agent_id, task_id, cond in seq:
        task = T.TASKS[task_id]
        if not alive.get(task["site"], False):
            rec = {"task": task_id, "agent": agent_id, "condition": cond,
                   "status": "site_down"}
            all_runs.append(rec); continue
        exp = Explorer(store, policy=agent_id[-1])
        with Session() as sess:
            try:
                m = exp.run_task(sess, task, cond, task_id)
                status = ("success" if m["subgoals_ok"] == m["subgoals_total"]
                          else "partial")
            except Exception as e:
                m, status = exp.m, f"error:{type(e).__name__}"
        st = store.stats()
        store.log_run(agent_id, task_id, cond, {**m, "status": status})
        rec = {"task": task_id, "agent": agent_id, "condition": cond,
               "status": status, **m}
        all_runs.append(rec)
        growth.append({"after_task": task_id, "cond": cond,
                       "store": st})
        print(f"{agent_id} {task_id:34s} {cond:12s} {status:8s} "
              f"act={m['actions']:3d} reused={m['reused']:3d} novel={m['novel']:3d} "
              f"fail={m['failed']:2d} recov={m['recoveries']} "
              f"{m['wall_ms']/1000:6.1f}s | store={st}")
    return all_runs, growth


def summarize(runs):
    def agg(rs):
        rs = [r for r in rs if r.get("status") in ("success", "partial")]
        if not rs:
            return {}
        n = len(rs)
        k = lambda key: sum(r.get(key, 0) for r in rs) / n
        return {"n": n,
                "actions_per_task": round(k("actions"), 2),
                "reused_per_task": round(k("reused"), 2),
                "novel_per_task": round(k("novel"), 2),
                "failures_per_task": round(k("failed"), 2),
                "recoveries_total": sum(r.get("recoveries", 0) for r in rs),
                "wall_s_per_task": round(k("wall_ms") / 1000, 1),
                "subgoal_success_rate": round(
                    sum(r["subgoals_ok"] for r in rs) /
                    max(1, sum(r["subgoals_total"] for r in rs)), 3)}
    return {
        "cold_first_exploration": agg([r for r in runs if r["condition"] == "cold"]),
        "inherit_composite": agg([r for r in runs if r["condition"] == "inherit"]),
        "replay_exact": agg([r for r in runs if r["condition"] == "replay"]),
    }


def main():
    alive = preflight()
    print("[preflight]", alive)
    if os.path.exists(DB):
        os.remove(DB)
    store = Store(DB)

    print("\n=== PHASE A: cold exploration (agentG builds store) ===")
    cold_runs, growth = run_sequence(T.AGENT_SEQUENCE_COLD_FIRST, store, alive)
    print("\n=== PHASE B: inheritance / composition / replay ===")
    inh_runs, g2 = run_sequence(T.AGENT_SEQUENCE_INHERIT, store, alive)
    runs = cold_runs + inh_runs

    result = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "preflight": alive,
              "runs": runs,
              "knowledge_growth": growth + g2,
              "summary": summarize(runs),
              "store_final": store.stats()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)
    print(f"\nwrote {OUT}")
    print(json.dumps(result["summary"], indent=1))


if __name__ == "__main__":
    main()
