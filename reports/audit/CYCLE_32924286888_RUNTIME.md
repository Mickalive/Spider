# RUNTIME INDEPENDENT AUDIT — CYCLE R1-1, REPAIR ROUND 2

Run: 32924286888 · Team snapshot: `origin/cycle/runtime/32924286888/team` @
`e0c6eb8713605699e1e237f4b61a5bc6f358e81d` (mounted at
`/tmp/spider_runtime_team`, byte-identical to pushed ref — full-tree diff
empty). Accepted base: `runtime-audit-base` @ `162468f` (post R0-2
integration). Prior gates in this cycle chain: 32916020607 REVISE
(RF-1..RF-3) → 32921019845 REVISE (RF-4..RF-5) → **this audit**.
Auditor: runtime_auditor, independent session. Date: 2026-08-26.

## Verdict

**PASS** — safe to integrate with exact wording of
`reports/runtime/R1_CYCLE1_REPORT.md` (+ repair round 1/2 reports) and
`results/runtime/r1_cycle1_state.json`. The cycle's scientific core is an
honest observation-strength scoped negative (B-KILLED), reproduced by this
audit from raw artifacts. Both repairs fixed exactly their assigned
required fixes; no outcome artifact moved; no benchmark or question was
repositioned after outcome.

## Scope and freeze integrity (verified mechanically)

- Full diff base→snapshot: 35 files, all under `runtime/`, `tests/runtime/`,
  `results/runtime/`, `reports/runtime/`; zero deletions; no other lane, no
  Director-owned file (`docs/RUNTIME_LEDGER.md`, `docs/NEXT_RUNTIME.md`,
  `state/runtime_loop.json`, `directives/RUNTIME.md`) touched.
- Freeze chain git-orderable, linear successors, no amend/rebase:
  harness `e95e4a9` → FROZEN prereg `1b5ae4d` (01:35:05Z) → disclosed
  pre-outcome blinding-fixture fix `20f285e` (01:39:50Z, zero outcomes
  existed) → outcomes `9ddd723` (01:40:03Z) → post-persist test fix
  `66468f4` (disclosed; part of initially-audited snapshot) → repair r1
  `93f374a`,`9e1875d` → repair r2 `ae9c0d1`,`e0c6eb8`.
- Outcome artifacts byte-untouched across BOTH repairs: `git diff` empty on
  every protected path (`9ddd723..e0c6eb8`); all seven headline artifact
  sha256 pins identical between `repair_round_1_provenance` and
  `repair_round_2_provenance` AND equal to current file hashes;
  events-stream sha256 `fdefc608ffecc440…` matches its round-1 pin.
  Audited modules `baseline.py`/`derive.py`/`gates.py`/`pilot2.py`
  byte-untouched. No live re-run occurred (none authorized).

## Recomputation performed (all from raw evidence, not reports)

1. OFFLINE POLICY SWEEP — independently re-implemented prereg §1.1–§1.4 from
   scratch (own tokenizer/scoring/oracle/permutations; no import of team
   modules): all 8 variant ranks reproduce (goal_only 3rd/3rd; +root2
   4th/4th; six variants permutation-stable top-1 frac 1.00 on both
   entries); survivor set and frozen tie-break winner `goal_href|root0`
   reproduce exactly. Snapshot dual-hash pins verified. Because the winner
   is a pure function of the frozen spec + hash-pinned snapshots, any
   hypothetical post-hoc edit of the sweep artifact would be irrelevant:
   the outcome is spec-determined. Lexicon canonical sha256 ==
   prereg pin `7c76bdb7…43d`; blinding fixture sha256 == pin `94114009…`.
2. LIVE ARM (the kill shot) — independent recount from raw
   `r1_strong/cost_events.jsonl` (60 unique rows after twin dedup; twins
   differ ONLY by the documented dual-name schema field): STRONG 4 vs
   SPIDER 4 stream-counted browser actions on ALL FOUR counterbalanced
   passes; margin 0 < M=2 everywhere; both arms harness-judged successful
   (verify rows TRUE with correct per-arm predicate refs); SPIDER reused=4
   = pinned steps_len via APPLICABILITY_PASS rows, novel=0; within-pair
   entry digests equal AND equal to the committed R0-2 page digests
   (zero drift); no censoring; G-R1a TRUE, G-R1b FALSE, G-R1c TRUE all
   reproduced. Row timestamps are this cycle's live session (01:36–01:37Z)
   — numbers were not reused from R0-2. **B-KILLED confirmed from raw
   stream.**
3. ECONOMICS (both repaired aggregates) — recomputed from the committed
   events stream: write_side := put_fresh 0.9124 + hygiene_filter 0.0014 +
   derive_successors 0.2395 + registry_append 0.6499 = **1.8032 ms/cycle**
   (committed 1.8032 ✓); incl. put_idempotent **1.9018** ✓;
   per_resolve := resolve_e2e alone **0.3839 ms** ✓. `operations[]` is an
   exact transcription of the stream summaries. `repair_r2.py --check`
   fixed-point verification PASSES in auditor sandbox. Containment
   relations verified by auditor-run spies/code: `resolve()` executes
   `Registry.all_latest()` internally (RF-1); `put_fresh` timed region is
   `store.put(fresh_record(...))` so construction is embedded (RF-4);
   residual `hygiene_filter ⊂ derive_successors` shared primitive measures
   **0.0776%** ≤ the disclosed ≤0.08%, direction inflates the overhead
   denominator (conservative). Superseded figures (2.3187/2.4173/0.5794)
   survive only inside labeled provenance/disclosure contexts (grep-swept).
4. NEGATIVE CONTROLS — fresh rerun through the real read path is DEEP-
   IDENTICAL to the committed artifact: 0/7 must-ABSTAIN leakage goals × 3
   registries (parent/wb/union), 0 near-miss cross-matches at n=4 capsules,
   constants tau=0.30/min_match=2 non-retuned.
5. WB-V2 DERIVATION JOIN — independently recomputed the task_id →
   final_url-host join over accepted `pilot_results.json`: effect-witnessed
   hosts = {quotes.toscrape.com} == capsule precondition host_allowlist;
   entry hosts correctly relocated to non-gating `context_signature`
   (gating modules do not read it; test-pinned); v1 byte-identical to base;
   index append-only 1→2; status stays CANDIDATE; negative_knowledge empty
   (v0 checker limit logged as third /v1 candidate); mechanism kind
   PROCEDURE — no predictor producer added.
6. AGENT-FACING CONTRACT — plan.v0 conformance fixture: all shipped
   valid/invalid examples behave correctly (silent-execution and unknown-
   code plans rejected); live RESOLVED and ABSTAIN emissions conform;
   `expected_host` is the only actionable param; blinding rule (zero-action
   UNACTIONABLE without it) encoded. Gates self-test proves outcome-
   blindness on fabricated streams for BOTH branches (success → survive;
   exhaustion → censored + not-survive) under identical gate code.
7. TEST SUITE — 129/129 pass in auditor sandbox (`pytest tests/runtime`,
   Python 3.12.3, pytest 9.1.1 installed fresh), matching the claimed
   count lineage 109→120→129 recorded in state JSON (RF-5).
8. SCHEMA FREEZE — both new event streams carry EXACTLY the frozen
   `spider.cost_event/v0` envelope fields (no additions, refuse list
   honored); economics telemetry rides note discriminators only.
9. BLINDING — `policies.py` scans clean against the forbidden-token
   fixture; goal text never names the anchor (`leakage_check` clean);
   extended scan hits only harness/gate/economics modules whose declared
   scope legitimately contains site/predicate/capsule references (outside
   prereg §2.2's policy-module scope).

## Claim-by-claim disposition

| # | CLAIM | EVIDENCE | RECOMPUTATION | FAILURE MODES TESTED | STATUS | MAXIMUM DEFENSIBLE WORDING |
|---|---|---|---|---|---|---|
| K1 | Near-repeat compression OBSERVATION does NOT survive strongest frozen scripted comparator (4v4 parity, margin 0 < M=2, all 4 passes) | r1_strong stream+results, gates_r1 | Independent recount: margins [0,0,0,0]; both arms succeed; digests equal+committed-matched | baseline strength (in-family-optimal policy, bias toward baseline, disclosed pre-outcome); DOM-order luck (K=100 permutation audit); order effects (counterbalanced); digest drift (none); censoring semantics (self-tested both branches) | SURVIVES_AUDIT | "observation-strength scoped negative, single task/site family" — never generalized |
| K2 | Offline bound: no memory-free policy without lexicon/href feature places anchor rank-1 stably; six survivors; winner by frozen tie-break | policy_sweep_r11.json | From-scratch spec reimplementation reproduces every rank/survivor/winner | substring false-affordances (token-boundary equality); tie luck (permutation bar); oracle dead-wiring (normalized clauses); post-outcome variant edits (single-shot hash pin + spec-reproducibility) | SURVIVES_AUDIT | necessary-condition bound on TWO committed snapshots of ONE site family; no live-behavior claim from offline numbers |
| K3 | W-C2-6 causal confirmation: legacy margin was comparator lexical inability (root bonus actively hurts: rank 4 vs 3) | sweep rows + report | Reproduced ranks incl. root-bonus degradation | inherited Graph-lineage defect recorded as negative knowledge | SURVIVES_AUDIT | intervention-backed diagnosis on these entries only |
| E1 | Write-side overhead ≈1.80 ms/cycle construct-once flow (≈1.90 incl. idempotent branch) | wb_maintenance events+results | Exact recomputation ✓; RF-4 double count confirmed removed; containment witnessed | double counting (two instances found across rounds — both now mechanically pinned); residual hygiene⊂derive overlap 0.078% conservative; flow-weighting caveat → W-R1-1 | SURVIVES_AUDIT_WITH_LIMITS | denominator measurement only, point measurement, no extrapolation, never a payoff claim |
| E2 | Recurring consumer tax ≈0.38 ms/resolve (resolve_e2e alone) | same | Exact recomputation ✓; RF-1 containment spy-verified | double counting removed; warm-index workload binding disclosed | SURVIVES_AUDIT_WITH_LIMITS | as E1 |
| E3 | reuse_yield UNDEFINED (consuming population empty) | results JSON + state | grep: no yield quotation anywhere; numerator definition pre-frozen | metric invention prevented; scenario stale-rates non-gating | SURVIVES_AUDIT | "undefined — not pending, not zero" |
| W1 | wb-v2 preconditions = effect-witnessed host via preregistered join; entry-host context demoted to non-gating signature | capsule + manifest | Join recomputed independently; non-gating test-pinned | silent tier upgrade (status CANDIDATE); in-place edit (v1 byte-identical, append-only); invented fields (nulls kept) | SURVIVES_AUDIT | derived candidate artifact with explicit provenance; already-authenticated ABSTAIN gap disclosed open |
| N1 | Retrieval negative controls clean (0 leakage, 0 cross-match, n=4) | negative_controls_r11.json | Fresh rerun deep-identical | invalid/stale-hit inflation; constant retuning (constants pinned, disclosure-only path) | SURVIVES_AUDIT | n=4 point measurement, not a scaling claim |
| F1 | plan.v0 conformance fixture enables alternate-caller implementation; consumers need no internal IDs | fixture + validator | Live emissions conform; unknown-code/blinding rules enforced | hidden ID dependence (capsule_id is provenance; expected_host sole actionable param); silent execution (rejected example) | SURVIVES_AUDIT | enables conformance, does NOT prove portability |

## Failure-mode coverage requested by charter (dispositions)

- Stale reuse / context mismatch: drift guard digest equality (live ==
  committed snapshots, within-pair equality); wrong-host ABSTAIN retained
  from audited base; wb v1+v2 coexistence produces zero invalid hits.
- Hidden answer leakage: token-boundary matching, generic single-shot
  lexicon with attestation, clean policy module, keyword leakage fixture,
  baseline-favoring selection bias disclosed pre-outcome.
- Internal-ID dependence: plan.v0 conformance (provenance-only ids).
- Missing fallback / silent execution: ABSTAIN→structured handoff;
  validator rejects silent-execution shapes; exhaustion censors rather
  than fabricates denominators.
- Expensive verification: verification symmetric across arms (same vendored
  predicate dialect, harness-only judge); consistent with ledger C4, no
  verification-cost claim made.
- Omitted maintenance overhead: measured decomposed; two double-counts
  found and fixed across rounds with mechanical containment pins.
- Metric double counting: none remaining above the disclosed 0.078%
  conservative residual.
- Evidence-tier inflation: headline quoted verbatim at prereg §8 B-KILLED
  ceiling; DURABLE_UNAUDITED until this gate; nothing self-upgraded.

## Warnings (carried to Director; none blocking)

- **W-R1-1** Economics "per-cycle" aggregates are decomposition-based point
  measurements whose cycle basis assumes the observed R0-2 rate
  (7 records / 6 executed tasks; `resolves_per_cycle_assumed`=7) and one
  construct-once fresh write; real flows with multiple idempotent re-puts
  or different task mixes pay different recurring costs. Non-gating today
  (no figure feeds any gate); REQUIRED before any default-path or
  break-even consumption: flow-weighted re-measurement.
- **W-R1-2** Disposition of the residual `hygiene_filter ⊂
  derive_successors` overlap left at the prescribed aggregation: ACCEPTED
  as conservative residual (≤0.08%, inflates denominator against mechanism
  interest). No action required unless a future gate consumes these
  figures.
- **W-R1-3** Immutable historical quotations retain superseded economics
  values (outcomes commit message "~2.3ms/~0.6ms"; round-1 report §RF-3a)
  by no-amend discipline; superseded by durable artifacts + provenance
  notes. Disclosed; acceptable.
- **W-R1-4** The kill and the offline bound are both scoped to ONE site
  family on ONE date with two committed entries; neither direction
  generalizes cross-site. Succession (effect-level addressing hypothesis,
  minimal wb-consumer cell) is correctly left to the Director.
- **W-R1-5** Stream recounting requires twin deduplication (dual-name rows
  differing only by `schema`); documented here so future auditors do not
  double-count as this auditor initially did in a first pass.

## Provenance of this audit

Sandbox: Python 3.12.3, pytest 9.1.1 (freshly installed), no network needed
except pytest install; all recomputation scripts run read-only against the
mounted worktree plus `/tmp/opencode` scratch. Gate JSON:
`results/audit/CYCLE_32924286888_RUNTIME_GATE.json`. The team's own
129-test suite, `gates_r1.self_test()`, `run_negative_controls`, and
`runtime.repair_r2 --check` were executed by the auditor, not trusted from
reports.
