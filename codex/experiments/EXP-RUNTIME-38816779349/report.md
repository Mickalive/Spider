# EXP-RUNTIME-38816779349 — EXECUTE report (runtime)

Repair-gated re-test: bulk-materialized localized repair vs cold re-derivation
at L=2/L=3 on both timed boundaries, with breadth/recurrence scaling.
Frozen design executed exactly; no re-design after outcomes.

## 1. Outcome

- `status=COMPLETE`, `outcome=INCONCLUSIVE`, frozen decision `INCONCLUSIVE`
  (marginal straddle: no re-admit, no permanent drop, thread parked).
- Class verdicts: P1-ENDPOINT `PRICED-MARGINAL`, P2-STRUCTURE `PRICED-WIN`,
  P3-PERMISSION `PRICED-MARGINAL`. No validity gate tripped
  (`invalid_reasons=[]`); this is a valid scientific non-decision, not a
  measurement failure.
- This packet is fully consistent with `result.json`; the JSON is the canonical
  handoff and this Markdown only explains it.

## 2. What was run

- Extracted the frozen v5 driver verbatim from `prereg.md` section-12
  (V1 canonical binding verified before the scored run) and executed it
  unmodified: 36 scored trials (3 classes x 12, fresh SEED5=162073685 bank,
  rotating targets), 2 untimed warmups per trial, gated parity 6/6 per class,
  diagnostic breadth episodes n=1/n=2 after the gated triple, NC trials,
  and family-wise Bonferroni bootstrap CIs (1-0.05/12, B=10000) over
  12 class x L x boundary cells.
- Treatment `T-REPAIR-REUSE-BULK`: identical episode semantics to the parent
  reuse arm except registry materialization is one `BulkArm`
  `MechanismRegistry.replace()` of the inherited set instead of N sequential
  `upsert()` read+rewrite cycles. Comparator `B-COLD`/`B-COLD-MIN` is the
  parent-identical `v2.Arm` cold path. Carrier bytes are byte-identical to the
  parent freeze (kernel `3a6caf97`, models `338aaf4d`, registry `51fb440d`,
  `__init__` `3d173722`; v2 runner `d4871091`, 60855 bytes).
- Raw evidence: `raw_evidence/driver_stdout.json` (36 trials + per-class
  metrics + attribution), `raw_evidence/runner_v5.py` (extracted frozen
  driver), `raw_evidence/liveness_only.json`, `raw_evidence/reachability_probe.json`.

## 3. RAW EVIDENCE vs OBSERVATION vs MEASUREMENT vs INTERPRETATION

- RAW EVIDENCE: per-trial episode latencies, phase timings, shipped counters,
  oplogs, guard verdicts, probe outcomes in `driver_stdout.json#trials`.
- OBSERVATION (direct, in `result.json#observations`): 36/36 valid trials;
  repair 36/36; guard 36/36 fired plus 36/36 fresh-silence plus 2/2 NC silent;
  literal-replay 0.0; cold 1.0; contamination 0/144; write max 1; shipped sums
  exact (204/216/228); 8 WIN + 4 MARGINAL cells with the stated ratios/CIs.
- DERIVED MEASUREMENT: medians, median ratios, bootstrap CI95 + Bonferroni
  family-wise CIs, Wilson lower bounds, N* crossovers, attribution set —
  computed by the frozen driver functions, recomputable by AUDIT from raw trials.
- INTERPRETATION (this report + `M-DECISION`): the pattern means the mandate
  question is NOT decided — see section 4. No interpretation is presented as
  raw observation anywhere in this packet.

## 4. Interpretation

- Functional/locality soundness (H1) is re-attested for the third time on this
  substrate/carrier: repair 1.0 (Wilson lower 0.7575), guard 1.0,
  write_set_max 1, contamination 0.0, live bitten and live insensitive controls.
- The removable tax is gone BY MEASUREMENT: S-REGISTRY-BUILD reuse medians fell
  from the parent 1.4866 ms to ~0.29 ms (cold ~0.045 ms; residual delta
  ~0.24 ms vs ~1.45 ms before). Registry content is pinned byte-identical
  (V-REG-EQUIV on every episode).
- With the tax removed, the empirical picture moved from the parent's six
  robust deficits (1.0235-1.2463) to zero robust deficits: 8/12 cells are robust
  reuse wins (every L3 cell on both boundaries plus all four P2 cells) and the
  remaining 4 cells (P1/P3 at L2) are near-1.00 straddles whose Bonferroni CIs
  span ~0.92-1.07. The NOARG boundary flips the P1/P3 L2 point estimates below
  1.00 (0.9950/0.9858), implicating the disclosed S-ARG deepcopy operand
  asymmetry (~0.10 ms reuse vs ~0.005 ms cold) as the residue at L2, but the CIs
  still straddle, so the frozen strict-robustness bar is not met there.
- Per the frozen falsifier, a straddle without any LOSS is INCONCLUSIVE:
  no re-admission to the C-PRODUCT-ECON story (SUPPORTS requires all 12 cells
  robustly below 1.00) and no permanent drop (DROP requires a robust LOSS).
  The mandate stop trigger does not fire. C-DELTA-REPAIR stays EXPERIMENTAL
  bounded to functional/locality soundness.
- Shipped-counter premise (H2) held exactly (17 vs 18/19, fetch ratios
  0.56-0.67) and is carried as a zero-variance drift-checked premise only,
  never as an empirical win. Attribution is MOOT (net L3 excess negative on all
  classes; no deficit to attribute). Breadth diagnostics show reuse latency
  improving as breadth narrows (n=1 ratios 0.68-0.76 at L3); recurrence N*
  at L3 is ~11-20 episodes.

## 5. Product consequence

`no-decision-no-drop-no-readmit`: localized repair is neither re-admitted to
nor permanently dropped from the C-PRODUCT-ECON story. No code promotion
(runtime lane; carrier byte-identical; harness-only BulkArm change measured,
not shipped). B3 real model-call/token economics remains an explicit recorded
blocker for any flagship product-economics claim.

## 6. Validity threats (see also `result.json#validity_notes`)

Localhost-only substrate with sub-millisecond gaps; wall-clock latency
measured, not deterministic; bootstrap tails coarse (~21 samples) but frozen
and deterministic; legacy-upsert warmup path (untimed, symmetric, V-RETAIN
enforced); vacuous B-NO-REPAIR gate disclosed; fixed n=2 breadth composition;
informational scaffold ratio excluded from the classifier; B3 unsatisfiable
by construction.

## 7. Unresolved

Whether P1/P3 L2 straddles resolve with larger N; why P2 wins at both L
while P1/P3 win only at L3 (S-REPAIR-SIGNAL class cost is a post-hoc
candidate, not a tested mechanism); any transfer beyond this
substrate/carrier/classes/counter; real model economics.
