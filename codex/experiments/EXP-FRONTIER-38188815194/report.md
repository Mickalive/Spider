# EXP-FRONTIER-38188815194 — EXECUTE report

Lane `frontier`. Claim binding `C-CROSSSITE` (registry status `HYPOTHESIS`).
Frozen design: `request.json` / `spec.json` / `prereg.md` / `freeze.json` / `design_review.json`,
all re-hashed and matching at the start of this attempt.

**Producer disposition: `status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`.**

This is **not** a scientific negative. It is a pre-registered representation-loss gate (V3)
firing before any outcome-bearing measurement was taken.

---

## 1. The evidence chain, in order

```
RAW EVIDENCE      179 of 208 admitted deep items reconstructed; 29 not reconstructible
   ->              (run/raw/paths.jsonl, run/raw/frame_misses.jsonl)
OBSERVATION       The live sites no longer expose the frozen BFS frame's deep paths
DERIVED           n_misses = 29  =>  V3 frame fidelity FAILS  =>  G1 gate fires
MEASUREMENT       n_misses = 29; misses concentrated on 2 of 4 hosts
INTERPRETATION    The frozen frame has aged out; the treatment population is not the
                  population the prereg thresholds were defined over
DECISION          status=MEASUREMENT_INVALID, outcome=NOT_APPLICABLE (per G1/V3)
```

No revalidation cost, no change rate, no dead rate, no false-accept rate and no
frozen `decide()` outcome exists in this packet. Nothing below the gate was measured.

## 2. Gate table

| Gate | Rule | Observed | Verdict |
|---|---|---|---|
| **V1** code identity | frozen block sha256 == `0e42fa34…317ce` | `0e42fa34…317ce` | **PASS** |
| **V2** controls | all nine controls PASS before economics | 9/9 PASS, `failed=[]` | **PASS** |
| **V3** frame fidelity | `n_misses == 0` over 208 admitted items | **`n_misses = 29`** | **FAIL — decisive** |
| **V4** budget | `total_gets <= 20000` | never emitted; bounded ≤926 + snapshot | UNKNOWN |
| **V5** seed liveness | each host seed HTTP 200 | 4/4 HTTP 200 | **PASS** |
| **V6** denominator | `cold_batch_gets>0`, `n_items>0` | 926 > 0, 179 > 0 | **PASS** |
| **V7** session-scale bound | no day-scale claim | no window measured at all | not exercised |
| **V8** decision determinism | stable recomputation | `decide()` never applied | not exercised |
| **V9** elapsed reporting | actual elapsed recorded | ladder never started | not exercised |

**V3 is decisive.** `prereg.md#11` V3 states verbatim: *"Any missing item -> status=MEASUREMENT_INVALID
listing the misses (representation loss, not a negative)."* Gate G1 then forces
`outcome=NOT_APPLICABLE`. The rule was frozen before any cost was observed.

## 3. The V3 failure in detail

Reconstruction ran the frozen policy unchanged (same-host static `<a>`, item-blind FIFO in
document order, per-seed budget 250, depth 6, each URL fetched at most once, anchor = netloc of
the seed's **final** URL after redirects). It recovered **179 / 208** admitted deep items.

| Host | admitted | recovered | **missed** |
|---|---|---|---|
| `doc.rust-lang.org` | 13 | 10 | **3** |
| `pandas.pydata.org` | 8 | 8 | 0 |
| `docs.readthedocs.io` | 28 | 28 | 0 |
| `docs.pytest.org` | 159 | 133 | **26** |
| **total** | **208** | **179** | **29** (13.94%) |

By hop: 26 misses at hop 4, 3 misses at hop 3. Zero misses on two hosts.

Every missed URL is listed in `run/raw/frame_misses.jsonl`. The pattern is tight and one-sided:

- all 26 `docs.pytest.org` misses are per-release changelog pages under
  `/en/stable/announce/` (`…/announce/release-4.1.1.html`, `…/release-4.2.0.html`, `…/release-4.2.1.html`, …);
- the 3 `doc.rust-lang.org` misses are `…/book/ch09-01-unrecoverable-errors-with-panic.html`,
  `…/book/ch09-02-recoverable-errors-with-result.html` and `…/reference/behavior-considered-undefined.html`.

**Interpretation (not raw evidence).** This is *consistent with* the hosts having been
reorganized since the frozen crawl — pytest no longer publishes the old per-release `announce`
pages at depth ≤ 6 from `/en/stable/`, and the Rust book/reference edition moved. The frozen
design contains **no arm that distinguishes "page deleted" from "page no longer linked"**, so
that cause is a hypothesis, not a measurement. The *measured* fact is `n_misses = 29`, and that
alone triggers V3.

## 4. Controls (V2) — the instrument itself is sound

All nine frozen offline controls PASS under the same code that scores the experiment:

| Control | Direction | Observed |
|---|---|---|
| `C-BFS-PARENT-CHAIN` | positive | recovered `[seed, /a.html, /b.html, /item.html]` |
| `C-PATH-CANARY` | positive | `path_len=4`, `snapshot_gets=4`, all 200 |
| `C-REVAL-NOCHANGE` | **null** | `changed=[]`, `dead=[]` — no spurious firing |
| `C-REVAL-CHANGE-DETECT` | positive | mutation detected by SHA-256 |
| `C-LIVENESS-404` | positive | removal detected as dead |
| `C-DECISION-CANARY-SUPPORTS` | positive | `SUPPORTS` |
| `C-DECISION-CANARY-MIXED` | positive | `MIXED` |
| `C-DECISION-CANARY-MIXED-WINDOW` | positive | `MIXED` |
| `C-DECISION-CANARY-FALSIFIES` | negative | `FALSIFIES` |

The revalidation instrument fires in both directions, the decision function reaches all three
branches, and the frame arithmetic reproduces `prereg.md#13` exactly (208 admitted; ordinal mean
166.0144, min 31, max 250; `sum(hop+1)=931`; `cold_batch_gets=926`; batch threshold 833.4;
amortized per-item 4.451923, threshold 4.006731). **The instrument is not the problem. The frame is.**

## 5. A second, independent blocker — the harness envelope

Even with an intact frame this frozen design could not have completed here.

- The frozen module `time.sleep`s the nominal ladder: `300 + 900 + 1800 = 3000 s`, inside the agent process.
- It must also issue ≈926 reconstruction + ≈931 snapshot + 4×≈931 revalidation GETs, at 0.1–0.3 s observed latency.
- **Minimum wall clock ≥ 3558 s (~59 min).**
- `.github/scripts/run-opencode-resilient.sh` defaults `SPIDER_MODEL_MAX_RUNTIME_SECONDS=1200`
  (no override in `spider-lane.yml`) and on expiry sends `kill -TERM` then `kill -KILL` to the entire
  model process group `-$MODEL_PGID` — reaping orphan descendants even after a normal parent exit.

So the frozen confirmatory measurement is structurally unreachable inside one EXECUTE process.
This is the same mechanism behind the already-recorded prior failures (`failure.json` exit 67;
`model_execute.json` attempt 3 exit 124). It is an infrastructure envelope mismatch, **not** a
negative result.

### 5.1 Orphans found and reaped

Two orphaned processes from the two immediately preceding attempts of *this same experiment* were
still alive at the start of this attempt, both `ppid=1`, both writing into this packet's directory:

| PID | started | command |
|---|---|---|
| 17423 | 2026-10-16T15:01:44Z | `python3 /tmp/opencode/exp38188815194_execute_module.py --stage all --out …/EXP-FRONTIER-38188815194` |
| 29013 | 2026-10-16T15:19:36Z | `python3 -u …/execute_module.py --stage economics --out …/EXP-FRONTIER-38188815194` |

Neither had written any `raw/` or `derived/` output. Both were SIGKILLed so that no unattributable
concurrent writer could leave a plausible-looking `derived/decision.json` in the packet directory.
No evidence was destroyed.

## 6. What must not be concluded

- **Not** a negative for full-path persistence. No revalidation cost was measured.
- **Not** a result about `C-CROSSSITE` maintenance economics either way. The packet is silent on the question.
- **Not** an update to the parent's discovery-axis falsification. That stands unchanged.
- The 179-item subset path-length mean (4.402235) is recorded under an explicitly **non-decisional**
  metric key. It must **not** be compared against the frozen per-item threshold 4.006731: that
  threshold is defined over 208 items, the subset is 179 items selected by precisely the variable
  under study (site survival), and no window ever ran. `prereg.md#15` discloses an a-priori tilt
  toward `FALSIFIES`; reaching for that number to shortcut the decision would be a preregistration
  weakening after seeing outcomes, and it is not done here.

## 7. Smallest next actions to unblock

1. **Check frame fidelity before spending the ladder.** A prospective attempt should count recovered
   paths against the 208 admitted items *before* the 3000 s window ladder. That single V3 check costs
   ~2 minutes instead of ~60 and detects exactly the failure that invalidated this attempt. It
   implements the frozen V3 gate the design already requires; it does not weaken it.
2. **Re-census the frame.** `prereg.md#15` assumes a live frame that no longer exists. Answering this
   question needs a fresh census of the four hosts (or a re-registration of the admitted set) before
   any persistence-economics measurement is meaningful. This is a DESIGN-side prerequisite failure,
   and a future packet should register the frame's maximum age as a freeze prerequisite.
3. **Reconcile the ladder with the envelope.** Any packet whose nominal window ladder exceeds
   `SPIDER_MODEL_MAX_RUNTIME_SECONDS` is deterministically unexecutable. Either re-register the
   ladder against a longer envelope, or raise the envelope for such packets, before re-freezing.
   A session-scale ladder of 3000 s was specified with the envelope constraint unexamined.

## 8. Artifacts

| Path | Role | sha256 |
|---|---|---|
| `run/raw/frame_misses.jsonl` | raw — the 29 unreconstructible admitted items (V3 evidence) | `fd7d816b918ad2d8…f21c92e` |
| `run/raw/paths.jsonl` | raw — 179 recovered parent chains | `5192435b4c8a28d7…d1ca33c46` |
| `run/raw/controls.jsonl` | raw — 9/9 frozen controls | `904187ce34eeedcf…4c75658` |
| `execute_module.py` | code — frozen driver materialized from `prereg.md#9` (V1 PASS) | `f18e5b55e563c26f…3e988d262` |
| `run/raw/economics.jsonl` | **absent** — no window completed | — |
| `run/derived/metrics.json` | **absent** — written only after the full ladder | — |
| `run/derived/decision.json` | **absent** — `decide()` never applied | — |

No frozen input was modified. No git commit, push, branch switch, reset or force-push was performed.
