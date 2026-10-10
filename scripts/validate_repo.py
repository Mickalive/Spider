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
    require(models["roles"]["research"][0] == "opencode/big-pickle", "research role must try the empirically successful provider first")
    require(models["roles"]["scout"][0] == "opencode/big-pickle" and models["roles"]["director"][0] == "opencode/big-pickle", "strategic roles must keep the proven provider first")

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
        ".github/workflows/factory-recovery.yml",
        ".github/workflows/codex-sync.yml",
        ".github/workflows/product-promote.yml",
        ".github/scripts/run-opencode-resilient.sh",
        ".opencode/agents/spider_lane_researcher.md",
        ".opencode/agents/spider_lane_auditor.md",
        ".opencode/agents/spider_lane_director.md",
        ".opencode/agents/spider_design_reviewer.md",
        ".opencode/agents/spider_portfolio_director.md",
        ".opencode/agents/spider_research_scout.md",
        "scripts/check_scope.py",
        "scripts/checkpoint.sh",
        "scripts/finalize_lane.py",
        "scripts/prepare_lane.py",
        "scripts/build_portfolio_snapshot.py",
        "scripts/build_scout_fallback.py",
        "scripts/validate_design_review.py",
        "scripts/validate_portfolio_allocation.py",
        "scripts/validate_scout_brief.py",
        "scripts/sync_codex.py",
        "scripts/research2_contract.py",
    ]
    for path in required_files:
        require((ROOT / path).exists(), f"missing Research 2.0 control file: {path}")

    freeze = text("scripts/freeze_experiment.py")
    require("freeze_eligibility" in freeze and "design_review.json" in freeze and "artifact_hashes" in freeze, "freezer must enforce v2 satisfiability review and bound artifacts")
    require("v2 spec claim_ids outside lane charter" in freeze, "freezer must enforce v2 lane claim scope")

    finalizer = text("scripts/finalize_lane.py")
    require("frozen artifact changed or missing" in finalizer and "v2 claim update outside frozen spec.claim_ids" in finalizer and "packet/operational status" in finalizer, "finalizer must enforce v2 frozen artifacts and claim semantics")

    scope = text("scripts/check_scope.py")
    require("from control_plane import CONTROL_ROOTS" in scope, "check_scope must use canonical CONTROL_ROOTS")
    require('"audit.json"' in scope and '"verdict.json"' in scope and '"handoff.json"' in scope and 'stage == "execute"' in scope, "EXECUTE scope must protect future-stage packet outputs")
    require("design_review.json" in scope and "model_design_review.json" in scope, "DESIGN scope must contain independent design-review outputs")
    require("--untracked-files=all" in scope and "SPIDER_SCOPE_REPAIRED" in scope, "scope checker lacks complete repair/revalidation path")

    resilient = text(".github/scripts/run-opencode-resilient.sh")
    require("restore_attempt_baseline" in resilient, "model fallback must restore a clean stage baseline between providers")
    require("git reset --hard \"$START_HEAD\"" in resilient and "git clean -fd -e .spider-runtime/" in resilient, "fallback retry baseline is incomplete")
    require("SPIDER_RETRY_BASELINE_RESTORE_FAILED" in resilient, "retry-baseline restoration failure must be explicit")
    require("setsid --wait" in resilient and "MODEL_PGID" in resilient, "model attempts must run in an isolated process group")
    require('kill -TERM -- "-$MODEL_PGID"' in resilient and 'kill -KILL -- "-$MODEL_PGID"' in resilient, "timeouts must terminate the entire model process tree")
    require("SPIDER_EXCLUDE_MODEL" in resilient and "design_review" in resilient, "audit/design review must support producer-model exclusion")

    lane_wf = text(".github/workflows/spider-lane.yml")
    require("SPIDER_REQUIRED_OUTPUTS" in lane_wf, "lane workflow must validate mandatory model outputs")
    require("SPIDER_WAKE_DEFERRED_UNPERSISTED_PACKET" in lane_wf, "wake must verify remote packet durability")
    require(lane_wf.count('exit "$rc"') >= 4, "stage workflow must propagate stage failure exit codes")
    require("director_mandate_b64" in lane_wf and "SPIDER_GLOBAL_DIRECTION_REQUIRED" in lane_wf, "lane workflow must require Global Director governance for NEW work")
    require("SPIDER_FACTORY_WAKE_AFTER_INCOMPLETE" in lane_wf and "gh workflow run factory-pulse.yml" in lane_wf, "incomplete lane runs must self-wake global direction from always() cleanup")
    require("spider_design_reviewer" in lane_wf and "validate_design_review.py" in lane_wf and "SPIDER_DESIGN_REVIEW_REVISE" in lane_wf, "v2 DESIGN must pass independent pre-freeze review")
    require("checkpoint.sh design-draft" in lane_wf, "v2 DESIGN must durably checkpoint the proposed design before reviewer fallback")
    require('gh workflow run spider-lane.yml --ref main -f "lane=$LANE" -f "reason=continuation"' not in lane_wf, "lane workflow must not self-dispatch local continuation")

    prepare = text("scripts/prepare_lane.py")
    require("product promotion pending" in prepare and "promotion_ready" in prepare, "Product allocator must honor the promotion transaction latch")
    require("Global Research Director mandate required" in prepare and "director_mandate" in prepare, "NEW experiments must carry a Global Director mandate")
    require('"design_contract_version": 2' in prepare and '"freeze_eligibility"' in prepare and '"freeze_artifacts"' in prepare, "NEW experiments must use design-contract v2")

    snapshot_builder = text("scripts/build_portfolio_snapshot.py")
    require("quarantine_by_id" in snapshot_builder and "lane_state_last_quarantined" in snapshot_builder and "canonical_last_decision" in snapshot_builder, "portfolio snapshot must exclude quarantined lane-state verdicts from Director evidence")
    require('req.get("director_mandate")' in snapshot_builder, "portfolio snapshot must detect current Director mandate field")
    require("effective_event_by_claim" in snapshot_builder and "active_mandate_claim_id" in snapshot_builder, "portfolio snapshot must use effective claim state and expose active mandate identity")
    require('effective.get("next_question") or cfg.get("next_gate")' in snapshot_builder and '"registry_next_gate"' in snapshot_builder, "portfolio snapshot must use the effective claim event's next question as current gate")

    ci_wf = text(".github/workflows/ci.yml")
    require("CODEX_LIVE_FALLBACK" in ci_wf and "quarantine_by_id" in ci_wf, "CI must allow only explicit quarantine with canonical fallback")

    pulse = text(".github/workflows/factory-pulse.yml")
    require("SPIDER_CIRCUIT_OPEN" in pulse and "last_failure_control_revision" in pulse, "factory pulse lacks repeated-failure circuit breaker")
    require("SPIDER_PRODUCT_PROMOTION_PENDING" in pulse, "factory pulse must block Product while promotion is pending")
    require("spider_research_scout" in pulse and "spider_portfolio_director" in pulse, "factory pulse must run Scout then Global Research Director")
    require("build_scout_fallback.py" in pulse and "SPIDER_SCOUT_UNAVAILABLE" in pulse, "Scout failure must degrade to a fallback brief instead of blocking direction")
    require("timeout --signal=TERM --kill-after=15s 180s" in pulse and "timeout --signal=TERM --kill-after=15s 480s" in pulse, "Scout and Global Director must have whole-stage deadlines below the 15-minute factory cadence")
    require("if: always()" in pulse and "frozen transactions may still resume" in pulse, "frozen transactions must resume despite strategic control outage")
    require("SPIDER_DIRECTION_OPENCODE_UNAVAILABLE" in pulse and "SPIDER_SCOUT_UNAVAILABLE" in pulse and "SPIDER_GLOBAL_DIRECTOR_UNAVAILABLE" in pulse, "strategic control failures must be visible and propagate to Factory failure")
    require("DIRECTION_MISSING" in pulse and "SPIDER_DIRECTION_UNAVAILABLE" in pulse, "factory pulse must fail closed when global direction is unavailable")
    recovery_wf = text(".github/workflows/lane-recovery.yml")
    require("GH_REPO:" in recovery_wf, "Lane recovery must provide explicit repository context to gh without checkout")
    require("workflow_run:" in recovery_wf and "SPIDER R2 Lane" in recovery_wf and "gh workflow run factory-pulse.yml" in recovery_wf, "failed/cancelled lane recovery must explicitly wake global direction outside Factory Pulse concurrency")
    require('cron: "*/5 * * * *"' in recovery_wf and "SPIDER_LANE_RECOVERY_PENDING" in recovery_wf and "SPIDER_LANE_RECOVERY_ALREADY_CONSIDERED" in recovery_wf, "Lane recovery must poll independently of GITHUB_TOKEN workflow_run delivery and avoid replaying failures already considered by a newer Factory")
    codex_wf = text(".github/workflows/codex-sync.yml")
    require("actions: write" in codex_wf and "Wake global direction after canonicalization" in codex_wf and "gh workflow run factory-pulse.yml" in codex_wf, "Codex sync must explicitly wake global direction after canonicalization")
    require("SPIDER_FACTORY_WAKE_SKIPPED_ACTIVE" not in codex_wf, "Codex sync must not skip a fresher direction wake because an older pulse is active")
    direction_validator = text("scripts/validate_portfolio_allocation.py")
    require("tunnel continuation/allocation requires" not in direction_validator, "direction validator must not override Director judgment with tunnel quotas")
    require("SPIDER_SUPERSEDE_PREFREEZE" in pulse and "SPIDER_RESUME_FROZEN" in pulse, "factory pulse must distinguish pre-freeze redirection from frozen transaction completion")
    require('NEW_DISPOSITION" == "USE"' in pulse and 'ACTIVE_OLD_CLAIM" == "$TARGET_CLAIM"' in pulse, "prefreeze resume must use strategic mandate identity rather than exact question wording")
    require("spider-r2-factory-pulse-${{ github.sha }}" in pulse and "SPIDER_STALE_DIRECTION_SKIP" in pulse and "CURRENT_MAIN" in pulse, "Factory concurrency must isolate control-plane SHAs and stale cycles must be unable to dispatch")
    factory_recovery = text(".github/workflows/factory-recovery.yml")
    require("SPIDER R2 Factory Pulse" in factory_recovery and "SPIDER_FACTORY_RECOVERY_RETRY" in factory_recovery and "SPIDER_FACTORY_RECOVERY_CIRCUIT_OPEN" in factory_recovery and "gh workflow run factory-pulse.yml" in factory_recovery, "Factory Pulse failures must have bounded external recovery")
    require('cron: "*/5 * * * *"' in factory_recovery and "gh run list --workflow=factory-pulse.yml --limit 1" in factory_recovery and "SPIDER_FACTORY_RECOVERY_ACTIVE" in factory_recovery, "Factory recovery must poll independently of GITHUB_TOKEN event chaining and inspect only the freshest pulse")
    require("CONSECUTIVE_FAILURES" in factory_recovery and "Historical failures" in factory_recovery, "Factory recovery circuit breaker must use consecutive failures, not lifetime failures on a long-lived SHA")
    require("GH_REPO:" in factory_recovery, "Factory recovery must provide explicit repository context to gh without checkout")
    require("conclusion == 'cancelled'" not in factory_recovery, "Factory recovery must not retry cancellation superseded by fresher direction")

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
    require("effective_event_by_claim" in codex and "non_epistemic" in codex and "claim_scope_warnings.json" in codex, "Codex must derive effective epistemic claim state and preserve scope warnings")
    require('"next_question": verdict.get("next_question")' in codex, "Codex claim events must carry the Director's next question for effective gate selection")
    require("artifact_hashes" in codex and "design_review.json" in codex, "Codex must validate v2 frozen artifacts and design review")
    require("DIRECTOR_CLAIM_STATUSES" in codex, "Codex must reject Director-emitted post-promotion-only claim states")

    scout = text(".opencode/agents/spider_research_scout.md")
    require("reconnaissance" in scout.lower() and "candidate_directions" in scout, "Scout agent lacks generalist reconnaissance contract")

    global_director = text(".opencode/agents/spider_portfolio_director.md")
    require("Research Scout" in global_director and "CONTINUE|PIVOT|PARK|REOPEN|TERMINATE" in global_director, "Global Director lacks Scout/decision contract")
    require("PROGRAM_AUDIT_2026-10-10.md" in global_director and "ALL THREE readiness conditions" in global_director, "Global Director must use current audit and enforce flagship readiness")
    scout_prompt = text(".opencode/agents/spider_research_scout.md")
    require("PROGRAM_AUDIT_2026-10-10.md" in scout_prompt, "Scout must use current program audit")
    require((ROOT / "research/portfolio/PROGRAM_AUDIT_2026-10-10.md").exists(), "current program audit missing")

    director = text(".opencode/agents/spider_lane_director.md")
    for status in sorted(CLAIM_STATUSES - {"SHIPPED"}):
        require(f"`{status}`" in director, f"Director prompt missing canonical status {status}")
    require("SHIPPED" in director and "MUST NOT" in director, "Director must reserve SHIPPED for post-promotion state")
    require("effective_event_by_claim" in director and "packet/operational" in director, "Lane Director must distinguish effective epistemic state from packet invalidity")

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
