#!/usr/bin/env python3
"""EXP-PHYSICS-35774039080 EXECUTE — frozen relaxed-substrate gate evaluation.

Frozen design (spec.json measurement_validity #1, prereg sections 6.1/13,
decision_rule "Relaxed substrate"): a dataset qualifies iff, after leakage-free
filtering, NL>=50 non-leakage transitions, strata_count>=5 unique
(URL_before,H_K=3,Action) with >=3 per stratum, singleton_SA_rate<70%,
leakage_validOnly<60%, dom_bytes>=500 and a11y non-empty on >=80% transitions.

Frozen halting rule (analysis plan step 1): "compute relaxed gate table — halt
if Q==0 with MEASUREMENT_INVALID." If Q==0, H_T/H_B must NOT be tested and
positive/null controls must NOT gate anything (they are pipeline gates for the
primary stage only).

This script therefore performs ONLY the gate computation and substrate
availability scan, writes gate_table.json, and halts. It performs no
outcome-bearing H_T/H_B measurements and runs no permutation machinery.

Deterministic: PYTHONHASHSEED=0; no RNG used. Reproducible from the frozen
commit; only elapsed timestamps vary.
"""
import hashlib
import json
import os
import sys
import urllib.parse
from collections import Counter

PYTHONHASHSEED = os.environ.get("PYTHONHASHSEED", "")

EXP_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(EXP_DIR, "..", "..", ".."))
SRC_DIR = os.path.join(REPO, "research", "experiments", "EXP-PHYSICS-35209110569")
EXPERIMENT_ID = "EXP-PHYSICS-35774039080"
LANE = "physics"

FROZEN_HASHES = {
    "prereg.md": "185b7642c45c803078e39882e7622aa60762055ec6d2295fc10585ca9b2cb21b",
    "request.json": "b0e6eeaccd5fa95cd6c403a1555e9176891b0eba2eec67de2a94e6eb026bce2a",
    "spec.json": "8eeebec9f069bd6a5247d5f9b85b66e8bf580553a626cf099a5a3ac2638bb5ee",
}

# sha256 recorded in EXP-PHYSICS-35209110569 result.json artifacts (raw role)
PRIOR_RAW_HASHES = {
    "raw_vanillajs.json": "8897172862238d5ce5f433090bdfeecbf7b5cb7485f3ccfea4b8887a796979fe",
    "raw_vanillajs_topup.json": "655178f7b98d5e4873ed061ad607dba8dd0c53e62e5d8469cb1686fd2ae2bb49",
    "raw_react.json": "4d0b19e27b3a081fe6c99f3e1e4386d4eccdb00561c84265a8bc9f1f8b644fb1",
    "raw_react_topup.json": "65aef7fe9980c50f72d8b7ba39a5f520b26c1e64101c325dc175442a0d5b3c99",
    "raw_vue.json": "de723933a67bfb6961e621193bc740ee97b6a37047624a9a7fb4a3b0938b4cc4",
    "raw_vue_topup.json": "59d701d8bc3627cc26a4ac8e51bb141a5da18b35dd3fb9bdda1c62169f856443",
    "raw_angular.json": "353489eb28bcbe4e7bb97756b785dfbec167a2950cc57e1636c57b32a1696f24",
    "raw_angular_topup.json": "f26d3767d7e2a789dd3d7e4daf8a4fab0755b07ca19f07eac6b92d51055e3f87",
    "raw_svelte.json": "88e2897a755608123f879772237a6d44cfed546d4f7abbf450dce05244068482",
    "raw_svelte_topup.json": "97893637f64953d0a6725dc5692c653413e605d0f32012e197bb4650b511537f",
}

VARIANTS = ["vanillajs", "react", "vue", "angular", "svelte"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_url(u):
    """Frozen: lowercase, strip query ?session=/?token=, preserve SPA hash
    fragment #/, strip trailing slash."""
    if u is None:
        return ""
    s = u.strip().lower()
    s = s.split("?", 1)[0]  # strip all query (frozen normalization used for
    # leakage/state; session/token params are the motivating case)
    while s.endswith("/") and "#" not in s:
        s = s[:-1]
    if s.endswith("/"):
        # keep leading slash of the fragment path, drop trailing slash only
        # if it is not part of the fragment
        if "#" in s:
            pre, frag = s.split("#", 1)
            pre = pre.rstrip("/")
            s = pre + "#" + frag
        else:
            s = s.rstrip("/")
    return s


def normalize_title(t):
    if t is None:
        return ""
    return t.strip().lower()[:200]


def target_href(rec):
    at = rec.get("action_target")
    if at is None:
        return None
    return at


def is_href_bearing(rec):
    return rec.get("action_primitive") == "link_click" and rec.get("action_target") is not None


def leakage_free_action_sig(rec):
    """Leakage-free A: primitive + target_sig WITHOUT href/URL/src. Raw files
    contain only primitive + resolved href (action_target); href never enters A.
    For non-link actions action_target is None. target_sig fields (role/name/
    testId/aria-label) were never captured in the reused TodoMVC raw files."""
    return (rec.get("action_primitive"),)


def s_primary(rec):
    u = normalize_url(rec.get("url_after", ""))
    t = normalize_title(rec.get("title_after", ""))
    return hashlib.sha256((u + "|" + t).encode("utf-8")).hexdigest()


def compute_gate(dataset_records, site):
    """Returns gate row dict per frozen relaxed sufficiency."""
    n_raw = len(dataset_records)
    n_sessions = len(set(r.get("session") for r in dataset_records))
    valid = [r for r in dataset_records if r.get("error") is None]
    n_valid = len(valid)

    # leakage among valid, href-bearing actions: normalized target_href ==
    # normalized state_after_url
    n_leaky_valid = 0
    for r in valid:
        if is_href_bearing(r):
            th = target_href(r)
            nu = normalize_url(r.get("url_after", ""))
            nth = normalize_url(th)
            if nth and nth == nu:
                n_leaky_valid += 1
    leakage_valid_only = n_leaky_valid / n_valid if n_valid else float("nan")

    nl_transitions = [r for r in valid if not (is_href_bearing(r) and
                       normalize_url(target_href(r)) == normalize_url(r.get("url_after", "")))]
    NL = len(nl_transitions)

    # strata: unique (URL_before_normalized, H_K=3 actions, Action) with >=3
    # per stratum; H_K requires steps t-2,t-1,t within same trajectory (session)
    per_session = {}
    for r in nl_transitions:
        per_session.setdefault(r["session"], []).append(r)
    strata_counts = Counter()
    for sess, recs in sorted(per_session.items()):
        for i in range(2, len(recs)):
            key = (
                normalize_url(recs[i].get("url_before", "")),
                tuple(leakage_free_action_sig(x) for x in recs[i - 2:i + 1]),
                leakage_free_action_sig(recs[i]),
            )
            strata_counts[key] += 1
    strata_total = len(strata_counts)
    strata_ge3 = sum(1 for c in strata_counts.values() if c >= 3)

    # singleton_SA_rate: fraction of (S_primary, A) pairs with count==1 among NL
    sa = Counter((s_primary(r), leakage_free_action_sig(r)) for r in nl_transitions)
    singleton_count = sum(1 for c in sa.values() if c == 1)
    singleton_sa_rate = singleton_count / len(sa) if sa else float("nan")

    # dom_bytes / a11y coverage: field-level presence scan
    dom_field_present = 0
    a11y_field_present = 0
    for r in dataset_records:
        keys = set(r.keys())
        if any(k in keys for k in ("dom_bytes", "visible_text", "visibleText",
                                   "innerText", "dom_text", "dom_snapshot")):
            db = r.get("dom_bytes")
            if db is not None and db >= 500:
                dom_field_present += 1
        if any(k in keys for k in ("a11y", "a11y_tree", "accessibility_tree",
                                   "ax_tree", "accessibility_roles")):
            v = r.get("a11y", r.get("a11y_tree", r.get("accessibility_tree",
                                                       r.get("accessibility_roles", ""))))
            if v not in (None, [], "", {}):
                a11y_field_present += 1
    dom_bytes_coverage = dom_field_present / n_raw if n_raw else 0.0
    a11y_coverage = a11y_field_present / n_raw if n_raw else 0.0

    titles = set(normalize_title(r.get("title_after", "")) for r in valid)
    unique_titles = len(titles)

    raw_keys = sorted(set().union(*(set(r.keys()) for r in dataset_records)))

    qualifies = (
        NL >= 50
        and strata_total >= 5
        and strata_ge3 >= 5
        and singleton_sa_rate < 0.70
        and leakage_valid_only < 0.60
        and dom_bytes_coverage >= 0.80
        and a11y_coverage >= 0.80
    )
    return {
        "site_id": site,
        "n_raw": n_raw,
        "n_sessions": n_sessions,
        "n_valid": n_valid,
        "n_leaky_valid": n_leaky_valid,
        "leakage_validOnly": round(leakage_valid_only, 4),
        "NL": NL,
        "nl_ge_50": NL >= 50,
        "strata_total": strata_total,
        "strata_ge3": strata_ge3,
        "strata_ge_5_with_ge3": (strata_total >= 5 and strata_ge3 >= 5),
        "singleton_SA_rate": round(singleton_sa_rate, 4),
        "singleton_sa_lt_70pct": singleton_sa_rate < 0.70,
        "dom_bytes_coverage": dom_bytes_coverage,
        "dom_coverage_ge_80pct": dom_bytes_coverage >= 0.80,
        "a11y_coverage": a11y_coverage,
        "a11y_coverage_ge_80pct": a11y_coverage >= 0.80,
        "unique_titles": unique_titles,
        "raw_record_keys": raw_keys,
        "qualifies": qualifies,
    }


def scan_substrate():
    """Substrate availability scan per frozen spec 6.1."""
    scan = {}
    intel = os.path.join(REPO, "research", "intel")
    scan["research_intel_exists"] = os.path.isdir(intel)
    scan["intel_manifest_path"] = os.path.join(intel, "manifest.json") if os.path.isdir(intel) else None
    scan["intel_manifest_exists"] = bool(scan["intel_manifest_path"]) and os.path.isfile(scan["intel_manifest_path"])
    bg = "/tmp/browsergym_cache"
    scan["browsergym_cache_exists"] = os.path.isdir(bg)
    # any BrowserGym/WebShop trajectory file anywhere under the repo?
    hits = []
    for root, dirs, files in os.walk(os.path.join(REPO, "research")):
        for fn in files:
            low = fn.lower()
            if "browsergym" in low or "webshop" in low or "webarena" in low or "miniwob" in low:
                hits.append(os.path.relpath(os.path.join(root, fn), REPO))
    scan["browsergym_webshop_trajectory_files"] = hits
    return scan


def main():
    print(f"PYTHONHASHSEED={PYTHONHASHSEED} experiment={EXPERIMENT_ID}")
    # 1. frozen-input hash verification
    freeze_ok = {}
    for name, expected in FROZEN_HASHES.items():
        p = os.path.join(EXP_DIR, name)
        h = sha256_file(p)
        freeze_ok[name] = (h == expected)
        print(f"freeze verify {name}: {h[:16]} {'MATCH' if h==expected else 'MISMATCH'}")
    assert all(freeze_ok.values()), "frozen input hash mismatch — aborting"

    # 2. raw hash verification against prior experiment artifacts
    raw_manifest = {}
    for fn, expected in PRIOR_RAW_HASHES.items():
        p = os.path.join(SRC_DIR, fn)
        h = sha256_file(p)
        raw_manifest[fn] = {"sha256": h, "matched_prior_record": h == expected}
        print(f"raw verify {fn}: {h[:16]} {'MATCH' if h==expected else 'MISMATCH'}")
    n_match = sum(1 for v in raw_manifest.values() if v["matched_prior_record"])

    # 3. load and gate each dataset variant
    gate_rows = []
    for site in VARIANTS:
        recs = []
        for fn in (f"raw_{site}.json", f"raw_{site}_topup.json"):
            recs.extend(json.load(open(os.path.join(SRC_DIR, fn))))
        row = compute_gate(recs, site)
        gate_rows.append(row)
        print(f"site={site} NL={row['NL']} strata={row['strata_total']}/{row['strata_ge3']} "
              f"singleton={row['singleton_SA_rate']} leak={row['leakage_validOnly']} "
              f"dom_cov={row['dom_bytes_coverage']} a11y_cov={row['a11y_coverage']} "
              f"qualifies={row['qualifies']}")

    Q = sum(1 for r in gate_rows if r["qualifies"])
    print(f"Q (qualifying datasets) = {Q}")

    # 4. substrate availability scan
    scan = scan_substrate()
    print("substrate scan:", json.dumps(scan))

    gate_table = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "frozen_rule": ("dataset qualifies iff after leakage-free filtering NL>=50, "
                        "strata_count>=5 unique (URL_before,H_K=3,Action) with >=3 per stratum, "
                        "singleton_SA_rate<70%, leakage_validOnly<60%, dom_bytes>=500 and "
                        "a11y non-empty on >=80% transitions"),
        "frozen_halt_rule": ("if Q==0 => MEASUREMENT_INVALID substrate_insufficient; "
                             "do not test H_T/H_B; publish gate_table.json"),
        "datasets": gate_rows,
        "Q": Q,
        "substrate_scan": scan,
        "raw_hash_verification": {"matched": n_match, "total": len(raw_manifest),
                                  "manifest": raw_manifest},
        "freeze_hash_verification": freeze_ok,
        "conclusion": ("MEASUREMENT_INVALID substrate_insufficient" if Q == 0
                       else "proceed to pipeline gates and primary H_T/H_B"),
    }
    out = os.path.join(EXP_DIR, "gate_table.json")
    with open(out, "w") as f:
        json.dump(gate_table, f, indent=2, sort_keys=True)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())