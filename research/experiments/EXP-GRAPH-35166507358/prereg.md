# EXP-GRAPH-35166507358 Preregistration

## Experiment Identity

- **Experiment ID**: EXP-GRAPH-35166507358
- **Lane**: graph
- **Claim**: C-FRESHNESS (SPIDER can detect when inherited knowledge is stale)
- **Parent**: EXP-GRAPH-35155716123 (MEASUREMENT_INVALID — behavioral signals computed analytically, not from HTTP)
- **Parent carry_forward preserved**: Six structural signal families falsified; behavioral signals untested on real HTTP; magnitude confound identified; block-zero orthogonality artefact identified.

## Question

Can session-level behavioral signals measured from real HTTP requests on a Flask+PyJWT HS256 server detect auth-state drift (TP>=0.9) while tolerating structural noise (FP<=0.15), and does the C4 orthogonality criterion survive when both behavioral and structural signals are measured on the same co-occurring drift+noise conditions without block-zero imputation?

## Hypothesis

Session-level behavioral signals — token validation failure rate (jwt.decode vs current signing key), session cookie validity (server-side session store lookup), and HTTP 401/403 boundary probing — detect auth-state drift with TP >= 0.90 and produce FP <= 0.15 on structural noise that does not affect auth state. When both behavioral and structural signals are measured on conditions where both are non-trivially present (co-occurring drift+noise), Pearson r < 0.3, demonstrating genuine orthogonality rather than block-zero artefact.

## Falsifier

Behavioral signals fail to detect auth drift (TP < 0.90), or produce high FP on structural noise (FP > 0.15), or Pearson r >= 0.3 on co-occurring drift+noise conditions (non-trivial orthogonality), or AUC <= 0.80. If behavioral signals also fail the C-FRESHNESS gate on real HTTP, the domain has exhausted all single-signal-family approaches in deterministic/mock settings.

## State Representation

- **Behavioral signals**: Three-dimensional feature per request: (token_validation_rate, session_state_change, auth_boundary_shift)
  - token_validation_rate: fraction of requests where jwt.decode() raises an exception (InvalidSignatureError, DecodeError, ExpiredSignatureError)
  - session_state_change: binary — 1 if Set-Cookie header present indicating new session, 0 otherwise
  - auth_boundary_shift: count of endpoints returning 401/403 (out of 3 probed: read, write, admin)
- **Structural signals**: Two features per condition: (1 - Jaccard_similarity, schema_diff_magnitude)
  - Jaccard: Jaccard index of (field_name, field_type) pairs between current and baseline response schema
  - schema_diff: weighted diff magnitude (add/remove=1.0, type change=0.5, description change=0.3)
- **Composite behavioral**: token_validation_rate + session_state_change + auth_boundary_shift (sum, range 0-3)

## Action Representation

- Drift patterns change ONLY auth state; structural properties of response payloads remain constant
- Noise patterns change ONLY structural properties; auth state remains constant
- Co-occurring patterns change BOTH auth state AND structural properties simultaneously

## Target

Binary drift-vs-noise classification: each condition labeled DRIFT or NOISE. Behavioral composite score used for AUC computation.

## Sampling Policy

- 30 independent request sequences per condition
- Each sequence: 3 API calls (read, write, admin) with token in Authorization header
- Token expiry timing jitter: ±1s uniform on base expiry
- Session TTL variation: 5-15s uniform
- Permission probe ordering: randomized per sequence
- Deterministic seed: SEED=42 for all RNG; each sequence uses seed + sequence_index
- Wilson 95% CIs for per-condition TP and FP rates
- Bootstrap 95% CI (1000 resamples) for AUC

## Unit of Analysis

Each (pattern, schema_size, sequence_index) triple = one observation. 45 patterns × 5 sizes × 30 sequences = 6750 total observations.

## Holdout

- 80/20 train/test split by condition (not by sample within condition)
- Structural signals computed on ALL conditions for baseline comparison
- Behavioral signals computed on ALL conditions for AUC
- Orthogonality test (C4) uses only co-occurring drift+noise conditions (NOT held out — this is a descriptive statistic, not a prediction)

## Nulls and Baselines

1. **B-RANDOM**: Random classifier, expected AUC=0.50
2. **B-STRUCTURAL-JACCARD**: Jaccard structural similarity, re-measured on this experiment's conditions
3. **B-STRUCTURAL-SCHEMA-DIFF**: Schema diff magnitude, re-measured on this experiment's conditions
4. **B-NULL-SHUFFLE**: Permutation null — labels shuffled 1000× to establish chance-level AUC

## Primary Metric

AUC of behavioral composite score on drift-vs-noise discrimination, computed on conditions where both behavioral and structural signals are non-trivially measured.

## Expected Direction

Behavioral AUC > 0.80 (drift produces higher behavioral composite than noise)

## Uncertainty Method

- Wilson CIs for per-condition TP and FP rates
- Bootstrap 95% CI (1000 resamples) for AUC
- Permutation test (1000 shuffles) for Pearson r significance

## Adequacy Rule

- Minimum 30 independent sequences per condition
- Minimum 3 co-occurring drift+noise conditions for C4
- All 5 drift patterns and 4 noise patterns tested across 5 schema sizes

## Decision Rule (frozen)

ALL of C1-C5 must pass for SURVIVES_CURRENT_TEST:

**C1 (drift detection)**: Mean TP rate >= 0.90 across 25 drift conditions, Wilson lower CI > 0.85 at each condition.

**C2 (noise tolerance)**: Mean FP rate <= 0.15 across 20 noise conditions, Wilson upper CI < 0.25 at each condition.

**C3 (discrimination)**: AUC >= 0.80 across all 45 conditions, bootstrap 95% CI lower bound > 0.70.

**C4 (non-trivial orthogonality)**: Pearson r between behavioral composite and best structural signal (Jaccard or schema_diff) < 0.3, computed ONLY on conditions where both signals are non-zero (co-occurring drift+noise conditions, or per-sample variation within drift conditions where structural is also measured). NOT on block-zero imputed vectors.

**C5 (positive control)**: Signing-key-rotation produces token_validation_rate=1.0 on 30/30 rotated-key requests.

If C1 or C2 fails: **FALSIFIES** behavioral signals for C-FRESHNESS in this setting.
If C3-C5 pass but C1-C2 fail: behavioral signals detected but not reliable enough for gate.
If C1-C2 pass but C4 fails: behavioral signals work but are not genuinely orthogonal.
If C1-C2 pass but C5 fails: measurement validity concern.

## Measurement Validity Requirements

1. Flask server must be a real subprocess, not mocked/imported
2. JWT tokens must be issued via jwt.encode() and validated via jwt.decode() — real cryptographic operations
3. Session cookies must use real Flask server-side session store
4. All behavioral signals derived from actual HTTP request/response cycles, not from code inspection or pattern names
5. Structural signals computed from actual response bodies, not from schema definitions
6. Per-sample variation within conditions (not zero-variance deterministic)
7. Co-occurring drift+noise conditions included (not clean separation only)

## Product Consequence

- **Positive**: New validated detection dimension for freshness guards; behavioral signals integrated into pipeline
- **Negative**: Domain exhausted at single-signal-family level; pivot to real-API or composite multi-signal approaches required
