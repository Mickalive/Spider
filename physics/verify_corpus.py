"""Corpus integrity verification for WP-003B-v2 (representation integrity §17).

For every usable row:
  1. reload the preserved raw pre/post DOM snapshots;
  2. recompute sha256 digest names;
  3. recompute derived features + raw counts from raw observables and compare
     to what the collector recorded (catches silent derivation drift);
  4. check trajectory chaining: contiguous step_id, prev_action_label ==
     primary_action(t-1), "<START>" at step 0.

Writes a compact verification record to results/physics/.
"""
import gzip
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from physics.collector import features, counts_of
from physics.run_wp003 import FEATURES

IN = os.environ.get("CORPUS", "/tmp/opencode/spider_data/wp003b_v2_transitions.jsonl")
RAW_DIR = "/tmp/opencode/spider_data/raw"
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "physics",
                   "wp003b_v2_corpus_verification.json")


def load_raw(digest):
    p = os.path.join(RAW_DIR, f"{digest}.json.gz")
    if not os.path.exists(p):
        return None
    with gzip.open(p, "rt") as f:
        return json.load(f)


def main():
    rows = []
    for line in open(IN):
        line = line.strip()
        if line:
            rows.append(json.loads(line))

    n = len(rows)
    fail_digest_pre = fail_digest_post = 0
    missing_raw = 0
    fail_features_pre = fail_features_post = 0
    fail_counts_pre = fail_counts_post = 0
    examples = []

    for r in rows:
        pre = load_raw(r["pre_raw"])
        post = load_raw(r["post_raw"])
        if pre is None or post is None:
            missing_raw += 1
            continue
        hpre = hashlib.sha256(json.dumps(pre, sort_keys=True).encode()).hexdigest()[:20]
        hpost = hashlib.sha256(json.dumps(post, sort_keys=True).encode()).hexdigest()[:20]
        if hpre != r["pre_raw"]:
            fail_digest_pre += 1
        if hpost != r["post_raw"]:
            fail_digest_post += 1
        if features(pre) != r["pre"]:
            fail_features_pre += 1
            if len(examples) < 10:
                examples.append({"row": r["trajectory_id"], "issue": "pre feature mismatch"})
        elif features(post) != r["post"]:
            fail_features_post += 1
        if counts_of(pre) != r.get("counts_pre"):
            fail_counts_pre += 1
        if counts_of(post) != r.get("counts_post"):
            fail_counts_post += 1

    by_traj = defaultdict(list)
    for r in rows:
        by_traj[r["trajectory_id"]].append(r)
    chain_fail = []
    for tid, rs in by_traj.items():
        rs.sort(key=lambda x: x["step_id"])
        if rs[0]["step_id"] != 0 or rs[0]["prev_action_label"] != "<START>":
            chain_fail.append(tid)
        for prev, cur in zip(rs, rs[1:]):
            if cur["step_id"] != prev["step_id"] + 1 or \
               cur["prev_action_label"] != prev["primary_action"]:
                chain_fail.append(tid)
                break

    h = hashlib.sha256(open(IN, "rb").read()).hexdigest()
    out = {
        "corpus_file": IN,
        "corpus_sha256": h,
        "rows": n,
        "trajectories": len(by_traj),
        "per_site": dict(Counter(r["site"] for r in rows)),
        "missing_raw_snapshots": missing_raw,
        "digest_mismatch_pre": fail_digest_pre,
        "digest_mismatch_post": fail_digest_post,
        "derived_feature_mismatch_pre": fail_features_pre,
        "derived_feature_mismatch_post": fail_features_post,
        "counts_mismatch_pre": fail_counts_pre,
        "counts_mismatch_post": fail_counts_post,
        "chain_violation_trajectories": len(chain_fail),
        "chain_violation_examples": chain_fail[:10],
        "examples": examples,
        "verdict": ("PASS" if (missing_raw == 0 and fail_digest_pre == 0
                               and fail_digest_post == 0
                               and fail_features_pre == 0
                               and fail_features_post == 0
                               and fail_counts_pre == 0
                               and fail_counts_post == 0
                               and not chain_fail) else "FAIL"),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
