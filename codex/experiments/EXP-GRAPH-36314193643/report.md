# EXP-GRAPH-36314193643 — C-FRESHNESS Freshness Guard on Real Credential-Free Public HTTP

## Experiment Summary

**Lane**: graph · **Claim**: C-FRESHNESS · **Cycle**: 36313602258 · **Director action**: PIVOT

**Status**: `MEASUREMENT_INVALID` · **Outcome**: `INCONCLUSIVE`

This experiment tested whether a four-channel response-derived freshness guard reaches a valid operating point on real credential-free public web origins, using a screen calibrated before use against positive and negative anchors. The experiment executed against the real public internet using only `urllib.request` (stdlib) and `html.parser` — no browser, no Docker, no credentials, no JavaScript execution.

**Result**: The experiment terminated at GATE 0 with `status=MEASUREMENT_INVALID` because the screen's calibration could not demonstrate detection power. Only 1 of 5 required positive anchors (CAL-POS-1: gitlab.com) showed session-scoped capability token variation in raw HTML. All 4 negative anchors were correctly rejected. The screen's representation layer (html.parser without JavaScript) is the primary limiting factor.

---

## 1. What Was Executed

The frozen design called for:

1. **GATE 0 Calibration** (pre-execution, before any candidate screening):
   - G0.2: ≥ 2 of 5 positive anchors must pass (show session-scoped token variation)
   - G0.3: All 4 of 4 negative anchors must be rejected (no session-scoped AGSI)
   - Any blocking failure → `MEASUREMENT_INVALID`, `INCONCLUSIVE`

2. **Candidate Screening**: 48 public origins across 9 strata, tested for reachability and AGSI presence

3. **Guard Evaluation**: If GATE 0 passed, compute the four-channel guard's operating point against B-NO-GUARD-REPLAY, B-INCUMBENT-SIGNAL-ONLY, and four single-channel ablations

4. **Economics**: Measure break-even abstention rate and per-item admission region

---

## 2. GATE 0 Results

### G0.2 — Positive Anchor Calibration (1/5 PASS → FAIL)

| Anchor | URL | Result | Distinct Values |
|--------|-----|--------|-----------------|
| CAL-POS-1 | gitlab.com/-/trial_registrations/new/ | **PASS** | 4 distinct authenticity_token values across 4 sessions |
| CAL-POS-2 | auth.wikimedia.org Special:CreateAccount | FAIL | 0 (wpCreateaccountToken field exists in HTML, value is JS-generated) |
| CAL-POS-3 | en.wikipedia.org Special:UserLogin | FAIL | 0 (wpEditToken field exists, value not in raw HTML) |
| CAL-POS-4 | meta.discourse.org/ | FAIL | 0 (meta csrf-token present, content not accessible) |
| CAL-POS-5 | bugs.launchpad.net/ubuntu/+reportbug | FAIL | 0 (HTTP 404 on all 4 sessions) |

**Analysis**: Only CAL-POS-1 (gitlab.com) demonstrated the expected behavior — session-minted authenticity_token values that differ across independent fresh sessions, each with a different ETag and body SHA-256. The other four anchors either render their tokens via JavaScript (invisible to html.parser), serve the token field without a value, or return HTTP 404.

### G0.3 — Negative Anchor Calibration (4/4 REJECTED → PASS)

All four negative anchors returned HTTP 200 across all 4 sessions and contained no session-scoped action-gating state items:

| Anchor | URL | Reason |
|--------|-----|--------|
| CAL-NEG-1 | www.iana.org/domains/reserved | NO_AGSI_DETECTED |
| CAL-NEG-2 | cdn.jsdelivr.net/gh/python/cpython@v3.12.0/README.rst | NO_AGSI_DETECTED |
| CAL-NEG-3 | www.debian.org/ | NO_AGSI_DETECTED |
| CAL-NEG-4 | httpbin.org/forms/post | NO_AGSI_DETECTED |

### GATE 0 VERDICT: FAIL

G0.2 requires ≥2 of 5 positive anchors to pass. Only 1 passed. The gate short-circuits to `status=MEASUREMENT_INVALID`, `outcome=INCONCLUSIVE`. No claim-level statement is licensed (falsifier F9).

---

## 3. Candidate Screening Results

Of 48 candidate hosts:
- **34 reachable** (HTTP 200)
- **14 blocked/unreachable** (HTTP error, timeout, or connection failure)
- **5 with session-minted AGSI** (all GitLab-family: gitlab.freedesktop.org, gitlab.gnome.org, gitlab.xfce.org, invent.kde.org, code.videolan.org)
- Each of the 5 AGSI-positive hosts showed only **1 distinct value** across 2 screening sessions
- **19 reachable hosts** returned 200 but contained no session-scoped AGSI

The GitLab-family hosts that showed AGSI had token fields matching the capability-token name list, but the values appeared identical across the 2 screening sessions. This may indicate:
1. The token does not rotate per session on these specific instances
2. The extraction captured only one value per session (the extraction ran 2 sessions, not 4)
3. The token value is identical when the page is served from the same geographic edge

---

## 4. Representation Loss Analysis

The experiment's primary validity threat is **V16 (representation loss)**. The screen uses `html.parser` on raw bytes with no JavaScript execution. This means:

- **Visible**: Server-rendered tokens in initial HTML (e.g., gitlab.com's authenticity_token)
- **Invisible**: JS-generated tokens (e.g., auth.wikimedia.org's wpCreateaccountToken), client-side-minted values, XHR/fetch-only gating, canvas-rendered content

This is a structural limitation of the instrument, not a scientific finding. The screen cannot detect what it cannot observe. The preregistration explicitly acknowledges this: "A non-zero prevalence here is a floor on the real prevalence, never an estimate of it."

The GATE 0 failure is therefore a **measurement-invalid outcome** (the instrument failed its own calibration), not a falsification of C-FRESHNESS. The claim remains at its pre-existing registry status.

---

## 5. Comparison with Prior C-FRESHNESS Experiments

This experiment continues the graph lane's C-FRESHNESS research program. The key difference from prior attempts is the substrate:

| Experiment | Substrate | Result |
|------------|-----------|--------|
| EXP-GRAPH-35389145821 | Local Flask mock | PASS (orthogonality at δ=0.15) |
| EXP-GRAPH-35353011131 | Local Flask mock (stochastic) | PASS (orthogonality at δ=0.15) |
| EXP-GRAPH-35375596525 | Local Flask mock (HTTP caching) | REVISE (C3 fails, measurement-confounded) |
| **EXP-GRAPH-36314193643** | **Real public HTTP** | **MEASUREMENT_INVALID (G0.2)** |

This is the first C-FRESHNESS experiment to attempt measurement on real public HTTP with a pre-use calibrated screen. The screen's failure to calibrate is primarily due to representation loss (V16), which is a known and disclosed limitation. The experiment did not fail due to a hypothesis defect; it failed because the instrument could not observe the target phenomenon on most anchors.

---

## 6. What This Does Not Mean

Per the preregistration's §13 (Non-outcomes):

- A GATE 0 failure is **not a negative about C-FRESHNESS** and does not lower its registry status
- The experiment provides **no evidence for or against** the guard's capability on real credential-free public HTTP
- The claim C-FRESHNESS remains at its pre-existing registry status (EXPERIMENTAL, per EXP-GRAPH-35389145821's PASS)
- The finding is about the **instrument's representation layer**, not about the underlying phenomenon

---

## 7. What This Does Mean

1. **The screen's detection power is substrate-dependent**. It works on server-rendered HTML (gitlab.com) but not on JS-rendered sites (wikimedia, discourse, launchpad). This is a measurement-instrument limitation, not a scientific result.

2. **The representation loss is the dominant validity threat**. Without JavaScript execution, the screen cannot observe the majority of capability tokens on the modern web. This was anticipated (V16) but its magnitude is now empirically documented.

3. **The anchor evidence quality varies dramatically**. Only CAL-POS-1 has SPIDER_CORROBORATED evidence that was confirmed on the execution date. CAL-POS-2 has SPIDER_PARTIAL evidence (token detected but distinctness never verified). CAL-POS-4 and CAL-POS-5 are A_PRIORI_CONSTRUCT assertions with no SPIDER evidence. This variation in anchor evidence quality is itself a finding about the experimental design.

4. **The frozen arithmetic certificate's preconditions are not met**. The certificate assumes ≥2 positive anchors will pass, which is not the case on this execution. The certificate is satisfiable in theory but its preconditions depend on the instrument's representation capabilities.

---

## 8. Next Actions

The frozen experiment's `director_mandate` dependencies include `frontier` and `runtime`. The unresolved questions are:

1. **JS-capable substrate**: The screen needs either a headless browser or a server-side rendering service to observe JS-generated tokens. This is a `runtime` lane substrate question.

2. **Full 4-session capture**: The 5 GitLab-family hosts showed AGSI but only 1 distinct value across 2 sessions. A full 4-session capture with body-hash comparison is needed to determine if these hosts actually rotate tokens.

3. **Credentialed probe**: Permission-boundary change (SB-01/F3) requires a credentialed substrate that no lane currently certifies.

4. **The structural invisible cell**: A stale item whose exact value is byte-identical across sessions remains unmeasurable without write verbs (SB-05).

---

## 9. Artifacts

- `raw_evidence/raw_evidence.jsonl` — 132 per-request JSONL entries with timestamps, status codes, ETags, body SHA-256 hashes, and cookie metadata
- `raw_evidence/execution_summary.json` — GATE 0 results, calibration data, screening summary
- `raw_evidence/host_screening.json` — Per-host screening results
- `/tmp/opencode/run_exp_36314193643.py` — Execution script (stdlib-only)
- `spec.json`, `prereg.md`, `request.json`, `freeze.json` — Frozen inputs

---

## 10. Compliance

This experiment followed the frozen design from `spec.json` and `prereg.md`. All validity requirements (V01–V21) were tracked. The experiment terminated at GATE 0 with `status=MEASUREMENT_INVALID`, `outcome=INCONCLUSIVE`, consistent with the frozen decision rule. No material fact was turned from interpretation into observation, and no missing measurement was converted into a negative result.
