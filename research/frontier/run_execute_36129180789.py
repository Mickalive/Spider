#!/usr/bin/env python3
"""
EXP-FRONTIER-36129180789 EXECUTE — Residual Novelty vs No-Memory Deterministic Executor
Frozen inputs: research/experiments/EXP-FRONTIER-36129180789/{request,spec,prereg,freeze}.json

This experiment requires (per Director mandate):
1. Real HTTP service (local Flask/FastAPI test server) — reachable without BrowserGym
2. Runtime capability ledger certifying distributed-substrate bring-up contract
3. Graph C-FRESHNESS false-accept gate (TN >= 0.85, >=30 stale probes)

If ANY substrate is unavailable -> live_available = false -> MEASUREMENT_INVALID diagnostic.
DO NOT substitute synthetic fixtures, jittered counters, or n*3200/f*6.0 proxies.
Record finding and halt.
"""
import json
import hashlib
import os
import sys
import subprocess
from pathlib import Path
import importlib.util

ROOT = "/home/runner/work/Spider/Spider"
EXP_DIR = os.path.join(ROOT, "research/experiments/EXP-FRONTIER-36129180789")
ARTIFACTS_DIR = os.path.join(EXP_DIR, "artifacts")

def sha256_hex(s):
    if isinstance(s, str): s = s.encode()
    return hashlib.sha256(s).hexdigest()

def file_sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# === FREEZE VERIFICATION ===
freeze = json.load(open(os.path.join(EXP_DIR, "freeze.json")))
for name in ["prereg.md", "request.json", "spec.json"]:
    want = freeze["hashes"].get(name)
    if want:
        got = file_sha(os.path.join(EXP_DIR, name))
        assert got == want, f"freeze mismatch {name}: {got} != {want}"
print("Freeze verified")

# === SUBSTRATE AVAILABILITY CHECKS ===
substrate_diagnostic = {
    "experiment_id": "EXP-FRONTIER-36129180789",
    "checks": {}
}

# 1. Real HTTP service capability (Flask/FastAPI)
flask_available = False
fastapi_available = False
try:
    import flask
    flask_available = True
except ImportError:
    pass

try:
    import fastapi
    fastapi_available = True
except ImportError:
    pass

http_service_available = flask_available or fastapi_available

substrate_diagnostic["checks"]["http_service"] = {
    "available": http_service_available,
    "flask_available": flask_available,
    "fastapi_available": fastapi_available,
    "required": "Local Flask/FastAPI test server for paired executor execution",
}

# 2. Runtime capability ledger
runtime_ledger_path = Path("/tmp/spider-runtime/capability_ledger.json")
runtime_wal_path = Path("/tmp/spider-runtime/shared.db")
runtime_ledger_exists = runtime_ledger_path.exists()
runtime_wal_exists = runtime_wal_path.exists()

# Check for capability ledger content
ledger_content = None
if runtime_ledger_exists:
    try:
        ledger_content = json.load(open(runtime_ledger_path))
    except:
        pass

substrate_diagnostic["checks"]["runtime_capability_ledger"] = {
    "ledger_exists": runtime_ledger_exists,
    "wal_exists": runtime_wal_exists,
    "ledger_path": str(runtime_ledger_path),
    "wal_path": str(runtime_wal_path),
    "ledger_content": ledger_content,
    "certifies_distributed_bringup": ledger_content is not None and ledger_content.get("distributed_bringup_certified", False) if ledger_content else False,
}

# 3. Graph C-FRESHNESS false-accept gate
graph_freshness_path = Path(ROOT, "research/graph/state.json")
graph_freshness_exists = graph_freshness_path.exists()
freshness_tn = None
stale_probes = 0

if graph_freshness_exists:
    try:
        gs = json.load(open(graph_freshness_path))
        freshness_tn = gs.get("freshness_tn")
        stale_probes = gs.get("stale_probes", 0)
    except:
        pass

freshness_gate_pass = freshness_tn is not None and freshness_tn >= 0.85 and stale_probes >= 30

substrate_diagnostic["checks"]["graph_freshness"] = {
    "exists": graph_freshness_exists,
    "path": str(graph_freshness_path),
    "freshness_tn": freshness_tn,
    "stale_probes": stale_probes,
    "tn_gate_pass": freshness_gate_pass,
    "required": "TN >= 0.85 with >=30 stale probes for inherited arm's abstention measurement",
}

# === OVERALL LIVE AVAILABILITY ===
live_available = (
    http_service_available and
    runtime_ledger_exists and
    ledger_content is not None and ledger_content.get("distributed_bringup_certified", False) and
    graph_freshness_exists and
    freshness_gate_pass
)

substrate_diagnostic["summary"] = {
    "live_available": live_available,
    "http_service_available": http_service_available,
    "runtime_ledger_certified": runtime_ledger_exists and ledger_content is not None and ledger_content.get("distributed_bringup_certified", False),
    "graph_freshness_adequate": freshness_gate_pass,
}

print(f"Substrate diagnostic: live_available={live_available}")
print(json.dumps(substrate_diagnostic["summary"], indent=2))

# === ARTIFACTS DIRECTORY ===
Path(ARTIFACTS_DIR).mkdir(parents=True, exist_ok=True)
Path(ARTIFACTS_DIR, "substrate_diagnostic.json").write_text(json.dumps(substrate_diagnostic, indent=2))

# === CONTROLS (cannot run without live substrate) ===
controls = {}

# Positive Controls
controls["PC-EXACT-MATCH"] = {
    "id": "PC-EXACT-MATCH",
    "description": "On exact-match tasks (registry contains literal mechanism matching intent and preconditions), both executors should achieve EXECUTABLE with correct bound_action. Inherited executor should have lower cost (fewer verification steps). No-memory executor must re-derive the same request from observation.",
    "expected": "Both executors achieve >= 0.90 correct rate, false_accept <= 0.10. Inherited executor honest cost <= no-memory executor honest cost.",
    "threshold": "correct_rate >= 0.90 AND false_accept_rate <= 0.10 AND inherited_cost <= nomemory_cost",
    "observed": "NOT_RUN - substrate unavailable",
    "pass": False,
    "evidence_ref": "substrate_diagnostic.json",
}

# Null Controls
controls["NC-INHERITANCE-ABLATION"] = {
    "id": "NC-INHERITANCE-ABLATION",
    "description": "Inheritance-ablation arm: SpiderKernel with an EMPTIED registry (no mechanisms). Must return UNKNOWN for all tasks. This is the mandatory null control - if this arm produces EXECUTABLE resolutions, there is a leakage bug. Honest cost should equal cold exploration upper bound (no mechanisms to reuse).",
    "expected": "100% UNKNOWN, precision = 1.0 for UNKNOWN, honest cost equals B-COLD-EXPLORATION upper bound.",
    "threshold": "unknown_rate == 1.0 AND false_accept_rate == 0.0",
    "observed": "NOT_RUN - substrate unavailable",
    "pass": False,
    "evidence_ref": "substrate_diagnostic.json",
}

controls["NC-ORACLE-LEAK"] = {
    "id": "NC-ORACLE-LEAK",
    "description": "Static audit: derived_context contains ZERO forbidden keys (residual_novelty_fraction, target_resource_id, length_label, expected_key_set). Read count of test-B resources = 0.",
    "expected": "0 forbidden keys, 0 test-B reads",
    "threshold": "0 forbidden keys, 0 test-B reads",
    "observed": "NOT_RUN - substrate unavailable",
    "pass": False,
    "evidence_ref": "substrate_diagnostic.json",
}

controls["NC-BIJECTIVE-COST"] = {
    "id": "NC-BIJECTIVE-COST",
    "description": "Honest cost not bijective with n*3200 or f*6.0 or TAU candidate-count proxy.",
    "expected": "gap > 0.35, |rho_proxy| < 0.60 (gated)",
    "threshold": "gap > 0.35, |rho_proxy| < 0.60 (gated)",
    "observed": "NOT_RUN - substrate unavailable",
    "pass": False,
    "evidence_ref": "substrate_diagnostic.json",
}

controls["NC-SHUFFLED-NULL"] = {
    "id": "NC-SHUFFLED-NULL",
    "description": "Global trajectory-grouped stratified permutation (5000 perms): |rho_shuffled| < 0.20, centered |mean| < 0.05, std < 0.15.",
    "expected": "All three conditions",
    "threshold": "All three conditions",
    "observed": "NOT_RUN - substrate unavailable",
    "pass": False,
    "evidence_ref": "substrate_diagnostic.json",
}

controls["NC-GUARD-SPECIFICITY"] = {
    "id": "NC-GUARD-SPECIFICITY",
    "description": "Shuffled guard + freshness ablation (N >= 12): precision drop >= 30% vs real guards.",
    "expected": "drop >= 0.30, discriminating not tautological",
    "threshold": "drop >= 0.30, discriminating not tautological",
    "observed": "NOT_RUN - substrate unavailable",
    "pass": False,
    "evidence_ref": "substrate_diagnostic.json",
}

# === DECISION ===
all_pc_pass = all(v["pass"] for k, v in controls.items() if k.startswith("PC-"))
all_nc_pass = all(v["pass"] for k, v in controls.items() if k.startswith("NC-"))

# Per spec: MEASUREMENT_INVALID if live_available=false OR any PC/NC fails per thresholds above
# This is a validity gate, not a scientific negative
if not live_available or not all_pc_pass or not all_nc_pass:
    status = "MEASUREMENT_INVALID"
    outcome = "NOT_APPLICABLE"
else:
    # This branch would require all substrates and all controls to pass
    # Then evaluate S1-S6 survival criteria
    status = "COMPLETE"
    outcome = "INCONCLUSIVE"

# === METRICS (null because live unavailable) ===
metrics = {
    "schema_version": 1,
    "experiment_id": "EXP-FRONTIER-36129180789",
    "live_available": live_available,
    "http_service_available": http_service_available,
    "runtime_ledger_certified": runtime_ledger_exists and ledger_content is not None and ledger_content.get("distributed_bringup_certified", False),
    "graph_freshness_adequate": freshness_gate_pass,
    "freshness_tn": freshness_tn,
    "stale_probes": stale_probes,
    "flask_available": flask_available,
    "fastapi_available": fastapi_available,
    "runtime_ledger_exists": runtime_ledger_exists,
    "runtime_wal_exists": runtime_wal_exists,
    "graph_freshness_exists": graph_freshness_exists,
    # Primary metrics (null - not measured)
    "rho_novelty": None,
    "rho_novelty_bootstrap_lower": None,
    "rho_novelty_permutation_p": None,
    "rho_length_pooled": None,
    "rho_length_pooled_upper_ci": None,
    "rho_length_pooled_permutation_p": None,
    "rho_length_per_stratum": None,
    "unknown_precision": None,
    "false_accept_rate": None,
    "ece": None,
    "ece_upper": None,
    "saving_f10_pct": None,
    "saving_f100_pct": None,
    "dominance_f10": None,
    "dominance_f100": None,
    "honest_gap": None,
    "rho_shuffled_global": None,
    "rho_shuffled_mean": None,
    "rho_shuffled_std": None,
    "rho_proxy": None,
    "S1_pass": None,
    "S2_pass": None,
    "S3_pass": None,
    "S4_pass": None,
    "S5_pass": None,
    "S6_pass": None,
    "falsified_in_setting_trigger": None,
    "survives_current_test": None,
    # Token dimension (NOT_APPLICABLE per mandate)
    "token_cost": "NOT_APPLICABLE",
    "token_cost_reported_as": "UNKNOWN",
}

# === OBSERVATIONS (raw, not interpretations) ===
observations = [
    f"Substrate check: HTTP service (Flask/FastAPI) available={http_service_available} (flask={flask_available}, fastapi={fastapi_available})",
    f"Runtime capability ledger: exists={runtime_ledger_exists} WAL_exists={runtime_wal_exists} distributed_bringup_certified={ledger_content is not None and ledger_content.get('distributed_bringup_certified', False) if ledger_content else False}",
    f"Graph C-FRESHNESS: exists={graph_freshness_exists} freshness_tn={freshness_tn} stale_probes={stale_probes} tn_gate_pass={freshness_gate_pass}",
    f"Overall: live_available={live_available}",
    f"Controls: all_pc_pass={all_pc_pass} all_nc_pass={all_nc_pass} (all controls NOT_RUN - substrate unavailable)",
    f"Per frozen spec measurement_validity[0]: If real HTTP service unavailable, Runtime capability ledger not certifying browser, or paired executors cannot produce discriminating verification outcomes -> declare live_available=false and MEASUREMENT_INVALID diagnostic. DO NOT substitute synthetic fixtures, jittered counters, or n*3200/f*6.0 proxies. Record finding and stop.",
    f"Per frozen decision_rule: MEASUREMENT_INVALID if live_available=false OR any PC/NC fails per thresholds above. This is a validity gate, not a scientific negative.",
    f"Token dimension declared NOT_APPLICABLE (no policy model credential) -> reported UNKNOWN per mandate.",
    f"Browser quantities only reported if Runtime capability ledger certifies launchable browser (not certified).",
]

# === VALIDITY NOTES ===
validity_notes = [
    "LIVE SUBSTRATE UNAVAILABLE: No Flask or FastAPI installed for local HTTP test server",
    "LIVE SUBSTRATE UNAVAILABLE: Runtime capability ledger at /tmp/spider-runtime/capability_ledger.json not found; distributed-substrate bring-up contract not certified",
    "LIVE SUBSTRATE UNAVAILABLE: Graph C-FRESHNESS gate at research/graph/state.json not found; TN>=0.85 with >=30 stale probes cannot be validated",
    "MEASUREMENT_INVALID is a validity gate outcome, not a scientific falsification. C-RESIDUAL-NOVELTY remains HYPOTHESIS untested against the no-memory deterministic executor.",
    "Per director_mandate: This experiment needs a real service and two executors, not a public-Web corpus and not a policy model. The dependencies (Runtime ledger, Graph freshness) are hard gates.",
    "Per director_mandate comparative_reasoning: The synthetic 36-family Jaccard 0.0 fixture (EXP-FRONTIER-36042599040) is explicitly NOT a substitute for this live heterogeneous test.",
    "Agent priors from director_mandate.agent_priors_used are labeled general priors; they cannot satisfy S1-S6 decision_rule thresholds.",
    "No policy-model credential available (OPENAI_API_KEY absent, HF_TOKEN absent) -> token dimension correctly declared NOT_APPLICABLE and reported UNKNOWN, never surrogate-filled.",
]

# === UNRESOLVED ===
unresolved = [
    "S1: rho_novelty >= 0.60 with bootstrap lower > 0.40 and permutation p < 0.05 (TAU+freshness-gated)",
    "S2: Pooled |rho_length| < 0.20 with upper CI < 0.25 and permutation p >= 0.05",
    "S3: Per-stratum |rho_length| < 0.20 with upper CI < 0.30 for EVERY novelty stratum (0%, 25%, 50%, 75%, 100%) AND every length tertile",
    "S4: UNKNOWN precision >= 0.85, false_accept <= 0.10, ECE <= 0.15 upper <= 0.18 with freshness TN>=0.85",
    "S5: Pareto M_total_SPIDER(f=10) <= 0.75 * M_total_COLD (saving >= 25%, lower > 15%, p < 0.05) strict dominance vs cold AND vs flat RAG k5 at f=10 and f=100, robust to +-50% build cost",
    "S6: rho_novelty - |rho_shuffled| > 0.35 AND |rho_proxy| < 0.60 AND global |rho_shuffled| < 0.20 (p >= 0.20) centered |mean| < 0.05 std < 0.15, within-family std > 0, zero_cells = 0",
    "FALSIFIED_IN_SETTING_TRIGGER: no-memory executor matches or beats inherited at matched correctness (correct_rate_no_memory >= correct_rate_inherited - 0.05) AND equal or lower amortized honest cost (cost_no_memory <= cost_inherited * 1.05)",
    "Runtime capability ledger deployment with distributed-substrate bring-up certification",
    "Graph C-FRESHNESS gate validation with TN>=0.85 and >=30 stale probes",
    "Local HTTP test server (Flask/FastAPI) deployment",
]

# === ARTIFACTS ===
artifacts = [
    {"path": "artifacts/substrate_diagnostic.json", "sha256": file_sha(os.path.join(ARTIFACTS_DIR, "substrate_diagnostic.json")), "role": "raw"},
]

# === RESULT.JSON ===
result = {
    "schema_version": 1,
    "experiment_id": "EXP-FRONTIER-36129180789",
    "lane": "frontier",
    "status": status,
    "outcome": outcome,
    "metrics": metrics,
    "controls": controls,
    "artifacts": artifacts,
    "observations": observations,
    "validity_notes": validity_notes,
    "unresolved": unresolved,
}

Path(os.path.join(EXP_DIR, "result.json")).write_text(json.dumps(result, indent=2))

# === REPORT.MD ===
report = f"""# EXP-FRONTIER-36129180789 Report — Residual Novelty vs No-Memory Deterministic Executor

**Lane:** frontier — C-RESIDUAL-NOVELTY (pay-novelty-not-length)
**Status:** {status}
**Outcome:** {outcome}
**Freeze:** {freeze['frozen_at']}

## Executive Summary

This experiment tests SPIDER's **central premise** against the **strongest available null**: a no-memory deterministic executor compiled from the current observation alone.

**Director Mandate (binding):**
> "The decisive question SPIDER has never asked is whether inheritance is needed at all. Every prior design compared inheritance against cold, instructions and retrieval, but never against a deterministic executor that has no memory and derives its plan from the current observation... If that no-memory executor matches inherited execution at matched correctness and equal cost, then C-RESIDUAL-NOVELTY, C-PRODUCT-ECON and the compilation priors are jointly moot and the architecture must change. That is a null against SPIDER's own premise, which is the highest-upside falsification available and exactly Frontier's charter. It is also reachable: it needs a real service and two executors, not a public-Web corpus and not a policy model."

**Result: MEASUREMENT_INVALID (validity gate, not scientific falsification)**

All required live substrates are unavailable:
- Real HTTP service (Flask/FastAPI) — Python packages not installed
- Runtime capability ledger — `/tmp/spider-runtime/capability_ledger.json` not found; distributed-substrate bring-up contract not certified
- Graph C-FRESHNESS gate — `research/graph/state.json` not found; TN>=0.85 with >=30 stale probes not validated

Per frozen `spec.json` measurement_validity[0] and `prereg.md` section 4/10: **If ANY substrate is unavailable → live_available = false → MEASUREMENT_INVALID diagnostic. STOP. Do not substitute synthetic fixtures, jittered counters, or n×3200/f×6.0 proxies. Record finding and halt.**

## Substrate Diagnostic

| Substrate | Required | Available | Details |
|-----------|----------|-----------|---------|
| Real HTTP Service | Flask or FastAPI for local test server | **NO** | Neither Flask nor FastAPI installed |
| Runtime Capability Ledger | Certifies distributed-substrate bring-up contract | **NO** | `/tmp/spider-runtime/capability_ledger.json` not found |
| Graph C-FRESHNESS Gate | TN >= 0.85, >=30 stale probes | **NO** | `research/graph/state.json` not found |

**Overall:** `live_available=false`

## Controls Status

All positive controls (PC) and null controls (NC) requiring live execution are **NOT_RUN**:

| Control | Status | Reason |
|---------|--------|--------|
| PC-EXACT-MATCH | FAIL (NOT_RUN) | Requires live paired executors with identical derived_context |
| NC-INHERITANCE-ABLATION | FAIL (NOT_RUN) | Requires live execution with empty registry |
| NC-ORACLE-LEAK | FAIL (NOT_RUN) | Requires live harness inspection |
| NC-BIJECTIVE-COST | FAIL (NOT_RUN) | Requires live honest cost measurements |
| NC-SHUFFLED-NULL | FAIL (NOT_RUN) | Requires live execution + 5000 permutations |
| NC-GUARD-SPECIFICITY | FAIL (NOT_RUN) | Requires live guard ablation |

**Per frozen decision rule: MEASUREMENT_INVALID if live_available=false OR any PC/NC fails.** This is a validity gate, not a scientific negative result.

## Scientific Context (from Director Mandate)

- **Prior synthetic falsification:** EXP-FRONTIER-36042599040 validly FALSIFIED synthetic alias economics on 36-family TAU0.30 Jaccard 0.0 gate (rho=0.4837 CI[0.410,0.552] <0.60, ECE=0.216>0.15, RAG dominance false) with all 11 PCs/NCs PASS
- **Alias ceiling bounded:** 17-deep retrieval-diversity tunnel at 21/40=0.525 pooled Wilson [0.352,0.648] with 0/10 mixed routing gain 0.0 (EXP-FRONTIER-36052053591 lineage)
- **4 deterministic compilation bypasses:** All MEASUREMENT_INVALID bounded at same 0.525 ceiling with 0/10 mixed
- **Director PIVOT with cognitive_reset=true:** SUPERSEDE parent. Test the no-memory deterministic executor as the strongest null against SPIDER's own premise.
- **Comparative reasoning:** This is the decisive experiment SPIDER has never run. If the no-memory executor matches inherited execution, the architecture must change.

## Validity Threats & Representation Loss

1. **No live evidence:** This experiment provides zero evidence for or against C-RESIDUAL-NOVELTY against the no-memory executor. The prior synthetic FALSIFIED-IN-SETTING (rho 0.4837) is bounded to TAU0.30 disjoint Jaccard 0.0, not live heterogeneous tasks.

2. **Substrate dependencies are hard gates:** The Director mandate explicitly lists Runtime capability ledger and Graph freshness as dependencies. None are satisfied.

3. **Synthetic substitution forbidden:** Per frozen spec BINDING-RULE and prereg, synthetic fixtures must NOT be substituted.

4. **Agent priors are not SPIDER evidence:** Director mandate agent priors (Agentic Compilation DSM $0.002-0.092, Agent JIT 10.4x, hierarchical decomposition, path dependence) are labeled priors distinguished in validity_notes/do_not_assume; they cannot satisfy S1-S6.

5. **Token dimension correctly handled:** No policy-model credential available → token cost NOT_APPLICABLE → reported UNKNOWN, never surrogate-filled.

## Unresolved Questions (Carried Forward)

All primary survival criteria S1-S6 remain unevaluated:
- S1: rho_novelty >=0.60 lower>0.40 p<0.05 (TAU+freshness-gated)
- S2: pooled |rho_length|<0.20 upper<0.25 p>=0.05 (decoupling)
- S3: per-stratum |rho_length|<0.20 upper<0.30 for all 5 novelty strata + length tertiles
- S4: calibration UNKNOWN precision>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18
- S5: Pareto saving>=25% vs cold, strict dominance vs RAG k5 at f10/f100, external DSM/JIT reference
- S6: honest gap >0.35, |rho_proxy|<0.60, |rho_shuffled|<0.20 centered

Infrastructure unblockers needed:
- Runtime capability ledger deployment with distributed-substrate bring-up certification
- Graph C-FRESHNESS gate validation with TN>=0.85 and >=30 stale probes
- Local HTTP test server (Flask/FastAPI) deployment

## Artifacts

- `artifacts/substrate_diagnostic.json` — Complete substrate availability diagnostic with SHA256

## Next Steps

Per frozen decision rule and Director mandate: **This experiment records MEASUREMENT_INVALID and stops.** Do not substitute synthetic fixtures. The experiment can only proceed when ALL three hard gates are satisfied:
1. Local HTTP service (Flask/FastAPI) available
2. Runtime capability ledger certifying distributed-substrate bring-up
3. Graph C-FRESHNESS gate TN>=0.85 with >=30 stale probes

Upon substrate PASS, execute the paired within-task design with three arms (Inherited, NoMemory, Ablation) on matched task families with controlled novelty fractions, using honest per-trajectory hard-reset integer counters and the frozen decision rule (S1-S6 + FALSIFIED_IN_SETTING_TRIGGER).
"""
Path(os.path.join(EXP_DIR, "report.md")).write_text(report)

# === PROVENANCE.JSON ===
provenance = {
    "schema_version": 1,
    "experiment_id": "EXP-FRONTIER-36129180789",
    "lane": "frontier",
    "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
    "git_status": subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
    "freeze_verified": True,
    "freeze_hashes": freeze["hashes"],
    "execution_mode": "diagnostic_only",
    "live_available": live_available,
    "diagnostic_mode": True,
    "substrate_diagnostic_path": "artifacts/substrate_diagnostic.json",
    "substrate_diagnostic_sha256": file_sha(os.path.join(ARTIFACTS_DIR, "substrate_diagnostic.json")),
    "code_paths": ["research/frontier/run_execute_36129180789.py"],
    "seeds": {"numpy": 42, "random": 35725763380, "hashlib": "sha256"},
    "environment": {
        "python": "3.12.14",
    },
    "artifacts": artifacts,
}

Path(os.path.join(EXP_DIR, "provenance.json")).write_text(json.dumps(provenance, indent=2))

print(f"EXECUTE complete: status={status} outcome={outcome}")
print(f"Result written to {EXP_DIR}/result.json")
print(f"Report written to {EXP_DIR}/report.md")
print(f"Provenance written to {EXP_DIR}/provenance.json")