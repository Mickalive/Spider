# EXP-RUNTIME-36106663091 execution report

- **Lane/claim:** `runtime` / `C-MEAS-VALID`
- **Measurement status:** `MEASUREMENT_INVALID`
- **Scientific outcome:** `INCONCLUSIVE`
- **Run timestamp:** `2026-09-25T08:14:42.459233+00:00`

## Scope and frozen decision
The distributed HTTP phase and any phases reached before the mandatory browser provisioning gate are reported exactly. Real browser capture did not complete, so no browser, writable, or downstream loopback/HIT claim is made. No synthetic browser or write path was used.

## Raw evidence
Raw observations are preserved in the JSONL artifacts listed in `result.json` and `provenance.json`. Browser-dependent raw artifacts are explicitly empty when the mandatory provisioning gate aborts execution; absence is not a negative scientific observation.

## Direct observations
- Two gunicorn origins and the exclusive nginx reverse proxy became ready on the frozen ports.
- Per-URI nginx requests produced stable worker assignment across the two origins.
- C1 captured 1000 plain HTTP observations through nginx, including 99 real 304 responses.
- Plain HTTP C2 paired observations: 160.
- Honest cost grouped 100 trajectories and performed 1000 trajectory-level permutations.

## Derived measurements

| Gate | Pass | Observed |
|---|---:|---|
| `C1` | `False` | `null` |
| `C2` | `False` | `null` |
| `C3` | `False` | `null` |
| `C4` | `False` | `null` |
| `C5` | `False` | `null` |
| `C6_BROWSER_HEALTH` | `False` | `null` |
| `C7_KMEANS` | `False` | `null` |
| `C8_WRITABLE` | `False` | `null` |

## Controls

| Control ID | Status | Observed |
|---|---|---|
| `B-DISTRIBUTED-HTTP-TRIPLE` | `UNKNOWN` | `{"C1": false, "C2": false, "C3": false, "C4": false, "C5": false}` |
| `B-BROWSER-DOM-AX-STRUCTURAL` | `UNKNOWN` | `{"browser_health_ax_median": null, "browser_health_dom_median": null, "browser_health_pc_health": null, "browser_health_viewport_ok": null}` |
| `B-WRITABLE-POSITIVE` | `UNKNOWN` | `{"writable_dom_delta_pos_rate": null, "writable_pos_rate": null, "writable_wal_pos_mutated_rate": null}` |
| `B-WRITABLE-NULL-READONLY` | `UNKNOWN` | `{"discrimination_rate": null, "dom_delta_mean": null, "wal_mutated": null}` |
| `B-WRITABLE-NULL-INVALID-AUTH` | `UNKNOWN` | `{"discrimination_rate": null, "dom_delta_mean": null, "wal_mutated": null}` |
| `B-WRITABLE-NULL-EXPIRED-AUTH` | `UNKNOWN` | `{"discrimination_rate": null, "dom_delta_mean": null, "wal_mutated": null}` |
| `B-WRITABLE-NULL-DELETED-SESSION` | `UNKNOWN` | `{"discrimination_rate": null, "dom_delta_mean": null, "wal_mutated": null}` |
| `B-WRITABLE-NULL-SAME-STATE` | `UNKNOWN` | `{"discrimination_rate": null, "dom_delta_mean": null, "wal_mutated": null}` |
| `B-TRAIN-ONLY-KMEANS` | `UNKNOWN` | `{"browser_kmeans_centroid_diff": null, "browser_kmeans_leakage_pass": null, "browser_kmeans_n_test": null, "browser_kmeans_n_train": null, "browser_kmeans_same_state_J": null}` |
| `B-HEADER-ONLY-JACCARD-STABLE-BROWSER` | `UNKNOWN` | `{"browser_header_only_jaccard_mean": null, "browser_header_only_jaccard_nullFP": null, "browser_header_only_jaccard_r": null, "browser_header_only_jaccard_same_state_J": null, "browser_header_only_jaccard_v": null}` |
| `B-FULL-VECTOR-BROWSER` | `UNKNOWN` | `{"browser_full_vector_body_only": null, "browser_full_vector_diff_lo": null, "browser_full_vector_full": null, "browser_full_vector_null": null, "browser_full_vector_status_only": null}` |
| `PC-REAL-BROWSER-PROVISIONED` | `UNKNOWN` | `{"agentlab_attempted": true, "agentlab_available": false, "agentlab_error": "ModuleNotFoundError(\"No module named 'agentlab'\")", "browsergym_core_import": true, "browsergym_import": true, "browsergym_version": "0.14.3", "compatibility_adapter_used": false, "native_path_helper": null, "native_path_helper_available": false, "native_path_helper_error": "required get_executable_path helper is absent", "nginx_started": true, "official_executable_path": "/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome", "playwright_version": "1.63.0", "token_creation": "HS256 with stable subject/session; no secret recorded in artifacts"}` |
| `NC-SYNTHETIC-FALLBACK-REJECTED` | `PASS` | `{"fallback_triggered": false, "real_page_interactions": false, "real_playwright_capture": false}` |

## Interpretation (bounded)

The measurement transaction was not sufficiently valid to support a scientific positive or negative conclusion. Missing or failed substrate operations remain unknown rather than being converted into falsification.

## Validity and unresolved threats

- Execution halted or was marked invalid because a required substrate/measurement operation failed: InfrastructureFailure('frozen Playwright provisioning gate failed: playwright._impl._path_utils.get_executable_path is unavailable')
- Mandatory frozen Playwright provisioning failed because the exact required playwright._impl._path_utils.get_executable_path helper was unavailable; the diagnostic public executable path was not substituted.
- Infrastructure failure: InfrastructureFailure('frozen Playwright provisioning gate failed: playwright._impl._path_utils.get_executable_path is unavailable')
- A later governed experiment would need a preregistered provisioning design compatible with the installed Playwright API; this immutable run cannot relax the helper requirement.

## Explicit unknowns

- TLS/HTTP2/QUIC, multi-host Redis, production CDN/edge, compressed encodings beyond greedy MAX_DEPTH5, timing-window header canonicalization, reboot durability, high write contention, task-level BrowserGym evaluation, and real-site generalization remain outside this experiment.
