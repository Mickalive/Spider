"""SPIDER TEAM GRAPH — strategy consumer for blind inheritance.

One consumer shell (inherited from Explorer: identical exploration policy,
identical replay/fallback machinery, identical budgets) parameterized ONLY
by which memory representation it consults:

  strategy="fragment"    SPIDER addressing layer over auto-derived fragment
                         metadata (graph.addressing). No goal_sig lookup.
  strategy="trajectory"  nearest-trajectory retrieval over stored text
                         profiles (strong memory baseline).
  strategy="graph"       BFS plan over the concrete state-transition graph
                         with keyword-scored goal states (no abstraction).
  strategy="none"        + store.allow_reads=False  => cold control.

All strategies inject their route into the SAME phase-R replay code path, so
reused/novel accounting and entry-reset recovery are matched by construction.
"""
import time

from graph.explorer import Explorer
from graph import addressing
from graph import baselines


class StrategyConsumer(Explorer):

    def __init__(self, store, policy="B", strategy="fragment"):
        super().__init__(store, policy=policy)
        assert strategy in ("fragment", "trajectory", "graph", "none")
        self.strategy = strategy
        self.site_key = None
        self._route_cache = {}
        self.diag = {"strategy": strategy,
                     "lookups": [], "n_lookups": 0,
                     "retrieval_ms": 0.0, "unknown": 0}

    # ---- hooks used by driver bookkeeping ----
    def on_event(self, event, **kw):
        pass

    def _remember(self, snap):
        super()._remember(snap)
        self._last_snap = snap

    def run_task(self, session, task, condition, task_id):
        self.site_key = task["site"]
        self._route_cache = {}
        return super().run_task(session, task, condition, task_id)

    def _lookup(self, sub):
        """Return a fragment-like route dict or None.

        Called by the parent phase-R loop; result is cached per subgoal so
        the reset-retry attempt replays the SAME retrieved route.
        """
        key = sub.get("sig")
        if key in self._route_cache:
            return self._route_cache[key]
        t0 = time.time()
        route, detail = self._retrieve(sub)
        ms = (time.time() - t0) * 1000
        self.diag["n_lookups"] += 1
        self.diag["retrieval_ms"] += ms
        if route is None:
            self.diag["unknown"] += 1
        else:
            self.diag.setdefault("injected", 0)
            self.diag["injected"] += 1
        rec = {"subgoal_prov": key, "kws": list(sub.get("keywords", [])),
               "route_found": route is not None, "ms": round(ms, 2),
               **detail}
        if route is not None:
            rec["n_steps"] = len(route["steps"])
            rec["route_source"] = route.get("goal_sig")
        self.diag["lookups"].append(rec)
        self.on_event("lookup", **rec)
        self._route_cache[key] = route
        return route

    def _retrieve(self, sub):
        kws = sub.get("keywords", [])
        site = self.site_key
        if self.strategy == "none":
            return None, {"reason": "read_disabled"}
        if self.strategy == "fragment":
            res = addressing.address_fragments(self.store, kws, site=site)
            cands = res["candidates"]
            top = [{"goal_sig": c["goal_sig"], "score": c["score"],
                    "content_hits": c["content_hits"],
                    "provenance_hits": c["provenance_hits"]}
                   for c in cands[:3]]
            detail = {"unknown": res["unknown"],
                      "n_scored": res["all_scored"], "top_candidates": top}
            if res["unknown"]:
                return None, detail
            best = cands[0]
            frag = self.store.best_fragment(best["goal_sig"], site=site)
            if not frag or not frag["steps"]:
                detail["reason"] = "fragment_row_missing"
                return None, detail
            detail["confidence"] = frag["confidence"]
            return {"steps": [dict(s) for s in frag["steps"]],
                    "confidence": frag["confidence"],
                    "site": frag["site"],
                    "goal_sig": f"addr:{best['goal_sig']}"}, detail
        if self.strategy == "trajectory":
            route, diag = baselines.nearest_trajectory_route(
                self.store, kws, site)
            return route, diag
        if self.strategy == "graph":
            snap = getattr(self, "_last_snap", None)
            if snap is None:
                return None, {"reason": "no_current_snapshot"}
            route, diag = baselines.graph_bfs_route(
                self.store, snap, kws, self.store.fingerprint)
            return route, diag
        raise AssertionError(self.strategy)
