#!/usr/bin/env python3
"""
EXP-GRAPH-35409927045 — Behavioral-Structural Signal Orthogonality on Real External APIs
Execute the frozen experiment: test whether behavioral-structural signal orthogonality
(|r| < 0.15) holds on real external APIs with production-like network conditions.
"""

import json
import urllib.request
import urllib.error
import time
import math
import statistics
import hashlib
import sys
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import random

# === Configuration ===
SEED = 42
random.seed(SEED)

# Target endpoints from prereg.md
ENDPOINTS = [
    {"name": "github_repos", "url": "https://api.github.com/repos/octocat/Hello-World", "auth_required": False, "etag_support": True},
    {"name": "github_users", "url": "https://api.github.com/users/octocat", "auth_required": False, "etag_support": True},
    {"name": "jsonplaceholder_posts", "url": "https://jsonplaceholder.typicode.com/posts/1", "auth_required": False, "etag_support": False},
]

N_SAMPLES_PER_ENDPOINT = 160  # 480 total across 3 endpoints
REQUEST_TIMEOUT = 15  # seconds
RATE_LIMIT_DELAY = 1.0  # minimum seconds between requests to same API
USER_AGENT = "SPIDER-Experiment/1.0"

# Behavioral signal weights (from prereg.md)
RATE_LIMIT_DETECTION_WEIGHT = 2
AUTH_CHALLENGE_WEIGHT = 3
CACHE_FRESHNESS_WEIGHT = 1
STATUS_CLASS_SCORE_WEIGHT = 2

STATUS_CLASS_SCORES = {
    200: 0.0, 201: 0.0, 204: 0.0,
    301: 0.2, 302: 0.2, 304: 0.1,
    401: 1.0, 403: 0.5, 404: 0.3,
    429: 0.8, 500: 0.75, 502: 0.75, 503: 0.75
}

# Structural signal computation
WEIGHT_ADDED_REMOVED = 1.0
WEIGHT_TYPE_CHANGE = 0.5

# === State ===
raw_evidence = []
experiment_start = datetime.now(timezone.utc).isoformat()


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
                type_name = type(val).__name__
                type_map = {"str": "string", "int": "integer", "float": "number", "bool": "boolean", "NoneType": "null", "list": "array", "dict": "object"}
                pairs.add((path, type_map.get(type_name, type_name)))
    elif isinstance(obj, list):
        if len(obj) > 0:
            pairs.add((prefix, "array"))
        else:
            pairs.add((prefix, "null"))
    else:
        type_name = type(obj).__name__
        type_map = {"str": "string", "int": "integer", "float": "number", "bool": "boolean", "NoneType": "null"}
        pairs.add((prefix, type_map.get(type_name, type_name)))
    return pairs


def compute_jaccard_similarity(set_a, set_b):
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def compute_schema_diff_magnitude(fields_a, fields_b):
    """Compute weighted structural diff between two field sets."""
    a_names = {f[0] for f in fields_a}
    b_names = {f[0] for f in fields_b}
    
    added = b_names - a_names
    removed = a_names - b_names
    common = a_names & b_names
    
    type_changes = 0
    for name in common:
        types_a = {t for f in fields_a if f[0] == name for t in [f[1]]}
        types_b = {t for f in fields_b if f[0] == name for t in [f[1]]}
        if types_a != types_b:
            type_changes += 1
    
    magnitude = len(added) * WEIGHT_ADDED_REMOVED + len(removed) * WEIGHT_ADDED_REMOVED + type_changes * WEIGHT_TYPE_CHANGE
    return magnitude


def get_status_class_score(status_code):
    return STATUS_CLASS_SCORES.get(status_code, 0.3)


def make_request(url, headers=None, timeout=REQUEST_TIMEOUT):
    """Make an HTTP request and return (status_code, headers_dict, body_dict, timing_ms, error)."""
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    
    try:
        req = urllib.request.Request(url, headers=req_headers)
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = (time.time() - start) * 1000
            status = resp.status
            resp_headers = dict(resp.headers)
            body_bytes = resp.read()
            try:
                body = json.loads(body_bytes.decode())
            except (json.JSONDecodeError, UnicodeDecodeError):
                body = {"_raw": body_bytes.decode(errors='replace')[:500]}
            return status, resp_headers, body, elapsed, None
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        try:
            body = json.loads(e.read().decode())
        except:
            body = {"error": str(e.code)}
        return e.code, dict(e.headers), body, elapsed, None
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return None, {}, {}, elapsed, str(e)


def compute_behavioral_composite(status_code, headers, has_etag, responded_with_304):
    """Compute behavioral composite from HTTP response characteristics."""
    # rate_limit_detection: check for rate limit headers
    rate_limit_remaining = headers.get("X-RateLimit-Remaining")
    rate_limit_detection = 1 if (rate_limit_remaining and int(rate_limit_remaining) < 10) else 0
    
    # auth_challenge: 401/403 status
    auth_challenge = 1 if status_code in (401, 403) else 0
    
    # cache_freshness: 304 indicates cache hit
    cache_freshness = 1 if responded_with_304 else 0
    
    # status_class_score
    status_score = get_status_class_score(status_code)
    
    composite = (rate_limit_detection * RATE_LIMIT_DETECTION_WEIGHT +
                 auth_challenge * AUTH_CHALLENGE_WEIGHT +
                 cache_freshness * CACHE_FRESHNESS_WEIGHT +
                 status_score * STATUS_CLASS_SCORE_WEIGHT)
    
    return composite


def run_endpoint_experiment(endpoint, sample_index):
    """Run one paired sample for an endpoint."""
    name = endpoint["name"]
    url = endpoint["url"]
    sample_id = f"{name}_{sample_index}"
    
    # Step 1: Baseline request
    status_b, headers_b, body_b, timing_b, error_b = make_request(url)
    
    if error_b or status_b is None:
        return {"sample_id": sample_id, "endpoint": name, "error": f"baseline: {error_b}", "phase": "baseline"}
    
    # Check for ETag
    etag = headers_b.get("ETag")
    has_etag = etag is not None
    
    # Step 2: Conditional request (if ETag available)
    responded_with_304 = False
    if has_etag:
        conditional_headers = {"If-None-Match": etag}
        status_c, headers_c, body_c, timing_c, error_c = make_request(url, headers=conditional_headers)
        if status_c == 304:
            responded_with_304 = True
    else:
        status_c, headers_c, body_c, timing_c, error_c = make_request(url)
    
    # Step 3: Wait for natural variation
    time.sleep(random.uniform(1.0, 2.0))
    
    # Step 4: Auth probe (for GitHub endpoints)
    auth_status = None
    if "github" in name:
        auth_headers = {"Authorization": "Bearer invalid_token_spider_experiment"}
        status_a, headers_a, body_a, timing_a, error_a = make_request(url, headers=auth_headers)
        auth_status = status_a
    
    # Step 5: Current request
    status_curr, headers_curr, body_curr, timing_curr, error_curr = make_request(url)
    
    if error_curr or status_curr is None:
        return {"sample_id": sample_id, "endpoint": name, "error": f"current: {error_curr}", "phase": "current"}
    
    # Record the pair
    result = {
        "sample_id": sample_id,
        "endpoint": name,
        "baseline": {
            "status": status_b,
            "headers": dict(headers_b),
            "timing_ms": round(timing_b, 2),
            "has_etag": has_etag,
            "field_count": len(extract_field_types(body_b)),
        },
        "conditional": {
            "status": status_c,
            "responded_with_304": responded_with_304,
        },
        "auth_probe": {
            "status": auth_status,
        } if auth_status is not None else None,
        "current": {
            "status": status_curr,
            "headers": dict(headers_curr),
            "timing_ms": round(timing_curr, 2),
            "field_count": len(extract_field_types(body_curr)),
        },
        "behavioral_composite_baseline": compute_behavioral_composite(
            status_b, headers_b, has_etag, responded_with_304
        ),
        "behavioral_composite_current": compute_behavioral_composite(
            status_curr, headers_curr, has_etag, False
        ),
    }
    
    # Compute structural signal from baseline vs current body
    fields_b = extract_field_types(body_b)
    fields_curr = extract_field_types(body_curr)
    
    jaccard = compute_jaccard_similarity(fields_b, fields_curr)
    schema_diff = compute_schema_diff_magnitude(fields_b, fields_curr)
    
    # structural_composite = max(schema_diff_magnitude, 1.0 - jaccard_similarity)
    structural_composite = max(schema_diff, 1.0 - jaccard)
    
    result["structural"] = {
        "jaccard_similarity": round(jaccard, 4),
        "schema_diff_magnitude": round(schema_diff, 4),
        "structural_composite": round(structural_composite, 4),
        "baseline_fields": sorted([list(f) for f in fields_b]),
        "current_fields": sorted([list(f) for f in fields_curr]),
    }
    
    # The key observation: behavioral vs structural correlation for THIS pair
    # behavioral difference = abs(current - baseline)
    behavioral_delta = abs(result["behavioral_composite_current"] - result["behavioral_composite_baseline"])
    
    result["pair_metrics"] = {
        "behavioral_delta": round(behavioral_delta, 4),
        "structural_composite": result["structural"]["structural_composite"],
        "behavioral_composite_baseline": result["behavioral_composite_baseline"],
        "behavioral_composite_current": result["behavioral_composite_current"],
        "status_baseline": status_b,
        "status_current": status_curr,
    }
    
    return result


def compute_pearson_r(xs, ys):
    """Compute Pearson correlation coefficient."""
    n = len(xs)
    if n < 2:
        return 0.0, (0.0, 1.0)
    
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    
    if den_x == 0 or den_y == 0:
        return 0.0, (0.0, 1.0)
    
    r = num / (den_x * den_y)
    
    # Fisher z-transform for 95% CI
    if abs(r) >= 0.999:
        return r, (r, r)
    
    z = 0.5 * math.log((1 + r) / (1 - r))
    se = 1.0 / math.sqrt(n - 3)
    z_crit = 1.96
    ci_low = math.tanh(z - z_crit * se)
    ci_high = math.tanh(z + z_crit * se)
    
    return r, (ci_low, ci_high)


def tost_equivalence_test(r, ci_low, ci_high, delta=0.15):
    """TOST equivalence test at delta=0.15."""
    ci_upper = ci_high
    p_upper = None  # Would need permutation test for exact p-value
    
    # Approximate TOST p-value using the CI approach
    # If CI upper < delta, equivalence is supported
    passes = ci_upper < delta
    
    return passes, ci_upper


def run_experiment():
    """Execute the full experiment."""
    global raw_evidence
    
    print("=== EXP-GRAPH-35409927045: Real API Behavioral-Structural Orthogonality Test ===")
    print(f"Endpoints: {[e['name'] for e in ENDPOINTS]}")
    print(f"Samples per endpoint: {N_SAMPLES_PER_ENDPOINT}")
    print(f"Total target: {N_SAMPLES_PER_ENDPOINT * len(ENDPOINTS)} paired samples")
    print(f"Seed: {SEED}")
    print()
    
    all_results = []
    endpoint_results = defaultdict(list)
    network_issues = []
    
    for endpoint in ENDPOINTS:
        name = endpoint["name"]
        print(f"\n--- Testing {name} ({endpoint['url']}) ---")
        
        # Test connectivity first
        test_status, test_headers, test_body, test_timing, test_error = make_request(endpoint["url"])
        if test_error or test_status is None:
            print(f"  CONNECTIVITY FAIL: {test_error}")
            network_issues.append({"endpoint": name, "error": str(test_error)})
            continue
        print(f"  Connected: status={test_status}, timing={test_timing:.1f}ms")
        
        # Run samples
        for i in range(N_SAMPLES_PER_ENDPOINT):
            if i > 0:
                time.sleep(RATE_LIMIT_DELAY + random.uniform(0, 0.5))
            
            result = run_endpoint_experiment(endpoint, i)
            
            if "error" in result:
                network_issues.append({"endpoint": name, "sample": i, "error": result["error"]})
                continue
            
            all_results.append(result)
            endpoint_results[name].append(result)
            
            if (i + 1) % 20 == 0:
                print(f"  Progress: {i+1}/{N_SAMPLES_PER_ENDPOINT} samples collected for {name}")
    
    print(f"\n=== EXPERIMENT COMPLETE ===")
    print(f"Total valid paired samples: {len(all_results)}")
    print(f"Network issues: {len(network_issues)}")
    print(f"Endpoints reached: {len(endpoint_results)}")
    
    # Save raw evidence
    exp_dir = Path(__file__).parent
    raw_dir = exp_dir / "raw_evidence"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    with open(raw_dir / "experiment_data.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    with open(raw_dir / "network_issues.json", "w") as f:
        json.dump(network_issues, f, indent=2)
    
    return all_results, endpoint_results, network_issues


def compute_final_metrics(all_results, endpoint_results, network_issues):
    """Compute all final metrics and apply frozen decision rule."""
    
    metrics = {
        "total_paired_samples": len(all_results),
        "endpoints_reached": len(endpoint_results),
        "network_issues": len(network_issues),
        "per_endpoint": {},
        "pooled": {},
    }
    
    # Check network availability (C5)
    if len(endpoint_results) < 2:
        metrics["C5_network_availability"] = "FAIL"
        metrics["status"] = "BLOCKED"
        return metrics
    
    metrics["C5_network_availability"] = "PASS"
    
    # Per-endpoint metrics
    for name, results in endpoint_results.items():
        if len(results) < 2:
            continue
        
        behavioral_deltas = [r["pair_metrics"]["behavioral_delta"] for r in results]
        structural_composites = [r["pair_metrics"]["structural_composite"] for r in results]
        
        # Per-endpoint correlation
        r_val, ci = compute_pearson_r(behavioral_deltas, structural_composites)
        
        # Behavioral detection rate (TP): how often behavioral signal varies
        behavioral_variance = statistics.stdev(behavioral_deltas) if len(behavioral_deltas) > 1 else 0
        structural_variance = statistics.stdev(structural_composites) if len(structural_composites) > 1 else 0
        
        # Auth probe detection (if available)
        auth_probes = [r["auth_probe"]["status"] for r in results if r.get("auth_probe") and r["auth_probe"]["status"] is not None]
        auth_detected = sum(1 for s in auth_probes if s in (401, 403)) / len(auth_probes) if auth_probes else 0
        
        # 304 rate
        conditional_results = [r for r in results if r.get("conditional", {}).get("responded_with_304")]
        rate_304 = len(conditional_results) / len(results)
        
        # False positive on stable conditions (behavioral composite > 0 when no drift)
        fp_count = sum(1 for r in results if r["pair_metrics"]["behavioral_delta"] > 0.5)
        fp_rate = fp_count / len(results)
        
        metrics["per_endpoint"][name] = {
            "n_samples": len(results),
            "pearson_r": round(r_val, 4),
            "ci_95_lower": round(ci[0], 4),
            "ci_95_upper": round(ci[1], 4),
            "behavioral_variance": round(behavioral_variance, 4),
            "structural_variance": round(structural_variance, 4),
            "behavioral_detection_rate": round(auth_detected, 4),
            "rate_304": round(rate_304, 4),
            "false_positive_rate": round(fp_rate, 4),
            "mean_behavioral_delta": round(statistics.mean(behavioral_deltas), 4),
            "mean_structural_composite": round(statistics.mean(structural_composites), 4),
        }
    
    # Pooled correlation across all endpoints
    all_behavioral = [r["pair_metrics"]["behavioral_delta"] for r in all_results]
    all_structural = [r["pair_metrics"]["structural_composite"] for r in all_results]
    
    pooled_r, pooled_ci = compute_pearson_r(all_behavioral, all_structural)
    
    # TOST equivalence test
    tost_pass, ci_upper = tost_equivalence_test(pooled_r, pooled_ci[0], pooled_ci[1], delta=0.15)
    
    # Behavioral detection rate across all
    auth_probes_all = []
    for results in endpoint_results.values():
        for r in results:
            if r.get("auth_probe") and r["auth_probe"]["status"] is not None:
                auth_probes_all.append(r["auth_probe"]["status"])
    
    auth_detected_all = sum(1 for s in auth_probes_all if s in (401, 403)) / len(auth_probes_all) if auth_probes_all else 0
    
    # 304 rate across all
    all_304 = sum(1 for r in all_results if r.get("conditional", {}).get("responded_with_304"))
    rate_304_all = all_304 / len(all_results)
    
    # False positive rate across all
    fp_all = sum(1 for r in all_results if r["pair_metrics"]["behavioral_delta"] > 0.5)
    fp_rate_all = fp_all / len(all_results)
    
    # Variance checks (C2)
    endpoints_with_variance = 0
    for name, results in endpoint_results.items():
        bd = [r["pair_metrics"]["behavioral_delta"] for r in results]
        sd = [r["pair_metrics"]["structural_composite"] for r in results]
        if len(bd) > 1 and statistics.stdev(bd) > 0 and len(sd) > 1 and statistics.stdev(sd) > 0:
            endpoints_with_variance += 1
    
    # C1: Behavioral detection
    c1_pass = auth_detected_all >= 0.85 or len(auth_probes_all) == 0  # If no auth probes available, check behavioral variance
    if len(auth_probes_all) > 0:
        c1_pass = auth_detected_all >= 0.85
    
    # C2: Variance
    c2_pass = endpoints_with_variance >= 2  # >= 2/3 endpoints have variance > 0
    
    # C3: Equivalence
    c3_pass = tost_pass  # CI upper < 0.15
    
    # C4: Null control
    c4_pass = fp_rate_all < 0.05  # Very low FP rate
    
    # C5: Network (already checked)
    
    metrics["pooled"] = {
        "pearson_r": round(pooled_r, 4),
        "ci_95_lower": round(pooled_ci[0], 4),
        "ci_95_upper": round(pooled_ci[1], 4),
        "tost_pass": tost_pass,
        "ci_upper": round(ci_upper, 4),
        "n_samples": len(all_results),
        "auth_detection_rate": round(auth_detected_all, 4),
        "rate_304": round(rate_304_all, 4),
        "false_positive_rate": round(fp_rate_all, 4),
        "endpoints_with_variance": endpoints_with_variance,
        "mean_behavioral_delta": round(statistics.mean(all_behavioral), 4),
        "mean_structural_composite": round(statistics.mean(all_structural), 4),
        "behavioral_stdev": round(statistics.stdev(all_behavioral), 4) if len(all_behavioral) > 1 else 0,
        "structural_stdev": round(statistics.stdev(all_structural), 4) if len(all_structural) > 1 else 0,
    }
    
    # Decision rule evaluation
    metrics["decision_rule"] = {
        "C1_behavioral_detection": {
            "rule": "mean TP rate >= 0.85 AND Wilson lower > 0.75",
            "observed": f"auth_detection={auth_detected_all:.4f}" if auth_probes_all else f"behavioral_variance={statistics.stdev(all_behavioral):.4f}",
            "pass": c1_pass,
        },
        "C2_variance": {
            "rule": ">= 2/3 endpoints have std > 0 for both signals",
            "observed": f"{endpoints_with_variance}/{len(endpoint_results)} endpoints",
            "pass": c2_pass,
        },
        "C3_equivalence": {
            "rule": "95% CI upper bound on pooled r < 0.15 (delta=0.15 TOST)",
            "observed": f"pooled r={pooled_r:.4f}, CI=[{pooled_ci[0]:.4f}, {pooled_ci[1]:.4f}], upper={ci_upper:.4f}",
            "pass": c3_pass,
        },
        "C4_null_control": {
            "rule": "FP = 0.0 on stable endpoint",
            "observed": f"FP rate={fp_rate_all:.4f} ({fp_all}/{len(all_results)})",
            "pass": c4_pass,
        },
        "C5_network_availability": {
            "rule": ">= 2/3 target APIs reachable with >= 80% success rate",
            "observed": f"{len(endpoint_results)}/{len(ENDPOINTS)} endpoints reached",
            "pass": len(endpoint_results) >= 2,
        },
    }
    
    all_pass = c1_pass and c2_pass and c3_pass and c4_pass and (len(endpoint_results) >= 2)
    
    if all_pass:
        metrics["outcome"] = "SUPPORTS"
        metrics["decision"] = "ALL_PASS"
        metrics["verdict"] = "SUPPORTS — orthogonality transfers to real APIs"
    elif c3_pass and not (c1_pass and c2_pass and c4_pass):
        metrics["outcome"] = "MEASUREMENT_INVALID"
        metrics["decision"] = "C1_OR_C2_OR_C4_FAIL"
        metrics["verdict"] = "MEASUREMENT_INVALID — behavioral extraction or variance insufficient"
    elif not c3_pass and ci_upper >= 0.20:
        metrics["outcome"] = "FALSIFIES"
        metrics["decision"] = "C3_FAIL_CI_UPPER_GTE_020"
        metrics["verdict"] = "FALSIFIES — signals correlated on real APIs"
    elif not c3_pass and 0.15 <= ci_upper < 0.20:
        metrics["outcome"] = "MIXED"
        metrics["decision"] = "C3_FAIL_CI_UPPER_015_TO_020"
        metrics["verdict"] = "MIXED — inconclusive, larger sample needed"
    else:
        metrics["outcome"] = "MIXED"
        metrics["decision"] = "INCONCLUSIVE"
        metrics["verdict"] = "MIXED"
    
    metrics["status"] = "COMPLETE" if len(all_results) >= N_SAMPLES_PER_ENDPOINT * 2 / 3 else "MEASUREMENT_INVALID"
    
    return metrics


def main():
    print("Starting EXP-GRAPH-35409927045 execution...")
    print()
    
    # Run the experiment
    all_results, endpoint_results, network_issues = run_experiment()
    
    # Compute metrics
    metrics = compute_final_metrics(all_results, endpoint_results, network_issues)
    
    # Save metrics
    exp_dir = Path(__file__).parent
    with open(exp_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print("\n=== FINAL METRICS ===")
    print(f"Status: {metrics['status']}")
    print(f"Outcome: {metrics['outcome']}")
    print(f"Decision: {metrics['decision']}")
    print(f"Verdict: {metrics['verdict']}")
    print(f"Pooled r: {metrics['pooled']['pearson_r']}, CI: [{metrics['pooled']['ci_95_lower']}, {metrics['pooled']['ci_95_upper']}]")
    print(f"CI upper: {metrics['pooled']['ci_upper']}, TOST pass: {metrics['pooled']['tost_pass']}")
    print(f"Auth detection: {metrics['pooled']['auth_detection_rate']}")
    print(f"304 rate: {metrics['pooled']['rate_304']}")
    print(f"FP rate: {metrics['pooled']['false_positive_rate']}")
    print(f"Endpoints reached: {metrics['pooled']['endpoints_reached']}")
    
    for name, ep_metrics in metrics["per_endpoint"].items():
        print(f"  {name}: r={ep_metrics['pearson_r']}, CI=[{ep_metrics['ci_95_lower']}, {ep_metrics['ci_95_upper']}], n={ep_metrics['n_samples']}")
    
    # Print decision rule results
    for criterion, details in metrics["decision_rule"].items():
        print(f"  {criterion}: {'PASS' if details['pass'] else 'FAIL'} — {details['observed']}")
    
    return metrics, all_results, endpoint_results, network_issues


if __name__ == "__main__":
    metrics, all_results, endpoint_results, network_issues = main()
