# EXP-INTEL-35697055679 — Execute Report

## 1. Identity

- **Experiment**: EXP-INTEL-35697055679
- **Lane**: Intel
- **Claims**: C-LLM-INHERIT, C-CROSSSITE
- **Parent**: EXP-INTEL-35651934683 (documentation survey, audit VF5: cross-site mechanism sharing assumed, not verified)
- **Director mandate**: PIVOT to C-LLM-INHERIT; resolve VF5 by extracting accessibility trees from 2-3 WebArena shopping stores and measuring mechanism overlap, parameterization prevalence, and duplication fraction
- **Status / Outcome**: COMPLETE / MIXED
- **Frozen inputs**: request.json, spec.json, prereg.md, freeze.json (immutable; not modified)

## 2. What was executed

All frozen measurement components were executed against the WebArena-Verified v2 Docker substrate:

1. **Docker + live store**: `am1n3e/webarena-verified-shopping:latest` (digest `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb`) running as container `78f4353eb11c`, serving the Magento store "One Stop Market" at `http://localhost:7770`.
2. **Dataset parsing**: official `webarena-verified.json` (812 tasks) downloaded from `ServiceNow/WebArena-Verified` (pin: commit `ef74e1bfd0d83d4bab1c55b2d1b4c2aeaac8e0d0`, local sha256 `d6527566…`), stored as raw artifact. Cross-checked the other two official dataset files (`test.raw.json`, `webarna-verfied-hard.json`).
3. **Task selection**: 10 shopping tasks, deterministic seed `35697055679`, stratified across 10 distinct intent-template families (task ids 25, 434, 468, 506, 514, 519, 532, 654, 673, 794).
4. **Accessibility tree extraction**: Playwright 1.63 + Chromium, CDP `Accessibility.getFullAXTree` at initial viewport 1280x720 (Playwright's `page.accessibility` API is removed; CDP path validated). 10/10 pages extracted; raw trees saved with sha256.
5. **Mechanism analysis**: duplication fraction, parameterization prevalence, mechanism reuse, positive control, and manual intent→element mapping for 5 tasks (frozen requirement).
6. **Bootstrap 95% CIs** (2000 reps, seed 35697055679) for the three main fractions per the frozen analysis plan (§9).

## 3. Primary empirical finding: the "12 store instances" premise is false for WebArena-Verified v2

The single most important discovery of this run resolves audit VF5 in a **corrective** direction:

- All three official WebArena-Verified v2 dataset files contain shopping tasks **only** on the single site `shopping` (192 / 192 / 61 tasks; site tuples `('shopping',)` and `('shopping','reddit')` only). No `shopping_0 … shopping_11` identifiers exist anywhere.
- The v2 infrastructure maps `WebArenaSite.SHOPPING` to **one** container (`src/webarena_verified/environments/container/config.py`), and Docker Hub hosts only tags `[latest, 0.1.0]` for that image — no per-store images.
- The live container has a single Magento store view (`store_id=1`, `general/single_store_mode/enabled=1`, one database), so it cannot be switched between store instances.

The parent survey's `M1=1.0` "12 store instances sharing search/add-to-cart/checkout" was a **WebArena v1 documentation-level** property, imported into the survey without dataset verification (exactly the VF5 gap). Against the dataset actually available for SPIDER experiments (WebArena-Verified v2), **cross-store mechanism sharing cannot be verified because the dataset does not contain multiple stores**. This is not an infrastructure blockage (the whole Docker stack works); it is a dataset-property correction.

## 4. Measured results (task-definition level, 192 shopping tasks)

| Metric (frozen name) | Value | 95% CI | vs frozen threshold |
|---|---|---|---|
| Duplication fraction (identical intent template) | **0.9479** | [0.9167, 0.9792] | ≥0.8 → **FAILS** (frozen M2 clause) |
| … of which true copies (identical template **and** instantiation) | **0.0781** | [0.0417, 0.1146] | (diagnostic; not in frozen rule) |
| Parameterization prevalence, tasks | **0.8958** | [0.8542, 0.9375] | ≥0.1 → **PASSES** |
| Parameterization prevalence, templates | 0.8367 (41/49) | — | ≥0.1 → **PASSES** |
| Mechanism overlap across stores | **vacuous (null)** | — | clause (1) not computable; see §5 |
| Template reuse across tasks (proxy) | 0.7959 (39/49 templates; 0.9479 of tasks) | — | informative proxy for within-store reuse |

The frozen duplication definition ("tasks with identical intent templates") is high because task families repeat a template with **different parameters**: of the 182 tasks in reuse families, only 15 are exact copies — 167 (91.8%) differ in `instantiation_dict` (overall copy fraction 0.0781). So the duplication signal is dominated by **parameterized task families** — the exact substrate SPIDER's parameterized inheritance consumes — not vacuous copying.

## 5. Live-store verification (documentation → execution mapping)

- **Positive control PASSES**: the search mechanism is present in the live accessibility tree as combobox "Search" + button "Search" (homepage, task 514 tree); DOM `input#search` (placeholder "Search entire store here...", `form action=/catalogsearch/result/`) has a submit button.
- **Mechanism catalog on live pages**: "add to cart" buttons, "add to wish list" links, "add to compare", "my cart", category menuitems, "contact us", "orders and returns" appear on all sampled pages; 87 "add to cart" / 84 "add to wish list" / 84 "add to compare" occurrences across the 10 pages.
- **Manual mapping (5/5 PASS, frozen requirement)**: task 25 (reviewer-of-reviews intent ↔ reviews mechanism on product page), task 519 / 514 / 468 (wish-list intents ↔ "add to wish list" elements), task 434 (cart intent ↔ "add to cart" + "my cart"). Homepage-start tasks require one navigation step before the intent completes (no agents were run — this experiment is mechanism verification only).
- **Documented intent templates DO map to actual interactive elements**: no `MEASUREMENT_INVALID` trigger (frozen falsifier (5) not met).

## 6. Frozen decision-rule application

Frozen rule: SURVIVES requires **ALL** of overlap≥0.5 across stores, duplication<0.8, parameterization≥0.1, positive control pass, infra-blocked stores ≤1.

| Clause | Verdict |
|---|---|
| (1) mechanism overlap ≥0.5 across stores | **VACUOUS / null** — one store exists; literal 0.0 is an absent-measurement artifact, cannot legitimately support either SURVIVES or FALSIFIED-IN-SETTING ("mechanisms are store-specific" is contradicted by the observed within-store reuse) |
| (2) duplication fraction <0.8 | **FAILS** — 0.9479 (measured; frozen definition) |
| (3) parameterization ≥0.1 | **PASSES** — 0.8958 |
| (4) positive control | **PASSES** — search mechanism on live store |
| (5) infra blocks ≤1 store | **Technically passes at 0 blocked**, but the ≥2-stores precondition is unachievable: dataset defines 1 store |

Per the frozen rule, duplication ≥0.8 ⇒ **verdict = MIXED** ("tasks duplicated, inheritance less meaningful"), with the important nuance in §4 that the duplication is parameterized family reuse, not verbatim copying. Status is **COMPLETE**: every measurement that the frozen design defines on this dataset was executed validly; the vacuous clause is reported as `null` per packet semantics, not as a scientific negative.

## 7. Claim consequences (per frozen product_consequence fields)

**For C-LLM-INHERIT / C-CROSSSITE — the frozen "cross-site pairs (train on N stores, test on held-out stores)" design cannot be built on WebArena-Verified v2 shipping** because there is only one store. Product lane alternatives, in information order:

1. **Within-store parameterized inheritance**: 49 template families, 89.6% parameterized tasks, 15/192 true copies only ⇒ hold out tasks *within* families (same mechanism, different parameters) and test parameterized transfer on the single store. This is testable with the existing Docker substrate and needs no LLM differences across stores — but it is **cross-task**, not **cross-site**, and its generalization meaning is narrower than the original claim.
2. **Mind2Web cross-website splits** — subject to corrected M1≈0.31 and audit VF6 (same-mechanism overlap across splits still unverified).
3. **Authenticated v1-era multi-store WebArena** (ghcr.io/web-arena-x) — the only path that could restore a real 12-store cross-site test; historically auth-blocked.

The documentation-level M1=1.0 is demonstrated to be misleading for the actual verified dataset (frozen product_consequence_negative branch of the cross-store premise). The measured parameterization (≥0.1) and mapping validity (5/5) means **within-store parameterized inheritance design is viable** — a partial positive for C-LLM-INHERIT's parameter-slot prerequisite.

## 8. Validity notes (summary)

Detailed in `result.json.validity_notes`. Headline limitations: single-store dataset makes the cross-store metric vacuous; initial-viewport extraction only; carts/checkout executed flows unmeasured; Wikipedia null control not exercisable (no container); mapping verified at mechanism level, not through full task completion.

## 9. Artifacts

Raw accessibility trees (10), raw dataset, derived measurements, bootstrap CIs, manifest, and measurement code are listed with sha256 in `result.json.artifacts` and `provenance.json`.

## 10. Interpretation discipline

- `status=COMPLETE`: the measurement transaction completed validly; the MIXED outcome is a valid scientific result, not an execution failure.
- The vacuous cross-store metric is `null` with explanation — a missing measurement object, never converted into a falsification.
- No claim beyond the frozen scope is made: this run does **not** test LLM inheritance, does **not** execute agents, and does **not** validate Mind2Web or v1 images.