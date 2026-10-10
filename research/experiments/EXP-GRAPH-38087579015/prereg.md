# EXP-GRAPH-38087579015 preregistration

Lane: `graph`. Claim: `C-DELTA-REPAIR` (Registry status HYPOTHESIS; next_gate "controlled local perturbations with repair cost and contamination bounds"). Director mandate: cycle `38087062712`, action `CONTINUE`, `cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`. Legacy classification `DISTINCT_EXTENSION`. Design contract v2.

This preregistration is written before any substrate episode. DESIGN performed no confirmatory measurement. Only the synthetic stdlib satisfiability probe in `spec.json#pre_freeze_satisfiability_dry_run` was run; it measures no repair behaviour.

## 1. Objective

Measure, on a controlled credential-free stdlib-only multi-node substrate with an independently verifiable local-perturbation surface, whether a local delta-repair treatment (`T-LOCAL-DELTA-REPAIR`) repairs its inherited **mirror** knowledge when the **world** has changed under a bounded local perturbation (blast radius 1-3), at a measured cost below an honest per-goal cold re-derivation (`B-COLD-REDERIVE`), while keeping contamination and false-accept below preregistered bounds, reporting per-family precision/recall and false-accept, keeping legitimate updates from being misclassified as repairs, and containing every repair to the true blast radius. This is the first valid multi-node read of `C-DELTA-REPAIR`'s registry next gate.

## 2. Substrate: world and mirror

- **World**: N=3 independent loopback HTTP origins (`ThreadingHTTPServer`), each with its own canonical-JSON registry file; R=24 inherited records (8 per node); one deterministic stdlib router as the single client-facing entrypoint. The world changes ONLY through the out-of-band perturbation controller; the system under test is **GET-only and never writes the world** (V09).
- **Mirror store**: the treatment's inherited client-side knowledge, cells keyed `(node_id, record_id, field_id)`. This is the only object any arm mutates. A "repair" rewrites the minimal changed mirror cells to the world's current canonical value; the **served answer** for an episode is the reconciled mirror value.
- Credential-free: every scored request is an idempotent GET; no auth/cookie/session/token/browser/network; no write verb is exposed to the system under test.
- Frozen candidate procedure space of size 12: the set of candidate endpoint/parameter templates an uninformed agent must search to re-derive a goal's procedure (`B-COLD-REDERIVE` searches it; the treatment inherits the correct member).
- Perturbation families: `CLS-A` FIELD classification-ambiguous (9), `CLS-B` FIELD clean (15), `ENDPOINT` (12), `TRANSPORT` (12), `LEGIT` legitimate-update control (15), `NO_PERT` (9). PERMISSION is NOT_APPLICABLE on a credential-free substrate and is declared, not dropped (SB-02).
- `CLS-A` and `LEGIT` present the **identical** primary signal (changed value, shape-invariant schema, normal transport); they are distinguishable only via a per-record provenance token on `/meta/{record_id}`, read at a bounded extra cost (+1 GET, +1 verification).
- Out-of-band perturbation controller plus an independent verifier that share no localization code with the treatment, and that recompute the true blast radius (mirror-cell set) and ground-truth values from retained pre/post registry sha256 snapshots.
- Single frozen seed 38087579015 drives all assignment via `random.Random(seed)`. The treatment receives only the goal `record_id` — never the family label, the round schedule, or the delta.

## 3. Arms

- `T-LOCAL-DELTA-REPAIR` (treatment): mirror lookup; fetch+verify the goal with the frozen primitive (`src.spider.kernel._matches`/`_bind`); on conformance serve the mirror value; on a shape-distinct mismatch localize the minimal mirror cells (one verification probe per candidate cell), rewrite only those cells, re-verify; on a shape-invariant mismatch or the LEGIT family read the provenance token and either refresh (token bumped; legitimate update) or repair (token unchanged). May abstain (UNKNOWN), which lowers recall.
- `B-COLD-REDERIVE` (primary comparator): honest per-goal cold re-derivation with an empty mirror store — search the frozen 12-member candidate procedure space with first-success stopping, bind params, read and verify the value for the SAME goal.
- `B-NOOP-STALE` (null / inherit-without-repair ablation): serve inherited mirror knowledge unchanged.
- `B-FULL-REFRESH` (cost/containment extreme): on any detection, refresh the entire 24-record mirror corpus.
- `B-LOCAL-ORACLE` (definitional floor): given the true delta and its class, serve the answer and apply only the minimal mirror write (no detection, no search, no token). Not a scientific arm.

All arms share identical counter instrumentation and the identical paired scored suite (72 episodes).

## 4. Counters and primary metric

Counters per scored episode: `http_requests`, `retrieval_calls`, `verification_calls`, `repair_attempts` (mirror-store writes). `M_COST_L1_X` is their sum; `M_COST_RATIO = M_COST_L1_T-LOCAL-DELTA-REPAIR / M_COST_L1_B-COLD-REDERIVE`, with a paired-bootstrap 95% upper bound `M_COST_RATIO_UPPER` over episodes (descriptive robustness, not a significance test). Client-boundary counters are cross-checked against raw per-request logs. The one-time inheritance-acquisition cost (72 L1) is recorded in full but excluded from the primary ratio; it is reported as `M_COST_RATIO_WITH_WARMUP`.

## 5. Frozen decision rule

1. GATE-V: if any blocking validity check (V02-V09, V11) fails, or any positive control fails, or any null control is insensitive, then `MEASUREMENT_INVALID` / INCONCLUSIVE — explicitly NOT a scientific negative.
2. SUPPORTS iff `M_COST_RATIO <= 0.70` AND `M_COST_RATIO_UPPER < 1.0` AND `M_CONTAMINATION <= 0.05` AND `M_FALSE_ACCEPT <= 0.05` AND min per-family recall (FIELD, ENDPOINT, TRANSPORT) `>= 0.90` AND min per-family precision `>= 0.80` AND `M_FALSE_REPAIR_LEGIT <= 0.05` AND `M_BLAST_RADIUS_CONTAINMENT == 1.0` AND `M_CROSS_NODE_CONTAMINATION == 0.0`.
3. FALSIFIES-COST iff `M_COST_RATIO >= 1.0` (LOCAL-REPAIR-NO-WORK-SAVED).
4. FALSIFIES-QUALITY iff `M_CONTAMINATION > 0.20` OR min per-family recall `< 0.50` OR min per-family precision `< 0.60` OR `M_FALSE_REPAIR_LEGIT > 0.20` (REPAIR-LEAKY-OR-DESTRUCTIVE).
5. FALSIFIES-CONTAIN iff `M_BLAST_RADIUS_CONTAINMENT < 1.0` OR `M_CROSS_NODE_CONTAMINATION > 0.0` (REPAIR-OVERREACH).
6. MIXED otherwise.

Threshold justification: the oracle floor (`B-LOCAL-ORACLE`) is 0.2308 and the no-localization extreme (`B-FULL-REFRESH`) is 3.9231 under the frozen honest unit model, so the support threshold 0.70 lies strictly inside the open interval (neither tautological nor unreachable). Reachability witnesses are recorded in `spec.json#pre_freeze_satisfiability_dry_run` (SUPPORTS 0.4808; FALSIFIES-COST 1.25 / 3.9231; FALSIFIES-QUALITY contamination 0.875, false-repair 1.0, precision 0.458; FALSIFIES-CONTAIN via `B-FULL-REFRESH` containment 0.0; MIXED cold space-7 ratio 0.7812 or false-repair 0.133 at a cost win).

## 6. Controls

Positive: PC-DETECT-CANARY (canary recall == 1.0), PC-COST-CANARY (cold strictly above oracle), PC-REPAIR-SEMANTICS (given-delta mirror state byte-equal to ground truth), PC-FALSE-REPAIR-CANARY (false-repair metric reads 0.0 clean / 1.0 greedy on the same fixture). Null: NC-NOOP-NO-PERTURBATION (no truth-changing write on NO_PERT), NC-INSTRUMENT-SENSITIVITY (B-NOOP-STALE contamination > 0.20 while B-COLD-REDERIVE reaches 0), NC-FALSE-REPAIR-SENSITIVITY (false-repair metric fires in both directions on a fixture), NC-VERIFIER-INDEPENDENCE, NC-CONTAMINATION-BYTE-EXACT, NC-WORLD-IMMUTABILITY (node registries unchanged except by the controller).

## 7. Validity and interpretation boundaries

Contamination, precision, recall, false-accept, false-repair and containment are scored against independently recomputed ground truth in mirror-cell coordinates, never treatment self-report. Determinism, raw-evidence retention, world immutability and freeze-integrity are blocking. This is a synthetic controlled substrate: no Web-prevalence statement (SB-01); no Product Core promotion (SB-05); no generalization beyond blast radius 1-3 or the frozen families (SB-06); MEASUREMENT_INVALID is operational, not falsification (SB-08). The bound artifact `src/spider/kernel.py` (sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`) is used only for verification/binding semantics and is immutable for the transaction. Objects of repair are the mirror's own cells; the world is never written by the system under test.

## 8. Consequences

- Positive (SUPPORTS): a bounded, auditable work-avoided ratio plus a contamination/false-accept/false-repair envelope and per-family precision/recall for local delta repair; decision-relevant input to whether to build delta-repair instrumentation. No status change is made here; DIRECTOR decides.
- Negative/Mixed (FALSIFIES-*, MIXED): closes the prior single-node positive as non-transferable and redirects effort to the critical path (shipped parameterized carrier / non-degenerate benchmark).
- Measurement-invalid: no scientific consequence; fix at the control-plane/substrate level.

## 9. Out of scope

No C-FRESHNESS / C-PARAM-INHERIT / C-RESIDUAL-NOVELTY / C-LLM-INHERIT / C-SEMANTIC-RESOLVE / C-MEAS-VALID / C-PRODUCT-ECON / C-CROSSSITE event; no web anchor contact; no kernel modification; no promotion.

## 10. Distinctness

DISTINCT_EXTENSION, stated honestly. The closest pre-2.0 precedent is `FRONTIER:frontier-scoped-delta-repair` (charter sha256 `4fe3e4a0042d5c0b28ee5bf554b4486c8eca4d65`, prereg `498a1649ae3ba6975ddc68903900fc63b0135882`, verdict `42a4c8c127b6509704a6da283b1127ff6251e554`, SURVIVES_CURRENT_TEST, PROOF_OF_CONCEPT ceiling), which measured scoped-blind repair versus full relearning on one deterministic synthetic shop in simulated actions across 5 disjoint single-segment mutations (n=5, no significance claim, zero corruption events). That precedent had no HTTP/verification/repair counter economics, no observationally-ambiguous stratum, no legitimate-update control, no contamination/false-accept/false-repair rates, and no multi-origin containment. The pre-2.0 graph repair-round artifacts (`results/graph/cycle3_REPAIR_ROUND1_recount.json` `f2239dd8dfb2f4744895bb9c3a6495646cfab31c`; `results/graph/fused_REPAIR_ROUND1_recount.json` `c7a052ea28929a9a62813b230480118d209eccde`; `reports/graph/robustness_repair_round1.md` `032c11f915eb4b235f2cba0fd907f9a81a0122b7`; `reports/graph/procedure_compilation_p0.md` `12eac599c2e907e442f74d48625bf404b259a74f`) concern repairing rejected experiment runs / orchestration. The prior R2 single-node (`EXP-GRAPH-36018188168`, definitional ceiling) and distributed (`EXP-GRAPH-36106653880`, MEASUREMENT_INVALID) packets and the never-frozen predecessor `EXP-GRAPH-38085175893` are superseded. The measured object, the comparator and the counter economics are new.
