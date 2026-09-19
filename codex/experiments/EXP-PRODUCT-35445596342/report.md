# EXP-PRODUCT-35445596342 — Execution Report (C-FRESHNESS orthogonality re-run)

- **experiment_id**: EXP-PRODUCT-35445596342
- **lane**: product
- **claim**: C-FRESHNESS
- **status**: COMPLETE
- **outcome**: SUPPORTS (frozen decision-rule wording: `SURVIVES_CURRENT_TEST`)
- **parent**: EXP-PRODUCT-35434772331 (MEASUREMENT_INVALID)

This run executes the EXACT frozen design (request/spec/prereg/freeze hashes
unchanged; see `provenance.json`). It does not modify production code. It
implements and measures the three frozen fixes for the C3 measurement
invalidity that blocked the parent experiment.

---

## 1. What was executed

All three frozen fixes, on a stochastic Flask 3.1.3 + SQLite WAL mock server
(`mock_server.py`) driven by `run_experiment.py`:

1. **Server replacement (fix 1)** — the deterministic WSGI server is replaced
   by a stochastic server matching EXP-GRAPH-35353011131: SQLite WAL DB for
   session/permission state, in-memory TTL cache (0.5 s) for the schema
   snapshot, I/O jitter 10–100 ms, mixed JWT algorithms (HS256 read/write,
   RS256 admin), random `X-Request-Id` per response.
2. **Scoring redesign (fix 2)** — `behavioral_score` is continuous and
   severity-weighted with distinct, non-overlapping per-drift ranges:
   permission_boundary [0.32, 0.545] (role + permission-count severity),
   token_refresh 0.65 (refresh + new-token signals), session_invalidation
   [0.75, 1.00] (session-invalid + revocation + graded status code
   401/403/500). No-drift baseline 0.05. Detection threshold 0.25.
3. **State reset (fix 3)** — `set_drift(None)` fully resets
   `current_role/session_valid/drift_active/drift_type/noise` and restores DB
   rows between every condition block; each condition starts from a verified
   clean state (control `CTL-STATE-RESET`).

Phases (all real HTTP on `127.0.0.1:18950`, seed 42, single-threaded server,
sequential client):

- A: C1 auth-state discrimination + baselines (40 probes, `/api/data`)
- B: 8 co-occurring conditions (2 drifts × 4 noises) × 60 = 480 paired
  samples (`/api/session/status` + `/api/schema`)
- C: 4 noise-only conditions × 60 = 240 samples (null control)
- D: 3 isolated drift types × 60 = 180 samples (TP test)
- E: pooled orthogonality (Pearson r + Fisher-z TOST, delta = 0.15)

---

## 2. Evidence layers

### RAW EVIDENCE
`raw_evidence/experiment_data.json` (sha256
`fc79a70f…`) contains every per-sample observable: behavioral score,
structural cardinality, HTTP status code, session-validity flag, schema
cache-status flag per condition, plus the raw phase-A HTTP responses.
`server_log.txt` is the access log.

### OBSERVATIONS (directly from the wire)
- Phase A: per-state fingerprints internally stable; expired_token and
  invalid_token share one surface (3 unique fingerprints of 4 states).
- Phase B: score ranges under co-occurring noise equal the isolated ranges
  (PB mean ≈ 0.45; SI mean ≈ 0.85–0.875). Noise does not move the means.
- Phase C: all 240 noise-only samples score exactly 0.05.
- Phase D: PB scores span 0.32–0.545, SI scores 0.75–1.0, TR fixed 0.65.

### DERIVED MEASUREMENTS (recomputed twice — by the driver and by an
independent script from the raw artifact alone; both agree exactly)
| Gate | Result | Frozen pass condition | Pass |
|---|---|---|---|
| C1 auth discrimination | 0.8333 (status-only 0.5; body-only 0.8333) | > 0.5 | ✓ |
| C2 TP isolated | 1.0 each (Wilson lower 0.9398) | ≥ 0.85 | ✓ |
| C2 TP co-occurring | 1.0 each (8/8) | ≥ 0.85 | ✓ |
| C3 variance | 8/8 conditions std > 0.05 (behav 0.087–0.104; struct 0.40–0.42) | ≥ 6/8 | ✓ |
| C3 orthogonality | r = −0.0258, CI [−0.115, 0.064], CI upper 0.064 < 0.15; TOST p_upper 5.6e-05, p_lower 3.1e-03 | CI upper < 0.15, p_upper < 0.05 | ✓ |
| C4 noise FP | 0.0 (240 samples) | ≤ 0.15 | ✓ |

### INTERPRETATION
- **The three root causes are fixed.** Behavioral variance is now real and
  within-condition (per-request permission-propagation sampling for PB;
  graded 401/403/500 status checks for SI), the score ranges are
  non-overlapping, and conditions do not contaminate one another.
- **Orthogonality at delta = 0.15 is reproduced** on the same methodology as
  EXP-GRAPH-35353011131 (same n = 480, same Fisher-z TOST; graph: r = 0.046,
  CI upper 0.135, p_upper 0.011 — this run: r = −0.026, CI upper 0.064,
  p_upper 5.6e-05). Both sit well inside the delta margin; the sign of the
  pooled r is noise, not mechanism.
- **Parallel channels justified at the frozen ceiling**: the claim is
  confirmed only for the localhost stochastic mock, HS256/RS256 JWT, delta =
  0.15, at the ceilings stated in prereg; no production generalization and no
  promotion are claimed here.

---

## 3. Determinism and verification

- Global RNG seeded at 42 before server start; werkzeug `threaded=False`;
  sequential client → the sample sequence is reproducible.
- Independent recomputation from `raw_evidence/experiment_data.json` (no
  HTTP) reproduced every metric in `result.json` exactly.
- Frozen input hashes in `provenance.json` match `freeze.json`.

## 4. Validity notes

- Bounded to localhost mock; zero LLM calls (prereg measurement_validity).
- token_refresh TP is deterministic by design (std 0.0) and is NOT part of
  the 8-condition orthogonality set; the C2 gate is a rate, not variance.
- C1 = 0.8333 (not 1.0) because expired ≡ invalid on purpose, replicating
  parent baselines; the frozen gate is > 0.5.
- PB behavioral std (0.087–0.099) is below the graph range (0.14–0.16) but
  above the 0.05 gate with ample TOST power.
- Full caveat list and open questions: `result.json` → `validity_notes`,
  `unresolved`.

## 5. Consequence for the claim

Per the frozen decision rule this is `SURVIVES_CURRENT_TEST` → canonical
`SUPPORTS`. The experiment resolves the single blocker (C3 measurement
invalidity) that prevented C-FRESHNESS from advancing. Whether the claim
moves toward PRODUCT_CORE and how product architecture proceeds is the
DIRECTOR's verdict decision, grounded on this packet plus the audit;
the producer does not self-promote claims.