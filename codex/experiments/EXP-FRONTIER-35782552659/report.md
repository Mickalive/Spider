# EXP-FRONTIER-35782552659 — Hierarchical decoupling-before-aggregation retrieval vs flat RAG on synthetic alias-OOD

- **Lane:** frontier · **Status:** COMPLETE · **Outcome:** MIXED
- **Claim under test (C-SEMANTIC-RESOLVE):** a decoupling-before-aggregation hierarchical retrieval layer (mechanisms as episodes, template-parsed semantic components, theme grouping, adaptive top-down selection) improves alias-OOD retrieval complementarity and downstream resolution vs flat top-5 RAG (TFIDF / all-MiniLM-L6-v2) and verbatim replay, reusing the byte-identical parent synthetic fixture (EXP-FRONTIER-35773143736, 70 tasks), no new BrowserGym SPAs.

## 1. What was executed

Frozen design, executed exactly: 70 tasks × 7 pipelines (B-EXACT-MATCH, B-VERBATIM-REPLAY, B-FLAT-RAG-TFIDF-K5, B-FLAT-RAG-EMBED-K5, B-FLAT-RAG-EMBED-K1, B-RANDOM-K5, H-HIERARCHICAL-XMEMORY) = 490 paired rows. Hierarchical index = train-registry episodes → template-parsed semantic components → agglomerative themes (Jaccard ≥ 0.6, average linkage, full component sets incl. url segments), TFIDF theme centroids (fit on train registry only), adaptive k ∈ [2,5] with entropy > 0.4 OR component-type coverage < 2 expansion and min-k top-up, max 2 mechanisms per theme. Downstream = parent genuine non-oracle RULE copied verbatim (choose_adoptions + rewrite_template_multi + reconstruct_resolve, softmax temp 0.15, jitter-gated UNKNOWN < 0.80). Baseline embeddings: local all-MiniLM-L6-v2. Seed 42. Re-run twice byte-identical raw evidence.

## 2. Results

| Pipeline (alias-OOD, N=40) | correct | FA | coverage | density | mean_k |
|---|---|---|---|---|---|
| B-EXACT-MATCH | 0/40 | 1.0 | 1.0 | 1.82 | 3.0 |
| B-VERBATIM-REPLAY | 0/40 | 1.0 | 1.0 | 1.82 | 3.0 |
| B-FLAT-RAG-TFIDF-K5 | 40/40 | 0.0 | 1.0 | 1.82 | 3.0 |
| B-FLAT-RAG-EMBED-K5 | 40/40 | 0.0 | 1.0 | 1.82 | 3.0 |
| B-FLAT-RAG-EMBED-K1 | 0/40 | 1.0 | 1.0 | 3.45 | 1.0 |
| B-RANDOM-K5 | 40/40 | 0.0 | 1.0 | 1.82 | 3.0 |
| **H-HIERARCHICAL-XMEMORY** | **40/40** | **0.0** | **1.0** | **1.95** | **2.75** |

- S1 pooled: 1.0 (binom p = 1.0e-40 vs 0.10; McNemar vs exact p = 6.98e-10); orthogonal 1.0, mixed 1.0, held-out 9/9 1.0, every family 1.0.
- S2: FA 0.0 ≤ 0.15 and 1.0 below verbatim (McNemar p = 6.98e-10).
- S3: exact-match 12/12 (no regression). S4: no-applicable precision 1.0, ECE 0.1076 (bootstrap CI upper 0.1149 ≤ 0.18). S5: not dominated (tie with best flat at 1.0).
- **S6: NOT met.** Coverage gain = 0.0 (bootstrap CI [0,0], p = 1.0); density gain 0.13 (bootstrap p = 0.33, not significant).
- All controls PASS (PC-EXACT-MATCH, PC-RETRIEVAL-HEALTH, PC-HIERARCHICAL-INDEX-BUILT, NC-NO-APPLICABLE, NC-EMPTY-REGISTRY, NC-ORACLE-LEAK); NC-FLAT-COLLAPSE-DIAGNOSTIC exploratory 0.59 < 0.80. Harness errors 0; leak 0/40; forbidden keys 0.

## 3. Interpretation — why MIXED

The resolution claim holds exactly as in the parent: hierarchical retrieval + reconstruction resolves 40/40 alias-OOD, ties the best flat RAG, beats exact/verbatim replay massively. But the complementarity claim cannot be evidenced on this substrate, and the mechanism under test did not demonstrate an advantage:

1. **Substrate saturation (primary cause of MIXED):** per-task registry = 3 mechanisms and every retriever runs with k ≥ 3, so flat top-k and hierarchical adaptive selection both return the full registry on all 40 tasks. Coverage is identically 1.0 for every pipeline; hierarchical coverage gain is identically 0.0 by construction, not by mechanism failure. S6 is therefore non-identifiable (see `unresolved[0]`).
2. **Index degeneracy:** at the frozen Jaccard ≥ 0.6 threshold the 63-episode train registry clusters into 63 singleton themes. The synthetic family structure produces within-task component overlap ~0.5 and cross-task overlap ~0, so the aggregation tier contributes no grouping; the adaptive selector then behaves like a flat scan with k ∈ {2,3} (k=3 on 30 tasks, k=2 on 10), and its retrieved sets coincide with flat retrieval. The hierarchical *selection* ran faithfully (entropy/coverage expansion, min-k top-up), it just had nothing to aggregate.
3. **Reconstruction ceiling dominates:** the parent RULE rewrites the correct bound from any single retrieved mechanism of the correct alias family, so once the full family set is retrieved every reconstructed pipeline saturates at 40/40. This is why resolution parity (S1–S5) is trivially met and cannot discriminate retrieval quality.

Frozen decision rule: S1–S5 pass, S6 fails ⇒ **MIXED — "retrieval complementarity not demonstrated despite resolution not regressing; bounded claim to no complementarity advantage"** on the tested synthetic orthogonal/mixed alias-OOD substrate with minimal derived dict. This does NOT falsify hierarchical retrieval in general; it closes this substrate's ability to expose a retrieval complementarity effect (`spec.json:falsifier` FALSIFIED-complementarity clause requires a substrate where hierarchical could beat flat).

## 4. Control notes (audit-relevant)

- **NC-NO-APPLICABLE** passed under the frozen formal definition: `spec.null_control` requires "UNKNOWN (or **gated confidence<0.80**)" with false_accept ≤ 0.10, where an accept is EXECUTABLE with confidence ≥ 0.80. Six reconstructed pipelines return UNKNOWN 12/12; the no-reconstruction ablation EMBED-K1 returns EXECUTABLE 12/12 but at confidence 0.196–0.231 (< 0.80, gated) → ungated FA 0/12. The prereg summary line ("all pipelines UNKNOWN") admits a stricter status-only reading that would flip this control and force MEASUREMENT_INVALID; the formal spec definition (higher precedence) was applied and both readings are recorded in `result.json:controls["NC-NO-APPLICABLE"].observed` so AUDIT can adjudicate.
- **NC-FLAT-COLLAPSE-DIAGNOSTIC** (0.59 < 0.80 exploratory threshold) did not show similarity collapse; with pool size ≤ k the diagnostic measures full-pool template similarity (2 shared components per same-family triplet), not truncation collapse.

## 5. Economics

Latency per successful alias-OOD task (CPU-only runner): hierarchical 0.0030 s, TFIDF 0.0019 s, embed-K5 0.0359 s, random 0.0002 s; exact/verbatim/embed-K1 have zero successes on alias-OOD (null). Zero LLM calls/tokens, zero browser navigations; embeddings cached. Hierarchical adds negligible latency for identical outcomes on this substrate.

## 6. Bounded claims and next step

Established (bounded to this synthetic substrate): hierarchical + reconstruction resolves alias-OOD 40/40 without regressing exact/no-applicable/empty strata; retrieval complementarity (coverage/density gains) not demonstrated — substrate saturated (pool ≤ k) and index fragmented to singletons under the frozen threshold; EMBED-K1 ablation false-accepts alias-OOD (verbatim bind without reconstruction) and is gated (< 0.80 confidence) on no-applicable.

Smallest discriminating next test (per `unresolved`): registry of 8–12 mechanisms per task with multiple same-family candidates (intra-family overlap > k so flat truncation can drop the correct family), held-equal intents, and entropy-driven selection allowed to choose 2–5 of them; then coverage-gain and density-gain become identifiable and hierarchical-vs-flat complementarity can be genuinely discriminated.