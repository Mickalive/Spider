#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from control_plane import CONTROL_ROOTS, VOLATILE_CONTROL_ROOTS
from research2_contract import CLAIM_STATUSES, LANES, PACKET_FILES

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    claims = load("research/claims/registry.json")
    lanes = load("research/lanes/registry.json")
    models = load("config/models.json")

    claim_ids = [c["id"] for c in claims["claims"]]
    require(len(claim_ids) == len(set(claim_ids)), "duplicate claim id")
    known = set(claim_ids)

    require(set(lanes["lanes"]) == set(LANES), f"lane registry/contract drift: {sorted(lanes['lanes'])} vs {sorted(LANES)}")
    for lane, cfg in lanes["lanes"].items():
        require(bool(cfg.get("mission")), f"lane {lane}: missing mission")
        unknown = set(cfg.get("priority_claims", [])) - known
        require(not unknown, f"lane {lane}: unknown claims {sorted(unknown)}")
        roots = cfg.get("allowed_code_roots", [])
        require(bool(roots) and len(roots) == len(set(roots)), f"lane {lane}: missing/duplicate allowed_code_roots")

    for claim in claims["claims"]:
        require(claim.get("status") in CLAIM_STATUSES, f"claim {claim.get('id')}: invalid registry status {claim.get('status')}")
        owners = set(claim.get("owner_lanes", []))
        require(owners <= set(LANES), f"claim {claim.get('id')}: unknown owner lanes {sorted(owners - set(LANES))}")

    for role, candidates in models["roles"].items():
        require(bool(candidates) and len(candidates) == len(set(candidates)), f"model role {role}: empty or duplicate candidates")

    critical_control = {
        ".github/scripts",
        ".github/workflows",
        "scripts",
        ".opencode/agents",
        "AGENTS.md",
        "SPIDER_ARCHITECTURE_RESEARCH2.md",
        "SPIDER_MASTER_PROMPT.md",
        "research/claims/registry.json",
        "research/lanes/registry.json",
        "research/portfolio",
        "research/scout",
        "research/EXPERIMENT_PACKET.md",
        "config/models.json",
        "SPIDER_CODEX.md",
        "codex",
    }
    require(critical_control <= set(CONTROL_ROOTS), f"control plane missing critical roots: {sorted(critical_control - set(CONTROL_ROOTS))}")
    require(len(CONTROL_ROOTS) == len(set(CONTROL_ROOTS)), "duplicate CONTROL_ROOTS")
    require({"SPIDER_CODEX.md", "codex"} <= set(VOLATILE_CONTROL_ROOTS), "canonical evidence roots must be volatile control-plane overlays")

    required_files = [
        ".github/workflows/spider-lane.yml",
        ".github/workflows/factory-pulse.yml",
        ".github/workflows/codex-sync.yml",
        ".github/workflows/product-promote.yml",
        ".github/scripts/run-opencode-resilient.sh",
        ".opencode/agents/spider_lane_researcher.md",
        ".opencode/agents/spider_lane_auditor.md",
        ".opencode/agents/spider_lane_director.md",
        ".opencode/agents/spider_portfolio_director.md",
        ".opencode/agents/spider_research_scout.md",
        "scripts/check_scope.py",
        "scripts/checkpoint.sh",
        "scripts/finalize_lane.py",
        "scripts/prepare_lane.py",
        "scripts/build_portfolio_snapshot.py",
        "scripts/validate_portfolio_allocation.py",
        "scripts/validate_scout_brief.py",
        "scripts/sync_codex.py",
        "scripts/research2_contract.py",
    ]
    for path in required_files:
        require((ROOT / path).exists(), f"missing Research 2.0 control file: {path}")

    scope = text("scripts/check_scope.py")
    require("from control_plane import CONTROL_ROOTS" in scope, "check_scope must use canonical CONTROL_ROOTS")
    require("--untracked-files=all" in scope and "SPIDER_SCOPE_REPAIRED" in scope, "scope checker lacks complete repair/revalidation path")

    resilient = text(".github/scripts/run-opencode-resilient.sh")
    require("restore_attempt_baseline" in resilient, "model fallback must restore a clean stage baseline between providers")
    require("git reset --hard \"$START_HEAD\"" in resilient and "git clean -fd -e .spider-runtime/" in resilient, "fallback retry baseline is incomplete")
    require("SPIDER_RETRY_BASELINE_RESTORE_FAILED" in resilient, "retry-baseline restoration failure must be explicit")
    require("setsid --wait" in resilient and "MODEL_PGID" in resilient, "model attempts must run in an isolated process group")
    require('kill -TERM -- "-$MODEL_PGID"' in resilient and 'kill -KILL -- "-$MODEL_PGID"' in resilient, "timeouts must terminate the entire model process tree")
    require("Independent audit requires a known producer model to exclude" in resilient, "audit must fail closed when producer-model identity is unknown")

    lane_wf = text(".github/workflows/spider-lane.yml")
    require("SPIDER_REQUIRED_OUTPUTS" in lane_wf, "lane workflow must validate mandatory model outputs")
    require("SPIDER_WAKE_DEFERRED_UNPERSISTED_PACKET" in lane_wf, "wake must verify remote packet durability")
    require(lane_wf.count('exit "$rc"') >= 4, "stage workflow must propagate stage failure exit codes")
    require("director_mandate_b64" in lane_wf and "SPIDER_GLOBAL_DIRECTION_REQUIRED" in lane_wf, "lane workflow must require Global Director governance for NEW work")
    require('gh workflow run spider-lane.yml --ref main -f "lane=$LANE" -f "reason=continuation"' not in lane_wf, "lane workflow must not self-dispatch local continuation")

    prepare = text("scripts/prepare_lane.py")
    require("product promotion pending" in prepare and "promotion_ready" in prepare, "Product allocator must honor the promotion transaction latch")
    require("Global Research Director mandate required" in prepare and "director_mandate" in prepare, "NEW experiments must carry a Global Director mandate")

    pulse = text(".github/workflows/factory-pulse.yml")
    require("SPIDER_CIRCUIT_OPEN" in pulse and "last_failure_control_revision" in pulse, "factory pulse lacks repeated-failure circuit breaker")
    require("SPIDER_PRODUCT_PROMOTION_PENDING" in pulse, "factory pulse must block Product while promotion is pending")
    require("spider_research_scout" in pulse and "spider_portfolio_director" in pulse, "factory pulse must run Scout then Global Research Director")
    require("DIRECTION_MISSING" in pulse and "SPIDER_DIRECTION_UNAVAILABLE" in pulse, "factory pulse must fail closed when global direction is unavailable")
    recovery_wf = text(".github/workflows/lane-recovery.yml")
    require("workflow_run:" in recovery_wf and "SPIDER R2 Lane" in recovery_wf and "conclusion != 'success'" in recovery_wf and "gh workflow run factory-pulse.yml" in recovery_wf, "failed/cancelled lane recovery must explicitly wake global direction outside Factory Pulse concurrency")
    codex_wf = text(".github/workflows/codex-sync.yml")
    require("actions: write" in codex_wf and "Wake global direction after canonicalization" in codex_wf and "gh workflow run factory-pulse.yml" in codex_wf, "Codex sync must explicitly wake global direction after canonicalization")
    require("SPIDER_FACTORY_WAKE_SKIPPED_ACTIVE" not in codex_wf, "Codex sync must not skip a fresher direction wake because an older pulse is active")
    direction_validator = text("scripts/validate_portfolio_allocation.py")
    require("tunnel continuation/allocation requires" not in direction_validator, "direction validator must not override Director judgment with tunnel quotas")
    require("SPIDER_SUPERSEDE_PREFREEZE" in pulse and "SPIDER_RESUME_FROZEN" in pulse, "factory pulse must distinguish pre-freeze redirection from frozen transaction completion")

    promote = text(".github/workflows/product-promote.yml")
    require("git merge --no-commit --no-ff origin/lab2/product" not in promote, "Product workflow must never merge the whole research branch")
    require("git diff --binary --full-index" in promote and "SOURCE_SHA" in promote, "Product promotion must apply a pinned experiment delta")
    require("--diff-filter=A" in promote, "Product promotion must pin the original verdict creation commit")
    require("post-finalization Product packet mutation" in promote, "Product promotion must reject mutated finalized packets")
    require("git apply --reverse --check" in promote and "SPIDER_PRODUCT_ALREADY_PROMOTED" in promote, "Product promotion must be idempotent across latch-write failures")
    require("actions: write" in promote and "SPIDER_FACTORY_WAKE_AFTER_PRODUCT_PROMOTION" in promote and "gh workflow run factory-pulse.yml" in promote, "Product promotion must explicitly wake global direction after clearing the promotion latch")

    codex = text("scripts/sync_codex.py")
    require("post-finalization mutation detected" in codex and "quarantine.json" in codex, "Codex sync lacks packet integrity quarantine")
    require("source_commit" in codex and "freeze hash mismatch" in codex, "Codex sync must pin and validate finalized packets")
    require('"--diff-filter=A"' in codex, "Codex must pin the original verdict creation commit")
    require("parent_handoff sha256 mismatch" in codex, "Codex must validate inherited handoff hashes")
    require("DIRECTOR_CLAIM_STATUSES" in codex, "Codex must reject Director-emitted post-promotion-only claim states")

    scout = text(".opencode/agents/spider_research_scout.md")
    require("reconnaissance" in scout.lower() and "candidate_directions" in scout, "Scout agent lacks generalist reconnaissance contract")

    global_director = text(".opencode/agents/spider_portfolio_director.md")
    require("Research Scout" in global_director and "CONTINUE|PIVOT|PARK|REOPEN|TERMINATE" in global_director, "Global Director lacks Scout/decision contract")

    director = text(".opencode/agents/spider_lane_director.md")
    for status in sorted(CLAIM_STATUSES - {"SHIPPED"}):
        require(f"`{status}`" in director, f"Director prompt missing canonical status {status}")
    require("SHIPPED" in director and "MUST NOT" in director, "Director must reserve SHIPPED for post-promotion state")

    required = set(PACKET_FILES)
    exp_root = ROOT / "research/experiments"
    if exp_root.exists():
        for exp in exp_root.glob("*"):
            if not exp.is_dir() or not (exp / "verdict.json").exists():
                continue
            missing = sorted(x for x in required if not (exp / x).exists())
            require(not missing, f"{exp.name}: finalized packet missing {missing}")

    print(f"SPIDER_R2_VALIDATE_OK claims={len(claim_ids)} lanes={len(lanes['lanes'])} roles={len(models['roles'])} control_roots={len(CONTROL_ROOTS)}")


if __name__ == "__main__":
    main()
