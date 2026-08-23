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

MAX_CLICKS, MAX_LOADS, WALL_S = 30, 16, 80
GENERIC = {"pager": "generic.paginate.next"}
CONF_MIN = 0.35


def overlap(text, kws):
    t = (text or "").lower()
    return sum(1 for k in kws if k and k.lower() in t)


class Explorer:
    def __init__(self, store: Store, policy="G"):
        self.store = store
        self.policy = policy
        self.m = self._zero()

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
        snap = session.goto(task["start"], task["site"])
        self.m["loads"] += 1
        start_sid = self.store.upsert_state(snap)
        for sub in task["subgoals"]:
            self.m["subgoals_total"] += 1
            snap = self._run_subgoal(session, snap, sub, condition, task_id,
                                     task["start"], task["site"])
        self.m["wall_ms"] += int((time.time() - t0) * 1000)
        return dict(self.m)

    # ---------------- internals ----------------
    def _run_subgoal(self, session, snap, sub, condition, task_id,
                     task_start=None, task_site=None):
        t0 = time.time()
        tried = set()           # (state_fp, kind, target_sig) failures this run
        steps_ok = []           # successful steps since subgoal start
        cur = snap
        if sub["accept"](cur):   # already satisfied (session carry-over)
            self.m["subgoals_ok"] += 1
            return cur

        # ---- phase R: cached replay (with entry-state reset retry) ----
        if condition in ("inherit", "replay"):
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
                    post = self._exec(session, cur, act, task_id, reused=True)
                    cur = post
                    steps_ok.append(step)
                    if post["last_action"].get("ok") is False:
                        ok_replay = False; break
                    if sub["accept"](cur):
                        break
                    if self.store.fingerprint(cur) == prev_fp and step["kind"] not in ("fill", "check"):
                        ok_replay = False; break   # step had no effect
                if ok_replay and sub.get("wait_text"):
                    self._maybe_wait(session, cur, sub)
                if sub["accept"](cur):
                    self.m["subgoals_ok"] += 1
                    self.store.save_fragment(sub["sig"], steps_ok, frag["site"])
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

        # ---- phase E: exploration ----
        steps = 0
        while steps < MAX_CLICKS * 2 and time.time() - t0 < WALL_S:
            if sub["accept"](cur):
                break
            cand_idx = self._rank(cur, sub, tried)
            if not cand_idx:
                break
            idx, act = cand_idx[0]
            sig = act.get("target_sig")
            key = (self.store.fingerprint(cur), act["kind"], sig)
            prev_fp = self.store.fingerprint(cur)
            post = self._exec(session, cur, act, task_id, reused=False,
                              task=task_id)
            cur = post
            steps += 1
            if post["last_action"].get("ok") is False:
                self.m["failed"] += 1
                tried.add(key)
                continue
            steps_ok.append({"kind": act["kind"], "target_sig": sig,
                             **({"value": act["value"]} if act["kind"] == "fill" else {})})
            if sub["accept"](cur):
                break
            # async pages: wait for the marker instead of exploring away
            if sub.get("wait_text") and not elem_has(cur, sub["wait_text"]):
                self._maybe_wait(session, cur, sub)
                cur = session.snapshot(_site_of(session), settle_ms=0)
                if sub["accept"](cur):
                    break
            # fills don't change captured fingerprints: always retire them;
            # retire no-effect clicks too
            if act["kind"] == "fill" or self.store.fingerprint(cur) == prev_fp:
                tried.add(key)

        ok = sub["accept"](cur)
        if not ok:
            ok = self._maybe_wait(session, cur, sub)
            cur = session.snapshot(_site_of(session), settle_ms=0)
            ok = ok or sub["accept"](cur)
        if ok:
            self.m["subgoals_ok"] += 1
            if steps_ok:
                self.store.save_fragment(sub["sig"], steps_ok, _site_of(session))
                if sub.get("hint") == "pager":
                    self.store.save_fragment("generic.paginate.next",
                                             steps_ok[-1:], _site_of(session))
                if any(f.get("hint_user") for f in sub["fills"]) if sub["fills"] else False:
                    self.store.save_fragment("generic.form.login",
                                             steps_ok, _site_of(session))
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
        err = "" if post["last_action"].get("ok") else \
            post["last_action"].get("error", "unknown")[:60]
        self.store.record_transition(from_sid, 
            {"kind": act["kind"], "target_sig": act.get("target_sig", "")},
            to_sid, "failure" if err else "success", error_class=err,
            task_id=task_id or "", agent_id=f"{self.policy}")
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

        # universal agent prior: when deep in a site, the site-root link
        # is a known escape hatch (costs an action like any other).
        # Above no-keyword candidates (+0/+1), below any keyword hit (>=+3).
        root_bonus = 2

        for e in els:
            if not clickable(e) or e.get("ext"):
                continue
            act = {"kind": "click", "target": e["i"], "target_sig": target_sig(e)}
            if self.policy == "G":
                s = overlap(e["text"] + " " + e["aria"] + " " + e["href"], kws) * 3
                s += 1 if e["tag"] == "button" else 0
                s += overlap(e["href"], kws) * 2
            else:                      # agentB: DOM order
                s = -e["i"] * 0.001
            if e["href"] in ("/", "#") or \
                    (e["text"] or "").lower() in ("home", "quotes to scrap",
                                                  "books to scrape"):
                s += root_bonus
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


def _site_of(session):
    from urllib.parse import urlsplit
    return urlsplit(session.page.url).netloc
