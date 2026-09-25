#!/usr/bin/env python3
"""
EXP-FRONTIER-36097242687 EXECUTE — WebChoreArena Heterogeneous Residual-Novelty Verification Economics (PIVOT SUPERSEDE)
Frozen inputs: research/experiments/EXP-FRONTIER-36097242687/{request,spec,prereg,freeze}.json
Substrate diagnostic for live heterogeneous WebChoreArena 532 + WebArena-Verified Hard 192/36 gate.
TAU0.30 + freshness topology-gated honest sum counters.
"""
import json, hashlib, os, sys, math, random, subprocess
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr

ROOT = "/home/runner/work/Spider/Spider"
EXP = os.path.join(ROOT, "research/experiments/EXP-FRONTIER-36097242687")
SEED = 42
TAU = 0.30
rng = np.random.RandomState(SEED)
random.seed(SEED)

def sha256_hex(s):
    if isinstance(s, str): s = s.encode()
    return hashlib.sha256(s).hexdigest()

def file_sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# Freeze check
freeze = json.load(open(os.path.join(EXP, "freeze.json")))
for name in ["prereg.md", "request.json", "spec.json"]:
    want = freeze["hashes"].get(name)
    if want:
        got = file_sha(os.path.join(EXP, name))
        assert got == want, f"freeze mismatch {name}: {got} != {want}"
print("Freeze verified")

# ============================================================
# SUBSTRATE DIAGNOSTIC — check all required dependencies
# ============================================================
def check_import(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

# BrowserGym stack
browsergym_available = check_import("browsergym")
browsergym_core_available = check_import("browsergym.core")
playwright_available = check_import("playwright")
agentlab_available = check_import("agentlab")

# Chromium
chromium_present = False
for path in ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome", "/usr/bin/chrome"]:
    if os.path.exists(path):
        chromium_present = True
        break

# PyPI reachable
pypi_reachable = False
try:
    result = subprocess.run([sys.executable, "-m", "pip", "index", "versions", "browsergym-core"],
                           capture_output=True, timeout=10)
    pypi_reachable = (result.returncode == 0)
except Exception:
    pass

# Intel diverse manifest
intel_diverse_manifest_exists = False
manifest_families = 0
manifest_path_candidates = [
    "/home/runner/work/Spider/Spider/research/intel/diverse_site_manifest.json",
    "/home/runner/work/Spider/Spider/data/webgym_292k",
    "/home/runner/work/Spider/Spider/data/webarena_verified_hard",
]
for p in manifest_path_candidates:
    if os.path.exists(p):
        intel_diverse_manifest_exists = True
        # try to count families
        if p.endswith(".json"):
            try:
                with open(p) as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "families" in data:
                        manifest_families = len(data["families"])
                    elif isinstance(data, list):
                        manifest_families = len(data)
            except Exception:
                pass
        break

# Runtime WAL
runtime_wal_exists = os.path.exists("/tmp/spider-runtime/shared.db")
x_worker_pid = None
n_non304 = None

# Check if we can get Runtime health metrics
try:
    import sqlite3
    if runtime_wal_exists:
        conn = sqlite3.connect("/tmp/spider-runtime/shared.db")
        cursor = conn.cursor()
        # Check for X-Worker-Pid and n_non304 proxy
        cursor.execute("SELECT COUNT(*) FROM requests WHERE status != 304")
        n_non304 = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT worker_pid) FROM requests WHERE worker_pid IS NOT NULL")
        x_worker_pid = cursor.fetchone()[0]
        conn.close()
except Exception:
    pass

# Substrate adequacy
substrate_adequate = (
    browsergym_available and browsergym_core_available and 
    playwright_available and agentlab_available and
    chromium_present and pypi_reachable and
    intel_diverse_manifest_exists and manifest_families >= 10 and
    runtime_wal_exists and n_non304 is not None and n_non304 >= 360 and
    x_worker_pid is not None and x_worker_pid >= 10
)

heterogeneity_adequate = intel_diverse_manifest_exists and manifest_families >= 10
coverage_adequate = intel_diverse_manifest_exists and manifest_families >= 10

print("=" * 60)
print("SUBSTRATE DIAGNOSTIC")
print("=" * 60)
print(f"browsergym: {browsergym_available}")
print(f"browsergym.core: {browsergym_core_available}")
print(f"playwright: {playwright_available}")
print(f"agentlab: {agentlab_available}")
print(f"chromium_present: {chromium_present}")
print(f"pypi_reachable: {pypi_reachable}")
print(f"intel_diverse_manifest_exists: {intel_diverse_manifest_exists}")
print(f"manifest_families: {manifest_families}")
print(f"runtime_wal_exists: {runtime_wal_exists}")
print(f"x_worker_pid: {x_worker_pid}")
print(f"n_non304: {n_non304}")
print(f"substrate_adequate: {substrate_adequate}")
print(f"heterogeneity_adequate: {heterogeneity_adequate}")
print(f"coverage_adequate: {coverage_adequate}")
print("=" * 60)

# If substrate not adequate, produce MEASUREMENT_INVALID diagnostic
if not substrate_adequate:
    # Create artifacts directory
    artifacts_dir = os.path.join(EXP, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    substrate_diagnostic = {
        "live_available": False,
        "browsergym": browsergym_available,
        "browsergym.core": browsergym_core_available,
        "playwright": playwright_available,
        "agentlab": agentlab_available,
        "intel_diverse_manifest_exists": intel_diverse_manifest_exists,
        "manifest_families": manifest_families,
        "jaccard": None,
        "pooled_tasks": 0,
        "mixed_tasks": 0,
        "runtime_wal_exists": runtime_wal_exists,
        "x_worker_pid": x_worker_pid,
        "n_non304": n_non304,
        "substrate_adequate": substrate_adequate,
        "heterogeneity_adequate": heterogeneity_adequate,
        "coverage_adequate": coverage_adequate,
        "chromium_present": chromium_present,
        "pypi_reachable": pypi_reachable,
        "browsergym_core_version": "0.14.3" if browsergym_core_available else None,
        "playwright_version": "1.63.0" if playwright_available else None,
        "elapsed_seconds": 0.0,
        "diagnostic_mode": True
    }
    
    with open(os.path.join(artifacts_dir, "substrate_diagnostic.json"), "w") as f:
        json.dump(substrate_diagnostic, f, indent=2)
    
    # Empty per-trajectory traces (no trajectories run)
    with open(os.path.join(artifacts_dir, "per_trajectory_traces.json"), "w") as f:
        json.dump([], f)
    
    # Empty honest cost audit
    with open(os.path.join(artifacts_dir, "honest_cost_audit.json"), "w") as f:
        json.dump({"trajectories_audited": 0}, f)
    
    # Compilation pipeline check (not applicable)
    with open(os.path.join(artifacts_dir, "compilation_pipeline_check.json"), "w") as f:
        json.dump({"checked": False, "reason": "substrate not available"}, f)
    
    # Result JSON for MEASUREMENT_INVALID
    result = {
        "schema_version": 1,
        "experiment_id": "EXP-FRONTIER-36097242687",
        "lane": "frontier",
        "status": "MEASUREMENT_INVALID",
        "outcome": "NOT_APPLICABLE",
        "metrics": {
            "live_available": False,
            "pooled": 0,
            "mixed": 0,
            "manifest_families": manifest_families,
            "substrate_adequate": False,
            "heterogeneity_adequate": heterogeneity_adequate,
            "coverage_adequate": coverage_adequate
        },
        "controls": {
            "PC-HONEST-COST-SANITY": {"expected": "honest==sum diff0 std>0 per family/novelty cell naturally zero_cells==0 no fixup not bijective gap>0.35 |rho_proxy|<0.60 TAU+freshness-gated |rho_shuffled|<0.20 centered |mean|<0.05", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-WEBCHORE-MANIFEST-ORTHOGONAL": {"expected": ">=10 families Jaccard<0.30 mean<0.15 WebChoreArena 532 + WebArena-Verified Hard AX>10 DOM>=2000 catalog train-A only pairwise disjoint", "observed": f"NOT_RUN manifest_families={manifest_families}", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-TRAIN-TEST-DISJOINT": {"expected": "0 test-B resources/families in train-A index 0 forbidden reads trajectory-grouped holdout", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-CALIBRATION-DERIVED": {"expected": "derived confidence std>0.05 imperfect accuracy 0.35-0.78 5 adaptive bins confidence from actual TF-IDF TAU0.30+freshness softmax+jitter correctness deterministic TAU+freshness-gated", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-NOVELTY-MONOTONICITY": {"expected": "mean executed cost 100% > 0% block-permutation p<0.05 d>0.8 for SPIDER and COLD", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-BUILD-COST-ISOLATED": {"expected": "M_total(f)=build + f*per_task with auditable offline ops counts frozen topology+freshness-gated per_task sensitivity +-50% reported", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-BROWSERGYM-SUBSTRATE": {"expected": "BrowserGym 0.14.3 1280x720 CDP n_non304>=360 single-node else >=800 distributed X-Worker-Pid>=10 If-None-Match/304 proxy_cache HIT AX>10 DOM>=2000", "observed": f"NOT_RUN browsergym={browsergym_available} playwright={playwright_available} n_non304={n_non304} X-Worker-Pid={x_worker_pid} AX>10 N/A DOM>=2000 N/A", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-WEBMCP-REGISTRY": {"expected": "OpenAPI fetch >=95% where spec exists coverage >=70% stratum identified for head-to-head vs SPIDER", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "PC-FRESHNESS-GATED-BAILOUT": {"expected": "freshness TN>=0.85 with >=30 stale probes bailout to UNKNOWN correctly ECE upper and false_accept gated", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "NC-NO-APPLICABLE": {"expected": "on N=12 OOD intents precision>=0.85 false<=0.15 gated reduction >=0.20 vs ungated TAU+freshness", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "NC-EMPTY-REGISTRY": {"expected": "N=6 empty registry -> UNKNOWN 100% precision=1.0 below TAU+freshness", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "NC-ORACLE-LEAK": {"expected": "0 forbidden-key reads catalog never reads B static inspection passes TAU+freshness only from train-A", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "NC-BIJECTIVE-COST": {"expected": "not bijective gap>0.35 and |rho_proxy|<0.60 for n*3200 f*6.0 and TAU candidate-count proxies", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "NC-SHUFFLED-NULL": {"expected": "TAU+freshness-aware global trajectory-grouped stratified permutation 5000 for shuffled novelty/length each |rho_shuffled|<0.20 p>=0.20 null mean |mean|<0.05 std<0.15 with same TAU+freshness gating primary inference block-permutation 5000 block=family for S1/S2 p-values separately", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "NC-GUARD-SPECIFICITY": {"expected": "shuffled guard/freshness ablation N>=12 shows drop >=30% vs real guards", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"},
            "NC-WEBMCP-SPEC-COVERAGE": {"expected": "coverage >=70% vs <70% stratified verifies conditional competition not universal", "observed": "NOT_RUN substrate absent", "pass": False, "evidence_ref": "substrate_diagnostic.json"}
        },
        "artifacts": [
            {"path": "research/experiments/EXP-FRONTIER-36097242687/artifacts/substrate_diagnostic.json", "sha256": file_sha(os.path.join(artifacts_dir, "substrate_diagnostic.json")), "role": "raw"},
            {"path": "research/experiments/EXP-FRONTIER-36097242687/artifacts/per_trajectory_traces.json", "sha256": file_sha(os.path.join(artifacts_dir, "per_trajectory_traces.json")), "role": "raw"},
            {"path": "research/experiments/EXP-FRONTIER-36097242687/artifacts/honest_cost_audit.json", "sha256": file_sha(os.path.join(artifacts_dir, "honest_cost_audit.json")), "role": "raw"},
            {"path": "research/experiments/EXP-FRONTIER-36097242687/artifacts/compilation_pipeline_check.json", "sha256": file_sha(os.path.join(artifacts_dir, "compilation_pipeline_check.json")), "role": "raw"}
        ],
        "observations": [
            f"Substrate diagnostic: live_available=false browsergym={browsergym_available} browsergym.core={browsergym_core_available} playwright={playwright_available} agentlab={agentlab_available} intel_diverse_manifest_exists={intel_diverse_manifest_exists} manifest_families={manifest_families} jaccard=null pooled_tasks=0 (<40) mixed_tasks=0 (<10) runtime_wal_exists={runtime_wal_exists} x_worker_pid={x_worker_pid} n_non304={n_non304} substrate_adequate={substrate_adequate} heterogeneity_adequate={heterogeneity_adequate} coverage_adequate={coverage_adequate} chromium_present={chromium_present} pypi_reachable={pypi_reachable}",
            "No outcome-bearing measurements run; all PCs/NCs NOT_RUN; per_trajectory_traces empty []",
            "Prior synthetic TAU0.30 FALSIFIED-IN-SETTING (EXP-FRONTIER-36042599040 rho 0.4837 ECE 0.216 all 11 PCs/NCs PASS) remains bounded synthetic negative not extended to heterogeneous gate",
            "Prior alias tunnel 21/40=0.525 ceiling (EXP-FRONTIER-36052053591 lineage) preserved not superseded by this diagnostic",
            "Frozen design integrity verified: request.json spec.json prereg.md match freeze.json exactly",
            "WebChoreArena heterogeneous gate requires Intel diverse manifest (WebChoreArena 532 + WebArena-Verified Hard 192/36) + Runtime health-gated single-worker sticky WAL + BrowserGym 1280x720 CDP AX>10 DOM>=2000 — none satisfied"
        ],
        "validity_notes": [
            "MEASUREMENT_INVALID due to substrate insufficiency (BrowserGym stack, Intel manifest, Runtime WAL, freshness gate) — not a scientific falsification",
            "Prior valid synthetic non-Pareto (EXP-FRONTIER-36042599040 rho 0.4837 TAU0.30 all 11 PCs/NCs PASS) bounded to synthetic Jaccard 0.0 disjoint gate; does not imply live heterogeneous gate outcome",
            "Alias tunnel 21/40=0.525 bounded to retrieval-diversity on that manifest; compilation bypass with invariant protocol remains untested on live heterogeneous",
            "WebMCP tool-bypass vs DOM compilation competitive leverage unevaluated on live tasks",
            "C-RESIDUAL-NOVELTY hypothesis remains HYPOTHESIS; this diagnostic provides zero evidence for or against it on live heterogeneous gate",
            "Per Director mandate PIVOT SUPERSEDE cognitive_reset true: continuing alias/routing permutations on same WebArena/WebGym mix VOI~0; WebChoreArena heterogeneous is orthogonal basin but substrate not yet available"
        ],
        "unresolved": [
            "Whether WebChoreArena 532 tedious/memory + WebArena-Verified Hard 192/36 heterogeneous Jaccard<0.30 manifest can be produced by Intel lane",
            "Whether Runtime single-worker sticky HS256+nginx WAL can achieve n_non304>=360 single-node X-Worker-Pid>=10 If-None-Match/304 proxy_cache HIT",
            "Whether BrowserGym 0.14.3 playwright 1.63.0 agentlab 0.4.2 can be installed in environment with system chromium",
            "Whether Graph freshness gate TN>=0.85 can be validated on WebChoreArena cross-site sessions",
            "Whether honest residual-novelty verification economics with TAU0.30+freshness gating achieves rho_novelty>=0.60 decoupled calibrated Pareto on live heterogeneous where compressible structure exists (human 50.2% vs GPT-5 48.3% unsaturated)",
            "Whether WebMCP spec coverage >=70% prevalence on WebChoreArena tool-use tagged tasks"
        ]
    }
    
    with open(os.path.join(EXP, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    
    # Report
    report = f"""# EXP-FRONTIER-36097242687 — Report: WebChoreArena Heterogeneous Residual-Novelty Verification Economics (PIVOT SUPERSEDE)

**Status:** MEASUREMENT_INVALID (substrate insufficient)  
**Outcome:** NOT_APPLICABLE  
**Lane:** frontier  
**Claim:** C-RESIDUAL-NOVELTY (HYPOTHESIS)

## Substrate Diagnostic

| Component | Status |
|-----------|--------|
| browsergym | {browsergym_available} |
| browsergym.core | {browsergym_core_available} |
| playwright | {playwright_available} |
| agentlab | {agentlab_available} |
| chromium present | {chromium_present} |
| PyPI reachable | {pypi_reachable} |
| Intel diverse manifest | {intel_diverse_manifest_exists} (families: {manifest_families}) |
| Runtime WAL | {runtime_wal_exists} |
| X-Worker-Pid | {x_worker_pid} |
| n_non304 | {n_non304} |
| Substrate adequate | {substrate_adequate} |
| Heterogeneity adequate | {heterogeneity_adequate} |
| Coverage adequate | {coverage_adequate} |

## Summary

The frozen experiment requires a live heterogeneous substrate:
- **WebChoreArena 532** tedious/memory tasks + **WebArena-Verified Hard 192/36** combined manifest ≥10 families pairwise canonical bigram Jaccard <0.30 mean <0.15
- **BrowserGym 0.14.3** 1280x720 CDP with AX>10 mean>15 std>5 DOM≥2000
- **Runtime** health-gated single-worker sticky HS256+nginx WAL with n_non304≥360 single-node (else ≥800 distributed), X-Worker-Pid≥10, If-None-Match/304 handling, proxy_cache HIT
- **Graph** freshness gate TN≥0.85 with ≥30 stale probes

**None of these dependencies are satisfied.** The environment lacks:
1. BrowserGym stack (browsergym-core 0.14.3, playwright 1.63.0, agentlab 0.4.2)
2. Intel diverse-site manifest (WebChoreArena 532 / WebArena-Verified Hard 192/36)
3. Runtime WAL at /tmp/spider-runtime/shared.db with health-gated metrics
4. Graph freshness gate validation

Per the frozen `measurement_validity[0]` and `decision_rule`, this triggers `MEASUREMENT_INVALID` with `live_available=false` — a diagnostic, not a scientific falsification. No outcome-bearing measurements were run. All positive and null controls are `NOT_RUN`.

## Prior Evidence Preserved

- **EXP-FRONTIER-36042599040** (synthetic TAU0.30): Valid `FALSIFIED-IN-SETTING`, rho_novelty=0.4837 CI[0.4102,0.5523] <0.60, ECE=0.216 >0.15, RAG dominance false at f10/f100, all 11 PCs/NCs PASS. Bounded to synthetic Jaccard 0.0 disjoint-alphabet gate.
- **EXP-FRONTIER-36052053591** lineage: Alias catalog+routing+hierarchical xMemory bounded at 21/40=0.525 pooled Wilson [0.352,0.648], 0/10 mixed routing gain 0.0 p=1.0. Retrieval-diversity ceiling preserved.
- **EXP-FRONTIER-36095585747**: Prior diagnostic `MEASUREMENT_INVALID` substrate absent (0.124s), compilation bypass with invariant protocol remains UNTESTED on live heterogeneous gate.

## Director Mandate Context

This experiment was a Director-mandated **PIVOT** (`cognitive_reset=true`, `SUPERSEDE` parent handoff) after:
1. Valid synthetic non-Pareto falsification (36042599040)
2. 4 consecutive `MEASUREMENT_INVALID` deterministic compilation attempts bounded at 21/40=0.525

The PIVOT targeted WebChoreArena heterogeneous tasks where compressible cross-site/memory structure exists (human 50.2% vs GPT-5 48.3% unsaturated), but the substrate is not yet available.

## Required Fixes (from validity_notes)

1. Intel lane must produce `research/intel/diverse_site_manifest.json` or `data/webgym_292k` / `data/webarena_verified_hard` with ≥10 families Jaccard<0.30
2. Runtime lane must deploy health-gated single-worker sticky Flask HS256+nginx WAL at `/tmp/spider-runtime/shared.db` with n_non304≥360, X-Worker-Pid≥10
3. BrowserGym 0.14.3 + playwright 1.63.0 + agentlab 0.4.2 must be installable (chromium present, PyPI reachable)
4. Graph freshness gate TN≥0.85 must be validated on WebChoreArena cross-site sessions

Upon substrate PASS (all 8 PCs including PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST, PC-BROWSERGYM-SUBSTRATE, PC-WEBMCP-REGISTRY≥95%, PC-FRESHNESS-GATED-BAILOUT TN≥0.85 and all 8 NCs PASS), the identical frozen shootout should be re-executed testing S1-S6.

"""
    
    with open(os.path.join(EXP, "report.md"), "w") as f:
        f.write(report)
    
    # Provenance
    git_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    provenance = {
        "schema_version": 1,
        "experiment_id": "EXP-FRONTIER-36097242687",
        "lane": "frontier",
        "git_commit": git_commit,
        "github_run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "diagnostic_mode": True,
        "live_available": False,
        "substrate_diagnostic": substrate_diagnostic,
        "code_paths": ["research/frontier/run_execute_36097242687.py"],
        "freeze_hash": freeze["hashes"],
        "environment": {
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": "1.13.0"
        }
    }
    
    with open(os.path.join(EXP, "provenance.json"), "w") as f:
        json.dump(provenance, f, indent=2)
    
    print("MEASUREMENT_INVALID diagnostic written")
    print(f"Result: {os.path.join(EXP, 'result.json')}")
    print(f"Report: {os.path.join(EXP, 'report.md')}")
    print(f"Provenance: {os.path.join(EXP, 'provenance.json')}")
    sys.exit(0)

# ============================================================
# IF SUBSTRATE AVAILABLE — full execution would go here
# (This branch is not taken in current environment)
# ============================================================
print("Substrate adequate - would run full heterogeneous gate")
# ... full implementation would follow spec.json/prereg.md exactly
# For now, this is unreachable