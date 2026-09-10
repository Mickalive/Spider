#!/usr/bin/env python3
"""
EXP-RUNTIME-34439061845 — Analysis of raw observations from multi-endpoint Keycloak test
=======================================================================================
Reads raw_observations.json and computes all frozen metrics, controls, and
decision-rule evaluation. Produces result.json, report.md, and provenance.json.
"""

import hashlib
import json
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# CONSTANTS (frozen from spec.json / prereg.md)
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-RUNTIME-34439061845"
LANE = "runtime"
SEED = 44
REPS = 10
EXCLUDED_HEADERS = {"date", "server", "x-request-id"}

# ---------------------------------------------------------------------------
# FINGERPRINT (deterministic sorted-tuple, excluding Date/Server/X-Request-Id)
# ---------------------------------------------------------------------------

def fingerprint(status, headers, body_bytes, redirect_url=""):
    body_hash = hashlib.sha256(body_bytes).hexdigest()
    headers_filtered = {k: v for k, v in headers.items()
                        if k.lower() not in EXCLUDED_HEADERS}
    vector = (
        status,
        tuple(sorted(headers_filtered.items())),
        body_hash,
        redirect_url,
    )
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# JACCARD SIMILARITY (bitwise on hex fingerprint)
# ---------------------------------------------------------------------------

def hex_to_bits(hex_str):
    return [int(c, 16) >> i & 1 for c in hex_str for i in range(3, -1, -1)]


def jaccard_similarity(fp_a, fp_b):
    bits_a = hex_to_bits(fp_a)
    bits_b = hex_to_bits(fp_b)
    both = sum(a & b for a, b in zip(bits_a, bits_b))
    either = sum(a | b for a, b in zip(bits_a, bits_b))
    return both / either if either > 0 else 0.0


# ---------------------------------------------------------------------------
# DISCRIMINATION SCORE
# ---------------------------------------------------------------------------

def compute_discrimination_score(fingerprints_by_state):
    all_states = list(fingerprints_by_state.keys())
    intra_matches = 0
    intra_total = 0
    inter_matches = 0
    inter_total = 0

    for i, s1 in enumerate(all_states):
        fps1 = fingerprints_by_state[s1]
        for a in range(len(fps1)):
            for b in range(a + 1, len(fps1)):
                intra_total += 1
                if fps1[a] == fps1[b]:
                    intra_matches += 1
        for j, s2 in enumerate(all_states):
            if j <= i:
                continue
            fps2 = fingerprints_by_state[s2]
            for fa in fps1:
                for fb in fps2:
                    inter_total += 1
                    if fa == fb:
                        inter_matches += 1

    intra_match_rate = intra_matches / intra_total if intra_total > 0 else 0
    inter_match_rate = inter_matches / inter_total if inter_total > 0 else 0
    return intra_match_rate - inter_match_rate


# ---------------------------------------------------------------------------
# SINGLE-HEADER DISCRIMINATION
# ---------------------------------------------------------------------------

def compute_single_header_discrimination(fingerprints_by_state, header_key, raw_observations):
    header_fps_by_state = {}
    for state, obs_list in raw_observations.items():
        fps = []
        for obs in obs_list:
            val = obs["headers"].get(header_key, "")
            fp = hashlib.sha256(val.encode("utf-8")).hexdigest()
            fps.append(fp)
        header_fps_by_state[state] = fps
    return compute_discrimination_score(header_fps_by_state)


# ---------------------------------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------------------------------

def main():
    # Load raw observations
    with open("raw_observations.json", "r") as f:
        raw = json.load(f)

    print(f"Loaded raw observations for endpoints: {list(raw.keys())}")
    total = sum(len(v) for state_obs in raw.values() for v in state_obs.values())
    print(f"Total observations: {total}")

    endpoint_results = {}
    auth_states = ["no_auth", "valid_token", "expired_token", "invalid_token"]

    for ep_name, ep_obs in raw.items():
        print(f"\n{'='*60}")
        print(f"Analyzing endpoint: {ep_name}")
        print(f"{'='*60}")

        # Verify 4 states x 10 reps
        for state, obs_list in ep_obs.items():
            assert len(obs_list) == REPS, f"State {state} has {len(obs_list)} reps, expected {REPS}"

        # Compute fingerprints
        fps_by_state = {}
        body_hashes_by_state = {}
        for state, obs_list in ep_obs.items():
            fps = []
            body_hashes = []
            for obs in obs_list:
                fps.append(obs["fingerprint"])
                body_hashes.append(obs["body_hash"])
            fps_by_state[state] = fps
            body_hashes_by_state[state] = list(set(body_hashes))

        # Body identity: expired vs invalid
        expired_invalid_identical = (
            len(body_hashes_by_state.get("expired_token", [])) >= 1
            and len(body_hashes_by_state.get("invalid_token", [])) >= 1
            and body_hashes_by_state["expired_token"][0] == body_hashes_by_state["invalid_token"][0]
        )

        # Full vector discrimination
        disc_score = compute_discrimination_score(fps_by_state)

        # Baselines
        url = ep_obs["valid_token"][0]["url"]
        b_url_fps = [hashlib.sha256(url.encode()).hexdigest() for _ in range(REPS)]
        b_url_by_state = {s: b_url_fps for s in auth_states}
        b_url_disc = compute_discrimination_score(b_url_by_state)

        rng = random.Random(99)
        b_rand_fps = [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest()
                      for _ in range(REPS * len(auth_states))]
        b_rand_by_state = {}
        idx = 0
        for s in auth_states:
            b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
            idx += REPS
        b_rand_disc = compute_discrimination_score(b_rand_by_state)

        b_status_by_state = {}
        for state, obs_list in ep_obs.items():
            fps = [hashlib.sha256(str(obs["status"]).encode()).hexdigest() for obs in obs_list]
            b_status_by_state[state] = fps
        b_status_disc = compute_discrimination_score(b_status_by_state)

        b_body_by_state = {}
        for state, obs_list in ep_obs.items():
            fps = [obs["body_hash"] for obs in obs_list]
            b_body_by_state[state] = fps
        b_body_disc = compute_discrimination_score(b_body_by_state)

        # Single-header discrimination
        www_auth_disc = compute_single_header_discrimination(
            fps_by_state, "WWW-Authenticate", ep_obs
        )
        cc_disc = compute_single_header_discrimination(
            fps_by_state, "Cache-Control", ep_obs
        )

        # Null FP rate
        null_results = {}
        for state in auth_states:
            fps = fps_by_state[state]
            unique = len(set(fps))
            total_r = len(fps)
            fp_rate = (unique - 1) / (total_r - 1) if total_r > 1 else 0.0
            null_results[state] = {"total": total_r, "unique": unique, "fp_rate": fp_rate}

        total_pairs = sum(max(r["total"] * (r["total"] - 1) // 2, 0) for r in null_results.values())
        total_diff_pairs = sum(
            max((r["unique"] - 1) * r["total"] // 2, 0) for r in null_results.values()
        ) if total_pairs > 0 else 0
        overall_fp_rate = total_diff_pairs / total_pairs if total_pairs > 0 else 0

        # Drift
        expired_fps = fps_by_state["expired_token"]
        invalid_fps = fps_by_state["invalid_token"]
        drift_jaccards = [jaccard_similarity(f1, f2) for f1 in expired_fps for f2 in invalid_fps]
        mean_drift = sum(drift_jaccards) / len(drift_jaccards) if drift_jaccards else 0

        # WWW-Authenticate verification
        www_auth_verification = {}
        for state in auth_states:
            obs_list = ep_obs[state]
            wa_vals = [obs["headers"].get("WWW-Authenticate", "(absent)") for obs in obs_list]
            www_auth_verification[state] = {
                "observed_values": list(set(wa_vals)),
                "consistent": len(set(wa_vals)) == 1,
            }

        endpoint_results[ep_name] = {
            "full_vector_discrimination": disc_score,
            "www_auth_only_discrimination": www_auth_disc,
            "cache_control_only_discrimination": cc_disc,
            "baselines": {
                "B-STATUS-ONLY": b_status_disc,
                "B-BODY-ONLY": b_body_disc,
                "B-URL-HASH": b_url_disc,
                "B-RANDOM": b_rand_disc,
            },
            "null_fp_rate": overall_fp_rate,
            "expired_invalid_identical": expired_invalid_identical,
            "drift_expired_invalid_jaccard": mean_drift,
            "www_auth_verification": www_auth_verification,
        }

        print(f"Full-vector discrimination: {disc_score:.6f}")
        print(f"WWW-Authenticate-only: {www_auth_disc:.6f}")
        print(f"B-BODY-ONLY: {b_body_disc:.6f}")
        print(f"Null FP rate: {overall_fp_rate:.1%}")

    # Decision rule
    additional_endpoints = [ep for ep in raw.keys() if "/userinfo" not in ep]
    www_auth_positive = sum(
        1 for ep in additional_endpoints
        if endpoint_results[ep]["www_auth_only_discrimination"] > 0
    )
    full_vector_positive = sum(
        1 for ep in additional_endpoints
        if endpoint_results[ep]["full_vector_discrimination"] > 0.5
    )
    userinfo_www_auth = endpoint_results.get("/userinfo (GET)", {}).get("www_auth_only_discrimination", 0)
    positive_control_pass = userinfo_www_auth > 0

    print(f"\n=== DECISION ===")
    print(f"WWW-Auth positive on {www_auth_positive}/3 additional endpoints")
    print(f"Full-vector > 0.5 on {full_vector_positive}/3 additional endpoints")
    print(f"Positive control: {positive_control_pass}")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
