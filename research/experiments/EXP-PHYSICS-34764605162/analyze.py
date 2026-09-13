#!/usr/bin/env python3
"""
EXP-PHYSICS-34764605162 — Conditional PMI Analysis (v3)

Tests whether DOM structural features encode predictive state variation
beyond action-history memory on non-deterministic SPAs.

Correctly shuffles DOM labels within (URL, ActionHistory_K) strata.
"""

import hashlib
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict

random.seed(42)

RAW_DATA_PATH = "research/experiments/EXP-PHYSICS-34764605162/raw_dom_captures.json"
OUTPUT_DIR = "research/experiments/EXP-PHYSICS-34764605162"
SPA_TYPES = ["deterministic", "random_API", "timing_dependent"]
NON_DETERMINISTIC_TYPES = ["random_API", "timing_dependent"]
HISTORY_LENGTHS = [1, 2, 3]
N_PERMUTATIONS = 1000
ALPHA = 0.05
N_COMPARISONS = 24
BONFERRONI_ALPHA = ALPHA / N_COMPARISONS
START_TOKEN = "<START>"
MIN_STRATUM_COUNT = 5
REPRESENTATIONS = [
    "visible_text_hash",
    "accessibility_tree_hash",
    "multi_feature_hash",
    "numeric_structural",
]


def load_data():
    with open(RAW_DATA_PATH) as f:
        return json.load(f)


def get_action_label(action):
    return f"{action['type']}:{action['target_href']}"


def get_dom_representation(dom_features, rep_name):
    if rep_name == "numeric_structural":
        ns = dom_features["numeric_structural"]
        return f"ns:{ns['element_count']}|{ns['tree_depth']}|{ns['interactive_density']}|{ns['form_count']}"
    return dom_features[rep_name]


def build_strata(transitions, K):
    """Group transitions by (URL, ActionHistory_K) stratum."""
    trajectories = defaultdict(list)
    for t in transitions:
        trajectories[t["trajectory_id"]].append(t)

    strata = defaultdict(list)
    for traj_id, steps in trajectories.items():
        steps_sorted = sorted(steps, key=lambda x: x["step"])
        action_seq = [get_action_label(s["action"]) for s in steps_sorted]
        for i, s in enumerate(steps_sorted):
            start = max(0, i - K + 1)
            hist = action_seq[start : i + 1]
            while len(hist) < K:
                hist = [START_TOKEN] + hist
            h = tuple(hist)
            url = s["url"]
            strata[(url, h)].append(s)

    return strata


def compute_pmi_from_strata(strata, rep_name, total_transitions):
    """Compute conditional PMI from pre-computed strata."""
    total_pmi = 0.0
    total_weight = 0
    n_strata_used = 0

    for (url, h), h_transitions in strata.items():
        n_h = len(h_transitions)
        if n_h < MIN_STRATUM_COUNT:
            continue

        joint = Counter()
        marginal_r = Counter()
        marginal_s = Counter()

        for t in h_transitions:
            r = get_dom_representation(t["state_before"]["dom_features"], rep_name)
            s = t["state_after"]["dom_features"]["visible_text_hash"]
            joint[(r, s)] += 1
            marginal_r[r] += 1
            marginal_s[s] += 1

        stratum_pmi = 0.0
        for (r, s), count in joint.items():
            p_rs = count / n_h
            p_r = marginal_r[r] / n_h
            p_s = marginal_s[s] / n_h
            if p_rs > 0 and p_r > 0 and p_s > 0:
                stratum_pmi += p_rs * math.log2(p_rs / (p_r * p_s))

        weight = n_h / total_transitions
        total_pmi += weight * stratum_pmi
        total_weight += n_h
        n_strata_used += 1

    return total_pmi, total_weight, n_strata_used


def permutation_test(strata, rep_name, total_transitions, n_perms=N_PERMUTATIONS):
    """Shuffle DOM labels within (URL, ActionHistory) strata, recompute PMI."""
    perm_pmis = []
    for _ in range(n_perms):
        shuffled_strata = {}
        for (url, h), h_trans in strata.items():
            n_h = len(h_trans)
            if n_h < MIN_STRATUM_COUNT:
                shuffled_strata[(url, h)] = h_trans
                continue

            # Extract DOM representation labels and shuffle
            dom_reps = [
                get_dom_representation(t["state_before"]["dom_features"], rep_name)
                for t in h_trans
            ]
            random.shuffle(dom_reps)

            # Create shuffled transitions
            shuffled_trans = []
            for i, t in enumerate(h_trans):
                t_copy = dict(t)
                t_copy["state_before"] = dict(t["state_before"])
                t_copy["state_before"]["dom_features"] = dict(t["state_before"]["dom_features"])
                # Store shuffled rep for PMI computation
                t_copy["_shuffled_rep"] = dom_reps[i]
                shuffled_trans.append(t_copy)
            shuffled_strata[(url, h)] = shuffled_trans

        # Compute PMI on shuffled data
        total_pmi = 0.0
        total_weight = 0
        for (url, h), h_trans in shuffled_strata.items():
            n_h = len(h_trans)
            if n_h < MIN_STRATUM_COUNT:
                continue
            joint = Counter()
            marginal_r = Counter()
            marginal_s = Counter()
            for t in h_trans:
                r = t["_shuffled_rep"]
                s = t["state_after"]["dom_features"]["visible_text_hash"]
                joint[(r, s)] += 1
                marginal_r[r] += 1
                marginal_s[s] += 1
            stratum_pmi = 0.0
            for (r, s), count in joint.items():
                p_rs = count / n_h
                p_r = marginal_r[r] / n_h
                p_s = marginal_s[s] / n_h
                if p_rs > 0 and p_r > 0 and p_s > 0:
                    stratum_pmi += p_rs * math.log2(p_rs / (p_r * p_s))
            weight = n_h / total_transitions
            total_pmi += weight * stratum_pmi
            total_weight += n_h

        perm_pmis.append(total_pmi)

    return perm_pmis


def compute_action_history_prediction(strata):
    """Accuracy of predicting S_next from ActionHistory alone."""
    correct = 0
    total = 0

    for (url, h), h_trans in strata.items():
        n_h = len(h_trans)
        if n_h < MIN_STRATUM_COUNT:
            continue
        s_next_counts = Counter()
        for t in h_trans:
            s_next = t["state_after"]["dom_features"]["visible_text_hash"]
            s_next_counts[s_next] += 1
        most_frequent = s_next_counts.most_common(1)[0][0]
        correct += sum(
            1 for t in h_trans
            if t["state_after"]["dom_features"]["visible_text_hash"] == most_frequent
        )
        total += n_h

    return correct / total if total > 0 else 0


def compute_determinism_check(transitions):
    """P(S_next | S_current, Action) using DOM hashes."""
    sa_map = defaultdict(Counter)
    for t in transitions:
        s = t["state_before"]["dom_features"]["visible_text_hash"]
        a = t["action"]["type"]
        s_next = t["state_after"]["dom_features"]["visible_text_hash"]
        sa_map[(s, a)][s_next] += 1

    total = 0
    deterministic = 0
    n_pairs = 0
    n_det_pairs = 0
    for (s, a), counts in sa_map.items():
        n = sum(counts.values())
        most_common = counts.most_common(1)[0][1]
        deterministic += most_common
        total += n
        n_pairs += 1
        if len(counts) == 1:
            n_det_pairs += 1

    return deterministic / total if total > 0 else 0, n_det_pairs / n_pairs if n_pairs > 0 else 0


def compute_positive_control(transitions):
    """Random DOM labels independent of state/action."""
    rng = random.Random(9999)
    shuffled = []
    for t in transitions:
        t_copy = dict(t)
        t_copy["state_before"] = dict(t["state_before"])
        t_copy["state_before"]["dom_features"] = dict(t["state_before"]["dom_features"])
        random_hash = hashlib.sha256(str(rng.randint(0, 1000000)).encode()).hexdigest()
        t_copy["state_before"]["dom_features"]["visible_text_hash"] = random_hash
        shuffled.append(t_copy)

    strata = build_strata(shuffled, 3)
    pmi, _, _ = compute_pmi_from_strata(strata, "visible_text_hash", len(shuffled))

    perm_pmis = permutation_test(strata, "visible_text_hash", len(shuffled), n_perms=100)
    perm_mean = sum(perm_pmis) / len(perm_pmis)
    perm_std = (sum((p - perm_mean) ** 2 for p in perm_pmis) / len(perm_pmis)) ** 0.5

    return {
        "conditional_pmi": pmi,
        "expected": 0.0,
        "pass": abs(pmi) < 3 * perm_std if perm_std > 0 else abs(pmi) < 0.01,
        "perm_mean": perm_mean,
        "perm_std": perm_std,
    }


def compute_null_control(transitions):
    """Shuffle DOM labels within strata."""
    strata = build_strata(transitions, 3)
    perm_pmis = permutation_test(strata, "visible_text_hash", len(transitions), n_perms=100)
    perm_mean = sum(perm_pmis) / len(perm_pmis)
    perm_std = (sum((p - perm_mean) ** 2 for p in perm_pmis) / len(perm_pmis)) ** 0.5

    return {
        "null_mean_pmi": perm_mean,
        "null_std": perm_std,
        "expected": 0.0,
        "pass": abs(perm_mean) < 3 * perm_std if perm_std > 0 else abs(perm_mean) < 0.01,
    }


def main():
    print("=" * 70)
    print("EXP-PHYSICS-34764605162 — Conditional PMI Analysis v3")
    print("=" * 70)

    data = load_data()
    results = {"site_results": {}, "controls": {}}

    for spa_type in SPA_TYPES:
        print(f"\n{'─' * 50}")
        print(f"SPA Type: {spa_type}")
        print(f"{'─' * 50}")
        transitions = data[spa_type]
        n_trans = len(transitions)
        print(f"  Transitions: {n_trans}")

        spa_result = {"n_transitions": n_trans}

        # Determinism check
        dom_det_acc, dom_det_pairs = compute_determinism_check(transitions)
        spa_result["determinism_accuracy"] = dom_det_acc
        spa_result["deterministic_pairs_fraction"] = dom_det_pairs
        print(f"  DOM determinism: {dom_det_acc:.4f} ({dom_det_pairs:.4f} pairs deterministic)")

        spa_result["conditional_pmi"] = {}
        spa_result["permutation_tests"] = {}
        spa_result["action_history_prediction"] = {}

        for rep_name in REPRESENTATIONS:
            spa_result["conditional_pmi"][rep_name] = {}
            spa_result["permutation_tests"][rep_name] = {}
            spa_result["action_history_prediction"][rep_name] = {}

            for K in HISTORY_LENGTHS:
                strata = build_strata(transitions, K)

                # Conditional PMI
                cond_pmi, weight, n_strata = compute_pmi_from_strata(
                    strata, rep_name, n_trans
                )
                spa_result["conditional_pmi"][rep_name][f"K{K}"] = {
                    "value": cond_pmi,
                    "weighted_transitions": weight,
                    "n_strata": n_strata,
                }

                # Action-history prediction
                ah_acc = compute_action_history_prediction(strata)
                spa_result["action_history_prediction"][rep_name][f"K{K}"] = ah_acc

                # Permutation test
                perm_pmis = permutation_test(strata, rep_name, n_trans, N_PERMUTATIONS)
                n_exceed = sum(1 for p in perm_pmis if p >= cond_pmi)
                p_value = n_exceed / N_PERMUTATIONS
                perm_mean = sum(perm_pmis) / len(perm_pmis)
                perm_std = (sum((p - perm_mean) ** 2 for p in perm_pmis) / len(perm_pmis)) ** 0.5

                spa_result["permutation_tests"][rep_name][f"K{K}"] = {
                    "observed_pmi": cond_pmi,
                    "n_exceed": n_exceed,
                    "n_perms": N_PERMUTATIONS,
                    "p_value_raw": p_value,
                    "p_value_bonferroni": min(p_value * N_COMPARISONS, 1.0),
                    "perm_mean": perm_mean,
                    "perm_std": perm_std,
                    "perm_pmi_sample": perm_pmis[:20],
                }

                print(
                    f"  {rep_name} K={K}: PMI={cond_pmi:.6f}, "
                    f"p_bonf={min(p_value * N_COMPARISONS, 1.0):.4f}, "
                    f"AH_acc={ah_acc:.4f}, strata={n_strata}"
                )

        results["site_results"][spa_type] = spa_result

    # ── Controls ──
    print(f"\n{'─' * 50}")
    print("Controls")
    print(f"{'─' * 50}")

    det_transitions = data["deterministic"]

    pos_control = compute_positive_control(det_transitions)
    results["controls"]["positive_control_random_labels"] = pos_control
    print(f"  Positive control: PMI={pos_control['conditional_pmi']:.6f}, pass={pos_control['pass']}")

    null_control = compute_null_control(det_transitions)
    results["controls"]["null_control_shuffled"] = null_control
    print(f"  Null control: mean_PMI={null_control['null_mean_pmi']:.6f}, pass={null_control['pass']}")

    det_dom_acc = results["site_results"]["deterministic"]["determinism_accuracy"]
    rand_dom_acc = results["site_results"]["random_API"]["determinism_accuracy"]
    timing_dom_acc = results["site_results"]["timing_dependent"]["determinism_accuracy"]
    det_pass = det_dom_acc >= 1.0
    nondet_pass = rand_dom_acc < 1.0 and timing_dom_acc < 1.0
    results["controls"]["determinism_control"] = {
        "deterministic_accuracy": det_dom_acc,
        "random_API_accuracy": rand_dom_acc,
        "timing_dependent_accuracy": timing_dom_acc,
        "pass": det_pass and nondet_pass,
    }
    print(f"  Determinism: det={det_dom_acc:.4f}, rand={rand_dom_acc:.4f}, timing={timing_dom_acc:.4f}, pass={det_pass and nondet_pass}")

    min_trans = min(len(data[s]) for s in SPA_TYPES)
    results["controls"]["data_quality"] = {
        "min_transitions_per_type": min_trans,
        "threshold": 300,
        "pass": min_trans >= 300,
    }
    print(f"  Data quality: min_transitions={min_trans}, pass={min_trans >= 300}")

    # ── Decision Rule ──
    print(f"\n{'=' * 70}")
    print("DECISION RULE")
    print(f"{'=' * 70}")

    nondet_surviving = 0
    for spa_type in NON_DETERMINISTIC_TYPES:
        pt = results["site_results"][spa_type]["permutation_tests"]["visible_text_hash"]["K3"]
        pmi = pt["observed_pmi"]
        p_bonf = pt["p_value_bonferroni"]
        survives = pmi > 0.0 and p_bonf < BONFERRONI_ALPHA
        if survives:
            nondet_surviving += 1
        print(f"  {spa_type} visible_text_hash K=3: PMI={pmi:.6f}, p_bonf={p_bonf:.4f}, survives={survives}")

    # Check all representations
    all_nondet_nonsignificant = True
    best_pmi_nondet = 0.0
    best_rep_nondet = ""
    best_type_nondet = ""
    for spa_type in NON_DETERMINISTIC_TYPES:
        for rep_name in REPRESENTATIONS:
            pt = results["site_results"][spa_type]["permutation_tests"][rep_name]["K3"]
            if pt["observed_pmi"] > best_pmi_nondet:
                best_pmi_nondet = pt["observed_pmi"]
                best_rep_nondet = rep_name
                best_type_nondet = spa_type
            if pt["observed_pmi"] > 0.0 and pt["p_value_bonferroni"] < BONFERRONI_ALPHA:
                all_nondet_nonsignificant = False

    det_pmi_k3 = results["site_results"]["deterministic"]["permutation_tests"]["visible_text_hash"]["K3"]["observed_pmi"]
    det_baseline_ok = abs(det_pmi_k3) < 0.05

    cond1 = nondet_surviving >= 2
    cond2 = pos_control["pass"]
    cond3 = null_control["pass"]
    cond4 = det_pass and nondet_pass
    cond5 = results["controls"]["data_quality"]["pass"]

    all_conditions = cond1 and cond2 and cond3 and cond4 and cond5 and det_baseline_ok

    print(f"\n  Conditions:")
    print(f"    1. PMI significant on >=2/2 non-det types: {cond1} ({nondet_surviving}/2)")
    print(f"    2. Positive control passes: {cond2}")
    print(f"    3. Null control passes: {cond3}")
    print(f"    4. Determinism check: {cond4}")
    print(f"    5. Data quality: {cond5}")
    print(f"    6. Deterministic baseline ~0 (PMI={det_pmi_k3:.6f}): {det_baseline_ok}")
    print(f"    Best PMI: {best_pmi_nondet:.6f} ({best_type_nondet}, {best_rep_nondet})")

    if all_conditions:
        verdict = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
    elif all_nondet_nonsignificant or not cond2 or not cond3 or not det_baseline_ok or not cond4:
        verdict = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
    else:
        verdict = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"

    print(f"\n  VERDICT: {verdict}")
    print(f"  OUTCOME: {outcome}")

    results["decision"] = {
        "verdict": verdict,
        "outcome": outcome,
        "conditions": {
            "pmi_significant_nondet_types": cond1,
            "n_nondet_surviving": nondet_surviving,
            "n_nondet_total": len(NON_DETERMINISTIC_TYPES),
            "positive_control_pass": cond2,
            "null_control_pass": cond3,
            "determinism_check_pass": cond4,
            "data_quality_pass": cond5,
            "deterministic_baseline_pmi_k3": det_pmi_k3,
            "deterministic_baseline_ok": det_baseline_ok,
            "all_nondet_nonsignificant_all_reps": all_nondet_nonsignificant,
            "best_pmi_nondet": best_pmi_nondet,
            "best_rep_nondet": best_rep_nondet,
            "best_type_nondet": best_type_nondet,
        },
        "bonferroni_alpha": BONFERRONI_ALPHA,
        "n_comparisons": N_COMPARISONS,
    }

    output_path = os.path.join(OUTPUT_DIR, "raw_analysis_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nRaw results saved to {output_path}")

    return results


if __name__ == "__main__":
    main()
