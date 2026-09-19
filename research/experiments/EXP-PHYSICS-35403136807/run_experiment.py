#!/usr/bin/env python3
"""EXP-PHYSICS-35403136807 - Signal Decomposition: Markov vs Beyond-Markov"""
import hashlib, json, math, random, collections, sys, time
from pathlib import Path
import numpy as np

EXPERIMENT_ID = "EXP-PHYSICS-35403136807"
SEED = 42
N_SHUFFLE = 1000
MIN_STRATUM_SIZE = 5
START_TOKEN = "<START>"
N_BOOTSTRAP = 200

# 12-state hash-routed SPA (identical to parent)
STATES = {
    0: "http://localhost:18973/#home",
    1: "http://localhost:18973/app#dashboard",
    2: "http://localhost:18973/app#analytics",
    3: "http://localhost:18973/user#profile",
    4: "http://localhost:18973/user#settings",
    5: "http://localhost:18973/app#search",
    6: "http://localhost:18973/app#notifications",
    7: "http://localhost:18973/admin#users",
    8: "http://localhost:18973/admin#reports",
    9: "http://localhost:18973/docs#getting-started",
    10: "http://localhost:18973/docs#api-ref",
    11: "http://localhost:18973/docs#changelog",
}
ACTIONS = ["form_submit", "button_click", "js_navigate", "menu_select"]
CANDIDATES = {
    0: {"form_submit": [1,5,3,9], "button_click": [2,6,4,10], "js_navigate": [3,7,5,11], "menu_select": [4,8,1,6]},
    1: {"form_submit": [2,5,7,3], "button_click": [4,0,8,10], "js_navigate": [6,3,9,1], "menu_select": [5,7,11,4]},
    2: {"form_submit": [1,6,0,8], "button_click": [3,5,9,4], "js_navigate": [7,1,10,2], "menu_select": [0,8,3,11]},
    3: {"form_submit": [4,0,6,10], "button_click": [1,7,5,11], "js_navigate": [2,8,0,9], "menu_select": [5,9,4,1]},
    4: {"form_submit": [3,1,8,0], "button_click": [6,2,7,11], "js_navigate": [5,0,3,10], "menu_select": [7,10,6,2]},
    5: {"form_submit": [0,3,11,6], "button_click": [1,4,8,2], "js_navigate": [9,6,0,7], "menu_select": [10,2,5,3]},
    6: {"form_submit": [2,8,0,4], "button_click": [3,9,7,1], "js_navigate": [4,10,1,5], "menu_select": [1,11,3,8]},
    7: {"form_submit": [8,1,3,5], "button_click": [9,0,6,2], "js_navigate": [10,4,0,8], "menu_select": [11,5,7,1]},
    8: {"form_submit": [7,2,0,6], "button_click": [10,3,1,9], "js_navigate": [11,5,4,0], "menu_select": [9,0,8,3]},
    9: {"form_submit": [10,0,2,7], "button_click": [11,1,5,3], "js_navigate": [0,4,8,6], "menu_select": [1,6,10,4]},
    10: {"form_submit": [11,4,1,9], "button_click": [0,5,3,8], "js_navigate": [1,6,7,2], "menu_select": [3,7,11,5]},
    11: {"form_submit": [9,3,5,1], "button_click": [10,2,6,0], "js_navigate": [0,7,4,8], "menu_select": [2,8,10,3]},
}

def choose_next(current, action, prev1, prev2):
    candidates = CANDIDATES[current][action]
    h = hashlib.sha256(f"{prev1}:{prev2}:{current}:{action}".encode()).hexdigest()
    idx = int(h[:8],16) % len(candidates)
    return candidates[idx]

def simulate_session(session_id, n_steps, rng):
    current = rng.choice(range(12))
    prev1, prev2 = current, current
    transitions = []
    for step in range(n_steps):
        action = rng.choice(ACTIONS)
        next_state = choose_next(current, action, prev1, prev2)
        transitions.append({
            "session": f"session_{session_id}",
            "step": step,
            "url_before": STATES[current],
            "url_after": STATES[next_state],
            "action_primitive": action,
            "error": None,
        })
        prev2, prev1 = prev1, current
        current = next_state
    return transitions

def collect_transitions(n_sessions=50, steps_per_session=100, seed=SEED):
    rng = random.Random(seed)
    all_transitions = []
    for sid in range(n_sessions):
        trans = simulate_session(sid, steps_per_session, rng)
        all_transitions.extend(trans)
    return all_transitions

def build_state_history_records(transitions, K):
    sessions = collections.defaultdict(list)
    for t in transitions:
        sessions[t["session"]].append(t)
    records = []
    for sid, sess_trans in sessions.items():
        sess_trans = sorted(sess_trans, key=lambda x: x["step"])
        url_before_seq = [t["url_before"] for t in sess_trans]
        for i, t in enumerate(sess_trans):
            if K == 0:
                history = tuple()
            elif i == 0:
                history = tuple([START_TOKEN]*K)
            elif i < K:
                history = tuple([START_TOKEN]*(K-i) + url_before_seq[:i])
            else:
                history = tuple(url_before_seq[i-K:i])
            records.append({
                "session": sid, "step": i,
                "url_before": t["url_before"],
                "history": history,
                "action": t["action_primitive"],
                "url_after": t["url_after"],
            })
    return records

def build_action_history_records(transitions, K):
    sessions = collections.defaultdict(list)
    for t in transitions:
        sessions[t["session"]].append(t)
    records = []
    for sid, sess_trans in sessions.items():
        sess_trans = sorted(sess_trans, key=lambda x: x["step"])
        actions = [t["action_primitive"] for t in sess_trans]
        for i, t in enumerate(sess_trans):
            if K == 0:
                history = tuple()
            elif i == 0:
                history = tuple([START_TOKEN]*K)
            elif i < K:
                history = tuple([START_TOKEN]*(K-i) + actions[:i])
            else:
                history = tuple(actions[i-K:i])
            records.append({
                "session": sid, "step": i,
                "url_before": t["url_before"],
                "history": history,
                "action": t["action_primitive"],
                "url_after": t["url_after"],
            })
    return records

def compute_conditional_pmi(records, K):
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    total_records = len(records)
    if total_records == 0:
        return {"pmi":0.0,"n_strata":0,"n_used":0,"total":0,"skipped_small":0,"skipped_zero_var":0}
    pmi_weighted_sum = 0.0
    n_used = 0; skipped_small = 0; skipped_zero_var = 0
    for stratum, stratum_records in strata.items():
        n_h = len(stratum_records)
        weight = n_h / total_records
        if n_h < MIN_STRATUM_SIZE:
            skipped_small += 1
            continue
        action_counts = collections.Counter(r["action"] for r in stratum_records)
        next_counts = collections.Counter(r["url_after"] for r in stratum_records)
        joint_counts = collections.Counter((r["action"], r["url_after"]) for r in stratum_records)
        distinct_nexts = len(next_counts)
        if distinct_nexts <= 1:
            skipped_zero_var += 1
            pmi_weighted_sum += weight * 0.0
            n_used += 1
            continue
        pmi_values = []
        for r in stratum_records:
            a = r["action"]
            s_next = r["url_after"]
            p_a = action_counts[a] / n_h
            p_s = next_counts[s_next] / n_h
            p_joint = joint_counts[(a,s_next)] / n_h
            denom = p_a * p_s
            if denom>0 and p_joint>0:
                pmi = math.log2(p_joint/denom)
            else:
                pmi = 0.0
            pmi_values.append(pmi)
        stratum_pmi = sum(pmi_values)/len(pmi_values)
        pmi_weighted_sum += weight * stratum_pmi
        n_used += 1
    return {"pmi": pmi_weighted_sum, "n_strata": len(strata), "n_used": n_used,
            "total": total_records, "skipped_small": skipped_small, "skipped_zero_var": skipped_zero_var}

def compute_prediction_accuracy(records, K):
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    correct = 0; total = 0
    for stratum, recs in strata.items():
        if len(recs) < MIN_STRATUM_SIZE:
            continue
        next_counts = collections.Counter(r["url_after"] for r in recs)
        majority_cnt = next_counts.most_common(1)[0][1]
        correct += majority_cnt
        total += len(recs)
    return correct/total if total>0 else 0.0

def determinism_check(records, K):
    strata = collections.defaultdict(list)
    for r in records:
        strata[(r["url_before"], r["history"])].append(r)
    deterministic = 0; stochastic = 0
    for stratum, recs in strata.items():
        next_counts = collections.Counter(r["url_after"] for r in recs)
        if len(next_counts) == 1:
            deterministic += 1
        elif len(next_counts) > 1:
            stochastic += 1
    total = deterministic+stochastic
    return {"deterministic": deterministic, "stochastic": stochastic, "total": total,
            "stoch_ratio": stochastic/total if total else 0, "det_ratio": deterministic/total if total else 0}

def permutation_test_within_stratum(records, K, n_permutations=1000, seed=42):
    strata = collections.defaultdict(list)
    for r in records:
        stratum = (r["url_before"], r["history"])
        strata[stratum].append(r)
    observed = compute_conditional_pmi(records, K)
    observed_pmi = observed["pmi"]
    rng = random.Random(seed)
    shuffled_pmis = []
    for _ in range(n_permutations):
        perm_rng = random.Random(rng.randint(0, 2**32))
        shuffled_records = []
        for stratum, stratum_records in strata.items():
            url_afters = [r["url_after"] for r in stratum_records]
            perm_rng.shuffle(url_afters)
            for i, r in enumerate(stratum_records):
                shuffled_records.append({
                    "session": r["session"], "step": r["step"],
                    "url_before": r["url_before"], "history": r["history"],
                    "action": r["action"], "url_after": url_afters[i],
                })
        stats = compute_conditional_pmi(shuffled_records, K)
        shuffled_pmis.append(stats["pmi"])
    shuffled_pmis = np.array(shuffled_pmis)
    count_ge = np.sum(shuffled_pmis >= observed_pmi)
    p_value = (count_ge + 1) / (n_permutations + 1)
    null_mean = float(np.mean(shuffled_pmis))
    null_std = float(np.std(shuffled_pmis, ddof=0))
    effect_d = float((observed_pmi - null_mean)/null_std) if null_std>0 else 0.0
    return {"observed_pmi": observed_pmi, "p_value": p_value, "null_mean": null_mean,
            "null_std": null_std, "effect_size_d": effect_d, "shuffled_pmis": shuffled_pmis.tolist()[:5],
            "observed_stats": observed}

def bootstrap_k3_minus_k2(transitions, n_bootstrap=N_BOOTSTRAP, seed=SEED):
    rng = random.Random(seed)
    sessions = collections.defaultdict(list)
    for t in transitions:
        sessions[t["session"]].append(t)
    session_ids = list(sessions.keys())
    n_sessions = len(session_ids)
    differences = []; k3_values = []; k2_values = []
    for b in range(n_bootstrap):
        boot_session_ids = [session_ids[rng.randint(0, n_sessions - 1)] for _ in range(n_sessions)]
        boot_transitions = []
        for sid in boot_session_ids:
            boot_transitions.extend(sessions[sid])
        recs_state_K2 = build_state_history_records(boot_transitions, 2)
        recs_action_K3 = build_action_history_records(boot_transitions, 3)
        pmi_k2 = compute_conditional_pmi(recs_state_K2, 2)
        pmi_k3 = compute_conditional_pmi(recs_action_K3, 3)
        diff = pmi_k3["pmi"] - pmi_k2["pmi"]
        differences.append(diff)
        k3_values.append(pmi_k3["pmi"])
        k2_values.append(pmi_k2["pmi"])
    differences = np.array(differences)
    k3_values = np.array(k3_values)
    k2_values = np.array(k2_values)
    ci_lower = float(np.percentile(differences, 2.5))
    ci_upper = float(np.percentile(differences, 97.5))
    mean_diff = float(np.mean(differences))
    std_diff = float(np.std(differences, ddof=0))
    return {
        "mean_difference": mean_diff, "ci_lower_95": ci_lower, "ci_upper_95": ci_upper,
        "std_difference": std_diff, "mean_k3": float(np.mean(k3_values)),
        "mean_k2": float(np.mean(k2_values)), "n_bootstrap": n_bootstrap,
        "differences_sample": differences[:10].tolist(),
    }

def shuffled_action_null(records, K, n_shuffle=N_SHUFFLE, seed=42):
    observed = compute_conditional_pmi(records, K)
    observed_pmi = observed["pmi"]
    rng = random.Random(seed)
    shuffled_pmis = []
    all_actions = [r["action"] for r in records]
    for _ in range(n_shuffle):
        perm_rng = random.Random(rng.randint(0, 2**32))
        shuffled_actions = all_actions[:]
        perm_rng.shuffle(shuffled_actions)
        shuffled_records = []
        for i, r in enumerate(records):
            shuffled_records.append({
                "session": r["session"], "step": r["step"],
                "url_before": r["url_before"], "history": r["history"],
                "action": shuffled_actions[i], "url_after": r["url_after"],
            })
        stats = compute_conditional_pmi(shuffled_records, K)
        shuffled_pmis.append(stats["pmi"])
    shuffled_pmis = np.array(shuffled_pmis)
    count_ge = np.sum(shuffled_pmis >= observed_pmi)
    p_value = (count_ge + 1) / (n_shuffle + 1)
    null_mean = float(np.mean(shuffled_pmis))
    null_std = float(np.std(shuffled_pmis, ddof=0))
    effect_d = float((observed_pmi - null_mean)/null_std) if null_std>0 else 0.0
    return {"observed_pmi": observed_pmi, "p_value": p_value, "null_mean": null_mean,
            "null_std": null_std, "effect_size_d": effect_d,
            "shuffled_pmis": shuffled_pmis.tolist()[:5]}

def run_positive_control(n_transitions=5000, seed=SEED):
    rng = random.Random(seed)
    positive_states = {
        0: "http://spa.test/home", 1: "http://spa.test/dashboard",
        2: "http://spa.test/profile", 3: "http://spa.test/settings",
        4: "http://spa.test/search", 5: "http://spa.test/notifications",
        6: "http://spa.test/admin", 7: "http://spa.test/help",
    }
    positive_transitions = {
        0: {"form_submit":1,"button_click":2,"js_navigate":3,"menu_select":4},
        1: {"form_submit":4,"button_click":5,"js_navigate":0,"menu_select":6},
        2: {"form_submit":3,"button_click":6,"js_navigate":1,"menu_select":7},
        3: {"form_submit":0,"button_click":7,"js_navigate":2,"menu_select":4},
        4: {"form_submit":5,"button_click":0,"js_navigate":6,"menu_select":7},
        5: {"form_submit":6,"button_click":1,"js_navigate":7,"menu_select":4},
        6: {"form_submit":7,"button_click":2,"js_navigate":4,"menu_select":5},
        7: {"form_submit":0,"button_click":3,"js_navigate":5,"menu_select":6},
    }
    transitions = []
    n_sessions = 50; steps_per_session = 100
    for sid in range(n_sessions):
        current = rng.choice(range(8))
        for step in range(steps_per_session):
            action = rng.choice(ACTIONS)
            next_state = positive_transitions[current][action]
            transitions.append({
                "session": f"pc_session_{sid}", "step": step,
                "url_before": positive_states[current],
                "url_after": positive_states[next_state],
                "action_primitive": action,
            })
            current = next_state
    recs_action_K3 = build_action_history_records(transitions, 3)
    pmi_action = compute_conditional_pmi(recs_action_K3, 3)
    perm_action = permutation_test_within_stratum(recs_action_K3, 3, 1000, SEED)
    return {
        "n_transitions": len(transitions),
        "pmi_action_K3": pmi_action["pmi"],
        "observed_p_action": perm_action["p_value"],
        "effect_d_action": perm_action["effect_size_d"],
        "passes": (pmi_action["pmi"] >= 1.0 and perm_action["p_value"] < 0.001),
    }

def main():
    print("="*70)
    print(f"EXPERIMENT {EXPERIMENT_ID}")
    print("Signal Decomposition: Markov vs Beyond-Markov")
    print("="*70)
    out_dir = Path("research/experiments") / EXPERIMENT_ID
    out_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: Collect 12-state SPA data N=5000
    print("\n[COLLECT] Simulating 12-state SPA 50x100=5000 transitions...")
    transitions = collect_transitions(n_sessions=50, steps_per_session=100, seed=SEED)
    print(f"  Total: {len(transitions)}")
    n_sessions = len(set(t["session"] for t in transitions))
    print(f"  Sessions: {n_sessions}")
    sha_raw = hashlib.sha256(json.dumps(transitions, sort_keys=True).encode()).hexdigest()
    print(f"  SHA256: {sha_raw[:16]}...")

    raw_path = out_dir / "raw_transitions.json"
    with open(raw_path, "w") as f:
        json.dump(transitions, f, indent=2)

    # Build records
    print("\n[BUILD] Building records...")
    recs_K0 = build_state_history_records(transitions, 0)
    recs_K1 = build_state_history_records(transitions, 1)
    recs_K2 = build_state_history_records(transitions, 2)
    recs_action_K3 = build_action_history_records(transitions, 3)

    # Compute PMIs
    print("\n[ANALYSIS] Computing PMIs...")
    results = {}
    for label, recs, K in [("K0_unconditional", recs_K0, 0), ("K1_state1", recs_K1, 1),
                            ("K2_state2", recs_K2, 2), ("K3_action3", recs_action_K3, 3)]:
        pmi_stats = compute_conditional_pmi(recs, K)
        acc = compute_prediction_accuracy(recs, K)
        det = determinism_check(recs, K) if K > 0 else {"deterministic":0,"stochastic":0,"total":0}
        results[label] = {
            "pmi_bits": pmi_stats["pmi"], "n_strata_total": pmi_stats["n_strata"],
            "n_strata_used": pmi_stats["n_used"], "n_total_records": pmi_stats["total"],
            "skipped_small": pmi_stats["skipped_small"],
            "skipped_zero_var": pmi_stats["skipped_zero_var"],
            "prediction_accuracy": acc, "determinism": det,
        }
        print(f"  {label} K={K}: PMI={pmi_stats['pmi']:.6f} used={pmi_stats['n_used']}/{pmi_stats['n_strata']} acc={acc:.4f}")

    k1_pmi = results["K1_state1"]["pmi_bits"]
    k2_pmi = results["K2_state2"]["pmi_bits"]
    k3_pmi = results["K3_action3"]["pmi_bits"]
    k3_minus_k2 = k3_pmi - k2_pmi
    k2_minus_k1 = k2_pmi - k1_pmi
    print(f"\n  K1 PMI: {k1_pmi:.6f}")
    print(f"  K2 PMI: {k2_pmi:.6f}")
    print(f"  K3 PMI: {k3_pmi:.6f}")
    print(f"  K3 - K2: {k3_minus_k2:.6f} bits")
    print(f"  K2 - K1: {k2_minus_k1:.6f} bits")

    # Bootstrap CI for K3 - K2
    print("\n" + "="*70)
    print("[BOOTSTRAP] 200 trajectory-block resamples for K3 - K2 CI")
    print("="*70)
    t0 = time.time()
    bc = bootstrap_k3_minus_k2(transitions, N_BOOTSTRAP, SEED)
    bt = time.time() - t0
    print(f"  Mean difference: {bc['mean_difference']:.6f} bits")
    print(f"  95% CI: [{bc['ci_lower_95']:.6f}, {bc['ci_upper_95']:.6f}]")
    print(f"  Std: {bc['std_difference']:.6f}")
    print(f"  Time: {bt:.1f}s")

    # Shuffled-action null for K2
    print("\n" + "="*70)
    print("[NULL CONTROL] Shuffled-action permutation N=1000 for K2")
    print("="*70)
    t0 = time.time()
    nc = shuffled_action_null(recs_K2, 2, N_SHUFFLE, SEED)
    nt = time.time() - t0
    print(f"  Observed K2 PMI: {nc['observed_pmi']:.6f}")
    print(f"  Null mean: {nc['null_mean']:.6f} std: {nc['null_std']:.6f}")
    print(f"  |null_mean|: {abs(nc['null_mean']):.6f}")
    print(f"  0.1 threshold: {'PASS' if abs(nc['null_mean']) < 0.1 else 'FAIL'}")
    print(f"  p-value: {nc['p_value']:.6f}")
    print(f"  Effect size d: {nc['effect_size_d']:.2f}")
    print(f"  Time: {nt:.1f}s")

    # Positive control
    print("\n" + "="*70)
    print("[CONTROL] Positive control 8-state deterministic N=5000")
    print("="*70)
    t0 = time.time()
    pc = run_positive_control(n_transitions=5000, seed=SEED)
    pt = time.time() - t0
    print(f"  K3 PMI: {pc['pmi_action_K3']:.6f}")
    print(f"  p-value: {pc['observed_p_action']:.6f}")
    print(f"  Effect size d: {pc['effect_d_action']:.2f}")
    print(f"  Passes (PMI>=1.0 & p<0.001): {pc['passes']}")
    print(f"  Time: {pt:.1f}s")

    # Exploratory: N=50000
    print("\n" + "="*70)
    print("[EXPLORATORY] K2 PMI at N=50000 (bias-scaling test)")
    print("="*70)
    t0 = time.time()
    trans_50k = collect_transitions(n_sessions=50, steps_per_session=1000, seed=SEED)
    recs_K2_50k = build_state_history_records(trans_50k, 2)
    pmi_K2_50k = compute_conditional_pmi(recs_K2_50k, 2)
    det_K2_50k = determinism_check(recs_K2_50k, 2)
    et = time.time() - t0
    print(f"  N={len(trans_50k)}")
    print(f"  K2 PMI: {pmi_K2_50k['pmi']:.6f}")
    print(f"  Used: {pmi_K2_50k['n_used']}/{pmi_K2_50k['n_strata']} strata")
    print(f"  Determinism: {det_K2_50k['det_ratio']:.3f}")
    print(f"  Time: {et:.1f}s")

    # DECISION RULE
    print("\n" + "="*70)
    print("DECISION RULE")
    print("="*70)
    c1_pass = k3_minus_k2 > 0.1 and bc["ci_lower_95"] > 0.0
    c2_pass = k2_pmi > k1_pmi + 0.05
    c3_pass = pc["passes"]
    c4_pass = abs(nc["null_mean"]) < 0.1

    print(f"C1: K3-K2={k3_minus_k2:.6f} > 0.1 = {k3_minus_k2 > 0.1}")
    print(f"  CI_lower={bc['ci_lower_95']:.6f} > 0 = {bc['ci_lower_95'] > 0.0}")
    print(f"  -> {'PASS' if c1_pass else 'FAIL'}")
    print(f"C2: K2={k2_pmi:.6f} > K1+0.05={k1_pmi+0.05:.6f} = {c2_pass}")
    print(f"  -> {'PASS' if c2_pass else 'FAIL'}")
    print(f"C3: Positive control K3={pc['pmi_action_K3']:.6f} >= 1.0 = {pc['pmi_action_K3'] >= 1.0}")
    print(f"  -> {'PASS' if c3_pass else 'FAIL'}")
    print(f"C4: Null control |mean|={abs(nc['null_mean']):.6f} < 0.1 = {c4_pass}")
    print(f"  -> {'PASS' if c4_pass else 'FAIL'}")

    if not c3_pass:
        decision = "MEASUREMENT_INVALID"; outcome = "NOT_APPLICABLE"
        reason = "Positive control K3 < 1.0 bit"
    elif not c4_pass:
        decision = "MEASUREMENT_INVALID"; outcome = "NOT_APPLICABLE"
        reason = "Null control |mean| >= 0.1 bits"
    elif c1_pass:
        decision = "SURVIVES_CURRENT_TEST"; outcome = "SUPPORTS"
        reason = f"K3-K2 = {k3_minus_k2:.6f} > 0.1 bits, CI [{bc['ci_lower_95']:.6f},{bc['ci_upper_95']:.6f}] excludes 0. Beyond-Markov structure demonstrated."
    else:
        decision = "FALSIFIED-IN-SETTING"; outcome = "FALSIFIES"
        reason = f"K3-K2 = {k3_minus_k2:.6f} <= 0.1 bits OR CI [{bc['ci_lower_95']:.6f},{bc['ci_upper_95']:.6f}] includes 0. Signal is primarily Markov."

    print(f"\nDECISION: {decision}")
    print(f"OUTCOME: {outcome}")
    print(f"REASON: {reason}")

    # Save results
    def to_json(o):
        if isinstance(o, (np.bool_, np.integer, np.floating)):
            return o.item()
        if isinstance(o, bool):
            return bool(o)
        if isinstance(o, tuple):
            return list(o)
        return o

    all_results = {
        "experiment_id": EXPERIMENT_ID,
        "n_transitions": int(len(transitions)),
        "n_sessions": int(n_sessions),
        "results": results,
        "k1_pmi": k1_pmi, "k2_pmi": k2_pmi, "k3_pmi": k3_pmi,
        "k3_minus_k2": k3_minus_k2, "k2_minus_k1": k2_minus_k1,
        "bootstrap": bc,
        "null_control": nc,
        "positive_control": pc,
        "exploratory_n50000": {
            "n": len(trans_50k),
            "k2_pmi": pmi_K2_50k["pmi"],
            "n_used": pmi_K2_50k["n_used"],
            "n_strata": pmi_K2_50k["n_strata"],
            "det_ratio": det_K2_50k["det_ratio"],
        },
        "decision": decision,
        "outcome": outcome,
        "reason": reason,
        "sha_raw": sha_raw,
    }

    with open(out_dir / "raw_results.json", "w") as f:
        json.dump(all_results, f, indent=2, default=to_json)

    print(f"\nSaved raw results to {out_dir / 'raw_results.json'}")
    return all_results

if __name__ == "__main__":
    main()
