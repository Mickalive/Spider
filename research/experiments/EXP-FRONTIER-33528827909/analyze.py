#!/usr/bin/env python3
"""
EXP-FRONTIER-33528827909: Regime-dependent action-conditioned prediction.

Frozen experiment code. Do not modify after freeze.

Generates synthetic Web-like transitions with controlled action-dependence
parameter lambda. Measures whether rule-memory accuracy difference scales
monotonically with lambda, testing dynamical heterogeneity.
"""

import json
import hashlib
import numpy as np
from collections import Counter, defaultdict
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def to_native(obj):
    """Recursively convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_native(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


# === FROZEN PARAMETERS (from prereg) ===
SEED = 42
FUNCTION_SEEDS = [42, 43, 44]
LAMBDA_LEVELS = [0.0, 0.25, 0.5, 1.0]
STATES = list(range(10))  # {0, 1, ..., 9}
ACTIONS = ['click', 'fill', 'submit', 'navigate']
N_TRANSITIONS = 250  # per lambda per function
TRAIN_FRACTION = 0.8
ALPHA = 0.05

# === DETERMINISTIC FUNCTIONS ===
def make_deterministic_function(seed):
    """Create a frozen lookup table mapping (state, action) -> next_state.
    Each function is a permutation of states for each action."""
    rng = np.random.RandomState(seed)
    table = {}
    for action in ACTIONS:
        perm = rng.permutation(STATES)
        for s, ns in zip(STATES, perm):
            table[(s, action)] = ns
    return table


# === DATA GENERATION ===
def generate_transitions(det_func, lambda_val, n, rng):
    """Generate synthetic transitions (S_t, A_t, S_{t+1}).
    With probability lambda: S_{t+1} = det_func(S_t, A_t)
    With probability (1-lambda): S_{t+1} = uniform random from STATES
    """
    transitions = []
    for _ in range(n):
        s = rng.choice(STATES)
        a = rng.choice(ACTIONS)
        if rng.random() < lambda_val:
            s_next = det_func[(s, a)]
        else:
            s_next = rng.choice(STATES)
        transitions.append((s, a, s_next))
    return transitions


# === BASELINES ===
def fit_rule_baseline(train):
    """Fit action-conditioned majority-vote rule."""
    pair_counts = defaultdict(Counter)
    for s, a, s_next in train:
        pair_counts[(s, a)][s_next] += 1
    rules = {}
    for pair, counter in pair_counts.items():
        rules[pair] = counter.most_common(1)[0][0]
    return rules


def predict_rule(rules, test, default_pred):
    """Predict using rule baseline. Unseen pairs use default_pred."""
    correct = 0
    for s, a, s_next in test:
        pred = rules.get((s, a), default_pred)
        if pred == s_next:
            correct += 1
    return correct / len(test)


def fit_memory_baseline(train):
    """Fit action-independent majority-vote memory."""
    state_counts = defaultdict(Counter)
    for s, a, s_next in train:
        state_counts[s][s_next] += 1
    memory = {}
    for s, counter in state_counts.items():
        memory[s] = counter.most_common(1)[0][0]
    return memory


def predict_memory(memory, test, default_pred):
    """Predict using memory baseline. Unseen states use default_pred."""
    correct = 0
    for s, a, s_next in test:
        pred = memory.get(s, default_pred)
        if pred == s_next:
            correct += 1
    return correct / len(test)


def predict_frequency(train, test):
    """Predict using marginal next-state distribution (frequency baseline)."""
    next_states = [s_next for _, _, s_next in train]
    if not next_states:
        return 0.0
    most_common = Counter(next_states).most_common(1)[0][0]
    correct = sum(1 for _, _, s_next in test if s_next == most_common)
    return correct / len(test)


def make_shuffled_train(train, rng):
    """Permute action labels across transitions."""
    actions = [a for _, a, _ in train]
    shuffled_actions = list(actions)
    rng.shuffle(shuffled_actions)
    return [(s, a_new, s_next) for (s, _, s_next), a_new in zip(train, shuffled_actions)]


# === MAIN EXPERIMENT ===
def run_experiment():
    """Execute the full frozen experiment."""
    print("=== EXP-FRONTIER-33528827909: Regime-Dependent Action-Conditioned Prediction ===")
    print(f"Seed: {SEED}")
    print(f"Lambda levels: {LAMBDA_LEVELS}")
    print(f"Functions: 3 (seeds {FUNCTION_SEEDS})")
    print(f"Transitions per level: {N_TRANSITIONS}")
    print()

    results = {
        "experiment_id": "EXP-FRONTIER-33528827909",
        "frozen_seed": SEED,
        "lambda_levels": LAMBDA_LEVELS,
        "function_seeds": FUNCTION_SEEDS,
        "n_transitions_per_level": N_TRANSITIONS,
        "per_function_results": {},
        "aggregate_results": {},
        "statistical_tests": {},
        "controls": {},
        "verdict": None,
        "raw_data": {}
    }

    all_rule_acc = {}
    all_memory_acc = {}
    all_shuffle_acc = {}
    all_freq_acc = {}

    for func_idx, func_seed in enumerate(FUNCTION_SEEDS):
        print(f"--- Function {func_idx+1} (seed={func_seed}) ---")
        det_func = make_deterministic_function(func_seed)
        func_results = {}

        for lam in LAMBDA_LEVELS:
            print(f"  lambda={lam}: ", end="")

            func_rng = np.random.RandomState(func_seed * 1000 + int(lam * 1000) + SEED)
            transitions = generate_transitions(det_func, lam, N_TRANSITIONS, func_rng)

            n_train = int(N_TRANSITIONS * TRAIN_FRACTION)
            indices = np.arange(N_TRANSITIONS)
            func_rng.shuffle(indices)
            train_idx = indices[:n_train]
            test_idx = indices[n_train:]

            train = [transitions[i] for i in train_idx]
            test = [transitions[i] for i in test_idx]

            train_next_states = [s_next for _, _, s_next in train]
            default_pred = Counter(train_next_states).most_common(1)[0][0] if train_next_states else 0

            rules = fit_rule_baseline(train)
            rule_acc = predict_rule(rules, test, default_pred)

            memory = fit_memory_baseline(train)
            memory_acc = predict_memory(memory, test, default_pred)

            shuffle_rng = np.random.RandomState(func_seed * 2000 + int(lam * 1000) + SEED)
            shuffled_train = make_shuffled_train(train, shuffle_rng)
            # Shuffle baseline: rules trained on shuffled data predict test
            shuffled_rules = fit_rule_baseline(shuffled_train)
            shuffled_default = Counter([s_next for _, _, s_next in shuffled_train]).most_common(1)[0][0]
            shuffle_acc = predict_rule(shuffled_rules, test, shuffled_default)

            freq_acc = predict_frequency(train, test)

            rule_mem_diff = rule_acc - memory_acc
            func_results[str(lam)] = {
                "rule_accuracy": round(rule_acc, 4),
                "memory_accuracy": round(memory_acc, 4),
                "shuffle_accuracy": round(shuffle_acc, 4),
                "frequency_accuracy": round(freq_acc, 4),
                "rule_memory_diff": round(rule_mem_diff, 4),
                "n_train": len(train),
                "n_test": len(test)
            }

            all_rule_acc.setdefault(lam, []).append(rule_acc)
            all_memory_acc.setdefault(lam, []).append(memory_acc)
            all_shuffle_acc.setdefault(lam, []).append(shuffle_acc)
            all_freq_acc.setdefault(lam, []).append(freq_acc)

            print(f"rule={rule_acc:.3f}, mem={memory_acc:.3f}, diff={rule_mem_diff:.4f}")

        results["per_function_results"][f"function_{func_idx+1}_seed{func_seed}"] = func_results
        print()

    # === AGGREGATE ANALYSIS ===
    print("=== Aggregate Analysis ===")
    agg_results = {}
    for lam in LAMBDA_LEVELS:
        rule_accs = all_rule_acc[lam]
        mem_accs = all_memory_acc[lam]
        shuffle_accs = all_shuffle_acc[lam]
        freq_accs = all_freq_acc[lam]
        diffs = [r - m for r, m in zip(rule_accs, mem_accs)]

        agg_results[str(lam)] = {
            "rule_accuracy_mean": round(float(np.mean(rule_accs)), 4),
            "rule_accuracy_std": round(float(np.std(rule_accs, ddof=0)), 4),
            "memory_accuracy_mean": round(float(np.mean(mem_accs)), 4),
            "memory_accuracy_std": round(float(np.std(mem_accs, ddof=0)), 4),
            "shuffle_accuracy_mean": round(float(np.mean(shuffle_accs)), 4),
            "frequency_accuracy_mean": round(float(np.mean(freq_accs)), 4),
            "rule_memory_diff_mean": round(float(np.mean(diffs)), 4),
            "rule_memory_diff_std": round(float(np.std(diffs, ddof=0)), 4),
            "rule_memory_diffs_per_function": [round(d, 4) for d in diffs]
        }
        print(f"lambda={lam}: rule={np.mean(rule_accs):.3f}+/-{np.std(rule_accs):.3f}, "
              f"mem={np.mean(mem_accs):.3f}+/-{np.std(mem_accs):.3f}, "
              f"diff={np.mean(diffs):.4f}+/-{np.std(diffs):.4f}")

    results["aggregate_results"] = agg_results

    # === STATISTICAL TESTS ===
    print("\n=== Statistical Tests ===")

    # 1. Spearman correlation: rule_memory_diff vs lambda
    lambda_vals = np.array(LAMBDA_LEVELS)
    diff_means = np.array([float(np.mean(np.array(all_rule_acc[l]) - np.array(all_memory_acc[l]))) for l in LAMBDA_LEVELS])
    spearman_rho, spearman_p = stats.spearmanr(lambda_vals, diff_means)

    # Per-function Spearman correlations
    per_func_spearman = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        func_diffs = [float(all_rule_acc[l][f_idx] - all_memory_acc[l][f_idx]) for l in LAMBDA_LEVELS]
        rho_f, p_f = stats.spearmanr(lambda_vals, func_diffs)
        per_func_spearman.append({"function": f_idx+1, "rho": round(float(rho_f), 4), "p_value": round(float(p_f), 4)})

    # Bonferroni correction across per-function comparisons
    n_spearman_comparisons = len(FUNCTION_SEEDS)
    bonferroni_spearman_p = min(spearman_p * n_spearman_comparisons, 1.0)

    spearman_results = {
        "aggregate_rho": round(float(spearman_rho), 4),
        "aggregate_p_value": round(float(spearman_p), 6),
        "bonferroni_corrected_p": round(float(bonferroni_spearman_p), 6),
        "per_function": per_func_spearman,
        "n_comparisons": n_spearman_comparisons
    }
    results["statistical_tests"]["spearman_correlation"] = spearman_results
    print(f"Spearman rho(rule_mem_diff, lambda): {spearman_rho:.4f}, p={spearman_p:.6f}, "
          f"Bonferroni p={bonferroni_spearman_p:.6f}")

    # 2. Paired t-tests at each lambda level (rule vs memory)
    paired_t_results = {}
    for lam in LAMBDA_LEVELS:
        rule_accs = np.array(all_rule_acc[lam])
        mem_accs = np.array(all_memory_acc[lam])
        t_stat, p_val = stats.ttest_rel(rule_accs, mem_accs)
        diff_std = np.std(rule_accs - mem_accs, ddof=1)
        cohens_d = float(np.mean(rule_accs - mem_accs) / diff_std) if diff_std > 0 else 0.0

        paired_t_results[str(lam)] = {
            "t_statistic": round(float(t_stat), 4),
            "p_value": round(float(p_val), 6),
            "cohens_d": round(cohens_d, 4),
            "rule_mean": round(float(np.mean(rule_accs)), 4),
            "memory_mean": round(float(np.mean(mem_accs)), 4),
            "diff_mean": round(float(np.mean(rule_accs - mem_accs)), 4)
        }
        print(f"Paired t-test lambda={lam}: t={t_stat:.3f}, p={p_val:.4f}, d={cohens_d:.3f}")

    results["statistical_tests"]["paired_t_tests"] = paired_t_results

    # 3. Two-way ANOVA: rule_memory_diff ~ lambda + function
    # NOTE: With 3 functions x 4 lambda levels = 12 observations,
    # a full two-way ANOVA with interaction has 0 residual df (saturated model).
    # We report the design limitation and use the main-effects-only model.
    anova_data = []
    for f_idx in range(len(FUNCTION_SEEDS)):
        for lam_idx, lam in enumerate(LAMBDA_LEVELS):
            diff = float(all_rule_acc[lam][f_idx] - all_memory_acc[lam][f_idx])
            anova_data.append({"lam_level": lam, "function": f_idx+1, "diff": diff})

    anova_results = {"design_note": "3 functions x 4 lambda levels = 12 cells with 1 obs/cell. "
                      "Full interaction model is saturated (0 residual df). "
                      "Reporting main-effects-only model."}

    try:
        import pandas as pd
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm

        df = pd.DataFrame(anova_data)
        df['lam_level'] = df['lam_level'].astype(str)
        df['function'] = df['function'].astype(str)

        # Main-effects-only model (no interaction)
        model = ols('diff ~ C(lam_level) + C(function)', data=df).fit()
        anova_table = anova_lm(model, typ=2)

        anova_results["main_effects_model"] = {
            "lambda_effect": {
                "F": round(float(anova_table.loc['C(lam_level)', 'F']), 4),
                "p_value": round(float(anova_table.loc['C(lam_level)', 'PR(>F)']), 6),
                "df": int(anova_table.loc['C(lam_level)', 'df'])
            },
            "function_effect": {
                "F": round(float(anova_table.loc['C(function)', 'F']), 4),
                "p_value": round(float(anova_table.loc['C(function)', 'PR(>F)']), 6),
                "df": int(anova_table.loc['C(function)', 'df'])
            },
            "residual_df": int(anova_table.loc['Residual', 'df']),
            "model_r_squared": round(float(model.rsquared), 4)
        }
        print(f"\nTwo-way ANOVA (main effects only):")
        print(f"  Lambda effect: F={anova_results['main_effects_model']['lambda_effect']['F']}, "
              f"p={anova_results['main_effects_model']['lambda_effect']['p_value']}")
        print(f"  Function effect: F={anova_results['main_effects_model']['function_effect']['F']}, "
              f"p={anova_results['main_effects_model']['function_effect']['p_value']}")
        print(f"  Residual df: {anova_results['main_effects_model']['residual_df']}")
    except Exception as e:
        anova_results["error"] = str(e)
        print(f"\nANOVA failed: {e}")

    # 4. Function invariance: coefficient of variation across functions at each lambda level
    cv_results = {}
    for lam in LAMBDA_LEVELS:
        diffs = np.array([all_rule_acc[lam][i] - all_memory_acc[lam][i] for i in range(len(FUNCTION_SEEDS))])
        mean_diff = float(np.mean(diffs))
        std_diff = float(np.std(diffs, ddof=0))
        cv = std_diff / mean_diff if mean_diff > 0 else float('inf')
        cv_results[str(lam)] = {
            "diffs_per_function": [round(d, 4) for d in diffs],
            "mean": round(mean_diff, 4),
            "std": round(std_diff, 4),
            "cv": round(cv, 4)
        }
    print(f"\nCoefficient of Variation across functions:")
    for lam_str, cv_data in cv_results.items():
        print(f"  lambda={lam_str}: CV={cv_data['cv']:.3f} (diffs: {cv_data['diffs_per_function']})")

    anova_results["coefficient_of_variation"] = cv_results
    results["statistical_tests"]["two_way_anova"] = anova_results

    # === CONTROL CHECKS ===
    print("\n=== Control Checks ===")
    controls = {}

    # Positive control: rules > 90% at lambda=1
    lambda_1_rules = all_rule_acc[1.0]
    positive_control_pass = bool(all(r > 0.90 for r in lambda_1_rules))
    controls["positive_control"] = {
        "description": "Rules >90% accuracy at lambda=1 across all functions",
        "rule_accuracies_lambda1": [round(r, 4) for r in lambda_1_rules],
        "pass": positive_control_pass,
        "threshold": 0.90
    }
    print(f"Positive control (lambda=1, rules >90%): {'PASS' if positive_control_pass else 'FAIL'}")
    print(f"  Accuracies: {[f'{r:.3f}' for r in lambda_1_rules]}")

    # Null control: rules not > memory at lambda=0
    lambda_0_diffs = [float(all_rule_acc[0.0][i] - all_memory_acc[0.0][i]) for i in range(len(FUNCTION_SEEDS))]
    lambda_0_t, lambda_0_p = stats.ttest_rel(all_rule_acc[0.0], all_memory_acc[0.0])
    null_control_pass = bool(lambda_0_p > 0.05)
    controls["null_control"] = {
        "description": "Rules not significantly outperform memory at lambda=0",
        "diffs_lambda0": [round(d, 4) for d in lambda_0_diffs],
        "paired_t_p_value": round(float(lambda_0_p), 6),
        "pass": null_control_pass,
        "threshold_alpha": 0.05
    }
    print(f"Null control (lambda=0, rules <= memory): {'PASS' if null_control_pass else 'FAIL'}")
    print(f"  Diffs: {[f'{d:.4f}' for d in lambda_0_diffs]}, p={lambda_0_p:.4f}")

    # Sensitivity control: monotonic rule-memory difference
    diff_means_list = [float(np.mean(np.array(all_rule_acc[l]) - np.array(all_memory_acc[l]))) for l in LAMBDA_LEVELS]
    monotonic_increasing = bool(all(
        diff_means_list[i] <= diff_means_list[i+1]
        for i in range(len(LAMBDA_LEVELS) - 1)
    ))
    controls["sensitivity_control"] = {
        "description": "Rule-memory difference is monotonically increasing",
        "pass": monotonic_increasing,
        "diff_means_by_lambda": [round(d, 4) for d in diff_means_list]
    }
    print(f"Sensitivity control (monotonic increase): {'PASS' if monotonic_increasing else 'FAIL'}")

    # Function invariance: CV < 0.3 at each level AND monotonic ordering preserved across all functions
    cv_all_under_threshold = all(cv_results[str(lam)]["cv"] < 0.3 for lam in LAMBDA_LEVELS)
    # Check if ALL functions show monotonic ordering
    all_funcs_monotonic = True
    for f_idx in range(len(FUNCTION_SEEDS)):
        func_diffs = [float(all_rule_acc[l][f_idx] - all_memory_acc[l][f_idx]) for l in LAMBDA_LEVELS]
        func_mono = all(func_diffs[i] <= func_diffs[i+1] for i in range(len(func_diffs) - 1))
        if not func_mono:
            all_funcs_monotonic = False
            break

    function_invariance_pass = bool(cv_all_under_threshold and all_funcs_monotonic)
    controls["function_invariance"] = {
        "description": "CV<0.3 at each lambda level AND monotonic ordering preserved across all functions",
        "cv_all_under_0.3": bool(cv_all_under_threshold),
        "all_functions_monotonic": bool(all_funcs_monotonic),
        "pass": function_invariance_pass,
        "threshold_cv": 0.3,
        "note": "Two-way ANOVA interaction term could not be estimated (0 residual df). "
                "Using CV + monotonic ordering as alternative validity check."
    }
    print(f"Function invariance (CV<0.3 & all monotonic): {'PASS' if function_invariance_pass else 'FAIL'}")

    results["controls"] = controls

    # === VERDICT ===
    print("\n=== Verdict ===")

    monotonicity_pass = bool(spearman_rho >= 0.7 and bonferroni_spearman_p < 0.05)

    conditions = {
        "monotonicity_spearman": {
            "rho": round(float(spearman_rho), 4),
            "threshold": 0.7,
            "bonferroni_p": round(float(bonferroni_spearman_p), 6),
            "pass": monotonicity_pass
        },
        "positive_control": {"pass": positive_control_pass},
        "null_control": {"pass": null_control_pass},
        "function_invariance": {"pass": function_invariance_pass}
    }

    all_pass = bool(all(c["pass"] for c in conditions.values()))

    if all_pass:
        verdict = "SURVIVES_CURRENT_TEST"
    else:
        failed = [k for k, v in conditions.items() if not v["pass"]]
        verdict = "FALSIFIED-IN-SETTING"

    results["verdict"] = {
        "decision": verdict,
        "conditions": conditions,
        "claim": "C-WEB-DYNAMICS",
        "falsification_summary": None if all_pass else f"Failed: {', '.join(failed)}"
    }

    print(f"Verdict: {verdict}")
    if not all_pass:
        failed = [k for k, v in conditions.items() if not v["pass"]]
        print(f"Failed conditions: {failed}")
    else:
        print("All conditions met.")

    # === SAVE RAW DATA ===
    results["raw_data"] = {
        "all_rule_accuracies": {str(l): [round(r, 4) for r in all_rule_acc[l]] for l in LAMBDA_LEVELS},
        "all_memory_accuracies": {str(l): [round(r, 4) for r in all_memory_acc[l]] for l in LAMBDA_LEVELS},
        "all_shuffle_accuracies": {str(l): [round(r, 4) for r in all_shuffle_acc[l]] for l in LAMBDA_LEVELS},
        "all_frequency_accuracies": {str(l): [round(r, 4) for r in all_freq_acc[l]] for l in LAMBDA_LEVELS}
    }

    return results


if __name__ == "__main__":
    results = run_experiment()

    # Write result.json
    result_path = Path(__file__).parent / "result.json"
    with open(result_path, 'w') as f:
        json.dump(to_native(results), f, indent=2)
    print(f"\nWrote {result_path}")

    # Compute hashes for provenance
    files_to_hash = ["prereg.md", "spec.json", "request.json", "analyze.py"]
    hashes = {}
    for fname in files_to_hash:
        fpath = Path(__file__).parent / fname
        if fpath.exists():
            h = hashlib.sha256(fpath.read_bytes()).hexdigest()
            hashes[fname] = h

    provenance = {
        "experiment_id": "EXP-FRONTIER-33528827909",
        "execution_timestamp": None,
        "analyzer_script": "analyze.py",
        "script_hashes": hashes,
        "result_hash": hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "verdict": results["verdict"]["decision"],
        "claim": "C-WEB-DYNAMICS",
        "lane": "frontier",
        "environment": {
            "python_version": "3.12.14",
            "numpy_version": np.__version__,
            "scipy_version": stats.__version__ if hasattr(stats, '__version__') else "unknown"
        }
    }
    provenance_path = Path(__file__).parent / "provenance.json"
    with open(provenance_path, 'w') as f:
        json.dump(to_native(provenance), f, indent=2)
    print(f"Wrote {provenance_path}")
