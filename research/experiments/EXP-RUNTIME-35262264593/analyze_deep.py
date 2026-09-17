#!/usr/bin/env python3
"""Deep analysis of double_br scenario and discrimination computation."""
import json
import hashlib
from collections import defaultdict

with open('raw_observations.json') as f:
    data = json.load(f)

# Focus on JSON_1KB
key = 'JSON_1KB'

print("=== DECOMPRESSION ANALYSIS ===\n")

for state in ['valid_token', 'no_auth', 'expired_token', 'invalid_token']:
    obs_list = data[key][state]
    by_scenario = defaultdict(list)
    for obs in obs_list:
        by_scenario[obs['encoding_scenario']].append(obs)
    
    print(f"State: {state}")
    for scenario in ['correct_br', 'missing_ce', 'incorrect_gzip', 'garbled_ce', 'double_br']:
        obs = by_scenario[scenario][0]
        print(f"  {scenario}: body_size={obs['body_size']}, "
              f"decomp_hash={obs['decompressed_hash'][:16]}..., "
              f"comp_hash={obs['body_hash_compressed'][:16]}...")
    print()

print("\n=== DISCRIMINATION MATH ===\n")

# Check why discrimination is 0.2911 instead of 0.5
# The issue is that double_br creates a different hash from all other scenarios
# With 5 scenarios per state, and double_br producing a unique hash:
# 4/5 requests share hash A (correct_br, missing_ce, incorrect_gzip, garbled_ce)
# 1/5 requests has hash B (double_br)
# This means intra-state similarity is higher than expected

# Let's compute manually for valid_token vs no_auth
valid_fps = [obs['fingerprint_decompressed'] for obs in data[key]['valid_token']]
noauth_fps = [obs['fingerprint_decompressed'] for obs in data[key]['no_auth']]

print(f"valid_token fingerprints: {len(set(valid_fps))} unique out of {len(valid_fps)}")
print(f"no_auth fingerprints: {len(set(noauth_fps))} unique out of {len(noauth_fps)}")
print(f"Overlap: {len(set(valid_fps) & set(noauth_fps))} fingerprints")

# Check what the fingerprints look like by scenario
for state_name, fps_list in [('valid_token', valid_fps), ('no_auth', noauth_fps)]:
    by_fp = defaultdict(int)
    for fp in fps_list:
        by_fp[fp] += 1
    print(f"\n{state_name} fingerprint distribution:")
    for fp, count in sorted(by_fp.items(), key=lambda x: -x[1]):
        print(f"  {fp[:16]}...: {count} times")

# Also check the hash differences between valid and no_auth for double_br
print("\n=== DOUBLE_BR HASH ANALYSIS ===")
for state in ['valid_token', 'no_auth']:
    obs = [o for o in data[key][state] if o['encoding_scenario'] == 'double_br'][0]
    print(f"{state} double_br:")
    print(f"  compressed_hash: {obs['body_hash_compressed']}")
    print(f"  decompressed_hash: {obs['decompressed_hash']}")
    print(f"  body_size: {obs['body_size']}")
    print(f"  content_encoding: {obs['content_encoding']}")
    print(f"  body_preview: {obs['body_preview'][:100]}...")
