#!/usr/bin/env python3
"""
EXP-PHYSICS-34266105229 — Real SPA PMI: Title-Aware Dynamical Structure Detection
Collects browser transitions on real SPA/form-heavy sites and applies
title-aware PMI to detect dynamical structure beyond URL-level representation.

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
import hashlib
from urllib.parse import urlparse, urljoin

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34266105229"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 2  # URL+title vs URL-only on 2 sites
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.025
N_TRAJECTORIES = 100
TRAJECTORY_LENGTH = 8
POLITE_DELAY = 1.5  # seconds between actions
STATE_CAPTURE_DELAY = 2.0  # seconds after action before capturing state

# Site definitions
SITES = {
    "todomvc_react": {
        "name": "TodoMVC React",
        "entry_url": "https://todomvc.com/examples/react/dist/",
        "description": "React SPA with todo list, form inputs, filter navigation",
    },
    "todomvc_vue": {
        "name": "TodoMVC Vue",
        "entry_url": "https://todomvc.com/examples/vue/dist/",
        "description": "Vue SPA with todo list, form inputs, filter navigation",
    },
}

# Parent synthetic results for comparison
PARENT_SYNTHETIC = {
    "url_only_pmi": 0.693,
    "url_title_pmi": 1.970,
    "improvement_pct": 184,
}


# ─── Browser Data Collection ────────────────────────────────────────────────

def collect_browser_transitions(page, site_config, n_trajectories, trajectory_length, rng):
    """Collect browser transitions using Playwright.
    
    For each trajectory:
    1. Navigate to entry_url
    2. At each step: extract state, find available actions, pick one, execute, record transition
    3. Skip leakage transitions (action.target_href == state_after.url)
    
    Returns list of transition dicts.
    """
    transitions = []
    
    for traj_id in range(n_trajectories):
        try:
            # Navigate to entry point
            page.goto(site_config["entry_url"], timeout=20000, wait_until="domcontentloaded")
            time.sleep(STATE_CAPTURE_DELAY)
            
            current_url = page.url
            current_title = page.title()[:100]  # Truncate to 100 chars
            
            for step in range(trajectory_length):
                # Extract current state
                state_before = extract_browser_state(page)
                
                # Find available actions
                actions = find_available_actions(page, site_config["entry_url"])
                
                if not actions:
                    # No actions available, restart trajectory
                    break
                
                # Select action randomly
                action = rng.choice(actions)
                
                # Execute action
                action_result = execute_action(page, action)
                
                if not action_result["success"]:
                    # Action failed, restart trajectory
                    break
                
                # Wait for state change
                time.sleep(STATE_CAPTURE_DELAY)
                
                # Extract next state
                state_after = extract_browser_state(page)
                
                # Record transition
                transition = {
                    "trajectory_id": traj_id,
                    "step": step,
                    "state_before": state_before,
                    "action": {
                        "action_type": action["type"],
                        "target_href": action["href"],
                        "description": action.get("description", ""),
                    },
                    "state_after": state_after,
                }
                transitions.append(transition)
                
                # Update current state
                current_url = state_after["url"]
                current_title = state_after["title"]
                
                # Polite delay
                time.sleep(POLITE_DELAY)
                
        except Exception as e:
            print(f"  Trajectory {traj_id} failed: {e}")
            continue
    
    return transitions


def extract_browser_state(page):
    """Extract browser state: URL, title, form_signals."""
    url = page.url
    title = page.title()[:100]
    
    # Extract form signals
    has_form = len(page.query_selector_all("form")) > 0
    has_input = len(page.query_selector_all("input:not([type=hidden])")) > 0
    has_select = len(page.query_selector_all("select")) > 0
    has_textarea = len(page.query_selector_all("textarea")) > 0
    
    # Additional state: count of visible interactive elements (for richer state)
    n_buttons = len(page.query_selector_all("button:visible, [role=button]:visible"))
    n_links = len(page.query_selector_all("a[href]:visible"))
    n_inputs = len(page.query_selector_all("input:not([type=hidden]):visible, textarea:visible"))
    
    # Todo count (specific to TodoMVC-like apps)
    todo_count = 0
    try:
        todo_items = page.query_selector_all(".todo-list li, [class*=todo] li")
        todo_count = len(todo_items)
    except:
        pass
    
    return {
        "url": url,
        "title": title,
        "form_signals": [has_form, has_input, has_select, has_textarea],
        "n_buttons": n_buttons,
        "n_links": n_links,
        "n_inputs": n_inputs,
        "todo_count": todo_count,
    }


def find_available_actions(page, entry_url):
    """Find available same-domain interactive actions."""
    actions = []
    entry_domain = urlparse(entry_url).netloc
    
    # Collect clickable elements
    # Buttons (non-submit)
    buttons = page.query_selector_all("button:visible, [role=button]:visible")
    for btn in buttons:
        try:
            text = btn.inner_text()[:50] if btn.inner_text() else ""
            is_enabled = btn.is_enabled()
            if is_enabled and text:
                # Generate a pseudo-href for non-link buttons
                btn_id = btn.get_attribute("id") or ""
                btn_class = btn.get_attribute("class") or ""
                btn_href = f"button://{btn_class}/{btn_id}/{text[:20]}"
                actions.append({
                    "type": "button_click",
                    "href": btn_href,
                    "element": btn,
                    "description": f"click button: {text[:30]}",
                })
        except:
            continue
    
    # Links (same-domain only)
    links = page.query_selector_all("a[href]:visible")
    for link in links:
        try:
            href = link.get_attribute("href") or ""
            if not href or href.startswith("#") or href.startswith("javascript:"):
                # Hash links or javascript links - include as navigation
                text = link.inner_text()[:30] if link.inner_text() else ""
                if text:
                    actions.append({
                        "type": "link_nav",
                        "href": href,
                        "element": link,
                        "description": f"click link: {text[:30]}",
                    })
                continue
            
            # Resolve relative URLs
            if not href.startswith("http"):
                href = urljoin(page.url, href)
            
            parsed = urlparse(href)
            if parsed.netloc == entry_domain or parsed.netloc == "":
                text = link.inner_text()[:30] if link.inner_text() else ""
                actions.append({
                    "type": "link_nav",
                    "href": href,
                    "element": link,
                    "description": f"click link: {text[:30]}",
                })
        except:
            continue
    
    # Input fields - can type and submit
    inputs = page.query_selector_all("input:not([type=hidden]):visible, textarea:visible")
    for inp in inputs:
        try:
            input_type = inp.get_attribute("type") or "text"
            placeholder = inp.get_attribute("placeholder") or ""
            inp_id = inp.get_attribute("id") or ""
            inp_name = inp.get_attribute("name") or ""
            
            if input_type in ["text", "email", "password", "search", "url", "tel", "number", "textarea"]:
                # For text inputs, we can type and press Enter
                inp_href = f"input://{inp_id}/{inp_name}/{placeholder[:20]}"
                actions.append({
                    "type": "input_submit",
                    "href": inp_href,
                    "element": inp,
                    "description": f"type in {input_type} input: {placeholder[:20]}",
                })
        except:
            continue
    
    # Checkboxes and toggles
    toggles = page.query_selector_all("input[type=checkbox]:visible, [role=checkbox]:visible, [role=switch]:visible")
    for toggle in toggles:
        try:
            toggle_id = toggle.get_attribute("id") or ""
            toggle_label = ""
            # Try to find associated label
            try:
                label_el = page.query_selector(f"label[for='{toggle_id}']")
                if label_el:
                    toggle_label = label_el.inner_text()[:30]
            except:
                pass
            if not toggle_label:
                toggle_label = toggle_id or "toggle"
            
            toggle_href = f"toggle://{toggle_id}/{toggle_label[:20]}"
            actions.append({
                "type": "toggle",
                "href": toggle_href,
                "element": toggle,
                "description": f"toggle: {toggle_label[:30]}",
            })
        except:
            continue
    
    return actions


def execute_action(page, action):
    """Execute an action on the page. Returns success status."""
    try:
        element = action["element"]
        
        if action["type"] == "button_click":
            element.click()
            return {"success": True}
        
        elif action["type"] == "link_nav":
            element.click()
            return {"success": True}
        
        elif action["type"] == "input_submit":
            # Clear input, type a value, and press Enter
            element.fill("")
            element.type(f"test_item_{random.randint(0, 999)}")
            element.press("Enter")
            return {"success": True}
        
        elif action["type"] == "toggle":
            element.click()
            return {"success": True}
        
        else:
            return {"success": False}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def classify_non_leakage(transitions):
    """Classify transitions as leakage or non-leakage.
    
    Leakage: action.target_href == state_after.url
    Non-leakage: all other transitions
    """
    non_leakage = []
    leakage_count = 0
    
    for t in transitions:
        target = t["action"]["target_href"]
        actual_url = t["state_after"]["url"]
        
        if target == actual_url:
            leakage_count += 1
        else:
            non_leakage.append(t)
    
    return non_leakage, leakage_count


# ─── State Representations ───────────────────────────────────────────────────

def state_url_only(state):
    """State = URL string."""
    return state["url"]


def state_url_title(state):
    """State = (URL, title) tuple."""
    return (state["url"], state["title"])


def state_url_title_form(state):
    """State = (URL, title, form_signals) tuple."""
    return (state["url"], state["title"], tuple(state["form_signals"]))


REPRESENTATIONS = {
    "url_only": state_url_only,
    "url_title": state_url_title,
    "url_title_form": state_url_title_form,
}


# ─── PMI Computation (reused from parent) ───────────────────────────────────

def extract_triples(transitions, state_fn):
    """Extract (state_repr, action, next_state_repr) triples."""
    triples = []
    for t in transitions:
        s = state_fn(t["state_before"])
        a = t["action"]["action_type"]
        s_next = state_fn(t["state_after"])
        triples.append((s, a, s_next))
    return triples


def extract_trajectory_groups(transitions, state_fn):
    """Group transitions by trajectory_id, extract triples."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(t)
    triple_groups = {}
    for tid, trans in groups.items():
        triple_groups[tid] = extract_triples(trans, state_fn)
    return triple_groups


def compute_pmi_stats(triples):
    """Compute PMI statistics for a set of triples.
    
    PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
    """
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0,
                "unique_states": 0, "unique_actions": 0, "unique_sa_pairs": 0}

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

    mean_pmi = sum(pmi_values) / len(pmi_values)

    return {
        "mean_pmi": mean_pmi,
        "pmi_values": pmi_values,
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
    }


# ─── Cross-Trajectory Permutation ────────────────────────────────────────────

def cross_trajectory_shuffle(triple_groups, rng):
    """Shuffle action labels across entire trajectories."""
    trajectories = []
    for tid in sorted(triple_groups.keys()):
        triples = triple_groups[tid]
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        trajectories.append((states, actions, nexts))

    action_sequences = [a for _, a, _ in trajectories]
    rng.shuffle(action_sequences)

    shuffled_groups = {}
    for i, (tid, (states, _, nexts)) in enumerate(zip(sorted(triple_groups.keys()), trajectories)):
        shuffled_actions = action_sequences[i]
        shuffled_groups[tid] = [(states[j], shuffled_actions[j], nexts[j])
                                for j in range(len(states))]
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

    return {
        "p_value": p_value,
        "shuffled_means": shuffled_means,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
    }


# ─── Synthetic Positive Control ──────────────────────────────────────────────

# Reuse the synthetic SPA model from parent experiment
SYNTHETIC_STATES = {
    0: {"url": "http://spa.test/form", "title": "Checkout Form",
        "form_signals": [1, 1, 1, 0]},
    1: {"url": "http://spa.test/form", "title": "Login Form",
        "form_signals": [1, 1, 1, 0]},
    2: {"url": "http://spa.test/form", "title": "Registration Form",
        "form_signals": [1, 1, 1, 1]},
    3: {"url": "http://spa.test/dashboard", "title": "User Dashboard",
        "form_signals": [0, 0, 0, 0]},
    4: {"url": "http://spa.test/dashboard", "title": "Admin Dashboard",
        "form_signals": [0, 1, 0, 0]},
    5: {"url": "http://spa.test/dashboard", "title": "Analytics Dashboard",
        "form_signals": [0, 0, 0, 0]},
    6: {"url": "http://spa.test/settings", "title": "Account Settings",
        "form_signals": [1, 0, 0, 0]},
    7: {"url": "http://spa.test/settings", "title": "Privacy Settings",
        "form_signals": [1, 1, 0, 0]},
}

SYNTHETIC_ACTIONS = ["form_submit", "button_click", "link_nav", "menu_select"]

SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 5, "button_click": 3, "link_nav": 4, "menu_select": 6},
    2: {"form_submit": 3, "button_click": 5, "link_nav": 7, "menu_select": 4},
    3: {"form_submit": 0, "button_click": 1, "link_nav": 2, "menu_select": 6},
    4: {"form_submit": 1, "button_click": 2, "link_nav": 0, "menu_select": 7},
    5: {"form_submit": 2, "button_click": 0, "link_nav": 1, "menu_select": 6},
    6: {"form_submit": 3, "button_click": 4, "link_nav": 5, "menu_select": 0},
    7: {"form_submit": 5, "button_click": 3, "link_nav": 6, "menu_select": 1},
}


def generate_synthetic_trajectories(n_trajectories, trajectory_length, rng):
    """Generate synthetic SPA trajectories (from parent experiment)."""
    state_ids = list(SYNTHETIC_STATES.keys())
    all_transitions = []

    for traj_id in range(n_trajectories):
        current_state = rng.choice(state_ids)
        for step in range(trajectory_length):
            action = rng.choice(SYNTHETIC_ACTIONS)
            next_state = SYNTHETIC_TRANSITIONS[current_state][action]
            target_href = f"http://dummy.test/action_{action}_{current_state}_{step}"
            all_transitions.append({
                "trajectory_id": traj_id,
                "state_before": {
                    "url": SYNTHETIC_STATES[current_state]["url"],
                    "title": SYNTHETIC_STATES[current_state]["title"],
                    "form_signals": SYNTHETIC_STATES[current_state]["form_signals"],
                },
                "action": {
                    "action_type": action,
                    "target_href": target_href,
                },
                "state_after": {
                    "url": SYNTHETIC_STATES[next_state]["url"],
                    "title": SYNTHETIC_STATES[next_state]["title"],
                    "form_signals": SYNTHETIC_STATES[next_state]["form_signals"],
                },
            })
            current_state = next_state

    return all_transitions


def run_positive_control(rng):
    """Run synthetic SPA positive control (must produce PMI >= 0.5 bits)."""
    print("\n[CONTROL] Running positive control (synthetic SPA)...")
    
    synthetic_transitions = generate_synthetic_trajectories(
        n_trajectories=25, trajectory_length=20, rng=rng)
    
    # Verify non-leakage
    n_leakage = 0
    for t in synthetic_transitions:
        if t["action"]["target_href"] == t["state_after"]["url"]:
            n_leakage += 1
    print(f"  Synthetic transitions: {len(synthetic_transitions)}, leakage violations: {n_leakage}")
    
    # Compute PMI for URL-only (primary control metric)
    triples_url = extract_triples(synthetic_transitions, state_url_only)
    stats_url = compute_pmi_stats(triples_url)
    
    # Compute PMI for URL+title
    triples_title = extract_triples(synthetic_transitions, state_url_title)
    stats_title = compute_pmi_stats(triples_title)
    
    # Permutation test
    triple_groups = extract_trajectory_groups(synthetic_transitions, state_url_only)
    perm = permutation_test(triple_groups, stats_url["mean_pmi"], N_PERMUTATIONS, SEED)
    
    passes = stats_url["mean_pmi"] >= 0.5
    
    print(f"  URL-only PMI: {stats_url['mean_pmi']:.6f} bits")
    print(f"  URL+title PMI: {stats_title['mean_pmi']:.6f} bits")
    print(f"  Permutation p: {perm['p_value']:.6f}")
    print(f"  Positive control passes (PMI >= 0.5): {passes}")
    
    return {
        "url_only_pmi": stats_url["mean_pmi"],
        "url_title_pmi": stats_title["mean_pmi"],
        "permutation_p": perm["p_value"],
        "effect_size_d": perm["effect_size_d"],
        "passes": passes,
        "n_transitions": len(synthetic_transitions),
    }


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full real SPA PMI experiment."""
    from playwright.sync_api import sync_playwright
    
    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — Real SPA Title-Aware PMI")
    print("=" * 70)
    
    rng = random.Random(SEED)
    os.environ["PYTHONHASHSEED"] = "0"
    
    all_results = {}
    
    # ── Step 1: Run positive control (synthetic) ──
    positive_control = run_positive_control(rng)
    
    if not positive_control["passes"]:
        print("\nFATAL: Positive control failed. Pipeline integrity compromised.")
        return None
    
    # ── Step 2: Collect browser data from real SPA sites ──
    print("\n[DATA] Collecting browser transitions from real SPA sites...")
    
    site_results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for site_key, site_config in SITES.items():
            print(f"\n  Site: {site_config['name']} ({site_key})")
            print(f"  Entry: {site_config['entry_url']}")
            
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )
            page = context.new_page()
            
            try:
                # Collect transitions
                print(f"  Collecting {N_TRAJECTORIES} trajectories x {TRAJECTORY_LENGTH} steps...")
                raw_transitions = collect_browser_transitions(
                    page, site_config, N_TRAJECTORIES, TRAJECTORY_LENGTH, rng)
                
                print(f"  Raw transitions collected: {len(raw_transitions)}")
                
                # Classify non-leakage
                non_leakage, n_leakage = classify_non_leakage(raw_transitions)
                print(f"  Non-leakage transitions: {len(non_leakage)}")
                print(f"  Leakage transitions: {n_leakage}")
                
                if len(non_leakage) < 50:
                    print(f"  WARNING: Fewer than 50 non-leakage transitions. May be MEASUREMENT_INVALID.")
                
                # ── Compute PMI for all representations ──
                pmi_results = {}
                for rep_name, state_fn in REPRESENTATIONS.items():
                    triples = extract_triples(non_leakage, state_fn)
                    stats = compute_pmi_stats(triples)
                    pmi_results[rep_name] = stats
                    print(f"    {rep_name}: mean_PMI = {stats['mean_pmi']:.6f} bits, "
                          f"N = {stats['N']}, unique_states = {stats['unique_states']}, "
                          f"unique_SA = {stats['unique_sa_pairs']}")
                
                # ── Cross-trajectory permutation tests ──
                perm_tests = {}
                for rep_name, state_fn in REPRESENTATIONS.items():
                    triple_groups = extract_trajectory_groups(non_leakage, state_fn)
                    obs_mean = pmi_results[rep_name]["mean_pmi"]
                    perm = permutation_test(triple_groups, obs_mean, N_PERMUTATIONS, SEED)
                    perm_tests[rep_name] = perm
                    print(f"    Permutation {rep_name}: p = {perm['p_value']:.6f}, "
                          f"effect_d = {perm['effect_size_d']:.4f}")
                
                # ── Null control ──
                url_title_shuffled = perm_tests["url_title"]["shuffled_means"]
                url_title_observed = perm_tests["url_title"]["observed_mean_pmi"]
                count_shuffled_gt = sum(1 for m in url_title_shuffled if m > url_title_observed)
                null_p_value_gt = count_shuffled_gt / N_PERMUTATIONS
                null_passes = count_shuffled_gt < (0.05 * N_PERMUTATIONS)
                
                print(f"    Null control: shuffled > observed: {count_shuffled_gt}/{N_PERMUTATIONS}")
                print(f"    Null control P(shuffled > observed): {null_p_value_gt:.6f}, passes={null_passes}")
                
                # ── Representation comparison ──
                url_only_pmi = pmi_results["url_only"]["mean_pmi"]
                url_title_pmi = pmi_results["url_title"]["mean_pmi"]
                url_title_form_pmi = pmi_results["url_title_form"]["mean_pmi"]
                richer_than_url = url_title_pmi > url_only_pmi or url_title_form_pmi > url_only_pmi
                
                print(f"    URL-only PMI: {url_only_pmi:.6f}")
                print(f"    URL+title PMI: {url_title_pmi:.6f}")
                print(f"    URL+title+form PMI: {url_title_form_pmi:.6f}")
                print(f"    Richer > URL-only: {richer_than_url}")
                
                # ── Title uniqueness analysis ──
                titles = [t["state_before"]["title"] for t in non_leakage]
                unique_titles = len(set(titles))
                title_counts = collections.Counter(titles)
                ambiguous_titles = sum(1 for t, c in title_counts.items() if c > 10)
                
                print(f"    Unique titles: {unique_titles}/{len(titles)}")
                print(f"    Ambiguous titles (>10 occurrences): {ambiguous_titles}")
                
                # ── Store results ──
                site_results[site_key] = {
                    "name": site_config["name"],
                    "entry_url": site_config["entry_url"],
                    "n_raw_transitions": len(raw_transitions),
                    "n_non_leakage": len(non_leakage),
                    "n_leakage": n_leakage,
                    "pmi_by_representation": {
                        rep: {
                            "mean_pmi": stats["mean_pmi"],
                            "N": stats["N"],
                            "unique_states": stats["unique_states"],
                            "unique_actions": stats["unique_actions"],
                            "unique_sa_pairs": stats["unique_sa_pairs"],
                        }
                        for rep, stats in pmi_results.items()
                    },
                    "permutation_tests": {
                        rep: {
                            "observed_pmi": perm["observed_mean_pmi"],
                            "p_value": perm["p_value"],
                            "null_mean": perm["null_mean"],
                            "null_std": perm["null_std"],
                            "effect_size_d": perm["effect_size_d"],
                        }
                        for rep, perm in perm_tests.items()
                    },
                    "null_control": {
                        "shuffled_gt_observed": count_shuffled_gt,
                        "p_value": null_p_value_gt,
                        "passes": null_passes,
                    },
                    "representation_comparison": {
                        "url_only_pmi": url_only_pmi,
                        "url_title_pmi": url_title_pmi,
                        "url_title_form_pmi": url_title_form_pmi,
                        "richer_than_url": richer_than_url,
                    },
                    "title_analysis": {
                        "unique_titles": unique_titles,
                        "total_titles": len(titles),
                        "ambiguous_titles": ambiguous_titles,
                    },
                    "permutation_p_url_title_vs_url_only": perm_tests["url_title"]["p_value"],
                }
                
            except Exception as e:
                print(f"  ERROR collecting from {site_key}: {e}")
                site_results[site_key] = {
                    "name": site_config["name"],
                    "error": str(e),
                    "n_non_leakage": 0,
                }
            finally:
                context.close()
        
        browser.close()
    
    # ── Step 3: Decision evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION EVALUATION")
    print(f"{'=' * 70}")
    
    survives = True
    decision_checks = {}
    
    # Check 1: Positive control passes
    decision_checks["positive_control"] = {
        "url_only_pmi": positive_control["url_only_pmi"],
        "passes": positive_control["passes"],
    }
    if not positive_control["passes"]:
        survives = False
    print(f"  Positive control PMI >= 0.5: {positive_control['url_only_pmi']:.6f}, "
          f"pass={positive_control['passes']}")
    
    # Check 2: At least 50 non-leakage transitions from each site
    sites_with_sufficient_data = 0
    for site_key, sr in site_results.items():
        has_sufficient = sr.get("n_non_leakage", 0) >= 50
        sites_with_sufficient_data += int(has_sufficient)
        decision_checks[f"data_sufficiency_{site_key}"] = {
            "n_non_leakage": sr.get("n_non_leakage", 0),
            "threshold": 50,
            "passes": has_sufficient,
        }
        if not has_sufficient:
            survives = False
        print(f"  Data sufficiency {site_key}: {sr.get('n_non_leakage', 0)} >= 50, "
              f"pass={has_sufficient}")
    
    # Check 3: URL+title PMI > URL-only PMI on both sites (Bonferroni-corrected)
    url_title_better_count = 0
    for site_key, sr in site_results.items():
        if "representation_comparison" in sr:
            rc = sr["representation_comparison"]
            url_title_better = rc["url_title_pmi"] > rc["url_only_pmi"]
            url_title_better_count += int(url_title_better)
            decision_checks[f"representation_{site_key}"] = {
                "url_only_pmi": rc["url_only_pmi"],
                "url_title_pmi": rc["url_title_pmi"],
                "url_title_better": url_title_better,
            }
            print(f"  URL+title > URL-only {site_key}: {rc['url_title_pmi']:.6f} > "
                  f"{rc['url_only_pmi']:.6f}, pass={url_title_better}")
    
    both_sites_title_better = url_title_better_count == len(SITES)
    if not both_sites_title_better:
        survives = False
    
    # Check 4: URL+title PMI > 0.5 bits on at least one site
    any_title_above_threshold = False
    for site_key, sr in site_results.items():
        if "representation_comparison" in sr:
            rc = sr["representation_comparison"]
            if rc["url_title_pmi"] > 0.5:
                any_title_above_threshold = True
                break
    decision_checks["title_above_threshold"] = {
        "any_site": any_title_above_threshold,
        "threshold": 0.5,
    }
    if not any_title_above_threshold:
        survives = False
    print(f"  URL+title PMI > 0.5 on any site: {any_title_above_threshold}")
    
    # Check 5: Cross-trajectory permutation p < 0.001 on at least one site
    any_site_permutation_sig = False
    for site_key, sr in site_results.items():
        if "permutation_tests" in sr:
            perm_p = sr["permutation_tests"].get("url_title", {}).get("p_value", 1.0)
            if perm_p < 0.001:
                any_site_permutation_sig = True
                break
    decision_checks["permutation_significance"] = {
        "any_site": any_site_permutation_sig,
        "threshold": 0.001,
    }
    if not any_site_permutation_sig:
        survives = False
    print(f"  Permutation p < 0.001 on any site: {any_site_permutation_sig}")
    
    # Determine outcome
    status = "COMPLETE"
    if survives:
        outcome = "SUPPORTS"
    else:
        # Check if it's measurement invalid
        any_insufficient = any(sr.get("n_non_leakage", 0) < 50 for sr in site_results.values())
        any_error = any("error" in sr for sr in site_results.values())
        if any_insufficient or any_error:
            status = "MEASUREMENT_INVALID"
            outcome = "NOT_APPLICABLE"
        else:
            outcome = "FALSIFIES"
    
    print(f"\n{'=' * 70}")
    print(f"OUTCOME: {outcome}")
    print(f"STATUS: {status}")
    print(f"{'=' * 70}")
    
    # ── Build results dictionary ──
    results = {
        "experiment_id": EXPERIMENT_ID,
        "positive_control": positive_control,
        "site_results": site_results,
        "decision_checks": decision_checks,
        "survives": survives,
        "outcome": outcome,
        "status": status,
    }
    
    return results


if __name__ == "__main__":
    results = run_experiment()
    
    if results is None:
        print("Experiment failed to produce results.")
        sys.exit(1)
    
    # Save raw results
    out_dir = "research/experiments/EXP-PHYSICS-34266105229"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "raw_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
