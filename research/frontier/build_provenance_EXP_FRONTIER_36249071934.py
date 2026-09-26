#!/usr/bin/env python3
"""Assemble provenance.json for EXP-FRONTIER-36249071934.

This script performs NO measurement. It records how the already-measured
artifacts were produced, re-verifies every artifact hash at assembly time, and
hashes the stage outputs. Run it AFTER result.json and report.md are final.

Usage:
    python3 research/frontier/build_provenance_EXP_FRONTIER_36249071934.py
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXP = "EXP-FRONTIER-36249071934"
REPO = Path(__file__).resolve().parents[2]
PKT = REPO / "research" / "experiments" / EXP
ART = PKT / "artifacts"
REPO_REL = f"research/experiments/{EXP}"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


m = json.loads((ART / "run_manifest.json").read_text())
av = json.loads((ART / "availability_probe.json").read_text())
role = {
    "availability_probe.json": "raw",
    "substrate_determinism_check.json": "raw",
    "kernel_probe.json": "raw",
    "spans_no-memory-deterministic.jsonl": "raw",
    "spans_inherited-spider.jsonl": "raw",
    "spans_cold-exploration.jsonl": "raw",
    "episodes_no-memory-deterministic.jsonl": "raw",
    "episodes_inherited-spider.jsonl": "raw",
    "episodes_cold-exploration.jsonl": "raw",
    "control_spans_pc_witnessed_determinism.jsonl": "raw",
    "control_spans_nc_zero_determinism.jsonl": "raw",
    "control_spans_pc_exact_replay.jsonl": "raw",
    "matched_task_instances_check.json": "derived",
    "controls.json": "derived",
    "sensitivity_novelty_sweep.json": "derived",
    "derived_metrics.json": "derived",
}
mismatch = [n for n, h in m["artifact_sha256"].items() if sha(ART / n) != h]

code = [
    "research/frontier/substrate_deterministic_http.py",
    "research/frontier/taskplan.py",
    "research/frontier/measure.py",
    "research/frontier/__init__.py",
    "research/frontier/arms/__init__.py",
    "research/frontier/arms/common.py",
    "research/frontier/arms/deopt_ratchet.py",
    "research/frontier/arms/inherited_spider.py",
    "research/frontier/arms/cold_exploration.py",
    "research/frontier/run_experiment_EXP_FRONTIER_36249071934.py",
    "research/frontier/build_result_EXP_FRONTIER_36249071934.py",
    "research/frontier/build_provenance_EXP_FRONTIER_36249071934.py",
]
shipped = ["src/spider/kernel.py", "src/spider/models.py", "src/spider/registry.py"]

prov = {
    "schema_version": 1,
    "experiment_id": EXP,
    "lane": "frontier",
    "stage": "EXECUTE",
    "produced_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "claim_ids": ["C-RESIDUAL-NOVELTY"],
    "github": {
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "workflow": os.environ.get("GITHUB_WORKFLOW"),
        "event_name": os.environ.get("GITHUB_EVENT_NAME"),
        "actor": os.environ.get("GITHUB_ACTOR"),
        "run_sha_env": os.environ.get("GITHUB_SHA"),
        "request_base_sha": "2f0310424190f4b0245164f6ad3cde49c742e3b6",
        "pre_execute_checkpoint_sha": "1246dea8cd4e7bd4251f85609a1e4775ea1e1126",
        "execution_head_sha": m["git_head"],
        "note": "the run is workflow_dispatch on branch lab2/frontier; execution_head_sha is the HEAD "
                "actually on disk during measurement, which differs from both the request base sha and "
                "the pre-execute checkpoint sha",
    },
    "git": {
        "branch": subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO, capture_output=True, text=True
        ).stdout.strip(),
        "head": m["git_head"],
        "remote_origin": "https://github.com/Mickalive/Spider",
        "commit_created_by_this_stage": False,
        "branch_or_history_operations_performed": [],
        "working_tree_state_at_end_of_run": m["git_status_porcelain"].splitlines(),
        "scope_note": "frontier allowed_code_root is research/frontier (research/harness unused). "
                      "research/experiments/EXP-FRONTIER-36249071934/ was written only by the "
                      "factory. src/spider/ was read and imported, never modified. .github/, "
                      ".opencode/, SPIDER_CODEX.md, other lanes and other experiments were not "
                      "touched.",
    },
    "frozen_inputs_verified": {
        "freeze_json": f"{REPO_REL}/freeze.json",
        "verified_before_execution": True,
        "verified_after_execution": True,
        "hashes": json.loads((PKT / "freeze.json").read_text())["hashes"],
        "mutated_by_this_stage": False,
    },
    "parent_handoff_reference": {
        "experiment_id": "EXP-FRONTIER-36129180789",
        "path": "research/experiments/EXP-FRONTIER-36129180789/handoff.json",
        "sha256": "3d1a056b0d8d997305f21d6694f36b2ead7cdd569d8e9b5976a25505deea28e2",
    },
    "environment": {
        "python": m["python"],
        "python_version_short": platform.python_version(),
        "platform": m["platform"],
        "libc": "glibc 2.39",
        "cwd": m["cwd"],
        "containerized": True,
        "host": "Azure Linux x86_64 GitHub-hosted runner",
        "network_access_required_at_runtime": False,
        "third_party_python_packages_installed": [],
    },
    "substrate": {
        "kind": "self-authored Python-stdlib ThreadingHTTPServer bound to 127.0.0.1 on an ephemeral port",
        "deterministic_by_construction": True,
        "randomness_in_bodies_or_headers": False,
        "volatile_headers_excluded_from_signature": ["Date", "Server", "Host", "Content-Length"],
        "idempotency_check": "8 request shapes x 100 identical repeats = 800 round trips, all identical",
        "flask_importable": av["flask_importable"],
        "fastapi_importable": av["fastapi_importable"],
        "browsergym_importable": av["browsergym_importable"],
        "playwright_importable": av["playwright_importable"],
        "openai_importable": av["openai_importable"],
        "env_OPENAI_API_KEY_present": av["env_OPENAI_API_KEY_present"],
        "env_HF_TOKEN_present": av["env_HF_TOKEN_present"],
        "docker_cli_available": av["docker_cli_available"],
        "docker_used": False,
        "model_provider": "none; the prereg.md 12 oracle is a deterministic perfect-policy function",
    },
    "datasets_and_fixtures": {
        "external_datasets": [],
        "fixture": "research/frontier/taskplan.py",
        "fixture_description": "5 preregistered intents x 4 work items x 6 steps = 24 spans per "
                               "episode, 50 episodes, target novelty rate 0.50, constant control "
                               "nonce rule",
        "fixture_is_experimenter_authored": True,
        "task_instances_identical_across_arms": True,
        "matched_instance_evidence": f"{REPO_REL}/artifacts/matched_task_instances_check.json",
    },
    "code_paths": [{"path": p, "sha256": sha(REPO / p)} for p in code],
    "shipped_code_imported_unmodified": [{"path": p, "sha256": sha(REPO / p)} for p in shipped],
    "artifacts": [
        {
            "path": f"{REPO_REL}/artifacts/{n}",
            "sha256": m["artifact_sha256"][n],
            "role": role[n],
            "bytes": (ART / n).stat().st_size,
        }
        for n in m["artifact_sha256"]
    ],
    "stage_outputs": [
        {"path": f"{REPO_REL}/result.json", "sha256": sha(PKT / "result.json"), "role": "producer_handoff"},
        {"path": f"{REPO_REL}/report.md", "sha256": sha(PKT / "report.md"), "role": "explanatory"},
        {
            "path": f"{REPO_REL}/provenance.json",
            "sha256": None,
            "role": "provenance",
            "note": "self; cannot hash itself",
        },
    ],
    "commands": [
        {
            "command": "python3 research/frontier/run_experiment_EXP_FRONTIER_36249071934.py",
            "purpose": "execute all arms, all controls and the sensitivity sweep; write artifacts/",
            "wall_time_seconds": m["wall_time_seconds"],
            "note": "re-running regenerates every artifact; the ephemeral substrate port and the wall "
                    "time differ between runs, everything else is deterministic given the same code",
        },
        {
            "command": "python3 research/frontier/build_result_EXP_FRONTIER_36249071934.py",
            "purpose": "project already-measured artifact numbers into result.json; performs no "
                       "measurement",
        },
        {
            "command": "python3 research/frontier/build_provenance_EXP_FRONTIER_36249071934.py",
            "purpose": "assemble provenance.json; performs no measurement",
        },
    ],
    "determinism_and_randomness": {
        "arm_action_selection": "deterministic",
        "model_oracle": "deterministic perfect policy (prereg.md 12)",
        "only_randomness_in_the_pipeline": "paired bootstrap resampling of episode costs",
        "bootstrap_seed": 20260926,
        "bootstrap_resamples": 10000,
        "rng": "python random.Random(seed), stdlib Mersenne Twister",
        "expected_run_to_run_variation": "only wall_time_seconds and the ephemeral substrate port",
    },
    "integrity": {
        "artifact_hashes_recomputed_and_verified_at_stage_end": len(m["artifact_sha256"]) - len(mismatch),
        "artifact_hashes_mismatched": mismatch,
        "frozen_input_hashes_reverified_at_stage_end": True,
        "self_reported_by": "EXECUTE producer; the independent AUDIT must recompute independently",
    },
    "measurement_scope": {
        "primary_spans_executed": 3600,
        "control_spans_executed": 2448,
        "sweep_spans_executed": 4800,
        "episodes": {
            "primary": 150,
            "pc_witnessed_determinism": 50,
            "nc_zero_determinism": 50,
            "pc_exact_replay": 2,
            "nc_empty_registry": 1,
            "sweep": 200,
        },
        "model_oracle_invocations": {
            "primary_arms": 3120,
            "primary_breakdown": {
                "B-NO-MEMORY-DETERMINISTIC": 720,
                "B-INHERITED-SPIDER": 1200,
                "B-COLD-EXPLORATION": 1200,
            },
            "controls": 1440,
            "control_breakdown": {
                "PC-WITNESSED-DETERMINISM": 240,
                "NC-ZERO-DETERMINISM": 1200,
                "PC-EXACT-REPLAY": 0,
                "NC-EMPTY-REGISTRY": 0,
            },
            "sweep": 3882,
            "total": 8442,
            "note": "PC-EXACT-REPLAY made 0 oracle invocations because every one of its 48 spans was "
                    "resolved by the shipped kernel rather than deopt-to-agent; that control therefore "
                    "measures the kernel's decision path, not the oracle",
        },
        "real_llm_calls": 0,
        "browser_sessions": 0,
        "docker_invocations": 0,
        "http_round_trips_against_the_substrate": 10848,
        "http_round_trips_note": "3600 primary + 2448 control + 4800 sweep = 10848 span executions, "
                                 "each one a real request over a real socket; in addition the "
                                 "substrate idempotency check issued 800 requests that are not part "
                                 "of any arm",
    },
    "reproduction": {
        "expected_to_reproduce": "all metrics exactly",
        "preconditions": [
            "checkout HEAD e178d5b18b5a935c39a4815cad21a952fb054a5c, or any commit whose "
            "research/frontier/ files hash as recorded in code_paths",
            "python 3.12 or compatible stdlib only",
            "no network, no API key, no browser, no docker required",
            "127.0.0.1 loopback must be bindable",
        ],
        "known_nondeterminism": ["wall_time_seconds", "ephemeral substrate port", "git_status_porcelain"],
    },
    "limitations_of_this_provenance": [
        "This provenance is producer-written and self-reported. It records how the numbers in "
        "result.json were produced; it does not attest that the design was adequate.",
        "The docker CLI was present in the environment although the frozen measurement_validity text "
        "says 'no docker'. It was deliberately unused; the experiment is stdlib-only. Recorded so the "
        "auditor does not have to re-derive the availability facts.",
        "No artifact hash in this file was produced by an independent party.",
    ],
}

out = PKT / "provenance.json"
out.write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")
print("wrote", out, out.stat().st_size, "bytes")
print("artifact hash mismatches:", mismatch)
print(
    "outputs hashed:",
    [(o["path"].rsplit("/", 1)[-1], (o["sha256"] or "self")[:12]) for o in prov["stage_outputs"]],
)
