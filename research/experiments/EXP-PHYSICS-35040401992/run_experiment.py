#!/usr/bin/env python3
"""
EXP-PHYSICS-35040401992 — Branching FSM network-response PMI experiment.

Frozen design: test whether network-response payload structure carries
conditional PMI about next state on a branching FSM where action-history
at K=3 does NOT fully determine next state (H > 0.2 bits).

Implements exactly the preregistered analysis plan.
"""

import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from typing import Any

import numpy as np

# ============================================================
# 1. FSM DEFINITION (frozen in spec.json)
# ============================================================

STATES = ["S0", "S1", "S2"]
ACTIONS = ["advance", "branch"]


def transition(state: str, action: str, direction: str) -> str:
    """Deterministic transition given session direction."""
    if state == "S0":
        if action == "advance":
            return "S1"
        else:  # branch
            return "S2" if direction == "left" else "S1"
    elif state == "S1":
        if action == "advance":
            return "S2"
        else:  # branch
            return "S0" if direction == "left" else "S2"
    elif state == "S2":
        if action == "advance":
            return "S0"
        else:  # branch
            return "S1" if direction == "left" else "S0"
    raise ValueError(f"Unknown state: {state}")


# ============================================================
# 2. RESPONSE GENERATION (frozen in spec.json)
# ============================================================

def make_state_dependent_response(state: str, step: int, session_id: str, direction: str) -> dict:
    """State-dependent response: encodes state information."""
    token = hashlib.sha256(session_id.encode()).hexdigest()[:8]
    return {
        "state_id": state,
        "step": step,
        "session_token": token,
        "direction": direction,
        "items": list(range(step)),
    }


def make_state_independent_response() -> dict:
    """State-independent response: constant regardless of state."""
    return {
        "state_id": "unknown",
        "step": 0,
        "session_token": "none",
        "direction": "unknown",
        "items": [],
    }


def response_hash(resp: dict) -> str:
    """SHA-256 hash of response, truncated to 16 hex chars."""
    raw = json.dumps(resp, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ============================================================
# 3. TRAJECTORY GENERATION
# ============================================================

def generate_trajectories(
    n_trajectories: int,
    n_steps: int,
    n_sessions: int,
    seed: int,
    state_dependent: bool,
    rng: random.Random,
) -> list[dict]:
    """Generate trajectories with given response type."""
    # Assign session IDs and directions
    session_ids = [f"session_{i}" for i in range(n_sessions)]
    session_directions = {sid: rng.choice(["left", "right"]) for sid in session_ids}

    trajectories = []
    for t in range(n_trajectories):
        session_id = rng.choice(session_ids)
        direction = session_directions[session_id]
        state = "S0"
        steps = []
        for step_idx in range(n_steps):
            action = rng.choice(ACTIONS)
            next_state = transition(state, action, direction)
            if state_dependent:
                resp = make_state_dependent_response(state, step_idx + 1, session_id, direction)
            else:
                resp = make_state_independent_response()
            resp_h = response_hash(resp)
            steps.append({
                "state": state,
                "action": action,
                "next_state": next_state,
                "response": resp,
                "response_hash": resp_h,
                "session_id": session_id,
                "direction": direction,
                "step": step_idx + 1,
            })
            state = next_state
        trajectories.append({
            "session_id": session_id,
            "direction": direction,
            "steps": steps,
        })
    return trajectories


# ============================================================
# 4. STRATIFICATION: build (URL, H_K) strata
# ============================================================

def build_action_history(steps: list[dict], k: int) -> str:
    """Build action history string of length k from trajectory steps.
    Uses START padding for initial steps."""
    if k == 0:
        return ""
    actions = [s["action"] for s in steps]
    # Pad with START on the left
    padded = ["START"] * k + actions
    # Take the last k actions before each step
    histories = []
    for i in range(len(steps)):
        # history at step i uses actions from steps [i-k+1, ..., i-1] (0-indexed)
        start_idx = i - k + 1
        if start_idx < 0:
            hist = ["START"] * max(0, -start_idx) + [steps[j]["action"] for j in range(max(0, start_idx), i + 1)]
            hist = hist[-k:]  # take last k
        else:
            hist = [steps[j]["action"] for j in range(start_idx, i + 1)]
        histories.append(tuple(hist))
    return histories


def build_strata(trajectories: list[dict], k: int) -> dict:
    """Build strata keyed by (URL_placeholder, action_history_k).
    URL is constant '/' for this experiment."""
    strata = defaultdict(list)
    for traj_idx, traj in enumerate(trajectories):
        steps = traj["steps"]
        histories = build_action_history(steps, k)
        for step_idx, step in enumerate(steps):
            # The history at step_idx is the action history BEFORE step_idx
            # Rebuild: history_k at step_idx uses actions from steps[max(0, step_idx-k+1):step_idx]
            if k == 0:
                hist = ()
            else:
                action_seq = [s["action"] for s in steps]
                start = max(0, step_idx - k + 1)
                hist = tuple(action_seq[start:step_idx + 1])
                # Ensure length k by padding START
                if len(hist) < k:
                    hist = ("START",) * (k - len(hist)) + hist
                hist = hist[-k:]
            key = ("/", hist)
            strata[key].append({
                "traj_idx": traj_idx,
                "step_idx": step_idx,
                "response_hash": step["response_hash"],
                "next_state": step["next_state"],
                "state": step["state"],
                "action": step["action"],
                "session_id": step["session_id"],
            })
    return strata


# ============================================================
# 5. PMI COMPUTATION
# ============================================================

def compute_pmi(stratum_entries: list[dict]) -> float:
    """Compute plug-in PMI for a stratum."""
    N = len(stratum_entries)
    if N < 2:
        return 0.0

    # Joint counts: n(r, s) for response_hash, next_state
    joint = Counter()
    marg_r = Counter()
    marg_s = Counter()
    for entry in stratum_entries:
        r = entry["response_hash"]
        s = entry["next_state"]
        joint[(r, s)] += 1
        marg_r[r] += 1
        marg_s[s] += 1

    # Weighted PMI
    pmi_sum = 0.0
    for (r, s), n_rs in joint.items():
        if n_rs == 0:
            continue
        p_rs = n_rs / N
        p_r = marg_r[r] / N
        p_s = marg_s[s] / N
        if p_r == 0 or p_s == 0:
            continue
        pmi = math.log2(p_rs / (p_r * p_s))
        pmi_sum += p_rs * pmi

    return pmi_sum


def compute_permutation_null(
    stratum_entries: list[dict],
    n_perms: int,
    rng: np.random.RandomState,
) -> tuple[float, float]:
    """Compute permutation null: mean and std of PMI under shuffled response labels."""
    N = len(stratum_entries)
    if N < 2:
        return 0.0, 0.0

    response_hashes = [e["response_hash"] for e in stratum_entries]
    perm_pmis = []

    for _ in range(n_perms):
        shuffled = response_hashes.copy()
        rng.shuffle(shuffled)
        perm_entries = [
            {**e, "response_hash": h}
            for e, h in zip(stratum_entries, shuffled)
        ]
        perm_pmis.append(compute_pmi(perm_entries))

    return float(np.mean(perm_pmis)), float(np.std(perm_pmis))


def compute_bias_corrected_pmi(
    strata: dict,
    n_perms: int,
    rng: np.random.RandomState,
) -> dict:
    """Compute bias-corrected PMI across all strata.

    Returns per-stratum and aggregate results.
    """
    results = {}
    total_observed = 0.0
    total_perm_mean = 0.0
    total_weight = 0
    all_perm_pmis = []

    for key, entries in strata.items():
        N = len(entries)
        if N < 2:
            continue

        observed = compute_pmi(entries)
        perm_mean, perm_std = compute_permutation_null(entries, n_perms, rng)

        bc_pmi = observed - perm_mean
        total_observed += observed * N
        total_perm_mean += perm_mean * N
        total_weight += N
        all_perm_pmis.append(perm_mean)

        results[key] = {
            "N": N,
            "observed_pmi": observed,
            "perm_mean": perm_mean,
            "perm_std": perm_std,
            "bias_corrected_pmi": bc_pmi,
            "n_unique_responses": len(set(e["response_hash"] for e in entries)),
        }

    if total_weight > 0:
        agg_observed = total_observed / total_weight
        agg_perm_mean = total_perm_mean / total_weight
        agg_bc = agg_observed - agg_perm_mean
    else:
        agg_observed = 0.0
        agg_perm_mean = 0.0
        agg_bc = 0.0

    return {
        "per_stratum": results,
        "aggregate": {
            "observed_pmi": agg_observed,
            "perm_mean": agg_perm_mean,
            "bias_corrected_pmi": agg_bc,
            "total_N": total_weight,
        },
    }


# ============================================================
# 6. PERMUTATION TEST WITHIN STRATA
# ============================================================

def permutation_test_stratum(
    stratum_entries: list[dict],
    n_perms: int,
    rng: np.random.RandomState,
) -> tuple[float, float, float]:
    """Permutation test for a single stratum.

    Returns: (p_raw, observed_pmi, perm_null_std)
    """
    observed = compute_pmi(stratum_entries)
    N = len(stratum_entries)
    if N < 2:
        return 1.0, observed, 0.0

    response_hashes = [e["response_hash"] for e in stratum_entries]
    count_ge = 0
    perm_pmis = []

    for _ in range(n_perms):
        shuffled = response_hashes.copy()
        rng.shuffle(shuffled)
        perm_entries = [
            {**e, "response_hash": h}
            for e, h in zip(stratum_entries, shuffled)
        ]
        perm_pmi = compute_pmi(perm_entries)
        perm_pmis.append(perm_pmi)
        if perm_pmi >= observed:
            count_ge += 1

    p_raw = count_ge / n_perms
    perm_std = float(np.std(perm_pmis))
    return p_raw, observed, perm_std


# ============================================================
# 7. BONFERRONI CORRECTION
# ============================================================

def bonferroni_correct(p_raw: float, n_comparisons: int) -> float:
    return min(p_raw * n_comparisons, 1.0)


# ============================================================
# 8. CONTROLS
# ============================================================

def session_randomized_control(
    trajectories: list[dict],
    state_dependent: bool,
    k: int,
    n_perms: int,
    rng_np: np.random.RandomState,
    seed: int,
) -> dict:
    """Session-randomized positive control: replace session_id with random from different trajectory."""
    rng_ctrl = random.Random(seed + 1000)
    all_sessions = [t["session_id"] for t in trajectories]

    # Build modified trajectories with randomized session assignment
    mod_trajs = []
    for i, traj in enumerate(trajectories):
        other_sessions = [s for j, s in enumerate(all_sessions) if j != i]
        new_session = rng_ctrl.choice(other_sessions)
        new_direction = rng_ctrl.choice(["left", "right"])
        steps = []
        for step in traj["steps"]:
            if state_dependent:
                resp = make_state_dependent_response(step["state"], step["step"], new_session, new_direction)
            else:
                resp = make_state_independent_response()
            resp_h = response_hash(resp)
            steps.append({
                **step,
                "response": resp,
                "response_hash": resp_h,
                "session_id": new_session,
                "direction": new_direction,
            })
        mod_trajs.append({"session_id": new_session, "direction": new_direction, "steps": steps})

    strata = build_strata(mod_trajs, k)
    results = compute_bias_corrected_pmi(strata, n_perms, rng_np)

    # Also compute per-stratum permutation test stats for the non-deterministic strata
    perm_null_stds = []
    for key, entries in strata.items():
        if len(entries) < 2:
            continue
        # Check if stratum is non-deterministic (multiple response hashes)
        unique_r = len(set(e["response_hash"] for e in entries))
        if unique_r > 1:
            _, _, perm_std = permutation_test_stratum(entries, min(n_perms, 100), rng_np)
            perm_null_stds.append(perm_std)

    return {
        "bias_corrected_pmi": results["aggregate"]["bias_corrected_pmi"],
        "observed_pmi": results["aggregate"]["observed_pmi"],
        "perm_mean": results["aggregate"]["perm_mean"],
        "perm_null_stds": perm_null_stds,
        "min_perm_null_std": min(perm_null_stds) if perm_null_stds else 0.0,
        "pass": abs(results["aggregate"]["bias_corrected_pmi"]) < 3 * max(min(perm_null_stds) if perm_null_stds else 0.0, 1e-10),
    }


def shuffled_labels_control(
    strata: dict,
    n_perms: int,
    rng_np: np.random.RandomState,
) -> dict:
    """Shuffled response labels null control within strata."""
    shuffled_pmis = []
    for key, entries in strata.items():
        if len(entries) < 2:
            continue
        # Check if non-deterministic
        unique_r = len(set(e["response_hash"] for e in entries))
        if unique_r > 1:
            for _ in range(100):
                response_hashes = [e["response_hash"] for e in entries]
                rng_np.shuffle(response_hashes)
                perm_entries = [
                    {**e, "response_hash": h}
                    for e, h in zip(entries, response_hashes)
                ]
                shuffled_pmis.append(compute_pmi(perm_entries))

    if shuffled_pmis:
        mean_shuffled = float(np.mean(shuffled_pmis))
        std_shuffled = float(np.std(shuffled_pmis))
    else:
        mean_shuffled = 0.0
        std_shuffled = 0.0

    return {
        "mean_shuffled_pmi": mean_shuffled,
        "std_shuffled_pmi": std_shuffled,
        "pass": abs(mean_shuffled) < 3 * max(std_shuffled, 1e-10),
    }


def determinism_check(trajectories: list[dict], state_dependent: bool) -> dict:
    """Check that P(response_hash | FSM_state, session) = 1.0 for both conditions."""
    # Group by (FSM_state, session_id)
    groups = defaultdict(list)
    for traj in trajectories:
        for step in traj["steps"]:
            groups[(step["state"], step["session_id"])].append(step["response_hash"])

    total = 0
    deterministic = 0
    for key, hashes in groups.items():
        total += 1
        if len(set(hashes)) == 1:
            deterministic += 1

    accuracy = deterministic / total if total > 0 else 0.0
    return {
        "total_groups": total,
        "deterministic_groups": deterministic,
        "accuracy": accuracy,
        "pass": accuracy == 1.0,
    }


# ============================================================
# 9. CONDITIONAL ENTROPY
# ============================================================

def compute_conditional_entropy(trajectories: list[dict], k: int) -> float:
    """Compute H(S_next | URL, H_K)."""
    strata = build_strata(trajectories, k)
    total_entropy = 0.0
    total_N = 0

    for key, entries in strata.items():
        N = len(entries)
        if N < 2:
            continue
        # Count next_state distribution
        next_states = Counter(e["next_state"] for e in entries)
        entropy = 0.0
        for s, count in next_states.items():
            p = count / N
            if p > 0:
                entropy -= p * math.log2(p)
        total_entropy += entropy * N
        total_N += N

    return total_entropy / total_N if total_N > 0 else 0.0


# ============================================================
# 10. MAIN EXPERIMENT
# ============================================================

def run_experiment(seed: int = 42, n_trajectories: int = 200, n_steps: int = 10,
                   n_sessions: int = 20, n_perms: int = 1000) -> dict:
    """Execute the full experiment."""
    print("=" * 60)
    print("EXP-PHYSICS-35040401992 — Branching FSM PMI Experiment")
    print("=" * 60)

    rng = random.Random(seed)
    rng_np = np.random.RandomState(seed)

    # --- Generate data ---
    print("\n[1] Generating trajectories...")
    trajs_sd = generate_trajectories(n_trajectories, n_steps, n_sessions, seed, state_dependent=True, rng=rng)
    trajs_si = generate_trajectories(n_trajectories, n_steps, n_sessions, seed + 1, state_dependent=False, rng=rng)

    print(f"  State-dependent: {len(trajs_sd)} trajectories, {len(trajs_sd) * n_steps} transitions")
    print(f"  State-independent: {len(trajs_si)} trajectories, {len(trajs_si) * n_steps} transitions")

    # --- Data quality check ---
    total_sd = sum(len(t["steps"]) for t in trajs_sd)
    total_si = sum(len(t["steps"]) for t in trajs_si)
    print(f"  Total transitions per condition: SD={total_sd}, SI={total_si}")

    # --- Conditional entropy check (ceiling elimination) ---
    print("\n[2] Checking conditional entropy (ceiling elimination)...")
    H_k3_sd = compute_conditional_entropy(trajs_sd, k=3)
    H_k3_si = compute_conditional_entropy(trajs_si, k=3)
    H_k1_sd = compute_conditional_entropy(trajs_sd, k=1)
    print(f"  H(S_next | URL, H_K=3) SD: {H_k3_sd:.4f} bits")
    print(f"  H(S_next | URL, H_K=3) SI: {H_k3_si:.4f} bits")
    print(f"  H(S_next | URL, H_K=1) SD: {H_k1_sd:.4f} bits")

    ceiling_eliminated = H_k3_sd > 0.2
    print(f"  Ceiling eliminated (H>0.2): {ceiling_eliminated}")

    # --- Build strata ---
    print("\n[3] Building strata...")
    strata_sd_k1 = build_strata(trajs_sd, k=1)
    strata_sd_k3 = build_strata(trajs_sd, k=3)
    strata_si_k1 = build_strata(trajs_si, k=1)
    strata_si_k3 = build_strata(trajs_si, k=3)

    print(f"  SD K=1: {len(strata_sd_k1)} strata, total N={sum(len(v) for v in strata_sd_k1.values())}")
    print(f"  SD K=3: {len(strata_sd_k3)} strata, total N={sum(len(v) for v in strata_sd_k3.values())}")
    print(f"  SI K=1: {len(strata_si_k1)} strata, total N={sum(len(v) for v in strata_si_k1.values())}")
    print(f"  SI K=3: {len(strata_si_k3)} strata, total N={sum(len(v) for v in strata_si_k3.values())}")

    # --- Compute bias-corrected PMI ---
    print("\n[4] Computing bias-corrected PMI...")
    bc_sd_k1 = compute_bias_corrected_pmi(strata_sd_k1, n_perms, rng_np)
    bc_sd_k3 = compute_bias_corrected_pmi(strata_sd_k3, n_perms, rng_np)
    bc_si_k1 = compute_bias_corrected_pmi(strata_si_k1, n_perms, rng_np)
    bc_si_k3 = compute_bias_corrected_pmi(strata_si_k3, n_perms, rng_np)

    print(f"  SD K=1: observed={bc_sd_k1['aggregate']['observed_pmi']:.4f}, "
          f"perm_mean={bc_sd_k1['aggregate']['perm_mean']:.4f}, "
          f"BC PMI={bc_sd_k1['aggregate']['bias_corrected_pmi']:.4f}")
    print(f"  SD K=3: observed={bc_sd_k3['aggregate']['observed_pmi']:.4f}, "
          f"perm_mean={bc_sd_k3['aggregate']['perm_mean']:.4f}, "
          f"BC PMI={bc_sd_k3['aggregate']['bias_corrected_pmi']:.4f}")
    print(f"  SI K=1: observed={bc_si_k1['aggregate']['observed_pmi']:.4f}, "
          f"perm_mean={bc_si_k1['aggregate']['perm_mean']:.4f}, "
          f"BC PMI={bc_si_k1['aggregate']['bias_corrected_pmi']:.4f}")
    print(f"  SI K=3: observed={bc_si_k3['aggregate']['observed_pmi']:.4f}, "
          f"perm_mean={bc_si_k3['aggregate']['perm_mean']:.4f}, "
          f"BC PMI={bc_si_k3['aggregate']['bias_corrected_pmi']:.4f}")

    # --- Permutation tests (4 comparisons for Bonferroni) ---
    print("\n[5] Running permutation tests (Bonferroni across 4 comparisons)...")
    n_comparisons = 4

    # SD K=3 (primary test)
    p_raw_sd_k3, obs_sd_k3, perm_std_sd_k3 = permutation_test_stratum_agg(
        strata_sd_k3, n_perms, rng_np
    )
    p_bonf_sd_k3 = bonferroni_correct(p_raw_sd_k3, n_comparisons)
    print(f"  SD K=3: p_raw={p_raw_sd_k3:.6f}, p_bonf={p_bonf_sd_k3:.6f}")

    # SD K=1
    p_raw_sd_k1, obs_sd_k1, perm_std_sd_k1 = permutation_test_stratum_agg(
        strata_sd_k1, n_perms, rng_np
    )
    p_bonf_sd_k1 = bonferroni_correct(p_raw_sd_k1, n_comparisons)
    print(f"  SD K=1: p_raw={p_raw_sd_k1:.6f}, p_bonf={p_bonf_sd_k1:.6f}")

    # SI K=3
    p_raw_si_k3, obs_si_k3, perm_std_si_k3 = permutation_test_stratum_agg(
        strata_si_k3, n_perms, rng_np
    )
    p_bonf_si_k3 = bonferroni_correct(p_raw_si_k3, n_comparisons)
    print(f"  SI K=3: p_raw={p_raw_si_k3:.6f}, p_bonf={p_bonf_si_k3:.6f}")

    # SI K=1
    p_raw_si_k1, obs_si_k1, perm_std_si_k1 = permutation_test_stratum_agg(
        strata_si_k1, n_perms, rng_np
    )
    p_bonf_si_k1 = bonferroni_correct(p_raw_si_k1, n_comparisons)
    print(f"  SI K=1: p_raw={p_raw_si_k1:.6f}, p_bonf={p_bonf_si_k1:.6f}")

    # --- Discrimination test: SD vs SI PMI difference ---
    print("\n[6] Discrimination test (SD vs SI)...")
    diff_k3 = bc_sd_k3["aggregate"]["bias_corrected_pmi"] - bc_si_k3["aggregate"]["bias_corrected_pmi"]
    diff_k1 = bc_sd_k1["aggregate"]["bias_corrected_pmi"] - bc_si_k1["aggregate"]["bias_corrected_pmi"]
    print(f"  K=3 difference: {diff_k3:.4f}")
    print(f"  K=1 difference: {diff_k1:.4f}")

    # Paired permutation test on difference across strata
    paired_p_k3 = paired_permutation_test(
        strata_sd_k3, strata_si_k3, n_perms=1000, rng_np=rng_np
    )
    paired_p_k1 = paired_permutation_test(
        strata_sd_k1, strata_si_k1, n_perms=1000, rng_np=rng_np
    )
    print(f"  K=3 paired permutation p: {paired_p_k3:.6f}")
    print(f"  K=1 paired permutation p: {paired_p_k1:.6f}")

    # --- Cardinality check ---
    print("\n[7] Cardinality check...")
    card_results = {}
    for name, strata in [("SD_K1", strata_sd_k1), ("SD_K3", strata_sd_k3),
                          ("SI_K1", strata_si_k1), ("SI_K3", strata_si_k3)]:
        stratum_cards = []
        all_pass = True
        for key, entries in strata.items():
            N = len(entries)
            n_unique = len(set(e["response_hash"] for e in entries))
            ratio = n_unique / N if N > 0 else 0
            passes = ratio < 0.8
            stratum_cards.append({
                "key": str(key),
                "N": N,
                "n_unique": n_unique,
                "ratio": ratio,
                "pass": passes,
            })
            if not passes:
                all_pass = False
        card_results[name] = {
            "all_pass": all_pass,
            "strata": stratum_cards,
        }
        print(f"  {name}: all_pass={all_pass}")

    # --- Controls ---
    print("\n[8] Running controls...")

    # Session-randomized control (positive control)
    print("  Session-randomized control (SD K=3)...")
    sess_rand = session_randomized_control(trajs_sd, state_dependent=True, k=3,
                                            n_perms=100, rng_np=np.random.RandomState(seed + 2000),
                                            seed=seed)
    print(f"    BC PMI: {sess_rand['bias_corrected_pmi']:.4f}")
    print(f"    min_perm_null_std: {sess_rand['min_perm_null_std']:.6f}")
    print(f"    pass: {sess_rand['pass']}")

    # Shuffled labels control
    print("  Shuffled labels control (SD K=3 non-deterministic strata)...")
    shuffled_ctrl = shuffled_labels_control(strata_sd_k3, n_perms=100, rng_np=np.random.RandomState(seed + 3000))
    print(f"    mean_shuffled_pmi: {shuffled_ctrl['mean_shuffled_pmi']:.6f}")
    print(f"    std_shuffled_pmi: {shuffled_ctrl['std_shuffled_pmi']:.6f}")
    print(f"    pass: {shuffled_ctrl['pass']}")

    # Determinism check
    print("  Determinism check...")
    det_sd = determinism_check(trajs_sd, state_dependent=True)
    det_si = determinism_check(trajs_si, state_dependent=False)
    print(f"  SD: accuracy={det_sd['accuracy']}, pass={det_sd['pass']}")
    print(f"  SI: accuracy={det_si['accuracy']}, pass={det_si['pass']}")

    # --- Action-history prediction accuracy ---
    print("\n[9] Action-history prediction accuracy...")
    acc_results = {}
    for k_val in [1, 2, 3]:
        strata = build_strata(trajs_sd, k=k_val)
        correct = 0
        total = 0
        for key, entries in strata.items():
            if len(entries) < 1:
                continue
            # Majority vote next_state
            ns_counts = Counter(e["next_state"] for e in entries)
            majority = ns_counts.most_common(1)[0][0]
            for e in entries:
                total += 1
                if e["next_state"] == majority:
                    correct += 1
        acc = correct / total if total > 0 else 0
        acc_results[f"K{k_val}"] = acc
        print(f"  K={k_val}: accuracy={acc:.4f}")

    # Frequency baseline
    all_next_states = Counter()
    for traj in trajs_sd:
        for step in traj["steps"]:
            all_next_states[step["next_state"]] += 1
    freq_acc = max(all_next_states.values()) / sum(all_next_states.values())
    print(f"  Frequency baseline: {freq_acc:.4f}")

    # --- Plug-in MI (uncorrected) for comparison with parent ---
    plug_in_mi_sd_k1 = bc_sd_k1["aggregate"]["observed_pmi"]
    plug_in_mi_sd_k3 = bc_sd_k3["aggregate"]["observed_pmi"]
    plug_in_mi_si_k1 = bc_si_k1["aggregate"]["observed_pmi"]
    plug_in_mi_si_k3 = bc_si_k3["aggregate"]["observed_pmi"]

    # --- Apply decision rule ---
    print("\n" + "=" * 60)
    print("DECISION RULE APPLICATION")
    print("=" * 60)

    decision = None
    reason_parts = []

    # Criterion 1: H(S_next|URL, H_K=3) > 0.2 bits
    c1 = ceiling_eliminated
    print(f"  C1: H(S_next|URL,H_K=3) > 0.2: {H_k3_sd:.4f} > 0.2 = {c1}")

    # Criterion 2: BC PMI on SD at K=3 > 0.05 with Bonferroni p < 0.0125
    c2_pmi = bc_sd_k3["aggregate"]["bias_corrected_pmi"] > 0.05
    c2_pval = p_bonf_sd_k3 < 0.0125
    c2 = c2_pmi and c2_pval
    print(f"  C2: BC PMI={bc_sd_k3['aggregate']['bias_corrected_pmi']:.4f} > 0.05: {c2_pmi}, "
          f"p_bonf={p_bonf_sd_k3:.6f} < 0.0125: {c2_pval} => {c2}")

    # Criterion 3: SD PMI > SI PMI by >= 0.05, paired p < 0.05
    c3_diff = diff_k3 >= 0.05
    c3_pval = paired_p_k3 < 0.05
    c3 = c3_diff and c3_pval
    print(f"  C3: diff={diff_k3:.4f} >= 0.05: {c3_diff}, paired_p={paired_p_k3:.6f} < 0.05: {c3_pval} => {c3}")

    # Criterion 4: Positive control passes AND perm_null_std > 0
    c4_pass = sess_rand["pass"]
    c4_std = sess_rand["min_perm_null_std"] > 0
    c4 = c4_pass and c4_std
    print(f"  C4: session-randomized pass={c4_pass}, perm_null_std>0={c4_std} => {c4}")

    # Criterion 5: Determinism check passes
    c5 = det_sd["pass"] and det_si["pass"]
    print(f"  C5: determinism SD={det_sd['pass']}, SI={det_si['pass']} => {c5}")

    # Criterion 6: >= 500 valid transitions per condition
    c6 = total_sd >= 500 and total_si >= 500
    print(f"  C6: SD={total_sd} >= 500, SI={total_si} >= 500 => {c6}")

    # Criterion 7: Cardinality |R| < 0.8 * N per stratum at K=3
    c7 = card_results["SD_K3"]["all_pass"]
    print(f"  C7: cardinality all_pass={c7}")

    all_pass = c1 and c2 and c3 and c4 and c5 and c6 and c7
    print(f"\n  ALL PASS: {all_pass}")

    if all_pass:
        decision = "SURVIVES_CURRENT_TEST"
    else:
        # Check if it's falsified or measurement invalid
        if not c1 or not c6 or not c7:
            decision = "MEASUREMENT_INVALID"
        else:
            decision = "FALSIFIED-IN-SETTING"

    print(f"  VERDICT: {decision}")

    # --- Package results ---
    result = {
        "experiment_id": "EXP-PHYSICS-35040401992",
        "lane": "physics",
        "seed": seed,
        "n_trajectories_per_condition": n_trajectories,
        "n_steps": n_steps,
        "n_sessions": n_sessions,
        "n_perms": n_perms,
        "ceiling_check": {
            "H_S_next_given_URL_HK_3_SD": H_k3_sd,
            "H_S_next_given_URL_HK_3_SI": H_k3_si,
            "H_S_next_given_URL_HK_1_SD": H_k1_sd,
            "ceiling_eliminated": ceiling_eliminated,
        },
        "per_k_results": {
            "1": {
                "state_dependent": {
                    "observed_pmi": bc_sd_k1["aggregate"]["observed_pmi"],
                    "perm_mean": bc_sd_k1["aggregate"]["perm_mean"],
                    "bias_corrected_pmi": bc_sd_k1["aggregate"]["bias_corrected_pmi"],
                    "perm_p_raw": p_raw_sd_k1,
                    "perm_p_bonf": p_bonf_sd_k1,
                    "perm_null_std": perm_std_sd_k1,
                },
                "state_independent": {
                    "observed_pmi": bc_si_k1["aggregate"]["observed_pmi"],
                    "perm_mean": bc_si_k1["aggregate"]["perm_mean"],
                    "bias_corrected_pmi": bc_si_k1["aggregate"]["bias_corrected_pmi"],
                    "perm_p_raw": p_raw_si_k1,
                    "perm_p_bonf": p_bonf_si_k1,
                    "perm_null_std": perm_std_si_k1,
                },
            },
            "3": {
                "state_dependent": {
                    "observed_pmi": bc_sd_k3["aggregate"]["observed_pmi"],
                    "perm_mean": bc_sd_k3["aggregate"]["perm_mean"],
                    "bias_corrected_pmi": bc_sd_k3["aggregate"]["bias_corrected_pmi"],
                    "perm_p_raw": p_raw_sd_k3,
                    "perm_p_bonf": p_bonf_sd_k3,
                    "perm_null_std": perm_std_sd_k3,
                },
                "state_independent": {
                    "observed_pmi": bc_si_k3["aggregate"]["observed_pmi"],
                    "perm_mean": bc_si_k3["aggregate"]["perm_mean"],
                    "bias_corrected_pmi": bc_si_k3["aggregate"]["bias_corrected_pmi"],
                    "perm_p_raw": p_raw_si_k3,
                    "perm_p_bonf": p_bonf_si_k3,
                    "perm_null_std": perm_std_si_k3,
                },
                "cardinality": {
                    "state_dependent": card_results["SD_K3"],
                    "state_independent": card_results["SI_K3"],
                },
            },
        },
        "discrimination": {
            "K3": {
                "diff_bc_pmi": diff_k3,
                "paired_perm_p": paired_p_k3,
                "diff_ge_005": diff_k3 >= 0.05,
                "paired_p_lt_005": paired_p_k3 < 0.05,
            },
            "K1": {
                "diff_bc_pmi": diff_k1,
                "paired_perm_p": paired_p_k1,
                "diff_ge_005": diff_k1 >= 0.05,
                "paired_p_lt_005": paired_p_k1 < 0.05,
            },
        },
        "controls": {
            "positive_control_session_randomized": {
                "description": "Replace session_id with random from different trajectory; response->state mapping broken",
                "bias_corrected_pmi": sess_rand["bias_corrected_pmi"],
                "min_perm_null_std": sess_rand["min_perm_null_std"],
                "pass_criterion": f"|{sess_rand['bias_corrected_pmi']:.6f}| < 3 * {sess_rand['min_perm_null_std']:.6f} = {3 * sess_rand['min_perm_null_std']:.6f}",
                "pass": sess_rand["pass"],
            },
            "null_control_shuffled_labels": {
                "description": "Permute response labels within strata; breaks R->S pairing",
                "mean_shuffled_pmi": shuffled_ctrl["mean_shuffled_pmi"],
                "std_shuffled_pmi": shuffled_ctrl["std_shuffled_pmi"],
                "pass_criterion": f"|{shuffled_ctrl['mean_shuffled_pmi']:.6f}| < 3 * {shuffled_ctrl['std_shuffled_pmi']:.6f} = {3 * shuffled_ctrl['std_shuffled_pmi']:.6f}",
                "pass": shuffled_ctrl["pass"],
            },
            "state_independent_baseline": {
                "description": "Same FSM, constant responses; expected BC PMI = 0",
                "K1_BC_PMI": bc_si_k1["aggregate"]["bias_corrected_pmi"],
                "K3_BC_PMI": bc_si_k3["aggregate"]["bias_corrected_pmi"],
                "pass": abs(bc_si_k3["aggregate"]["bias_corrected_pmi"]) < 0.01,
            },
            "determinism_check": {
                "state_dependent": det_sd,
                "state_independent": det_si,
            },
        },
        "action_history_accuracy": {
            **acc_results,
            "frequency_baseline": freq_acc,
        },
        "plug_in_mi_uncorrected": {
            "SD_K1": plug_in_mi_sd_k1,
            "SD_K3": plug_in_mi_sd_k3,
            "SI_K1": plug_in_mi_si_k1,
            "SI_K3": plug_in_mi_si_k3,
        },
        "total_transitions": {
            "state_dependent": total_sd,
            "state_independent": total_si,
        },
        "decision": decision,
        "decision_criteria": {
            "C1_ceiling_eliminated": c1,
            "C2_BC_PMI_gt_005_bonf_lt_0125": c2,
            "C3_SD_gt_SI_by_005_paired_p_lt_005": c3,
            "C4_positive_control_pass": c4,
            "C5_determinism_pass": c5,
            "C6_data_quality": c6,
            "C7_cardinality_bounded": c7,
        },
    }

    return result


# ============================================================
# 11. HELPERS
# ============================================================

def permutation_test_stratum_agg(
    strata: dict,
    n_perms: int,
    rng_np: np.random.RandomState,
) -> tuple[float, float, float]:
    """Aggregate permutation test across strata.

    For each non-deterministic stratum, compute p_raw.
    Then aggregate: overall p = weighted average of per-stratum p_raw.
    Also return aggregate observed PMI and perm null std.
    """
    total_N = 0
    total_observed = 0.0
    p_raw_values = []
    perm_stds = []

    for key, entries in strata.items():
        N = len(entries)
        if N < 2:
            continue
        # Check if non-deterministic
        unique_r = len(set(e["response_hash"] for e in entries))
        if unique_r <= 1:
            # Deterministic stratum: PMI = 0 trivially
            continue

        observed = compute_pmi(entries)
        response_hashes = [e["response_hash"] for e in entries]
        count_ge = 0
        perm_pmis = []

        for _ in range(n_perms):
            shuffled = response_hashes.copy()
            rng_np.shuffle(shuffled)
            perm_entries = [
                {**e, "response_hash": h}
                for e, h in zip(entries, shuffled)
            ]
            perm_pmi = compute_pmi(perm_entries)
            perm_pmis.append(perm_pmi)
            if perm_pmi >= observed:
                count_ge += 1

        p_raw = count_ge / n_perms
        perm_std = float(np.std(perm_pmis))
        p_raw_values.append(p_raw * N)
        perm_stds.append(perm_std)
        total_observed += observed * N
        total_N += N

    if total_N > 0:
        agg_p_raw = sum(p_raw_values) / total_N
        agg_observed = total_observed / total_N
    else:
        agg_p_raw = 1.0
        agg_observed = 0.0

    avg_perm_std = float(np.mean(perm_stds)) if perm_stds else 0.0

    return agg_p_raw, agg_observed, avg_perm_std


def paired_permutation_test(
    strata_a: dict,
    strata_b: dict,
    n_perms: int,
    rng_np: np.random.RandomState,
) -> float:
    """Paired permutation test on PMI difference across strata.

    For each stratum present in both A and B, compute the PMI difference.
    Then test whether the mean difference is > 0 by permuting condition labels.
    """
    # Compute per-stratum BC PMI differences
    diffs = []
    common_keys = set(strata_a.keys()) & set(strata_b.keys())

    for key in common_keys:
        entries_a = strata_a[key]
        entries_b = strata_b[key]
        if len(entries_a) < 2 or len(entries_b) < 2:
            continue
        pmi_a = compute_pmi(entries_a)
        pmi_b = compute_pmi(entries_b)
        diffs.append(pmi_a - pmi_b)

    if not diffs:
        return 1.0

    observed_mean_diff = float(np.mean(diffs))

    # Permutation test: flip signs of differences
    count_ge = 0
    for _ in range(n_perms):
        perm_diffs = [d if rng_np.random() > 0.5 else -d for d in diffs]
        if float(np.mean(perm_diffs)) >= observed_mean_diff:
            count_ge += 1

    return count_ge / n_perms


# ============================================================
# 12. EXECUTE
# ============================================================

if __name__ == "__main__":
    result = run_experiment(seed=42, n_trajectories=200, n_steps=10,
                            n_sessions=20, n_perms=1000)

    # Save result
    import os
    outdir = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(outdir, "raw_result.json")
    with open(outpath, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nRaw result saved to {outpath}")
