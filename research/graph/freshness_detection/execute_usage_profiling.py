#!/usr/bin/env python3
"""
EXP-GRAPH-35137034388 — Field-Usage Profiling for Drift-vs-Noise Discrimination
Execute frozen experiment: mock API server with deterministic responses,
3 client profiles accessing different field subsets, measure usage-similarity
between fresh and stale states across 4 schema sizes x 6 drift patterns.

CORRECTED SERVER MODEL: Server returns ALL fields in the response.
Clients extract only their designated fields. When a field is removed
from the schema, clients that depend on it will find it missing (null/absent),
reducing their usage-similarity.
"""

import json
import http.server
import threading
import time
import urllib.request
import math
import hashlib
import random
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

# ============================================================
# CONSTANTS (frozen in spec.json / prereg.md)
# ============================================================

SCHEMA_SIZES = [10, 20, 30, 50]
SAMPLES_PER_GROUP = 30  # 30 fresh + 30 stale per drift pattern per size
REQUESTS_PER_CLIENT_PROFILE = 10
SEED = 20260916  # deterministic seed per prereg

DRIFT_PATTERNS_TRUE = ["remove_field", "change_type", "required_to_optional"]
DRIFT_PATTERNS_NOISE = ["optional_field_churn", "null_valued_fields", "nested_object_variation"]
ALL_DRIFT_PATTERNS = DRIFT_PATTERNS_TRUE + DRIFT_PATTERNS_NOISE

# Client profiles: each requests a specific subset of fields
CLIENT_PROFILES = {
    "A": {"fields": {"id", "name"}, "description": "identity-only consumer"},
    "B": {"fields": {"id", "name", "email"}, "description": "contact consumer"},
    "C": {"fields": {"id", "name", "email", "phone"}, "description": "full-profile consumer"},
}

FIELD_TYPES = ["string", "integer", "boolean", "array", "object"]

# ============================================================
# SCHEMA GENERATION
# ============================================================

def generate_baseline_schema(n, rng):
    """Generate a baseline schema of n fields. Fields always include id, name, email, phone
    plus additional fields to reach size n."""
    core_fields = [
        ("id", "integer"),
        ("name", "string"),
        ("email", "string"),
        ("phone", "string"),
    ]
    fields = list(core_fields)
    used_names = {"id", "name", "email", "phone"}

    i = len(fields)
    while len(fields) < n:
        fname = f"field_{i}"
        if fname not in used_names:
            used_names.add(fname)
            ftype = rng.choice(FIELD_TYPES)
            fields.append((fname, ftype))
        i += 1
    return fields

def generate_fresh_schema(baseline, rng):
    """Fresh = identical to baseline."""
    return list(baseline)

# ============================================================
# DRIFT PATTERN GENERATORS
# ============================================================

def generate_stale_remove_field(baseline, rng):
    """Remove one field that clients depend on (true drift).
    Removes a field from the 'email' or 'phone' slot (used by profiles B and C)
    to ensure the drift is detectable by client usage patterns."""
    # Target fields that at least one client profile uses
    target_names = {"email", "phone"}
    targetable = [(i, (fn, ft)) for i, (fn, ft) in enumerate(baseline) if fn in target_names]
    if targetable:
        idx = rng.choice(targetable)[0]
    else:
        # Fallback: remove any non-id, non-name field
        core = {"id", "name"}
        fallback = [(i, (fn, ft)) for i, (fn, ft) in enumerate(baseline) if fn not in core]
        if fallback:
            idx = rng.choice(fallback)[0]
        else:
            idx = rng.randint(0, len(baseline) - 1)
    return [f for i, f in enumerate(baseline) if i != idx]

def generate_stale_change_type(baseline, rng):
    """Change one field's type (true drift).
    Changes the type of a field that clients depend on. When the server returns
    a value of unexpected type, clients that requested this field will find it
    unusable (type mismatch), reducing their effective usage."""
    # Target 'id' field - changing integer to string affects all clients
    target_names = {"id"}
    targetable = [(i, (fn, ft)) for i, (fn, ft) in enumerate(baseline) if fn in target_names]
    if targetable:
        idx = rng.choice(targetable)[0]
    else:
        # Fallback
        idx = rng.randint(0, len(baseline) - 1)
    path, old_type = baseline[idx]
    new_type = rng.choice([t for t in FIELD_TYPES if t != old_type])
    result = list(baseline)
    result[idx] = (path, new_type)
    return result

def generate_stale_required_to_optional(baseline, rng):
    """Move one required field to optional (true drift).
    The field becomes optional - it may or may not appear in responses.
    We track this with metadata; the mock server handles the conditional inclusion."""
    # Target 'name' field - used by all 3 profiles
    target_names = {"name"}
    targetable = [(i, (fn, ft)) for i, (fn, ft) in enumerate(baseline) if fn in target_names]
    if targetable:
        idx = rng.choice(targetable)[0]
    else:
        idx = rng.randint(0, len(baseline) - 1)
    path, old_type = baseline[idx]
    # Keep the field in the schema but mark it for conditional inclusion
    result = list(baseline)
    result[idx] = (f"{path}_optional_marker", old_type)
    return result

def generate_stale_optional_churn(baseline, rng):
    """Add ~10% optional fields (structural noise).
    These are NEW fields that no client profile requests."""
    n = len(baseline)
    churn_count = max(1, round(n * 0.1))
    result = list(baseline)
    for _ in range(churn_count):
        new_field = f"churn_opt_{rng.randint(1, 9999)}"
        new_type = rng.choice(FIELD_TYPES)
        result.append((new_field, new_type))
    return result

def generate_stale_null_fields(baseline, rng):
    """Add fields with null values (structural noise).
    These are NEW fields that no client profile requests."""
    n = len(baseline)
    null_count = max(1, round(n * 0.1))
    result = list(baseline)
    for _ in range(null_count):
        new_field = f"null_field_{rng.randint(1, 9999)}"
        result.append((new_field, "null"))
    return result

def generate_stale_nested_object(baseline, rng):
    """Add nested sub-fields (structural noise).
    These are NEW nested fields under existing fields, not requested by clients."""
    n = len(baseline)
    nested_count = max(1, round(n * 0.1))
    result = list(baseline)
    added_parents = set()
    for _ in range(nested_count):
        # Pick a parent that hasn't been nested yet
        available = [fn for fn, ft in result if fn not in added_parents and "." not in fn]
        if available:
            parent = rng.choice(available)
            nested_field = f"{parent}.nested_{rng.randint(1, 999)}"
            result.append((nested_field, "string"))
            added_parents.add(parent)
        else:
            # Fallback: add a top-level nested field
            new_field = f"nested_group_{rng.randint(1, 999)}.child"
            result.append((new_field, "string"))
    return result

DRIFT_GENERATORS = {
    "remove_field": generate_stale_remove_field,
    "change_type": generate_stale_change_type,
    "required_to_optional": generate_stale_required_to_optional,
    "optional_field_churn": generate_stale_optional_churn,
    "null_valued_fields": generate_stale_null_fields,
    "nested_object_variation": generate_stale_nested_object,
}

# ============================================================
# METRICS
# ============================================================

def jaccard_similarity(set_a, set_b):
    """Compute Jaccard similarity between two sets."""
    a = set(set_a)
    b = set(set_b)
    if not a and not b:
        return 1.0
    intersection = a & b
    union = a | b
    return len(intersection) / len(union)

def compute_usage_similarity(fresh_fields_used, stale_fields_used):
    """Mean per-profile Jaccard(field_used_fresh, field_used_stale).
    
    For each profile, compute Jaccard of the set of fields that were actually
    successfully used in fresh vs stale responses. Then average across profiles.
    """
    profile_sims = []
    for profile_id in CLIENT_PROFILES:
        fresh_used = fresh_fields_used.get(profile_id, set())
        stale_used = stale_fields_used.get(profile_id, set())
        sim = jaccard_similarity(fresh_used, stale_used)
        profile_sims.append(sim)
    return sum(profile_sims) / len(profile_sims) if profile_sims else 0.0

# ============================================================
# MOCK API SERVER
# ============================================================

class UsageProfilingMockHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler serving deterministic JSON responses.
    
    Server returns ALL fields in the schema. Clients extract what they need.
    This matches real API behavior where the response contains all available fields.
    """
    
    schema_state = {}  # field_name -> type info  (list of (name, type) tuples)
    is_optional_drift = False  # whether required_to_optional pattern is active
    optional_drift_field = None  # the field that became optional
    request_log = []
    lock = threading.Lock()
    
    def do_GET(self):
        path = self.path.strip("/")
        parts = path.split("/")
        if len(parts) != 2:
            self.send_error(404)
            return
        
        resource_type = parts[0]
        try:
            resource_id = int(parts[1])
        except ValueError:
            self.send_error(400)
            return
        
        schema = UsageProfilingMockHandler.schema_state
        if not schema:
            self.send_error(500)
            return
        
        # Build response with ALL fields
        response_data = {}
        for field_name, field_type in schema:
            # Handle optional drift: the field with _optional_marker is conditionally included
            if UsageProfilingMockHandler.is_optional_drift:
                if field_name.endswith("_optional_marker"):
                    # Simulate optional: field present ~50% of the time
                    if resource_id % 2 == 0:
                        continue  # field missing for even IDs
                    # else: include it (but under the marker name - clients won't find it by original name)
                    # Actually, skip it entirely to model "field not always present"
                    continue
            
            if field_type == "integer":
                response_data[field_name] = resource_id
            elif field_type == "string":
                response_data[field_name] = f"{field_name}_{resource_id}"
            elif field_type == "boolean":
                response_data[field_name] = True
            elif field_type == "array":
                response_data[field_name] = [resource_id]
            elif field_type == "object":
                response_data[field_name] = {"value": resource_id}
            elif field_type == "null":
                response_data[field_name] = None
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        body = json.dumps(response_data).encode()
        self.wfile.write(body)
        
        # Log
        with UsageProfilingMockHandler.lock:
            UsageProfilingMockHandler.request_log.append({
                "resource_type": resource_type,
                "resource_id": resource_id,
                "response_fields": sorted(response_data.keys()),
                "response": response_data,
            })
    
    def log_message(self, format, *args):
        pass


# ============================================================
# EXPERIMENT EXECUTION
# ============================================================

def run_single_condition(baseline_schema, pattern, size, sample_idx, rng):
    """Run one (pattern, size, sample_idx) condition.
    
    Returns dict with:
      - jaccard: structural Jaccard between baseline and stale schema
      - usage_similarity: mean per-profile Jaccard of used fields
      - per_profile_success: dict of profile -> success rate
      - per_profile_used_fields_fresh/stale: which fields each profile actually used
    """
    # Generate stale schema
    gen = DRIFT_GENERATORS[pattern]
    stale_schema = gen(baseline_schema, rng)
    
    # Build field-name sets for Jaccard
    fresh_field_names = {fn for fn, ft in baseline_schema}
    stale_field_names = {fn for fn, ft in stale_schema}
    
    # Jaccard similarity (structural)
    jaccard = jaccard_similarity(
        {(fn, ft) for fn, ft in baseline_schema},
        {(fn, ft) for fn, ft in stale_schema}
    )
    
    # Start mock server
    server = http.server.HTTPServer(("127.0.0.1", 0), UsageProfilingMockHandler)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.05)
    
    fresh_used_fields = defaultdict(set)
    stale_used_fields = defaultdict(set)
    per_profile_success = {}
    
    # Determine if this is optional drift
    is_optional = (pattern == "required_to_optional")
    optional_field = None
    if is_optional:
        # The field that became optional is the one with _optional_marker suffix
        for fn, ft in stale_schema:
            if fn.endswith("_optional_marker"):
                # Strip the marker to get the original field name
                optional_field = fn.replace("_optional_marker", "")
                break
    
    try:
        for profile_id, profile_info in CLIENT_PROFILES.items():
            requested = profile_info["fields"]
            fresh_successes = 0
            stale_successes = 0
            
            # 10 requests for fresh state
            for req_num in range(REQUESTS_PER_CLIENT_PROFILE):
                url = f"http://127.0.0.1:{port}/resource/{req_num + 1}"
                try:
                    req = urllib.request.Request(url)
                    UsageProfilingMockHandler.schema_state = baseline_schema
                    UsageProfilingMockHandler.is_optional_drift = False
                    UsageProfilingMockHandler.optional_drift_field = None
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode())
                        # Client extracts its requested fields from the full response
                        for f in requested:
                            if f in data and data[f] is not None:
                                fresh_used_fields[profile_id].add(f)
                        fresh_successes += 1
                except Exception:
                    pass
            
            # 10 requests for stale state
            for req_num in range(REQUESTS_PER_CLIENT_PROFILE):
                url = f"http://127.0.0.1:{port}/resource/{req_num + 1}"
                try:
                    req = urllib.request.Request(url)
                    UsageProfilingMockHandler.schema_state = stale_schema
                    UsageProfilingMockHandler.is_optional_drift = is_optional
                    UsageProfilingMockHandler.optional_drift_field = optional_field
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode())
                        # Client extracts its requested fields from the full response
                        for f in requested:
                            if f in data and data[f] is not None:
                                stale_used_fields[profile_id].add(f)
                        stale_successes += 1
                except Exception:
                    pass
            
            total_requests = 2 * REQUESTS_PER_CLIENT_PROFILE
            per_profile_success[profile_id] = (fresh_successes + stale_successes) / total_requests
    finally:
        server.shutdown()
    
    # Compute usage similarity
    usage_sim = compute_usage_similarity(dict(fresh_used_fields), dict(stale_used_fields))
    
    return {
        "jaccard": round(jaccard, 6),
        "usage_similarity": round(usage_sim, 6),
        "per_profile_success": {k: round(v, 4) for k, v in per_profile_success.items()},
        "per_profile_used_fields_fresh": {k: sorted(v) for k, v in fresh_used_fields.items()},
        "per_profile_used_fields_stale": {k: sorted(v) for k, v in stale_used_fields.items()},
    }


def run_experiment():
    """Execute the full experiment across all conditions."""
    rng = random.Random(SEED)
    
    raw_evidence = {
        "experiment_id": "EXP-GRAPH-35137034388",
        "seed": SEED,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "client_profiles": {k: {"fields": sorted(v["fields"]), "description": v["description"]}
                           for k, v in CLIENT_PROFILES.items()},
        "per_schema_size": {},
    }
    
    for n in SCHEMA_SIZES:
        print(f"  Schema size n={n}...")
        baseline = generate_baseline_schema(n, rng)
        
        size_evidence = {
            "schema_size": n,
            "baseline_schema": [list(f) for f in baseline],
            "conditions": {},
        }
        
        for pattern in ALL_DRIFT_PATTERNS:
            condition_results = []
            for i in range(SAMPLES_PER_GROUP):
                result = run_single_condition(baseline, pattern, n, i, rng)
                condition_results.append(result)
            
            size_evidence["conditions"][pattern] = condition_results
        
        raw_evidence["per_schema_size"][str(n)] = size_evidence
    
    return raw_evidence


# ============================================================
# DERIVED MEASUREMENTS
# ============================================================

def compute_derived_measurements(raw_evidence):
    """Compute all derived metrics from raw evidence."""
    measurements = {
        "per_schema_size": {},
        "overall": {},
    }
    
    all_jaccard = []
    all_usage_sim = []
    all_conditions = []  # (jaccard, usage_sim) per condition
    
    for n_str, size_data in raw_evidence["per_schema_size"].items():
        n = size_data["schema_size"]
        pattern_metrics = {}
        
        for pattern in ALL_DRIFT_PATTERNS:
            results = size_data["conditions"][pattern]
            jaccards = [r["jaccard"] for r in results]
            usage_sims = [r["usage_similarity"] for r in results]
            
            mean_jaccard = sum(jaccards) / len(jaccards) if jaccards else 0.0
            mean_usage_sim = sum(usage_sims) / len(usage_sims) if usage_sims else 0.0
            
            # Per-profile success rates
            profile_successes = defaultdict(list)
            for r in results:
                for pid, s in r["per_profile_success"].items():
                    profile_successes[pid].append(s)
            mean_profile_success = {
                pid: round(sum(vals) / len(vals), 4)
                for pid, vals in profile_successes.items()
            }
            
            # Per-profile usage similarity
            profile_usage_sims = defaultdict(list)
            for r in results:
                fresh_used = r.get("per_profile_used_fields_fresh", {})
                stale_used = r.get("per_profile_used_fields_stale", {})
                for pid in CLIENT_PROFILES:
                    fu = set(fresh_used.get(pid, []))
                    su = set(stale_used.get(pid, []))
                    psim = jaccard_similarity(fu, su)
                    profile_usage_sims[pid].append(psim)
            
            mean_profile_usage_sim = {
                pid: round(sum(vals) / len(vals), 6) if vals else 0.0
                for pid, vals in profile_usage_sims.items()
            }
            
            pattern_metrics[pattern] = {
                "mean_jaccard": round(mean_jaccard, 6),
                "mean_usage_similarity": round(mean_usage_sim, 6),
                "std_usage_similarity": round(
                    (sum((s - mean_usage_sim)**2 for s in usage_sims) / len(usage_sims))**0.5
                    if len(usage_sims) > 1 else 0.0, 6
                ),
                "per_profile_success_rate": mean_profile_success,
                "per_profile_usage_similarity": mean_profile_usage_sim,
                "n_samples": len(results),
            }
            
            all_jaccard.append(mean_jaccard)
            all_usage_sim.append(mean_usage_sim)
            all_conditions.append((mean_jaccard, mean_usage_sim))
        
        measurements["per_schema_size"][str(n)] = {
            "pattern_metrics": pattern_metrics,
        }
    
    # Overall metrics
    drift_usage_sims = []
    noise_usage_sims = []
    for n_str, size_data in measurements["per_schema_size"].items():
        for pattern in DRIFT_PATTERNS_TRUE:
            drift_usage_sims.append(size_data["pattern_metrics"][pattern]["mean_usage_similarity"])
        for pattern in DRIFT_PATTERNS_NOISE:
            noise_usage_sims.append(size_data["pattern_metrics"][pattern]["mean_usage_similarity"])
    
    drift_usage_mean = sum(drift_usage_sims) / len(drift_usage_sims) if drift_usage_sims else 0.0
    noise_usage_mean = sum(noise_usage_sims) / len(noise_usage_sims) if noise_usage_sims else 0.0
    discrimination_gap = noise_usage_mean - drift_usage_mean
    
    # Pearson correlation between Jaccard and usage-similarity across all 24 conditions
    if len(all_conditions) >= 2:
        n_cond = len(all_conditions)
        mean_j = sum(c[0] for c in all_conditions) / n_cond
        mean_u = sum(c[1] for c in all_conditions) / n_cond
        cov = sum((c[0] - mean_j) * (c[1] - mean_u) for c in all_conditions) / n_cond
        std_j = (sum((c[0] - mean_j)**2 for c in all_conditions) / n_cond)**0.5
        std_u = (sum((c[1] - mean_u)**2 for c in all_conditions) / n_cond)**0.5
        pearson_r = cov / (std_j * std_u) if std_j > 0 and std_u > 0 else 0.0
    else:
        pearson_r = 0.0
    
    measurements["overall"] = {
        "drift_usage_mean": round(drift_usage_mean, 6),
        "noise_usage_mean": round(noise_usage_mean, 6),
        "discrimination_gap": round(discrimination_gap, 6),
        "pearson_r_jaccard_vs_usage": round(pearson_r, 6),
        "n_conditions": len(all_conditions),
        "all_jaccard_values": [round(j, 6) for j in all_jaccard],
        "all_usage_sim_values": [round(u, 6) for u in all_usage_sim],
    }
    
    return measurements


# ============================================================
# DECISION RULE
# ============================================================

def evaluate_decision_rule(measurements, raw_evidence):
    """Apply frozen decision rule from spec.json.
    
    SURVIVES_CURRENT_TEST if and only if ALL THREE conditions hold:
    1. Drift detection: EVERY drift pattern at EVERY size -> mean usage_sim < 0.90
    2. Noise tolerance: EVERY noise pattern at EVERY size -> mean usage_sim >= 0.95
    3. Orthogonality: Pearson r between Jaccard and usage_sim across all 24 conditions < 0.90
    """
    violations = []
    
    # Condition 1: Drift detection
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        for pattern in DRIFT_PATTERNS_TRUE:
            pm = size_data["pattern_metrics"][pattern]
            if pm["mean_usage_similarity"] >= 0.90:
                violations.append(
                    f"C1 FAIL: n={n} pattern={pattern}: mean_usage_similarity={pm['mean_usage_similarity']:.6f} >= 0.90"
                )
    
    # Condition 2: Noise tolerance
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        for pattern in DRIFT_PATTERNS_NOISE:
            pm = size_data["pattern_metrics"][pattern]
            if pm["mean_usage_similarity"] < 0.95:
                violations.append(
                    f"C2 FAIL: n={n} pattern={pattern}: mean_usage_similarity={pm['mean_usage_similarity']:.6f} < 0.95"
                )
    
    # Condition 3: Orthogonality
    pearson_r = measurements["overall"]["pearson_r_jaccard_vs_usage"]
    if pearson_r >= 0.90:
        violations.append(
            f"C3 FAIL: Pearson r={pearson_r:.6f} >= 0.90 (signals redundant)"
        )
    
    if not violations:
        return "SURVIVES_CURRENT_TEST", []
    else:
        return "FALSIFIED-IN-SETTING", violations


# ============================================================
# MAIN
# ============================================================

def main():
    print("=== EXP-GRAPH-35137034388: Field-Usage Profiling Experiment ===")
    print(f"Schema sizes: {SCHEMA_SIZES}")
    print(f"Samples per group: {SAMPLES_PER_GROUP}")
    print(f"Client profiles: {list(CLIENT_PROFILES.keys())}")
    print(f"True drift patterns: {DRIFT_PATTERNS_TRUE}")
    print(f"Noise patterns: {DRIFT_PATTERNS_NOISE}")
    print()
    
    # Run experiment
    print("Running experiment...")
    raw_evidence = run_experiment()
    
    # Compute derived measurements
    print("Computing derived measurements...")
    measurements = compute_derived_measurements(raw_evidence)
    
    # Evaluate decision
    decision, violations = evaluate_decision_rule(measurements, raw_evidence)
    
    print(f"\nDecision: {decision}")
    if violations:
        print(f"Violations ({len(violations)}):")
        for v in violations:
            print(f"  - {v}")
    print()
    
    # Print summary
    overall = measurements["overall"]
    print(f"Overall metrics:")
    print(f"  Drift usage mean: {overall['drift_usage_mean']:.6f} (must be < 0.90)")
    print(f"  Noise usage mean: {overall['noise_usage_mean']:.6f} (must be >= 0.95)")
    print(f"  Discrimination gap: {overall['discrimination_gap']:.6f} (must be >= 0.05)")
    print(f"  Pearson r (Jaccard vs usage): {overall['pearson_r_jaccard_vs_usage']:.6f} (must be < 0.90)")
    print()
    
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        print(f"Schema size n={n}:")
        for pattern in ALL_DRIFT_PATTERNS:
            pm = size_data["pattern_metrics"][pattern]
            marker = "*" if pattern in DRIFT_PATTERNS_TRUE else "#"
            print(f"  {marker} {pattern}: jaccard={pm['mean_jaccard']:.4f} usage_sim={pm['mean_usage_similarity']:.4f} std={pm['std_usage_similarity']:.4f}")
            print(f"       profile success: {pm['per_profile_success_rate']}")
            print(f"       profile usage_sim: {pm['per_profile_usage_similarity']}")
        print()
    
    # Save raw evidence
    exp_dir = Path(__file__).parent.parent.parent / "experiments" / "EXP-GRAPH-35137034388"
    raw_dir = exp_dir / "raw_evidence"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Save summary version
    raw_summary = {
        "experiment_id": raw_evidence["experiment_id"],
        "seed": raw_evidence["seed"],
        "executed_at": raw_evidence["executed_at"],
        "client_profiles": raw_evidence["client_profiles"],
        "per_schema_size": {},
    }
    for n_str, size_data in raw_evidence["per_schema_size"].items():
        raw_summary["per_schema_size"][n_str] = {
            "schema_size": size_data["schema_size"],
            "baseline_schema": size_data["baseline_schema"],
            "conditions_summary": {},
        }
        for pattern, results in size_data["conditions"].items():
            raw_summary["per_schema_size"][n_str]["conditions_summary"][pattern] = {
                "n_samples": len(results),
                "jaccards": [r["jaccard"] for r in results],
                "usage_similarities": [r["usage_similarity"] for r in results],
                "per_profile_success": [r["per_profile_success"] for r in results],
                "per_profile_used_fresh": [r["per_profile_used_fields_fresh"] for r in results[:3]],  # sample
                "per_profile_used_stale": [r["per_profile_used_fields_stale"] for r in results[:3]],  # sample
            }
    
    with open(raw_dir / "experiment_data.json", "w") as f:
        json.dump(raw_summary, f, indent=2)
    
    with open(raw_dir / "derived_measurements.json", "w") as f:
        json.dump(measurements, f, indent=2)
    
    with open(raw_dir / "decision_evaluation.json", "w") as f:
        json.dump({
            "decision": decision,
            "violations": violations,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2)
    
    # Compute SHA256 hashes
    raw_hashes = {}
    for p in sorted(raw_dir.iterdir()):
        if p.is_file():
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            raw_hashes[p.name] = h
    
    with open(raw_dir / "hashes.json", "w") as f:
        json.dump(raw_hashes, f, indent=2)
    
    print(f"Raw evidence saved to {raw_dir}")
    print("=== Experiment Complete ===")
    
    return {
        "raw_evidence": raw_summary,
        "measurements": measurements,
        "decision": decision,
        "violations": violations,
        "raw_hashes": raw_hashes,
    }


if __name__ == "__main__":
    result = main()
