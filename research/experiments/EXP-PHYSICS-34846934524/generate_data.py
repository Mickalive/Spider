#!/usr/bin/env python3
"""
EXP-PHYSICS-34846934524 — Data Generation

Generates three SPA types with controlled non-determinism:
1. Deterministic: 1 DOM per state (baseline)
2. Independent per-step noise: DOM variants drawn independently per step (no session)
3. Session-correlated: persistent session_id determines DOM variant at each state

The session-correlated SPA creates genuine dependency between DOM_before and DOM_after
through the shared latent session variable, enabling positive PMI by construction.
"""

import hashlib
import json
import os
import random

random.seed(42)

OUTPUT_DIR = "research/experiments/EXP-PHYSICS-34846934524"
N_TRAJECTORIES = 500
STEPS_PER_TRAJECTORY = 10
N_SESSIONS = 10
N_VARIANTS = 5

# Linear FSM: each state has a unique outgoing action
FSM = {
    "landing": {"action": "begin", "next": "form_s1"},
    "form_s1": {"action": "advance", "next": "form_s2"},
    "form_s2": {"action": "finalize", "next": "review"},
    "review": {"action": "submit", "next": "complete"},
    "complete": {"action": "restart", "next": "landing"},
}

# State-specific DOM content
STATE_DOM = {
    "landing": {
        "title": "Welcome Page",
        "subtitle": "Start your journey",
        "buttons": ["Begin"],
        "nav": ["Home", "Help"],
    },
    "form_s1": {
        "title": "Step 1: Personal Info",
        "subtitle": "Enter your details",
        "form_fields": ["first_name", "last_name", "email"],
        "buttons": ["Advance"],
        "nav": ["Home", "Help", "Profile"],
    },
    "form_s2": {
        "title": "Step 2: Preferences",
        "subtitle": "Choose settings",
        "form_fields": ["theme", "language", "notifications"],
        "buttons": ["Finalize"],
        "nav": ["Home", "Help", "Settings"],
    },
    "review": {
        "title": "Review & Confirm",
        "subtitle": "Check your choices",
        "buttons": ["Submit", "Edit"],
        "nav": ["Home", "Help", "Cart"],
    },
    "complete": {
        "title": "Thank You",
        "subtitle": "Submission received",
        "buttons": ["Start Over"],
        "nav": ["Home", "Help"],
    },
}

# Independent per-step noise: 3 variants per state
INDEPENDENT_VARIANTS = 3


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_visible_text(state, variant_id=0, extra=""):
    dom = STATE_DOM[state]
    parts = [dom["title"], dom["subtitle"]]
    if "form_fields" in dom:
        parts.append("fields:" + "|".join(dom["form_fields"]))
    parts.append("btns:" + "|".join(dom["buttons"]))
    parts.append("nav:" + "|".join(dom["nav"]))
    if extra:
        parts.append(extra)
    parts.append(f"v{variant_id}")
    return "~".join(parts)


def make_a11y_tree(state, variant_id=0, extra=""):
    dom = STATE_DOM[state]
    lines = [
        "document",
        f"  heading1:{dom['title']}",
        f"  heading2:{dom['subtitle']}",
    ]
    for btn in dom["buttons"]:
        lines.append(f"  button:{btn}")
    if "form_fields" in dom:
        lines.append("  form")
        for field in dom["form_fields"]:
            lines.append(f"    textbox:{field}")
    lines.append("  navigation")
    for nav in dom["nav"]:
        lines.append(f"    link:{nav}")
    if extra:
        lines.append(f"  meta:{extra}")
    lines.append(f"  variant:{variant_id}")
    return "\n".join(lines)


def compute_numeric(state):
    dom = STATE_DOM[state]
    btn_count = len(dom["buttons"])
    field_count = len(dom.get("form_fields", []))
    nav_count = len(dom["nav"])
    element_count = 3 + btn_count + field_count + nav_count
    return {
        "element_count": element_count,
        "tree_depth": 4 if "form_fields" in dom else 3,
        "interactive_density": round(btn_count / max(element_count, 1), 4),
        "form_count": field_count,
    }


def multi_feature_hash(df):
    ns = df["numeric_structural"]
    combined = f"{df['visible_text_hash']}|{ns['element_count']}|{ns['tree_depth']}|{ns['interactive_density']}|{ns['form_count']}"
    return sha256(combined)


def make_dom_features(state, variant_id=0, extra=""):
    vt = make_visible_text(state, variant_id, extra)
    at = make_a11y_tree(state, variant_id, extra)
    ns = compute_numeric(state)
    df = {
        "visible_text": vt,
        "visible_text_hash": sha256(vt),
        "accessibility_tree": at,
        "accessibility_tree_hash": sha256(at),
        "numeric_structural": ns,
    }
    df["multi_feature_hash"] = multi_feature_hash(df)
    return df


def make_deterministic_dom(state, variant_id=0):
    return make_dom_features(state, variant_id)


def make_independent_noise_dom(state, rng):
    variant_id = rng.randint(0, INDEPENDENT_VARIANTS - 1)
    notification_count = variant_id * 33
    n_items = variant_id
    items = [f"item_{variant_id}_{i}" for i in range(n_items)]
    extra = f"notif:{notification_count}|items:{'|'.join(items)}"
    return make_dom_features(state, variant_id, extra)


def make_session_correlated_dom(state, session_id):
    """DOM variant is deterministic given session_id — the key mechanism for correlated non-determinism."""
    variant_id = session_id % N_VARIANTS
    notification_count = variant_id * 33
    n_items = variant_id
    items = [f"item_{variant_id}_{i}" for i in range(n_items)]
    # Session token encodes session identity in DOM
    session_token = sha256(f"session_{session_id}")
    extra = f"notif:{notification_count}|items:{'|'.join(items)}|token:{session_token[:16]}"
    return make_dom_features(state, variant_id, extra)


def generate_trajectory(spa_type, traj_id, rng):
    transitions = []
    current_state = "landing"

    # For session-correlated SPA, assign a persistent session_id
    if spa_type == "session_correlated":
        session_id = rng.randint(0, N_SESSIONS - 1)
    else:
        session_id = None

    for step in range(STEPS_PER_TRAJECTORY):
        fsm = FSM[current_state]
        action_label = fsm["action"]
        next_state = fsm["next"]

        # Generate DOM for current state
        if spa_type == "deterministic":
            current_dom = make_deterministic_dom(current_state)
        elif spa_type == "independent_noise":
            current_dom = make_independent_noise_dom(current_state, rng)
        else:  # session_correlated
            current_dom = make_session_correlated_dom(current_state, session_id)

        # Generate DOM for next state
        if spa_type == "deterministic":
            next_dom = make_deterministic_dom(next_state)
        elif spa_type == "independent_noise":
            next_dom = make_independent_noise_dom(next_state, rng)
        else:  # session_correlated
            next_dom = make_session_correlated_dom(next_state, session_id)

        transitions.append({
            "trajectory_id": traj_id,
            "step": step,
            "url": f"/{current_state}",
            "action": {"type": action_label, "target_href": f"/{action_label}"},
            "fsm_state_before": current_state,
            "fsm_state_after": next_state,
            "session_id": session_id,
            "state_before": {"dom_features": {
                "visible_text_hash": current_dom["visible_text_hash"],
                "accessibility_tree_hash": current_dom["accessibility_tree_hash"],
                "numeric_structural": current_dom["numeric_structural"],
                "multi_feature_hash": current_dom["multi_feature_hash"],
            }},
            "state_after": {"dom_features": {
                "visible_text_hash": next_dom["visible_text_hash"],
                "accessibility_tree_hash": next_dom["accessibility_tree_hash"],
                "numeric_structural": next_dom["numeric_structural"],
                "multi_feature_hash": next_dom["multi_feature_hash"],
            }},
        })

        current_state = next_state

    return transitions


def verify_session_mapping(transitions):
    """Verify session-to-variant determinism: for each session, DOM variant at each FSM state is deterministic."""
    # For each (session_id, fsm_state), collect the set of visible_text_hash values
    session_state_hashes = {}
    for t in transitions:
        sid = t.get("session_id")
        if sid is None:
            continue
        fsm_state = t["fsm_state_before"]
        vth = t["state_before"]["dom_features"]["visible_text_hash"]
        key = (sid, fsm_state)
        if key not in session_state_hashes:
            session_state_hashes[key] = set()
        session_state_hashes[key].add(vth)

    # Count violations: any (session, state) pair with >1 hash
    violations = sum(1 for hashes in session_state_hashes.values() if len(hashes) > 1)
    total_pairs = len(session_state_hashes)
    fraction_deterministic = 1.0 - (violations / total_pairs) if total_pairs > 0 else 1.0

    return {
        "total_session_state_pairs": total_pairs,
        "violations": violations,
        "fraction_deterministic": fraction_deterministic,
    }


def main():
    print("=" * 70)
    print("EXP-PHYSICS-34846934524 — Data Generation")
    print("=" * 70)

    all_data = {}
    spa_types = ["deterministic", "independent_noise", "session_correlated"]

    for spa_type in spa_types:
        print(f"\nGenerating {spa_type} SPA data...")
        all_transitions = []

        for traj_id in range(N_TRAJECTORIES):
            rng = random.Random(42 + traj_id)
            traj = generate_trajectory(spa_type, traj_id, rng)
            all_transitions.extend(traj)

        print(f"  Total transitions: {len(all_transitions)}")

        # Determinism check: P(DOM_hash_next | DOM_hash_current, Action)
        sa_map = {}
        for t in all_transitions:
            key = (
                t["state_before"]["dom_features"]["visible_text_hash"],
                t["action"]["type"],
            )
            if key not in sa_map:
                sa_map[key] = set()
            sa_map[key].add(t["state_after"]["dom_features"]["visible_text_hash"])

        det_pairs = sum(1 for v in sa_map.values() if len(v) == 1)
        det_acc = det_pairs / len(sa_map) if sa_map else 0
        print(f"  Determinism accuracy: {det_acc:.4f}")
        print(f"  Unique (S_before, Action) pairs: {len(sa_map)}, deterministic: {det_pairs}")

        # Session mapping verification for session_correlated
        if spa_type == "session_correlated":
            mapping = verify_session_mapping(all_transitions)
            print(f"  Session mapping: {mapping['fraction_deterministic']:.4f} "
                  f"({mapping['violations']}/{mapping['total_session_state_pairs']} violations)")

        # Count unique hashes
        vis_before = set(t["state_before"]["dom_features"]["visible_text_hash"] for t in all_transitions)
        vis_after = set(t["state_after"]["dom_features"]["visible_text_hash"] for t in all_transitions)
        print(f"  Unique visible_text_hash (before): {len(vis_before)}, (after): {len(vis_after)}")

        all_data[spa_type] = all_transitions

    output_path = os.path.join(OUTPUT_DIR, "raw_dom_captures.json")
    with open(output_path, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"\nRaw data saved to {output_path}")


if __name__ == "__main__":
    main()
