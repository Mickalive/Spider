# SPIDER — Global scientific-to-product audit (10 October 2026)

**Nature:** strategic synthesis, not canonical scientific evidence. **As-of:** all 1,401 uniquely indexed historical source artifacts plus the 434 subsequently finalized Research 2.0 packets, at the last verified R2 synchronization commit `8b0af54c2fa1e04e39d7ded0234c37ec896b1b4c`. **Continuity update:** the original 22 MB historical blob is now present byte-for-byte on `main` at `codex/sources/0000-historical-evidence.md`; both eras are in ONE generated `SPIDER_CODEX.md`, ONE `codex/index.json` and ONE `codex/claim_state.json`. This is a complete inventory and synthesis with selected original primary-evidence checks, **not** independent re-execution or line-by-line validation of every artifact.

## Decision in one paragraph

**The factory is generating evidence but has not generated a validated external-agent product.** The strongest defensible design is to preserve and reuse **procedures and parameterized mechanisms** while re-observing unstable values. No experiment yet establishes a net end-to-end cost reduction per successful partially novel Web task for a real external LLM agent against cold/instructions/retrieval under the same model, tools and budget. The shipped `src/spider/kernel.py` still has no `distill_parameterized()` and creates literal candidates at confidence 0.5, below the default 0.8 execution threshold. Therefore **do not equate experiment volume, PASS status, Codex synchronization, or automation reliability with product readiness**.

## 1. Sources and counting rules

1. **Historical first epoch (original, lossless)**: `codex/sources/0000-historical-evidence.md`, a byte-identical Git-blob source also frozen at `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md` (`9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`), 21,974,490 characters and 1,401 unique scientific artifacts. Source-line metadata for all artifacts is joined into `codex/index.json.historical.artifacts`. A compact source-anchored precedent for each scientific claim is joined into `codex/claim_state.json.historical_precedents_by_claim`. Selected original passages were inspected: corrected Graph speed (4.114), WP-003 invalidity (4.203), WP-003B bounded follow-up (4.237), and Product synthesis (4.697). Full inventory is **not** a fresh line-by-line independent audit.
2. **Subsequent Research 2.0 packets, same Codex**: `SPIDER_CODEX.md` at the above sync. All **434 subsequent experiment rows** were read and counted. **0 coverage gaps and 2 quarantined packets** are reported by the compiler; they do not imply every experiment is valid or reproducible. The current Codex was updated **after** the dated 433-experiment program audit.
3. **One cumulative claim state**: current effective-claim table in `SPIDER_CODEX.md`, preceded by explicit historical findings in `codex/claim_state.json`, cross-checked against `research/portfolio/PROGRAM_AUDIT_2026-10-10.md` (433-experiment snapshot) and `research/claims/registry.json`. An operational packet state must never overwrite a previous accepted epistemic status.
4. **Selected primary packets**: `EXP-PRODUCT-37973256064`, `EXP-PRODUCT-37989728440`, `EXP-GRAPH-37992949248`, together with the dated audit's referenced packets for measurement, model capability and Physics. **Source-level checks**: `src/spider/kernel.py` and `src/spider/__init__.py`.
5. **Not done**: re-run code, independently verify every historical raw artifact, inspect all 434 packets one by one, or compare every live lane branch HEAD with `main`. These must not be claimed as completed.

**Count warning:** pre-2.0 science blobs, archived workflow runs, Research 2.0 packets and PASS audits have **different units**. Do not add them into a fictional total of independent successful experiments.

## 2. Research 2.0 portfolio, exhaustive index-level reconciliation (434)

| Lane | Packets | PASS audit | REVISE | MEASUREMENT_INVALID | FAIL | BLOCKED |
|---|---:|---:|---:|---:|---:|---:|
| Graph | 79 | 28 | 16 | 23 | 7 | 5 |
| Physics | 68 | 13 | 21 | 29 | 5 | 0 |
| Runtime | 68 | 30 | 21 | 16 | 1 | 0 |
| Product | 83 | 34 | 25 | 21 | 2 | 1 |
| Frontier | 58 | 21 | 17 | 17 | 3 | 0 |
| Intel | 78 | 24 | 42 | 7 | 3 | 2 |
| **Total** | **434** | **150** | **142** | **113** | **21** | **8** |

- PASS means **audit PASS**, not a positive scientific hypothesis verdict. PASS includes valid falsifications and valid demonstrations of **infeasibility** or correct rejection. It is not a 150/434 product success rate.
- `REVISE + MEASUREMENT_INVALID = 255 / 434 = 58.8%`: enormous validation/design friction. These categories are not all wasted science, but they expose poor yield per unit of factory work. `MEASUREMENT_INVALID = 113 / 434 = 26.0%`.
- The 434th accepted canonical packet is Graph `EXP-GRAPH-37992949248`, audit PASS. It **replicates a repaired extraction certificate** but finds a **single-anchor, transport-coupled D1V population**, inadequate for a clustered false-accept estimate. It is **not** a product promotion and **does not validate freshness**.
- The prior strategic audit at `research/portfolio/PROGRAM_AUDIT_2026-10-10.md` is stale by **one packet**; otherwise its central product conclusion remains consistent with this sync.

## 2A. Continuity review — what the ORIGINAL research actually established

The original research is not discarded and its results are not counted as a new universe of independent confirmations:

| Original thread | Exact bounded result | Consequence for today's SPIDER |
|---|---|---|
| WP-000 / WP-001 | Mechanics-only rule accuracy 0.6595 on 200 tasks from 56 sites; across 100 splits, rule minus shuffle dimensional accuracy +0.0505 (95% empirical interval +0.0249 to +0.0756). | Nonrandom structure under those task protocols, **not** universal Web dynamics or a website-independent product advantage. |
| WP-002B | 300 trajectories, 901 real next-state transitions; dimensional accuracy rule 0.6238, nearest neighbour 0.6295, shuffle 0.5706; repeated-trajectory rather than website holdout. | Website transfer and rule superiority over strong NN comparator **not** established. |
| Mind2Web V0.50 | On 176 task routes, exact human route 6/176; strict causal chains 4/176; available action extraction 3843/6766. | Literal human route imitation / automatic compositionality is a weak general thesis. |
| Graph G-H1 (artifact 4.114) | Original 8.5x speed headline withdrawn; **matched** tasks: 2.822 s cold vs 2.816 s replay = **1.002x**. Replay eliminated novel decisions in this scripted setting. | Procedure reuse is credible, wall-time / real-agent savings are still unproven. |
| Graph G-H2 / G-H4 (Product ledger 4.697) | Blind composition reported 3/3 vs 0/3 limited baselines with keyword/oracle dependence. Scripted V31 paraphrase retrieval@1 2/8 to 6/8 with fresh-instrument selection caveat. | Small bounded evidence of retrieval and procedural composition, no reliable LLM consumer or true cross-site transfer. |
| WP-003 / WP-003B follow-up | WP-003 **MEASUREMENT_INVALID** (target leakage + invalid uncertainty estimate). Controlled follow-up, 875 rows, action-only MSE ~0.756 vs full ~0.735; incremental pre-state structure tiny and sensitive to outliers. | Do not resurrect the invalid original claim; action semantics and direct observation matter more than elaborate global dynamical prediction on tested features. |
| Physics WP-005 / WP-007 (historical ledgers) | Held-out-site response-transfer nulls were competitive; the WP-007 report explicitly describes negligible/outlier-driven, nonsignificant effects. | No accepted general Web-physics law emerged from the original era. |

**Longitudinal reading:** from the earliest WP tasks to the latest credential-free live HTTP work, SPIDER increasingly supports a practical distinction between **reusable procedures/mechanisms** and **unreliable ephemeral site state**. It has repeatedly failed to establish robust universal site-held-out dynamics and has not shown superior end-to-end agent economics. That consistency makes the procedural-inheritance product thesis worth **one decisive fair test**, not endless mechanism proliferation.

**Critical guard:** early historical PASS/VALIDATED labels and later R2 audit PASS have different source-specific semantics; the joint Codex records both as provenance without pretending that source artifact tokens are equivalent to final scientific decisions.

## 3. Claims: what is truly known and what is still missing

| Claim | Effective Codex state | Strongest useful finding | Product gate still missing |
|---|---|---|---|
| `C-MEAS-VALID` | **VALIDATED (bounded)** | Independent real-Chromium/authorship-separated intervention fixture, sensitivity/specificity 1.0 in the tested arms (`EXP-RUNTIME-36293257855`) | production-like, out-of-surface and transport-stable oracle; recent `EXP-RUNTIME-37973247935` was invalid due to volatile `Connection` fingerprint and stability-gate mismatch |
| `C-PARAM-INHERIT` | **EXPERIMENTAL** | Causally live parametrized path: 12/15 new identifiers executed on credential-free localhost; 0/15 literal incumbent at its frozen confidence gate (`EXP-PRODUCT-37973256064`) | integrate into shipped kernel; known-negative refusal; outperform **strong** non-degenerate cold/retrieval, not a deliberately non-executing literal baseline |
| `C-FRESHNESS` | **EXPERIMENTAL** | Two independent extraction paths agree 4/4, token/session-scoped extraction 3/4, replicated (`EXP-GRAPH-37992949248`) | multi-anchor D1V population, clustered false-accept bounds, actionable guard and cost comparison; stop replaying same four coupled anchors |
| `C-DELTA-REPAIR` | **EXPERIMENTAL** | Bounded single-node positive (`EXP-GRAPH-36018188168`) | realistic distributed repair costs and contamination; later invalid attempts do not erase old positive |
| `C-RESIDUAL-NOVELTY` | **EXPERIMENTAL** | Controlled narrow-family signal; newer Product test exposes deterministic benchmark failure | cost as a function of novelty at non-ceiling comparator performance, with real agents and amortization |
| `C-LLM-INHERIT` | **HYPOTHESIS** | Comparator wiring / candidate endpoints, but minimal Web agent capability failed on tested local 3B/7B models at 0/5 each under underspecified prompt (`EXP-INTEL-37982024058`) | functional same-model four-arm COLD / INSTRUCTIONS / RETRIEVAL / SPIDER randomized or matched test |
| `C-PRODUCT-ECON` | **HYPOTHESIS** | Break-even algebra from an external paper was not evaluable using its own commensurable denominators (`EXP-INTEL-37950616801`) | measured real recurrence, write/read/retrieval/verification/repair cost, marginal cost per **successful** task |
| `C-CROSSSITE` | **HYPOTHESIS** | No convincing leakage-free website-holdout transfer | true held-out websites and task transfer |
| `C-SEMANTIC-RESOLVE` | **HYPOTHESIS** | Bounded aliasing research, mixed real-HTTP grounding | unseen-goal calibrated resolution with abstention in product path |
| `C-WEB-DYNAMICS` | **HYPOTHESIS** | Valid negative on public HTTP server-minted gating values: only 2/46 predictable fields at 27 sites, fraction 0.04348 and site-clustered upper 95% bound 0.116 (`EXP-PHYSICS-37973239386`) | an independent, transferable mechanism producing material utility; no general 'Web physics' result |

**Mechanistic inference, not a proven commercial claim:** cache the **how** (procedure, parameters, preconditions, side-effects and verification), re-read the **what** (session identifiers, CSRF/state tokens, responses) when cheap/volatile. Neither exact replay speedups nor local accuracy suffice to establish overall cost reduction.

## 4. Three decisive product blockers, verified today

**B1 — No promoted parameterized carrier.** `src/spider/kernel.py` contains `distill()`, explicitly literal. Its candidate has confidence **0.5** and the kernel threshold defaults to **0.8**; `resolve()` can bind manually registered templates, but `distill_parameterized()` is absent. A more capable experimental carrier is **not shipped**. Audited promotion, with positive/negative tests, is prerequisite. Do not bypass the promotion gate by manual file copy.

**B2 — Benchmark degeneracy.** `EXP-PRODUCT-37989728440` and `EXP-PRODUCT-37973256064` expose cold/retrieval success **1.0** on deterministic HTTP tasks. A SPIDER treatment cannot establish a success-rate advantage over already perfect baselines. A real, multi-step, genuine-discovery task bank with reproducible counterfactual and sufficient dynamic range is necessary **before** full runs.

**B3 — Agent capability and economics.** The 3B and 7B tested endpoint candidates failed the minimal click-then-answer goal **0/5** each under a bounded underspecified prompt. The problem may be instruction quality or model ability; it is not yet resolved. No real 4-arm, same-model/same-tools/same-budget trial has demonstrated reduced total compute+browser+verification+repair+memory cost per success.

## 5. Historical pre-2.0 lessons — continuity, NOT a newly certified re-audit

The original Codex source is frozen as **historical evidence within one cumulative scientific record**. Its 1,401 individually indexed evidence artefacts and the 434 subsequent canonical experiment packets are joined through `SPIDER_CODEX.md`, `codex/index.json` and `codex/claim_state.json`. They retain distinct provenance and incomparable counting units, but **not separate research programs**. Do not confuse archived source blobs or historical run memories with independent R2 experiment packets.

Earlier project-level work reported three relevant failure patterns, which require line-level cross-checks against the large archive before being treated as revalidated:

1. **False headline improvement:** the claimed ~8.5x Graph speed result collapsed to ~1.002x on identical tasks under a fair comparison. Performance claims need same task and correct denominator.
2. **Target leakage / invalid bootstrap:** historical `WP-003` was deemed `MEASUREMENT_INVALID`; apparent predictive value from leaked `prev_action` or a mis-specified bootstrap is not evidence of transferable Web physics.
3. **Factory-control fragility:** stale prompts, branch drift, premature stopping and loss of scientific artifacts motivated the frozen Codex and Research 2.0 transaction design. Increased orchestration complexity is a **cost**, not a product feature.

**Historical verification boundary:** The frozen 21.97-million-character source and its 1,401-entry manifest are now technically readable through the Git blob. The new crosswalk, index and compact snapshot avoid forcing models to ingest the archive wholesale. Selected historical reports and the original archive summary have been read, but no complete 1,401-artifact forensic re-audit or independent re-execution has occurred. The Research 2.0 director now has explicit historical context for non-duplication. The source remains frozen.

## 6. Opportunity / risk: useful knowledge vs research theatre

### Defensible positive assets
- Frozen, audited and indexed experimental memory; negative results are retained.
- Instrumentation on a bounded Chromium fixture.
- Parameterized mechanisms can execute on a real local HTTP substrate; partial abstention/guard logic exists.
- A clear negative result on widespread persistence of ephemeral values in the public HTTP substrate.
- Independent DESIGN REVIEW and frozen-design checks reduce new avoidable invalids; **the reduction has not yet been quantified prospectively**.

### Material liabilities
- **255/434** packets are REVISE or MEASUREMENT_INVALID. Activity and correctness of workflow infrastructure risk substituting for progress.
- Benchmark families have repeatedly measured ceiling baselines, not value.
- Six lanes + Scout + Global Director + audits + Codex reconciliation are an expensive self-hosted research factory; no evidence yet that this complexity pays for itself.
- Work on marginal freshness estimators, Web dynamics or benchmark mechanics can be rational locally but useless to the near-term product.
- Persistent scientific evidence does not itself establish product-market demand or a defensible advantage over vendor-native caching, compiled workflows and retrieval.

## 7. Concrete decision and falsifiable exit criteria

**Do not fund another indefinite factory-repair/physics iteration as if it were a product milestone.** Prioritize three dependencies only:

1. **Product:** get one `distill_parameterized → resolve → execute → verify/UNKNOWN` treatment **into `src/spider/` through independent promotion**, demonstrate one known positive and one known negative, and pin the exact shipped version for testing.
2. **Runtime:** pre-certify a real multi-step task bank where cold and retrieval are **not at ceiling**, with the same task distribution, exact instrumentation, failure accounting, leakage checks and success oracle.
3. **Intel:** prove that the chosen agent can perform the **minimal** task reliably with the same tool protocol before paying for four arms; resolve prompt underspecification or explicitly choose a working endpoint.

Then run the **one decisive benchmark**: COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER; identical model, tools, budget and tasks; pre-registered success, total marginal cost **per successful task**, writes/reads, maintenance, verification, repair, repeats, novelty and repeated-task amortization. Include at least a second distinct task family to check nontrivial transfer.

**Proposed go/no-go threshold, not an observed result:** >=20% lower **fully loaded** cost per successful task compared with the strongest non-SPIDER baseline, non-inferior success/safety and a reproducible second-family effect; exact sample size/power to be pre-registered based on pilot variance. If the treatment cannot clear the positive/negative shipped-carrier gate or no non-degenerate task bank is feasible, **pause flagship economics experiments rather than regenerate invalid packets**. If it fails well-powered comparison, either narrow to the demonstrated reusable workflow niche or stop this product thesis.

**Capacity allocation recommendation:** temporarily **concentrate Product, Runtime and Intel on those three gates**. Keep Graph limited to blocking freshness/safety evidence; **PARK** repeating the same four D1V anchors. Physics and Frontier continue only with predeclared orthogonal expected decision value and a capped budget; otherwise PARK. This is an **audit recommendation**, not a change to the running workflows.

## 7A. Verification of unified Codex delivery

The latest observed `main` head at review time was `5b45e01e2f71bd8b2b7cbfdfa63b69bb1348ae6f` (2026-10-10 16:02:45 UTC). `SPIDER R2 CI` on that exact commit completed **successfully** (GitHub Actions run 38066057780). The `codex/sources/0000-historical-evidence.md` blob SHA equals the frozen archival source SHA `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`. This verifies integration integrity and control-plane tests; it **does not independently validate all experimental findings**. A Codex sync run during the integration sequence had failed on an intermediate revision; the latest successful CI is a stronger current signal of repository validity, though it is not proof that every future scheduled sync or agent run will succeed.

## 8. Answers and immediate bookkeeping

- **Are new experiments in the Codex?** Yes: `SPIDER_CODEX.md` now contains 434 accepted experiment rows; the latest verified `codex: sync Research 2.0 evidence` commit is `8b0af54c...` on **10 October 2026**. Its Graph packet is incorporated into effective C-FRESHNESS history and does **not** authorize Product promotion.
- **Does the Codex cover the historical program continuously?** Yes: original 1,401 unique source artifacts and 434 subsequent experiments are now indexed together, and the ten claim histories include historical precedents. `PROGRAM_AUDIT_2026-10-10.md` is an older 433-packet snapshot; this global audit is the newer cumulative synthesis. A merged index is not a new line-by-line scientific validation.
- **Does a usable product exist?** A conservative kernel and supporting infrastructure exist. A causally proven economically superior, externally agent-usable product **does not yet**.
- **What matters next?** Shipped executable carrier, non-degenerate task bank, capable real agent, then one directly monetizable marginal-cost result.
