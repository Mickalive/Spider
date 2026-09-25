#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECENT_WINDOW = 60
DEFAULT_LANE_HISTORY = 15
CLOSED_STATUSES = {"REJECTED", "SUPERSEDED", "SHIPPED"}


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git_file_exists(ref: str, path: str) -> bool:
    p = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p.returncode == 0


def git_show_json(ref: str, path: str) -> dict:
    try:
        raw = subprocess.check_output(
            ["git", "show", f"{ref}:{path}"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return json.loads(raw)
    except Exception:
        return {}


def created_key(entry: dict) -> str:
    return str(entry.get("created_at") or "")


def primary_claim(entry: dict) -> str | None:
    claims = entry.get("claim_ids") or []
    return claims[0] if claims else None


def claim_streak(entries: list[dict]) -> tuple[str | None, int]:
    if not entries:
        return None, 0
    last_claim = primary_claim(entries[-1])
    if not last_claim:
        return None, 0
    streak = 0
    for entry in reversed(entries):
        if last_claim in (entry.get("claim_ids") or []):
            streak += 1
        else:
            break
    return last_claim, streak


def compact_experiment(entry: dict) -> dict:
    return {
        "experiment_id": entry.get("experiment_id"),
        "created_at": entry.get("created_at"),
        "claim_ids": entry.get("claim_ids") or [],
        "question": entry.get("question"),
        "audit_status": entry.get("audit_status"),
        "decision": entry.get("decision"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle-id", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--recent-window", type=int, default=DEFAULT_RECENT_WINDOW)
    ap.add_argument("--lane-history", type=int, default=DEFAULT_LANE_HISTORY)
    args = ap.parse_args()

    lane_registry = load("research/lanes/registry.json")["lanes"]
    claim_registry = {c["id"]: c for c in load("research/claims/registry.json")["claims"]}
    index = load("codex/index.json").get("experiments", {})
    quarantine = load("codex/quarantine.json")
    quarantine_by_id = {
        item.get("experiment_id"): item
        for item in quarantine
        if item.get("experiment_id")
    }
    claim_state = load("codex/claim_state.json")
    latest_claim_events = claim_state.get("latest_event_by_claim", {})

    experiments: list[dict] = []
    for exp_id, raw in index.items():
        entry = dict(raw)
        entry["experiment_id"] = exp_id
        experiments.append(entry)
    experiments.sort(key=created_key)

    recent_global = experiments[-args.recent_window :]
    global_recent_counts = {
        claim_id: sum(claim_id in (e.get("claim_ids") or []) for e in recent_global)
        for claim_id in claim_registry
    }
    global_total_counts = {
        claim_id: sum(claim_id in (e.get("claim_ids") or []) for e in experiments)
        for claim_id in claim_registry
    }

    claims: dict[str, dict] = {}
    for claim_id, cfg in claim_registry.items():
        latest = latest_claim_events.get(claim_id) or {}
        effective_status = latest.get("status") or cfg.get("status")
        last_entries = [e for e in experiments if claim_id in (e.get("claim_ids") or [])]
        last = last_entries[-1] if last_entries else None
        claims[claim_id] = {
            "title": cfg.get("title"),
            "registry_status": cfg.get("status"),
            "effective_status": effective_status,
            "owner_lanes": cfg.get("owner_lanes") or [],
            "next_gate": cfg.get("next_gate"),
            "product_capability": cfg.get("product_capability"),
            "total_experiments": global_total_counts[claim_id],
            "recent_experiments": global_recent_counts[claim_id],
            "last_experiment_id": last.get("experiment_id") if last else None,
            "last_experiment_at": last.get("created_at") if last else None,
            "last_decision": last.get("decision") if last else None,
        }

    starved_claims = [
        claim_id
        for claim_id, c in claims.items()
        if c["recent_experiments"] == 0 and c["effective_status"] not in CLOSED_STATUSES
    ]

    lanes: dict[str, dict] = {}
    for lane, cfg in lane_registry.items():
        ref = f"origin/lab2/{lane}"
        state = git_show_json(ref, f"research/lanes/{lane}/state.json")
        lane_entries = [e for e in experiments if e.get("lane") == lane]
        lane_entries.sort(key=created_key)
        history = lane_entries[-args.lane_history :]
        last_claim, streak = claim_streak(lane_entries)
        last_ten = lane_entries[-10:]
        dominant_recent_claim = None
        dominant_recent_count = 0
        if last_ten:
            counts: dict[str, int] = {}
            for e in last_ten:
                for claim_id in e.get("claim_ids") or []:
                    counts[claim_id] = counts.get(claim_id, 0) + 1
            if counts:
                dominant_recent_claim, dominant_recent_count = max(
                    counts.items(), key=lambda kv: (kv[1], kv[0])
                )
        tunnel = streak >= 5 or dominant_recent_count >= 8

        active_id = state.get("active_experiment_id")
        active_stage = "IDLE"
        active_has_portfolio_mandate = False
        if active_id:
            base = f"research/experiments/{active_id}"
            req = git_show_json(ref, f"{base}/request.json")
            active_has_portfolio_mandate = isinstance(req.get("portfolio_allocation"), dict)
            if git_file_exists(ref, f"{base}/verdict.json"):
                active_stage = "FINALIZED"
            elif git_file_exists(ref, f"{base}/audit.json"):
                active_stage = "AUDITED"
            elif git_file_exists(ref, f"{base}/result.json"):
                active_stage = "EXECUTED"
            elif git_file_exists(ref, f"{base}/freeze.json"):
                active_stage = "FROZEN"
            elif git_file_exists(ref, f"{base}/request.json"):
                active_stage = "PREFREEZE"
            else:
                active_stage = "BROKEN_REFERENCE"

        priority = cfg.get("priority_claims") or []
        lane_recent_counts = {
            claim_id: sum(claim_id in (e.get("claim_ids") or []) for e in history)
            for claim_id in priority
        }
        neglected_priority = sorted(
            priority,
            key=lambda claim_id: (
                global_recent_counts.get(claim_id, 0),
                lane_recent_counts.get(claim_id, 0),
                global_total_counts.get(claim_id, 0),
                claim_id,
            ),
        )

        state_last_id = state.get("last_experiment_id")
        state_last_quarantine = quarantine_by_id.get(state_last_id)
        canonical_last = lane_entries[-1] if lane_entries else None
        canonical_last_id = canonical_last.get("experiment_id") if canonical_last else None
        canonical_last_decision = canonical_last.get("decision") if canonical_last else None

        lanes[lane] = {
            "mission": cfg.get("mission"),
            "priority_claims": priority,
            "active_experiment_id": active_id,
            "active_stage": active_stage,
            "active_has_portfolio_mandate": active_has_portfolio_mandate,
            "last_failure_retryable": state.get("last_failure_retryable"),
            "same_failure_count": state.get("same_failure_count", 0),
            # Direction must reason from accepted evidence. Preserve the lane's
            # raw operational pointer separately when it points at quarantine.
            "last_experiment_id": canonical_last_id,
            "last_verdict": canonical_last_decision,
            "lane_state_last_experiment_id": state_last_id,
            "lane_state_last_quarantined": bool(state_last_quarantine),
            "lane_state_last_quarantine_reason": (
                state_last_quarantine.get("error") if state_last_quarantine else None
            ),
            "parent_handoff_proposal": (
                None if state_last_quarantine else state.get("next_question")
            ),
            "continue_requested": bool(state.get("continue_immediately", False)),
            "last_claim": last_claim,
            "claim_streak": streak,
            "dominant_recent_claim": dominant_recent_claim,
            "dominant_recent_count_last10": dominant_recent_count,
            "tunnel_flag": tunnel,
            "neglected_priority_claims": neglected_priority,
            "recent_claim_counts": lane_recent_counts,
            "recent_experiments": [compact_experiment(e) for e in history],
        }

    snapshot = {
        "schema_version": 1,
        "cycle_id": str(args.cycle_id),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reset_question": (
            "If SPIDER were discovered today with all accepted evidence, "
            "what should receive the next unit of research attention?"
        ),
        "global": {
            "canonical_experiments": len(experiments),
            "quarantined_experiments": len(quarantine_by_id),
            "recent_window": args.recent_window,
            "recent_experiments": len(recent_global),
            "starved_claims": starved_claims,
            "claim_recent_counts": global_recent_counts,
        },
        "claims": claims,
        "lanes": lanes,
    }

    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "SPIDER_PORTFOLIO_SNAPSHOT "
        f"cycle={args.cycle_id} experiments={len(experiments)} "
        f"starved={len(starved_claims)} tunnels="
        f"{sum(1 for x in lanes.values() if x['tunnel_flag'])}"
    )


if __name__ == "__main__":
    main()
