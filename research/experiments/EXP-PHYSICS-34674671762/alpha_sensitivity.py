#!/usr/bin/env python3
"""Alpha sensitivity analysis for network request PMI."""
import json
import math
import collections
from pathlib import Path

def compute_pmi_stats(triples, alpha):
    """Compute PMI statistics with specified alpha."""
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "N": 0}
    
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
        
        p_a_given_s = (count_sa + alpha) / (count_s + alpha * distinct_actions_s)
        p_s_next_given_s = (count_ss_next + alpha) / (count_s + alpha * distinct_next_s)
        p_joint_given_s = count_sas_next / count_s
        
        denom = p_a_given_s * p_s_next_given_s
        if denom > 0 and p_joint_given_s > 0:
            pmi = math.log2(p_joint_given_s / denom)
        else:
            pmi = 0.0
        pmi_values.append(pmi)
    
    return {"mean_pmi": sum(pmi_values) / len(pmi_values), "N": N}

# Load synthetic transitions
out_dir = Path("/home/runner/work/Spider/Spider/research/experiments/EXP-PHYSICS-34674671762")
transitions_path = out_dir / "synthetic_transitions_network_v2.json"
with open(transitions_path) as f:
    transitions = json.load(f)

# Build triples
net_triples = [(t["state_before"]["net_hash"], t["action"], t["state_after"]["net_hash"]) for t in transitions]
url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in transitions]

print("Alpha Sensitivity Analysis (Synthetic SPA)")
print("=" * 60)
print(f"{'Alpha':>8} {'Net PMI':>12} {'URL PMI':>12}")
print("-" * 60)

alphas = [0.0, 0.5, 1.0, 2.0]
results = {}
for alpha in alphas:
    net_stats = compute_pmi_stats(net_triples, alpha)
    url_stats = compute_pmi_stats(url_triples, alpha)
    results[alpha] = {
        "net_pmi": net_stats["mean_pmi"],
        "url_pmi": url_stats["mean_pmi"],
        "gain": net_stats["mean_pmi"] - url_stats["mean_pmi"]
    }
    print(f"{alpha:>8.1f} {net_stats['mean_pmi']:>12.6f} {url_stats['mean_pmi']:>12.6f}")

print("-" * 60)
print("\nGain (Net - URL) by alpha:")
for alpha in alphas:
    print(f"  alpha={alpha:.1f}: {results[alpha]['gain']:.6f} bits")

# Load real site results
real_results_path = out_dir / "real_site_results_network_v2.json"
with open(real_results_path) as f:
    real_results = json.load(f)

print("\n\nAlpha Sensitivity Analysis (Real Sites)")
print("=" * 60)

for site in real_results:
    if site.get("status") != "COMPLETE":
        continue
    print(f"\n{site['site_name']}:")
    site_transitions = site.get("raw_transitions", [])
    site_net_triples = [(t["state_before"]["net_hash"], t["action"], t["state_after"]["net_hash"]) for t in site_transitions]
    site_url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in site_transitions]
    
    print(f"  {'Alpha':>8} {'Net PMI':>12} {'URL PMI':>12} {'Gain':>12}")
    print(f"  {'-'*56}")
    for alpha in alphas:
        net_stats = compute_pmi_stats(site_net_triples, alpha)
        url_stats = compute_pmi_stats(site_url_triples, alpha)
        gain = net_stats["mean_pmi"] - url_stats["mean_pmi"]
        print(f"  {alpha:>8.1f} {net_stats['mean_pmi']:>12.6f} {url_stats['mean_pmi']:>12.6f} {gain:>12.6f}")

# Save results
alpha_results = {
    "synthetic_spa": results,
    "real_sites": {}
}
for site in real_results:
    if site.get("status") != "COMPLETE":
        continue
    site_transitions = site.get("raw_transitions", [])
    site_net_triples = [(t["state_before"]["net_hash"], t["action"], t["state_after"]["net_hash"]) for t in site_transitions]
    site_url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in site_transitions]
    
    site_alpha = {}
    for alpha in alphas:
        net_stats = compute_pmi_stats(site_net_triples, alpha)
        url_stats = compute_pmi_stats(site_url_triples, alpha)
        site_alpha[alpha] = {
            "net_pmi": net_stats["mean_pmi"],
            "url_pmi": url_stats["mean_pmi"],
            "gain": net_stats["mean_pmi"] - url_stats["mean_pmi"]
        }
    alpha_results["real_sites"][site["site_name"]] = site_alpha

alpha_path = out_dir / "alpha_sensitivity.json"
with open(alpha_path, "w") as f:
    json.dump(alpha_results, f, indent=2)
print(f"\nAlpha sensitivity results saved to {alpha_path}")
