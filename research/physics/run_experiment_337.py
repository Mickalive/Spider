#!/usr/bin/env python3
"""
EXP-PHYSICS-33788037373 Corrected Experiment Runner

Implements frozen design with four mandatory fixes:
1. Trajectory-grouped holdout evaluation
2. Permutation test with independent RNG (not invalid bootstrap)
3. Overlapping-action positive control (discriminates (S,A) from A alone)
4. Richer state representation (URL + link_texts + tag_counts + form_signals)

Stdlib only: random.Random for RNG, no numpy/scipy.
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

from physics.substrate_337 import (
    PositiveControl, NullControl, LiveWebCollector,
    Transition, State, Action,
    trajectory_split,
    accuracy_action_conditioned, accuracy_action_frequency, accuracy_state_only,
    accuracy_in_sample,
    permutation_test_sa_vs_shuffle, permutation_test_sa_vs_action_freq,
    bonferroni_correction, check_validity,
)

EXPERIMENT_DIR = RESEARCH_DIR / "experiments" / "EXP-PHYSICS-33788037373"


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

            # Build State/Action objects
            state = ctrl.get_state(current_id)
            # For the positive control, target_href is the SHARED constant (same across states)
            # target_text is derived from the action type for display purposes
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
# Phase 3: Live Web Collection
# ---------------------------------------------------------------------------

def run_live_test(seed: int = 43, n_trajectories: int = 20,
                  max_steps: int = 10) -> tuple[list[Transition], dict]:
    """
    Collect transitions from live web pages.
    Site 1: Wikipedia (high link density, server-rendered)
    Site 2: Python docs (medium link density, server-rendered)
    """
    sites = [
        ("https://en.wikipedia.org/wiki/Main_Page", "wikipedia"),
        ("https://docs.python.org/3/", "python_docs"),
    ]

    all_transitions = {}
    collection_info = {}

    # Assign per-site seeds as per frozen spec (Section 5.3)
    site_seeds = {"wikipedia": 43, "python_docs": 45}
    for site_url, site_name in sites:
        print(f"[live_test] Collecting from {site_name}: {site_url}")
        collector = LiveWebCollector(seed=site_seeds.get(site_name, seed))
        try:
            transitions = collector.collect_trajectories(
                start_url=site_url,
                n_trajectories=n_trajectories,
                max_steps=max_steps,
                polite_delay=0.5,
            )
            all_transitions[site_name] = transitions
            n_traj = len(set(t.trajectory_id for t in transitions))
            collection_info[site_name] = {
                "url": site_url,
                "n_transitions": len(transitions),
                "n_trajectories": n_traj,
                "avg_steps": len(transitions) / max(1, n_traj),
            }
            print(f"[live_test] {site_name}: {len(transitions)} transitions, "
                  f"{n_traj} trajectories")
        except Exception as e:
            print(f"[live_test] {site_name} FAILED: {e}")
            all_transitions[site_name] = []
            collection_info[site_name] = {
                "url": site_url, "n_transitions": 0, "n_trajectories": 0,
                "error": str(e),
            }
        time.sleep(1.0)

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

    # Accuracy metrics
    acc_sa_train = accuracy_action_conditioned(train, train)
    acc_sa_test = accuracy_action_conditioned(train, test)
    acc_af_test = accuracy_action_frequency(train, test)
    acc_state_test = accuracy_state_only(train, test)
    acc_in_sample = accuracy_in_sample(transitions)

    memorization_ratio = acc_sa_train / max(acc_sa_test, 1e-10)

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
        "memorization_ratio": memorization_ratio,
        "diff_SA_vs_shuffle": acc_sa_test - _shuffle_baseline(train, test),
        "diff_SA_vs_AF": acc_sa_test - acc_af_test,
    }


def _shuffle_baseline(train: list[Transition], test: list[Transition]) -> float:
    """Compute shuffle null accuracy for reference."""
    from physics.substrate_337 import _evaluate_shuffle_null
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

    FALSIFIED-IN-SETTING if (1)-(3) pass but (4) fails.
    MEASUREMENT_INVALID if validity fails or infrastructure prevents collection.
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
    if any(p < 0.05 for p in corrected):
        return "SURVIVES_CURRENT_TEST"

    return "FALSIFIED-IN-SETTING"


# ---------------------------------------------------------------------------
# Phase 7: Write Output Files
# ---------------------------------------------------------------------------

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
    obs = result["observations"]
    validity = result["validity_notes"]

    report = f"""# EXP-PHYSICS-33788037373 Report

## Experiment: Corrected Action-Conditioned Transition Substrate

**Lane**: Physics
**Experiment ID**: EXP-PHYSICS-33788037373
**Status**: {result['status']}
**Outcome**: {result['outcome']}

---

## 1. Hypothesis

After correcting three methodology defects (in-sample evaluation, invalid bootstrap,
non-discriminating positive control) identified in EXP-PHYSICS-33528829431, does the
measurement substrate reveal genuine action-conditioned transition structure on live
Web pages with navigational density?

---

## 2. Results Summary

### Positive Control
- **Transitions**: {metrics.get('positive_control', {}).get('n_transitions', 'N/A')}
- **Action-Conditioned Accuracy (held-out)**: {metrics.get('positive_control', {}).get('accuracy_SA_heldout', 'N/A'):.4f}
- **Action-Frequency Accuracy (held-out)**: {metrics.get('positive_control', {}).get('accuracy_AF_heldout', 'N/A'):.4f}
- **Memorization Ratio**: {metrics.get('positive_control', {}).get('memorization_ratio', 'N/A'):.2f}

### Null Control
- **Transitions**: {metrics.get('null_control', {}).get('n_transitions', 'N/A')}
- **Action-Conditioned Accuracy (held-out)**: {metrics.get('null_control', {}).get('accuracy_SA_heldout', 'N/A'):.4f}
- **Action-Frequency Accuracy (held-out)**: {metrics.get('null_control', {}).get('accuracy_AF_heldout', 'N/A'):.4f}

### Live Tests
"""
    for site in ["wikipedia", "python_docs"]:
        site_m = metrics.get(f"live_{site}", {})
        sa_heldout = site_m.get('accuracy_SA_heldout', None)
        sa_str = f"{sa_heldout:.4f}" if isinstance(sa_heldout, (int, float)) else "N/A"
        diff_val = site_m.get('diff_SA_vs_shuffle', None)
        diff_str = f"{diff_val:.4f}" if isinstance(diff_val, (int, float)) else "N/A"
        report += f"""
**{site.title()}**:
- Transitions: {site_m.get('n_transitions', 'N/A')}
- Action-Conditioned Accuracy (held-out): {sa_str}
- SA vs Shuffle Diff: {diff_str}
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

    report += f"""
---

## 4. Validity Gates

"""
    for note in validity:
        report += f"- {note}\n"

    report += f"""
---

## 5. Observations

"""
    for obs_item in obs:
        report += f"- {obs_item}\n"

    report += f"""
---

## 6. Interpretation

### Memorization Artifact (H1)
"""
    pc = metrics.get("positive_control", {})
    if pc.get("memorization_ratio", 1.0) > 1.5:
        report += f"The memorization ratio ({pc.get('memorization_ratio', 0):.2f}) confirms that "
        report += "in-sample accuracy was inflated by memorization. The corrected held-out evaluation "
        report += "produces substantially lower accuracy, validating H1.\n"
    else:
        report += f"The memorization ratio ({pc.get('memorization_ratio', 0):.2f}) is modest. "
        report += "In-sample memorization was not the dominant artifact.\n"

    report += "\n### Positive Control Discrimination (H2)\n"
    pos_disc = controls.get("positive_SA_vs_AF", {})
    if pos_disc.get("p_value", 1.0) < 0.05:
        report += f"The positive control discriminates (SA > AF, p={pos_disc.get('p_value', 1.0):.4f}). "
        report += "The measurement substrate can detect state-dependent structure when it exists.\n"
    else:
        report += f"The positive control FAILS to discriminate (p={pos_disc.get('p_value', 1.0):.4f}). "
        report += "The substrate cannot distinguish (S,A) structure from action-only patterns.\n"

    report += "\n### Live Action-Conditioned Structure (H3)\n"
    live_corrected = []
    for key, val in controls.items():
        if key.startswith("live_") and key.endswith("_SA_vs_shuffle"):
            if "p_value" in val:
                live_corrected.append((key, val["p_value"]))
    if live_corrected:
        corrected_p = bonferroni_correction([p for _, p in live_corrected])
        for (key, raw_p), corr_p in zip(live_corrected, corrected_p):
            report += f"- {key}: raw p={raw_p:.4f}, corrected p={corr_p:.4f}\n"
    else:
        report += "- No live site permutation tests available.\n"

    report += f"""
---

## 7. Verdict

**{result['outcome']}**

{result.get('validity_notes', [''])[0] if result.get('validity_notes') else ''}

---

## 8. Validity Threats

1. **HTTP fetch only**: No JavaScript execution, no accessibility tree. SPA pages
   may appear structurally identical across navigations.
2. **Sample size**: ~200 transitions per live site. Limited power for small effects.
3. **Multiple comparisons**: 6 comparisons (3 null tests x 2 sites), Bonferroni conservative.
4. **Synthetic-to-real gap**: Positive control validates pipeline, not Web dynamics.
5. **Link text representation**: Empty link texts (image links) reduce state information.
"""

    path = EXPERIMENT_DIR / "report.md"
    with open(path, "w") as f:
        f.write(report)
    print(f"[output] Wrote {path}")
    return report


def write_provenance(result: dict, all_data: dict) -> dict:
    """Write provenance.json with reproduction context."""
    import sys

    # Compute data hashes
    data_hashes = {}
    for key, transitions in all_data.items():
        if transitions:
            data_list = [{
                "state_url": t.state.url,
                "action_type": t.action.action_type,
                "action_text": t.action.target_text,
                "next_state_url": t.next_state.url,
                "traj": t.trajectory_id,
                "step": t.step_index,
            } for t in transitions]
            data_hashes[key] = hashlib.sha256(
                json.dumps(data_list, sort_keys=True, default=str).encode()
            ).hexdigest()

    provenance = {
        "experiment_id": "EXP-PHYSICS-33788037373",
        "lane": "physics",
        "request_hash": "0e23a544b82cb71413cf4d130ec5d82a4e4bae42a551a65ba8de6d0ae6c668d7",
        "freeze_hash_prereg": "edef86688d34e165a026576e9f8c27edc95a0b3a73c5c80c2c52a4a234f610ea",
        "freeze_hash_request": "b014f5c206a83409bfd5326bc8d2e8183609e0ef80ed0e6078d50e2dae209ff6",
        "freeze_hash_spec": "818348452206b27e26f4dc645bb03bc3ccd982287f54fcd3d2f6f5b3101ce863",
        "pre_execute_sha": "33ef08894b52ac68b84d27cc9a5489bcf1d759b6",
        "execution_sha": hashlib.sha256(
            json.dumps(result, sort_keys=True, default=str).encode()
        ).hexdigest(),
        "code_paths": [
            "research/physics/substrate_337.py",
            "research/physics/run_experiment_337.py",
        ],
        "environment": {
            "python_version": sys.version,
            "platform": sys.platform,
        },
        "seeds": {
            "positive_control": 42,
            "null_control": 44,
            "live_site1": 43,
            "live_site2": 43,
            "split": 42,
            "permutation_base": 42,
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
    print("EXP-PHYSICS-33788037373: Corrected Action-Conditioned Transition Substrate")
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

    # Phase 3: Live Web
    print("\n" + "=" * 70)
    print("PHASE 3: LIVE WEB COLLECTION")
    print("=" * 70)
    live_sites, live_info = run_live_test(seed=43, n_trajectories=20, max_steps=10)

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
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  {name}: {status}")
    print(f"  Overall: {'PASS' if validity['all_passed'] else 'FAIL'}")

    # Phase 7: Verdict
    print("\n" + "=" * 70)
    print("PHASE 7: VERDICT")
    print("=" * 70)
    outcome = determine_verdict(validity, positive_metrics,
                                 perm_results.get("null_SA_vs_shuffle", {}),
                                 perm_results, live_info)
    print(f"  OUTCOME: {outcome}")

    # Determine status and map verdict to allowed outcome values
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
    outcome = outcome_mapped

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
        f"AF held-out acc={positive_metrics.get('accuracy_AF_heldout', 0):.4f}",
        f"Null control: {null_metrics.get('n_transitions', 0)} transitions, "
        f"SA held-out acc={null_metrics.get('accuracy_SA_heldout', 0):.4f}",
    ]
    for site_name, info in live_info.items():
        observations.append(
            f"Live {site_name}: {info.get('n_transitions', 0)} transitions, "
            f"{info.get('n_trajectories', 0)} trajectories"
        )

    # Validity notes
    validity_notes = []
    if not validity["all_passed"]:
        validity_notes.append("VALIDITY GATE FAILURE: see validity checks above")
    for name, check in validity["checks"].items():
        if not check["passed"]:
            validity_notes.append(f"Validity gate {name} FAILED: {check.get('issues', [])}")

    # Representation loss notes
    validity_notes.extend([
        "REPRESENTATION LOSS: HTTP fetch only, no JavaScript execution",
        "REPRESENTATION LOSS: No accessibility tree (ARIA roles, states)",
        "REPRESENTATION LOSS: No visual structure (CSS, layout, images)",
        "REPRESENTATION LOSS: Link texts may be empty (image links, aria-hidden)",
        "REPRESENTATION LOSS: Tag counts are aggregate, not hierarchical",
        "REPRESENTATION LOSS: Query string stripped from URL",
    ])

    # Unresolved
    unresolved = [
        "Whether JavaScript-heavy SPA sites show different structure",
        "Whether browser-based collection with accessibility tree reveals more structure",
        "Whether the tested representation level is sufficient for Web dynamics",
    ]

    # Write result.json
    print("\n" + "=" * 70)
    print("PHASE 8: WRITING RESULTS")
    print("=" * 70)
    all_data = {"positive": positive, "null": null, **live_sites}
    result = write_result(
        experiment_id="EXP-PHYSICS-33788037373",
        status=status,
        outcome=outcome,
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
    write_provenance(result, all_data)

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print(f"  Status: {status}")
    print(f"  Outcome: {outcome}")
    print("=" * 70)

    return result


if __name__ == "__main__":
    main()
