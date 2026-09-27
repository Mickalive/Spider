# Preregistration: EXP-INTEL-36293264917

**Lane:** intel  
**Experiment ID:** EXP-INTEL-36293264917  
**Date:** 2026-09-27  
**Parent Handoff:** EXP-INTEL-36287179392 (sha256: b82164952115ec3ac051c2b1f26ac167eb8ab44c7b928eef0ae0be24c4e9f9e2)  
**Director Mandate:** CONTINUE on C-CROSSSITE with cognitive reset; two bounded external questions.

---

## 1. Questions

### Q1: Cross-Site Transfer as a Measurable Quantity
Does any published system or benchmark report a cross-site transfer result — mechanisms learned on one set of real websites and executed on a held-out set of never-seen websites — as **four separately measurable quantities on a stated denominator**:
- (a) Transfer success on a stated N of held-out sites
- (b) Execution correctness conditional on resolution
- (c) Abstention-or-refusal rate
- (d) Either a stated boilerplate-exclusion rule OR an explicit split of task/actionable structure from shared HTML template boilerplate

Together with its **holdout rule** (leave-one-site-out or equivalent, no site-identity leakage) and its **denominators**?

And specifically, does any such report **isolate the site-pair-specific stratum** from the ubiquitous-template stratum?

**Falsifier:** If no source publishes a cross-site transfer rate in that four-part form with a stated holdout split, then C-CROSSSITE has NO external numeric comparator, the registry `next_gate` "true website holdout without site identity leakage" must be set internally, and the external-bar question is closed in the negative FOR THAT CORPUS ONLY, with bounded recall over the mandated target list recorded exactly.

### Q2: Bounding Parameters of the Whole Product
What are the exact reported figures, with source, for:
- The routine/delegable recurrence fraction in real computer and agent use (**h**)
- The overhead ratio paid for re-deriving recurrent work (**R**)
- The compile-versus-reuse build/amortization accounting convention used to report them

The Scout brief cites: Activity Frames, Routine Overhead Ratio R = 60–343x, delegable recurrence h = 7.7–9%. These are the only items in the brief that would bound SPIDER's entire economic premise from outside, and they appear nowhere in SPIDER evidence.

---

## 2. Hypotheses

- **H1 (Q1):** No published source reports cross-site transfer in the required four-part form with stated holdout split and stratum isolation. (The falsifier is the positive finding.)
- **H2 (Q2):** The only locatable primary source for the cited figures is the Activity Frames paper/report; its methodology, denominator, accounting convention, and uncertainty are not documented in a form that SPIDER can use as a measured value. (The falsifier is locating a primary source with full metadata that either confirms or refutes the cited range.)

---

## 3. Search Strategy (Frozen Before Execution)

### 3.1 Target Corpus (Mandated by Director)
The search is bounded to the following explicit target list from the director mandate dependencies and their citation snowball (1 hop):

1. **Activity Frames** (the Scout-cited source) — locate primary paper/report, extract h, R, methodology, denominator, accounting convention.
2. **WebArena** — all published papers, technical reports, benchmark documentation.
3. **WebGym** — all published papers, technical reports, benchmark documentation.
4. **WebShop** — all published papers.
5. **Mind2Web** — all published papers, especially holdout evaluation sections.
6. **MiniWoB++** — all published papers.
7. **BrowserGym** — all published papers.
8. **AgentBench** (web subset) — all published papers.
9. **Crux** / **WebVoyager** / **SeeAct** / **WebAgent** — relevant papers with cross-site or holdout evaluation.
10. **Any paper citing the above** that claims cross-site transfer or holdout evaluation (1-hop citation snowball, bounded to 50 additional papers max).

### 3.2 Search Procedure
For each target:
1. **Resolve identity:** Locate verified artifact (DOI, arXiv ID, official PDF URL, GitHub repo with paper). Record resolution status: `LOCATED` / `NOT_LOCATED` / `AMBIGUOUS`.
2. **Retrieve full text:** Download PDF or HTML via credential-free public HTTP. Record retrieval status.
3. **Extract structured metadata:** Using a fixed extraction schema (Section 4), search for:
   - Cross-site transfer claims (Q1)
   - h, R, accounting convention claims (Q2)
4. **Score against decision rule:** Apply the frozen decision rule (Section 6) to each candidate.
5. **Record outcome:** `FOUND` / `NOT_FOUND` / `PARTIAL` / `UNMEASURED` with evidence.

### 3.3 Search Tools
- Google Scholar / Semantic Scholar / arXiv API via public HTTP (no API keys required for basic search)
- Direct PDF downloads from publisher pages, arXiv, or author websites
- stdlib `requests` + `beautifulsoup4` + `tiktoken` for token counting if needed
- No browser, Docker, model API, credentials, or GPU

---

## 4. Extraction Schema (Frozen)

### For Q1 (Cross-Site Transfer)
Each candidate paper/benchmark is scored on **five required fields**. All five must be present and non-empty for `FOUND`.

| Field | Required | Description |
|-------|----------|-------------|
| `transfer_success_N` | YES | Transfer success rate on held-out sites, with explicit N (number of held-out sites) and denominator (e.g., "8/10 held-out sites succeeded" → success=0.8, N=10, denominator=10). |
| `execution_correctness_given_resolution` | YES | Execution correctness **conditional on successful mechanism resolution** (e.g., "of resolved mechanisms, 85% executed correctly"). Not overall success. |
| `abstention_refusal_rate` | YES | Rate of abstention or refusal (mechanism not applied, or agent declined to act). Must be separately reported. |
| `boilerplate_exclusion_or_split` | YES | Either: (i) explicit rule for excluding shared HTML template boilerplate from the transfer metric, OR (ii) explicit split of results into "task/actionable structure" vs "shared boilerplate" strata. |
| `holdout_rule` | YES | Stated holdout procedure: leave-one-site-out, k-fold site holdout, or equivalent. Must explicitly state no site-identity leakage (e.g., no site-specific features in training). |

**Stratum Isolation (additional required field for FOUND):**
| Field | Required | Description |
|-------|----------|-------------|
| `site_pair_stratum_isolation` | YES | Explicit separation of site-pair-specific transfer (mechanisms that transfer between specific site pairs) from ubiquitous-template transfer (mechanisms that work everywhere because of shared HTML boilerplate like `<ul>`, `<nav>`, etc.). |

### For Q2 (Bounding Parameters)
Each candidate source is scored on **four required fields**. All four must be present for `LOCATED`.

| Field | Required | Description |
|-------|----------|-------------|
| `delegable_recurrence_fraction_h` | YES | Reported value of h (fraction of activity that is routine/delegable/recurrent), with explicit denominator (e.g., "7.7% of all user actions" or "9% of task steps"). |
| `overhead_ratio_R` | YES | Reported value of R (overhead ratio for re-deriving recurrent work vs. reusing), with explicit definition of numerator and denominator (e.g., "re-derivation cost / reuse cost = 60x"). |
| `accounting_convention` | YES | Explicit statement of the compile-versus-reuse build/amortization accounting convention: how fixed costs are allocated, what counts as "compile" vs "reuse", time horizon, discounting. |
| `uncertainty_or_range` | YES | Reported uncertainty, confidence interval, or range (e.g., "60–343x" with explanation of what drives the range). |

---

## 5. Controls (Frozen)

### Positive Control: PC-KNOWN-TRANSFER-PAPER
- **Target:** A known paper reporting cross-site transfer in a multi-quantity form (e.g., WebShop holdout evaluation, Mind2Web cross-domain results).
- **Purpose:** Verify the search pipeline can detect transfer claims when they exist.
- **Pass criterion:** Pipeline extracts at least `transfer_success_N` and `holdout_rule` from this paper. Absence of the full four-part form is recorded as `PARTIAL` detection, not failure.
- **If this control fails (pipeline finds nothing):** Measurement is INVALID — search pipeline has no sensitivity.

### Null Control: NC-FABRICATED-CLAIM
- **Target:** A deliberately fabricated claim inserted into the search corpus:
  - Title: "Universal Cross-Site Transfer at 95% Success Across 100 Held-Out Sites"
  - arXiv ID: `arXiv:2609.99999` (non-existent)
  - Claimed four-part form with all five Q1 fields populated.
- **Purpose:** Verify the pipeline flags unverifiable claims as `NOT_LOCATED`/`UNMEASURED`, not as verified findings.
- **Pass criterion:** Pipeline records this target as `NOT_LOCATED` (identity resolution fails) or `UNVERIFIED` (identity resolves but claims cannot be verified in source). **Must not** record as `FOUND` or `PARTIAL` with positive scores.
- **If this control fails (pipeline accepts fabricated claim):** Measurement is INVALID — pipeline has no specificity.

---

## 6. Decision Rule (Frozen)

### Q1 Decision Rule
| Outcome | Condition |
|---------|-----------|
| `FOUND` | ≥1 source with **all five Q1 fields** non-empty and verified in source text. |
| `PARTIAL` | ≥1 source with ≥3 of 5 Q1 fields, OR all 5 fields but `site_pair_stratum_isolation` missing, OR holdout rule/denominators missing. Each gap recorded. |
| `NOT_FOUND` | Zero sources with ≥3 of 5 Q1 fields after exhaustive search over bounded target list. Bounded recall = (targets searched) / (targets in mandated list + snowball). |
| `UNMEASURED` | Target identity not resolved (`NOT_LOCATED`), or full text not retrievable. Recorded per target. |

**Terminal condition for Q1:** Search completes over bounded target list → `FOUND` / `NOT_FOUND` / `PARTIAL` with bounded recall recorded.

### Q2 Decision Rule
| Outcome | Condition |
|---------|-----------|
| `LOCATED` | ≥1 source with **all four Q2 fields** non-empty and verified in source text. |
| `PARTIAL` | ≥1 source with 2–3 of 4 Q2 fields, OR Activity Frames located but fields partially documented. Gaps recorded. |
| `NOT_LOCATED` | Zero sources with ≥2 of 4 Q2 fields after exhaustive search. Bounded recall recorded. |
| `UNMEASURED` | Target identity not resolved or full text not retrievable. |

**Terminal condition for Q2:** Search completes over bounded target list → `LOCATED` / `NOT_LOCATED` / `PARTIAL` with bounded recall recorded.

### Overall Experiment Status
| Status | Condition |
|--------|-----------|
| `COMPLETE` | Both Q1 and Q2 reach terminal state (`FOUND`/`NOT_FOUND`/`PARTIAL`/`LOCATED`/`NOT_LOCATED`) with bounded recall recorded. NC-FABRICATED-CLAIM passes (flagged as unverified). Identity-before-scoring respected for all targets. |
| `MEASUREMENT_INVALID` | NC-FABRICATED-CLAIM accepted as verified, OR identity-before-scoring violated for any scored target, OR infrastructure failure prevents search completion. |
| `BLOCKED` | Infrastructure failure (network, rate limits) prevents completing the bounded search. Retryable. |

---

## 7. Validity Threats (Declared Upfront)

1. **Search incompleteness:** Bounded target list may miss relevant sources. Mitigated by: explicit mandated list + 1-hop snowball, bounded recall recorded exactly.
2. **Publication bias:** Negative results (no transfer) are rarely published. Mitigated by: decision rule treats `NOT_FOUND` as a valid scientific outcome, not a failure.
3. **Extraction ambiguity:** Papers may report transfer in non-standard terms. Mitigated by: frozen extraction schema requires explicit fields; ambiguous reports score as `PARTIAL` or `UNMEASURED`, not `FOUND`.
4. **Identity resolution failure:** Some targets may not have accessible full text. Mitigated by: `NOT_LOCATED` recorded as `UNMEASURED`, never as negative.
5. **Null control failure mode:** If NC-FABRICATED-CLAIM is accidentally resolved to a real paper (arXiv collision), the control is void. Mitigated by: using a clearly fake arXiv ID (`2609.99999`) and fake title.

---

## 8. Artifacts to Produce

1. `search_log.jsonl` — One line per target: target_id, resolution_status, retrieval_status, extracted_fields, decision_rule_score, evidence_quotes.
2. `q1_summary.json` — Aggregated Q1 result: outcome, bounded_recall, list of FOUND/PARTIAL sources with field completion.
3. `q2_summary.json` — Aggregated Q2 result: outcome, bounded_recall, extracted h/R/accounting/uncertainty with source.
4. `controls_result.json` — PC-KNOWN-TRANSFER-PAPER and NC-FABRICATED-CLAIM results.
5. `bounded_recall.json` — Exact accounting: mandated_targets, snowball_targets, searched, located, retrieved, scored.
6. `result.json` — Canonical producer handoff per EXPERIMENT_PACKET.md.
7. `report.md` — Interpretation bounded by measurements.
8. `provenance.json` — Commits, environment, commands, artifact hashes.

---

## 9. Consequences

### If Q1 = FOUND
- C-CROSSSITE gains an external numeric comparator.
- The program can benchmark against it rather than setting its own holdout rule.
- Registry `next_gate` for C-CROSSSITE updated to reference the external comparator.

### If Q1 = NOT_FOUND
- C-CROSSSITE has NO external numeric comparator.
- Registry `next_gate` "true website holdout without site identity leakage" **must be set internally** by the owner lanes (physics, graph, frontier).
- The external-bar question is **closed in the negative FOR THAT CORPUS ONLY**.
- Bounded recall over the mandated target list recorded exactly in Codex.
- 47 prior C-CROSSSITE experiments failing to produce one become explicable.

### If Q2 = LOCATED
- SPIDER has measured bounding parameters h and R with known accounting.
- Product economics can be quantitatively bounded.
- Break-even for inheritance becomes computable with defended assumptions.

### If Q2 = NOT_LOCATED
- SPIDER has NO measured value for h and R.
- The Scout brief's figures (R=60–343x, h=7.7–9%) remain **unverified priors**.
- If h is truly ~8%, no inheritance quality changes the economic ceiling — this is a critical product-bounding fact.
- The program must either measure h/R internally or acknowledge the unbounded economics.

---

## 10. Scope Boundaries (Do Not Assume)

- This experiment does **not** run any Web-agent evaluation, browser automation, or model inference.
- This experiment does **not** measure SPIDER's own cross-site transfer (that belongs to physics/graph/frontier owner lanes).
- This experiment does **not** re-crawl the 15-host corpus from EXP-INTEL-36287179392.
- This experiment does **not** validate or invalidate C-CROSSSITE as a scientific hypothesis — it only resolves whether an **external comparator in the required form exists**.
- Negative outcomes (`NOT_FOUND`, `NOT_LOCATED`) are **first-class scientific results**, not failures.
- The null control NC-FABRICATED-CLAIM is **essential** — if it fails, the entire measurement is INVALID regardless of Q1/Q2 outcomes.

---

## 11. Inherited State from Parent Handoff (Preserved Per Contract)

| Category | Content |
|----------|---------|
| **Established** | Per-observation cost floor: 763 tokens / 2,801 bytes (minimal HTTP+HTML structural representation), 68x/66x/22x vs baselines, n=155 from 15 eTLD+1 hosts, paired bootstrap CIs strictly negative. Frozen primary prevalence clause UNEVALUABLE (algebraic identity x>x). 97.25% matched instances are list signatures; 3.51% site-pair-specific stratum. NC-SIG-REASSIGN powered null shows observed sharing below random re-partition. |
| **Rejected** | Frozen primary clause as prevalence test; frozen 2-host positive-control threshold (arithmetically unreachable); AGF magnitude as prevalence fraction or comparable to external numbers; 22.01x a11y ratio as real browser advantage; measured sharing as evidence for addressable cross-site market. |
| **Unknown** | Whether alias-generalizable cross-site TASK structure exists vs. boilerplate; whether 3.51% site-pair stratum is above its own null; client-rendered cost floor; whether unmeasured hosts would change decomposition; whether powered-null direction is robust; whether conservative template extractor reduces boilerplate share; whether external baseline exists; whether cost ratios survive rendering substrate; sample skew effects. |
| **Do Not Assume** | `primary_satisfied=null` ≠ false/negative; MIXED ≠ partial support for prevalence; 97.25% list share ≠ bounded negative on C-CROSSSITE; 83.51 ≠ fraction in [0,1]; 22.01x ≠ real a11y advantage; cost floor not portable outside scope; unmeasured hosts ≠ negatives; gitlab.com etc. entries ≠ platform measurements; NC-SIG-REASSIGN ≠ frozen decision input; this packet ≠ promotion; parked census route ≠ reopened; parent handoff next_question ≠ authorized; B-CROSSSITE-HIERARCHICAL ≠ re-validated. |

---

## 12. Signatures

This preregistration is frozen before any search execution. The frozen hash will be recorded in `freeze.json` by the deterministic freezer.

**Designer:** SPIDER Research 2.0 Intel Lane  
**Date:** 2026-09-27