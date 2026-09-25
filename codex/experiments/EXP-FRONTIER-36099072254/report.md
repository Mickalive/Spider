# EXP-FRONTIER-36099072254 — Report: PIVOT to WebChoreArena Heterogeneous Residual-Novelty Verification Economics (SUPERSEDE)

**Status:** MEASUREMENT_INVALID (substrate insufficient)  
**Outcome:** NOT_APPLICABLE  
**Lane:** frontier  
**Claim:** C-RESIDUAL-NOVELTY (HYPOTHESIS)  
**Experiment ID:** EXP-FRONTIER-36099072254  
**Director Mandate:** PIVOT with cognitive_reset=true, parent_handoff_disposition=SUPERSEDE, claim_id=C-RESIDUAL-NOVELTY  
**Frozen Hashes:** prereg.md=a44a265c03be... request.json=b8957021fb74... spec.json=a5d2512a4bd1...

## 1. Substrate Diagnostic (RAW EVIDENCE)

| Component | Observed | Required | Pass |
|-----------|----------|----------|------|
| browsergym | False | True | ✗ |
| browsergym.core | False | True (0.14.3) | ✗ |
| playwright | False | True (1.63.0) | ✗ |
| agentlab | False | True (0.4.2) | ✗ |
| chromium present | True | True | ✓ |
| Intel diverse manifest | exists=False families=0 | >=10 families WebChoreArena 532 + WebArena-Verified Hard 192/36 Jaccard<0.30 mean<0.15 | ✗ |
| Runtime WAL | exists=False n_non304=None | >=360 single-node HS256 sticky WAL X-Worker-Pid>=10 | ✗ |
| Graph freshness | TN=None stale_probes=0 | TN>=0.85 stale>=30 | ✗ |
| BrowserGym CDP 1280x720 | AX>10 DOM>=2000 not measured | AX>10 mean>15 std>5 DOM>=2000 | ✗ |
| WebMCP registry | coverage=None fetch=None | coverage>=70% fetch>=95% | ✗ |
| **Overall live_available** | **False** | **True** | **MEASUREMENT_INVALID** |

Artifacts:
- `artifacts/substrate_diagnostic.json` sha256=414635428e3f05d2ad724f0e4e25cbc7ebbeea9aefc1999402caa6a52397e223
- `artifacts/per_trajectory_traces.json` sha256=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- `artifacts/honest_cost_audit.json` sha256=0b8beff4e6ff247f409857527b335d36847f6e0232e1c7bb5faedd763e9a9f35
- `artifacts/freshness_gate_check.json` sha256=9e7c9a8ad20de58b354c519a1ea5fedaa5285e524b427a60aed4ab406b169cdb
- `artifacts/webmcp_registry_check.json` sha256=57d14fe50c36d734daf27144bb162cc9f19100efd7ecb4ce6947ae03be5994fe

All 9 PCs and 7 NCs are NOT_RUN (pass=false) per `result.json:controls`. Per frozen `measurement_validity[0]` and `decision_rule`, any PC/NC failure triggers MEASUREMENT_INVALID — no SURVIVES/FALSIFIES inference is justified.

## 2. What Was NOT Run (Frozen Design Integrity)

The frozen heterogeneous gate required:

- **Heterogeneous substrate:** WebChoreArena 532 tedious/memory tasks (massive-memory, cross-site, long-horizon human 50.2% vs GPT-5 48.3% unsaturated) plus WebArena-Verified Hard 192/36 combined manifest >=10 families pairwise canonical bigram Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 at 1280x720 CDP AX>10 mean>15 std>5 DOM>=2000, header+body+query+auth plus cross-site memory/tool-use tagged, deterministic seed 35725763380, TRAIN-only vocab isolation 0 leakage, trajectory-grouped holdout whole trajectories never indexed, controlled novelty 0/25/50/75/100% via family-resource holdout + memory stratification.
- **Honest cost pipeline:** Per-trajectory hard-reset sum counters resolve+bind+verify+freshness+browser_steps instrumented integers TAU0.30 topology-gated + freshness TN>=0.85 gate, no jitter/n*3200/f*6.0, real TF-IDF TAU0.30 over train-A with softmax temp 0.15 + deterministic hashlib.sha256(task_id) jitter 0.02 UNKNOWN<0.80, correctness deterministic exact key-set equality after alias resolution, counted build cost frozen before outcomes, 5000 family-stratified bootstrap + 5000 family-block permutation + 5000 global permutation, trajectory-grouped CIs, per-stratum N>=30 per-family per-stratum N>=3 coverage>=8/10 pooled>=40.
- **Baselines:** B-COLD-LLM, B-FLAT-RAG-K5 (TAU0.30 strong), B-SPIDER-RESIDUAL (primary), B-WEBMCP-TOOL-BYPASS (conditional >=70% coverage), B-RANDOM-GATE — all paired trajectory-grouped with identical acceptance predicate and honest counters.
- **Decision thresholds:** S1 rho_novelty>=0.60 lower>0.40 p<0.05, S2 pooled |rho_length|<0.20 upper<0.25 p>=0.05, S3 per-stratum |rho_length|<0.20 upper<0.30, S4 calibration precision>=0.85 false_accept<=0.10 ECE<=0.15 upper<=0.18, S5 Pareto saving>=25% lower>15% dominance vs cold and vs RAG k5 at f=10 and f=100 with +-50% build sensitivity strict lower>0, S6 honest gap>0.35 and |rho_proxy|<0.60 and |rho_shuffled|<0.20 centered.

**None executed.** Per `spec.json:measurement_validity[0]` frozen clause: *"If BrowserGym 0.14.3 CDP or Intel heterogeneous manifest unavailable or n_non304 insufficient declare live_available=false and MEASUREMENT_INVALID diagnostic without falsifying claim — do not substitute synthetic disjoint alphabets (36-family TAU0.30 Jaccard 0.0 gate) as heterogeneous evidence."* This prohibition was obeyed. Synthetic 36-family disjoint-alphabet results (EXP-FRONTIER-36042599040) are not reported here as heterogeneous evidence.

## 3. Observations vs Interpretations (Separation)

**RAW EVIDENCE (observations):**
- Substrate diagnostic JSON with live_available=false, manifest_families=0, browsergym false, playwright false, n_non304 null
- Empty per_trajectory_traces [] and honest_cost_audit trajectories_audited=0
- Freeze hash verification PASS for all three frozen files vs freeze.json
- Chromium binary present at /usr/bin/chromium but BrowserGym stack not installable (no browsergym/playwright/agentlab modules, no Intel manifest directory, no /tmp/spider-runtime/shared.db)

**DERIVED MEASUREMENTS:** None (no rho, no ECE, no M_total computed; metrics null in result.json)

**INTERPRETATION:** MEASUREMENT_INVALID prevents any claim about C-RESIDUAL-NOVELTY on heterogeneous gate. The prior bounded evidence remains the only valid evidence (see §4).

## 4. Prior Evidence Preserved (Codex Lineage)

- **EXP-FRONTIER-36042599040:** Valid FALSIFIED-IN-SETTING synthetic TAU0.30 orthogonal gate (PASS all 11 PCs/NCs): rho_novelty 0.4837 CI[0.410,0.552] <0.60, pooled |rho_length| not decoupled per S3, ECE 0.216 >0.15 upper>0.18, RAG dominance false at f=10/f=100 — validly non-Pareto under QCR with honest per-trajectory hard-reset counters on 36-family Jaccard 0.0 disjoint alphabets. Bounded to synthetic gate only.
- **EXP-FRONTIER-36052053591 lineage & 17-deep alias tunnel:** Bounded at 21/40=0.525 Wilson [0.352,0.648] pooled 0/10 mixed triple-channel (retrieval-diversity ceiling).
- **EXP-FRONTIER-36097242687 (parent):** MEASUREMENT_INVALID diagnostic live_available=false 0.0s, substrate absent — preserved as parent handoff sha 0fe3c2b5d610d4da20e9b49fb35f2033f858ff9a55e22e8cdc66f2f9ee769de8 with SUPERSEDE disposition; Director PIVOT cognitive_reset true continuity maintained.
- **4 consecutive MEASUREMENT_INVALID deterministic compilation bypasses** bounded at 21/40 before pivot.

C-RESIDUAL-NOVELTY remains **HYPOTHESIS** in `codex/claim_state.json`. No promotion to EXPERIMENTAL/VALIDATED/PRODUCT_CORE is authorized by this packet.

## 5. Validity Notes & Threats

- Measurement validity precedes interpretation per SPIDER_MASTER_PROMPT. No synthetic substitution was made.
- Representation loss disclosed: WebChoreArena cross-site tool-use OpenAPI coverage unknown (<70% would stratify not gate), DOM style/layout and cross-site auth state discarded beyond freshness gate, guard set limited to freshness+URL+DOM precondition.
- Prior tautological metrics (rho 0.8998/0.8117 saving 34.53%) are not evidence per prereg §10.
- Agent priors (5 priors in director_mandate.agent_priors_used) labeled priors not SPIDER evidence.
- Single-node health gate n>=360 must PASS before distributed n>=800 f=100 authorization per portfolio_assessment.

## 6. Product Consequences (Frozen)

- **If SURVIVES (not observed):** Would demonstrate honest residual-novelty verification economics tracks residual novelty not length with calibrated abstention and Pareto >=25% saving vs cold and strict dominance vs flat RAG k5 at f=10/100 (and vs WebMCP where coverage>=70%) on heterogeneous WebChoreArena where compressible structure exists — breaking both 21/40 alias ceiling and synthetic TAU0.30 non-Pareto, advancing C-RESIDUAL-NOVELTY HYPOTHESIS->EXPERIMENTAL heterogeneous-gate-passed and authorizing cross-site replication with Runtime distributed n>=800 and Intel larger manifest before PRODUCT_CORE.
- **If FALSIFIED-IN-SETTING (not observed):** Would validly park heterogeneous residual-novelty verification economics even where compressible structure exists and trigger per Director comparative_reasoning to PIVOT frontier to barrier-physics (Physics lane on live BrowserGym) or per-value alias via Runtime diverse substrate.
- **Actual MEASUREMENT_INVALID:** Neither. Frontier C-RESIDUAL-NOVELTY remains HYPOTHESIS pending substrate. No product promotion. Do not cite this diagnostic as falsification.

## 7. Required Fixes (Smallest Next Actions)

1. **Intel lane:** Produce WebChoreArena 532 tedious/memory + WebArena-Verified Hard 192/36 shared manifest with >=10 families Jaccard<0.30 mean<0.15 product-subtree anchored depth>=2 at 1280x720 CDP AX>10 mean>15 std>5 DOM>=2000 deterministic seed 35725763380 TRAIN-only vocab isolation (path: research/intel/diverse_site_manifest.json or data/webgym_292k)
2. **Runtime lane:** Deploy health-gated single-node HS256 sticky WAL at /tmp/spider-runtime/shared.db with n_non304>=360 X-Worker-Pid>=10 If-None-Match/304 proxy_cache HIT, then distributed n>=800
3. **Graph lane:** Validate freshness TN>=0.85 with >=30 stale probes on WebChoreArena cross-site sessions for TAU0.30+freshness-gated bailout
4. **Environment:** Install browsergym-core 0.14.3 + playwright 1.63.0 + agentlab 0.4.2 with system chromium for 1280x720 CDP trajectory capture
5. **Re-execute:** Run frozen `research/frontier/run_execute_36099072254.py` (to be created from spec/prereg) exactly with 5000 family-stratified bootstrap + 5000 block-permutation + 5000 global permutation TAU+freshness-gated and honest per-trajectory hard-reset counters

Upon all 9 PCs and 7 NCs PASS, re-evaluate S1-S6 per frozen decision_rule.

## 8. Reproduction

```bash
python research/frontier/run_execute_36099072254.py  # after substrate fixes
# diagnostic mode (current):
python /tmp/run_diag2.py
cat research/experiments/EXP-FRONTIER-36099072254/result.json | python -m json.tool
cat research/experiments/EXP-FRONTIER-36099072254/artifacts/substrate_diagnostic.json
```

---

*Lane charter:* frontier — search outside current solution basin for high-upside falsifiable mechanisms (allowed roots research/harness, research/frontier only)  
*Parent:* EXP-FRONTIER-36097242687 handoff.json sha 0fe3c2b5d610d4da20e9b49fb35f2033f858ff9a55e22e8cdc66f2f9ee769de8 — MEASUREMENT_INVALID continuity preserved, SUPERSEDE disposition  
*Grandparent:* EXP-FRONTIER-36042599040 FALSIFIED-IN-SETTING rho 0.4837 valid synthetic 36-family TAU0.30  
*Codex:* codex/claim_state.json C-RESIDUAL-NOVELTY HYPOTHESIS  
*Portfolio:* only C-MEAS-VALID VALIDATED via EXP-RUNTIME-36094450333 distributed plain-HTTP; all 9 other claims HYPOTHESIS/MEASUREMENT_INVALID
