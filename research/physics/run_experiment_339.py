#!/usr/bin/env python3
"""
EXP-PHYSICS-33965269281 Experiment Runner

Frozen design: Playwright-based collection with full DOM/accessibility tree state.
Implements all four mandatory fixes from EXP-PHYSICS-33788037373 handoff.

Stdlib only for analysis; Playwright for browser-based collection.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import sys
import time
from pathlib import Path

# Add research directory to path
RESEARCH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RESEARCH_DIR))

from physics.substrate_339 import (
    PositiveControl, NullControl, PlaywrightLiveCollector,
    Transition, State, Action,
    trajectory_split,
    accuracy_action_conditioned, accuracy_action_frequency, accuracy_state_only,
    accuracy_in_sample,
    permutation_test_sa_vs_shuffle, permutation_test_sa_vs_action_freq,
    bonferroni_correction, check_validity,
)

EXPERIMENT_DIR = RESEARCH_DIR / "experiments" / "EXP-PHYSICS-33965269281"


# ---------------------------------------------------------------------------
# Phase 1: Positive Control (synthetic deterministic graph)
# ---------------------------------------------------------------------------

def run_positive_control(seed: int = 42, n_trajectories: int = 60,
                         steps_per_trajectory: int = 10) -> list[Transition]:
    """Generate transitions from the 8-state overlapping-action positive control."""
    print(f"[positive_control] Running {n_trajectories} trajectories, seed={seed}")
    ctrl = PositiveControl()
    rng = random.Random(seed)
    all_transitions = []

    for i in range(n_trajectories):
        traj_id = f"pos_{i}"
        start_id = rng.choice(ctrl.get_all_state_ids())
        current_id = start_id

        for step in range(steps_per_trajectory):
            valid_actions = ctrl.get_valid_actions(current_id)
            if not valid_actions:
                current_id = "A"
                continue

            action_type, target_href = rng.choice(valid_actions)
            next_id = ctrl.step(current_id, action_type, target_href)

            state = ctrl.get_state(current_id)
            action = Action(action_type=action_type, target_text=target_href,
                           target_href=target_href)
            next_state = ctrl.get_state(next_id)

            all_transitions.append(Transition(
                state=state, action=action, next_state=next_state,
                trajectory_id=traj_id, step_index=step,
            ))
            current_id = next_id

    print(f"[positive_control] Collected {len(all_transitions)} transitions "
          f"from {n_trajectories} trajectories")
    return all_transitions


# ---------------------------------------------------------------------------
# Phase 2: Null Control (random transitions)
# ---------------------------------------------------------------------------

def run_null_control(seed: int = 44, n_trajectories: int = 30,
                     steps_per_trajectory: int = 10) -> list[Transition]:
    """Generate transitions from the null control (random, action-independent)."""
    print(f"[null_control] Running {n_trajectories} trajectories, seed={seed}")
    ctrl = NullControl(seed=seed)
    transitions = ctrl.generate_trajectories(
        n_trajectories=n_trajectories,
        steps_per_trajectory=steps_per_trajectory,
    )
    print(f"[null_control] Collected {len(transitions)} transitions "
          f"from {n_trajectories} trajectories")
    return transitions


# ---------------------------------------------------------------------------
# Phase 3: Live Web Collection (Playwright-based)
# ---------------------------------------------------------------------------

def run_live_test(seed: int = 43, n_trajectories: int = 110,
                  max_steps: int = 8) -> tuple[dict[str, list[Transition]], dict]:
    """
    Collect transitions from live web pages using Playwright.
    Site 1: en.wikipedia.org/wiki/Web_browser (high link density)
    Site 2: docs.python.org/3/library/index.html (high link density)
    """
    sites = [
        ("https://en.wikipedia.org/wiki/Web_browser", "wikipedia"),
        ("https://docs.python.org/3/library/index.html", "python_docs"),
    ]

    all_transitions = {}
    collection_info = {}

    # Per-site seeds
    site_seeds = {"wikipedia": 43, "python_docs": 45}

    for site_url, site_name in sites:
        print(f"\n[live_test] === Collecting from {site_name}: {site_url} ===")
        print(f"[live_test] Target: {n_trajectories} trajectories, {max_steps} steps each")
        collector = PlaywrightLiveCollector(seed=site_seeds.get(site_name, seed))
        try:
            transitions, info = collector.collect_trajectories(
                start_url=site_url,
                n_trajectories=n_trajectories,
                max_steps=max_steps,
                polite_delay=0.3,
                max_retries=3,
            )
            all_transitions[site_name] = transitions
            collection_info[site_name] = info
            print(f"[live_test] {site_name}: {info['n_transitions']} transitions, "
                  f"{info['n_trajectories']} trajectories, "
                  f"{info['n_failed_trajectories']} failed trajectories, "
                  f"{info['n_failed_steps']} failed steps")
        except Exception as e:
            print(f"[live_test] {site_name} FAILED: {e}")
            all_transitions[site_name] = []
            collection_info[site_name] = {
                "start_url": site_url, "n_transitions": 0, "n_trajectories": 0,
                "error": str(e),
            }
        time.sleep(2.0)

    return all_transitions, collection_info


# ---------------------------------------------------------------------------
# Phase 4: Compute All Metrics
# ---------------------------------------------------------------------------

def compute_metrics_for_condition(transitions: list[Transition], label: str,
                                   train_frac: float = 0.7) -> dict:
    """Compute all metrics for a condition with trajectory-grouped holdout."""
    if not transitions:
        return {"error": "no_transitions", "label": label}

    train, test = trajectory_split(transitions, train_frac=train_frac, seed=42)

    acc_sa_train = accuracy_action_conditioned(train, train)
    acc_sa_test = accuracy_action_conditioned(train, test)
    acc_af_test = accuracy_action_frequency(train, test)
    acc_state_test = accuracy_state_only(train, test)
    acc_in_sample = accuracy_in_sample(transitions)

    memorization_ratio = acc_sa_train / max(acc_sa_test, 1e-10)

    shuffle_acc = _shuffle_baseline(train, test)

    return {
        "label": label,
        "n_transitions": len(transitions),
        "n_trajectories": len(set(t.trajectory_id for t in transitions)),
        "n_train_transitions": len(train),
        "n_train_trajectories": len(set(t.trajectory_id for t in train)),
        "n_test_transitions": len(test),
        "n_test_trajectories": len(set(t.trajectory_id for t in test)),
        "accuracy_SA_train": acc_sa_train,
        "accuracy_SA_heldout": acc_sa_test,
        "accuracy_AF_heldout": acc_af_test,
        "accuracy_state_heldout": acc_state_test,
        "accuracy_in_sample": acc_in_sample,
        "accuracy_shuffle": shuffle_acc,
        "memorization_ratio": memorization_ratio,
        "diff_SA_vs_shuffle": acc_sa_test - shuffle_acc,
        "diff_SA_vs_AF": acc_sa_test - acc_af_test,
    }


def _shuffle_baseline(train: list[Transition], test: list[Transition]) -> float:
    """Compute shuffle null accuracy for reference."""
    from physics.substrate_339 import _evaluate_shuffle_null
    return _evaluate_shuffle_null(train, test, seed=9999)


# ---------------------------------------------------------------------------
# Phase 5: Permutation Tests
# ---------------------------------------------------------------------------

def run_permutation_tests(positive: list[Transition], null: list[Transition],
                           live_sites: dict[str, list[Transition]],
                           n_permutations: int = 1000) -> dict:
    """Run all permutation tests per the prereg."""
    results = {}

    # Positive control: SA vs shuffle
    print("[perm_test] Positive control: SA vs shuffle")
    results["positive_SA_vs_shuffle"] = permutation_test_sa_vs_shuffle(
        positive, n_permutations=n_permutations, seed=42)

    # Positive control: SA vs action-frequency (discrimination)
    print("[perm_test] Positive control: SA vs action-frequency")
    results["positive_SA_vs_AF"] = permutation_test_sa_vs_action_freq(
        positive, n_permutations=n_permutations, seed=42)

    # Null control: SA vs shuffle
    print("[perm_test] Null control: SA vs shuffle")
    results["null_SA_vs_shuffle"] = permutation_test_sa_vs_shuffle(
        null, n_permutations=n_permutations, seed=44)

    # Live sites: SA vs shuffle
    for site_name, site_transitions in live_sites.items():
        if site_transitions:
            print(f"[perm_test] Live {site_name}: SA vs shuffle")
            results[f"live_{site_name}_SA_vs_shuffle"] = permutation_test_sa_vs_shuffle(
                site_transitions, n_permutations=n_permutations, seed=43)
        else:
            results[f"live_{site_name}_SA_vs_shuffle"] = {
                "error": "no_transitions", "p_value": 1.0}

    return results


# ---------------------------------------------------------------------------
# Phase 6: Determine Verdict
# ---------------------------------------------------------------------------

def determine_verdict(
    validity: dict,
    positive_metrics: dict,
    null_perm: dict,
    live_perm: dict,
    live_collection: dict,
) -> str:
    """
    Verdict per frozen decision rule:
    SURVIVES_CURRENT_TEST if ALL:
      1. Positive control discriminates (SA > AF, p < 0.05)
      2. Positive control accuracy > 90%
      3. Null control passes (p > 0.05)
      4. >= 1 live site shows SA > shuffle (p < 0.05 after Bonferroni x6)
      5. All validity gates pass
      6. >= 100 live transitions from >= 2 sites
      7. diff_SA_vs_shuffle > 0.03 on at least one site
    """
    # Gate 5: Validity
    if not validity["all_passed"]:
        return "MEASUREMENT_INVALID"

    # Gate 6: Live data collection
    n_live_sites = sum(1 for v in live_collection.values()
                       if v.get("n_transitions", 0) > 0)
    n_live_transitions = sum(v.get("n_transitions", 0)
                             for v in live_collection.values())
    if n_live_transitions < 100 or n_live_sites < 2:
        return "MEASUREMENT_INVALID"

    # Gate 1: Positive control discriminates (SA vs AF, p < 0.05)
    pos_discrim = live_perm.get("positive_SA_vs_AF", {})
    pos_discrim_p = pos_discrim.get("p_value", 1.0)
    if pos_discrim_p >= 0.05:
        return "MEASUREMENT_INVALID"

    # Gate 2: Positive control accuracy > 90%
    pos_acc = positive_metrics.get("accuracy_SA_heldout", 0.0)
    if pos_acc < 0.90:
        return "MEASUREMENT_INVALID"

    # Gate 3: Null control passes (p > 0.05)
    null_p = null_perm.get("p_value", 0.0)
    if null_p < 0.05:
        return "MEASUREMENT_INVALID"

    # Gate 4: >= 1 live site shows SA > shuffle (Bonferroni x6)
    live_p_values = []
    for key, val in live_perm.items():
        if key.startswith("live_") and key.endswith("_SA_vs_shuffle"):
            if "p_value" in val:
                live_p_values.append(val["p_value"])
    if not live_p_values:
        return "FALSIFIED-IN-SETTING"

    corrected = bonferroni_correction(live_p_values)
    has_significant = any(p < 0.05 for p in corrected)

    if not has_significant:
        return "FALSIFIED-IN-SETTING"

    # Gate 7: effect size > 0.03
    has_effect = False
    for key, val in live_perm.items():
        if key.startswith("live_") and key.endswith("_SA_vs_shuffle"):
            if val.get("observed_diff", 0) > 0.03:
                has_effect = True
    if not has_effect:
        return "FALSIFIED-IN-SETTING"

    return "SURVIVES_CURRENT_TEST"


# ---------------------------------------------------------------------------
# Phase 7: Write Output Files
# ---------------------------------------------------------------------------

def sha256_file(path: str) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_result(
    experiment_id: str,
    status: str,
    outcome: str,
    metrics: dict,
    controls: dict,
    artifacts: list,
    observations: list,
    validity_notes: list,
    unresolved: list,
) -> dict:
    """Write result.json with mandatory packet fields."""
    result = {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "lane": "physics",
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    path = EXPERIMENT_DIR / "result.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[output] Wrote {path}")
    return result


def write_report(result: dict, all_data: dict) -> str:
    """Write report.md with interpretation."""
    metrics = result["metrics"]
    controls = result["controls"]

    report = f"""# EXP-PHYSICS-33965269281 Report

## Experiment: Playwright-Based Action-Conditioned Transition Substrate

**Lane**: Physics
**Experiment ID**: EXP-PHYSICS-33965269281
**Status**: {result['status']}
**Outcome**: {result['outcome']}

---

## 1. Hypothesis

The previous MEASUREMENT_INVALID result (EXP-PHYSICS-33788037373) was caused by
representation degradation: HTTP fetch discarded DOM structure, accessibility tree,
and form signals. With Playwright-based collection extracting full DOM structure,
accessibility tree, link texts, tag counts, and form signals, the corrected substrate
will reveal action-conditioned transition structure on live Web pages.

---

## 2. Results Summary

### Positive Control
- **Transitions**: {metrics.get('positive_control', {}).get('n_transitions', 'N/A')}
- **Action-Conditioned Accuracy (held-out)**: {metrics.get('positive_control', {}).get('accuracy_SA_heldout', 'N/A'):.4f}
- **Action-Frequency Accuracy (held-out)**: {metrics.get('positive_control', {}).get('accuracy_AF_heldout', 'N/A'):.4f}
- **Shuffle Accuracy**: {metrics.get('positive_control', {}).get('accuracy_shuffle', 'N/A'):.4f}
- **Memorization Ratio**: {metrics.get('positive_control', {}).get('memorization_ratio', 'N/A'):.2f}
- **diff_SA_vs_shuffle**: {metrics.get('positive_control', {}).get('diff_SA_vs_shuffle', 'N/A'):.4f}

### Null Control
- **Transitions**: {metrics.get('null_control', {}).get('n_transitions', 'N/A')}
- **Action-Conditioned Accuracy (held-out)**: {metrics.get('null_control', {}).get('accuracy_SA_heldout', 'N/A'):.4f}
- **Action-Frequency Accuracy (held-out)**: {metrics.get('null_control', {}).get('accuracy_AF_heldout', 'N/A'):.4f}
- **diff_SA_vs_shuffle**: {metrics.get('null_control', {}).get('diff_SA_vs_shuffle', 'N/A'):.4f}

### Live Tests
"""
    for site in ["wikipedia", "python_docs"]:
        site_m = metrics.get(f"live_{site}", {})
        sa_heldout = site_m.get('accuracy_SA_heldout', None)
        sa_str = f"{sa_heldout:.4f}" if isinstance(sa_heldout, (int, float)) else "N/A"
        diff_val = site_m.get('diff_SA_vs_shuffle', None)
        diff_str = f"{diff_val:.4f}" if isinstance(diff_val, (int, float)) else "N/A"
        report += f"""
**{site.replace('_', ' ').title()}**:
- Transitions: {site_m.get('n_transitions', 'N/A')}
- Trajectories: {site_m.get('n_trajectories', 'N/A')}
- Action-Conditioned Accuracy (held-out): {sa_str}
- Action-Frequency Accuracy (held-out): {site_m.get('accuracy_AF_heldout', 'N/A') if isinstance(site_m.get('accuracy_AF_heldout'), (int, float)) else 'N/A'}
- SA vs Shuffle Diff: {diff_str}
- Memorization Ratio: {site_m.get('memorization_ratio', 'N/A') if isinstance(site_m.get('memorization_ratio'), (int, float)) else 'N/A'}
"""

    report += f"""
---

## 3. Permutation Tests

| Condition | Observed Diff | p-value | Significant? |
|-----------|--------------|---------|--------------|
"""
    for key, val in controls.items():
        if isinstance(val, dict) and "observed_diff" in val:
            p = val.get("p_value", 1.0)
            sig = "YES" if p < 0.05 else "NO"
            report += f"| {key} | {val['observed_diff']:.4f} | {p:.4f} | {sig} |\n"

    # Bonferroni correction for live sites
    live_p_values = []
    for key, val in controls.items():
        if key.startswith("live_") and key.endswith("_SA_vs_shuffle"):
            if isinstance(val, dict) and "p_value" in val:
                live_p_values.append((key, val["p_value"]))

    if live_p_values:
        raw_ps = [p for _, p in live_p_values]
        corrected_ps = bonferroni_correction(raw_ps)
        report += f"""
### Bonferroni Correction (6 comparisons)

| Site | Raw p-value | Corrected p-value | Significant? |
|------|------------|-------------------|--------------|
"""
        for (key, raw_p), corr_p in zip(live_p_values, corrected_ps):
            sig = "YES" if corr_p < 0.05 else "NO"
            report += f"| {key} | {raw_p:.4f} | {corr_p:.4f} | {sig} |\n"

    report += f"""
---

## 4. Validity Gates

"""
    for note in result["validity_notes"]:
        report += f"- {note}\n"

    report += f"""
---

## 5. Observations

"""
    for obs_item in result["observations"]:
        report += f"- {obs_item}\n"

    report += f"""
---

## 6. Interpretation

### Representation
This experiment uses Playwright-based collection with:
- Full DOM structure (tag counts)
- Accessibility tree (ARIA roles and names)
- Link texts (first 30 visible)
- Form signals (has_form, has_input, has_select, has_textarea)
- target_href = destination URL (fixed from prior experiment)

### Prior Experiment Comparison
EXP-PHYSICS-33788037373 used HTTP fetch with URL-only state representation.
Best result: Python docs diff_SA_vs_shuffle = 0.030, SA==AF, p_corr=0.096 (NOT significant).
State representation was degraded (URL-only, no DOM/accessibility tree).

### Positive Control
"""
    pc = metrics.get("positive_control", {})
    if pc.get("accuracy_SA_heldout", 0) > 0.9:
        report += f"The positive control achieves {pc.get('accuracy_SA_heldout', 0):.1%} held-out accuracy "
        report += f"with SA > AF (diff = {pc.get('diff_SA_vs_AF', 0):.4f}), confirming the pipeline "
        report += "can learn deterministic transitions with overlapping actions.\n"
    else:
        report += f"The positive control achieves only {pc.get('accuracy_SA_heldout', 0):.1%} held-out accuracy.\n"

    report += "\n### Null Control\n"
    nc = metrics.get("null_control", {})
    report += f"Null control SA held-out accuracy: {nc.get('accuracy_SA_heldout', 0):.4f}. "
    if nc.get("diff_SA_vs_shuffle", 0) < 0.05:
        report += "No false positive detected (diff near zero).\n"
    else:
        report += f"Diff_SA_vs_shuffle = {nc.get('diff_SA_vs_shuffle', 0):.4f} (unexpected for random data).\n"

    report += "\n### Live Web Structure\n"
    for site in ["wikipedia", "python_docs"]:
        site_m = metrics.get(f"live_{site}", {})
        diff_val = site_m.get('diff_SA_vs_shuffle', 0)
        report += f"- **{site.replace('_', ' ').title()}**: diff_SA_vs_shuffle = {diff_val:.4f}\n"

    report += f"""
---

## 7. Verdict

**{result['outcome']}**

"""
    if result["outcome"] == "SUPPORTS":
        report += "Browser-based collection with full state representation reveals "
        report += "action-conditioned structure on live Web, supporting C-WEB-DYNAMICS.\n"
    elif result["outcome"] == "FALSIFIES":
        report += "Browser-based collection with full state representation does NOT reveal "
        report += "action-conditioned structure on live Web at this representation level. "
        report += "C-WEB-DYNAMICS is falsified at this specific setting.\n"
    elif result["outcome"] == "NOT_APPLICABLE":
        report += "Measurement invalid: see validity notes above.\n"
    else:
        report += "Outcome inconclusive.\n"

    report += f"""
---

## 8. Validity Threats

1. **Synthetic-to-real gap**: Positive control validates pipeline, not Web dynamics.
2. **Multiple comparisons**: 6 comparisons (3 null tests x 2 sites), Bonferroni conservative.
3. **Sample size**: Target 100+ trajectories per site. Actual counts may vary.
4. **Navigation depth**: Limited to 8 steps per trajectory.
5. **Link selection**: Uniform random over available links (no content-aware selection).
"""

    path = EXPERIMENT_DIR / "report.md"
    with open(path, "w") as f:
        f.write(report)
    print(f"[output] Wrote {path}")
    return report


def write_provenance(result: dict, all_data: dict) -> dict:
    """Write provenance.json with reproduction context."""
    import subprocess
    import sys

    # Compute data hashes
    data_hashes = {}
    for key, transitions in all_data.items():
        if transitions:
            data_list = [{
                "state_url": t.state.url,
                "action_type": t.action.action_type,
                "action_text": t.action.target_text,
                "action_href": t.action.target_href,
                "next_state_url": t.next_state.url,
                "traj": t.trajectory_id,
                "step": t.step_index,
            } for t in transitions]
            data_hashes[key] = hashlib.sha256(
                json.dumps(data_list, sort_keys=True, default=str).encode()
            ).hexdigest()

    # Get git info
    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        git_sha = "unknown"

    provenance = {
        "experiment_id": "EXP-PHYSICS-33965269281",
        "lane": "physics",
        "request_hash": "5128ce15f6cae2a19a4b7c4526f74ee77b74d803fcb91dabeb6048c65e01f55e",
        "freeze_hash_prereg": "5158b63d7e3d646e932cf7fa677d0709fd25da2c8a2d2ed866057dd5104491d8",
        "freeze_hash_request": "1e2103fdc982e84c4ec36d2ee7cab2393a663c14de893a8ee5a1884d60d59d6a",
        "freeze_hash_spec": "0717f4c5c8c4b161389094ec7987a2bc410088d599825d606292e26781235b40",
        "git_sha": git_sha,
        "execution_sha": hashlib.sha256(
            json.dumps(result, sort_keys=True, default=str).encode()
        ).hexdigest(),
        "code_paths": [
            "research/physics/substrate_339.py",
            "research/physics/run_experiment_339.py",
        ],
        "environment": {
            "python_version": sys.version,
            "platform": sys.platform,
        },
        "seeds": {
            "positive_control": 42,
            "null_control": 44,
            "live_wikipedia": 43,
            "live_python_docs": 45,
            "split": 42,
            "permutation_base": 42,
            "shuffle_null": 9999,
        },
        "data_hashes": data_hashes,
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    path = EXPERIMENT_DIR / "provenance.json"
    with open(path, "w") as f:
        json.dump(provenance, f, indent=2, default=str)
    print(f"[output] Wrote {path}")
    return provenance


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("EXP-PHYSICS-33965269281: Playwright-Based Action-Conditioned Transition Substrate")
    print("=" * 70)
    print(f"Started: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")

    # Phase 1: Positive Control
    print("\n" + "=" * 70)
    print("PHASE 1: POSITIVE CONTROL (8 states, 3 action types, overlapping)")
    print("=" * 70)
    positive = run_positive_control(seed=42, n_trajectories=60, steps_per_trajectory=10)

    # Phase 2: Null Control
    print("\n" + "=" * 70)
    print("PHASE 2: NULL CONTROL (30 states, random transitions)")
    print("=" * 70)
    null = run_null_control(seed=44, n_trajectories=30, steps_per_trajectory=10)

    # Phase 3: Live Web (Playwright)
    print("\n" + "=" * 70)
    print("PHASE 3: LIVE WEB COLLECTION (Playwright)")
    print("=" * 70)
    live_sites, live_info = run_live_test(seed=43, n_trajectories=110, max_steps=8)

    # Phase 4: Metrics
    print("\n" + "=" * 70)
    print("PHASE 4: COMPUTE METRICS")
    print("=" * 70)
    positive_metrics = compute_metrics_for_condition(positive, "positive_control")
    null_metrics = compute_metrics_for_condition(null, "null_control")

    live_metrics = {}
    for site_name, site_trans in live_sites.items():
        live_metrics[f"live_{site_name}"] = compute_metrics_for_condition(
            site_trans, f"live_{site_name}")

    all_metrics = {
        "positive_control": positive_metrics,
        "null_control": null_metrics,
        **live_metrics,
    }

    # Phase 5: Permutation Tests
    print("\n" + "=" * 70)
    print("PHASE 5: PERMUTATION TESTS (1000 permutations)")
    print("=" * 70)
    perm_results = run_permutation_tests(
        positive, null, live_sites, n_permutations=1000)

    # Phase 6: Validity Gates
    print("\n" + "=" * 70)
    print("PHASE 6: VALIDITY GATES")
    print("=" * 70)
    all_transitions = positive + null
    for site_trans in live_sites.values():
        all_transitions.extend(site_trans)
    validity = check_validity(all_transitions, seed=42)

    for name, check in validity["checks"].items():
        status_str = "PASS" if check["passed"] else "FAIL"
        print(f"  {name}: {status_str}")
    print(f"  Overall: {'PASS' if validity['all_passed'] else 'FAIL'}")

    # Phase 7: Verdict
    print("\n" + "=" * 70)
    print("PHASE 7: VERDICT")
    print("=" * 70)
    outcome = determine_verdict(validity, positive_metrics,
                                 perm_results.get("null_SA_vs_shuffle", {}),
                                 perm_results, live_info)
    print(f"  OUTCOME: {outcome}")

    # Map verdict to status/outcome
    if outcome == "MEASUREMENT_INVALID":
        status = "MEASUREMENT_INVALID"
        outcome_mapped = "NOT_APPLICABLE"
    elif outcome == "SURVIVES_CURRENT_TEST":
        status = "COMPLETE"
        outcome_mapped = "SUPPORTS"
    elif outcome == "FALSIFIED-IN-SETTING":
        status = "COMPLETE"
        outcome_mapped = "FALSIFIES"
    else:
        status = "COMPLETE"
        outcome_mapped = "INCONCLUSIVE"
    final_outcome = outcome_mapped

    # Build controls dict
    controls = {}
    for key, val in perm_results.items():
        controls[key] = {
            "expected": "p < 0.05" if "positive" in key else ("p > 0.05" if "null" in key else "p < 0.05 after correction"),
            "observed_diff": val.get("observed_diff", None),
            "p_value": val.get("p_value", None),
            "pass": (val.get("p_value", 1.0) < 0.05) if "positive" in key or "live" in key
                     else (val.get("p_value", 0.0) > 0.05) if "null" in key else None,
        }

    # Build observations
    observations = [
        f"Positive control: {positive_metrics.get('n_transitions', 0)} transitions, "
        f"SA held-out acc={positive_metrics.get('accuracy_SA_heldout', 0):.4f}, "
        f"AF held-out acc={positive_metrics.get('accuracy_AF_heldout', 0):.4f}, "
        f"diff_SA_vs_AF={positive_metrics.get('diff_SA_vs_AF', 0):.4f}",
        f"Null control: {null_metrics.get('n_transitions', 0)} transitions, "
        f"SA held-out acc={null_metrics.get('accuracy_SA_heldout', 0):.4f}, "
        f"diff_SA_vs_shuffle={null_metrics.get('diff_SA_vs_shuffle', 0):.4f}",
    ]
    for site_name, info in live_info.items():
        site_m = live_metrics.get(f"live_{site_name}", {})
        observations.append(
            f"Live {site_name}: {info.get('n_transitions', 0)} transitions, "
            f"{info.get('n_trajectories', 0)} trajectories, "
            f"SA held-out acc={site_m.get('accuracy_SA_heldout', 0):.4f}, "
            f"diff_SA_vs_shuffle={site_m.get('diff_SA_vs_shuffle', 0):.4f}"
        )

    # Validity notes
    validity_notes = []
    if not validity["all_passed"]:
        validity_notes.append("VALIDITY GATE FAILURE: see validity checks above")
    for name, check in validity["checks"].items():
        if not check["passed"]:
            validity_notes.append(f"Validity gate {name} FAILED: {check.get('issues', [])[:5]}")

    # Representation loss notes
    validity_notes.extend([
        "REPRESENTATION: Playwright-based collection with full DOM, accessibility tree, link texts, tag counts, form_signals",
        "REPRESENTATION LOSS: No visual layout or CSS structure",
        "REPRESENTATION LOSS: No interaction history (hover, scroll, focus)",
        "REPRESENTATION LOSS: Accessibility tree may be incomplete on some pages",
        "REPRESENTATION LOSS: Query string stripped from URL",
        "COLLECTION: Chromium headless, JavaScript enabled, domcontentloaded wait",
        "FIX APPLIED: target_href = destination URL (not source URL as in EXP-PHYSICS-33788037373)",
        "FIX APPLIED: Full state representation stored in raw data",
        "FIX APPLIED: Bonferroni correction for 6 comparisons",
    ])

    # Unresolved
    unresolved = [
        "Whether JavaScript-heavy SPA sites show different structure",
        "Whether even richer representations (visual, interaction) reveal more structure",
        "Whether authenticated/form-heavy sites show different dynamics",
        "Whether the tested sites are representative of dynamical regimes",
    ]

    # Write result.json
    print("\n" + "=" * 70)
    print("PHASE 8: WRITING RESULTS")
    print("=" * 70)
    all_data = {"positive": positive, "null": null, **live_sites}
    result = write_result(
        experiment_id="EXP-PHYSICS-33965269281",
        status=status,
        outcome=final_outcome,
        metrics=all_metrics,
        controls=controls,
        artifacts=[],
        observations=observations,
        validity_notes=validity_notes,
        unresolved=unresolved,
    )

    # Write report.md
    write_report(result, all_data)

    # Write provenance.json
    provenance = write_provenance(result, all_data)

    # Now populate artifacts with sha256 hashes
    artifact_files = [
        ("result.json", "result"),
        ("report.md", "report"),
        ("provenance.json", "provenance"),
    ]
    artifacts = []
    for fname, role in artifact_files:
        fpath = EXPERIMENT_DIR / fname
        if fpath.exists():
            h = sha256_file(str(fpath))
            artifacts.append({
                "path": f"research/experiments/EXP-PHYSICS-33965269281/{fname}",
                "sha256": h,
                "role": role,
            })

    # Save raw transition data as artifacts
    for key, transitions in all_data.items():
        if transitions:
            data_path = EXPERIMENT_DIR / f"raw_{key}.json"
            data_list = [{
                "state_before": t.state.to_dict(),
                "action": t.action.to_dict(),
                "state_after": t.next_state.to_dict(),
                "trajectory_id": t.trajectory_id,
                "step_index": t.step_index,
            } for t in transitions]
            with open(data_path, "w") as f:
                json.dump(data_list, f, indent=2, default=str)
            h = sha256_file(str(data_path))
            artifacts.append({
                "path": f"research/experiments/EXP-PHYSICS-33965269281/raw_{key}.json",
                "sha256": h,
                "role": "raw",
            })

    # Update result.json with artifacts
    result["artifacts"] = artifacts
    path = EXPERIMENT_DIR / "result.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print(f"  Status: {status}")
    print(f"  Outcome: {final_outcome}")
    print(f"  Artifacts: {len(artifacts)} files")
    print("=" * 70)

    return result


if __name__ == "__main__":
    main()
