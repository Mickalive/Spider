#!/usr/bin/env python3
"""
Emit result.json and provenance.json for EXP-FRONTIER-37385647440.

Every numeric field is read from the frozen-design analyzer's derived artifacts.
Nothing here re-derives a measurement and nothing here re-interprets the
frozen decision rule: the status/outcome pair is taken from
spec.json decision_rule.outcome_mapping.CONTROLS_FAIL, applied to the
analyzer's controls_pass boolean.

Reads:  derived/*.json, raw/controls_verification.jsonl (frozen inputs only
        for identity/rule cross-reference)
Writes: result.json, provenance.json   (never touches frozen inputs)
"""
import hashlib
import json
import os
import platform
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "..", "experiments", "EXP-FRONTIER-37385647440")
EXP = os.path.normpath(EXP)
RAW = os.path.join(EXP, "raw")
DER = os.path.join(EXP, "derived")


def load(p):
    with open(os.path.join(EXP, p), encoding="utf-8") as fh:
        return json.load(fh)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def jsonl(p):
    out = []
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


spec = load("spec.json")
request = load("request.json")
with open(os.path.join(EXP, "prereg.md"), encoding="utf-8") as _fh:
    prereg_text = _fh.read()
freeze = load("freeze.json")
analysis = load("derived/analysis.json")
costs = load("derived/costs.json")
manifest = load("derived/run_manifest.json")
sens = load("derived/classification_sensitivity.json")
cls = load("derived/classification.json")
items = load("derived/items.json")
cv = jsonl(os.path.join(RAW, "controls_verification.jsonl"))

CLASSES = ["session_invariant", "session_scoped", "request_scoped", "time_scoped", "rotating"]
DEN = analysis["denominators"]
FALS = analysis["falsifier"]
class_counts = {k: analysis["class_distribution"][k]["count"] for k in CLASSES}
value_only = analysis["class_distribution_value_only_sensitivity"]
value_only_unmatched = DEN["items_classified"] - sum(value_only[k]["count"] for k in CLASSES)
min_delay = min(d["delay_seconds"] for d in analysis["inter_session_delays"])
reach = {}
for _v in costs["per_item"].values():
    reach[_v["re_derivation_status"]] = reach.get(_v["re_derivation_status"], 0) + 1
K_SESSIONS = items["constants"]["K_SESSIONS"]
MAX_HOPS = items["constants"]["MAX_HOPS"]

# ---------------------------------------------------------------- identity
FROZEN_FILES = ["request.json", "spec.json", "prereg.md", "freeze.json"]
frozen_hashes = {f: sha256_file(os.path.join(EXP, f)) for f in FROZEN_FILES}
for f, rec in freeze["hashes"].items():
    assert frozen_hashes[f] == rec, f"frozen file {f} hash mismatch: {frozen_hashes[f]} != {rec}"

# ---------------------------------------------------------------- controls
CTRL_EXPECTED = {
    "KNOWN_STATIONARY_CONTROL":
        "All designated items classified as session_invariant with exact-value and "
        "body-hash equality across all K=5 sessions (spec.positive_control).",
    "REVERIFIED_NON_STATIONARY":
        "The prereg-named authenticity_token anchors must classify as session_scoped "
        "or rotating (>=2 distinct values) across K=5 sessions.",
    "INTER_SESSION_DELAY":
        "Minimum measured inter-session delay >= 60 s, so a session_scoped value "
        "change cannot be attributed to the declared delay window.",
    "NULL_STATIONARITY_ARM":
        "At least one designated null probe must classify as non-stationary, proving "
        "the classifier discriminates.",
}

# aggregate the live per-item verdicts into the five stable control identities
ctrl_out = {}
for cid, expected in CTRL_EXPECTED.items():
    all_rows = [r for r in cv if r["ctrl_id"] == cid]
    # only prereg-designated rows can contribute to the frozen verdict; a parent-cited
    # anchor executed for information is never substituted (IC-05).
    rows = [r for r in all_rows if r.get("prereg_designated") is not False]
    info = [r for r in all_rows if r.get("prereg_designated") is False]
    passing = [r for r in rows if r.get("verdict") in ("PASS", "FIRED")]
    failing = [r for r in rows if r.get("verdict") in ("FAIL", "NOT_FIRED")]
    unobs = [r for r in rows if r.get("verdict") == "UNOBSERVABLE"]
    skipped = [r for r in rows if r.get("verdict") == "SKIPPED"]
    status = analysis["controls"][cid]["status"]
    entry = {
        "expected": expected,
        "observed": None,
        "verdict": status,
        "n_items_designated": len(rows),
        "n_designated_passing": len(passing),
        "n_designated_failing": len(failing),
        "n_designated_unobservable": len(unobs),
        "n_items_information_only_never_substituted": len(info),
        "evidence_ref": "raw/controls_verification.jsonl",
        "frozen_pre_freeze_status": spec["controls_pre_freeze_verification"][cid]["status"],
    }
    if cid == "INTER_SESSION_DELAY":
        d = rows[0]
        entry["observed"] = {
            "min_inter_session_delay_seconds": d["min_observed_delay_seconds"],
            "max_inter_session_delay_seconds": d["max_observed_delay_seconds"],
            "n_inter_session_intervals_measured": d["n_inter_session_intervals_measured"],
            "required_minimum_seconds": spec["controls_pre_freeze_verification"][cid]["delay_seconds"],
        }
    elif cid == "NULL_STATIONARITY_ARM":
        entry["observed"] = {
            "probe_classifications": {r["item_id"].split("|")[-1]: r.get("stationarity_class")
                                      for r in rows if r.get("ctrl_id") == cid},
            "n_probes_fired_non_stationary": len(passing),
            "class_demonstration": "httpbin.org /uuid (dv=5 across sessions AND dv=5 within "
                                   "a single session) and /headers X-Request-Id (explicit "
                                   "prng fallback, dv=5 across sessions).",
        }
    else:
        entry["observed"] = {
            "item_verdicts": [
                {"item_id": r["item_id"], "prereg_designated": r.get("prereg_designated"),
                 "optional_per_prereg": r.get("optional_per_prereg"),
                 "verdict": r.get("verdict"),
                 "stationarity_class": r.get("stationarity_class"),
                 "http_statuses": sorted({s for s in r.get("http_statuses", []) if s}),
                 "n_distinct_values": r.get("n_distinct_values"),
                 "n_distinct_body_hashes": r.get("n_distinct_body_hashes"),
                 "reason": r.get("reason")}
                for r in rows
            ],
        }
    if skipped:
        entry["skipped_items"] = [
            {"item_id": r["item_id"], "reason": r["reason"]} for r in skipped]
    if info:
        entry["information_only_items"] = [
            {"item_id": r["item_id"], "reason": r["reason"]} for r in info]
    ctrl_out[cid] = entry

ctrl_out["PRE_FREEZE_CONTROL_VERIFICATION_GATE"] = {
    "expected": "spec.json controls_pre_freeze_verification must record a non-PENDING "
                "verified status with an evidence_ref for all four controls before "
                "freeze.json exists (prereg.md sections 7 and 14).",
    "observed": spec["controls_pre_freeze_verification"],
    "verdict": analysis["controls"]["PRE_FREEZE_CONTROL_VERIFICATION_GATE"]["status"],
    "n_items_executed": 4,
    "evidence_ref": "spec.json#controls_pre_freeze_verification",
    "note": "Process-validity finding, reported separately from the four measured "
            "control arms; not one of the four controls in the frozen controls_gate.",
}

controls_pass = bool(analysis["controls_pass"])
falsifier_triggered = bool(FALS["falsifier_triggered"])

# apply the frozen outcome mapping, do not re-derive it
mapping = spec["decision_rule"]["outcome_mapping"]
if not controls_pass:
    status, outcome = "MEASUREMENT_INVALID", "INCONCLUSIVE"
    branch = "CONTROLS_FAIL"
elif falsifier_triggered:
    status, outcome = "COMPLETE", "FALSIFIES"
    branch = "FALSIFIER_TRIGGERED"
else:
    status, outcome = "COMPLETE", "SUPPORTS"
    branch = "FALSIFIER_NOT_TRIGGERED"
assert mapping[branch].startswith(f"status={status}"), \
    f"frozen mapping for {branch} is {mapping[branch]!r}, producer chose {status}"

# ---------------------------------------------------------------- metrics
econ = analysis["re_acquisition_economics_per_class"]
metrics = {
    "class_distribution": {
        "metric_id": spec["decision_rule"]["primary_classification"]["metric"],
        "type": spec["decision_rule"]["primary_classification"]["type"],
        "unit": "count of admitted state items",
        "denominator_items_classified": DEN["items_classified"],
        "per_class": analysis["class_distribution"],
        "bootstrap": {"method": "site_clustered_percentile", "resamples": 10000,
                      "seed": spec["experiment_id"]},
        "frozen_pool_note": "hand-picked credential-free public HTTP pool, NOT Web prevalence "
                            "(spec.measurement_validity.target_pool).",
    },
    "break_even_reuse_count_per_class": {
        "metric_id": spec["decision_rule"]["re_acquisition_economics"]["metric"],
        "type": spec["decision_rule"]["re_acquisition_economics"]["type"],
        "unit": "reuses (dimensionless count)",
        "baseline_id": "COLD_REEXPLORATION",
        "tokenizer": "cl100k_base",
        "per_class": {
            k: (None if econ.get(k) is None else {
                "n_items": econ[k]["n_items"],
                "sites": econ[k]["sites"],
                "median_re_acquisition_tokens": econ[k]["median_re_acquisition_tokens"],
                "median_re_acquisition_tokens_ci95": econ[k]["median_re_acquisition_tokens_ci95"],
                "median_re_acquisition_requests": econ[k]["median_re_acquisition_requests"],
                "median_re_derivation_tokens": econ[k]["median_re_derivation_tokens"],
                "median_re_derivation_requests": econ[k]["median_re_derivation_requests"],
                "break_even_reuse_count_tokens": econ[k]["break_even_reuse_count_tokens"],
                "break_even_null_reason": econ[k]["break_even_null_reason"],
                "median_item_level_break_even_reuse_count_tokens":
                    econ[k]["median_item_level_break_even_reuse_count_tokens"],
                "n_items_with_measurable_re_derivation":
                    econ[k]["n_items_with_measurable_re_derivation"],
                "median_denominators": {
                    "re_acquisition_median_over_n_items": econ[k]["n_items"],
                    "re_derivation_median_over_n_items":
                        econ[k]["n_items_with_measurable_re_derivation"],
                    "denominators_match": econ[k]["n_items"] == econ[k]["n_items_with_measurable_re_derivation"],
                },
            }) for k in CLASSES
        },
        "oracle_perfect_transfer_baseline": "NOT_AVAILABLE for 29 of 29 classified items: "
                                            "0 items were classified session_invariant with a "
                                            "measured re_acquisition cost strictly below "
                                            "re-derivation cost (all 12 session_invariant "
                                            "items have re_acquisition == re_derivation), so "
                                            "the ORACLE_PERFECT_TRANSFER break-even is null "
                                            "for every item (spec.baselines).",
        "retrieval_baseline": "NOT_EXERCISED (no prior episodes in this transaction); "
                              "recorded as null per spec.baselines.RETRIEVAL_BASELINE.",
    },
    "falsifier_triggered": {
        "metric_id": spec["decision_rule"]["falsifier_evaluation"]["metric"],
        "type": "boolean",
        "value": falsifier_triggered,
        "condition": spec["decision_rule"]["falsifier_evaluation"]["condition"],
        "majority_non_stationary": FALS["majority_non_stationary"],
        "majority_class": FALS["majority_non_stationary_class"],
        "non_stationary_items": FALS["n_non_stationary"],
        "stationary_items": FALS["n_stationary"],
        "cost_condition": FALS["cost_condition"],
        "attainability_audit": FALS["attainability_audit"],
        "cost_condition_evaluated_over":
            "median re_acquisition vs median unconditional re-derivation of the "
            "majority class (request_scoped), both in cl100k_base tokens and requests",
    },
    "controls_pass": {
        "metric_id": spec["decision_rule"]["controls_gate"]["metric"],
        "type": "boolean",
        "value": controls_pass,
        "required": spec["decision_rule"]["controls_gate"]["required"],
        "control_statuses": {c: v["status"] for c, v in analysis["controls"].items()},
        "note": analysis["controls_pass_note"],
    },
    "sample_composition": {
        "items_admitted": DEN["items_total"],
        "items_classified": DEN["items_classified"],
        "items_unclassifiable": DEN["items_unclassifiable"],
        "sites_executed": len(costs["cold_crawl_summary"]),
        "sites_with_classified_items": DEN["sites_with_at_least_one_classified_item"],
        "sessions_per_target": K_SESSIONS,
        "inter_session_delay_min_seconds": min_delay,
        "inter_session_delay_required_seconds":
            spec["controls_pre_freeze_verification"]["INTER_SESSION_DELAY"]["delay_seconds"],
        "cold_crawl_depth_bound": {"max_hops": MAX_HOPS,
                                   "max_pages_per_cold_crawl":
                                       items["constants"]["MAX_PAGES_PER_COLD_CRAWL"],
                                   "max_items_per_site": items["constants"]["MAX_ITEMS_PER_SITE"]},
        "frozen_floor": {"min_items": DEN["frozen_floor_items"],
                         "min_sites": DEN["frozen_floor_sites"],
                         "meets_floor_items": DEN["meets_frozen_floor_items"],
                         "meets_floor_sites": DEN["meets_frozen_floor_sites"]},
        "max_hop_of_any_admitted_item": max(
            (it.get("hop") for it in items["items"] if it.get("hop") is not None), default=None),
        "hop_histogram": {
            str(h): sum(1 for it in items["items"] if it.get("hop") == h)
            for h in sorted({it.get("hop") for it in items["items"]}, key=lambda v: (v is None, v))},
    },
    "substrate_economics": {
        "get_requests_sent": analysis["get_requests_sent"],
        "non_get_requests_sent": analysis["non_get_requests_sent"],
        "responses_cached": manifest["responses_cached"],
        "cache_bytes_uncompressed": manifest["cache_bytes_uncompressed"],
        "wall_clock_seconds": manifest["wall_clock_seconds"],
        "cold_crawl_summary": costs["cold_crawl_summary"],
    },
    "value_only_sensitivity": {
        "purpose": "IC-01 disclosure: the frozen rule hashes the whole containing page "
                   "body, so any item on a page whose bytes churn is request_scoped even "
                   "when its own value is byte-stable.",
        "per_class": value_only,
        "n_items_unmatched_by_the_frozen_value_only_table": value_only_unmatched,
        "n_items_that_change_class_vs_primary": sum(
            abs(value_only[k]["count"] - analysis["class_distribution"][k]["count"])
            for k in CLASSES) // 2,
        "class_comparison": {
            k: {"primary": analysis["class_distribution"][k]["count"],
                "value_only": value_only[k]["count"]} for k in CLASSES},
    },
}

# ---------------------------------------------------------------- observations
obs = [
    {"id": "OBS-01", "kind": "raw_observation",
     "statement": f"{manifest['http_log_records']} HTTP requests were issued, all GET; "
                  f"{analysis['non_get_requests_sent']} non-GET requests were issued.",
     "evidence_ref": "raw/http.jsonl"},
    {"id": "OBS-02", "kind": "raw_observation",
     "statement": f"K={K_SESSIONS} sessions were executed per frozen target with disjoint "
                  f"cookie jars; measured minimum inter-session delay {min_delay} s over "
                  f"{len(jsonl(os.path.join(RAW, 'session_timing.jsonl')))} timing records.",
     "evidence_ref": "raw/session_timing.jsonl"},
    {"id": "OBS-03", "kind": "raw_observation",
     "statement": f"{DEN['items_classified']} of {DEN['items_total']} admitted items "
                  f"received a class; {class_counts['session_invariant']} session_invariant, "
                  f"{class_counts['request_scoped']} request_scoped, "
                  f"{class_counts['session_scoped']} session_scoped, "
                  f"{class_counts['time_scoped']} time_scoped, "
                  f"{class_counts['rotating']} rotating.",
     "evidence_ref": "derived/classification.json"},
    {"id": "OBS-04", "kind": "raw_observation",
     "statement": "The Wikimedia authenticity_token designated at "
                  "https://auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount "
                  "and the GitLab authenticity_token at "
                  "https://gitlab.com/-/trial_registrations/new/ each produced 5 distinct "
                  "values across the 5 sessions AND 5 distinct values across 5 GETs issued "
                  "inside a single session (within-session distinct-value count = 5).",
     "evidence_ref": "raw/observations.jsonl"},
    {"id": "OBS-05", "kind": "raw_observation",
     "statement": "https://httpbin.org/uuid produced 5 distinct values across sessions and 5 "
                  "distinct values within one session; https://httpbin.org/headers "
                  "X-Request-Id reported its explicit 'prng' fallback on every session and "
                  "produced 5 distinct values.",
     "evidence_ref": "raw/observations.jsonl"},
    {"id": "OBS-06", "kind": "raw_observation",
     "statement": "The prereg-named REVERIFIED_NON_STATIONARY anchor "
                  "https://gitlab.com/users/sign_in returned HTTP 403 in all 5 sessions, so "
                  "the designated input was never observable; the parent-cited anchor "
                  "https://gitlab.com/-/trial_registrations/new/ returned HTTP 200 and was "
                  "observable but was never substituted for the prereg-named anchor.",
     "evidence_ref": "raw/controls_verification.jsonl"},
    {"id": "OBS-07", "kind": "raw_observation",
     "statement": "https://httpbin.org/sitemap.xml returned HTTP 404 in all 5 sessions; the "
                  "frozen conditional 'sitemap.xml (if exists, else skip)' therefore skipped "
                  "it, and a byte-stable 404 error page was excluded from the verdict.",
     "evidence_ref": "raw/controls_verification.jsonl"},
    {"id": "OBS-08", "kind": "raw_observation",
     "statement": "4 of 6 frozen roots redirected off their nominal host: gitlab.com -> "
                  "about.gitlab.com, auth.wikimedia.org -> www.wikimedia.org, "
                  "en.wikipedia.org -> en.wikipedia.org/wiki/Main_Page, postman-echo.com -> "
                  "www.postman.com/postman/workspace/published-postman-templates/... "
                  "bitbucket.org and httpbin.org did not redirect.",
     "evidence_ref": "derived/costs.json#cold_crawl_summary"},
    {"id": "OBS-09", "kind": "raw_observation",
     "statement": "Under the frozen host-pinned cold breadth-first crawl, the wikimedia and "
                  "postman_echo targets yielded 0 admitted items (1 request each, 0 "
                  "same-host HTML candidates detected); bitbucket and gitlab admitted items "
                  "only from their own root pages.",
     "evidence_ref": "derived/costs.json#cold_crawl_summary"},
    {"id": "OBS-10", "kind": "raw_observation",
     "statement": "Every session_invariant item had re-acquisition cost exactly equal to its "
                  "re-derivation cost (1 request, identical cl100k_base token count), so "
                  "break_even_reuse_count is null (infinite) for all of them.",
     "evidence_ref": "derived/costs.json"},
    {"id": "OBS-11", "kind": "raw_observation",
     "statement": "For the depth-1 wikipedia items, re-acquisition was 2 requests / ~93k "
                  "tokens while unconditional re-derivation was 15-26 requests / ~0.97-1.50M "
                  "tokens. For root-hosted bitbucket items, re-acquisition and re-derivation "
                  "were the same single GET and differed only by ~13 tokens, which made the "
                  "frozen break-even formula return values from 1 to 34,299 for economically "
                  "identical items.",
     "evidence_ref": "derived/costs.json"},
    {"id": "OBS-12", "kind": "raw_observation",
     "statement": f"Under the disclosed value-only variant of the frozen rule the class "
                  f"distribution is {value_only['session_invariant']['count']} session_invariant "
                  f"/ {value_only['request_scoped']['count']} request_scoped, with "
                  f"{value_only_unmatched} of {DEN['items_classified']} classified items "
                  f"unmatched by the frozen value-only table.",
     "evidence_ref": "derived/classification_sensitivity.json"},
    {"id": "OBS-13", "kind": "raw_observation",
     "statement": f"{reach.get('not_reached_within_frozen_crawl_bounds', 0)} of "
                  f"{DEN['items_total']} items were not reached within the frozen crawl "
                  f"bounds ({reach}), so their unconditional re-derivation cost is not "
                  f"measurable under this design and their class-level economics rest on the "
                  f"measured subset only.",
     "evidence_ref": "derived/costs.json"},
    {"id": "OBS-14", "kind": "raw_observation",
     "statement": "https://gitlab.com redirected to https://about.gitlab.com/, which contains "
                  "no /explore link, so the prereg-named KNOWN_STATIONARY_CONTROL anchor "
                  "https://gitlab.com/explore was unobservable in all 5 sessions; the anchor "
                  "was probed separately and returned HTTP 200.",
     "evidence_ref": "raw/controls_verification.jsonl"},
    {"id": "OBS-16", "kind": "derived_measurement",
     "statement": "The class-level break_even_reuse_count for session_invariant is 2 reuses, "
                  "yet every one of the 12 session_invariant items individually has "
                  "re-acquisition exactly equal to re-derivation and therefore an infinite "
                  "item-level break-even. The class number arises because the re-acquisition "
                  "median is taken over all 12 items (median 37,357 tokens) while the "
                  "re-derivation median is taken over only the 7 items the bounded crawl "
                  "could reach (median 71,673 tokens), and the 5 unreachable items are the "
                  "cheap static files (79-1,923 tokens). The same denominator mismatch applies "
                  "to request_scoped (re-acquisition median over 17 items, re-derivation "
                  "median over 13).",
     "evidence_ref": "derived/costs.json"},
    {"id": "OBS-17", "kind": "derived_measurement",
     "statement": "Restricting to the 20 items where BOTH costs are measured, re-derivation "
                  "was greater than or equal to re-acquisition on both units for 20 of 20 "
                  "items. The frozen falsifier's cost condition held for 0 of 20.",
     "evidence_ref": "derived/analysis.json#falsifier.attainability_audit"},
    {"id": "OBS-15", "kind": "raw_observation",
     "statement": "The KNOWN_STATIONARY_CONTROL anchor "
                  "https://en.wikipedia.org/wiki/Main_Page (the site self-link on Main_Page) "
                  "had 1 distinct value across 5 sessions but 5 distinct page body hashes, "
                  "so the frozen rule classified it request_scoped.",
     "evidence_ref": "derived/classification.json"},
]

# ---------------------------------------------------------------- validity notes
vn = [
    {"id": "VN-01", "severity": "decisive",
     "note": "The frozen controls_gate requires all four pre-freeze controls to PASS and maps "
             "any control FAIL to status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE. Two of "
             "the four measured arms FAILED, so no classification or economic result in this "
             "packet may be read as a validated scientific answer.",
     "evidence_ref": "spec.json#decision_rule.controls_gate"},
    {"id": "VN-02", "severity": "high",
     "note": "spec.json controls_pre_freeze_verification records status PENDING, "
             "verified_at null, evidence_ref null for all four controls at the time "
             "freeze.json exists, although prereg.md sections 7 and 14 require verified "
             "controls before freeze. The frozen design was never validated before "
             "execution.",
     "evidence_ref": "spec.json#controls_pre_freeze_verification"},
    {"id": "VN-03", "severity": "high",
     "note": "Frozen control-design defect: spec.positive_control and prereg 6.1 designate "
             "5 anchors as known-stationary, but 2 of them are not available on the live "
             "web (gitlab /explore absent from the page gitlab.com actually serves; "
             "httpbin /sitemap.xml absent). Even ignoring availability, the wikipedia "
             "Main_Page self-link anchor is not stationary under the frozen rule because "
             "Main_Page's body churns within a session. A 'known stationary' class with "
             "only 3 genuinely testable anchors, of which 1 is not stationary, cannot "
             "calibrate a five-class taxonomy.",
     "evidence_ref": "raw/controls_verification.jsonl"},
    {"id": "VN-04", "severity": "high",
     "note": "Frozen control-design defect: the REVERIFIED_NON_STATIONARY accept list is "
             "'session_scoped or rotating with >= 2 distinct values', which excludes "
             "request_scoped. Both observable anchors of that control fell into "
             "request_scoped (5 distinct values across sessions AND within a session), "
             "i.e. they demonstrated non-stationarity MORE strongly than the control "
             "anticipated, yet the frozen criterion rejects them. The control can only "
             "fail; no live outcome could pass it.",
     "evidence_ref": "raw/controls_verification.jsonl"},
    {"id": "VN-05", "severity": "high",
     "note": "Frozen rule defect (spec.measurement_validity.classification_method): the "
             "evaluation order places session_scoped before time_scoped and rotating, so "
             "time_scoped and rotating are unreachable for any item whose value differs "
             "within a session. Both classes therefore have count 0 by construction, not "
             "by observation.",
     "evidence_ref": "spec.json#measurement_validity.classification_method"},
    {"id": "VN-06", "severity": "high",
     "note": "Frozen rule defect: the primary rule requires value AND containing-page "
             "body-hash invariance across sessions, so an item is session_invariant only "
             "if its whole page is byte-stable. Any item on a page with per-request byte "
             "churn is request_scoped regardless of its own value stability. This makes "
             "request_scoped a near-catch-all channel and is why the class distribution "
             "moves from 12/17 to 12/5 under the value-only variant. The choice of "
             "channel is decision-relevant, not cosmetic.",
     "evidence_ref": "derived/classification_sensitivity.json"},
    {"id": "VN-07", "severity": "decisive",
     "note": "The frozen falsifier has an empty trigger interior. Its cost condition "
             "compares median re-acquisition against median unconditional re-derivation as "
             "measured by the frozen cold breadth-first crawl. A breadth-first route is a "
             "shortest path, and the re-derivation token sum is a superset of the "
             "re-acquisition token sum, so re_derivation >= re_acquisition on both units for "
             "every reachable item. Empirically the condition held for 0 of 20 items with "
             "measurable re-derivation. The FALSIFIES outcome was therefore unreachable for "
             "any execution of this frozen rule, independent of the substrate.",
     "evidence_ref": "derived/analysis.json#falsifier.attainability_audit"},
    {"id": "VN-08", "severity": "medium",
     "note": "The frozen break_even formula ceil(re_acq / (re_deriv - re_acq)) has no guard "
             "against a near-degenerate denominator. For root-hosted items where "
             "re-acquisition and re-derivation are the same single GET differing by ~13 "
             "tokens of header jitter, it returns break-even counts spanning 1 to 34,299 "
             "for economically identical items, and the class-median value (1) disagrees "
             "with the median item-level value (1256) for the same class.",
     "evidence_ref": "derived/costs.json"},
    {"id": "VN-09", "severity": "medium",
     "note": "The site-clustered bootstrap CI95 is degenerate because every class is "
             "perfectly separated at the site level (gitlab/wikipedia/bitbucket/httpbin each "
             "contain only request_scoped or only session_invariant items), so resampling "
             "sites collapses to the two extreme proportions. The intervals "
             "(0.045-0.759 for session_invariant, 0.241-0.955 for request_scoped) are "
             "reported for contract compliance but carry no useful precision.",
     "evidence_ref": "derived/analysis.json#class_distribution"},
    {"id": "VN-10", "severity": "medium",
     "note": "Substrate drift is not a producer defect but limits what the pool can say: the "
             "prereg-named GitLab control anchor returns HTTP 403 credential-free, the "
             "prereg-named httpbin sitemap anchor returns 404, and 4 of 6 roots redirect off "
             "their nominal host, so 'site' is not a stable unit here.",
     "evidence_ref": "raw/controls_verification.jsonl"},
    {"id": "VN-11", "severity": "low",
     "note": "tiktoken 0.14.0 is provisioned in the workflow image but is NOT declared in "
             "pyproject.toml, and the frontier lane may not edit pyproject.toml. All token "
             "figures are therefore 'environment-provisioned tokenizer', not 'declared "
             "pure-stdlib run' as spec.measurement_validity.substrate requires.",
     "evidence_ref": "pyproject.toml"},
    {"id": "VN-12", "severity": "low",
     "note": "Storage-format deviation: response bodies are persisted as gzip files at "
             "raw/responses_cache/<sha256>.json.gz where <sha256> is the SHA256 of the "
             "UNCOMPRESSED body bytes, so the content address is still verifiable; the gzip "
             "wrapper is not the frozen 'raw/<hash>.json' layout.",
     "evidence_ref": "raw/responses_cache"},
    {"id": "VN-13", "severity": "medium",
     "note": "Two earlier complete passes of the same frozen design were discarded and their "
             "raw evidence deleted: (1) a pass in which relative hrefs were matched only "
             "against absolute designated URLs, and (2) a pass in which item identity "
             "(ctrl_id, element_type, element_name) collided between the prereg-named and "
             "parent-cited GitLab anchors and silently discarded the prereg-named anchor's "
             "observations. Both defects are recorded in the shipped executor as "
             "implementation notes IC-09 and IC-10. Only the final pass is authoritative, "
             "so no statement in this packet depends on the discarded passes; however "
             "this is a third execution of the same frozen question.",
     "evidence_ref": "derived/items.json#implementation_choices"},
    {"id": "VN-14", "severity": "medium",
     "note": "In one discarded pass (about 20 minutes before the shipped pass) the GitLab "
             "favicon was byte-unstable across sessions and was therefore classified "
             "request_scoped; in the shipped pass it was byte-stable and classified "
             "session_invariant. The designated 'known stationary' asset class is thus not "
             "robust at the scale of minutes. The discarded pass evidence is not retained, "
             "so this is an unreplicated informational observation, not a result.",
     "evidence_ref": None},
    {"id": "VN-15", "severity": "low",
     "note": "request.json records base_sha 0a3b7f96f488b6da77728973ea1fcc6caaa17e38 "
             "(an ancestor of the execution HEAD 0b89abe47cf4710dff8c4736d08fee9e671d6f73). "
             "Execution used the working tree with the two untracked frontier-lane "
             "executor/analyzer files; no committed revision contains them.",
     "evidence_ref": "request.json#base_sha"},
    {"id": "VN-16", "severity": "medium",
     "note": "request.json director_mandate.allocation.question names predecessor "
             "EXP-FRONTIER-36314209725, which failed on installation. This packet is the "
             "reallocated CONTINUE transaction and carries the same mandate text; the "
             "mandate's question is therefore answered by EXP-FRONTIER-37385647440.",
     "evidence_ref": "request.json#director_mandate"},
    {"id": "VN-17", "severity": "medium",
     "note": "3 of 32 admitted items are unclassifiable (gitlab /explore anchor absent, "
             "GitLab /users/sign_in HTTP 403, httpbin /date HTTP 404). They are excluded "
             "from the class denominator and reported separately rather than being forced "
             "into a class.",
     "evidence_ref": "derived/classification.json"},
    {"id": "VN-19", "severity": "decisive",
     "note": "The frozen break_even_reuse_count metric silently requires that the "
             "re-acquisition and re-derivation medians be taken over the SAME item set. The "
             "frozen crawl bounds break that precondition: 11 of 32 items were never reached, "
             "and they are the cheap ones. For session_invariant the resulting class number "
             "(2 reuses) is an artifact of a 12-item re-acquisition median against a 7-item "
             "re-derivation median; every individual item in that class has infinite "
             "break-even. The economically meaningful reading is the item-level one, and at "
             "item level the entire invariant class has NO amortization surface.",
     "evidence_ref": "derived/costs.json"},
    {"id": "VN-18", "severity": "low",
     "note": "Every discovered item sits at hop 0 or hop 1 of the frozen crawl, so the "
             "re-acquisition/re-derivation contrast exercised here is the extreme-favourable "
             "case for handle persistence: the target is one or two GETs from the root. No "
             "item at depth >= 2 was admitted, so the cost argument is untested at real "
             "depths.",
     "evidence_ref": "derived/costs.json"},
]

unresolved = [
    {"id": "UR-01",
     "question": "Does a genuinely session_scoped class exist anywhere on the "
                 "credential-free public HTTP substrate class?",
     "why_unresolved": "0 of 29 items classified session_scoped, but the two server-minted "
                       "CSRF handles that the parent packet reported as session-scoped were "
                       "observed to change between two GETs one second apart inside one "
                       "session, so this run cannot separate 'no session_scoped class "
                       "exists' from 'the frozen rule's body-hash channel masks it'."},
    {"id": "UR-02",
     "question": "What are the true class proportions of this object class, on the frozen "
                 "pool and beyond?",
     "why_unresolved": "The frozen (value, page-hash) rule and the disclosed value-only rule "
                       "disagree by 12 of 29 items, and the frozen pool is hand-picked, so "
                       "neither the class proportions nor their ordering is identified by "
                       "this design."},
    {"id": "UR-03",
     "question": "Are any items time_scoped or rotating?",
     "why_unresolved": "Both classes are unreachable under the frozen rule order (VN-05). A "
                       "correctly ordered rule plus a declared per-session sampling schedule "
                       "would be required."},
    {"id": "UR-04",
     "question": "Would the 3 unclassifiable items classify on a browser or "
                 "credential-bearing substrate?",
     "why_unresolved": "The frozen substrate is GET-only and credential-free by mandate, and "
                       "this lane may not substitute a parent-cited URL for the prereg-named "
                       "anchor, so the drift was recorded rather than repaired."},
    {"id": "UR-05",
     "question": "Is the amortization question answerable at all with an instrument whose "
                 "falsifier can trigger?",
     "why_unresolved": "The frozen falsifier's accept region is empty (VN-07). A falsifiable "
                       "version needs a re-derivation baseline that is strictly more "
                       "expensive than re-acquisition by construction, e.g. an adversarial "
                       "crawl of the full site with no path memory, or a cost model that "
                       "charges for re-deriving the whole observation procedure rather than "
                       "re-walking a known shortest path."},
    {"id": "UR-06",
     "question": "What is the unconditional re-derivation cost of the 11 items not reached "
                 "within the frozen crawl bounds?",
     "why_unresolved": "The frozen crawl depth/width bounds never reached their pages, so the "
                       "cost cell is genuinely unmeasured and is reported as null rather "
                       "than imputed."},
    {"id": "UR-07",
     "question": "Do the KNOWN_STATIONARY_CONTROL anchors behave as specified on a stable "
                 "or credential-bearing substrate?",
     "why_unresolved": "Only 3 of 5 anchors are testable and 1 of those 3 is not stationary, "
                       "so the control arm cannot be re-run to PASS without either a "
                       "different anchor set or a different substrate."},
]

# ---------------------------------------------------------------- artifacts
art_paths = [
    ("code", "research/frontier/stationarity_37385647440.py"),
    ("code", "research/frontier/analyze_stationarity_37385647440.py"),
    ("code", "research/frontier/emit_result_37385647440.py"),
    ("raw", "research/experiments/EXP-FRONTIER-37385647440/raw/http.jsonl"),
    ("raw", "research/experiments/EXP-FRONTIER-37385647440/raw/observations.jsonl"),
    ("raw", "research/experiments/EXP-FRONTIER-37385647440/raw/session_timing.jsonl"),
    ("raw", "research/experiments/EXP-FRONTIER-37385647440/raw/controls_verification.jsonl"),
    ("derived", "research/experiments/EXP-FRONTIER-37385647440/derived/items.json"),
    ("derived", "research/experiments/EXP-FRONTIER-37385647440/derived/classification.json"),
    ("derived", "research/experiments/EXP-FRONTIER-37385647440/derived/classification_sensitivity.json"),
    ("derived", "research/experiments/EXP-FRONTIER-37385647440/derived/costs.json"),
    ("derived", "research/experiments/EXP-FRONTIER-37385647440/derived/analysis.json"),
    ("derived", "research/experiments/EXP-FRONTIER-37385647440/derived/run_manifest.json"),
]
artifacts = []
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
for role, p in art_paths:
    ap = os.path.join(REPO, p)
    if not os.path.exists(ap):
        raise SystemExit(f"artifact missing: {p} -> {ap}")
    if True:
        artifacts.append({"path": p, "sha256": sha256_file(ap), "role": role})
    else:
        artifacts.append({"path": p, "sha256": None, "role": role,
                          "note": "absent at emit time"})
cache_dir = os.path.join(RAW, "responses_cache")
cache_files = sorted(os.listdir(cache_dir))
artifacts.append({
    "path": "research/experiments/EXP-FRONTIER-37385647440/raw/responses_cache/",
    "sha256": None,
    "role": "raw",
    "note": f"{len(cache_files)} content-addressed response bodies named "
            f"<sha256-of-uncompressed-body-bytes>.json.gz; the directory itself is not "
            f"hashable as a single object; each name is the verification handle.",
})

# stable ascending identity order for downstream AUDIT cross-referencing
obs.sort(key=lambda o: o["id"])
vn.sort(key=lambda v: v["id"])
unresolved.sort(key=lambda u: u["id"])

result = {
    "schema_version": 1,
    "experiment_id": spec["experiment_id"],
    "lane": spec["lane"],
    "status": status,
    "outcome": outcome,
    "metrics": metrics,
    "controls": ctrl_out,
    "artifacts": artifacts,
    "observations": obs,
    "validity_notes": vn,
    "unresolved": unresolved,
    "decision_rule_application": {
        "frozen_branch": branch,
        "frozen_mapping": mapping,
        "controls_pass": controls_pass,
        "falsifier_triggered": falsifier_triggered,
        "note": "status and outcome are the frozen mapping applied to the analyzer's "
                "booleans. No alternative branch was selected, and no promotion is claimed.",
    },
    "claim_ceiling_producer": (
        "This transaction supports no claim update. Its only admissible conclusion is a "
        "measurement-validity finding about the instrument, plus three substrate "
        "observations that are consistent with, and bounded by, the inherited parent "
        "handoff: (1) on the credential-free GET-only substrate the objects a persistent "
        "agent would replay across episodes are dominated by objects that are already stale "
        "within a single episode; (2) the class of objects that ARE byte-stable across "
        "episodes carries no amortization surface at all, because re-acquiring them costs "
        "exactly what re-deriving them costs; (3) the frozen instrument could not have "
        "returned its own positive-negative answer. Do not read the class proportions as "
        "Web prevalence and do not read 'request_scoped' as a mechanism claim until the "
        "page-hash versus value channel ambiguity (VN-06) is resolved."
    ),
    "evidence_refs": [
        "derived/analysis.json",
        "derived/classification.json",
        "derived/classification_sensitivity.json",
        "derived/costs.json",
        "raw/controls_verification.jsonl",
        "raw/http.jsonl",
        "raw/observations.jsonl",
        "raw/session_timing.jsonl",
        "../EXP-FRONTIER-36306528608/handoff.json",
        "../EXP-FRONTIER-36314209725/failure.json",
    ],
}

with open(os.path.join(EXP, "result.json"), "w", encoding="utf-8") as fh:
    json.dump(result, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

# ---------------------------------------------------------------- provenance
def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True,
                          cwd=HERE).stdout.strip()


import tiktoken  # noqa: E402

enc = tiktoken.get_encoding("cl100k_base")
prov = {
    "schema_version": 1,
    "experiment_id": spec["experiment_id"],
    "lane": spec["lane"],
    "stage": "EXECUTE",
    "generated_by": "research/frontier/emit_result_37385647440.py",
    "request": {
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "origin_github_run_id": request["origin_github_run_id"],
        "created_at": request["created_at"],
        "chain_depth": request["chain_depth"],
        "parent_handoff": request.get("parent_handoff"),
        "base_sha": request["base_sha"],
    },
    "frozen_inputs": {
        "paths": {f: frozen_hashes[f] for f in FROZEN_FILES},
        "freeze_manifest": freeze,
        "freeze_hashes_verified": sorted(freeze["hashes"]),
        "verified_unmodified": True,
        "note": "Each frozen file's SHA256 was recomputed at emit time and matched against "
                "freeze.json. No frozen file was written by any code path in this lane.",
    },
    "git": {
        "execution_head": git("rev-parse", "HEAD"),
        "execution_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "base_sha_is_ancestor_of_head": True,
        "tracked_tree_clean": git("status", "--porcelain", "--untracked-files=no") == "",
        "untracked_paths_created_by_this_lane": [
            "research/frontier/stationarity_37385647440.py",
            "research/frontier/analyze_stationarity_37385647440.py",
            "research/frontier/emit_result_37385647440.py",
            "research/experiments/EXP-FRONTIER-37385647440/raw/",
            "research/experiments/EXP-FRONTIER-37385647440/derived/",
        ],
        "preexisting_untracked_not_created_by_this_lane": [
            "research/experiments/EXP-FRONTIER-37385647440/model_execute.json"
        ],
        "operations_performed": ["git status", "git log", "git rev-parse",
                                 "git merge-base --is-ancestor"],
        "no_commit_no_push": True,
    },
    "code_paths": {
        "executor": {"path": "research/frontier/stationarity_37385647440.py",
                     "sha256": sha256_file(os.path.join(HERE, "stationarity_37385647440.py"))},
        "analyzer": {"path": "research/frontier/analyze_stationarity_37385647440.py",
                     "sha256": sha256_file(os.path.join(HERE, "analyze_stationarity_37385647440.py"))},
        "emitter": {"path": "research/frontier/emit_result_37385647440.py",
                    "sha256": None},
        "entry_points": [
            "python3 research/frontier/stationarity_37385647440.py",
            "python3 research/frontier/analyze_stationarity_37385647440.py",
            "python3 research/frontier/emit_result_37385647440.py",
        ],
        "reproduction_note": "The executor performs live network GETs. Re-running it produces "
                            "a NEW measurement against the live web and will not reproduce "
                            "these byte-level results; only the frozen input hashes, the code "
                            "hashes and the shipped raw/derived artifacts are reproducible "
                            "exactly.",
    },
    "environment": {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "tokenizer": {
            "name": "cl100k_base",
            "library": "tiktoken",
            "library_version": tiktoken.__version__,
            "declared_in_pyproject": False,
            "note": "Environment-provisioned. spec.measurement_validity.substrate requires "
                    "tiktoken to be declared in pyproject.toml before claiming a pure-stdlib "
                    "run; the frontier lane may not edit pyproject.toml, so this run does "
                    "not claim pure-stdlib.",
            "vocabulary_sha256_of_mergeable_ranks_prefix":
                hashlib.sha256(str(enc._mergeable_ranks).encode()).hexdigest()[:16],
        },
        "http_clients_used": ["urllib.request (stdlib)", "requests (fallback path, unused)"],
        "browser": False, "docker": False, "credentials": False, "model_key": False,
        "network_egress": "credential-free public HTTPS GET only",
    },
    "dataset": {
        "kind": "live credential-free public HTTP target pool (frozen, hand-picked)",
        "targets": sorted(costs["cold_crawl_summary"].keys()),
        "sessions_per_target": K_SESSIONS,
        "admitted_items": DEN["items_total"],
        "classified_items": DEN["items_classified"],
        "declared_vs_discovered": {"declared_controls": 13, "discovered": 19},
        "target_pool_scope": "sample of a hand-picked credential-free pool; NOT Web "
                             "prevalence (spec.measurement_validity.target_pool).",
        "discarded_executions": 2,
        "discarded_execution_reason": "two producer-side instrument defects found by "
                                      "self-check (relative-href matching; item-identity "
                                      "collision). Both passes and their evidence were "
                                      "deleted; only the shipped pass is authoritative.",
    },
    "material_artifacts": artifacts,
    "frozen_input_hashes": [
        {"path": f"research/experiments/EXP-FRONTIER-37385647440/{f}", "sha256": frozen_hashes[f]}
        for f in FROZEN_FILES
    ],
    "upstream_evidence": [
        {"path": "research/experiments/EXP-FRONTIER-36306528608/handoff.json",
         "role": "parent handoff named by request.json"},
        {"path": "research/experiments/EXP-FRONTIER-36314209725/failure.json",
         "role": "predecessor named by request.json director_mandate; failed installation"},
        {"path": "research/lanes/registry.json", "role": "frontier lane authorization"},
        {"path": "research/EXPERIMENT_PACKET.md", "role": "binding packet contract"},
    ],
    "commands_materially_affecting_reproduction": [
        "python3 -m py_compile research/frontier/stationarity_37385647440.py "
        "research/frontier/analyze_stationarity_37385647440.py",
        "python3 research/frontier/stationarity_37385647440.py  # live GET-only network pass",
        "python3 research/frontier/analyze_stationarity_37385647440.py  # offline, deterministic",
        "python3 research/frontier/emit_result_37385647440.py  # offline, deterministic",
    ],
    "wall_clock_seconds_of_network_pass": manifest["wall_clock_seconds"],
    "http_requests_sent": manifest["http_log_records"],
    "limitations": [
        "Live-network measurement against a drifting web; not byte-reproducible.",
        "No credentials, no browser, no write verb, per frozen substrate mandate.",
        "All discovered items lie at crawl hop 0 or 1, so the cost contrast is the "
        "extreme-favourable case for handle persistence.",
        "The frozen falsifier cannot trigger (VN-07) and two frozen controls failed (VN-01), "
        "so this packet carries a measurement-validity finding, not a scientific answer.",
    ],
}
prov["emitter"] = {"path": "research/frontier/emit_result_37385647440.py",
                   "sha256": sha256_file(os.path.abspath(__file__))}
for a in prov["material_artifacts"]:
    if a["path"].endswith("emit_result_37385647440.py"):
        a["sha256"] = prov["emitter"]["sha256"]

with open(os.path.join(EXP, "provenance.json"), "w", encoding="utf-8") as fh:
    json.dump(prov, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

print(json.dumps({
    "status": status, "outcome": outcome, "branch": branch,
    "controls_pass": controls_pass, "falsifier_triggered": falsifier_triggered,
    "metrics_keys": list(metrics.keys()),
    "controls_keys": list(ctrl_out.keys()),
    "n_observations": len(obs), "n_validity_notes": len(vn),
    "n_unresolved": len(unresolved), "n_artifacts": len(artifacts),
}, indent=1))