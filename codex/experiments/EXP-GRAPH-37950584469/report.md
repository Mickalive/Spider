# EXP-GRAPH-37950584469 — EXECUTE report

Lane: `graph` · Status: **MEASUREMENT_INVALID** · Outcome: **INCONCLUSIVE** · Branch: **F-CERT**

This report explains `result.json`; it does not exceed the frozen claim or silently contradict the canonical JSON. RAW EVIDENCE (`raw/`), OBSERVATIONS and DERIVED MEASUREMENTS (`result.json`) are kept distinct from INTERPRETATION (this section).

## 1. What was run

- Frozen anchor set: CAL-POS-1..4 positive, CAL-NEG-1..4 negative; CAL-POS-5 retired. K=4 disjoint-cookie-jar sessions (S1 recorded, S2–S4 current) plus 2 warm-jar re-captures per positive anchor. Total requests: 40 (cap 200).
- Two independently written stdlib extraction paths: `P-EXTRACT-A` (html.parser) and `P-EXTRACT-B` (regex/lexer with hand-written entity decoder). Same byte-identical bodies to both.
- GATE C (substrate certificate) → GATE E (instrument + E3 extraction agreement) → D1/D2/D3 anchor verdicts → conditional GATE B (value-only-rotation blindness).

## 2. Certificate and instrument gates

- GATE-C1 (`M-CERT-ROUTE-OK`, `M-CERT-FIELD-PRESENT`): 4/4, 3/4.
- GATE-C2 (`M-CERT-NEG-VALUES-A/B`): 0/0.
- GATE-C3 session isolation: **FAIL** (terminal). The frozen predicate is pairwise
  disjointness of the four sessions' cookie jars on `(name, value)`. It fails on
  CAL-POS-1/2/3 because the servers set **constant configuration cookies** with
  identical `(name, value)` across independent sessions; no session-identifying
  cookie value is shared and every first request is cookie-free. Diagnosis:
  `derived/session_isolation_diagnostic.json` (see §2.1).
- GATE-C4 body variation: PASS.
- GATE-E1 canary: M-CANARY-PASS=True; GATE-E2 fixtures/path-independence: PASS; GATE-E3 agreement: PASS.
  (These were computed but are **not read** because GATE-C3 is terminal; no claim-level statement is licensed.)

## 2.1 GATE-C3 diagnosis (derived, non-gate)

`M-CERT-SESSION-ISOLATION-PASS=false` is driven entirely by server-set constant
cookies, not by session contamination. Per anchor, the shared `(name, value)`
pairs are:

| anchor | shared `(name, value)` pairs (all constant cookies) | session-scoped cookie names (values differ across sessions) |
|---|---|---|
| CAL-POS-1 | `preferred_language=en` | `_gitlab_session` |
| CAL-POS-2 | `GeoIP=...`, `NetworkProbeLimit=0.001`, `WMF-Last-Access=<date>` | `WMF-Uniq`, `authSession` |
| CAL-POS-3 | `CentralAuthAnonTopLevel=1`, `GeoIP=...`, `NetworkProbeLimit=0.001`, `WMF-Last-Access=<date>`, `WMF-Last-Access-Global=<date>` | `WMF-Uniq`, `authSession`, `enwikiSession` |
| CAL-POS-4 | (none; no cookies set) | (none) |

All first requests carried no Cookie header; jar digests differ per session. Thus
the literal frozen C3 predicate is structurally unsatisfiable on the
Wikimedia/gitlab anchors. Under the frozen fail-closed rule this is a terminal
`MEASUREMENT_INVALID` (`F-CERT`) and no gate was relaxed after outcomes were
seen. The important consequence is a **design/operationalization defect** of
this packet's certificate, not a fact about C-FRESHNESS.

## 3. Per-anchor extraction verdicts

| anchor | verdict_A | distinct_A | verdict_B | distinct_B | route_ok | distinct_body |
|---|---|---|---|---|---|---|
| CAL-POS-1 | RECOVERED_SESSION_SCOPED | 16 | RECOVERED_SESSION_SCOPED | 16 | 4/4 | 4/4 |
| CAL-POS-2 | RECOVERED_SESSION_SCOPED | 5 | RECOVERED_SESSION_SCOPED | 5 | 4/4 | 4/4 |
| CAL-POS-3 | RECOVERED_SESSION_SCOPED | 5 | RECOVERED_SESSION_SCOPED | 5 | 4/4 | 4/4 |
| CAL-POS-4 | NO_FIELD | 0 | NO_FIELD | 0 | 4/4 | 4/4 |

## 4. Falsifiers reached and decision

- Branch `F-CERT`; falsifier flags recorded under `controls`.
- Part (ii): M-N-D1V=3, M-N-DECISIONS-D1V=2, M-FA-INCUMBENT-D1V=1.0, M-FA-VALUEAWARE-D1V=0.0, M-PAIRED-FA-DIFF-D1V=1.0, low=1.0, gate_b_branch=DATA-INSUFFICIENT-D1V.

## 5. Interpretation (bounded)

Any interpretation here is bounded by CC-A..CC-F. No prevalence over 'the Web' is claimed, no guard operating point is measured, and nothing is promoted into Product Core. `M-INVISIBLE-STALE-PREV` is null, never 0.0.

## 6. Provenance and raw evidence

- Raw records: `raw/records.jsonl`; raw bodies: `raw/bodies/<anchor>/<session>_<phase>.html`; derived extraction: `derived/extraction.jsonl`; GATE-C3 diagnostic: `derived/session_isolation_diagnostic.json`; code: `research/graph/freshness_detection/exp_37950584469/` (runner `run_experiment.py`; post-run diagnostic `analyze_session_isolation.py`).
