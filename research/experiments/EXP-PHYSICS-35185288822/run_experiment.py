#!/usr/bin/env python3
"""
EXP-PHYSICS-35185288822 — EXECUTE: Title-aware conditional PMI on production sites.

Frozen inputs: request.json, spec.json, prereg.md, freeze.json
All computation deterministic (seed=42, PYTHONHASHSEED=0).

Pipeline:
1. Synthetic positive control (8-state SPA with unique deterministic titles)
2. Browser data collection from 3 production sites (Wikipedia, MDN, GitHub)
3. Non-leakage filtering and title variation check
4. BC PMI computation (title-aware and URL-only) with cross-trajectory permutation
5. Bonferroni correction (6 comparisons)
6. Title-shuffled negative control
7. Conditional entropy ceiling
8. Decision rule evaluation
"""

import json
import math
import random
import collections
import os
import sys
import time
import traceback
from urllib.parse import urlparse, urljoin
from datetime import datetime, timezone

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-35185288822"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing for PMI
BONFERRONI_COMPARISONS = 6  # 3 sites x 2 conditions (title-aware, URL-only)
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.00833

N_TRAJECTORIES = 15  # per site
TRAJECTORY_LENGTH = 10  # per trajectory
POLITE_DELAY = 1.5  # seconds between actions
STATE_CAPTURE_DELAY = 2.0  # seconds after action before state capture
MIN_NON_LEAKAGE = 50  # per site

EXPT_DIR = "research/experiments/EXP-PHYSICS-35185288822"

SITES = {
    "wikipedia": {
        "name": "Wikipedia",
        "entry_url": "https://en.wikipedia.org",
    },
    "mdn": {
        "name": "MDN Web Docs",
        "entry_url": "https://developer.mozilla.org",
    },
    "github": {
        "name": "GitHub",
        "entry_url": "https://github.com",
    },
}


# ─── Browser Data Collection ────────────────────────────────────────────────

def extract_browser_state(page):
    """Extract browser state: URL, title."""
    url = page.url
    title = page.title()[:100] if page.title() else ""
    return {"url": url, "title": title}


def find_available_actions(page, entry_url):
    """Find available same-domain interactive actions."""
    actions = []
    entry_domain = urlparse(entry_url).netloc

    # Links (same-domain only)
    try:
        links = page.query_selector_all("a[href]:visible")
        for link in links:
            try:
                href = link.get_attribute("href") or ""
                if not href or href.startswith("#") or href.startswith("javascript:"):
                    continue
                if not href.startswith("http"):
                    href = urljoin(page.url, href)
                parsed = urlparse(href)
                if parsed.netloc == entry_domain:
                    text = link.inner_text()[:30] if link.inner_text() else ""
                    if text and len(text.strip()) > 0:
                        actions.append({
                            "type": "link_nav",
                            "href": href,
                            "element": link,
                        })
            except:
                continue
    except:
        pass

    # Buttons
    try:
        buttons = page.query_selector_all("button:visible, [role=button]:visible")
        for btn in buttons:
            try:
                text = btn.inner_text()[:50] if btn.inner_text() else ""
                if btn.is_enabled() and text and len(text.strip()) > 0:
                    btn_id = btn.get_attribute("id") or ""
                    btn_class = btn.get_attribute("class") or ""
                    btn_href = f"button://{btn_class}/{btn_id}/{text[:20]}"
                    actions.append({
                        "type": "button_click",
                        "href": btn_href,
                        "element": btn,
                    })
            except:
                continue
    except:
        pass

    # Search inputs
    try:
        inputs = page.query_selector_all("input[type=search]:visible, input[name=q]:visible, input[name=search]:visible")
        for inp in inputs:
            try:
                inp_id = inp.get_attribute("id") or ""
                inp_name = inp.get_attribute("name") or ""
                inp_href = f"input://{inp_id}/{inp_name}"
                actions.append({
                    "type": "search_input",
                    "href": inp_href,
                    "element": inp,
                })
            except:
                continue
    except:
        pass

    return actions


def execute_action(page, action):
    """Execute an action on the page."""
    try:
        element = action["element"]
        if action["type"] in ("link_nav", "button_click"):
            element.click()
            return {"success": True}
        elif action["type"] == "search_input":
            element.fill("")
            element.type(f"test_{random.randint(0, 999)}")
            element.press("Enter")
            return {"success": True}
        return {"success": False}
    except Exception as e:
        return {"success": False, "error": str(e)}


def collect_site_transitions(page, site_config, n_trajectories, trajectory_length, rng):
    """Collect browser transitions from a single site."""
    transitions = []
    for traj_id in range(n_trajectories):
        try:
            page.goto(site_config["entry_url"], timeout=30000, wait_until="domcontentloaded")
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
                    "action": {
                        "action_type": action["type"],
                        "target_href": action["href"],
                    },
                    "state_after": state_after,
                })
                time.sleep(POLITE_DELAY)
        except Exception as e:
            print(f"    Trajectory {traj_id} failed: {e}")
            continue
    return transitions


# ─── State Representations ───────────────────────────────────────────────────

def state_url(state):
    return state["url"]

def state_url_title(state):
    return (state["url"], state["title"])


# ─── PMI Computation ─────────────────────────────────────────────────────────

def extract_triples(transitions, state_fn):
    """Extract (state, action, next_state) triples."""
    triples = []
    for t in transitions:
        s = state_fn(t["state_before"])
        a = t["action"]["action_type"]
        s_next = state_fn(t["state_after"])
        triples.append((s, a, s_next))
    return triples


def extract_trajectory_groups(transitions, state_fn):
    """Group transitions by trajectory_id."""
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(t)
    triple_groups = {}
    for tid, trans in groups.items():
        triple_groups[tid] = extract_triples(trans, state_fn)
    return triple_groups


def compute_pmi_stats(triples):
    """Compute mean PMI across triples using Laplace-smoothed conditional MI."""
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

    return {
        "mean_pmi": sum(pmi_values) / len(pmi_values),
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
    }


# ─── Cross-Trajectory Permutation (validated in parent experiments) ─────────

def cross_trajectory_shuffle(triple_groups, rng):
    """
    Shuffle entire action sequences across trajectories.
    This breaks action-outcome links while preserving trajectory structure.
    Validated in EXP-PHYSICS-34348438464 and parent experiments.
    """
    trajectories = []
    for tid in sorted(triple_groups.keys()):
        triples = triple_groups[tid]
        states = [t[0] for t in triples]
        actions = [t[1] for t in triples]
        nexts = [t[2] for t in triples]
        trajectories.append((tid, states, actions, nexts))

    action_sequences = [a for _, _, a, _ in trajectories]
    rng.shuffle(action_sequences)

    shuffled_groups = {}
    for i, (tid, states, _, nexts) in enumerate(trajectories):
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
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
    }


def compute_bc_pmi_with_permutation(transitions, state_fn, n_permutations, seed):
    """Compute bias-corrected PMI with cross-trajectory permutation test."""
    triples = extract_triples(transitions, state_fn)
    obs_stats = compute_pmi_stats(triples)
    obs_pmi = obs_stats["mean_pmi"]

    triple_groups = extract_trajectory_groups(transitions, state_fn)
    perm = permutation_test(triple_groups, obs_pmi, n_permutations, seed)

    bc_pmi = obs_pmi - perm["null_mean"]

    return {
        "bc_pmi": bc_pmi,
        "observed_pmi": obs_pmi,
        "perm_mean": perm["null_mean"],
        "perm_std": perm["null_std"],
        "p_value": perm["p_value"],
        "effect_size_d": perm["effect_size_d"],
        "N": obs_stats["N"],
        "unique_states": obs_stats["unique_states"],
        "unique_actions": obs_stats["unique_actions"],
        "unique_sa_pairs": obs_stats["unique_sa_pairs"],
    }


# ─── Conditional Entropy ─────────────────────────────────────────────────────

def compute_conditional_entropy(transitions, state_fn):
    """Compute H(S_next | S) using collected transitions."""
    triples = extract_triples(transitions, state_fn)
    if not triples:
        return 0.0

    state_counts = collections.Counter()
    state_next_counts = collections.Counter()

    for s, a, s_next in triples:
        state_counts[s] += 1
        state_next_counts[(s, s_next)] += 1

    entropy = 0.0
    total = len(triples)
    for s, count in state_counts.items():
        p_s = count / total
        for (si, s_next), cn in state_next_counts.items():
            if si == s and cn > 0:
                p_next_given_s = cn / count
                entropy -= p_s * p_next_given_s * math.log2(p_next_given_s)

    return entropy


# ─── Title-Shuffled Negative Control ─────────────────────────────────────────

def title_shuffled_pmi(transitions, state_fn, seed):
    """
    Compute PMI with title labels shuffled across all transitions.
    This destroys title-state associations while preserving other structure.
    """
    rng = random.Random(seed)
    shuffled_transitions = list(transitions)

    # Shuffle all title labels
    titles = [t["state_before"]["title"] for t in shuffled_transitions]
    rng.shuffle(titles)
    for i, t in enumerate(shuffled_transitions):
        shuffled_transitions[i] = {
            **t,
            "state_before": {**t["state_before"], "title": titles[i]},
        }

    triples = extract_triples(shuffled_transitions, state_fn)
    return compute_pmi_stats(triples)["mean_pmi"]


# ─── Synthetic Positive Control ──────────────────────────────────────────────

def run_positive_control(seed):
    """
    Positive control: 8-state linear SPA with unique deterministic titles.
    Each state has a unique URL AND unique title.
    Expected: title-aware BC PMI > 0.5 bits.
    """
    print("\n[CONTROL] Synthetic positive control (8-state SPA, unique titles)...")

    # 8 states with unique URLs AND unique titles
    states = {
        i: {"url": f"http://spa.test/state_{i}", "title": f"Page Title {i}"}
        for i in range(8)
    }

    actions = ["click_a", "click_b", "click_c", "click_d"]

    def next_state(s, a):
        action_idx = actions.index(a) + 1
        return (s + action_idx) % 8

    rng = random.Random(seed)
    all_transitions = []

    for traj_id in range(25):
        current_state = rng.choice(range(8))
        for step in range(20):
            action = rng.choice(actions)
            nxt = next_state(current_state, action)
            all_transitions.append({
                "trajectory_id": traj_id,
                "step": step,
                "state_before": {
                    "url": states[current_state]["url"],
                    "title": states[current_state]["title"],
                },
                "action": {
                    "action_type": action,
                    "target_href": f"http://spa.test/action_{action}_{current_state}_{step}",
                },
                "state_after": {
                    "url": states[nxt]["url"],
                    "title": states[nxt]["title"],
                },
            })
            current_state = nxt

    n_leakage = sum(1 for t in all_transitions
                    if t["action"]["target_href"] == t["state_after"]["url"])
    print(f"  Total transitions: {len(all_transitions)}, leakage: {n_leakage}")

    # Title-aware PMI
    bc_title = compute_bc_pmi_with_permutation(
        all_transitions, state_url_title, N_PERMUTATIONS, seed)

    # Determinism check: P(Title | FSM_state, step) = 1.0
    state_step_titles = collections.defaultdict(set)
    for t in all_transitions:
        key = (t["state_before"]["url"], t["step"])
        state_step_titles[key].add(t["state_before"]["title"])
    max_titles = max(len(v) for v in state_step_titles.values()) if state_step_titles else 0
    determinism_acc = 1.0 if max_titles <= 1 else 0.0

    passes = bc_title["bc_pmi"] > 0.5 and bc_title["perm_std"] > 0 and bc_title["p_value"] < ALPHA_BONFERRONI

    print(f"  Observed PMI: {bc_title['observed_pmi']:.6f} bits")
    print(f"  Perm mean: {bc_title['perm_mean']:.6f}, perm_std: {bc_title['perm_std']:.6f}")
    print(f"  BC PMI: {bc_title['bc_pmi']:.6f} bits")
    print(f"  p-value: {bc_title['p_value']:.6f}")
    print(f"  Determinism accuracy: {determinism_acc:.4f}")
    print(f"  Pass (BC_PMI > 0.5 AND perm_std > 0 AND p < {ALPHA_BONFERRONI:.6f}): {passes}")

    return {
        "bc_pmi": bc_title["bc_pmi"],
        "observed_pmi": bc_title["observed_pmi"],
        "perm_mean": bc_title["perm_mean"],
        "perm_std": bc_title["perm_std"],
        "p_value": bc_title["p_value"],
        "determinism_acc": determinism_acc,
        "passes": passes,
        "n_transitions": len(all_transitions),
    }


# ─── Non-Leakage Classification ─────────────────────────────────────────────

def classify_non_leakage(transitions):
    non_leakage = []
    leakage_count = 0
    for t in transitions:
        if t["action"]["target_href"] == t["state_after"]["url"]:
            leakage_count += 1
        else:
            non_leakage.append(t)
    return non_leakage, leakage_count


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    """Execute the full experiment pipeline."""
    from playwright.sync_api import sync_playwright

    print("=" * 70)
    print(f"EXPERIMENT {EXPERIMENT_ID} — Production Site Title-Aware PMI")
    print("=" * 70)

    rng = random.Random(SEED)
    os.environ["PYTHONHASHSEED"] = "0"

    # ── Step 1: Positive Control ──
    positive_control = run_positive_control(SEED)
    if not positive_control["passes"]:
        print("\nFATAL: Positive control failed.")
        return None

    # ── Step 2: Browser data collection ──
    print("\n[DATA] Collecting browser transitions from production sites...")
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
                raw_transitions = collect_site_transitions(
                    page, site_config, N_TRAJECTORIES, TRAJECTORY_LENGTH, rng)
                print(f"    Raw transitions: {len(raw_transitions)}")
            except Exception as e:
                print(f"    Collection ERROR: {e}")
                traceback.print_exc()
                raw_transitions = []
            finally:
                context.close()

            non_leakage, n_leakage = classify_non_leakage(raw_transitions)
            print(f"    Non-leakage: {len(non_leakage)}, Leakage: {n_leakage}")

            titles = [t["state_before"]["title"] for t in non_leakage]
            unique_titles = len(set(titles))
            print(f"    Unique titles: {unique_titles}/{len(titles)}")

            action_types = collections.Counter(t["action"]["action_type"] for t in non_leakage)
            print(f"    Action types: {dict(action_types)}")

            # ── BC PMI: title-aware and URL-only ──
            # Title-aware: I(S_next; (URL, Title) | A)
            bc_title_k3 = compute_bc_pmi_with_permutation(
                non_leakage, state_url_title, N_PERMUTATIONS, SEED)

            # URL-only: I(S_next; URL | A)
            bc_url_k3 = compute_bc_pmi_with_permutation(
                non_leakage, state_url, N_PERMUTATIONS, SEED)

            print(f"    Title-aware K=3: BC_PMI={bc_title_k3['bc_pmi']:.6f}, "
                  f"obs={bc_title_k3['observed_pmi']:.6f}, "
                  f"perm_mean={bc_title_k3['perm_mean']:.6f}, "
                  f"p={bc_title_k3['p_value']:.6f}, d={bc_title_k3['effect_size_d']:.4f}")
            print(f"    URL-only K=3: BC_PMI={bc_url_k3['bc_pmi']:.6f}, "
                  f"obs={bc_url_k3['observed_pmi']:.6f}, "
                  f"perm_mean={bc_url_k3['perm_mean']:.6f}, "
                  f"p={bc_url_k3['p_value']:.6f}, d={bc_url_k3['effect_size_d']:.4f}")

            # ── Conditional entropy ──
            h_entropy = compute_conditional_entropy(non_leakage, state_url)
            print(f"    H(S_next | URL) = {h_entropy:.6f} bits")

            # ── Title-shuffled negative control ──
            shuffled_pmi = title_shuffled_pmi(non_leakage, state_url_title, SEED)
            print(f"    Title-shuffled PMI: {shuffled_pmi:.6f}")

            # Save per-site transitions
            site_trans_path = os.path.join(EXPT_DIR, f"{site_key}_transitions.json")
            with open(site_trans_path, "w") as f:
                json.dump(raw_transitions, f, indent=2, default=str)

            site_results[site_key] = {
                "name": site_config["name"],
                "entry_url": site_config["entry_url"],
                "n_raw_transitions": len(raw_transitions),
                "n_non_leakage": len(non_leakage),
                "n_leakage": n_leakage,
                "unique_titles": unique_titles,
                "total_titles": len(titles),
                "title_aware_k3": bc_title_k3,
                "url_only_k3": bc_url_k3,
                "h_entropy": h_entropy,
                "shuffled_pmi": shuffled_pmi,
                "action_type_distribution": dict(action_types),
                "title_samples": list(set(titles))[:10],
            }

        browser.close()

    # ── Save raw data ──
    raw_path = os.path.join(EXPT_DIR, "raw_site_data.json")
    with open(raw_path, "w") as f:
        json.dump(site_results, f, indent=2, default=str)
    print(f"\nRaw site data saved to {raw_path}")

    # ── Step 3: Decision Rule Evaluation ──
    print(f"\n{'=' * 70}")
    print("DECISION RULE EVALUATION (frozen from spec.json)")
    print(f"{'=' * 70}")

    checks = {}

    # C1: URL-only BC PMI > 0.05 bits with Bonferroni p < 0.00833 on >= 2/3 sites
    url_only_pass_count = 0
    for sk, sr in site_results.items():
        bc = sr["url_only_k3"]
        passes = bc["bc_pmi"] > 0.05 and bc["p_value"] < ALPHA_BONFERRONI
        if passes:
            url_only_pass_count += 1
        print(f"  C1 URL-only {sk}: BC_PMI={bc['bc_pmi']:.6f}, p={bc['p_value']:.6f}, pass={passes}")
    checks["C1_url_only"] = {"sites_passing": url_only_pass_count, "passes": url_only_pass_count >= 2}
    print(f"  C1 result: {url_only_pass_count}/3 sites pass -> {'PASS' if checks['C1_url_only']['passes'] else 'FAIL'}")

    # C2: Title-aware BC PMI > 0.05 bits with Bonferroni p < 0.00833 on >= 2/3 sites
    title_pass_count = 0
    for sk, sr in site_results.items():
        bc = sr["title_aware_k3"]
        passes = bc["bc_pmi"] > 0.05 and bc["p_value"] < ALPHA_BONFERRONI
        if passes:
            title_pass_count += 1
        print(f"  C2 Title-aware {sk}: BC_PMI={bc['bc_pmi']:.6f}, p={bc['p_value']:.6f}, pass={passes}")
    checks["C2_title_aware"] = {"sites_passing": title_pass_count, "passes": title_pass_count >= 2}
    print(f"  C2 result: {title_pass_count}/3 sites pass -> {'PASS' if checks['C2_title_aware']['passes'] else 'FAIL'}")

    # C3: Title variation >= 2 unique titles per site on >= 2/3 sites
    title_var_count = sum(1 for sr in site_results.values() if sr["unique_titles"] >= 2)
    checks["C3_title_variation"] = {"sites_passing": title_var_count, "passes": title_var_count >= 2}
    print(f"  C3 Title variation: {title_var_count}/3 sites pass -> {'PASS' if checks['C3_title_variation']['passes'] else 'FAIL'}")

    # C4: Positive control BC PMI > 0.5 bits with p < 0.00833
    checks["C4_positive_control"] = {"passes": positive_control["passes"],
                                       "bc_pmi": positive_control["bc_pmi"],
                                       "p_value": positive_control["p_value"]}
    print(f"  C4 Positive control: BC_PMI={positive_control['bc_pmi']:.6f}, p={positive_control['p_value']:.6f}, "
          f"pass={positive_control['passes']}")

    # C5: Negative control (title-shuffled PMI < 0.05 bits)
    neg_ctrl_pass = all(abs(sr["shuffled_pmi"]) < 0.05 for sr in site_results.values())
    checks["C5_negative_control"] = {"passes": neg_ctrl_pass,
                                       "shuffled_pmis": {sk: sr["shuffled_pmi"] for sk, sr in site_results.items()}}
    print(f"  C5 Negative control: pass={neg_ctrl_pass}")

    # C6: Determinism check on positive control
    checks["C6_determinism"] = {"passes": positive_control["determinism_acc"] == 1.0,
                                 "accuracy": positive_control["determinism_acc"]}
    print(f"  C6 Determinism: acc={positive_control['determinism_acc']:.4f}, pass={checks['C6_determinism']['passes']}")

    # C7: >= 50 non-leakage transitions per site
    suff_count = sum(1 for sr in site_results.values() if sr["n_non_leakage"] >= MIN_NON_LEAKAGE)
    checks["C7_data_sufficiency"] = {"sites_passing": suff_count, "passes": suff_count >= 2}
    print(f"  C7 Data sufficiency: {suff_count}/3 sites pass -> {'PASS' if checks['C7_data_sufficiency']['passes'] else 'FAIL'}")

    # C8: H(S_next | URL) > 0.2 bits on >= 2/3 sites
    h_count = sum(1 for sr in site_results.values() if sr["h_entropy"] > 0.2)
    checks["C8_ceiling"] = {"sites_passing": h_count, "passes": h_count >= 2}
    print(f"  C8 Ceiling (H > 0.2): {h_count}/3 sites pass -> {'PASS' if checks['C8_ceiling']['passes'] else 'FAIL'}")

    # ── Determine outcome ──
    all_pass = all(c["passes"] for c in checks.values())

    if all_pass:
        decision = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif not checks["C4_positive_control"]["passes"] or not checks["C6_determinism"]["passes"]:
        decision = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif not checks["C7_data_sufficiency"]["passes"] or not checks["C3_title_variation"]["passes"]:
        decision = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif checks["C1_url_only"]["passes"] and not checks["C2_title_aware"]["passes"]:
        decision = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not checks["C1_url_only"]["passes"]:
        decision = "INCONCLUSIVE"
        outcome = "INCONCLUSIVE"
        status = "COMPLETE"
    else:
        decision = "FALSIFIED-IN-SETTING"
        outcome = "FALSIFIES"
        status = "COMPLETE"

    print(f"\n{'=' * 70}")
    print(f"DECISION: {decision}")
    print(f"OUTCOME: {outcome}")
    print(f"STATUS: {status}")
    print(f"{'=' * 70}")

    return {
        "positive_control": positive_control,
        "site_results": site_results,
        "checks": checks,
        "decision": decision,
        "outcome": outcome,
        "status": status,
    }


if __name__ == "__main__":
    results = run_experiment()
    if results is None:
        print("Experiment failed.")
        sys.exit(1)

    out_path = os.path.join(EXPT_DIR, "raw_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results saved to {out_path}")
