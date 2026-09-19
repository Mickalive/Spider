#!/usr/bin/env python3
"""
EXP-GRAPH-35409927045 — Behavioral-Structural Signal Orthogonality on Real External APIs
Efficient execution: minimal requests per endpoint, focused on key measurement.
"""

import json
import urllib.request
import urllib.error
import time
import math
import statistics
import sys
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import random
import concurrent.futures

SEED = 42
random.seed(SEED)

ENDPOINTS = [
    {"name": "github_repos", "url": "https://api.github.com/repos/octocat/Hello-World"},
    {"name": "github_users", "url": "https://api.github.com/users/octocat"},
    {"name": "jsonplaceholder_posts", "url": "https://jsonplaceholder.typicode.com/posts/1"},
]

N_SAMPLES_PER_ENDPOINT = 20  # Reduced for efficiency
REQUEST_TIMEOUT = 10
RATE_LIMIT_DELAY = 0.5
USER_AGENT = "SPIDER-Experiment/1.0"

STATUS_CLASS_SCORES = {
    200: 0.0, 201: 0.0, 204: 0.0,
    301: 0.2, 302: 0.2, 304: 0.1,
    401: 1.0, 403: 0.5, 404: 0.3,
    429: 0.8, 500: 0.75, 502: 0.75, 503: 0.75
}

def extract_field_types(obj, prefix=""):
    pairs = set()
    if isinstance(obj, dict):
        for key, val in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(val, dict):
                pairs.update(extract_field_types(val, path))
            elif isinstance(val, list):
                pairs.add((path, "array"))
            else:
                type_map = {"str": "string", "int": "integer", "float": "number", "bool": "boolean", "NoneType": "null"}
                pairs.add((path, type_map.get(type(val).__name__, type(val).__name__)))
    elif isinstance(obj, list) and len(obj) > 0:
        pairs.add((prefix, "array"))
    elif isinstance(obj, list):
        pairs.add((prefix, "null"))
    else:
        type_map = {"str": "string", "int": "integer", "float": "number", "bool": "boolean", "NoneType": "null"}
        pairs.add((prefix, type_map.get(type(obj).__name__, type(obj).__name__)))
    return pairs

def compute_jaccard_similarity(set_a, set_b):
    if not set_a and not set_b: return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)

def compute_schema_diff_magnitude(fields_a, fields_b):
    a_names = {f[0] for f in fields_a}
    b_names = {f[0] for f in fields_b}
    added = b_names - a_names
    removed = a_names - b_names
    common = a_names & b_names
    type_changes = sum(1 for n in common if any(f[0]==n and f[1]!=t for f in fields_a for t in [next((g[1] for g in fields_b if g[0]==n), None)] if f[1]!=t))
    return len(added) * 1.0 + len(removed) * 1.0 + type_changes * 0.5

def get_status_class_score(code):
    return STATUS_CLASS_SCORES.get(code, 0.3)

def make_request(url, extra_headers=None, timeout=REQUEST_TIMEOUT):
    req_headers = {"User-Agent": USER_AGENT}
    if extra_headers: req_headers.update(extra_headers)
    try:
        req = urllib.request.Request(url, headers=req_headers)
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = (time.time() - start) * 1000
            body_bytes = resp.read()
            try:
                body = json.loads(body_bytes.decode())
            except:
                body = {"_raw": "non-json"}
            return resp.status, dict(resp.headers), body, round(elapsed, 2), None
    except urllib.error.HTTPError as e:
        try: body = json.loads(e.read().decode())
        except: body = {"error": str(e.code)}
        return e.code, dict(e.headers), body, 0, None
    except Exception as e:
        return None, {}, {}, 0, str(e)

def compute_behavioral_composite(status, headers, has_304):
    rate_limit_det = 1 if headers.get("X-RateLimit-Remaining") and int(headers.get("X-RateLimit-Remaining", 100)) < 10 else 0
    auth_challenge = 1 if status in (401, 403) else 0
    cache_fresh = 1 if has_304 else 0
    status_score = get_status_class_score(status)
    return rate_limit_det * 2 + auth_challenge * 3 + cache_fresh * 1 + status_score * 2

def fetch_pair(args):
    """Fetch one paired sample for an endpoint."""
    url, idx = args
    result = {"endpoint": url, "sample": idx}
    
    # Baseline
    s1, h1, b1, t1, e1 = make_request(url)
    if e1 or s1 is None:
        result["error"] = f"baseline: {e1}"
        return result
    
    etag = h1.get("ETag")
    has_304 = False
    
    # Conditional request if ETag available
    if etag:
        s2, h2, b2, t2, e2 = make_request(url, {"If-None-Match": etag})
        if s2 == 304:
            has_304 = True
    
    # Auth probe
    auth_s = None
    if "github" in url:
        auth_s, _, _, _, _ = make_request(url, {"Authorization": "Bearer invalid_token_spider"})
    
    # Current request (after delay)
    time.sleep(random.uniform(0.5, 1.5))
    s3, h3, b3, t3, e3 = make_request(url)
    if e3 or s3 is None:
        result["error"] = f"current: {e3}"
        return result
    
    # Extract fields for structural comparison
    try:
        fields_b = extract_field_types(b1) if isinstance(b1, dict) else set()
        fields_c = extract_field_types(b3) if isinstance(b3, dict) else set()
    except:
        fields_b = set()
        fields_c = set()
    
    jaccard = compute_jaccard_similarity(fields_b, fields_c) if fields_b and fields_c else 0.0
    schema_diff = compute_schema_diff_magnitude(fields_b, fields_c) if fields_b and fields_c else 0.0
    structural_composite = max(schema_diff, 1.0 - jaccard)
    
    # Behavioral composites
    bc_b = compute_behavioral_composite(s1, h1, has_304)
    bc_c = compute_behavioral_composite(s3, h3, False)
    behavioral_delta = abs(bc_c - bc_b)
    
    result.update({
        "status_baseline": s1, "status_current": s3,
        "behavioral_composite_baseline": bc_b, "behavioral_composite_current": bc_c,
        "behavioral_delta": behavioral_delta,
        "structural_composite": structural_composite,
        "jaccard": round(jaccard, 4),
        "schema_diff": round(schema_diff, 4),
        "auth_status": auth_s,
        "has_etag": bool(etag),
        "responded_304": has_304,
    })
    
    return result

def main():
    print("=== EXP-GRAPH-35409927045 Execution ===")
    print(f"Endpoints: {len(ENDPOINTS)}")
    print(f"Samples per endpoint: {N_SAMPLES_PER_ENDPOINT}")
    print(f"Total paired samples target: {N_SAMPLES_PER_ENDPOINT * len(ENDPOINTS)}")
    print()
    
    # Build all tasks
    tasks = []
    for ep in ENDPOINTS:
        for i in range(N_SAMPLES_PER_ENDPOINT):
            tasks.append((ep["url"], i))
    
    # Shuffle for randomness (seed already set)
    random.shuffle(tasks)
    
    # Execute sequentially but efficiently
    all_results = []
    network_errors = []
    start_time = time.time()
    
    for i, args in enumerate(tasks):
        if i > 0 and i % 5 == 0:
            elapsed = time.time() - start_time
            print(f"  Progress: {i}/{len(tasks)} ({elapsed:.0f}s elapsed)")
        
        result = fetch_pair(args)
        
        if "error" in result:
            network_errors.append(result)
        else:
            all_results.append(result)
        
        # Brief delay between requests
        if i < len(tasks) - 1:
            time.sleep(RATE_LIMIT_DELAY)
    
    elapsed = time.time() - start_time
    print(f"\n=== EXECUTION COMPLETE ===")
    print(f"Total paired samples: {len(all_results)}/{len(tasks)}")
    print(f"Network errors: {len(network_errors)}")
    print(f"Time elapsed: {elapsed:.0f}s")
    print(f"Time per sample: {elapsed/len(tasks):.1f}s" if tasks else "N/A")
    
    # Save raw evidence
    exp_dir = Path(__file__).parent
    raw_dir = exp_dir / "raw_evidence"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    with open(raw_dir / "experiment_data.json", "w") as f:
        json.dump(all_results, f, indent=2)
    with open(raw_dir / "network_errors.json", "w") as f:
        json.dump(network_errors, f, indent=2)
    
    # === COMPUTE METRICS ===
    print("\n=== COMPUTING METRICS ===")
    
    # Group by endpoint
    ep_results = defaultdict(list)
    for r in all_results:
        ep_results[r["endpoint"]].append(r)
    
    # Per-endpoint metrics
    per_endpoint = {}
    for name, results in ep_results.items():
        if len(results) < 2:
            continue
        bd = [r["behavioral_delta"] for r in results]
        sc = [r["structural_composite"] for r in results]
        r_val, ci = pearson_r(bd, sc)
        per_endpoint[name] = {
            "n": len(results),
            "r": round(r_val, 4),
            "ci_lower": round(ci[0], 4),
            "ci_upper": round(ci[1], 4),
            "bd_mean": round(statistics.mean(bd), 4),
            "bd_stdev": round(statistics.stdev(bd), 4) if len(bd) > 1 else 0,
            "sc_mean": round(statistics.mean(sc), 4),
            "sc_stdev": round(statistics.stdev(sc), 4) if len(sc) > 1 else 0,
            "has_variance": statistics.stdev(bd) > 0 and statistics.stdev(sc) > 0 if len(bd) > 1 and len(sc) > 1 else False,
        }
    
    # Pooled metrics
    all_bd = [r["behavioral_delta"] for r in all_results]
    all_sc = [r["structural_composite"] for r in all_results]
    pooled_r, pooled_ci = pearson_r(all_bd, all_sc)
    
    # TOST equivalence test at delta=0.15
    ci_upper = pooled_ci[1]
    tost_pass = ci_upper < 0.15
    
    # Decision rule evaluation
    c1_auth = []
    for r in all_results:
        if r.get("auth_status") is not None:
            c1_auth.append(r["auth_status"])
    auth_detection = sum(1 for s in c1_auth if s in (401, 403)) / len(c1_auth) if c1_auth else None
    
    # C1: Behavioral detection
    if auth_detection is not None:
        c1_pass = auth_detection >= 0.85
        c1_observed = f"auth_detection={auth_detection:.4f}"
    else:
        # Fallback: check behavioral variance
        bd_stdev = statistics.stdev(all_bd) if len(all_bd) > 1 else 0
        c1_pass = bd_stdev > 0
        c1_observed = f"behavioral_stdev={bd_stdev:.4f} (no auth probes)"
    
    # C2: Variance
    ep_with_var = sum(1 for v in per_endpoint.values() if v["has_variance"])
    c2_pass = ep_with_var >= 2
    c2_observed = f"{ep_with_var}/{len(per_endpoint)} endpoints"
    
    # C3: Equivalence
    c3_pass = tost_pass
    c3_observed = f"pooled_r={pooled_r:.4f}, CI=[{pooled_ci[0]:.4f}, {ci_upper:.4f}], upper={ci_upper:.4f}"
    
    # C4: Null control (FP rate)
    fp_count = sum(1 for r in all_results if r["behavioral_delta"] > 0.5)
    fp_rate = fp_count / len(all_results)
    c4_pass = fp_rate < 0.05
    c4_observed = f"FP_rate={fp_rate:.4f} ({fp_count}/{len(all_results)})"
    
    # C5: Network availability
    c5_pass = len(ep_results) >= 2
    c5_observed = f"{len(ep_results)}/{len(ENDPOINTS)} endpoints reached"
    
    all_pass = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass
    
    # Determine outcome
    if not c5_pass:
        outcome = "BLOCKED"
        decision = "C5_FAIL"
        verdict = "BLOCKED — network unavailable"
    elif all_pass:
        outcome = "SUPPORTS"
        decision = "ALL_PASS"
        verdict = "SUPPORTS — orthogonality transfers to real APIs"
    elif not c3_pass and ci_upper >= 0.20:
        outcome = "FALSIFIES"
        decision = "C3_FAIL_CI_UPPER_GTE_020"
        verdict = "FALSIFIES — signals correlated on real APIs"
    elif not c3_pass and ci_upper >= 0.15:
        outcome = "MIXED"
        decision = "C3_FAIL_CI_UPPER_015_TO_020"
        verdict = "MIXED — inconclusive, larger sample needed"
    elif not (c1_pass and c2_pass and c4_pass):
        outcome = "MEASUREMENT_INVALID"
        decision = "C1_OR_C2_OR_C4_FAIL"
        verdict = "MEASUREMENT_INVALID — behavioral extraction or variance insufficient"
    else:
        outcome = "MIXED"
        decision = "INCONCLUSIVE"
        verdict = "MIXED"
    
    status = "COMPLETE" if len(all_results) >= N_SAMPLES_PER_ENDPOINT * len(ENDPOINTS) * 0.5 else "MEASUREMENT_INVALID"
    
    metrics = {
        "pooled": {
            "pearson_r": round(pooled_r, 4),
            "ci_95_lower": round(pooled_ci[0], 4),
            "ci_95_upper": round(ci_upper, 4),
            "tost_pass": tost_pass,
            "n_samples": len(all_results),
            "fp_rate": round(fp_rate, 4),
            "fp_count": fp_count,
            "auth_detection_rate": round(auth_detection, 4) if auth_detection is not None else None,
            "rate_304": round(sum(1 for r in all_results if r.get("responded_304")) / len(all_results), 4) if all_results else 0,
            "mean_behavioral_delta": round(statistics.mean(all_bd), 4),
            "mean_structural_composite": round(statistics.mean(all_sc), 4),
            "behavioral_stdev": round(statistics.stdev(all_bd), 4) if len(all_bd) > 1 else 0,
            "structural_stdev": round(statistics.stdev(all_sc), 4) if len(all_sc) > 1 else 0,
        },
        "per_endpoint": per_endpoint,
        "decision_rule": {
            "C1_behavioral_detection": {"pass": c1_pass, "observed": c1_observed},
            "C2_variance": {"pass": c2_pass, "observed": c2_observed},
            "C3_equivalence": {"pass": c3_pass, "observed": c3_observed},
            "C4_null_control": {"pass": c4_pass, "observed": c4_observed},
            "C5_network_availability": {"pass": c5_pass, "observed": c5_observed},
        },
    }
    
    print(f"\n=== RESULTS ===")
    print(f"Status: {status}")
    print(f"Outcome: {outcome}")
    print(f"Decision: {decision}")
    print(f"Verdict: {verdict}")
    print(f"Pooled r: {pooled_r:.4f}, CI: [{pooled_ci[0]:.4f}, {ci_upper:.4f}]")
    print(f"TOST pass (CI upper < 0.15): {tost_pass}")
    print(f"FP rate: {fp_rate:.4f}")
    print(f"Auth detection: {auth_detection:.4f}" if auth_detection is not None else "Auth detection: N/A")
    print(f"304 rate: {metrics['pooled']['rate_304']:.4f}")
    print()
    for name, ep in per_endpoint.items():
        print(f"  {name}: r={ep['r']}, n={ep['n']}, has_var={ep['has_variance']}")
    print()
    for crit, details in metrics["decision_rule"].items():
        print(f"  {crit}: {'PASS' if details['pass'] else 'FAIL'} — {details['observed']}")
    
    # Save metrics
    with open(exp_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    return metrics, all_results, network_errors, status, outcome, decision, verdict

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2: return 0.0, (0.0, 1.0)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0 or den_y == 0: return 0.0, (0.0, 1.0)
    r = num / (den_x * den_y)
    if abs(r) >= 0.999: return r, (r, r)
    z = 0.5 * math.log((1 + r) / (1 - r))
    se = 1.0 / math.sqrt(n - 3)
    z_crit = 1.96
    ci_low = math.tanh(z - z_crit * se)
    ci_high = math.tanh(z + z_crit * se)
    return r, (ci_low, ci_high)

if __name__ == "__main__":
    metrics, all_results, network_errors, status, outcome, decision, verdict = main()
