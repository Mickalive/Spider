# EXP-RUNTIME-38340133174 preregistration — scaffolding-attributed terminal comparison with B11 certificate

- experiment_id: `EXP-RUNTIME-38340133174`
- lane: `runtime` (design_contract_version 2)
- target claim: `C-DELTA-REPAIR` (effective status EXPERIMENTAL; retain-or-bound only)
- director action: REOPEN (runtime IDLE reactivation on the single shared validity blocker)
- design status: PRE-FREEZE (DESIGN ONLY; no outcome-bearing measurement has been run)

## 1. Strategic question (binding director mandate, refined)

Which uncounted episode-scaffolding component accounts for the ~0.2–0.9ms reuse
latency excess, and under a shipped scaffolding-priced end-to-end counter
(`http_requests` + `retrieval_calls` + `verification_calls` + `repair_attempts`,
plus a measured probe-coverage certificate or runtime observation guard for the
B11 budget-sparse boundary as the second deliverable), is reuse-based localized
repair strictly cheaper than cold re-derivation at L=2 and L=3 — i.e. does the
SINGLE-SURFACE-MIXED split resolve toward re-admission or permanent drop from
the C-PRODUCT-ECON product story? If real model-call/token economics (B3)
remain unsatisfiable, price in counters only and record the blocker.

Refinement (no drift): the mandate names the counter fields and the two
deliverables. This design fixes them as: (D1) the shipped 4-field unit counter
(zero fitted quantities) plus the parity-controlled latency surface that prices
all scaffolding in wall-clock, plus an honest preregistered 5-field
scaffolding-inclusive sensitivity; (D2) a measured guard probe-coverage
certificate over the frozen perturbation bank. "Scaffolding-priced" is honored
by the pair: latency prices every scaffolding operation in time, the 5-field
sensitivity prices it in ops, and the phase attribution locates it. The
classifier decides on the shipped 4-field counter plus latency only, for the
reachability reason recorded in §9 (the 5-field unit counter is deterministically
reuse-negative on nominal vectors, so deciding on it would make SUPPORTS
arithmetically unreachable — a degenerate design; it is reported, not decided).

## 2. Inherited state (parent handoff EXP-RUNTIME-38291097112, sha 3139aa3b...)

Established (preserved, not re-litigated): measurement-valid MIXED-PARTIAL
transaction (audit PASS); functional/locality soundness 36/36; equal-weight
strict win reproduces (0.9444 L2 / 0.8947 L3); calibrated counted-op surface
favors reuse (0.61–0.78) while the only true end-to-end surface (latency)
disfavors it (R 1.05–1.25, 36/36 per-trial signs); surface divergence held open
as the finding; NOT re-admitted; permanent drop NOT self-executing (parent
AF-7 ambiguity adjudicated as drop-pending-scaffolding-complete-counter).

Rejected (bounded): STRICT-WIN-MEASURED on this substrate/carrier/classes;
the 4-op calibrated counter as a complete end-to-end model; dissolution of
counter-dependence under product-correct accounting.

Unknown (this packet answers #1 fully, #2 terminally): (#1) which scaffolding
component accounts for the excess → §5 attribution; (#2) whether any justifiable
scaffolding-priced counter shows strict reuse win at L=2 AND L=3 → §8 terminal
rule; (#3) transfer off-substrate ( untouched, out of scope); (#4) B3 model
economics (unsatisfiable here → counters-only + recorded blocker, §7).

Do-not-assume (preserved): no end-to-end product win reading of any counted-op
win; no transfer beyond localhost; model zeros are structural, not findings;
P2-L3 CI margin carried, not overstated; contamination count, not rate; no L=4
claim; no conservative-arm superiority claim.

## 3. Substrate, carrier, pins (all verified at DESIGN, §10)

- Python 3.12 stdlib only; `ThreadingHTTPServer` on localhost ephemeral port.
- Carrier (byte-identical to parent freeze, re-verified 2026-10-14):
  `src/spider/kernel.py` 3a6caf970f5c86db19419f7ae57c7125f409eceba922eb2d5a9f5964140bb1b3,
  `src/spider/models.py` 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78,
  `src/spider/registry.py` 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c.
- Immutable substrate reference: parent v2 runner
  `research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py`
  (60855 bytes, sha256 d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608;
  V0 gate refuses on mismatch). The v4 driver calls its arm/substrate functions;
  it never reimplements them.
- Classes/targets/seeds: P1-ENDPOINT, P2-STRUCTURE, P3-PERMISSION × rotating
  TARGETS=[users,posts,comments], TRIALS_PER_CLASS=12, SEED4=3980394806
  (38340133174 mod 2**32), per-trial seed SEED4+1000*(ci+1)+j, parity
  rep_first=(j%2==0) → exactly 6/6 per class.
- No external task bank/dataset/fixture/model endpoint is read. B3 endpoint
  absent by construction.

## 4. Arms, shipped counter, scaffold units

Timed episodes (v4 inclusive boundary: arg deepcopy materialization + arm
execution; applied symmetrically; v3-exact boundary via S-ARG subtraction as
sensitivity): T-REPAIR-REUSE vs B-COLD (L=3) vs B-COLD-MIN (L=2), 2 excluded
warmups per trial, predeclared parity order. Untimed in-trial: T-REPAIR-CONSERVATIVE
and T-REPAIR-LEGACY sensitivities, B-LITERAL-REPLAY / B-NO-REPAIR mechanism
controls, contamination and write-set probes (outside timed sections, exactly as
parent v3). Baseline/treatment identifiers are frozen as in spec.json and reused
verbatim in result/audit transmission.

D1 decision counter (shipped, unit weights, zero fitted quantities): per-episode
sums of `http_requests + retrieval_calls + verification_calls + repair_attempts`
from the shipped `TrajectoryCounters` surface via the pinned `Arm` counters.
Per-class M-SHIPPED-RATIO-L2/L3 = reuse-sum / cold-sum (exact integer ratios).

Preregistered scaffold units (each = 1 `scaffold_op`, integer-counted at
instrumentation points in the v4 driver, never double-counted against shipped
fields): (S1) one arg-deepcopy materialization per timed episode; (S2) one per
`MechanismRegistry.upsert` in episode scope (reuse build = 5, cold build = 0,
post-repair/distill writes = 1); (S3) one per `registry.all()` full scan
(`target_mech`); (S4) one per `guard()` evaluation; (S5) one per
`local_repair()` signal evaluation; (S6) one per `distill_parameterized()`
invocation. Kernel resolve/verify/fetch/repair charges stay in shipped fields
only. The 5-field sensitivity M-SP5-RATIO-* = (shipped + scaffold) ratios,
informational, excluded from the classifier (§9 reason).

## 5. Attribution method (answers unknown #1; never gates the priced decision)

Preregistered phases (perf_counter deltas per timed episode; keys accumulate):
S-ARG, S-REGISTRY-BUILD, S-REGISTRY-SCAN, S-PROBE (fused first-task
resolve+fetch), S-GUARD (includes its verify), S-REPAIR-SIGNAL, S-REGISTRY-WRITE,
S-CHARGE, S-POST-VERIFY, S-EXECUTE, S-DISCOVERY, S-OBSERVE, S-DISTILL,
S-MISC (= episode − Σrecorded, residual). Components: REGISTRY =
BUILD+SCAN+WRITE; GUARD = PROBE+GUARD; plus REPAIR-SIGNAL, ARG, EXECUTE,
DISTILL/DISCOVERY/OBSERVE (cold-side), OTHER. Per class: phase-median deltas
reuse−coldL3; excess E = median episode gap. Closure gate V-CLOSURE: median
|S-MISC|/episode ≤ 0.20 per class. Component X ATTRIBUTED iff its median delta
≥ 0.50×E on ≥ 2/3 classes with closure holding; E ≤ 0 → ATTRIBUTION-MOOT;
closure failure → ATTRIBUTION-INVALID; else UNATTRIBUTED (honest unknown carried
forward). DESIGN smoke (single discarded N=1 trial) confirmed the instrument
executes and the registry-IO vs guard-compute asymmetry is measurable
(5-upsert+scan ≈1.6ms vs token probe ≈9µs) — instrument liveness only, no
outcome recorded.

## 6. Controls and validity gates

PC-BASE-LIVENESS in every scored trial (V12); B-LITERAL-REPLAY/B-NO-REPAIR
must-fail (V4/V6); NC-NO-PERTURBATION/NC-NOISE must-silent (V7);
NC-OVERBROAD-REPAIR live > 0.10 (V15); V0 pin; V1 freeze binding (v4 driver hash);
V2 isolation; V3 determinism-projection (counters/oplogs/flags deterministic;
latency wall-clock, not projected); V5 cold live; V8 leakage (write_set_max 1,
in-support contamination probe id 14); V9 integer counters; V10 not-fitted (no
calibration workload exists in v4 — the parent Stage-A fitter is deliberately
removed because its repair weight 0.000582 predetermined the win direction,
audit AF-3); V11 n=12 + 72 warmups; V13 legacy-regression premise (reported
caveat); V14 reuse identity (oplogs + phases); V-EQ reproduction premise
(deterministic shipped-counter eq holds every class; break = drift →
MEASUREMENT_INVALID, never a negative); V-TIMING parity/finite; V-CLOSURE and
V-CERT on independent tracks (§8).

## 7. B11 second deliverable: probe-coverage certificate (V-CERT track)

Bank (frozen, enumerated pre-run): the exact 36 scored perturbations
(class,target,seed) with ground truth stale=True (guard verdict recorded from
each reuse episode) + NC-NO-PERTURBATION and NC-NOISE with ground truth
stale=False. Metrics: M-CERT-SENSITIVITY (fire rate on stale),
M-CERT-SPECIFICITY (silence on fresh), M-CERT-COVERAGE (= sensitivity),
M-CERT-FALSE-ACCEPTS (exact stale-but-silent count). Residual boundary,
explicitly labeled: BND-REQUIRED-PATHS (DERIVED — perturbations outside
required_paths cannot fire the Jaccard guard by construction);
BND-THRESHOLD (DERIVED — within-envelope perturbations holding Jaccard ≥ 0.85
with verify-True cannot fire by construction); BND-PROBE-BUDGET (MEASURED —
single fused probe at TASK_IDS[0]=14 per episode; detection measured only
there). V-CERT: bank fully enumerated, each item scored exactly once with
verdict+truth recorded, boundary enumerated with measured-vs-derived labels;
failure invalidates only the certificate, never the priced decision. Schema
co-owned with product for B11; this packet measures the runtime instance, it
does not close product B11. B3: model_calls/model_tokens structurally 0 —
counters-only pricing with the blocker recorded (H5).

## 8. Decision rule (frozen pure classifier; synthetic reachability verified)

Per class (n=12): functional_ok (parent bars); eq/V-EQ (shipped reuse<cold at L2
AND L3, fetch_L3≤0.90); sp := M-SHIPPED-RATIO-L2<1.00 AND M-SHIPPED-RATIO-L3<1.00;
lw := M-LATENCY-R-L2<1.00 AND M-LATENCY-R-L3<1.00 (medians; B_LAT=2000 bootstrap
CIs reported alongside per-trial 12/12 sign patterns). Class first match:
FUNCTIONAL-FAIL / COST-UNKNOWN (any ratio None) / PRICED-WIN (sp AND lw) /
PRICED-DEFICIT. Aggregate first match: gate failure → MEASUREMENT_INVALID; any
COST-UNKNOWN → INCONCLUSIVE; any FUNCTIONAL-FAIL → FALSIFIES-FUNCTIONAL; all
PRICED-WIN → SUPPORTS (re-admit localized repair to C-PRODUCT-ECON with honest
denominators; no promotion; B3 blocker recorded); else → PERMANENT-DROP-BOUNDED
(mandate stop trigger: persistent split converts to permanent bounded drop from
the C-PRODUCT-ECON story, no further L-sweeps; C-DELTA-REPAIR stays
EXPERIMENTAL bounded to functional/locality soundness). Outcome mapping:
SUPPORTS→SUPPORTS, PERMANENT-DROP-BOUNDED→FALSIFIES (bounded product-story
drop, explicitly NOT a mechanism falsification), FALSIFIES-FUNCTIONAL→FALSIFIES
(bounded functional), MEASUREMENT_INVALID/INCONCLUSIVE→INCONCLUSIVE.
Attribution and certificate tracks resolve independently and never flip the
priced decision.

## 9. Satisfiability self-attack (DESIGN, pre-freeze; all branches live)

- Empty/unreachable branches: frozen pure classifier driven with synthetic rows
  at DESIGN — all 4 class branches and all 4 aggregates produced (all True);
  strict-inequality boundary tested (1.00 is NOT a win). Reachability probe
  re-runs inside the frozen driver (`--reachability-probe`, pure, no substrate).
- Arithmetic impossibility: nominal-vector arithmetic at DESIGN showed the
  5-field unit counter deterministically reuse-negative (≈27–28 vs 21–22) →
  DELIBERATELY excluded from the classifier (reported sensitivity instead);
  the deciding surfaces (shipped 4-field: nominal win, deterministic premise;
  latency: parent P2-L3 CI95 lower 1.0022, genuinely flippable) keep both
  SUPPORTS and PERMANENT-DROP-BOUNDED reachable.
- Ceiling baselines: success-rate 1.0 ceilings are functional gates, never
  deciders; the deciders (integer cost ratios, continuous latency) have live
  dynamic range.
- Treatment/comparator identity: arms share substrate/seeds/perturbations and
  differ only in preregistered physical/scaffold counts, evidenced by oplogs +
  phase timings + scaffold counts (V14); timed boundary symmetric (S-ARG
  sensitivity isolates the v3→v4 boundary change).
- Insensitive controls: overbroad instrument live in parent (4/4 every trial)
  and path re-verified in DESIGN smoke; must-fail/must-silent controls retained
  with INVALID (not negative) failure policy.
- Missing prerequisites: none — imports, pins, hashes, timer, bank
  enumerability all verified at DESIGN (§10 PASS).
- Unbound mutable artifacts: exactly the 3 carrier files, hashes verified,
  listed in spec.freeze_artifacts; v4 driver embedded below and hash-bound;
  v2/v3 immutable pins; no external banks/fixtures.

## 10. Freeze binding

freeze_artifacts = [`src/spider/kernel.py`, `src/spider/models.py`,
`src/spider/registry.py`]. The v4 driver is the exact text between
the two standalone marker lines in §12 (unique occurrences in this file); EXECUTE extracts by splitting
those markers and checks CANONICAL-RUNNER-V4-SHA256 (recorded at freeze).
Request/spec/prereg/carrier hashes verified against freeze.json (V1).

## 11. Legacy differentiation (pre-2.0 precedents; targeted comparison)

- P2-REPLAY-COST (sha 9687ff787f2d74460bb7006826008852f5b4416b): withdrawn 8.5x
  for unmatched/uncounted replay economics. This design honors its guard
  exactly: matched tasks (identical TASK_IDS both arms), fully-loaded
  counterfactual (inclusive timed boundary + scaffold accounting), no
  scripted-replay-as-economics framing. Comparative: DISTINCT_EXTENSION
  (scaffolding-complete counter + attribution, which P2 never priced).
- P2-AUTOMATION (operational lesson, no sha): immutable identity, explicit
  write sets, hash-pinned inheritance, per-item recovery — licensed as method
  (V0/V1/V8/per-trial recovery semantics inherited from v2/v3).
- P2-WP003 (sha 292e3243d9bc7a3b88712788a7cb05709eb74eb9, leakage-invalid):
  guard is leakage containment here — no post-state features enter the guard
  beyond the live probe both arms could observe; repair writes exactly one
  mechanism (V8); no jitter-CIs (exact integer ratios + empirical bootstrap on
  wall-clock only).
- Calibrated-counter lineage (parent v3, not pre-2.0): the time-fitted surface
  is REMOVED, not repeated, per audit AF-3 (quasi-structural win direction).
  No identical invalid/degenerate design is repeated: equal-weight-only reruns
  are excluded by the terminating rule; the priced comparison is continuity
  with new instruments (attribution + certificate) and a terminal decision.
- LEGACY verdict: NO_MATCH for scaffolding attribution/pricing (per mandate
  comparative_reasoning); DISTINCT_EXTENSION on replay-cost guards.

## 12. Frozen executable driver v4 (extract between markers; sha-bound)

V4-RUNNER-BEGIN
```python
#!/usr/bin/env python3
# FROZEN RUNNER v4 for EXP-RUNTIME-38340133174 (runtime, design_contract_version 2).
# C-DELTA-REPAIR terminal comparison: shipped 4-field unit counter + inclusive
# episode latency + scaffolding attribution + B11 probe-coverage certificate.
# Reuses the IMMUTABLE parent v2 module by pin-checked import ONLY. Stdlib only.
# Usage (stdout is always a single JSON object):
#   python runner_delta_repair_scaffold_v4.py                      # scored run
#   python runner_delta_repair_scaffold_v4.py --mechanics-only     # canary (discrete projection)
#   python runner_delta_repair_scaffold_v4.py --reachability-probe # synthetic classifier probes (pure)
#   python runner_delta_repair_scaffold_v4.py --liveness-only      # non-outcome-bearing liveness
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

EXP_ID4 = "EXP-RUNTIME-38340133174"
SEED4 = 3980394806  # 38340133174 % 2**32
V2_PIN_SHA = "d4871091dc5bf9aa21d918f2577612aa8c5762e314033d0bbbee46b4962bc608"
V2_PIN_BYTES = 60855
B_LAT = 2000
CLOSURE_BAR = 0.20
ATTRIB_SHARE = 0.50
FETCH_BAR = 0.90


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here.parent, *here.parents):
        if (p / "src" / "spider" / "kernel.py").is_file():
            return p
    return Path("/home/runner/work/Spider/Spider")


REPO = _repo_root()
V2_PATH = REPO / "research/experiments/EXP-RUNTIME-38244432934/raw_evidence/runner_delta_repair_reuse_v2.py"


def _load_v2():
    raw = V2_PATH.read_bytes()
    if len(raw) != V2_PIN_BYTES or hashlib.sha256(raw).hexdigest() != V2_PIN_SHA:
        raise SystemExit("V0-SUBSTRATE-PIN failure: parent v2 runner mismatch; refusing to run.")
    spec = importlib.util.spec_from_file_location("v2frozen", str(V2_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def _arm_counters(arm):
    return arm.counters.as_dict()


def run_reuse_episode(app, origin, mechs, cached, resource):
    """Instrumented treatment episode. Mirrors v2.run_repair_reuse semantics."""
    log = ScafLog()
    t0 = time.perf_counter()
    md = log.timed("S-ARG", copy.deepcopy, mechs)
    log.add_scaf(1)
    arm = log.timed("S-REGISTRY-BUILD", v2.Arm, md, Path("/tmp"), "reuse4")
    log.add_scaf(len(md))
    mech = log.timed("S-REGISTRY-SCAN", arm.target_mech, resource)
    log.add_scaf(1)
    if mech is None:
        return {"ok": False, "reason": "not-executable", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf,
                "episode_s": time.perf_counter() - t0}
    slot = mech.parameter_slots[0]
    intent = mech.intent
    context = {"resource_type": resource}
    required_paths = set(v2.flatten(mech.postconditions))
    r0 = log.timed("S-PROBE", arm.resolve, intent, context, {slot: str(v2.TASK_IDS[0])})
    if r0.status.name != "EXECUTABLE" or r0.bound_action is None:
        return {"ok": False, "reason": "not-executable", "arm": arm,
                "phases": dict(log.t), "scaffold": log.scaf,
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
                "episode_s": ep, "misc_s": ep - sum(log.t.values())}
    patched, probe_body, probe_header = log.timed(
        "S-REPAIR-SIGNAL", v2.local_repair, arm, mech, resource, slot,
        v2.TASK_IDS[0], failed, origin)
    log.add_scaf(1)
    if patched is None:
        ep = time.perf_counter() - t0
        return {"ok": False, "reason": "repair-failed", "arm": arm, "guard_fired": True,
                "guard_info": ginfo, "phases": dict(log.t), "scaffold": log.scaf,
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
            "scaffold": log.scaf, "episode_s": ep,
            "misc_s": ep - sum(log.t.values())}


def run_cold_episode(app, origin, resource, ids, tag):
    """Instrumented cold episode. Mirrors v2.run_cold semantics exactly."""
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


def run_trial_v4(cls, target, seed, j):
    app = v2.LocalApp()
    try:
        if not v2.wait_ready(app):
            return {"valid": False, "reason": "server-not-ready"}
        mechs, cached = v2.make_mech_dicts(app.origin, v2.Counters())
        if mechs is None:
            return {"valid": False, "reason": "learn-failed"}
        base_live = {"mech_dicts": {m["mechanism_id"]: m for m in mechs.values()}}
        for r in v2.RESOURCES:
            base_live[r] = v2.unaffected_behavior(mechs, app.origin, r, "base",
                                                 v2.IN_SUPPORT_PROBE_ID)
        pre_unaffected = {r: base_live[r] for r in v2.RESOURCES}
        app.state.set_perturb(cls, target, seed)
        try:
            v2.run_repair_reuse(app, app.origin, copy.deepcopy(mechs), cached[target],
                                target, "reuse")
            v2.run_cold(app, app.origin, target, v2.LEARN_IDS, "warmcold")
            warmups = 2
            rep_first = (j % 2 == 0)
            if rep_first:
                rep = _timed_episode(run_reuse_episode, app, app.origin,
                                     copy.deepcopy(mechs), cached[target], target)
                c2 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS_MIN, "coldmin")
                c3 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS, "cold")
            else:
                c3 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS, "cold")
                c2 = _timed_episode(run_cold_episode, app, app.origin, target,
                                    v2.LEARN_IDS_MIN, "coldmin")
                rep = _timed_episode(run_reuse_episode, app, app.origin,
                                     copy.deepcopy(mechs), cached[target], target)
            cons = v2.run_repair_reuse(app, app.origin, copy.deepcopy(mechs),
                                       cached[target], target, "conservative")
            leg = v2.run_repair_legacy(app, app.origin, copy.deepcopy(mechs),
                                       cached[target], target)
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
                     for a in (rep, cons, leg, c3, c2) if "arm" in a)
        mtokens = sum(int(getattr(a["arm"].kernel.counters, "model_tokens", 0) or 0)
                      for a in (rep, cons, leg, c3, c2) if "arm" in a)
        return {
            "valid": True, "class": cls, "target": target,
            "repair_success": bool(rep.get("ok")),
            "repair_guard_fired": bool(rep.get("guard_fired")),
            "repair_reason": rep.get("reason"),
            "conservative_success": bool(cons["success"]),
            "legacy_success": bool(leg["success"]),
            "cold_success": bool(c3.get("ok")),
            "cold_min_success": bool(c2.get("ok")),
            "cold_deep_success": None,
            "literal_success": bool(lit["success"]),
            "norepair_success": bool(nor["success"]),
            "norepair_guard_fired": bool(nor.get("guard_fired")),
            "repair_cost": _arm_counters(rep["arm"]),
            "conservative_cost": _arm_counters(cons["arm"]),
            "legacy_cost": _arm_counters(leg["arm"]),
            "cold_cost": _arm_counters(c3["arm"]),
            "cold_min_cost": _arm_counters(c2["arm"]),
            "literal_cost": _arm_counters(lit["arm"]),
            "repair_oplog": list(rep["arm"].oplog),
            "conservative_oplog": list(cons["arm"].oplog),
            "legacy_oplog": list(leg["arm"].oplog),
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
            "unaffected_n": n_unaff,
            "base_liveness": all(v and v[0] == 200 and v[2] for v in
                                 (pre_unaffected[r] for r in v2.RESOURCES)),
            "t_reuse_s": rep.get("episode_s"), "t_cold_min_s": c2.get("episode_s"),
            "t_cold_s": c3.get("episode_s"),
            "order_rep_first": bool(rep_first), "warmups_done": warmups,
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


def cost_verdict_v4(m):
    if not v2.functional_ok(m):
        return "FUNCTIONAL-FAIL"
    sp2, sp3 = m.get("M-SHIPPED-RATIO-L2"), m.get("M-SHIPPED-RATIO-L3")
    lw2, lw3 = m.get("M-LATENCY-R-L2"), m.get("M-LATENCY-R-L3")
    if sp2 is None or sp3 is None or lw2 is None or lw3 is None:
        return "COST-UNKNOWN"
    if sp2 < 1.0 and sp3 < 1.0 and lw2 < 1.0 and lw3 < 1.0:
        return "PRICED-WIN"
    return "PRICED-DEFICIT"


def aggregate_v4(cvs):
    if any(v == "COST-UNKNOWN" for v in cvs):
        return "INCONCLUSIVE"
    if any(v == "FUNCTIONAL-FAIL" for v in cvs):
        return "FALSIFIES-FUNCTIONAL"
    if all(v == "PRICED-WIN" for v in cvs):
        return "SUPPORTS"
    return "PERMANENT-DROP-BOUNDED"


def synthetic_reachability_probe_v4():
    def row(ok=True, sp2=0.9, sp3=0.85, lw2=0.95, lw3=0.93):
        return {"M-REPAIR-SUCCESS": 1.0 if ok else 0.0,
                "M-REPAIR-SUCCESS-WILSON-LOWER": 0.7575 if ok else 0.0,
                "M-CONTAMINATION-RATE": 0.0, "M-WRITE-SET-MAX": 1,
                "M-GUARD-FIRE-RATE": 1.0,
                "M-SHIPPED-RATIO-L2": sp2, "M-SHIPPED-RATIO-L3": sp3,
                "M-LATENCY-R-L2": lw2, "M-LATENCY-R-L3": lw3}
    cases = {
        "PRICED-WIN": row(),
        "PRICED-DEFICIT-shipped": row(sp2=1.05),
        "PRICED-DEFICIT-latency": row(lw3=1.10),
        "PRICED-DEFICIT-boundary": row(sp2=1.0),
        "FUNCTIONAL-FAIL": row(ok=False),
        "COST-UNKNOWN": row(sp2=None, sp3=None, lw2=None, lw3=None),
    }
    verdicts = {k: cost_verdict_v4(v) for k, v in cases.items()}
    aggregates = {
        "SUPPORTS": aggregate_v4(["PRICED-WIN"] * 3),
        "PERMANENT-DROP-BOUNDED": aggregate_v4(["PRICED-WIN", "PRICED-DEFICIT",
                                                "PRICED-WIN"]),
        "FALSIFIES-FUNCTIONAL": aggregate_v4(["PRICED-WIN", "FUNCTIONAL-FAIL",
                                              "PRICED-WIN"]),
        "INCONCLUSIVE": aggregate_v4(["PRICED-WIN", "COST-UNKNOWN",
                                      "PRICED-DEFICIT"]),
    }
    all_class = {"PRICED-WIN", "PRICED-DEFICIT", "FUNCTIONAL-FAIL", "COST-UNKNOWN"}
    all_agg = {"SUPPORTS", "PERMANENT-DROP-BOUNDED", "FALSIFIES-FUNCTIONAL",
               "INCONCLUSIVE"}
    return {
        "class_cost_verdicts": verdicts,
        "aggregate_decisions": aggregates,
        "all_class_branches_reachable": set(verdicts.values()) == all_class,
        "all_aggregate_branches_reachable": set(aggregates.values()) == all_agg,
    }


def _carrier():
    return {
        "kernel_sha256": hashlib.sha256((REPO / "src/spider/kernel.py").read_bytes()).hexdigest(),
        "models_sha256": hashlib.sha256((REPO / "src/spider/models.py").read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((REPO / "src/spider/registry.py").read_bytes()).hexdigest(),
        "v2_runner_sha256": V2_PIN_SHA,
        "v2_runner_bytes": V2_PIN_BYTES,
    }


def _per_class_metrics(cls, rows, seed_base):
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
    h_c3 = sum(_http_of(r["cold_cost"]) for r in rows)
    m["M-SHIPPED-REUSE"] = sh_re
    m["M-SHIPPED-COLD-L2"] = sh_c2
    m["M-SHIPPED-COLD-L3"] = sh_c3
    m["M-SHIPPED-RATIO-L2"] = (sh_re / sh_c2) if sh_c2 else None
    m["M-SHIPPED-RATIO-L3"] = (sh_re / sh_c3) if sh_c3 else None
    m["M-COST-FETCH-RATIO-L3"] = (h_re / h_c3) if h_c3 else None
    m["M-SCAFFOLD-REUSE"] = sc_re
    m["M-SCAFFOLD-COLD-L3"] = sc_c3
    m["M-SP5-RATIO-L2"] = ((sh_re + sc_re) / (sh_c2 + sc_c2)) if (sh_c2 + sc_c2) else None
    m["M-SP5-RATIO-L3"] = ((sh_re + sc_re) / (sh_c3 + sc_c3)) if (sh_c3 + sc_c3) else None
    leg_re = sum(_shipped_sum(r["legacy_cost"]) for r in rows)
    m["M-LEGACY-RATIO-L2"] = (leg_re / sh_c2) if sh_c2 else None
    t_rep = [r["t_reuse_s"] for r in rows]
    t_c2 = [r["t_cold_min_s"] for r in rows]
    t_c3 = [r["t_cold_s"] for r in rows]
    med_rep, med_c2, med_c3 = _median(t_rep), _median(t_c2), _median(t_c3)
    m["M-LATENCY-REUSE-MED-S"] = med_rep
    m["M-LATENCY-COLD-L2-MED-S"] = med_c2
    m["M-LATENCY-COLD-L3-MED-S"] = med_c3
    m["M-LATENCY-R-L2"] = (med_rep / med_c2) if (med_rep is not None and med_c2) else None
    m["M-LATENCY-R-L3"] = (med_rep / med_c3) if (med_rep is not None and med_c3) else None
    if all(v is not None for v in (t_rep, t_c2, t_c3)) and n >= 2:
        lo2, hi2 = _median_ratio_ci(t_rep, t_c2, seed_base + 1, B_LAT)
        lo3, hi3 = _median_ratio_ci(t_rep, t_c3, seed_base + 2, B_LAT)
        m["M-LATENCY-R-L2-CI95"] = [lo2, hi2]
        m["M-LATENCY-R-L3-CI95"] = [lo3, hi3]
    else:
        m["M-LATENCY-R-L2-CI95"] = None
        m["M-LATENCY-R-L3-CI95"] = None
    m["M-LATENCY-SIGN-REUSE-SLOWER-L3"] = sum(1 for a, b in zip(t_rep, t_c3) if a > b)
    no_arg_rep = [r["t_reuse_s"] - (r.get("repair_phases") or {}).get("S-ARG", 0.0)
                  for r in rows]
    no_arg_c3 = [r["t_cold_s"] - (r.get("cold_phases") or {}).get("S-ARG", 0.0)
                 for r in rows]
    m["M-LATENCY-R-L3-NOARG"] = ((_median(no_arg_rep) / _median(no_arg_c3))
        if (_median(no_arg_rep) is not None and _median(no_arg_c3)) else None)
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
    m["M-MODEL-CALLS"] = sum(r.get("model_calls", 0) or 0 for r in rows)
    m["M-MODEL-TOKENS"] = sum(r.get("model_tokens", 0) or 0 for r in rows)
    m["M-N"] = n
    return m


def _attribution(per_class):
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
    attributed = None
    votes = {}
    for key, per_cls in shares.items():
        votes[key] = sum(1 for cls in per_class
                         if per_cls.get(cls) is not None and per_cls[cls] >= ATTRIB_SHARE)
        if votes[key] >= 2 and attributed is None:
            attributed = "ATTRIBUTED-" + key
    closure_ok = all(
        (per_class[cls].get("M-CLOSURE-REUSE-MED") is not None
         and per_class[cls]["M-CLOSURE-REUSE-MED"] <= CLOSURE_BAR)
        for cls in per_class)
    if not closure_ok:
        answer = "ATTRIBUTION-INVALID"
    elif all((e or 0.0) <= 0 for e in excess.values() if e is not None):
        answer = "ATTRIBUTION-MOOT"
    elif attributed is None:
        answer = "UNATTRIBUTED"
    else:
        answer = attributed
    return {"excess_med_s": excess, "phase_deltas_med_s": comps,
            "shares_of_excess": shares, "votes_ge_half": votes,
            "closure_ok": closure_ok, "answer": answer}


def _certificate(trials, np_t, nz_t):
    bank = []
    for r in trials:
        if not r.get("valid"):
            continue
        bank.append({"class": r["class"], "target": r["target"],
                     "ground_truth_stale": True,
                     "guard_fired": bool(r.get("repair_guard_fired"))})
    nc_items = [
        {"probe": "NC-NO-PERTURBATION", "ground_truth_stale": False,
         "guard_fired": bool(np_t.get("stale")) if np_t.get("stale") is not None else None},
        {"probe": "NC-NOISE", "ground_truth_stale": False,
         "guard_fired": bool(nz_t.get("stale")) if nz_t.get("stale") is not None else None},
    ]
    stale_items = [b for b in bank if b["ground_truth_stale"]]
    sens = (sum(1 for b in stale_items if b["guard_fired"]) / len(stale_items)
            if stale_items else None)
    fresh_known = [n for n in nc_items if n["guard_fired"] is not None]
    spec = (sum(1 for n in fresh_known if not n["guard_fired"]) / len(fresh_known)
            if fresh_known else None)
    fa = sum(1 for b in stale_items if not b["guard_fired"])
    complete = (len(bank) == len(CLASSES) * TRIALS_PER_CLASS and len(fresh_known) == 2
                and sens is not None and spec is not None)
    return {
        "bank_n": len(bank), "bank_expected": len(CLASSES) * TRIALS_PER_CLASS,
        "M-CERT-COVERAGE": sens, "M-CERT-SENSITIVITY": sens,
        "M-CERT-SPECIFICITY": spec, "M-CERT-FALSE-ACCEPTS": fa,
        "M-CERT-BOUNDARY": [
            {"id": "BND-REQUIRED-PATHS", "kind": "DERIVED",
             "statement": "Perturbations outside the mechanism required_paths cannot fire the Jaccard guard by construction (filtered token sets)."},
            {"id": "BND-THRESHOLD", "kind": "DERIVED",
             "statement": "Within-envelope perturbations holding required-path Jaccard >= 0.85 with verify-True cannot fire by construction."},
            {"id": "BND-PROBE-BUDGET", "kind": "MEASURED",
             "statement": "Single fused probe at TASK_IDS[0]=14 per episode; detection measured only at that probe.",
             "coverage_measured": sens, "false_accepts_measured": fa},
        ],
        "certificate_complete": bool(complete),
        "nc_detail": nc_items,
    }


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
        out = {"status": "V4-REACHABILITY-PROBE", "experiment_id": EXP_ID4,
               "lane": "runtime", "runner_self_sha": runner_self_sha,
               "decision_rule": synthetic_reachability_probe_v4(),
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
            if live:
                arm = v2.Arm(mechs, Path("/tmp"), "live4")
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
                ep = run_cold_episode(app, app.origin, "users", v2.LEARN_IDS_MIN,
                                      "livecold")
                phase_keys = sorted((ep.get("phases") or {}).keys())
                ep_s = ep.get("episode_s") or 0.0
                closure_finite = (math.isfinite(ep_s) and ep_s > 0
                                  and math.isfinite(ep.get("misc_s") or float("nan")))
            np_t = v2.no_perturbation_trial(SEED4 + 1) if ready else {"stale": None}
            nz_t = v2.noise_trial(SEED4 + 2) if ready else {"stale": None}
        finally:
            app.stop()
        print(json.dumps({"status": "V4-LIVENESS-ONLY", "experiment_id": EXP_ID4,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "server_ready": ready, "distill_live": live,
                          "task_read_verified": bool(one_ok),
                          "in_support_probe_id": v2.IN_SUPPORT_PROBE_ID,
                          "contamination_instrument_live": in_support_ok,
                          "out_of_support_probe_degenerate": out_deg,
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
            r = run_trial_v4(cls, TARGETS[ci % len(TARGETS)], SEED4 + 900 + ci, ci)
            canary.append({k: r.get(k) for k in (
                "valid", "class", "target", "order_rep_first", "repair_success",
                "conservative_success", "legacy_success", "cold_success",
                "cold_min_success", "literal_success", "norepair_success",
                "repair_guard_fired", "contamination_n", "overbroad_contamination_n",
                "unaffected_n", "base_liveness", "write_set_n", "repair_cost",
                "conservative_cost", "legacy_cost", "cold_cost", "cold_min_cost",
                "repair_oplog", "legacy_oplog", "warmups_done", "model_calls",
                "repair_scaffold", "cold_scaffold", "t_reuse_s", "t_cold_s",
                "repair_misc_s", "timed_error")})
        np_t = v2.no_perturbation_trial(SEED4 + 1)
        nz_t = v2.noise_trial(SEED4 + 2)
        print(json.dumps({"status": "V4-MECHANICS-ONLY", "experiment_id": EXP_ID4,
                          "lane": "runtime", "runner_self_sha": runner_self_sha,
                          "seed": SEED4, "carrier": carrier,
                          "canary": canary, "nc_no_perturbation": np_t,
                          "nc_noise": nz_t}, indent=2))
        return

    trials = []
    for ci, cls in enumerate(CLASSES):
        for j in range(TRIALS_PER_CLASS):
            target = TARGETS[(ci + j) % len(TARGETS)]
            trials.append(run_trial_v4(cls, target, SEED4 + 1000 * (ci + 1) + j, j))
    np_t = v2.no_perturbation_trial(SEED4 + 1)
    nz_t = v2.noise_trial(SEED4 + 2)

    invalid = []
    legacy_caveats = []
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
        m = _per_class_metrics(cls, rows, SEED4 + 7000 * (ci + 1))
        if not all(r.get("base_liveness") for r in rows):
            invalid.append(f"{cls}:base-liveness-miss")
        if (m["M-LITERAL-SUCCESS"] or 1.0) > 0.10:
            invalid.append(f"{cls}:perturbation-does-not-bite")
        if (m["M-COLD-SUCCESS"] or 0.0) < 0.90:
            invalid.append(f"{cls}:cold-baseline-not-live")
        if (m["M-NOREPAIR-SUCCESS"] or 1.0) > 0.10:
            invalid.append(f"{cls}:abstention-control-fired")
        if (m["M-GUARD-FIRE-RATE"] or 0.0) < 0.80:
            invalid.append(f"{cls}:guard-not-live")
        if (m["M-CONTAMINATION-RATE"] or 1.0) > 0.10:
            invalid.append(f"{cls}:contamination-above-bar")
        if (m["M-WRITE-SET-MAX"] or 99) > 1:
            invalid.append(f"{cls}:write-set-leakage")
        if not (m["M-OVERBROAD-CONTAMINATION-N"] is not None
                and m["M-OVERBROAD-CONTAMINATION-N"] > 0.10):
            invalid.append(f"{cls}:overbroad-instrument-insensitive")
        if sum(1 for r in rows if r.get("order_rep_first")) != TRIALS_PER_CLASS // 2:
            invalid.append(f"{cls}:parity-order-broken")
        if any(not r.get("warmups_done") == 2 for r in rows):
            invalid.append(f"{cls}:warmup-violation")
        if any(not (math.isfinite(r.get("t_reuse_s") or float("nan"))
                   and math.isfinite(r.get("t_cold_s") or float("nan"))
                   and math.isfinite(r.get("t_cold_min_s") or float("nan"))
                   and (r.get("t_reuse_s") or 0) > 0) for r in rows):
            invalid.append(f"{cls}:nonfinite-latency")
        eq = (m["M-SHIPPED-RATIO-L2"] is not None and m["M-SHIPPED-RATIO-L3"] is not None
              and m["M-SHIPPED-RATIO-L2"] < 1.0 and m["M-SHIPPED-RATIO-L3"] < 1.0
              and (m["M-COST-FETCH-RATIO-L3"] or 1.0) <= FETCH_BAR)
        if not eq:
            invalid.append(f"{cls}:V-EQ-reproduction-broken")
        if not (m["M-LEGACY-RATIO-L2"] is not None and m["M-LEGACY-RATIO-L2"] > 1.00):
            legacy_caveats.append(f"{cls}:V13-legacy-regression-not-reproduced")
        m["V-EQ-HOLDS"] = bool(eq)
        per_class[cls] = m

    cert = _certificate(trials, np_t, nz_t)
    attribution = _attribution(per_class) if per_class else {"answer": "ATTRIBUTION-INVALID",
                                                             "closure_ok": False}
    class_verdicts = {cls: cost_verdict_v4(m) for cls, m in per_class.items()}
    if invalid:
        decision, outcome, status = "MEASUREMENT_INVALID", "INCONCLUSIVE", "MEASUREMENT_INVALID"
    elif any(v == "COST-UNKNOWN" for v in class_verdicts.values()):
        decision, outcome, status = "INCONCLUSIVE", "INCONCLUSIVE", "COMPLETE"
    else:
        agg = aggregate_v4(list(class_verdicts.values()))
        decision = agg
        outcome = "SUPPORTS" if agg == "SUPPORTS" else ("INCONCLUSIVE" if agg == "INCONCLUSIVE"
                                                        else "FALSIFIES")
        status = "COMPLETE"
    if decision in ("SUPPORTS", "PERMANENT-DROP-BOUNDED", "FALSIFIES-FUNCTIONAL"):
        product_note = ("re-admit" if decision == "SUPPORTS"
                        else "permanent-bounded-drop-no-further-L-sweeps")
    else:
        product_note = "no-decision-no-drop-no-readmit"
    out = {"status": status, "outcome": outcome, "decision": decision,
           "experiment_id": EXP_ID4, "lane": "runtime",
           "runner_self_sha": runner_self_sha, "seed": SEED4,
           "invalid_reasons": invalid, "legacy_caveats": legacy_caveats,
           "class_verdicts": class_verdicts, "per_class": per_class,
           "attribution": attribution, "certificate": cert,
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
```
V4-RUNNER-END

...[truncated 8903 chars]