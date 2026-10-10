# SPIDER — Global scientific-to-product audit (10 October 2026)

**Nature:** strategic synthesis, not canonical scientific evidence. **As-of:** `main` Codex sync commit `8b0af54c2fa1e04e39d7ded0234c37ec896b1b4c` (2026-10-10 10:30:57 UTC). **Status:** Research 2.0 **index-level** audit, selected source-packet cross-checks, with a supplementary (2026-10-10) archive manifest and selected original historical passages now read. It is **not** a re-execution of 434 experiments or a line-by-line re-audit of the ~22 MB pre-2.0 archive.

## Decision in one paragraph

**The factory is generating evidence but has not generated a validated external-agent product.** The strongest defensible design is to preserve and reuse **procedures and parameterized mechanisms** while re-observing unstable values. No experiment yet establishes a net end-to-end cost reduction per successful partially novel Web task for a real external LLM agent against cold/instructions/retrieval under the same model, tools and budget. The shipped `src/spider/kernel.py` still has no `distill_parameterized()` and creates literal candidates at confidence 0.5, below the default 0.8 execution threshold. Therefore **do not equate experiment volume, PASS status, Codex synchronization, or automation reliability with product readiness**.

## 1. Sources and counting rules

1. **Frozen historical archive**: `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md`, commit `b5f305af3608e5c3a4e0198f505b9ced7e5f8005`, retained as the original source-of-record. Initial GitHub file reads returned an empty body due to file size, but **a direct Git-blob fetch subsequently recovered the complete 21,974,490-character archived document**, including its 1,401-entry primary manifest. Its source and metadata are now indexed in `codex/legacy_artifact_index.json`, with a curated `codex/legacy_brief.json` integrated into the global Director snapshot and a navigation protocol in `codex/LEGACY_EVIDENCE_GUIDE.md`. Selected original historical passages were inspected: the corrected 8.5x-to-1.002x matched-task comparison (artifact 4.114), WP-003 invalidity (artifact 4.203), and the bounded WP-003B follow-up (artifact 4.237). This is **access to the complete archive plus targeted primary reading**, not an independent line-by-line re-audit of all 1,401 artifacts.
2. **Research 2.0 canonical inventory**: `SPIDER_CODEX.md` at the above sync commit. All **434 experiment index rows** were read and counted. **0 coverage gaps and 2 quarantined packets** are reported by the compiler; they do not imply every experiment is valid or reproducible. The current Codex was updated **after** the dated 433-experiment program audit.
3. **Current state**: effective-claim table in `SPIDER_CODEX.md`, cross-checked against `research/portfolio/PROGRAM_AUDIT_2026-10-10.md` (433-experiment snapshot) and `research/claims/registry.json`. An operational packet state must never overwrite a previous accepted epistemic status.
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

The archived Codex is frozen and deliberately **separate** from the 434 Research 2.0 packet ledger. Preserve it; do not conflate its original science blobs, run memories or failed workflows with canonical R2 experiments.

Earlier project-level work reported three relevant failure patterns, which require line-level cross-checks against the large archive before being treated as revalidated:

1. **False headline improvement:** the claimed ~8.5x Graph speed result collapsed to ~1.002x on identical tasks under a fair comparison. Performance claims need same task and correct denominator.
2. **Target leakage / invalid bootstrap:** historical `WP-003` was deemed `MEASUREMENT_INVALID`; apparent predictive value from leaked `prev_action` or a mis-specified bootstrap is not evidence of transferable Web physics.
3. **Factory-control fragility:** stale prompts, branch drift, premature stopping and loss of scientific artifacts motivated the frozen Codex and Research 2.0 transaction design. Increased orchestration complexity is a **cost**, not a product feature.

**Historical verification boundary (updated):** The frozen 21.97-million-character source and its 1,401-entry manifest are now technically readable through the Git blob. The new crosswalk, index and compact snapshot avoid forcing models to ingest the archive wholesale. Selected historical reports and the original archive summary have been read, but no complete 1,401-artifact forensic re-audit or independent re-execution has occurred. The Research 2.0 director now has explicit historical context for non-duplication. The source remains frozen.

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

## 8. Answers and immediate bookkeeping

- **Are new experiments in the Codex?** Yes: `SPIDER_CODEX.md` now contains 434 accepted experiment rows; the latest verified `codex: sync Research 2.0 evidence` commit is `8b0af54c...` on **10 October 2026**. Its Graph packet is incorporated into effective C-FRESHNESS history and does **not** authorize Product promotion.
- **Does the dated file cover the entire historical program?** No. `PROGRAM_AUDIT_2026-10-10.md` covers 433 R2 experiments, not the newly synchronized 434th, and it explicitly treats the pre-2.0 archive as a separate frozen source.
- **Does a usable product exist?** A conservative kernel and supporting infrastructure exist. A causally proven economically superior, externally agent-usable product **does not yet**.
- **What matters next?** Shipped executable carrier, non-degenerate task bank, capable real agent, then one directly monetizable marginal-cost result.
