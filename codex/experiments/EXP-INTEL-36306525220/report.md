# EXP-INTEL-36306525220 — measurement-validity report for C-PRODUCT-ECON

- **Lane:** intel
- **Claim:** `C-PRODUCT-ECON`
- **Status:** `MEASUREMENT_INVALID`
- **Packet outcome:** `NOT_APPLICABLE`
- **Frozen per-part outcomes:** Part 1 `MEASUREMENT_INVALID`, Part 2 `INCONCLUSIVE`, Part 3 `INCONCLUSIVE`, overall `MEASUREMENT_INVALID`
- **Machine-readable packet:** `result.json` (validated by `validate_packet.py`), `provenance.json`, derived table `results/table.json`

This is a producer report for a **frozen measurement-validity check**. It adopts no claim, promotes nothing to Product Core, and is not an independent audit.

## 0. Plain answer to the mandate's explicit question

The mandate requires this packet to "state plainly whether external justification for the persistence premise exists at all".

**Within the corpus this run actually reached, no published artifact was found that reports a break-even reuse count with a denominator, an accounting convention and stated uncertainty, and no published artifact was found that shows persistent cross-episode state beating re-derivation on a real, billed cost basis.** The one artifact that reports the cost-accounting construct explicitly reserves its live billing and states that its own live in-loop saving is about 14% against a modeled 83.3%.

That statement is **not** licensed as a literature-level answer, and this packet does not make it: the frozen gates fire (gate 1 on a frozen corpus defect, gate 5 on identity recall), so the frozen decision rule returns `MEASUREMENT_INVALID` and the packet outcome is `NOT_APPLICABLE`. The searched corpus was 5 benchmarks plus 1 memory paper, and none of the 5 is a memory-augmented or workflow-inducing agent. The honest product-facing consequence is the one in `result.json.unresolved` U-1: SPIDER cannot currently borrow external justification for its persistence premise from this packet, and this packet does not establish that such justification is absent.

## 0b. Relationship to accepted Codex evidence

- `codex/experiments/EXP-INTEL-36293264917/verdict.json` adjudicates the parent `EXP-INTEL-36293264917` as `MEASUREMENT_INVALID`, holds `C-PRODUCT-ECON` at `HYPOTHESIS` with `promote_to_product=false` and no product action, and sets `continue=false` for the parent's Q1 framing. This packet does not contest that adjudication, does not change any claim status (that is the director's field), and adopts no product action.
- `codex/experiments/EXP-INTEL-36293264917/audit.json` `claim_ceiling` permits Q2 to be carried forward as PARTIAL, bounded to "figures quoted in one preprint's abstract, n=1 user, with the accounting convention and a five-item limitations section still unread", and it bars any measured value of `h` or `R` from being used to bound SPIDER's product economics. This run read the accounting convention and the limitations section (5 items, §8.4) from the full text rather than the abstract, so it extends that ceiling only along the axis the audit named as unread. It keeps the bar: `result.json.validity_notes` VN-7 and report §11 state that no `h` or `R` value here bounds SPIDER economics.
- The audit names the parent's specific instrument failures. Each is addressed by a frozen mechanism in this design, and the address is checkable rather than asserted: identity before scoring (§3, 0 rows scored `NOT_FOUND`); a null control with real power (§2, a real-but-wrong artifact flagged `AMBIGUOUS`); a positive control that fails when its minimum fields are absent (§2, `PC-COST-ACCOUNTING` FAIL); a coverage metric that can vary (§3, `0.357143` over a denominator that is a constant 14, with snowball coverage stated separately).
- The mandate's standing control-plane condition — that gates of the form "code hashed into `freeze.json`" are unsatisfiable, and that packets should use EXECUTE-stage sha256 attestation instead — was honoured: this design binds code by EXECUTE-stage sha256 in `result.json.artifacts` and `provenance.json.artifact_index`, and freezes no code-bound gate. The residual gap against the mandate's "reusable artifact at an exact commit" dependency is disclosed in VN-14 and `provenance.json.commits`: branch discipline in this session forbids committing, so the artifacts are pinned by hash and the working-tree HEAD is recorded instead.
- The parent's Q1 (`C-CROSSSITE` four-part cross-site transfer form) is out of scope here and is not re-opened, attempted or answered in any form.

## 1. What was asked and what was run

The director mandate asked whether published web-agent evaluations expose a cost denominator, a real cost advantage that persists, a performance envelope, and whether a common success convention exists. The frozen design (`spec.json`, `prereg.md`) converted that into a bounded identity-resolution instrument applied to 14 frozen target entries, four controls, three evidence parts, and five gates.

What actually ran, end to end, with no outcome inspected before the frozen rule was applied:

| Stage | Script | Output |
|---|---|---|
| Transport probe + identity resolution of 14 targets | `resolve_identity.py` | `raw/identity_resolution.json` |
| Base-identifier recheck + frozen snowball | `recheck_and_snowball.py` | `raw/base_id_recheck.json`, `raw/references/snowball_candidates.json` |
| 4 controls | `run_controls.py` | `raw/controls_result.json` |
| Quote extraction from 7 full texts | `extract_spans.py` | `raw/spans.json` |
| 29 field determinations + absence determinations | `field_determinations.py` | `raw/field_determinations.json` |
| Frozen part rules, gates, integrity self-checks | `build_table.py` | `results/table.json`, `results/coverage.json` |

Cost: 32 HTTP GET attempts (27×200, 3×404, 2×406), 0 model calls, 0 model tokens, 0 browser interactions, no credentials, 152 s of retrieval. Every raw page, PDF, text layer and log line is retained under `raw/` with sha256 hashes in `result.json.artifacts`.

## 2. Controls

| Control | Expectation | Result |
|---|---|---|
| `PC-COST-ACCOUNTING` | must pass before Part 1 may be scored | **FAIL** |
| `PC-PERFORMANCE-ENVELOPE` | pass | **PASS** |
| `NC-REAL-BUT-WRONG` | must flag the real-but-wrong artifact | **PASS** |
| `NC-FABRICATED-CLAIM` | must emit `NOT_LOCATED` | **PASS** |

`PC-COST-ACCOUNTING` fails for one reason, recorded before any metric was read: `spec.json` freezes `expected_authors=["TBD"]` for the `ActivityFrames` entry, while `prereg.md` §4.1 condition 3 requires at least one author-name substring match. The condition is unsatisfiable for that entry, so the resolver recorded `pass=null`, `reason=C3_author_unevaluable_TBD`. The artifact itself is real and correct (`raw/identity_resolution.json`; title coverage 1.0, 5/6 domain keywords, single author "Iyamu, Nossa") — the frozen target list, not the resolver, is what fails. No "author list unavailable" branch was added, because adding one after observing this outcome would be a post-hoc change to a frozen identity contract that flips the verdict.

## 3. Identity resolution (raw observation, then derived measurement)

- **Observation:** 5 of 14 frozen entries satisfied all four frozen identity conditions: WebShop `2207.01206v4`, Mind2Web `2306.06070v3`, WebVoyager `2401.13919v4`, WebArena `2307.13854v3`, AgentBench-web `2308.03688v2`.
- **Observation:** 5 frozen entries resolve to real artifacts that are demonstrably not the named system, and 5 more to real artifacts outside the agent domain. All 10 were flagged `AMBIGUOUS` and none was scored. Three of those are *undeclared* frozen-list defects: BrowserGym `2401.15378` = MufassirQAS, MiniWoB++ `1802.08827` = integrable spin chains, SeeAct `2402.04566` = radiotherapy dose prediction.
- **Observation:** 6 of 14 entries freeze `expected_authors=["TBD"]`, so condition 3 is unevaluable for all of them.
- **Measurement:** `identity_resolution_recall = 5/14 = 0.357143`, threshold `0.6`, so **gate 5 fires**. Variants: `0.555556` excluding the 5 prereg-declared placeholders; `0.625` over the 8 entries with real author lists. The metric is therefore not denominator-invariant (`recall_robust_to_denominator_choice = false`), which is reported rather than resolved.
- **Measurement:** the bounded snowball, capped at 25, examined 0 papers and yielded 0 usable candidates. The PC artifact's reference list prints no arXiv identifiers, so the frozen inclusion rule selected nothing. The one `arXiv:` string in its text layer is the paper's own identifier in body text, not a reference entry.

## 4. Part 1 — cost accounting, denominators, persistence (frozen outcome `MEASUREMENT_INVALID`)

Everything in this section is *what one artifact reports*, recorded with denominators exposed and modeled quantities labelled. Because gate 1 fires, none of it is a packet-adopted measurement of the mandate's question.

- **Observation:** in `arXiv:2608.05784v1` the reuse count `N` appears only as a symbol in the piecewise cost model of Eq. (1); the paper never solves it. The frozen pattern sweep over the 69,607-character text layer found 0 hits for break-even/breakeven/break even reuse/reuse count/payback/amortization point/`f*`.
- **Measurement:** `p1_break_even_reuse_count_fstar = null`, `status = NOT_REPORTED_AS_A_COMPUTED_QUANTITY`.
- **Observation:** the Routine Overhead Ratio is a two-rung ladder with a **modeled** numerator and **measured** denominators — `R_inject = 60x` operational (IQR 59–62x) and `R_info = 343x` ceiling (IQR 297–390x). Derived as `R = C_agent(k)/C_replay(k)`, tokens counted, numerator modeled and not executed, denominator tokenized deterministically.
- **Measurement:** delegable recurrence is reported as measured, at two levels: `h_raw = 0.831` in-sample, `h_specific = 0.090` in-sample, `0.131` at URL granularity, `0.077` out-of-sample on a temporal holdout (8.6% in-sample on training days). The paper's all-fleet ceiling `h(1 − 1/R_info) ≈ 0.077`. Hence `p1_all_fleet_ceiling_h_times_1_minus_1_over_Rinfo = 0.077`.
- **Observation:** the three-arm dollar comparison is stated to be modeled from measured artifacts and token counts and explicitly **not billed**; live three-arm billing with real usage JSON is reserved. The one live in-loop comparison against an accessibility-tree agent saved about 14%.
- **Measurement:** modeled arm-B `0.833`, arm-C `0.408`, marginal cached-vs-derived ≈ `6.0x` per occurrence, measured guard coverage median `0.415`, measured live in-loop saving `0.14`, `p1_real_cost_advantage_persistence = "no_measured_real_cost_advantage"`.
- **Observation:** no quantified staleness/forgetting/maintenance cost of retained state. The staleness-adjacent surface is unquantified: "interface drift that a live run must confirm", a "stale attribution" defect the compiler repairs, and a 9.5 GB capture corpus at ~0.19 GB per active day with the accessibility tree present on 81.5% of frames. `p1_staleness_forgetting_maintenance_cost = null`, `status = NOT_REPORTED_AS_A_QUANTIFIED_COST`.
- **Measurement:** corpus = 1 subject, 51 active days, 128,756 frames; 5 self-declared limitations in §8.4, including that every number comes from one user's machine.
- **Measurement (derived, not frozen):** `p1_n_correctly_resolved_targets_persisting_state_across_sessions = 0`. The frozen list of 14 named systems is a list of benchmarks and environments; none of the 5 correctly resolved targets persists state across sessions or episodes. `identity_resolution_recall` is a name-to-artifact identity metric and is not a coverage metric for the Part 1 construct, yet frozen gate 5 uses it as one.

## 5. Part 2 — performance envelope (frozen outcome `INCONCLUSIVE`)

Frozen outcome is `INCONCLUSIVE` because gate 5 fires; the spread below is recorded, not adopted.

| Benchmark | Rate | Convention | Denominator |
|---|---|---|---|
| WebVoyager (own benchmark, 15 sites) | 0.591 | Task Success Rate, stated to follow the WebArena convention; GPT-4V judge over all screenshots and all actions, 300-task human-agreement subset | 643 tasks, 40–45 per site |
| WebVoyager on the SeeAct online test set | 0.300 | same Task Success Rate convention | the 50 tasks of SeeAct's online evaluation |
| WebArena | 0.1441 (human 0.7824) | end-to-end | 812 tasks |
| Mind2Web MINDACT/Flan-T5L | step SR 0.503, task SR 0.071 / 0.011 / 0.027 | ground-truth action history at every step | cross-task / 177 cross-website / 912 cross-domain |
| WebShop | 0.291 (human 0.59) | Task Score = 100 × average reward, reported jointly | 500-instance test split |
| AgentBench-web | `null` | `NOT_REPORTED_AS_A_SINGLE_EXTRACTABLE_HEADLINE_RATE` | — |

The 0.300 row is the WebVoyager *system* measured on the SeeAct test set, not a SeeAct result; the same artifact states the best SeeAct autonomous agent scores 0.26 there, and reports GPT-4 (All Tools) at 0.308 and WebVoyager text-only at 0.401 on its own benchmark.

Observation: WebVoyager states it follows the WebArena evaluation convention, so those two are comparable to each other; Mind2Web, WebShop and AgentBench are not comparable to either. None of the 5 correctly resolved artifacts is a memory-augmented or workflow-inducing agent, so the mandate's actual comparison target was not reached by the frozen corpus at all.

## 6. Part 3 — retrieval ablation (frozen outcome `INCONCLUSIVE`)

- **Observation:** §6.2 varies the WRITE representation (raw search-API JSON 126,812 tokens; compiled schema document 34,815; compact context block 1,469; LLM summary) while holding retrieved context CONSTANT, reporting `0.984` answer accuracy, Wilson 95% CI 0.917–0.997, 8 days, 64 ground-truth questions against an independent SQL oracle, versus 0.66–0.80 for the LLM summary.
- **Measurement:** `p3_compiled_block_answer_accuracy = 0.984`; retrieval quality (`recall`, `precision`, `nDCG`, `hit rate`, `MRR`) is not varied and not reported.
- **Observation:** the ablation therefore supports a claim about representation token cost, not about retrieval quality. `p3_retrieval_quality_over_recall_ndcg_hit_rate = null`, `status = NOT_VARIED`.

## 7. Frozen gates

| Gate | Fired |
|---|---|
| 1 — `PC-COST-ACCOUNTING` fails | **yes** |
| 2 — `NC-REAL-BUT-WRONG` fails to flag | no |
| 3 — any target scored `NOT_FOUND` | no |
| 4 — `PC-PERFORMANCE-ENVELOPE` fails | no |
| 5 — identity recall below 0.6 | **yes** |

Gates 1 and 5 fire. Under `prereg.md` §8, Part 1 is `MEASUREMENT_INVALID`, Parts 2 and 3 are `INCONCLUSIVE` (not `SUPPORTS`: the SUPPORTS clause is not licensed when gate 5 fires), and the overall is `MEASUREMENT_INVALID`. Per `research/EXPERIMENT_PACKET.md` §4 the packet encodes that as `status=MEASUREMENT_INVALID` with `outcome=NOT_APPLICABLE`, because no scientific verdict is licensed for the experiment as a whole. This is a measurement-validity failure, not a scientific falsification and not an infrastructure failure.

## 8. Integrity self-checks (`results/table.json`)

- 38 rows: 9 identity rows + 29 field determinations.
- 0 rows with `resolution_status=NOT_FOUND`; 0 rows scored `NOT_FOUND`; 11 rows scored `UNMEASURED` (identifier and unresolved-reference cells only).
- 13 rows with a null value, all 13 carrying explicit absence evidence; 0 nulls without it.
- 17 value-bearing rows expose their denominator; 7 modeled rows carry `modeled_vs_measured="modeled"` and an explicit `accounting_convention`.
- No row is scored `NOT_FOUND`: gate 3's forbidden-literal check over `scored_as` and `resolution_status` returns 0 rows.

## 9. Validity threats

Full text in `result.json.validity_notes` (VN-1…VN-14). The load-bearing ones:

1. **The binding invalid trigger is a frozen corpus defect** (gate 1, C3 unevaluable because `expected_authors=["TBD"]`), not resolver failure. The resolver correctly refused an unsatisfiable target.
2. **No preregistration was weakened.** Three substitutions are logged in `provenance.json.deviations_from_frozen_design`: arXiv abs/PDF transport instead of the blocked Atom API (406 from arXiv's own varnish, `raw/identity_resolution.json.transport_probes`); a base-identifier re-probe of two targets whose 404 was a non-existent version suffix; and reading the title condition as a case-insensitive substring test with a token-coverage threshold, because a full-token-set Jaccard of 0.85 is arithmetically unsatisfiable for a 1–2 token expected title. Both Jaccard and coverage are logged per target. Under the strict full-set-Jaccard reading, recall would be 0.0 and Parts 2–3 would all be `INCONCLUSIVE` — which strengthens rather than weakens the conclusion that this frozen list cannot decide the science.
3. **PDF text-layer representation loss.** Quotes are whitespace-normalized slices of the text layer: ligatures dropped, de-hyphenation across line breaks, tables not linearised. A missing number may exist in a figure or table cell — hence AgentBench-web is `NOT_REPORTED` rather than a number. Every absence determination records the retrieval scope and character count searched, so absence is claimed only at the strength "absent from the retrieved text".
4. **Sub-validity of all recorded quantities** (gate 1 fires): claim ceiling is "verbatim from a named artifact, denominators exposed, modeled quantities labelled".
5. **No independent verification.** Every value is read from a published artifact; nothing was reproduced. `prereg.md` §10 excludes reproduction by design, so the envelope is a report of what papers claim, not of what those systems do.
6. **Coverage metric is not denominator-invariant** and conflates corpus design errors with resolver failure; both are present.
7. **Reusable artifacts are published as code plus raw evidence at exact repository-relative paths with sha256, not at a commit** — branch discipline in this session forbids committing. `provenance.json` records the working-tree HEAD.
8. **This is a producer self-check, not the independent audit** required by `research/EXPERIMENT_PACKET.md` §6. No claim is self-promoted.

## 10. Consequences of both outcomes, and the smallest next actions

**If the packet had been valid and positive** (e.g. an artifact had reported a measured `f*` with denominator, convention and uncertainty): the director could have cited a published break-even reuse count as a cost-denominator precedent for `C-PRODUCT-ECON` and used the Part 2 envelope as a bound. **If it had been valid and negative** (frozen list repaired, controls passing, still no measured `f*`): the negative would have licensed "published memory-augmented web agents do not report a measured break-even reuse count", and Part 1 would have flipped to `SUPPORTS` in the negative direction. Neither is licensed here. The gate fires before any of these.

Smallest next actions, each requiring a director mandate (see `result.json.unresolved` U-1…U-8):

- **U-2** permit an identifier repair pass whose only permitted mutation is replacing a frozen arXiv ID that provably resolves to an unrelated artifact (BrowserGym, MiniWoB++, SeeAct), every repair logged, identity rule unchanged;
- **U-3** restate the Part 1 target population as systems that actually persist state across sessions or episodes and authorize a corpus search for that population — the frozen benchmark list cannot answer the frozen Part 1 question at any identity recall;
- **U-4** permit the snowball to resolve reference entries by author-title-year against the Semantic Scholar graph API (HTTP 200 on this run's substrate probe), identity rule unchanged; the visible candidates are "Agent workflow memory" and "Position: Episodic memory is the missing piece for long-term LLM agents";
- **U-6** a director ruling on which title-condition reading is binding — the only implementation decision that moves recall between 0.0 and 0.357, and it does not change the overall `MEASUREMENT_INVALID`, which rests on gate 1 independently;
- **U-5 / U-7** whether any published system reports a measured break-even reuse count, and whether the Part 2 spread is real or an artifact of the list's benchmark-era composition, remain genuinely unknown; no prevalence estimate is offered.

## 11. What must not be assumed from this packet

- Do not assume published break-even reuse counts do not exist; only that none was located in the corpus actually reached (5 benchmarks + 1 memory paper).
- Do not assume the Part 2 rates are comparable; only WebVoyager↔WebArena state a shared convention.
- Do not assume the 2608.05784 numbers are SPIDER economics; they are one person's 51-day corpus, with a modeled numerator and an explicitly unbilled dollar table.
- Do not assume absence from the retrieved PDF text layer means absence from the paper.
- Do not assume this instrument is a coverage metric for persistent-state web agents; by construction it is not.
