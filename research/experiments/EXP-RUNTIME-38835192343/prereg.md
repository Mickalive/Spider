# EXP-RUNTIME-38835192343 preregistration — larger-N L2 resolution (runtime, design-contract v2)

Director mandate (binding): Global Research Director CONTINUE on C-DELTA-REPAIR —
at larger N sufficient to resolve the +/-6% L2 CIs on P1-ENDPOINT and P3-PERMISSION
(or on a higher-resolution timing substrate preserving the BulkArm single-replace
treatment and dual inclusive/NOARG boundaries), do the four L2 MARGINAL cells
resolve to robust reuse WINs completing the 12-cell re-admission bar, or does any
cell show a robust LOSS triggering the bounded permanent drop? Baselines (cold
re-derivation, inclusive/NOARG timing boundaries, BulkArm single-replace treatment)
are frozen from the parent, so this is a pure power increase, not a redesign. Stop
trigger: this N is the last budgeted resolution attempt; a second consecutive
straddle PARKs the thread rather than funding a third. The inherited parent handoff
(EXP-RUNTIME-38816779349) is continuity evidence only; its `next_question` matches
the mandate question and is therefore adopted, but no threshold, ratio, or wording
from the parent packet is inherited as evidence, and nothing in the handoff
overrides the Director's CONTINUE allocation, stop trigger, or claim binding.

Parent handoff carry-forward (preserved distinctions; evidence refs in
`research/experiments/EXP-RUNTIME-38816779349/handoff.json`):
established — reuse-based signal-driven localized repair is functionally and
locally sound on this substrate/carrier for the third time (36/36 valid trials,
repair_success 1.0 with Wilson lower 0.7575>=0.60, guard_fire 1.0, write_set_max 1,
contamination 0/144 with the correct 48/class denominator, literal-replay 0.0,
cold 1.0, drift/equivalence pins exact); the registry-materialization tax was
removed BY MEASUREMENT (BulkArm reuse build medians ~0.29ms vs parent ~1.49ms,
content-pinned identical); priced at the audited ceiling: 8 robust WIN cells and 4
near-1.00 MARGINAL cells (P1/P3 L2 on both boundaries), 0 LOSS, aggregate
INCONCLUSIVE. rejected — (none; the parent rejected nothing). unknown — whether
the four P1/P3 L2 MARGINAL cells resolve to WIN, LOSS, or remain straddles at
larger N (the sole blocker for re-admission-vs-drop); why P2 wins at both L while
P1/P3 win only at L3 (post-hoc candidate only); any transfer beyond this
substrate/carrier/classes/counters; real model-call/token economics (B3
UNSATISFIABLE here). do_not_assume — the 8 WIN cells do not imply 12-cell
SUPPORTS; the shipped 17-vs-18/19 counter is a zero-variance drift-checked premise,
never an empirical win; absolute gaps are sub-millisecond (L2 0.02-0.09ms),
smaller than one local GET and 2-3 orders below real web navigation economics;
latency is wall-clock, not deterministic; breadth/recurrence episodes are ungated
diagnostics; no cross-lane claim status is mutated.

## 1. Background and decision context

The parent packet (EXP-RUNTIME-38816779349, audit PASS, verdict
INCONCLUSIVE-MARGINAL-STRADDLE-NO-READMIT-NO-PERMANENT-DROP-RETAIN-C-DELTA-REPAIR-EXPERIMENTAL-NO-PROMOTION)
removed the known removable tax BY MEASUREMENT and moved the priced picture from
six robust deficits to 8 robust WIN cells (every L3/L3-NOARG cell on all classes
plus all four P2-STRUCTURE cells, Bonferroni CIBF uppers 0.85-0.97) with 4
near-1.00 MARGINAL cells (P1 L2 1.0158 CIBF [0.9345,1.0707] / NOARG 0.9950
[0.9203,1.0535]; P3 L2 1.0039 [0.9509,1.0628] / NOARG 0.9858 [0.9369,1.0425]).
Parent audit AF-5 (paired-bootstrap diagnostic) and AF-6 (order-parity split)
confirm the straddle is real at n=12, not a resampling or ordering artifact;
AF-7 states the environment could express the effect at L3 but not at L2 at n=12
(L2 median gaps 0.02-0.09ms vs ~0.06-0.07ms bootstrap half-width) and the frozen
rule correctly parks instead of deciding. This experiment varies ONLY the
resolution confound: TRIALS_PER_CLASS 12 -> 36 (3x, fresh SEED6 bank), which
narrows family-wise half-widths by sqrt(12/36) ~= 0.577 (projected ~3.2-4.1%,
§15), sufficient to convert any true |R-1| effect above ~4% into a robust WIN or
LOSS. Non-degeneracy note (inherited lesson): shipped-counter-only deciding is
structurally reuse-positive (deterministic 17/18, 17/19 by arm protocol) and
scaffold-unit deciding is structurally reuse-negative under an arbitrary 1:1
weight choice, so the shipped premise PLUS the dual-boundary CI-gated latency
decider remains the unique non-degenerate structure. Substrate-resolution
alternative (mandate-authorized option): rejected in favor of larger N because a
new timing substrate would break cross-packet comparability (V-DRIFT-COLD
nominals, phase medians, audit AF-8 tax accounting) and introduce fresh validity
threats, while N increase preserves every pin and the audit chain intact.

## 2. Claim, hypothesis, falsifier

Claim: C-DELTA-REPAIR (status EXPERIMENTAL; runtime co-owns it in the lane registry).
H1 (functional/locality, re-attested): per class, repair_success >= 0.80 AND
Wilson lower >= 0.60 AND contamination <= 0.10 (144 in-support unaffected probes
per class, 432 total) AND write_set_max <= 1 AND guard_fire >= 0.80.
H2 (shipped counter, deterministic drift-checked premise): reuse ships exactly 17
units vs cold 18 (L=2) / 19 (L=3) by arm protocol on functional_ok trials; checked as
V-DRIFT-COLD + V-DRIFT-REUSE + reported V-EQ-HOLDS; zero empirical variance by
construction; never claimed as an empirical win.
H3 (latency, empirical decider): on all 12 cells (3 classes x L=2/L=3 x
inclusive/NOARG), median reuse/cold ratio < 1.00 with the Bonferroni family-wise
bootstrap CI (1-0.05/12, B=10000) strictly below 1.00.
H4 (recurrence, descriptive only): per-trial learning cost t_learn_s
(make_mech_dicts, untimed, outside the episode window in both arms) is timed as a
diagnostic; N* = learn_med/(cold_med - reuse_med) per class/L/boundary, null when
the denominator is <= 0 (never amortizes). Breadth scaling is NOT re-measured:
the parent ungated breadth diagnostics (n=1,2,5) stand as recorded; re-running
them would add ~40% wall-clock without moving the gated decision.
H5 (B3): model_calls/model_tokens structural zeros; real model economics UNSATISFIABLE
here (mandate-authorized counters-only pricing, blocker recorded).
H6 (treatment identity): bulk registry content == upsert content exactly (V-REG-EQUIV
every timed episode).
Falsifier: any robust LOSS cell (R >= 1.00 with BFCI_lower >= 1.00, valid gates) ->
PERMANENT-DROP-BOUNDED. Broken H1 -> FALSIFIES-FUNCTIONAL (bounded, no drop).
Any MARGINAL-without-LOSS, any UNKNOWN, or any tripped validity gate ->
INCONCLUSIVE / MEASUREMENT_INVALID (never a negative, never a drop, never re-admit;
a second consecutive straddle PARKs the thread per the mandate stop trigger).
H4 diagnostics and the attribution tie set can never flip the gated decision.

## 3. Measurement prerequisites (all verified at DESIGN, §15)

Python 3.12.15 stdlib-only. Carrier byte-identical to the parent freeze
(kernel.py 3a6caf97, models.py 338aaf4d, registry.py 51fb440d, __init__.py 3d173722).
Parent v2 module pinned (60855 bytes, d4871091; all 30 v2 attributes used by the
v6 driver verified present by name check). Fresh seeds SEED6=180486679
(38835192343 % 2**32; disjoint from SEED5=162073685 and SEED4=3980394806) with
disjoint offsets (scored +1000*(ci+1)+j; NC +1/+2; bootstrap +7000*(ci+1)+k;
DESIGN canaries on discarded offsets). DESIGN liveness: server/distill (5 mechs)/
resolve-EXECUTABLE/fetch-200/verify-True/guard-silent/registry-RW booleans
(unperturbed, discarded), BulkArm-vs-upsert byte-equality canary (discrete content
compare, untimed, identical bytes), timer granularity ~61ns nonzero minimum (4-5
orders below the 0.02-1.0ms gaps). No timed reuse-vs-cold comparison is run at
DESIGN. Warmup non-interference by inspection (read-only GET server, no POST
handler, set_perturb never called by trial arms, pure guard) enforced per trial by
V-RETAIN. N=36 parity 18/18 even; Bonferroni tail indices integral at B=10000
(lo 20, hi 9978). No external bank, dataset, fixture, model endpoint, browser, or
network required.

## 4. Treatment, comparator, recurrence

Substrate: parent-identical in-process localhost ThreadingHTTPServer JSON API with
5 resources (users/posts/comments/albums/photos), 3 LOCAL perturbation classes
(P1-ENDPOINT/P2-STRUCTURE/P3-PERMISSION), rotating targets
(TARGETS[(ci+j)%3], each target exactly 12x per class at N=36),
TRIALS_PER_CLASS=36, LEARN_IDS=[11,12,13], LEARN_IDS_MIN=[11,12],
TASK_IDS=[14,15,16,17,18], in-support probe id 14. Shipped parameterized carrier
held fixed (no kernel/registry change). Comparator B-COLD/B-COLD-MIN:
parent-identical v2.Arm path (0 upserts at build, 1 upsert after distill), timed in
parity order (18 reuse-first/18 cold-first per class). Treatment
T-REPAIR-REUSE-BULK: identical episode semantics to the parent v5 bulk episode
(fused freshness probe, one repair_attempts, one post-repair verify, execute
TASK_IDS[1:]) with S-REGISTRY-BUILD constructing BulkArm — ONE
MechanismRegistry.replace() of the inherited set instead of N sequential
upsert() read+rewrite cycles. Gated breadth n=5 (full set) only. Recurrence:
per-trial learning cost t_learn_s (make_mech_dicts, untimed, outside the episode
window in both arms) is timed as a diagnostic; N* per class/L/boundary, null when
the denominator is <= 0. Sequence-equivalence map (timed reuse): S-ARG deepcopy
-> S-REGISTRY-BUILD BulkArm(5) -> S-REGISTRY-SCAN target_mech -> S-PROBE
resolve+fetch -> S-GUARD -> S-REPAIR-SIGNAL local_repair -> S-REGISTRY-WRITE
upsert(patched, the single repaired target) -> S-CHARGE -> S-POST-VERIFY ->
S-EXECUTE batch. Charging semantics live entirely in pinned v2/carrier code the
driver calls but never reimplements. Why N=36: parent half-widths 5.6-7.1% x
sqrt(12/36) project to 3.2-4.1% (§15) — the smallest integer multiple of 12 that
preserves exact target-rotation balance (each target 12x) while projecting
resolution of any true effect above ~4%; N=24 would project only to ~4.0-5.0%
(likely still straddling), N=48 buys only marginal extra narrowing (50% vs 42%)
for 33% more wall-clock. True effects below ~3-4% remain straddles by
construction and PARK the thread per the stop trigger — a bounded, honest
non-resolution, not a third funding request.

## 5. Metrics (stable identities for downstream transmission)

Per class (n=36): M-REPAIR-SUCCESS, M-REPAIR-SUCCESS-WILSON-LOWER, M-CONTAMINATION-RATE
(denominator 144; 432 total), M-WRITE-SET-MAX, M-GUARD-FIRE-RATE, M-COLD-SUCCESS,
M-LITERAL-SUCCESS, M-NOREPAIR-SUCCESS (diagnostic; vacuity disclosed), M-BASE-LIVENESS,
M-OVERBROAD-CONTAMINATION-N, M-SHIPPED-REUSE/COLD-L2/COLD-L3 (+RATIOs, +HTTP splits),
M-COST-FETCH-RATIO-L3, M-EQUIV-MATCH-N/M-EQUIV-MATCH-DEN (raw identifiers; no
synthetic key), M-SCAFFOLD-REUSE/COLD-L3 (+M-SP5-RATIO-L2/L3 informational, excluded
from the classifier), M-LATENCY-{REUSE,COLD-L2,COLD-L3}-MED-S, M-LATENCY-R-L2/L3 with
M-LATENCY-R-L2/L3-CI95 (diagnostic, B=2000) and M-LATENCY-R-L2/L3-CIBF (gated,
Bonferroni 1-0.05/12, B=10000), M-LATENCY-R-L2/L3-NOARG with matching NOARG CIs,
M-LATENCY-SIGN-REUSE-SLOWER-L3, M-PHASE-DELTAS, M-CLOSURE-REUSE/COLD-MED,
M-MODEL-CALLS/TOKENS (structural zeros), M-N (=36), M-CELL-L2/L2NA/L3/L3NA
(WIN/LOSS/MARGINAL/UNKNOWN), M-T-LEARN-MED-S, M-RECURRENCE-N-STAR-{L2,L2NA,L3,L3NA}
(diagnostic, null if never), M-SHIPPED sums (nominal 612/648/684 reuse/cold-L2/cold-L3
per class), V-DRIFT-COLD-HOLDS, V-DRIFT-REUSE-HOLDS, V-EQ-HOLDS. Totals:
M-MODEL-CALLS-TOTAL/M-MODEL-TOKENS-TOTAL (=0), M-N-VALID-TRIALS (=108).
M-BREADTH-* identities are RETIRED in v6 (no breadth episodes run; parent values
stand as recorded ungated diagnostics). Attribution (diagnostic, tie set):
excess_med_s, phase_deltas_med_s, shares_of_excess, votes_ge_half, closure_ok,
attribution_set (ALL phases clearing >= 0.50 on >= 2/3 classes), answer (single
ATTRIBUTED-X, TIE-A+B, UNATTRIBUTED, ATTRIBUTION-MOOT, ATTRIBUTION-INVALID).
Net-vs-gross semantics preregistered: the denominator is the NET median episode gap
(reuse minus cold, net of cold-side savings such as S-DISCOVERY/S-OBSERVE/S-DISTILL);
shares may therefore exceed 1.0 and are non-decomposable; gross reuse-phase medians
are reported alongside; the single value is never determined by driver iteration
order.

## 6. Controls

PC-BASE-LIVENESS (scored in every trial; DESIGN basis in spec). B-LITERAL-REPLAY
(live must-fail; V4). B-NO-REPAIR (abstention; gate vacuous by pinned-v2
construction — success hardcoded False — disclosed; only the 108/108 guard-fired
diagnostic is informative; live must-fail role held by B-LITERAL-REPLAY).
NC-NO-PERTURBATION + NC-NOISE (must-silent) + 108 per-trial fresh-silence
probes (pooled specificity) + NC-OVERBROAD-REPAIR (must-fire > 0.10; parent 4/4;
re-fired at DESIGN). V-CLOSURE (attribution-only). V-REG-EQUIV (content pin, every
timed episode; DESIGN byte-equality canary). V-DRIFT-COLD (repair-independent
cold nominals 648/684 + http 288/324 at N=36). V-DRIFT-REUSE (successful-repaired
reuse trials ship exactly 17 with class http 6/5/6; genuine repair failures exempt).
V-RETAIN (post-warmup retention re-check per trial). V-TIMING (2 warmups, 18/18
parity, finite positive latencies, dual boundaries). V-EQUIV (warmup
original-function vs bulk-timed discrete projections, recorded for audit). No
control is given the treatment answer; ground truth (perturbed=stale by runner
construction; fresh=silent by pre-perturbation read) is independent of the guard
verdict. Failure policy INVALID-not-negative throughout.

## 7. Validity threats and representation loss

Localhost ThreadingHTTPServer vantage only: the parent L2 excess (0.02-0.09ms
median gaps) was sub-one-local-GET and 2-3 orders below real navigation economics
— no transfer of ratios to real web/browser/production/external-agent economics is
licensed. Simplified JSON API, not real websites. h(N)=1 in the timed window with
learning cost outside it in both arms; recurrence is a derived N*, not a measured
amortization. B3 model economics structurally zero (blocker recorded, not a result).
Multiplicity is handled by Bonferroni family-wise CIs for gating (12 cells); 95%
CIs are reported uncorrected as diagnostics. Bootstrap tail Monte Carlo noise at
B_BONF=10000 (~21 samples per 0.0021 tail) is frozen by pinned bootstrap seeds,
hence deterministic for this packet; audit may recompute. At N=36 the tail masses
the same 21 samples/side over a tighter sampling distribution — the projection in
§4/§15, not a guarantee; if dispersion does not shrink as 1/sqrt(N) (e.g.
bimodal latency), straddles persist and PARK. S-ARG operand asymmetry
(reuse deepcopies the full dict, cold {}) is disclosed and neutralized by requiring
wins on BOTH boundaries. Order effects across the 3 timed episodes are controlled
by gated-triple parity (18/18); residual order influence is second-order on a
read-only server and inspectable via order-split medians in the raw trials (audit
may repeat the parent AF-6 diagnostic; it cannot flip the frozen decision).

## 8. Decision rule (frozen; pure functions cost_verdict_v6 / aggregate_v6)

Per class c, TRIALS_PER_CLASS=36 valid trials. functional_ok per §2 bars. For each of
12 cells (class x L x boundary): R and BFCI per §5. Cell: UNKNOWN if R/BFCI missing;
WIN if R < 1.00 AND BFCI_upper < 1.00; LOSS if R >= 1.00 AND BFCI_lower >= 1.00; else
MARGINAL. Class (first match): FUNCTIONAL-FAIL if !functional_ok; COST-UNKNOWN if
any UNKNOWN; PRICED-DEFICIT if any LOSS; PRICED-WIN if all WIN; else PRICED-MARGINAL.
Aggregate (first match): FALSIFIES-FUNCTIONAL if any FUNCTIONAL-FAIL; INCONCLUSIVE
if any COST-UNKNOWN; PERMANENT-DROP-BOUNDED if any PRICED-DEFICIT; SUPPORTS if all
PRICED-WIN; else INCONCLUSIVE (marginal straddle: second consecutive straddle, so
PARK per the mandate stop trigger). Any tripped validity gate ->
MEASUREMENT_INVALID (status; outcome INCONCLUSIVE). 1.00 is never a win. DROP
requires a ROBUST deficit (CIs gate both directions, so a single near-1.00 point
estimate can never convert to a permanent drop; straddles park). Outcome mapping:
SUPPORTS->SUPPORTS; PERMANENT-DROP-BOUNDED->FALSIFIES;
FALSIFIES-FUNCTIONAL->FALSIFIES; INCONCLUSIVE->INCONCLUSIVE;
MEASUREMENT_INVALID->INCONCLUSIVE(status INVALID). Product mapping:
SUPPORTS->re-admit completing the 12-cell bar (spec §product_consequence_positive);
PERMANENT-DROP-BOUNDED->permanent-bounded-drop-no-further-L-sweeps-or-N-increases;
else no-decision-no-drop-no-readmit-park.

## 9. Design notes (deviations from the parent, all deliberate)

(a) Resolution-only change: N 12 -> 36 per class with a fresh SEED6 bank
(independent measurement, not a re-run of the same seeds); substrate, carrier,
perturbation bank, BulkArm treatment, comparators, dual boundaries, Bonferroni
gating, drift/equivalence pins, and bars all frozen from the parent. Previously-WIN
cells are re-measured at common N, never carried forward, so regressions are
detectable and the family keeps one N and one family-wise error rate.
(b) Dropped the n=1/n=2 breadth diagnostic episodes (parent mandate scaling
questions already answered ungated there; smallest decisive batch per mandate).
Recurrence N* retained as a derived diagnostic from the gated triple plus t_learn.
(c) Contamination denominator 144/class, 432 total (4x36); cold nominals scaled to
648/684 sums and 288/324 http; shipped reuse nominal 612/class; parity 18/18.
(d) Rejected the mandate-authorized higher-resolution-substrate option (§1 reason:
comparability + audit-chain preservation).
(e) Gate-coverage probe rescaled to N=36 with minimal crossing counts
(literal/norepair 4/36, cold 32/36, guard 28/36, contam 15/144).
(f) Stop trigger encoded: second consecutive straddle PARKs, funds no third attempt.

## 10. Freeze binding and driver extraction

Freeze artifacts (5 file paths; hashed into freeze.json.artifact_hashes):
src/spider/__init__.py, src/spider/kernel.py, src/spider/models.py,
src/spider/registry.py,
research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py.
The v6 driver has no file identity until EXECUTE extracts it; it is bound stronger by
content: embedded verbatim in section-12 between the marker lines
`# === V6-DRIVER-BEGIN ===` and `# === V6-DRIVER-END ===`, pinned by
CANONICAL-RUNNER-V6-SHA256 = "fe053ea64f74c3eb00e42d849a15a1225881d7f03d963fb6c616b8d0a924c245" (sha256 over the
canonical bytes defined below). Extraction algorithm (frozen; also implemented
as the driver's V1 runtime check): split this prereg.md into lines; find the
first line that EXACTLY equals the BEGIN marker line and the first subsequent
line that EXACTLY equals the END marker line; the driver is the lines strictly
between them joined with "\n" (no trailing newline added). Canonical bytes for
hashing: the extracted driver text with the single self-referential assignment
line starting `CANONICAL_RUNNER_V6_SHA256 = "` replaced by the fixed placeholder
line `CANONICAL_RUNNER_V6_SHA256 = "<PINNED>"` (this closes the fixed point: the
constant's value cannot affect its own digest). Line-exact matching is
load-bearing: prose and code references to the markers always sit inside longer
lines and therefore never collide with the standalone marker lines. The V1 check
recomputes sha256 over the canonical bytes and refuses to run on mismatch; the
V0 check refuses when the parent v2 module differs in bytes or sha. EXECUTE runs
the extracted driver only. The python fence around section-12 is presentational.

## 11. Product consequences

SUPPORTS: complete the 12-cell bar and re-admit localized repair to the
C-PRODUCT-ECON story with honest denominators (shipped unit counter +
dual-boundary family-wise latency at N=36 + recurrence scaling + tie-set
attribution); no code promotion (runtime lane; carrier byte-identical); B3 blocker
recorded. PERMANENT-DROP-BOUNDED: permanent bounded drop from the C-PRODUCT-ECON
story on this substrate/carrier/classes/counter, no further L-sweeps, no further N
increases, thread stopped (mandate stop trigger — licensed here because the known
removable tax was removed by measurement in the parent and a robust larger-N
deficit is therefore structural at resolvable resolution). FALSIFIES-FUNCTIONAL:
bounded mechanism concern, no re-admit, no drop. INCONCLUSIVE /
MEASUREMENT_INVALID: PARK per the stop trigger; no re-admit, no drop, no
promotion; narrowed CIs stay on file. C-DELTA-REPAIR stays EXPERIMENTAL bounded to
functional/locality soundness in every branch except FALSIFIES-FUNCTIONAL.

## 12. Frozen driver (v6; executable; content-bound by §10)

```python
# === V6-DRIVER-BEGIN ===
#!/usr/bin/env python3
# FROZEN RUNNER v6 for EXP-RUNTIME-38835192343 (runtime, design_contract_version 2).
# C-DELTA-REPAIR larger-N resolution: bulk-materialized localized repair vs cold
# re-derivation at L=2/L=3 on both timed boundaries at TRIALS_PER_CLASS=36.
# Gated triple only (no breadth episodes); recurrence N* derived from gated medians.
# Reuses the IMMUTABLE parent v2 module by pin-checked import ONLY. Stdlib only.
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import random
import sys
import time
from pathlib import Path

EXP_ID6 = "EXP-RUNTIME-38835192343"
SEED6 = 180486679  # 38835192343 % 2**32 (fresh; disjoint from SEED5=162073685 and SEED4=3980394806)
V2_PIN_SHA = "d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608"
V2_PIN_BYTES = 60855
B_LAT = 2000
B_BONF = 10000
N_CELLS = 12
ALPHA_FAMILY = 0.05
# v6: breadth diagnostic episodes removed (smallest decisive batch; see prereg section-4).
# Recurrence N* remains derived from the gated triple plus t_learn (diagnostic).
CLOSURE_BAR = 0.20
ATTRIB_SHARE = 0.50
FETCH_BAR = 0.90
NOMINAL = {"reuse_sum": 17, "cold_l2_sum": 18, "cold_l3_sum": 19,
           "cold_l2_http": 8, "cold_l3_http": 9}
REUSE_HTTP_EXPECTED = {"P1-ENDPOINT": 6, "P2-STRUCTURE": 5, "P3-PERMISSION": 6}
CANONICAL_RUNNER_V6_SHA256 = "fe053ea64f74c3eb00e42d849a15a1225881d7f03d963fb6c616b8d0a924c245"


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here.parent, *here.parents):
        if (p / "src" / "spider" / "kernel.py").is_file():
            return p
    return Path("/home/runner/work/Spider/Spider")


REPO = _repo_root()
V2_PATH = REPO / "research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py"
PREREG_PATH = REPO / "research/experiments/EXP-RUNTIME-38835192343/prereg.md"


def _load_v2():
    raw = V2_PATH.read_bytes()
    if len(raw) != V2_PIN_BYTES or hashlib.sha256(raw).hexdigest() != V2_PIN_SHA:
        raise SystemExit("V0-SUBSTRATE-PIN failure: parent v2 runner mismatch; refusing to run.")
    spec = importlib.util.spec_from_file_location("v2frozen", str(V2_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _extract_driver(text):
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l == "# === V6-DRIVER-BEGIN ===")
    end = next(i for i, l in enumerate(lines[start + 1:], start + 1)
               if l == "# === V6-DRIVER-END ===")
    return "\n".join(lines[start + 1:end])


def _canonical_bytes(driver):
    """Normalize the single self-referential hash constant before hashing.

    The CANONICAL_RUNNER_V6_SHA256 assignment line is part of the embedded text,
    so hashing raw bytes would be circular. Both DESIGN finalization and the V1
    runtime check hash the text with that one line replaced by a fixed
    placeholder; the constant's value therefore cannot affect the digest, and a
    single assignment closes the fixed point.
    """
    out = []
    for line in driver.split("\n"):
        if line.startswith('CANONICAL_RUNNER_V6_SHA256 = "'):
            out.append('CANONICAL_RUNNER_V6_SHA256 = "<PINNED>"')
        else:
            out.append(line)
    return "\n".join(out).encode("utf-8")


def _check_v1_binding():
    driver = _extract_driver(PREREG_PATH.read_text(encoding="utf-8"))
    digest = hashlib.sha256(_canonical_bytes(driver)).hexdigest()
    if digest != CANONICAL_RUNNER_V6_SHA256:
        raise SystemExit("V1-FREEZE-BINDING failure: embedded driver hash mismatch; refusing to run.")
    return digest


v2 = _load_v2()

CLASSES = v2.CLASSES
TARGETS = v2.TARGETS
TRIALS_PER_CLASS = 36  # frozen larger-N resolution: 3x parent n=12; NOT v2.TRIALS_PER_CLASS
PHASE_KEYS = ["S-ARG", "S-REGISTRY-BUILD", "S-REGISTRY-SCAN", "S-PROBE", "S-GUARD",
              "S-REPAIR-SIGNAL", "S-REGISTRY-WRITE", "S-CHARGE", "S-POST-VERIFY",
              "S-EXECUTE", "S-DISCOVERY", "S-OBSERVE", "S-DISTILL"]
REGISTRY_PHASES = ["S-REGISTRY-BUILD", "S-REGISTRY-SCAN", "S-REGISTRY-WRITE"]
GUARD_PHASES = ["S-PROBE", "S-GUARD"]
COLD_FETCH_PHASES = ["S-DISCOVERY", "S-OBSERVE"]


class BulkArm(v2.Arm):
    """Reuse arm with single-bulk registry materialization (the mandate repair).

    Registry content is semantically identical to N sequential upsert() calls
    (byte-identical file content, verified by the DESIGN canary): one
    MechanismRegistry.replace() of the full subset instead of one upsert() per
    mechanism, where each upsert() is a full JSONL read+rewrite (the 39.2x tax
    at n=5). Uses only the frozen shipped replace() API; no carrier change.
    Cold arms keep the parent v2.Arm path byte-identical to the parent packet.
    """

    def __init__(self, mech_subset, reg_dir: Path, tag: str):
        v2.Arm._seq += 1
        self.path = v2._RUN_DIR / f"reg-{tag}-{v2.Arm._seq:06d}.jsonl"
        self.registry = v2.MechanismRegistry(self.path)
        self.registry.replace(sorted((v2.Mechanism(**m) for m in mech_subset.values()),
                                     key=lambda m: m.mechanism_id))
        self.kernel = v2.SpiderKernel(self.registry, min_confidence=v2.MIN_CONFIDENCE,
                                      counters=v2.TrajectoryCounters())
        self.counters = v2.Counters()
        self.oplog = []


def _breadth_subset(mechs, resource, breadth):
    """Deterministic inheritance-breadth subset: target + first (breadth-1) others."""
    others = sorted(r for r in mechs if r != resource)
    keep = [resource] + others[:max(0, breadth - 1)]
    return {r: mechs[r] for r in keep if r in mechs}


class ScafLog:
    """Phase timers + preregistered integer scaffold units for one episode."""

    def __init__(self):
        self.t = {}
        self.scaf = 0

    def timed(self, key, fn, *a, **k):
        t0 = time.perf_counter()
        out = fn(*a, **k)
        self.t[key] = self.t.get(key, 0.0) + (time.perf_counter() - t0)
        return out

    def add_scaf(self, n=1):
        self.scaf += n


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return None
    m = n // 2
    return float(xs[m]) if n % 2 else (xs[m - 1] + xs[m]) / 2.0


def _median_ratio_ci(rs, cs, seed, B):
    rng = random.Random(seed)
    n = len(rs)
    out = []
    for _ in range(B):
        r = _median([rs[rng.randrange(n)] for _ in range(n)])
        c = _median([cs[rng.randrange(n)] for _ in range(n)])
        out.append(r / c)
    out.sort()
    return out[int(0.025 * B)], out[int(0.975 * B) - 1]


def _median_ratio_ci_bf(rs, cs, seed, B):
    tail = (ALPHA_FAMILY / N_CELLS) / 2.0
    rng = random.Random(seed)
    n = len(rs)
    out = []
    for _ in range(B):
        r = _median([rs[rng.randrange(n)] for _ in range(n)])
        c = _median([cs[rng.randrange(n)] for _ in range(n)])
        out.append(r / c)
    out.sort()
    return out[int(tail * B)], out[int((1.0 - tail) * B) - 1]


def _arm_counters(arm):
    return arm.counters.as_dict()
def run_reuse_episode_bulk(app, origin, mechs, cached, resource, breadth, tag):
    """Instrumented treatment episode with the registry tax removed.

    Mirrors v2.run_repair_reuse semantics exactly except S-REGISTRY-BUILD uses
    BulkArm (single replace) over the breadth subset instead of v2.Arm (one
    upsert per mechanism). All charging/verify/execute calls are unchanged.
    """
    log = ScafLog()
    t0 = time.perf_counter()
    md = log.timed("S-ARG", copy.deepcopy, mechs)
    log.add_scaf(1)
    sub = _breadth_subset(md, resource, breadth)
    arm = log.timed("S-REGISTRY-BUILD", BulkArm, sub, Path("/tmp"), tag)
    log.add_scaf(len(sub))
    reg_equiv = ({m.mechanism_id: m.as_dict() for m in arm.registry.all()}
                 == {m["mechanism_id"]: m for m in sub.values()})
    mech = log.timed("S-REGISTRY-SCAN", arm.target_mech, resource)
    log.add_scaf(1)
    if mech is None:
        return {"ok": False, "reason": "not-executable", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf, "reg_equiv": reg_equiv,
                "episode_s": time.perf_counter() - t0}
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(v2.flatten(mech.postconditions))
    r0 = log.timed("S-PROBE", arm.resolve, intent, context, {slot: str(v2.TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"ok": False, "reason": "not-executable", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf, "reg_equiv": reg_equiv,
                "episode_s": time.perf_counter() - t0}
    failed = log.timed("S-PROBE", arm.netfetch, r0.bound_action["url"],
                       r0.bound_action.get("headers", {}), origin=origin)
    stale, ginfo = log.timed("S-GUARD", v2.guard, cached, required_paths, failed,
                             arm, mech, {slot: str(v2.TASK_IDS[0])})
    log.add_scaf(1)
    if not stale:
        ok, _ = log.timed("S-EXECUTE", v2.execute_batch, arm, intent, context,
                          slot, v2.TASK_IDS[1:])
        ep = time.perf_counter() - t0
        return {"ok": bool(ok), "reason": "fresh", "arm": arm, "guard_fired": False,
                "guard_info": ginfo, "phases": dict(log.t), "scaffold": log.scaf,
                "reg_equiv": reg_equiv,
                "episode_s": ep, "misc_s": ep - sum(log.t.values())}
    patched, probe_body, probe_header = log.timed(
        "S-REPAIR-SIGNAL", v2.local_repair, arm, mech, resource, slot,
        v2.TASK_IDS[0], failed, origin)
    log.add_scaf(1)
    if patched is None:
        ep = time.perf_counter() - t0
        return {"ok": False, "reason": "repair-failed", "arm": arm, "guard_fired": True,
                "guard_info": ginfo, "phases": dict(log.t), "scaffold": log.scaf,
                "reg_equiv": reg_equiv,
                "episode_s": ep, "misc_s": ep - sum(log.t.values())}
    log.timed("S-REGISTRY-WRITE", arm.registry.upsert, patched)
    log.add_scaf(1)
    log.timed("S-CHARGE", arm.charge_repair_attempt)
    first_ok = False
    if probe_body is not None:
        first_ok = bool(log.timed("S-POST-VERIFY", arm.verify, patched.mechanism_id,
                                  probe_body, {slot: str(v2.TASK_IDS[0])}))
    ok, _ = log.timed("S-EXECUTE", v2.execute_batch, arm, intent, context,
                      slot, v2.TASK_IDS[1:])
    ep = time.perf_counter() - t0
    return {"ok": bool(first_ok and ok), "reason": "repaired", "arm": arm,
            "guard_fired": True, "guard_info": ginfo, "phases": dict(log.t),
            "scaffold": log.scaf, "reg_equiv": reg_equiv, "episode_s": ep,
            "misc_s": ep - sum(log.t.values())}


def run_cold_episode(app, origin, resource, ids, tag):
    """Instrumented cold episode. Mirrors v2.run_cold semantics exactly (parent-identical)."""
    ids = list(ids)
    log = ScafLog()
    t0 = time.perf_counter()
    log.timed("S-ARG", copy.deepcopy, {})
    log.add_scaf(1)
    arm = log.timed("S-REGISTRY-BUILD", v2.Arm, {}, Path("/tmp"), tag)
    base = f"{origin}/api/{resource}"
    extra_header = {}
    probe = log.timed("S-DISCOVERY", arm.netfetch, f"{base}/{ids[0]}", {},
                      origin=origin)
    if probe.status in (301, 302, 303, 307, 308) and probe.headers.get("Location"):
        loc = probe.headers["Location"]
        base = origin + "/".join(loc.split("/")[:-1])
    elif probe.status == 403:
        for k, vv in probe.headers.items():
            if k.lower().startswith("x-required-"):
                extra_header["X-" + k[len("x-required-"):]] = vv
    elif probe.status != 200:
        ep = time.perf_counter() - t0
        return {"ok": False, "reason": "discovery-failed", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
                "misc_s": ep - sum(log.t.values())}
    obs = []
    for rid in ids:
        res = log.timed("S-OBSERVE", arm.netfetch, f"{base}/{rid}", extra_header)
        if res.status != 200 or res.body is None:
            ep = time.perf_counter() - t0
            return {"ok": False, "reason": "observation-failed", "arm": arm,
                    "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
                    "misc_s": ep - sum(log.t.values())}
        obs.append(v2.Observation(intent=f"read_{resource}",
                                  state={"resource_type": resource},
                                  action={"method": "GET",
                                          "url": f"{base}/{rid}",
                                          "headers": dict(extra_header)},
                                  next_state=res.body, success=True))
    mech = log.timed("S-DISTILL", arm.kernel.distill_parameterized, obs)
    log.add_scaf(1)
    if mech is None:
        ep = time.perf_counter() - t0
        return {"ok": False, "reason": "distill-failed", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
                "misc_s": ep - sum(log.t.values())}
    log.timed("S-REGISTRY-WRITE", arm.registry.upsert, mech)
    log.add_scaf(1)
    slot = mech.parameter_slots[0]
    ok, _ = log.timed("S-EXECUTE", v2.execute_batch, arm, mech.intent,
                      {"resource_type": resource}, slot, v2.TASK_IDS)
    ep = time.perf_counter() - t0
    return {"ok": bool(ok), "reason": "cold", "arm": arm,
            "phases": dict(log.t), "scaffold": log.scaf, "episode_s": ep,
            "misc_s": ep - sum(log.t.values())}


def _timed_episode(fn, *a, **k):
    return fn(*a, **k)


def run_trial_v6(cls, target, seed, j):
    app = v2.LocalApp()
    try:
        if not v2.wait_ready(app):
            return {"valid": False, "reason": "server-not-ready"}
        t_learn0 = time.perf_counter()
        mechs, cached = v2.make_mech_dicts(app.origin, v2.Counters())
        t_learn_s = time.perf_counter() - t_learn0
        if mechs is None:
            return {"valid": False, "reason": "learn-failed"}
        base_live = {"mech_dicts": {m["mechanism_id"]: m for m in mechs.values()}}
        for r in v2.RESOURCES:
            base_live[r] = v2.unaffected_behavior(mechs, app.origin, r, "base",
                                                 v2.IN_SUPPORT_PROBE_ID)
        pre_unaffected = {r: base_live[r] for r in v2.RESOURCES}
        fresh_silent = None
        try:
            farm = v2.Arm(copy.deepcopy(mechs), Path("/tmp"), "fresh5")
            fmech = farm.target_mech(target)
            if fmech is not None:
                fslot = fmech.parameter_slots[0]
                fr0 = farm.resolve(fmech.intent, {"resource_type": target},
                                   {fslot: str(v2.TASK_IDS[0])})
                if fr0.status.name == "EXECUTABLE" and fr0.bound_action is not None:
                    ffailed = farm.netfetch(fr0.bound_action["url"],
                                            fr0.bound_action.get("headers", {}),
                                            origin=app.origin)
                    fstale, _ = v2.guard(cached[target],
                                         set(v2.flatten(fmech.postconditions)),
                                         ffailed, farm, fmech,
                                         {fslot: str(v2.TASK_IDS[0])})
                    fresh_silent = (not bool(fstale))
        except Exception:
            fresh_silent = None
        app.state.set_perturb(cls, target, seed)
        try:
            wu_reuse = v2.run_repair_reuse(app, app.origin, copy.deepcopy(mechs),
                                           cached[target], target, "reuse")
            wu_cold = v2.run_cold(app, app.origin, target, v2.LEARN_IDS, "warmcold")
            warmups = 2
            wu_reuse_arm = (wu_reuse or {}).get("arm")
            wu_cold_arm = (wu_cold or {}).get("arm")
            try:
                retain_arm = v2.Arm(copy.deepcopy(mechs), Path("/tmp"), "retain5")
                retain_mech = retain_arm.target_mech(target)
                retained = False
                if retain_mech is not None:
                    retain_slot = retain_mech.parameter_slots[0]
                    retain_r0 = retain_arm.resolve(
                        retain_mech.intent, {"resource_type": target},
                        {retain_slot: str(v2.TASK_IDS[0])})
                    if (retain_r0.status.name == "EXECUTABLE"
                            and retain_r0.bound_action is not None):
                        retain_failed = retain_arm.netfetch(
                            retain_r0.bound_action["url"],
                            retain_r0.bound_action.get("headers", {}),
                            origin=app.origin)
                        retain_stale, _ = v2.guard(
                            cached[target],
                            set(v2.flatten(retain_mech.postconditions)),
                            retain_failed, retain_arm, retain_mech,
                            {retain_slot: str(v2.TASK_IDS[0])})
                        retained = bool(retain_stale)
            except Exception:
                retained = False
            if not retained:
                return {"valid": False, "reason": "perturbation-not-retained",
                        "class": cls, "target": target}
            rep_first = (j % 2 == 0)
            if rep_first:
                rep = _timed_episode(run_reuse_episode_bulk, app, app.origin,
                                     copy.deepcopy(mechs), cached[target], target, 5, "bulk5")
                c2 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS_MIN, "coldmin")
                c3 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS, "cold")
                order = ["R5", "C2", "C3"]
            else:
                c3 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS, "cold")
                c2 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS_MIN, "coldmin")
                rep = _timed_episode(run_reuse_episode_bulk, app, app.origin,
                                     copy.deepcopy(mechs), cached[target], target, 5, "bulk5")
                order = ["C3", "C2", "R5"]
            lit = v2.run_literal(app, app.origin, copy.deepcopy(mechs), target)
            nor = v2.run_norepair(app, app.origin, copy.deepcopy(mechs),
                                  cached[target], target)
        except Exception as exc:
            return {"valid": False, "reason": "timed-episode-error",
                    "error": type(exc).__name__}
        post_dicts = {m.mechanism_id: m.as_dict() for m in rep["arm"].registry.all()}
        base_dicts = base_live["mech_dicts"]
        write_set = sorted(mid for mid in set(base_dicts) | set(post_dicts)
                           if base_dicts.get(mid) != post_dicts.get(mid))
        contam = 0
        for r in v2.RESOURCES:
            if r == target:
                continue
            post = v2.unaffected_behavior(post_dicts, app.origin, r, "post",
                                          v2.IN_SUPPORT_PROBE_ID)
            if post != pre_unaffected[r]:
                contam += 1
        n_unaff = len(v2.RESOURCES) - 1
        patched_mech = rep["arm"].target_mech(target)
        overbroad = None
        if patched_mech is not None:
            overbroad = v2.overbroad_contamination(
                base_live, app.origin, target, patched_mech.as_dict(),
                v2.IN_SUPPORT_PROBE_ID)
        mcalls = sum(int(getattr(a["arm"].kernel.counters, "model_calls", 0) or 0)
                     for a in (rep, c3, c2) if "arm" in a)
        mtokens = sum(int(getattr(a["arm"].kernel.counters, "model_tokens", 0) or 0)
                      for a in (rep, c3, c2) if "arm" in a)

        return {
            "valid": True, "class": cls, "target": target,
            "retention_ok": True, "t_learn_s": t_learn_s,
            "repair_success": bool(rep.get("ok")),
            "repair_guard_fired": bool(rep.get("guard_fired")),
            "repair_reason": rep.get("reason"),
            "cold_success": bool(c3.get("ok")),
            "cold_min_success": bool(c2.get("ok")),
            "literal_success": bool(lit["success"]),
            "norepair_success": bool(nor["success"]),
            "norepair_guard_fired": bool(nor.get("guard_fired")),
            "repair_cost": _arm_counters(rep["arm"]),
            "cold_cost": _arm_counters(c3["arm"]),
            "cold_min_cost": _arm_counters(c2["arm"]),
            "literal_cost": _arm_counters(lit["arm"]),
            "norepair_cost": _arm_counters(nor["arm"]),
            "repair_oplog": list(rep["arm"].oplog),
            "cold_oplog": list(c3["arm"].oplog),
            "repair_scaffold": rep.get("scaffold"),
            "cold_scaffold": c3.get("scaffold"),
            "cold_min_scaffold": c2.get("scaffold"),
            "repair_phases": rep.get("phases"),
            "cold_phases": c3.get("phases"),
            "cold_min_phases": c2.get("phases"),
            "repair_misc_s": rep.get("misc_s"),
            "cold_misc_s": c3.get("misc_s"),
            "contamination_n": contam,
            "overbroad_contamination_n": overbroad,
            "write_set_n": len(write_set),
            "fresh_silent": fresh_silent,
            "unaffected_n": n_unaff,
            "base_liveness": all(v and v[0] == 200 and v[2] for v in
                                 (pre_unaffected[r] for r in v2.RESOURCES)),
            "t_reuse_s": rep.get("episode_s"), "t_cold_min_s": c2.get("episode_s"),
            "t_cold_s": c3.get("episode_s"),
            "reg_equiv": bool(rep.get("reg_equiv")),
            "order_rep_first": bool(rep_first), "episode_order": order,
            "warmups_done": warmups,
            "warmup_reuse_success": bool((wu_reuse or {}).get("success")),
            "warmup_reuse_shipped": (_shipped_sum(_arm_counters(wu_reuse_arm))
                                     if wu_reuse_arm is not None else None),
            "warmup_cold_success": bool((wu_cold or {}).get("success")),
            "warmup_cold_shipped": (_shipped_sum(_arm_counters(wu_cold_arm))
                                    if wu_cold_arm is not None else None),
            "timed_error": None, "model_calls": mcalls, "model_tokens": mtokens,
        }
    finally:
        app.stop()
def _shipped_sum(cost):
    return (cost["http_requests"] if "http_requests" in cost else cost["http"]) + \
           (cost["retrieval_calls"] if "retrieval_calls" in cost else cost["retrieval"]) + \
           (cost["verification_calls"] if "verification_calls" in cost else cost["verification"]) + \
           (cost["repair_attempts"] if "repair_attempts" in cost else cost["repair"])


def _http_of(cost):
    return cost["http_requests"] if "http_requests" in cost else cost["http"]


def _cell_status(r, ci):
    if r is None or ci is None or ci[0] is None or ci[1] is None:
        return "UNKNOWN"
    lo, hi = ci
    if r < 1.0 and hi < 1.0:
        return "WIN"
    if r >= 1.0 and lo >= 1.0:
        return "LOSS"
    return "MARGINAL"


def cost_verdict_v6(m):
    if not v2.functional_ok(m):
        return "FUNCTIONAL-FAIL"
    cells = [m.get("M-CELL-L2"), m.get("M-CELL-L2-NA"),
             m.get("M-CELL-L3"), m.get("M-CELL-L3-NA")]
    if any(v == "UNKNOWN" for v in cells):
        return "COST-UNKNOWN"
    if any(v == "LOSS" for v in cells):
        return "PRICED-DEFICIT"
    if all(v == "WIN" for v in cells):
        return "PRICED-WIN"
    return "PRICED-MARGINAL"


def aggregate_v6(cvs):
    if any(v == "FUNCTIONAL-FAIL" for v in cvs):
        return "FALSIFIES-FUNCTIONAL"
    if any(v == "COST-UNKNOWN" for v in cvs):
        return "INCONCLUSIVE"
    if any(v == "PRICED-DEFICIT" for v in cvs):
        return "PERMANENT-DROP-BOUNDED"
    if all(v == "PRICED-WIN" for v in cvs):
        return "SUPPORTS"
    return "INCONCLUSIVE"


def _synth_cells(r2=0.9, r2n=0.91, r3=0.88, r3n=0.89, half=0.03):
    def ci(r):
        return [r - half, r + half]
    return {"M-CELL-L2": _cell_status(r2, ci(r2)),
            "M-CELL-L2-NA": _cell_status(r2n, ci(r2n)),
            "M-CELL-L3": _cell_status(r3, ci(r3)),
            "M-CELL-L3-NA": _cell_status(r3n, ci(r3n))}


def synthetic_reachability_probe_v6():
    def row(ok=True, cells=None):
        m = {"M-REPAIR-SUCCESS": 1.0 if ok else 0.0,
             "M-REPAIR-SUCCESS-WILSON-LOWER": 0.7575 if ok else 0.0,
             "M-CONTAMINATION-RATE": 0.0, "M-WRITE-SET-MAX": 1,
             "M-GUARD-FIRE-RATE": 1.0}
        m.update(cells if cells is not None else _synth_cells())
        return m
    cases = {
        "PRICED-WIN": row(),
        "PRICED-DEFICIT-loss": row(cells=_synth_cells(r3=1.10)),
        "PRICED-MARGINAL-at-1.00": row(cells=_synth_cells(r2=1.0, half=0.03)),
        "PRICED-MARGINAL-straddle": row(cells=_synth_cells(r3=0.99, half=0.03)),
        "PRICED-MARGINAL-boundary-win": row(cells=_synth_cells(r2n=1.0, half=0.03)),
        "FUNCTIONAL-FAIL": row(ok=False),
        "COST-UNKNOWN": row(cells={"M-CELL-L2": "UNKNOWN", "M-CELL-L2-NA": "WIN",
                                   "M-CELL-L3": "WIN", "M-CELL-L3-NA": "WIN"}),
    }
    verdicts = {k: cost_verdict_v6(v) for k, v in cases.items()}
    aggregates = {
        "SUPPORTS": aggregate_v6(["PRICED-WIN"] * 3),
        "PERMANENT-DROP-BOUNDED": aggregate_v6(["PRICED-WIN", "PRICED-DEFICIT",
                                                "PRICED-WIN"]),
        "FALSIFIES-FUNCTIONAL": aggregate_v6(["PRICED-WIN", "FUNCTIONAL-FAIL",
                                              "PRICED-WIN"]),
        "INCONCLUSIVE-unknown": aggregate_v6(["PRICED-WIN", "COST-UNKNOWN",
                                              "PRICED-DEFICIT"]),
        "INCONCLUSIVE-marginal": aggregate_v6(["PRICED-WIN", "PRICED-MARGINAL",
                                               "PRICED-WIN"]),
    }
    all_class = {"PRICED-WIN", "PRICED-DEFICIT", "PRICED-MARGINAL",
                 "FUNCTIONAL-FAIL", "COST-UNKNOWN"}
    all_agg = {"SUPPORTS", "PERMANENT-DROP-BOUNDED", "FALSIFIES-FUNCTIONAL",
               "INCONCLUSIVE"}
    return {
        "class_cost_verdicts": verdicts,
        "aggregate_decisions": aggregates,
        "all_class_branches_reachable": set(verdicts.values()) == all_class,
        "all_aggregate_branches_reachable": set(aggregates.values()) == all_agg,
    }


def _synth_trial_row(lit_ok=False, cold_ok=True, nor_ok=False, guard=True,
                     contam_n=0, write_n=1, overbroad=0.5, base=True,
                     rep_first=True, warmups=2, finite=True, equiv=True,
                     reuse_sum=17, reuse_http=6, cold2_sum=18, cold3_sum=19):
    fin = 0.004 if finite else float("nan")
    cost_re = {"http_requests": reuse_http, "retrieval_calls": 5,
               "verification_calls": 5, "repair_attempts": 1,
               "model_calls": 0, "model_tokens": 0,
               "browser_actions": 0, "latency_ms": 0.0}
    cost_c2 = {"http_requests": 8, "retrieval_calls": 5,
               "verification_calls": 5, "repair_attempts": 0,
               "model_calls": 0, "model_tokens": 0,
               "browser_actions": 0, "latency_ms": 0.0}
    cost_c3 = {"http_requests": 9, "retrieval_calls": 5,
               "verification_calls": 5, "repair_attempts": 0,
               "model_calls": 0, "model_tokens": 0,
               "browser_actions": 0, "latency_ms": 0.0}
    assert _shipped_sum(cost_re) == reuse_sum
    assert _shipped_sum(cost_c2) == cold2_sum
    assert _shipped_sum(cost_c3) == cold3_sum
    phases = {k: 0.0001 for k in PHASE_KEYS}
    return {"repair_success": True, "repair_guard_fired": guard,
            "repair_reason": "repaired", "cold_success": cold_ok,
            "cold_min_success": cold_ok, "literal_success": lit_ok,
            "norepair_success": nor_ok, "norepair_guard_fired": guard,
            "repair_cost": dict(cost_re), "cold_cost": dict(cost_c3),
            "cold_min_cost": dict(cost_c2),
            "repair_scaffold": 9, "cold_scaffold": 3, "cold_min_scaffold": 3,
            "repair_phases": dict(phases), "cold_phases": dict(phases),
            "cold_min_phases": dict(phases),
            "repair_misc_s": 0.0001, "cold_misc_s": 0.0001,
            "contamination_n": contam_n, "overbroad_contamination_n": overbroad,
            "write_set_n": write_n, "fresh_silent": True, "unaffected_n": 4,
            "base_liveness": base, "t_reuse_s": fin, "t_cold_min_s": fin,
            "t_cold_s": fin, "reg_equiv": equiv,
            "order_rep_first": rep_first, "warmups_done": warmups,
            "warmup_reuse_success": True,
            "warmup_reuse_shipped": reuse_sum,
            "warmup_cold_success": True, "warmup_cold_shipped": cold3_sum,
            "model_calls": 0, "model_tokens": 0}


def _mutrow(**kw):
    r = _synth_trial_row()
    r.update(kw)
    return r


def _mutcost(row, key, **kw):
    row[key] = dict(row[key], **kw)
    return row


def synthetic_gate_coverage_probe_v6():
    """Drive the frozen gate block at pass/fail INCLUDING 0.0/0.10 boundaries.

    v6 rescaling for TRIALS_PER_CLASS=36 (unaffected denominator 144/class):
    proves the explicit is-None checks classify legitimately observed 0.0 values
    correctly (they pass upper-bound gates) and trip exactly above the bars.
    Mutation counts are the smallest integers that cross each bar at n=36:
    literal/norepair 4/36=0.111>0.10, cold 32/36=0.889<0.90,
    guard 28/36=0.778<0.80, contamination 15/144=0.104>0.10.
    """
    base_rows = [_synth_trial_row() for _ in range(TRIALS_PER_CLASS)]
    for i, r in enumerate(base_rows):
        r["order_rep_first"] = (i % 2 == 0)
    out = {}
    m = _per_class_metrics_v6("P1-ENDPOINT", base_rows, SEED6 + 70001)
    out["all-pass-0.0-boundaries"] = {"gates": class_gate_reasons("P1-ENDPOINT", base_rows, m),
                                      "literal": m["M-LITERAL-SUCCESS"],
                                      "norepair": m["M-NOREPAIR-SUCCESS"],
                                      "guard": m["M-GUARD-FIRE-RATE"],
                                      "contam": m["M-CONTAMINATION-RATE"]}
    mut = {
        "literal-0.11-trips": [_mutrow(literal_success=True)
                               for _ in range(4)],
        "cold-0.89-trips": [_mutrow(cold_success=False, cold_min_success=False)
                            for _ in range(4)],
        "norepair-0.11-trips": [_mutrow(norepair_success=True)
                                for _ in range(4)],
        "guard-0.79-trips": [_mutrow(repair_guard_fired=False)
                             for _ in range(8)],
        "contam-15of144-trips": [_mutrow(contamination_n=1)
                                 for _ in range(15)],
        "write-2-trips": [_mutrow(write_set_n=2)
                          for _ in range(1)],
        "overbroad-0.09-trips": [_mutrow(overbroad_contamination_n=0.09)
                                 for _ in range(TRIALS_PER_CLASS)],
        "overbroad-0.11-passes": [_mutrow(overbroad_contamination_n=0.11)
                                  for _ in range(TRIALS_PER_CLASS)],
        "equiv-false-trips": [_mutrow(reg_equiv=False)
                              for _ in range(1)],
        "drift-cold-trips": [_mutcost(_mutrow(), "cold_cost", http_requests=10)],
        "drift-reuse-trips": [_mutcost(_mutrow(), "repair_cost", retrieval_calls=6)],
        "drift-reuse-exempt-passes": [_mutrow(repair_success=False,
                                             repair_reason="repair-failed")],
        "parity-broken-trips": "PARITY",
        "warmup-violation-trips": [_mutrow(warmups_done=1)],
    }
    for name, mrows in mut.items():
        rows = [dict(r) for r in base_rows]
        if mrows == "PARITY":
            for r in rows:
                r["order_rep_first"] = True
        else:
            for i, mr in enumerate(mrows):
                rows[i] = mr
            for i, r in enumerate(rows):
                r["order_rep_first"] = (i % 2 == 0)
        m = _per_class_metrics_v6("P1-ENDPOINT", rows, SEED6 + 70002)
        out[name] = {"gates": class_gate_reasons("P1-ENDPOINT", rows, m)}
    return out


def _carrier():
    return {
        "kernel_sha256": hashlib.sha256((REPO / "src/spider/kernel.py").read_bytes()).hexdigest(),
        "models_sha256": hashlib.sha256((REPO / "src/spider/models.py").read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((REPO / "src/spider/registry.py").read_bytes()).hexdigest(),
        "init_sha256": hashlib.sha256((REPO / "src/spider/__init__.py").read_bytes()).hexdigest(),
        "v2_runner_sha256": V2_PIN_SHA,
        "v2_runner_bytes": V2_PIN_BYTES,
    }
def _per_class_metrics_v6(cls, rows, seed_base):
    n = len(rows)
    rep_ok = sum(1 for r in rows if r["repair_success"])
    guard_ok = sum(1 for r in rows if r["repair_guard_fired"])
    contam = sum(r["contamination_n"] for r in rows)
    unaff = sum(r["unaffected_n"] for r in rows)
    write_max = max([r.get("write_set_n") for r in rows if r.get("write_set_n") is not None]
                    or [None])
    base_live_true = sum(1 for r in rows if r.get("base_liveness"))
    overbroad = v2.mean([r["overbroad_contamination_n"] for r in rows
                         if r.get("overbroad_contamination_n") is not None])
    m = {
        "M-REPAIR-SUCCESS": rep_ok / n if n else None,
        "M-REPAIR-SUCCESS-WILSON-LOWER": v2.wilson_lower(rep_ok, n) if n else None,
        "M-CONTAMINATION-RATE": (contam / unaff) if unaff else None,
        "M-WRITE-SET-MAX": write_max,
        "M-GUARD-FIRE-RATE": guard_ok / n if n else None,
        "M-COLD-SUCCESS": sum(1 for r in rows if r["cold_success"]) / n if n else None,
        "M-LITERAL-SUCCESS": sum(1 for r in rows if r["literal_success"]) / n if n else None,
        "M-NOREPAIR-SUCCESS": sum(1 for r in rows if r["norepair_success"]) / n if n else None,
        "M-BASE-LIVENESS": base_live_true / n if n else None,
        "M-OVERBROAD-CONTAMINATION-N": overbroad,
    }
    sh_re = sum(_shipped_sum(r["repair_cost"]) for r in rows)
    sh_c2 = sum(_shipped_sum(r["cold_min_cost"]) for r in rows)
    sh_c3 = sum(_shipped_sum(r["cold_cost"]) for r in rows)
    sc_re = sum(r["repair_scaffold"] for r in rows if r.get("repair_scaffold") is not None)
    sc_c2 = sum(r["cold_min_scaffold"] for r in rows if r.get("cold_min_scaffold") is not None)
    sc_c3 = sum(r["cold_scaffold"] for r in rows if r.get("cold_scaffold") is not None)
    h_re = sum(_http_of(r["repair_cost"]) for r in rows)
    h_c2 = sum(_http_of(r["cold_min_cost"]) for r in rows)
    h_c3 = sum(_http_of(r["cold_cost"]) for r in rows)
    m["M-SHIPPED-REUSE"] = sh_re
    m["M-SHIPPED-COLD-L2"] = sh_c2
    m["M-SHIPPED-COLD-L3"] = sh_c3
    m["M-SHIPPED-RATIO-L2"] = (sh_re / sh_c2) if sh_c2 else None
    m["M-SHIPPED-RATIO-L3"] = (sh_re / sh_c3) if sh_c3 else None
    m["M-COST-FETCH-RATIO-L3"] = (h_re / h_c3) if h_c3 else None
    m["M-COLD-HTTP-L2"] = h_c2
    m["M-COLD-HTTP-L3"] = h_c3
    m["M-REUSE-HTTP"] = h_re
    equiv = [r for r in rows if r.get("repair_reason") == "repaired"
             and r.get("repair_success")
             and r.get("warmup_reuse_shipped") is not None]
    m["M-EQUIV-MATCH-N"] = sum(1 for r in equiv if r["warmup_reuse_shipped"]
                               == _shipped_sum(r["repair_cost"]))
    m["M-EQUIV-MATCH-DEN"] = len(equiv)
    m["M-SCAFFOLD-REUSE"] = sc_re
    m["M-SCAFFOLD-COLD-L3"] = sc_c3
    m["M-SP5-RATIO-L2"] = ((sh_re + sc_re) / (sh_c2 + sc_c2)) if (sh_c2 + sc_c2) else None
    m["M-SP5-RATIO-L3"] = ((sh_re + sc_re) / (sh_c3 + sc_c3)) if (sh_c3 + sc_c3) else None
    t_rep = [r["t_reuse_s"] for r in rows]
    t_c2 = [r["t_cold_min_s"] for r in rows]
    t_c3 = [r["t_cold_s"] for r in rows]
    med_rep, med_c2, med_c3 = _median(t_rep), _median(t_c2), _median(t_c3)
    m["M-LATENCY-REUSE-MED-S"] = med_rep
    m["M-LATENCY-COLD-L2-MED-S"] = med_c2
    m["M-LATENCY-COLD-L3-MED-S"] = med_c3
    m["M-LATENCY-R-L2"] = (med_rep / med_c2) if (med_rep is not None and med_c2) else None
    m["M-LATENCY-R-L3"] = (med_rep / med_c3) if (med_rep is not None and med_c3) else None
    no_arg_rep = [r["t_reuse_s"] - (r.get("repair_phases") or {}).get("S-ARG", 0.0)
                  for r in rows]
    no_arg_c2 = [r["t_cold_min_s"] - (r.get("cold_min_phases") or {}).get("S-ARG", 0.0)
                 for r in rows]
    no_arg_c3 = [r["t_cold_s"] - (r.get("cold_phases") or {}).get("S-ARG", 0.0)
                 for r in rows]
    med_nar, med_nac2, med_nac3 = _median(no_arg_rep), _median(no_arg_c2), _median(no_arg_c3)
    m["M-LATENCY-R-L2-NOARG"] = ((med_nar / med_nac2)
        if (med_nar is not None and med_nac2) else None)
    m["M-LATENCY-R-L3-NOARG"] = ((med_nar / med_nac3)
        if (med_nar is not None and med_nac3) else None)
    if all(v is not None for v in (t_rep, t_c2, t_c3)) and n >= 2:
        lo2, hi2 = _median_ratio_ci(t_rep, t_c2, seed_base + 1, B_LAT)
        lo3, hi3 = _median_ratio_ci(t_rep, t_c3, seed_base + 2, B_LAT)
        m["M-LATENCY-R-L2-CI95"] = [lo2, hi2]
        m["M-LATENCY-R-L3-CI95"] = [lo3, hi3]
        blo2, bhi2 = _median_ratio_ci_bf(t_rep, t_c2, seed_base + 11, B_BONF)
        blo3, bhi3 = _median_ratio_ci_bf(t_rep, t_c3, seed_base + 12, B_BONF)
        m["M-LATENCY-R-L2-CIBF"] = [blo2, bhi2]
        m["M-LATENCY-R-L3-CIBF"] = [blo3, bhi3]
    else:
        m["M-LATENCY-R-L2-CI95"] = None
        m["M-LATENCY-R-L3-CI95"] = None
        m["M-LATENCY-R-L2-CIBF"] = None
        m["M-LATENCY-R-L3-CIBF"] = None
    if all(v is not None for v in (no_arg_rep, no_arg_c2, no_arg_c3)) and n >= 2:
        nlo2, nhi2 = _median_ratio_ci(no_arg_rep, no_arg_c2, seed_base + 3, B_LAT)
        nlo3, nhi3 = _median_ratio_ci(no_arg_rep, no_arg_c3, seed_base + 4, B_LAT)
        m["M-LATENCY-R-L2-NOARG-CI95"] = [nlo2, nhi2]
        m["M-LATENCY-R-L3-NOARG-CI95"] = [nlo3, nhi3]
        blo2, bhi2 = _median_ratio_ci_bf(no_arg_rep, no_arg_c2, seed_base + 13, B_BONF)
        blo3, bhi3 = _median_ratio_ci_bf(no_arg_rep, no_arg_c3, seed_base + 14, B_BONF)
        m["M-LATENCY-R-L2-NOARG-CIBF"] = [blo2, bhi2]
        m["M-LATENCY-R-L3-NOARG-CIBF"] = [blo3, bhi3]
    else:
        m["M-LATENCY-R-L2-NOARG-CI95"] = None
        m["M-LATENCY-R-L3-NOARG-CI95"] = None
        m["M-LATENCY-R-L2-NOARG-CIBF"] = None
        m["M-LATENCY-R-L3-NOARG-CIBF"] = None
    m["M-CELL-L2"] = _cell_status(m["M-LATENCY-R-L2"], m["M-LATENCY-R-L2-CIBF"])
    m["M-CELL-L2-NA"] = _cell_status(m["M-LATENCY-R-L2-NOARG"], m["M-LATENCY-R-L2-NOARG-CIBF"])
    m["M-CELL-L3"] = _cell_status(m["M-LATENCY-R-L3"], m["M-LATENCY-R-L3-CIBF"])
    m["M-CELL-L3-NA"] = _cell_status(m["M-LATENCY-R-L3-NOARG"], m["M-LATENCY-R-L3-NOARG-CIBF"])
    m["M-LATENCY-SIGN-REUSE-SLOWER-L3"] = sum(1 for a, b in zip(t_rep, t_c3) if a > b)
    comp = {}
    for key in PHASE_KEYS:
        mr = _median([(r.get("repair_phases") or {}).get(key, 0.0) for r in rows])
        mc = _median([(r.get("cold_phases") or {}).get(key, 0.0) for r in rows])
        comp[key] = {"reuse_med_s": mr, "cold_med_s": mc, "delta_med_s": mr - mc}
    m["M-PHASE-DELTAS"] = comp
    clos = []
    for r in rows:
        ep = r.get("t_reuse_s")
        ms = r.get("repair_misc_s")
        if ep:
            clos.append(abs(ms or 0.0) / ep)
    m["M-CLOSURE-REUSE-MED"] = _median(clos)
    clos_c = []
    for r in rows:
        ep = r.get("t_cold_s")
        ms = r.get("cold_misc_s")
        if ep:
            clos_c.append(abs(ms or 0.0) / ep)
    m["M-CLOSURE-COLD-MED"] = _median(clos_c)
    learn = [r.get("t_learn_s") for r in rows if r.get("t_learn_s") is not None]
    learn_med = _median(learn)
    m["M-T-LEARN-MED-S"] = learn_med
    for tag, cold_med, reuse_med in (("L2", med_c2, med_rep), ("L2NA", med_nac2, med_nar),
                                     ("L3", med_c3, med_rep), ("L3NA", med_nac3, med_nar)):
        denom = (cold_med - reuse_med) if (cold_med is not None and reuse_med is not None) else None
        m[f"M-RECURRENCE-N-STAR-{tag}"] = ((learn_med / denom)
            if (learn_med is not None and denom is not None and denom > 0) else None)
    m["M-MODEL-CALLS"] = sum(r.get("model_calls", 0) or 0 for r in rows)
    m["M-MODEL-TOKENS"] = sum(r.get("model_tokens", 0) or 0 for r in rows)
    m["M-N"] = n
    return m


def _attribution_v6(per_class):
    excess = {}
    for cls, m in per_class.items():
        mr = m.get("M-LATENCY-REUSE-MED-S")
        mc = m.get("M-LATENCY-COLD-L3-MED-S")
        excess[cls] = (mr - mc) if (mr is not None and mc is not None) else None
    comps = {}
    for key in PHASE_KEYS + ["REGISTRY", "GUARD", "COLD-FETCH"]:
        for cls, m in per_class.items():
            d = m.get("M-PHASE-DELTAS", {})
            if key == "REGISTRY":
                delta = sum(d.get(k, {}).get("delta_med_s", 0.0) for k in REGISTRY_PHASES)
            elif key == "GUARD":
                delta = sum(d.get(k, {}).get("delta_med_s", 0.0) for k in GUARD_PHASES)
            elif key == "COLD-FETCH":
                delta = -sum(d.get(k, {}).get("delta_med_s", 0.0)
                             for k in COLD_FETCH_PHASES + ["S-DISTILL"])
            else:
                delta = d.get(key, {}).get("delta_med_s", 0.0)
            comps.setdefault(key, {})[cls] = delta
    shares = {}
    for key, per_cls in comps.items():
        for cls, delta in per_cls.items():
            e = excess.get(cls)
            shares.setdefault(key, {})[cls] = (delta / e) if e else None
    votes = {}
    for key, per_cls in shares.items():
        votes[key] = sum(1 for cls in per_class
                         if per_cls.get(cls) is not None and per_cls[cls] >= ATTRIB_SHARE)
    qual = sorted(k for k in votes if votes[k] >= 2)
    closure_ok = all(
        (per_class[cls].get("M-CLOSURE-REUSE-MED") is not None
         and per_class[cls]["M-CLOSURE-REUSE-MED"] <= CLOSURE_BAR)
        for cls in per_class)
    if not closure_ok:
        answer, aset = "ATTRIBUTION-INVALID", []
    elif all((e or 0.0) <= 0 for e in excess.values() if e is not None):
        answer, aset = "ATTRIBUTION-MOOT", []
    elif not qual:
        answer, aset = "UNATTRIBUTED", []
    elif len(qual) == 1:
        answer, aset = "ATTRIBUTED-" + qual[0], qual
    else:
        answer, aset = "TIE-" + "+".join(qual), qual
    return {"excess_med_s": excess, "phase_deltas_med_s": comps,
            "shares_of_excess": shares, "votes_ge_half": votes,
            "attribution_set": aset, "closure_ok": closure_ok, "answer": answer,
            "semantics": ("net-gap shares: denominator is the NET median episode gap "
                          "(reuse minus cold, net of cold-side savings); shares may exceed "
                          "1.0 and are non-decomposable; gross reuse-phase medians are in "
                          "M-PHASE-DELTAS; the answer is the full qualifying set, never "
                          "selected by driver iteration order.")}
def class_gate_reasons(cls, rows, m):
    """Frozen validity-gate block with explicit is-None checks (RF-6 remedy).

    Legitimately observed 0.0 values PASS upper-bound gates; only None (missing)
    or above-bar values trip. Returns the list of invalid reasons (empty = pass).
    """
    bad = []
    if not all(r.get("base_liveness") for r in rows):
        bad.append(f"{cls}:base-liveness-miss")
    if m.get("M-LITERAL-SUCCESS") is None or m["M-LITERAL-SUCCESS"] > 0.10:
        bad.append(f"{cls}:perturbation-does-not-bite")
    if m.get("M-COLD-SUCCESS") is None or m["M-COLD-SUCCESS"] < 0.90:
        bad.append(f"{cls}:cold-baseline-not-live")
    if m.get("M-NOREPAIR-SUCCESS") is None or m["M-NOREPAIR-SUCCESS"] > 0.10:
        bad.append(f"{cls}:abstention-control-fired")
    if m.get("M-GUARD-FIRE-RATE") is None or m["M-GUARD-FIRE-RATE"] < 0.80:
        bad.append(f"{cls}:guard-not-live")
    if m.get("M-CONTAMINATION-RATE") is None or m["M-CONTAMINATION-RATE"] > 0.10:
        bad.append(f"{cls}:contamination-above-bar")
    if m.get("M-WRITE-SET-MAX") is None or m["M-WRITE-SET-MAX"] > 1:
        bad.append(f"{cls}:write-set-leakage")
    if not (m.get("M-OVERBROAD-CONTAMINATION-N") is not None
            and m["M-OVERBROAD-CONTAMINATION-N"] > 0.10):
        bad.append(f"{cls}:overbroad-instrument-insensitive")
    if sum(1 for r in rows if r.get("order_rep_first")) != TRIALS_PER_CLASS // 2:
        bad.append(f"{cls}:parity-order-broken")
    if any(r.get("warmups_done") != 2 for r in rows):
        bad.append(f"{cls}:warmup-violation")
    if any(not (math.isfinite(r.get("t_reuse_s") or float("nan"))
               and math.isfinite(r.get("t_cold_s") or float("nan"))
               and math.isfinite(r.get("t_cold_min_s") or float("nan"))
               and (r.get("t_reuse_s") or 0) > 0) for r in rows):
        bad.append(f"{cls}:nonfinite-latency")
    if any(not r.get("reg_equiv") for r in rows):
        bad.append(f"{cls}:registry-equivalence-broken")
    drift_cold = (m["M-SHIPPED-COLD-L2"] != TRIALS_PER_CLASS * NOMINAL["cold_l2_sum"]
                  or m["M-SHIPPED-COLD-L3"] != TRIALS_PER_CLASS * NOMINAL["cold_l3_sum"]
                  or m.get("M-COLD-HTTP-L2") != TRIALS_PER_CLASS * NOMINAL["cold_l2_http"]
                  or m.get("M-COLD-HTTP-L3") != TRIALS_PER_CLASS * NOMINAL["cold_l3_http"])
    if drift_cold:
        bad.append(f"{cls}:V-DRIFT-COLD-nominal-mismatch")
    drift_reuse = False
    for r in rows:
        if r.get("repair_reason") == "repaired" and r.get("repair_success"):
            if (_shipped_sum(r["repair_cost"]) != NOMINAL["reuse_sum"]
                    or _http_of(r["repair_cost"]) != REUSE_HTTP_EXPECTED[cls]):
                drift_reuse = True
                break
    if drift_reuse:
        bad.append(f"{cls}:V-DRIFT-REUSE-nominal-mismatch")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mechanics-only", action="store_true")
    ap.add_argument("--reachability-probe", action="store_true")
    ap.add_argument("--liveness-only", action="store_true")
    args = ap.parse_args()

    runner_self_sha = "UNKNOWN"
    try:
        runner_self_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        pass
    carrier = _carrier()

    if args.reachability_probe:
        out = {"status": "V6-REACHABILITY-PROBE", "experiment_id": EXP_ID6,
               "lane": "runtime", "runner_self_sha": runner_self_sha,
               "decision_rule": synthetic_reachability_probe_v6(),
               "gate_coverage": synthetic_gate_coverage_probe_v6(),
               "repair_signal_probe": v2.synthetic_repair_signal_probe()}
        print(json.dumps(out, indent=2))
        return

    if args.liveness_only:
        app = v2.LocalApp()
        try:
            ready = v2.wait_ready(app)
            c = v2.Counters()
            mechs, cached = v2.make_mech_dicts(app.origin, c) if ready else (None, None)
            live = bool(mechs)
            one_ok = in_support_ok = out_deg = None
            phase_keys = None
            closure_finite = None
            bulk_bytes_equal = None
            bulk_target_only_ok = None
            if live:
                arm = v2.Arm(copy.deepcopy(mechs), Path("/tmp"), "live5")
                mech = arm.target_mech("users")
                slot = mech.parameter_slots[0]
                r = arm.resolve(mech.intent, {"resource_type": "users"},
                                {slot: str(v2.TASK_IDS[0])})
                if r.status.name == "EXECUTABLE" and r.bound_action is not None:
                    res = arm.netfetch(r.bound_action["url"],
                                       r.bound_action.get("headers", {}))
                    one_ok = res.status == 200 and res.body is not None and arm.verify(
                        r.mechanism_id, res.body, {slot: str(v2.TASK_IDS[0])})
                in_support = {rr: v2.unaffected_behavior(mechs, app.origin, rr, "liveinst",
                                                         v2.IN_SUPPORT_PROBE_ID)
                              for rr in v2.RESOURCES}
                out_support = {rr: v2.unaffected_behavior(mechs, app.origin, rr, "liveold", "1")
                               for rr in v2.RESOURCES}
                in_support_ok = all(v is not None and v[0] == 200 and v[2] is True
                                    for v in in_support.values())
                out_deg = all(v is not None and v[0] == "NO-RESOLVE"
                              for v in out_support.values())
                up = v2.Arm(copy.deepcopy(mechs), Path("/tmp"), "liveup")
                bk = BulkArm(_breadth_subset(copy.deepcopy(mechs), "users", 5),
                             Path("/tmp"), "livebulk")
                bulk_bytes_equal = (up.path.read_bytes() == bk.path.read_bytes())
                up_ids = sorted(m.mechanism_id for m in up.registry.all())
                bk_ids = sorted(m.mechanism_id for m in bk.registry.all())
                bulk_target_only_ok = (bk_ids == up_ids)  # n=5 full-set identity (no n=1 episode in v6)
                ep = run_cold_episode(app, app.origin, "users", v2.LEARN_IDS_MIN,
                                      "livecold")
                phase_keys = sorted((ep.get("phases") or {}).keys())
                ep_s = ep.get("episode_s") or 0.0
                closure_finite = (math.isfinite(ep_s) and ep_s > 0
                                  and math.isfinite(ep.get("misc_s") or float("nan")))
            np_t = v2.no_perturbation_trial(SEED6 + 1) if ready else {"stale": None}
            nz_t = v2.noise_trial(SEED6 + 2) if ready else {"stale": None}
        finally:
            app.stop()
        print(json.dumps({"status": "V6-LIVENESS-ONLY", "experiment_id": EXP_ID6,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "server_ready": ready, "distill_live": live,
                          "task_read_verified": bool(one_ok),
                          "in_support_probe_id": v2.IN_SUPPORT_PROBE_ID,
                          "contamination_instrument_live": in_support_ok,
                          "out_of_support_probe_degenerate": out_deg,
                          "bulk_bytes_equal_upsert": bulk_bytes_equal,
                          "bulk_target_only_ok": bulk_target_only_ok,
                          "nc_no_perturbation_stale": np_t.get("stale"),
                          "nc_noise_stale": nz_t.get("stale"),
                          "timer_resolution_s": time.get_clock_info("perf_counter").resolution,
                          "instrumented_episode_phase_keys": phase_keys,
                          "instrumented_episode_closure_finite": closure_finite,
                          "carrier": carrier}, indent=2))
        return

    if args.mechanics_only:
        canary = []
        for ci, cls in enumerate(CLASSES):
            r = run_trial_v6(cls, TARGETS[ci % len(TARGETS)], SEED6 + 91000 + ci, ci)
            canary.append({k: r.get(k) for k in (
                "valid", "class", "target", "order_rep_first", "episode_order",
                "repair_success", "cold_success",
                "cold_min_success", "literal_success", "norepair_success",
                "repair_guard_fired", "contamination_n", "overbroad_contamination_n",
                "unaffected_n", "base_liveness", "write_set_n", "repair_cost",
                "cold_cost", "cold_min_cost",
                "repair_oplog", "cold_oplog", "warmups_done", "model_calls",
                "repair_scaffold", "cold_scaffold", "t_reuse_s", "t_cold_s",
                "t_learn_s", "reg_equiv", "repair_misc_s", "timed_error")})
        np_t = v2.no_perturbation_trial(SEED6 + 1)
        nz_t = v2.noise_trial(SEED6 + 2)
        print(json.dumps({"status": "V6-MECHANICS-ONLY", "experiment_id": EXP_ID6,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "seed": SEED6, "carrier": carrier,
                          "canary": canary, "nc_no_perturbation": np_t,
                          "nc_noise": nz_t}, indent=2))
        return

    _check_v1_binding()
    trials = []
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial_v6(cls, target, SEED6 + 1000 * (ci + 1) + j, j))
    np_t = v2.no_perturbation_trial(SEED6 + 1)
    nz_t = v2.noise_trial(SEED6 + 2)

    invalid = []
    for r in trials:
        if not r.get("valid"):
            invalid.append(f"{r.get('class')}:{r.get('reason')}")
        if r.get("timed_error"):
            invalid.append(f"{r.get('class')}:timed-episode-error")
    per_class = {}
    for ci, cls in enumerate(CLASSES):
        rows = [r for r in trials if r.get("valid") and r["class"] == cls]
        if len(rows) != TRIALS_PER_CLASS:
            invalid.append(f"{cls}:n-control-{len(rows)}!={TRIALS_PER_CLASS}")
            continue
        m = _per_class_metrics_v6(cls, rows, SEED6 + 7000 * (ci + 1))
        invalid.extend(class_gate_reasons(cls, rows, m))
        m["V-DRIFT-COLD-HOLDS"] = not any("V-DRIFT-COLD" in v for v in invalid if v.startswith(cls))
        m["V-DRIFT-REUSE-HOLDS"] = not any("V-DRIFT-REUSE" in v for v in invalid if v.startswith(cls))
        eq = (m["M-SHIPPED-RATIO-L2"] is not None and m["M-SHIPPED-RATIO-L3"] is not None
              and m["M-SHIPPED-RATIO-L2"] < 1.0 and m["M-SHIPPED-RATIO-L3"] < 1.0
              and m.get("M-COST-FETCH-RATIO-L3") is not None
              and m["M-COST-FETCH-RATIO-L3"] <= FETCH_BAR)
        m["V-EQ-HOLDS"] = bool(eq)
        per_class[cls] = m

    attribution = _attribution_v6(per_class) if per_class else {"answer": "ATTRIBUTION-INVALID",
                                                                "attribution_set": [],
                                                                "closure_ok": False}
    class_verdicts = {cls: cost_verdict_v6(m) for cls, m in per_class.items()}
    if invalid:
        decision, outcome, status = "MEASUREMENT_INVALID", "INCONCLUSIVE", "MEASUREMENT_INVALID"
    elif any(v == "FUNCTIONAL-FAIL" for v in class_verdicts.values()):
        decision, outcome, status = "FALSIFIES-FUNCTIONAL", "FALSIFIES", "COMPLETE"
    elif any(v == "COST-UNKNOWN" for v in class_verdicts.values()):
        decision, outcome, status = "INCONCLUSIVE", "INCONCLUSIVE", "COMPLETE"
    else:
        agg = aggregate_v6(list(class_verdicts.values()))
        decision = agg
        outcome = "SUPPORTS" if agg == "SUPPORTS" else ("INCONCLUSIVE" if agg == "INCONCLUSIVE"
                                                        else "FALSIFIES")
        status = "COMPLETE"
    if decision in ("SUPPORTS", "PERMANENT-DROP-BOUNDED", "FALSIFIES-FUNCTIONAL"):
        product_note = ("re-admit" if decision == "SUPPORTS"
                        else ("permanent-bounded-drop-no-further-L-sweeps"
                              if decision == "PERMANENT-DROP-BOUNDED"
                              else "bounded-mechanism-concern-no-drop-no-readmit"))
    else:
        product_note = "no-decision-no-drop-no-readmit"
    out = {"status": status, "outcome": outcome, "decision": decision,
           "experiment_id": EXP_ID6, "lane": "runtime",
           "runner_self_sha": runner_self_sha, "seed": SEED6,
           "invalid_reasons": invalid,
           "class_verdicts": class_verdicts, "per_class": per_class,
           "attribution": attribution,
           "nc_no_perturbation_stale": np_t.get("stale"),
           "nc_noise_stale": nz_t.get("stale"),
           "product_note": product_note,
           "b3_model_economics": "UNSATISFIABLE-no-endpoint-counters-only-blocker-recorded",
           "model_calls_total": sum(r.get("model_calls", 0) or 0 for r in trials),
           "model_tokens_total": sum(r.get("model_tokens", 0) or 0 for r in trials),
           "carrier": carrier, "trials": trials}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
# === V6-DRIVER-END ===
```

## 13. Pre-2.0 comparison (non-duplication record)

Screened `codex/legacy_brief.json` (7 findings), `codex/legacy_artifact_index.json`
(1401 artifacts; subject search on repair/delta/perturb returned 218 candidates,
of which the repair-bearing clusters were inspected: graph cycle3/fused REPAIR
recounts sha f2239dd8dfb2/c7a052ea289, runtime R0/R1/R2 repair rounds,
frontier-scoped-delta-repair capsule plumbing sha f12a5662825a, intel repair
reproductions), and `codex/claim_state.json` (C-DELTA-REPAIR precedents: only
P2-AUTOMATION, an operational orchestration lesson). All pre-2.0 repair-bearing
artifacts sit on DIFFERENT substrates (historical capsule/procedure stores,
form-login procedures, taglove snapshots, graph robustness banks) with DIFFERENT
treatments (no shipped-parameterized-carrier reuse-vs-cold comparison),
DIFFERENT comparators, and UNTRUSTED verdict tokens (navigation metadata only).
None combined a perturbable fetch-scarce substrate, the shipped parameterized
carrier, reuse-vs-cold accounting with contamination bounds, and CI-gated latency
deciding — and none tested a larger-N resolution of CI-straddled cells at all.
Classification: LEGACY: NO_MATCH for a larger-N power increase on the frozen
R2 design (a frozen-design N increase cannot duplicate archive content in any
case). Cited artifact SHAs live in the legacy index entries above; the frozen
archive blob is 9bb76113aeaf46d9aecdd8a38349a3a7741e57c3 (per
codex/legacy_brief.json). This design never repeats an identical
invalid/degenerate design: every parent-packet validity property (gate idiom,
family-wise CIs, content-pinned bulk materialization, correct contamination
denominator, complete freeze set, disclosed abstention-control vacuity, symmetric
CI-gated asymmetry) is preserved at N=36 scale, and the rescaled gate-coverage
probe (§15) re-demonstrates each one. Research 2.0 continuity: reuses the accepted
R2 packets EXP-RUNTIME-38244432934 (v2 module, frozen) and
EXP-RUNTIME-38816779349 (BulkArm treatment, nominal vectors, functional bars, audit
diagnostics AF-5/AF-6/AF-7) by exact immutable reference, with a fresh SEED6 bank
making this an independent measurement rather than a re-run.

## 14. Pre-freeze self-attack (satisfiability)

E1 empty branches: the pure classifier + gate block were driven with synthetic rows
at DESIGN (§15): all 5 class branches and all 4 aggregates plus MEASUREMENT_INVALID
produce; strict-inequality boundaries hold (R=1.00 never a win); no branch is empty.
The PARK-on-second-straddle trigger is not a new branch — it is the PRODUCT mapping
of INCONCLUSIVE-via-MARGINAL, so no hidden state evades the frozen rule. E2
treatment/comparator identity: BulkArm changes only the write pattern (1 replace vs
N upserts) with byte-identical content (canary §15); cold path is parent-identical;
the gated comparison differs in physical resolve/fetch/verify/scaffold counts plus
wall-clock — never identical. N changes trial count only, never the code path, so
identity transfers. E3 ceiling baselines: cold latency is continuous (no ceiling);
1.0 success levels are functional gates, never deciders; the 12 deciders have live
dynamic range (61ns timer granularity vs 0.02-1.0ms gaps, 4-5 orders). The shipped
17/18/19 counter is a drift-checked premise, never the decider. E4 insensitive
controls: literal-replay must-fail live (parent 0.0); overbroad fires 4/4 in the
parent and the instrument is re-fired at DESIGN; NCs silent; guard fires 108/108
expected at full function; B-NO-REPAIR vacuity is disclosed and never load-bearing.
Gate-coverage at N=36 proves minimal crossing inputs trip exactly one gate each.
E5 missing prerequisites: none — §3 all verified (§15); the only scale-sensitive
inputs (parity evenness, tail indices, Wilson bar slack, nominal products
36x17/18/19, rotation balance 12x/target) are arithmetically confirmed. E6 unbound
mutables: the 5 freeze paths plus the content-bound driver exhaust the import
closure (stdlib + pinned v2; all 30 invoked v2 attributes name-checked); no
bank/dataset/fixture is read. E7 arithmetic: Bonferroni 1-0.05/12 CIs with B=10000
are computable from n=36 (tail ~21 samples/side, frozen seeds => deterministic);
strict inequalities partition every cell into exactly one of
WIN/LOSS/MARGINAL/UNKNOWN; nominal products verified (36x18=648, 36x19=684,
36x8=288, 36x9=324, 36x17=612). E8 scope discipline: DESIGN ran no
outcome-bearing measurement — no timed reuse-vs-cold comparison exists anywhere in
§15 evidence; the only executed episodes at DESIGN are unperturbed discarded
fresh-path reads plus a discrete byte compare. E9 power honesty: the 1/sqrt(N)
projection is stated as a projection with a named failure mode (non-shrinking
dispersion -> straddle -> PARK), not a guarantee; no feasible N is promised to
resolve a sub-3% true effect, and the stop trigger converts that case into a
bounded PARK rather than an open-ended funding loop. E10 regression blindness:
previously-WIN cells are re-measured at common N (not carried forward), so a
larger-N regression surfaces as LOSS/MARGINAL under the same frozen rule.

## 15. DESIGN probe evidence (cheap, non-outcome-bearing)

Classifier reachability (pure synthetic, v6 functions): all class branches
{PRICED-WIN, PRICED-DEFICIT, PRICED-MARGINAL, FUNCTIONAL-FAIL, COST-UNKNOWN} and all
aggregates {SUPPORTS, PERMANENT-DROP-BOUNDED, FALSIFIES-FUNCTIONAL, INCONCLUSIVE}
(via UNKNOWN and via MARGINAL paths) reachable; all-branch flags true.
Gate-coverage at N=36 (pure synthetic, 36 rows): all-pass-0.0-boundaries -> [];
literal-4/36 -> [perturbation-does-not-bite]; cold-32/36 -> [cold-baseline-not-live];
norepair-4/36 -> [abstention-control-fired]; guard-28/36 -> [guard-not-live];
contam-15/144 -> [contamination-above-bar]; write-2 -> [write-set-leakage];
overbroad-0.09 -> [overbroad-instrument-insensitive]; overbroad-0.11 -> [];
equiv-false -> [registry-equivalence-broken]; drift-cold (+1 http) and drift-reuse
(+1 retrieval) -> [nominal-mismatch]; genuine repair-failed exempt -> [];
parity-broken -> [parity-order-broken]; warmup-1 -> [warmup-violation].
Arithmetic: SEED6=180486679 disjoint from SEED5=162073685 and SEED4=3980394806;
Wilson lower for 36/36 = 0.903578 >= 0.60; parent half-widths 0.060/0.068/0.056/0.071
project to 0.0346/0.0393/0.0323/0.0410 at N=36; parity 18/18 even; Bonferroni tail
indices at B=10000 are integral (lo 20, hi 9978); rotation TARGETS[(ci+j)%3] yields
exactly 12x per target per class. Liveness (discarded, unperturbed, this machine):
Python 3.12.15, distill 5 mechs, resolve EXECUTABLE, fetch 200 with body, verify
True, guard silent on unperturbed body, BulkArm-vs-upsert registry bytes
byte-identical at n=5, timer nonzero minimum ~61ns. v2 module: 60855 bytes,
d4871091, all 30 invoked attributes present (Arm, Mechanism, MechanismRegistry,
SpiderKernel, TrajectoryCounters, Counters, MIN_CONFIDENCE, CLASSES, TARGETS,
TRIALS_PER_CLASS, RESOURCES, LEARN_IDS, LEARN_IDS_MIN, TASK_IDS,
IN_SUPPORT_PROBE_ID, LocalApp, wait_ready, make_mech_dicts, unaffected_behavior,
overbroad_contamination, guard, local_repair, execute_batch, run_repair_reuse,
run_cold, run_literal, run_norepair, functional_ok, flatten, plus mean,
wilson_lower, no_perturbation_trial, noise_trial, synthetic_repair_signal_probe).
Carrier hashes match the parent freeze exactly
(3d173722/3a6caf97/338aaf4d/51fb440d). Full probe outputs are reproduced by
EXECUTE preflight from the frozen driver; the DESIGN runs above carry no outcome
information about reuse-vs-cold latency at any N.
