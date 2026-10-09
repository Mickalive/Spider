# EXP-INTEL-37950616801 — Report

**Lane:** intel
**Status:** COMPLETE
**Outcome:** FALSIFIES
**Primary class:** FINITE_NOT_EVALUABLE
**Conditional class (if placeholder `w` sweep accepted):** REACHABLE

---

## 1. Question

Does the hash-pinned persistent-state economics artifact
(`research/experiments/EXP-INTEL-36306525220/raw/fulltext/2608.05784v1.txt`,
arXiv:2608.05784v1, sha256 `e286167a…4dbf`) report, or permit derivation of,
a **measured break-even reuse count `f*`** for persistent browser/agent state —
i.e. an `f*` with a stated denominator backed by the artifact's own published
numbers — or is the persistence-economics anchor unavailable by construction?

This is a reportability determination over one artifact. It is **not** a
prevalence claim over the literature, and it does **not** measure SPIDER's own
recurrence.

The frozen claim under test is `C-PRODUCT-ECON` (status HYPOTHESIS, owner lanes
product + graph). This experiment may not promote it; it produces bounded
evidence for the lane DIRECTOR.

## 2. Evidence and equation

Evidence was verified against `spec.json`: sha256, 70,219 bytes, 69,607
characters, 1,447 lines — all match; PC-EXTRACT recovered all 34 anchors.

Eq. (1) (lines 231–240) is the per-task economics:

```
E[$/task] = (1-hq) · Cmiss/p + hq · (Chit + Cverify)
            + h(1-q) · Cwrong + Cwrite/N
```

- **cold term** = `Cmiss/p` (OCR linearization; the stacked fraction is printed
  as numerator line `/` denominator line),
- **write term** = `Cwrite/N`,
- `N` = reuse count; `h` = recurrence rate; `q` = hit/typing accuracy.

**PC-READING** derived the stacked-fraction = division rule from Eqs. (2)–(3)
(`wh/750`, `Cagent(k)/C` `replay(k)`) and applied it to Eq. (1), selecting
**VAR-LIT** (`Cmiss/p`, `Cwrite/N`) as the primary reading. The mandate's literal
secondary reading **VAR-MAN** (`Cmiss·p`, `Cwrite·N`) is carried throughout and
never collapsed.

## 3. Algebra

Write `g = q·(Cmiss/p − Chit − Cverify) − (1−q)·Cwrong` (dimensionless saving
bracket; independent of `h` and `w = Cwrite/Cmiss`). Under AMORTIZE-ONCE:

```
f* = w / (h · g)
```

For the per-reuse comparison convention, the write term is charged every reuse,
so `f* = 1` when `h·g > w` and no finite `f*` otherwise (degenerate).

The break-even is only meaningful when `g > 0`. At the artifact's published
point estimates (`r = 1/60`, `b = 0`, `c = 1`, `p = 1`):

| q | g | meaning |
|---|---|---|
| 0.82 | **+0.6263** | entity-typing accuracy (published) |
| 1.0 | +0.9833 | perfect typing (upper bound) |
| 0.415 | −0.1769 | guard-coverage proxy, **not** Eq. (1)'s q |

So structural divergence (`g ≤ 0`) does **not** occur at the published `q ≈ 0.82`:
there is a positive finite `f*` *if* `h` and `w` are known.

## 4. The blocking quantity: `w = Cwrite/Cmiss`

The artifact does **not** publish a commensurable write cost:

- compile cost is printed only as “**≤0.5 ms, 0 tokens**” (line 912) — a
  **degenerate zero write**, `f* = 0`, not a positive break-even;
- capture/storage cost is printed only as “**9.5 GB**”, “**~0.19 GB per active
  day**”, “OCR runs on **96%** of frames” (lines 1202–1207) — **not** in
  dollars-per-task commensurable with `Cmiss`;
- `p` (base success rate, line 237), `Cverify` and `Cwrong` are never published
  numerically.

Therefore no artifact-internal commensurable `w` exists. What *is* reportable
without external inputs is the **critical-h locus**:

```
h*(w) = w / (N_reach · g),   N_reach = 181
```

With `g = 0.6263`: `h* = 0.000147` for `w = 1/60`; `0.0000257` for `w = 1/343`;
`0.00882` for `w = 1`; `0.08821` for `w = 10`.

## 5. Regime table and controls

- Primary regime table: **1,680** cells; sensitivity grid: **17,280** cells.
- Two independent implementations (direct evaluator vs closed form `w/(h·g)`)
  agree at **every** cell, 0 mismatches.
- Conditional `f*` at the published point (`h = 0.077`, `q = 0.82`):
  `0.346` (w = 1/60), `0.0605` (w = 1/343), `20.74` (w = 1), `207.35` (w = 10);
  `f* = 0` at `w = 0`. At `h = 0.090`: `0.296`, `0.0517`, `17.74`, `177.40`.
- Reachability (`f* ≤ 181`): satisfied for `w ∈ {1/60, 1/343, 1}` at `h ≤ 0.077`;
  `w = 10` needs `h ≥ 0.0882` (the published slice tops out at 0.131).

| Control | Purpose | Result |
|---|---|---|
| PC-ALGEBRA | reproduce hand `f* = 2.0` | PASS (relerr 0.0) |
| NC-DIVERGENT | fire `g ≤ 0` and `f* > N_reach` branches | PASS (both fire) |
| PC-READING | derive division rule; select VAR-LIT | PASS |
| PC-EXTRACT | re-extract all frozen anchors | PASS (34/34) |
| NC-CONVENTION | distinguish AMORTIZE-ONCE vs PER-REUSE | PASS (20.74 vs degenerate) |
| B-PUBLISHED-NUMBERS-ONLY | no `f*` in artifact's own text | PASS (0 hits; 1 `amortiz`, 1 `reuse count`) |
| B-FLEET-CEILING | all-fleet ceiling can't invert to `f*` | PASS (`0.07677`, no Cwrite term, no cold arm) |

Absence sweep (`B-PUBLISHED-NUMBERS-ONLY`): 0 hits for `break-even`,
`breakeven`, `break even`, `payback`, `f*`, `stationar`; 1 hit `amortiz`
(line 228), 1 hit `reuse count` (line 237, the Eq. (1) definition of `N`).

## 6. Classification and verdict

**Primary (no artifact-internal commensurable `w`).** All four
(reading × convention) combinations classify **FINITE_NOT_EVALUABLE**: `g > 0`
somewhere, but no artifact-internal commensurable write/cold anchor fixes a
numeric `f*`. Per frozen gate_2 this falsifies the reachability of a reportable
`f*` under the primary adjudication, bounded to this artifact.

**Conditional sensitivity.** If the frozen placeholder `w` sweep is accepted as
a reportable input, all four combinations classify **REACHABLE**. This branch is
recorded for the DIRECTOR, not adopted as the primary result; it rests on values
that are not artifact measurements.

## 7. Interpretation (bounded)

The artifact is a genuine persistent-state economics model, but its own numbers
cannot yield a break-even reuse count: the write cost is either literally zero
(compile) or dimensionally incommensurable (GB/active-day capture), and `p`,
`Cverify`, `Cwrong` are absent. The only artifact-internal lever is the
critical-h locus `h*(w)`.

For `C-PRODUCT-ECON` this is a **scope finding**: the external anchor is
unavailable by construction in this artifact class, which supports the claim
only in the negative and obliges **Product to measure its own first-party
marginal recurrence `h(N)` and first-party `Cwrite`** rather than importing an
`f*` from the literature. The result does not license a follow-up census on this
evidence, because the class is FINITE_NOT_EVALUABLE rather than REACHABLE; a
census would first require a second artifact that *does* publish `w` in
commensurable units.

## 8. Validity threats and non-adoption

- **Scope:** one artifact; not a literature-level negative.
- **Reading ambiguity:** OCR multiply-vs-divide is reported per reading
  (VAR-LIT primary, VAR-MAN secondary); at the divergence cell the readings
  differ by 6.69×, so the choice is material — hence PC-READING.
- **Unpublished `p`:** swept {0.5, 0.8, 1.0}; classification passes through `g`.
- **Modeled quantities:** `R` numerator, three-arm dollars and the all-fleet
  ceiling are labelled “modeled, not billed” (lines 1160–1168); preserved.
- **Non-adoption bar:** no quantity from arXiv:2608.05784v1 enters a SPIDER cost
  model, break-even derivation, product plan or investor-facing material. The
  artifact is the object of analysis, not an input or comparator.
- **Measurement validity:** gate_0 passed every check (evidence hash/size,
  PC-EXTRACT, PC-READING, PC-ALGEBRA, NC-DIVERGENT, NC-CONVENTION, table
  agreement). This is a valid scientific negative, not an infrastructure
  failure.

## 9. What would change the verdict

- A published persistent-state artifact that reports `Cwrite` and `Cmiss` in
  commensurable units (making `w` artifact-internal) → potential REACHABLE.
- A DIRECTOR decision that the frozen placeholder `w` sweep counts as a
  reportable explicitly-swept input → the already-computed conditional
  REACHABLE branch applies.

## 10. Artifacts

- `result.json` — mandatory packet keys.
- `raw/spans.json` — verbatim anchor spans + evidence path/sha256 + PC-READING.
- `raw/regime_table.json` — full 1,680-row primary table.
- `raw/controls_result.json` — all seven controls.
- `raw/classification.json` — per-combination classes and verdict.
- `raw/metrics.json` — required metrics `M-*`.
- `run_determination.py`, `build_result.py` — deterministic producers.
