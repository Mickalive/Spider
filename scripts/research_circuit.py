#!/usr/bin/env python3
"""Conservative lane backoff driven by durable lane state and control revision.

Non-retryable repeated failures park until a control-plane change.
Retryable repeated failures receive a time-limited circuit (default six hours).
A fresh control revision permits a new bounded probe; state is never rewritten.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def circuit_decision(state: dict, control_revision: str, now: datetime | None = None,
                     threshold: int = 3, cooldown_hours: int = 24) -> tuple[bool, str]:
    if int(state.get("same_failure_count") or 0) < threshold:
        return False, "below repeated-failure threshold"
    if state.get("last_failure_control_revision") != control_revision:
        return False, "control-plane changed; bounded probe allowed"
    if state.get("last_failure_retryable") is False:
        return True, "repeated non-retryable failure; requires control-plane repair"
    if state.get("last_failure_retryable") is not True:
        return True, "repeated failure with unknown retryability"
    now = now or datetime.now(timezone.utc)
    try:
        failure_time = parse_utc(state["updated_at"])
    except (KeyError, ValueError, TypeError):
        return True, "repeated provider failure with missing/invalid timestamp"
    if now < failure_time + timedelta(hours=cooldown_hours):
        return True, "transient provider pool exhausted; cooldown active"
    return False, "cooldown elapsed; single bounded probe allowed"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-json", required=True)
    parser.add_argument("--control-rev", required=True)
    parser.add_argument("--threshold", type=int, default=3)
    parser.add_argument("--cooldown-hours", type=int, default=24)
    args = parser.parse_args()
    if args.threshold < 1 or args.cooldown_hours < 1:
        parser.error("threshold and cooldown-hours must be positive")
    open_, reason = circuit_decision(
        json.loads(args.state_json),
        args.control_rev,
        threshold=args.threshold,
        cooldown_hours=args.cooldown_hours,
    )
    print(("OPEN" if open_ else "CLOSED") + ": " + reason)


if __name__ == "__main__":
    main()
