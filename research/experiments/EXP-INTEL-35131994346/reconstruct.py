#!/usr/bin/env python3
"""
EXP-INTEL-35131994346: Reconstruction of the 3-definition per-role-filtered analysis.

Attempts to reproduce the stored analysis_results.json from EXP-INTEL-35124660457
by reconstructing the uncommitted script that produced it.
"""

import json
import numpy as np
from collections import Counter
from pathlib import Path
import hashlib

RAW_DATA = Path("research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json")
STORED_RESULTS = Path("research/experiments/EXP-INTEL-35124660457/analysis_results.json")
OUTPUT_DIR = Path("research/experiments/EXP-INTEL-35131994346")

# 3-definition role mapping (as described in the hypothesis)
DEFINITIONS = {
    'DEF-FULL-MAP': {'roles': ['a', 'button', 'input', 'combobox'], 'description': 'Full interactive map'},
    'DEF-FORM-ONLY': {'roles': ['button', 'combobox'], 'description': 'Form elements only'},
    'ISOLATED-A-LINK': {'roles': ['a'], 'description': 'Links only'},
}


def load_data():
    """Load raw evidence and filter to valid measurements."""
    with open(RAW_DATA) as f:
        data = json.load(f)
    valid = [m for m in data['measurements'] if m.get('dom_stats') and m.get('locatable_elements')]
    return valid


def deduplicate_tasks(measurements):
    """Remove duplicate cart_1 entries (keep first occurrence)."""
    seen = set()
    unique = []
    duplicates = []
    for m in measurements:
        task_id = m['task_id']
        if task_id not in seen:
            seen.add(task_id)
            unique.append(m)
        else:
            duplicates.append(task_id)
    return unique, duplicates


def compute_truncated_count(measurement, definition_roles):
    """Count elements matching definition roles in the first-20 locatable_sample."""
    role_counts = Counter(e['role'] for e in measurement['locatable_sample'])
    return sum(role_counts.get(r, 0) for r in definition_roles)


def compute_full_count(measurement, definition_roles):
    """
    Estimate full-DOM count for definition roles.
    For roles with direct DOM equivalents, use DOM tag counts.
    For others, scale truncated-sample counts proportionally.
    """
    ds = measurement['dom_stats']
    locatable = measurement['locatable_elements']
    sample_count = len(measurement['locatable_sample'])

    # DOM tag mapping for roles with direct equivalents
    dom_mapping = {
        'a': ds['linksCount'],
        'button': ds['buttonsCount'],
        'form': ds['formsCount'],
        'input': ds['inputsCount'],
    }

    # Sample role counts for scaling
    sample_roles = Counter(e['role'] for e in measurement['locatable_sample'])
    scale_factor = locatable / sample_count if sample_count > 0 else 1

    full_estimates = {}
    for role in definition_roles:
        if role in dom_mapping:
            full_estimates[role] = dom_mapping[role]
        else:
            # Scale from sample
            full_estimates[role] = sample_roles.get(role, 0) * scale_factor

    return sum(full_estimates.values())


def compute_density(count, elements_with_bbox):
    """Compute density: count / elements_with_bbox."""
    return count / elements_with_bbox if elements_with_bbox > 0 else 0


def compute_ordering(density_by_page_type):
    """Sort page types by density (descending)."""
    return sorted(density_by_page_type.keys(), key=lambda x: density_by_page_type[x], reverse=True)


def random_baseline(measurement, definition_roles, n_simulations=1000, seed=42):
    """
    Random baseline: simulate random 20-element draws from the full DOM distribution.
    This matches the committed script's approach.
    """
    rng = np.random.RandomState(seed)
    locatable = measurement['locatable_elements']
    sample_count = len(measurement['locatable_sample'])
    elements_with_bbox = measurement['elements_with_bbox']

    if locatable < sample_count:
        return None

    # Full DOM estimates (same as committed script)
    ds = measurement['dom_stats']
    sample_roles = Counter(e['role'] for e in measurement['locatable_sample'])
    scale_factor = locatable / sample_count if sample_count > 0 else 1

    full_estimates = {
        'a': ds['linksCount'],
        'button': ds['buttonsCount'],
        'form': ds['formsCount'],
        'input': ds['inputsCount'],
    }
    for role in ['combobox', 'div', 'label', 'span']:
        full_estimates[role] = int(sample_roles.get(role, 0) * scale_factor)

    # Full density for definition roles
    full_count_def = sum(full_estimates.get(r, 0) for r in definition_roles)
    full_density = compute_density(full_count_def, elements_with_bbox)

    # Probability distribution from full DOM estimates (all roles)
    roles = list(full_estimates.keys())
    counts = np.array([full_estimates[r] for r in roles], dtype=float)
    total = counts.sum()
    if total == 0:
        return None
    probs = counts / total

    biases = []
    for _ in range(n_simulations):
        drawn = rng.choice(len(roles), size=sample_count, replace=True, p=probs)
        sim_counts = Counter()
        for idx in drawn:
            sim_counts[roles[idx]] += 1

        sim_count_def = sum(sim_counts.get(r, 0) for r in definition_roles)
        sim_density = compute_density(sim_count_def, elements_with_bbox)
        abs_bias = abs(sim_density - full_density)
        biases.append(abs_bias)

    return {
        'mean_abs_bias': float(np.mean(biases)),
        'all_lower': None,  # Will be filled in comparison
    }


def run_reconstruction():
    """Run the full reconstruction attempt."""
    measurements = load_data()
    unique_measurements, duplicates = deduplicate_tasks(measurements)

    print(f"Loaded {len(measurements)} valid measurements")
    print(f"After deduplication: {len(unique_measurements)} unique tasks")
    print(f"Duplicates removed: {duplicates}")
    print()

    # Load stored results for comparison
    with open(STORED_RESULTS) as f:
        stored = json.load(f)

    results = {}
    for def_name, def_info in DEFINITIONS.items():
        print(f"=== {def_name} ({def_info['description']}) ===")
        print(f"  Roles: {def_info['roles']}")

        def_tasks = []
        truncated_densities = {}
        full_densities = {}

        for m in unique_measurements:
            task_id = m['task_id']
            page_type = m['page_type']
            ewb = m['elements_with_bbox']

            trunc_count = compute_truncated_count(m, def_info['roles'])
            full_count = compute_full_count(m, def_info['roles'])

            trunc_density = compute_density(trunc_count, ewb)
            full_density = compute_density(full_count, ewb)

            abs_bias = abs(full_density - trunc_density)
            rel_bias = abs_bias / full_density if full_density > 0 else 0

            def_tasks.append({
                'task_id': task_id,
                'page_type': page_type,
                'locatable_elements': m['locatable_elements'],
                'ewb': ewb,
                'truncated_count': trunc_count,
                'full_count': full_count,
                'truncated_density': trunc_density,
                'full_density': full_density,
                'abs_bias': abs_bias,
                'rel_bias': rel_bias,
            })

            if page_type not in truncated_densities:
                truncated_densities[page_type] = []
                full_densities[page_type] = []
            truncated_densities[page_type].append(trunc_density)
            full_densities[page_type].append(full_density)

            # Compare with stored
            stored_task = None
            for st in stored['definitions'][def_name]['tasks']:
                if st['task_id'] == task_id:
                    stored_task = st
                    break

            if stored_task:
                trunc_match = abs(trunc_density - stored_task['truncated_density']) < 0.001
                full_match = abs(full_density - stored_task['full_density']) < 0.001
                match_str = "MATCH" if (trunc_match and full_match) else "MISMATCH"
                print(f"  {task_id}: trunc={trunc_density:.6f} (stored={stored_task['truncated_density']:.6f}) "
                      f"full={full_density:.6f} (stored={stored_task['full_density']:.6f}) [{match_str}]")
            else:
                print(f"  {task_id}: trunc={trunc_density:.6f} full={full_density:.6f} [NOT IN STORED]")

        # Compute ordering
        truncated_avg = {pt: float(np.mean(v)) for pt, v in truncated_densities.items()}
        full_avg = {pt: float(np.mean(v)) for pt, v in full_densities.items()}

        truncated_ordering = compute_ordering(truncated_avg)
        full_ordering = compute_ordering(full_avg)
        ordering_changed = truncated_ordering != full_ordering

        # Compare ordering with stored
        stored_ordering = stored['definitions'][def_name]
        trunc_order_match = truncated_ordering == stored_ordering['truncated_ordering']
        full_order_match = full_ordering == stored_ordering['full_ordering']

        print(f"\n  Truncated ordering: {truncated_ordering} (stored: {stored_ordering['truncated_ordering']})")
        print(f"  Full ordering: {full_ordering} (stored: {stored_ordering['full_ordering']})")
        print(f"  Ordering changed: {ordering_changed} (stored: {stored_ordering['ordering_changed']})")
        print(f"  Trunc order match: {trunc_order_match}, Full order match: {full_order_match}")

        results[def_name] = {
            'tasks': def_tasks,
            'truncated_avg': truncated_avg,
            'full_avg': full_avg,
            'truncated_ordering': truncated_ordering,
            'full_ordering': full_ordering,
            'ordering_changed': ordering_changed,
        }
        print()

    return results


if __name__ == '__main__':
    results = run_reconstruction()
    
    # Save reconstruction output
    output_path = OUTPUT_DIR / 'reconstruction_output.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nReconstruction output saved to {output_path}")
