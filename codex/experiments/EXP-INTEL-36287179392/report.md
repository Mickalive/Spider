# EXP-INTEL-36287179392 — EXECUTE report

- **Lane**: intel
- **Claim**: C-CROSSSITE (`research/claims/registry.json`, status `HYPOTHESIS` at execute time)
- **Mandate**: `REOPEN` with cognitive reset, `request.json.director_mandate.allocation`
- **Frozen inputs**: `request.json`, `spec.json`, `prereg.md` — all three sha256-verified unmodified against `freeze.json` at execute time
- **Status**: `COMPLETE` — **Outcome**: `MIXED` (prereg §12 MIXED clause 3)
- **Canonical machine handoff**: `result.json`. This report explains it and must not exceed it.

---

## 1. The one-paragraph version

The measurement ran. Credential-free public HTTP was enough: 177 requests to 23 hosts, 155 real pages from 15 of the 20 pre-registered sites, 0 extraction failures, no credentials, no browser, no model API, no registry. The **cost** half of the frozen design is measured and strongly satisfied: a minimal HTTP+HTML structural representation costs 763 tokens per observation against 16 794 for an accessibility-tree approximation, 50 907 for full DOM and 52 020 for raw HTML — 22.0x, 66.7x and 68.2x smaller respectively, on the same 155 observations. The **prevalence** half of the frozen design **cannot return a verdict**, because the frozen null control is an exact algebraic identity on the frozen estimator: 1 000 permutations of the eTLD+1 labels produced exactly one distinct AGF value, bitwise equal to the observed point estimate. The frozen primary clause is `83.51083467094703 > 83.51083467094703`. **This is not a negative result about C-CROSSSITE and not an infrastructure failure.** It is a defect in the frozen estimator/null pair, it is the exact failure class the director mandate predicted, and the packet says so in `result.json.validity_notes[0..1]` rather than hiding it inside a `false`.

---

## 2. What was measured, and how

Frozen `prereg.md` §§5–12 executed as written. Site sample frozen in §5.2 before any request; 10 pages/site cap; 1.05 s per-host minimum interval; `robots.txt` fetched once per host and honoured wherever a parsable body was returned (16 hosts HTTP 200; `git-scm.com` and `kernel.org` 404, treated as unrestricted per §13; `stackoverflow.com` 418 and `www.npmjs.com` 403 returned no rules and none were applied); `User-Agent: SPIDER-Research/1.0`; no JS execution.

| | |
|---|---|
| Sites pre-registered / measured (≥2 pages) | 20 / 15 |
| Pages retained / extraction failures | 155 / **0** |
| HTTP requests / distinct hosts | 177 / 23 |
| Total signatures extracted | 4 984 |
| Bootstrap (eTLD+1-level) | 10 000 replicates, seed 36287179392 |
| Shuffled-host null | 1 000 permutations, seed 36287179393 |
| Tokenizer | `cl100k_base`, n_vocab 100 277 |

**Producer verification before any conclusion** (`provenance.json.verification_performed_by_producer`): the frozen AGF and mean pairwise Jaccard were recomputed by brute force over all 105 host pairs, written without reference to the pipeline's closed form, and agree exactly (`matched 416218`, `total 4984`, `AGF 83.510834670947`, `mean Jaccard 0.126721042325`). Two consecutive analysis runs are byte-identical.

---

## 3. The primary result: the frozen design cannot answer its own question

`prereg` §7.3 defines

```
AGF = (matched signature instances across all eTLD+1 pairs) / (total signatures)
```

and `prereg` §8.1 defines the null as *"randomly permute eTLD+1 labels"*.

Write AGF key-by-key. For signature key `K` with `n_{s,K}` instances on host `s` and total `T_K`:

```
AGF = Σ_K (T_K² − Σ_s n_{s,K}²) / (2 · total_signatures)
```

**`Σ_s n_{s,K}²` is symmetric in the hosts.** Permuting the eTLD+1 labels is a bijection on hosts, so it permutes the vector `(n_{s,K})_s` and leaves every `Σ_s n_{s,K}²`, hence every `T_K`, hence `AGF` **exactly invariant**. The prescribed null is an identity, not a weak null.

Empirically: **1 distinct value over 1 000 permutations.** The frozen secondary metric, mean pairwise Jaccard, is invariant for the same reason and also took exactly 1 distinct value.

Consequence, stated precisely so nothing downstream over-reads it:

- `metrics.decision_rule_evaluation.primary_evaluable = false`
- `metrics.decision_rule_evaluation.primary_satisfied = **null**` — *not* `false`
- validity sub-condition `null_std_gt_0` fails; the other two (`agf_ci_width_gt_0`, `n_sites_ge_2pages_ge_10`) pass, so validity is *partially* failed
- `prereg` §12 MIXED clause 3 applies → `outcome = MIXED`

**MIXED here does not mean partial support for the prevalence hypothesis.** It records that the cost half produced a valid, strong measurement while the prevalence half is unevaluable. `prereg` §18's `INCONCLUSIVE (MEASUREMENT_INVALID)` row was considered and rejected: there was no infrastructure or substrate failure, 0 extractions failed, and encoding this as `MEASUREMENT_INVALID` would teach the lane the wrong lesson — the director mandate §`portfolio_assessment` explicitly warns against converting absent capability into a validity gate. The smallest unblocking action here is a null with power, not a new prerequisite.

---

## 4. Why the frozen positive control could not have passed either

`prereg` §11.2 expects `AGF > 0.8` from a **2-host** synthetic pair. Under the frozen §7.3 definition, a 2-host design caps at exactly **0.5**: with `n` signatures per host, all keys distinct and matched 1:1, matched instances `= n` and total signatures `= 2n`, so `AGF = n/2n = 0.5`. The threshold is arithmetically unreachable whatever the synthetic content. Observed `0.5833` — above the 0.5 ceiling, because two matched instances come from duplicated keys.

**The pipeline's sensitivity is nonetheless confirmed**, on two independent powered comparisons:

| Positive-control evidence | Value | Null | Verdict |
|---|---|---|---|
| mean pairwise Jaccard, 2 hosts | **1.0** (identical signature sets) | NC-SIG-REASSIGN p95 = 0.818 | detected |
| AGF, 2 hosts | **0.583** | NC-SIG-REASSIGN p95 = 0.500 | detected |
| 4-host extension: related pair | Jaccard **1.0** (1/1 pairs) | null Jaccard p95 = 0.1646 | detected |
| 4-host extension: unrelated pairs | Jaccard **0.0** (5/5 pairs) | — | discriminated |

So `PC-SYNTHETIC-ALIAS` **passes on its stated purpose** (confirm the pipeline detects known cross-site correspondence) and its numeric threshold is a design defect. A 4-host power extension was added — clearly labelled **not frozen, decision-not-used** — because with 2 hosts the label-permutation null is symmetric and hence exactly degenerate by the same identity as §3. Note its own limit honestly: at 30 signatures over 4 hosts the AGF-vs-null comparison is *underpowered* (null reaches the observed 0.4667), so the extension's verdict rests on Jaccard, not AGF.

---

## 5. What the measurement actually shows about prevalence (supplementary, decision-not-used)

`result.json` reports this as non-frozen. It is included because a packet that says only "the null was broken" wastes a completed real-Web run over 155 pages.

**A null with power.** `NC-SIG-REASSIGN` permutes the pooled signature multiset across hosts while preserving each host's signature count *and* the global multiset exactly. 869 distinct null values over 1 000 draws (vs 1 for the frozen null).

| Statistic | Observed | Frozen null p95 | Powered null p95 | Observed vs powered null |
|---|---|---|---|---|
| AGF (frozen population) | **83.51** | 83.51 (identity) | 102.09 | **−18.58** |
| AGF (typed-slot population) | **80.04** | 80.04 (identity) | 100.67 | **−20.63** |
| mean pairwise Jaccard | **0.1267** | 0.1267 (identity) | 0.3774 | **−0.2507** |

Cross-site structural sharing on this sample sits **at or below** what a random re-partition of the same template vocabulary produces. Read carefully: this is evidence against the specific mechanism the frozen statistic can see. It is **not** a bounded negative on C-CROSSSITE, because the frozen statistic cannot tell reusable *task* structure from shared *boilerplate*.

**The decomposition is the informative part.** Only **67 distinct signature keys** are shared by ≥2 of the 15 hosts, and they account for all 416 218 matched instances:

| Driver key | Share of all matched instances |
|---|---|
| `list(ul, /{slug}/{slug})` — a `<ul>` whose items link to a 2-segment path | **49.6 %** |
| `list(ul, <li>)` — a `<ul>` of `<li>`s with no links at all | **20.5 %** |
| `list(ul, /{slug})` | 9.6 % |
| `list(div-children, <a>)` | 7.7 % |
| *top 4 combined* | **87.4 %** |

Stratified by how many hosts carry the shared key:

| Hosts carrying the key | Share of matched instances |
|---|---|
| exactly 2 of 15 | 0.33 % |
| 3–5 of 15 | 3.19 % |
| 6–10 of 15 | 53.11 % |
| 11–15 of 15 | 43.38 % |

**96.5 % of all measured cross-site matching comes from structure carried by 6 or more of the 15 hosts, and only 3.5 % from the site-pair-specific regime** — which is the regime a cross-site *inheritance* product would actually monetise. `list` signatures are 67.4 % of all signatures and 97.3 % of all matched instances; `pagination` produced 3 matched instances out of 26 signatures. The frozen AGF is, in substance, measuring the fact that the Web is built out of `<ul>` elements. That is a tautology, not an addressable market — and it is not detectable from the AGF magnitude alone, which is why the packet reports the decomposition rather than the headline number.

---

## 6. The cost result (frozen, valid, decision-relevant)

All four representations computed on the same 155 observations. Frozen `prereg` §10 cost clause **satisfied**.

Per observation, mean (median):

| Representation | bytes | tokens |
|---|---|---|
| `B-RAW-HTML` | 151 741 (48 773) | 52 020 (13 432) |
| `B-FULL-DOM` | 145 141 (47 512) | 50 907 (12 887) |
| `B-A11Y-TREE` (prereg approximation) | 48 693 (30 447) | 16 794 (10 599) |
| **minimal structural** | **2 801 (2 138)** | **763 (576)** |

Paired differences, `minimal − baseline`, with eTLD+1-level bootstrap 95 % CI:

| Comparison | mean diff | CI upper | % observations where minimal is smaller |
|---|---|---|---|
| vs full DOM (tokens) | **−50 144** | **−22 824** | 155/155 = 100 % |
| vs a11y (tokens) | **−16 031** | **−8 932** | 150/155 = 96.8 % |
| vs raw HTML (tokens) | −51 257 | — | 155/155 = 100 % |
| vs full DOM (bytes) | −142 340 | — | 155/155 = 100 % |
| vs a11y (bytes) | −45 892 | — | 150/155 = 96.8 % |

Ratios (mean baseline ÷ mean minimal): **66.7x** tokens / 51.8x bytes vs full DOM; **22.0x** tokens / 17.4x bytes vs a11y; 68.2x tokens vs raw HTML. Every CI upper bound is strictly negative, so the frozen cost clause passes with room.

This is the `spec.estimated_cost` and `product_consequence` half of the mandate answered by measurement: the observation-cost floor is real and large, and it carries denominators (155 observations, 15 hosts) and a stated convention (`cl100k_base`) with every number, per the mandated shared per-span cost ledger.

---

## 7. Validity threats, disclosed

Full list in `result.json.validity_notes` (13 entries). The load-bearing ones:

1. **No JS execution** (frozen). Under-samples client-rendered sites; `crates.io` yielded *zero* discoverable pages for this reason. The measured AGF is a lower bound on the HTTP-observable structure of this sample and says nothing about the JS-observable remainder.
2. **`B-A11Y-TREE` is the prereg approximation**, not a browser accessibility tree — no browser binary was available and the frozen prereg forbids requiring one. It is a lower bound on true a11y cost, so 22.0x is an **upper** bound on the real advantage.
3. **Typed-slot parameterization is a heuristic.** Any single-segment path templates to `/{slug}`, so structurally unlike sites can share a template. This inflates AGF in *every* population including the nulls. 66.1 % of signatures carry ≥1 typed slot.
4. **Sampling bias.** 15/20 hosts measured; 4 of the 5 failures were edge blocks of the frozen User-Agent, so the surviving sample skews toward documentation/reference/foundation sites — the least e-commerce-like members of the frozen sample.
5. **Frozen-sample fidelity deviation.** 3 of 20 base URLs crossed hosts on redirect (`gitlab.com` → `about.gitlab.com`, `linuxfoundation.org` → `www.linuxfoundation.org`, `readthedocs.io` → `about.readthedocs.com`), so those entries measured corporate sites rather than the sites §5.2 named. Not corrected: the sample is immutable and the prereg forbids adaptive sampling.
6. **6 of 20 frozen "eTLD+1" labels are not registrable domains** (`docs.python.org`→`python.org`, `dockerhub.io`→`docker.com`, …). Frozen labels were used as the shuffle/bootstrap unit as specified; derived domains recorded per site.
7. **`AGF` is unbounded above** — one signature can match on every host pair. 83.51 is not a fraction in [0,1] despite §7.3's wording, and is not comparable to any externally reported prevalence number without that convention.
8. **Discarded attempt 1**, retained as evidence: it resolved §5.3 "same-origin" as same-registrable-domain, walking `en.wikipedia.org` onto 300+ sibling language Wikipedias (400 distinct request hosts for a 20-site sample), and applied an unauthorised Content-Type filter that discarded 540 valid Wikipedia pages. **No outcome metric was computed from it.** Conforming re-run: 177 requests, 23 hosts.

### NOT_MEASURED, per portfolio directive G1

Five hosts yielded <2 pages. None is a negative; each carries its exact blocking artefact in `provenance.json.dataset.not_measured`:

| Host | Blocking artefact |
|---|---|
| `npmjs.com` | HTTP 403 on homepage; `robots.txt` also 403 |
| `sourceforge.net` | HTTP 403 on homepage |
| `stackoverflow.com` | HTTP 403 on homepage; `robots.txt` also 418 |
| `crates.io` | HTTP 200, zero same-origin anchors (client-rendered app) |
| `kernel.org` | HTTP 200, zero same-origin anchors (external links only) |

The `robots.txt` fetches independently corroborate the two most important blocks: the 403 on `www.npmjs.com/robots.txt` and the 418 on `stackoverflow.com/robots.txt` show these are **host-level edge behaviours under the frozen User-Agent**, not per-path decisions by those sites. That also means the frozen sample's three largest developer-package/documentation hubs are structurally unreachable to any SPIDER probe presenting this identity.

---

## 8. What this packet does and does not license

**Established at the measured ceiling:**

- The per-observation cost floor for a minimal HTTP+HTML structural representation on real public sites is **763 tokens / 2 801 bytes** (n = 155, 15 hosts), **22.0x–68.2x smaller in tokens** than accessibility-tree, full-DOM and raw-HTML representations, with every paired bootstrap CI upper bound strictly negative. This is a *cost* fact about observation representation, nothing more.
- The frozen pipeline **can** detect known cross-site structural correspondence (positive control, Jaccard 1.0) and **can** discriminate unrelated structure (5/5 unrelated pairs exactly 0.0).
- The frozen `AGF` + label-permutation null pair is **provably non-identifying**, and the frozen 2-host `AGF > 0.8` positive-control threshold is **arithmetically unreachable**. Both are reusable facts for any future C-CROSSSITE design.

**Explicitly NOT established, and must not be assumed:**

- That alias-generalizable cross-site structure is prevalent on the real Web. The frozen clause is unevaluable (`primary_satisfied = null`).
- That it is *absent*. The supplementary powered-null direction is suggestive, not a bounded negative; the statistic cannot separate reusable task structure from shared boilerplate.
- Any external baseline bar. This packet produced none for prevalence.
- Anything about JS-rendered sites, mobile, authenticated apps, or the 5 unmeasured hosts.
- That `C-CROSSSITE` should change status. The producer does not self-promote and proposes no status change; the claim is `HYPOTHESIS` and the Director owns that call.

**Smallest unblocking action, if the Director wants the prevalence side closed:** a *statistic* that is not invariant to host relabelling and a null built on a permutation that is. `NC-SIG-REASSIGN` is one working construction, already implemented and seeded, but it was produced here and is not frozen — it needs independent confirmation before any lane re-scopes on its direction. The cheap precursor is a falsifier test on the decomposition itself: if reusable cross-site structure is real, the site-pair-specific stratum (keys shared by 2–5 hosts) should be non-trivial relative to its own null, and on this sample it is 3.5 % of matched instances.
