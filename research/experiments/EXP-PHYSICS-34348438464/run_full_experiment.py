#!/usr/bin/env python3
"""
Full experiment runner using subprocess to avoid Playwright timeout issues.
"""

import json
import subprocess
import sys
import os

WORK_DIR = "/home/runner/work/Spider/Spider"
EXP_DIR = "research/experiments/EXP-PHYSICS-34348438464"

def run_playwright_collection():
    """Run Playwright collection for both sites."""
    script = '''
import json
import time
import random
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urljoin

SEED = 42
rng = random.Random(SEED)
N_TRAJECTORIES = 20
TRAJECTORY_LENGTH = 8

SITES = {
    "github": {"name": "GitHub", "entry_url": "https://github.com"},
    "mdn": {"name": "MDN Web Docs", "entry_url": "https://developer.mozilla.org"},
}

all_results = {}

print("Starting Playwright collection...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for site_key, site_config in SITES.items():
        print(f"\\nCollecting from: {site_config['name']}")
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        
        transitions = []
        
        for traj_id in range(N_TRAJECTORIES):
            try:
                page.goto(site_config["entry_url"], timeout=15000, wait_until="domcontentloaded")
                time.sleep(1)
                
                for step in range(TRAJECTORY_LENGTH):
                    url = page.url
                    title = page.title()[:100]
                    
                    state_before = {
                        "url": url,
                        "title": title,
                        "form_signals": [
                            len(page.query_selector_all("form")) > 0,
                            len(page.query_selector_all("input:not([type=hidden])")) > 0,
                            len(page.query_selector_all("select")) > 0,
                            len(page.query_selector_all("textarea")) > 0,
                        ],
                    }
                    
                    links = page.query_selector_all("a[href]:visible")
                    actions = []
                    entry_domain = urlparse(site_config["entry_url"]).netloc
                    
                    for link in links:
                        try:
                            href = link.get_attribute("href") or ""
                            if href.startswith("#") or href.startswith("javascript:"):
                                continue
                            if not href.startswith("http"):
                                href = urljoin(url, href)
                            parsed = urlparse(href)
                            if parsed.netloc == entry_domain or parsed.netloc == "":
                                actions.append({"element": link, "href": href})
                        except:
                            continue
                    
                    if not actions:
                        break
                    
                    action = rng.choice(actions)
                    try:
                        action["element"].click()
                        time.sleep(1)
                        
                        state_after = {
                            "url": page.url,
                            "title": page.title()[:100],
                            "form_signals": [
                                len(page.query_selector_all("form")) > 0,
                                len(page.query_selector_all("input:not([type=hidden])")) > 0,
                                len(page.query_selector_all("select")) > 0,
                                len(page.query_selector_all("textarea")) > 0,
                            ],
                        }
                        
                        transitions.append({
                            "trajectory_id": traj_id,
                            "step": step,
                            "state_before": state_before,
                            "action": {"action_type": "link_nav", "target_href": action["href"]},
                            "state_after": state_after,
                        })
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  Action failed: {e}")
                        break
                
            except Exception as e:
                print(f"  Trajectory {traj_id} failed: {e}")
                continue
        
        context.close()
        
        # Classify non-leakage
        non_leakage = []
        leakage_count = 0
        for t in transitions:
            target = t["action"]["target_href"]
            actual_url = t["state_after"]["url"]
            if target == actual_url:
                leakage_count += 1
            else:
                non_leakage.append(t)
        
        titles = [t["state_before"]["title"] for t in non_leakage]
        unique_titles = len(set(titles))
        
        print(f"  Raw transitions: {len(transitions)}")
        print(f"  Non-leakage: {len(non_leakage)}")
        print(f"  Leakage: {leakage_count}")
        print(f"  Unique titles: {unique_titles}/{len(titles)}")
        
        all_results[site_key] = {
            "name": site_config["name"],
            "raw_transitions": transitions,
            "non_leakage": non_leakage,
            "n_leakage": leakage_count,
            "unique_titles": unique_titles,
        }
    
    browser.close()

# Save results
with open("research/experiments/EXP-PHYSICS-34348438464/all_browser_transitions.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)

print("\\nAll data saved to all_browser_transitions.json")
'''
    
    script_path = "/tmp/full_collection.py"
    with open(script_path, "w") as f:
        f.write(script)
    
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=WORK_DIR
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR (last 500 chars):")
        print(result.stderr[-500:])
    
    return result.returncode == 0


def run_analysis():
    """Run PMI analysis on collected data."""
    script = '''
import json
import math
import random
import collections
import numpy as np

ALPHA = 1.0
N_PERMUTATIONS = 100
SEED = 42

def state_url_only(state):
    return state["url"]

def state_url_title(state):
    return (state["url"], state["title"])

def state_url_title_form(state):
    return (state["url"], state["title"], tuple(state["form_signals"]))

REPRESENTATIONS = {
    "url_only": state_url_only,
    "url_title": state_url_title,
    "url_title_form": state_url_title_form,
}

def extract_triples(transitions, state_fn):
    triples = []
    for t in transitions:
        s = state_fn(t["state_before"])
        a = t["action"]["action_type"]
        s_next = state_fn(t["state_after"])
        triples.append((s, a, s_next))
    return triples

def compute_pmi_stats(triples):
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "N": 0, "unique_states": 0, "unique_sa_pairs": 0}

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
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
    }

def extract_trajectory_groups(transitions, state_fn):
    groups = collections.defaultdict(list)
    for t in transitions:
        groups[t["trajectory_id"]].append(t)
    triple_groups = {}
    for tid, trans in groups.items():
        triple_groups[tid] = extract_triples(trans, state_fn)
    return triple_groups

def cross_trajectory_shuffle(triple_groups, rng):
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

# Load data
with open("research/experiments/EXP-PHYSICS-34348438464/all_browser_transitions.json") as f:
    all_data = json.load(f)

site_results = {}

for site_key, site_data in all_data.items():
    print(f"\\nAnalyzing: {site_data['name']}")
    
    non_leakage = site_data["non_leakage"]
    print(f"  Non-leakage transitions: {len(non_leakage)}")
    
    if len(non_leakage) < 30:
        print(f"  WARNING: Less than 30 non-leakage transitions")
    
    # Compute PMI for all representations
    pmi_results = {}
    for rep_name, state_fn in REPRESENTATIONS.items():
        triples = extract_triples(non_leakage, state_fn)
        stats = compute_pmi_stats(triples)
        pmi_results[rep_name] = stats
        print(f"    {rep_name}: PMI = {stats['mean_pmi']:.6f} bits, N = {stats['N']}")
    
    # Permutation tests
    perm_tests = {}
    for rep_name, state_fn in REPRESENTATIONS.items():
        triple_groups = extract_trajectory_groups(non_leakage, state_fn)
        obs_mean = pmi_results[rep_name]["mean_pmi"]
        perm = permutation_test(triple_groups, obs_mean, N_PERMUTATIONS, SEED)
        perm_tests[rep_name] = perm
        print(f"    Permutation {rep_name}: p = {perm['p_value']:.6f}")
    
    # Null control
    url_title_shuffled = perm_tests["url_title"]["shuffled_means"]
    url_title_observed = perm_tests["url_title"]["observed_mean_pmi"]
    count_shuffled_gt = sum(1 for m in url_title_shuffled if m > url_title_observed)
    null_p_value_gt = count_shuffled_gt / N_PERMUTATIONS
    null_passes = count_shuffled_gt < (0.05 * N_PERMUTATIONS)
    
    # Representation comparison
    url_only_pmi = pmi_results["url_only"]["mean_pmi"]
    url_title_pmi = pmi_results["url_title"]["mean_pmi"]
    url_title_form_pmi = pmi_results["url_title_form"]["mean_pmi"]
    richer_than_url = url_title_pmi > url_only_pmi or url_title_form_pmi > url_only_pmi
    
    print(f"  URL-only PMI: {url_only_pmi:.6f}")
    print(f"  URL+title PMI: {url_title_pmi:.6f}")
    print(f"  URL+title+form PMI: {url_title_form_pmi:.6f}")
    print(f"  Richer > URL-only: {richer_than_url}")
    
    site_results[site_key] = {
        "name": site_data["name"],
        "n_non_leakage": len(non_leakage),
        "unique_titles": site_data["unique_titles"],
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
    }

# Save analysis results
with open("research/experiments/EXP-PHYSICS-34348438464/analysis_results.json", "w") as f:
    json.dump(site_results, f, indent=2, default=str)

print("\\nAnalysis results saved to analysis_results.json")
'''
    
    script_path = "/tmp/analysis.py"
    with open(script_path, "w") as f:
        f.write(script)
    
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=WORK_DIR
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR (last 500 chars):")
        print(result.stderr[-500:])
    
    return result.returncode == 0


if __name__ == "__main__":
    print("=" * 70)
    print("STEP 1: Collect browser transitions")
    print("=" * 70)
    
    if not run_playwright_collection():
        print("Collection failed!")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("STEP 2: Run PMI analysis")
    print("=" * 70)
    
    if not run_analysis():
        print("Analysis failed!")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)
