#!/usr/bin/env python3
"""
EXP-RUNTIME-35741906498 — canonical packet builder (EXECUTE stage).

Reads experiment_result.json (derived) + raw artifacts, computes SHA-256, and
emits:
  result.json      — canonical producer handoff (EXPERIMENT_PACKET.md §4)
  provenance.json — reproduction provenance (EXPERIMENT_PACKET.md §5)

Frozen decision rule (spec.json/prereg.md §6) is reproduced here so the
mapping from derived measurements to {status, outcome} is explicit.
"""

import hashlib
import json
import platform
import socket
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
EXPERIMENT_ID = "EXP-RUNTIME-35741906498"
LANE = "runtime"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    derived = json.load(open(OUT / "experiment_result.json"))
    m = derived["metrics"]
    conditions = derived["conditions"]
    validity = derived["validity"]

    # ── Frozen decision rule mapping (prereg §6) ──────────────────────────
    all_pass = all(conditions[k]["pass"] for k in conditions)
    if derived["status"] == "COMPLETE":
        status = "COMPLETE"
        outcome = "SUPPORTS" if all_pass else "FALSIFIES"
    else:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"

    # ── controls: frozen C1-C6 + frozen baseline ids ──────────────────────
    controls = {}
    for cid, payload in conditions.items():
        controls[cid] = {
            "type": ("positive" if cid in ("C1_FULL_HEADER_DRIFT",
                                           "C2_HEADERS_ONLY_SIGNAL",
                                           "C4_FULL_EXCEEDS_BASELINES_NONVACUOUS",
                                           "C6_CONTENT_LENGTH_IDENTITY")
                     else "null" if cid == "C5_NULL_NO_FALSE_POSITIVE"
                     else "isolation"),
            "expected": payload["expected"],
            "observed": payload["observed"],
            "pass": bool(payload["pass"]),
            "evidence_refs": payload["evidence"],
        }
    # Frozen baselines (spec.json baselines; expected on A vs E)
    controls["B-STATUS-ONLY"] = {
        "type": "baseline-strong-null",
        "expected": "0.0 on all header-only comparisons (status 200 vs 200)",
        "observed": {
            "header_drift": m["header_drift_status"]["discrimination"],
            "cache_only": m["cache_only_status"]["discrimination"],
            "etag_only": m["etag_only_status"]["discrimination"],
            "cookie_only": m["cookie_only_status"]["discrimination"],
            "null_control": m["null_control_status"]["discrimination"],
        },
        "pass": all(m[f"{n}_status"]["discrimination"] == 0.0
                    for n in ("header_drift", "cache_only", "etag_only",
                              "cookie_only", "null_control")),
        "evidence_refs": "metrics.*_status",
    }
    controls["B-BODY-ONLY"] = {
        "type": "baseline-strong-null",
        "expected": "0.0 on all header-only comparisons (bodies byte-identical)",
        "observed": {
            "header_drift": m["header_drift_body"]["discrimination"],
            "cache_only": m["cache_only_body"]["discrimination"],
            "etag_only": m["etag_only_body"]["discrimination"],
            "cookie_only": m["cookie_only_body"]["discrimination"],
            "null_control": m["null_control_body"]["discrimination"],
        },
        "pass": all(m[f"{n}_body"]["discrimination"] == 0.0
                    for n in ("header_drift", "cache_only", "etag_only",
                              "cookie_only", "null_control")),
        "evidence_refs": "metrics.*_body",
    }
    controls["B-HEADERS-ONLY"] = {
        "type": "baseline-positive",
        "expected": "> 0.5 on A vs E and >= 2/3 per-header isolations",
        "observed": {
            "header_drift": m["header_drift_headers"]["discrimination"],
            "cache_only": m["cache_only_headers"]["discrimination"],
            "etag_only": m["etag_only_headers"]["discrimination"],
            "cookie_only": m["cookie_only_headers"]["discrimination"],
            "null_control": m["null_control_headers"]["discrimination"],
        },
        "pass": (m["header_drift_headers"]["discrimination"] > 0.5
                 and sum(m[f"{n}_headers"]["discrimination"] > 0.5
                         for n in ("cache_only", "etag_only", "cookie_only")) >= 2),
        "evidence_refs": "metrics.*_headers",
    }

    # ── metrics: stable names, explicit values ────────────────────────────
    metrics = {}
    for k, v in m.items():
        if k == "effective_distinct_n":
            metrics["effective_distinct_n"] = v
            continue
        metrics[k] = {
            "discrimination": v["discrimination"],
            "ci_95": [v["ci_95_lower"], v["ci_95_upper"]],
            "set_a_unique_fingerprints": v["set_a_size"],
            "set_b_unique_fingerprints": v["set_b_size"],
            "nominal_n": [v["nominal_n_a"], v["nominal_n_b"]],
            "degenerate_ci": v["degenerate_ci"],
        }
    metrics["body_sha256_across_A_E"] = derived["identity_checks"]["body_sha256_by_state"]["A"]
    metrics["content_length_by_state"] = derived["identity_checks"]["content_length_by_state"]
    metrics["body_len_by_state"] = derived["identity_checks"]["body_len_by_state"]
    metrics["raw_line_count"] = derived["raw_line_count"]
    metrics["null_e_exploratory_full"] = metrics["null_e_exploratory_full"]

    # ── observations: direct observations only, no interpretation ─────────
    observations = [
        "All 180 raw observations returned HTTP status 200 ([200]) on GET /resource.",
        "Response body SHA-256 identical across states A/B/C/D/E and all null batches "
        "(d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34; 31 bytes, "
        "json '{\"data\": \"hello\", \"version\": 1}').",
        "Content-Length header value '31' on all 180 observations; Body length 31 in all batches.",
        "Filtered header dict per state differed ONLY in Cache-Control, ETag, Set-Cookie, "
        "Vary; Connection=close, Content-Type=application/json, Content-Length=31 constant "
        "across all observations.",
        "Set-Cookie header present in exactly 80/180 observations "
        "(states D, E, null_E1, null_E2 = 4 batches x 20); absent from A, B, C, null_A1, null_A2.",
        "Date header varied across observations (20 unique values in 180 lines); Server "
        "constant (1 unique value); both excluded from fingerprints; 0 excluded-header "
        "leakage into filtered dicts (verified per line).",
        "Exactly 1 unique fingerprint per state per source (full/status/body/headers): "
        "deterministic responses; effective distinct N=1 per state despite nominal N=20.",
        "null_A1 vs null_A2 (same committed STATE_A, no write between batches) produced "
        "identical fingerprints on all four sources.",
        "Exploratory null null_E1 vs null_E2 (same committed STATE_E, no write between "
        "batches) produced identical fingerprints on all four sources.",
        "server_state write (POST /admin/set_headers) was followed by SQLite SELECT "
        "matching the intended state before every observation batch (batch_state_log.jsonl, 15 lines).",
    ]

    # ── validity notes ────────────────────────────────────────────────────
    validity_notes = [
        "Degenerate bootstrap CI: responses are deterministic (1 unique fingerprint per "
        "state), so CI is [1.0,1.0] or [0.0,0.0]. Per frozen design this is EXPECTED "
        "deterministic behavior (prereg §6), NOT inferential precision; effective distinct "
        "N=1 is reported alongside nominal N=20.",
        "Setting bounded to localhost Flask 3.1.3 development server (Werkzeug) on "
        "127.0.0.1:19848, single sequential client, no concurrency, no TLS/HTTP2, no "
        "production WSGI (gunicorn/nginx), no CDN. Generalization to those settings is "
        "untested (see unresolved).",
        "Werkzeug dev server emits constant 'Connection: close'; constant across all "
        "observations so it neither contributes to discrimination nor to the null.",
        "Prereg §5.4 projected 140 primary raw lines; frozen spec null_control clause adds "
        "an exploratory STATE_E resampled null (40 lines), total 180. E-null is exploratory "
        "and excluded from decision-rule C5.",
        "Fingerprint algorithm copied verbatim from parent "
        "EXP-RUNTIME-35697043449/run_experiment.py (compute_fingerprint/jaccard_distance/"
        "bootstrap_jaccard_ci). Independent recomputation from raw_observations.jsonl "
        "reproduced all 180x4 fingerprints with 0 mismatches.",
        "Status/body identity verified on every observation (not sampled): all 200s, single "
        "body SHA-256, single Content-Length. C3/C6 therefore hold by construction of the "
        "writable header_config design and are independently confirmed in raw evidence.",
    ]

    # ── unresolved ────────────────────────────────────────────────────────
    unresolved = [
        "Same-status body-only permission change (200 vs 200 with different body content) "
        "remains untested (parent unresolved[3]).",
        "Production middleware header behavior (Django/Express/FastAPI, gunicorn, nginx) "
        "untested; localhost Werkzeug only (parent unresolved[2] partially).",
        "Concurrency, HTTP/2, TLS, multi-client header handling untested.",
        "Non-degenerate bootstrap CI cannot be obtained on this deterministic substrate; "
        "header nondeterminism (e.g., CDN) needed for genuine CI.",
        "Per-header signal strength for header freshness policy design (which header "
        "subsets an agent should fingerprint) remains uncharacterized: all three isolated "
        "headers produced 1.0, so no ordering/sensitivity gradient was measured here.",
        "Distributed/production freshness and delta-repair testing remains blocked; this "
        "result unblocks localhost synthetic testing only (as specified in "
        "product_consequence_positive).",
    ]

    # Non-canonical artifacts (stable content at build time)
    artifacts = [
        {"path": f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
         "sha256": sha256(OUT / "run_experiment.py"), "role": "code"},
        {"path": f"research/experiments/{EXPERIMENT_ID}/raw_observations.jsonl",
         "sha256": sha256(OUT / "raw_observations.jsonl"), "role": "raw"},
        {"path": f"research/experiments/{EXPERIMENT_ID}/batch_state_log.jsonl",
         "sha256": sha256(OUT / "batch_state_log.jsonl"), "role": "raw"},
        {"path": f"research/experiments/{EXPERIMENT_ID}/experiment_result.json",
         "sha256": sha256(OUT / "experiment_result.json"), "role": "derived"},
        {"path": f"research/experiments/{EXPERIMENT_ID}/build_packet.py",
         "sha256": sha256(OUT / "build_packet.py"), "role": "code"},
        {"path": f"research/experiments/{EXPERIMENT_ID}/report.md",
         "sha256": sha256(OUT / "report.md"), "role": "canonical-packet"},
    ]

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": [],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }
    result["metrics"]["failing_conditions"] = (
        derived.get("failing_conditions", [])
        if derived["status"] == "COMPLETE" else null_failing()
    )

    # ── provenance (written BEFORE result.json so result.json can reference
    #    provenance.json's real hash; provenance.json does not reference
    #    result.json — result.json is the terminal canonical file of EXECUTE) ──
    git_head = ""
    try:
        import subprocess
        git_head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=OUT).decode().strip()
    except Exception:  # noqa: BLE001
        git_head = "unavailable"

    provenance = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "github_run_id": "35741906498",
        "github_run_attempt": 1,
        "commits": {
            "request_base_sha": "e606e040dfa1154aa4bae2ae4b456f81fd16781c",
            "freeze_commit": "9ed7c1a1ef212a3ad93b7c24e9c12b36be78c41c",
            "execution_base_sha": "d474f13ed0e194ef7228f7f350692e3a4b60f194",
            "head_sha_at_execution": git_head,
        },
        "design_inputs": {
            "request.json_sha256": "b2a59d9244cf4302722d0504d4523c23c73984fc3f6badbd037400c8b81e7222",
            "spec.json_sha256": "80e8cef6a256201c8cfb64f296c87c24fcc8085f83f95b96132c96e5ecad7c7c",
            "prereg.md_sha256": "1143ca059319a5dd083a18fb08116a36a2a6398fad97c3a78787257cf207c3df",
            "parent_handoff_sha256": "d3144036f4663aabfd22b0fc44386f8d067f3da8cf3ced65b53a400e270d2f43",
        },
        "environment": {
            "python": platform.python_version(),
            "flask": "3.1.3",
            "pyjwt": "2.14.0",
            "requests": "2.34.2",
            "sqlite": "3.45.1",
            "platform": platform.platform(),
            "host": socket.gethostname(),
            "server_endpoint": "http://127.0.0.1:19848",
            "db_path": "/tmp/spider_hdrdrift_testbed.db",
            "db_mode": "SQLite WAL",
            "jwt_algorithm": "HS256",
            "jwt_secret_note": "test-only fixed secret; not production material",
        },
        "fixtures": {
            "seed": 44,
            "n_samples_per_batch": 20,
            "jitter_ms": [50, 150],
            "bootstrap_b": 1000,
            "bootstrap_alpha": 0.05,
            "excluded_headers": ["Date", "Server", "X-Request-Id"],
            "header_states": derived["states"],
            "resource_body_sha256": derived["resource_body_sha256"],
            "batch_sequence": [
                "write A; batch A; write B; batch B; write C; batch C; write D; batch D; "
                "write E; batch E; batch null_E1; batch null_E2; write A; batch null_A1; "
                "batch null_A2"
            ],
        },
        "code_paths": [
            f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
            f"research/experiments/{EXPERIMENT_ID}/build_packet.py",
            "research/experiments/EXP-RUNTIME-35697043449/run_experiment.py (parent "
            "fingerprint algorithm source)",
        ],
        "commands": [
            "python3 run_experiment.py --smoke   # setup verification only",
            "python3 run_experiment.py           # full frozen execution",
            "python3 build_packet.py             # canonical packet emission",
        ],
        "artifacts": artifacts,
        "notes": [
            "Working tree contained pre-existing factory modifications to .github/ and "
            "scripts/validate_repo.py at execution time; those files were not touched by "
            "this EXECUTE stage.",
            "No git commit/push/switch/reset performed by EXECUTE.",
            "Timing: full run completed in one pass; no retries required.",
            "result.json is the terminal canonical file of EXECUTE; its own SHA-256 is "
            "not self-referenced inside any EXECUTE-produced file (AUDIT/DIRECTOR "
            "recompute it from the file content).",
        ],
    }
    with open(OUT / "provenance.json", "w") as f:
        json.dump(provenance, f, indent=2, sort_keys=False)
        f.write("\n")

    artifacts_with_provenance = artifacts + [
        {"path": f"research/experiments/{EXPERIMENT_ID}/provenance.json",
         "sha256": sha256(OUT / "provenance.json"), "role": "canonical-packet"},
    ]
    result["artifacts"] = artifacts_with_provenance

    with open(OUT / "result.json", "w") as f:
        json.dump(result, f, indent=2, sort_keys=False)
        f.write("\n")

    print(f"status={status} outcome={outcome} all_conditions_pass={all_pass}")
    print("result.json + provenance.json written")
    return 0


def null_failing():
    return []


if __name__ == "__main__":
    sys.exit(main())