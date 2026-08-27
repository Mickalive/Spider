# INDEPENDENT AUDIT — PHYSICS LANE, CYCLE 1 (GitHub run 32676578274)

Auditor: Independent Auditor, Physics lane. Date: 2026-08-24.
Team branch audited: completed team workspace `/tmp/spider_physics_team`
(head `d22aa83`, "Physics WP-003B-R2: FALSIFIED verdict with full evidence").
Base under audit write-scope: current checkout (`lab/physics` accepted state).
Subject: WP-003B-R2 — action-conditioned next-state structure under true
website holdout. Team verdict: **FALSIFIED**.

Audit method: code + artifact inspection, git forensics on the freeze
timeline, sha256 verification of the committed dataset, and a full
INDEPENDENT RECOMPUTATION of every headline number from the committed data
using a from-scratch implementation (`/tmp/opencode/audit_r2/recompute.py`)
that imports no team analysis code.

---

## 1. Claims checked and statuses

### C1. Dataset `wp003b_r2_v1`: 681 collected / 564 confirmed / 117 not-ok; per-site counts as reported — **VALIDATED_FOR_CURRENT_TEST**
- Committed `data/physics/wp003b_r2_transitions.jsonl.gz` sha256
  `eff6928b…ea439` and uncompressed sha256 `ab8b93ca…6600` match
  `data/manifests/wp003b_r2_dataset_manifest.json` exactly; 681 rows.
- Recomputed from the file: confirmed = 564, excluded = 117; per-site
  confirmed books 120 / quotes 120 / internet 52 / wikipedia 101 /
  hackernews 15 / gutenberg 118 / openlibrary 38 — matches results JSON.
- Timestamp forensics: all rows collected 01:04:38–01:33:52 UTC in the
  driver's site order; single seed base 20260824 across ALL rows including
  not-ok ones (no v1-instrument contamination visible in committed data).
- Internals consistent with real browser collection: pre(t+1) == post(t)
  for 625/625 contiguous steps; all 117 not-ok rows have url_changed=False;
  failure anatomy is site-plausible (openlibrary 82 failed executions,
  mostly click/select/check).

### C2. Target integrity: no post-state/target leakage into predictors — **VALIDATED_FOR_CURRENT_TEST**
- Collector computes `pre_feat = features(cur)` before action selection and
  execution; `post_feat = features(post)` after (`physics/collector.py`
  lines ~173–195). Post-only fields (url_changed, load_ms, n_elements_post,
  DOM digests) are stored but NOT used in any feature block.
- The WP-003 leak vector is structurally absent: `prev_action_label` is the
  previous transition's primary action (validated by step-contiguity
  alignment on the full corpus: 0 violations), and it is not used as a
  feature at all in the R2 analysis. Action conditioning uses only labels of
  the CURRENT chain (first/last), which are fixed before s_{t+1} exists.
  Guard prev==target rate on non-start rows: 0.541 (< 0.98 assertion).
- G1 identity/alignment independently reproduced on all 681 rows: PASS.

### C3. Split integrity: leave-one-site-out, train-only vocabularies, no cross-fold content — **VALIDATED_FOR_CURRENT_TEST**
- Fold construction asserts train/test site disjointness; each trajectory
  belongs to exactly one site (checked).
- Train-vocab rule (support >= 3) applied to TRAIN rows only; scored test
  subset = test rows whose class is in train vocab; coverage reported per
  fold (quotes 0.5917, others 1.0; gutenberg 0 → skipped; hackernews n=8
  scored → inadequate). Harsh variant counting exclusions as errors for
  every predictor is reported. No post-hoc outcome-based filtering found.
- Minor (non-blocking): the one-hot vocabulary for action blocks
  (`first=`/`last=` labels) and the global 13-class label space are derived
  from the pooled confirmed corpus, i.e., mildly transductive encoding. This
  cannot manufacture the negative result, but any future POSITIVE claim must
  fit encoders/vocabularies on train folds only.

### C4. Headline arithmetic: mean D = −0.5016; grouped-bootstrap 95% CI [−0.6467, −0.3153]; fold wins 0/5; verdict FALSIFIED — **VALIDATED_FOR_CURRENT_TEST (bit-exact reproduction)**
Independent recomputation reproduces, to the reported precision:
- All five adequate folds' balanced accuracies for M_SA, M_S, N_MAJ,
  N_PERSIST, N_NN_Z, N_NN_ZA (e.g. books M_SA 0.200 vs PERSIST 0.4698;
  wikipedia M_SA 0.000 vs PERSIST 0.8968);
- D_f = {−0.2698, −0.4177, −0.913, −0.0107, −0.8968}; mean −0.5016;
- trajectory-grouped bootstrap CI with seed 17: [−0.6467, −0.3153]
  (reproduced exactly, same RNG stream semantics);
- wins 0/5 < needed 3 ⇒ FALSIFIED per frozen rule §8. Rule applied exactly
  once; verdict arithmetic verified.

### C5. Disclosed metric defect and correction (report §7) — **REPRODUCED; ACCEPTED WITH PROCESS CAVEAT**
- Git confirms the first committed analysis (`4dae86c`) passed
  `np.arange(len(vocab))` where the frozen metric requires actual class
  values; final commit (`d22aa83`) fixes both analyzer and verifier to
  `np.array(sorted(vocab))`. The fix implements prereg §5 as written; it did
  not change the frozen design.
- I re-ran the buggy variant on the committed data: mean D = −0.4983,
  exactly the disclosed intermediate. Correction direction is AGAINST the
  candidate model (−0.4983 → −0.5016); verdict FALSIFIED either way.
- Caveats: the correction was applied after outcomes were seen, and the
  buggy-run artifacts were overwritten rather than preserved (only the
  corrected outputs are stored). Mitigation accepted here because both
  variants are exactly reproducible from the committed data and the verdict
  is invariant. For future cycles: preserve pre-correction artifacts or
  recompute-and-hash them at correction time.

### C6. Preregistration timing — **SURVIVES_AUDIT_WITH_LIMITS**
- Verified via git: prereg frozen at commit `9dc895d` (00:34 UTC), before
  ANY committed dataset existed; all row timestamps are ≥ 01:04 UTC.
  Hypothesis, representations, target, policy, holdout unit, nulls, metric,
  uncertainty method, adequacy and verdict rules were genuinely frozen
  pre-data.
- DISCREPANCY: prereg §11 states "Analysis code is committed in the same
  freeze commit as this file." False — `run_wp003b_r2.py`/`verify_r2.py`
  first appear in `4dae86c` (01:04), together with the collector v2
  hardening. Only the collector and driver were actually frozen at 00:34.
  This is a provenance misstatement in the prereg text (not a design change),
  and it interacts with C5's post-hoc fix. It does not alter the frozen
  hypothesis/rules, so the confirmatory status stands, but the claim in
  §11 should be corrected by the Lane Director note, not silently.
- The v1→v2 instrument swap ("no model outcome had been computed when this
  decision was made") is UNVERIFIABLE from preserved artifacts (v1 data kept
  ephemerally, dry-run outputs not stored). Timestamps are consistent with a
  single v2 recollection after hardening; the disclosure is accepted as
  plausible but is recorded as unverifiable provenance.

### C7. Uncertainty integrity — **VALIDATED_FOR_CURRENT_TEST (with a noted probe anomaly)**
- Bootstrap resamples whole trajectories within each fold (dependency unit
  respected), no refit inside the bootstrap, fixed seeds, percentile CI —
  implemented exactly as frozen and reproduced bit-exact here.
- No jitter of point estimates anywhere (the WP-003 failure mode is absent).
- ANOMALY (team's own P3 probe, `wp003b_r2_verification.json`): on the books
  fold the grouped CI width (0.4392) came out NARROWER than the naive row
  bootstrap width (0.4824), contrary to the probe's stated expectation.
  Unresolved diagnostic. It does not threaten the primary conclusion: the
  aggregate upper bound −0.3153 is far from 0 and all five folds are
  individually negative (sign test 0/5 needs no CI at all). Flagged for the
  Lane Director as a methods question to settle before the next cycle.

### C8. Null strength / alternative explanations — **SURVIVES_AUDIT_WITH_LIMITS (adequate for this negative result)**
- The persistence null (no training, no leakage surface) beat the trained
  model on all five adequate folds and is the best null everywhere; NN memory
  nulls never rescue M_SA under holdout. In-site diagnostic shows signal is
  persistence + site-local retrieval, matching WP-002B's lesson now under
  true website holdout.
- Degenerate-null note: N_MAJ macro-balanced accuracy is ≈0 by construction
  under many-class macro recall; it never competes as best null. Harmless,
  but its billing as a "strong null" is cosmetic.
- The negative claim's bounded wording ("representation family Z × this
  action encoding × coarse structural target") is present in prereg §8 and
  report §4/§8 and is appropriate: coarse target includes persistence-favored
  components by design, gutenberg is coverage-0 isolated, and finer targets
  remain untested. No overgeneralization detected.

### C9. Policy confounding / object of study — **VALIDATED_FOR_CURRENT_TEST**
- The primary object is environment response P(class(s_{t+1}) | Z(s_t), a_t)
  conditioned on EXECUTED actions; sampling policy is uniform over available
  action classes, identical across sites (policy-matched by construction);
  policy regularity is not interpreted as environment physics anywhere in
  the report.
- Instrument notes (non-blocking): snapshot settle differs by action type
  (80 ms fill/check vs 350 ms default) — disclosed, uniform across folds;
  multi-step chains resolve the second element index against the
  intermediate post-state (a fidelity limitation that can only inject noise
  into action conditioning, biasing against signal, and only affects 35
  confirmed two-step chains).

### C10. Identifiability gate / WP-004 — **CORRECTLY BLOCKED**
- Revisit/branching diagnostics quoted in the report match the results JSON
  (max 8 structural-class branch points on quotes; url-shape pairs 6/5/5/2/
  1/2/3). Descriptive only; WP-004 remains BLOCKED. Consistent with
  directive and constitution §22.

### C11. Scope and history discipline — **VALIDATED**
- Team diff vs base touches only permitted areas (physics/, reports/physics/,
  results/physics/, data/, docs/PHYSICS_LEDGER.md, tests/test_integrity.py).
  Historical JSONs untouched; ledger entry is marked "TEAM RESULT … pending
  independent audit". No constitution/workflow edits.
- `tests/test_integrity.py` fixture edit repairs the pass-case fixture to
  satisfy the >=2-trajectory validator requirement — legitimate, disclosed
  in diff; shared-file change noted for Meta-Director reconciliation.
- Team test suite passes as committed (4/4 OK).
- Report-vs-artifact consistency: every number quoted in the report tables
  and prose matches the results JSON and my recomputation (including the
  4/6 sites with M_SA == M_S in-site, gutenberg in-site values, identifiability counts, class imbalance extremes 103/1).

---

## 2. Failure modes tested (none produced an invalidating finding)

| Attack | Result |
|---|---|
| Target/post-state leakage | None found; pre-features precede execution; leaky fields stored but unused |
| prev_action misalignment (WP-003 repeat) | 0 violations on 681 rows; variable unused as feature |
| Site/task identity leakage | Site-disjoint LOSO asserted and verified |
| Train-only preprocessing | Vocab/standardization/majority all train-fit (action-vocab pool-level caveat noted) |
| Outcome-based filtering | Exclusions use execution flags only (any_ok), counted/reported |
| Fake/unpreserved data | Dataset internally consistent, hash-manifested, timestamps coherent; raw DOM ephemeral (disclosed unrecomputable layer) |
| Seed nondeterminism | Integer/sha256 seeds; single base seed across all trajectories; no Python hash() |
| Invalid uncertainty (jitter) | Absent; grouped percentile bootstrap reproduced bit-exact |
| Wrong dependency unit | Trajectory-grouped (P3 anomaly noted, non-threatening here) |
| Prereg timing | Frozen pre-data (git + row timestamps); §11 provenance sentence inaccurate |
| Post-hoc analysis change | Metric fix after outcomes — disclosed, implements frozen spec, reproduced, verdict-invariant |
| Degenerate baseline inflating model | Persistence null dominates against the model; no help to M_SA |
| Class imbalance mishandling | Macro balanced accuracy + per-class tables + harsh variant reported |
| Arithmetic/report mismatch | None; all quoted numbers reproduce |
| Verdict inflation | FALSIFIED is the conservative outcome; bounded family wording enforced |

## 3. Corrected interpretation

No correction to the scientific conclusion is required. The defensible
statement is exactly what the team claims, in bounded form:

> At the frozen 13-dim mechanics representation, coarse next-state structural
> class does NOT transfer across these seven websites better than structural
> persistence plus site-local memorization; the frozen decision rule returns
> FALSIFIED (mean D = −0.5016, grouped 95% CI entirely below zero, 0/5 folds
> positive). This is evidence about this representation family only, not
> about web dynamics in general.

Process corrections required (not scientific ones):
1. Fix the prereg §11 provenance sentence (analysis code was NOT in the
   freeze commit) via an explicit director/audit annotation — do not rewrite
   the prereg file silently.
2. Preserve pre-correction artifacts (or their recomputed hashes) whenever a
   post-hoc defect fix is applied to a confirmatory pipeline.
3. Resolve the P3 grouped-vs-naive bootstrap anomaly before the next cycle
   relies on CI widths (point/sign-test conclusions here do not depend on it).

## 4. Required fixes

- None blocking integration. Items 1–3 above are procedural and belong in
  the Lane Director's directive update for cycle 2.
- For any future positive claim: train-fold-only encoder/action vocabulary
  fitting; keep N_MAJ but stop describing it as strong; document that
  within-trajectory state is carried forward exactly (pre(t+1)==post(t)) so
  the corpus models discrete action-conditioned response without inter-step
  environmental drift.

## 5. Integration safety

**SAFE TO INTEGRATE.** The team's FALSIFIED verdict, its headline arithmetic,
its uncertainty statement, its disclosures, and its bounded interpretation
all survive adversarial recomputation and code inspection. The negative
result is measurement-valid under the constitution's validity gates
(§18): target, split, sampling, uncertainty, and representation checks pass.
WP-004 remains blocked pending an identifiability demonstration; the
descriptive diagnostics supplied do not unblock it.

Audit status of the lane output: **VALIDATED_FOR_CURRENT_TEST** (primary
claim C4/C8), with recorded process caveats C5/C6/C7 that limit provenance
purity but not the validity of the tested negative claim.

*Raw audit scratchwork: `/tmp/opencode/audit_r2/recompute.py` (independent
recomputation; imports no team analysis code). Machine-readable findings:
`results/audit/CYCLE_32676578274_PHYSICS_findings.json`.*
