# EXP-INTEL-37950616801 preregistration

Lane: `intel`. Target claim: `C-PRODUCT-ECON` (status HYPOTHESIS, owner lane `product`).
Director mandate action: `CONTINUE`, cycle `37949204501`.
Mode: zero-new-corpus analytic determination. No new request, corpus, browser, Docker, credential, or model call.

## 1. Question

From the already hash-pinned text layer `research/experiments/EXP-INTEL-36306525220/raw/fulltext/2608.05784v1.txt`
(sha256 `e286167a6ae51eebe1552f655876bae5a9c1728e16793b31e4adac4e9b154dbf`, 70,219 bytes / 69,607 characters / 1,447 lines):

**Is a measured break-even reuse count `f*` reportable from this literature class at all, or is the persistence-economics anchor unavailable by construction?**

The artifact prices only the branch an agent takes (the warm branch); it publishes no `f*`, no payback term and no `f*` symbol (verified: zero hits for `break-even`, `breakeven`, `break even`, `payback`, `f*`; only one `reuse count`, itself the definition of `N`). The determination is therefore whether a break-even can be **derived** from the artifact's own published values, not whether one was **published**.

## 2. Frozen artifact anchors (verbatim, line-numbered)

Eq. (1), lines 231-240:
`E[$/task] = (1-hq) Cmiss` / `p` `+hq(Chit+Cverify)` `+h(1-q)Cwrong + Cwrite` / `N` ,
`where h is recurrence, q the fraction of hits correctly matched, p the base success rate, N the reuse count, and the C-terms per-branch costs. Every term is already priced in the works above; the one input none of them measures is h on the pre-delegation passive corpus.`

Corroborating stacked equations (lines 826-833, 851-854): Eq. (2) `Cagent(k)=k(wh/750 + 350 + 180)`; Eq. (3) `R = Cagent(k)/Creplay(k)`, `Creplay(k)=|tiktoken(.)|`.

Published anchors: `R_inject = 60x` (IQR 59-62), `R_info = 343x` (lines 876, 880, 910, 913); `h = 9.0%` in-sample action granularity, `13.1%` at URL granularity, `8.6%` in-sample training days, `7.7%` out-of-sample -- "7.7% is the recurrence the cost accounting should carry" (lines 973-975, 994-995, 1010-1015); entity typing `~82%` accurate, so `q < 1` and "We do not assume q = 1" (lines 1214-1219); compile cost `<=0.5ms, 0 tokens` (line 912); median guard coverage `0.415` (lines 943, 1171); modeled 3-arm dollars `$125.81 / $20.96 / $74.46` (lines 954-957); per-covered-step recovery `1-1/R ~ 99%` (line 938); all-fleet ceiling `h(1-1/R_info) ~ 7.7%` (lines 972-975). R's numerator and the 3-arm dollars are explicitly "modeled, not billed" (lines 1160-1168).

## 3. Frozen readings and conventions (NOT silently resolved)

The preserved equation is OCR-linearized (stacked numerator over denominator), corroborated by `wh/750` and `Cagent/Creplay`. Two ambiguities move `f*` by orders of magnitude and both are carried explicitly:

- **Reading.** `VAR-LIT` (primary): the literal division reading `(1-hq)*Cmiss/p + hq(Chit+Cverify) + h(1-q)Cwrong + Cwrite/N`. `VAR-MAN` (secondary): the mandate's literal form `Cmiss*p` and `Cwrite*N`, preserved because the mandate is binding direction and may not be silently overridden.
- **Write convention.** `AMORTIZE-ONCE` (primary): `Cwrite` charged once in total, per-task write `Cwrite/N`; consistent with `f* = Cwrite/(E_cold - E_warm)`. `PER-REUSE` (secondary): `Cwrite` charged on every reuse, total `Cwrite*N`; the break-even degenerates to a single-task inequality.

Every reportability class is reported per (reading, convention) quadruple.

## 4. Derivations

(a) **Cold counterfactual, stated explicitly.** With no carried state the hit branch is empty (`h=0`) and the one-time write is absent, so `E_cold = Cmiss/p` (VAR-LIT) or `E_cold = Cmiss*p` (VAR-MAN). The artifact never prices this arm; it is supplied here because a break-even is meaningless without the alternative branch.

(b) **Warm, delta, break-even.** `E_warm = (1-hq)*E_cold + hq*(Chit+Cverify) + h(1-q)*Cwrong`. Therefore `delta = E_cold - E_warm = h*g`, with the dimensionless bracket
`g = q*(E_cold_unit - Chit - Cverify) - (1-q)*Cwrong`, independent of `h`.
`AMORTIZE-ONCE`: total warm over `N` tasks is `N*E_warm + Cwrite`, total cold is `N*E_cold`, so the break-even is `f* = Cwrite/(E_cold - E_warm) = Cwrite/(h*g)`.
`PER-REUSE`: total warm is `N*(E_warm + Cwrite)`, so the condition collapses to `E_cold > E_warm + Cwrite` and `f*=1` if true, else no `f*`.

(c) **Dimensionless form.** Normalize every C-term by `Cmiss`: `r = Chit/Cmiss = 1/R` (`R in {60,343}`), `b = Cverify/Cmiss`, `c = Cwrong/Cmiss`, `w = Cwrite/Cmiss`. Then `f* = w/(h*g)` depends only on ratios, not on absolute dollars. This is why a numeric `f*` is reportable **iff** the artifact supplies `w` in units commensurable with `Cmiss`.

(d) **Divergence condition.** Structural: `E_cold <= E_warm`, i.e. `g <= 0` -- carried state does not pay even if the write is free. Operational (AMORTIZE-ONCE): `E_cold <= E_warm + Cwrite/N`, i.e. `f* > N`. Both are stated in the report even when neither fires.

**Regime table.** Primary axes `(h, q, Cwrite/Cmiss, Cverify/Cmiss)`, frozen in `spec.json.regime_table`, with fixed primary anchors `r=1/60`, `c=1`, `p=1.0`, `N_reach=181`, and sensitivity blocks over `r in {1/60,1/343}`, `c in {0.1,1,10}`, `p in {0.5,0.8,1.0}`, `N_reach in {9,25,181}`. Per-cell outputs: `g`, `f*` (real and ceil), reachability, divergence, and the critical `h*(w) = w/(N_reach*g)`. `N_reach=181` is the artifact's own observed maximum routine occurrences (line 919) -- i.e. the most generous horizon, so a POSITIVE finding is conservative.

## 5. Controls (stable ids reused by EXECUTE/AUDIT)

- `PC-ALGEBRA` (positive): hand-computed finite `f*` (e.g. `h=0.5, q=1, p=1`, other C-terms 0, `Cwrite=1` => `f*=2`) must be reproduced to 1e-9 relative error.
- `NC-DIVERGENT` (null, must fire): a cell with `g<=0` must return divergent, and a cell with `181<f*<inf` must return unreachable; never a spurious finite positive.
- `PC-READING`: derive the fraction-parsing rule from Eqs. (2)-(3) before applying it to Eq. (1); failure => `MEASUREMENT_INVALID`.
- `PC-EXTRACT`: independent re-extraction must recover the frozen anchors; mismatch => that anchor is unavailable, not zero.
- `NC-CONVENTION` (must fire): the two write conventions must give materially different `f*`.
- `B-PUBLISHED-NUMBERS-ONLY`: the artifact itself reports no `f*` (empty baseline by construction).
- `B-FLEET-CEILING`: the artifact's strongest quantity, `h(1-1/R_info) ~ 7.7%`, is a saving rate and cannot be inverted into a break-even without the cold arm and `Cwrite`; the inversion must fail.

## 6. Measurement validity

Evidence is one hash-pinned file; any hash/size mismatch invalidates all derived measurements. All formulas/parameters are quoted verbatim with lines. The multiply-vs-divide and once-vs-per-reuse ambiguities are reported per axis, never collapsed. `p` is not published numerically and is swept, labeled unpublished. `Cwrite` is printed as compile `0 tokens` but capture/storage only in wall-clock/GB (`9.5GB`, `~0.19GB/active day`, OCR on `96%` of frames), never in dollars-per-task commensurable with `Cmiss`; whether that is an artifact-internal `w` is adjudicated explicitly, not assumed. Modeled-vs-measured follows the artifact's own labels. Scope is this artifact, not the literature class. The inherited bar is preserved: **no quantity from arXiv:2608.05784v1 may enter a SPIDER cost model, break-even derivation, product plan or investor-facing material** -- the experiment analyzes reportability of the artifact as an object and adopts none of its numbers. The table is produced by two implementations that must agree. An unresolvable mandatory input is reported as absent, never as zero.

## 7. Decision rule (ordered)

1. `MEASUREMENT_INVALID` if evidence hash/size, required span location, `PC-READING`, `PC-EXTRACT`, `PC-ALGEBRA`, `NC-DIVERGENT`, `NC-CONVENTION` or table cross-check fails. Measurement failure is not a scientific negative.
2. Classify the published slice per (reading, convention): `DIVERGENT` (`g<=0` everywhere), `FINITE_NOT_EVALUABLE` (`g>0` but no commensurable `w`, so only `h*(w)` is reportable), `UNREACHABLE` (`g>0`, `f*>N_reach` everywhere), or `REACHABLE` (some published-slice cell with `g>0`, `f*<=N_reach`).
3. Verdict: `SUPPORTS` iff `REACHABLE` for all non-secondary readings and the reachable region includes `h<=0.077`; `FALSIFIES` iff every (reading, convention) is `DIVERGENT`/`UNREACHABLE`/`FINITE_NOT_EVALUABLE`; otherwise `MIXED`, including `REACHABLE` only at `h>0.077`.
4. Always report `h*(w)` and the smallest published `h` at which `f*<=N_reach`, flagged as `<=0.077` (conservative), `<=0.131` (max published), or `>0.131` (never measured => unavailable by construction).
5. Always report both divergence conditions of section 4(d).

## 8. Consequences of positive and negative outcomes

**Positive (`REACHABLE`).** A measured break-even reuse count IS reportable from this literature class; the persistence-economics anchor is not structurally missing; one properly designed external census is worth funding as the next Intel mandate; Product may treat `h(N)` as an external estimable quantity. `C-PRODUCT-ECON` remains HYPOTHESIS pending that census; this experiment does not promote it.

**Negative (`DIVERGENT`/`UNREACHABLE`/`FINITE_NOT_EVALUABLE`).** The anchor is unavailable BY CONSTRUCTION from this artifact class: the multi-cycle external search for a published `f*` is retired permanently, no census is funded, and Product must measure its own marginal recurrence `h(N)` and first-party `Cwrite` on the shipped path before any break-even claim is admissible.

## 9. Out of scope / explicitly not done

No new corpus, search, HTTP request, browser, Docker or credential; no measurement of SPIDER's own recurrence; no prevalence claim over all persistent-state economics literature; no promotion of `C-PRODUCT-ECON`; no adoption of any artifact quantity into SPIDER economics. Prior continuity: this executes the Part B proposal of `EXP-INTEL-36306525220`, left unexecuted, and is orthogonal to the two failed external searches (`EXP-INTEL-36314207239` verdict MIXED; identity gate anti-correlated with its target).
