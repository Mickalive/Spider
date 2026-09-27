"""Analysis stage for EXP-FRONTIER-36306528608.

Produces the DERIVED MEASUREMENTS from the RAW EVIDENCE in raw/, applying the frozen
analysis plan (prereg section 17) and the frozen decision rule (prereg section 14).

Nothing here creates new observations and nothing here relaxes a frozen threshold. Where a
frozen quantity could not be measured, it is emitted as null with the reason, never as 0.
"""

from __future__ import annotations

import json
import os
import random
import statistics
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EXPERIMENT_ID = "EXP-FRONTIER-36306528608"
PKG = os.path.join("research", "experiments", EXPERIMENT_ID)
RAW = os.path.join(PKG, "raw")
DERIVED = os.path.join(PKG, "derived")

BOOTSTRAP_RESAMPLES = 10000  # prereg 17.1
SEED = 36306528608


def read_jsonl(path: str) -> list[dict[str, Any]]:
    out = []
    if not os.path.exists(path):
        return out
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def site_clustered_bootstrap(site_rows: list[tuple[int, int]], rng: random.Random) -> list[float]:
    """Resample SITES with replacement (prereg 17.1: clustered by site)."""
    by_site: dict[str, list[tuple[int, int]]] = {}
    for num, den in site_rows:
        by_site.setdefault(f"s{len(by_site)}", []).append((num, den))
    keys = list(by_site)
    vals: list[float] = []
    for _ in range(BOOTSTRAP_RESAMPLES):
        num = den = 0
        for _ in range(len(keys)):
            for n, d in by_site[keys[rng.randrange(len(keys))]]:
                num += n
                den += d
        if den:
            vals.append(num / den)
    return vals


def pct(vals: list[float], p: float) -> float:
    if not vals:
        return float("nan")
    s = sorted(vals)
    k = (len(s) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def main() -> int:
    rng = random.Random(SEED)
    os.makedirs(DERIVED, exist_ok=True)

    calib = read_jsonl(os.path.join(RAW, "calibration.jsonl"))[0]
    screen = read_jsonl(os.path.join(RAW, "screen.jsonl"))
    objects = read_jsonl(os.path.join(RAW, "objects.jsonl"))
    classes = read_jsonl(os.path.join(RAW, "classification.jsonl"))
    idents = read_jsonl(os.path.join(RAW, "identifiers.jsonl"))
    pages = read_jsonl(os.path.join(RAW, "pages.jsonl"))
    http = read_jsonl(os.path.join(RAW, "http.jsonl"))
    token_stability = read_jsonl(os.path.join(RAW, "token_stability.jsonl"))
    pass2 = read_jsonl(os.path.join(RAW, "repeat_screen.jsonl"))

    crit = ("C1", "C2", "C3", "C4", "C5", "C6", "C7")
    qualifying = [r for r in screen if r.get("qualifies")]
    reached = [r for r in screen if (r.get("C6") or {}).get("reachable")]

    # ---------------- screen outcome (frozen) ---------------- #
    per_criterion = {
        c: {
            "n_pass": sum(1 for r in screen if r[c]["pass"]),
            "n_evaluated": len(screen),
            "pass_urls": [r["url"] for r in screen if r[c]["pass"]],
        }
        for c in crit
    }
    missing_by_site = {
        r["url"]: r.get("missing_ingredients", []) for r in screen if not r.get("qualifies")
    }

    # ---------------- same-unit prevalence (prereg 11) ---------------- #
    site_rows: list[tuple[int, int]] = []
    per_site_rf: list[dict[str, Any]] = []
    for r in screen:
        objs = [o for o in objects if o.get("site_url") == r["url"]]
        if not objs:
            per_site_rf.append({"site": r["url"], "n_action_gating_spans": 0,
                                "n_rederivable_spans": 0, "rederivable_fraction_site": None})
            continue
        n_red = sum(1 for o in objs if o.get("rederivable") is True)
        site_rows.append((n_red, len(objs)))
        per_site_rf.append({"site": r["url"], "n_action_gating_spans": len(objs),
                            "n_rederivable_spans": n_red,
                            "rederivable_fraction_site": n_red / len(objs)})

    tot_den = sum(d for _, d in site_rows)
    tot_num = sum(n for n, _ in site_rows)
    pooled = (tot_num / tot_den) if tot_den else None
    boot = site_clustered_bootstrap(site_rows, rng)
    rf_lo, rf_hi = pct(boot, 0.025), pct(boot, 0.975)
    # Equal-weight per-site average, the stratification prereg 11 requires.
    nonzero = [r["rederivable_fraction_site"] for r in per_site_rf
               if r["rederivable_fraction_site"] is not None]
    equal_weight = statistics.mean(nonzero) if nonzero else None

    # ---------------- controls / arm gating ---------------- #
    ARMS = ["RE_DERIVABLE", "CACHE_AND_REVALIDATE", "NULL_COST", "COLD_REEXPLORATION",
            "NO_MEMORY_DETERMINISTIC", "WITHIN_EPISODE_SCRATCHPAD", "ORACLE_PERFECT_TRANSFER"]
    arms_run = False
    arms_blocked_reason = (
        f"prereg section 6 admits the arm phase only on a qualifying site set; the frozen "
        f"screen admitted {len(qualifying)} of {len(screen)} frozen candidate sites "
        f"(minimum {3}), so no arm was executed. Arm metrics are null, NOT zero."
    )

    # ---------------- cost basis (prereg 8, body-sensitive) ---------------- #
    toks = [p["observation_tokens"] for p in pages]
    token_stats = {
        "unit": "cl100k_base tokens over the FULL body-sensitive MinimalObservation structure",
        "n_page_observations": len(toks),
        "mean": round(statistics.mean(toks), 1) if toks else None,
        "median": statistics.median(toks) if toks else None,
        "min": min(toks) if toks else None,
        "max": max(toks) if toks else None,
        "total": sum(toks) if toks else 0,
        "body_sensitive": True,
        "includes": ["url", "method", "status", "links", "forms", "inputs", "landmarks",
                     "headers", "body_sha256", "key_body_fields", "body_bytes"],
    }
    by_host: dict[str, list[int]] = {}
    for p in pages:
        by_host.setdefault(p["url"].split("/")[2], []).append(p["observation_tokens"])
    token_stats["by_host"] = {
        h: {"n": len(v), "mean": round(statistics.mean(v), 1), "median": statistics.median(v)}
        for h, v in sorted(by_host.items())
    }

    # ---------------- identifier inventory ---------------- #
    ident_types: dict[str, int] = {}
    ident_stability: dict[str, int] = {}
    for i in idents:
        ident_types[i["identifier_type"]] = ident_types.get(i["identifier_type"], 0) + 1
        st = i.get("stability", "unknown")
        ident_stability[st] = ident_stability.get(st, 0) + 1
    session_scoped = [i for i in idents if i.get("stability") == "session_scoped"]

    # ---------------- token stability probe ---------------- #
    ts = {}
    for r in token_stability:
        lab = r["probe_label"]
        fields = r["token_stability_by_field"]
        ts[lab] = {
            "url": r["url"],
            "sessions": r["n_sessions_with_value"] if False else len(r["sessions"]),
            "n_distinct_body_hashes": r["n_distinct_body_hashes"],
            "per_field": {
                f: {"n_distinct_values": v["n_distinct_values"],
                    "STABLE_ACROSS_INDEPENDENT_SESSIONS": v["STABLE_ACROSS_INDEPENDENT_SESSIONS"]}
                for f, v in fields.items()
            },
            "any_field_unstable": any(
                not v["STABLE_ACROSS_INDEPENDENT_SESSIONS"] for v in fields.values()
            ) if fields else None,
        }

    # ---------------- reproducibility ---------------- #
    pass1 = {r["url"]: {"objects": r.get("object_count", len(r.get("objects", []))),
                        "criteria": {c: r[c]["pass"] for c in crit},
                        "by_type": (r.get("C2") or {}).get("by_type")}
             for r in screen}
    repro = []
    for r in pass2:
        u = r["url"]
        p1 = pass1.get(u)
        if p1 is None:
            continue
        repro.append({
            "url": u,
            "pass1_objects": p1["objects"],
            "pass2_objects": r["objects_detected"],
            "objects_identical": p1["objects"] == r["objects_detected"],
            "by_type_identical": p1["by_type"] == r.get("by_type"),
            "criteria_identical": p1["criteria"] == r["criteria_pass"],
            "qualifies_pass1": p1["criteria"] and all(p1["criteria"].values()),
            "qualifies_pass2": r["qualifies"],
        })

    # ---------------- frozen decision rule (prereg 14) ---------------- #
    n_qual = len(qualifying)
    branch = None
    if n_qual < 3:
        branch = "ROW_1_screen_yields_lt_3_qualifying_sites"
    elif rf_hi < 0.5 and pooled is not None and pooled <= 0.3:
        branch = "ROW_2_supports"
    elif rf_lo > 0.6 and pooled is not None and pooled >= 0.8:
        branch = "ROW_3_falsifies"
    else:
        branch = "ROW_4_inconclusive"

    # Whether branch ROW_1's own stated interpretation survives this run's raw evidence.
    # prereg 4.4 asserts that <3 qualifying sites means "no action-gating structure exists
    # to require cross-episode state". This run observed real token-gated objects.
    row1_premise_falsified = (n_qual < 3 and tot_den > 0)

    out = {
        "experiment_id": EXPERIMENT_ID,
        "seed": SEED,
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "calibration": {
            "site": calib["calibration_site"],
            "pass": calib["calibration_pass"],
            "criteria": {c: calib["criteria"][c]["pass"] for c in crit},
            "c3_detail": calib["criteria"]["C3"],
            "root_form_input_names": calib["root_observation_forms"][0]["input_names"]
            if calib["root_observation_forms"] else [],
            "objects_detected": calib["objects_detected"],
            "prereg_claim_about_site": calib["prereg_claim_about_site"],
        },
        "screen": {
            "n_candidates": len(screen),
            "n_reachable": len(reached),
            "n_unreachable": [r["url"] for r in screen if not (r.get("C6") or {}).get("reachable")],
            "n_qualifying": n_qual,
            "qualifying_urls": [r["url"] for r in qualifying],
            "per_criterion": per_criterion,
            "missing_ingredients_by_site": missing_by_site,
        },
        "prevalence": {
            "definition_source": "prereg section 11 (same unit: span counts)",
            "numerator_unit": "count of action-gating spans re-derivable from one unconditional GET of the root observation",
            "denominator_unit": "count of action-gating spans",
            "total_action_gating_spans": tot_den,
            "total_rederivable_spans": tot_num,
            "pooled_rederivable_fraction": pooled,
            "pooled_ci95_lower": rf_lo,
            "pooled_ci95_upper": rf_hi,
            "equal_weight_per_site_mean": equal_weight,
            "per_site": per_site_rf,
            "is_frozen_primary_metric": False,
            "why_not_primary": (
                "The frozen primary metric is defined over the qualifying site set. The frozen "
                "screen admitted 0 sites, so this figure is a DIAGNOSTIC over all detected "
                "objects on all reachable frozen candidates, computed with the frozen prereg-11 "
                "protocol and the frozen same-unit numerator/denominator, but it is NOT the "
                "frozen primary metric and must not be read against the frozen thresholds."
            ),
        },
        "cost_basis": token_stats,
        "identifiers": {
            "n_detected": len(idents),
            "by_type": ident_types,
            "by_stability": ident_stability,
            "n_session_scoped": len(session_scoped),
            "session_scoped_sites": sorted({i["site"] for i in session_scoped}),
        },
        "token_stability_probe": ts,
        "reproducibility": {
            "second_live_pass_sites": len(repro),
            "rows": repro,
            "objects_identical_all": all(r["objects_identical"] for r in repro) if repro else None,
            "criteria_identical_all": all(r["criteria_identical"] for r in repro) if repro else None,
            "qualifying_stable": (all(r["qualifies_pass1"] == r["qualifies_pass2"] for r in repro)
                                  if repro else None),
        },
        "arms": {
            "arm_ids": ARMS,
            "executed": arms_run,
            "metrics": {a: None for a in ARMS},
            "reason": arms_blocked_reason,
        },
        "decision_rule": {
            "branch_mechanically_selected": branch,
            "n_qualifying_sites": n_qual,
            "min_required": 3,
            "row1_stated_interpretation": (
                "prereg 4.4 / section 14 row 1: <3 qualifying sites means re-derivable surface "
                "= 1.0 in this substrate class because no action-gating structure exists to "
                "require cross-episode state -> C-CROSSSITE falsified in this substrate"
            ),
            "row1_premise_falsified_by_this_run": row1_premise_falsified,
            "row1_premise_evidence": {
                "total_action_gating_spans_observed": tot_den,
                "sites_with_token_gated_objects": sorted(
                    {o["site_url"] for o in objects if o["gating_type"] == "csrf_token"}),
                "csrf_token_objects": sum(1 for o in objects if o["gating_type"] == "csrf_token"),
                "server_minted_tokens_unstable_across_sessions": [
                    k for k, v in ts.items() if v["any_field_unstable"]],
            },
            "hypothesis_H1": "rederivable_fraction < 0.3 on qualifying sites",
            "falsifier_F1": "rederivable_fraction > 0.8 on qualifying sites",
            "H1_evaluated": False,
            "F1_evaluated": False,
            "why_not_evaluated": (
                "Both H1 and F1 are defined over a qualifying site set of >= 3 sites. The frozen "
                "screen admitted 0, and the frozen calibration gate failed, so neither the "
                "hypothesis nor its falsifier is evaluable from this run."
            ),
        },
        "http": {
            "total_requests_logged": len(http),
            "by_method": {m: sum(1 for h in http if h["method"] == m)
                          for m in sorted({h["method"] for h in http})},
            "non_get_requests_sent": sum(1 for h in http if h["method"] != "GET"),
            "distinct_hosts": len({h["url"].split("/")[2] for h in http if "//" in h["url"]}),
        },
    }
    path = os.path.join(DERIVED, "analysis.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
    print(json.dumps({
        "calibration_pass": out["calibration"]["pass"],
        "n_qualifying": out["screen"]["n_qualifying"],
        "pooled_rf": out["prevalence"]["pooled_rederivable_fraction"],
        "ci": [out["prevalence"]["pooled_ci95_lower"], out["prevalence"]["pooled_ci95_upper"]],
        "spans": out["prevalence"]["total_action_gating_spans"],
        "obs_tokens_mean": out["cost_basis"]["mean"],
        "branch": out["decision_rule"]["branch_mechanically_selected"],
        "repro_objects_identical": out["reproducibility"]["objects_identical_all"],
        "non_get_requests_sent": out["http"]["non_get_requests_sent"],
    }, indent=1))
    print("->", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
