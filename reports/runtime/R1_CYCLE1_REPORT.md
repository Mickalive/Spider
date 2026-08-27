# R1 CYCLE 1 REPORT — Compression Validation & Honest Economics

Cycle: R1-1, GitHub run 32916020607, branch `cycle/runtime/32916020607/team`.
Prereg: `reports/runtime/R1_CYCLE1_PREREG.md` (FROZEN at commit `1b5ae4d`,
before any outcome existed). Outcome branch realized: **B-KILLED**.

> **REPAIR ROUND 1 (run 32921019845):** this report was corrected after the
> independent REVISE audit of run 32916020607 — Priority-3 economics
> wording/figures only (RF-1 double count, RF-2 guard claim, RF-3
> precision). Corrections are marked inline; before→after quotes live in
> `reports/runtime/R1_CYCLE1_REPAIR_ROUND1.md`. The headline, all outcome
> artifacts and the frozen prereg are untouched.
>
> **REPAIR ROUND 2 (run 32924286888):** corrected after the independent
> REVISE audit of run 32921019845 — Priority-3 write-side figures only
> (RF-4 construction double count) plus lane-state test-count lineage
> (RF-5). Corrections are marked inline; before→after quotes live in
> `reports/runtime/R1_CYCLE1_REPAIR_ROUND2.md`. The headline, all outcome
> artifacts, the frozen prereg and the round-1 corrections are untouched.

## Headline (prereg §8 ceiling wording — do not strengthen)

> On the strongest frozen scripted comparator (`goal_href|root0`: goal
> tokens plus a generic href-pattern prior — no site-specific strings),
> the near-repeat compression OBSERVATION **does not survive**: STRONG 4
> vs SPIDER 4 browser actions on EVERY pass (margin 0 < M=2 on all four
> passes), both arms harness-judged successful, zero novel SPIDER
> decisions, 2 paired passes × 2 committed offset entries (/tag/love/,
> /page/10/), single task/site family — an observation-strength scoped
> negative. The R0-2 "4 vs 11" margin is bounded by the legacy greedy
> comparator's lexical inability and its brand-text root prior, exactly
> as audit warning W-C2-6 hypothesized.

## Priority 1 — offline policy-sweep gate (B-survivor side)

Sweep artifact: `results/runtime/probes/policy_sweep_r11.json`
(zero browser launches; snapshots dual-hash-verified).

| variant | /tag/love/ rank | /page/10/ rank | perm-stable top-1 | survives |
|---|---|---|---|---|
| goal_only\|root0 | 3 | 3 | no (frac 0.00) | NO |
| goal_only\|root2 | 4 | 4 | no (frac 0.00) | NO |
| goal_lexicon\|root0 | 1 | 1 | yes (1.00) | YES |
| goal_lexicon\|root2 | 1 | 1 | yes (1.00) | YES |
| goal_href\|root0 | 1 | 1 | yes (1.00) | YES |
| goal_href\|root2 | 1 | 1 | yes (1.00) | YES |
| goal_lexicon_href\|root0 | 1 | 1 | yes (1.00) | YES |
| goal_lexicon_href\|root2 | 1 | 1 | yes (1.00) | YES |

* Raw goal-token matching (the legacy comparator's scoring core) places
  the login anchor at rank 3–4 on BOTH entries — the offline replication
  of the R0-2 finding; root bonus actively hurts (rank 4).
* Six variants survive; frozen tie-break (fewest feature additions, then
  lexicographic id) selects **`goal_href|root0`** — the SIMPLER href-prior
  policy, not a lexicon-bearing one.
* Lexicon sha256 `7c76bdb7…43d` single-shot attestation honored; no
  variant was added/reweighted after output was viewed.

## Priority 2 — live strongest-baseline arm (the kill shot)

Results: `results/runtime/r1_strong/r1_strong_results.json`; stream:
`results/runtime/r1_strong/cost_events.jsonl` (60 spider rows + twins;
twin identity errors: 0).

| pass (counterbalanced) | STRONG actions | success | SPIDER actions | reused/novel | margin |
|---|---|---|---|---|---|
| T3P1 p1 (STRONG first) | 4 | TRUE | 4 | 4/0 | 0 |
| T3P2 p1 (STRONG first) | 4 | TRUE | 4 | 4/0 | 0 |
| T3P1 p2 (SPIDER first) | 4 | TRUE | 4 | 4/0 | 0 |
| T3P2 p2 (SPIDER first) | 4 | TRUE | 4 | 4/0 | 0 |

Gates (mechanically derived, `runtime/gates_r1.py`, witness refs read from
registry artifacts): **G-R1a TRUE, G-R1b FALSE, G-R1c TRUE**; derivation
errors empty; discordance none; censoring none (both arms succeeded
everywhere); committed-digest drift none (live digests matched R0-2
recordings); within-pair entry digests equal.

Interpretation (scoped): one frozen memory-free feature — a GENERIC
account-route href prior with no target-site knowledge — collapses the
entire R0-2 near-repeat margin from 7 to 0. Inheritance value on this
cell class is therefore bounded above by the affordance/href synonym gap
of the legacy comparator. No claim is made beyond this cell class, this
site family, or scripted policies; wall-clock stayed advisory; ratios are
reported as numbers only (4/4 = 1.0 per pass).

## Priority 3 — write-back economics (denominator only)

Artifacts: `results/runtime/economics/wb_maintenance_results.json`,
`wb_maintenance_events.jsonl` (single-schema `spider.cost_event/v0`
single-written rows riding note discriminators inside the frozen envelope;
no new fields — wording corrected in repair round 1; the pilot-era
"dual-named rows" term does not apply here). Bench ran on /tmp clones;
post-run guard at original outcomes time checked existence/counts only
(audit RF-2); repair round 1 strengthened it to a fail-closed per-file
sha256 pre/post digest comparison wired into the bench runner itself
(`runtime/economics.py::accepted_state_digests` +
`assert_accepted_state_untouched`) — prospective strengthening only;
the original run's protection argument remains /tmp-confinement by code
inspection plus a clean tracked tree.

Median ms per operation (cold rep reported separately in artifact):

| op | median ms | asymptotic order (analytic) |
|---|---|---|
| build_record | 0.516 | O(record size) hash+validate — component ⊂ put_fresh (decomposition only) |
| put_fresh | 0.912 | O(1) write + O(N) index rewrite; timed WITH one embedded construction |
| put_idempotent | 0.099 | O(size) read+compare |
| hygiene_filter | 0.0014 | O(keys×exclusions) |
| derive_successors | 0.240 | O(R×K) incl. dominance scan |
| registry_append | 0.650 | O(1)+O(N) index rewrite |
| index_read_all | 0.196 | component OF resolve_e2e (decomposition only) |
| resolve_e2e | 0.384 | retrieval+applicability, no browser |

The per-op table is a decomposition, not an addition, in TWO places:
`index_read_all` measures `Registry.all_latest()`, which
`resolver.resolve()` executes internally, so its work is contained in
`resolve_e2e` [pinned by
`tests/runtime/test_repair_r1.py::TestRecurringContainment`]; and
`build_record` measures observation construction standalone, while
`put_fresh` is timed as `store.put(fresh_record(...))`, so construction
is embedded in `put_fresh` — `build_record ⊂ put_fresh` [corrected per
audit RF-4; pinned by live call-count witness
`tests/runtime/test_repair_r2.py::TestWriteContainment`].

Write-side construct-once fresh-write total ≈ **1.80 ms/cycle** — this
sum EXCLUDES `put_idempotent` (0.099 ms, idempotent re-put branch
reported separately); including it ≈ **1.90 ms/cycle** [exclusion named
per audit RF-3a; corrected in repair round 2 from the previously quoted
≈2.32 / ≈2.42, which summed standalone `build_record` on top of
`put_fresh` and counted one record construction twice (~22%, an upper
bound biased AGAINST write-back) — audit RF-4; see
`reports/runtime/R1_CYCLE1_REPAIR_ROUND2.md`]. Disclosed residual
shared-primitive overlap: `hygiene_filter ⊂ derive_successors` (both
execute `strip_value_tokens`), ≤0.08% of the aggregate, conservative
direction, left at the auditor-prescribed aggregation pending auditor
disposition. Recurring consumer-side tax ≈ **0.38 ms/resolve** =
`resolve_e2e`
ALONE [corrected in repair round 1 from the previously quoted ≈0.58, which
double counted the embedded index read — audit RF-1; see
`reports/runtime/R1_CYCLE1_REPAIR_ROUND1.md`]. **reuse_yield: UNDEFINED**
(consuming-task population empty — no wb capsule has ever been consumed by
any cell); break-even outputs are monotone hypothetical tables over
x ∈ {1..5} caller-action units, never a headline number. Recovery term
anchored as LOWER bound (≥1 caller action + 1 load, single C2 datapoint);
stale-rate scenarios never gate. The minimal R1-2 wb-consumer cell design
is preregistered in the prereg §3.3.

### wb-v2 (W-C2-2 fix)

`runtime/form-login-procedure-wb@v2` persisted to the quarantined
registry (content sha256 `f14ab94a15bb02ce…`, index 1→2, append-only).
Preconditions carry ONLY the effect-witnessed host
(`quotes.toscrape.com`) obtained by the preregistered EVIDENCE JOIN
(observation task_id → accepted pilot2 verify rows' final_url hosts) plus
the execution-witnessed step-1 affordance (`login`) as a separately-named
class; observed entry-hosts (incl. books.toscrape.com, which hosted a
correct ABSTAIN) moved to `context_signature.observed_entry_hosts`.
`context_signature.observed_entry_hosts` is descriptive and NON-GATING by
construction: no gating code path (`retrieval`, `resolver`, `predicates`,
`validate`) reads `context_signature` — now mechanically pinned by
`tests/runtime/test_repair_r1.py::TestNonGatingContextSignature`
[explicit per audit RF-3c].
Manifest: `results/runtime/capsules-wb/DERIVATION_MANIFEST_WB_V2.json`
(records the join table; logs `effect_host` unexpressible on
spider.observation/v0 as the THIRD /v1 schema candidate). v1 file
byte-identical before/after (sha verified). Status CANDIDATE;
negative_knowledge empty; validate_capsule clean.
Disclosed open failure mode: already-authenticated caller → ABSTAIN, not
short-circuit (unresolved, scoped out).

## Priorities 4–6

* **plan.v0 conformance fixture** published:
  `runtime/schemas/plan.v0.conformance.json` +
  `runtime.plan_conformance.validate_plan_conformance()`; code-set
  cross-checked against the FROZEN `PLAN_V0_MESSAGE_CODES.md`; resolver
  RESOLVED/ABSTAIN emissions conform; blinding rule encoded
  (`caller_actionable_params`). Enables alternate-caller conformance; does
  NOT prove portability.
* **W-C2-5 analyze() golden pin** shipped WITH this harness change:
  deep-equality vs accepted R0-2 stream under ADDENDUM wiring (ten TRUE,
  margins [7,7], 224-row truncation guard) + ORIGINAL live analysis
  (three FALSE) preserved as negative fixture; read-only byte-identity
  proven.
* **Retrieval negative controls** (n=4 capsules across parent+wb):
  `results/runtime/probes/negative_controls_r11.json` — must-ABSTAIN
  leakage 0/7 goals × 3 registries; near-miss cross-matches 0 across all
  registries at adopted constants (tau=0.30/min_match=2). Invalid/stale
  hit rate currently ZERO at this registry size; disclosed as n=4 point
  measurement, not a scaling claim.

## Negative knowledge (first-class, scoped)

1. The near-repeat compression OBSERVATION does not survive its strongest
   frozen scripted comparator: parity (4v4) is achievable by a one-feature
   memory-free policy using a generic href prior. The inheritance edge on
   this cell class was comparator weakness (W-C2-6 confirmed causally by
   intervention, not just diagnosis).
2. Root-bonus HURTS route-finding on deep entries (goal_only ranks Login
   4th with it vs 3rd without): the legacy baseline's brand-text root
   prior is self-handicapping — recorded as an inherited Graph-lineage
   defect for any future reuse of that explorer lineage.
3. Affordance-lexicon and href-prior features are individually sufficient
   for stable top-1 anchor placement on these entries (six surviving
   variants); neither requires target-site strings.
4. Write-back maintenance overhead is measurable and small at current
   scale (~ms/cycle) but has NO demonstrated payoff: numerator structurally
   absent; yield stays undefined until a consumer cell exists.

## Provenance discipline

Freeze chain git-orderable: harness `e95e4a9` → FROZEN prereg `1b5ae4d`
→ outcomes commit (this report's sibling). One pre-outcome harness fix is
disclosed: the blinding fixture initially scanned the shared task echo
(goal text/credentials both arms receive identically) and aborted BEFORE
any launch or row existed; corrected to scan capsule-knowledge channels
only + shared-inputs identity assertion, exactly per prereg §2.2. No
outcomes were re-run, edited, or reinterpreted. Audited modules
(`baseline.py`, `derive.py`, `gates.py`, `pilot2.py`) byte-untouched;
`state/runtime_loop.json`, ledger and directive left Director-owned.

Environment: Python 3.12.3, Playwright chromium headless-shell 151.0.7922.34,
single machine, warm cache; economics figures are point measurements.

## Next high-information action (for Director/R1-2 decision)

Per directive stop/succession: the compression question is answered
NEGATIVELY at observation strength against the strongest comparator.
Multi-task replication of a killed observation is NOT informative;
R1-2 as originally gated should NOT run its compression-replication arm.
Succession requires a measured dominant bottleneck plus a materially
different mechanism — the recorded successor hypothesis is EFFECT-LEVEL
(witness-level) addressing rather than route-level replay, plus the
preregistered minimal wb-consumer cell if write-back value is still worth
resolving. This lane's honest state: the agent-facing loop works end-to-end
(resolve/execute/verify/report, attributed abstain→handoff→repair), but NO
work-compression claim currently survives its strongest scripted
comparator anywhere it has been tested.
