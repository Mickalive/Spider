#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_circuit import circuit_decision


def run():
    now = datetime(2026, 10, 11, tzinfo=timezone.utc)
    base = dict(same_failure_count=6, last_failure_control_revision="rev-a",
                last_failure_retryable=False, updated_at=now.isoformat())
    assert circuit_decision(base, "rev-a", now)[0] is True
    assert circuit_decision(base, "rev-b", now)[0] is False
    assert circuit_decision({**base, "same_failure_count": 2}, "rev-a", now)[0] is False
    transient = {**base, "last_failure_retryable": True}
    assert circuit_decision(transient, "rev-a", now)[0] is True
    assert circuit_decision(transient, "rev-a", now + timedelta(hours=6, minutes=1))[0] is False
    assert circuit_decision({**transient, "updated_at": "invalid"}, "rev-a", now)[0] is True
    assert circuit_decision({**transient, "last_failure_retryable": None}, "rev-a", now)[0] is True
    print("SPIDER_RESEARCH_CIRCUIT_TEST_OK")


if __name__ == "__main__":
    run()
