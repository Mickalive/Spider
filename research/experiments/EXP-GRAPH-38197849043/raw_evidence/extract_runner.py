#!/usr/bin/env python3
"""EXECUTE helper: extract the frozen runner from the frozen prereg.md.

The frozen prereg (prereg.md section 11/12) specifies that EXECUTE extracts the
block delimited by the FROZEN-RUNNER begin/end HTML comment markers (captured
group) to raw_evidence/runner_delta_repair.py and verifies it against
CANONICAL-RUNNER-SHA256. This helper performs exactly that extraction and fails
loudly if the hash does not match, so the frozen executable path is bound.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP = ROOT / "research/experiments/EXP-GRAPH-38197849043"
PREREG = EXP / "prereg.md"
OUT = EXP / "raw_evidence" / "runner_delta_repair.py"
CANONICAL = "0322d92cfbc1314437a92eb0cdfeac43a8ecd3c5cdd520bae0a443c8d669eed1"

BEGIN = "<!-- BEGIN FROZEN-RUNNER -->"
END = "<!-- END FROZEN-RUNNER -->"


def main() -> int:
    text = PREREG.read_text(encoding="utf-8")
    m = re.search(re.escape(BEGIN) + r"\n(.*?)" + re.escape(END), text, re.S)
    if m is None:
        print("FATAL: FROZEN-RUNNER markers not found", file=sys.stderr)
        return 2
    runner = m.group(1)
    sha = hashlib.sha256(runner.encode()).hexdigest()
    if sha != CANONICAL:
        print(f"FATAL: extracted runner sha256 {sha} != canonical {CANONICAL}",
              file=sys.stderr)
        return 3
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(runner, encoding="utf-8")
    print(f"OK extracted {len(runner)} bytes; sha256={sha} (matches CANONICAL-RUNNER-SHA256)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
