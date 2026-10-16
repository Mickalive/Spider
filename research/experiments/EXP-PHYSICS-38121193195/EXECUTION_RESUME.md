# EXECUTION RESUME CHECKPOINT — EXP-PHYSICS-38121193195 (lane=physics)

Written by the EXECUTE model attempt that started 2026-10-16T17:50:03Z, after it
verified the freeze and after a prior attempt had already launched the frozen
collection. **Read this before doing anything else.**

## 1. Current state (as of 2026-10-16T18:05Z)

- **Freeze integrity: VERIFIED 8/8.** `freeze.json.hashes` for
  `design_review.json`, `prereg.md`, `request.json`, `spec.json` and all four
  `artifact_hashes` (parent spec, parent raw 228-row fixture, bound parent lib,
  bound parent run) match on disk. Frozen inputs are untouched.
- **MV5 parent replay: 0/228 mismatches** using the bound classifier imported
  from `research/physics/exp_38074818597_lib.py` (`classify_stored` on every row
  of `research/experiments/EXP-PHYSICS-38074818597/raw/ambient_collection.jsonl`).
- **The frozen 456-GET two-vantage sweep is ALREADY RUNNING** as an orphaned
  process: `pid 19005  python3 research/physics/exp_38121193195_run.py --phase all`
  (own session, sid=19001, started 2026-10-16T17:39:08Z, log `/tmp/exp_run.log`).
  Its source file was deleted from the worktree by a later retry baseline
  (`git clean -fd`), but the process is alive and executing the frozen protocol.
- Collection timeline from the run log (RAW OBSERVATION, not interpretation):
  - t0 = 2026-10-16T17:39:34.763Z (first V2 GET of rung 0)
  - rung 0 (+0 s) started 17:39:34, rung 1 (+300 s) ~17:46, rung 2 (+900 s)
    started 17:54:34, rung 3 (+1800 s) scheduled to start 18:09:34 UTC.
  - Rung 0 took ~6.5 min (several slow/timeouting endpoints), so rung 3 is
    expected to finish ~18:15-18:18 UTC. The script buffers records and writes
    its output files only at the END of collection.
- **Ports 127.0.0.1:19051 (HTTPTunnelPort) and 127.0.0.1:19052 (ControlPort)
  are already bound** by the Tor instance backing the run (`tor -f /tmp/torrc-v2`,
  DataDirectory `/tmp/tor-data`).

## 2. DO NOT do these

1. **Do NOT start a second collection and do NOT start a second Tor** on
   19051/19052. A second sweep would double-hit the frozen 57-endpoint pool in
   the same window (protocol self-induction contamination, spec
   `measurement_validity.validity_notes`) and a second Tor cannot bind the ports.
2. **Do NOT kill pid 19005** before it finishes; it holds the only in-flight raw
   evidence of this frozen transaction.
3. **Do NOT re-freeze, re-design, re-spec or weaken the prereg** — the packet is
   frozen and immutable.
4. **Do NOT start the sweep from scratch** in order to "own" the code: the frozen
   window ladder is already being measured; a restart would spend a whole
   1800 s ladder and is not needed.

## 3. Evidence preservation

A watchdog daemon (`/tmp/spider_preserve/watchdog.py`, setsid, independent of any
model process group) mirrors everything this run produces to
`/tmp/spider_preserve/mirror/…` and restores it into the worktree if a retry
baseline (`git reset --hard` + `git clean -fd`) deletes it. If you find `raw/`
missing, the preserved copy is at `/tmp/spider_preserve/mirror/research/experiments/EXP-PHYSICS-38121193195/raw/`
and `/tmp/spider_preserve/exp_run.log` holds the full collection log.

## 4. Substrate facts already recorded (RAW OBSERVATION, start-of-session)

- V1 (direct runner egress): ip 57.154.4.117, AS8075 (Microsoft), US/Arizona/Phoenix, IsTor=false.
- V2 (treatment: pinned Tor exit): ip 192.42.116.54, AS215125 (Church of Cyberology),
  NL/North Holland/Amsterdam, IsTor=true,
  pinned relay fingerprint `5BAFA0BD32297E5B6EA5817125E2DF4DF64F008E` (nick NTH54R2),
  `SETCONF ExitNodes=$5BAFA0BD32297E5B6EA5817125E2DF4DF64F008E` + `StrictNodes=1` confirmed.
- MV1 at session start therefore holds on the hard clauses (distinct IP, distinct
  ASN, non-identical geo tuple). MID identity check was recorded at rung 2 start
  (17:54:48Z, same IP/fingerprint) — see `/tmp/exp_run.log`.
- Live oracle controls passed at BOTH vantages at rung 0 and rung 2 starts
  (7/7 hosts each, including the Tor-side 503-resolve failure for
  `no-such-host.invalid` which correctly classifies TRANSPORT_ERROR).

## 5. What the next EXECUTE agent must do (in order)

1. Wait for pid 19005 to exit (check `/tmp/exp_run.log` for
   `collection complete` / process gone) and for the raw output files to appear
   under `research/experiments/EXP-PHYSICS-38121193195/raw/` (restore from
   `/tmp/spider_preserve/mirror/...` if a retry baseline removed them).
2. Verify completeness before any analysis: 4 rungs x 57 endpoints x 2 vantages =
   456 pool records, oracles at both vantages at every rung, identity checks at
   start/mid/end, `delta_ref_actual_s >= 1500` (MV4), 57/57 anchors on both
   vantages (MV3), 57/57 delta on both, byte-identical pool (MV10), live
   double-classification replay 0 mismatches (MV5), pinned exit unchanged (MV2),
   V1 ASN constant (MV8), tunnel live (MV9/MV6a).
3. Run the frozen analysis: `research/physics/exp_38121193195_finalize.py`
   (written by the 17:50Z EXECUTE attempt; `python3 -m py_compile` passed and
   its no-evidence guard was exercised at 18:09Z — it verified freeze 8/8 and
   exited 78 WITHOUT writing any packet when `raw/` was still absent, i.e. it
   cannot invent a result; mirrored at
   `/tmp/spider_preserve/mirror/research/physics/exp_38121193195_finalize.py`).
   It imports the BOUND parent lib primitives, computes every metric in
   `spec.json#metrics_primary` / `metrics_secondary`, runs the five synthetic
   controls at the frozen R/perms/boot, evaluates the frozen five-clause
   decision rule with the frozen precedence, and writes
   `result.json` / `report.md` / `provenance.json` only if every MV prerequisite
   it can check passes; otherwise it refuses to write a packet and reports the
   exact failing prerequisite (MEASUREMENT_INVALID is a status, not a
   falsification).
4. Independently re-read the raw evidence and the written packet before
   returning; do not trust this note for anything it labels interpretation.

## 6. Contract reminders for this packet

- `status` = measurement validity (`COMPLETE|BLOCKED|MEASUREMENT_INVALID`);
  `outcome` = scientific answer (`SUPPORTS|FALSIFIES|MIXED|INCONCLUSIVE`).
- A second egress that cannot be provisioned/pinned/held stable is
  MEASUREMENT_INVALID, never FALSIFIES, and never a single-vantage substitute.
- A validly measured V2 with < 3 intrinsic endpoints is SCIENTIFIC evidence and
  routes to `S0_VANTAGE_SPECIFIC` (frozen LOW-V2-INTRINSIC convention), not to
  MEASUREMENT_INVALID; only zero intrinsic at BOTH anchors (MV3a) is an
  instrument-exercise failure.
- Record the pinned exit fingerprint in `result.json` and `provenance.json`
  (design review finding N1: treatment identity is EXECUTE's responsibility).
