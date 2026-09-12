#!/usr/bin/env python3
"""
EXP-GRAPH-34711403174 — Freshness Detection via Postcondition Similarity
Execute frozen experiment: mock server with drift injection, Jaccard similarity detection.
"""

import json
import http.server
import threading
import time
import urllib.request
import math
import hashlib
import sys
import os
from pathlib import Path

# --- Configuration ---
REQUESTS_PER_FAMILY = 10
DRIFT_POINT = 6  # drift occurs at request 6 (1-indexed), i.e. the 6th request
THRESHOLD = 0.85
SENSITIVITY_THRESHOLDS = [0.7, 0.8, 0.85, 0.9, 0.95]

# --- Resource Families ---

# Pre-drift (fresh) postconditions: sets of (field_path, type) pairs
FRESH_POSTCONDITIONS = {
    "users": {("id", "integer"), ("name", "string"), ("email", "string")},
    "posts": {("id", "integer"), ("title", "string"), ("body", "string"), ("userId", "integer")},
    "comments": {("id", "integer"), ("postId", "integer"), ("author", "string"), ("text", "string")},
    "users_stable": {("id", "integer"), ("name", "string"), ("email", "string")},
}

# Drifted (stale) postconditions
STALE_POSTCONDITIONS = {
    "users": {("id", "integer"), ("name", "string"), ("email", "string"), ("phone", "string")},  # add field
    "posts": {("id", "string"), ("title", "string"), ("body", "string"), ("userId", "integer")},  # change type
    "comments": {("id", "integer"), ("postId", "integer"), ("text", "string")},  # remove field
}

# Mock response templates
FRESH_RESPONSES = {
    "users": lambda rid: {"id": rid, "name": f"User {rid}", "email": f"user{rid}@example.com"},
    "posts": lambda rid: {"id": rid, "title": f"Post {rid}", "body": f"Body of post {rid}", "userId": rid % 10 + 1},
    "comments": lambda rid: {"id": rid, "postId": rid % 20 + 1, "author": f"Author {rid}", "text": f"Comment {rid}"},
    "users_stable": lambda rid: {"id": rid, "name": f"User {rid}", "email": f"user{rid}@example.com"},
}

STALE_RESPONSES = {
    "users": lambda rid: {"id": rid, "name": f"User {rid}", "email": f"user{rid}@example.com", "phone": f"555-{rid:04d}"},  # add field
    "posts": lambda rid: {"id": str(rid), "title": f"Post {rid}", "body": f"Body of post {rid}", "userId": rid % 10 + 1},  # change type id int->str
    "comments": lambda rid: {"id": rid, "postId": rid % 20 + 1, "text": f"Comment {rid}"},  # remove author
}


class DriftMockHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler with drift injection per resource family."""

    request_counts = {}  # family -> count
    lock = threading.Lock()

    def do_GET(self):
        path = self.path.strip("/")
        parts = path.split("/")
        if len(parts) == 2 and parts[0] in ("users", "posts", "comments", "users_stable"):
            family = parts[0]
            try:
                rid = int(parts[1])
            except ValueError:
                self.send_error(400)
                return

            with DriftMockHandler.lock:
                count = DriftMockHandler.request_counts.get(family, 0) + 1
                DriftMockHandler.request_counts[family] = count

            # Drift at request 6+ (only for drift families, not stable control)
            if count >= DRIFT_POINT and family in STALE_RESPONSES:
                response_data = STALE_RESPONSES[family](rid)
                ground_truth = "stale"
            else:
                response_data = FRESH_RESPONSES[family](rid)
                ground_truth = "fresh"

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            body = json.dumps(response_data).encode()
            self.wfile.write(body)

            # Log to raw evidence
            log_entry = {
                "family": family,
                "request_number": count,
                "url": self.path,
                "response": response_data,
                "ground_truth": ground_truth,
            }
            RawEvidence.log(log_entry)

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # suppress server logs


class RawEvidence:
    """Thread-safe raw evidence logger."""
    entries = []
    lock = threading.Lock()

    @classmethod
    def log(cls, entry):
        with cls.lock:
            cls.entries.append(entry)

    @classmethod
    def get_entries(cls):
        with cls.lock:
            return list(cls.entries)


TYPE_MAP = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "NoneType": "null",
    "list": "array",
    "dict": "object",
}


def normalize_type(python_type_name):
    """Map Python type names to schema-style type names."""
    return TYPE_MAP.get(python_type_name, python_type_name)


def extract_field_types(obj, prefix=""):
    """Extract set of (field_path, type) pairs from a JSON object."""
    pairs = set()
    if isinstance(obj, dict):
        for key, val in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(val, dict):
                pairs.update(extract_field_types(val, path))
            elif isinstance(val, list):
                pairs.add((path, "array"))
            else:
                pairs.add((path, normalize_type(type(val).__name__)))
    elif isinstance(obj, list):
        pairs.add((prefix, "array"))
    else:
        pairs.add((prefix, normalize_type(type(obj).__name__)))
    return pairs


def jaccard_similarity(set_a, set_b):
    """Compute Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def wilson_ci(successes, n, z=1.96):
    """Wilson score interval for a proportion."""
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return (max(0, center - margin), min(1, center + margin))


def run_experiment():
    """Execute the full experiment."""
    # Reset state
    DriftMockHandler.request_counts = {}
    RawEvidence.entries = []

    # Start mock server
    server = http.server.HTTPServer(("127.0.0.1", 0), DriftMockHandler)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.2)  # let server start

    print(f"Mock server started on port {port}")

    families = ["users", "posts", "comments", "users_stable"]
    family_labels = {
        "users": "add_field",
        "posts": "change_type",
        "comments": "remove_field",
        "users_stable": "no_drift",
    }

    # Run requests
    for family in families:
        for i in range(1, REQUESTS_PER_FAMILY + 1):
            url = f"http://127.0.0.1:{port}/{family}/{i}"
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
            except Exception as e:
                print(f"ERROR: {family} request {i}: {e}")
                RawEvidence.log({
                    "family": family,
                    "request_number": i,
                    "url": url,
                    "response": None,
                    "ground_truth": "error",
                    "error": str(e),
                })

    server.shutdown()

    # Compute freshness scores and detection decisions
    entries = RawEvidence.get_entries()
    results = []

    for entry in entries:
        family = entry["family"]
        req_num = entry["request_number"]
        response = entry["response"]
        ground_truth = entry["ground_truth"]

        if response is None:
            results.append({
                "family": family,
                "family_pattern": family_labels[family],
                "request_number": req_num,
                "ground_truth": ground_truth,
                "similarity": None,
                "detected_stale": None,
                "correct": None,
                "error": entry.get("error"),
            })
            continue

        actual_fields = extract_field_types(response)
        cached_fields = FRESH_POSTCONDITIONS[family]
        similarity = jaccard_similarity(cached_fields, actual_fields)
        detected_stale = similarity < THRESHOLD

        # Ground truth: "stale" means drift has occurred (req >= 6 for drift families)
        is_stale = ground_truth == "stale"
        correct = detected_stale == is_stale

        results.append({
            "family": family,
            "family_pattern": family_labels[family],
            "request_number": req_num,
            "ground_truth": ground_truth,
            "actual_fields": sorted([list(p) for p in actual_fields]),
            "cached_fields": sorted([list(p) for p in cached_fields]),
            "similarity": round(similarity, 4),
            "detected_stale": detected_stale,
            "correct": correct,
        })

    return results


def compute_metrics(results):
    """Compute all metrics from experiment results."""
    # Separate drift families from control
    drift_families = ["users", "posts", "comments"]
    control_family = "users_stable"

    # Primary metrics: TP rate across drift families, FP rate on control
    tp_total = 0
    fn_total = 0
    fp_total = 0
    tn_total = 0

    per_family = {}
    per_pattern = {}

    for r in results:
        if r.get("error"):
            continue
        family = r["family"]
        is_stale = r["ground_truth"] == "stale"
        detected = r["detected_stale"]

        if family not in per_family:
            per_family[family] = {"tp": 0, "fp": 0, "tn": 0, "fn": 0, "total": 0}
        per_family[family]["total"] += 1

        if is_stale and detected:
            tp_total += 1
            per_family[family]["tp"] += 1
        elif is_stale and not detected:
            fn_total += 1
            per_family[family]["fn"] += 1
        elif not is_stale and detected:
            fp_total += 1
            per_family[family]["fp"] += 1
        elif not is_stale and not detected:
            tn_total += 1
            per_family[family]["tn"] += 1

    # TP rate = TP / (TP + FN) across drift families
    drift_tp = sum(per_family[f]["tp"] for f in drift_families)
    drift_fn = sum(per_family[f]["fn"] for f in drift_families)
    drift_total = drift_tp + drift_fn
    tp_rate = drift_tp / drift_total if drift_total > 0 else 0.0

    # FP rate = FP / (FP + TN) on control
    ctrl = per_family.get(control_family, {"fp": 0, "tn": 0})
    fp_total_ctrl = ctrl["fp"]
    tn_total_ctrl = ctrl["tn"]
    fp_rate = fp_total_ctrl / (fp_total_ctrl + tn_total_ctrl) if (fp_total_ctrl + tn_total_ctrl) > 0 else 0.0

    # Per-family TP rates
    per_family_tp = {}
    for f in drift_families:
        pf = per_family.get(f, {"tp": 0, "fn": 0})
        total = pf["tp"] + pf["fn"]
        per_family_tp[f] = pf["tp"] / total if total > 0 else 0.0

    # Per-pattern TP rates
    pattern_map = {
        "users": "add_field",
        "posts": "change_type",
        "comments": "remove_field",
    }
    per_pattern_tp = {pattern_map[f]: per_family_tp[f] for f in drift_families}

    # Sensitivity analysis
    sensitivity = {}
    all_stale_results = [r for r in results if r["ground_truth"] == "stale" and r.get("similarity") is not None]
    all_fresh_results = [r for r in results if r["ground_truth"] == "fresh" and r.get("similarity") is not None]

    for thresh in SENSITIVITY_THRESHOLDS:
        s_tp = sum(1 for r in all_stale_results if r["similarity"] < thresh)
        s_fp = sum(1 for r in all_fresh_results if r["similarity"] < thresh)
        s_tp_rate = s_tp / len(all_stale_results) if all_stale_results else 0.0
        s_fp_rate = s_fp / len(all_fresh_results) if all_fresh_results else 0.0
        sensitivity[str(thresh)] = {
            "threshold": thresh,
            "tp_rate": round(s_tp_rate, 4),
            "fp_rate": round(s_fp_rate, 4),
        }

    # Wilson CIs
    tp_ci = wilson_ci(drift_tp, drift_total) if drift_total > 0 else (0.0, 1.0)
    fp_ci = wilson_ci(fp_total_ctrl, fp_total_ctrl + tn_total_ctrl) if (fp_total_ctrl + tn_total_ctrl) > 0 else (0.0, 1.0)

    # Similarity distributions
    fresh_sims = [r["similarity"] for r in all_fresh_results]
    stale_sims = [r["similarity"] for r in all_stale_results]

    metrics = {
        "true_positive_rate": round(tp_rate, 4),
        "false_positive_rate": round(fp_rate, 4),
        "tp_rate_95ci": [round(tp_ci[0], 4), round(tp_ci[1], 4)],
        "fp_rate_95ci": [round(fp_ci[0], 4), round(fp_ci[1], 4)],
        "per_family_tp_rate": {k: round(v, 4) for k, v in per_family_tp.items()},
        "per_pattern_tp_rate": {k: round(v, 4) for k, v in per_pattern_tp.items()},
        "confusion_matrix": {
            "tp": drift_tp,
            "fn": drift_fn,
            "fp": fp_total_ctrl,
            "tn": tn_total_ctrl,
        },
        "sensitivity_analysis": sensitivity,
        "similarity_distributions": {
            "fresh": {
                "values": [round(s, 4) for s in fresh_sims],
                "mean": round(sum(fresh_sims) / len(fresh_sims), 4) if fresh_sims else None,
                "min": round(min(fresh_sims), 4) if fresh_sims else None,
                "max": round(max(fresh_sims), 4) if fresh_sims else None,
            },
            "stale": {
                "values": [round(s, 4) for s in stale_sims],
                "mean": round(sum(stale_sims) / len(stale_sims), 4) if stale_sims else None,
                "min": round(min(stale_sims), 4) if stale_sims else None,
                "max": round(max(stale_sims), 4) if stale_sims else None,
            },
        },
        "total_requests": len([r for r in results if not r.get("error")]),
        "failed_requests": len([r for r in results if r.get("error")]),
        "threshold_used": THRESHOLD,
    }

    return metrics


def evaluate_decision(metrics):
    """Apply frozen decision rule."""
    tp_rate = metrics["true_positive_rate"]
    fp_rate = metrics["false_positive_rate"]
    per_family_tp = metrics["per_family_tp_rate"]
    failed = metrics["failed_requests"]

    # MEASUREMENT_INVALID conditions
    if failed > 0:
        return "MEASUREMENT_INVALID", "Mock server or request failures detected"

    # SURVIVES_CURRENT_TEST conditions (all must hold)
    conditions_survive = [
        tp_rate >= 0.8,
        fp_rate <= 0.1,
        all(v > 0.7 for v in per_family_tp.values()),
    ]

    if all(conditions_survive):
        return "SURVIVES_CURRENT_TEST", "All decision rule conditions met"

    # FALSIFIED-IN-SETTING
    reasons = []
    if tp_rate < 0.8:
        reasons.append(f"TP rate {tp_rate} < 0.8")
    if fp_rate > 0.1:
        reasons.append(f"FP rate {fp_rate} > 0.1")
    for fam, rate in per_family_tp.items():
        if rate <= 0.7:
            reasons.append(f"Per-family TP {fam}={rate} <= 0.7")

    return "FALSIFIED-IN-SETTING", "; ".join(reasons)


def main():
    print("=== EXP-GRAPH-34711403174: Freshness Detection Experiment ===")
    print(f"Threshold: {THRESHOLD}, Requests per family: {REQUESTS_PER_FAMILY}")
    print(f"Drift point: request {DRIFT_POINT}")
    print()

    # Run experiment
    results = run_experiment()
    print(f"\nCompleted {len(results)} requests")

    # Compute metrics
    metrics = compute_metrics(results)

    # Evaluate decision
    decision, reason = evaluate_decision(metrics)
    print(f"\nDecision: {decision}")
    print(f"Reason: {reason}")
    print(f"TP rate: {metrics['true_positive_rate']}, FP rate: {metrics['false_positive_rate']}")
    print(f"Per-family TP: {metrics['per_family_tp_rate']}")

    # Save raw evidence
    raw_path = Path(__file__).parent.parent.parent / "experiments" / "EXP-GRAPH-34711403174" / "raw_evidence"
    raw_path.mkdir(parents=True, exist_ok=True)

    with open(raw_path / "execution_results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open(raw_path / "request_logs.json", "w") as f:
        json.dump(RawEvidence.get_entries(), f, indent=2)

    with open(raw_path / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    with open(raw_path / "decision.json", "w") as f:
        json.dump({"decision": decision, "reason": reason}, f, indent=2)

    print(f"\nRaw evidence saved to {raw_path}")
    print("=== Experiment Complete ===")


if __name__ == "__main__":
    main()
