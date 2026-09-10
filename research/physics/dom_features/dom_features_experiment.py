#!/usr/bin/env python3
"""
EXP-PHYSICS-34524411213 — DOM Structural Features as State Representation for Web Dynamics
Tests whether DOM structural features predict next-state transitions on real SPA/form-heavy sites.

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).
"""

import json
import math
import random
import collections
import os
import sys
import time
from urllib.parse import urlparse, urljoin

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34524411213"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 2
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.025
N_TRAJECTORIES = 25
TRAJECTORY_LENGTH = 6
POLITE_DELAY = 0.3
STATE_CAPTURE_DELAY = 1.0

# Site definitions — genuine SPA sites
SITES = {
    "todomvc_react": {
        "name": "TodoMVC React",
        "entry_url": "https://todomvc.com/examples/react/dist/",
    },
    "todomvc_vue": {
        "name": "TodoMVC Vue",
        "entry_url": "https://todomvc.com/examples/vue/dist/",
    },
}


# ─── DOM Feature Extraction ──────────────────────────────────────────────────

def extract_dom_features(page):
    """Extract DOM structural features via Playwright page.evaluate()."""
    try:
        features = page.evaluate("""() => {
            function computeMaxDepth(el) {
                if (!el || !el.children || el.children.length === 0) return 1;
                let maxChild = 0;
                for (let i = 0; i < el.children.length; i++) {
                    const d = computeMaxDepth(el.children[i]);
                    if (d > maxChild) maxChild = d;
                }
                return 1 + maxChild;
            }
            const allElements = document.querySelectorAll('*');
            const interactiveElements = document.querySelectorAll(
                'button, a, input, select, textarea, [role="button"]'
            );
            return {
                element_count: allElements.length,
                tree_depth: computeMaxDepth(document.body),
                interactive_density: interactiveElements.length / Math.max(allElements.length, 1),
                form_count: document.querySelectorAll('form').length,
                input_count: document.querySelectorAll('input, select, textarea').length,
                button_count: document.querySelectorAll('button, [role="button"]').length
            };
        }""")
        return features
    except Exception as e:
        return {"element_count": 0, "tree_depth": 0, "interactive_density": 0,
                "form_count": 0, "input_count": 0, "button_count": 0}


def extract_browser_state(page):
    """Extract full browser state: URL, title, and DOM features."""
    url = page.url
    title = page.title()[:100]
    dom_features = extract_dom_features(page)
    return {"url": url, "title": title, "dom_features": dom_features}


# ─── Browser Data Collection ────────────────────────────────────────────────

def find_available_actions(page, entry_url):
    """Find available same-domain interactive actions."""
    actions = []
    entry_domain = urlparse(entry_url).netloc
    
    # Buttons
    try:
        buttons = page.locator("button:visible, [role=button]:visible").all()
        for btn in buttons[:15]:  # Limit to prevent explosion
            try:
                if btn.is_visible() and btn.is_enabled():
                    text = btn.inner_text()[:30].strip()
                    if text:
                        sel = f"button:has-text('{text[:20]}')"
                        actions.append({"type": "button_click", "href": f"btn://{text[:20]}",
                                        "selector": sel, "description": f"click: {text[:20]}"})
            except Exception:
                continue
    except Exception:
        pass
    
    # Links (same-domain)
    try:
        links = page.locator("a[href]:visible").all()
        for link in links[:15]:
            try:
                href = link.get_attribute("href") or ""
                if href.startswith("javascript:"):
                    continue
                if not href.startswith("http"):
                    href = urljoin(page.url, href)
                parsed = urlparse(href)
                if parsed.netloc == entry_domain or parsed.netloc == "":
                    text = link.inner_text()[:30].strip()
                    if text:
                        sel = f"a:has-text('{text[:20]}')"
                        actions.append({"type": "link_nav", "href": href,
                                        "selector": sel, "description": f"link: {text[:20]}"})
            except Exception:
                continue
    except Exception:
        pass
    
    # Inputs
    try:
        inputs = page.locator("input:not([type=hidden]):visible, textarea:visible").all()
        for inp in inputs[:10]:
            try:
                inp_id = inp.get_attribute("id") or ""
                placeholder = inp.get_attribute("placeholder") or ""
                sel = f"input[id='{inp_id}']" if inp_id else "input:visible"
                actions.append({"type": "input_submit", "href": f"input://{inp_id}",
                                "selector": sel, "description": f"input: {placeholder[:20]}"})
            except Exception:
                continue
    except Exception:
        pass
    
    return actions


def execute_action(page, action):
    """Execute an action on the page."""
    try:
        selector = action.get("selector", "")
        if not selector:
            return {"success": False, "error": "no selector"}
        element = page.locator(selector).first
        if action["type"] == "button_click":
            element.click(timeout=3000)
        elif action["type"] == "link_nav":
            element.click(timeout=3000)
        elif action["type"] == "input_submit":
            element.fill("")
            element.type(f"item_{random.randint(0, 999)}")
            element.press("Enter")
        else:
            element.click(timeout=3000)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def collect_browser_transitions(page, site_config, n_trajectories, trajectory_length, rng):
    """Collect browser transitions with DOM feature extraction."""
    transitions = []
    
    for traj_id in range(n_trajectories):
        try:
            page.goto(site_config["entry_url"], timeout=20000, wait_until="domcontentloaded")
            time.sleep(STATE_CAPTURE_DELAY)
            
            for step in range(trajectory_length):
                state_before = extract_browser_state(page)
                actions = find_available_actions(page, site_config["entry_url"])
                
                if not actions:
                    break
                
                action = rng.choice(actions)
                action_result = execute_action(page, action)
                
                if not action_result["success"]:
                    break
                
                time.sleep(STATE_CAPTURE_DELAY)
                state_after = extract_browser_state(page)
                
                transitions.append({
                    "trajectory_id": traj_id,
                    "step": step,
                    "state_before": state_before,
                    "action": {"action_type": action["type"], "target_href": action["href"],
                               "description": action.get("description", "")},
                    "state_after": state_after,
                })
                
                time.sleep(POLITE_DELAY)
        except Exception as e:
            continue
    
    return transitions


def classify_non_leakage(transitions):
    """Classify transitions as leakage or non-leakage."""
    non_leakage = []
    leakage_count = 0
    for t in transitions:
        target = t["action"]["target_href"]
        actual_url = t["state_after"]["url"]
        if target == actual_url and not target.startswith(("button://", "input://")):
            leakage_count += 1
        else:
            non_leakage.append(t)
    return non_leakage, leakage_count


# ─── State Representations ───────────────────────────────────────────────────

def state_url_only(state):
    """State = URL path."""
    return urlparse(state["url"]).path

def state_url_title(state):
    """State = (URL path, title)."""
    return (urlparse(state["url"]).path, state["title"])


# ─── Discretization ──────────────────────────────────────────────────────────

def fit_quantile_bins(values, n_bins=5):
    """Fit quantile bin edges."""
    if not values:
        return [0, 1]
    sorted_vals = sorted(set(values))
    if len(sorted_vals) <= n_bins:
        # Use unique values as edges
        edges = list(sorted_vals) + [sorted_vals[-1] + 1]
        return edges
    n = len(sorted_vals)
    edges = []
    for i in range(n_bins + 1):
        idx = min(int(i * (n - 1) / n_bins), n - 1)
        edges.append(sorted_vals[idx])
    return sorted(set(edges))


def discretize_value(value, edges):
    """Discretize a value into bin index."""
    for i in range(len(edges) - 1):
        if value < edges[i + 1]:
            return i
    return len(edges) - 2


def make_dom_state_fn(transitions, n_bins=5):
    """Create discretized DOM feature state function."""
    element_counts = [t["state_before"]["dom_features"]["element_count"] for t in transitions]
    tree_depths = [t["state_before"]["dom_features"]["tree_depth"] for t in transitions]
    densities = [t["state_before"]["dom_features"]["interactive_density"] for t in transitions]
    
    ec_edges = fit_quantile_bins(element_counts, n_bins)
    td_edges = fit_quantile_bins(tree_depths, n_bins)
    id_edges = fit_quantile_bins(densities, n_bins)
    
    def state_fn(state):
        df = state["dom_features"]
        return (discretize_value(df["element_count"], ec_edges),
                discretize_value(df["tree_depth"], td_edges),
                discretize_value(df["interactive_density"], id_edges))
    
    return state_fn, {"ec_edges": ec_edges, "td_edges": td_edges, "id_edges": id_edges}


# ─── PMI Computation ─────────────────────────────────────────────────────────

def extract_triples(transitions, state_fn):
    """Extract (state_repr, action, next_state_repr) triples."""
    return [(state_fn(t["state_before"]), t["action"]["action_type"],
             state_fn(t["state_after"])) for t in transitions]


def extract_trajectory_groups(transitions, state_fn):
    """Group transitions by trajectory_id."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(
            (state_fn(t["state_before"]), t["action"]["action_type"],
             state_fn(t["state_after"])))
    return dict(groups)


def compute_pmi_stats(triples):
    """Compute PMI statistics."""
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "N": 0, "unique_states": 0,
                "unique_actions": 0, "unique_sa_pairs": 0}

    state_counts = collections.Counter()
    state_action_counts = collections.Counter()
    state_next_counts = collections.Counter()
    triple_counts = collections.Counter()

    for s, a, s_next in triples:
        state_counts[s] += 1
        state_action_counts[(s, a)] += 1
        state_next_counts[(s, s_next)] += 1
        triple_counts[(s, a, s_next)] += 1

    pmi_values = []
    for s, a, s_next in triples:
        count_s = state_counts[s]
        count_sa = state_action_counts[(s, a)]
        count_ss_next = state_next_counts[(s, s_next)]
        count_sas_next = triple_counts[(s, a, s_next)]

        distinct_actions_s = sum(1 for (si, ai) in state_action_counts if si == s)
        distinct_next_s = sum(1 for (si, sni) in state_next_counts if si == s)

        p_a_given_s = (count_sa + ALPHA) / (count_s + ALPHA * distinct_actions_s)
        p_s_next_given_s = (count_ss_next + ALPHA) / (count_s + ALPHA * distinct_next_s)
        p_joint_given_s = count_sas_next / count_s

        denom = p_a_given_s * p_s_next_given_s
        if denom > 0 and p_joint_given_s > 0:
            pmi = math.log2(p_joint_given_s / denom)
        else:
            pmi = 0.0
        pmi_values.append(pmi)

    return {"mean_pmi": sum(pmi_values) / len(pmi_values), "N": N,
            "unique_states": len(state_counts),
            "unique_actions": len(set(a for _, a, _ in triples)),
            "unique_sa_pairs": len(state_action_counts)}


# ─── Cross-Trajectory Permutation ────────────────────────────────────────────

def cross_trajectory_shuffle(triple_groups, rng):
    """Shuffle action labels across trajectories."""
    tids = sorted(triple_groups.keys())
    if not tids:
        return {}
    
    max_len = max(len(triple_groups[tid]) for tid in tids)
    
    shuffled_groups = {tid: [] for tid in tids}
    
    for j in range(max_len):
        actions_at_j = []
        tids_with_j = []
        for tid in tids:
            if j < len(triple_groups[tid]):
                triple = triple_groups[tid][j]
                actions_at_j.append(triple[1])
                tids_with_j.append(tid)
        
        rng.shuffle(actions_at_j)
        
        for idx, tid in enumerate(tids_with_j):
            triple = triple_groups[tid][j]
            shuffled_groups[tid].append((triple[0], actions_at_j[idx], triple[2]))
    
    return shuffled_groups


def permutation_test(triple_groups, observed_mean_pmi, n_permutations, seed):
    """Cross-trajectory permutation test."""
    rng = random.Random(seed)
    shuffled_means = []
    
    for _ in range(n_permutations):
        shuffled_groups = cross_trajectory_shuffle(triple_groups, rng)
        all_shuffled = []
        for triples in shuffled_groups.values():
            all_shuffled.extend(triples)
        stats = compute_pmi_stats(all_shuffled)
        shuffled_means.append(stats["mean_pmi"])

    count_gt = sum(1 for m in shuffled_means if m > observed_mean_pmi)
    p_value = (count_gt + 1) / (n_permutations + 1)
    null_mean = float(np.mean(shuffled_means))
    null_std = float(np.std(shuffled_means))
    effect_d = float((observed_mean_pmi - null_mean) / null_std) if null_std > 0 else 0.0

    return {"p_value": p_value, "shuffled_means": shuffled_means,
            "observed_mean_pmi": observed_mean_pmi, "null_mean": null_mean,
            "null_std": null_std, "effect_size_d": effect_d}


# ─── Synthetic SPA (Positive Control with DOM Features) ──────────────────────

SYNTHETIC_STATES = {
    0: {"url": "http://spa.test/step1", "title": "Step 1",
        "dom_features": {"element_count": 15, "tree_depth": 3, "interactive_density": 0.20,
                         "form_count": 1, "input_count": 2, "button_count": 1}},
    1: {"url": "http://spa.test/step2", "title": "Step 2",
        "dom_features": {"element_count": 22, "tree_depth": 4, "interactive_density": 0.18,
                         "form_count": 1, "input_count": 3, "button_count": 2}},
    2: {"url": "http://spa.test/step3", "title": "Step 3",
        "dom_features": {"element_count": 30, "tree_depth": 5, "interactive_density": 0.17,
                         "form_count": 2, "input_count": 4, "button_count": 2}},
    3: {"url": "http://spa.test/step4", "title": "Step 4",
        "dom_features": {"element_count": 38, "tree_depth": 5, "interactive_density": 0.16,
                         "form_count": 2, "input_count": 5, "button_count": 3}},
    4: {"url": "http://spa.test/review", "title": "Review",
        "dom_features": {"element_count": 42, "tree_depth": 6, "interactive_density": 0.14,
                         "form_count": 1, "input_count": 3, "button_count": 4}},
    5: {"url": "http://spa.test/confirm", "title": "Confirm",
        "dom_features": {"element_count": 35, "tree_depth": 5, "interactive_density": 0.17,
                         "form_count": 1, "input_count": 2, "button_count": 3}},
    6: {"url": "http://spa.test/done", "title": "Done",
        "dom_features": {"element_count": 20, "tree_depth": 3, "interactive_density": 0.15,
                         "form_count": 0, "input_count": 1, "button_count": 2}},
    7: {"url": "http://spa.test/error", "title": "Error",
        "dom_features": {"element_count": 12, "tree_depth": 2, "interactive_density": 0.25,
                         "form_count": 0, "input_count": 0, "button_count": 2}},
}

SYNTHETIC_ACTIONS = ["form_submit", "button_click", "link_nav", "menu_select"]
SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 1, "button_click": 2, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 2, "button_click": 3, "link_nav": 6, "menu_select": 7},
    2: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    3: {"form_submit": 4, "button_click": 5, "link_nav": 6, "menu_select": 7},
    4: {"form_submit": 5, "button_click": 5, "link_nav": 6, "menu_select": 7},
    5: {"form_submit": 6, "button_click": 6, "link_nav": 0, "menu_select": 0},
    6: {"form_submit": 0, "button_click": 0, "link_nav": 0, "menu_select": 0},
    7: {"form_submit": 0, "button_click": 0, "link_nav": 0, "menu_select": 0},
}


def generate_synthetic_trajectories(n_trajectories, trajectory_length, rng):
    """Generate synthetic SPA trajectories with DOM features."""
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []
    for traj_id in range(n_trajectories):
        current_state = rng.choice(state_ids)
        for step in range(trajectory_length):
            action = rng.choice(SYNTHETIC_ACTIONS)
            next_state = SYNTHETIC_TRANSITIONS[current_state][action]
            all_transitions.append({
                "trajectory_id": traj_id, "step": step,
                "state_before": {"url": SYNTHETIC_STATES[current_state]["url"],
                                 "title": SYNTHETIC_STATES[current_state]["title"],
                                 "dom_features": dict(SYNTHETIC_STATES[current_state]["dom_features"])},
                "action": {"action_type": action, "target_href": f"http://dummy/{action}"},
                "state_after": {"url": SYNTHETIC_STATES[next_state]["url"],
                                "title": SYNTHETIC_STATES[next_state]["title"],
                                "dom_features": dict(SYNTHETIC_STATES[next_state]["dom_features"])},
            })
            current_state = next_state
    return all_transitions


def run_positive_control(rng):
    """Run synthetic SPA positive control with DOM features."""
    print("\n[CONTROL] Running positive control...")
    synthetic_transitions = generate_synthetic_trajectories(25, 20, rng)
    
    dom_state_fn, disc_info = make_dom_state_fn(synthetic_transitions, 5)
    
    reps = {"url_only": state_url_only, "url_title": state_url_title, "dom_features": dom_state_fn}
    pmi_results = {}
    for name, fn in reps.items():
        triples = extract_triples(synthetic_transitions, fn)
        pmi_results[name] = compute_pmi_stats(triples)
    
    dom_groups = extract_trajectory_groups(synthetic_transitions, dom_state_fn)
    dom_perm = permutation_test(dom_groups, pmi_results["dom_features"]["mean_pmi"], N_PERMUTATIONS, SEED)
    
    passes = pmi_results["dom_features"]["mean_pmi"] >= 0.5 and dom_perm["p_value"] < 0.001
    
    print(f"  URL-only PMI: {pmi_results['url_only']['mean_pmi']:.4f}")
    print(f"  DOM PMI: {pmi_results['dom_features']['mean_pmi']:.4f}, p={dom_perm['p_value']:.4f}")
    print(f"  Positive control passes: {passes}")
    
    return {"url_only_pmi": pmi_results["url_only"]["mean_pmi"],
            "dom_pmi": pmi_results["dom_features"]["mean_pmi"],
            "dom_perm_p": dom_perm["p_value"], "passes": passes,
            "discretization": disc_info}


def run_null_control(rng):
    """Run null control: shuffled synthetic SPA."""
    print("\n[CONTROL] Running null control...")
    synthetic_transitions = generate_synthetic_trajectories(25, 20, rng)
    
    # Shuffle actions
    rng_null = random.Random(SEED + 1000)
    trajectories_by_id = collections.defaultdict(list)
    for t in synthetic_transitions:
        trajectories_by_id[t["trajectory_id"]].append(t)
    
    all_actions = [t["action"]["action_type"] for t in synthetic_transitions]
    rng_null.shuffle(all_actions)
    
    null_transitions = []
    idx = 0
    for tid in sorted(trajectories_by_id.keys()):
        for t in trajectories_by_id[tid]:
            new_t = dict(t)
            new_t["action"] = dict(t["action"])
            new_t["action"]["action_type"] = all_actions[idx]
            null_transitions.append(new_t)
            idx += 1
    
    dom_state_fn, _ = make_dom_state_fn(null_transitions, 5)
    triples = extract_triples(null_transitions, dom_state_fn)
    stats = compute_pmi_stats(triples)
    
    groups = extract_trajectory_groups(null_transitions, dom_state_fn)
    perm = permutation_test(groups, stats["mean_pmi"], N_PERMUTATIONS, SEED)
    
    passes = perm["p_value"] > 0.05
    
    print(f"  Null DOM PMI: {stats['mean_pmi']:.4f}, p={perm['p_value']:.4f}")
    print(f"  Null control passes: {passes}")
    
    return {"null_dom_pmi": stats["mean_pmi"], "null_perm_p": perm["p_value"],
            "passes": passes}


def alpha_sensitivity(non_leakage, dom_state_fn):
    """Compute PMI at different alpha values."""
    triples = extract_triples(non_leakage, dom_state_fn)
    results = {}
    for alpha in [0.0, 0.5, 1.0, 2.0]:
        # Modified PMI computation with different alpha
        N = len(triples)
        if N == 0:
            results[f"alpha_{alpha}"] = 0.0
            continue
        state_counts = collections.Counter()
        sa_counts = collections.Counter()
        ss_counts = collections.Counter()
        triple_counts = collections.Counter()
        for s, a, s_next in triples:
            state_counts[s] += 1; sa_counts[(s, a)] += 1
            ss_counts[(s, s_next)] += 1; triple_counts[(s, a, s_next)] += 1
        pmi_vals = []
        for s, a, s_next in triples:
            cs = state_counts[s]; csa = sa_counts[(s, a)]
            css = ss_counts[(s, s_next)]; csas = triple_counts[(s, a, s_next)]
            da = sum(1 for (si, ai) in sa_counts if si == s)
            dns = sum(1 for (si, sni) in ss_counts if si == s)
            p_a = (csa + alpha) / (cs + alpha * da)
            p_sn = (css + alpha) / (cs + alpha * dns)
            p_joint = csas / cs
            denom = p_a * p_sn
            pmi_vals.append(math.log2(p_joint / denom) if denom > 0 and p_joint > 0 else 0.0)
        results[f"alpha_{alpha}"] = sum(pmi_vals) / len(pmi_vals)
    return results


def compute_entropy_rates(non_leakage, state_fn):
    """Compute entropy rates H(S'|S), H(S'|S,A)."""
    triples = extract_triples(non_leakage, state_fn)
    state_counts = collections.Counter()
    ss_counts = collections.Counter()
    sa_counts = collections.Counter()
    sas_counts = collections.Counter()
    for s, a, s_next in triples:
        state_counts[s] += 1; ss_counts[(s, s_next)] += 1
        sa_counts[(s, a)] += 1; sas_counts[(s, a, s_next)] += 1
    
    h_ss = 0.0
    for (s, sn), c in ss_counts.items():
        p = c / state_counts[s]
        if p > 0: h_ss -= p * math.log2(p)
    
    h_sas = 0.0
    for (s, a, sn), c in sas_counts.items():
        p = c / sa_counts[(s, a)]
        if p > 0: h_sas -= p * math.log2(p)
    
    return {"H_S_prime_given_S": h_ss, "H_S_prime_given_SA": h_sas,
            "entropy_reduction": h_ss - h_sas}


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full DOM-features experiment."""
    from playwright.sync_api import sync_playwright
    
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — DOM Structural Features PMI")
    print("=" * 70)
    
    rng = random.Random(SEED)
    os.environ["PYTHONHASHSEED"] = "0"
    
    # ── Step 1: Positive control ──
    positive_control = run_positive_control(rng)
    if not positive_control["passes"]:
        print("\nFATAL: Positive control failed.")
        return None
    
    # ── Step 2: Null control ──
    null_control = run_null_control(rng)
    
    # ── Step 3: Browser data collection ──
    print("\n[DATA] Collecting browser transitions...")
    site_results = {}
    
    with sync_playwright() as p:
        for site_key, site_config in SITES.items():
            print(f"\n  Site: {site_config['name']}")
            
            # Fresh browser for each site to avoid resource exhaustion
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0"
            )
            page = context.new_page()
            
            try:
                raw_transitions = collect_browser_transitions(
                    page, site_config, N_TRAJECTORIES, TRAJECTORY_LENGTH, rng)
                
                print(f"  Raw: {len(raw_transitions)} transitions")
                
                non_leakage, n_leakage = classify_non_leakage(raw_transitions)
                print(f"  Non-leakage: {len(non_leakage)}, Leakage: {n_leakage}")
                
                data_sufficient = len(non_leakage) >= 30
                
                if not data_sufficient:
                    print(f"  WARNING: < 30 non-leakage transitions")
                    site_results[site_key] = {
                        "name": site_config["name"], "n_raw": len(raw_transitions),
                        "n_non_leakage": len(non_leakage), "data_sufficient": False,
                    }
                    continue
                
                # Discretize DOM features
                dom_state_fn, disc_info = make_dom_state_fn(non_leakage, 5)
                
                reps = {"url_only": state_url_only, "url_title": state_url_title,
                        "dom_features": dom_state_fn}
                
                pmi_results = {}
                for name, fn in reps.items():
                    triples = extract_triples(non_leakage, fn)
                    pmi_results[name] = compute_pmi_stats(triples)
                    print(f"    {name}: PMI={pmi_results[name]['mean_pmi']:.4f}, "
                          f"states={pmi_results[name]['unique_states']}, "
                          f"SA={pmi_results[name]['unique_sa_pairs']}")
                
                # Permutation tests
                perm_tests = {}
                for name, fn in reps.items():
                    groups = extract_trajectory_groups(non_leakage, fn)
                    perm_tests[name] = permutation_test(
                        groups, pmi_results[name]["mean_pmi"], N_PERMUTATIONS, SEED)
                    print(f"    perm {name}: p={perm_tests[name]['p_value']:.4f}, "
                          f"d={perm_tests[name]['effect_size_d']:.2f}")
                
                # Alpha sensitivity
                alpha_res = alpha_sensitivity(non_leakage, dom_state_fn)
                
                # Entropy rates
                ent_url = compute_entropy_rates(non_leakage, state_url_only)
                ent_dom = compute_entropy_rates(non_leakage, dom_state_fn)
                
                # DOM vs URL comparison
                dom_improvement = pmi_results["dom_features"]["mean_pmi"] - pmi_results["url_only"]["mean_pmi"]
                
                site_results[site_key] = {
                    "name": site_config["name"], "entry_url": site_config["entry_url"],
                    "n_raw": len(raw_transitions), "n_non_leakage": len(non_leakage),
                    "n_leakage": n_leakage, "data_sufficient": data_sufficient,
                    "pmi": {k: {"mean_pmi": v["mean_pmi"], "N": v["N"],
                               "unique_states": v["unique_states"],
                               "unique_sa_pairs": v["unique_sa_pairs"]}
                           for k, v in pmi_results.items()},
                    "permutation": {k: {"p_value": v["p_value"], "null_mean": v["null_mean"],
                                       "effect_d": v["effect_size_d"]}
                                   for k, v in perm_tests.items()},
                    "dom_vs_url": {"improvement_bits": dom_improvement,
                                   "dom_pmi": pmi_results["dom_features"]["mean_pmi"],
                                   "url_pmi": pmi_results["url_only"]["mean_pmi"],
                                   "dom_better": dom_improvement > 0},
                    "alpha_sensitivity": alpha_res,
                    "entropy": {"url_only": ent_url, "dom_features": ent_dom},
                    "discretization": disc_info,
                }
                
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback; traceback.print_exc()
                site_results[site_key] = {"name": site_config["name"], "error": str(e),
                                          "n_non_leakage": 0, "data_sufficient": False}
            finally:
                context.close()
                browser.close()
    
    # ── Step 4: Decision evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION")
    print(f"{'=' * 70}")
    
    survives = True
    checks = {}
    valid_sites = [k for k, v in site_results.items() if v.get("data_sufficient", False)]
    total_sites = len(site_results)
    n_valid = len(valid_sites)
    
    # Check 1: Positive control
    checks["positive_control"] = {"passes": positive_control["passes"]}
    if not positive_control["passes"]: survives = False
    print(f"  Positive control: {positive_control['passes']}")
    
    # Check 2: Null control
    checks["null_control"] = {"passes": null_control["passes"]}
    if not null_control["passes"]: survives = False
    print(f"  Null control: {null_control['passes']}")
    
    # Check 3: Data sufficiency
    checks["data_sufficiency"] = {"valid": n_valid, "total": total_sites,
                                   "passes": n_valid >= max(2, math.ceil(2/3 * total_sites))}
    if n_valid < max(2, math.ceil(2/3 * total_sites)): survives = False
    print(f"  Data sufficiency: {n_valid}/{total_sites} valid")
    
    # Check 4: DOM > URL+0.1 on >= 2/3 valid sites
    dom_better_count = 0
    for sk in valid_sites:
        dvu = site_results[sk]["dom_vs_url"]
        better = dvu["dom_better"] and dvu["improvement_bits"] >= 0.1
        dom_better_count += int(better)
        checks[f"dom_vs_url_{sk}"] = {"improvement": dvu["improvement_bits"], "passes": better}
        print(f"  DOM vs URL {sk}: {dvu['improvement_bits']:.4f} bits, pass={better}")
    
    dom_better_pass = dom_better_count >= max(2, math.ceil(2/3 * n_valid)) if n_valid > 0 else False
    checks["dom_better_overall"] = {"count": dom_better_count, "passes": dom_better_pass}
    if not dom_better_pass: survives = False
    
    # Check 5: DOM PMI > 0 sig on >= 2/3 valid sites
    dom_sig_count = 0
    for sk in valid_sites:
        p_val = site_results[sk]["permutation"]["dom_features"]["p_value"]
        sig = p_val < ALPHA_BONFERRONI
        dom_sig_count += int(sig)
        checks[f"dom_sig_{sk}"] = {"p_value": p_val, "passes": sig}
        print(f"  DOM sig {sk}: p={p_val:.4f}, pass={sig}")
    
    dom_sig_pass = dom_sig_count >= max(2, math.ceil(2/3 * n_valid)) if n_valid > 0 else False
    checks["dom_sig_overall"] = {"count": dom_sig_count, "passes": dom_sig_pass}
    if not dom_sig_pass: survives = False
    
    # Determine outcome
    status = "COMPLETE"
    if survives:
        outcome = "SUPPORTS"
    elif n_valid < 2:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
    else:
        outcome = "FALSIFIES"
    
    print(f"\n  OUTCOME: {outcome}")
    print(f"  STATUS: {status}")
    
    return {"experiment_id": EXPERIMENT_ID, "positive_control": positive_control,
            "null_control": null_control, "site_results": site_results,
            "decision_checks": checks, "survives": survives,
            "outcome": outcome, "status": status}


if __name__ == "__main__":
    results = run_experiment()
    if results is None:
        print("Experiment failed."); sys.exit(1)
    
    out_dir = "research/experiments/EXP-PHYSICS-34524411213"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "raw_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_dir}/raw_results.json")
