"""Frozen-design analysis stage for EXP-FRONTIER-37385647440.

Lane: frontier. Consumes the durable raw evidence written by
research/frontier/stationarity_37385647440.py and applies the frozen
spec.json decision_rule and the frozen prereg.md classification and cost
definitions. It performs NO network access: every number here is recomputable
from raw/http.jsonl, raw/observations.jsonl, raw/responses_cache/ and
derived/items.json without re-hitting a live network.

OUTPUTS
  derived/classification.json               frozen-rule primary classification
  derived/classification_sensitivity.json   the two disclosed frozen ambiguities
  derived/costs.json                        re-acquisition and re-derivation costs
  derived/analysis.json                     class distribution, bootstrap CIs,
                                           break-even, falsifier, controls
  raw/controls_verification.jsonl           per-control, per-item live verdicts
"""

from __future__ import annotations

import json
import math
import os
import random
import statistics
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP_DIR = os.path.join(ROOT, "research", "experiments", "EXP-FRONTIER-37385647440")
RAW_DIR = os.path.join(EXP_DIR, "raw")
DERIVED_DIR = os.path.join(EXP_DIR, "derived")
BOOTSTRAP_RESAMPLES = 10000
BOOTSTRAP_SEED = 37385647440
K = 5
MIN_DELAY = 60

CLASSES = ["session_invariant", "session_scoped", "request_scoped", "time_scoped", "rotating"]
NON_STATIONARY = ["request_scoped", "time_scoped", "rotating"]
STATIONARY = ["session_invariant", "session_scoped"]


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def line_hash(rec: dict) -> str:
    return __import__("hashlib").sha256(
        canonical_json({k: v for k, v in rec.items() if k != "observation_hash"}).encode()
    ).hexdigest()


def load_jsonl(path: str) -> list[dict]:
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def median(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def main() -> int:
    items_blob = json.load(open(os.path.join(DERIVED_DIR, "items.json"), encoding="utf-8"))
    items = items_blob["items"]
    cold = items_blob["cold"]
    delays = items_blob["inter_session_delays"]
    env = items_blob["environment"]

    http = load_jsonl(os.path.join(RAW_DIR, "http.jsonl"))

    # ---- per-session, per-URL observation token table (from raw evidence) ----
    url_tokens: dict[tuple, int] = {}
    url_body: dict[tuple, str] = {}
    url_status: dict[tuple, Any] = {}
    for r in http:
        if r.get("phase") != "stationarity" or r.get("replication") != 0:
            continue
        key = (r["site"], r["session"], r["url"])
        if r.get("ok"):
            url_tokens[key] = r["observation_tokens"]
            url_body[key] = r["body_sha256"]
            url_status[key] = r["status"]

    # ---- cold crawl index: url -> ordered position and cumulative cost -------
    cold_index: dict[str, dict] = {}
    for label, cd in cold.items():
        cum_tok = 0
        cum_req = 0
        for pe in cd["pages"]:
            cum_req += 1
            cum_tok += pe["tokens"] if pe["tokens"] is not None else 0
            cold_index[(label, pe["url"])] = {
                "fetch_order": pe["fetch_order"], "hop": pe["hop"],
                "tokens_up_to": cum_tok, "requests_up_to": cum_req,
                "page_tokens": pe["tokens"], "status": pe["status"],
            }
        cd["cold_total_requests"] = cum_req
        cd["cold_total_tokens"] = cum_tok
        cd["cold_pages_reached"] = len(cd["pages"])

    # ---- frozen classification ---------------------------------------------
    def per_session_reps(entry):
        return [r for r in entry.get("replications", [])
                if not r.get("secondary") and "replication" in r]

    def analyse(item, mode):
        """mode: 'pair' (primary, IC-01) or 'value_only' (sensitivity)."""
        obs_ok, absent, errors = [], [], []
        series_value, series_hash = [], []
        within = []
        for entry in item["per_session"]:
            reps = per_session_reps(entry)
            if len(reps) < 2 or any(not r.get("observed") for r in reps):
                obs_ok.append(False)
                absent.append(entry["session"])
                continue
            r0, r1 = reps[0], reps[1]
            if r0.get("value_extract_status") in ("absent", "error") or \
               r1.get("value_extract_status") in ("absent", "error"):
                obs_ok.append(False)
                (errors if r0.get("value_extract_status") == "error" else absent).append(
                    entry["session"])
                continue
            obs_ok.append(True)
            series_value.append(r0.get("value"))
            series_hash.append(r0.get("body_sha256"))
            within.append({
                "value": {r0.get("value"), r1.get("value")},
                "pair": {(r0.get("value"), r0.get("body_sha256")),
                         (r1.get("value"), r1.get("body_sha256"))},
            })
        out = {
            "n_sessions_observed": sum(1 for x in obs_ok if x),
            "n_sessions_required": K,
            "sessions_unobserved_or_unextractable": sorted(set(absent)),
            "sessions_extract_error": sorted(set(errors)),
            "n_distinct_values": None, "n_distinct_body_hashes": None,
            "n_distinct_within_session_values": None, "n_distinct_within_session_pairs": None,
            "stationarity_class": None, "rule_matched": None, "unclassifiable_reason": None,
            "values_series": series_value, "body_hash_series": series_hash,
        }
        if not all(obs_ok):
            out["unclassifiable_reason"] = (
                "designated element not extractable in one or more sessions "
                f"(sessions {sorted(set(absent))})" if absent or errors else
                "fewer than 2 observed replications in one or more sessions")
            return out
        dv = len(set(series_value))
        dh = len(set(series_hash))
        wv = sum(1 for w in within if len(w["value"]) > 1)
        wp = sum(1 for w in within if len(w["pair"]) > 1)
        out["n_distinct_values"] = dv
        out["n_distinct_body_hashes"] = dh
        out["n_distinct_within_session_values"] = wv
        out["n_distinct_within_session_pairs"] = wp
        # ---- frozen rule order, prereg section 4 ----
        if dv == 1 and dh == 1:
            out["stationarity_class"] = "session_invariant"
            out["rule_matched"] = "session_invariant: len(set(values))==1 and len(set(body_hashes))==1"
        elif mode == "pair" and all(len(w["pair"]) == 1 for w in within) and dv > 1:
            out["stationarity_class"] = "session_scoped"
            out["rule_matched"] = ("session_scoped: every within-session (value, body_hash) "
                                   "pair set has size 1 and values differ across sessions")
        elif mode == "value_only" and all(len(w["value"]) == 1 for w in within) and dv > 1:
            out["stationarity_class"] = "session_scoped"
            out["rule_matched"] = ("session_scoped, value-only variant: every within-session "
                                   "value set has size 1 and values differ across sessions")
        elif (wp > 1 if mode == "pair" else wv > 1):
            out["stationarity_class"] = "request_scoped"
            out["rule_matched"] = (
                "request_scoped: within-session (value, body_hash) varies" if mode == "pair"
                else "request_scoped, value-only variant: within-session value varies")
        else:
            # Frozen-table gap, not a class: value constant everywhere, body hash varies
            # across sessions only. prereg 4 rule 2's operational test requires
            # len(set(across_session_values)) > 1, which fails, so no class matches.
            out["stationarity_class"] = None
            out["rule_matched"] = None
            out["unclassifiable_reason"] = (
                "unmatched_by_frozen_table: value identical across all sessions "
                f"(n_distinct_values={dv}) while body hash differs across sessions "
                f"(n_distinct_body_hashes={dh}) and is constant within every session; "
                "prereg section 4 rule 2's operational test requires the values to "
                "differ, so no frozen class matches this item. NOT labelled rotating: "
                "prereg section 4 defines rotating as a session-scoped pattern, which "
                "requires values to differ across sessions.")
        # ---- IC-03: rules 4 and 5 are unreachable under the frozen tie-break ----
        out["time_scoped_reachable_under_frozen_order"] = False
        return out

    primary, sens = {}, {}
    for item in items:
        primary[item["item_id"]] = analyse(item, "pair")
        sens[item["item_id"]] = analyse(item, "value_only")

    # ---- IC-03 / IC-04 secondary post-hoc split of the session-scoped class ----
    for iid, p in primary.items():
        p = primary[iid]
        if p["stationarity_class"] != "session_scoped":
            continue
        vals = p["values_series"]
        repeats = [(i, j) for i in range(len(vals)) for j in range(i + 2, len(vals))
                   if vals[i] == vals[j]]
        p["post_hoc_unordered_class"] = "time_scoped" if repeats else "rotating"
        p["post_hoc_evidence"] = {
            "n_distinct_values": p["n_distinct_values"], "n_sessions": len(vals),
            "exact_value_recurrence_pairs_nonconsecutive": len(repeats),
            "statistic": ("a non-consecutive exact-value recurrence across sessions; "
                          "POST-HOC ONLY, not part of the frozen decision rule (IC-03/IC-04)"),
        }

    # ---- IC-02 secondary resource-level probe for the root nav-link controls ---
    resource_probe = {}
    for r in http:
        if r.get("phase") == "secondary_resource_probe" and r.get("ok"):
            resource_probe.setdefault(r["resource_for"], []).append(
                {"session": r["session"], "body_sha256": r["body_sha256"],
                 "final_url": r["final_url"], "status": r["status"]})
    for iid, rows in resource_probe.items():
        if iid in primary:
            hashes = [x["body_sha256"] for x in rows]
            primary[iid]["secondary_resource_probe"] = {
                "n_sessions": len(rows), "n_distinct_body_hashes": len(set(hashes)),
                "final_url": rows[0]["final_url"],
                "interpretation": ("resource-level body stability of the linked target; "
                                  "DISCLOSED SENSITIVITY under IC-02, never overrides the "
                                  "frozen primary classification"),
            }

    # ---- costs ---------------------------------------------------------------
    def bfs_path(label, page_url):
        cd = cold.get(label, {})
        if page_url == cd.get("root_url"):
            return [cd["root_url"]]
        path, cur = [], page_url
        seen = set()
        while cur and cur not in seen:
            seen.add(cur)
            path.append(cur)
            cur = cd.get("parent", {}).get(cur)
        return list(reversed(path))

    import hashlib as _h
    import re as _re
    _cb = _re.compile(r"\{rand16\}")

    def expand(url, session):
        return _cb.sub(lambda _: _h.sha256(f"{url}|{session}".encode()).hexdigest()[:16], url)

    costs = {}
    for item in items:
        iid = item["item_id"]
        label = item["site"]
        page_url = expand(item["page_url"], 0)
        path = bfs_path(label, page_url)
        per_sess_tok, per_sess_req, detail = [], [], []
        for s in range(K):
            toks = 0
            for u in path:
                toks += url_tokens.get((label, s, expand(u, s)), 0)
            n = sum(1 for u in path
                    if (label, s, expand(u, s)) in url_tokens)
            per_sess_tok.append(toks if n == len(path) else None)
            per_sess_req.append(len(path) if n == len(path) else None)
        cold_row = cold_index.get((label, page_url))
        if cold_row is not None:
            red_tok = cold_row["tokens_up_to"] if cold_row["status"] == 200 else None
            red_req = cold_row["requests_up_to"] if cold_row["status"] == 200 else None
            red_status = "reachable_in_bounded_cold_crawl"
        else:
            red_tok = red_req = None
            red_status = "not_reached_within_frozen_crawl_bounds"
        ra_tok = median(per_sess_tok)
        ra_req = median(per_sess_req)
        be_tok = None
        if ra_tok is not None and red_tok is not None:
            be_tok = math.ceil(ra_tok / (red_tok - ra_tok)) if red_tok > ra_tok else None
        be_req = None
        if ra_req is not None and red_req is not None:
            be_req = math.ceil(ra_req / (red_req - ra_req)) if red_req > ra_req else None
        costs[iid] = {
            "site": label, "page_url": page_url,
            "re_acquisition_path": path, "re_acquisition_request_count": len(path),
            "re_acquisition_tokens_per_session": per_sess_tok,
            "re_acquisition_requests_per_session": per_sess_req,
            "median_re_acquisition_tokens": ra_tok,
            "median_re_acquisition_requests": ra_req,
            "re_derivation_tokens": red_tok, "re_derivation_requests": red_req,
            "re_derivation_status": red_status,
            "re_derivation_at_least_full_cold_crawl_tokens":
                cold.get(label, {}).get("cold_total_tokens"),
            "re_derivation_at_least_full_cold_crawl_requests":
                cold.get(label, {}).get("cold_total_requests"),
            "break_even_reuse_count_tokens": be_tok,
            "break_even_reuse_count_requests": be_req,
            "break_even_null_reason": None if be_tok is not None else (
                "infinite (re_derivation <= re_acquisition)" if
                (ra_tok is not None and red_tok is not None) else
                "not computable: re_derivation unmeasured under the frozen crawl bounds"),
        }

    # ---- class distribution + site-clustered bootstrap -----------------------
    classified = [i["item_id"] for i in items if primary[i["item_id"]]["stationarity_class"]]
    unclass = [i["item_id"] for i in items
               if not primary[i["item_id"]]["stationarity_class"]]
    sites_of = {i["item_id"]: i["site"] for i in items}
    by_site: dict[str, list[str]] = {}
    for iid in sites_of:
        by_site.setdefault(sites_of[iid], []).append(iid)
    site_list = sorted(by_site)

    def counts_for(cls_map):
        c = {k: 0 for k in CLASSES}
        for iid, r in cls_map.items():
            if r["stationarity_class"]:
                c[r["stationarity_class"]] += 1
        return c

    c_primary = counts_for(primary)
    c_sens = counts_for(sens)

    rng = random.Random(BOOTSTRAP_SEED)
    boots_prop: dict[str, list[float]] = {k: [] for k in CLASSES}
    for _ in range(BOOTSTRAP_RESAMPLES):
        draw = [rng.choice(site_list) for _ in site_list]
        pool = [iid for s in draw for iid in by_site[s]
                if primary[iid]["stationarity_class"]]
        for k in CLASSES:
            boots_prop[k].append(
                (sum(1 for iid in pool if primary[iid]["stationarity_class"] == k) / len(pool))
                if pool else None)

    def ci(samples):
        vals = [x for x in samples if x is not None]
        if not vals:
            return None
        vals.sort()
        lo = vals[max(0, int(0.025 * len(vals)) - 1)]
        hi = vals[min(len(vals) - 1, int(0.975 * len(vals)))]
        return [lo, hi]

    n_classified = len(classified)
    dist = {}
    for k in CLASSES:
        dist[k] = {
            "count": c_primary[k],
            "proportion": (c_primary[k] / n_classified) if n_classified else None,
            "ci95_low": (ci(boots_prop[k]) or [None, None])[0],
            "ci95_high": (ci(boots_prop[k]) or [None, None])[1],
        }

    # ---- per-class economics -------------------------------------------------
    econ = {}
    for k in CLASSES:
        ids = [iid for iid in classified if primary[iid]["stationarity_class"] == k]
        if not ids:
            econ[k] = None
            continue
        ra_t = [costs[i]["median_re_acquisition_tokens"] for i in ids]
        ra_r = [costs[i]["median_re_acquisition_requests"] for i in ids]
        rd_t = [costs[i]["re_derivation_tokens"] for i in ids]
        rd_r = [costs[i]["re_derivation_requests"] for i in ids]
        m_ra_t, m_ra_r = median(ra_t), median(ra_r)
        m_rd_t, m_rd_r = median(rd_t), median(rd_r)
        be = None
        be_reason = None
        if m_ra_t is None or m_rd_t is None:
            be_reason = "not computable: at least one required median is unmeasured (null)"
        elif m_rd_t > m_ra_t:
            be = math.ceil(m_ra_t / (m_rd_t - m_ra_t))
        else:
            be_reason = "infinite (median re_derivation <= median re_acquisition)"
        be_item = [costs[i]["break_even_reuse_count_tokens"] for i in ids]
        # site-clustered CI on the class median re-acquisition tokens
        rng2 = random.Random(BOOTSTRAP_SEED + 1)
        ms = []
        for _ in range(BOOTSTRAP_RESAMPLES):
            draw = [rng2.choice(site_list) for _ in site_list]
            pool = [iid for s in draw for iid in by_site[s] if iid in ids]
            m = median([costs[i]["median_re_acquisition_tokens"] for i in pool])
            if m is not None:
                ms.append(m)
        econ[k] = {
            "n_items": len(ids), "sites": sorted({sites_of[i] for i in ids}),
            "median_re_acquisition_tokens": m_ra_t,
            "median_re_acquisition_requests": m_ra_r,
            "median_re_acquisition_tokens_ci95": ci(ms),
            "median_re_derivation_tokens": m_rd_t,
            "median_re_derivation_requests": m_rd_r,
            "break_even_reuse_count_tokens": be,
            "break_even_null_reason": be_reason,
            "median_item_level_break_even_reuse_count_tokens": median(be_item),
            "n_items_with_measurable_re_derivation":
                sum(1 for i in ids if costs[i]["re_derivation_tokens"] is not None),
        }

    # ---- falsifier -----------------------------------------------------------
    non_stat = sum(c_primary[k] for k in NON_STATIONARY)
    stat = sum(c_primary[k] for k in STATIONARY)
    majority_non_stationary = non_stat > stat
    maj_class = None
    if majority_non_stationary:
        present = [(c_primary[k], k) for k in NON_STATIONARY if c_primary[k] > 0]
        maj_class = max(present)[1] if present else None
    cost_condition = None
    cost_condition_reason = None
    if majority_non_stationary and maj_class:
        e = econ.get(maj_class)
        if e is None:
            cost_condition_reason = "majority non-stationary class has zero items"
        elif e["median_re_acquisition_tokens"] is None or e["median_re_derivation_tokens"] is None:
            cost_condition = None
            cost_condition_reason = (
                "median re_acquisition or median re_derivation for the majority "
                "non-stationary class is unmeasured (null), so the comparison the frozen "
                "rule requires cannot be evaluated in either direction")
        else:
            cost_condition = (e["median_re_acquisition_tokens"] >=
                              e["median_re_derivation_tokens"])
    falsifier_triggered = (majority_non_stationary and cost_condition is True)
    falsifier_state = ("NOT_TRIGGERED" if falsifier_triggered is False else
                       "TRIGGERED" if falsifier_triggered is True else "UNDEFINED")

    # ---- attainability audit of the frozen falsifier's cost condition ---------
    # The frozen COLD_REEXPLORATION baseline charges the cold agent every request of a
    # breadth-first crawl from root until the item's page is reached, while
    # re_acquisition charges the SHORTEST path to the same page. The BFS route to a
    # page is by construction a shortest path, so the cold route is never shorter and
    # never cheaper than the re-acquisition route. The frozen cost condition
    # (median re_acquisition >= median re_derivation) can therefore be TRUE only if
    # the cold agent pays strictly more for strictly more work, i.e. never.
    reach = [i for i in classified if costs[i]["re_derivation_tokens"] is not None]
    dominated = [i for i in reach
                 if costs[i]["re_derivation_tokens"] >= costs[i]["median_re_acquisition_tokens"]
                 and costs[i]["re_derivation_requests"] >= costs[i]["re_acquisition_request_count"]]
    attainability = {
        "question": ("Can the frozen falsifier's cost_condition ever be TRUE for any "
                     "item reachable within the frozen crawl bounds?"),
        "argument": ("For an item whose page is reached by the cold breadth-first crawl, "
                     "re_derivation_requests is the BFS fetch order of that page and "
                     "re_acquisition_request_count is the length of a shortest path to it. "
                     "The BFS route is itself a shortest path, so "
                     "re_derivation_requests >= re_acquisition_request_count, and "
                     "re_derivation_tokens is the token sum of a superset of those same "
                     "responses, so re_derivation_tokens >= re_acquisition_tokens. Hence "
                     "median_re_acquisition >= median_re_derivation is FALSE whenever both "
                     "medians are measured, and TRUE only where re_derivation is null, "
                     "which makes the comparison undefined rather than true."),
        "n_items_classified_with_measurable_re_derivation": len(reach),
        "n_items_where_re_derivation_ge_re_acquisition_on_both_units": len(dominated),
        "empirical_share": (len(dominated) / len(reach)) if reach else None,
        "frozen_falsifier_trigger_region_is_empty": len(reach) > 0 and len(dominated) == len(reach),
        "consequence": ("The frozen accept region for FALSIFIES has empty interior: no "
                        "execution of this frozen decision rule can produce outcome="
                        "FALSIFIES. The reachable branches are controls-fail "
                        "(MEASUREMENT_INVALID), SUPPORTS and MIXED."),
    }

    # ---- controls ------------------------------------------------------------
    ctrl_rows: list[dict] = []

    def control_items(ctrl_id, designated_only=False):
        return [i for i in items if i["ctrl_id"] == ctrl_id
                and (not designated_only or i.get("prereg_designated"))]

    pc = control_items("KNOWN_STATIONARY_CONTROL")
    pc_detail = []
    pc_pass = True
    for it in pc:
        r = primary[it["item_id"]]
        design = {"item_id": it["item_id"], "page_url": it["page_url"],
                  "prereg_designated": it.get("prereg_designated"),
                  "optional_per_prereg": it.get("optional"),
                  "final_url_observed": None, "http_statuses": [],
                  "value_extract_statuses": [], "n_sessions_observed": r["n_sessions_observed"],
                  "n_distinct_values": r["n_distinct_values"],
                  "n_distinct_body_hashes": r["n_distinct_body_hashes"],
                  "stationarity_class": r["stationarity_class"],
                  "verdict": None, "reason": None}
        reps = [x for e in it["per_session"] for x in per_session_reps(e)]
        design["http_statuses"] = [x.get("http_status") for x in reps if x.get("observed")]
        design["value_extract_statuses"] = [x.get("value_extract_status") for x in reps
                                            if x.get("observed")]
        if reps and reps[0].get("final_url"):
            design["final_url_observed"] = reps[0]["final_url"]
        if it.get("optional"):
            statuses = sorted({x for x in design["http_statuses"] if x})
            present = any(s is not None and s < 400 for s in design["http_statuses"])
            design["verdict"] = "SKIPPED"
            design["reason"] = (
                "prereg 6.1 conditional 'sitemap.xml (if exists, else skip)'; observed "
                f"HTTP statuses {statuses} -> the resource is "
                f"{'present' if present else 'ABSENT'}. A byte-stable 404 error page is "
                "NOT evidence of stationary state and is excluded from the verdict by "
                "the frozen conditional, not by producer choice.")
            pc_pass = pc_pass
        elif r["stationarity_class"] is None:
            design["verdict"] = "UNOBSERVABLE"
            design["reason"] = (
                f"designated element not present at the designated URL: "
                f"statuses={sorted(set(x for x in design['http_statuses'] if x))}, "
                f"extract_statuses={sorted(set(x for x in design['value_extract_statuses'] if x))}, "
                f"unclassifiable_reason={r['unclassifiable_reason']}")
            pc_pass = False
        elif r["stationarity_class"] == "session_invariant":
            design["verdict"] = "PASS"
            design["reason"] = ("exact-value and body-hash invariance across all "
                                f"{r['n_sessions_observed']} sessions")
        else:
            design["verdict"] = "FAIL"
            design["reason"] = (f"classified {r['stationarity_class']} "
                                f"(n_distinct_values={r['n_distinct_values']}, "
                                f"n_distinct_body_hashes={r['n_distinct_body_hashes']})")
            pc_pass = False
        pc_detail.append(design)
        ctrl_rows.append({"ctrl_id": "KNOWN_STATIONARY_CONTROL", **design})

    pn = control_items("REVERIFIED_NON_STATIONARY", designated_only=True)
    pn_detail = []
    pn_pass = True
    for it in pn:
        r = primary[it["item_id"]]
        d = {"item_id": it["item_id"], "page_url": it["page_url"], "prereg_designated": True,
             "http_statuses": [], "value_extract_statuses": [],
             "n_sessions_observed": r["n_sessions_observed"],
             "n_distinct_values": r["n_distinct_values"],
             "n_distinct_body_hashes": r["n_distinct_body_hashes"],
             "stationarity_class": r["stationarity_class"], "verdict": None, "reason": None}
        reps = [x for e in it["per_session"] for x in per_session_reps(e)]
        d["http_statuses"] = [x.get("http_status") for x in reps if x.get("observed")]
        d["value_extract_statuses"] = [x.get("value_extract_status") for x in reps
                                       if x.get("observed")]
        if r["stationarity_class"] is None:
            d["verdict"] = "UNOBSERVABLE"
            d["reason"] = (f"designated input not observable at the prereg-named URL: "
                           f"statuses={sorted(set(x for x in d['http_statuses'] if x))}; "
                           f"unclassifiable_reason={r['unclassifiable_reason']}")
            pn_pass = False
        elif r["stationarity_class"] in ("session_scoped", "rotating") and \
                (r["n_distinct_values"] or 0) >= 2:
            d["verdict"] = "PASS"
            d["reason"] = (f"classified {r['stationarity_class']} with "
                           f"{r['n_distinct_values']} distinct values across "
                           f"{r['n_sessions_observed']} sessions")
        elif r["stationarity_class"] == "session_invariant":
            d["verdict"] = "FAIL"
            d["reason"] = "classified session_invariant, which the prereg declares invalidating"
            pn_pass = False
        else:
            d["verdict"] = "FAIL"
            d["reason"] = (f"classified {r['stationarity_class']}; criterion requires "
                           "session_scoped or rotating with >=2 distinct values")
            pn_pass = False
        pn_detail.append(d)
        ctrl_rows.append({"ctrl_id": "REVERIFIED_NON_STATIONARY", **d})
    for it in [i for i in control_items("REVERIFIED_NON_STATIONARY")
               if not i.get("prereg_designated")]:
        r = primary[it["item_id"]]
        reps = [x for e in it["per_session"] for x in per_session_reps(e)]
        d = {"item_id": it["item_id"], "page_url": it["page_url"],
             "prereg_designated": False,
             "note": it.get("note"),
             "http_statuses": [x.get("http_status") for x in reps if x.get("observed")],
             "value_extract_statuses": [x.get("value_extract_status") for x in reps
                                        if x.get("observed")],
             "n_sessions_observed": r["n_sessions_observed"],
             "n_distinct_values": r["n_distinct_values"],
             "n_distinct_body_hashes": r["n_distinct_body_hashes"],
             "stationarity_class": r["stationarity_class"],
             "verdict": "INFORMATION_ONLY_NEVER_SUBSTITUTED",
             "reason": ("parent-cited URL for the same control item; executed for "
                        "information and excluded from the control verdict (IC-05)")}
        ctrl_rows.append({"ctrl_id": "REVERIFIED_NON_STATIONARY", **d})

    min_delay = min((d_["delay_seconds"] for d_ in delays), default=None)
    delay_pass = min_delay is not None and min_delay >= MIN_DELAY
    ctrl_rows.append({
        "ctrl_id": "INTER_SESSION_DELAY",
        "declared_delay_seconds": MIN_DELAY,
        "n_inter_session_intervals_measured": len(delays),
        "min_observed_delay_seconds": min_delay,
        "max_observed_delay_seconds": max((d_["delay_seconds"] for d_ in delays), default=None),
        "verdict": "PASS" if delay_pass else "FAIL",
        "reason": ("every inter-session interval between consecutive sessions of the same "
                   f"target is >= {MIN_DELAY} s" if delay_pass else
                   "at least one interval below the declared 60 s"),
        "evidence_ref": "raw/session_timing.jsonl"})

    null_items = control_items("NULL_STATIONARITY_ARM")
    null_detail = []
    null_pass = False
    for it in null_items:
        r = primary[it["item_id"]]
        reps = [x for e in it["per_session"] for x in per_session_reps(e)]
        fired = r["stationarity_class"] in ("request_scoped", "rotating")
        d = {"item_id": it["item_id"], "page_url": it["page_url"],
             "http_statuses": [x.get("http_status") for x in reps if x.get("observed")],
             "value_extract_statuses": [x.get("value_extract_status") for x in reps
                                        if x.get("observed")],
             "n_sessions_observed": r["n_sessions_observed"],
             "n_distinct_values": r["n_distinct_values"],
             "stationarity_class": r["stationarity_class"],
             "arm_fired": bool(fired),
             "verdict": "FIRED" if fired else ("NOT_FIRED" if r["stationarity_class"]
                                                 else "UNOBSERVABLE")}
        null_pass = null_pass or fired
        null_detail.append(d)
        ctrl_rows.append({"ctrl_id": "NULL_STATIONARITY_ARM", **d})
    null_verdict = "PASS" if null_pass else "FAIL"

    controls = {
        "KNOWN_STATIONARY_CONTROL": {
            "expected_behavior": ("ALL non-optional designated items classified "
                                  "session_invariant with exact-value and body-hash "
                                  "equality across all 5 sessions"),
            "status": "PASS" if pc_pass else "FAIL",
            "metric_value": c_primary["session_invariant"],
            "items": pc_detail, "evidence_ref": "raw/observations.jsonl",
        },
        "REVERIFIED_NON_STATIONARY": {
            "expected_behavior": ("ALL designated items classified session_scoped or "
                                  "rotating with >= 2 distinct values across 5 sessions; "
                                  "any session_invariant verdict invalidates the run"),
            "status": "PASS" if pn_pass else "FAIL",
            "metric_value": None, "items": pn_detail,
            "evidence_ref": "raw/observations.jsonl",
        },
        "INTER_SESSION_DELAY": {
            "expected_behavior": f"all inter-session delays >= {MIN_DELAY} s",
            "status": "PASS" if delay_pass else "FAIL",
            "metric_value": min_delay,
            "items": [], "evidence_ref": "raw/session_timing.jsonl",
        },
        "NULL_STATIONARITY_ARM": {
            "expected_behavior": ("at least one designated null item classified "
                                  "request_scoped or rotating, proving the arm can fire"),
            "status": null_verdict,
            "metric_value": sum(1 for d in null_detail if d["arm_fired"]),
            "items": null_detail, "evidence_ref": "raw/observations.jsonl",
        },
    }
    all_controls_pass = all(v["status"] == "PASS" for v in controls.values())

    ctrl_rows.append({
        "ctrl_id": "PRE_FREEZE_CONTROL_VERIFICATION_GATE",
        "expected_behavior": ("spec.json.controls_pre_freeze_verification must carry "
                              "status PASS with verified_at and evidence_ref for all four "
                              "controls BEFORE freeze.json is created (prereg section 7 "
                              "and section 14)"),
        "status": "FAIL",
        "metric_value": 0,
        "items": [],
        "reason": ("at freeze time all four entries in spec.json"
                   ".controls_pre_freeze_verification were status=PENDING with "
                   "verified_at=null and evidence_ref=null, while freeze.json existed "
                   "with frozen_at=2026-10-05T23:05:10.661240+00:00. The live control "
                   "verification the mandate required was performed by EXECUTE instead, "
                   "which is a DESIGN-phase process defect, not a substrate failure."),
        "evidence_ref": "research/experiments/EXP-FRONTIER-37385647440/spec.json"})
    controls["PRE_FREEZE_CONTROL_VERIFICATION_GATE"] = {
        "expected_behavior": ("all four pre-freeze controls verified live and PASS before "
                              "freeze.json was created"),
        "status": "FAIL", "metric_value": 0, "items": [],
        "evidence_ref": "spec.json.controls_pre_freeze_verification",
    }
    controls_pass = all(v["status"] == "PASS" for k, v in controls.items()
                        if k != "PRE_FREEZE_CONTROL_VERIFICATION_GATE")

    with open(os.path.join(RAW_DIR, "controls_verification.jsonl"), "w",
              encoding="utf-8") as fh:
        for row in ctrl_rows:
            row = dict(row)
            row["experiment_id"] = "EXP-FRONTIER-37385647440"
            row["observation_hash"] = line_hash(row)
            fh.write(canonical_json(row) + "\n")

    # ---- write derived outputs ----------------------------------------------
    def dump(name, obj):
        with open(os.path.join(DERIVED_DIR, name), "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=1)

    dump("classification.json", {
        "experiment_id": "EXP-FRONTIER-37385647440",
        "rule_source": "prereg.md section 4, frozen rule order, first match wins",
        "primary_mode": "pair (IC-01)",
        "time_scoped_and_rotating_reachable_under_frozen_order": False,
        "items": primary,
    })
    dump("classification_sensitivity.json", {
        "experiment_id": "EXP-FRONTIER-37385647440",
        "variant_1_value_only_within_session_test_IC_01": sens,
        "variant_2_resource_level_probe_IC_02": {
            k: v for k, v in resource_probe.items()},
    })
    dump("costs.json", {
        "experiment_id": "EXP-FRONTIER-37385647440",
        "tokenizer": TOKENIZER_LABEL,
        "cold_crawl_summary": {
            label: {"root_url": cd["root_url"], "final_root": cd["final_root"],
                    "root_redirected_off_nominal_host": cd["root_redirected"],
                    "cold_total_requests": cd["cold_total_requests"],
                    "cold_total_tokens": cd["cold_total_tokens"],
                    "n_candidates_detected": cd.get("n_candidates_detected")}
            for label, cd in cold.items()},
        "per_item": costs,
    })

    analysis = {
        "experiment_id": "EXP-FRONTIER-37385647440",
        "lane": "frontier", "environment": env,
        "denominators": {
            "items_total": len(items),
            "items_discovered_and_admitted": sum(1 for i in items if not i["is_control"]),
            "items_control_declared": sum(1 for i in items if i["is_control"]),
            "items_classified": n_classified,
            "items_unclassifiable": len(unclass),
            "sites_with_at_least_one_classified_item": len(
                {sites_of[iid] for iid in classified}),
            "frozen_floor_items": 20, "frozen_floor_sites": 4,
            "meets_frozen_floor_items": n_classified >= 20,
            "meets_frozen_floor_sites": len({sites_of[iid] for iid in classified}) >= 4,
        },
        "class_distribution": dist,
        "class_distribution_value_only_sensitivity": {
            k: {"count": c_sens[k],
                "proportion": (c_sens[k] / sum(c_sens.values())) if sum(c_sens.values())
                else None}
            for k in CLASSES},
        "bootstrap": {"resamples": BOOTSTRAP_RESAMPLES, "seed": BOOTSTRAP_SEED,
                      "unit": "site", "sites": site_list},
        "re_acquisition_economics_per_class": econ,
        "falsifier": {
            "frozen_text": spec_falsifier_text(),
            "majority_non_stationary": majority_non_stationary,
            "n_non_stationary": non_stat, "n_stationary": stat,
            "majority_non_stationary_class": maj_class,
            "cost_condition": cost_condition,
            "cost_condition_reason": cost_condition_reason,
            "falsifier_triggered": falsifier_triggered,
            "falsifier_state": falsifier_state,
            "attainability_audit": attainability,
        },
        "controls": controls,
        "controls_pass": controls_pass,
        "controls_pass_note": ("the frozen controls_gate counts the FOUR pre-freeze controls. "
                               "PRE_FREEZE_CONTROL_VERIFICATION_GATE is reported separately "
                               "as a process finding and is excluded from that count, but it "
                               "is itself a FAIL of the frozen prereg section 7 precondition."),
        "token_to_latency": None, "token_to_dollar": None,
        "retrieval_baseline_exercised": False,
        "oracle_perfect_transfer_exercised": False,
        "non_get_requests_sent": 0,
        "get_requests_sent": sum(1 for r in http),
        "inter_session_delays": delays,
    }
    dump("analysis.json", analysis)
    print(json.dumps({
        "items": len(items), "classified": n_classified, "unclassifiable": len(unclass),
        "class_counts": c_primary, "value_only_counts": c_sens,
        "controls_pass": controls_pass,
        "control_statuses": {k: v["status"] for k, v in controls.items()},
        "falsifier_state": falsifier_state,
        "majority_non_stationary": majority_non_stationary,
        "maj_class": maj_class, "cost_condition": cost_condition,
        "min_delay": min_delay,
    }, indent=1))
    return 0


TOKENIZER_LABEL = "cl100k_base (tiktoken, NOT declared in pyproject.toml)"


def spec_falsifier_text() -> str:
    p = os.path.join(EXP_DIR, "spec.json")
    return json.load(open(p, encoding="utf-8"))["falsifier"]


if __name__ == "__main__":
    sys.exit(main())