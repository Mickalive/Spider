#!/usr/bin/env python3
"""
EXP-INTEL-35124660457: Truncation Bias Analysis
Analyzes whether first-20 locatable_sample truncation systematically biases
role counts and density-based page-type orderings.
"""

import json
import numpy as np
from collections import Counter
from pathlib import Path

RAW_DATA = Path("research/experiments/EXP-INTEL-34782350557/raw_evidence/exp347_raw_results.json")
OUTPUT_DIR = Path("research/experiments/EXP-INTEL-35124660457")


def load_data():
    with open(RAW_DATA) as f:
        data = json.load(f)
    valid = [m for m in data['measurements'] if m.get('dom_stats') and m.get('locatable_elements')]
    return valid


def compute_truncated_role_counts(measurement):
    """Count roles in the first-20 locatable_sample."""
    return Counter(e['role'] for e in measurement['locatable_sample'])


def compute_full_dom_estimates(measurement):
    """
    Estimate full-DOM role counts using dom_stats tag counts.
    For roles with direct DOM equivalents, use tag counts.
    For others, scale truncated-sample counts proportionally.
    """
    ds = measurement['dom_stats']
    locatable = measurement['locatable_elements']
    sample_count = len(measurement['locatable_sample'])

    full_estimates = {
        'a': ds['linksCount'],
        'button': ds['buttonsCount'],
        'form': ds['formsCount'],
        'input': ds['inputsCount'],
    }

    sample_roles = compute_truncated_role_counts(measurement)
    scale_factor = locatable / sample_count if sample_count > 0 else 1

    for role in ['combobox', 'div', 'label', 'span']:
        full_estimates[role] = int(sample_roles.get(role, 0) * scale_factor)

    return full_estimates


def compute_density(role_counts, elements_with_bbox):
    """Compute density: sum of role counts / elements_with_bbox."""
    return sum(role_counts.values()) / elements_with_bbox if elements_with_bbox > 0 else 0


def compute_ordering(density_by_page_type):
    """Sort page types by density (descending)."""
    return sorted(density_by_page_type.keys(), key=lambda x: density_by_page_type[x], reverse=True)


def random_sample_baseline(measurement, n_simulations=1000, seed=42):
    """
    Simulate random 20-element draws from locatable_elements pool.
    
    Since we don't have individual element data for the full pool, we use
    the DOM tag counts as a proxy for the role distribution in the full pool.
    For each simulation, we draw 20 elements with probabilities proportional
    to the full-DOM role estimates.
    """
    rng = np.random.RandomState(seed)
    locatable = measurement['locatable_elements']
    sample_count = len(measurement['locatable_sample'])

    if locatable < sample_count:
        return None

    full_estimates = compute_full_dom_estimates(measurement)
    elements_with_bbox = measurement['elements_with_bbox']

    # Role probability distribution (from full-DOM estimates, normalized)
    roles = list(full_estimates.keys())
    counts = np.array([full_estimates[r] for r in roles], dtype=float)
    total = counts.sum()
    if total == 0:
        return None
    probs = counts / total

    biases_per_sim = []
    density_diffs = []

    for _ in range(n_simulations):
        # Draw 20 elements with replacement (approximation for without-replacement at small n/total ratio)
        drawn = rng.choice(len(roles), size=sample_count, replace=True, p=probs)
        sim_counts = Counter()
        for idx in drawn:
            sim_counts[roles[idx]] += 1

        sim_density = compute_density(dict(sim_counts), elements_with_bbox)
        full_density = compute_density(full_estimates, elements_with_bbox)

        abs_bias = abs(sim_density - full_density)
        if full_density > 0:
            rel_bias = abs_bias / full_density
        else:
            rel_bias = 0

        biases_per_sim.append(rel_bias)
        density_diffs.append(abs_bias)

    return {
        'mean_relative_bias': float(np.mean(biases_per_sim)),
        'std_relative_bias': float(np.std(biases_per_sim)),
        'median_relative_bias': float(np.median(biases_per_sim)),
        'p95_relative_bias': float(np.percentile(biases_per_sim, 95)),
        'mean_abs_density_diff': float(np.mean(density_diffs)),
    }


def compute_per_task_truncation_bias(measurement):
    """Compute the truncation bias for a single task."""
    truncated_roles = compute_truncated_role_counts(measurement)
    full_estimates = compute_full_dom_estimates(measurement)
    ewb = measurement['elements_with_bbox']

    trunc_density = compute_density(truncated_roles, ewb)
    full_density = compute_density(full_estimates, ewb)

    if full_density > 0:
        abs_bias = abs(full_density - trunc_density)
        rel_bias = abs_bias / full_density
    else:
        abs_bias = 0
        rel_bias = 0

    return {
        'truncated_density': trunc_density,
        'full_density': full_density,
        'abs_bias': abs_bias,
        'rel_bias': rel_bias,
        'truncated_roles': dict(truncated_roles),
        'full_estimates': full_estimates,
    }


def main():
    measurements = load_data()
    print(f"Loaded {len(measurements)} valid measurements\n")

    task_results = []
    for m in measurements:
        task_id = m['task_id']
        page_type = m['page_type']

        bias_info = compute_per_task_truncation_bias(m)
        rb = random_sample_baseline(m)

        task_results.append({
            'task_id': task_id,
            'page_type': page_type,
            'locatable_elements': m['locatable_elements'],
            'elements_with_bbox': m['elements_with_bbox'],
            **bias_info,
            'random_baseline': rb,
        })

    # --- Per-page-type averages ---
    page_types = {}
    for t in task_results:
        pt = t['page_type']
        if pt not in page_types:
            page_types[pt] = {'truncated': [], 'full': []}
        page_types[pt]['truncated'].append(t['truncated_density'])
        page_types[pt]['full'].append(t['full_density'])

    truncated_avg = {pt: float(np.mean(v['truncated'])) for pt, v in page_types.items()}
    full_avg = {pt: float(np.mean(v['full'])) for pt, v in page_types.items()}

    truncated_ordering = compute_ordering(truncated_avg)
    full_ordering = compute_ordering(full_avg)
    ordering_changed = truncated_ordering != full_ordering

    # Count tasks where ordering direction changes (per-task check)
    tasks_ordering_changed = 0
    for t in task_results:
        # A task changes if its relative position among same-type peers shifts
        # Simplified: check if truncated vs full density difference is >1%
        if t['rel_bias'] > 0.01:
            tasks_ordering_changed += 1

    # --- Condition 1: >=2/7 tasks ordering changed ---
    # Use page-type ordering change as proxy
    cond1 = ordering_changed
    cond1_detail = {
        'page_type_ordering_changed': ordering_changed,
        'truncated_ordering': truncated_ordering,
        'full_ordering': full_ordering,
        'n_tasks_with_bias_gt_1pct': tasks_ordering_changed,
    }

    # --- Condition 2: >=2/7 tasks with >20% relative bias ---
    tasks_gt_20 = sum(1 for t in task_results if t['rel_bias'] > 0.20)
    cond2 = tasks_gt_20 >= 2
    cond2_detail = {
        'tasks_gt_20pct': tasks_gt_20,
        'threshold': 0.20,
        'per_task_rel_bias': [(t['task_id'], t['page_type'], t['rel_bias']) for t in task_results],
    }

    # --- Condition 3: Random baseline lower bias than truncation ---
    random_biases = []
    trunc_biases = []
    for t in task_results:
        if t['random_baseline']:
            random_biases.append(t['random_baseline']['mean_relative_bias'])
        trunc_biases.append(t['rel_bias'])

    mean_random = float(np.mean(random_biases)) if random_biases else None
    mean_trunc = float(np.mean(trunc_biases))

    cond3 = mean_random is not None and mean_random < mean_trunc
    cond3_detail = {
        'mean_random_bias': mean_random,
        'mean_truncation_bias': mean_trunc,
        'random_lower': cond3,
        'n_tasks_with_random': len(random_biases),
    }

    decision = "SURVIVES_CURRENT_TEST" if (cond1 and cond2 and cond3) else "FALSIFIED-IN-SETTING"

    # --- Print summary ---
    print("=== ORDERING COMPARISON ===")
    print(f"  Truncated ordering:  {truncated_ordering}")
    print(f"  Full-DOM ordering:   {full_ordering}")
    print(f"  Changed: {ordering_changed}\n")

    print("=== PER-TASK BIAS ===")
    for t in task_results:
        print(f"  {t['task_id']:40s}  trunc={t['truncated_density']:.6f}  full={t['full_density']:.6f}  rel_bias={t['rel_bias']:.3f}  ({t['page_type']})")
    print()

    print("=== DECISION RULE ===")
    print(f"  C1 page-type ordering changed:      {cond1}  ({truncated_ordering} -> {full_ordering})")
    print(f"  C2 >=2/7 tasks >20% bias:           {cond2}  ({tasks_gt_20}/7)")
    print(f"  C3 random baseline lower bias:      {cond3}  (random={mean_random:.4f}, trunc={mean_trunc:.4f})")
    print(f"  VERDICT: {decision}\n")

    # Build output
    output = {
        'tasks': task_results,
        'ordering': {
            'truncated_avg_by_type': truncated_avg,
            'full_dom_avg_by_type': full_avg,
            'truncated_ordering': truncated_ordering,
            'full_ordering': full_ordering,
            'ordering_changed': ordering_changed,
        },
        'conditions': {
            'c1_ordering_changed': cond1_detail,
            'c2_large_bias': cond2_detail,
            'c3_random_lower': cond3_detail,
        },
        'decision': decision,
    }

    with open(OUTPUT_DIR / 'analysis_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"Results written to {OUTPUT_DIR / 'analysis_results.json'}")
    return output


if __name__ == '__main__':
    main()
