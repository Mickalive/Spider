# EXP-RUNTIME-35913894863 — Execution Report

**Status:** MEASUREMENT_INVALID
**Outcome:** INCONCLUSIVE
**Lane:** runtime
**Claims:** C-MEAS-VALID, C-FRESHNESS
**Reason:** Infrastructure substrate failure — not a scientific falsification

## Infrastructure Failure Summary

The Flask + gunicorn + nginx substrate could not be brought up within the health-gated startup window (15s). Gunicorn failed to import the Flask app module via `run_experiment:app` reference because the module-level `app = create_app(...)` executes `init_db()` before gunicorn workers can properly set `SPIDER_DB_PATH`. This caused the health gate (`GET /health` via nginx returning 200+X-Worker-Pid) to fail.

Per the packet contract (section 1): **infrastructure or substrate failure must never be encoded as scientific falsification.** All six measurement hardenings remain untested.

## Distributed C-FRESHNESS (B-SHARED-STORE primary)

| Metric | Value | Target |
|--------|-------|--------|
| freshness_c1_tn_mean | 0.0000 | >=0.85 |
| freshness_n_non304 | 0 | >=800 |
| freshness_hs256_valid_success_rate | 0.0000 | >=0.90 |
| batch_state_log distinct_ts | 0 | >=27 |

### B-PER-NODE baseline
| per_node_tn_mean | 0.0000 | <0.85 |

### B-STICKY-URL
| sticky_tn_mean | 0.0000 | >=0.85 |

### Honest-cost
| |rho_shuffled| | 0.0000 | <0.20 |

### HIT byte-preserving
| HIT/DYNAMIC byte-identical | N/A | 330/330 |

### Browser
| bg_ax_nodes_median | 0 | >10 |
| bg_pc_health_pct | 0 | >=80 |

## Controls

| Control | Pass |
|---------|------|
| C1-FRESHNESS | null (HEALTH_GATE_FAILED) |
| C2-FRESHNESS | null (HEALTH_GATE_FAILED) |
| C3-FRESHNESS | null (HEALTH_GATE_FAILED) |
| C4-FRESHNESS | null (HEALTH_GATE_FAILED) |
| C7-HONEST-COST | null (HEALTH_GATE_FAILED) |
| C8-HIT-NGINX | null (HEALTH_GATE_FAILED) |
| B-PER-NODE | null (HEALTH_GATE_FAILED) |
| B-STICKY-URL | null (HEALTH_GATE_FAILED) |
| V-HEALTH-GATE | **false** |
| C5-BROWSER | null (HEALTH_GATE_FAILED) |

## Validity Notes

- HEALTH_GATE_FAILED: nginx+gunicorn did not respond with 200+X-Worker-Pid within 15s
- Infrastructure substrate unavailable: gunicorn import of run_experiment:app failed
- This is an infrastructure/substrate failure, NOT a scientific falsification
- All six measurement hardenings remain untested

## Unresolved (All six hardenings remain UNKNOWN)

1. Whether shared WAL header-only Jaccard MINUS body-derived achieves C1 TN>=0.85 with health-gated HS256>=32
2. Whether per-trajectory-reset honest sum counters achieve |rho_shuffled|<0.20 B=5000 trajectory-grouped
3. Whether sticky URL-bound hash $request_uri >=10 URIs achieves TN>=0.85 skew>0.90
4. Whether nginx HIT byte-preserving 330/330 with oracle-free greedy MAX_DEPTH5 holds
5. Whether BrowserGym 1280x720 CDP AX>10 with non-deterministic pool yields non-degenerate B=1000 CIs
6. Production CDN HIT byte-preserving (free-tier ceiling)

## Required Fix for Next Execution

- Use `gunicorn --chdir <dir> run_experiment:app` with proper WSGI module import
- Or start gunicorn with `python -c "from run_experiment import app; app.run()"`
- Fix nginx proxy_cache_path directory permissions
- Ensure module-level `app = create_app(...)` does not call `init_db()` before gunicorn workers can set environment variables
