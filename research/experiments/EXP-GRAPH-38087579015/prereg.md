# EXP-GRAPH-38087579015 preregistration

Lane: `graph`. Claim: `C-DELTA-REPAIR` (Registry status HYPOTHESIS; next_gate "controlled local perturbations with repair cost and contamination bounds"). Director mandate: cycle `38087062712`, action `CONTINUE`, `cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`. Legacy classification `DISTINCT_EXTENSION`. Design contract v2.

This preregistration is written before any substrate episode. DESIGN performed no confirmatory measurement. Only the synthetic stdlib satisfiability probe in `spec.json#pre_freeze_satisfiability_dry_run` was run; it measures no repair behaviour.

## 1. Objective

Measure, on a controlled credential-free stdlib-only multi-node substrate with an independently verifiable local-perturbation surface, whether a local delta-repair treatment (`T-LOCAL-DELTA-REPAIR`) repairs inherited knowledge affected by a bounded local change (blast radius 1-3) at a measured cost below an honest per-goal cold re-derivation (`B-COLD-REDERIVE`), while keeping contamination and false-accept below preregistered bounds, reporting per-family precision/recall, and containing every repair to the true blast radius. This is the first valid multi-node read of `C-DELTA-REPAIR`'s registry next gate.

## 2. Substrate

- N=3 independent loopback HTTP origins (`ThreadingHTTPServer`), each with its own canonical-JSON registry file; R=24 inherited records (8 per node); one deterministic stdlib router as the single client-facing entrypoint.
- Credential-free: every scored request is an idempotent GET; no auth/cookie/session/token/browser/network; no write verb is exposed to the system under test.
- Frozen candidate procedure space of size 8: the set of candidate endpoint/parameter templates an uninformed agent must search to re-derive a goal's procedure.
- Perturbation families: FIELD (radius 1, includes a surface-ambiguous sub-stratum), ENDPOINT (radius 1-2), TRANSPORT (radius 1-3), LEGIT (legitimate update control), NO-PERT (no change). PERMISSION is NOT_APPLICABLE on a credential-free substrate and is declared, not dropped.
- Out-of-band perturbation controller plus an independent verifier that share no localization code with the treatment, and that recompute the true blast radius and ground-truth values from retained pre/post registry sha256 snapshots.
- Single frozen seed 38087579015 drives all assignment via `random.Random(seed)`.

## 3. Arms

- `T-LOCAL-DELTA-REPAIR` (treatment): retrieve inherited mechanism, bind+execute (using `src.spider.kernel._bind`), verify (`_matches`), localize the minimal cell set, re-fetch only the affected item, apply a minimal registry mutation, re-verify. On the ambiguous stratum it may pay to disambiguate, abstain (UNKNOWN), or risk error.
- `B-COLD-REDERIVE` (primary comparator): honest per-goal cold re-derivation with an empty inherited store — search the frozen 8-member candidate procedure space, bind params, read and verify the value for the SAME goal.
- `B-NOOP-STALE` (null / inherit-without-repair ablation): serve inherited knowledge unchanged.
- `B-FULL-REFRESH` (cost extreme): on any detection, refresh the entire 24-record corpus.
- `B-LOCAL-ORACLE` (definitional floor): given the true delta, serve the answer and apply only the minimal mutation (no detection, no localization). Not a scientific arm.

All arms share identical counter instrumentation and the identical paired scored suite (72 episodes).

## 4. Counters and primary metric

Counters per scored episode: `http_requests`, `retrieval_calls`, `verification_calls`, `repair_attempts`. `M_COST_L1_X` is their sum; `M_COST_RATIO = M_COST_L1_T-LOCAL-DELTA-REPAIR / M_COST_L1_B-COLD-REDERIVE`, with a paired-bootstrap 95% upper bound `M_COST_RATIO_UPPER` over episodes. Client-boundary counters are cross-checked against raw per-request logs.

## 5. Frozen decision rule

1. GATE-V: if any blocking validity check (V02-V09, V11) fails, or any positive control fails, or any null control is insensitive, then `MEASUREMENT_INVALID` / INCONCLUSIVE — explicitly NOT a scientific negative.
2. SUPPORTS iff `M_COST_RATIO <= 0.70` AND `M_COST_RATIO_UPPER < 1.0` AND `M_CONTAMINATION <= 0.05` AND `M_FALSE_ACCEPT <= 0.05` AND min per-family recall (FIELD, ENDPOINT, TRANSPORT) `>= 0.90` AND `M_FALSE_REPAIR_LEGIT <= 0.05` AND `M_BLAST_RADIUS_CONTAINMENT == 1.0` AND `M_CROSS_NODE_CONTAMINATION == 0.0`.
3. FALSIFIES-COST iff `M_COST_RATIO >= 1.0` (LOCAL-REPAIR-NO-WORK-SAVED).
4. FALSIFIES-QUALITY iff `M_CONTAMINATION > 0.20` OR min per-family recall `< 0.50` (REPAIR-LEAKY).
5. FALSIFIES-CONTAIN iff `M_BLAST_RADIUS_CONTAINMENT < 1.0` OR `M_CROSS_NODE_CONTAMINATION > 0.0` (REPAIR-OVERREACH).
6. MIXED otherwise.

Threshold justification: the oracle floor (B-LOCAL-ORACLE aggregate) is ~0.606 and the no-localization extreme (B-FULL-REFRESH) is ~4.64, so the support threshold 0.70 lies strictly inside the open interval (neither tautological nor unreachable). Reachability witnesses are recorded in `spec.json#pre_freeze_satisfiability_dry_run` (SUPPORTS ~0.664; FALSIFIES-COST >= 1.0; FALSIFIES-QUALITY contamination 0.236 / recall 0.333; FALSIFIES-CONTAIN via B-FULL-REFRESH; MIXED at 0.664 with contamination 0.12).

## 6. Controls

Positive: PC-DETECT-CANARY (canary recall == 1.0), PC-COST-CANARY (cold strictly above oracle), PC-REPAIR-SEMANTICS (given-delta output byte-equal to ground truth). Null: NC-NOOP-NO-PERTURBATION (no spurious mutation), NC-LEGIT-NO-REPAIR (legitimate updates not "repaired"), NC-INSTRUMENT-SENSITIVITY (B-NOOP-STALE contamination above bound while B-COLD-REDERIVE reaches 0), NC-VERIFIER-INDEPENDENCE, NC-CONTAMINATION-BYTE-EXACT.

## 7. Validity and interpretation boundaries

Contamination, precision, recall, false-accept and containment are scored against independently recomputed ground truth, never treatment self-report. Determinism, raw-evidence retention and freeze-integrity are blocking. This is a synthetic controlled substrate: no Web-prevalence statement (SB-01); no Product Core promotion (SB-05); no generalization beyond blast radius 1-3 or the frozen families (SB-06); MEASUREMENT_INVALID is operational, not falsification (SB-08). The bound artifact `src/spider/kernel.py` is used only for verification/binding semantics and is immutable for the transaction.

## 8. Consequences

- Positive (SUPPORTS): bounded, auditable work-avoided ratio and a contamination envelope for local delta repair; decision-relevant input to whether to build delta-repair instrumentation. No status change is made here; DIRECTOR decides.
- Negative/Mixed (FALSIFIES-*, MIXED): closes the prior single-node positive as non-transferable, redirects effort to the critical path (shipped parameterized carrier / non-degenerate benchmark).
- Measurement-invalid: no scientific consequence; fix at the control-plane/substrate level.

## 9. Out of scope

No C-FRESHNESS / C-PARAM-INHERIT / C-RESIDUAL-NOVELTY / C-LLM-INHERIT / C-SEMANTIC-RESOLVE / C-MEAS-VALID / C-PRODUCT-ECON / C-CROSSSITE event; no web anchor contact; no kernel modification; no promotion.

## 10. Distinctness

This is a DISTINCT_EXTENSION from the pre-2.0 repair-round artifacts (they repaired rejected experiment runs/orchestration), from the prior R2 single-node (EXP-GRAPH-36018188168, definitional ceiling) and distributed (EXP-GRAPH-36106653880, MEASUREMENT_INVALID) packets, and from the never-frozen predecessor EXP-GRAPH-38085175893. The measured object and the primary comparator (honest per-goal cold re-derivation) are new.
