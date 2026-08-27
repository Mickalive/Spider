# INTEL AUDIT — CYCLE 7, RUN 32908028297 (repair round 0)

**Mechanism:** `unbrowse-route-capture-replay-ladder` — clean-instrument confirmation round 3 under the Director's CAP.
**Object audited:** Reproducer workspace `/tmp/spider_intel_repro` @ `aed19d1` (branch `cycle/intel/cycle7/repro`, base = accepted Intel tip `9f9a757`), Scout workspace `/tmp/spider_intel_scout` @ `76d4e8f`. Read-only audit; no reproduced file was edited.
**Reproducer verdict under audit:** frozen rule evaluated EXACTLY ONCE → `INCONCLUSIVE`, measurement claimed VALID, stop rule not triggered.

---

## 0. Gate summary

| Item | Value |
|---|---|
| Gate | **PASS** |
| Mechanism status | **INCONCLUSIVE** |
| safe_to_integrate | true (documentation + observation-tier facts only; NOTHING enters `VALIDATED_MECHANISMS`) |
| Claim tier ceiling | OBSERVATION_TIER_ONLY (clause-scoped facts inside an INCONCLUSIVE verdict) |
| Required fixes | none |

A valid measurement that lands INCONCLUSIVE by its own frozen rule is a successful audit object. This is the second run in lane history in the contemplated "PASS documenting an honestly measured non-positive outcome" class (cycle 6 was MEASUREMENT_INVALID; this cycle 7 is VALID-but-INCONCLUSIVE) — they are different classes and must not be conflated: this round's instruments demonstrably worked and produced interpretable per-clause data.

## 1. Provenance chain verification

- **Scout → candidate:** Scout snapshot commit `76d4e8f`; `state/intel_candidate.json` sha256 `7a772973…55bf9` byte-identical between Scout workspace and repro tree (recomputed both sides). Mission source `state/intel_loop.json` priority 1 matches what was executed (clean-instrument confirmation, five open questions, CAP + stop rule acknowledged).
- **Freeze before outcomes:** prereg frozen at commit `7a1c878` (2026-08-26T00:13:41Z) with full pre-freeze activity ledger (§11), NON-EVIDENCE proof-pass artifacts committed in the same commit and labeled `NON-EVIDENCE` (`marked` field verified). The frozen region of the prereg is **byte-identical from the freeze commit to HEAD** (verified by git extraction and separator-split comparison); only errata E1/E2 were appended below the separator.
- **Attempt ledger coherent with git clock:** attempt 1 launched 00:14Z, voided pre-evidence at E1 (`8fe298e`, 00:20:31Z; side effects disclosed without euphemism); committed evidence timestamps begin 00:20:36Z (availability log ts_ms 1787703636872 ≈ 00:20:36Z), i.e., immediately after the E1 restart commit — physically coherent. E2 wiring repair committed 00:41:18Z; single guarded evaluator invocation logged 00:41:41Z (23 s later); final commit `aed19d1` 00:47:16Z.
- **Frozen implementation hashes:** all 24 rows verified against the working tree (23 section-16 rows + the two declared supersessions: `run_all.py` E1 row, `evaluate_rule.py` E2 row). 24/24 match, zero undeclared deltas.
- **Evidence sealing:** `SHA256SUMS.txt` verifies clean 38/38. Improvement over the cycle-6 nit: the stray `.rb_cap_path` scratch file is now INSIDE the manifest. Remaining outside the manifest by structural necessity: `decision_rule_evaluation.json` (written by the once-only guarded invocation after sealing) and `evaluator_invocations.log`/`evaluator_invocations.json` (appended by the guard). Both are provenance-nit class only; the evaluation output's integrity is covered by my byte-exact rerun (§3).

## 2. The two post-freeze repairs (adversarial focus)

This cycle applied TWO post-freeze mechanical repairs, both disclosed with attestations. I attacked both.

**E1 (voided attempt 1, pre-evidence):** P2 drove discovery-time replay with empty params on petstore — a never-executed path that repair R3 exposed. Fix aligns P2 to each task's own call sequence. Verified properties: killed before any A/B/C/D pass row existed (no passes_raw in tree until final commit); partial artifacts deleted uncommitted; collection restarted FROM SCRATCH (committed discovery timestamps postdate the E1 commit); delta touches P2 discovery checks only, cannot affect C2/C3 economics arms; direction monotone-honest (it lets frozen C1 execute rather than guaranteeing an artifact verdict).

**E2 (evaluator filename wiring c6→c7, pre-first-invocation):** without the fix, clause 1 gated on `_c6` filenames absent from the c7 REQUIRED list ⇒ `c1={}` ⇒ mechanically forced FAILED_TO_REPRODUCE regardless of evidence. Verified properties: no `decision_rule_evaluation.json` existed anywhere before `e43a87d` (it first appears in `aed19d1`); invocation log contains exactly one EXECUTED entry, zero REFUSED entries, timestamped after the E2 commit; the committed output reproduces byte-equivalently from the POST-E2 code (a pre-E2 secret run would have produced a different file that then blocked the guard); the fix cannot manufacture advantage — it changes which filenames clause 1 reads. Residual caveat: git cannot prove the absence of an unlogged direct `evaluate_rule.py` execution bypassing the guard; this is the same inherent single-runner attestation class already accepted in cycles 5–6 ("attestation-based freeze timing"). It travels as a caveat, not a blocker. The Reproducer itself flags the accumulating observer-drift pattern (two mechanical repairs in one cycle, three rounds across the lineage) and correctly demands independent recomputation before any positive reading — which this audit then performed.

## 3. Independent recomputation (all headline numbers)

Second-path script: `results/intel/audit/CYCLE_32908028297_auditor_recompute.py` — **57/57 checks PASS**, including:

**C1 multi-host discovery (PASS 4/4 confirmed).** All four host-tasks: both genuine completions accepted `[True,True]`, ≥1 route learned (1/1/2/7 — demoblaze learned all seven API routes incl. login/addtocart/viewcart), discovery-time replay REPLAY_OK + equivalent. Includes the pivotal spec-less session-token SPA cell.

**C2 replay economics (per-task 4/4 PASS confirmed; family gate FAIL confirmed mechanical).**
From raw interleaved pairs (n=5 valid pairs/task, warmups excluded but committed, B actions == 0 everywhere, B equivalence on ALL pairs):

| Task | med A ms | med B ms | speedup | wins |
|---|---|---|---|---|
| T_HTTPBIN_FORM | 795.4 | 224.7 | 3.54× | 5/5 |
| T_HTTPBIN_COOKIE | 616.6 | 231.5 | 2.66× | 5/5 |
| T_PETSTORE_FIND | 2531.5 | 331.3 | 7.64× | 5/5 |
| T_DEMOBLAZE_CART | 7133.0 | 341.3 | 20.90× | 5/5 |

BCa log-ratio CIs reproduce **exactly** under their frozen deterministic implementation (LCG seed 20260826) AND agree to <0.02 in log-space under my own independently written 200k-resample bootstrap with a different RNG stream; every ci_low > 0. LOHO stable in all three exclusions (10/10 and 15/15 paired wins).
**Zero-power family gate CONFIRMED BY MY OWN ARITHMETIC:** the smallest achievable exact one-sided sign-test p at n=5 is 2⁻⁵ = 0.03125; Holm's smallest-of-four multiplier is 4; adjusted-p floor = 0.125 > 0.05 for ANY possible data. As frozen (structure inherited unchanged from cycle-6 §14, where it was never reached because invalidity fired first), the family gate could not pass under any outcome this design could produce. The Reproducer discovered and disclosed this post hoc, changed nothing, and let the mechanical verdict stand: per-task gates passed, `holm_family_all_significant=false` ⇒ clause FAIL ⇒ verdict INCONCLUSIVE. This is correct handling of a preregistration design defect: post-outcome repair would have been forbidden retuning. Consequence: **no cross-host economics advantage claim exists from this run, and REPRODUCED_USEFUL was unreachable by construction.**

**C3 capture-value-over-declaration (PASS confirmed, interpretation bounded).** Demoblaze B 30/30 REPLAY_OK vs D 0/5 SCHEMA_MISMATCH — counts, codes and rates recompute exactly. Internal control present: petstore-D (public contract) 5/5 descriptive, so the D machinery is not broken per se. **Auditor bounding (new finding):** tracing `run_D_pass` + `SpecClient.run`, D's demoblaze failure occurred at strict response-body validation (`SCHEMA_MISMATCH "non-json body"`) AFTER the server had already accepted its literal-body request (status 2xx — any 4xx would have produced AUTH_FAIL/HTTP_ERROR instead). So on THIS cell the measured differentiator is the frozen response-representation asymmetry (B's predeclared P-WRITE tolerance of non-JSON-labeled writes vs D's strict JSON validation) meeting the audited environment fact (api.demoblaze.com cart-write answers 200 text/html), NOT superiority of captured parameterization over declarations on credential/token lifecycle — that quantity was not isolated here. D-independence protocol verified structurally (dedicated third-capture manifest `T_DEMOBLAZE_CART_dspec_manifest.json`, note field, separate recorder; generated spec contains all seven endpoints, so D-failure is not capture starvation).

**C4 replica-scoped mutation detection (PASS confirmed).** Sealed-schedule chain verified end-to-end: deterministic rebuild hash == prereg-frozen value == value recorded by P5 == revealed-steps hash (`276132df…`). Execution order matches the sealed schedule step-for-step. M1/M2/M3/M5/M6 each fired SCHEMA_MISMATCH ×2; M4 behaved exactly as predeclared blind (REPLAY_OK ×2); benign FPR 0/25 with Wilson 95% upper 0.1332 ≤ 0.15 (recomputed); pristine rechecks OK. Replica-scoped ONLY.

**C5 lifecycle core (FAIL confirmed, attribution confirmed environment-side).** The mandated cooldown check and both Q1 booking creations were refused HTTP 418 (persistent write protection documented since the PRE-FREEZE probe); Q1 fails via the pre-frozen honest-clause-failure fallback. Q2 corrupted-auth negative control PASSED (AUTH_FAIL, nothing presented); positive control structurally impossible (null, honestly reported). Q3 rewind compliance, Q4 deleted-record absence surfacing (HTTP_ERROR, deleted=true), pointer-only assertion: all PASS. Checker's empty escalation counters are downstream consequences of Q1 never reaching replay stage. Parameterization-to-new-ids therefore remains UNTESTED this round — genuinely, not instrumentally.

**Invalidity conditions:** none. 11 required files present; 5/5 hosts up at start and end supplement; zero tasks below the pair floor; schedule_hash_verified True. Ladder event stream: 160/160 REPLAY_OK, zero substitution surfaces. Selftest rerun in the audit environment: 72/72 PASS (browser import stubbed; unit tests offline). Import scan: stdlib + playwright + SPIDER's own audited cycle-6 modules only — clean-room lineage holds.

**Evaluator integrity:** reran the committed evaluator code on a COPY of the evidence: output key-equivalent byte-for-byte with the committed `decision_rule_evaluation.json`; verdict mapping followed mechanically.

## 4. External source claim

arXiv:2604.00694 re-fetched LIVE this session (fourth consecutive independent auditor verification): "Internal APIs Are All You Need: Shadow APIs, Shadow APIs…" — Tham / Mac Gregor Garcia / Hahn, submitted 2026-04-01; abstract headline verbatim (94 domains, warmed cached 950 ms vs Playwright 3,404 ms, 3.6× mean / 5.4× median, sub-100 ms well-cached routes, x402 tiers). The vendor headline remains OFFICIAL_CLAIM, untested by this run and untested by anyone independent (Scout: citationCount = 0 again this cycle, plus a NEW recorded blog-vs-paper numeric inconsistency — both OFFICIAL_CLAIM tier). Faithful reconstruction of the external mechanism family: confirmed (capture→filter→extract/parameterize→replay→escalate, plus SPIDER's own decisive spec-null comparator, tested clean-room).

## 5. Confounder attack summary

- **Leakage/target integrity:** none found. Equivalence oracles are acceptance modes frozen pre-outcome (deep_canonical / volatile-public-data / shared-demo-DB shape oracle); warmups excluded symmetrically; B charged its full call-sequence http_txs (login bootstrap untimed IDENTICALLY across arms per frozen §6 — symmetric treatment).
- **Budget/matching:** A and B interleaved per rep in seeded block order (block_order.json == seeded shuffle, seed 20260826); n=5 matched pairs/task; B extras (to 30) occur AFTER the paired block and feed only C3's rate, as frozen.
- **Baseline strength:** C privileged-docs null ran where docs exist (5/5/5, demoblaze honestly NULL-celled); D generated-spec null is the decisive comparator with a public-contract internal control (petstore-D 5/5). The knowledge-privileged bare-HTTP null from cycle 5 remains the binding latency baseline: nothing here overturns "no latency advantage over raw HTTP".
- **Hand-authoring:** intent maps and addressing ground truth disclosed; prefix column structurally disabled and EXCLUDED from claims (artifact_confirmed=true), continuing the cycle-6 precedent of exclusion-over-silent-reporting; addressing arm descriptive only (exact 5/8, lexical 5/8).
- **Selection pressure:** examined and judged low-risk this round: the headline verdict leans NEGATIVE-leaning-neutral (INCONCLUSIVE despite strong per-task numbers), the two repairs ran AGAINST convenience (one voided a whole attempt, one prevented a guaranteed artifact verdict that would have falsely triggered the STOP RULE), and every defect was disclosed without euphemism.
- **Environment confounds:** restful-booker 418 write-protection is environment-side and pre-disclosed; demoblaze HTML-labeled write endpoint is an audited standing fact now shown to decide the D-arm outcome (see §3 C3 bound); demoblaze shared-DB contamination contained by arm-namespaced uuids + shape-only oracle (D 0/5 vs B 30/30 separation consistent with containment); cleanup executed after each block (removed=0 — namespacing made it a no-op; residue disclosure unchanged).
- **Timing hygiene:** pacing outside timers, perf_counter inside, same clock semantics both arms (design-frozen); wall_ms distributions organic (no quantization artifacts); quiescence values frozen in prereg §6.

## 6. What this run establishes — and what it does not

Established at OBSERVATION tier inside a valid measurement (each bound below is binding):
1. Clean-instrument restoration SUCCEEDED: the four audited cycle-6 instrument defects plus the two structural call-site defects were repaired and the full pipeline P0–P7 executed end-to-end producing interpretable data — the exact purpose of this capped round.
2. C1 PASS 4/4: multi-host capture→extract→parameterize→discovery-replay reach, including the spec-less session-token SPA cell, within scripted sandbox scope.
3. Per-task economics observations (speedups above) exist as measurements but are locked inside the INCONCLUSIVE verdict by the zero-power family gate; they neither extend nor replicate the cycle-5 result in accepted-knowledge terms.
4. C3 PASS mechanically, bounded per §3: declaration-insufficiency AS FROZEN on the spec-less cell; response-representation dimension isolated; token-lifecycle superiority NOT isolated.
5. C4 PASS replica-scoped only.
6. C5 environment-blocked: lifecycle parameterization-to-new-ids and auth positive control remain open questions.
7. Natural-TTL: window-1 fresh anchor committed; window 2 clock-gated to ≥ 2026-08-26T22:05:30Z; ALL staleness claims withheld (never enters verdict — structure honored).

NOT established: cross-host economics advantage; replication/strengthening of cycle-5; staleness/drift behavior on live sites; vendor headline support; anything about LLM-agent operation or production targets.

## 7. Continuation semantics (Director input, not Auditor decision)

The stop rule did NOT fire (this is not a second MEASUREMENT_INVALID). The report's §10 framing is accurate: INCONCLUSIVE sits outside both the CAP close-set and the stop-trigger, so continuation requires an explicit Director decision between (approximately): (a) one more narrowly-scoped preregistered attempt whose statistics plan has reachable power (the zero-power finding is precisely the kind of "materially new" design fact the CAP contemplates — but the Director should weigh the observer-drift pattern against it), or (b) integrating clause-scoped observation-tier findings and closing the mission with open questions routed to queued candidates. If (a): the new prereg MUST derive its family gate from reachable significance arithmetic BEFORE freezing (e.g., sign tests need n≥8 for raw p<0.05·(1/4)… actually n≥10 for p≤0.00098? No: exact binomial n=10 all-wins p=0.00098, Holm-adjusted ×4 still <0.05 — such arithmetic must be shown in-prereg), and SHOULD consider isolating the token-lifecycle question from the response-policy question in the D comparator.

## 8. Claim-by-claim status table

| CLAIM (source) | EVIDENCE | RECOMPUTATION | STATUS | MAX DEFENSIBLE WORDING |
|---|---|---|---|---|
| Measurement VALID, zero invalidity | decision_rule_evaluation.json, availability logs, SHA256SUMS | 38/38 manifest, 11/11 required files, 5/5 hosts, 0 sub-floor tasks, hash chain | VERIFIED | "Valid measurement, frozen rule evaluated exactly once" |
| Verdict INCONCLUSIVE mechanical | decision_rule_evaluation.json | byte-equivalent rerun; mapping traced in code | VERIFIED | Binding; may not be relabeled success or failure |
| C1 PASS 4/4 | disc_meta_c7, discovery_checks_c7, stores | 57-check script | VERIFIED (observation tier) | Multi-host discovery reach incl. spec-less SPA cell, scripted sandbox scope |
| C2 per-task 4/4 + family FAIL | passes_raw.json | medians/speedups/wins/CI exact; Holm floor 0.125 proven | VERIFIED | Observations inside INCONCLUSIVE; NO advantage claim |
| Family gate zero power | prereg §10 inherited; my arithmetic | min adjusted p = 0.125 ∀ outcomes | VERIFIED | Preregistration design defect, disclosed post hoc, not measurement invalidity, not falsification |
| C3 PASS | passes_raw D/B demo rows | 30/30 vs 0/5 exact; petstore-D 5/5 | VERIFIED, INTERPRETATION BOUNDED | Declaration-insufficiency AS FROZEN; failure at strict response validation after server acceptance; response-representation dimension isolated; token lifecycle NOT isolated |
| C4 PASS replica-scoped | mutation_arm.json, revealed schedule | hash chain 4-way equal; codes/FPR/Wilson exact | VERIFIED | Replica-scoped sensitivity + 0/25 FP Wilson≤0.1332; no live-site claim |
| C5 FAIL environment-side | probe_events_rb.json | 418 refusal chain, Q2-neg/Q3/Q4/pointer PASS | VERIFIED | Environment-blocked; parameterization-to-new-ids untested |
| TTL window-1 anchor, window-2 pending | ttl_window1.json, protocol | timestamps coherent (+24h eligibility) | VERIFIED | Staleness claims withheld |
| Vendor headline OFFICIAL_CLAIM | arXiv live fetch | verbatim match | VERIFIED (as OFFICIAL_CLAIM) | Never citable alongside SPIDER results |

## 9. Residual caveats that travel with this audit

1. Outcome-blindness of the two post-freeze repairs is attestation-plus-artifact-supported, not provable from git alone (single-runner inherent limit).
2. Observer-drift pattern across rounds 6→7 is real and must temper any future positive reading of this lineage until a clean single-shot run with a powered rule completes.
3. `decision_rule_evaluation.json` + `evaluator_invocations.json` sit outside the sealed manifest (structural; integrity covered by byte-exact rerun).
4. Cleanup efficacy was a no-op this run (removed=0); ethics residue disclosure from cycles 6–7 stands.
5. Audit-environment selftest used a stubbed playwright import (offline units only); no live collection was performed by the Auditor, deliberately.

## 10. Maximum defensible wording (binding)

See `maximum_defensible_wording` in `results/intel/audit/CYCLE_32908028297_INTEL_GATE.json`. In short: an honestly measured, valid, single-shot INCONCLUSIVE with verified clause-level observations; zero accepted-mechanism content beyond the already-binding cycle-5/cycle-1 wordings.

— INTEL_AUDITOR, run 32908028297, repair round 0, 2026-08-26
