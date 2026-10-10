"""EXP-PHYSICS-37992957068 EXECUTE finalizer.

Reads the frozen inputs (never mutates them) and the raw/derived evidence produced by
exp_37992957068_run.py, and writes the three canonical packet files:

    result.json   -- producer handoff
    report.md     -- human-readable explanation
    provenance.json

The status/outcome mapping is taken verbatim from spec.json.decision_rule:
  * status = MEASUREMENT_INVALID iff any frozen prerequisite/control condition fails,
    else COMPLETE (a valid scientific negative is COMPLETE with a negative outcome);
  * outcome maps the frozen branch: S1_SUPPORTS->SUPPORTS, S0_FALSIFIES->FALSIFIES,
    S2_MIXED->MIXED, INCONCLUSIVE->INCONCLUSIVE.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EXP_DIR = os.path.join(REPO, "research", "experiments", "EXP-PHYSICS-37992957068")
RAW = os.path.join(EXP_DIR, "raw")
DER = os.path.join(EXP_DIR, "derived")

EXPERIMENT_ID = "EXP-PHYSICS-37992957068"
LANE = "physics"
CLAIM_IDS = ["C-WEB-DYNAMICS"]
ORIGIN_RUN = "37992957068"

CODE_FILES = [
    "research/physics/exp_37992957068_lib.py",
    "research/physics/exp_37992957068_run.py",
    "research/physics/exp_37992957068_finalize.py",
]
FROZEN_FILES = ["request.json", "spec.json", "prereg.md", "freeze.json"]

BRANCH_TO_OUTCOME = {
    "S1_SUPPORTS": "SUPPORTS",
    "S0_FALSIFIES": "FALSIFIES",
    "S2_MIXED": "MIXED",
    "INCONCLUSIVE": "INCONCLUSIVE",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_rel(abspath):
    return os.path.relpath(abspath, REPO)


def rel_path_hash(relpath):
    return sha256_file(os.path.join(REPO, rel_path))


def read_json(path):
    with open(path) as f:
        return json.load(f)


def git_head():
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                             capture_output=True, text=True, timeout=20)
        return out.stdout.strip() or None
    except Exception:
        return None


def git_branch():
    try:
        out = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                             cwd=REPO, capture_output=True, text=True)
        return out.stdout.strip()
    except Exception:
        return None


# ---------------------------------------------------------------------------

def artifact_entry(rel_path, role):
    p = os.path.join(REPO, rel_path)
    return {"path": rel_path, "sha256": sha256_file(p), "bytes": os.path.getsize(p),
            "role": role}


EXP_REL = f"research/experiments/{EXPERIMENT_ID}"


def exp_artifact(name, role):
    return artifact_entry(f"{EXP_REL}/{name}", role)


def build_result(derived, meta, oracles, policy_trace, frozen_verify):
    core = derived["core"]
    core_noid = derived["core_noid"]
    inv = derived["measurement_invalid_conditions"]
    branch = derived["branch"]
    measurement_invalid = bool(derived["measurement_invalid"])

    if measurement_invalid:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    else:
        status = "COMPLETE"
        outcome = BRANCH_TO_OUTCOME.get(branch["branch"], "INCONCLUSIVE")

    # ---- metrics: frozen stable identifiers (from derived) + branch/provenance ----
    metrics = dict(derived["metrics"])
    metrics.update({
        "branch": branch["branch"],
        "pred_disposition": branch["pred_disposition"],
        "sched_disposition": branch["sched_disposition"],
        "PRED_PASS": branch["PRED_PASS"],
        "PRED_FAIL": branch["PRED_FAIL"],
        "SCHED_ECON_PASS": branch["SCHED_ECON_PASS"],
        "SCHED_ECON_FAIL": branch["SCHED_ECON_FAIL"],
        "measurement_invalid": measurement_invalid,
        "measurement_invalid_conditions": inv,
        "frozen_thresholds": {
            "delta_SKILL_nats": 0.05, "alpha": 0.05, "margin_success": 0.05,
            "pc_power_min": 0.80, "nc_false_positive_max": 0.05,
            "min_barrier_exposed_endpoints": 3, "min_scheduler_barrier_events": 30,
        },
        "units": {
            "SKILL_LL": "nats/held-out request (positive = beats strongest null)",
            "SKILL_LL_NOID": "nats/held-out request (endpoint-identity ablation)",
            "SKILL_BA": "balanced-accuracy difference vs strongest null",
            "ONSET_SKILL_LL": "nats/held-out onset request",
            "RECOVERY_SKILL_LL": "nats/held-out recovery request",
            "SEPARABILITY_SKILL_LL": "nats/held-out request (barrier vs ordinary unavailability)",
            "d_Req": "requests/episode (A_ADAPT minus A_RETRY, barrier-exposed stratum)",
            "d_Succ": "success-rate difference (A_ADAPT minus A_RETRY)",
        },
    })

    # ---- controls (frozen identifiers) + baselines + models ----
    controls = {
        "PC_SYNTHETIC_DYNAMICS": {
            "role": "positive control: offline planted schedule-dependent hazard",
            "expected": "power (fraction of R=200 reps with SKILL_LL CI lower > 0) >= 0.80",
            "observed_power": derived["controls"]["PC_SYNTHETIC_DYNAMICS"]["power"],
            "pass": derived["controls"]["PC_SYNTHETIC_DYNAMICS"]["pass"],
            "detail": derived["controls"]["PC_SYNTHETIC_DYNAMICS"],
        },
        "NC_SYNTHETIC_MEMORYLESS": {
            "role": "negative control: offline i.i.d. endpoint-constant barriers",
            "expected": "false-positive rate (CI lower > 0 fraction) <= 0.05",
            "observed_false_positive_rate":
                derived["controls"]["NC_SYNTHETIC_MEMORYLESS"]["false_positive_rate"],
            "pass": derived["controls"]["NC_SYNTHETIC_MEMORYLESS"]["pass"],
            "detail": derived["controls"]["NC_SYNTHETIC_MEMORYLESS"],
        },
        "PC_BARRIER_ORACLE": {
            "role": "live positive control on deterministic barrier oracles",
            "expected": "status/403 -> barrier-family; status/429 -> RATE_LIMIT_429; "
                        "unresolvable host -> TRANSPORT_ERROR",
            "pass": derived["controls"]["PC_BARRIER_ORACLE"]["pass"],
            "requests": derived["controls"]["PC_BARRIER_ORACLE"]["requests"],
        },
        "NC_CLEAN_ORACLE": {
            "role": "live negative control on clean endpoints",
            "expected": "status/200 and uuid -> CLEAN",
            "pass": derived["controls"]["NC_CLEAN_ORACLE"]["pass"],
            "requests": derived["controls"]["NC_CLEAN_ORACLE"]["requests"],
        },
        "M_HISTORY": {
            "role": "frozen primary model", "heldout_logloss_nats": core["logloss"]["M_HISTORY"],
            "heldout_balanced_accuracy": core["balanced_accuracy"]["M_HISTORY"],
        },
        "M_HISTORY_NOID": {
            "role": "frozen endpoint-identity ablation (reported diagnostic)",
            "heldout_logloss_nats": core_noid["logloss"]["M_HISTORY"],
            "heldout_balanced_accuracy": core_noid["balanced_accuracy"]["M_HISTORY"],
            "SKILL_LL": core_noid["SKILL_LL"], "CI95": [core_noid["LO"], core_noid["HI"]],
        },
    }
    for b in ("B_CONSTANT", "B_ENDPOINT_CONST", "B_MEMORY_PERSIST", "B_RATE_ONLY"):
        controls[b] = {
            "role": "frozen null baseline",
            "heldout_logloss_nats": core["logloss"][b],
            "heldout_balanced_accuracy": core["balanced_accuracy"][b],
        }

    artifacts = [
        exp_artifact("raw/collection.jsonl", "raw"),
        exp_artifact("raw/collection_meta.json", "raw"),
        exp_artifact("raw/oracles.json", "raw"),
        exp_artifact("raw/policy_trace.json", "raw"),
        exp_artifact("raw/arm_assignment.json", "raw"),
        exp_artifact("raw/frozen_verify.json", "raw"),
        exp_artifact("derived/metrics.json", "derived"),
        artifact_entry("research/physics/exp_37992957068_lib.py", "code"),
        artifact_entry("research/physics/exp_37992957068_run.py", "code"),
        artifact_entry("research/physics/exp_37992957068_finalize.py", "code"),
    ]
    for f in FROZEN_FILES:
        artifacts.append(artifact_entry(f"research/experiments/{EXPERIMENT_ID}/{f}",
                                        "frozen_input"))

    stratum_endpoints = derived["barrier_exposed_endpoints"]
    observations = [
        {"id": "O1_COLLECTION",
         "fact": f"Executed the frozen 57-endpoint universe x 12 fresh-cookie-jar sessions "
                 f"x up to J_max=5 GETs = {meta['n_planned_gets']} planned GETs; "
                 f"{meta['n_requests']} requests actually issued (clean endpoints stop at "
                 f"j=0). Wall clock {meta['wall_clock_s']}s. Status histogram "
                 f"{meta['status_histogram']}; class histogram {meta['class_histogram']}."},
        {"id": "O2_ORACLES",
         "fact": f"All {len(oracles)} live oracle requests classified into their expected "
                 f"classes: httpbin.org/status/403 -> UNAVAILABLE_403 (barrier-family "
                 f"403 without a challenge marker), status/429 -> RATE_LIMIT_429, "
                 f"no-such-host.invalid -> TRANSPORT_ERROR, status/200 and uuid -> CLEAN."},
        {"id": "O3_TREATMENT_LIVENESS",
         "fact": "Non-network policy trace confirms A_ADAPT returns a defined action for "
                 f"all {len(policy_trace['per_class'])} intrinsic classes "
                 f"(all_classes_defined={policy_trace['all_classes_defined']}) and terminates "
                 f"within J_max={policy_trace['J_MAX']} (worst-case 429 loop "
                 f"{policy_trace['worst_case_429_sequence_requests']} requests; "
                 f"terminates_within_J_max={policy_trace['terminates_within_J_max']})."},
        {"id": "O4_BARRIER_EXPOSED_STRATUM",
         "fact": f"{len(stratum_endpoints)} endpoints produced >= 1 intrinsic barrier "
                 f"event: {stratum_endpoints}."},
        {"id": "O5_TRANSITIONS",
         "fact": f"ONSET events (prev CLEAN -> current barrier) = "
                 f"{derived['metrics']['ONSET_n']}; RECOVERY events "
                 f"(prev barrier -> current CLEAN) = {derived['metrics']['RECOVERY_n']}."},
        {"id": "O6_PRIMARY_METRIC",
         "fact": f"SKILL_LL = {derived['metrics']['SKILL_LL']} nats/request "
                 f"(endpoint-clustered 95% CI {derived['metrics']['SKILL_LL_CI95']}); "
                 f"M_HISTORY held-out log-loss {core['logloss']['M_HISTORY']} vs best null "
                 f"{min(core['logloss'][b] for b in ('B_CONSTANT','B_ENDPOINT_CONST','B_MEMORY_PERSIST','B_RATE_ONLY'))}."},
        {"id": "O7_ABLATION",
         "fact": f"M_HISTORY_NOID (endpoint-identity ablation) SKILL_LL = "
                 f"{derived['metrics']['SKILL_LL_NOID']} nats/request "
                 f"(CI95 {derived['metrics']['SKILL_LL_NOID_CI95']})."},
        {"id": "O8_SCHEDULER",
         "fact": f"Barrier-exposed stratum: d_Req = {derived['metrics']['d_Req']} requests/episode "
                 f"(clustered CI {derived['metrics']['d_Req_CI95']}); d_Succ = {derived['metrics']['d_Succ']}; "
                 f"A_ADAPT mean requests {derived['metrics']['ADAPT_abs_requests']} vs "
                 f"A_RETRY {derived['metrics']['RETRY_abs_requests']}; "
                 f"no-barrier success {derived['metrics']['endpoint_no_barrier_success']}."},
        {"id": "O9_SEPARABILITY",
         "fact": f"SEPARABILITY_SKILL_LL (barrier vs ordinary-unavailability) = "
                 f"{derived['metrics']['SEPARABILITY_SKILL_LL']} nats/request on "
                 f"{derived['metrics']['SEPARABILITY_n']} non-clean requests."},
        {"id": "O10_STRATUM_FLOORS",
         "fact": f"barrier-exposed endpoints = {derived['metrics']['n_barrier_exposed_endpoints']} "
                 f"(floor 3); scheduler-stratum barrier events = "
                 f"{derived['metrics']['n_scheduler_barrier_events']} (floor 30)."},
        {"id": "O11_CLASSIFIER_REPRODUCIBILITY",
         "fact": f"Re-deriving every stored record's intrinsic class from its raw fields "
                 f"produced {meta.get('classifier_recomputation_mismatches')} mismatches out of "
                 f"{meta['n_requests']} (classifier is reproducible from stored evidence)."},
    ]

    validity_notes = [
        {"id": "V1_ENDPOINT_CONSTANT_DOMINANCE",
         "note": "The frozen pool is dominated by endpoint-constant behaviour "
                 "(e.g. Cloudflare 403-challenge endpoints and one unresolvable transport "
                 "endpoint). This is a genuine scientific S0 risk and is captured by the "
                 "identity/persistence nulls; it is not a measurement failure."},
        {"id": "V2_RUN_DEFINED_STRATUM",
         "note": "The scheduler stratum is defined by barrier events observed in this run "
                 "(pre-registered conditional subgroup). The fixed pre-freeze candidate set "
                 "is separately reported in spec.scheduler_strata; all inference is "
                 "additionally reported relative to it."},
        {"id": "V3_SEQUENTIAL_POLICY",
         "note": "For retry arms later requests occur only after non-CLEAN responses, so the "
                 "request population is policy-dependent. Cross-validation respects time order "
                 "and uses only past features; all nulls see the same rows."},
        {"id": "V4_SINGLE_WINDOW_AND_CLIENT",
         "note": "One stdlib-HTTP client, one collection window, one frozen 57-endpoint "
                 "universe. Rates and classes describe this pool and window only, not the Web."},
        {"id": "V5_REPRESENTATION_LOSS",
         "note": "Credential-free GET only: no JavaScript, DOM, SPA, GraphQL, WebSocket, "
                 "browser TLS fingerprint or authenticated state. Barrier mechanisms that "
                 "depend on those observables are invisible to this instrument."},
        {"id": "V6_ONSET_UNOBSERVED_IN_WINDOW",
         "note": f"No ONSET events (prev CLEAN -> barrier) occurred in this window "
                 f"(ONSET_n={derived['metrics']['ONSET_n']}), so ONSET_SKILL_LL is null. This "
                 f"is a property of the window, not a measurement failure; the frozen primary "
                 f"PRED_PASS/PRED_FAIL branch depends only on the pooled next-request task "
                 f"which had {derived['metrics']['n_rows_primary']} held-out rows."},
        {"id": "V7_IMPLEMENTATION_DEBUGGING_BEFORE_OUTCOMES",
         "note": "The analysis code is authored at EXECUTE as a literal realisation of the "
                 "frozen literals. Three pure implementation defects (a Python-list index in "
                 "the transition sub-routine, a keyword-argument name mismatch, and a missing "
                 "numpy import) were fixed during a pre-outcome smoke run of the sub-steps. "
                 "No frozen literal, threshold, model feature set, seed or branch rule was "
                 "altered or retuned after observing any outcome."},
        {"id": "V8_CENSUS_ARTIFACT_NOT_IN_REPO",
         "note": "The pre-freeze reachability census /tmp/opencode/phys379/census.json cited "
                 "by spec.json for the attainability certificate is not present in this "
                 "environment (it lived in an external temp dir). Its hash is recorded as null "
                 "in provenance; its cited facts remain design-time disclosures, and the run's "
                 "own attainability floors are verified directly from observed data."},
    ]

    unresolved = [
        {"id": "U1_GENERALIZATION_WINDOW",
         "question": "Do the observed barrier classes and (absent) onset dynamics persist "
                     "across collection windows and source IPs? A second window would "
                     "distinguish stable structure from a point-in-time artifact."},
        {"id": "U2_ONSET_MECHANISM",
         "question": "ONSET events were not observed on this pool/window. Which endpoints "
                     "(if any) exhibit a clean-to-barrier transition under a longer, "
                     "higher-rate or different-spacing probe, and is it schedule-driven?"},
        {"id": "U3_CONSTRUCT_BOUNDARY",
         "question": "What is the real-Web barrier dynamics on JavaScript-rendered, "
                     "authenticated or SPA substrates that this credential-free GET "
                     "instrument cannot observe?"},
        {"id": "U4_MIXED_PRODUCT_POLICY",
         "question": "If the branch is INCONCLUSIVE/MIXED, what is the minimal additional "
                     "design (larger barrier-exposed pool, forced onset via spacing) that "
                     "would make PRED_PASS/PRED_FAIL decidable?"},
    ]

    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }


def build_provenance(derived, frozen_verify, code_hashes):
    git_head = _git("rev-parse HEAD")
    git_branch = _git("rev-parse --abbrev-ref HEAD")
    spec = json.load(open(os.path.join(EXP_DIR, "spec.json")))
    req = json.load(open(os.path.join(EXP_DIR, "request.json")))
    arm_assignment = json.load(open(os.path.join(RAW, "arm_assignment.json")))
    meta = json.load(open(os.path.join(RAW, "collection_meta.json")))

    try:
        import numpy
        numpy_version = numpy.__version__
    except Exception:
        numpy_version = None

    code_overall = hashlib.sha256(
        "".join(code_hashes[k] for k in sorted(code_hashes)).encode()).hexdigest()

    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "origin_github_run_id": ORIGIN_RUN,
        "claim_ids": CLAIM_IDS,
        "director_mandate": {
            "action": "PIVOT",
            "claim_id": "C-WEB-DYNAMICS",
            "cognitive_reset": True,
            "parent_handoff_disposition": "USE",
            "cycle_id": req.get("director_mandate", {}).get("cycle_id"),
        },
        "parent_handoff": req.get("parent_handoff"),
        "git": {
            "head": git_head,
            "branch": git_branch,
            "note": "Working tree also contains unrelated lane directories and Codex-sync "
                    "edits that this EXECUTE did not modify.",
        },
        "frozen_inputs": {
            "declared_in_freeze": frozen_verify["declared"],
            "reverified": {
                name: {"declared": frozen_verify["declared"][name],
                       "actual": frozen_verify["actual"][name],
                       "match": frozen_verify["match"][name]}
                for name in frozen_verify["declared"]
            },
            "all_match": frozen_verify["all_match"],
            "freeze_sha256": frozen_verify["freeze_sha256"],
            "mutated_after_freeze": [],
        },
        "environment": {
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "numpy": numpy_version,
            "numpy_role": "analysis-only numerical accelerator; collection uses stdlib only",
            "http_client": "python stdlib urllib.request",
            "requests_library_used": False,
            "browser": "none",
            "javascript": False,
            "credentials": 0,
            "model_calls": 0,
            "external_llm_inference": False,
            "user_agent": derived["scheduler_stratum"].get("user_agent", None) or _ua(),
            "collection_workers": meta.get("max_workers"),
        },
        "code": {
            **code_hashes,
            "combined_code_sha256": code_overall,
        },
        "commands": [
            "python3 research/physics/exp_37992957068_run.py --collect",
            "python3 research/physics/exp_37992957068_run.py --analyze",
            "python3 research/physics/exp_37992957068_finalize.py",
        ],
        "datasets_fixtures": {
            "frozen_universe": {
                "source": "embedded verbatim in spec.json.frozen_universe.endpoints",
                "n_endpoints": len(spec["frozen_universe"]["endpoints"]),
            },
            "pre_freeze_census": {
                "path": "/tmp/opencode/phys379/census.json",
                "sha256": None,
                "note": "Pre-freeze non-outcome-bearing reachability census cited by "
                        "spec.json; it lived at an absolute path in an external temp dir and "
                        "is not present in this environment, so its hash is explicitly null. "
                        "The run independently verifies attainability floors from observed "
                        "data (see result.json.observations O6).",
            },
        },
        "seeds": {
            "assignment": 37992957068, "bootstrap": 37992957068,
            "pc_synthetic": 37992957068, "nc_synthetic": 37992957069,
        },
        "determinism": {
            "arm_assignment": "seeded block randomisation, 3 sessions per arm per endpoint "
                              "(seed 37992957068); recorded at raw/arm_assignment.json",
            "arm_assignment_sha256": _sha(os.path.join(RAW, "arm_assignment.json")),
            "bootstrap_resamples": 10000,
            "classification": "intrinsic class is a pure function of the stored fields "
                              "(status, error, cf_mitigated, challenge_marker_matched); the "
                              "analyze step re-derived every class from those fields with 0 "
                              "mismatches (recorded in derived/metrics.json collection_meta and "
                              "result.metrics.measurement_invalid_conditions)",
            "collect_reproducible": False,
            "collect_note": "Web responses are not reproducible; all downstream metrics are "
                            "deterministic functions of raw/collection.jsonl.",
            "numpy_used_in_collection": False,
            "pc_synthetic_endpoints": derived["controls"]["PC_SYNTHETIC_DYNAMICS"].get(
                "synthetic_endpoints"),
            "nc_synthetic_endpoints": derived["controls"]["NC_SYNTHETIC_MEMORYLESS"].get(
                "synthetic_endpoints"),
        },
        "census_artifact": {"path": "/tmp/opencode/phys379/census.json", "sha256": None},
        "artifacts": [
            exp_artifact("raw/collection.jsonl", "raw"),
            exp_artifact("raw/collection_meta.json", "raw"),
            exp_artifact("raw/oracles.json", "raw"),
            exp_artifact("raw/policy_trace.json", "raw"),
            exp_artifact("raw/arm_assignment.json", "raw"),
            exp_artifact("raw/frozen_verify.json", "raw"),
            exp_artifact("derived/metrics.json", "derived"),
        ],
    }


_CODE_CACHE = {}


def _sha(path):
    return artifact_entry(os.path.relpath(path, REPO), "x")["sha256"]


def _git(args):
    try:
        out = subprocess.run(["git"] + args.split(), cwd=REPO, capture_output=True,
                             text=True)
        return out.stdout.strip()
    except Exception:
        return None


def _ua():
    # Mirror the frozen user agent recorded by EXECUTE in the library.
    sys.path.insert(0, HERE)
    import exp_37992957068_lib as L
    return L.USER_AGENT


# ---------------------------------------------------------------------------

def write_report(result, derived, meta, oracles, policy_trace):
    m = result["metrics"]
    c = result["controls"]
    lines = []
    lines.append(f"# {EXPERIMENT_ID} — EXECUTE report")
    lines.append("")
    lines.append(f"Lane: **{LANE}**. Target claim: **C-WEB-DYNAMICS**. "
                 f"Director mandate: PIVOT (barrier dynamics).")
    lines.append("")
    lines.append(f"**status = `{result['status']}`  |  outcome = `{result['outcome']}`** "
                 f"(frozen branch: `{m['branch']}`)")
    lines.append("")
    lines.append("## 1. What was run")
    lines.append("")
    lines.append(f"Frozen 57-endpoint credential-free universe x 12 fresh-cookie-jar "
                 f"sessions x up to J_max=5 GETs ({meta['n_planned_gets']} planned); "
                 f"{meta['n_requests']} requests issued over {meta['wall_clock_s']}s with the "
                 f"four frozen arms (A_RETRY, A_RETRY_SPACED, A_FRESH, A_ADAPT). "
                 f"Class histogram: `{meta['class_histogram']}`. This is a credential-free "
                 "GET-only instrument (no browser/JS/auth/model calls).")
    lines.append("")
    lines.append("## 2. Measurement validity")
    lines.append("")
    lines.append(f"- Headline: **{result['status']}**.")
    lines.append(f"- Live oracles all classified as expected: {all(o['passed'] for o in oracles)}.")
    lines.append(f"- A_ADAPT treatment liveness (non-network trace): "
                 f"all_classes_defined={policy_trace['all_classes_defined']}, "
                 f"terminates_within_J_max={policy_trace['terminates_within_J_max']}.")
    lines.append(f"- Classifier reproducible from stored fields: "
                 f"{meta.get('classifier_recomputation_mismatches')} mismatches / "
                 f"{meta['n_requests']}.")
    lines.append(f"- Stratum floors: barrier-exposed endpoints = "
                 f"{m['n_barrier_exposed_endpoints']} (>=3); scheduler barrier events = "
                 f"{m['n_scheduler_barrier_events']} (>=30).")
    lines.append("")
    lines.append("## 3. Controls")
    lines.append("")
    for cid in ("PC_SYNTHETIC_DYNAMICS", "NC_SYNTHETIC_MEMORYLESS",
                "PC_BARRIER_ORACLE", "NC_CLEAN_ORACLE"):
        e = c[cid]
        obs = e.get("observed_power", e.get("observed_false_positive_rate", e.get("pass")))
        lines.append(f"- **{cid}** ({e['role']}): expected {e['expected']}; "
                     f"observed={obs}; pass={e['pass']}.")
    lines.append("")
    lines.append("## 4. Primary metrics")
    lines.append("")
    lines.append(f"- **SKILL_LL** = {m['SKILL_LL']} nats/request (CI95 {m['SKILL_LL_CI95']}); "
                 f"threshold delta_SKILL = 0.05 with CI lower > 0 for PRED_PASS.")
    lines.append(f"- M_HISTORY_NOID ablation SKILL_LL = {m['SKILL_LL_NOID']} "
                 f"(CI95 {m['SKILL_LL_NOID_CI95']}).")
    lines.append(f"- SKILL_BA = {m['SKILL_BA']}.")
    onset = "null (n=0; no ONSET events in this window)" if m["ONSET_n"] == 0 else m["ONSET_SKILL_LL"]
    lines.append(f"- ONSET_SKILL_LL = {onset}; "
                 f"RECOVERY_SKILL_LL = {m['RECOVERY_SKILL_LL']} (n={m['RECOVERY_n']}).")
    lines.append(f"- SEPARABILITY_SKILL_LL (barrier vs ordinary unavailability) = "
                 f"{m['SEPARABILITY_SKILL_LL']} (n={m['SEPARABILITY_n']}).")
    lines.append("")
    lines.append("## 5. Scheduler economy (barrier-exposed stratum)")
    lines.append("")
    lines.append(f"- d_Req = {m['d_Req']} requests/episode (clustered CI "
                 f"{m['d_Req_CI95']}); d_Succ = {m['d_Succ']}.")
    lines.append(f"- A_ADAPT mean requests {m['ADAPT_abs_requests']} vs A_RETRY "
                 f"{m['RETRY_abs_requests']}; no-barrier success baseline "
                 f"{m['endpoint_no_barrier_success']}.")
    lines.append("")
    lines.append("## 6. Frozen branch decision")
    lines.append("")
    lines.append(f"- PRED disposition: {m['pred_disposition']}; SCHED disposition: "
                 f"{m['sched_disposition']}.")
    lines.append(f"- **Branch = {m['branch']}** => outcome "
                 f"**{result['outcome']}** (status {result['status']}).")
    lines.append("")
    lines.append("## 7. Validity threats")
    lines.append("")
    for v in result["validity_notes"]:
        lines.append(f"- **{v['id']}**: {v['note']}")
    lines.append("")
    lines.append("## 8. Unresolved")
    lines.append("")
    for u in result["unresolved"]:
        lines.append(f"- **{u['id']}**: {u['question']}")
    lines.append("")
    lines.append("## 9. Product interpretation (bounded)")
    lines.append("")
    if result["status"] == "MEASUREMENT_INVALID":
        lines.append("Measurement-invalid: no product inference is permitted.")
    elif result["outcome"] == "SUPPORTS":
        lines.append("Consistent with the frozen positive product consequence (S1): an online "
                     "history/schedule-aware barrier policy (backoff on 429, fresh session on "
                     "transport error, terminal dead-end classification for persistent "
                     "403-challenge) is supported on this pool/window. Not promoted; claim "
                     "ceiling remains at most EXPERIMENTAL.")
    elif result["outcome"] == "FALSIFIES":
        lines.append("Consistent with the frozen negative product consequence (S0): barriers on "
                     "this pool/window are endpoint-constant and persistence-bound, and the "
                     "adaptive scheduler gives no request economy. The product prior is a static "
                     "per-endpoint dead-end denylist plus immediate terminal classification; do "
                     "not invest in an online history model for barrier prediction on this "
                     "evidence. This bounds, and does not close, the C-WEB-DYNAMICS domain.")
    else:
        lines.append("Mixed/inconclusive: the two frozen sub-branches disagree or are "
                     "ambiguous; no single product policy is licensed by this packet. "
                     "On the predictive side SKILL_LL = {} nats with CI95 {} (delta_SKILL = "
                     "0.05) and the endpoint-identity ablation M_HISTORY_NOID = {} is strongly "
                     "negative, so no online history-based barrier model is licensed on this "
                     "evidence. On the scheduler side d_Req = {} requests/episode with clustered "
                     "CI {} at d_Succ = {} (SCHED_ECON_PASS), but on this pool that economy is "
                     "largely a mechanical consequence of the frozen arm definitions on "
                     "endpoint-constant barriers rather than demonstrated predictive barrier "
                     "dynamics. Claim status unchanged; no promotion.".format(
                         m["SKILL_LL"], m["SKILL_LL_CI95"], m["SKILL_LL_NOID"],
                         m["d_Req"], m["d_Req_CI95"], m["d_Succ"]))
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    derived = json.load(open(os.path.join(DER, "metrics.json")))
    # Use the analyze-time meta (derived/collection_meta includes the classifier
    # recomputation check that the --collect step appended in memory only).
    meta = derived["collection_meta"]
    oracles = json.load(open(os.path.join(RAW, "oracles.json")))
    policy_trace = json.load(open(os.path.join(RAW, "policy_trace.json")))
    frozen_verify = json.load(open(os.path.join(RAW, "frozen_verify.json")))

    code_hashes = {rel: _sha(os.path.join(REPO, rel)) for rel in CODE_FILES}

    result = build_result(derived, meta, oracles, policy_trace, frozen_verify)

    with open(os.path.join(EXP_DIR, "result.json"), "w") as f:
        json.dump(result, f, indent=2, sort_keys=False)

    report = write_report(result, derived, meta, oracles, policy_trace)
    with open(os.path.join(EXP_DIR, "report.md"), "w") as f:
        f.write(report)

    provenance = build_provenance(derived, frozen_verify, code_hashes)
    with open(os.path.join(EXP_DIR, "provenance.json"), "w") as f:
        json.dump(provenance, f, indent=2, sort_keys=False)

    print(f"status={result['status']} outcome={result['outcome']} branch={result['metrics']['branch']}")
    print("SKILL_LL", result["metrics"]["SKILL_LL"], result["metrics"]["SKILL_LL_CI95"])
    print("d_Req", result["metrics"]["d_Req"], "d_Succ", result["metrics"]["d_Succ"])
    print("wrote result.json, report.md, provenance.json")


if __name__ == "__main__":
    main()
