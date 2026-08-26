# PREREGISTRATION FREEZE — frontier-instrument-ledger charter v1

- Team: `frontier-instrument-ledger`
- Charter: v1, snapshot `charter_snapshot.json` (sha256 `491ed9b1cb671214d4964012a49961a71e2e326e77de489e8074a64e6c659aa3`)
- GitHub run: 32922388029
- Authority: HUMAN_FORCED_HISTORICAL_CTO25_ONE_SHOT — exactly ONE backfill/check/audit cycle; no auto-continuation; no deployment.
- Freeze timing: this file is committed BEFORE any extractor/checker is run against the accepted evidence mounts. The only prior activity was read-only survey of mounts to confirm parseability. No hazard-flag outcome has been observed or computed at freeze time.

## 1. Question under test (verbatim from charter)

> Can a minimal provenance/spentness ledger mechanically flag known instrument-reuse, post-adaptation and comparability hazards in accepted SPIDER evidence without inventing scientific verdicts?

## 2. Unit of analysis and mechanical sample selection

Unit = one **instrument-use record**: a named instrument, fixture, benchmark, dataset, metric/gate script, preregistration, or mechanism-reproduction lineage referenced by durable accepted-state files.

Sample is enumerated MECHANICALLY by the extractor from these and ONLY these durable sources in the accepted mounts `/tmp/spider_{graph,physics,intel,product,runtime}`:

- S1: `state/graph_loop.json`, `state/physics_loop.json`, `state/intel_loop.json`, `state/runtime_loop.json`, `state/product_current.json`
- S2: lane ledgers `docs/{GRAPH,PHYSICS,INTEL,PRODUCT}_LEDGER.md` (section headings + verbatim Status lines)
- S3: every `results/audit/CYCLE_*_GATE.json` / `*_FINDINGS.json` present in the mounts
- S4: `results/intel/{VALIDATED_MECHANISMS,COMPETITOR_INDEX,MECHANISM_CANDIDATES}.json`

No hand-typed ledger entries are permitted. Every entry must carry `provenance_refs` (source paths) plus the extraction method (`parsed_field | regex_extracted | section_parse`), and every copied status/verdict string must be byte-verifiable in its cited source (safety invariant §5).

## 3. Minimal ledger schema v0 (UNKNOWN-safe semantics)

```json
{
  "record_id": "IUL-<lane>-<nnn>",
  "instrument_id": "<normalized name>",
  "instrument_kind": "eval_fixture|benchmark|dataset|prereg|gate_or_metric_script|harness|mechanism_lineage|shared_test_fixture",
  "lanes_seen": ["graph|physics|intel|product|runtime"],
  "uses": [
    {"source_ref": "<path>", "run_id": "<id|null>", "role": "producer|audit|director|repair",
     "status_at_source_verbatim": "<exact substring or UNKNOWN>",
     "extraction_method": "parsed_field|regex_extracted|section_parse"}
  ],
  "adaptation_events": [
    {"kind": "amendment|erratum|repair|repin|supersession", "commit": "<sha|null>",
     "timing": "PRE_EVALUATION|POST_EVALUATION_DISCLOSED|POST_EVALUATION_UNDISCLOSED_SUSPECTED|UNKNOWN",
     "evidence_quote": "<verbatim>"}
  ],
  "spentness": "SPENT_CONFIRMATORY|SPENT_EXPLORATORY_ONLY|REUSABLE_UNSPENT|UNKNOWN",
  "spentness_basis": "<quote/ref or UNKNOWN>",
  "cross_lane_links": [{"from_lane": "...", "to_lane": "...", "via_ref": "<path>", "caveat_travel_documented": true|false|null}],
  "unknown_fields": ["<list of schema fields that could not be derived>"]
}
```

UNKNOWN-safe rules (binding):
- U1: any field not derivable from S1–S4 is `"UNKNOWN"` (or listed in `unknown_fields`), never an inferred value, never silently empty.
- U2: UNKNOWN never counts as clean/pass in any check; it produces at minimum a `REVIEW_UNKNOWN` flag.
- U3: statuses/verdicts are copied verbatim; the ledger never reclassifies, summarizes, or re-grades accepted evidence.

## 4. Mechanical hazard checks (frozen definitions)

Each check is a deterministic function over ledger entries + their cited source files. Flag levels: `HAZARD` (known-hazard class matched), `REVIEW_UNKNOWN` (insufficient provenance), `OK`.

- C-REUSE **[reuse/adaptation disclosure]**: instrument_id appears in ≥2 distinct lanes OR ≥2 claim-bearing uses → for each use pair, require an explicit adaptation/caveat-disclosure marker (regex family: `amendment|erratum|repair|repin|supersession|caveat|binding|adaptation|pre-evaluation|pre-outcome|pre-freeze`) in the joined use evidence. Missing marker on any pair ⇒ `HAZARD_REUSE_WITHOUT_DISCLOSURE`.
- C-POSTADAPT **[post-adaptation]**: adaptation event with `timing != PRE_EVALUATION` whose commit/date cannot be shown to precede recorded outcomes ⇒ if disclosure markers exist: record as POST_EVALUATION_DISCLOSED + `HAZARD_POST_ADAPTATION_DISCLOSED` (still flagged — adaptation after outcomes is always flag-worthy); if no markers: `HAZARD_POST_ADAPTATION_UNDISCLOSED`. Undatable ⇒ `REVIEW_UNKNOWN`.
- C-COMPARABILITY **[comparability]**: same instrument_id used across uses whose recorded scope/holdout/surface differs OR is UNKNOWN while any use carries a quantitative claim context ⇒ `HAZARD_COMPARABILITY_RISK` or `REVIEW_UNKNOWN`.
- C-SPENTNESS **[spentness]**: explicit spentness marker (`instrument spent|spent-instrument|selection-on-instrument decision|CAP|capped|final round|closed permanently`) + any later confirmatory-use reference ⇒ `HAZARD_SPENT_REUSE`; explicit spentness + no later use ⇒ OK (spentness=SPENT_CONFIRMATORY); no spentness derivable ⇒ spentness=UNKNOWN + `REVIEW_UNKNOWN`.
- C-GATELINEAGE **[invalid/power-deficient instrument lineage]**: source text for a use contains measurement-invalidity or unreachability markers (`MEASUREMENT_INVALID|zero power|undecidable|by construction|unreachable|min achievable|Holm-adjusted p > 0.05|invalidated|leaked|process-randomized|non-deterministic seed|hash\(`) ⇒ `HAZARD_INVALID_OR_POWERLESS_INSTRUMENT_LINEAGE`; any later reuse of the same instrument_id/mechanism lineage inherits the flag.
- C-SHAREDFIXTURE **[shared fixture divergence]**: same shared test-fixture/test-case id referenced by ≥2 lanes where the recorded status mentions diverge (one lane records failure/pre-existing failure; another treats suite as green) or ownership is cross-lane-ambiguous ⇒ `HAZARD_SHARED_FIXTURE_STATUS_DIVERGENCE`.

Anti-gaming constraints:
- A1: extractor/checker code MUST NOT read this prereg's §6 expectation list or otherwise receive the expected answers; expectations exist only for post-hoc scoring.
- A2: entries derive only from mounted files; the working repo copy is write-scope, never an evidence source.
- A3: all raw outputs (extraction manifest with file sha256s, ledger, flags, safety verification) are committed.

## 5. Safety invariant (no invented verdicts)

For every record: each `status_at_source_verbatim` string must be found byte-exact inside the current content of its `source_ref` file (verified post-extraction by re-read + substring check). Violations counted as `false_reclassification_count`. Requirement: **0**. Any violation = automatic fail of the safety dimension regardless of other results.

## 6. Preregistered known-hazard/capture expectations (frozen BEFORE measurement)

Six items expect a specific HAZARD-class flag; four items expect correct CAPTURE (right classification, no false hazard). Scoring: item handled correctly iff expected flag/class emitted for the right record(s); capture items also fail if mislabeled as hazards. Threshold D1: ≥8/10 correct.

| id | expectation | class expected | durable citation (read pre-freeze) |
|----|-------------|----------------|-------------------------------------|
| K1 | WP-003 site-seed nondeterminism (process-randomized `hash(site)` invalidated frozen seed) | HAZARD via C-GATELINEAGE (seed/invalid marker) | `/tmp/spider_physics/docs/PHYSICS_LEDGER.md` WP-003 section (~L386+); SPIDER_MASTER_PROMPT §23 |
| K2 | WP-003 `prev_action_label` target leakage | HAZARD via C-GATELINEAGE (leakage marker) | same sources as K1 |
| K3 | Graph books composite fixture adapted pre-evaluation via Amendments A1/A2 (compliant repair) | CAPTURE: adaptation_events timing=PRE_EVALUATION, no hazard flag | `/tmp/spider_graph/state/graph_loop.json` reason field; `/tmp/spider_graph/docs/GRAPH_LEDGER.md` G-H6 (~L406–475) |
| K4 | Runtime gate code existing only from outcomes-era commit (W-C2-3) | HAZARD via C-POSTADAPT (post-evaluation, disclosed) | `/tmp/spider_runtime/state/runtime_loop.json` warnings_disposition W-C2-3 |
| K5 | Intel cycle-7 Holm-family gate had zero reachable power (min adjusted p 0.125 > 0.05 at n=5) | HAZARD via C-GATELINEAGE (power/undecidable marker) | `/tmp/spider_intel/state/intel_loop.json` reason; `/tmp/spider_intel/docs/INTEL_LEDGER.md` CYCLE 7 |
| K6 | Intel cycle-6 unbrowse multi-host line ended MEASUREMENT_INVALID (instrument defects) | HAZARD via C-GATELINEAGE on that lineage | `/tmp/spider_intel/state/intel_loop.json`; `/tmp/spider_intel/docs/INTEL_LEDGER.md` CYCLE 6 |
| K7 | Shared `PhysicsLeakageGuardTests` fixture failing identically across lanes while suites report green elsewhere | HAZARD via C-SHAREDFIXTURE | `/tmp/spider_runtime/state/runtime_loop.json` audit_integration.pre_existing_unrelated_failure; `/tmp/spider_graph/state/graph_loop.json` reason ("known pre-existing Physics fixture failure"); GRAPH_LEDGER G-H6 integrity note |
| K8 | PB-001 verdict script analysis_code_hash repinned post-pin via DISCLOSED commit (dress-rehearsal supersession) | CAPTURE: adaptation_events repin/supersession POST_EVALUATION_DISCLOSED, no undisclosed-hazard flag | `/tmp/spider_product/state/product_current.json` artifact_pins.verdict_script_current; run-memory INDEX run 32908007576 (radar tier, citation only) |
| K9 | Intel R-1 SGDR fused-scoring mechanism reused cross-lane into Graph successor program with binding caveats required to travel | CAPTURE (+C-REUSE link): cross_lane_links intel→graph with caveat_travel_documented=true; REVIEW_UNKNOWN acceptable only if linkage truly absent from S1–S4 (scored incorrect if linkage exists but missed) | `/tmp/spider_intel/state/intel_loop.json` next_mission (R-2 gating); `/tmp/spider_graph/state/graph_loop.json` next_program.rationale; `/tmp/spider_intel/results/intel/VALIDATED_MECHANISMS.json` caveats |
| K10 | Graph V31 addressing instrument marked SPENT (selection-on-instrument decision outcome); later programs used third-authorship instruments instead | CAPTURE: spentness=SPENT_CONFIRMATORY with basis quote; no SPENT_REUSE flag unless a later confirmatory V31-instrument use exists | `/tmp/spider_graph/docs/GRAPH_LEDGER.md` G-H4 (~L215–303) & G-H5 third-authorship notes (~L326, L361) |

## 7. Manual-baseline comparison protocol (frozen questions)

Ground truth established FIRST by manual grep/read over the mounts, logging tool invocations and files opened per question; then the identical questions answered from the built ledger alone; answers compared for correctness. Metrics per question: `manual_steps`, `manual_files_opened`, `manual_ambiguous_candidates`, `ledger_steps`, `ledger_wrong` (bool).

- M1: What spentness/discipline status does the V31 addressing instrument carry, and what does any future quantitative claim require of it?
- M2: Has the books composite evaluation fixture been adapted since creation, and were adaptations before or after evaluation?
- M3: Which lanes reference `PhysicsLeakageGuardTests`, and what status does each record?
- M4: Is the Intel unbrowse route-ladder instrument eligible for further confirmatory use under its own CAP/final-round rules?
- M5: Were WP-006 collector instruments repaired before outcomes, and is that compliantly documented?
- M6: Does the SGDR fused-scoring mechanism carry binding caveats that must travel into Graph integration?

Threshold D4: ledger resolves ≥5/6 questions with strictly fewer inspection steps than manual AND zero wrong answers.

## 8. Decision rule (frozen)

VERDICT = **LEDGER_WORTH_RETAINING** (as candidate infrastructure recommendation only — NOT deployed, NOT mandatory) iff ALL hold:
- D1 detection: ≥8/10 expectation items handled correctly;
- D2 safety: `false_reclassification_count == 0`;
- D3 UNKNOWN-safety: 100% of records with non-derivable provenance fields have UNKNOWN values there AND emit at least `REVIEW_UNKNOWN`;
- D4 lookup: as in §7.

Otherwise VERDICT = **NOT_WORTH_RETAINING_AS_IS**, reporting per-dimension failures. Cost vector (build/backfill wall-clock, LOC, tokens≈n/a local, lookup costs both ways) reported regardless. Either way: `continue_recommended=false`, no deployment, no core-lane writes, no lifecycle continuation (HUMAN-FORCED ONE-SHOT).

## 9. Claim ceiling

Results are PROOF-OF-CONCEPT/OBSERVATION tier about THIS backfill sample and THIS implementation only. No generalization to unseen instruments, no scientific reclassification of any lane evidence, no orchestration mandate. Negative results are first-class outcomes.
