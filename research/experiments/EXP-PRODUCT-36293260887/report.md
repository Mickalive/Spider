# EXP-PRODUCT-36293260887 — Durability and cross-resource parameter transfer

**Lane:** product · **Status:** `MEASUREMENT_INVALID` · **Outcome:** `MIXED` · **Gate:** `NOT_DECIDABLE_AS_FROZEN` · **Promotion:** `DO_NOT_PROMOTE`

---

## 1. What this experiment was supposed to decide

The director mandate asked whether the corrected parameter-induction kernel could **durably** inherit web knowledge into a reusable mechanism, judged by five things at once: prefix preservation, end-to-end success on never-observed resources, amortization against three executed baselines, correct abstention under scrambled intent, and a hash-verified committed artifact.

**None of the five were measurable as frozen.** Three of the five were structurally undecidable before a single request was issued. That is the headline, and it is a finding about the control plane and the design, not about inheritance.

## 2. The five preconditions, and what happened to each

| # | Mandate requirement | State at freeze | Verdict |
|---|---|---|---|
| 1 | Kernel fixes **committed before freeze** | `git diff base..HEAD -- src/ tests/` was **empty** | **Not met** |
| 2 | Durable, committed, hash-verified artifact | No commit mechanism in this lane | **Not met** |
| 3 | `N_MAX` frozen in spec/freeze | Absent from **both** files | **Not met** |
| 4 | Substrate matches prereg §7 | Digest matches; **endpoints do not exist** | **Not met** |
| 5 | `n ≥ 50/family` for all arms | Substrate has 126 resource-B ids → 42/family | **Not met** |

The kernel-build failure has a precise cause. `prereg.md` §5 orders kernel fixes to be *committed before freeze*, but `scripts/check_scope.py` restricts the `design` stage to `{exp}/spec.json`, `{exp}/prereg.md`, `{exp}/failure.json`, `{exp}/model_design.json`. Product's `allowed_code_roots` are writable only in the `execute` stage. **The product lane was ordered to perform, before freeze, a step the control plane does not permit before freeze.** No prereg could have been satisfied. This is a control-plane defect, not a producer failure — and it will silently break every future product-lane prereg that has a build step.

## 3. The substrate is authentic and misdesigned

`substrate.py` hashes to `d3fe358e…f26`, exactly as prereg §7 declares. But probing it returned:

```
GET  /api/v1/schema            → 404
GET  /api/v1/items/item-1      → 404
GET  /api/v1/products/PROD-100 → 404
GET  /api/v1/collections       → 404
GET  /api/v1/categories        → 404
POST /auth/token               → 401
GET  /items?page=1&page_size=10 → 200, no Link header, parameters ignored
```

The real surface is `/`, `/{collection}/{id}`, `/{collection}?q=&limit=`. Three static tokens, no issuance, `TOKEN_EXPIRY=100` on a monotone shared store. The digest is the only thing prereg §7 checks, so a wrong design passed the freeze gate. **The substrate digest is not a design audit.**

## 4. Arm results (1158 rows, 1746 HTTP requests, 14 re-auths)

| Arm | n | Task success | 95% CI | HTTP-OK | req/task |
|---|---|---|---|---|---|
| `PC-SAME-RESOURCE` | 150 | **1.0000** | [1.0000, 1.0000] | 1.0000 | 1.0133 |
| `Treatment` *(prereg-named)* | 126 | **0.0000** | [0.0000, 0.0000] | 0.0000 | 1.0159 |
| `Treatment-IDENTITY-SLOT` | 126 | **1.0000** | [1.0000, 1.0000] | 1.0000 | 1.0159 |
| `NC-SHUFFLED-INTENT` | 126 | **0.0000** | [0.0000, 0.0000] | 0.0000 | 0.0000 |
| `NC-SHUFFLED-INTENT-FORCED` | 126 | 0.3333 | [0.3333, 0.3333] | **1.0000** | 1.0159 |
| `B-COLD` | 126 | 1.0000 | [1.0000, 1.0000] | 1.0000 | **4.0794** |
| `B-LITERAL-REPLAY` | 126 | 0.0000 | [0.0000, 0.0000] | **1.0000** | 1.0159 |
| `B-RETRIEVAL-K5` | 126 | 0.0000 | [0.0000, 0.0000] | 0.7063 | 2.2857 |

Success is strict (verb ∧ status ∧ returned entity), not HTTP-OK. That distinction is what makes the table legible.

## 5. The one genuine mechanism finding

**Prefix preservation is necessary but not sufficient for cross-resource transfer.**

The prereg-named `Treatment` binds `/items/${id}`. It correctly refuses to emit a prefix-free path — but the collection is constant across all 50 training identifiers, so a segment that never varies carries no evidence that it *should* vary. It emits `/items/PROD-100` for every product task: well-formed, prefix-preserved, HTTP 404, success 0.0000.

Make the collection a **declared identity slot** and the identical pipeline emits `/${collection}/${id}` and reaches **1.0000 on the same 126 never-observed resource-B identifiers** at 1.0159 requests/task. Held-out resource-A ids are index-disjoint from the training ids, and the A/B id namespaces are disjoint by construction, so this is not leakage.

This is a real, bounded result: it localizes the missing ingredient to *how variable resources enter induction*, and it shows prereg §5.1 alone cannot produce transfer.

## 6. The economic result is real — against one baseline only

`B-COLD` finally has genuine dynamic range: **4.0794** vs **1.0159** requests/task. Amortized ratio **0.5447** ≤ 0.85. Break-even at 50 transfer tasks; **126** were executed, so the mechanism is past break-even. Ratios against the other two baselines are **2.1875** and **0.9722**, both failing.

But `B-LITERAL-REPLAY` is not a comparator: **HTTP-OK 1.0000, task success 0.0000**, at 1.0159 requests/task. It is *cheaper than the treatment* and silently acts on the wrong entity. And decision-rule condition 5 asks for the treatment to win **"at matched end-to-end success"** while §8.5 expects those baselines to fail — so the arm with success 1.0 is compared against two arms with success 0.0. **"Matched end-to-end success" has no referent here.** The parent's flagged compound-gate pathology has recurred in the economics, not just the falsifiers.

## 7. Three frozen clauses cannot discriminate

- **F2** — requires bound path `/api/v1/<collection>/<slot>`. No implementation can satisfy this on a substrate with no `/api/v1` prefix. It is also self-contradictory: **T1 pins the collection** while **F2 requires it to vary**.
- **F6** — `N_MAX = ceil(induction/(mean_bcold − treatment))` and break-even are *the same expression*. Verified numerically: 50 == 50, `f6_is_identity = true`. It cannot fire at any data. And `N_MAX` was never frozen anyway.
- **F9** — requires the null arm's cost ratio vs `B-COLD` to be **≥ 1.0**. A correctly abstaining arm issues **zero** requests. **The threshold penalises correct abstention.**

A nine-clause conjunction containing three undiscriminable clauses is a gate that reports `SUPPORTS` by luck of arithmetic, not by evidence.

## 8. The safety finding is the strongest thing here

`NC-SHUFFLED-INTENT` abstained on **126/126** tasks at **0 requests** (induced confidences 0.38/0.40/0.44 vs a 0.8 threshold). Bypass the gate and the same mechanisms return **HTTP 200 on 100%** of tasks, apply the **wrong verb on 84/126**, and succeed on 0.3333.

The parent's liability estimate — "silently replays 80 wrong actions" — is reproduced at **84/126 (66.7%)** on an independently built substrate. **`min_confidence` is the safety mechanism, and it is load-bearing.**

**But abstention guards intent, not slot values.** False-accept: **20/20** out-of-support identifier bindings, **10/20** empty-string params, 0/20 invalid intents. A product kernel would act on any string in any slot.

One integrity note: an early draft of the runner supplied the *task family's* verb instead of the resolved mechanism's verb. That silently rescued the null arm to a false 1.0. It was found and corrected (amendment A2). It is recorded because the corrected 0.3333 is only trustworthy *because* the defect was found.

## 9. Why `MEASUREMENT_INVALID` and not `FALSIFIES`

The conjunction fails. But it fails for three reasons that must not be pooled:

1. **genuine mechanism result** — `Treatment` 0.0000;
2. **three clauses that cannot discriminate** — F2, F6, F9;
3. **substrate capacity** — F12, 42/family.

Reporting `FALSIFIES` would convert design and infrastructure defects into a scientific negative, which `AGENTS.md` forbids. `MEASUREMENT_INVALID` with `outcome: MIXED` records that the gate is undecidable **while the mechanism evidence stands on its own**.

## 10. Disposition

**DO NOT PROMOTE.** The parent promotion rule forces `promote_to_product=false` whenever the gate does not return `SUPPORTS`, and durability — the mandate's central word — is untested and untestable here.

**What is established:** a corrected prefix-preserving induction pipeline exists, reaches `EXECUTABLE` through `distill_parameterized`, passes 10/10 tests, transfers exactly when a resource is a declared slot, and amortizes to ~0.55× an executed cold baseline.

**What is not:** durability; the `/api/v1` bound-path claim; any matched-success cost comparison; anything about real Web APIs, browsers, tokens, latency or cross-site transfer.

## 11. Recommended next actions

1. **Fix the control plane**: allow a product-lane `build` stage between prereg and freeze, or move kernel fixes into `execute` and prereg them as a measurement rather than a precondition. *(blocks every product prereg with a build step)*
2. **Replace the substrate digest with a surface contract test** in the freeze gate.
3. **Make the substrate supply ≥150 resource-B identifiers** and a `N_MAX` computed at execute.
4. **Delete F6** (identity) and **restate F9** as an abstention-cost claim, not a ratio threshold; **restate F2** to match T1 or drop the `/api/v1` pattern.
5. **Re-register two stronger baselines** that succeed, so "matched end-to-end success" has a referent.
6. **Add a slot-value validity guard** before any kernel is used outside tests.

---

### Evidence index

`raw_evidence/substrate_surface_probe.json` (API surface) · `observations.jsonl` (150 obs / 50 distinct ids) · `task_results.jsonl` (1158 rows) · `probe_results.jsonl` (180 probes) · `mechanisms.json` (induced mechanisms) · `derived.json` (B=5000 family-stratified bootstraps)

`status=MEASUREMENT_INVALID` · `outcome=MIXED` · 15 falsifier clauses evaluated individually · 19 validity notes · 17 raw/derived observations · 8 unresolved items · 13 artifacts, all digests verified
