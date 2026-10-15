# EXP-RUNTIME-38816779349 preregistration — no-tax repair-gated re-test (runtime, design-contract v2)

Director mandate (binding): Global Research Director REOPEN on C-DELTA-REPAIR —
once the carrier per-episode registry-materialization tax is removed (single bulk
replace or target-only registration) and the frozen driver gate defect is repaired,
is reuse-based localized repair strictly cheaper than cold re-derivation at L=2 and
L=3 on both timed boundaries, and how does the margin scale with inheritance breadth
and recurrence? The parent handoff (EXP-RUNTIME-38340133174) is continuity evidence
only; its `next_question` matches the mandate question and is therefore adopted, but
no threshold, ratio, or wording from the parent packet is inherited as evidence.

## 1. Background and decision context

The parent packet (EXP-RUNTIME-38340133174, audit REVISE, verdict
ADOPT-AUDIT-REVISE-IMPLEMENTATION-BOUNDED-NEGATIVE) re-attested functional/locality
soundness of reuse-based localized repair (36/36 valid trials, repair_success 1.0,
guard_fire 1.0, write_set_max 1, contamination 0/144, literal-replay 0.0) but measured
an as-implemented single-episode wall-clock deficit on both frozen timed boundaries at
both L (six ratios 1.0235-1.2463, all CI95 above 1.00, 35/36 paired signs). Audit AF-6
localized the entire deficit to a removable harness artifact: v2 `Arm.__init__`
performs one full JSONL read+rewrite (`upsert`) per inherited mechanism — 5 for the
reuse arm vs 1 for the cold arm (39.2x in S-REGISTRY-BUILD medians) — and equalizing
only that phase from packet-raw medians flips all six gated ratios below 1.00 (a
decomposition diagnostic, NOT a measurement). The verdict therefore records NO
re-admission and NO permanent drop. This experiment removes the tax BY MEASUREMENT
and forces the terminal decision: SUPPORTS re-admits localized repair to the
C-PRODUCT-ECON story; a robust persistent deficit makes the drop permanent (mandate
stop trigger); a near-1.00 straddle parks the thread (INCONCLUSIVE, neither).
Non-degeneracy note (parent lesson): shipped-counter-only deciding is structurally
reuse-positive (deterministic 17/18, 17/19 by arm protocol) and scaffold-unit deciding
is structurally reuse-negative under an arbitrary 1:1 weight choice, so the shipped
premise PLUS the dual-boundary CI-gated latency decider is the unique non-degenerate
structure. The defensive shipped-deficit path is retained for classifier totality;
PRICED-DEFICIT remains reachable via robust latency LOSS, so no decision branch is empty.

## 2. Claim, hypothesis, falsifier

Claim: C-DELTA-REPAIR (status EXPERIMENTAL; runtime co-owns it in the lane registry).
H1 (functional/locality, re-attested): per class, repair_success >= 0.80 AND
Wilson lower >= 0.60 AND contamination <= 0.10 (48 in-support unaffected probes) AND
write_set_max <= 1 AND guard_fire >= 0.80.
H2 (shipped counter, deterministic drift-checked premise): reuse ships exactly 17
units vs cold 18 (L=2) / 19 (L=3) by arm protocol on functional_ok trials; checked as
V-DRIFT-COLD + V-DRIFT-REUSE + reported V-EQ-HOLDS; zero empirical variance by
construction; never claimed as an empirical win (parent AF-3 lesson).
H3 (latency, empirical decider): on all 12 cells (3 classes x L=2/L=3 x
inclusive/NOARG), median reuse/cold ratio < 1.00 with the Bonferroni family-wise
bootstrap CI (1-0.05/12, B=10000) strictly below 1.00.
H4 (scaling, descriptive only): breadth medians at n=1,2,5 and derived N* crossovers.
H5 (B3): model_calls/model_tokens structural zeros; real model economics UNSATISFIABLE
here (mandate-authorized counters-only pricing, blocker recorded).
H6 (treatment identity): bulk registry content == upsert content exactly (V-REG-EQUIV).
Falsifier: any robust LOSS cell (R >= 1.00 with BFCI_lower >= 1.00, valid gates) ->
PERMANENT-DROP-BOUNDED. Broken H1 -> FALSIFIES-FUNCTIONAL (bounded, no drop).
Any MARGINAL-without-LOSS, any UNKNOWN, or any tripped validity gate ->
INCONCLUSIVE / MEASUREMENT_INVALID (never a negative, never a drop, never re-admit).
H4 diagnostics and the attribution tie set can never flip the gated decision.

## 3. Measurement prerequisites (all verified at DESIGN, §15)

Python 3.12.15 stdlib-only. Carrier byte-identical to the parent freeze
(kernel.py 3a6caf97, models.py 338aaf4d, registry.py 51fb440d, __init__.py 3d173722;
the last closes parent audit RF-8). Parent v2 module pinned (60855 bytes, d4871091;
all 30+ v2 attributes used by the v5 driver verified present by name check).
Fresh seeds SEED5=162073685 with disjoint offsets (scored +1000*(ci+1)+j; NC +1/+2;
bootstrap +7000*(ci+1)+k; DESIGN canaries on discarded offsets). DESIGN liveness:
server/distill/resolve-EXECUTABLE/fetch-200/verify-True/guard-silent/registry-RW
booleans (unperturbed, discarded), synthetic repair-signal probe (patched True on
P1/P2/P3), BulkArm-vs-upsert byte-equality canary (discrete content compare, untimed),
timer resolution 1ns, instrumented cold-episode smoke (phase keys present, closure
finite). No timed reuse-vs-cold comparison is run at DESIGN. Warmup non-interference
by inspection (read-only GET server, no POST handler, set_perturb never called by
trial arms, pure guard) enforced per trial by V-RETAIN. No external bank, dataset,
fixture, model endpoint, browser, or network required.

## 4. Treatment, comparator, breadth, recurrence

Substrate: parent-identical in-process localhost ThreadingHTTPServer JSON API with
5 resources (users/posts/comments/albums/photos), 3 LOCAL perturbation classes
(P1-ENDPOINT/P2-STRUCTURE/P3-PERMISSION), rotating targets, TRIALS_PER_CLASS=12,
LEARN_IDS=[11,12,13], LEARN_IDS_MIN=[11,12], TASK_IDS=[14,15,16,17,18], in-support
probe id 14. Shipped parameterized carrier held fixed (no kernel/registry change).
Comparator B-COLD/B-COLD-MIN: parent-identical v2.Arm path (0 upserts at build, 1
upsert after distill), timed in parity order (6 reuse-first/6 cold-first per class).
Treatment T-REPAIR-REUSE-BULK: identical episode semantics to v2.run_repair_reuse
(fused freshness probe, one repair_attempts, one post-repair verify, execute
TASK_IDS[1:]) except S-REGISTRY-BUILD constructs BulkArm — ONE
MechanismRegistry.replace() of the inherited set instead of N sequential
upsert() read+rewrite cycles. Gated breadth n=5 (full set). Diagnostic breadths n=2
(target + first sorted other) and n=1 (target-only registration: the mandate's
second authorized repair, measured here as a diagnostic) run the identical episode on
deterministic subsets AFTER the gated triple in j-parity-rotated order; S-ARG still
deepcopies the full dict on every episode, so breadth scaling isolates to
S-REGISTRY-BUILD by construction. Recurrence: per-trial learning cost t_learn_s
(make_mech_dicts, untimed, outside the episode window in both arms) is timed as a
diagnostic; N* = learn_med/(cold_med - reuse_med) per class/L/boundary, null when
the denominator is <= 0 (never amortizes). Sequence-equivalence map (timed reuse):
S-ARG deepcopy -> S-REGISTRY-BUILD BulkArm(n) -> S-REGISTRY-SCAN target_mech ->
S-PROBE resolve+fetch -> S-GUARD -> S-REPAIR-SIGNAL local_repair ->
S-REGISTRY-WRITE upsert(patched, the single repaired target) -> S-CHARGE ->
S-POST-VERIFY -> S-EXECUTE batch. Charging semantics live entirely in pinned
v2/carrier code the driver calls but never reimplements.

## 5. Metrics (stable identities for downstream transmission)

Per class (n=12): M-REPAIR-SUCCESS, M-REPAIR-SUCCESS-WILSON-LOWER, M-CONTAMINATION-RATE
(denominator 48; 144 total), M-WRITE-SET-MAX, M-GUARD-FIRE-RATE, M-COLD-SUCCESS,
M-LITERAL-SUCCESS, M-NOREPAIR-SUCCESS (diagnostic; vacuity disclosed), M-BASE-LIVENESS,
M-OVERBROAD-CONTAMINATION-N, M-SHIPPED-REUSE/COLD-L2/COLD-L3 (+RATIOs, +HTTP splits),
M-COST-FETCH-RATIO-L3, M-EQUIV-MATCH-N/M-EQUIV-MATCH-DEN (raw identifiers; no
synthetic key), M-SCAFFOLD-REUSE/COLD-L3 (+M-SP5-RATIO-L2/L3 informational, excluded
from the classifier), M-LATENCY-{REUSE,COLD-L2,COLD-L3}-MED-S, M-LATENCY-R-L2/L3 with
M-LATENCY-R-L2/L3-CI95 (diagnostic, B=2000) and M-LATENCY-R-L2/L3-CIBF (gated,
Bonferroni 1-0.05/12, B=10000), M-LATENCY-R-L2/L3-NOARG with matching NOARG CIs,
M-LATENCY-SIGN-REUSE-SLOWER-L3, M-PHASE-DELTAS, M-CLOSURE-REUSE/COLD-MED,
M-MODEL-CALLS/TOKENS (structural zeros), M-N, M-CELL-L2/L2NA/L3/L3NA
(WIN/LOSS/MARGINAL/UNKNOWN), M-BREADTH-{1,2}-{MED-S,R-L3,R-L3-NOARG,N-OK} (diagnostic),
M-T-LEARN-MED-S, M-RECURRENCE-N-STAR-{L2,L2NA,L3,L3NA} (diagnostic, null if never),
M-SHIPPED sums, V-DRIFT-COLD-HOLDS, V-DRIFT-REUSE-HOLDS, V-EQ-HOLDS. Totals:
M-MODEL-CALLS-TOTAL/M-MODEL-TOKENS-TOTAL (=0), M-N-VALID-TRIALS (=36).
Attribution (diagnostic, tie set): excess_med_s, phase_deltas_med_s, shares_of_excess,
votes_ge_half, closure_ok, attribution_set (ALL phases clearing >= 0.50 on >= 2/3
classes), answer (single ATTRIBUTED-X, TIE-A+B, UNATTRIBUTED, ATTRIBUTION-MOOT,
ATTRIBUTION-INVALID). Net-vs-gross semantics preregistered: the denominator is the
NET median episode gap (reuse minus cold, net of cold-side savings such as
S-DISCOVERY/S-OBSERVE/S-DISTILL); shares may therefore exceed 1.0 and are
non-decomposable; gross reuse-phase medians are reported alongside; the single value
is never determined by driver iteration order (parent RF-2/AF-5 remedy).

## 6. Controls

PC-BASE-LIVENESS (scored in every trial; DESIGN basis in spec). B-LITERAL-REPLAY
(live must-fail; V4). B-NO-REPAIR (abstention; gate vacuous by pinned-v2
construction — success hardcoded False — disclosed; only the 36/36 guard-fired
diagnostic is informative; live must-fail role held by B-LITERAL-REPLAY; parent RF-9
remedy). NC-NO-PERTURBATION + NC-NOISE (must-silent) + 36 per-trial fresh-silence
probes (pooled specificity) + NC-OVERBROAD-REPAIR (must-fire > 0.10; parent 4/4;
re-fired at DESIGN). V-CLOSURE (attribution-only). V-REG-EQUIV (content pin, all
breadth episodes; DESIGN byte-equality canary). V-DRIFT-COLD (repair-independent
cold nominals 216/228 + http 96/108). V-DRIFT-REUSE (successful-repaired reuse
trials ship exactly 17 with class http 6/5/6; genuine repair failures exempt).
V-RETAIN (post-warmup retention re-check per trial). V-TIMING (2 warmups, 6/6 parity,
finite positive latencies, dual boundaries). V-EQUIV (warmup original-function vs
bulk-timed discrete projections, recorded for audit). No control is given the
treatment answer; ground truth (perturbed=stale by runner construction;
fresh=silent by pre-perturbation read) is independent of the guard verdict. Failure
policy INVALID-not-negative throughout.

## 7. Validity threats and representation loss

Localhost ThreadingHTTPServer vantage only: the whole parent excess (0.21-0.75ms)
was sub-one-local-GET and 2-3 orders below real navigation economics — no transfer
of ratios to real web/browser/production/external-agent economics is licensed (parent
AF-8). Simplified JSON API, not real websites. h(N)=1 in the timed window with
learning cost outside it in both arms; recurrence is a derived N*, not a measured
amortization. B3 model economics structurally zero (blocker recorded, not a result).
Multiplicity is handled by Bonferroni family-wise CIs for gating (12 cells); 95%
CIs are reported uncorrected as diagnostics. Bootstrap tail Monte Carlo noise at
B_BONF=10000 (~21 samples per 0.0021 tail) is frozen by pinned bootstrap seeds, hence
deterministic for this packet; audit may recompute. S-ARG operand asymmetry
(reuse deepcopies the full dict, cold {}) is disclosed and neutralized by requiring
wins on BOTH boundaries. Breadth composition (which non-target mechs fill n=2) is
fixed deterministic, not swept. Order effects across the 5 timed episodes are
controlled by gated-triple parity plus recorded rotated diagnostic order; residual
order influence is second-order on a read-only server and inspectable via
order-split medians in the raw trials.

## 8. Decision rule (frozen; pure functions cost_verdict_v5 / aggregate_v5)

Per class c, TRIALS_PER_CLASS=12 valid trials. functional_ok per §2 bars. For each of
12 cells (class x L x boundary): R and BFCI per §5. Cell: UNKNOWN if R/BFCI missing;
WIN if R < 1.00 AND BFCI_upper < 1.00; LOSS if R >= 1.00 AND BFCI_lower >= 1.00; else
MARGINAL. Class (first match): FUNCTIONAL-FAIL if !functional_ok; COST-UNKNOWN if
any UNKNOWN; PRICED-DEFICIT if any LOSS; PRICED-WIN if all WIN; else PRICED-MARGINAL.
Aggregate (first match): FALSIFIES-FUNCTIONAL if any FUNCTIONAL-FAIL; INCONCLUSIVE
if any COST-UNKNOWN; PERMANENT-DROP-BOUNDED if any PRICED-DEFICIT; SUPPORTS if all
PRICED-WIN; else INCONCLUSIVE (marginal straddle). Any tripped validity gate ->
MEASUREMENT_INVALID (status; outcome INCONCLUSIVE). 1.00 is never a win. DROP
requires a ROBUST deficit (this is the parent RF-10 remedy: CIs gate both
directions, so a single near-1.00 point estimate can no longer convert to a
permanent drop; straddles park). Outcome mapping: SUPPORTS->SUPPORTS;
PERMANENT-DROP-BOUNDED->FALSIFIES; FALSIFIES-FUNCTIONAL->FALSIFIES;
INCONCLUSIVE->INCONCLUSIVE; MEASUREMENT_INVALID->INCONCLUSIVE(status INVALID).
Product mapping: SUPPORTS->re-admit (spec §product_consequence_positive);
PERMANENT-DROP-BOUNDED->permanent-bounded-drop-no-further-L-sweeps; else
no-decision-no-drop-no-readmit.

## 9. Design notes (deviations from the parent, all deliberate)

(a) Tax removed by measurement: v2.Arm per-mech upserts -> BulkArm single replace()
(same shipped API; content pinned identical by V-REG-EQUIV + DESIGN byte canary).
Cold path parent-identical (v2.Arm), so V-DRIFT-COLD stays cross-packet comparable.
(b) Dropped T-REPAIR-CONSERVATIVE/T-REPAIR-LEGACY scored arms and the V13 replication
premise (legacy regression 1.1111 at L2 stands established per parent AF-2; smallest
decisive batch per mandate). (c) Dropped the B11 certificate track (held-out probes,
certificate metrics): the runtime instance stands certified per parent audit AF-11;
guard wiring is re-attested via fresh-silence + NCs; the mandate's smallest batch is
L=2/L=3 on both timed boundaries only. (d) New breadth (n=1,2 diagnostic episodes)
and recurrence (t_learn_s + N*) diagnostics answer the mandate scaling question
without gating power. (e) CI-gated cells with Bonferroni family-wise error control;
NOARG CIs added (parent gated NOARG point estimates without CIs). (f) All
`(m or default)` gate idioms replaced by explicit is-None checks (parent RF-6), with
dedicated 0.0/0.10 boundary coverage in the reachability probe (parent RF-7).
(g) Attribution reports the tie SET with preregistered net-vs-gross semantics
(parent RF-2). (h) Contamination denominator 48/class, 144 total; raw metric
identifiers preserved with no nulls and no synthetic keys (parent RF-3/RF-4/RF-5).
(i) Freeze set gains src/spider/__init__.py (parent RF-8). (j) B-NO-REPAIR vacuity
disclosed, live must-fail role assigned to B-LITERAL-REPLAY (parent RF-9).
(k) Fresh SEED5 bank (independent measurement, not a re-run of the same seeds).

## 10. Freeze binding and driver extraction

Freeze artifacts (5 file paths; hashed into freeze.json.artifact_hashes):
src/spider/__init__.py, src/spider/kernel.py, src/spider/models.py,
src/spider/registry.py,
research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py.
The v5 driver has no file identity until EXECUTE extracts it; it is bound stronger by
content: embedded verbatim in section-12 between the marker lines
`# === V5-DRIVER-BEGIN ===` and `# === V5-DRIVER-END ===`, pinned by
CANONICAL-RUNNER-V5-SHA256 = "b6db1effc40bac0357d30dab546d9ef98bc3570b998998486c6409a6c96b10b1" (sha256 over the
canonical bytes defined below). Extraction algorithm (frozen; also implemented
as the driver's V1 runtime check): split this prereg.md into lines; find the
first line that EXACTLY equals the BEGIN marker line and the first subsequent
line that EXACTLY equals the END marker line; the driver is the lines strictly
between them joined with "\n" (no trailing newline added). Canonical bytes for
hashing: the extracted driver text with the single self-referential assignment
line starting `CANONICAL_RUNNER_V5_SHA256 = "` replaced by the fixed placeholder
line `CANONICAL_RUNNER_V5_SHA256 = "<PINNED>"` (this closes the fixed point: the
constant's value cannot affect its own digest). Line-exact matching is
load-bearing: prose and code references to the markers always sit inside longer
lines and therefore never collide with the standalone marker lines. The V1 check
recomputes sha256 over the canonical bytes and refuses to run on mismatch; the
V0 check refuses when the parent v2 module differs in bytes or sha. EXECUTE runs
the extracted driver only. The python fence around section-12 is presentational.

## 11. Product consequences

SUPPORTS: re-admit localized repair to the C-PRODUCT-ECON story with honest
denominators (shipped unit counter + dual-boundary family-wise latency + breadth /
recurrence scaling + tie-set attribution); no code promotion (runtime lane; carrier
byte-identical); B3 blocker recorded. PERMANENT-DROP-BOUNDED: permanent bounded drop
from the C-PRODUCT-ECON story on this substrate/carrier/classes/counter, no further
L-sweeps, thread stopped (mandate stop trigger — licensed here because the known
removable tax was removed by measurement). FALSIFIES-FUNCTIONAL: bounded mechanism
concern, no re-admit, no drop. INCONCLUSIVE / MEASUREMENT_INVALID: park; no
re-admit, no drop, no promotion. C-DELTA-REPAIR stays EXPERIMENTAL bounded to
functional/locality soundness in every branch except FALSIFIES-FUNCTIONAL.

## 12. Frozen driver (v5; executable; content-bound by §10)

```python
# === V5-DRIVER-BEGIN ===
#!/usr/bin/env python3
# FROZEN RUNNER v5 for EXP-RUNTIME-38816779349 (runtime, design_contract_version 2).
# C-DELTA-REPAIR repair-gated re-test: bulk-materialized localized repair vs cold
# re-derivation at L=2/L=3 on both timed boundaries + breadth/recurrence diagnostics.
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

EXP_ID5 = "EXP-RUNTIME-38816779349"
SEED5 = 162073685  # 38816779349 % 2**32 (fresh; parent SEED4=3980394806 disjoint)
V2_PIN_SHA = "d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608"
V2_PIN_BYTES = 60855
B_LAT = 2000
B_BONF = 10000
N_CELLS = 12
ALPHA_FAMILY = 0.05
BREADTHS_DIAG = (1, 2)
CLOSURE_BAR = 0.20
ATTRIB_SHARE = 0.50
FETCH_BAR = 0.90
NOMINAL = {"reuse_sum": 17, "cold_l2_sum": 18, "cold_l3_sum": 19,
           "cold_l2_http": 8, "cold_l3_http": 9}
REUSE_HTTP_EXPECTED = {"P1-ENDPOINT": 6, "P2-STRUCTURE": 5, "P3-PERMISSION": 6}
CANONICAL_RUNNER_V5_SHA256 = "b6db1effc40bac0357d30dab546d9ef98bc3570b998998486c6409a6c96b10b1"


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here.parent, *here.parents):
        if (p / "src" / "spider" / "kernel.py").is_file():
            return p
    return Path("/home/runner/work/Spider/Spider")


REPO = _repo_root()
V2_PATH = REPO / "research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py"
PREREG_PATH = REPO / "research/experiments/EXP-RUNTIME-38816779349/prereg.md"


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
    start = next(i for i, l in enumerate(lines) if l == "# === V5-DRIVER-BEGIN ===")
    end = next(i for i, l in enumerate(lines[start + 1:], start + 1)
               if l == "# === V5-DRIVER-END ===")
    return "\n".join(lines[start + 1:end])


def _canonical_bytes(driver):
    """Normalize the single self-referential hash constant before hashing.

    The CANONICAL_RUNNER_V5_SHA256 assignment line is part of the embedded text,
    so hashing raw bytes would be circular. Both DESIGN finalization and the V1
    runtime check hash the text with that one line replaced by a fixed
    placeholder; the constant's value therefore cannot affect the digest, and a
    single assignment closes the fixed point.
    """
    out = []
    for line in driver.split("\n"):
        if line.startswith('CANONICAL_RUNNER_V5_SHA256 = "'):
            out.append('CANONICAL_RUNNER_V5_SHA256 = "<PINNED>"')
        else:
            out.append(line)
    return "\n".join(out).encode("utf-8")


def _check_v1_binding():
    driver = _extract_driver(PREREG_PATH.read_text(encoding="utf-8"))
    digest = hashlib.sha256(_canonical_bytes(driver)).hexdigest()
    if digest != CANONICAL_RUNNER_V5_SHA256:
        raise SystemExit("V1-FREEZE-BINDING failure: embedded driver hash mismatch; refusing to run.")
    return digest


v2 = _load_v2()

CLASSES = v2.CLASSES
TARGETS = v2.TARGETS
TRIALS_PER_CLASS = v2.TRIALS_PER_CLASS
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


def run_trial_v5(cls, target, seed, j):
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
                b2 = _timed_episode(run_reuse_episode_bulk, app, app.origin,
                                    copy.deepcopy(mechs), cached[target], target, 2, "bulkb2")
                b1 = _timed_episode(run_reuse_episode_bulk, app, app.origin,
                                    copy.deepcopy(mechs), cached[target], target, 1, "bulkb1")
                order = ["R5", "C2", "C3", "B2", "B1"]
            else:
                c3 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS, "cold")
                c2 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS_MIN, "coldmin")
                rep = _timed_episode(run_reuse_episode_bulk, app, app.origin,
                                     copy.deepcopy(mechs), cached[target], target, 5, "bulk5")
                b1 = _timed_episode(run_reuse_episode_bulk, app, app.origin,
                                    copy.deepcopy(mechs), cached[target], target, 1, "bulkb1")
                b2 = _timed_episode(run_reuse_episode_bulk, app, app.origin,
                                    copy.deepcopy(mechs), cached[target], target, 2, "bulkb2")
                order = ["C3", "C2", "R5", "B1", "B2"]
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

        def _brief(ep):
            return {"ok": bool(ep.get("ok")), "reason": ep.get("reason"),
                    "t_s": ep.get("episode_s"), "misc_s": ep.get("misc_s"),
                    "phases": ep.get("phases"), "scaffold": ep.get("scaffold"),
                    "reg_equiv": bool(ep.get("reg_equiv")),
                    "shipped": _shipped_sum(_arm_counters(ep["arm"])) if "arm" in ep else None}

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
            "breadth_b2": _brief(b2), "breadth_b1": _brief(b1),
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


def cost_verdict_v5(m):
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


def aggregate_v5(cvs):
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


def synthetic_reachability_probe_v5():
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
    verdicts = {k: cost_verdict_v5(v) for k, v in cases.items()}
    aggregates = {
        "SUPPORTS": aggregate_v5(["PRICED-WIN"] * 3),
        "PERMANENT-DROP-BOUNDED": aggregate_v5(["PRICED-WIN", "PRICED-DEFICIT",
                                                "PRICED-WIN"]),
        "FALSIFIES-FUNCTIONAL": aggregate_v5(["PRICED-WIN", "FUNCTIONAL-FAIL",
                                              "PRICED-WIN"]),
        "INCONCLUSIVE-unknown": aggregate_v5(["PRICED-WIN", "COST-UNKNOWN",
                                              "PRICED-DEFICIT"]),
        "INCONCLUSIVE-marginal": aggregate_v5(["PRICED-WIN", "PRICED-MARGINAL",
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


def synthetic_gate_coverage_probe_v5():
    """Drive the frozen gate block at pass/fail INCLUDING 0.0/0.10 boundaries.

    Remedy for parent audit RF-6/RF-7: proves the explicit is-None checks classify
    legitimately observed 0.0 values correctly (they pass upper-bound gates) and
    trip exactly above the bars.
    """
    base_rows = [_synth_trial_row() for _ in range(12)]
    for i, r in enumerate(base_rows):
        r["order_rep_first"] = (i % 2 == 0)
    out = {}
    m = _per_class_metrics_v5("P1-ENDPOINT", base_rows, SEED5 + 70001)
    out["all-pass-0.0-boundaries"] = {"gates": class_gate_reasons("P1-ENDPOINT", base_rows, m),
                                      "literal": m["M-LITERAL-SUCCESS"],
                                      "norepair": m["M-NOREPAIR-SUCCESS"],
                                      "guard": m["M-GUARD-FIRE-RATE"],
                                      "contam": m["M-CONTAMINATION-RATE"]}
    mut = {
        "literal-0.11-trips": [_mutrow(literal_success=True)
                               for _ in range(2)],
        "cold-0.89-trips": [_mutrow(cold_success=False, cold_min_success=False)
                            for _ in range(2)],
        "norepair-0.11-trips": [_mutrow(norepair_success=True)
                                for _ in range(2)],
        "guard-0.79-trips": [_mutrow(repair_guard_fired=False)
                             for _ in range(3)],
        "contam-5of48-trips": [_mutrow(contamination_n=1)
                               for _ in range(5)],
        "write-2-trips": [_mutrow(write_set_n=2)
                          for _ in range(1)],
        "overbroad-0.09-trips": [_mutrow(overbroad_contamination_n=0.09)
                                 for _ in range(12)],
        "overbroad-0.11-passes": [_mutrow(overbroad_contamination_n=0.11)
                                  for _ in range(12)],
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
        m = _per_class_metrics_v5("P1-ENDPOINT", rows, SEED5 + 70002)
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
def _per_class_metrics_v5(cls, rows, seed_base):
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
    for breadth, bkey in ((2, "breadth_b2"), (1, "breadth_b1")):
        bt = [r[bkey]["t_s"] for r in rows
              if isinstance(r.get(bkey), dict) and r[bkey].get("ok")
              and r[bkey].get("t_s") is not None]
        bn = len(bt)
        bmed = _median(bt)
        m[f"M-BREADTH-{breadth}-N-OK"] = bn
        m[f"M-BREADTH-{breadth}-MED-S"] = bmed
        m[f"M-BREADTH-{breadth}-R-L3"] = ((bmed / med_c3)
            if (bmed is not None and med_c3) else None)
        bna = [r[bkey]["t_s"] - ((r[bkey].get("phases") or {}).get("S-ARG", 0.0))
               for r in rows
               if isinstance(r.get(bkey), dict) and r[bkey].get("ok")
               and r[bkey].get("t_s") is not None]
        bnamed = _median(bna)
        m[f"M-BREADTH-{breadth}-R-L3-NOARG"] = ((bnamed / med_nac3)
            if (bnamed is not None and med_nac3) else None)
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


def _attribution_v5(per_class):
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
        out = {"status": "V5-REACHABILITY-PROBE", "experiment_id": EXP_ID5,
               "lane": "runtime", "runner_self_sha": runner_self_sha,
               "decision_rule": synthetic_reachability_probe_v5(),
               "gate_coverage": synthetic_gate_coverage_probe_v5(),
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
                b1 = BulkArm(_breadth_subset(copy.deepcopy(mechs), "users", 1),
                             Path("/tmp"), "livebulk1")
                b1_ids = sorted(m.mechanism_id for m in b1.registry.all())
                up_ids = sorted(m.mechanism_id for m in up.registry.all())
                tgt = up.target_mech("users")
                bulk_target_only_ok = (len(b1_ids) == 1 and b1_ids[0] == tgt.mechanism_id
                                       and b1_ids[0] in up_ids)
                ep = run_cold_episode(app, app.origin, "users", v2.LEARN_IDS_MIN,
                                      "livecold")
                phase_keys = sorted((ep.get("phases") or {}).keys())
                ep_s = ep.get("episode_s") or 0.0
                closure_finite = (math.isfinite(ep_s) and ep_s > 0
                                  and math.isfinite(ep.get("misc_s") or float("nan")))
            np_t = v2.no_perturbation_trial(SEED5 + 1) if ready else {"stale": None}
            nz_t = v2.noise_trial(SEED5 + 2) if ready else {"stale": None}
        finally:
            app.stop()
        print(json.dumps({"status": "V5-LIVENESS-ONLY", "experiment_id": EXP_ID5,
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
            r = run_trial_v5(cls, TARGETS[ci % len(TARGETS)], SEED5 + 91000 + ci, ci)
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
        np_t = v2.no_perturbation_trial(SEED5 + 1)
        nz_t = v2.noise_trial(SEED5 + 2)
        print(json.dumps({"status": "V5-MECHANICS-ONLY", "experiment_id": EXP_ID5,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "seed": SEED5, "carrier": carrier,
                          "canary": canary, "nc_no_perturbation": np_t,
                          "nc_noise": nz_t}, indent=2))
        return

    _check_v1_binding()
    trials = []
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial_v5(cls, target, SEED5 + 1000 * (ci + 1) + j, j))
    np_t = v2.no_perturbation_trial(SEED5 + 1)
    nz_t = v2.noise_trial(SEED5 + 2)

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
        m = _per_class_metrics_v5(cls, rows, SEED5 + 7000 * (ci + 1))
        invalid.extend(class_gate_reasons(cls, rows, m))
        m["V-DRIFT-COLD-HOLDS"] = not any("V-DRIFT-COLD" in v for v in invalid if v.startswith(cls))
        m["V-DRIFT-REUSE-HOLDS"] = not any("V-DRIFT-REUSE" in v for v in invalid if v.startswith(cls))
        eq = (m["M-SHIPPED-RATIO-L2"] is not None and m["M-SHIPPED-RATIO-L3"] is not None
              and m["M-SHIPPED-RATIO-L2"] < 1.0 and m["M-SHIPPED-RATIO-L3"] < 1.0
              and m.get("M-COST-FETCH-RATIO-L3") is not None
              and m["M-COST-FETCH-RATIO-L3"] <= FETCH_BAR)
        m["V-EQ-HOLDS"] = bool(eq)
        per_class[cls] = m

    attribution = _attribution_v5(per_class) if per_class else {"answer": "ATTRIBUTION-INVALID",
                                                                "attribution_set": [],
                                                                "closure_ok": False}
    class_verdicts = {cls: cost_verdict_v5(m) for cls, m in per_class.items()}
    if invalid:
        decision, outcome, status = "MEASUREMENT_INVALID", "INCONCLUSIVE", "MEASUREMENT_INVALID"
    elif any(v == "FUNCTIONAL-FAIL" for v in class_verdicts.values()):
        decision, outcome, status = "FALSIFIES-FUNCTIONAL", "FALSIFIES", "COMPLETE"
    elif any(v == "COST-UNKNOWN" for v in class_verdicts.values()):
        decision, outcome, status = "INCONCLUSIVE", "INCONCLUSIVE", "COMPLETE"
    else:
        agg = aggregate_v5(list(class_verdicts.values()))
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
           "experiment_id": EXP_ID5, "lane": "runtime",
           "runner_self_sha": runner_self_sha, "seed": SEED5,
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
# === V5-DRIVER-END ===
```

## 13. Pre-2.0 comparison (non-duplication record)

Screened `codex/legacy_brief.json` (7 findings), `codex/legacy_artifact_index.json`
(1401 artifacts, subject search on delta/repair/reuse), and `codex/claim_state.json`
(C-DELTA-REPAIR precedents). Pre-2.0 repair-bearing artifacts found: graph
cycle3/fused REPAIR recounts (artifacts 28/31), runtime R0/R1/R2 repair rounds
(artifacts 598/599/604), frontier-scoped-delta-repair capsules and probes
(artifacts 528/529/637), intel repair reproductions (artifacts 245/290/291/436-469).
All sit on DIFFERENT substrates (historical capsule/procedure stores, form-login
procedures, taglove snapshots, graph robustness banks) with DIFFERENT treatments
(no parameterized-carrier reuse-vs-cold comparison), DIFFERENT comparators, and
UNTRUSTED verdict tokens (navigation metadata only; several rounds
REVISE/REJECTED/FAIL). None tested reuse-based localized repair vs cold
re-derivation at L=2/L=3 on a fetch-scarce perturbable substrate with the shipped
parameterized carrier, contamination bounds, and dual timed boundaries — and none
tested the no-tax (bulk/target-only) counterfactual at all. Classification:
LEGACY: DISTINCT_EXTENSION (new independent test on a different substrate with
repaired validity: explicit gate idiom, family-wise CIs, content-pinned bulk
materialization, correct contamination denominator). Cited artifact SHAs live in the
legacy index entries above; the frozen archive blob is
9bb76113aeaf46d9aecdd8a38349a3a7741e57c3 (per codex/legacy_brief.json). This design
never repeats an identical invalid/degenerate design: the parent packet's six
degeneracies (RF-1 ceiling overstatement, RF-2 single-component attribution,
RF-3/RF-4 metric nulls/renames, RF-5 denominator miscount, RF-6/RF-7 gate defect and
coverage gap, RF-8 unbound __init__.py, RF-9 vacuous control, RF-10 CI asymmetry) are
each structurally closed in §§5/6/8/10 above. Research 2.0 continuity: reuses the
accepted R2 packets EXP-RUNTIME-38244432934 (v2 module, frozen) and
EXP-RUNTIME-38340133174 (bank construction, nominal vectors, functional bars) by
exact immutable reference, with fresh SEED5 seeds making this an independent
measurement rather than a re-run.

## 14. Pre-freeze self-attack (satisfiability)

E1 empty branches: the pure classifier + gate block were driven with synthetic rows
at DESIGN (§15): all 5 class branches and all 4 aggregates plus MEASUREMENT_INVALID
produce; no branch is empty. E2 treatment/comparator identity: BulkArm changes only
the write pattern (1 replace vs N upserts) with byte-identical content (canary §15);
cold path is parent-identical; the gated comparison differs in physical
resolve/fetch/verify/scaffold counts plus wall-clock — never identical. E3 ceiling
baselines: cold latency is continuous (no ceiling); 1.0 success levels are
functional gates, never deciders; the 12 deciders have live dynamic range (1ns
timer vs 0.2-0.9ms parent gaps). E4 insensitive controls: literal-replay must-fail
live (parent 0.0, re-verified bitten at DESIGN via mechanics canary discrete fields
only); overbroad fires 4/4 in the parent and is re-fired at DESIGN; NCs silent;
guard fires 36/36 expected; B-NO-REPAIR vacuity is disclosed and never load-bearing.
E5 missing prerequisites: none — §3 all verified (§15). E6 unbound mutables: the 5
freeze paths plus the content-bound driver exhaust the import closure
(stdlib + pinned v2); no bank/dataset/fixture is read. E7 arithmetic: Bonferroni
1-0.05/12 CIs with B=10000 are computable from n=12 (tail ~21 samples/side, frozen
seeds => deterministic); strict inequalities partition every cell into exactly one
of WIN/LOSS/MARGINAL/UNKNOWN. E8 scope discipline: DESIGN ran no outcome-bearing
measurement — no timed reuse-vs-cold comparison exists anywhere in §15 evidence;
the only timed episode at DESIGN is a single cold-arm smoke with no comparator.

## 15. DESIGN probe evidence (cheap, non-outcome-bearing)

Reachability probe (pure synthetic): all class branches
{PRICED-WIN, PRICED-DEFICIT, PRICED-MARGINAL, FUNCTIONAL-FAIL, COST-UNKNOWN} and all
aggregates {SUPPORTS, PERMANENT-DROP-BOUNDED, FALSIFIES-FUNCTIONAL, INCONCLUSIVE}
(via UNKNOWN and via MARGINAL paths) reachable; boundary rows confirm R=1.00 with a
straddling CI -> MARGINAL in both directions (never a win; LOSS needs R>=1.00 with
CI_lo>=1.00, demonstrated by the 1.10 case); gate-coverage rows confirm 0.0 passes
upper-bound gates (literal 0.0, norepair 0.0, contam 0.0) while 0.11/0.79/5-of-48/
write-2/overbroad-0.09 trip exactly the expected gate and overbroad-0.11 passes;
drift pins trip on a one-unit cold/reuse nominal deviation while a genuine
repair-failed trial with a deviant count stays exempt; parity and warmup violations
trip. Liveness (discarded, unperturbed): server_ready, distill_live, task_read_verified (EXECUTABLE/200/True),
contamination instrument live on in-support probe 14, out-of-support degenerate,
NC-NO-PERTURBATION/NC-NOISE silent, timer 1ns, cold-episode phase keys present with
finite closure, BulkArm-vs-upsert registry bytes byte-identical at n=5,
target-only (n=1) registry holds exactly the target mechanism. Full probe outputs
are reproduced by EXECUTE preflight from the frozen driver; the DESIGN runs above
are summarized here and carry no outcome information about reuse-vs-cold latency.






