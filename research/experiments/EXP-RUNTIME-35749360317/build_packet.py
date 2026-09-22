#!/usr/bin/env python3
"""
EXP-RUNTIME-35749360317 — canonical packet builder (EXECUTE stage).

Reads experiment_result.json (derived) + raw artifacts, computes SHA-256, and
emits:
  result.json      — canonical producer handoff (EXPERIMENT_PACKET.md §4)
  provenance.json — reproduction provenance (EXPERIMENT_PACKET.md §5)

Frozen decision rule (spec.json decision_rule / prereg.md §6) is reproduced
here so the mapping from derived measurements to {status, outcome} is explicit.
"""

import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
EXPERIMENT_ID = "EXP-RUNTIME-35749360317"
LANE = "runtime"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=OUT).decode().strip()
    except Exception:  # noqa: BLE001
        return "unavailable"


def main() -> int:
    derived = json.load(open(OUT / "experiment_result.json"))
    m = derived["metrics"]
    conditions = derived["conditions"]
    validity = derived["validity"]
    ident = derived["identity_checks"]

    # ── Frozen decision rule mapping (spec.json decision_rule, prereg §6) ──
    all_pass = all(conditions[k]["pass"] for k in conditions)
    if derived["status"] == "COMPLETE":
        status = "COMPLETE"
        outcome = "SUPPORTS" if all_pass else "FALSIFIES"
    else:
        status = "MEASUREMENT_INVALID"
        outcome = "NOT_APPLICABLE"

    # ── controls: frozen C1-C8 + exploratory C5B + frozen baseline ids ────
    controls = {}
    for cid, payload in conditions.items():
        controls[cid] = {
            "type": payload.get("type", "positive"),
            "expected": payload.get("expected"),
            "observed": payload.get("observed"),
            "pass": bool(payload.get("pass")),
            "evidence_refs": payload.get("evidence_refs"),
        }
    for bid, payload in derived["baselines"].items():
        controls[bid] = {
            "type": payload.get("type", "baseline"),
            "expected": payload.get("expected"),
            "observed": payload.get("observed"),
            "pass": bool(payload.get("pass")),
            "evidence_refs": payload.get("evidence_refs"),
        }

    # ── metrics: stable names, explicit values (mirrors derived artifact) ──
    metrics = {}
    for k, v in m.items():
        if k in ("effective_distinct_n",):
            metrics[k] = v
            continue
        metrics[k] = {
            "discrimination": v["discrimination"],
            "ci_95": v["ci_95"],
            "set_a_unique_fingerprints": v.get("set_a_size", v.get("set_a_unique_fingerprints")),
            "set_b_unique_fingerprints": v.get("set_b_size", v.get("set_b_unique_fingerprints")),
            "nominal_n": v.get("nominal_n"),
            "degenerate_ci": v.get("degenerate_ci"),
        }
    # Identity metrics (raw-derived, at state granularity)
    metrics["body_sha256_by_state"] = ident["body_sha_by_state"]
    metrics["content_length_by_state"] = ident["content_length_by_state"]
    metrics["body_len_by_state"] = ident["body_len_by_state"]
    metrics["non_clen_headers_by_state"] = ident["non_clen_headers_by_state"]
    metrics["statuses_by_state"] = ident["statuses_by_state"]
    metrics["raw_line_count"] = derived["raw_line_count"]
    metrics["failing_conditions"] = derived.get("failing_conditions", [])

    # ── observations: direct observations only, no interpretation ─────────
    observations = [
        "300 raw observations: 180x HTTP 200 (body-only A/B/C 60, null A1/A2 40, null "
        "C1/C2 40, perm_200 20, sess_200 20), 60x HTTP 403 (perm_403 20, perm403 null 40), "
        "60x HTTP 401 (sess_401 20, sess401 null 40).",
        "Body SHA-256 per state, single value across its 20 observations and resampled "
        "nulls: A d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34 (31 B), "
        "B 67c186f2cee1ccf01f55c80235eb9b1b1d14b073223a807b9ce944405e67999c (70 B), "
        "C b46c461cceeefa595c3ac0d706689ed382340b59c20a269a930c786c8389dd32 (117 B).",
        "403 body constant on all 60x403 observations "
        "(387fe73d9abe7e6c32a0eb6113efea98dea609edefe9c3b4c9788fcaaef1603b, 22 B); 401 body "
        "constant on all 60x401 observations "
        "(9df366cd61d0e8a1bd9c4462d4f032e5317b2708d154047affa816e234518f34, 25 B).",
        "Content-Length == body_len on all 300 observations; CLEN by state 31 / 70 / 117 "
        "(distinct, strictly increasing).",
        "Non-CLEN filtered headers identical across A/B/C (Cache-Control max-age=3600, "
        "ETag W/\"fixed-aaa-111\", Vary Accept-Encoding, Content-Type application/json, "
        "Connection close); Set-Cookie absent on all 300 observations.",
        "Date header varied across observations (excluded, 0 leakage into filtered dicts); "
        "Server constant; EXCLUDED_HEADERS unchanged.",
        "Exactly 1 unique fingerprint per state per source (full/status/body/headers/"
        "headers_no_clen): deterministic responses; effective distinct N=1 per state "
        "despite nominal N=20.",
        "null_A1 vs null_A2 (same committed STATE_A, no write between) identical on all "
        "five sources; exploratory null_C1 vs null_C2 (same STATE_C) identical; "
        "perm403_null_1/2 identical; sess401_null_1/2 identical.",
        "All 12 admin writes returned HTTP 200 with post-SELECT state matching intent "
        "(batch_state_log.jsonl, 27 lines); every observation batch was preceded by a "
        "pre-batch state-snapshot verify entry (15).",
        "sess_401 batch observed only after invalidate_session post-SELECT showed "
        "reader_valid_sessions=0; perm_403 batch observed only after set_role post-SELECT "
        "showed reader role=viewer.",
    ]

    # ── validity notes ────────────────────────────────────────────────────
    validity_notes = [
        "Degenerate bootstrap CI: responses are deterministic (1 unique fingerprint per "
        "state per source), so CI is [1.0,1.0] or [0.0,0.0]. Per frozen design this is "
        "EXPECTED deterministic behavior (prereg §6), NOT inferential precision; "
        "effective distinct N=1 is reported alongside nominal N=20.",
        "Setting bounded to localhost Flask 3.1.3 development server (Werkzeug) on "
        "127.0.0.1:19849, single sequential client, no concurrency, no TLS/HTTP2, no "
        "production WSGI (gunicorn/nginx), no CDN. Generalization untested (see "
        "unresolved).",
        "Werkzeug dev server emits constant 'Connection: close'; constant across all "
        "observations, so it neither contributes to discrimination nor to the null.",
        "Body B/C effective lengths are 70/117 bytes for the exact frozen canonical JSON "
        "(prereg §4.2 marks them '~52'/'~95 (exact logged)'); frozen C6 strict inequality "
        "(31<70<117) and proportionality via CLEN==body_len are satisfied; body A pin "
        "exact (31 B, d0ca833f…).",
        "Line count 300 = 15 batches x 20. Frozen spec null_control (N1, N2 exploratory, "
        "N3 same-state 403/401) and decision rule C7/C8 null requirements mandate the "
        "full schedule; prereg §5.4/§11 prose nominal 140-180 predates N3; disclosed "
        "nominal vs effective per prereg §11 and batch_state_log is consistent.",
        "First attempt (run 35749360317) failed with EXECUTION_FAILURE exit 75 "
        "(retryable=true, fingerprint fbf5825e…) during pre-execution environment checks "
        "(failure.json). That is an infrastructure failure, not a negative result; this "
        "run executed cleanly.",
        "Pre-measurement server fix: initial smoke pass showed GET /resource returned a "
        "reason-specific 401 body ({\"error\":\"session_invalid\"}) for invalidated "
        "sessions, contradicting the frozen prereg S_401 pin (401 body "
        "{\"error\":\"unauthorized\"}). The server error mapping was corrected to the "
        "frozen constant error bodies before any full measurement; smoke re-passed; no "
        "measurement was taken with the non-conforming body.",
        "Fingerprint algorithm copied verbatim from parent "
        "EXP-RUNTIME-35741906498/run_experiment.py (which itself copies "
        "EXP-RUNTIME-35697043449) — compute_fingerprint/jaccard_distance/"
        "bootstrap_jaccard_ci. Independent recomputation from raw_observations.jsonl "
        "reproduced all 300x5 fingerprints with 0 mismatches.",
        "Status/body/CLEN identity verified on every observation (not sampled): all "
        "body-only+null observations 200; single body SHA per state; CLEN==body_len "
        "everywhere. C3/C6 hold by construction and are independently confirmed in raw "
        "evidence.",
    ]

    # ── unresolved ────────────────────────────────────────────────────────
    unresolved = [
        "Role-column-driven permission-filtered body (P1 spelling: two tokens, same "
        "body_config) is not separately measured; A vs C (body_config variant) realized "
        "the permission-level 200 vs 200 comparison per frozen C7(a).",
        "Production WSGI (gunicorn), nginx, CDN, load balancer, "
        "Django/Express/FastAPI middleware body/header behavior untested; localhost "
        "Werkzeug only.",
        "Concurrency, HTTP/2, TLS, multi-client handling untested.",
        "Non-degenerate bootstrap CI cannot be obtained on this deterministic substrate; "
        "body/header nondeterminism (e.g., real CDN) needed for genuine CI.",
        "Body magnitude gradient beyond 31/70/117 and per-field sensitivity ordering "
        "remain uncharacterized: all variants produced ceiling 1.0.",
        "Distributed SQLite replication / shared-session distributed C-FRESHNESS and "
        "C-DELTA-REPAIR remain blocked; this result unblocks localhost synthetic testing "
        "for both branches only (as specified in product_consequence_positive).",
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

    # ── provenance (written BEFORE result.json so result.json can reference
    #    provenance.json's real hash; provenance.json does not reference
    #    result.json — result.json is the terminal canonical file of EXECUTE) ──
    head = git_head()
    trigger = os.environ.get("GITHUB_SHA", "unavailable")

    provenance = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "github_run_id": "35756234169",
        "github_run_attempt": 1,
        "commits": {
            "request_base_sha": "21f749ffe2433ef3711887b35288e7f0216d4821",
            "freeze_commit": "dbc22b7455719d0bcf63e14ea48ec1cb6d5b4d84",
            "execution_base_sha": "8998cd0f160f3e5a7b6a81a36551eda8646fa761",
            "head_sha_at_execution": head,
            "github_trigger_sha": trigger,
        },
        "design_inputs": {
            "request.json_sha256": "622d624e32ae4d90e8d905f02d028000d0853105cc4af53d36a2d2677ba5e5bb",
            "spec.json_sha256": "eaedd7140a27c6362d29b66b15ed7965cade4a50d215e1ee49977de7d7ebc70d",
            "prereg.md_sha256": "78a5ec55dbce6f07a5ca1d7a11a3a78696cca1ccf865958e97e8e7098a3a893d",
            "freeze.json_sha256": sha256(OUT / "freeze.json"),
            "parent_handoff_sha256": "6e8a1eaa717dc59bfcdf4c0d464072ef1db429dffabe7bc2eef0d01ca56f6039",
        },
        "environment": {
            "python": platform.python_version(),
            "flask": "3.1.3",
            "pyjwt": "2.14.0",
            "requests": "2.34.2",
            "sqlite": "3.45.1",
            "platform": platform.platform(),
            "host": socket.gethostname(),
            "server_endpoint": "http://127.0.0.1:19849",
            "db_path": "/tmp/spider_bodydrift_testbed.db",
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
            "fixed_header_config": derived["fixed_header_config"],
            "bodies": {
                "A": {"len": 31, "sha256": "d0ca833f843c6d70ec9d6755f52a92dcbfc8b4ab601b871bced09ad027172e34"},
                "B": {"len": 70, "sha256": "67c186f2cee1ccf01f55c80235eb9b1b1d14b073223a807b9ce944405e67999c"},
                "C": {"len": 117, "sha256": "b46c461cceeefa595c3ac0d706689ed382340b59c20a269a930c786c8389dd32"},
            },
            "body_403": {"len": 22, "sha256": "387fe73d9abe7e6c32a0eb6113efea98dea609edefe9c3b4c9788fcaaef1603b"},
            "body_401": {"len": 25, "sha256": "9df366cd61d0e8a1bd9c4462d4f032e5317b2708d154047affa816e234518f34"},
            "batch_sequence": [
                "set_headers -> body_A -> body_B -> body_C -> null_A1 -> null_A2 -> "
                "null_C1 -> null_C2 -> perm_403 -> perm_200 -> perm403_null_1 -> "
                "perm403_null_2 -> sess_200 -> sess_401 -> sess401_null_1 -> "
                "sess401_null_2 (12 writable commits, 15 pre-batch verifies)"
            ],
        },
        "code_paths": [
            f"research/experiments/{EXPERIMENT_ID}/run_experiment.py",
            f"research/experiments/{EXPERIMENT_ID}/build_packet.py",
            "research/experiments/EXP-RUNTIME-35741906498/run_experiment.py (parent "
            "fingerprint algorithm source)",
        ],
        "commands": [
            "python3 run_experiment.py --smoke   # setup verification only",
            "python3 run_experiment.py           # full frozen execution",
            "python3 build_packet.py             # canonical packet emission",
        ],
        "artifacts": artifacts,
        "notes": [
            "Working tree contained pre-existing factory modifications (SPIDER_CODEX.md, "
            "codex/, research/lanes/runtime/state.json etc.) at execution time; none were "
            "touched by this EXECUTE stage.",
            "run_experiment.py and build_packet.py are uncommitted working-tree files; "
            "EXECUTE performs no git commit/push/switch/reset by policy.",
            "Attempt-1 run 35749360317 failed at exit 75 (failure.json, retryable); "
            "attempt-4 of an earlier retry run exited 1 transiently (model_execute.json); "
            "this run (35756234169, attempt 1) executed cleanly in one pass.",
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


if __name__ == "__main__":
    sys.exit(main())