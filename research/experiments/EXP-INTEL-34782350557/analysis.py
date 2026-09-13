#!/usr/bin/env python3
"""
EXP-INTEL-34782350557 — Tightened Definition Analysis
Computes interactive fraction metrics under ROLE-ONLY definition from
existing EXP-INTEL-34718481334 raw measurement data.

Frozen definition (from prereg):
  Elements with non-null bbox AND role in
  ['button','link','textbox','checkbox','radio','combobox','listbox',
   'menuitem','tab','slider','spinbutton','searchbox','switch']
  No form-membership clause, no onclick/onsubmit, no aria-label/aria-describedby.

IMPORTANT: The role field in the raw data uses `el.getAttribute('role') || el.tagName.toLowerCase()`.
This means:
  - <A> without explicit role → role="a" (NOT "link")
  - <BUTTON> without explicit role → role="button"
  - <INPUT> without explicit role → role="input" (NOT "textbox")
  - <INPUT role="combobox"> → role="combobox"
  - <A role="button"> → role="button"

Two matching strategies are computed:
  1. STRICT: role must exactly match the interactive set (only "button" and "combobox" match from the data)
  2. MAPPED: "a"→"link", "input"→"textbox" (semantic mapping of HTML tag names to ARIA roles)
"""

import json
import math
import hashlib
import statistics
from pathlib import Path
from collections import defaultdict

# Paths
RAW_DATA_PATH = Path(__file__).parent.parent / "EXP-INTEL-34718481334" / "exp347_raw_results.json"
OUTPUT_DIR = Path(__file__).parent

# Frozen tightened definition: role-only, no form-membership
INTERACTIVE_ROLES = {
    "button", "link", "textbox", "checkbox", "radio",
    "combobox", "listbox", "menuitem", "tab", "slider",
    "spinbutton", "searchbox", "switch"
}

# Semantic mapping: HTML tag name fallback → ARIA role
ROLE_MAP = {
    "a": "link",
    "input": "textbox",
    # Everything else: use as-is
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(812), b""):
            h.update(chunk)
    return h.hexdigest()


def count_strict(sample):
    """Count elements where role (as-is) is in INTERACTIVE_ROLES."""
    return sum(1 for el in sample if el["role"] in INTERACTIVE_ROLES)


def count_mapped(sample):
    """Count elements where mapped role is in INTERACTIVE_ROLES."""
    count = 0
    for el in sample:
        mapped = ROLE_MAP.get(el["role"], el["role"])
        if mapped in INTERACTIVE_ROLES:
            count += 1
    return count


def compute_cv(values):
    """Coefficient of variation. Returns 0 if n<2 or mean==0."""
    if len(values) < 2:
        return 0.0
    m = statistics.mean(values)
    if m == 0:
        return 0.0
    return statistics.stdev(values) / m


def main():
    # Load raw data
    with open(RAW_DATA_PATH) as f:
        raw = json.load(f)

    measurements = raw["measurements"]

    # Filter successful tasks (error=null, http_status=200)
    successful = [m for m in measurements if m.get("error") is None and m.get("http_status") == 200]

    print(f"Total measurements: {len(measurements)}")
    print(f"Successful tasks: {len(successful)}")
    print(f"Excluded: {[m['task_id'] for m in measurements if m not in successful]}")
    print()

    # Verify data completeness: all successful tasks have locatable_sample with role and inForm fields
    missing_fields = []
    for m in successful:
        if "locatable_sample" not in m:
            missing_fields.append(f"{m['task_id']}: no locatable_sample")
        else:
            for i, el in enumerate(m["locatable_sample"]):
                if "role" not in el:
                    missing_fields.append(f"{m['task_id']} element {i}: missing role")
                if "inForm" not in el:
                    missing_fields.append(f"{m['task_id']} element {i}: missing inForm")

    if missing_fields:
        print("MEASUREMENT_INVALID: Missing fields in raw data:")
        for mf in missing_fields:
            print(f"  {mf}")
        return

    print("Data completeness: ALL tasks have role and inForm fields in locatable_sample")
    print()

    # Verify we have at least 3 page types
    page_types = set(m["page_type"] for m in successful)
    if len(page_types) < 3:
        print(f"MEASUREMENT_INVALID: Only {len(page_types)} page types represented")
        return

    print(f"Page types: {page_types}")
    print()

    # ── Analysis per matching strategy ──
    for strategy_name, count_fn in [("STRICT", count_strict), ("MAPPED", count_mapped)]:
        print(f"{'='*60}")
        print(f"STRATEGY: {strategy_name}")
        print(f"{'='*60}")

        # Per-task computation
        task_results = []
        for m in successful:
            sample = m["locatable_sample"]
            sample_size = len(sample)
            tightened_count_in_sample = count_fn(sample)
            total_dom = m["total_dom_elements"]
            locatable = m["locatable_elements"]

            # Prereg computation: count from sample / total_dom_elements
            tightened_fraction_sample = tightened_count_in_sample / total_dom if total_dom > 0 else 0.0

            # Extrapolated estimate: (sample_match / sample_size) * locatable / total_dom
            if sample_size > 0 and total_dom > 0:
                match_rate = tightened_count_in_sample / sample_size
                estimated_total_tightened = match_rate * locatable
                tightened_fraction_extrapolated = estimated_total_tightened / total_dom
            else:
                tightened_fraction_extrapolated = 0.0

            task_results.append({
                "task_id": m["task_id"],
                "page_type": m["page_type"],
                "sample_size": sample_size,
                "tightened_count_in_sample": tightened_count_in_sample,
                "total_dom": total_dom,
                "locatable": locatable,
                "tightened_fraction_sample": tightened_fraction_sample,
                "tightened_fraction_extrapolated": tightened_fraction_extrapolated,
                "original_fraction": m["interactive_fraction"],
                "roles_in_sample": [el["role"] for el in sample],
            })

            print(f"  {m['task_id']}: sample={sample_size}, "
                  f"strict_match={tightened_count_in_sample}, "
                  f"sample_frac={tightened_fraction_sample:.6f}, "
                  f"extrap_frac={tightened_fraction_extrapolated:.6f}, "
                  f"original_frac={m['interactive_fraction']:.6f}")

        print()

        # ── Per-type aggregation ──
        types = defaultdict(list)
        for tr in task_results:
            types[tr["page_type"]].append(tr)

        type_stats = {}
        for pt, tasks in types.items():
            sample_fracs = [t["tightened_fraction_sample"] for t in tasks]
            extrap_fracs = [t["tightened_fraction_extrapolated"] for t in tasks]
            sample_counts = [t["tightened_count_in_sample"] for t in tasks]
            n = len(tasks)

            stats = {
                "n": n,
                "sample_count_mean": statistics.mean(sample_counts),
                "sample_frac_mean": statistics.mean(sample_fracs),
                "sample_frac_cv": compute_cv(sample_fracs),
                "extrap_frac_mean": statistics.mean(extrap_fracs),
                "extrap_frac_cv": compute_cv(extrap_fracs),
            }
            type_stats[pt] = stats

            print(f"  {pt} (n={n}):")
            print(f"    tightened_count_in_sample: {sample_counts} mean={stats['sample_count_mean']:.2f}")
            print(f"    sample_fraction: mean={stats['sample_frac_mean']:.6f} cv={stats['sample_frac_cv']:.6f}")
            print(f"    extrapolated_fraction: mean={stats['extrap_frac_mean']:.6f} cv={stats['extrap_frac_cv']:.6f}")

        print()

        # ── Within-type CV (sample-based) ──
        cv_results = {}
        for pt, stats in type_stats.items():
            if stats["n"] >= 2:
                cv_results[pt] = stats["sample_frac_cv"]
            else:
                cv_results[pt] = None  # cannot compute

        print("  Within-type CV (sample-based, n>=2):")
        for pt, cv in cv_results.items():
            status = f"CV={cv:.6f}" if cv is not None else "n=1, cannot compute"
            passed = "PASS" if cv is not None and cv < 0.3 else ("FAIL" if cv is not None and cv >= 0.3 else "N/A")
            print(f"    {pt}: {status} [{passed}]")

        # Count how many page types have CV < 0.3
        cv_pass_count = sum(1 for cv in cv_results.values() if cv is not None and cv < 0.3)
        cv_eligible_count = sum(1 for cv in cv_results.values() if cv is not None)
        print(f"  CV < 0.3: {cv_pass_count}/{cv_eligible_count} eligible types pass")
        stability_holds = cv_pass_count >= 2
        print(f"  Stability criterion (>=2 types with CV<0.3): {'PASS' if stability_holds else 'FAIL'}")
        print()

        # ── Between-type vs within-type variance (sample-based) ──
        type_means_sample = {pt: stats["sample_frac_mean"] for pt, stats in type_stats.items()}

        if len(type_means_sample) > 1:
            between_var = statistics.variance(list(type_means_sample.values()))

            within_vars = []
            for pt, tasks in types.items():
                if len(tasks) > 1:
                    fracs = [t["tightened_fraction_sample"] for t in tasks]
                    within_vars.append(statistics.variance(fracs))
            within_var = statistics.mean(within_vars) if within_vars else 0.0

            discrimination_ratio = between_var / within_var if within_var > 0 else float('inf')

            print(f"  Between-type variance (sample): {between_var:.12f}")
            print(f"  Within-type variance (sample): {within_var:.12f}")
            print(f"  Discrimination ratio: {discrimination_ratio:.4f}")
            discrimination_holds = between_var > within_var
            print(f"  Discrimination criterion (between > within): {'PASS' if discrimination_holds else 'FAIL'}")
        else:
            between_var = 0.0
            within_var = 0.0
            discrimination_ratio = 0.0
            discrimination_holds = False
            print("  Cannot compute discrimination: need >1 page type")
        print()

        # ── Ordering assessment ──
        listing_mean = type_stats.get("product_listing", {}).get("sample_frac_mean", 0)
        detail_mean = type_stats.get("detail", {}).get("sample_frac_mean", 0)
        cart_mean = type_stats.get("cart", {}).get("sample_frac_mean", 0)

        ordering_preserved = listing_mean > detail_mean > cart_mean
        ordering_strict = listing_mean > detail_mean and detail_mean > cart_mean
        ordering_with_tolerance = (listing_mean > detail_mean - 0.001) and (detail_mean > cart_mean - 0.001)

        print(f"  Ordering: listing={listing_mean:.6f}, detail={detail_mean:.6f}, cart={cart_mean:.6f}")
        print(f"  listing > detail: {listing_mean > detail_mean} ({listing_mean:.6f} vs {detail_mean:.6f})")
        print(f"  detail > cart: {detail_mean > cart_mean} ({detail_mean:.6f} vs {cart_mean:.6f})")
        print(f"  Ordering preserved (strict): {'PASS' if ordering_strict else 'FAIL'}")
        print()

        # ── Positive control: tightened_count > 0 on all tasks ──
        pos_control_pass = all(t["tightened_count_in_sample"] > 0 for t in task_results)
        pos_control_counts = [(t["task_id"], t["tightened_count_in_sample"]) for t in task_results]
        print(f"  Positive control (count > 0 on all tasks): {'PASS' if pos_control_pass else 'FAIL'}")
        for tid, cnt in pos_control_counts:
            print(f"    {tid}: {cnt}")
        print()

        # ── Null control: tightened_count <= original_locatable on all tasks ──
        null_control_pass = all(t["tightened_count_in_sample"] <= t["locatable"] for t in task_results)
        print(f"  Null control (sample_count <= locatable_elements): {'PASS' if null_control_pass else 'FAIL'}")
        print()

        # ── Downward shift comparison ──
        print("  Original vs tightened (extrapolated) fractions:")
        for t in task_results:
            delta = t["original_fraction"] - t["tightened_fraction_extrapolated"]
            pct = (delta / t["original_fraction"] * 100) if t["original_fraction"] > 0 else 0
            print(f"    {t['task_id']}: original={t['original_fraction']:.6f}, "
                  f"extrapolated={t['tightened_fraction_extrapolated']:.6f}, "
                  f"delta={delta:.6f} ({pct:.1f}% reduction)")
        print()

    # ── Save detailed results for downstream consumption ──
    # Run full analysis with both strategies and save
    results = {"strict": {}, "mapped": {}}

    for strategy_name, count_fn in [("strict", count_strict), ("mapped", count_mapped)]:
        task_results = []
        for m in successful:
            sample = m["locatable_sample"]
            sample_size = len(sample)
            tightened_count = count_fn(sample)
            total_dom = m["total_dom_elements"]
            locatable = m["locatable_elements"]
            sample_frac = tightened_count / total_dom if total_dom > 0 else 0.0

            if sample_size > 0 and total_dom > 0:
                match_rate = tightened_count / sample_size
                est_total = match_rate * locatable
                extrap_frac = est_total / total_dom
            else:
                extrap_frac = 0.0

            task_results.append({
                "task_id": m["task_id"],
                "page_type": m["page_type"],
                "sample_size": sample_size,
                "tightened_count_in_sample": tightened_count,
                "total_dom": total_dom,
                "locatable": locatable,
                "tightened_fraction_sample": sample_frac,
                "tightened_fraction_extrapolated": extrap_frac,
                "original_fraction": m["interactive_fraction"],
            })

        types = defaultdict(list)
        for tr in task_results:
            types[tr["page_type"]].append(tr)

        type_means = {pt: statistics.mean([t["tightened_fraction_sample"] for t in tasks])
                      for pt, tasks in types.items()}

        within_cv = {}
        for pt, tasks in types.items():
            if len(tasks) >= 2:
                fracs = [t["tightened_fraction_sample"] for t in tasks]
                within_cv[pt] = compute_cv(fracs)

        if len(type_means) > 1:
            between_var = statistics.variance(list(type_means.values()))
            within_vars = []
            for pt, tasks in types.items():
                if len(tasks) > 1:
                    fracs = [t["tightened_fraction_sample"] for t in tasks]
                    within_vars.append(statistics.variance(fracs))
            within_var = statistics.mean(within_vars) if within_vars else 0.0
        else:
            between_var = 0.0
            within_var = 0.0

        results[strategy_name] = {
            "task_results": task_results,
            "type_means": type_means,
            "within_cv": within_cv,
            "between_variance": between_var,
            "within_variance": within_var,
            "discrimination_ratio": between_var / within_var if within_var > 0 else None,
        }

    # Save analysis results
    out_path = OUTPUT_DIR / "analysis_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nAnalysis results saved to {out_path}")
    print(f"SHA256: {sha256_file(out_path)}")


if __name__ == "__main__":
    main()
