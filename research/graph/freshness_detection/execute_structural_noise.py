#!/usr/bin/env python3
"""
EXP-GRAPH-34788722106 — Confirmatory test of adaptive Jaccard freshness threshold
under structural noise. Tests T(n)=1-0.8/(n+1) on schemas with 10-50 fields,
with 6 drift patterns (3 true drift + 3 structural noise).

The experiment operates on (field_path, type) pairs directly.
Fresh = identical field set (Jaccard=1.0 by construction).
Stale = modified field set per drift pattern.
"""

import json
import math
import hashlib
import random
import sys
from pathlib import Path
from datetime import datetime, timezone

# ============================================================
# CONSTANTS (frozen in spec.json)
# ============================================================

SCHEMA_SIZES = [10, 20, 30, 50]
SAMPLES_PER_GROUP = 30  # 30 fresh + 30 stale per drift pattern per size
DRIFT_PATTERNS_TRUE = ["add_field", "remove_field", "change_type"]
DRIFT_PATTERNS_NOISE = ["optional_field_churn", "null_valued_fields", "nested_object_variation"]
ALL_DRIFT_PATTERNS = DRIFT_PATTERNS_TRUE + DRIFT_PATTERNS_NOISE
FIELD_TYPES = ["string", "integer", "boolean", "array", "object"]
SEED = 20260913  # deterministic seed

# ============================================================
# ADAPTIVE THRESHOLD
# ============================================================

def adaptive_threshold(n):
    """T(n) = 1 - 0.8 / (n + 1)"""
    return 1.0 - 0.8 / (n + 1)

# ============================================================
# MOCK SCHEMA GENERATION
# ============================================================

def generate_baseline_schema(n, rng):
    """Generate n unique (field_path, type) pairs as baseline schema."""
    fields = []
    used_names = set()
    for i in range(n):
        while True:
            if rng.random() < 0.2 and i > 0:
                # Nested path (20% chance)
                parents = [f for f, _ in fields if "." not in f]
                if parents:
                    parent = rng.choice(parents)
                    suffix = f"sub_{rng.randint(1, 99)}"
                    path = f"{parent}.{suffix}"
                else:
                    path = f"field_{rng.randint(1, 9999)}"
            else:
                path = f"field_{rng.randint(1, 9999)}"
            if path not in used_names:
                used_names.add(path)
                break
        ftype = rng.choice(FIELD_TYPES)
        fields.append((path, ftype))
    return fields

def generate_fresh_schema(baseline, rng):
    """Generate fresh schema with identical (path, type) pairs. Jaccard=1.0 by construction."""
    return list(baseline)  # identical copy

def generate_stale_add_field(baseline, rng):
    """Add one new field (true drift)."""
    new_field = f"new_field_{rng.randint(1, 9999)}"
    new_type = rng.choice(FIELD_TYPES)
    return baseline + [(new_field, new_type)]

def generate_stale_remove_field(baseline, rng):
    """Remove one field (true drift)."""
    idx = rng.randint(0, len(baseline) - 1)
    return [f for i, f in enumerate(baseline) if i != idx]

def generate_stale_change_type(baseline, rng):
    """Change one field's type (true drift)."""
    idx = rng.randint(0, len(baseline) - 1)
    path, old_type = baseline[idx]
    new_type = rng.choice([t for t in FIELD_TYPES if t != old_type])
    result = list(baseline)
    result[idx] = (path, new_type)
    return result

def generate_stale_optional_churn(baseline, rng):
    """Randomly add/remove ~10% of fields (structural noise)."""
    n = len(baseline)
    churn_count = max(1, round(n * 0.1))
    result = list(baseline)
    # Remove churn_count fields
    indices_to_remove = sorted(rng.sample(range(len(result)), min(churn_count, len(result))), reverse=True)
    for idx in indices_to_remove:
        result.pop(idx)
    # Add churn_count new fields
    for _ in range(churn_count):
        new_field = f"churn_field_{rng.randint(1, 9999)}"
        new_type = rng.choice(FIELD_TYPES)
        result.append((new_field, new_type))
    return result

def generate_stale_null_fields(baseline, rng):
    """Set random fields to null type (structural noise)."""
    n = len(baseline)
    null_count = max(1, round(n * 0.1))
    indices = set(rng.sample(range(n), min(null_count, n)))
    return [("field_null", "null") if i in indices else (p, t) for i, (p, t) in enumerate(baseline)]

def generate_stale_nested_object(baseline, rng):
    """Convert a field to nested object (structural noise)."""
    idx = rng.randint(0, len(baseline) - 1)
    path, old_type = baseline[idx]
    # Replace with nested: original path becomes parent, add nested field
    nested_path = f"{path}.nested_child"
    result = list(baseline)
    result[idx] = (nested_path, "string")
    return result

DRIFT_GENERATORS = {
    "add_field": generate_stale_add_field,
    "remove_field": generate_stale_remove_field,
    "change_type": generate_stale_change_type,
    "optional_field_churn": generate_stale_optional_churn,
    "null_valued_fields": generate_stale_null_fields,
    "nested_object_variation": generate_stale_nested_object,
}

# ============================================================
# JACCARD SIMILARITY
# ============================================================

def jaccard_similarity(set_a, set_b):
    """Compute Jaccard similarity between two sets of (path, type) tuples."""
    a = set(set_a)
    b = set(set_b)
    if not a and not b:
        return 1.0
    intersection = a & b
    union = a | b
    return len(intersection) / len(union)

# ============================================================
# WILSON CI
# ============================================================

def wilson_ci(successes, n, z=1.96):
    """Wilson score interval for a proportion."""
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))

# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment():
    """Execute the full experiment and return raw evidence."""
    rng = random.Random(SEED)
    
    raw_evidence = {
        "experiment_id": "EXP-GRAPH-34788722106",
        "seed": SEED,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "per_schema_size": {},
    }
    
    for n in SCHEMA_SIZES:
        threshold = adaptive_threshold(n)
        size_evidence = {
            "schema_size": n,
            "threshold": round(threshold, 6),
            "fresh_similarities": [],
            "stale_similarities": {},
        }
        
        # Generate baseline schema for this size
        baseline = generate_baseline_schema(n, rng)
        size_evidence["baseline_schema"] = [list(f) for f in baseline]
        
        # Generate 30 fresh schemas (identical to baseline, Jaccard=1.0)
        for i in range(SAMPLES_PER_GROUP):
            fresh = generate_fresh_schema(baseline, rng)
            sim = jaccard_similarity(baseline, fresh)
            size_evidence["fresh_similarities"].append(round(sim, 6))
        
        # Generate 30 stale variants per drift pattern
        for pattern in ALL_DRIFT_PATTERNS:
            sims = []
            for i in range(SAMPLES_PER_GROUP):
                gen = DRIFT_GENERATORS[pattern]
                stale = gen(baseline, rng)
                sim = jaccard_similarity(baseline, stale)
                sims.append(round(sim, 6))
            size_evidence["stale_similarities"][pattern] = sims
        
        raw_evidence["per_schema_size"][str(n)] = size_evidence
    
    return raw_evidence

def compute_derived_measurements(raw_evidence):
    """Compute TP, FP, Wilson CIs, detection margins from raw evidence."""
    measurements = {
        "per_schema_size": {},
        "overall": {},
    }
    
    all_tp = 0
    all_tp_total = 0
    all_fp = 0
    all_fp_total = 0
    
    for n_str, size_data in raw_evidence["per_schema_size"].items():
        n = size_data["schema_size"]
        threshold = size_data["threshold"]
        
        # FP: fresh schemas where Jaccard < threshold (should be 0 since Jaccard=1.0)
        fresh_sims = size_data["fresh_similarities"]
        fp_count = sum(1 for s in fresh_sims if s < threshold)
        fp_total = len(fresh_sims)
        fp_rate = fp_count / fp_total if fp_total > 0 else 0.0
        fp_ci = wilson_ci(fp_count, fp_total)
        
        all_fp += fp_count
        all_fp_total += fp_total
        
        # TP per drift pattern
        pattern_metrics = {}
        for pattern in ALL_DRIFT_PATTERNS:
            sims = size_data["stale_similarities"][pattern]
            tp_count = sum(1 for s in sims if s < threshold)
            tp_total = len(sims)
            tp_rate = tp_count / tp_total if tp_total > 0 else 0.0
            tp_ci = wilson_ci(tp_count, tp_total)
            
            mean_sim = sum(sims) / len(sims) if sims else 0.0
            detection_margin = threshold - mean_sim
            
            pattern_metrics[pattern] = {
                "tp_count": tp_count,
                "tp_total": tp_total,
                "tp_rate": round(tp_rate, 4),
                "tp_ci_lower": round(tp_ci[0], 4),
                "tp_ci_upper": round(tp_ci[1], 4),
                "mean_jaccard": round(mean_sim, 6),
                "detection_margin": round(detection_margin, 6),
                "threshold": round(threshold, 6),
            }
            
            if pattern in DRIFT_PATTERNS_TRUE:
                all_tp += tp_count
                all_tp_total += tp_total
        
        # Aggregate TP across true drift patterns
        true_tp_rates = [pattern_metrics[p]["tp_rate"] for p in DRIFT_PATTERNS_TRUE]
        overall_tp_rate = sum(true_tp_rates) / len(true_tp_rates) if true_tp_rates else 0.0
        true_tp_ci = wilson_ci(all_tp, all_tp_total) if all_tp_total > 0 else (0.0, 1.0)
        
        # Aggregate FP across noise patterns
        noise_fp_details = {}
        total_noise_fp = 0
        total_noise_n = 0
        for pattern in DRIFT_PATTERNS_NOISE:
            sims = size_data["stale_similarities"][pattern]
            noise_fp = sum(1 for s in sims if s < threshold)
            noise_n = len(sims)
            noise_fp_details[pattern] = {
                "fp_count": noise_fp,
                "fp_total": noise_n,
                "fp_rate": round(noise_fp / noise_n, 4) if noise_n > 0 else 0.0,
            }
            total_noise_fp += noise_fp
            total_noise_n += noise_n
        
        overall_noise_fp_rate = total_noise_fp / total_noise_n if total_noise_n > 0 else 0.0
        overall_noise_fp_ci = wilson_ci(total_noise_fp, total_noise_n)
        
        measurements["per_schema_size"][str(n)] = {
            "threshold": round(threshold, 6),
            "fp_rate_fresh": round(fp_rate, 4),
            "fp_ci_fresh": [round(fp_ci[0], 4), round(fp_ci[1], 4)],
            "overall_tp_rate_true_drift": round(overall_tp_rate, 4),
            "overall_tp_ci_true_drift": [round(true_tp_ci[0], 4), round(true_tp_ci[1], 4)],
            "overall_noise_fp_rate": round(overall_noise_fp_rate, 4),
            "overall_noise_fp_ci": [round(overall_noise_fp_ci[0], 4), round(overall_noise_fp_ci[1], 4)],
            "per_pattern": pattern_metrics,
            "noise_pattern_details": noise_fp_details,
            "detection_margins": {
                p: round(threshold - sum(size_data["stale_similarities"][p]) / len(size_data["stale_similarities"][p]), 6)
                for p in ALL_DRIFT_PATTERNS
            },
        }
    
    # Overall metrics
    overall_tp_rate = all_tp / all_tp_total if all_tp_total > 0 else 0.0
    overall_tp_ci = wilson_ci(all_tp, all_tp_total)
    overall_fp_rate = all_fp / all_fp_total if all_fp_total > 0 else 0.0
    overall_fp_ci = wilson_ci(all_fp, all_fp_total)
    
    measurements["overall"] = {
        "total_true_stale_samples": all_tp_total,
        "total_true_detected": all_tp,
        "overall_tp_rate": round(overall_tp_rate, 4),
        "overall_tp_ci": [round(overall_tp_ci[0], 4), round(overall_tp_ci[1], 4)],
        "total_fresh_samples": all_fp_total,
        "total_fresh_fp": all_fp,
        "overall_fp_rate_fresh": round(overall_fp_rate, 4),
        "overall_fp_ci_fresh": [round(overall_fp_ci[0], 4), round(overall_fp_ci[1], 4)],
    }
    
    return measurements

def evaluate_decision_rule(measurements, raw_evidence):
    """Apply frozen decision rule from spec.json."""
    violations = []
    
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        
        # Condition 1: TP lower bound of 95% Wilson CI >= 0.8 across true drift patterns
        for pattern in DRIFT_PATTERNS_TRUE:
            p = size_data["per_pattern"][pattern]
            if p["tp_ci_lower"] < 0.8:
                violations.append(f"n={n} pattern={pattern}: TP CI lower bound {p['tp_ci_lower']} < 0.8")
        
        # Condition 2: FP upper bound of 95% Wilson CI <= 0.15 across noise patterns
        # Check fresh FP
        if size_data["fp_ci_fresh"][1] > 0.15:
            violations.append(f"n={n}: Fresh FP CI upper bound {size_data['fp_ci_fresh'][1]} > 0.15")
        
        # Check noise pattern FP (structural noise patterns should NOT be detected)
        for pattern in DRIFT_PATTERNS_NOISE:
            sims = raw_evidence["per_schema_size"][n_str]["stale_similarities"][pattern]
            threshold = size_data["threshold"]
            noise_fp = sum(1 for s in sims if s < threshold)
            noise_n = len(sims)
            noise_ci = wilson_ci(noise_fp, noise_n)
            if noise_ci[1] > 0.15:
                violations.append(f"n={n} pattern={pattern}: Noise FP CI upper bound {noise_ci[1]:.4f} > 0.15 (FP rate={noise_fp}/{noise_n}={noise_fp/noise_n:.4f})")
        
        # Condition 3: Detection margin positive for all drift patterns
        for pattern in ALL_DRIFT_PATTERNS:
            margin = size_data["detection_margins"][pattern]
            if margin <= 0:
                violations.append(f"n={n} pattern={pattern}: Detection margin {margin} <= 0")
        
        # Condition 4: Positive control - add_field TP >= 0.8
        add_field_tp = size_data["per_pattern"]["add_field"]["tp_rate"]
        if add_field_tp < 0.8:
            violations.append(f"n={n}: Positive control (add_field) TP {add_field_tp} < 0.8")
        
        # Condition 5: Null control - fresh FP = 0
        fresh_fp = size_data["fp_rate_fresh"]
        if fresh_fp > 0:
            violations.append(f"n={n}: Null control (fresh) FP {fresh_fp} > 0")
    
    if violations:
        return "FALSIFIED-IN-SETTING", violations
    else:
        return "SURVIVES_CURRENT_TEST", []

# ============================================================
# EXECUTION AND OUTPUT
# ============================================================

def main():
    print("=== EXP-GRAPH-34788722106: Adaptive Jaccard Threshold under Structural Noise ===")
    print(f"Schema sizes: {SCHEMA_SIZES}")
    print(f"Samples per group: {SAMPLES_PER_GROUP}")
    print(f"True drift patterns: {DRIFT_PATTERNS_TRUE}")
    print(f"Noise patterns: {DRIFT_PATTERNS_NOISE}")
    print()
    
    # Run experiment
    raw_evidence = run_experiment()
    
    # Compute derived measurements
    measurements = compute_derived_measurements(raw_evidence)
    
    # Evaluate decision
    decision, violations = evaluate_decision_rule(measurements, raw_evidence)
    
    print(f"Decision: {decision}")
    if violations:
        print(f"Violations ({len(violations)}):")
        for v in violations:
            print(f"  - {v}")
    print()
    
    # Print summary per schema size
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        threshold = size_data["threshold"]
        print(f"Schema size n={n}, threshold T(n)={threshold:.4f}")
        print(f"  Fresh FP rate: {size_data['fp_rate_fresh']:.4f} CI: {size_data['fp_ci_fresh']}")
        print(f"  True drift TP rate: {size_data['overall_tp_rate_true_drift']:.4f} CI: {size_data['overall_tp_ci_true_drift']}")
        print(f"  Noise FP rate: {size_data['overall_noise_fp_rate']:.4f} CI: {size_data['overall_noise_fp_ci']}")
        for pattern in ALL_DRIFT_PATTERNS:
            p = size_data["per_pattern"][pattern]
            marker = "*" if pattern in DRIFT_PATTERNS_TRUE else "#"
            print(f"  {marker} {pattern}: mean_jaccard={p['mean_jaccard']:.4f} detected={p['tp_count']}/{p['tp_total']} ({p['tp_rate']:.2f}) margin={p['detection_margin']:.4f}")
        print()
    
    print(f"Overall: TP={measurements['overall']['overall_tp_rate']:.4f} CI={measurements['overall']['overall_tp_ci']}")
    print(f"         FP(fresh)={measurements['overall']['overall_fp_rate_fresh']:.4f} CI={measurements['overall']['overall_fp_ci_fresh']}")
    print()
    
    # Save raw evidence
    exp_dir = Path(__file__).parent.parent.parent / "experiments" / "EXP-GRAPH-34788722106"
    raw_dir = exp_dir / "raw_evidence"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    with open(raw_dir / "mock_schemas.json", "w") as f:
        json.dump({
            "per_schema_size": {
                n: {
                    "baseline": raw_evidence["per_schema_size"][n]["baseline_schema"],
                    "fresh_similarities": raw_evidence["per_schema_size"][n]["fresh_similarities"],
                    "stale_similarities": raw_evidence["per_schema_size"][n]["stale_similarities"],
                }
                for n in [str(s) for s in SCHEMA_SIZES]
            }
        }, f, indent=2)
    
    with open(raw_dir / "derived_measurements.json", "w") as f:
        json.dump(measurements, f, indent=2)
    
    with open(raw_dir / "decision_evaluation.json", "w") as f:
        json.dump({
            "decision": decision,
            "violations": violations,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2)
    
    # Compute SHA256 of raw evidence for provenance
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
        "raw_evidence": raw_evidence,
        "measurements": measurements,
        "decision": decision,
        "violations": violations,
        "raw_hashes": raw_hashes,
    }

if __name__ == "__main__":
    result = main()
