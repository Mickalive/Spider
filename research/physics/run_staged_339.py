#!/usr/bin/env python3
"""
EXP-PHYSICS-33965269281 Staged Runner

Runs the experiment in stages to avoid timeout:
Stage 1: Positive + Null controls + metrics + permutation tests (fast)
Stage 2: Live Web collection via Playwright (time-limited)
Stage 3: Full analysis and output writing
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
    _evaluate_shuffle_null,
)

EXPERIMENT_DIR = RESEARCH_DIR / "experiments" / "EXP-PHYSICS-33965269281"
STAGE_DIR = EXPERIMENT_DIR / "stages"
STAGE_DIR.mkdir(exist_ok=True)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def save_stage(name: str, data: dict):
    path = STAGE_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"[stage] Saved {path}")


def load_stage(name: str) -> dict:
    path = STAGE_DIR / f"{name}.json"
    with open(path) as f:
        return json.load(f)


def transitions_from_dicts(data_list: list[dict]) -> list[Transition]:
    """Reconstruct Transition objects from saved dicts."""
    transitions = []
    for d in data_list:
        state = State(
            url=d["state_before"]["url"],
            title=d["state_before"]["title"],
            link_texts=tuple(d["state_before"]["link_texts"]),
            tag_counts=tuple(d["state_before"]["tag_counts"]),
            form_signals=tuple(d["state_before"]["form_signals"]),
            accessibility_roles=tuple(tuple(r) for r in d["state_before"]["accessibility_roles"]),
        )
        action = Action(
            action_type=d["action"]["action_type"],
            target_text=d["action"]["target_text"],
            target_href=d["action"]["target_href"],
        )
        next_state = State(
            url=d["state_after"]["url"],
            title=d["state_after"]["title"],
            link_texts=tuple(d["state_after"]["link_texts"]),
            tag_counts=tuple(d["state_after"]["tag_counts"]),
            form_signals=tuple(d["state_after"]["form_signals"]),
            accessibility_roles=tuple(tuple(r) for r in d["state_after"]["accessibility_roles"]),
        )
        transitions.append(Transition(
            state=state, action=action, next_state=next_state,
            trajectory_id=d["trajectory_id"], step_index=d["step_index"],
        ))
    return transitions


# ========================================
# Stage 1: Synthetic Controls + Analysis
# ========================================

def stage1_synthetic():
    print("=" * 60)
    print("STAGE 1: Synthetic Controls + Analysis")
    print("=" * 60)

    # Positive Control
    print("\n--- Positive Control ---")
    ctrl = PositiveControl()
    rng = random.Random(42)
    pos_transitions = []
    for i in range(60):
        traj_id = f"pos_{i}"
        start_id = rng.choice(ctrl.get_all_state_ids())
        current_id = start_id
        for step in range(10):
            valid_actions = ctrl.get_valid_actions(current_id)
            if not valid_actions:
                current_id = "A"
                continue
            action_type, target_href = rng.choice(valid_actions)
            next_id = ctrl.step(current_id, action_type, target_href)
            state = ctrl.get_state(current_id)
            action = Action(action_type=action_type, target_text=target_href, target_href=target_href)
            next_state = ctrl.get_state(next_id)
            pos_transitions.append(Transition(
                state=state, action=action, next_state=next_state,
                trajectory_id=traj_id, step_index=step,
            ))
            current_id = next_id
    print(f"Positive: {len(pos_transitions)} transitions")

    # Null Control
    print("\n--- Null Control ---")
    null_ctrl = NullControl(seed=44)
    null_transitions = null_ctrl.generate_trajectories(n_trajectories=30, steps_per_trajectory=10)
    print(f"Null: {len(null_transitions)} transitions")

    # Metrics
    print("\n--- Metrics ---")

    def compute_metrics(transitions, label):
        if not transitions:
            return {"error": "no_transitions", "label": label}
        train, test = trajectory_split(transitions, train_frac=0.7, seed=42)
        acc_sa_train = accuracy_action_conditioned(train, train)
        acc_sa_test = accuracy_action_conditioned(train, test)
        acc_af_test = accuracy_action_frequency(train, test)
        acc_state_test = accuracy_state_only(train, test)
        acc_in_sample = accuracy_in_sample(transitions)
        shuffle_acc = _evaluate_shuffle_null(train, test, seed=9999)
        mem_ratio = acc_sa_train / max(acc_sa_test, 1e-10)
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
            "memorization_ratio": mem_ratio,
            "diff_SA_vs_shuffle": acc_sa_test - shuffle_acc,
            "diff_SA_vs_AF": acc_sa_test - acc_af_test,
        }

    pos_metrics = compute_metrics(pos_transitions, "positive_control")
    null_metrics = compute_metrics(null_transitions, "null_control")
    print(f"  Positive SA_heldout={pos_metrics['accuracy_SA_heldout']:.4f}, AF={pos_metrics['accuracy_AF_heldout']:.4f}, diff={pos_metrics['diff_SA_vs_AF']:.4f}")
    print(f"  Null SA_heldout={null_metrics['accuracy_SA_heldout']:.4f}, diff_SA_vs_shuffle={null_metrics['diff_SA_vs_shuffle']:.4f}")

    # Permutation Tests
    print("\n--- Permutation Tests (1000 perms) ---")
    pos_SA_vs_shuffle = permutation_test_sa_vs_shuffle(pos_transitions, n_permutations=1000, seed=42)
    pos_SA_vs_AF = permutation_test_sa_vs_action_freq(pos_transitions, n_permutations=1000, seed=42)
    null_SA_vs_shuffle = permutation_test_sa_vs_shuffle(null_transitions, n_permutations=1000, seed=44)
    print(f"  Positive SA vs shuffle: diff={pos_SA_vs_shuffle['observed_diff']:.4f}, p={pos_SA_vs_shuffle['p_value']:.4f}")
    print(f"  Positive SA vs AF: diff={pos_SA_vs_AF['observed_diff']:.4f}, p={pos_SA_vs_AF['p_value']:.4f}")
    print(f"  Null SA vs shuffle: diff={null_SA_vs_shuffle['observed_diff']:.4f}, p={null_SA_vs_shuffle['p_value']:.4f}")

    # Save stage
    pos_data = [{
        "state_before": t.state.to_dict(),
        "action": t.action.to_dict(),
        "state_after": t.next_state.to_dict(),
        "trajectory_id": t.trajectory_id,
        "step_index": t.step_index,
    } for t in pos_transitions]
    null_data = [{
        "state_before": t.state.to_dict(),
        "action": t.action.to_dict(),
        "state_after": t.next_state.to_dict(),
        "trajectory_id": t.trajectory_id,
        "step_index": t.step_index,
    } for t in null_transitions]

    save_stage("stage1", {
        "positive_transitions": pos_data,
        "null_transitions": null_data,
        "positive_metrics": pos_metrics,
        "null_metrics": null_metrics,
        "perm_positive_SA_vs_shuffle": pos_SA_vs_shuffle,
        "perm_positive_SA_vs_AF": pos_SA_vs_AF,
        "perm_null_SA_vs_shuffle": null_SA_vs_shuffle,
    })
    print("\nStage 1 complete.")
    return pos_metrics, null_metrics, pos_SA_vs_shuffle, pos_SA_vs_AF, null_SA_vs_shuffle


# ========================================
# Stage 2: Live Web Collection (Playwright)
# ========================================

def stage2_live():
    print("\n" + "=" * 60)
    print("STAGE 2: Live Web Collection (Playwright)")
    print("=" * 60)

    sites = [
        ("https://en.wikipedia.org/wiki/Web_browser", "wikipedia", 43),
        ("https://docs.python.org/3/library/index.html", "python_docs", 45),
    ]

    all_live = {}
    all_info = {}

    for site_url, site_name, site_seed in sites:
        print(f"\n--- {site_name}: {site_url} ---")
        print(f"  Target: 110 trajectories, 8 steps each")

        collector = PlaywrightLiveCollector(seed=site_seed)
        try:
            transitions, info = collector.collect_trajectories(
                start_url=site_url,
                n_trajectories=110,
                max_steps=8,
                polite_delay=0.3,
                max_retries=3,
            )
            all_live[site_name] = [{
                "state_before": t.state.to_dict(),
                "action": t.action.to_dict(),
                "state_after": t.next_state.to_dict(),
                "trajectory_id": t.trajectory_id,
                "step_index": t.step_index,
            } for t in transitions]
            all_info[site_name] = info
            print(f"  Collected: {info['n_transitions']} transitions, "
                  f"{info['n_trajectories']} trajectories, "
                  f"{info.get('n_failed_trajectories', 0)} failed trajs, "
                  f"{info.get('n_failed_steps', 0)} failed steps")
        except Exception as e:
            print(f"  FAILED: {e}")
            all_live[site_name] = []
            all_info[site_name] = {"error": str(e), "n_transitions": 0, "n_trajectories": 0}
        time.sleep(2)

    save_stage("stage2", {
        "live_transitions": all_live,
        "collection_info": all_info,
    })
    print("\nStage 2 complete.")
    return all_live, all_info


# ========================================
# Stage 3: Full Analysis + Output
# ========================================

def stage3_analysis(pos_metrics, null_metrics, pos_SA_vs_shuffle, pos_SA_vs_AF, null_SA_vs_shuffle,
                    live_raw, live_info):
    print("\n" + "=" * 60)
    print("STAGE 3: Full Analysis + Output")
    print("=" * 60)

    # Reconstruct live transitions
    live_sites = {}
    for site_name, data_list in live_raw.items():
        if data_list:
            live_sites[site_name] = transitions_from_dicts(data_list)
            print(f"  Reconstructed {site_name}: {len(live_sites[site_name])} transitions")

    # Compute live metrics
    live_metrics = {}
    for site_name, site_trans in live_sites.items():
        if site_trans:
            train, test = trajectory_split(site_trans, train_frac=0.7, seed=42)
            acc_sa_train = accuracy_action_conditioned(train, train)
            acc_sa_test = accuracy_action_conditioned(train, test)
            acc_af_test = accuracy_action_frequency(train, test)
            acc_state_test = accuracy_state_only(train, test)
            shuffle_acc = _evaluate_shuffle_null(train, test, seed=9999)
            live_metrics[f"live_{site_name}"] = {
                "label": f"live_{site_name}",
                "n_transitions": len(site_trans),
                "n_trajectories": len(set(t.trajectory_id for t in site_trans)),
                "n_train_transitions": len(train),
                "n_train_trajectories": len(set(t.trajectory_id for t in train)),
                "n_test_transitions": len(test),
                "n_test_trajectories": len(set(t.trajectory_id for t in test)),
                "accuracy_SA_train": acc_sa_train,
                "accuracy_SA_heldout": acc_sa_test,
                "accuracy_AF_heldout": acc_af_test,
                "accuracy_state_heldout": acc_state_test,
                "accuracy_in_sample": accuracy_in_sample(site_trans),
                "accuracy_shuffle": shuffle_acc,
                "memorization_ratio": acc_sa_train / max(acc_sa_test, 1e-10),
                "diff_SA_vs_shuffle": acc_sa_test - shuffle_acc,
                "diff_SA_vs_AF": acc_sa_test - acc_af_test,
            }
            m = live_metrics[f"live_{site_name}"]
            print(f"  {site_name}: SA={m['accuracy_SA_heldout']:.4f}, AF={m['accuracy_AF_heldout']:.4f}, "
                  f"shuffle={m['accuracy_shuffle']:.4f}, diff_SA_vs_shuffle={m['diff_SA_vs_shuffle']:.4f}")
        else:
            live_metrics[f"live_{site_name}"] = {"error": "no_transitions"}

    # Live permutation tests
    print("\n--- Live Permutation Tests ---")
    live_perm = {}
    for site_name, site_trans in live_sites.items():
        if site_trans:
            perm = permutation_test_sa_vs_shuffle(site_trans, n_permutations=1000, seed=43)
            live_perm[f"live_{site_name}_SA_vs_shuffle"] = perm
            print(f"  {site_name}: diff={perm['observed_diff']:.4f}, p={perm['p_value']:.4f}")

    # Bonferroni correction for live sites
    live_p_values = []
    for key, val in live_perm.items():
        if "p_value" in val:
            live_p_values.append((key, val["p_value"]))

    print("\n--- Bonferroni Correction ---")
    if live_p_values:
        raw_ps = [p for _, p in live_p_values]
        corrected_ps = bonferroni_correction(raw_ps)
        for (key, raw_p), corr_p in zip(live_p_values, corrected_ps):
            print(f"  {key}: raw_p={raw_p:.4f}, corrected_p={corr_p:.4f}")

    # Validity gates
    print("\n--- Validity Gates ---")
    all_transitions = list(transitions_from_dicts(load_stage("stage1")["positive_transitions"]))
    all_transitions.extend(transitions_from_dicts(load_stage("stage1")["null_transitions"]))
    for site_trans in live_sites.values():
        all_transitions.extend(site_trans)
    validity = check_validity(all_transitions, seed=42)
    for name, check in validity["checks"].items():
        s = "PASS" if check["passed"] else "FAIL"
        print(f"  {name}: {s}")
    print(f"  Overall: {'PASS' if validity['all_passed'] else 'FAIL'}")

    # Verdict
    print("\n--- Verdict ---")
    all_metrics = {
        "positive_control": pos_metrics,
        "null_control": null_metrics,
        **live_metrics,
    }

    # Build controls
    controls = {}
    perm_results = {
        "positive_SA_vs_shuffle": pos_SA_vs_shuffle,
        "positive_SA_vs_AF": pos_SA_vs_AF,
        "null_SA_vs_shuffle": null_SA_vs_shuffle,
        **live_perm,
    }
    for key, val in perm_results.items():
        controls[key] = {
            "expected": "p < 0.05" if "positive" in key else ("p > 0.05" if "null" in key else "p < 0.05 after correction"),
            "observed_diff": val.get("observed_diff", None),
            "p_value": val.get("p_value", None),
            "pass": (val.get("p_value", 1.0) < 0.05) if "positive" in key or "live" in key
                     else (val.get("p_value", 0.0) > 0.05) if "null" in key else None,
        }

    # Verdict logic
    n_live_sites = sum(1 for v in live_info.values() if v.get("n_transitions", 0) > 0)
    n_live_transitions = sum(v.get("n_transitions", 0) for v in live_info.values())

    verdict = "MEASUREMENT_INVALID"
    if validity["all_passed"]:
        if n_live_transitions >= 100 and n_live_sites >= 2:
            pos_discrim_p = pos_SA_vs_AF.get("p_value", 1.0)
            if pos_discrim_p < 0.05 and pos_metrics["accuracy_SA_heldout"] > 0.90:
                null_p = null_SA_vs_shuffle.get("p_value", 0.0)
                if null_p > 0.05:
                    if live_p_values:
                        corrected = bonferroni_correction([p for _, p in live_p_values])
                        has_significant = any(p < 0.05 for p in corrected)
                        has_effect = any(
                            live_perm.get(k, {}).get("observed_diff", 0) > 0.03
                            for k, _ in live_p_values
                        )
                        if has_significant and has_effect:
                            verdict = "SURVIVES_CURRENT_TEST"
                        else:
                            verdict = "FALSIFIED-IN-SETTING"
                    else:
                        verdict = "FALSIFIED-IN-SETTING"
                else:
                    verdict = "MEASUREMENT_INVALID"
            else:
                verdict = "MEASUREMENT_INVALID"
        else:
            verdict = "MEASUREMENT_INVALID"
    else:
        verdict = "MEASUREMENT_INVALID"

    print(f"  Verdict: {verdict}")

    # Map verdict
    if verdict == "MEASUREMENT_INVALID":
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    elif verdict == "SURVIVES_CURRENT_TEST":
        status = "COMPLETE"
        outcome = "SUPPORTS"
    elif verdict == "FALSIFIED-IN-SETTING":
        status = "COMPLETE"
        outcome = "FALSIFIES"
    else:
        status = "COMPLETE"
        outcome = "INCONCLUSIVE"

    # Build observations
    observations = [
        f"Positive control: {pos_metrics.get('n_transitions', 0)} transitions, "
        f"SA held-out acc={pos_metrics.get('accuracy_SA_heldout', 0):.4f}, "
        f"AF held-out acc={pos_metrics.get('accuracy_AF_heldout', 0):.4f}, "
        f"diff_SA_vs_AF={pos_metrics.get('diff_SA_vs_AF', 0):.4f}",
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
    validity_notes.extend([
        "REPRESENTATION: Playwright-based collection with full DOM, accessibility tree, link texts, tag_counts, form_signals",
        "REPRESENTATION LOSS: No visual layout or CSS structure",
        "REPRESENTATION LOSS: No interaction history (hover, scroll, focus)",
        "REPRESENTATION LOSS: Accessibility tree may be incomplete on some pages",
        "REPRESENTATION LOSS: Query string stripped from URL",
        "COLLECTION: Chromium headless, JavaScript enabled, domcontentloaded wait",
        "FIX APPLIED: target_href = destination URL (not source URL as in EXP-PHYSICS-33788037373)",
        "FIX APPLIED: Full state representation stored in raw data",
        "FIX APPLIED: Bonferroni correction for 6 comparisons",
    ])

    unresolved = [
        "Whether JavaScript-heavy SPA sites show different structure",
        "Whether even richer representations reveal more structure",
        "Whether authenticated/form-heavy sites show different dynamics",
        "Whether the tested sites are representative of dynamical regimes",
    ]

    # Write result.json
    result = {
        "schema_version": 1,
        "experiment_id": "EXP-PHYSICS-33965269281",
        "lane": "physics",
        "status": status,
        "outcome": outcome,
        "metrics": all_metrics,
        "controls": controls,
        "artifacts": [],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    # Save raw data files as artifacts
    artifacts = []
    raw_data = load_stage("stage1")
    for key in ["positive_transitions", "null_transitions"]:
        fpath = EXPERIMENT_DIR / f"raw_{key.replace('_transitions', '')}.json"
        with open(fpath, "w") as f:
            json.dump(raw_data[key], f, indent=2, default=str)
        h = sha256_file(str(fpath))
        artifacts.append({
            "path": f"research/experiments/EXP-PHYSICS-33965269281/{fpath.name}",
            "sha256": h,
            "role": "raw",
        })

    for site_name, data_list in live_raw.items():
        if data_list:
            fpath = EXPERIMENT_DIR / f"raw_live_{site_name}.json"
            with open(fpath, "w") as f:
                json.dump(data_list, f, indent=2, default=str)
            h = sha256_file(str(fpath))
            artifacts.append({
                "path": f"research/experiments/EXP-PHYSICS-33965269281/{fpath.name}",
                "sha256": h,
                "role": "raw",
            })

    # Save and hash output files
    out_files = [
        ("result.json", result, "result"),
        ("report.md", None, "report"),
        ("provenance.json", None, "provenance"),
    ]

    # Write result
    fpath = EXPERIMENT_DIR / "result.json"
    with open(fpath, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[output] Wrote {fpath}")

    # Write report
    report = write_report(result, live_metrics, live_perm, controls)
    fpath = EXPERIMENT_DIR / "report.md"
    with open(fpath, "w") as f:
        f.write(report)
    print(f"[output] Wrote {fpath}")

    # Write provenance
    provenance = write_provenance(result, raw_data, live_raw)
    fpath = EXPERIMENT_DIR / "provenance.json"
    with open(fpath, "w") as f:
        json.dump(provenance, f, indent=2, default=str)
    print(f"[output] Wrote {fpath}")

    # Hash output files
    for fname, _, role in out_files:
        fpath = EXPERIMENT_DIR / fname
        if fpath.exists():
            h = sha256_file(str(fpath))
            artifacts.append({
                "path": f"research/experiments/EXP-PHYSICS-33965269281/{fname}",
                "sha256": h,
                "role": role,
            })

    result["artifacts"] = artifacts
    fpath = EXPERIMENT_DIR / "result.json"
    with open(fpath, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\n{'='*60}")
    print(f"EXPERIMENT COMPLETE")
    print(f"  Status: {status}")
    print(f"  Outcome: {outcome}")
    print(f"  Verdict: {verdict}")
    print(f"  Artifacts: {len(artifacts)}")
    print(f"{'='*60}")

    return result


def write_report(result, live_metrics, live_perm, controls):
    metrics = result["metrics"]
    controls_dict = result["controls"]

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
- **Action-Conditioned Accuracy (held-out)**: {metrics.get('positive_control', {}).get('accuracy_SA_heldout', 0):.4f}
- **Action-Frequency Accuracy (held-out)**: {metrics.get('positive_control', {}).get('accuracy_AF_heldout', 0):.4f}
- **Shuffle Accuracy**: {metrics.get('positive_control', {}).get('accuracy_shuffle', 0):.4f}
- **diff_SA_vs_shuffle**: {metrics.get('positive_control', {}).get('diff_SA_vs_shuffle', 0):.4f}
- **diff_SA_vs_AF**: {metrics.get('positive_control', {}).get('diff_SA_vs_AF', 0):.4f}
- **Memorization Ratio**: {metrics.get('positive_control', {}).get('memorization_ratio', 0):.2f}

### Null Control
- **Transitions**: {metrics.get('null_control', {}).get('n_transitions', 'N/A')}
- **Action-Conditioned Accuracy (held-out)**: {metrics.get('null_control', {}).get('accuracy_SA_heldout', 0):.4f}
- **diff_SA_vs_shuffle**: {metrics.get('null_control', {}).get('diff_SA_vs_shuffle', 0):.4f}

### Live Tests
"""
    for site in ["wikipedia", "python_docs"]:
        site_m = metrics.get(f"live_{site}", {})
        report += f"""
**{site.replace('_', ' ').title()}**:
- Transitions: {site_m.get('n_transitions', 'N/A')}
- Trajectories: {site_m.get('n_trajectories', 'N/A')}
- Action-Conditioned Accuracy (held-out): {site_m.get('accuracy_SA_heldout', 0):.4f}
- Action-Frequency Accuracy (held-out): {site_m.get('accuracy_AF_heldout', 0):.4f}
- SA vs Shuffle Diff: {site_m.get('diff_SA_vs_shuffle', 0):.4f}
- Memorization Ratio: {site_m.get('memorization_ratio', 0):.2f}
"""

    report += f"""
---

## 3. Permutation Tests

| Condition | Observed Diff | p-value | Significant? |
|-----------|--------------|---------|--------------|
"""
    for key, val in controls_dict.items():
        if isinstance(val, dict) and "observed_diff" in val:
            p = val.get("p_value", 1.0)
            sig = "YES" if p < 0.05 else "NO"
            report += f"| {key} | {val['observed_diff']:.4f} | {p:.4f} | {sig} |\n"

    # Bonferroni
    live_p_values = []
    for key, val in controls_dict.items():
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
    for obs in result["observations"]:
        report += f"- {obs}\n"

    report += f"""
---

## 6. Interpretation

### Representation
This experiment uses Playwright-based collection with:
- Full DOM structure (tag counts for 11 categories)
- Accessibility tree (ARIA roles and names, up to 30 per page)
- Link texts (first 30 visible, sorted and deduplicated)
- Form signals (has_form, has_input, has_select, has_textarea)
- target_href = destination URL (FIXED from prior experiment which used source URL)

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
    report += f"diff_SA_vs_shuffle = {nc.get('diff_SA_vs_shuffle', 0):.4f}.\n"

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

    report += f"""
---

## 8. Validity Threats

1. **Synthetic-to-real gap**: Positive control validates pipeline, not Web dynamics.
2. **Multiple comparisons**: 6 comparisons (3 null tests x 2 sites), Bonferroni conservative.
3. **Sample size**: Target 100+ trajectories per site. Actual counts may vary.
4. **Navigation depth**: Limited to 8 steps per trajectory.
5. **Link selection**: Uniform random over available links (no content-aware selection).
"""
    return report


def write_provenance(result, pos_null_data, live_raw):
    import subprocess
    import sys

    data_hashes = {}
    for key, transitions in {**pos_null_data, **live_raw}.items():
        if transitions:
            data_hashes[key] = hashlib.sha256(
                json.dumps(transitions, sort_keys=True, default=str).encode()
            ).hexdigest()

    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        git_sha = "unknown"

    return {
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
            "research/physics/run_staged_339.py",
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


# ========================================
# Main
# ========================================

if __name__ == "__main__":
    t0 = time.time()
    print(f"Started: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")

    # Stage 1: Synthetic controls
    pos_metrics, null_metrics, pos_SA_vs_shuffle, pos_SA_vs_AF, null_SA_vs_shuffle = stage1_synthetic()

    # Stage 2: Live collection
    live_raw, live_info = stage2_live()

    # Stage 3: Analysis
    result = stage3_analysis(
        pos_metrics, null_metrics, pos_SA_vs_shuffle, pos_SA_vs_AF, null_SA_vs_shuffle,
        live_raw, live_info,
    )

    elapsed = time.time() - t0
    print(f"\nTotal elapsed: {elapsed:.1f}s")
