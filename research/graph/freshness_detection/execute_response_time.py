#!/usr/bin/env python3
"""
EXP-GRAPH-35083040517 — Response-Time Profiling for Schema Drift Detection
Execute frozen experiment: mock server with controlled computation paths,
KS two-sample test on response-time distributions.
"""

import json
import http.server
import threading
import time
import urllib.request
import random
import hashlib
import sys
import os
import statistics
from pathlib import Path
from scipy import stats
import numpy as np

# === FROZEN PARAMETERS ===
SEED_FIELDGEN = 20260916
SEED_PATTERN = 20260917
SEED_JITTER = 20260918
N_REPS = 30  # requests per condition
SCHEMA_SIZES = [10, 20, 30, 50]
ALPHA = 0.05
BONFERRONI_N = 24  # 4 sizes x 6 patterns
CORRECTED_ALPHA = ALPHA / BONFERRONI_N
JITTER_MAX_MS = 50  # uniform 0-50ms jitter per request

EXPERIMENT_ID = "EXP-GRAPH-35083040517"
RAW_EVIDENCE_DIR = Path(__file__).parent.parent.parent / "experiments" / EXPERIMENT_ID / "raw_evidence"

# === SCHEMA GENERATION ===
FIELD_TYPES = ["string", "integer", "number", "boolean"]
FIELD_PREFIXES = [
    "user_", "order_", "product_", "payment_", "shipping_",
    "inventory_", "notification_", "analytics_", "auth_", "session_",
    "config_", "cache_", "log_", "event_", "metric_",
    "report_", "export_", "import_", "sync_", "queue_",
]

def generate_field_name(idx, rng):
    prefix = FIELD_PREFIXES[rng.randint(0, len(FIELD_PREFIXES) - 1)]
    suffix = rng.randint(1000, 9999)
    return f"{prefix}{suffix}"

def generate_schema(n_fields, rng):
    schema = []
    used_names = set()
    for i in range(n_fields):
        while True:
            name = generate_field_name(i, rng)
            if name not in used_names:
                used_names.add(name)
                break
        ftype = FIELD_TYPES[rng.randint(0, len(FIELD_TYPES) - 1)]
        schema.append({"name": name, "type": ftype})
    return schema

def schema_to_dict(schema, rng):
    result = {}
    for field in schema:
        if field["type"] == "string":
            result[field["name"]] = f"value_{rng.randint(1000, 9999)}"
        elif field["type"] == "integer":
            result[field["name"]] = rng.randint(1, 10000)
        elif field["type"] == "number":
            result[field["name"]] = round(rng.random() * 1000, 2)
        elif field["type"] == "boolean":
            result[field["name"]] = rng.randint(0, 1) == 1
    return result

# === PATTERN APPLICATION ===
def apply_pattern(schema, pattern, rng):
    new_schema = [dict(f) for f in schema]

    if pattern == "add_field":
        new_name = f"new_field_{rng.randint(1000, 9999)}"
        new_type = FIELD_TYPES[rng.randint(0, len(FIELD_TYPES) - 1)]
        new_schema.append({"name": new_name, "type": new_type})
        return new_schema, f"added field {new_name}:{new_type}"

    elif pattern == "remove_field":
        if len(new_schema) > 1:
            idx = rng.randint(0, len(new_schema) - 1)
            removed = new_schema.pop(idx)
            return new_schema, f"removed field {removed['name']}"
        return new_schema, "no removal (schema too small)"

    elif pattern == "change_type":
        if new_schema:
            idx = rng.randint(0, len(new_schema) - 1)
            old_type = new_schema[idx]["type"]
            new_type = "string" if old_type != "string" else "integer"
            new_schema[idx] = {"name": new_schema[idx]["name"], "type": new_type}
            return new_schema, f"changed {new_schema[idx]['name']} from {old_type} to {new_type}"
        return new_schema, "no change (empty schema)"

    elif pattern == "optional_field_churn":
        for _ in range(2):
            opt_name = f"opt_{rng.randint(1000, 9999)}"
            new_schema.append({"name": opt_name, "type": "string"})
        if len(new_schema) > 3:
            idx = rng.randint(0, len(new_schema) - 3)
            new_schema.pop(idx)
        return new_schema, "optional field churn (add 2 nullable, remove 1)"

    elif pattern == "null_valued_fields":
        for i in range(len(new_schema)):
            new_schema[i] = {"name": new_schema[i]["name"], "type": "null"}
        return new_schema, "all fields set to null"

    elif pattern == "nested_object_variation":
        nest_name = f"nested_{rng.randint(1000, 9999)}"
        new_schema.append({"name": nest_name, "type": "object"})
        nest_inner = f"inner_{rng.randint(1000, 9999)}"
        new_schema.append({"name": nest_inner, "type": "string"})
        return new_schema, f"added nested object {nest_name}"

    elif pattern == "fresh_copy":
        return new_schema, "no modification (fresh copy)"

    return new_schema, f"unknown pattern {pattern}"

# === MOCK SERVER (POST-based) ===
class ResponseTimeHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler: POST /api/compute receives schema as JSON body, returns computed response."""

    lock = threading.Lock()
    request_log = []

    # Serialization iterations per field — must be high enough that per-field
    # computation time (~1-2ms) is comparable to jitter range (0-50ms).
    # Reduced from 8000 to avoid timeout; 2000 iters × 50 fields ≈ 100ms total
    SERIAL_ITERS_PER_FIELD = 2000

    def do_POST(self):
        if self.path == "/api/compute":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode("utf-8"))
                schema = data["schema"]
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError) as e:
                self.send_error(400, f"Invalid request: {e}")
                return

            # --- Computation-dependent serialization ---
            # Generate values for each field based on type
            field_results = {}
            for field in schema:
                name = field.get("name", "unknown")
                ftype = field.get("type", "string")
                if ftype == "string":
                    field_results[name] = f"val_{hashlib.md5(name.encode()).hexdigest()[:8]}"
                elif ftype == "integer":
                    field_results[name] = hash(name) % 10000
                elif ftype == "number":
                    field_results[name] = round(abs(hash(name)) / 1000.0, 4)
                elif ftype == "boolean":
                    field_results[name] = hash(name) % 2 == 0
                elif ftype == "null":
                    field_results[name] = None
                elif ftype == "object":
                    field_results[name] = {"nested": True, "key": name}

            # Per-field computation: repeated json.dumps + json.loads + sha256
            # This makes response time proportional to field count
            for key, val in field_results.items():
                serialized = json.dumps(val).encode("utf-8")
                for _ in range(self.SERIAL_ITERS_PER_FIELD):
                    serialized = json.dumps(val).encode("utf-8")
                    _ = hashlib.sha256(serialized).digest()
                    _ = json.loads(serialized)

            response_bytes = json.dumps(field_results).encode("utf-8")

            # --- Jitter injection ---
            jitter_s = random.random() * JITTER_MAX_MS / 1000.0
            time.sleep(jitter_s)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-Field-Count", str(len(schema)))
            self.end_headers()
            self.wfile.write(response_bytes)

            log_entry = {
                "schema_size": len(schema),
                "response_bytes": len(response_bytes),
                "jitter_ms": round(jitter_s * 1000, 2),
            }
            with ResponseTimeHandler.lock:
                ResponseTimeHandler.request_log.append(log_entry)
        else:
            self.send_error(404)

    def do_GET(self):
        """Health check."""
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass

# === CLIENT MEASUREMENT ===
def measure_response_time(base_url, schema_list, n_reps):
    """Measure response times for a given schema configuration using POST.
    
    schema_list: list of {"name": ..., "type": ...} dicts (schema metadata)
    """
    payload = json.dumps({"schema": schema_list}).encode("utf-8")
    times = []

    for i in range(n_reps):
        start = time.perf_counter()
        try:
            req = urllib.request.Request(
                f"{base_url}/api/compute",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp.read()
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            times.append(elapsed_ms)
        except Exception as e:
            print(f"  ERROR: request {i}: {e}")
            times.append(None)

    return [t for t in times if t is not None]

# === STATISTICAL TESTS ===
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return 0.0
    var1 = statistics.variance(group1)
    var2 = statistics.variance(group2)
    pooled_std = ((var1 * (n1 - 1) + var2 * (n2 - 1)) / (n1 + n2 - 2)) ** 0.5
    if pooled_std == 0:
        return 0.0
    return (statistics.mean(group2) - statistics.mean(group1)) / pooled_std

def wilson_ci(successes, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * (max(0, (p * (1 - p) + z**2 / (4 * n))) / n) ** 0.5 / denom
    return (max(0, center - margin), min(1, center + margin))

# === MAIN EXPERIMENT ===
def run_experiment():
    print(f"=== {EXPERIMENT_ID}: Response-Time Profiling Experiment ===")
    print(f"Schema sizes: {SCHEMA_SIZES}")
    print(f"Reps per condition: {N_REPS}")
    print(f"Corrected alpha: {CORRECTED_ALPHA:.6f} (Bonferroni, {BONFERRONI_N} comparisons)")
    print()

    rng_field = random.Random(SEED_FIELDGEN)
    rng_pattern = random.Random(SEED_PATTERN)
    random.seed(SEED_JITTER)

    patterns = ["add_field", "remove_field", "change_type",
                "optional_field_churn", "null_valued_fields",
                "nested_object_variation", "fresh_copy"]

    # Start mock server
    server = http.server.HTTPServer(("127.0.0.1", 0), ResponseTimeHandler)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.3)
    base_url = f"http://127.0.0.1:{port}"
    print(f"Mock server on port {port}")

    # Verify server is running
    try:
        req = urllib.request.Request(f"{base_url}/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"Health check: {resp.read().decode()}")
    except Exception as e:
        print(f"WARNING: Health check failed: {e}")

    raw_measurements = []
    all_before = {}
    all_after = {}

    try:
        for size in SCHEMA_SIZES:
            print(f"\n--- Schema size: {size} fields ---")
            base_schema = generate_schema(size, rng_field)

            for pattern in patterns:
                # Send schema metadata (list of {name, type} dicts) to server
                # Server generates values and computes response internally
                before_schema_list = base_schema  # original schema
                after_schema, desc = apply_pattern(base_schema, pattern, rng_pattern)
                after_schema_list = after_schema

                print(f"  Pattern: {pattern:25s} ({desc})")

                before_times = measure_response_time(base_url, before_schema_list, N_REPS)
                after_times = measure_response_time(base_url, after_schema_list, N_REPS)

                all_before[(pattern, size)] = before_times
                all_after[(pattern, size)] = after_times

                raw_measurements.append({
                    "pattern": pattern,
                    "schema_size": size,
                    "description": desc,
                    "before_times_ms": [round(t, 3) for t in before_times],
                    "after_times_ms": [round(t, 3) for t in after_times],
                    "before_n": len(before_times),
                    "after_n": len(after_times),
                    "before_mean_ms": round(statistics.mean(before_times), 3) if before_times else None,
                    "after_mean_ms": round(statistics.mean(after_times), 3) if after_times else None,
                    "before_median_ms": round(statistics.median(before_times), 3) if before_times else None,
                    "after_median_ms": round(statistics.median(after_times), 3) if after_times else None,
                    "before_std_ms": round(statistics.stdev(before_times), 3) if len(before_times) > 1 else None,
                    "after_std_ms": round(statistics.stdev(after_times), 3) if len(after_times) > 1 else None,
                })

                if len(before_times) >= 2 and len(after_times) >= 2:
                    ks_stat, ks_p = stats.ks_2samp(before_times, after_times)
                    print(f"    KS D={ks_stat:.4f}, p={ks_p:.6f} (before mean={statistics.mean(before_times):.1f}ms, after mean={statistics.mean(after_times):.1f}ms)")
                else:
                    print(f"    Insufficient data (before={len(before_times)}, after={len(after_times)})")

    finally:
        server.shutdown()

    print(f"\nServer log entries: {len(ResponseTimeHandler.request_log)}")
    return raw_measurements, all_before, all_after

def analyze_results(raw_measurements, all_before, all_after):
    patterns_true_drift = ["add_field", "remove_field", "change_type"]
    patterns_noise = ["optional_field_churn", "null_valued_fields", "nested_object_variation"]
    pattern_control = "fresh_copy"

    per_condition = []
    tp_detections = 0
    tp_total = 0
    fp_detections = 0
    fp_total = 0

    for m in raw_measurements:
        pattern = m["pattern"]
        size = m["schema_size"]
        before = all_before[(pattern, size)]
        after = all_after[(pattern, size)]

        if len(before) < 2 or len(after) < 2:
            per_condition.append({
                "pattern": pattern,
                "schema_size": size,
                "ks_d": None,
                "ks_p": None,
                "detected": None,
                "cohens_d": None,
                "mean_diff_ms": None,
                "before_mean_ms": None,
                "after_mean_ms": None,
                "before_n": len(before),
                "after_n": len(after),
                "error": "insufficient data"
            })
            continue

        ks_stat, ks_p = stats.ks_2samp(before, after)
        detected = ks_p < CORRECTED_ALPHA
        d = cohens_d(before, after)
        mean_diff = statistics.mean(after) - statistics.mean(before)

        per_condition.append({
            "pattern": pattern,
            "schema_size": size,
            "ks_d": round(ks_stat, 6),
            "ks_p": round(ks_p, 8),
            "detected": detected,
            "cohens_d": round(d, 4),
            "mean_diff_ms": round(mean_diff, 3),
            "before_mean_ms": round(statistics.mean(before), 3),
            "after_mean_ms": round(statistics.mean(after), 3),
            "before_n": len(before),
            "after_n": len(after),
        })

        if pattern in patterns_true_drift:
            tp_total += 1
            if detected:
                tp_detections += 1
        elif pattern in patterns_noise or pattern == pattern_control:
            fp_total += 1
            if detected:
                fp_detections += 1

    # TP/FP rates
    tp_rate = tp_detections / tp_total if tp_total > 0 else 0.0
    fp_rate = fp_detections / fp_total if fp_total > 0 else 0.0
    tp_ci = wilson_ci(tp_detections, tp_total) if tp_total > 0 else (0.0, 1.0)
    fp_ci = wilson_ci(fp_detections, fp_total) if fp_total > 0 else (0.0, 1.0)

    # Per-pattern TP rates
    per_pattern_tp = {}
    for p in patterns_true_drift:
        pattern_conditions = [c for c in per_condition if c["pattern"] == p and c["detected"] is not None]
        n_detected = sum(1 for c in pattern_conditions if c["detected"])
        n_total = len(pattern_conditions)
        per_pattern_tp[p] = {
            "tp_rate": round(n_detected / n_total, 4) if n_total > 0 else 0.0,
            "n_detected": n_detected,
            "n_total": n_total,
            "detected_at_sizes": [c["schema_size"] for c in pattern_conditions if c["detected"]],
            "missed_at_sizes": [c["schema_size"] for c in pattern_conditions if not c["detected"]],
        }

    # Per-pattern FP rates
    per_pattern_fp = {}
    for p in patterns_noise + [pattern_control]:
        pattern_conditions = [c for c in per_condition if c["pattern"] == p and c["detected"] is not None]
        n_detected = sum(1 for c in pattern_conditions if c["detected"])
        n_total = len(pattern_conditions)
        per_pattern_fp[p] = {
            "fp_rate": round(n_detected / n_total, 4) if n_total > 0 else 0.0,
            "n_detected": n_detected,
            "n_total": n_total,
            "false_alarm_at_sizes": [c["schema_size"] for c in pattern_conditions if c["detected"]],
            "correct_reject_at_sizes": [c["schema_size"] for c in pattern_conditions if not c["detected"]],
        }

    # Per-schema-size analysis
    per_schema_size = {}
    for size in SCHEMA_SIZES:
        size_conditions = [c for c in per_condition if c["schema_size"] == size and c["ks_d"] is not None]
        if not size_conditions:
            continue

        drift_conds = [c for c in size_conditions if c["pattern"] in patterns_true_drift]
        noise_conds = [c for c in size_conditions if c["pattern"] in patterns_noise]

        drift_d_values = [c["ks_d"] for c in drift_conds]
        noise_d_values = [c["ks_d"] for c in noise_conds]

        if len(drift_d_values) >= 2 and len(noise_d_values) >= 2:
            try:
                mw_stat, mw_p_one_sided = stats.mannwhitneyu(
                    drift_d_values, noise_d_values, alternative='greater'
                )
                mw_p_two_sided = mw_p_one_sided * 2 if mw_p_one_sided < 1 else 1.0
            except ValueError:
                mw_stat, mw_p_one_sided, mw_p_two_sided = None, 1.0, 1.0
        else:
            mw_stat, mw_p_one_sided, mw_p_two_sided = None, 1.0, 1.0

        if len(drift_d_values) >= 2 and len(noise_d_values) >= 2:
            mw_cohens_d = cohens_d(noise_d_values, drift_d_values)
        else:
            mw_cohens_d = None

        detected_drift = sum(1 for c in drift_conds if c["detected"])
        detected_noise = sum(1 for c in noise_conds if c["detected"])

        per_schema_size[str(size)] = {
            "n_conditions": len(size_conditions),
            "drift_patterns_detected": detected_drift,
            "drift_patterns_total": len(drift_conds),
            "noise_patterns_detected": detected_noise,
            "noise_patterns_total": len(noise_conds),
            "mean_ks_d_drift": round(statistics.mean(drift_d_values), 4) if drift_d_values else None,
            "mean_ks_d_noise": round(statistics.mean(noise_d_values), 4) if noise_d_values else None,
            "mean_cohens_d_drift": round(statistics.mean([c["cohens_d"] for c in drift_conds]), 4) if drift_conds else None,
            "mean_cohens_d_noise": round(statistics.mean([c["cohens_d"] for c in noise_conds]), 4) if noise_conds else None,
            "mann_whitney_u": round(mw_stat, 4) if mw_stat is not None else None,
            "mann_whitney_p_one_sided": round(mw_p_one_sided, 6),
            "mann_whitney_p_two_sided": round(mw_p_two_sided, 6),
            "mann_whitney_cohens_d": round(mw_cohens_d, 4) if mw_cohens_d is not None else None,
            "per_pattern": {c["pattern"]: {
                "ks_d": c["ks_d"],
                "ks_p": c["ks_p"],
                "detected": c["detected"],
                "cohens_d": c["cohens_d"],
                "mean_diff_ms": c["mean_diff_ms"],
            } for c in size_conditions},
        }

    # === CONTROLS ===
    controls = {}

    # Positive control: add_field at n>=30
    pos_conds = [c for c in per_condition if c["pattern"] == "add_field" and c["schema_size"] >= 30 and c["ks_d"] is not None]
    pos_detected = [c for c in pos_conds if c["detected"]]
    pos_ks_d_values = [c["ks_d"] for c in pos_conds]
    controls["positive_control_add_field"] = {
        "description": "add_field at n>=30: KS D > 0.1, p < 0.05",
        "conditions_tested": len(pos_conds),
        "detected": len(pos_detected),
        "mean_ks_d": round(statistics.mean(pos_ks_d_values), 4) if pos_ks_d_values else None,
        "all_detected": len(pos_detected) == len(pos_conds) if pos_conds else False,
        "result": "PASS" if len(pos_detected) == len(pos_conds) and pos_ks_d_values and statistics.mean(pos_ks_d_values) > 0.1 else "FAIL",
    }

    # Null control: fresh_copy at all sizes
    fresh_conds = [c for c in per_condition if c["pattern"] == "fresh_copy" and c["ks_d"] is not None]
    fresh_false_alarms = [c for c in fresh_conds if c["detected"]]
    fresh_fp_rate = len(fresh_false_alarms) / len(fresh_conds) if fresh_conds else 1.0
    controls["null_control_fresh_copy"] = {
        "description": "fresh_copy: KS test should not detect shift (FP <= 0.15)",
        "conditions_tested": len(fresh_conds),
        "false_alarms": len(fresh_false_alarms),
        "fp_rate": round(fresh_fp_rate, 4),
        "result": "PASS" if fresh_fp_rate <= 0.15 else "FAIL",
    }

    # Separation control: Mann-Whitney across all sizes
    all_mw_p = [per_schema_size[s]["mann_whitney_p_one_sided"] for s in per_schema_size
                if per_schema_size[s]["mann_whitney_p_one_sided"] is not None]
    separation_passes = sum(1 for p in all_mw_p if p < 0.05)
    controls["separation_control_mann_whitney"] = {
        "description": "Mann-Whitney one-sided: drift > noise KS D values, p < 0.05",
        "sizes_tested": len(all_mw_p),
        "sizes_passing": separation_passes,
        "p_values": {s: per_schema_size[s]["mann_whitney_p_one_sided"] for s in per_schema_size},
        "result": "PASS" if separation_passes >= 3 else "FAIL",
    }

    # Calibration control: response time proportional to field count
    size_means = {}
    for size in SCHEMA_SIZES:
        fresh_before = [c for c in per_condition if c["pattern"] == "fresh_copy" and c["schema_size"] == size and c["before_mean_ms"] is not None]
        if fresh_before:
            size_means[size] = fresh_before[0]["before_mean_ms"]

    if len(size_means) >= 3:
        sizes_sorted = sorted(size_means.keys())
        means_sorted = [size_means[s] for s in sizes_sorted]
        x = np.array(sizes_sorted, dtype=float)
        y = np.array(means_sorted, dtype=float)
        correlation = np.corrcoef(x, y)[0, 1] if len(x) >= 2 else 0.0
        r_squared = correlation ** 2
    else:
        r_squared = 0.0

    controls["calibration_control_field_count"] = {
        "description": "Response time proportional to field count (R² > 0.7)",
        "size_means_ms": {str(k): round(v, 3) for k, v in size_means.items()},
        "r_squared": round(float(r_squared), 4),
        "result": "PASS" if r_squared > 0.7 else "FAIL",
    }

    # === DECISION RULE ===
    conditions = {}
    conditions["1_positive_control"] = controls["positive_control_add_field"]["result"] == "PASS"
    conditions["2_null_control"] = controls["null_control_fresh_copy"]["result"] == "PASS"
    patterns_passing_08 = sum(1 for p in patterns_true_drift if per_pattern_tp[p]["tp_rate"] >= 0.8)
    conditions["3_drift_patterns"] = patterns_passing_08 >= 2
    conditions["4_separation"] = controls["separation_control_mann_whitney"]["result"] == "PASS"
    noise_passing = sum(1 for p in patterns_noise if per_pattern_fp[p]["fp_rate"] <= 0.15)
    conditions["5_noise_fp"] = noise_passing >= 1

    all_pass = all(conditions.values())
    decision = "SURVIVES_CURRENT_TEST" if all_pass else "FALSIFIED-IN-SETTING"

    # Check MEASUREMENT_INVALID
    cal_pass = controls["calibration_control_field_count"]["result"] == "PASS"
    if not cal_pass and decision == "FALSIFIED-IN-SETTING":
        decision = "MEASUREMENT_INVALID"

    failed_conditions = [k for k, v in conditions.items() if not v]
    if all_pass:
        decision_reason = "All 5 frozen decision rule conditions satisfied"
    else:
        reasons = []
        if not conditions["1_positive_control"]:
            reasons.append(f"positive_control={controls['positive_control_add_field']['result']}")
        if not conditions["2_null_control"]:
            reasons.append(f"null_control={controls['null_control_fresh_copy']['result']} (FP={fresh_fp_rate:.4f})")
        if not conditions["3_drift_patterns"]:
            reasons.append(f"drift_patterns_passing_0.8={patterns_passing_08}/3 (need >=2)")
        if not conditions["4_separation"]:
            reasons.append(f"separation={controls['separation_control_mann_whitney']['result']}")
        if not conditions["5_noise_fp"]:
            reasons.append(f"noise_patterns_passing_FP<=0.15={noise_passing}/3 (need >=1)")
        decision_reason = "; ".join(reasons)

    if decision == "MEASUREMENT_INVALID":
        decision_reason = f"Calibration control failed (R²={r_squared:.4f} < 0.7): server response times not proportional to field count. Cannot distinguish drift from noise without computation-dependent timing."

    print(f"\n=== DECISION: {decision} ===")
    print(f"Reason: {decision_reason}")
    print(f"\nConditions: {conditions}")
    print(f"TP rate: {tp_rate:.4f} ({tp_detections}/{tp_total})")
    print(f"FP rate: {fp_rate:.4f} ({fp_detections}/{fp_total})")
    print(f"Patterns passing TP>=0.8: {patterns_passing_08}/3")
    print(f"Noise patterns passing FP<=0.15: {noise_passing}/3")

    return {
        "per_condition": per_condition,
        "per_pattern_tp": per_pattern_tp,
        "per_pattern_fp": per_pattern_fp,
        "per_schema_size": per_schema_size,
        "controls": controls,
        "decision": decision,
        "decision_reason": decision_reason,
        "decision_conditions": conditions,
        "overall_tp_rate": round(tp_rate, 4),
        "overall_fp_rate": round(fp_rate, 4),
        "tp_ci_95": [round(tp_ci[0], 4), round(tp_ci[1], 4)],
        "fp_ci_95": [round(fp_ci[0], 4), round(fp_ci[1], 4)],
        "tp_detections": tp_detections,
        "tp_total": tp_total,
        "fp_detections": fp_detections,
        "fp_total": fp_total,
    }

def main():
    raw_measurements, all_before, all_after = run_experiment()

    print("\n" + "="*60)
    print("ANALYSIS")
    print("="*60)

    analysis = analyze_results(raw_measurements, all_before, all_after)

    RAW_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    with open(RAW_EVIDENCE_DIR / "response_time_raw_measurements.json", "w") as f:
        json.dump(raw_measurements, f, indent=2)

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.bool_,)):
                return bool(obj)
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)

    with open(RAW_EVIDENCE_DIR / "response_time_derived_measurements.json", "w") as f:
        summary = {k: v for k, v in analysis.items() if k != "per_condition"}
        json.dump(summary, f, indent=2, cls=NumpyEncoder)

    with open(RAW_EVIDENCE_DIR / "response_time_per_condition.json", "w") as f:
        json.dump(analysis["per_condition"], f, indent=2, cls=NumpyEncoder)

    with open(RAW_EVIDENCE_DIR / "server_log.json", "w") as f:
        json.dump(ResponseTimeHandler.request_log, f, indent=2)

    print(f"\nRaw evidence saved to {RAW_EVIDENCE_DIR}")
    print(f"=== {EXPERIMENT_ID} Analysis Complete ===")

    return analysis

if __name__ == "__main__":
    analysis = main()
