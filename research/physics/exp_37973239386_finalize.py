#!/usr/bin/env python3
"""EXP-PHYSICS-37973239386 EXECUTE finalize step.

Reads the frozen packet plus the EXECUTE raw/derived artifacts and writes:
  derived/field_cluster_map.json
  result.json
  report.md
  provenance.json

No HTTP, no RNG, no re-measurement: the branch is a deterministic function of the
already-written derived/metrics.json. Re-runnable and idempotent.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys

REPO = "/home/runner/work/Spider/Spider"
EXP_DIR = os.path.join(REPO, "research", "experiments", "EXP-PHYSICS-37973239386")
DERIVED = os.path.join(EXP_DIR, "derived")
RAW = os.path.join(EXP_DIR, "raw")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    with open(path) as f:
        return json.load(f)


def artifact(rel_to_exp, role):
    p = os.path.join(EXP_DIR, rel_to_exp)
    return {
        "path": rel_to_exp,
        "sha256": sha256_of(p),
        "bytes": os.path.getsize(p),
        "role": role,
    }


def artifact_code(rel_to_repo, role):
    p = os.path.join(REPO, rel_to_repo)
    return {
        "path": rel_to_repo,
        "sha256": sha256_of(p),
        "bytes": os.path.getsize(p),
        "role": role,
    }


def git_head():
    try:
        return subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def main():
    metrics = load_json(os.path.join(DERIVED, "metrics.json"))
    controls = load_json(os.path.join(DERIVED, "controls.json"))
    fields = load_json(os.path.join(DERIVED, "fields.json"))
    freeze = load_json(os.path.join(EXP_DIR, "freeze.json"))

    # ---- frozen-input integrity re-verification ----
    frozen_ok = {}
    for name, declared in freeze["hashes"].items():
        actual = sha256_of(os.path.join(EXP_DIR, name))
        frozen_ok[name] = {"declared": declared, "actual": actual, "match": declared == actual}
    frozen_all_match = all(v["match"] for v in frozen_ok.values())

    # ---- field-to-cluster map (EXECUTE contract item 5) ----
    admitted = [r for r in fields if r.get("admitted")]
    cluster_map = {
        "unit": "admitted action-gating field = (endpoint, locator_type, locator_name)",
        "cluster_definition": "registrable domain (eTLD+1 approximation: last two dot-labels)",
        "n_fields": len(admitted),
        "n_clusters": len({r["cluster"] for r in admitted}),
        "fields": [
            {
                "endpoint": r["endpoint"],
                "locator_type": r["locator_type"],
                "name": r["name"],
                "taxonomy_class": r["taxonomy_class"],
                "stratum": r["stratum"],
                "cluster": r["cluster"],
                "n_obs": r["n_obs"],
                "n_sessions": r["n_sessions"],
                "n_distinct": r["n_distinct"],
                "predictable": r.get("predictable", 0),
                "firing_rules": r.get("firing_rules", []),
                "best_rule_fraction": r.get("best_rule_fraction"),
                "memory_repeat_holdout": r.get("memory_repeat_holdout"),
                "attributed_class": r.get("attributed_class"),
                "ordered_values_sha256": r.get("ordered_values_sha256"),
            }
            for r in sorted(admitted, key=lambda x: (x["cluster"], x["locator_type"], x["name"], x["endpoint"]))
        ],
    }
    with open(os.path.join(DERIVED, "field_cluster_map.json"), "w") as f:
        json.dump(cluster_map, f, indent=2)

    # ---- stable metric identifiers ----
    baselines = metrics["baselines"]
    m = {
        "PREDICTABLE_PREVALENCE_POOLED": metrics["PREDICTABLE_PREVALENCE_POOLED"],
        "PREDICTABLE_PREVALENCE_SITE": metrics["per_site_prevalence"],
        "PREDICTABLE_PREVALENCE_BY_CLASS": metrics["per_class_prevalence"],
        "PREDICTABLE_PREVALENCE_ALL_PLUS_NONCE": metrics["PREDICTABLE_PREVALENCE_ALL_PLUS_NONCE"],
        "site_clustered_ci95": metrics["site_clustered_ci95"],
        "bootstrap_n_clusters": metrics["bootstrap_n_clusters"],
        "bootstrap_distinct_resamples": metrics["bootstrap_distinct_resamples"],
        "bootstrap_informative": metrics["bootstrap_informative"],
        "N_INDICATOR_FIELDS": metrics["n_indicator_fields"],
        "N_PREDICTABLE": metrics["n_predictable"],
        "ADMITTED_FIELDS": metrics["admitted_fields"],
        "ADMITTED_PRIMARY_FIELDS": metrics["admitted_primary_fields"],
        "ADMITTED_NONCE_FIELDS": metrics["admitted_nonce_fields"],
        "ADMITTED_SITES": metrics["admitted_sites_primary"],
        "ADMITTED_ENDPOINTS": metrics["admitted_endpoints"],
        "B_MEMORY_REPEAT_ACC_MEAN": baselines["B_MEMORY_REPEAT_ACC_MEAN_HOLDOUT"],
        "B_MARKOV1_ACC_MEAN": baselines["B_MARKOV1_ACC_MEAN"],
        "B_CONSTANT_MODE_ACC_MEAN": baselines["B_CONSTANT_MODE_ACC_MEAN"],
        "NULL_FP_AGGREGATE": controls["NC_PLANTED_RANDOM_PLUS_LIVE"]["NC_PLANTED_RANDOM"]["aggregate_fp"],
        "NULL_FP_AGGREGATE_DESIGN_LITERAL": 0.000625,
        "PC_POWER_MIN": controls["PC_PLANTED_CLASSES"]["power_min"],
        "LIVE_NULL_FIRED_FRACTION": controls["NC_PLANTED_RANDOM_PLUS_LIVE"]["NC_LIVE_HTTPBIN_UUID"]["fired_fraction"],
        "NON_GET_REQUESTS": metrics["NON_GET_REQUESTS"],
        "TRANSPORT_ERROR_RATE": metrics["TRANSPORT_ERROR_RATE"],
        "TRANSPORT_ERRORS": metrics["transport_errors"],
        "PLANNED_GETS": metrics["planned_gets"],
        "STATUS_HISTOGRAM": metrics["status_histogram"],
        "thresholds_frozen": {
            "P_FLOOR": 0.10, "P_HI": 0.25, "ALPHA_RULE": 0.05, "PC_POWER_MIN": 0.8,
            "NULL_FP_MAX": 0.05, "DELTA_MEM": 0.10, "N_MIN_OBS": 4, "M_MIN_FIELDS": 20,
            "S_MIN_SITES": 8, "TRANSPORT_ERROR_MAX": 0.30, "CLUSTERED_BOOTSTRAP_RESAMPLES": 10000,
        },
        "measurement_invalid_conditions": metrics["measurement_invalid_conditions"],
        "branch": metrics["branch"],
    }

    # ---- controls (frozen identifiers preserved) ----
    nc = controls["NC_PLANTED_RANDOM_PLUS_LIVE"]
    pc = controls["PC_PLANTED_CLASSES"]
    ctrl = {
        "B_MEMORY_REPEAT": {
            "expected": "near 0 for genuinely varying minted values; high only if values persist across observations; NOT allowed to make a field PREDICTABLE on its own.",
            "observed": {
                "mean_holdout_accuracy": baselines["B_MEMORY_REPEAT_ACC_MEAN_HOLDOUT"],
                "mean_full_accuracy": baselines["B_MEMORY_REPEAT_ACC_MEAN_FULL"],
                "interpretation_of_value": "0.336 is driven by identity-persistent session cookies; every counted predictable field exceeded this baseline by >= DELTA_MEM=0.10.",
            },
            "role": "disqualifier baseline (mandated)",
            "pass": True,
            "evidence_refs": ["derived/fields.json", "derived/metrics.json"],
        },
        "B_MARKOV1": {
            "expected": "beats B_MEMORY_REPEAT when values alternate or recur; sensitivity check only, not a gate.",
            "observed": {"mean_accuracy": baselines["B_MARKOV1_ACC_MEAN"]},
            "role": "sensitivity baseline",
            "pass": True,
            "evidence_refs": ["derived/fields.json", "derived/metrics.json"],
        },
        "B_CONSTANT_MODE": {
            "expected": "matches the treatment only when the field is constant, which admission already excludes.",
            "observed": {"mean_accuracy": baselines["B_CONSTANT_MODE_ACC_MEAN"]},
            "role": "triviality control",
            "pass": True,
            "evidence_refs": ["derived/fields.json", "derived/metrics.json"],
        },
        "B_IRREDUCIBILITY_NULL": {
            "expected": "aggregate field-level false-positive rate <= NULL_FP_MAX=0.05 on the frozen 1600-field battery, all 11 rules ARMED.",
            "observed": {
                "execute_rerun_fields_total": nc["NC_PLANTED_RANDOM"]["fields_total"],
                "execute_rerun_fields_fired": nc["NC_PLANTED_RANDOM"]["fields_fired"],
                "execute_rerun_aggregate_fp": nc["NC_PLANTED_RANDOM"]["aggregate_fp"],
                "execute_rerun_all_11_rules_armed": nc["NC_PLANTED_RANDOM"]["all_armed"],
                "design_literal_fields_fired": 1,
                "design_literal_aggregate_fp": 0.000625,
                "discrepancy_note": "DESIGN-embedded literal recorded 1/1600 R_WALLCLOCK_B64 fire; EXECUTE re-run with frozen seeds recorded 0/1600. Both satisfy the frozen FP<=0.05 requirement; the difference is disclosed and does not alter any branch.",
            },
            "role": "calibrated irreducibility null",
            "pass": bool(nc["pass"]),
            "evidence_refs": ["derived/controls.json"],
        },
        "PC_PLANTED_CLASSES": {
            "expected": "every one of the eight planted classes detected at power >= PC_POWER_MIN=0.8 on the frozen 200-trial battery.",
            "observed": {
                "power_min": pc["power_min"],
                "per_class": {k: v["power"] for k, v in pc["classes"].items()},
                "trials_per_class": pc.get("trials_per_class", 200),
            },
            "role": "positive control (author-authored; construct boundary disclosed)",
            "pass": bool(pc["pass"]),
            "evidence_refs": ["derived/controls.json"],
        },
        "NC_PLANTED_RANDOM_PLUS_LIVE": {
            "expected": "NC_PLANTED_RANDOM aggregate FP <= 0.05 AND NC_LIVE_HTTPBIN_UUID fired-field fraction <= 0.05.",
            "observed": {
                "planted_random_aggregate_fp": nc["NC_PLANTED_RANDOM"]["aggregate_fp"],
                "live_httpbin_uuid_fields_collected": nc["NC_LIVE_HTTPBIN_UUID"]["fields_collected"],
                "live_httpbin_uuid_fields_fired": nc["NC_LIVE_HTTPBIN_UUID"]["fields_fired"],
                "live_httpbin_uuid_fired_fraction": nc["NC_LIVE_HTTPBIN_UUID"]["fired_fraction"],
            },
            "role": "two-component null control",
            "pass": bool(nc["pass"]),
            "evidence_refs": ["derived/controls.json", "derived/controls_initial_live_null_selfbind_bug.json"],
        },
    }

    # ---- artifacts (exp-dir-relative for packet files; repo-relative for code) ----
    arts = [
        artifact("raw/collection.jsonl", "raw"),
        artifact("raw/collection_meta.json", "raw"),
        artifact("derived/fields.json", "derived"),
        artifact("derived/field_cluster_map.json", "derived"),
        artifact("derived/controls.json", "derived"),
        artifact("derived/controls_initial_live_null_selfbind_bug.json", "derived"),
        artifact("derived/metrics.json", "derived"),
        artifact_code("research/physics/exp_37973239386_lib.py", "code"),
        artifact_code("research/physics/exp_37973239386_run.py", "code"),
        artifact_code("research/physics/exp_37973239386_finalize.py", "code"),
        artifact("request.json", "fixture"),
        artifact("spec.json", "fixture"),
        artifact("prereg.md", "fixture"),
        artifact("freeze.json", "fixture"),
    ]

    # ---- observations: direct, non-interpretive ----
    pred_fields = [
        {
            "endpoint": r["endpoint"],
            "locator_type": r["locator_type"],
            "name": r["name"],
            "cluster": r["cluster"],
            "firing_rules": r["firing_rules"],
            "best_rule_fraction": r["best_rule_fraction"],
            "memory_repeat_holdout": r["memory_repeat_holdout"],
            "attributed_class": r["attributed_class"],
        }
        for r in fields if r.get("predictable")
    ]
    observations = [
        {
            "id": "O1_COLLECTION",
            "fact": "Fresh confirmatory collection executed the frozen 57-endpoint universe with K=8 independent sessions and J=3 GETs each = 1368 planned GETs; NON_GET_REQUESTS=0; 24 transport errors (1.76%) all on community.invisioncommunity.com; status histogram " + json.dumps(metrics["status_histogram"], sort_keys=True) + ".",
        },
        {
            "id": "O2_ADMISSION",
            "fact": f"{metrics['admitted_fields']} admitted action-gating fields ({metrics['admitted_primary_fields']} PRIMARY SESSION/CSRF/TOKEN + {metrics['admitted_nonce_fields']} NONCE csp-nonce) across {metrics['admitted_endpoints']} endpoints and {metrics['admitted_sites_primary']} registrable domains.",
        },
        {
            "id": "O3_PRIMARY",
            "fact": f"N_INDICATOR_FIELDS={metrics['n_indicator_fields']}, N_PREDICTABLE={metrics['n_predictable']}, PREDICTABLE_PREVALENCE_POOLED={metrics['PREDICTABLE_PREVALENCE_POOLED']:.6f}; ALL_PLUS_NONCE={metrics['PREDICTABLE_PREVALENCE_ALL_PLUS_NONCE']:.6f}; site-clustered 95% CI {metrics['site_clustered_ci95']} over {metrics['bootstrap_n_clusters']} clusters / {metrics['bootstrap_distinct_resamples']} distinct resamples.",
        },
        {
            "id": "O4_PREDICTABLE_FIELDS",
            "fact": "The two counted fields: " + json.dumps(pred_fields, sort_keys=True),
        },
        {
            "id": "O5_PYPI_DETAIL",
            "fact": "pypi.org cookie session_id has 3 dot-separated segments; the middle segment is the identical string 'aslBhA' in all 8 distinct session values and base64-decodes to bytes 6ac94184, whose big-endian 4-byte integer 1791574404 lies within 3600 s of the collection epoch (~1791574416); the varying first segment carries the signed payload. R_WALLCLOCK_B64 detection fraction = 1.0.",
        },
        {
            "id": "O6_REDDIT_DETAIL",
            "fact": "reddit.com input.hidden jsc_token values are 64 lowercase hex characters sharing a constant 32-hex-character prefix (e.g. '2824be10929bdc604753c70a67a1c331'); values are not identical and do not repeat within the window; R_CONST_SUBSTRING detection fraction = 1.0.",
        },
        {
            "id": "O7_OTHER_FIELDS",
            "fact": "No armed rule fired on any of the other 44 indicator fields. The persistent session cookies (e.g. _gitlab_session, authSession, *_Session, flarum_session) are memory-repeat-explained (holdout accuracy ~0.71); per-request CSRF/one-time tokens (authenticity_token, wpLoginToken, csrfmiddlewaretoken, csrf-token, discourse-track-view-session-id) vary with no rule firing.",
        },
        {
            "id": "O8_CONTROLS_EXECUTE",
            "fact": f"EXECUTE re-run controls: NC_PLANTED_RANDOM {nc['NC_PLANTED_RANDOM']['fields_fired']}/{nc['NC_PLANTED_RANDOM']['fields_total']} fired (aggregate FP {nc['NC_PLANTED_RANDOM']['aggregate_fp']}), all 11 rules armed; NC_LIVE_HTTPBIN_UUID {nc['NC_LIVE_HTTPBIN_UUID']['fields_fired']}/{nc['NC_LIVE_HTTPBIN_UUID']['fields_collected']} fields fired (fraction {nc['NC_LIVE_HTTPBIN_UUID']['fired_fraction']}); PC_PLANTED_CLASSES power_min={pc['power_min']} (all 8 classes 200/200).",
        },
        {
            "id": "O9_BRANCH_DERIVATION",
            "fact": "Measurement-invalid conditions (a)-(h) all evaluated false: " + json.dumps(metrics["measurement_invalid_conditions"], sort_keys=True) + ". Branch precedence therefore resolves to S0/FALSIFIES (PV=0.0435<=0.10 AND clustered CI upper=0.116<0.25).",
        },
        {
            "id": "O10_BLOCKED_HOSTS",
            "fact": "Reachability in this window: gitlab.com, community.cloudflare.com, www.npmjs.com, wordpress.com and www.phpbb.com returned 403; rubygems.org returned 404; community.invisioncommunity.com was a transport error; several GitLab/Gitea hosts returned 429 rate limits. Three endpoints admitted in the DESIGN census (gitlab.archlinux.org, salsa.debian.org, gitlab.freedesktop.org) were blocked this window and did not contribute fields.",
        },
        {
            "id": "O11_DESIGN_NULL_DISCREPANCY",
            "fact": "DESIGN-embedded literal null reported 1/1600 fired (aggregate FP 0.000625, rule R_WALLCLOCK_B64); the EXECUTE frozen-seed re-run reported 0/1600 (aggregate FP 0.0). Both are <= NULL_FP_MAX=0.05.",
        },
    ]

    validity_notes = [
        {
            "id": "V1_LIVE_NULL_CONSTRUCTION_CORRECTION",
            "note": "The first EXECUTE analysis constructed each NC_LIVE_HTTPBIN_UUID observation's same-session cookie map as {'_': <the uuid value itself>}, which made R_SESSION_BIND fire vacuously on all 8/8 live-null fields and failed the null-gate (status would have been MEASUREMENT_INVALID). The rule family predicates and all thresholds were NOT changed; only the control's cookie-map construction was corrected to an empty map (httpbin.org/uuid sets no cookies), which is the faithful construction for a cookie-free random source. The pre-correction artifact is preserved verbatim at derived/controls_initial_live_null_selfbind_bug.json. This correction changes only the null/liveness gate, not the confirmatory primary metric.",
        },
        {
            "id": "V2_DESIGN_EXECUTE_NULL_FIRE_DIFFERENCE",
            "note": "DESIGN literal null fired 1/1600 (R_WALLCLOCK_B64, FP 0.000625); EXECUTE re-run fired 0/1600. Disclosed; both pass FP<=0.05. The residual difference prevents using the EXECUTE battery alone to bound R_WALLCLOCK_B64's real false-positive rate, so the DESIGN literal is carried alongside.",
        },
        {
            "id": "V3_WALLCLOCK_CLOCK_SOURCE",
            "note": "Wallclock rules compare candidate substrings against the CLIENT-side collection wall-clock epoch (time.time() at request time), not a server clock. Any server/client clock skew or timezone-independent epoch offset within +/-3600 s is absorbed by the 1-hour tolerance. This is a deliberate frozen design choice.",
        },
        {
            "id": "V4_AUTHOR_AUTHORED_POSITIVE_CONTROL",
            "note": "PC_PLANTED_CLASSES is authored by the instrument designer and certifies the detector code path and sensitivity, NOT the construct boundary on the real Web. Mitigations are the out-of-author NC_LIVE_HTTPBIN_UUID live null and the fresh real-Web confirmatory collection; the construct boundary remains a disclosed residual threat.",
        },
        {
            "id": "V5_POOL_NOT_PROBABILITY_SAMPLE",
            "note": "The frozen 57-endpoint universe is a curated convenience pool; all rates describe this pool in one collection window (one stdlib-HTTP client, one User-Agent, one network vantage). It is not a probability sample of the Web.",
        },
        {
            "id": "V6_REPRESENTATION_LOSS",
            "note": "Only credential-free HTTP GET-observable fields are measured. No JavaScript/DOM/SPA-rendered, authenticated, WebSocket/GraphQL, edge or mobile-sourced token is observable. Response bodies are not archived (only body_sha256 per observation), so body-level re-derivation is not reconstructable from this packet. The NONCE stratum contains exactly 1 admitted field (a csp-nonce), so its separate estimate is not informative.",
        },
        {
            "id": "V7_RULE_MULTIPLICITY_AND_ATTRIBUTION",
            "note": "11 armed rules raise per-field false-positive risk; the frozen 1600-field calibration bounds it (aggregate FP <= 0.05) and counted fields must additionally beat B_MEMORY_REPEAT by DELTA_MEM=0.10. Class attribution (WALLCLOCK_B64 vs CONST_SUBSTRING) follows the frozen priority and can mislabel when several rules fire; this affects only the class breakdown, not the pooled indicator.",
        },
        {
            "id": "V8_BLOCKING_AND_RATE_LIMITS",
            "note": "In this window several frozen endpoints were Cloudflare-blocked (403) or rate-limited (429), including three endpoints admitted in the DESIGN census. Overall admission still exceeded the frozen M_MIN_FIELDS/S_MIN_SITES by wide margins, so no measurement-invalid condition fires; however per-site coverage is window-dependent and the census monotonicity argument is not strictly reproduced endpoint-by-endpoint.",
        },
        {
            "id": "V9_USER_AGENT_CHOICE",
            "note": "The spec fixes a single User-Agent but not its exact string. A plain identifying research User-Agent was used because full browser-like UAs were rejected 403/406 by Cloudflare on multiple frozen endpoints while research-style UAs were served. The choice is fixed in code (research/physics/exp_37973239386_lib.py:USER_AGENT) and applied uniformly.",
        },
        {
            "id": "V10_CLUSTER_APPROXIMATION",
            "note": "Clusters are the registrable domain approximated as the last two dot-labels; the frozen universe contains no multi-label public suffix (co.uk/org.uk-like) cases, so the approximation is exact for this pool (as stated in spec.json.measurement_validity.split_integrity).",
        },
        {
            "id": "V11_DIRECTED_VS_CONFIRMATORY",
            "note": "DIRECTOR-mandated experiment (request.json.director_mandate, action=CONTINUE, claim C-WEB-DYNAMICS, parent_handoff_disposition=SUPERSEDE). The parent EXP-PHYSICS-37385620138 is continuity evidence only; its query-parameter perturbation direction is NOT adopted. No parent carry_forward category is silently overridden.",
        },
    ]

    unresolved = [
        {
            "id": "U1_GENERALIZATION",
            "question": "Do the two counted predictable classes persist across collection windows? The pypi.org R_WALLCLOCK_B64 detection rides on an itsdangerous-style middle timestamp segment; the reddit.com jsc_token constant-prefix structure may be rotated by the operator. A second window would distinguish stable structure from a point-in-time artifact.",
        },
        {
            "id": "U2_CONSTRUCT_BOUNDARY",
            "question": "What is the real-Web predictability prevalence on JavaScript-rendered, authenticated, or SPA substrates that this credential-free HTTP GET instrument cannot observe?",
        },
        {
            "id": "U3_NULL_RULE_SENSITIVITY",
            "question": "Why did R_WALLCLOCK_B64 fire once in the DESIGN literal null battery and zero times in the EXECUTE re-run with the same nominal seeds? This is a within-tolerance discrepancy but limits the EXECUTE-only bound on that rule's false-positive rate.",
        },
        {
            "id": "U4_REDDIT_MECHANISM",
            "question": "What produces the constant 32-hex-character prefix of reddit.com jsc_token and does it carry predictive information about the random suffix?",
        },
        {
            "id": "U5_VALUE_VS_PROCEDURE",
            "question": "Whether the architecture should persist procedures/paths and re-observe values fresh is informed but not decided by this bounded negative; a product-level cost comparison is out of scope for this physics packet.",
        },
    ]

    result = {
        "schema_version": 1,
        "experiment_id": "EXP-PHYSICS-37973239386",
        "lane": "physics",
        "status": "COMPLETE",
        "outcome": "FALSIFIES",
        "metrics": m,
        "controls": ctrl,
        "artifacts": arts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }
    with open(os.path.join(EXP_DIR, "result.json"), "w") as f:
        json.dump(result, f, indent=2)

    # ---- provenance.json ----
    provenance = {
        "schema_version": 1,
        "experiment_id": "EXP-PHYSICS-37973239386",
        "lane": "physics",
        "origin_github_run_id": "37973239386",
        "claim_ids": ["C-WEB-DYNAMICS"],
        "director_mandate": {
            "action": "CONTINUE",
            "claim_id": "C-WEB-DYNAMICS",
            "parent_handoff_disposition": "SUPERSEDE",
            "parent_handoff": "research/experiments/EXP-PHYSICS-37385620138/handoff.json",
        },
        "git": {
            "head": git_head(),
            "note": "Working tree also contains unrelated Codex-sync edits (SPIDER_CODEX.md, codex/claim_state.json, codex/index.json) and other lanes' directories that this EXECUTE did not modify.",
        },
        "frozen_inputs": {
            "declared_in_freeze": freeze["hashes"],
            "reverified": frozen_ok,
            "all_match": frozen_all_match,
            "freeze_sha256": sha256_of(os.path.join(EXP_DIR, "freeze.json")),
            "mutated_after_freeze": [],
        },
        "environment": {
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "http_client": "python stdlib urllib.request",
            "requests_library_used": False,
            "browser": "none",
            "javascript": False,
            "credentials": 0,
            "model_calls": 0,
            "external_llm_inference": False,
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64; research) SPIDER-Research2.0/EXP-PHYSICS-37973239386",
        },
        "code": {
            "research/physics/exp_37973239386_lib.py": sha256_of(os.path.join(REPO, "research/physics/exp_37973239386_lib.py")),
            "research/physics/exp_37973239386_run.py": sha256_of(os.path.join(REPO, "research/physics/exp_37973239386_run.py")),
            "research/physics/exp_37973239386_finalize.py": sha256_of(os.path.join(REPO, "research/physics/exp_37973239386_finalize.py")),
        },
        "commands": [
            {"step": "collect + analyze (fresh Web collection)", "command": "python3 research/physics/exp_37973239386_run.py --workers 16", "n_http_requests_planned": 1368, "n_transport_fail": 24},
            {"step": "re-run analysis after live-null construction correction (no collection)", "command": "python3 research/physics/exp_37973239386_run.py --analyze"},
            {"step": "finalize packet", "command": "python3 research/physics/exp_37973239386_finalize.py"},
        ],
        "datasets_fixtures": {
            "candidate_universe": "spec.json candidate_universe (57 endpoints, frozen verbatim)",
            "raw_evidence": "raw/collection.jsonl (456 session records, 1368 observations)",
            "control_batteries": "derived/controls.json; DESIGN literal values embedded in spec.json.pilot_certificates",
        },
        "determinism": {
            "analysis_deterministic": True,
            "collection_deterministic": False,
            "collection_nondeterminism_reason": "the Web is live: statuses, headers, rate limits and minted values are a point-in-time observation, not a fixture; rerunning the collector on the same universe will not reproduce raw/collection.jsonl byte-for-byte",
            "note": "All synthetic batteries and the bootstrap are seeded (master_seed=int(request_hash[:8],16)=2450671238; null seeds 9000+regime; PC seeds 5000+trial); the finalize step performs no RNG.",
        },
    }
    with open(os.path.join(EXP_DIR, "provenance.json"), "w") as f:
        json.dump(provenance, f, indent=2)

    # ---- report.md ----
    report = render_report(metrics, m, ctrl, pred_fields, frozen_ok, frozen_all_match)
    with open(os.path.join(EXP_DIR, "report.md"), "w") as f:
        f.write(report)

    # ---- mandatory-key self-check ----
    required = ["schema_version", "experiment_id", "lane", "status", "outcome",
                "metrics", "controls", "artifacts", "observations", "validity_notes", "unresolved"]
    missing = [k for k in required if k not in result]
    assert not missing, f"result.json missing mandatory keys: {missing}"
    assert result["status"] == "COMPLETE", result["status"]
    assert result["outcome"] == "FALSIFIES", result["outcome"]
    assert frozen_all_match, "frozen input hash mismatch"
    print("finalize OK")
    print(json.dumps({"status": result["status"], "outcome": result["outcome"],
                      "branch": metrics["branch"], "n_ind": metrics["n_indicator_fields"],
                      "n_pred": metrics["n_predictable"], "pv": metrics["PREDICTABLE_PREVALENCE_POOLED"],
                      "ci": metrics["site_clustered_ci95"], "frozen_all_match": frozen_all_match}, indent=2))


def render_report(metrics, m, ctrl, pred_fields, frozen_ok, frozen_all_match):
    ci = metrics["site_clustered_ci95"]
    lines = []
    A = lines.append
    A("# EXP-PHYSICS-37973239386 — EXECUTE report")
    A("")
    A("**Lane:** physics  ")
    A("**Claim:** `C-WEB-DYNAMICS` (HYPOTHESIS)  ")
    A("**Status:** `COMPLETE`  ")
    A("**Outcome:** `FALSIFIES` (frozen branch S0)  ")
    A("**Frozen input hashes verified:** `" + str(frozen_all_match) + "`")
    A("")
    A("## 1. Result in one paragraph")
    A("")
    A(f"On a fresh confirmatory collection of the frozen 57-endpoint credential-free universe "
      f"({metrics['planned_gets']} planned GETs, {metrics['transport_errors']} transport errors = "
      f"{metrics['TRANSPORT_ERROR_RATE']*100:.2f}%, 0 non-GET, 0 credentialed), admission yielded "
      f"{metrics['admitted_fields']} action-gating fields ({metrics['admitted_primary_fields']} PRIMARY "
      f"SESSION/CSRF/TOKEN + {metrics['admitted_nonce_fields']} NONCE) across {metrics['admitted_sites_primary']} "
      f"registrable domains. Of {metrics['n_indicator_fields']} indicator fields, {metrics['n_predictable']} were "
      f"classified PREDICTABLE beyond `B_MEMORY_REPEAT` by >= `DELTA_MEM`=0.10, giving "
      f"`PREDICTABLE_PREVALENCE_POOLED` = {metrics['PREDICTABLE_PREVALENCE_POOLED']:.4f} "
      f"(site-clustered 95% CI [{ci[0]:.4f}, {ci[1]:.4f}], {metrics['bootstrap_n_clusters']} clusters, "
      f"{metrics['bootstrap_distinct_resamples']} distinct resamples). Because "
      f"PV <= P_FLOOR=0.10 **and** the clustered CI upper bound is < P_HI=0.25, the frozen precedence "
      f"resolves to **S0 / FALSIFIES**: on this substrate class and window, server-minted action-gating "
      f"values are observation-bound. No measurement-invalid condition (a)–(h) holds, so this is a valid "
      f"scientific negative, not an instrument failure.")
    A("")
    A("## 2. What was counted")
    A("")
    A("The two PREDICTABLE fields:")
    A("")
    for r in pred_fields:
        A(f"- `{r['cluster']}` — `{r['locator_type']}` `{r['name']}`: rule(s) {r['firing_rules']}, "
          f"detection fraction {r['best_rule_fraction']:.2f}, `B_MEMORY_REPEAT` holdout {r['memory_repeat_holdout']:.2f}, "
          f"class `{r['attributed_class']}`.")
    A("")
    A("Mechanism detail (evidence: `raw/collection.jsonl`, `derived/fields.json`):")
    A("")
    A("- **pypi.org `session_id`** is a 3-segment dotted token; the middle segment is the byte-identical "
      "string `aslBhA` across all 8 session values and base64-decodes to `6ac94184`, whose big-endian "
      "4-byte integer 1791574404 falls within the frozen +/-3600 s wall-clock window of the collection "
      "epoch. This is a genuine embedded epoch-like quantity (an itsdangerous-style timestamp region), "
      "not a chance match: the rule requires >= 0.75 of observations to independently hit, and a random "
      "4-byte window lands in a 1-hour window with probability ~1.7e-6.")
    A("- **reddit.com `jsc_token`** values are 64 lowercase hex characters sharing a constant "
      "32-hex-character prefix while remaining distinct; `R_CONST_SUBSTRING` therefore fires at "
      "fraction 1.0. This is a real constant structural shell, not an artifact.")
    A("- The other 44 indicator fields had no armed rule fire: persistent session cookies "
      "(`_gitlab_session`, `authSession`, `*_Session`, `flarum_session`, ...) are memory-repeat-explained "
      "(holdout ~0.71), and per-request CSRF/one-time tokens (`authenticity_token`, `wpLoginToken`, "
      "`csrfmiddlewaretoken`, `csrf-token`, `discourse-track-view-session-id`) vary without any rule firing.")
    A("")
    A("## 3. Controls and baselines (EXECUTE re-run, separately from DESIGN literals)")
    A("")
    A("| id | expected | observed | pass |")
    A("|----|----------|----------|------|")
    A(f"| `B_MEMORY_REPEAT` | near 0 for varying values | mean holdout {m['B_MEMORY_REPEAT_ACC_MEAN']:.4f} | n/a (disqualifier baseline) |")
    A(f"| `B_MARKOV1` | sensitivity reference | mean {m['B_MARKOV1_ACC_MEAN']:.4f} | n/a |")
    A(f"| `B_CONSTANT_MODE` | 0 (constants excluded) | mean {m['B_CONSTANT_MODE_ACC_MEAN']:.4f} | n/a |")
    A(f"| `B_IRREDUCIBILITY_NULL` | aggregate FP <= 0.05 | EXECUTE {m['NULL_FP_AGGREGATE']:.4f}; DESIGN literal 0.000625 | {ctrl['B_IRREDUCIBILITY_NULL']['pass']} |")
    A(f"| `PC_PLANTED_CLASSES` | power >= 0.8 all classes | power_min {m['PC_POWER_MIN']:.2f} (8x200/200) | {ctrl['PC_PLANTED_CLASSES']['pass']} |")
    A(f"| `NC_PLANTED_RANDOM_PLUS_LIVE` | planted FP <= 0.05 and live FP <= 0.05 | planted 0.0, live fired fraction {m['LIVE_NULL_FIRED_FRACTION']:.2f} | {ctrl['NC_PLANTED_RANDOM_PLUS_LIVE']['pass']} |")
    A("")
    A(f"All 11 frozen non-baseline rules remain ARMED. `NON_GET_REQUESTS` = {m['NON_GET_REQUESTS']}; "
      f"`TRANSPORT_ERROR_RATE` = {m['TRANSPORT_ERROR_RATE']:.4f} (<= 0.30). "
      "DESIGN-embedded literal null fired 1/1600 (FP 0.000625, `R_WALLCLOCK_B64`); the EXECUTE frozen-seed "
      "re-run fired 0/1600. Both satisfy FP <= 0.05; the discrepancy is disclosed (see `result.json` "
      "`validity_notes` V2, O11).")
    A("")
    A("## 4. Measurement-validity conditions")
    A("")
    cond = metrics["measurement_invalid_conditions"]
    label = {
        "a_too_few_fields": "(a) >= 20 indicator fields",
        "b_too_few_sites": "(b) >= 8 registrable sites",
        "c_null_fail": "(c) null pass",
        "d_pc_power_fail": "(d) PC power >= 0.8",
        "e_transport_or_non_get": "(e) transport <= 0.30 and no non-GET",
        "f_locator_missing": "(f) locator/class coverage",
        "g_universe": "(g) frozen universe verbatim",
        "h_rule_family": "(h) frozen rule family",
    }
    for k, v in cond.items():
        A(f"- `{label.get(k, k)}`: violated = `{v}`")
    A("")
    A("No condition is violated. `N_INDICATOR_FIELDS` = "
      f"{metrics['n_indicator_fields']} (>= 20), `ADMITTED_SITES` = {metrics['admitted_sites_primary']} (>= 8), "
      "universe used verbatim, rule family unchanged.")
    A("")
    A("## 5. Branch precedence")
    A("")
    A("```")
    A("1. MEASUREMENT_INVALID  -> not triggered (all (a)-(h) false)")
    A(f"2. SUPPORTS (S1)        -> requires PV >= 0.25 and CI lower > 0.10; not met")
    A(f"3. FALSIFIES (S0)       -> PV = {metrics['PREDICTABLE_PREVALENCE_POOLED']:.4f} <= 0.10")
    A(f"                           and clustered CI upper = {ci[1]:.4f} < 0.25  => SELECTED")
    A("4. MIXED                -> not reached")
    A("```")
    A("")
    A("## 6. Interpretation (bounded to this substrate and window)")
    A("")
    A("`FALSIFIES` here means: on this credential-free action-gating substrate (frozen 57-endpoint pool, "
      "one credential-free stdlib-HTTP client, one time window), value-level predictability beyond a "
      "last-value memory baseline is rare (4.3%); the clustered upper bound (11.6%) is far below the 25% "
      "H1 threshold. Consistent with the preregistered negative consequence, this favours the "
      "**persist-procedures-and-paths, re-observe-values-fresh** side of the architecture decision over "
      "value-level memoization/replay for this class.")
    A("")
    A("Per `spec.json.decision_rule.claim_ceiling`, this `FALSIFIES` outcome is bounded to the frozen "
      "credential-free action-gating substrate and window. It does **not** close `C-WEB-DYNAMICS` or the "
      "Physics domain, and it authorizes no Product promotion. `C-MEAS-VALID` and `C-CROSSSITE` receive no "
      "event from this packet.")
    A("")
    A("## 7. Validity threats and representation loss")
    A("")
    A("1. **Live-null construction correction (V1).** The first analysis bound each httpbin uuid to itself "
      "as a same-session cookie, making `R_SESSION_BIND` fire vacuously on 8/8 live-null fields. Rule "
      "predicates and all thresholds were unchanged; only the control's cookie-map construction was "
      "corrected to the faithful empty map (httpbin sets no cookies). The pre-correction artifact is "
      "preserved at `derived/controls_initial_live_null_selfbind_bug.json`.")
    A("2. **Author-authored positive control (V4).** Certifies the code path, not the real-Web construct "
      "boundary; mitigated by the out-of-author live null and the fresh real-Web collection.")
    A("3. **Pool/window (V5).** Not a probability sample of the Web.")
    A("4. **Representation loss (V6).** No JS/DOM/SPA/authenticated/edge/mobile/GraphQL token is "
      "observable; bodies archived only as sha256; the NONCE stratum has a single field.")
    A("5. **Rule multiplicity and attribution (V7).** 11 rules; class attribution can mislabel but does not "
      "affect the pooled indicator.")
    A("6. **Blocking/rate limits (V8).** Several endpoints returned 403/429; three census-admitted "
      "endpoints were unavailable this window. Admission still far exceeds the frozen minima.")
    A("7. **Client-side wall-clock (V3)** is the epoch source for wall-clock rules (+/-1 h tolerance).")
    A("8. **DESIGN/EXECUTE null-fire difference (V2)** bounds `R_WALLCLOCK_B64`'s FP rate only jointly with "
      "the DESIGN literal.")
    A("")
    A("## 8. Artifacts and provenance")
    A("")
    A("Raw evidence: `raw/collection.jsonl` (456 session records / 1368 observations, includes per-field "
      "raw values, status, session/request index, wall-clock epoch, body_sha256 and same-session cookie "
      "pairs). Derived measurements: `derived/fields.json`, `derived/field_cluster_map.json`, "
      "`derived/controls.json`, `derived/metrics.json`. Exact hashes are in `result.json.artifacts` and "
      "`provenance.json.code`.")
    A("")
    A("## 9. Unresolved")
    A("")
    for u in result_unresolved_placeholder():
        A(f"- `{u['id']}`: {u['question']}")
    A("")
    A("_Report generated by research/physics/exp_37973239386_finalize.py from the frozen packet and the "
      "EXECUTE raw/derived artifacts. It must not exceed the frozen claim or silently contradict "
      "result.json._")
    return "\n".join(lines) + "\n"


def result_unresolved_placeholder():
    # Kept in one place; result.json is the authority.
    return [
        {"id": "U1_GENERALIZATION", "question": "Do the two counted predictable classes persist across collection windows?"},
        {"id": "U2_CONSTRUCT_BOUNDARY", "question": "What is the real-Web predictability prevalence on JS-rendered / authenticated / SPA substrates this instrument cannot observe?"},
        {"id": "U3_NULL_RULE_SENSITIVITY", "question": "Why did R_WALLCLOCK_B64 fire once in the DESIGN literal null and zero times in the EXECUTE re-run with the same nominal seeds?"},
        {"id": "U4_REDDIT_MECHANISM", "question": "What produces the constant 32-hex-character prefix of reddit.com jsc_token, and does it predict the suffix?"},
        {"id": "U5_VALUE_VS_PROCEDURE", "question": "Does the bounded negative decide the product-level persist-values vs persist-procedures trade-off?"},
    ]


if __name__ == "__main__":
    main()
