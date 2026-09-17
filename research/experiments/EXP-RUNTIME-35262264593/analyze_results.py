#!/usr/bin/env python3
"""Diagnostic script to understand the determinism failure."""
import json
from collections import defaultdict

with open('raw_observations.json') as f:
    data = json.load(f)

# Check first condition
key = 'JSON_1KB'
state = 'valid_token'
obs_list = data[key][state]
print(f"Condition: {key}, State: {state}")
print(f"Total observations: {len(obs_list)}")

# Group by encoding scenario
by_scenario = defaultdict(list)
for obs in obs_list:
    scenario = obs['encoding_scenario']
    by_scenario[scenario].append(obs)

for scenario, scenario_obs in sorted(by_scenario.items()):
    hashes = [o['decompressed_hash'] for o in scenario_obs]
    unique_hashes = set(hashes)
    ce_values = [o['content_encoding'] for o in scenario_obs]
    print(f"\n  Scenario: {scenario}")
    print(f"    Content-Encoding headers: {set(ce_values)}")
    print(f"    Decompressed hashes: {unique_hashes}")
    print(f"    Unique count: {len(unique_hashes)}")
    for o in scenario_obs[:2]:
        print(f"    rep={o['rep']}: body_size={o['body_size']}, "
              f"decomp_err={o['decompression_error']}, "
              f"decomp_hash={o['decompressed_hash'][:16]}..., "
              f"body_preview={o['body_preview'][:80]}...")

# Now check cross-scenario: are the hashes the same or different?
print("\n\nCross-scenario hash comparison:")
all_hashes_by_scenario = {}
for scenario, scenario_obs in by_scenario.items():
    hashes = set(o['decompressed_hash'] for o in scenario_obs)
    all_hashes_by_scenario[scenario] = hashes
    print(f"  {scenario}: {hashes}")

# Are all scenarios producing the same hashes?
all_hashes = set()
for h in all_hashes_by_scenario.values():
    all_hashes.update(h)
print(f"\nTotal unique decompressed hashes across all scenarios: {len(all_hashes)}")
print(f"Hashes: {all_hashes}")

# Check if some scenarios produce the same hash as correct_br
correct_hashes = all_hashes_by_scenario.get('correct_br', set())
for scenario, hashes in all_hashes_by_scenario.items():
    overlap = hashes & correct_hashes
    print(f"  {scenario} overlap with correct_br: {len(overlap)} hashes")
