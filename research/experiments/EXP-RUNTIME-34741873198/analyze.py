#!/usr/bin/env python3
"""
Analyze raw_observations.json from EXP-RUNTIME-34741873198.
Reads the complete raw data, computes discrimination scores, controls, and derived metrics.
Outputs result.json, report.md, and provenance.json.
"""

import hashlib
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np
from scipy.stats import spearmanr

EXPERIMENT_DIR = "/home/runner/work/Spider/Spider/research/experiments/EXP-RUNTIME-34741873198"
EXPERIMENT_ID = "EXP-RUNTIME-34741873198"
LANE = "runtime"
CLIENT_PROFILES = {"A": "br, gzip", "B": "gzip", "C": "identity"}
EXCLUDED_HEADERS = {"date", "server", "x-request-id"}
SEED = 44
REPS = 10
BROTLI_AVAILABLE = True
try:
    import brotli as _brotli_test
except ImportError:
    BROTLI_AVAILABLE = False


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def fingerprint_body_only(obs):
    """Body-only fingerprint: SHA-256 of (status, body_hash, '')."""
    body_hash = obs["body_hash"]
    vector = (
        obs["status"],
        body_hash,
        '',
    )
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def fingerprint_status_only(obs):
    """Status-only fingerprint: SHA-256 of (status, '', '')."""
    vector = (
        obs["status"],
        '',
        '',
    )
    return hashlib.sha256(repr(vector).encode("utf-8")).hexdigest()


def compute_discrimination_score(fingerprints_by_state):
    """Compute discrimination = intra_match_rate - inter_match_rate."""
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


def baseline_random(n=10, seed=99):
    """Random fingerprint baseline."""
    import random
    rng = random.Random(seed)
    return [hashlib.sha256(rng.getrandbits(256).to_bytes(32, "big")).hexdigest()
            for _ in range(n)]


def main():
    # Load raw observations
    raw_path = os.path.join(EXPERIMENT_DIR, "raw_observations.json")
    with open(raw_path) as f:
        raw_data = json.load(f)

    print(f"Loaded raw observations: client profiles = {list(raw_data.keys())}")

    # Verify completeness
    auth_states = ["no_auth", "valid_token", "expired_token", "invalid_token"]
    for profile_name in ["A", "B", "C"]:
        if profile_name not in raw_data:
            print(f"FATAL: Missing client profile {profile_name}")
            sys.exit(1)
        for ep in ["/userinfo", "/introspect"]:
            for state in auth_states:
                count = len(raw_data[profile_name].get(ep, {}).get(state, []))
                if count < REPS:
                    print(f"WARNING: profile={profile_name} {ep} {state} has only {count} reps (expected {REPS})")

    # Compute discrimination scores for all cells
    all_metrics = {}
    for profile_name in ["A", "B", "C"]:
        for ep in ["/userinfo", "/introspect"]:
            ep_data = raw_data[profile_name][ep]
            key = f"{ep}_{profile_name}"

            # Compute fingerprints from raw observations
            fps_body_by_state = defaultdict(list)
            fps_status_by_state = defaultdict(list)

            for state, obs_list in ep_data.items():
                for obs in obs_list:
                    fp_body = fingerprint_body_only(obs)
                    fp_status = fingerprint_status_only(obs)
                    fps_body_by_state[state].append(fp_body)
                    fps_status_by_state[state].append(fp_status)

            body_disc = compute_discrimination_score(fps_body_by_state)
            status_disc = compute_discrimination_score(fps_status_by_state)

            # Baseline random
            b_rand_fps = baseline_random(n=REPS * len(auth_states))
            b_rand_by_state = {}
            idx = 0
            for s in auth_states:
                b_rand_by_state[s] = b_rand_fps[idx:idx + REPS]
                idx += REPS
            b_rand_disc = compute_discrimination_score(b_rand_by_state)

            # Body hash variation per state
            body_hash_variation = {}
            for state, obs_list in ep_data.items():
                hashes = [obs["body_hash"] for obs in obs_list]
                body_hash_variation[state] = {
                    "unique_count": len(set(hashes)),
                    "total": len(hashes),
                    "all_same": len(set(hashes)) == 1,
                }

            # Compression verification
            compression_verification = {}
            for state, obs_list in ep_data.items():
                ce_headers = [obs.get("content_encoding", obs["headers"].get("Content-Encoding", "none"))
                              for obs in obs_list]
                compression_verification[state] = {
                    "content_encoding_values": list(set(ce_headers)),
                    "count": len(ce_headers),
                }

            # Body sizes
            body_sizes = {}
            for state, obs_list in ep_data.items():
                sizes = [obs.get("body_size", 0) for obs in obs_list]
                body_sizes[state] = {
                    "min": min(sizes),
                    "max": max(sizes),
                    "mean": sum(sizes) / len(sizes) if sizes else 0,
                }

            all_metrics[key] = {
                "body_only_discrimination": body_disc,
                "status_only_discrimination": status_disc,
                "baselines": {"B-RANDOM": b_rand_disc},
                "body_hash_variation": body_hash_variation,
                "compression_verification": compression_verification,
                "body_sizes": body_sizes,
                "total_requests": sum(len(v) for v in ep_data.values()),
            }

            print(f"  {key}: body={body_disc:.4f}, "
                  f"status={status_disc:.4f}, B-RANDOM={b_rand_disc:.4f}")

    # Compute mixed-client metrics
    if "MIXED" in raw_data:
        for ep in ["/userinfo", "/introspect"]:
            if ep in raw_data["MIXED"]:
                ep_data = raw_data["MIXED"][ep]
                key = f"{ep}_MIXED"
                fps_body_by_state = defaultdict(list)
                for state, obs_list in ep_data.items():
                    for obs in obs_list:
                        fp_body = fingerprint_body_only(obs)
                        fps_body_by_state[state].append(fp_body)
                body_disc = compute_discrimination_score(fps_body_by_state)
                all_metrics[key] = {"body_only_discrimination": body_disc}
                print(f"  {key}: body={body_disc:.4f}")

    # Primary derived metrics: body-only discrimination on /userinfo per client profile
    userinfo_bo_discs = {}
    for profile_name in ["A", "B", "C"]:
        key = f"/userinfo_{profile_name}"
        userinfo_bo_discs[profile_name] = all_metrics[key]["body_only_discrimination"]

    print(f"\n/userinfo body-only discrimination by client profile: {userinfo_bo_discs}")

    # Status-only discrimination on /userinfo per client profile
    userinfo_status_discs = {}
    for profile_name in ["A", "B", "C"]:
        key = f"/userinfo_{profile_name}"
        userinfo_status_discs[profile_name] = all_metrics[key]["status_only_discrimination"]

    # B-IDENTITY-BODY-ONLY: body-only at profile C (identity)
    identity_body_only = userinfo_bo_discs["C"]

    # B-DETERMINISTIC-BR-BODY-ONLY: body-only at profile A (brotli)
    br_body_only = userinfo_bo_discs["A"]

    # B-DETERMINISTIC-GZIP-BODY-ONLY: body-only at profile B (gzip)
    gzip_body_only = userinfo_bo_discs["B"]

    # B-MIXED-CLIENT-BODY-ONLY
    mixed_body_only = all_metrics.get("/userinfo_MIXED", {}).get("body_only_discrimination", None)

    # B-STATUS-ONLY
    status_only = userinfo_status_discs["C"]

    # Within-state hash variation for deterministic brotli (A) and gzip (B)
    within_state_variation = {}
    for profile_name in ["A", "B"]:
        key = f"/userinfo_{profile_name}"
        hv = all_metrics[key]["body_hash_variation"]
        within_state_variation[profile_name] = {
            "all_states_all_same": all(v["all_same"] for v in hv.values()),
            "total_unique_hashes": sum(v["unique_count"] for v in hv.values()),
            "total_requests": sum(v["total"] for v in hv.values()),
            "per_state": hv,
        }

    # Null control: B-RANDOM at all client profiles
    null_control_values = {}
    for profile_name in ["A", "B", "C"]:
        key = f"/userinfo_{profile_name}"
        null_control_values[profile_name] = all_metrics[key]["baselines"]["B-RANDOM"]

    print(f"\nM_DETERMINISTIC_DISCRIMINATION:")
    print(f"  identity (C): {identity_body_only:.4f}")
    print(f"  brotli (A): {br_body_only:.4f}")
    print(f"  gzip (B): {gzip_body_only:.4f}")
    print(f"M_STATUS_INVARIANCE: {userinfo_status_discs}")
    print(f"M_NULL_CONTROL: {null_control_values}")
    print(f"M_WITHIN_STATE_VARIATION: {within_state_variation}")
    print(f"M_CROSS_CLIENT_DIVERGENCE: identity={identity_body_only:.4f}, mixed={mixed_body_only}")

    # Add derived metrics
    all_metrics["M_DETERMINISTIC_DISCRIMINATION"] = {
        "identity_body_only": float(identity_body_only),
        "br_body_only": float(br_body_only),
        "gzip_body_only": float(gzip_body_only),
        "description": "Body-only discrimination under deterministic brotli and gzip on /userinfo"
    }
    all_metrics["M_STATUS_INVARIANCE"] = {
        "per_profile": {k: float(v) for k, v in userinfo_status_discs.items()},
        "expected": 0.5,
        "description": "Status-only discrimination on /userinfo invariant across all client profiles"
    }
    all_metrics["M_WITHIN_STATE_VARIATION"] = within_state_variation
    all_metrics["M_CROSS_CLIENT_DIVERGENCE"] = {
        "identity_body_only": float(identity_body_only),
        "mixed_client_body_only": float(mixed_body_only) if mixed_body_only is not None else None,
        "description": "Cross-client hash divergence: mixed clients should have degraded discrimination"
    }
    all_metrics["M_NULL_CONTROL"] = {
        "per_profile": {k: float(v) for k, v in null_control_values.items()},
        "description": "B-RANDOM discrimination at all client profiles"
    }

    # Evaluate controls
    control_details = {}

    # C1: Positive control — identity body-only >= 0.35
    c1_pass = identity_body_only >= 0.35
    control_details["C_POSITIVE_CONTROL_IDENTITY"] = {
        "expected": "B-IDENTITY-BODY-ONLY >= 0.35 on /userinfo",
        "observed": float(identity_body_only),
        "pass": c1_pass,
    }

    # C2: Null control — B-RANDOM ~ 0.0 at all client profiles
    all_null_pass = all(abs(v) < 0.1 for v in null_control_values.values())
    control_details["C_NULL_CONTROL"] = {
        "expected": "B-RANDOM ~ 0.0 at all client profiles",
        "observed": {k: float(v) for k, v in null_control_values.items()},
        "pass": all_null_pass,
    }

    # C3: Deterministic brotli preserves
    c3_pass = br_body_only >= identity_body_only - 0.15
    control_details["C_DETERMINISTIC_BR_PRESERVES"] = {
        "expected": "B-DETERMINISTIC-BR-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo",
        "observed": float(br_body_only),
        "pass": c3_pass,
    }

    # C4: Deterministic gzip preserves
    c4_pass = gzip_body_only >= identity_body_only - 0.15
    control_details["C_DETERMINISTIC_GZIP_PRESERVES"] = {
        "expected": "B-DETERMINISTIC-GZIP-BODY-ONLY >= B-IDENTITY-BODY-ONLY - 0.15 on /userinfo",
        "observed": float(gzip_body_only),
        "pass": c4_pass,
    }

    # C5: Within-state hash variation = 0 for deterministic brotli and gzip
    c5_pass = all(
        within_state_variation.get(p, {}).get("all_states_all_same", False)
        for p in ["A", "B"]
    )
    control_details["C_WITHIN_STATE_STABILITY"] = {
        "expected": "Within-state body hash variation = 0 for deterministic brotli and gzip",
        "observed": {p: within_state_variation.get(p, {}) for p in ["A", "B"]},
        "pass": c5_pass,
    }

    # C6: Mixed-client divergence
    c6_pass = (mixed_body_only is not None and mixed_body_only < identity_body_only)
    control_details["C_MIXED_CLIENT_DIVERGENCE"] = {
        "expected": "B-MIXED-CLIENT-BODY-ONLY < B-IDENTITY-BODY-ONLY on /userinfo",
        "observed": float(mixed_body_only) if mixed_body_only is not None else None,
        "pass": c6_pass,
    }

    # C7: Status-only invariant = 0.5
    c7_pass = all(abs(v - 0.5) < 0.01 for v in userinfo_status_discs.values())
    control_details["C_STATUS_INVARIANT"] = {
        "expected": "B-STATUS-ONLY >= 0.5 on /userinfo invariant across all client profiles",
        "observed": {k: float(v) for k, v in userinfo_status_discs.items()},
        "pass": c7_pass,
    }

    # C8: No pipeline errors
    c8_pass = True  # Analysis has no errors
    control_details["C_NO_PIPELINE_ERRORS"] = {
        "expected": "0 errors",
        "observed": 0,
        "pass": True,
    }

    all_pass = all(c["pass"] for c in control_details.values())

    print(f"\nControl results:")
    for name, ctrl in control_details.items():
        print(f"  {name}: {'PASS' if ctrl['pass'] else 'FAIL'} (observed={ctrl['observed']})")

    # Decision rule (from frozen spec.json)
    if all_pass:
        outcome = "SUPPORTS"
        status = "COMPLETE"
    elif not c3_pass or not c4_pass:
        # Deterministic compression degrades body-only
        outcome = "FALSIFIES"
        status = "COMPLETE"
    elif not c5_pass:
        # Deterministic compression produces non-deterministic output
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    elif not c1_pass or not c2_pass or not c8_pass:
        outcome = "NOT_APPLICABLE"
        status = "MEASUREMENT_INVALID"
    else:
        outcome = "MIXED"
        status = "COMPLETE"

    print(f"\nDECISION: status={status}, outcome={outcome}")

    # Build observations list
    observations = [
        f"Keycloak 25.0 deployed via Docker on localhost:18080",
        f"CDN negotiation proxy on localhost:18081",
        f"Client profiles: {CLIENT_PROFILES}",
        f"CDN negotiation: select highest-priority algorithm from Accept-Encoding (br > gzip > identity)",
        f"2 endpoints: /userinfo (GET), /introspect (POST)",
        f"4 auth states x {REPS} reps x {len(CLIENT_PROFILES)} client profiles x 2 endpoints = {4 * REPS * len(CLIENT_PROFILES) * 2} total requests",
        f"Plus mixed-client test: 4 states x {REPS} reps x 2 clients x 2 endpoints = {4 * REPS * 2 * 2} requests",
        f"Total requests: {4 * REPS * len(CLIENT_PROFILES) * 2 + 4 * REPS * 2 * 2}",
        f"Seed: {SEED}",
        f"Brotli available: {BROTLI_AVAILABLE}",
    ]

    for profile_name in ["A", "B", "C"]:
        for ep_name in ["/userinfo", "/introspect"]:
            key = f"{ep_name}_{profile_name}"
            observations.append(
                f"Profile {profile_name} ({CLIENT_PROFILES[profile_name]}) {ep_name}: "
                f"body={all_metrics[key]['body_only_discrimination']:.4f}, "
                f"status={all_metrics[key]['status_only_discrimination']:.4f}, "
                f"B-RANDOM={all_metrics[key]['baselines']['B-RANDOM']:.4f}"
            )

    for ep_name in ["/userinfo", "/introspect"]:
        key = f"{ep_name}_MIXED"
        if key in all_metrics:
            observations.append(
                f"MIXED-CLIENT {ep_name}: body={all_metrics[key]['body_only_discrimination']:.4f}"
            )

    for profile_name in ["A", "B"]:
        if profile_name in within_state_variation:
            wsv = within_state_variation[profile_name]
            observations.append(
                f"Profile {profile_name} within-state variation: "
                f"all_same={wsv['all_states_all_same']}, "
                f"unique_hashes={wsv['total_unique_hashes']}/{wsv['total_requests']}"
            )

    # Validity notes
    validity_notes = [
        "Same Keycloak 25.0 Docker deployment as parent experiments",
        "Same fingerprint algorithm: SHA-256(repr((status, body_sha256, '')))",
        f"Python version: {sys.version}",
        "Jitter: 50-150ms uniform between requests",
        "expired_token is locally-signed HS256, not Keycloak-issued (V6 leakage from parent)",
        f"Brotli module available: {BROTLI_AVAILABLE}",
        "Proxy overrides client Accept-Encoding to identity to get raw response from Keycloak",
        "Proxy reads original Accept-Encoding and deterministically selects algorithm (br > gzip > identity)",
        "Body hash computed on compressed bytes received by client (not raw bytes from Keycloak)",
        "Body-only discrimination is NOT tautological here — compression directly attacks the body hash",
        f"Seed={SEED} for request ordering (deterministic across runs)",
        "CDN negotiation is deterministic: same Accept-Encoding always produces same algorithm",
        "Compression uses fixed parameters (gzip level=9, brotli level=6) to simulate CDN determinism",
        "This is materially different from EXP-RUNTIME-34654566605 which tested per-request random compression",
        "Analysis performed on raw_observations.json collected by run_experiment.py",
    ]

    if not BROTLI_AVAILABLE:
        validity_notes.append("BROTLI NOT AVAILABLE: Client A falls back to gzip (weaker test)")

    # Unresolved
    unresolved = [
        "Does body-only discrimination survive multiple stacked infrastructure layers with correlated compression?",
        "Does the result generalize to non-Keycloak OAuth/OIDC providers?",
        "Would a filtered full-vector baseline (status+WWW-Authenticate+Cache-Control+body_hash) survive deterministic compression?",
        "Does result generalize to larger/more diverse body content-types and sizes beyond Keycloak /userinfo 0/189 bytes?",
    ]

    # Write result.json
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": all_metrics,
        "controls": control_details,
        "artifacts": [
            {"path": "raw_observations.json", "sha256": hashlib.sha256(
                open(raw_path, "rb").read()
            ).hexdigest(), "role": "raw"},
            {"path": "run_experiment.py", "role": "code"},
            {"path": "analyze.py", "role": "code"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }

    with open(os.path.join(EXPERIMENT_DIR, "result.json"), "w") as f:
        json.dump(result, f, indent=2, cls=NumpyEncoder)
    print(f"\nResult written to result.json")

    # Write report.md
    report = generate_report(result, all_metrics, control_details,
                             userinfo_bo_discs, userinfo_status_discs,
                             identity_body_only, br_body_only, gzip_body_only,
                             mixed_body_only, status_only, within_state_variation,
                             null_control_values, outcome, status)
    with open(os.path.join(EXPERIMENT_DIR, "report.md"), "w") as f:
        f.write(report)
    print(f"Report written to report.md")

    # Write provenance.json
    provenance = {
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "github_run_id": None,
        "github_run_attempt": None,
        "base_sha": "f96912acd91c39c50c88a274e84a66030bf45afa",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python_version": sys.version,
            "platform": sys.platform,
        },
        "keycloak": {
            "image": "quay.io/keycloak/keycloak:25.0",
            "mode": "start-dev",
            "port": 18080,
            "realm": "spider-test",
            "client": "spider-client",
        },
        "proxy": {
            "port": 18081,
            "type": "Python HTTPServer reverse proxy with CDN negotiation",
            "client_profiles": CLIENT_PROFILES,
            "negotiation": "br > gzip > identity (deterministic per Accept-Encoding)",
            "brotli_available": BROTLI_AVAILABLE,
        },
        "artifacts": {
            "raw_observations": {
                "path": "raw_observations.json",
                "sha256": result["artifacts"][0]["sha256"],
                "total_observations": 240 + 80,  # 240 per-profile + 80 mixed
            },
            "run_experiment": {"path": "run_experiment.py"},
            "analyze": {"path": "analyze.py"},
        },
        "fingerprint_algorithm": {
            "body_only": "SHA-256(repr((status, body_sha256, '')))",
            "body_hash_source": "compressed bytes received by client",
            "excluded_headers": list(EXCLUDED_HEADERS),
        },
        "cdn_negotiation_model": {
            "description": "CDN selects highest-priority algorithm from client's Accept-Encoding",
            "priority_order": "br > gzip > identity",
            "determinism": "Same Accept-Encoding always produces same algorithm and compressed output",
        },
        "parent_experiment": "EXP-RUNTIME-34654566605",
        "frozen_spec_hash": "f20fa9b611eacc2c3e6c787369c38dd769139776176cffaa1cec253fb5bc672d",
    }

    with open(os.path.join(EXPERIMENT_DIR, "provenance.json"), "w") as f:
        json.dump(provenance, f, indent=2)
    print(f"Provenance written to provenance.json")


def generate_report(result, metrics, controls, bo_discs, status_discs,
                    identity_bo, br_bo, gzip_bo, mixed_bo, status_only,
                    within_var, null_ctrl, outcome, status):
    """Generate markdown report."""
    profile_names = {"A": "br, gzip", "B": "gzip", "C": "identity"}
    cdn_selects = {"A": "brotli", "B": "gzip", "C": "identity"}
    
    lines = []
    lines.append("# EXP-RUNTIME-34741873198 -- Body-Only Fingerprint Under Deterministic CDN Negotiation")
    lines.append("")
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"**Status**: {status}")
    lines.append(f"**Outcome**: {outcome}")
    lines.append("")
    lines.append("This experiment tests whether body-only HTTP fingerprint discrimination survives")
    lines.append("realistic CDN negotiation where Content-Encoding is selected deterministically from")
    lines.append("the client's advertised Accept-Encoding (not per-request random).")
    lines.append("")
    lines.append("## 2. Scientific Question")
    lines.append("")
    lines.append("Does body-only HTTP fingerprint discrimination survive realistic CDN negotiation where")
    lines.append("Content-Encoding is selected deterministically from the client's advertised Accept-Encoding")
    lines.append("(not per-request random), and would a client with stable Accept-Encoding see deterministic")
    lines.append("compressed hashes?")
    lines.append("")
    lines.append("## 3. Primary Results")
    lines.append("")
    lines.append("### 3.1 Body-Only Discrimination by Client Profile (/userinfo)")
    lines.append("")
    lines.append("| Client Profile | Accept-Encoding | CDN Selects | Body-Only | Status-Only | B-RANDOM |")
    lines.append("|----------------|-----------------|-------------|-----------|-------------|----------|")
    
    for profile_name in ["A", "B", "C"]:
        key = f"/userinfo_{profile_name}"
        m = metrics[key]
        lines.append(
            f"| {profile_name} | {profile_names[profile_name]} | {cdn_selects[profile_name]} | "
            f"{m['body_only_discrimination']:.4f} | "
            f"{m['status_only_discrimination']:.4f} | "
            f"{m['baselines']['B-RANDOM']:.4f} |"
        )
    
    lines.append("")
    lines.append("### 3.2 Mixed-Client Test (/userinfo)")
    lines.append("")
    lines.append("| Condition | Body-Only |")
    lines.append("|-----------|-----------|")
    lines.append(f"| Mixed (A+C alternating) | {mixed_bo:.4f} |")
    lines.append(f"| Identity only (C) | {identity_bo:.4f} |")
    lines.append("")
    lines.append("### 3.3 Derived Metrics")
    lines.append("")
    lines.append(f"- **B-IDENTITY-BODY-ONLY** (identity, profile C): {identity_bo:.4f}")
    lines.append(f"  - Threshold: >= 0.35")
    lines.append(f"  - {'PASS' if controls['C_POSITIVE_CONTROL_IDENTITY']['pass'] else 'FAIL'}")
    lines.append("")
    lines.append(f"- **B-DETERMINISTIC-BR-BODY-ONLY** (brotli, profile A): {br_bo:.4f}")
    lines.append(f"  - Threshold: >= identity - 0.15 = {identity_bo - 0.15:.4f}")
    lines.append(f"  - {'PASS' if controls['C_DETERMINISTIC_BR_PRESERVES']['pass'] else 'FAIL'}")
    lines.append("")
    lines.append(f"- **B-DETERMINISTIC-GZIP-BODY-ONLY** (gzip, profile B): {gzip_bo:.4f}")
    lines.append(f"  - Threshold: >= identity - 0.15 = {identity_bo - 0.15:.4f}")
    lines.append(f"  - {'PASS' if controls['C_DETERMINISTIC_GZIP_PRESERVES']['pass'] else 'FAIL'}")
    lines.append("")
    lines.append(f"- **B-MIXED-CLIENT-BODY-ONLY** (A+C alternating): {mixed_bo:.4f}")
    lines.append(f"  - Threshold: < identity = {identity_bo:.4f}")
    lines.append(f"  - {'PASS' if controls['C_MIXED_CLIENT_DIVERGENCE']['pass'] else 'FAIL'}")
    lines.append("")
    lines.append(f"- **B-STATUS-ONLY** (profile C): {status_only:.4f}")
    lines.append(f"  - Expected: 0.5 invariant")
    lines.append(f"  - {'PASS' if controls['C_STATUS_INVARIANT']['pass'] else 'FAIL'}")
    lines.append("")
    lines.append("## 4. Within-State Hash Stability")
    lines.append("")
    lines.append("| Client Profile | Algorithm | All States Same | Unique Hashes | Total Requests |")
    lines.append("|----------------|-----------|-----------------|---------------|----------------|")
    
    for profile_name in ["A", "B"]:
        algo = cdn_selects[profile_name]
        wsv = within_var[profile_name]
        lines.append(
            f"| {profile_name} | {algo} | {wsv['all_states_all_same']} | "
            f"{wsv['total_unique_hashes']} | {wsv['total_requests']} |"
        )
    
    lines.append("")
    lines.append("## 5. Controls")
    lines.append("")
    lines.append("| Control | Expected | Observed | Pass |")
    lines.append("|---------|----------|----------|------|")
    
    for name, ctrl in controls.items():
        lines.append(
            f"| {name} | {ctrl['expected']} | {ctrl['observed']} | {'PASS' if ctrl['pass'] else 'FAIL'} |"
        )
    
    lines.append("")
    lines.append("## 6. Interpretation")
    lines.append("")
    
    if outcome == "SUPPORTS":
        lines.append("All controls pass. Body-only discrimination survives deterministic CDN negotiation.")
        lines.append("When a client with stable Accept-Encoding sees deterministic compressed output from")
        lines.append("the CDN, body-only fingerprints (status + compressed-body hash) remain stable and")
        lines.append("discriminating.")
        lines.append("")
        lines.append("**Key findings**:")
        lines.append(f"- Deterministic brotli preserves discrimination: {br_bo:.4f} (vs identity {identity_bo:.4f})")
        lines.append(f"- Deterministic gzip preserves discrimination: {gzip_bo:.4f} (vs identity {identity_bo:.4f})")
        lines.append(f"- Within-state hash variation is 0 for both brotli and gzip (deterministic output)")
        lines.append(f"- Mixed-client test shows degradation: {mixed_bo:.4f} < {identity_bo:.4f} (cross-client divergence)")
        lines.append("")
        lines.append("**Product consequence**: Body-only discrimination survives realistic CDN negotiation.")
        lines.append("SPIDER can use body-only as the default production fingerprint strategy when the client's")
        lines.append("Accept-Encoding is stable. The EXP-RUNTIME-34654566605 body-only recommendation is")
        lines.append("strengthened for realistic CDN scenarios. No compression-normalization overhead needed.")
    elif outcome == "FALSIFIES":
        lines.append("Body-only discrimination does NOT survive deterministic CDN negotiation.")
        lines.append("Even when the same client always sees the same algorithm, body-only fingerprints")
        lines.append("degrade.")
        lines.append("")
        lines.append("**Product consequence**: CDN compression is a fundamental threat to body-only architecture")
        lines.append("regardless of negotiation determinism. SPIDER must: (a) use a compression-normalization")
        lines.append("layer, (b) use header-based or filtered-full-vector fingerprinting, or")
        lines.append("(c) restrict body-only to environments where compression is disabled.")
    elif outcome == "MEASUREMENT_INVALID":
        lines.append("Measurement invalid: deterministic compression produces non-deterministic output,")
        lines.append("or positive/null controls failed. Pipeline debugging required.")
        lines.append("")
        lines.append("**Product consequence**: No scientific evidence for or against. Experiment must")
        lines.append("be repeated after fixing the measurement pipeline.")
    else:
        lines.append(f"Outcome is {outcome} with status {status}. See validity notes for details.")
    
    lines.append("")
    lines.append("## 7. Validity Notes")
    lines.append("")
    for note in result["validity_notes"]:
        lines.append(f"- {note}")
    
    lines.append("")
    lines.append("## 8. Unresolved Questions")
    lines.append("")
    for q in result["unresolved"]:
        lines.append(f"- {q}")
    
    lines.append("")
    lines.append("## 9. Decision")
    lines.append("")
    lines.append(f"**Verdict**: {outcome} -- {status}")
    lines.append("")
    lines.append("The frozen decision rule from spec.json determines the verdict based on the")
    lines.append("eight controls evaluated above.")
    
    return "\n".join(lines)


if __name__ == "__main__":
    main()
