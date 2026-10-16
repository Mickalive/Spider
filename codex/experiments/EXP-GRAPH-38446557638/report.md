# EXP-GRAPH-38446557638 — EXECUTE report (Graph abstention-boundary retest, runner-repair transaction)

## 1. What was executed

Frozen design from `request.json` / `spec.json` / `prereg.md` / `freeze.json`
(design_contract_version 2), claim `C-SEMANTIC-RESOLVE`, Director question: under the
pre-registered exclusive `unknown_precision` denominator and an honest out-of-sample
retrieval fit (pooled FIT-TRAIN n>=78, disjoint FIT-SELECT, hard mu>0, resubstitution
forbidden), does the AXIS-G2-RETEST shortfall persist or does the branch flip, once the
parent `UnboundLocalError` is repaired.

Procedure exactly per `prereg.md#10`: extracted `FROZEN-RUNNER` to
`raw_evidence/runner_tframe_g3_oos.py` (sha256
`4c412aec6ba21c9d1733ccb1d5e1105ea62bf116395a142ce72ddb9651f9a7b8` =
`CANONICAL-RUNNER-SHA256`), ran two byte-identical `--mechanics-only` canaries
(both exit 0, sha256 `eb45678216c11bbd797fefc454e754324508f3d83b1c043288aed54e53fbaea8`,
matching the DESIGN prediction, empty stderr), then the scored run to
`raw_evidence/run_output.json` (sha256 `2c8adbb7e6d0072b1f919bea44dd285f9a9479f4bf4b178bc303b65541b99966`).
`result.json` is written from `run_output.json` only. No parent numbers inherited.
Runner repair (the sole logic delta vs the parent): the two `select_gids`
comprehensions now bind `for a, r in ...` instead of `for _, r in ...` interpolating
`{a}`. The crash site executes before the mechanics branch, so the clean canaries are a
true liveness proof of the escaped defect.

## 2. RAW EVIDENCE vs OBSERVATION vs MEASUREMENT vs INTERPRETATION

- RAW EVIDENCE: `raw_evidence/runner_tframe_g3_oos.py`, `raw_evidence/run_output.json`,
  `raw_evidence/mechanics_only_1.json`, `raw_evidence/mechanics_only_2.json` (hashes in
  `result.json#artifacts`).
- OBSERVATIONS: `result.json#observations` (directly read off the raw output).
- DERIVED MEASUREMENTS: `result.json#metrics` and `#controls` (gate evaluations, fork,
  decision via the frozen cascade).
- INTERPRETATION (this report, §§3–5): H1 SUPPORTED, honest-retrieval fork
  TFRAME_DOMINATES_G3, decision DECIDE_REQUIRE_RETRIEVAL_B. AUDIT may dispute the
  interpretation but may not rewrite the raw evidence.

## 3. Outcome measurements (exclusive denominator; inclusive sensitivity-only)

Arm A (T-FRAME+) TEST, exclusive gates (`FA<=0.10, cov>=0.50, UP_excl>=0.85`):

| axis | FA | cov | UP_excl | UP_incl | sel | gate |
|---|---|---|---|---|---|---|
| AXIS-G3-NEW | 0.10 (2/20) | 1.00 (36/36) | 1.00 | 1.00 | 1.00 | MET |
| AXIS-G2-RETEST | 0.00 | 0.925 (37/40) | **0.8333 (10/12)** | 0.8696 | 1.00 | FALSE solely on UP |
| AXIS-G1-PRIMARY | 0.0556 | 0.9464 | 1.00 | 0.85 | 0.9057 | MET |
| AXIS-G1-ALTLEX (PC) | 0.0556 | 0.9464 | 1.00 | 0.85 | 1.00 | MET |

`selection_preserved=true`. G2 flip needs 11/12=0.9167 — a one-row margin around the
0.85 bar. The gate vector reproduces the parent exactly at gate level: **H1 SUPPORTED**
(no-refit structural bound persists; branch does not flip).

Arm B-OOS (honest, mu>0): SELECT-feasible (`tau=0.4156, mu=0.0005` active; select gate
FA 0.10 / cov 0.9412 / UP 0.9643, but SELECT `selective_acc=0.0` co-reported per
RQF-05). Frozen gate on TEST: G3 (FA 0.05, cov 0.7778, UP 0.7037, sel 0.25), G2 (FA 0.0,
cov 0.35, UP 0.4348, sel 0.0714), G1/ALTLEX (FA 0.0, cov 0.4286, UP 0.36, sel 0.125) —
all gate-false on UP (and G2/G1/ALTLEX also on coverage). Fork:
**TFRAME_DOMINATES_G3**. Frozen cascade: **DECIDE_REQUIRE_RETRIEVAL_B**.

C7 diagnostic: fires on 0 applicable rows every axis; strictly reduces TEST FA
G3 0.20→0.10 and G2 0.10→0.00 vs `tframe_frozen`. Controls all live: gatefree TEST FA
0.2778–0.50 vs Arm A 0.0–0.10; random-gate FA 0.60–0.7778; shuffled 0.0–0.0556,
random-role 0.0189–0.1081; abstain-all coverage 0.0 / FA null / UP_excl 0.0862–0.2041;
incumbent FA 0.1667–0.20, sel 0.9057–1.0. Fit-pool bars hold (102/34/60, both
disjointness checks true). No invalidity trigger fired.

## 4. Interpretation and product consequence

Per the frozen cascade (`prereg.md#7`), REQUIRE + TFRAME_DOMINATES_G3 strengthens the
no-refit structural bound but **VACATES the retrieval-B requirement as specified**:
honest retrieval with a mu>0 out-of-sample gate is feasible on SELECT yet collapses on
every axis TEST (selective_acc 0.0 on SELECT, ≤0.25 on tests), so Product may no longer
cite retrieval viability as the reason for the conservative boundary. The boundary /
architecture question returns to the Director with HYPOTHESIS retained and a narrowed
ceiling. This packet promotes nothing itself. Overall experiment `outcome=MIXED`
(`status=COMPLETE`): H1 supported (bound persists) combined with a negative honest-retrieval
viability leg — a valid scientific negative on the retrieval leg, not an
infrastructure failure.

## 5. Caveats (binding on AUDIT/DIRECTOR)

Pooled-retrieval dilution biases against retrieval (pre-registered): the collapse
vacates the requirement *as specified* without falsifying retrieval in general.
Gating on inclusive UP is pre-declared invalid (on these rows inclusive would read
G2 0.8696≥0.85 and manufacture a flip without new evidence). The T-FRAME+ leg is a
disclosed validity-transaction reproduction, not new evidence for Arm A; new evidence
is the denominator fixing plus the honest-retrieval leg. Screen drops (G3 5, G1 9/axis)
are recorded, not counted.
