#!/usr/bin/env python3
"""
EXP-PHYSICS-35137030850 — EXECUTE
Branching FSM with stochastic transitions, many-to-one vs unique content mapping.
Tests whether PMI persists when content does NOT uniquely determine state.
"""

import json
import hashlib
import numpy as np
from collections import defaultdict, Counter
from itertools import product
import os
import time

# ─── Configuration ───────────────────────────────────────────────────────────
SEED = 42
N_TRAJECTORIES = 200
STEPS_PER_TRAJECTORY = 10
N_SESSIONS = 20
N_STATES = 3
STATE_LABELS = ["S0", "S1", "S2"]
ACTIONS = ["advance", "branch"]
P_LEFT = 0.7  # P(next_state = intended) for left direction
P_RIGHT = 0.3  # P(next_state = intended) for right direction
N_PERMUTATIONS = 1000
K_VALUES = [1, 2, 3]
BONFERRONI_COMPARISONS = 4  # 2 conditions x 2 K values

# Content definitions
CONTENT_MANY_TO_ONE = {
    "S0": {
        "page_title": "Shared Content",
        "page_description": "Content shared between states",
        "content_items": ["Item A", "Item B", "Item C"],
        "status_text": "shared",
        "navigation": {"available_actions": ["advance", "branch"]}
    },
    "S1": {
        "page_title": "Shared Content",
        "page_description": "Content shared between states",
        "content_items": ["Item A", "Item B", "Item C"],
        "status_text": "shared",
        "navigation": {"available_actions": ["advance", "branch"]}
    },
    "S2": {
        "page_title": "Details",
        "page_description": "Item specifications and reviews",
        "content_items": ["Customer Reviews", "Technical Specs", "Related Items"],
        "status_text": "reviewing",
        "navigation": {"available_actions": ["advance", "branch"]}
    }
}

CONTENT_UNIQUE = {
    "S0": {
        "page_title": "Home",
        "page_description": "Welcome to the application",
        "content_items": ["Featured Products", "Popular Categories", "New Arrivals"],
        "status_text": "browsing",
        "navigation": {"available_actions": ["advance", "branch"]}
    },
    "S1": {
        "page_title": "Browse",
        "page_description": "Explore available items",
        "content_items": ["Filter Options", "Sort By Price", "View Details"],
        "status_text": "comparing",
        "navigation": {"available_actions": ["advance", "branch"]}
    },
    "S2": {
        "page_title": "Details",
        "page_description": "Item specifications and reviews",
        "content_items": ["Customer Reviews", "Technical Specs", "Related Items"],
        "status_text": "reviewing",
        "navigation": {"available_actions": ["advance", "branch"]}
    }
}

# URL is constant (single-page app)
URL = "/app"


def hash_content(content_dict):
    """SHA-256 of JSON response, truncated to 16 hex chars."""
    s = json.dumps(content_dict, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def generate_session_directions(rng):
    """Generate session directions ONCE with seed=42."""
    return {f"session_{i}": rng.choice(["left", "right"]) for i in range(N_SESSIONS)}


def get_p_dir(direction):
    return P_LEFT if direction == "left" else P_RIGHT


def next_state_stochastic(state, action, direction, rng):
    """Stochastic transition: p_dir probability of 'intended' next state."""
    # Intended transition: cyclic advance or branch
    if action == "advance":
        intended = STATE_LABELS[(STATE_LABELS.index(state) + 1) % N_STATES]
        other = STATE_LABELS[(STATE_LABELS.index(state) + 2) % N_STATES]
    else:  # branch
        intended = STATE_LABELS[(STATE_LABELS.index(state) + 2) % N_STATES]
        other = STATE_LABELS[(STATE_LABELS.index(state) + 1) % N_STATES]

    p = get_p_dir(direction)
    if rng.random() < p:
        return intended
    else:
        return other


def generate_trajectories(session_directions, content_map, rng):
    """Generate trajectories: list of (session_id, step, state, action, next_state, response_hash)."""
    transitions = []
    for traj_idx in range(N_TRAJECTORIES):
        session_id = f"session_{rng.integers(0, N_SESSIONS)}"
        state = STATE_LABELS[rng.integers(0, N_STATES)]
        direction = session_directions[session_id]

        for step in range(STEPS_PER_TRAJECTORY):
            action = rng.choice(ACTIONS)
            ns = next_state_stochastic(state, action, direction, rng)
            resp_hash = hash_content(content_map[state])
            transitions.append({
                "session_id": session_id,
                "traj_idx": traj_idx,
                "step": step,
                "state": state,
                "action": action,
                "next_state": ns,
                "response_hash": resp_hash,
                "url": URL,
                "direction": direction
            })
            state = ns
    return transitions


def build_strata(transitions, K):
    """Build strata by (url, action_history_K, step)."""
    strata = defaultdict(list)
    # Group transitions by session and trajectory for history building
    by_traj = defaultdict(list)
    for t in transitions:
        by_traj[(t["session_id"], t["traj_idx"])].append(t)

    # Sort each trajectory by step
    for key in by_traj:
        by_traj[key].sort(key=lambda x: x["step"])

    # Build action history for each transition
    for (sess, traj), traj_trans in by_traj.items():
        actions_in_traj = [t["action"] for t in traj_trans]
        states_in_traj = [t["state"] for t in traj_trans]
        for i, t in enumerate(traj_trans):
            # Action history: last K actions before this step (or START padding)
            history = []
            for k in range(1, K + 1):
                if i - k >= 0:
                    history.append(actions_in_traj[i - k])
                else:
                    history.append("START")
            history_key = tuple(history)
            stratum_key = (t["url"], history_key, t["step"])
            strata[stratum_key].append({
                "state": t["state"],
                "next_state": t["next_state"],
                "response_hash": t["response_hash"],
                "session_id": t["session_id"],
                "traj_idx": t["traj_idx"]
            })
    return strata


def compute_pmi(strata):
    """Compute plug-in PMI per stratum, weighted average."""
    total_pmi = 0.0
    total_weight = 0
    stratum_details = {}

    for stratum_key, items in strata.items():
        N = len(items)
        if N < 2:
            continue

        # P(S_next, Response)
        joint = Counter()
        for item in items:
            joint[(item["next_state"], item["response_hash"])] += 1

        # P(S_next), P(Response)
        marg_next = Counter()
        marg_resp = Counter()
        for item in items:
            marg_next[item["next_state"]] += 1
            marg_resp[item["response_hash"]] += 1

        # PMI for this stratum
        pmi = 0.0
        for (ns, rh), count in joint.items():
            p_joint = count / N
            p_next = marg_next[ns] / N
            p_resp = marg_resp[rh] / N
            if p_joint > 0 and p_next > 0 and p_resp > 0:
                pmi += p_joint * np.log2(p_joint / (p_next * p_resp))

        # Weight by stratum size
        total_pmi += pmi * N
        total_weight += N

        stratum_details[stratum_key] = {
            "N": N,
            "PMI": pmi,
            "unique_responses": len(marg_resp),
            "unique_next_states": len(marg_next)
        }

    if total_weight == 0:
        return 0.0, stratum_details, 0
    return total_pmi / total_weight, stratum_details, total_weight


def permutation_test_pmi(strata, rng, n_perms=N_PERMUTATIONS):
    """Within-strata permutation test: shuffle Response_before labels."""
    perm_pmis = []
    for perm_idx in range(n_perms):
        shuffled_strata = {}
        for stratum_key, items in strata.items():
            resp_hashes = [item["response_hash"] for item in items]
            rng.shuffle(resp_hashes)
            shuffled_items = []
            for item, new_resp in zip(items, resp_hashes):
                shuffled_items.append({**item, "response_hash": new_resp})
            shuffled_strata[stratum_key] = shuffled_items
        pmi, _, _ = compute_pmi(shuffled_strata)
        perm_pmis.append(pmi)
    return np.array(perm_pmis)


def content_shuffled_control(transitions, session_directions, rng):
    """Positive control: replace each transition's response with content from a random state.
    
    Per spec: "replace each trajectory's response content with content from a random state
    (preserving the many-to-one mapping structure but breaking state→content pairing)."
    
    This randomly assigns response hashes from the pool of possible hashes, independent
    of the actual state, breaking R→S pairing while preserving the many-to-one hash pool.
    """
    # Pool of possible response hashes (preserving many-to-one structure: 2 unique hashes)
    mto_hashes = [hash_content(CONTENT_MANY_TO_ONE[s]) for s in STATE_LABELS]
    unique_hashes = list(set(mto_hashes))  # Should be 2 unique hashes

    shuffled_transitions = []
    for t in transitions:
        # Replace with a random hash from the pool (independent of actual state)
        new_hash = rng.choice(unique_hashes)
        shuffled_transitions.append({**t, "response_hash": new_hash})
    return shuffled_transitions


def state_independent_baseline(transitions, rng):
    """Baseline: constant response regardless of state."""
    constant_hash = hash_content({"constant": True})
    return [{**t, "response_hash": constant_hash} for t in transitions]


def compute_conditional_entropy(transitions, K):
    """H(S_next | URL, H_K)."""
    strata = build_strata(transitions, K)
    total_entropy = 0.0
    total_weight = 0

    for stratum_key, items in strata.items():
        N = len(items)
        if N < 2:
            continue

        # P(S_next | stratum)
        next_counts = Counter(item["next_state"] for item in items)
        entropy = 0.0
        for ns, count in next_counts.items():
            p = count / N
            if p > 0:
                entropy -= p * np.log2(p)

        total_entropy += entropy * N
        total_weight += N

    if total_weight == 0:
        return 0.0
    return total_entropy / total_weight


def check_determinism(transitions):
    """P(Response_hash | FSM_state, session, step) = 1.0"""
    groups = defaultdict(set)
    for t in transitions:
        key = (t["state"], t["session_id"], t["step"])
        groups[key].add(t["response_hash"])

    violations = 0
    for key, hashes in groups.items():
        if len(hashes) > 1:
            violations += 1

    total_groups = len(groups)
    if total_groups == 0:
        return 0.0, 0, 0
    return 1.0 - (violations / total_groups), total_groups, violations


def verify_transitions(transitions, session_directions):
    """Verify transition probabilities."""
    counts = defaultdict(lambda: {"total": 0, "intended": 0})
    intended_next = {
        ("S0", "advance"): "S1", ("S0", "branch"): "S2",
        ("S1", "advance"): "S2", ("S1", "branch"): "S0",
        ("S2", "advance"): "S0", ("S2", "branch"): "S1"
    }

    for t in transitions:
        direction = session_directions[t["session_id"]]
        key = (t["state"], t["action"], direction)
        counts[key]["total"] += 1
        if t["next_state"] == intended_next[(t["state"], t["action"])]:
            counts[key]["intended"] += 1

    results = {}
    for key, c in sorted(counts.items()):
        if c["total"] > 0:
            p_hat = c["intended"] / c["total"]
            results[f"{key[0]}_{key[1]}_{key[2]}"] = {
                "p_hat": round(p_hat, 4),
                "total": c["total"],
                "intended": c["intended"],
                "expected": P_LEFT if key[2] == "left" else P_RIGHT
            }
    return results


def main():
    print("=" * 70)
    print("EXP-PHYSICS-35137030850 — EXECUTE")
    print("Branching FSM: many-to-one vs unique content mapping")
    print("=" * 70)

    t_start = time.time()
    rng = np.random.default_rng(SEED)

    # ─── Step 1: Generate session directions ONCE ──────────────────────────
    session_directions = generate_session_directions(rng)
    print(f"\nSession directions: {dict(session_directions)}")

    # ─── Step 2: Generate trajectories for both conditions ────────────────
    print("\n--- Generating many-to-one condition ---")
    trans_mto = generate_trajectories(session_directions, CONTENT_MANY_TO_ONE, rng)
    print(f"  Transitions: {len(trans_mto)}")

    print("\n--- Generating unique-content condition ---")
    trans_uniq = generate_trajectories(session_directions, CONTENT_UNIQUE, rng)
    print(f"  Transitions: {len(trans_uniq)}")

    # ─── Step 3: Verify response hashes ──────────────────────────────────
    print("\n--- Response hash verification ---")
    mto_hashes = set(t["response_hash"] for t in trans_mto)
    uniq_hashes = set(t["response_hash"] for t in trans_uniq)
    print(f"  Many-to-one unique hashes: {len(mto_hashes)} (expected ~2)")
    print(f"  Unique-content unique hashes: {len(uniq_hashes)} (expected ~3)")

    # ─── Step 4: Determinism check ────────────────────────────────────────
    print("\n--- Determinism check ---")
    det_acc_mto, det_groups_mto, det_viol_mto = check_determinism(trans_mto)
    det_acc_uniq, det_groups_uniq, det_viol_uniq = check_determinism(trans_uniq)
    print(f"  Many-to-one: accuracy={det_acc_mto:.4f} groups={det_groups_mto} violations={det_viol_mto}")
    print(f"  Unique-content: accuracy={det_acc_uniq:.4f} groups={det_groups_uniq} violations={det_viol_uniq}")

    # ─── Step 5: Transition verification ──────────────────────────────────
    print("\n--- Transition probability verification ---")
    trans_verify_mto = verify_transitions(trans_mto, session_directions)
    for k, v in list(trans_verify_mto.items())[:4]:
        print(f"  {k}: p_hat={v['p_hat']:.4f} (expected={v['expected']}) N={v['total']}")

    # ─── Step 6: Conditional entropy ──────────────────────────────────────
    print("\n--- Conditional entropy ---")
    H_mto_K3 = compute_conditional_entropy(trans_mto, 3)
    H_uniq_K3 = compute_conditional_entropy(trans_uniq, 3)
    print(f"  H(S_next|URL,H_K=3) many-to-one: {H_mto_K3:.4f} bits")
    print(f"  H(S_next|URL,H_K=3) unique: {H_uniq_K3:.4f} bits")

    # ─── Step 7: PMI computation for both conditions at K=1 and K=3 ──────
    results = {}
    for condition_name, transitions in [("mto", trans_mto), ("uniq", trans_uniq)]:
        results[condition_name] = {}
        for K in K_VALUES:
            print(f"\n--- PMI: {condition_name} K={K} ---")
            strata = build_strata(transitions, K)
            n_strata = len(strata)
            n_items = sum(len(v) for v in strata.values())
            print(f"  Strata: {n_strata}, Items: {n_items}")

            obs_pmi, stratum_details, total_weight = compute_pmi(strata)
            print(f"  Observed PMI: {obs_pmi:.6f} bits")

            # Cardinality check
            cardinalities = [d["unique_responses"] for d in stratum_details.values()]
            max_card = max(cardinalities) if cardinalities else 0
            max_card_ratio = max_card / max(total_weight, 1)
            print(f"  Max |R|: {max_card}, max ratio: {max_card_ratio:.4f}")

            # Permutation test
            perm_seed = SEED + abs(hash((condition_name, K))) % (2**31)
            perm_rng = np.random.default_rng(perm_seed)
            perm_pmis = permutation_test_pmi(strata, perm_rng, N_PERMUTATIONS)
            perm_mean = perm_pmis.mean()
            perm_std = perm_pmis.std()
            bc_pmi = obs_pmi - perm_mean

            # One-sided p-value: fraction of permuted PMIs >= observed
            p_value = (perm_pmis >= obs_pmi).mean()
            # Bonferroni corrected
            p_bonf = min(p_value * BONFERRONI_COMPARISONS, 1.0)

            print(f"  Perm mean: {perm_mean:.6f}, perm std: {perm_std:.6f}")
            print(f"  BC PMI: {bc_pmi:.6f}")
            print(f"  Raw p: {p_value:.6f}, Bonf p: {p_bonf:.6f}")

            results[condition_name][K] = {
                "observed_pmi": round(obs_pmi, 6),
                "perm_mean": round(perm_mean, 6),
                "perm_std": round(perm_std, 6),
                "bc_pmi": round(bc_pmi, 6),
                "p_value": round(p_value, 6),
                "p_bonf": round(p_bonf, 6),
                "n_strata": n_strata,
                "n_items": n_items,
                "max_cardinality": max_card,
                "max_card_ratio": round(max_card_ratio, 6),
                "stratum_details": {str(k): v for k, v in stratum_details.items()}
            }

    # ─── Step 8: Positive control (content-shuffled) on H>0 strata ───────
    print("\n--- Positive control: content-shuffled on many-to-one ---")
    trans_cs = content_shuffled_control(trans_mto, session_directions, np.random.default_rng(SEED + 1000))

    # Only on H>0 strata
    strata_mto_K3 = build_strata(trans_mto, 3)
    h0_strata_keys = {k for k, v in strata_mto_K3.items()
                      if len(set(item["next_state"] for item in v)) > 1}
    print(f"  H>0 strata: {len(h0_strata_keys)} / {len(strata_mto_K3)}")

    # Filter content-shuffled transitions to H>0 strata
    cs_filtered = []
    for t in trans_cs:
        sess, traj = t["session_id"], t["traj_idx"]
        # Rebuild stratum key
        strata_all = build_strata(trans_cs, 3)
        # We'll compute PMI on full data and H>0 subset
    strata_cs = build_strata(trans_cs, 3)

    # H>0 strata for content-shuffled
    cs_h0_strata = {k: v for k, v in strata_cs.items() if k in h0_strata_keys}
    obs_pmi_cs, _, _ = compute_pmi(strata_cs)
    perm_rng_cs = np.random.default_rng(SEED + 2000)
    perm_pmi_cs = permutation_test_pmi(strata_cs, perm_rng_cs, N_PERMUTATIONS)
    bc_pmi_cs = obs_pmi_cs - perm_pmi_cs.mean()
    perm_std_cs = perm_pmi_cs.std()

    # H>0 strata only
    obs_pmi_cs_h0, _, _ = compute_pmi(cs_h0_strata)
    perm_pmi_cs_h0 = permutation_test_pmi(cs_h0_strata, perm_rng_cs, N_PERMUTATIONS)
    bc_pmi_cs_h0 = obs_pmi_cs_h0 - perm_pmi_cs_h0.mean()
    perm_std_cs_h0 = perm_pmi_cs_h0.std()

    print(f"  Full: BC PMI={bc_pmi_cs:.6f}, perm_std={perm_std_cs:.6f}")
    print(f"  H>0:  BC PMI={bc_pmi_cs_h0:.6f}, perm_std={perm_std_cs_h0:.6f}")

    positive_control_pass = (abs(bc_pmi_cs_h0) < 3 * perm_std_cs_h0) and (perm_std_cs_h0 > 0)
    print(f"  Positive control pass: {positive_control_pass}")

    # ─── Step 9: Null control (shuffled labels within strata) ────────────
    print("\n--- Null control: shuffled labels within strata ---")
    # Compute shuffled PMI for each of N_PERMUTATIONS independent shuffles
    null_rng = np.random.default_rng(SEED + 3000)
    perm_pmi_null = permutation_test_pmi(strata_mto_K3, null_rng, N_PERMUTATIONS)
    # BC corrected shuffled PMI: each shuffled PMI minus the permutation mean
    perm_mean_null = perm_pmi_null.mean()
    bc_shuffled_pmi = perm_pmi_null - perm_mean_null
    bc_null_mean = bc_shuffled_pmi.mean()  # Should be ~0 by construction
    bc_null_std = bc_shuffled_pmi.std()
    # Also report raw (un-corrected) shuffled PMI mean for reference
    raw_null_mean = perm_pmi_null.mean()
    raw_null_std = perm_pmi_null.std()
    print(f"  Raw shuffled PMI mean: {raw_null_mean:.6f}, std: {raw_null_std:.6f}")
    print(f"  BC shuffled PMI mean: {bc_null_mean:.6f}, std: {bc_null_std:.6f}")
    print(f"  Perm mean (bias estimate): {perm_mean_null:.6f}")
    # Null control pass: raw shuffled PMI should be near zero
    null_control_pass_raw = abs(raw_null_mean) < 3 * raw_null_std
    # BC-corrected check
    null_control_pass_bc = abs(bc_null_mean) < 3 * bc_null_std
    print(f"  Null control pass (raw): {null_control_pass_raw}")
    print(f"  Null control pass (BC): {null_control_pass_bc}")

    # ─── Step 10: Cardinality summary ─────────────────────────────────────
    print("\n--- Cardinality summary ---")
    for cond, trans in [("mto", trans_mto), ("uniq", trans_uniq)]:
        strata3 = build_strata(trans, 3)
        all_card = [len(set(item["response_hash"] for item in items))
                    for items in strata3.values()]
        print(f"  {cond}: cardinalities {Counter(all_card)}")

    # ─── Step 11: Compute diff between conditions ────────────────────────
    bc_mto_K3 = results["mto"][3]["bc_pmi"]
    bc_uniq_K3 = results["uniq"][3]["bc_pmi"]
    diff_K3 = bc_mto_K3 - bc_uniq_K3
    print(f"\n--- Condition comparison at K=3 ---")
    print(f"  Many-to-one BC PMI: {bc_mto_K3:.6f}")
    print(f"  Unique-content BC PMI: {bc_uniq_K3:.6f}")
    print(f"  Difference (mto - uniq): {diff_K3:.6f}")

    # ─── Step 12: Apply frozen decision rule ──────────────────────────────
    print("\n" + "=" * 70)
    print("DECISION RULE EVALUATION")
    print("=" * 70)

    c1 = H_mto_K3 > 0.2
    c2 = (bc_mto_K3 > 0.05) and (results["mto"][3]["p_bonf"] < 0.0125)
    c3 = bc_mto_K3 > bc_uniq_K3 - 0.1
    c4 = positive_control_pass
    c5 = (det_acc_mto == 1.0) and (det_acc_uniq == 1.0)
    c6 = len(trans_mto) >= 500 and len(trans_uniq) >= 500
    # c7: cardinality check on mto
    mto_card_ok = results["mto"][3]["max_card_ratio"] < 0.8

    print(f"  C1 (H > 0.2): {c1} (H={H_mto_K3:.4f})")
    print(f"  C2 (BC PMI > 0.05, Bonf p < 0.0125): {c2} (BC={bc_mto_K3:.6f}, p_bonf={results['mto'][3]['p_bonf']:.6f})")
    print(f"  C3 (mto > uniq - 0.1): {c3} (diff={diff_K3:.6f})")
    print(f"  C4 (positive control): {c4}")
    print(f"  C5 (determinism): {c5}")
    print(f"  C6 (N >= 500): {c6}")
    print(f"  C7 (cardinality < 0.8): {mto_card_ok} (max_ratio={results['mto'][3]['max_card_ratio']:.4f})")

    all_pass = c1 and c2 and c3 and c4 and c5 and c6 and mto_card_ok
    if all_pass:
        verdict = "SURVIVES_CURRENT_TEST"
    elif bc_mto_K3 <= 0.05 or bc_mto_K3 < bc_uniq_K3 - 0.1:
        verdict = "FALSIFIED-IN-SETTING"
    else:
        verdict = "MEASUREMENT_INVALID"

    print(f"\n  VERDICT: {verdict}")

    t_end = time.time()
    print(f"\nElapsed: {t_end - t_start:.1f}s")

    # ─── Write raw results JSON ──────────────────────────────────────────
    raw_output = {
        "experiment_id": "EXP-PHYSICS-35137030850",
        "seed": SEED,
        "n_trajectories": N_TRAJECTORIES,
        "steps_per_trajectory": STEPS_PER_TRAJECTORY,
        "n_sessions": N_SESSIONS,
        "session_directions": session_directions,
        "mto_unique_hashes": sorted(list(mto_hashes)),
        "uniq_unique_hashes": sorted(list(uniq_hashes)),
        "determinism": {
            "mto": {"accuracy": det_acc_mto, "groups": det_groups_mto, "violations": det_viol_mto},
            "uniq": {"accuracy": det_acc_uniq, "groups": det_groups_uniq, "violations": det_viol_uniq}
        },
        "conditional_entropy": {
            "mto_K3": round(H_mto_K3, 6),
            "uniq_K3": round(H_uniq_K3, 6)
        },
        "pmi_results": results,
        "positive_control": {
            "bc_pmi_full": round(bc_pmi_cs, 6),
            "bc_pmi_h0": round(bc_pmi_cs_h0, 6),
            "perm_std_full": round(perm_std_cs, 6),
            "perm_std_h0": round(perm_std_cs_h0, 6),
            "h0_strata_count": len(h0_strata_keys),
            "total_strata_count": len(strata_mto_K3),
            "pass": positive_control_pass
        },
        "null_control": {
            "raw_shuffled_pmi_mean": round(raw_null_mean, 6),
            "raw_shuffled_pmi_std": round(raw_null_std, 6),
            "bc_shuffled_pmi_mean": round(bc_null_mean, 6),
            "bc_shuffled_pmi_std": round(bc_null_std, 6),
            "perm_mean_bias": round(perm_mean_null, 6),
            "pass_raw": null_control_pass_raw,
            "pass_bc": null_control_pass_bc
        },
        "condition_comparison": {
            "bc_mto_K3": round(bc_mto_K3, 6),
            "bc_uniq_K3": round(bc_uniq_K3, 6),
            "diff_K3": round(diff_K3, 6)
        },
        "transition_verification": trans_verify_mto,
        "decision_criteria": {
            "C1_entropy": {"pass": c1, "value": round(H_mto_K3, 4)},
            "C2_primary_pmi": {"pass": c2, "bc_pmi": round(bc_mto_K3, 6), "p_bonf": round(results["mto"][3]["p_bonf"], 6)},
            "C3_condition_diff": {"pass": c3, "diff": round(diff_K3, 6)},
            "C4_positive_control": {"pass": c4},
            "C5_determinism": {"pass": c5},
            "C6_sample_size": {"pass": c6, "mto_n": len(trans_mto), "uniq_n": len(trans_uniq)},
            "C7_cardinality": {"pass": mto_card_ok, "max_ratio": results["mto"][3]["max_card_ratio"]}
        },
        "verdict": verdict,
        "elapsed_seconds": round(t_end - t_start, 1)
    }

    # Convert numpy types to native Python for JSON serialization
    def to_native(v):
        if isinstance(v, (np.bool_,)):
            return bool(v)
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            return float(v)
        if isinstance(v, np.str_):
            return str(v)
        if isinstance(v, dict):
            return {to_native(k): to_native(v2) for k, v2 in v.items()}
        if isinstance(v, list):
            return [to_native(x) for x in v]
        if isinstance(v, tuple):
            return tuple(to_native(x) for x in v)
        return v

    raw_output = to_native(raw_output)

    outdir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(outdir, "raw_result.json")
    with open(raw_path, "w") as f:
        json.dump(raw_output, f, indent=2)
    print(f"\nRaw results written to {raw_path}")

    return raw_output


if __name__ == "__main__":
    main()
