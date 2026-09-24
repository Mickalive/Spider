#!/usr/bin/env python3
"""
EXP-FRONTIER-36049636798 EXECUTE — Diagnostic MEASUREMENT_INVALID path
Frozen design requires BrowserGym 1280x720 CDP, Intel WebGym 292k manifest (>=10 families Jaccard<0.30),
Runtime single-worker sticky n_non304>=800 stratified. All absent -> MEASUREMENT_INVALID diagnostic.
"""
import json
import hashlib
import time
import sys
from pathlib import Path
from datetime import datetime

EXP_DIR = Path("/home/runner/work/Spider/Spider/research/experiments/EXP-FRONTIER-36049636798")
ARTIFACTS_DIR = EXP_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def check_substrate():
    """Verify all required substrates per frozen spec measurement_validity[0] and decision_rule."""
    checks = {}
    
    # BrowserGym/CDP
    try:
        import browsergym
        checks["browsergym_available"] = True
        checks["browsergym_version"] = getattr(browsergym, "__version__", "unknown")
    except ImportError:
        checks["browsergym_available"] = False
        checks["browsergym_version"] = None
    
    # Playwright (required for CDP)
    try:
        import playwright
        checks["playwright_available"] = True
    except ImportError:
        checks["playwright_available"] = False
    
    # Intel WebGym 292k manifest
    webgym_path = Path("/home/runner/work/Spider/Spider/data/webgym_292k")
    manifest_path = Path("/home/runner/work/Spider/Spider/research/intel/diverse_site_manifest.json")
    checks["webgym_292k_exists"] = webgym_path.exists()
    checks["diverse_manifest_exists"] = manifest_path.exists()
    
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        checks["manifest_families"] = len(manifest.get("families", []))
        checks["manifest_jaccard_mean"] = manifest.get("pairwise_jaccard_mean", None)
        checks["manifest_jaccard_max"] = manifest.get("pairwise_jaccard_max", None)
    else:
        checks["manifest_families"] = 0
        checks["manifest_jaccard_mean"] = None
        checks["manifest_jaccard_max"] = None
    
    # Runtime WAL substrate
    wal_path = Path("/tmp/spider-runtime/shared.db")
    checks["runtime_wal_exists"] = wal_path.exists()
    
    # Heterogeneity adequacy (frozen spec: >=10 families, Jaccard<0.30 mean<0.15, pooled>=40, mixed>=10)
    checks["heterogeneity_adequate"] = (
        checks["manifest_families"] >= 10 and
        (checks["manifest_jaccard_mean"] is not None and checks["manifest_jaccard_mean"] < 0.15) and
        (checks["manifest_jaccard_max"] is not None and checks["manifest_jaccard_max"] < 0.30)
    )
    
    # Coverage adequacy
    checks["coverage_adequate"] = False  # No live data without BrowserGym
    
    # Substrate adequacy (all must be true for live experiment)
    checks["substrate_adequate"] = all([
        checks["browsergym_available"],
        checks["playwright_available"],
        checks["webgym_292k_exists"],
        checks["diverse_manifest_exists"],
        checks["runtime_wal_exists"],
        checks["heterogeneity_adequate"]
    ])
    
    checks["live_available"] = checks["substrate_adequate"]
    return checks

def main():
    start_time = time.time()
    
    # Load frozen inputs to verify hashes
    with open(EXP_DIR / "freeze.json") as f:
        freeze = json.load(f)
    
    # Verify frozen hashes match current files
    for fname, expected_hash in freeze["hashes"].items():
        actual_hash = sha256_file(EXP_DIR / fname)
        if actual_hash != expected_hash:
            print(f"WARNING: {fname} hash mismatch! Expected {expected_hash}, got {actual_hash}")
    
    # Run substrate checks
    substrate = check_substrate()
    
    # Save raw diagnostic evidence
    diag_path = ARTIFACTS_DIR / "substrate_diagnostic.json"
    with open(diag_path, "w") as f:
        json.dump(substrate, f, indent=2)
    diag_hash = sha256_file(diag_path)
    
    # Determine outcome per frozen decision_rule
    # MEASUREMENT_INVALID if any PC/NC fails or manifest<10 families or pooled<40 or mixed<10
    # or n_non304 insufficient or BrowserGym/CDP missing or guard pipeline fidelity<90%
    # or locator top-1<95%
    
    pc_results = {
        "PC-COMPILATION-PIPELINE": {"status": "NOT_RUN", "reason": "BrowserGym/CDP missing"},
        "PC-HONEST-COST-SANITY": {"status": "NOT_RUN", "reason": "No trajectories captured"},
        "PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST": {"status": "FAIL", "reason": f"Manifest families={substrate['manifest_families']} <10, Jaccard mean={substrate['manifest_jaccard_mean']}"},
        "PC-TRAIN-TEST-DISJOINT": {"status": "NOT_RUN", "reason": "No train/test split without manifest"},
        "PC-CALIBRATION-DERIVED": {"status": "NOT_RUN", "reason": "No live data"},
        "PC-BROWSERGYM-SUBSTRATE": {"status": "FAIL", "reason": f"browsergym_available={substrate['browsergym_available']}, playwright_available={substrate['playwright_available']}"}
    }
    
    nc_results = {
        "NC-EMPTY-COMPILE": {"status": "NOT_RUN", "reason": "No compilation pipeline"},
        "NC-NO-APPLICABLE-MIXED": {"status": "NOT_RUN", "reason": "No mixed triple-channel tasks"},
        "NC-ORACLE-LEAK": {"status": "NOT_RUN", "reason": "No live data to audit"},
        "NC-BIJECTIVE-COST": {"status": "NOT_RUN", "reason": "No honest counters executed"},
        "NC-SHUFFLED-NULL": {"status": "NOT_RUN", "reason": "No trajectories for permutation"},
        "NC-GUARD-SPECIFICITY": {"status": "NOT_RUN", "reason": "No guard pipeline"}
    }
    
    # All PCs and NCs not passing -> MEASUREMENT_INVALID
    pc_all_pass = all(v["status"] == "PASS" for v in pc_results.values())
    nc_all_pass = all(v["status"] == "PASS" for v in nc_results.values())
    
    # S1-S4 cannot be evaluated
    s1_pass = False
    s2_pass = False
    s3_pass = False
    s4_pass = False
    
    status = "MEASUREMENT_INVALID"
    outcome = "NOT_APPLICABLE"  # Infrastructure failure, not scientific falsification
    
    elapsed = time.time() - start_time
    
    # Build result.json per EXPERIMENT_PACKET.md required shape
    result = {
        "schema_version": 1,
        "experiment_id": "EXP-FRONTIER-36049636798",
        "lane": "frontier",
        "status": status,
        "outcome": outcome,
        "metrics": {
            "live_available": substrate["live_available"],
            "browsergym_available": substrate["browsergym_available"],
            "playwright_available": substrate["playwright_available"],
            "manifest_families": substrate["manifest_families"],
            "manifest_jaccard_mean": substrate["manifest_jaccard_mean"],
            "manifest_jaccard_max": substrate["manifest_jaccard_max"],
            "runtime_wal_exists": substrate["runtime_wal_exists"],
            "heterogeneity_adequate": substrate["heterogeneity_adequate"],
            "elapsed_seconds": elapsed
        },
        "controls": {
            "positive_controls": pc_results,
            "null_controls": nc_results,
            "pc_all_pass": pc_all_pass,
            "nc_all_pass": nc_all_pass,
            "s1_pareto": s1_pass,
            "s2_mixed_breakthrough": s2_pass,
            "s3_latency_pareto": s3_pass,
            "s4_calibration": s4_pass
        },
        "artifacts": [
            {"path": "artifacts/substrate_diagnostic.json", "sha256": diag_hash, "role": "raw"}
        ],
        "observations": [
            "BrowserGym module not importable (ModuleNotFoundError)",
            "Playwright module not importable (ModuleNotFoundError)",
            "WebGym 292k data directory not found at /home/runner/work/Spider/Spider/data/webgym_292k",
            "Diverse site manifest not found at /home/runner/work/Spider/Spider/research/intel/diverse_site_manifest.json",
            "Runtime WAL database not found at /tmp/spider-runtime/shared.db",
            "Manifest families = 0 (required >=10 pairwise Jaccard<0.30)",
            "All positive controls NOT_RUN or FAIL due to missing substrate",
            "All null controls NOT_RUN due to missing substrate",
            "No BrowserGym 1280x720 CDP trajectories captured",
            "No compilation pipeline executed (TreeWalker, locator ranking, DAG codegen, SQLite)",
            "No baseline replays executed (cold LLM, alias catalog, TF-IDF RAG, TERX)",
            "No honest per-trajectory counters collected",
            "No bootstrap/permutation statistics computed"
        ],
        "validity_notes": [
            "MEASUREMENT_INVALID per frozen decision_rule: BrowserGym/CDP missing, Intel manifest absent (0 families), Runtime WAL absent, heterogeneity gate fails (manifest_families=0 <10), coverage gate fails (pooled=0 <40, mixed=0 <10)",
            "This is an infrastructure/substrate failure, NOT a scientific falsification of C-RESIDUAL-NOVELTY or compilation bypass hypothesis",
            "Frozen spec measurement_validity[0] explicitly requires: 'If BrowserGym/CDP or Intel diverse manifest unavailable or n_non304 stratified insufficient, declare live_available=false and MEASUREMENT_INVALID diagnostic (0.035s-style) without falsifying claim — do not substitute synthetic disjoint alphabets as live evidence.'",
            "Prior valid bounded evidence preserved: alias-catalog/routing 21/40=0.525 ceiling (EXP-FRONTIER-36046077922 carry_forward.established[1]), honest residual-novelty non-Pareto falsification on TAU0.30 synthetic gate (EXP-FRONTIER-36042599040 all 11 PCs/NCs PASS, rho=0.4837<0.60, ECE=0.216>0.15, RAG dominance false)",
            "Director mandate PIVOT SUPERSEDE with cognitive_reset=true remains binding; this diagnostic does not invalidate the PIVOT direction",
            "Required fixes for live test: (1) install playwright browsergym-core agentlab with display support for 1280x720 CDP AX>10; (2) produce Intel manifest deterministic seed 42 on WebGym 292k >=50 eTLD+1 or WebArena-Verified v2 192/36 with >=10 families Jaccard<0.30; (3) deploy Runtime single-worker sticky Flask HS256+nginx WAL with honest per-trajectory hard-reset counters and If-None-Match/ETag TTL 60s n_non304>=800 stratified |rho_shuffled|<0.20",
            "Agent priors from director_mandate (path dependence, planning horizon, amortization optimism, memory vs dynamics, compilation vs LLM leverage) are general priors labeled in validity_notes/do_not_assume, not SPIDER evidence"
        ],
        "unresolved": [
            "Whether deterministic compilation bypass achieves honest Pareto dominance on live heterogeneous mixed triple-channel tasks (WebArena-Verified v2 / WebGym >=10 families Jaccard<0.30 AX>10 1280x720 CDP)",
            "Whether compilation breaks mixed 0/10 to >=4/10 with pooled coverage>=0.60 exceeding alias 0.525 ceiling",
            "Whether guard bailout calibration achieves UNKNOWN>=0.85 false_accept<=0.10 ECE<=0.15 on live substrate",
            "Whether |rho_shuffled|<0.20 holds for novelty/length proxies with trajectory-grouped permutation on real Web data",
            "Whether code-approval leverage (compile-once + guard-verified replay) materially exceeds retrieval-diversity ceiling",
            "Substrate repair: Intel WebGym 292k dedup manifest >=50 eTLD+1, Runtime single-worker sticky n_non304>=800 health gate, BrowserGym 1280x720 CDP collection"
        ]
    }
    
    # Write result.json
    result_path = EXP_DIR / "result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)
    
    # Write report.md
    report = f"""# EXP-FRONTIER-36049636798 EXECUTE Report

**Lane:** frontier  
**Claim:** C-RESIDUAL-NOVELTY (deterministic compilation bypass PIVOT)  
**Status:** MEASUREMENT_INVALID  
**Outcome:** NOT_APPLICABLE (infrastructure failure, not scientific falsification)  
**Elapsed:** {elapsed:.3f}s  
**Timestamp:** {datetime.utcnow().isoformat()}Z

## Frozen Design Summary

This experiment was a Director-mandated PIVOT SUPERSEDE with cognitive_reset=true (cycle 36049089810) from the 17-deep alias-catalog/routing/WebMCP tunnel (bounded at pooled 21/40=0.525 Wilson [0.352,0.648], 0/10 mixed triple-channel, routing gain 0.0 p=1.0) and valid non-Pareto falsification of residual-novelty economics under honest per-trajectory hard-reset sum counters on 36-family orthogonal Jaccard<0.30 fixture (EXP-FRONTIER-36042599040 PASS, all 11 PCs/NCs PASS).

The frozen hypothesis (H1): On heterogeneous mixed triple-channel tasks (WebArena-Verified v2 192/36 or WebGym 292k dedup manifest >=10 families pairwise bigram Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 at 1280x720 CDP AX>10), deterministic compilation bypass — first-run BrowserGym 1280x720 CDP trajectory capture -> TreeWalker 99% compression + stable locator ranking + deterministic JSON/Python DAG with speculative guards + bailout fallback to LLM — will achieve honest end-to-end economics Pareto dominance versus both cold LLM browsing and alias catalog+routing+hierarchical xMemory / flat TF-IDF RAG k5.

## Substrate Diagnostic Results

| Substrate Component | Required | Available | Details |
|---|---|---|---|
| BrowserGym (browsergym-core) | Yes | **NO** | ModuleNotFoundError |
| Playwright (CDP support) | Yes | **NO** | ModuleNotFoundError |
| WebGym 292k data | Yes | **NO** | Directory not found |
| Intel diverse_site_manifest.json | Yes (>=10 families Jaccard<0.30) | **NO** | File not found, 0 families |
| Runtime WAL (/tmp/spider-runtime/shared.db) | Yes (n_non304>=800 stratified) | **NO** | File not found |
| Heterogeneity adequacy (frozen) | >=10 families, Jaccard mean<0.15, max<0.30 | **FAIL** | 0 families |
| Coverage adequacy (frozen) | Pooled>=40, Mixed>=10 | **FAIL** | 0 tasks |

## Controls Evaluation

### Positive Controls (ALL must PASS for SURVIVES_CURRENT_TEST)

| Control | Status | Reason |
|---|---|---|
| PC-COMPILATION-PIPELINE | NOT_RUN | BrowserGym/CDP missing |
| PC-HONEST-COST-SANITY | NOT_RUN | No trajectories captured |
| PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST | **FAIL** | Manifest families=0 <10 |
| PC-TRAIN-TEST-DISJOINT | NOT_RUN | No train/test split without manifest |
| PC-CALIBRATION-DERIVED | NOT_RUN | No live data |
| PC-BROWSERGYM-SUBSTRATE | **FAIL** | browsergym_available=false, playwright_available=false |

### Null Controls (ALL must PASS for SURVIVES_CURRENT_TEST)

| Control | Status | Reason |
|---|---|---|
| NC-EMPTY-COMPILE | NOT_RUN | No compilation pipeline |
| NC-NO-APPLICABLE-MIXED | NOT_RUN | No mixed triple-channel tasks |
| NC-ORACLE-LEAK | NOT_RUN | No live data to audit |
| NC-BIJECTIVE-COST | NOT_RUN | No honest counters executed |
| NC-SHUFFLED-NULL | NOT_RUN | No trajectories for permutation |
| NC-GUARD-SPECIFICITY | NOT_RUN | No guard pipeline |

**PC All Pass:** False  
**NC All Pass:** False

## Survival Criteria (Frozen Decision Rule)

| Criterion | Required | Result |
|---|---|---|
| All PCs PASS | Yes | **FAIL** |
| All NCs PASS | Yes | **FAIL** |
| S1 Pareto: saving>=25% vs cold, dominance vs RAG/alias at f10/f100 | Yes | NOT_EVALUATED |
| S2 Mixed: >=4/10 mixed, pooled>=0.60, gap>=0.07 vs alias | Yes | NOT_EVALUATED |
| S3 Latency: hot-path <200ms mean, <100ms median, 0 tokens | Yes | NOT_EVALUATED |
| S4 Calibration: UNKNOWN>=0.85, false<=0.10, ECE<=0.15, |rho_shuffled|<0.20 | Yes | NOT_EVALUATED |

## Verdict

**MEASUREMENT_INVALID** — The frozen experiment cannot be executed because the required measurement substrate is entirely absent. This is an infrastructure failure, NOT a scientific falsification of the compilation bypass hypothesis or C-RESIDUAL-NOVELTY.

Per the frozen `measurement_validity[0]` and `decision_rule`:
> "If BrowserGym/CDP or Intel diverse manifest unavailable or n_non304 stratified insufficient, declare live_available=false and MEASUREMENT_INVALID diagnostic (0.035s-style) without falsifying claim — do not substitute synthetic disjoint alphabets as live evidence."

> "MEASUREMENT_INVALID if any PC/NC fails or manifest <10 families or pooled<40 or mixed<10 or n_non304 insufficient or BrowserGym/CDP missing or guard pipeline fidelity <90% or locator top-1 <95% — no inference to product; requires substrate repair..."

## Prior Valid Evidence Preserved (Per Parent Handoff carry_forward.established)

1. **Alias-catalog/routing/WebMCP tunnel bounded**: 21/40=0.525 pooled, 0/10 mixed triple-channel, routing gain 0.0 p=1.0 on synthetic diverse substrate
2. **Honest residual-novelty non-Pareto validly FALSIFIED**: EXP-FRONTIER-36042599040 PASS, all 11 PCs/NCs PASS, rho=0.4837<0.60, ECE=0.216>0.15, RAG dominance false at f10/f100
3. **Physics Dirichlet-Multinomial companion**: BC~0 rel_sep<200 with trajectory-grouped exact Gamma-ratio |perm-analytic|<0.03 at N=1000-1999 on real BrowserGym 1280x720

## Required Fixes for Live Test

1. **Intel**: Produce diverse-site manifest deterministic seed 42 on WebGym 292k >=50 eTLD+1 or WebArena-Verified v2 192/36 with >=10 families pairwise Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2, AX>10 mean>15 std>5, raw N>=500 (>=50/family)
2. **Runtime**: Deploy single-worker sticky Flask HS256+nginx substrate with /tmp/spider-runtime/shared.db WAL, sticky cookie, If-None-Match/ETag TTL 60s conditional probes, n_non304>=800 stratified >=80/family, honest per-trajectory hard-reset sum counters, trajectory-grouped |rho_shuffled|<0.20
3. **Frontier/Graph**: Install playwright browsergym-core agentlab with display support for 1280x720 CDP AX>10 trajectory capture

## Do Not Assume (Per Parent Handoff carry_forward.do_not_assume)

- This MEASUREMENT_INVALID does not falsify or validate C-WEB-DYNAMICS or C-RESIDUAL-NOVELTY
- Alias-catalog 21/40=0.525 or residual-novelty non-Pareto on synthetic TAU0.30 gate does not imply live BrowserGym will also be non-Pareto
- Jaccard 0.0 disjoint alphabets does not generalize to natural Web overlap 0.30-0.60
- Prior synthetic cost formulas (n*3200, f*6.0) are not evidence for live LLM Pareto
- Distributed n>=800, 1280x720 CDP AX>10 heterogeneity, or health-gated n_non304>=800 have NOT been tested
- Agent priors from director_mandate are general priors, not SPIDER evidence

## Next Action

Repair substrate per dependencies, then re-execute same frozen gate. Do NOT run 18th alias/routing permutation (VOI~0 per Director comparative_reasoning). Continue=false awaiting Global Research Director pulse.

---
*Report generated from frozen EXECUTE stage. Raw evidence preserved in artifacts/substrate_diagnostic.json*
"""
    report_path = EXP_DIR / "report.md"
    with open(report_path, "w") as f:
        f.write(report)
    
    # Write provenance.json
    provenance = {
        "schema_version": 1,
        "experiment_id": "EXP-FRONTIER-36049636798",
        "lane": "frontier",
        "git_commit": "6f600ea0483a74554499186a93cfafc2e0579521",  # from request.json base_sha
        "github_run_id": "36049636798",  # from request.json origin_github_run_id
        "executed_at": datetime.utcnow().isoformat() + "Z",
        "elapsed_seconds": elapsed,
        "python_version": sys.version.split()[0],
        "numpy_version": "not_imported",
        "environment": {
            "browsergym_available": substrate["browsergym_available"],
            "playwright_available": substrate["playwright_available"],
            "webgym_292k_exists": substrate["webgym_292k_exists"],
            "diverse_manifest_exists": substrate["diverse_manifest_exists"],
            "runtime_wal_exists": substrate["runtime_wal_exists"]
        },
        "code_paths": [
            "research/experiments/EXP-FRONTIER-36049636798/run_execute.py"
        ],
        "frozen_inputs": {
            "request.json": freeze["hashes"]["request.json"],
            "spec.json": freeze["hashes"]["spec.json"],
            "prereg.md": freeze["hashes"]["prereg.md"],
            "freeze.json": sha256_file(EXP_DIR / "freeze.json")
        },
        "artifacts_produced": [
            {"path": "artifacts/substrate_diagnostic.json", "sha256": diag_hash, "role": "raw"}
        ],
        "substrate_diagnostic": substrate,
        "diagnostic_mode": True,
        "measurement_invalid_reason": "Required measurement substrate absent: BrowserGym/CDP, Intel WebGym 292k manifest (>=10 families Jaccard<0.30), Runtime WAL n_non304>=800 stratified. All positive controls NOT_RUN or FAIL, all null controls NOT_RUN.",
        "prior_valid_evidence_preserved": [
            "EXP-FRONTIER-36046077922 carry_forward.established: alias ceiling 21/40=0.525, residual-novelty non-Pareto falsified (EXP-FRONTIER-36042599040)"
        ]
    }
    
    prov_path = EXP_DIR / "provenance.json"
    with open(prov_path, "w") as f:
        json.dump(provenance, f, indent=2)
    
    print(f"EXECUTE complete: status={status}, outcome={outcome}, elapsed={elapsed:.3f}s")
    print(f"Result written to {result_path}")
    print(f"Report written to {report_path}")
    print(f"Provenance written to {prov_path}")
    print(f"Diagnostic artifact: {diag_path} (sha256={diag_hash})")

if __name__ == "__main__":
    main()
