#!/usr/bin/env python3
"""
EXP-GRAPH-35154724244 — Direct Schema Comparison for Drift-vs-Noise Discrimination
Execute frozen experiment: structural diff of JSON Schema definitions.

Tests whether direct schema comparison (field names, types, nesting depth,
required/optional status, enum constraints) provides reliable drift-vs-noise
discrimination that all five tested indirect signal families cannot.

Schema diff magnitude = weighted sum of structural changes:
  - 1.0 per added/removed field
  - 0.5 per type change
  - 0.3 per required→optional change
  - 0.2 per enum change
"""

import json
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
SAMPLES_PER_GROUP = 30  # 30 fresh + 30 stale per condition per size
SEED = 20260917  # deterministic seed per prereg

DRIFT_PATTERNS = ["add_field", "remove_field", "change_type", "required_to_optional", "rename_field"]
NOISE_PATTERNS = ["description_change", "default_value_change", "optional_field_addition",
                  "nested_property_addition", "enum_expansion"]
ALL_PATTERNS = DRIFT_PATTERNS + NOISE_PATTERNS

FIELD_TYPES = ["string", "integer", "boolean", "array", "object"]

# Schema diff weights (frozen in spec.json)
WEIGHT_ADDED_REMOVED = 1.0
WEIGHT_TYPE_CHANGE = 0.5
WEIGHT_REQUIRED_TO_OPTIONAL = 0.3
WEIGHT_ENUM_CHANGE = 0.2

# Client profiles with increasing validation strictness
CLIENT_PROFILES = {
    "A": {
        "description": "light validation: no validation, just requests fields",
        "validate_types": False,
        "validate_required": False,
        "validate_enums": False,
        "fields": {"id", "name"},
    },
    "B": {
        "description": "medium validation: type checking only",
        "validate_types": True,
        "validate_required": False,
        "validate_enums": False,
        "fields": {"id", "name", "email"},
    },
    "C": {
        "description": "heavy validation: type + required + enum",
        "validate_types": True,
        "validate_required": True,
        "validate_enums": True,
        "fields": {"id", "name", "email", "phone", "status"},
    },
}


# ============================================================
# JSON SCHEMA GENERATION
# ============================================================

def generate_baseline_schema(n, rng):
    """Generate a baseline JSON Schema definition of n fields.
    
    Each field is a dict with keys:
      - name: field name
      - type: one of FIELD_TYPES
      - required: bool
      - description: str
      - enum: list of valid values or None
      - nested: list of nested field dicts (for object type) or None
    """
    core_fields = [
        {"name": "id", "type": "integer", "required": True,
         "description": "Unique identifier", "enum": None, "nested": None},
        {"name": "name", "type": "string", "required": True,
         "description": "Display name", "enum": None, "nested": None},
        {"name": "email", "type": "string", "required": True,
         "description": "Contact email", "enum": None, "nested": None},
        {"name": "phone", "type": "string", "required": False,
         "description": "Phone number", "enum": None, "nested": None},
        {"name": "status", "type": "string", "required": True,
         "description": "Account status", "enum": ["active", "inactive", "pending"], "nested": None},
    ]
    fields = list(core_fields)
    used_names = {f["name"] for f in fields}

    i = len(fields)
    while len(fields) < n:
        fname = f"field_{i}"
        if fname not in used_names:
            used_names.add(fname)
            ftype = rng.choice(FIELD_TYPES)
            field = {
                "name": fname,
                "type": ftype,
                "required": rng.random() > 0.3,
                "description": f"Auto-generated field {fname}",
                "enum": ["val_a", "val_b", "val_c"] if ftype == "string" and rng.random() > 0.7 else None,
                "nested": [{"name": "sub_field", "type": "string"}] if ftype == "object" and rng.random() > 0.5 else None,
            }
            fields.append(field)
        i += 1
    return fields


def generate_fresh_schema(baseline, rng):
    """Fresh = identical to baseline."""
    return json.loads(json.dumps(baseline))  # deep copy


# ============================================================
# DRIFT PATTERN GENERATORS (true drift)
# ============================================================

def apply_add_field(baseline, rng):
    """Add one required field to the schema."""
    schema = json.loads(json.dumps(baseline))
    n = len(schema)
    new_field = {
        "name": f"new_drift_field_{rng.randint(1, 9999)}",
        "type": rng.choice(FIELD_TYPES),
        "required": True,
        "description": "New required field from drift",
        "enum": None,
        "nested": None,
    }
    schema.append(new_field)
    return schema


def apply_remove_field(baseline, rng):
    """Remove one required field from the schema."""
    schema = json.loads(json.dumps(baseline))
    required_fields = [i for i, f in enumerate(schema) if f["required"] and f["name"] not in {"id"}]
    if required_fields:
        idx = rng.choice(required_fields)
        schema.pop(idx)
    return schema


def apply_change_type(baseline, rng):
    """Change one field's type (e.g., integer → string)."""
    schema = json.loads(json.dumps(baseline))
    # Target a field that clients use (id, name, email, phone, status)
    target_names = {"id", "name", "email", "phone", "status"}
    targetable = [(i, f) for i, f in enumerate(schema) if f["name"] in target_names]
    if targetable:
        idx, field = rng.choice(targetable)
    else:
        idx = rng.randint(0, len(schema) - 1)
        field = schema[idx]
    old_type = field["type"]
    new_type = rng.choice([t for t in FIELD_TYPES if t != old_type])
    schema[idx]["type"] = new_type
    return schema


def apply_required_to_optional(baseline, rng):
    """Move one required field to optional."""
    schema = json.loads(json.dumps(baseline))
    required_fields = [i for i, f in enumerate(schema) if f["required"] and f["name"] not in {"id"}]
    if required_fields:
        idx = rng.choice(required_fields)
        schema[idx]["required"] = False
    return schema


def apply_rename_field(baseline, rng):
    """Rename one field (keeping type)."""
    schema = json.loads(json.dumps(baseline))
    # Don't rename core fields
    core_names = {"id", "name", "email", "phone", "status"}
    renameable = [(i, f) for i, f in enumerate(schema) if f["name"] not in core_names]
    if renameable:
        idx, field = rng.choice(renameable)
        old_name = field["name"]
        new_name = f"renamed_{old_name}_{rng.randint(1, 999)}"
        schema[idx]["name"] = new_name
        # Update description to include old name for traceability
        schema[idx]["description"] = f"Renamed from {old_name}"
    return schema


DRIFT_GENERATORS = {
    "add_field": apply_add_field,
    "remove_field": apply_remove_field,
    "change_type": apply_change_type,
    "required_to_optional": apply_required_to_optional,
    "rename_field": apply_rename_field,
}


# ============================================================
# NOISE PATTERN GENERATORS (structural noise, redesigned to overlap
# with client-requested fields — fixing V_NOISE_TAUTOLOGICAL)
# ============================================================

def apply_description_change(baseline, rng):
    """Change description of a used field."""
    schema = json.loads(json.dumps(baseline))
    used_names = {"id", "name", "email", "phone", "status"}
    targetable = [(i, f) for i, f in enumerate(schema) if f["name"] in used_names]
    if targetable:
        idx, field = rng.choice(targetable)
        schema[idx]["description"] = f"Updated description for {field['name']} at {rng.randint(1,9999)}"
    return schema


def apply_default_value_change(baseline, rng):
    """Change default value metadata of a used field."""
    schema = json.loads(json.dumps(baseline))
    used_names = {"id", "name", "email", "phone", "status"}
    targetable = [(i, f) for i, f in enumerate(schema) if f["name"] in used_names]
    if targetable:
        idx, field = rng.choice(targetable)
        # Add/change default value in description (noise at metadata level)
        schema[idx]["description"] = f"{field['description']} [default: {rng.randint(0,999)}]"
    return schema


def apply_optional_field_addition(baseline, rng):
    """Add optional fields that may be used by heavy client."""
    schema = json.loads(json.dumps(baseline))
    n = len(schema)
    add_count = max(1, round(n * 0.1))
    for _ in range(add_count):
        new_field = {
            "name": f"opt_{rng.randint(1, 9999)}",
            "type": rng.choice(FIELD_TYPES),
            "required": False,
            "description": "Optional addition",
            "enum": None,
            "nested": None,
        }
        schema.append(new_field)
    return schema


def apply_nested_property_addition(baseline, rng):
    """Add nested properties to existing object fields."""
    schema = json.loads(json.dumps(baseline))
    # Find object-type fields or any field to nest under
    available = [i for i, f in enumerate(schema) if f["name"] not in {"id", "name"}]
    if available:
        idx = rng.choice(available)
        parent_name = schema[idx]["name"]
        if schema[idx]["nested"] is None:
            schema[idx]["nested"] = []
        schema[idx]["nested"].append({
            "name": f"nested_{rng.randint(1, 999)}",
            "type": "string",
        })
    return schema


def apply_enum_expansion(baseline, rng):
    """Add extra enum values to a used field."""
    schema = json.loads(json.dumps(baseline))
    used_names = {"id", "name", "email", "phone", "status"}
    targetable = [(i, f) for i, f in enumerate(schema)
                  if f["name"] in used_names and f["enum"] is not None]
    if not targetable:
        # Fallback: add enum to any string field without enum
        targetable = [(i, f) for i, f in enumerate(schema)
                      if f["name"] in used_names and f["type"] == "string"]
    if targetable:
        idx, field = rng.choice(targetable)
        if field["enum"] is None:
            schema[idx]["enum"] = ["val_a", "val_b"]
        schema[idx]["enum"] = list(schema[idx]["enum"]) + [f"extra_{rng.randint(1,999)}"]
    return schema


NOISE_GENERATORS = {
    "description_change": apply_description_change,
    "default_value_change": apply_default_value_change,
    "optional_field_addition": apply_optional_field_addition,
    "nested_property_addition": apply_nested_property_addition,
    "enum_expansion": apply_enum_expansion,
}


# ============================================================
# SCHEMA DIFF COMPUTATION
# ============================================================

def compute_schema_diff(fresh_schema, stale_schema):
    """Compute weighted structural diff between two schema definitions.
    
    Returns:
      - diff_magnitude: weighted sum of changes
      - diff_details: dict with counts of each change type
    """
    fresh_fields = {f["name"]: f for f in fresh_schema}
    stale_fields = {f["name"]: f for f in stale_schema}
    
    fresh_names = set(fresh_fields.keys())
    stale_names = set(stale_fields.keys())
    
    added = stale_names - fresh_names
    removed = fresh_names - stale_names
    common = fresh_names & stale_names
    
    type_changes = 0
    required_to_optional_changes = 0
    enum_changes = 0
    
    for name in common:
        fresh_f = fresh_fields[name]
        stale_f = stale_fields[name]
        
        # Type change
        if fresh_f["type"] != stale_f["type"]:
            type_changes += 1
        
        # Required → optional change
        if fresh_f["required"] and not stale_f["required"]:
            required_to_optional_changes += 1
        
        # Enum change
        fresh_enum = set(fresh_f["enum"]) if fresh_f["enum"] else set()
        stale_enum = set(stale_f["enum"]) if stale_f["enum"] else set()
        if fresh_enum != stale_enum:
            enum_changes += 1
    
    magnitude = (
        len(added) * WEIGHT_ADDED_REMOVED +
        len(removed) * WEIGHT_ADDED_REMOVED +
        type_changes * WEIGHT_TYPE_CHANGE +
        required_to_optional_changes * WEIGHT_REQUIRED_TO_OPTIONAL +
        enum_changes * WEIGHT_ENUM_CHANGE
    )
    
    return magnitude, {
        "added_fields": len(added),
        "removed_fields": len(removed),
        "type_changes": type_changes,
        "required_to_optional_changes": required_to_optional_changes,
        "enum_changes": enum_changes,
        "total_fresh_fields": len(fresh_fields),
        "total_stale_fields": len(stale_fields),
    }


# ============================================================
# JACCARD STRUCTURAL SIMILARITY (baseline)
# ============================================================

def compute_jaccard_structural(fresh_schema, stale_schema):
    """Compute Jaccard similarity on (field_path, type) pairs."""
    fresh_pairs = {(f["name"], f["type"]) for f in fresh_schema}
    stale_pairs = {(f["name"], f["type"]) for f in stale_schema}
    intersection = fresh_pairs & stale_pairs
    union = fresh_pairs | stale_pairs
    return len(intersection) / len(union) if union else 1.0


# ============================================================
# CLIENT VALIDATION (type-aware)
# ============================================================

def validate_client_request(schema_fields, profile, response_data):
    """Simulate client validation. Returns fraction of requests failing validation.
    
    For profile C (heavy): validates types, required fields, and enum constraints.
    """
    schema_map = {f["name"]: f for f in schema_fields}
    failures = 0
    total = 0
    
    for field_name in profile["fields"]:
        if field_name not in schema_map:
            # Field missing from schema — validation failure for required
            if profile.get("validate_required", False):
                failures += 1
            total += 1
            continue
        
        field_schema = schema_map[field_name]
        
        # Type validation
        if profile.get("validate_types", False):
            # Simulate: if type changed, validation fails
            expected_type = field_schema["type"]
            # In our mock, response data always matches schema type
            # The validation check is: does the client EXPECT a different type?
            # We check if the field exists with a compatible type
            if field_name in response_data:
                val = response_data[field_name]
                type_ok = True
                if expected_type == "integer" and not isinstance(val, int):
                    type_ok = False
                elif expected_type == "string" and not isinstance(val, str):
                    type_ok = False
                elif expected_type == "boolean" and not isinstance(val, bool):
                    type_ok = False
                elif expected_type == "array" and not isinstance(val, list):
                    type_ok = False
                elif expected_type == "object" and not isinstance(val, dict):
                    type_ok = False
                if not type_ok:
                    failures += 1
            else:
                # Field missing from response
                failures += 1
        
        # Required validation
        if profile.get("validate_required", False) and field_schema["required"]:
            if field_name not in response_data:
                failures += 1
        
        # Enum validation
        if profile.get("validate_enums", False) and field_schema.get("enum"):
            if field_name in response_data:
                val = response_data[field_name]
                if val not in field_schema["enum"]:
                    failures += 1
        
        total += 1
    
    return failures / total if total > 0 else 0.0


def build_response_data(schema_fields, resource_id):
    """Build deterministic response data from schema fields."""
    data = {}
    for field in schema_fields:
        name = field["name"]
        ftype = field["type"]
        if ftype == "integer":
            data[name] = resource_id
        elif ftype == "string":
            if field.get("enum"):
                data[name] = field["enum"][0]
            else:
                data[name] = f"{name}_{resource_id}"
        elif ftype == "boolean":
            data[name] = True
        elif ftype == "array":
            data[name] = [resource_id]
        elif ftype == "object":
            data[name] = {"value": resource_id}
    return data


# ============================================================
# EXPERIMENT EXECUTION
# ============================================================

def run_single_condition(baseline_schema, pattern, size, sample_idx, rng):
    """Run one (pattern, size, sample_idx) condition.
    
    Returns dict with schema_diff_magnitude, jaccard, diff_details, validation_rates.
    """
    # Generate fresh and stale schemas
    fresh = generate_fresh_schema(baseline_schema, rng)
    
    if pattern in DRIFT_GENERATORS:
        stale = DRIFT_GENERATORS[pattern](baseline_schema, rng)
    else:
        stale = NOISE_GENERATORS[pattern](baseline_schema, rng)
    
    # Schema diff magnitude
    diff_mag, diff_details = compute_schema_diff(fresh, stale)
    
    # Jaccard structural similarity (baseline)
    jaccard = compute_jaccard_structural(fresh, stale)
    
    # Client validation failure rates
    validation_rates = {}
    for profile_id, profile in CLIENT_PROFILES.items():
        # Build response data from stale schema
        response_data = build_response_data(stale, sample_idx + 1)
        fail_rate = validate_client_request(stale, profile, response_data)
        validation_rates[profile_id] = fail_rate
    
    return {
        "schema_diff_magnitude": round(diff_mag, 6),
        "jaccard": round(jaccard, 6),
        "diff_details": diff_details,
        "validation_rates": validation_rates,
        "fresh_field_count": len(fresh),
        "stale_field_count": len(stale),
    }


def run_experiment():
    """Execute the full experiment across all conditions."""
    rng = random.Random(SEED)
    
    raw_evidence = {
        "experiment_id": "EXP-GRAPH-35154724244",
        "seed": SEED,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "client_profiles": {k: {
            "fields": sorted(v["fields"]),
            "description": v["description"],
            "validate_types": v["validate_types"],
            "validate_required": v["validate_required"],
            "validate_enums": v["validate_enums"],
        } for k, v in CLIENT_PROFILES.items()},
        "per_schema_size": {},
    }
    
    for n in SCHEMA_SIZES:
        print(f"  Schema size n={n}...")
        baseline = generate_baseline_schema(n, rng)
        
        size_evidence = {
            "schema_size": n,
            "baseline_field_count": len(baseline),
            "conditions": {},
        }
        
        for pattern in ALL_PATTERNS:
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
    
    all_diff_mags = []
    all_jaccards = []
    all_conditions = []  # (diff_mag, jaccard) per condition
    
    for n_str, size_data in raw_evidence["per_schema_size"].items():
        n = size_data["schema_size"]
        pattern_metrics = {}
        
        for pattern in ALL_PATTERNS:
            results = size_data["conditions"][pattern]
            diff_mags = [r["schema_diff_magnitude"] for r in results]
            jaccards = [r["jaccard"] for r in results]
            
            mean_diff = sum(diff_mags) / len(diff_mags) if diff_mags else 0.0
            mean_jaccard = sum(jaccards) / len(jaccards) if jaccards else 0.0
            
            # Validation rates per profile
            profile_val_rates = defaultdict(list)
            for r in results:
                for pid, rate in r["validation_rates"].items():
                    profile_val_rates[pid].append(rate)
            mean_val_rates = {
                pid: round(sum(vals) / len(vals), 6) if vals else 0.0
                for pid, vals in profile_val_rates.items()
            }
            
            pattern_metrics[pattern] = {
                "mean_schema_diff_magnitude": round(mean_diff, 6),
                "mean_jaccard": round(mean_jaccard, 6),
                "std_schema_diff_magnitude": round(
                    (sum((d - mean_diff)**2 for d in diff_mags) / len(diff_mags))**0.5
                    if len(diff_mags) > 1 else 0.0, 6
                ),
                "mean_validation_rates": mean_val_rates,
                "n_samples": len(results),
            }
            
            all_diff_mags.append(mean_diff)
            all_jaccards.append(mean_jaccard)
            all_conditions.append((mean_diff, mean_jaccard))
        
        measurements["per_schema_size"][str(n)] = {
            "pattern_metrics": pattern_metrics,
        }
    
    # Overall metrics
    drift_diffs = []
    noise_diffs = []
    for n_str, size_data in measurements["per_schema_size"].items():
        for pattern in DRIFT_PATTERNS:
            drift_diffs.append(size_data["pattern_metrics"][pattern]["mean_schema_diff_magnitude"])
        for pattern in NOISE_PATTERNS:
            noise_diffs.append(size_data["pattern_metrics"][pattern]["mean_schema_diff_magnitude"])
    
    drift_diff_mean = sum(drift_diffs) / len(drift_diffs) if drift_diffs else 0.0
    noise_diff_mean = sum(noise_diffs) / len(noise_diffs) if noise_diffs else 0.0
    discrimination_gap = drift_diff_mean - noise_diff_mean
    
    # Pearson correlation between schema_diff_magnitude and Jaccard
    if len(all_conditions) >= 2:
        n_cond = len(all_conditions)
        mean_d = sum(c[0] for c in all_conditions) / n_cond
        mean_j = sum(c[1] for c in all_conditions) / n_cond
        cov = sum((c[0] - mean_d) * (c[1] - mean_j) for c in all_conditions) / n_cond
        std_d = (sum((c[0] - mean_d)**2 for c in all_conditions) / n_cond)**0.5
        std_j = (sum((c[1] - mean_j)**2 for c in all_conditions) / n_cond)**0.5
        pearson_r = cov / (std_d * std_j) if std_d > 0 and std_j > 0 else 0.0
    else:
        pearson_r = 0.0
    
    # Type-aware validation: profile C detection rate for change_type vs noise
    type_aware_detection = {}
    for n_str, size_data in measurements["per_schema_size"].items():
        # change_type detection
        ct_metrics = size_data["pattern_metrics"].get("change_type", {})
        ct_val = ct_metrics.get("mean_validation_rates", {}).get("C", 0.0)
        
        # noise detection (mean across all noise patterns)
        noise_vals = []
        for pattern in NOISE_PATTERNS:
            pm = size_data["pattern_metrics"].get(pattern, {})
            noise_vals.append(pm.get("mean_validation_rates", {}).get("C", 0.0))
        noise_mean_val = sum(noise_vals) / len(noise_vals) if noise_vals else 0.0
        
        type_aware_detection[str(n)] = {
            "change_type_C_validation_rate": round(ct_val, 6),
            "noise_mean_C_validation_rate": round(noise_mean_val, 6),
        }
    
    measurements["overall"] = {
        "drift_diff_mean": round(drift_diff_mean, 6),
        "noise_diff_mean": round(noise_diff_mean, 6),
        "discrimination_gap": round(discrimination_gap, 6),
        "pearson_r_diff_vs_jaccard": round(pearson_r, 6),
        "n_conditions": len(all_conditions),
        "type_aware_detection": type_aware_detection,
    }
    
    return measurements


# ============================================================
# DECISION RULE (frozen in spec.json)
# ============================================================

def evaluate_decision_rule(measurements):
    """Apply frozen decision rule.
    
    SURVIVES_CURRENT_TEST if and only if ALL FOUR conditions hold:
    1. Drift detection: EVERY drift pattern at EVERY size -> mean diff > 0.0
    2. Noise tolerance: EVERY noise pattern at EVERY size -> mean diff <= 0.5
    3. Orthogonality: Pearson r between diff and Jaccard < 0.90
    4. Type-aware: Profile C change_type rate > 0.8, noise rate < 0.1
    """
    violations = []
    condition_pass = {}
    
    # Condition 1: Drift detection
    c1_pass = True
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        for pattern in DRIFT_PATTERNS:
            pm = size_data["pattern_metrics"][pattern]
            if pm["mean_schema_diff_magnitude"] <= 0.0:
                violations.append(
                    f"C1 FAIL: n={n} pattern={pattern}: "
                    f"mean_diff={pm['mean_schema_diff_magnitude']:.6f} <= 0.0"
                )
                c1_pass = False
    condition_pass["C1_drift_detection"] = "PASS" if c1_pass else "FAIL"
    
    # Condition 2: Noise tolerance
    c2_pass = True
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        for pattern in NOISE_PATTERNS:
            pm = size_data["pattern_metrics"][pattern]
            if pm["mean_schema_diff_magnitude"] > 0.5:
                violations.append(
                    f"C2 FAIL: n={n} pattern={pattern}: "
                    f"mean_diff={pm['mean_schema_diff_magnitude']:.6f} > 0.5"
                )
                c2_pass = False
    condition_pass["C2_noise_tolerance"] = "PASS" if c2_pass else "FAIL"
    
    # Condition 3: Orthogonality
    pearson_r = measurements["overall"]["pearson_r_diff_vs_jaccard"]
    c3_pass = pearson_r < 0.90
    if not c3_pass:
        violations.append(
            f"C3 FAIL: Pearson r={pearson_r:.6f} >= 0.90 (signals redundant)"
        )
    condition_pass["C3_orthogonality"] = "PASS" if c3_pass else "FAIL"
    
    # Condition 4: Type-aware validation
    c4_pass = True
    type_det = measurements["overall"]["type_aware_detection"]
    for n_str, td in type_det.items():
        n = int(n_str)
        ct_rate = td["change_type_C_validation_rate"]
        noise_rate = td["noise_mean_C_validation_rate"]
        if ct_rate <= 0.8:
            violations.append(
                f"C4 FAIL: n={n}: change_type C validation rate {ct_rate:.6f} <= 0.8"
            )
            c4_pass = False
        if noise_rate >= 0.1:
            violations.append(
                f"C4 FAIL: n={n}: noise mean C validation rate {noise_rate:.6f} >= 0.1"
            )
            c4_pass = False
    condition_pass["C4_type_aware"] = "PASS" if c4_pass else "FAIL"
    
    all_pass = c1_pass and c2_pass and c3_pass and c4_pass
    decision = "SURVIVES_CURRENT_TEST" if all_pass else "FALSIFIED-IN-SETTING"
    
    return decision, violations, condition_pass


# ============================================================
# MAIN
# ============================================================

def main():
    print("=== EXP-GRAPH-35154724244: Direct Schema Comparison Experiment ===")
    print(f"Schema sizes: {SCHEMA_SIZES}")
    print(f"Samples per group: {SAMPLES_PER_GROUP}")
    print(f"Drift patterns: {DRIFT_PATTERNS}")
    print(f"Noise patterns: {NOISE_PATTERNS}")
    print(f"Client profiles: {list(CLIENT_PROFILES.keys())}")
    print()
    
    # Run experiment
    print("Running experiment...")
    raw_evidence = run_experiment()
    
    # Compute derived measurements
    print("Computing derived measurements...")
    measurements = compute_derived_measurements(raw_evidence)
    
    # Evaluate decision
    decision, violations, condition_pass = evaluate_decision_rule(measurements)
    
    print(f"\nDecision: {decision}")
    if violations:
        print(f"Violations ({len(violations)}):")
        for v in violations:
            print(f"  - {v}")
    print()
    
    # Print summary
    overall = measurements["overall"]
    print(f"Overall metrics:")
    print(f"  Drift diff mean: {overall['drift_diff_mean']:.6f} (must be > 0.0)")
    print(f"  Noise diff mean: {overall['noise_diff_mean']:.6f} (must be <= 0.5)")
    print(f"  Discrimination gap: {overall['discrimination_gap']:.6f}")
    print(f"  Pearson r (diff vs Jaccard): {overall['pearson_r_diff_vs_jaccard']:.6f} (must be < 0.90)")
    print()
    
    for n_str, size_data in measurements["per_schema_size"].items():
        n = int(n_str)
        print(f"Schema size n={n}:")
        for pattern in ALL_PATTERNS:
            pm = size_data["pattern_metrics"][pattern]
            marker = "*" if pattern in DRIFT_PATTERNS else "#"
            print(f"  {marker} {pattern}: diff={pm['mean_schema_diff_magnitude']:.4f} "
                  f"jaccard={pm['mean_jaccard']:.4f} "
                  f"val_rates={pm['mean_validation_rates']}")
        print()
    
    # Save raw evidence
    exp_dir = Path(__file__).parent.parent.parent / "experiments" / "EXP-GRAPH-35154724244"
    raw_dir = exp_dir / "raw_evidence"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Save summary version (full raw would be too large)
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
            "baseline_field_count": size_data["baseline_field_count"],
            "conditions_summary": {},
        }
        for pattern, results in size_data["conditions"].items():
            raw_summary["per_schema_size"][n_str]["conditions_summary"][pattern] = {
                "n_samples": len(results),
                "schema_diff_magnitudes": [r["schema_diff_magnitude"] for r in results],
                "jaccards": [r["jaccard"] for r in results],
                "validation_rates": [r["validation_rates"] for r in results],
                "diff_details_sample": results[0]["diff_details"] if results else {},
            }
    
    with open(raw_dir / "experiment_data.json", "w") as f:
        json.dump(raw_summary, f, indent=2)
    
    with open(raw_dir / "derived_measurements.json", "w") as f:
        json.dump(measurements, f, indent=2)
    
    with open(raw_dir / "decision_evaluation.json", "w") as f:
        json.dump({
            "decision": decision,
            "violations": violations,
            "condition_pass": condition_pass,
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
        "condition_pass": condition_pass,
        "raw_hashes": raw_hashes,
    }


if __name__ == "__main__":
    result = main()
