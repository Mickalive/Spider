#!/usr/bin/env python3
import json
import sys
import math

# interactive roles per tightened definition (ROLE-ONLY)
INTERACTIVE_ROLES = {
    'button', 'link', 'textbox', 'checkbox', 'radio', 'combobox',
    'listbox', 'menuitem', 'tab', 'slider', 'spinbutton', 'searchbox', 'switch'
}
# mapping from raw role to canonical role (if needed)
ROLE_MAP = {
    'a': 'link',
    'input': 'textbox',
    # keep others as-is
}

def canonical_role(role):
    return ROLE_MAP.get(role, role)

def is_interactive(element):
    role = element.get('role', '')
    canon = canonical_role(role)
    return canon in INTERACTIVE_ROLES

def main():
    if len(sys.argv) < 2:
        print("Usage: tightened.py <exp347_raw_results.json>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)
    measurements = data['measurements']
    # filter successful tasks
    tasks = []
    for m in measurements:
        if m.get('error') is None and m.get('http_status') == 200:
            tasks.append(m)
    print(f"Total successful tasks: {len(tasks)}")
    results = []
    for m in tasks:
        sample = m.get('locatable_sample', [])
        # compute tightened count
        tightened_count = sum(1 for e in sample if is_interactive(e))
        total_dom = m['total_dom_elements']
        fraction = tightened_count / total_dom if total_dom > 0 else 0
        results.append({
            'task_id': m['task_id'],
            'page_type': m['page_type'],
            'tightened_locatable_count': tightened_count,
            'total_dom_elements': total_dom,
            'tightened_interactive_fraction': fraction,
            'original_locatable_elements': m['locatable_elements'],
            'original_interactive_fraction': m['interactive_fraction'],
        })
    # compute per-type stats
    types = {}
    for r in results:
        t = r['page_type']
        types.setdefault(t, []).append(r)
    print("\nPer-type results:")
    for t, items in types.items():
        fracs = [r['tightened_interactive_fraction'] for r in items]
        mean = sum(fracs) / len(fracs)
        if len(fracs) > 1:
            var = sum((x - mean) ** 2 for x in fracs) / (len(fracs) - 1)
            std = math.sqrt(var)
            cv = std / mean if mean > 0 else float('inf')
        else:
            var = 0.0
            std = 0.0
            cv = 0.0
        print(f"  {t}: n={len(items)}, mean={mean:.6f}, std={std:.6f}, CV={cv:.4f}")
        for r in items:
            print(f"    {r['task_id']}: tightened_count={r['tightened_locatable_count']}, fraction={r['tightened_interactive_fraction']:.6f}, original_fraction={r['original_interactive_fraction']:.6f}")
    # compute between-type variance
    type_means = {t: sum(r['tightened_interactive_fraction'] for r in items) / len(items) for t, items in types.items()}
    overall_mean = sum(type_means.values()) / len(type_means)
    between_var = sum((m - overall_mean) ** 2 for m in type_means.values()) / (len(type_means) - 1) if len(type_means) > 1 else 0
    # compute within-type variance (average of per-type variances weighted by n-1)
    within_var = 0.0
    total_n = 0
    for t, items in types.items():
        fracs = [r['tightened_interactive_fraction'] for r in items]
        if len(fracs) > 1:
            var = sum((x - sum(fracs)/len(fracs)) ** 2 for x in fracs) / (len(fracs) - 1)
            within_var += var * (len(fracs) - 1)
            total_n += len(fracs) - 1
    if total_n > 0:
        within_var /= total_n
    else:
        within_var = 0.0
    print(f"\nBetween-type variance: {between_var:.12f}")
    print(f"Within-type variance (weighted): {within_var:.12f}")
    print(f"Discrimination ratio (between/within): {between_var / within_var if within_var > 0 else float('inf'):.2f}")
    # ordering
    print("\nOrdering of type means:")
    for t, m in sorted(type_means.items(), key=lambda x: x[1], reverse=True):
        print(f"  {t}: {m:.6f}")
    # positive control
    zero_count = [r for r in results if r['tightened_locatable_count'] == 0]
    if zero_count:
        print("\nPOSITIVE CONTROL FAIL: zero tightened locatable count on tasks:")
        for r in zero_count:
            print(f"  {r['task_id']}")
    else:
        print("\nPOSITIVE CONTROL PASS: all tasks have >0 tightened locatable count")
    # null control: tightened <= original
    violations = [r for r in results if r['tightened_locatable_count'] > r['original_locatable_elements']]
    if violations:
        print("\nNULL CONTROL FAIL: tightened > original on tasks:")
        for r in violations:
            print(f"  {r['task_id']}: tightened={r['tightened_locatable_count']}, original={r['original_locatable_elements']}")
    else:
        print("\nNULL CONTROL PASS: tightened <= original on all tasks")
    # save detailed results as JSON for later use
    per_type_stats = {}
    for t, items in types.items():
        fracs = [r['tightened_interactive_fraction'] for r in items]
        mean = sum(fracs) / len(fracs)
        if len(fracs) > 1:
            var = sum((x - mean) ** 2 for x in fracs) / (len(fracs) - 1)
            std = math.sqrt(var)
            cv = std / mean if mean > 0 else float('inf')
        else:
            cv = 0.0
        per_type_stats[t] = {
            'n': len(items),
            'mean': mean,
            'cv': cv,
            'values': fracs,
        }
    output = {
        'per_task': results,
        'per_type': per_type_stats,
        'between_type_variance': between_var,
        'within_type_variance': within_var,
        'type_means': type_means,
    }
    with open('/tmp/opencode/analysis/tightened_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("\nDetailed results saved to /tmp/opencode/analysis/tightened_results.json")

if __name__ == '__main__':
    main()