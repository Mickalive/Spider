# INTEL AUDIT — CYCLE 5, RUN 32873081963, REPAIR ROUND 1

- Auditor: INTEL_AUDITOR (`docs/roles/INTEL_AUDITOR.md` binding; `directives/INTEL_AUDITOR.md` mandatory gate). Independent session. The round-0 cycle-5 audit (`origin/cycle/intel/32861355080/audit`, commit `516d99c`) was read as the object of repair and re-verified, not trusted.
- Date: 2026-08-25. Stance: adversarial ("assume the headline may be wrong").
- Mechanism: `unbrowse-route-capture-replay-ladder` (Unbrowse; vendor paper arXiv:2604.00694 CC BY 4.0; client boundary MIT; backend PRIVATE).
- Object under audit: Reproducer repair round 1 snapshot `/tmp/spider_intel_repro` (commit `5eaa700`, "Intel cycle 5 repair 1: reproduction", on refreshed lane base `cc49ba3`). Repair scope claimed: RF-1..RF-4 documentary fixes only; frozen code/data/results byte-identical to the audited round-0 snapshot (`ac87074`).
- Verdict summary: **PASS.** The round-0 gate's own flip condition is met exactly — all four required fixes delivered, documentary-only, zero changes to any frozen path (proven by git tree comparison against the audited round-0 commit, not merely against the now-vanished `/tmp/spider_intel_old_repro` mount). Beyond the spot-check the flip condition requires, this session independently re-ran the full measurement verification: every headline number recomputes exactly from raw evidence, probes verify from event streams, hashes match 11/11, selftest passes 25/25, and the external source claim was re-verified live and verbatim. Mechanism status stands at **VALIDATED_USEFUL**, ceiling **PROOF OF CONCEPT**. A positive result received no special treatment: it passed because its measurement survived fresh adversarial recomputation, not because it is attractive.

---

## 1. Repair-scope verification (RF-1..RF-4)

Ground truth used: committed round-0 audited snapshot `ac87074` (the `/tmp/spider_intel_old_repro` reference in report §11 no longer exists; the git branch is the stronger witness).

| Fix | Claimed | Verified |
|---|---|---|
| RF-4 (no code/data/results edits) | zero modifications under `intel/experiments/unbrowse_ladder_repro/` (11 files), prereg, `results/intel/reproductions/cycle5*` (12 files) | `git diff ac87074 5eaa700` over all frozen paths = **EMPTY** (byte-identical). Commit `5eaa700` touches, relative to its parent, only frozen-content-restored paths + the three documentary targets. Role-doc deltas visible in cross-base diff originate from pre-existing infra commit `cc49ba3` (timestamped before all cycle-5 work) — shared lineage, not a Reproducer edit. |
| RF-1 (cycle-5 report) | `reports/intel/reproductions/cycle5_report.md` with mechanism identity + Scout run ID, disposition table, per-clause evaluation, quotes reliability datum, intent-inheritance artifact, vestigial `C_RECIPES['T_BIN_COOKIE']`, caveats, wording verbatim | EXISTS; every mandated element present (§§1–9); §10 wording **byte-equal** to round-0 gate `maximum_defensible_wording` (programmatic check); forbidden-wordings list identical |
| RF-2 (state file) | cycle-5 record; complete cycle-1 record preserved untouched under `historical_cycle1_record` | Done; `historical_cycle1_record` compared key-by-key against the pre-repair file (`git show ac87074:state/intel_reproduction.json`): **zero diffs** — accepted history preserved intact |
| RF-3 (candidate hygiene) | `state/intel_candidate.json` = byte-copy of Scout cycle-5 candidate incl. `workflow_run_id 32861355080` | **Byte-identical** to the mounted Scout workspace candidate; `workflow_run_id: 32861355080` present; both runs' scout branches point at the same snapshot commit `56310b6` |

No protected files touched by the repair; `VALIDATED_MECHANISMS.json` still contains only cycle-1 SGDR — nothing integrated prematurely.

## 2. Fresh measurement audit (independent, beyond flip-condition spot-check)

Recomputed this session from raw evidence with a newly written script (not a rerun of the round-0 auditor's code):

- Structure: 34 rows = 30 measured + 4 warmups (A,B × 2 tasks — matches prereg §5, which defines warmups for A/B only; C is the post-block). Summary wall lists trace to raw measured rows **exactly** for all six arm/task cells. Env failures/errors: 0. Row order confirms fixed interleaving A,B×5 then C×5 per task.
- T_BIN_FORM: A median **1218.8 ms** / B median **32.9 ms** → median speedup **37.05×** (exact); mean speedup **17.17×**; paired wins **5/5** (strict `<`, no tie-gaming); A actions [6]×5 vs B [0]×5; B payload_ok 5/5; B codes all REPLAY_OK; C median 30.3 ms → C/B **0.92**.
- T_BIN_COOKIE: A median **559.7 ms** / B median **64.6 ms** → median speedup **8.66×** (exact); wins **5/5**; B actions [0]×5; equivalence 5/5; C median 47.0 ms → C/B **0.73**.
- Decision rule: evaluated once in round 0, as frozen; all four clauses verified satisfied by the same recomputation → REPRODUCED_USEFUL follows the rule as written. 0 exclusions vs the 20% INCONCLUSIVE threshold.
- Probes (from `probe_events.json`): P1 ids **3081/3084** field-equal to ground truth; P2 negative **AUTH_FAIL** (403), positive control round-trip PASS; P3 **STALE_TTL** at age **172800.5 s** (> 24 h TTL); P4 delete 201 → replay **HTTP_ERROR** → escalation confirmed **404** absence, provenance `escalated_html_tier:HTTP_ERROR`; structural pointer-only store re-checked mechanically on BOTH stores (no body/content/text/html values >64 chars anywhere).
- Timeline coherence: ladder events span 83.5 s (16:15:19→16:16:43Z) preceded by ~12 s discovery ≈ 95 s total — consistent with ≥2 s pacing across ~40 gaps plus task times; report's "~93 s" accurate in magnitude.
- Integrity reruns: SHA-256 manifest **11/11 OK** (from inside `cycle5/`); prereg FROZEN IMPLEMENTATION hash table vs committed code **11/11 exact** (recomputed myself); offline selftest **25/25 PASS**.

## 3. Implementation inspection (confounder attack — all negative)

- V1 timing hygiene: single clock `perf_counter` around full task execution for all arms; the only `sleep` in the package is pacing between passes, outside timed regions; no `wait_for_timeout`. Context creation outside A's timer favors A — conservative direction.
- V2 targeted extraction both arms (`tasks.py`: selector/JSON-parse; no raw dumps in timed paths).
- V4 capture-origin proof re-verified structurally: route store body template carries `custtel=''` and `delivery=''` (live-form-only fields absent from C's public-doc recipe); cookie route carries `headers_required.cookie ← auth_material`; `run_B_pass` never reads `C_RECIPES`.
- V5 hashlib-only stable hashing; no process-randomized `hash()` anywhere.
- Checker caveat (disclosed, non-blocking): `taxonomy_violations` counters hardcoded to zero, not derived — confirmed in code exactly as disclosed in report §6; functional coverage via probe checks holds for stale_silent/wrong_data_presented_live/missing_code; unreported_substitution is covered structurally (pointer-only store + P4 provenance) rather than by a flipping counter. Travels as disclosed limitation.
- Intent-inheritance artifact re-confirmed in committed store: `POST /booking` (create) and `PUT /booking/{id}` (update) labeled `rsb.list_bookings` via prefix fallback — no metric impact (probes select by method+slots; Role-1 uses exact intents); honestly disclosed.
- `C_RECIPES["T_BIN_COOKIE"]` confirmed dead config: measured C path executes the prereg §4 recipe (GET `/cookies` over bootstrapped jar), hard-coded at `run_all.py:185`.

## 4. External source claim

- **RE-VERIFIED LIVE this session**: arXiv:2604.00694 exists ("Internal APIs Are All You Need: Shadow APIs, Shared Discovery, and the Case Against Browser-First Agent Architectures", Tham/Garcia/Hahn, submitted 2026-04-01); abstract states the vendor headline **verbatim**: warmed cached execution averaged 950 ms vs 3,404 ms Playwright across 94 domains, 3.6× mean / 5.4× median, well-cached routes <100 ms, three-path execution model, x402 tiers — exactly as OFFICIAL_CLAIM records it. The sandbox reproduction correctly does NOT cite itself as support for this headline.
- restful-booker environment fact re-verified live today: root page is a static welcome page ("API playground … resets itself every 10 minutes"), **no booking UI** — confirming the disclosed prereg §8 environment change and Revision-2 auth context.
- Licensing/IP: clean-room statement consistent with stdlib-only code structure; vendor backend private and untouched; sandbox-only targets; demo credentials published constants; nothing copied.

## 5. Residual notes (non-blocking; recorded for provenance)

1. `speedup_mean` for T_BIN_COOKIE is **9.66** in committed summaries but the raw-unrounded ratio is 583.24/60.42 = 9.653 → **9.65**; the committed value divides pre-rounded means (583.2/60.4 → 9.656). Double-rounding artifact on a SECONDARY metric; headline median speedups (37.05× / 8.66×) are exact from raw values. V6 forbids post-outcome edits; travels as disclosed precision note, not a fix.
2. Manifest invocation: `sha256sum -c results/intel/reproductions/cycle5_SHA256SUMS.txt` works only from within `results/intel/reproductions/cycle5/` (entries are directory-relative). Report §11's literal command needs that cwd. Content integrity unaffected (verified 11/11).
3. Attestation-based freeze timing remains a structural limit of single-commit snapshots (disclosed since round 0); mitigations re-verified this session (hash match, timeline physics, protocol-code match, live environment facts).

## 6. Claim-by-claim status

| # | Claim | Evidence files | Recomputation/check | Status |
|---|---|---|---|---|
| R1 | Repair is documentary-only | `git ac87074..5eaa700` | Frozen-path tree diff EMPTY; only report/state changed | VERIFIED |
| R2 | Cycle-1 history preserved | `state/intel_reproduction.json` | Key-level equality vs pre-repair version | VERIFIED |
| R3 | Snapshot self-describing | `state/intel_candidate.json` | Byte-equality with Scout mount; run id present | VERIFIED |
| M1 | Discovery 2/2 passive capture→replayable routes | `discovery_checks.json`, `routestore_snapshot.json`, `traffic_manifests.json` | REPLAY_OK+equivalent 2/2; capture-origin fields present | VERIFIED |
| M2 | Median speedups 37.05×/8.66×, 10/10 wins, 0 browser actions, 100% equivalence | `passes_raw.json`, `latency_summary.json` | Exact recomputation from raw rows | VERIFIED |
| M3 | No latency win over privileged raw HTTP (C/B 0.92/0.73, qualitative only) | `passes_raw.json` | Exact; interpretation bounded by prereg | VERIFIED |
| M4 | No-silent-substitution core (P1–P4 + pointer-only store) | `probe_events.json`, `role3_routestore.json` | Event-stream + structural recheck | VERIFIED |
| M5 | Role-2 honest classification incl. quotes fallback FAILURE | `role2_results.json` | SCHEMA_MISMATCH surfaced, no substitution | VERIFIED |
| E1 | Vendor headline exists as stated | arXiv:2604.00694 | Live verbatim fetch | VERIFIED (OFFICIAL_CLAIM, untested here) |
| D1 | Mandatory durable outputs delivered | report + state files | Present, complete, wording-bound | VERIFIED (round-0 defect cleared) |

## 7. Relevance assessments

- PRODUCT_INFRA: **HIGH** — direct-endpoint escalation attacks repeated-exploration cost (master-prompt §1 sanctions direct endpoints/cached transformations); artifacts feed shared-capability registry questions (versioning/TTL/lifecycle/trust) per directives priority 2.
- GRAPH: **MEDIUM** — route records are exactly the §10 "APIs/direct routes" layer and the miss-path feeds exploration; store integration undemonstrated; addressing exact-intent only (prefix artifact shows naive generalization degrades immediately).
- PHYSICS: **LOW** — execution mechanics and lifecycle policy, not environment dynamics.

## 8. Gate

Machine-readable: `results/intel/audit/CYCLE_32873081963_INTEL_GATE.json` — `gate: PASS`, `mechanism_status: VALIDATED_USEFUL`, `safe_to_integrate: true`, ceiling PROOF OF CONCEPT. Integration is a Director decision under the round-0 gate's integration conditions; the maximum defensible wording and forbidden wordings remain the round-0 binding text, carried forward verbatim (every factual assertion in it re-verified this session).

Audit artifacts: this report; `results/intel/audit/CYCLE_32873081963_INTEL_GATE.json`. Independent recompute script preserved at `/tmp/opencode/audit_cycle5_recompute.py` (session-ephemeral; all values re-derivable from committed `passes_raw.json` per §2 formulas).
