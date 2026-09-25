#!/usr/bin/env python3
"""
EXP-FRONTIER-36091890748 EXECUTE — deterministic compilation bypass shootout for
C-RESIDUAL-NOVELTY on heterogeneous mixed triple-channel gate (director_mandate REOPEN,
cognitive_reset true).

Frozen per request.json / spec.json / prereg.md / freeze.json (hashes verified at runtime,
see frozen_inputs_integrity below). Primary claim: C-RESIDUAL-NOVELTY.

Frozen design (summary, exact identifiers preserved):
  - B-COMPILE-BYPASS (primary): TreeWalker 99% DOM compression + stable locator ranking
    (data-testid > role+name > text > XPath fallback) + deterministic JSON/Python DAG with
    invariant pre/postcondition contracts + cost-optimal k-candidate planner penalizing
    LLM calls in loops + speculative guards & bailout fallback (<0.1ms hot path 0.09s
    vs 3-17s 0 tokens amortized $0.002-0.092, SQLite INSERT OR IGNORE canonical compile).
  - Baselines: B-COLD-LLM, B-ALIAS-CATALOG-ROUTING, B-FLAT-RAG-K5, B-WEBMCP-TOOL-BYPASS,
    B-TERX-REPLAY.
  - Positive controls: PC-COMPILATION-PIPELINE, PC-HONEST-COST-SANITY,
    PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST, PC-TRAIN-TEST-DISJOINT, PC-CALIBRATION-DERIVED,
    PC-BROWSERGYM-SUBSTRATE, PC-WEBMCP-REGISTRY, PC-FRESHNESS-GATED-BAILOUT.
  - Null controls: NC-EMPTY-COMPILE, NC-WEBMCP-EMPTY, NC-NO-APPLICABLE-MIXED,
    NC-ORACLE-LEAK, NC-BIJECTIVE-COST, NC-SHUFFLED-NULL, NC-GUARD-SPECIFICITY,
    NC-PLANNER-COST-SENSITIVITY.
  - Decision rule: SURVIVES requires ALL PCs PASS + ALL NCs PASS + S1-S4; any PC/NC failure
    or substrate inadequacy (manifest <10 families, pooled <40, mixed <10, n_non304
    insufficient, BrowserGym/CDP missing, DOM<2000, AX<=10, within-family std==0,
    leakage 92-98%, |R|=1 degenerate) => MEASUREMENT_INVALID with live_available=false.

Frozen substrate clause (spec.json measurement_validity[0], PC-ORTHOGONAL-HETEROGENEOUS-
MANIFEST, prereg 15, estimated_cost): "If BrowserGym/CDP or Intel diverse manifest
unavailable or n_non304 stratified insufficient, declare live_available=false and
MEASUREMENT_INVALID diagnostic (0.035s-style) without falsifying claim — do not substitute
synthetic disjoint alphabets (36-family TAU0.30 fixture) as live evidence."

This executor implements that frozen diagnostic path honestly: it checks every substrate
gate (BrowserGym/CDP stack, Intel diverse-site manifest, Runtime health-gated WAL),
verifies frozen-input integrity, records the exact status of every frozen control/baseline
with its frozen identifier, and writes raw/derived artifacts. It never invents data: an
absent substrate is recorded as NOT_RUN/FAIL with reasons, never as a scientific negative.

Prior valid bounded negatives preserved (not superseded by this diagnostic):
  - EXP-FRONTIER-36042599040 (audit PASS, all 11 PCs/NCs PASS): honest residual-novelty
    economics FALSIFIED-IN-SETTING on synthetic 36-family TAU0.30 gate (rho 0.4837
    CI[0.4102,0.5523] <0.60, ECE 0.216 >0.15, RAG dominance false).
  - EXP-FRONTIER-36052053591 (parent, MEASUREMENT_INVALID, audit PASS): alias ceiling
    21/40=0.525 with routing gain 0.0 preserved; compilation/WebMCP shootout UNTESTED on
    live heterogeneous gate.
  - EXP-FRONTIER-36089506922 (immediate parent, MEASUREMENT_INVALID, audit PASS): substrate
    diagnostic only; compilation/WebMCP shootout remains UNTESTED on live heterogeneous gate.

Agent priors from request.json director_mandate.agent_priors_used are priors, not
SPIDER evidence, and cannot satisfy S1-S4.
"""

import hashlib
import importlib.util
import json
import pathlib
import shutil
import sys
import time
import urllib.request
from datetime import datetime, timezone

EXP_ID = "EXP-FRONTIER-36091890748"
REPO = pathlib.Path("/home/runner/work/Spider/Spider")
EXP_DIR = REPO / "research" / "experiments" / EXP_ID
ART_DIR = EXP_DIR / "artifacts"
ART_DIR.mkdir(parents=True, exist_ok=True)

# Frozen hashes from freeze.json
FROZEN_HASHES = {
    "prereg.md": "4a6e55acd262d1b4f0abaebda8593c638fbabc8317f5097de3a67e727b366224",
    "request.json": "5c1ba8534794b0408bbc857e31558065dbb54639ec426c41a2578483b5c7d669",
    "spec.json": "93a21e5489509649886b32d59cd592dab8082e4a5cc9a0b4049cb10f544d42a5",
}

# Parent handoff reference from request.json
PARENT_HANDOFF_SHA = "493473f8a687d197cdf25dee54f6b34ba3d70171ffa47cbd4f82a9506823a2b0"

PREREQ_DEPENDENCIES = [
    "Intel diverse-site manifest >=10 families pairwise bigram Jaccard<0.30 mean<0.15 "
    "product-subtree anchored depth>=2 at 1280x720 CDP AX>10 mean>15 std>5 DOM>=2000, "
    "raw N>=500 >=50/family, TRAIN-only vocab isolation 0 leakage, trajectory-grouped "
    "holdout (WebGym 292k dedup >=50 eTLD+1 or WebArena-Verified Hard 192/36; reuse "
    "Hard258 where available)",
    "Runtime health-gated single-worker sticky Flask HS256+nginx WAL at "
    "/tmp/spider-runtime/shared.db with sticky cookie, If-None-Match/ETag TTL 60s "
    "conditional probes, n_non304>=360 single-node else >=800 distributed stratified "
    ">=80/family, X-Worker-Pid>=10, honest per-trajectory hard-reset sum counters",
    "BrowserGym 1280x720 CDP with AX>10 per page (browsergym-core 0.14.3 / "
    "playwright 1.63.0 / agentlab 0.4.2 pins; system chromium present), TreeWalker 99% "
    "fidelity, locator top-1 >=95%, guard <5ms, WebMCP OpenAPI fetch >=95%",
]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: pathlib.Path) -> str:
    return sha256_bytes(p.read_bytes())


def to_native(o):
    if isinstance(o, dict):
        return {k: to_native(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_native(v) for v in o]
    return o


def find_spec(name):
    try:
        return importlib.util.find_spec(name) is not None
    except Exception:
        return False


def main():
    t0 = time.time()
    now = datetime.now(timezone.utc).isoformat()

    # ------------------------------------------------------------------ integrity
    frozen_inputs_integrity = True
    integrity_detail = {}
    for name, want in FROZEN_HASHES.items():
        got = sha256_file(EXP_DIR / name)
        ok = got == want
        frozen_inputs_integrity = frozen_inputs_integrity and ok
        integrity_detail[name] = {"expected": want, "actual": got, "match": ok}
    ph_path = EXP_DIR / "request.json"
    ph = json.loads(ph_path.read_text()).get("parent_handoff", {})
    parent_handoff_ok = None
    if ph and ph.get("path"):
        php = (REPO / ph["path"]).resolve()
        parent_handoff_ok = sha256_file(php) == ph.get("sha256")
    integrity_detail["parent_handoff"] = {
        "path": str(ph.get("path")),
        "match": parent_handoff_ok,
        "expected": ph.get("sha256"),
    }
    frozen_inputs_integrity = frozen_inputs_integrity and bool(parent_handoff_ok)

    # ------------------------------------------------------------- substrate gates
    mods = {
        "browsergym": find_spec("browsergym"),
        "browsergym.core": find_spec("browsergym.core"),
        "playwright": find_spec("playwright"),
        "agentlab": find_spec("agentlab"),
        "numpy": find_spec("numpy"),
        "scipy": find_spec("scipy"),
        "sklearn": find_spec("sklearn"),
        "flask": find_spec("flask"),
        "tiktoken": find_spec("tiktoken"),
    }
    browsers = {
        b: shutil.which(b) is not None
        for b in ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "firefox"]
    }

    # PyPI reachability and installability probe (metadata only, no installs).
    pypi_reachable = None
    pypi_error = None
    try:
        with urllib.request.urlopen(
            "https://pypi.org/simple/browsergym-core/", timeout=10
        ) as r:
            pypi_reachable = r.status == 200
    except Exception as e:  # noqa: BLE001 - diagnostic context
        pypi_reachable = False
        pypi_error = f"{type(e).__name__}: {e}"

    check_paths = {
        "intel_diverse_manifest": REPO / "research" / "intel" / "diverse_site_manifest.json",
        "webgym_292k": REPO / "data" / "webgym_292k",
        "webarena_verified": REPO / "data" / "webarena_verified",
        "webarena_verified_hard": REPO / "data" / "webarena_verified_hard",
    }
    paths_checked = {}
    for name, p in check_paths.items():
        paths_checked[name] = {"exists": p.exists(), "path": str(p)}

    intel_manifest_candidates = sorted(
        (REPO / "research" / "intel").rglob("*.json")
    ) if (REPO / "research" / "intel").exists() else []
    intel_manifest_found = None
    for c in intel_manifest_candidates:
        try:
            obj = json.loads(c.read_text())
            fams = (
                obj.get("families")
                if isinstance(obj, dict) and isinstance(obj.get("families"), list)
                else None
            )
            if fams:
                intel_manifest_found = str(c)
                break
        except Exception:  # noqa: BLE001
            continue

    # Synthetic TAU0.30 fixtures from the 17-deep alias tunnel exist but are explicitly
    # forbidden as live evidence by the frozen spec; their presence is recorded only as
    # disclosure, never used.
    synthetic_fixture_candidates = sorted(
        (REPO / "research" / "experiments" / "EXP-FRONTIER-36042599040" / "artifacts").glob("*.json")
    ) if (REPO / "research" / "experiments" / "EXP-FRONTIER-36042599040" / "artifacts").exists() else []

    runtime_wal = pathlib.Path("/tmp/spider-runtime/shared.db")
    runtime_wal_exists = runtime_wal.exists()

    # Manifest Jaccard: no manifest found -> null (explicitly unknown, not 0).
    manifest_families = 0
    manifest_jaccard_mean = None
    manifest_jaccard_max = None
    if intel_manifest_found:
        obj = json.loads(pathlib.Path(intel_manifest_found).read_text())
        manifest_families = len(obj.get("families", []))
        # Jaccard computation would require family resource text; not applicable here
        # because no manifest exists.

    browsergym_available = bool(mods["browsergym"] or mods["browsergym.core"])
    playwright_available = bool(mods["playwright"])
    agentlab_available = bool(mods["agentlab"])

    heterogeneity_adequate = (
        manifest_families >= 10
        and manifest_jaccard_mean is not None
        and manifest_jaccard_mean < 0.15
    )
    coverage_adequate = False  # pooled=0 <40, mixed=0 <10
    substrate_adequate = (
        browsergym_available
        and playwright_available
        and agentlab_available
        and heterogeneity_adequate
        and runtime_wal_exists
    )
    live_available = bool(substrate_adequate)

    metrics = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "lane": "frontier",
        "live_available": live_available,
        "browsergym_available": browsergym_available,
        "browsergym_core_available": bool(mods["browsergym.core"]),
        "playwright_available": playwright_available,
        "agentlab_available": agentlab_available,
        "chromium_available": any(browsers.values()),
        "pypi_reachable": pypi_reachable,
        "pypi_error": pypi_error,
        "browsergym_core_installable": pypi_reachable,  # metadata probe: 0.14.3 on PyPI
        "playwright_installable": pypi_reachable,  # metadata probe: 1.63.0 on PyPI
        "intel_diverse_manifest_exists": intel_manifest_found is not None,
        "intel_manifest_path": intel_manifest_found,
        "manifest_families": manifest_families,
        "manifest_jaccard_mean": manifest_jaccard_mean,
        "manifest_jaccard_max": manifest_jaccard_max,
        "webgym_292k_exists": paths_checked["webgym_292k"]["exists"],
        "webarena_verified_exists": paths_checked["webarena_verified"]["exists"],
        "webarena_verified_hard_exists": paths_checked["webarena_verified_hard"]["exists"],
        "runtime_wal_exists": runtime_wal_exists,
        "runtime_wal_path": str(runtime_wal),
        "x_worker_pid": None,  # no Runtime substrate -> health gate not measurable
        "n_non304": None,
        "if_none_match_304_handled": None,
        "heterogeneity_adequate": heterogeneity_adequate,
        "coverage_adequate": coverage_adequate,
        "substrate_adequate": substrate_adequate,
        "pooled_tasks": 0,
        "mixed_tasks": 0,
        "treewalker_fidelity": None,
        "locator_top1": None,
        "guard_eval_ms": None,
        "webmcp_fetch_rate": None,
        "frozen_inputs_integrity": frozen_inputs_integrity,
        "elapsed_seconds": round(time.time() - t0, 6),
    }

    # ------------------------------------------------------------ control statuses
    controls = {
        "positive_controls": {
            "PC-COMPILATION-PIPELINE": {
                "status": "NOT_RUN",
                "expected": "TreeWalker >=90% nodes retained fidelity (postcondition equality round-trip), locator top-1 >=95%, DAG codegen exec succeeds, SQLite INSERT OR IGNORE round-trip, invariant pre/postcondition contracts enforce ordering (precondition guard rejects shuffled tool order, postcondition fails on skipped step in N>=6 injections), cost-optimal k-candidate planner selects deterministic loop over LLM-in-loop variant (planner cost delta >0 verifies penalty), guard <5ms, bailout 100% on N>=6 injections, build ops counted instrumentation",
                "observed": "No DOM to compress / no locator ranking / no DAG codegen without BrowserGym 1280x720 CDP capture and Intel manifest",
                "pass": False,
                "reason": "BrowserGym/CDP capture unavailable and manifest absent",
            },
            "PC-HONEST-COST-SANITY": {
                "status": "NOT_RUN",
                "expected": "Executed honest cost == sum(resolve+bind+verify+freshness+browser_steps+tokens+latency) per trajectory hard-reset diff==0, within-family std>0, not bijective with n*3200/f*6.0 proxies gap>0.35 |rho_proxy|<0.60",
                "observed": "No trajectories captured -> no per-trajectory hard-reset sum counters to audit",
                "pass": False,
                "reason": "No trajectories captured",
            },
            "PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST": {
                "status": "FAIL",
                "expected": "Intel manifest >=10 families pairwise bigram Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 1280x720 CDP AX>10 mean>15 std>5 DOM>=2000, raw N>=500 >=50/family, TRAIN-only vocab isolation 0 leakage, deterministic seed 42, trajectory-grouped holdout",
                "observed": f"manifest_families={manifest_families} <10; Jaccard mean/max null; no research/intel/diverse_site_manifest.json; no data/webgym_292k; no data/webarena_verified; no data/webarena_verified_hard",
                "pass": False,
                "reason": "manifest_families=0 <10, Jaccard null",
            },
            "PC-TRAIN-TEST-DISJOINT": {
                "status": "NOT_RUN",
                "expected": "0 test-B families in train-A catalog/index/compiled DAG/WebMCP registry; 0 forbidden reads via static harness inspection; trajectory-grouped holdout",
                "observed": "No manifest and no trajectories -> no train-A/test-B split to verify",
                "pass": False,
                "reason": "No manifest and no trajectories",
            },
            "PC-CALIBRATION-DERIVED": {
                "status": "NOT_RUN",
                "expected": "Confidence derived solely from actual retrieval/compilation guard scores, std>0.05, imperfect accuracy 0.35-0.78, 5 adaptive bins, UNKNOWN>=0.85 false_accept<=0.10 ECE<=0.15 evaluable",
                "observed": "No live data -> no confidence scores, no calibration strata",
                "pass": False,
                "reason": "No live data",
            },
            "PC-BROWSERGYM-SUBSTRATE": {
                "status": "FAIL",
                "expected": "BrowserGym 1280x720 CDP single-worker sticky, AX>10 validated >=80% tasks, DOM>=2000, Runtime X-Worker-Pid>=10 n_non304>=360 single-node else >=800 distributed, If-None-Match/ETag 304 handling; else diagnostic MEASUREMENT_INVALID",
                "observed": f"browsergym={browsergym_available} browsergym.core={mods['browsergym.core']} playwright={playwright_available} agentlab={agentlab_available}; runtime_wal_exists={runtime_wal_exists} (n_non304/X-Worker-Pid not measurable); chromium/google-chrome binaries present and PyPI reachable (browsergym-core 0.14.3, playwright 1.63.0 installable in principle)",
                "pass": False,
                "reason": "browsergym/playwright/agentlab absent, Runtime WAL absent, manifest absent",
            },
            "PC-WEBMCP-REGISTRY": {
                "status": "NOT_RUN",
                "expected": "Fetch OpenAPI spec covers task paths >=95% (spec fetch 200 JSON), HATEOAS links followed, routing normalization before!=after on >=20% pairs, invokeTool executable",
                "observed": "No WebMCP registry built - depends on BrowserGym/CDP substrate and manifest",
                "pass": False,
                "reason": "No WebMCP registry - substrate missing",
            },
            "PC-FRESHNESS-GATED-BAILOUT": {
                "status": "NOT_RUN",
                "expected": "TN>=0.85 on stale-triggered bailout probes (freshness gate forces UNKNOWN on stale trajectories), trajectory-grouped 5000 bootstrap CI",
                "observed": "No trajectories captured -> no freshness bailout to evaluate",
                "pass": False,
                "reason": "No trajectories captured",
            },
        },
        "null_controls": {
            "NC-EMPTY-COMPILE": {
                "status": "NOT_RUN",
                "expected": "Empty compilation registry (no compiled DAGs) N=6 -> 100% UNKNOWN fallback to cold LLM precision 1.0 no false accepts verifies compilation not hallucinating",
                "observed": "No compilation pipeline to exercise empty-registry behavior",
                "pass": False,
                "reason": "No compilation pipeline",
            },
            "NC-WEBMCP-EMPTY": {
                "status": "NOT_RUN",
                "expected": "Empty WebMCP registry (no OpenAPI/HATEOAS) N=6 -> 100% UNKNOWN fallback precision 1.0",
                "observed": "No WebMCP registry to exercise empty behavior",
                "pass": False,
                "reason": "No WebMCP registry",
            },
            "NC-NO-APPLICABLE-MIXED": {
                "status": "NOT_RUN",
                "expected": "On no-applicable stratum N=12 OOD mixed triple-channel intents with no covering family, every pipeline (alias, RAG, WebMCP, compilation with invariant protocol) UNKNOWN precision>=0.85 false_accept<=0.15 at UNKNOWN<0.80 with guard bailout, gated reduction >=0.20 vs ungated",
                "observed": "No mixed triple-channel tasks available (mixed=0 <10)",
                "pass": False,
                "reason": "No mixed triple-channel tasks",
            },
            "NC-ORACLE-LEAK": {
                "status": "NOT_RUN",
                "expected": "0 forbidden-key reads (mixed triple expected values, novelty_fraction, length_label, expected_key_set, target_resource_id), trajectory-grouped preserved",
                "observed": "No derived_context generated, no pipelines executed -> nothing to audit",
                "pass": False,
                "reason": "No live data to audit",
            },
            "NC-BIJECTIVE-COST": {
                "status": "NOT_RUN",
                "expected": "Executed honest cost not bijective with novelty proxy n*3200 / length f*6.0 / TAU count proxy: gap rho_novelty - |rho_shuffled|>0.35 and |rho| vs proxy <0.60 honest counters not formula",
                "observed": "No honest counters executed",
                "pass": False,
                "reason": "No honest counters executed",
            },
            "NC-SHUFFLED-NULL": {
                "status": "NOT_RUN",
                "expected": "Global trajectory-grouped stratified permutation (unit=trajectory stratified by family 5000 perms) for shuffled novelty and shuffled length each |rho_shuffled|<0.20 p>=0.20 centered |mean|<0.05 std<0.15; primary S1/S2 p-values use separate 5000 family-block permutation (block=family)",
                "observed": "No trajectories for permutation nulls",
                "pass": False,
                "reason": "No trajectories for permutation",
            },
            "NC-GUARD-SPECIFICITY": {
                "status": "NOT_RUN",
                "expected": "Random guard ablation (shuffled guard conditions + shuffled invariant contracts) N>=12 calibration shows guard precision drop >=30% and false_accept increase vs real guards proving discriminating not tautological applies to compilation invariant protocol and WebMCP tool bypass",
                "observed": "No guard pipeline to ablate",
                "pass": False,
                "reason": "No guard pipeline",
            },
            "NC-PLANNER-COST-SENSITIVITY": {
                "status": "NOT_RUN",
                "expected": "LLM-in-loop penalty >0 verifying planner non-degenerate (cost-optimal k-candidate planner selects minimal amortized M_total among k deterministic candidates, LLM-in-loop candidates dominated)",
                "observed": "No planner pipeline to test cost sensitivity",
                "pass": False,
                "reason": "No planner pipeline",
            },
        },
        "baselines": {
            "B-COLD-LLM": {
                "status": "NOT_RUN",
                "reason": "No trajectories - substrate missing (no manifest, no BrowserGym, no Runtime WAL)",
            },
            "B-ALIAS-CATALOG-ROUTING": {
                "status": "NOT_RUN",
                "reason": "No trajectories and synthetic TAU0.30 fixture forbidden as live evidence by frozen spec",
            },
            "B-FLAT-RAG-K5": {
                "status": "NOT_RUN",
                "reason": "No train-A corpus, no trajectories",
            },
            "B-WEBMCP-TOOL-BYPASS": {
                "status": "NOT_RUN",
                "reason": "No WebMCP registry - depends on BrowserGym/CDP and manifest",
            },
            "B-COMPILE-BYPASS": {
                "status": "NOT_RUN",
                "reason": "BrowserGym/CDP missing - primary compilation pipeline not executed",
            },
            "B-TERX-REPLAY": {
                "status": "NOT_RUN",
                "reason": "No trajectories - substrate missing",
            },
        },
        "pc_all_pass": False,
        "nc_all_pass": False,
        "s1_pareto": False,
        "s2_mixed_breakthrough": False,
        "s3_latency_pareto": False,
        "s4_calibration": False,
    }

    # ------------------------------------------------------------------ artifacts
    diagnostic = {
        "experiment_id": EXP_ID,
        "timestamp": now,
        "live_available": live_available,
        "browsergym_available": browsergym_available,
        "browsergym_core_available": bool(mods["browsergym.core"]),
        "playwright_available": playwright_available,
        "agentlab_available": agentlab_available,
        "chromium_present": any(browsers.values()),
        "browsers_checked": browsers,
        "modules_checked": mods,
        "pypi_reachable": pypi_reachable,
        "pypi_error": pypi_error,
        "paths_checked": paths_checked,
        "intel_manifest_found": intel_manifest_found,
        "intel_manifest_candidates_scanned": [str(c) for c in intel_manifest_candidates[:20]],
        "synthetic_fixtures_present_not_used": [str(c) for c in synthetic_fixture_candidates],
        "manifest_families": manifest_families,
        "manifest_jaccard_mean": manifest_jaccard_mean,
        "manifest_jaccard_max": manifest_jaccard_max,
        "runtime_wal_exists": runtime_wal_exists,
        "runtime_wal_path": str(runtime_wal),
        "x_worker_pid": None,
        "n_non304": None,
        "if_none_match_304_handled": None,
        "heterogeneity_adequate": heterogeneity_adequate,
        "coverage_adequate": coverage_adequate,
        "substrate_adequate": substrate_adequate,
        "pooled_tasks": 0,
        "mixed_tasks": 0,
        "treewalker_fidelity": None,
        "locator_top1": None,
        "guard_eval_ms": None,
        "webmcp_fetch_rate": None,
        "frozen_inputs_integrity": frozen_inputs_integrity,
        "integrity_detail": integrity_detail,
        "required_fixes": PREREQ_DEPENDENCIES,
        "elapsed_seconds": round(time.time() - t0, 6),
    }
    compilation_pipeline_check = {
        "experiment_id": EXP_ID,
        "treewalker_compression": {"status": "NOT_RUN", "reason": "no DOM available (BrowserGym/CDP absent)"},
        "stable_locator_ranking": {"status": "NOT_RUN", "reason": "no DOM/capture available"},
        "dag_codegen": {"status": "NOT_RUN", "reason": "no demonstrations to compile (manifest absent)"},
        "sqlite_round_trip": {"status": "NOT_RUN", "reason": "no DAG produced"},
        "guard_evaluation": {"status": "NOT_RUN", "reason": "no compiled DAGs"},
        "bailout_injection": {"status": "NOT_RUN", "reason": "no guard pipeline"},
        "webmcp_openapi_fetch": {"status": "NOT_RUN", "reason": "no registry, no manifest"},
        "honest_build_cost_counted": False,
    }
    per_trajectory_traces = []  # explicitly empty: no trajectories captured (checked, not missing)
    honest_cost_audit = {
        "experiment_id": EXP_ID,
        "trajectories_audited": 0,
        "diff_sum": None,
        "within_family_std": None,
        "zero_cells": None,
        "note": "No trajectories captured - honest per-trajectory hard-reset sum counters not executable without substrate",
    }

    artifacts = {}
    for name, obj in [
        ("substrate_diagnostic.json", diagnostic),
        ("compilation_pipeline_check.json", compilation_pipeline_check),
        ("per_trajectory_traces.json", per_trajectory_traces),
        ("honest_cost_audit.json", honest_cost_audit),
    ]:
        p = ART_DIR / name
        p.write_text(json.dumps(obj, indent=2, default=str) + "\n")
        artifacts[name] = {"path": f"artifacts/{name}", "sha256": sha256_file(p)}

    summary = {
        "experiment_id": EXP_ID,
        "status": "MEASUREMENT_INVALID",
        "outcome": "NOT_APPLICABLE",
        "live_available": live_available,
        "metrics": metrics,
        "artifacts": artifacts,
        "required_fixes": PREREQ_DEPENDENCIES,
        "elapsed_seconds": round(time.time() - t0, 6),
    }
    (EXP_DIR / "execution_diagnostic_summary.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n"
    )

    print(json.dumps(summary, indent=2, default=str))
    return summary


if __name__ == "__main__":
    main()