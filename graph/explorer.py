"""SPIDER TEAM GRAPH — heuristic explorer agents with cumulative inheritance.

Two independent policies stand in for different foundation models
(G10 proxy): both consume the SAME accumulated store.
  agentG ("greedy ranker"): ranks candidates by keyword overlap.
  agentB ("breadth walker"): walks actionable elements in DOM order.

Conditions:
  cold          : read disabled; exploration writes knowledge.
  inherit       : fragment lookup+replay per subgoal; local re-exploration
                  from first failure point (novelty localized).
  inherit-cold  : like cold but store readable (measures retrieval miss).
  replay        : whole-task replay validation.
"""
import json, time
from shared.browser import Session
from graph.store import Store, target_sig

MAX_CLICKS, MAX_LOADS, WALL_S = 30, 16, 140
EXPLORATION_STEPS = MAX_CLICKS * 3   # equal budget for every condition
MAX_HUB_RETURNS = 20   # generic crawler prior: dead-end -> return toward hub
GENERIC = {"pager": "generic.paginate.next"}
CONF_MIN = 0.35
# Action kinds that legitimately leave the structural fingerprint unchanged.
# ("press" added in cycle 32670239235: typing into an input changes dynamic
# variables, not page structure.)
NO_EFFECT_EXEMPT = ("fill", "check", "press")


def overlap(text, kws):
    t = (text or "").lower()
    return sum(1 for k in kws if k and k.lower() in t)


class Explorer:
    def __init__(self, store: Store, policy="G"):
        self.store = store
        self.policy = policy
        self.m = self._zero()
        # per-task observability hooks (overridden by consumers/drivers)
        self.hook = lambda event, **kw: None
        # canonical task-site key (set in run_task); used for fragment rows
        self.site_hint = None
        # per-subgoal context used to auto-derive fragment metadata
        self._ctx_pairs = []
        self._entry_snap = None
        # per-subgoal edge journal for route distillation:
        # (fp_from, kind, target_sig, value, fp_to)
        self._edge_journal = []

    def _distill_route(self, entry_snap, final_snap):
        """Reconstruct the accepted path from this subgoal's own recorded
        transition edges (BFS over experienced navigation edges only; no
        extra web calls). Removes exploratory detour clicks that would
        otherwise be saved into fragments (run2/run2c lesson).

        Actions that do not change the structural fingerprint (fills,
        checks, presses -> self-loop edges) are re-interleaved
        chronologically onto the states of the chosen path, because they
        can be causally required (login credentials!) even though they
        leave page structure unchanged."""
        start = self.store.fingerprint(entry_snap)
        goal = self.store.fingerprint(final_snap)
        nav_edges = {}
        journal = list(getattr(self, "_edge_journal", []))
        for fp_from, kind, sig, val, fp_to in journal:
            if fp_from == fp_to:
                continue
            nav_edges.setdefault(fp_from, []).append((fp_to, kind, sig, val))
        from collections import deque
        q = deque([start])
        parent = {start: None}
        while q:
            cur = q.popleft()
            if cur == goal:
                break
            for fp_to, kind, sig, val in nav_edges.get(cur, []):
                if fp_to not in parent:
                    parent[fp_to] = (cur, kind, sig, val)
                    q.append(fp_to)
        if goal not in parent:
            return None
        # ordered states along the chosen route
        chain = []
        node = goal
        while node is not None:
            chain.append(node)
            node = parent[node][0] if parent[node] else None
        chain.reverse()
        order = {fp: i for i, fp in enumerate(chain)}
        # chronological single pass over the journal:
        #  - self-loop actions are kept while "on" a route state
        #  - navigation actions are kept when they match the next route leg
        steps = []
        pos = 0
        for fp_from, kind, sig, val, fp_to in journal:
            if fp_from == fp_to:
                if order.get(fp_from) == pos:
                    step = {"kind": kind, "target_sig": sig}
                    if val is not None:
                        step["value"] = val
                    steps.append(step)
            else:
                if pos + 1 < len(chain) and fp_from == chain[pos] \
                        and fp_to == chain[pos + 1]:
                    steps.append({"kind": kind, "target_sig": sig})
                    pos += 1
        return steps

    @staticmethod
    def _zero():
        return {"loads": 0, "actions": 0, "reused": 0, "novel": 0,
                "failed": 0, "recoveries": 0, "decision_points": 0,
                "llm_calls": 0, "subgoals_ok": 0, "subgoals_total": 0,
                "wall_ms": 0}

    # ---------------- public ----------------
    def run_task(self, session: Session, task: dict, condition: str,
                 task_id: str):
        t0 = time.time()
        self.m = self._zero()   # per-task metrics, not cumulative
        self.site_hint = task["site"]
        self._visited = []      # trajectory record for memory baselines
        self._traj_steps = []
        snap = session.goto(task["start"], task["site"])
        self.m["loads"] += 1
        start_sid = self.store.upsert_state(snap)
        for sub in task["subgoals"]:
            self.m["subgoals_total"] += 1
            snap = self._run_subgoal(session, snap, sub, condition, task_id,
                                     task["start"], task["site"])
        self.m["wall_ms"] += int((time.time() - t0) * 1000)
        # bounded trajectory profile: url shapes + sampled text tokens
        toks = []
        for v in getattr(self, "_visited", []):
            toks.extend(_slug_tokens(v.get("url_shape", "")))
            toks.extend(v.get("text_sample", [])[:60])
            toks.extend(v.get("element_tokens", []))
        traj = {"task_id": task_id, "site": task["site"],
                "profile_tokens": toks[:800],
                "steps": list(getattr(self, "_traj_steps", []))}
        self.hook("trajectory", **traj)
        return dict(self.m)

    # ---------------- internals ----------------
    def _remember(self, snap):
        """Track a visited observation for trajectory memory."""
        if not hasattr(self, "_visited"):
            self._visited = []
        el_toks = []
        for e in snap.get("elements", [])[:80]:
            el_toks.extend(_slug_tokens(e.get("text", ""))[:4])
        self._visited.append({"url_shape": snap.get("url_shape", ""),
                              "text_sample": _slug_tokens(
                                  snap.get("page_text", "")[:1200]),
                              "element_tokens": el_toks[:60]})

    def _ctx_of(self, cur, act):
        """Auto-derived content context of an action target (no hand labels)."""
        try:
            el = cur["elements"][act["target"]]
        except Exception:
            return {}
        return {"kind": act["kind"],
                "text_tokens": _slug_tokens(el.get("text", ""))[:8],
                "href_tokens": _slug_tokens(el.get("href", ""))[:8]}

    def _frag_meta(self, sub):
        entry = getattr(self, "_entry_snap", None) or {}
        return {
            "entry_url_shape": entry.get("url_shape", ""),
            "entry_url": entry.get("url", ""),
            "kws_producer": list(sub.get("keywords", [])),
            "steps_ctx": list(getattr(self, "_ctx_pairs", [])),
            "derived_by": "auto-context-v1",
        }

    def _run_subgoal(self, session, snap, sub, condition, task_id,
                     task_start=None, task_site=None):
        t0 = time.time()
        tried = set()           # (state_fp, kind, target_sig) failures this run
        steps_ok = []           # successful steps since subgoal start
        self._ctx_pairs = []
        self._entry_snap = snap
        self._edge_journal = []
        self._last_nav_key = None
        self._remember(snap)
        seen_fps = {self.store.fingerprint(snap)}
        cur = snap
        self.hook("subgoal_start", sig=sub.get("sig"), condition=condition)
        if sub["accept"](cur):   # already satisfied (session carry-over)
            self.m["subgoals_ok"] += 1
            self.hook("subgoal_done", sig=sub.get("sig"),
                      outcome="already_satisfied")
            return cur

        # ---- phase R: cached replay (with entry-state reset retry) ----
        if condition in ("inherit", "replay", "blind"):
            for attempt in range(2):
                frag = self._lookup(sub)
                if not (frag and frag["confidence"] >= CONF_MIN):
                    break
                ok_replay = True
                for step in frag["steps"]:
                    idx = self._find_by_sig(cur, step["target_sig"])
                    if idx is None:
                        ok_replay = False; break
                    act = {"kind": step["kind"], "target": idx,
                           "target_sig": step["target_sig"],
                           "value": step.get("value", "")}
                    prev_fp = self.store.fingerprint(cur)
                    ctx = self._ctx_of(cur, act)      # PRE-action element
                    post = self._exec(session, cur, act, task_id, reused=True)
                    cur = post
                    steps_ok.append(step)
                    self._ctx_pairs.append(ctx)
                    if post["last_action"].get("ok") is False:
                        ok_replay = False; break
                    if sub["accept"](cur):
                        break
                    if self.store.fingerprint(cur) == prev_fp and \
                            step["kind"] not in NO_EFFECT_EXEMPT:
                        ok_replay = False; break   # step had no effect
                if ok_replay and sub.get("wait_text"):
                    self._maybe_wait(session, cur, sub)
                if sub["accept"](cur):
                    self.m["subgoals_ok"] += 1
                    self.store.save_fragment(
                        sub["sig"], steps_ok,
                        frag.get("site") or self.site_hint or _site_of(session),
                        meta=self._frag_meta(sub))
                    self.hook("subgoal_done", sig=sub.get("sig"),
                              outcome="replay_ok" if attempt == 0
                              else "reset_replay_ok")
                    self.m["wall_ms"] += int((time.time() - t0) * 1000)
                    return cur
                # context mismatch: reset to the fragment's known entry region
                # once, then retry replay from there (novelty localized to glue)
                if attempt == 0 and task_start:
                    cur = session.goto(task_start, task_site or
                                       _site_of(session))
                    steps_ok.clear()
                    self.m["loads"] += 1
                    self.m["actions"] += 1
                    self.m["novel"] += 1
                else:
                    self.m["recoveries"] += 1   # degraded to exploration
                self.hook("subgoal_retry", sig=sub.get("sig"), attempt=attempt)

        # ---- phase E: exploration ----
        steps = 0
        hub_returns = 0
        stale_steps = 0   # actions since last NEW structural state
        while steps < EXPLORATION_STEPS and time.time() - t0 < WALL_S:
            if sub["accept"](cur):
                break
            cand_idx = self._rank(cur, sub, tried)
            if not cand_idx or stale_steps >= 6:
                # generic crawler prior, available EQUALLY in every condition
                # (including cold): dead-end OR churn (no new structural
                # state for 6 actions — e.g. flash-dismiss/login-submit
                # micro-cycles) -> return to the task entry region and
                # continue scanning. Charged as load + novel action. Uses
                # deterministic goto rather than browser history (run2c
                # lesson: history-back after a replay walks the replay
                # path, not the site structure).
                if task_start and hub_returns < MAX_HUB_RETURNS:
                    if self._last_nav_key:
                        tried.add(self._last_nav_key)
                        self._last_nav_key = None
                    cur = session.goto(task_start,
                                       task_site or _site_of(session))
                    self._remember(cur)
                    hub_returns += 1
                    stale_steps = 0
                    new_fp = self.store.fingerprint(cur) not in seen_fps
                    seen_fps.add(self.store.fingerprint(cur))
                    self.m["loads"] += 1
                    self.m["actions"] += 1
                    self.m["novel"] += 1
                    continue
                break
            idx, act = cand_idx[0]
            sig = act.get("target_sig")
            key = (self.store.fingerprint(cur), act["kind"], sig)
            prev_fp = self.store.fingerprint(cur)
            prev_url = cur["url"]
            ctx = self._ctx_of(cur, act)              # PRE-action element
            post = self._exec(session, cur, act, task_id, reused=False,
                              task=task_id)
            cur = post
            steps += 1
            self._remember(cur)
            if post["last_action"].get("ok") is False:
                self.m["failed"] += 1
                tried.add(key)
                continue
            steps_ok.append({"kind": act["kind"], "target_sig": sig,
                             **({"value": act["value"]} if act["kind"] in ("fill", "press") else {})})
            self._ctx_pairs.append(ctx)
            if sub["accept"](cur):
                break
            # async pages: wait for the marker instead of exploring away
            if sub.get("wait_text") and not elem_has(cur, sub["wait_text"]):
                self._maybe_wait(session, cur, sub)
                cur = session.snapshot(_site_of(session), settle_ms=0)
                self._remember(cur)
                if sub["accept"](cur):
                    break
            # fills don't change captured fingerprints: always retire them;
            # retire no-effect clicks too; retire clicks that re-enter an
            # already-visited structural state (cycle guard).
            post_fp = self.store.fingerprint(cur)
            if act["kind"] == "fill":
                tried.add(key)
            elif post_fp == prev_fp:
                tried.add(key)
            elif post_fp in seen_fps:
                tried.add(key)
            else:
                seen_fps.add(post_fp)
                stale_steps = 0
                continue
            stale_steps += 1

        ok = sub["accept"](cur)
        if not ok:
            ok = self._maybe_wait(session, cur, sub)
            cur = session.snapshot(_site_of(session), settle_ms=0)
            self._remember(cur)
            ok = ok or sub["accept"](cur)
        if ok:
            self.m["subgoals_ok"] += 1
            if steps_ok:
                distilled = self._distill_route(self._entry_snap, cur) or steps_ok
                self.store.save_fragment(sub["sig"], distilled,
                                         self.site_hint or _site_of(session),
                                         meta=self._frag_meta(sub))
                if sub.get("hint") == "pager":
                    tail = distilled[-1:] if distilled else steps_ok[-1:]
                    self.store.save_fragment("generic.paginate.next",
                                             tail,
                                             self.site_hint or _site_of(session),
                                             meta=self._frag_meta(sub))
                if any(f.get("hint_user") for f in sub["fills"]) if sub["fills"] else False:
                    d2 = self._distill_route(self._entry_snap, cur) or steps_ok
                    self.store.save_fragment("generic.form.login",
                                             d2,
                                             self.site_hint or _site_of(session),
                                             meta=self._frag_meta(sub))
        self.hook("subgoal_done", sig=sub.get("sig"),
                  outcome="explored_ok" if ok else "failed")
        self.m["wall_ms"] += int((time.time() - t0) * 1000)
        return cur

    def _lookup(self, sub):
        f = self.store.best_fragment(sub["sig"])
        if f:
            return f
        gen = GENERIC.get(sub.get("hint"))
        if sub["fills"]:
            gen = "generic.form.login"
        if gen:
            return self.store.best_fragment(gen)
        return None

    def _exec(self, session, cur, act, task_id, reused=False, task=None):
        """Execute, bookkeep costs, write transition to store."""
        self.m["actions"] += 1
        self.m["reused" if reused else "novel"] += 1
        if act["kind"] == "fill":
            act = dict(act); act["value"] = act.get("value", "")
        post = session.act(cur, act)
        if act["kind"] in ("goto",) or (
                post["url"] != cur["url"] and act["kind"] in ("click", "submit_enter")):
            self.m["loads"] += 1
        from_sid = self.store.upsert_state(cur)
        to_sid = self.store.upsert_state(post)
        # journal the experienced edge for route distillation
        try:
            self._edge_journal.append(
                (self.store.fingerprint(cur), act["kind"],
                 act.get("target_sig", ""),
                 str(act["value"])[:40] if act.get("value") else None,
                 self.store.fingerprint(post)))
        except AttributeError:
            pass
        if act["kind"] == "click" and post["url"] != cur["url"] and \
                post["last_action"].get("ok"):
            self._last_nav_key = (self.store.fingerprint(cur), "click",
                                  act.get("target_sig", ""))
        err = "" if post["last_action"].get("ok") else \
            post["last_action"].get("error", "unknown")[:60]
        self.store.record_transition(from_sid, 
            {"kind": act["kind"], "target_sig": act.get("target_sig", "")},
            to_sid, "failure" if err else "success", error_class=err,
            task_id=task_id or "", agent_id=f"{self.policy}")
        if hasattr(self, "_traj_steps"):
            step_rec = {"kind": act["kind"],
                        "target_sig": act.get("target_sig", "")}
            if act.get("value"):
                step_rec["value"] = str(act["value"])[:40]
            self._traj_steps.append(step_rec)
        return post

    def _find_by_sig(self, snap, sig):
        hits = [e["i"] for e in snap["elements"]
                if target_sig(e) == sig and e["enabled"]]
        return hits[0] if hits else None

    def _rank(self, snap, sub, tried):
        """Return ranked [(idx, action)] candidate list."""
        els = snap["elements"]; kws = sub["keywords"]; out = []
        fp = self.store.fingerprint(snap)
        hint = sub.get("hint")

        # typed fill actions first when form values are specified
        if sub["fills"] and snap["forms"]:
            fields = [e for e in els if e["tag"] == "input" and e["enabled"]]
            pw = [e for e in fields if e["type"] == "password"]
            txt = [e for e in fields if e["type"] in ("", "text", "email")]
            pending = []
            for f in sub["fills"]:
                pool = pw if f.get("hint_pass") else txt
                while pool:
                    e = pool.pop(0)
                    if (fp, "fill", target_sig(e)) not in tried:
                        pending.append((e["i"], {"kind": "fill", "target": e["i"],
                                                 "target_sig": target_sig(e),
                                                 "value": f["value"]}))
                        break
            subs = [e for e in els if e["type"] == "submit" and e["enabled"]]
            sub_e = next((e for e in subs
                          if (fp, "click", target_sig(e)) not in tried), None)
            if pending or sub_e:
                seq = list(pending)
                if sub_e:
                    seq.append((sub_e["i"], {"kind": "click", "target": sub_e["i"],
                                             "target_sig": target_sig(sub_e)}))
                elif pending:
                    last = pending[-1]
                    seq.append((last[0], {"kind": "submit_enter",
                                          "target": last[0],
                                          "target_sig": last[1]["target_sig"]}))
                return seq

        def clickable(e):
            return e["enabled"] and (e["tag"] in ("a", "button")
                                     or e["type"] == "submit"
                                     or e["role"] == "button" or e["cls"])

        # universal agent prior removed (run2c): the site-root escape hatch
        # is superseded by the generic back()-recovery mechanism; keeping a
        # root bonus made logo hops outrank content links and polluted
        # acquired fragments with via-home routes.

        # universal URL-shape prior (cycle 32670239235, shared by ALL
        # policies and conditions): among otherwise equal candidates,
        # prefer shallower href paths (content pages) over deep taxonomy
        # paths (index/classification pages). Uses only universal URL
        # structure; no site-specific vocabulary. Scale kept strictly
        # below one keyword hit.
        def depth_bonus(e):
            if not e.get("href"):
                return 0.0
            return max(0, 4 - e["href"].count("/")) * 0.3

        for e in els:
            if not clickable(e) or e.get("ext"):
                continue
            act = {"kind": "click", "target": e["i"], "target_sig": target_sig(e)}
            if self.policy == "G":
                # keyword hits must always dominate generic structural
                # priors (run2 lesson). Visible text/aria outweigh href
                # tokens (run2b lesson: empty-text carousel links whose
                # HREF merely contained a keyword outranked the real
                # navigation link when both channels were equal-weight).
                s = overlap(e["text"] + " " + e["aria"], kws) * 6
                s += 1 if e["tag"] == "button" else 0
                s += overlap(e["href"], kws) * 1
            else:                      # agentB: DOM order
                s = -e["i"] * 0.001
            s += depth_bonus(e)
            if hint == "pager":
                tl = (e["text"] or "").strip().lower()
                if tl in ("next", "»", "next →") or "next" in tl.split():
                    s += 10
            if hint == "check_first_input":
                pass
            if hint == "button_start":
                if (e["text"] or "").strip().lower() == "start":
                    s += 10
            if hint == "first_product_link":
                if "/catalogue/" in e["href"] and "category" not in e["href"]:
                    s += 8 + (1000 - min(e["y"], 1000)) / 1000
            if (fp, "click", act["target_sig"]) in tried:
                s -= 100
            out.append((s, e["i"], act))
        if hint == "check_first_input":
            boxes = [e for e in els if e["type"] == "checkbox" and e["enabled"]]
            if boxes:
                out.insert(0, (99, boxes[0]["i"],
                               {"kind": "check", "target": boxes[0]["i"],
                                "target_sig": target_sig(boxes[0])}))
        if hint == "input_press":
            # generic keyboard-press candidate: first visible enabled
            # text-like input; the pressed key comes from the task, not from
            # site-specific knowledge.
            fields = [e for e in els if e["tag"] == "input" and e["enabled"]
                      and e["type"] in ("", "text", "search")]
            if fields:
                act = {"kind": "press", "target": fields[0]["i"],
                       "target_sig": target_sig(fields[0]),
                       "value": sub.get("press_value", "A")}
                out.insert(0, (99, fields[0]["i"], act))
        out.sort(key=lambda x: -x[0])
        self.m["decision_points"] += len(out)
        return [(i, a) for _, i, a in out]

    def _maybe_wait(self, session, snap, sub):
        wt, ws = sub.get("wait_text"), sub.get("wait_s", 0)
        if not wt:
            return False
        t0 = time.time()
        cur = snap
        while time.time() - t0 < ws:
            if elem_has(cur, wt):
                return True
            time.sleep(0.7)
            cur = session.snapshot(_site_of(session), settle_ms=0)
        return elem_has(cur, wt)

    def _waited_ok(self, cur, sub):
        wt = sub.get("wait_text")
        return bool(wt) and elem_has(cur, wt)


def elem_has(snap, frag):
    f = frag.lower()
    if any(f in (e["text"] or "").lower() for e in snap["elements"]):
        return True
    return f in (snap.get("page_text") or "").lower()


def _slug_tokens(s, n=24):
    """Lowercase alphanumeric token stream for lexical memory layers."""
    out = []
    for w in "".join(c if c.isalnum() else " " for c in (s or "").lower()).split():
        if len(w) > 1:
            out.append(w[:n])
    return out


def _site_of(session):
    from urllib.parse import urlsplit
    return urlsplit(session.page.url).netloc
