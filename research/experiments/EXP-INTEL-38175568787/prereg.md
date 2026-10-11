# EXP-INTEL-38175568787 preregistration

Lane: `intel` — design_contract_version 2
Status: **DESIGN — NOT YET FROZEN**

Director mandate: `research/experiments/EXP-INTEL-38175568787/request.json#director_mandate` (typed `allocation_directive`; `allocation: NEW`; binding target claim `C-LLM-INHERIT`; `comparative_reasoning.legacy_classification: LEGACY: NO_MATCH` with the limitation that the 21.97 MB pre-2.0 archive was screened only through the compact brief/index).
Refined into the smallest rigorous falsifiable probe (one bounded capability ladder + one non-gating provisioning census + one conditional external-comparator readiness table), **not** a substitute objective and **not** a re-run of the spent 3B–8B prompt ablation.
Predecessor chain: EXP-INTEL-37973264582 (grandparent; endpoint/comparator obtainability, Gate 2 FAIL, `DESIGN_COMPROMISED`) → EXP-INTEL-37982024058 (frozen runner + base fixture; FALSIFIES; audit PASS) → EXP-INTEL-38164607941 (parent; goal/schema prompt ablation; FALSIFIES; audit PASS) → this packet.
Superseded pre-freeze siblings (NOT evidence): EXP-INTEL-38123995594 (the spent 3B–8B prompt ablation, executed as the parent) and EXP-INTEL-38013769440 (broadened capability-ceiling census over 0.5B/3B/7B Qwen + the anonymous proxy). Neither froze; neither is cited as evidence.
Product/runtime context (parallel, not a dependency): `research/portfolio/PROGRAM_AUDIT_2026-10-10.md` — B1 (shipped carrier) and B2 (non-ceiling dynamic-range task bank) are open; B3 (a capable same-model endpoint for the gated four-arm benchmark COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER) is the target of this packet.

---

## 1. Question

Which hosted/capable model class (or alternative credential-free path) can clear the minimal multi-step Web-agent bar required by readiness condition (3) / blocker B3 of the gated four-arm benchmark — given that the credential-free local 3B–8B Qwen class failed even with the goal/schema prompt (EXP-INTEL-38164607941, FALSIFIES) — and, if no capable same-protocol endpoint can be provisioned, what is the exact credential/operational blocker?

Refinement into the smallest rigorous falsifiable probe (three components, one decision):

1. **Capability ladder (primary, gating).** Measure predeclared credential-free local classes that the parent handoff left explicitly untested (unknown U-03): a **larger same-family** class (M-14B-QWEN) and a **different-family** class (M-8B-LLAMA), under the byte-frozen minimal protocol and the frozen **P-TREAT-GOAL-SCHEMA** prompt, against the inherited bar `task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6` over the 5 frozen seeded episodes.
2. **Provisioning census (secondary, non-gating).** Record, per predeclared hosted provider, whether a same-protocol endpoint is provisionable and if not the exact credential/operational blocker (missing environment variable, HTTP status, or operational cap). This answers the mandate's blocker clause observationally.
3. **External-comparator readiness table (conditional, non-gating).** Enumerate the strongest externally published inheritance/memory systems (QCR arXiv:2608.12847, compile-and-execute arXiv:2604.09718, site-memory/ColorBrowserAgent) as `CANDIDATE_NOT_EVIDENCE` with their reported numbers, denominators and reproduction prerequisites.

The Director's binding strategic question is component (1) plus the blocker clause (2); component (3) is the mandate's explicitly required conditional deliverable. No external vendor number is used as SPIDER evidence.

## 2. Hypotheses

- **H1 (capability).** At least one predeclared credential-free candidate class not previously tested — M-14B-QWEN (Qwen2.5-14B-Instruct Q4_K_M; scale beyond the tested 8B ceiling) or M-8B-LLAMA (Meta-Llama-3.1-8B-Instruct Q4_K_M; non-Qwen family) — clears the inherited bar under the frozen minimal protocol and P-TREAT-GOAL-SCHEMA, thereby satisfying readiness condition (3) at mechanism level with a factory-provisionable credential-free local endpoint.
- **H2 (provisioning).** No hosted same-protocol model endpoint is provisionable in this factory without a human-issued credential: every predeclared hosted provider is credential-gated (exact missing environment variable recorded) or unreachable, and the only reachable credential-free hosted path (Pollinations gpt-oss-20b) is operationally capped (reasoning-only content, ~197 completion-token cap, intermittent HTTP 402, no model pinning/SLA).

## 3. Falsifier

**H0 (bounded negative).** No predeclared credential-free candidate clears the bar — every COMPLETE candidate cell has `task_success_rate < 0.6` — AND the census finds no `PROVISIONABLE_CREDENTIATED` hosted provider, so no currently-provisionable same-protocol endpoint can drive the minimal multi-step Web-agent test and readiness condition (3) is `NOT_SATISFIED`. The gated four-arm benchmark must then be re-scoped (drop the same-model external published-baseline anchor in favour of internally re-run comparators on a task bank with a dynamic-range certificate, or obtain a hosted credential with pinning/SLA, or pursue a different model class).

FALSIFIES is asserted only over the COMPLETE, predeclared credential-free local candidate set; it is a **capability bound on the tested classes and quantisation**, not a global rejection of `C-LLM-INHERIT` and not a closure of hosted frontier classes (which remain `UNRESOLVED`-by-blocker). A candidate whose GGUF fails digest verification or load is `UNMEASURED_LOAD_FAILED`; a candidate whose treatment PC gate fails is `UNMEASURED_TREATMENT_PC_FAILED`; neither is counted as a capability failure. If no candidate is COMPLETE, the packet is `MEASUREMENT_INVALID`, not a scientific negative.

## 4. Substrate, task and protocol

### 4.1 Frozen task and harness (inherited byte-for-byte)

The task, page fixture, GBNF grammar, user template, sampling schedule, seeds, parsing and scoring are inherited from `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (file sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`), executed by the **frozen parent runner** `research/intel/run_exp_37982024058.py` (file sha256 `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`):

- Task: single page with a `#reveal-btn`; clicking it hides the button and makes `#target` visible with text `TARGET-42`; the agent must click then answer `TARGET-42`. `task.max_steps_per_episode = 5`, `task.threshold_target_text = TARGET-42`.
- Frozen sampling: `temperature=0.0`, `max_tokens=512`, `n_ctx=2048`, `llama_seed=42`, episodes seeded `base_seed(42) + episode_idx` ⇒ seeds 42–46. `n_threads=4`. `chat_format` is a per-candidate load parameter (changed by the overlay; section 4.2).
- Frozen parsing (`parse_action`): the whole completion must be valid JSON matching `{action: "click"|"answer", selector?: str, text?: str}` with the action-appropriate required field; any error/violation = parse failure.
- Frozen scorer (`run_episode`): mechanical reveal detection (`#target` visible with text `TARGET-42`) AND a terminal `answer` action whose text equals `TARGET-42` ⇒ `task_success=true`.
- Frozen clearing threshold: `task_success_rate_min = 0.6`, `parseable_action_rate_step1_min = 0.6`, `episodes = 5`.

### 4.2 The manipulated variable: deterministic per-candidate config overlay

The ONLY varied dimension between candidate cells is the model weights (plus the family `chat_format` required to load them). For each candidate we materialize a per-candidate `raw/harness_config.json` by loading the frozen base config bytes (`7aba9dc8…`) and replacing **only**:

- `prompts.system` ← the frozen **P-TREAT-GOAL-SCHEMA** string (sha256 `36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716`):
  `You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<id>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.`
- `sampling.chat_format` ← `qwen` for M-14B-QWEN, `llama-3` for M-8B-LLAMA.
- `candidate_models_frozen` ← the single frozen candidate entry (section 4.4).

Every other config key (`positive_control`, `null_control`, `random_baseline`, `clearing_threshold`, `gbnf_grammar`, `prompts.user_template`, `prompts.positive_control_probe`, `task`, `sampling` other keys, `metrics_stable_ids`, `action_schema`) is inherited byte-for-byte from the frozen base file. The overlay changes exactly 3 keys and is a pure deterministic transformation of the bound base fixture, so no outcome-relevant key is unbound at freeze time.

**Materialization path (binding).** The frozen runner's `load_config(outdir)` reads exactly `os.path.join(outdir, "raw", "harness_config.json")` (read from the frozen runner). Each per-candidate config is materialized at **`<per-candidate-outdir>/raw/harness_config.json`**, where `<per-candidate-outdir>` is the `--outdir` passed to the frozen runner for that candidate; there is no `--config` flag for model cells. A provenance mirror is recorded at `configs/config_<candidate_id>.json` (deterministic name; both sha256 recorded in `provenance.json`). EXECUTE must verify the object-level diff between the materialized config and the frozen base config is confined to the 3 keys above.

The section-4.2 overlay materializer is provided by the thin driver `research/intel/exp_38175568787_materialize.py` (Authored-at-EXECUTE; bound by this section; sha256 recorded in `provenance.json`; parent precedent: `exp_38164607941_materialize.py`).

**Prompt provenance.** The treatment string is the grandparent harness-goal/schema prompt (derived from `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`, file sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`, with the single `ref`→`selector` schema alignment already frozen by the parent). It does **not** contain the substrings `#reveal-btn` or `TARGET-42` (design-time verified), so a positive outcome cannot be attributed to answer leakage.

### 4.3 Candidate ladder, ordering and engine

Model cells are executed by the **frozen parent runner** `research/intel/run_exp_37982024058.py` (sha256 `2b5d5bb5…`), invoked once per candidate:

```
python research/intel/run_exp_37982024058.py --mode probe-candidate \
  --outdir <per-candidate-dir> --candidate <candidate_id> --gguf <pinned gguf path> \
  --chrome /usr/bin/google-chrome --n-threads 4
```

`<per-candidate-dir>/raw/harness_config.json` is the section-4.2 overlay. `mode_probe_candidate` runs the frozen `PC-JSON-CONSTRAINED-DECODING` gate (10 probes), then — only if it passes — the 5 frozen seeded episodes against the served task page, writing `raw/model_receipts.json`. No new model-path or scoring code is authored.

Ladder order and early stop (frozen): `[M-14B-QWEN, M-8B-LLAMA]`. M-14B-QWEN is tested first because the leading general prior (below) is that quantisation/scale dominates small-model capability; if it CLEARS, the ladder stops (SUPPORTS) before testing the second family, saving its download. If it does not clear, M-8B-LLAMA tests the family dimension at the same size band as the failed Qwen 7B. Load failure or PC failure for a candidate is non-terminal: record and continue.

The three mechanical controls (`PC-ORACLE-EPISODE`, `NC-NO-MODEL-ACTION`, `B-RANDOM-ACTION`) and the evaluator are provided by the thin driver specified in **Appendix A**. That driver must import the frozen parent primitives (`run_episode`, `make_null_producer`, `make_random_producer`, `parse_action`, `start_page_server`) rather than re-implement them, and must navigate the page to the served task URL before running any episode (repairing the parent's `mode_null_random` about:blank defect, Appendix A.2).

### 4.4 Frozen candidate table

| candidate_id | role | model | quant | chat_format | bytes | sha256 |
|---|---|---|---|---|---|---|
| `M-14B-QWEN` | primary | Qwen2.5-14B-Instruct | Q4_K_M | `qwen` | 8988110976 | `d989c91de35f32c18bdb8bec96a4b9fff2c3e5bca066503c63a5ca54dd537a4b` |
| `M-8B-LLAMA` | secondary | Meta-Llama-3.1-8B-Instruct | Q4_K_M | `llama-3` | 4920739232 | `854506123b68372492b8a99bb3a999594672b394791cf1153f8da5ffb5f1c59a` |

URLs (design-time HTTP 200 via the `huggingface.co` resolve-redirect route; the sha256 equals the HF LFS OID i.e. the CDN etag):
- `https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/Qwen2.5-14B-Instruct-Q4_K_M.gguf`
- `https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`

**Leading general prior (theory, not factory evidence).** The largest credential-free **same-protocol** hosted chat surfaces are credential-gated; the reachable credential-free hosted path is operationally capped; and sub-30B quantised local models rarely complete multi-step Web tasks reliably. This prior predicts a likely bounded negative. It is declared here so that a confirmatory SUPPORTS is not post-hoc. The ladder is **not** an elaborate post-hoc theory of failure: it is a mechanism test of one variable that existed before any decision — model capacity (scale and family).

## 5. Measurements

Stable metric ids (parent ids preserved; new ids defined here):

| id | definition | unit |
|---|---|---|
| `positive_control_pass_rate` | PC-JSON-CONSTRAINED-DECODING probes returning valid schema JSON / 10 | fraction |
| `parseable_action_rate_step1` | episodes whose step-0 completion passes frozen `parse_action` / 5 | fraction |
| `answer_action_emission_rate` | episodes emitting ≥1 terminal `answer` action with `parse_ok` / 5 | fraction |
| `task_success_rate` | episodes with `task_success=true` under the frozen scorer / 5 | fraction |
| `mean_inference_latency_s` | mean per-call latency over a candidate cell's model calls | seconds |
| `mean_completion_tokens` | mean completion tokens over a candidate cell's model calls | tokens |
| `b3_status` | **new**: derived readiness-condition-(3) status `SATISFIED` / `NOT_SATISFIED` / `UNRESOLVED` | enum |
| `providers_credential_required` | **new**: census count of providers classified `CREDENTIAL_REQUIRED` | count |
| `providers_credential_free_operationally_capped` | **new**: census count classified `CREDENTIAL_FREE_OPERATIONALLY_CAPPED` | count |
| `providers_provisionable_credentialed` | **new**: census count classified `PROVISIONABLE_CREDENTIATED` | count |
| `candidates_measured_complete` | **new**: candidate cells that are COMPLETE | count |
| `comparators_enumerated` | **new**: external-comparator readiness-table entries emitted | count |

`answer_action_emission_rate` is inherited from the parent (where the zero-answer fact had to be inferred from raw traces); it makes the failure mode directly measurable. `b3_status` and the census counts are the mandate's decision-facing outputs; they do not override the frozen `OUTCOME`.

`metrics_stable_ids` in spec.json is the frozen identity list for EXECUTE/AUDIT.

## 6. Controls (stable ids)

- **PC-SUITE-EXP-INTEL-38175568787** (positive-control suite)
  - `PC-JSON-CONSTRAINED-DECODING`: 10 probes per candidate of the frozen probe string `Emit exactly: {"action":"click","selector":"#test"}` under P-TREAT-GOAL-SCHEMA with the frozen grammar (string sha256 `16c9877c0829b2099bd7180c212f28d8c545b095e9a4411afa7cabccd3fa6a65`). Success 10/10; a failing candidate is EXCLUDED (no episodes) and recorded `UNMEASURED_TREATMENT_PC_FAILED`.
  - `PC-ORACLE-EPISODE`: 5 scripted episodes (`click #reveal-btn`; `answer TARGET-42`) driven through the **real** frozen `run_episode` scorer against the served page. Success 5/5 `task_success=true`. Failure ⇒ preflight MEASUREMENT_INVALID.
- **NC-NO-MODEL-ACTION** (null control): 5 episodes of the fixed non-JSON content `I will click the button` through the real scorer against the served page. Expected `parseable_action_rate_step1=0.0` AND `task_success_rate=0.0`; anything else ⇒ verification broken ⇒ MEASUREMENT_INVALID.
- **B-RANDOM-ACTION** (chance baseline): uniform action from the frozen 5-action space, 5 episodes, `random.Random(42)` created once and reused (as the frozen `make_random_producer` does), run against the served page. Expected `parseable_action_rate_step1=1.0` (valid JSON by construction) and `task_success_rate < 0.6`. Analytic per-episode success probability is `sum_{j=1..4}(1/5)^(j+1) = 0.04992`, so `P(task_success_rate >= 3/5) = P(Binomial(5,0.04992) >= 3) ≈ 1.15e-3`; the bar is effectively unreachable by chance. If `task_success_rate >= 0.6` ⇒ MEASUREMENT_INVALID.
- **B-CARRIED-3B-8B-QWEN-GOAL-SCHEMA** (carried reference baseline, NOT re-run): parent's M-7B-QWEN 0/5 and M-3B-QWEN 0/5 with `parseable_action_rate_step1=1.0`. Reserved as the protocol-hardness anchor only, never as a within-run comparator arm (no treatment/comparator identity problem).
- **B-POLLINATIONS-CARRIED** (carried reference baseline, NOT re-run): grandparent endpoint receipt for the anonymous Pollinations gpt-oss-20b path (reasoning-only, ~197-token cap, intermittent 402, no pinning/SLA). Recorded in the census as `CREDENTIAL_FREE_OPERATIONALLY_CAPPED`.

Control-sensitivity repair: this design runs all mechanical controls against the served page (Appendix A.2), so a positive is registerable and a null cannot be an artifact of broken navigation.

## 7. Decision rule (frozen)

`OUTCOME ∈ {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}`; `B3_STATUS ∈ {SATISFIED, NOT_SATISFIED, UNRESOLVED}` is a separate derived field. `status=COMPLETE` for SUPPORTS/FALSIFIES; `status=MEASUREMENT_INVALID` for the invalid branches.

**Definitions.** A **cell** is one candidate = PC-JSON gate (10 probes; passed iff `positive_control_pass_rate == 1.0`) + an episode batch (`clearing_threshold.episodes = 5`). A cell is **COMPLETE** iff `load_status == LOADED` AND its PC gate passed AND it recorded exactly 5 episode records; **EXCLUDED** iff loaded and its PC gate did not pass (no episodes); **UNMEASURED_LOAD_FAILED** iff the GGUF digest mismatched or the model failed to load; **PARTIAL** iff its PC gate passed but it recorded fewer than 5 episode records; **CLEARS** iff COMPLETE and `task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6`.

**Precedence (first matching rule wins).**

1. **PREFLIGHT** (executed once, before the ladder). `PC-ORACLE-EPISODE == 5/5` AND `NC-NO-MODEL-ACTION == (parseable 0.0, success 0.0)` AND `B-RANDOM-ACTION == (parseable 1.0, task_success_rate < 0.6)` AND all `freeze_artifact` hash checks match AND required stack imports OK; else `OUTCOME=MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP.
2. **ENDPOINT CENSUS** (executed independently; non-gating for OUTCOME). For each predeclared provider: record `credential_env`, `credential_present`, unauthenticated `reachability_http_status`, and `classification ∈ {PROVISIONABLE_CREDENTIATED, CREDENTIAL_REQUIRED, CREDENTIAL_FREE_OPERATIONALLY_CAPPED, UNREACHABLE}` plus the exact `blocker`. No model is invoked.
3. **CAPABILITY LADDER** over `[M-14B-QWEN, M-8B-LLAMA]` in order; for each candidate `c`:
   - 3a. Verify the pinned GGUF sha256 + bytes. Mismatch ⇒ `UNMEASURED_LOAD_FAILED`, continue.
   - 3b. Load the model. Load failure ⇒ `UNMEASURED_LOAD_FAILED`, continue.
   - 3c. Run the PC gate, then the 5 episodes. If EXCLUDED ⇒ `UNMEASURED_TREATMENT_PC_FAILED`, continue. If PARTIAL ⇒ record and continue (a partial cell cannot decide a clearance).
   - 3d. If COMPLETE and CLEARS ⇒ `OUTCOME=SUPPORTS`, `B3_STATUS=SATISFIED`, **STOP** (early stop on the first clearing candidate).
   - 3e. If COMPLETE and does not CLEAR ⇒ record `TREATMENT_FAILS_BAR`, continue.
4. **AFTER THE LADDER** (no candidate cleared). Let `measured = { c in ladder : CELL(c) COMPLETE and not CLEARS }`.
   - If `measured` is empty (no candidate COMPLETE) ⇒ `OUTCOME=MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP.
   - Else ⇒ `OUTCOME=FALSIFIES` and `B3_STATUS = NOT_SATISFIED` iff every predeclared hosted provider is `CREDENTIAL_REQUIRED` / `UNREACHABLE` / `CREDENTIAL_FREE_OPERATIONALLY_CAPPED`, else `UNRESOLVED` (a credentialed hosted provider is provisionable, so a hosted capability test remains the smallest next action).

A candidate PC failure or load failure is never encoded as a capability failure.

**Canonical packet mapping.** `SUPPORTS` → `result.outcome=SUPPORTS`, `result.status=COMPLETE`. `FALSIFIES` → `result.outcome=FALSIFIES`, `result.status=COMPLETE`. `MEASUREMENT_INVALID` → `result.status=MEASUREMENT_INVALID`, `result.outcome=INCONCLUSIVE`. `B3_STATUS`, the census records and the external-comparator readiness table are written in `result.metrics` / `result.observations` and do not override the frozen `OUTCOME`.

## 8. Validity threats and limitations

- **Bounded negative scope.** FALSIFIES is bounded to the predeclared credential-free local Q4_K_M classes tested (Qwen2.5-14B, Llama-3.1-8B) plus the carried Qwen 3B–8B anchors and the recorded non-provisionable hosted census. It does not close hosted frontier classes (blocked, not tested), other quantisations, other tasks or other domains, and it does not globally reject `C-LLM-INHERIT`.
- **Task-bank granularity.** The frozen task has only 6 successful step-1 action space drawable options and even the reference Qwen3-4B WebArena headline is 24.3% on one benchmark; the frozen gate is near-deterministic by construction. Clearing this bar is necessary but **not sufficient** for Gate-3 readiness: comparators on the attained model family with their own denominators are separately required (`research/portfolio/PROGRAM_AUDIT_2026-10-10.md` line 218 records comparator-at-ceiling as a core readiness condition; that is B2-owned).
- **No embedded comparator cell.** There is no COLD/INSTRUCTIONS/RETRIEVAL/SPIDER comparator cell inside this packet, by mandate. It probes obtainability of a capable, fair-comparator-capable subject model only; multi-step-depth and comparator equivalence are certified by a specific companion experiment in the production task bank (B2), outside this packet. The subject model is a component, not the benchmark.
- **Scale vs family are not separated within a candidate.** The ladder tests scale (14B vs the carried 7B) and family (Llama vs Qwen) at different points; a SUPPORTS by M-14B-QWEN does not attribute causation to scale vs any Qwen-14B-specific property, and the early stop may leave the family dimension untested (recorded as unknown).
- **Provisioning deviation.** The 14B GGUF (~9.0 GB) may fail to load on a 15 GB box; if so it is `UNMEASURED_LOAD_FAILED` (operational, not capability) and the 8B Llama (~4.9 GB) is comfortably loadable. If `llama-3` chat_format is unsupported by the installed llama-cpp-python build, M-8B-LLAMA is `UNMEASURED_LOAD_FAILED`; M-14B-QWEN can still yield a COMPLETE cell. These are provisioning/packaging deviations, not model substitutions.
- **Grammar admission vs parse acceptance.** The frozen GBNF admits any single-field object whose keys are `selector` or `text` independent of the `click`/`answer` action, so grammar-feasible completions include schema-mismatched objects the frozen `parse_action` rejects. Liveness rests on the empirically verified PC 10/10 and carried 5/5 step-1 parseable behaviour; a candidate with `parseable_action_rate_step1 < 0.6` cannot clear the bar, so this residual cannot manufacture a false SUPPORTS.
- **Deterministic protocol / no variance.** `temperature=0.0` + fixed seeds. The 3/5 rule is the pre-declared adequacy rule for a capability gate, not a statistical threshold; no variance estimate is possible. n=5 per candidate and n=5 controls, per the frozen adequacy rule.
- **Representation loss (inherited).** State is a simplified text observation (`PAGE_TEXT` 300 chars, `ELEMENTS`, `HISTORY`), not a full accessibility tree; after the reveal `PAGE_TEXT` contains `TARGET-42` and `ELEMENTS` still lists the (now hidden) reveal button. This packet changes only the model class, not the observation representation.
- **Observation-only census.** The census is env-var presence + unauthenticated HTTP status/reachability + carried receipts; it does not attempt credential use (none exists) and cannot prove a credentialed provider would clear the bar — only that it is provisionable.
- **CANDIDATE_NOT_EVIDENCE comparators.** The external-comparator readiness table is a literature-identity enumeration (pinned arXiv IDs/titles/reported numbers/denominators/reproduction prerequisites); no vendor number is SPIDER evidence and no external number is reproduced by this packet.
- **Scorer scope.** Mechanical verification only (DOM + JSON schema); no LLM grading. The `#target` reveal and the terminal answer must both be observed by the frozen scorer.

## 9. Consequences

- **Positive (SUPPORTS, B3_STATUS=SATISFIED).** A factory-provisionable credential-free local endpoint (the clearing candidate's GGUF + llama.cpp) satisfies readiness condition (3) at mechanism level. The gated four-arm benchmark (COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER, same model/tools/budget) becomes executable at that model class with the verified goal/schema prompt, subject to B1 (shipped carrier) and B2 (non-ceiling dynamic-range task bank), which are parallel, not dependent. Whether `C-LLM-INHERIT` advances from HYPOTHESIS toward EXPERIMENTAL is a DIRECTOR adjudication.
- **Negative (FALSIFIES, B3_STATUS=NOT_SATISFIED).** No credential-free Q4_K_M local class tested up to 14B and a non-Qwen 8B family clears the minimal multi-step bar, and the only reachable credential-free hosted path is operationally capped; readiness condition (3) is not satisfied. The recorded exact blocker per hosted provider (missing credential environment variable or unreachable endpoint) and the census classification become decision inputs for the Global Research Director, who owns the re-scope choice. This packet does not pre-decide the re-scope.
- **MEASUREMENT_INVALID.** No claim changes; the recorded repair must precede any re-run.

## 10. Prerequisites and satisfiability probes (design-time, non-outcome-bearing)

Design-time probes performed (allowed: cheap, non-outcome-bearing) and their results:

1. **Stack.** `python 3.12.15`; `nproc=4`; 15 GB total RAM (~14 GB available); 85 GB free disk; `/usr/bin/google-chrome` present. `llama-cpp-python`, `playwright` and `openai` are NOT preinstalled ⇒ EXECUTE installs/builds them. `llama-cpp-python==0.2.90` has a PyPI sdist and no cp312 wheel (the parent built it); `playwright` installs from PyPI without downloading a browser when `executable_path` points at system Chrome (confirmed by the design-time canary).
2. **Grammar.** `raw/harness_config.json#gbnf_grammar` parsed rule-by-rule: all 7 rules (`root`, `ws`, `action`, `field`, `string`, `strchars`, `strchar`) defined and referenced; string sha256 `16c9877c0829b2099bd7180c212f28d8c545b095e9a4411afa7cabccd3fa6a65` (re-verified by EXECUTE after each per-candidate overlay). **Success-path feasibility (no floor degeneracy):** `strchar ::= [^"\\]` admits every character except `"` and `\`, so both `"text":"TARGET-42"` and `"selector":"#reveal-btn"` are grammar-admissible; the click-then-answer completion path is NOT blocked by the grammar, so a success is grammatically possible and FALSIFIES cannot be a grammar artifact.
3. **Candidate URLs and digests.** Both candidate GGUFs return HTTP 200 via the `huggingface.co` resolve-redirect route (design-time probe): M-14B-QWEN content-length 8988110976, sha256 `d989c91de35f32c18bdb8bec96a4b9fff2c3e5bca066503c63a5ca54dd537a4b`; M-8B-LLAMA content-length 4920739232, sha256 `854506123b68372492b8a99bb3a999594672b394791cf1153f8da5ffb5f1c59a`; each digest equals the HF LFS OID (CDN etag). Digest mismatch at EXECUTE is fail-closed.
4. **Chance baseline.** Analytic result in section 6 (non-outcome-bearing).
5. **Runner contract.** Read the frozen parent runner: `mode_probe_candidate` reads `<outdir>/raw/harness_config.json` and uses `cfg["prompts"]["system"]`, `cfg["positive_control"]`, `cfg["clearing_threshold"]`, `cfg["task"]`, `cfg["candidate_models_frozen"]` and `cfg["sampling"]["chat_format"]`; it navigates to the served page. `mode_null_random` starts the page server but never navigates to it — the documented control defect this design repairs (section 6, Appendix A.2).
6. **Endpoint census method.** Probed live at design time: `api.openai.com/v1/models` HTTP 401, `api.anthropic.com/v1/models` HTTP 401, `api.groq.com/openai/v1/models` HTTP 401, `text.pollinations.ai/models` HTTP 200 (only `openai-fast` = gpt-oss-20b reasoning), `openrouter.ai/api/v1/models` HTTP 200 (public list). No credential exists in the environment. The census is executable.
7. **Control/scorer canary (executed at design time).** The three mechanical controls were driven through the REAL frozen `run_episode` scorer with a REAL browser (Playwright + `/usr/bin/google-chrome`, headless, `--no-sandbox`) against the served task page, using a **name-only `llama_cpp` stub** (no GGUF load, no model inference) so the frozen runner could be imported without a multi-GB build. Results: `PC-ORACLE-EPISODE` = 5/5 `task_success` (each episode revealed `TARGET-42` and answered it); `NC-NO-MODEL-ACTION` = parseable 0.0, task_success 0.0; `B-RANDOM-ACTION` = parseable 1.0, task_success 0.2 (< 0.6). This proves the scorer registers the full completion path, rejects non-JSON, and that the chance baseline stays below the bar. Non-outcome-bearing: no model was under test (Appendix B disclosure).

Provisioning plan: download the pinned GGUF for the next unresolved candidate (digest-verified, fail-closed), build `llama-cpp-python==0.2.90`, install `playwright`, then run preflight controls.

## 11. Cost and information gain

CPU-only, up to 2 candidates × (10 PC probes + up to 5 episodes × up to 5 steps) llama.cpp inferences. Frozen runner per-call latency measured by the parent: 6.22 s (7B, 35 calls), 2.73 s (3B, 35 calls); scaling to ~10–12 s/call for 14B gives ~5–15 min inference per candidate (early stop after the first clearing candidate). Downloads ~13.9 GB worst case (M-14B 9.0 GB + M-8B 4.9 GB; early stop may avoid the second). `llama-cpp-python` build ~5–15 min; `playwright` <5 min; census <5 min. No external API spend. Wall-clock estimate 60–180 min.

Information gain is high and decision-changing in both directions. SUPPORTS unblocks the flagship four-arm benchmark with a factory-provisionable credential-free endpoint. FALSIFIES closes the credential-free Q4_K_M local path up to 14B/non-Qwen-8B as a capability result, records the exact hosted-credential blocker per provider, sets B3_STATUS=NOT_SATISFIED, and hands the Director a concrete re-scope set plus a bounded external-comparator readiness table. It directly tests the parent handoff's declared unknown U-03 and the mandate's hosted-provisioning clause, and it does NOT re-run the spent 3B–8B prompt ablation or the spent Pollinations agent attempt.

## 12. Inherited state from the parent handoff (four-way, preserved)

From EXP-INTEL-38164607941 handoff:

- **established**: under the frozen goal/schema prompt, no credential-free model cleared the bar (M-7B-QWEN 0/5, M-3B-QWEN 0/5; audit PASS); constrained decoding verified 10/10; verification logic sound (NC 0/5 parseable/success, random 5/5 parseable/0/5 success); prompt-sensitive failure mode (step-0 reveal succeeds, then hidden-button re-click loop, no answer action); prompt underspecification was NOT the driver.
- **rejected**: bounded to the frozen 3B–8B Qwen class under the goal/schema prompt (no general rejection of the credential-free path — a larger/non-Qwen class remained untested); bounded to the frozen minimal synthetic task and Qwen family.
- **unknown**: whether 14B+/non-Qwen GGUFs clear the bar (U-03) — this packet tests it; provisioning stability of larger GGUF packages; whether a hosted same-protocol endpoint will ever be provisionable (this packet records the blocker, not the future).
- **do_not_assume**: FALSIFIES is at the frozen protocol ceiling only; the deterministic protocol has no variance estimate (3/5 is an adequacy rule, not statistics); the failure is not due to missing page text; `C-LLM-INHERIT` remains HYPOTHESIS (not globally rejected).

From EXP-INTEL-37973264582 handoff: Pollinations gpt-oss-20b receipts (reasoning-only, ~197-token cap, intermittent 402); E-LOCAL-LLAMA 0.5B receipts; the endpoint obtainability census; Gate 3 FAIL_ZERO_PASS.

## 13. Non-duplication

`spec.comparative_reasoning` records the LEGACY: NO_MATCH classification (with its search limitation), the literal-search near-hits classified as NON-MATCHES, the superseded siblings and why they are not evidence, and why this probe is a distinct extension: (1) the two capacity axes the parent handoff left explicitly open (U-03: >8B scale and non-Qwen family); (2) a provisioning census that answers the mandate's exact hosted credential/operational blocker clause; (3) a conditional external-comparator readiness table for QCR / compile-and-execute / site-memory. Nearest substantive precedents, not duplicates: P2-REPLAY-COST (whose matched-task, fully-loaded-counterfactual guard applies only downstream to the four-arm benchmark) and the grandparent EXP-INTEL-37973264582 (obtainability; this packet extends to capability).

## 14. Freeze artifacts

Every existing mutable local code/data/fixture dependency whose identity can change the interpretation:

- `research/intel/run_exp_37982024058.py`
- `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json`
- `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`

All six `freeze_eligibility` checks are PASS with evidence refs in `spec.json`. The per-candidate configs are deterministic transformations of the bound base config (section 4.2) and therefore need no separate local file at freeze time; EXECUTE records their materialized sha256 in `provenance.json`. The thin materializer/controls/census/evaluator drivers are authored at EXECUTE and fully specified by Appendices A and C; their behaviour is a deterministic function of the frozen base fixture, the pinned candidate digests and the frozen thresholds, and EXECUTE records their sha256 in `provenance.json`. Remote GGUFs are frozen as URLs + digests, not bytes. `prereg.md` (this file) is hashed into `freeze.json`.

---

## Appendix A — controls & evaluator driver spec (thin, new, bounded)

The driver is the only new outcome-adjacent code. It must be minimal and must import, not re-implement, the frozen parent primitives.

**A.1 CLI.** `research/intel/exp_38175568787_controls.py` with a single mode `preflight-and-controls`:
`--outdir <dir> --config <config.json> --chrome /usr/bin/google-chrome`.
`<config.json>` may be the frozen base config or any per-candidate overlay: all controls-relevant keys (`task`, `null_control`, `random_baseline`, `sampling`) are inherited byte-for-byte and identical across candidates (section 4.2). It writes `raw/controls.json` (PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION, B-RANDOM-ACTION records) and `raw/preflight.json`.

**A.2 Server + navigation repair.** Start the page server via the frozen `start_page_server(cfg["task"]["page_html"])`; launch Chromium with `executable_path=--chrome, headless=True, args=["--no-sandbox"]`; **explicitly `page.goto("http://127.0.0.1:<port>/")` before any episode** (repair of the parent's `mode_null_random` about:blank defect). `run_episode` re-navigates to `page.url`, so the served page persists across episodes.

**A.3 Imported frozen primitives (no reimplementation).** From `run_exp_37982024058.py`: `run_episode`, `make_null_producer`, `make_random_producer`, `start_page_server`, and (for sanity) `parse_action`.

**Producer contract (binding).** The frozen `step_producer(obs, step) -> (raw, latency_s, completion_tokens, producer_meta)` passes `raw` directly to the frozen `parse_action`, which requires the completion **string** and calls `json.loads` on it. Every step producer therefore returns `raw` as a **string**: `json.dumps(...)` of the action object. Returning a dict (unserialized) is a contract violation that would make even the oracle fail `parse_action`; the design-time canary (Appendix B) validated the exact string-returning oracle through the real `run_episode` with a real browser (5/5).

- For **PC-ORACLE-EPISODE** the step producer is a fixed scripted producer returning `json.dumps({"action":"click","selector":"#reveal-btn"})` on step 0 and `json.dumps({"action":"answer","text":"TARGET-42"})` on steps ≥ 1 (the episode terminates after the first answered step), fed through the real `run_episode`.
- For **NC** use `make_null_producer(cfg["null_control"]["fixed_invalid_content"])` (raw = the fixed non-JSON string).
- For **B-RANDOM** use `make_random_producer(cfg["random_baseline"]["action_space"], random.Random(cfg["sampling"]["base_seed"]))` (raw = `json.dumps` of the chosen action; the frozen runner already returns strings here).

**A.4 Preflight outputs.** `PC-ORACLE-EPISODE` = 5/5 `task_success`; `NC` = parseable 0.0 & success 0.0; `B-RANDOM` = parseable 1.0 & `task_success_rate < 0.6`. Any deviation ⇒ `preflight.json.pass=false` ⇒ section 7 rule 1.

**A.5 Evaluator.** `research/intel/exp_38175568787_eval.py` aggregates each candidate's `raw/model_receipts.json` + the controls into `result.json` metrics/controls using the section-5 metric ids, computes the section-7 decision and the derived `b3_status`, and never inspects outcomes during DESIGN. It records raw evidence paths/hashes in `result.json.artifacts`. The endpoint census is produced by `research/intel/exp_38175568787_census.py` (Appendix C) and the external-comparator readiness table by `research/intel/exp_38175568787_comparators.py` (Section 7 / Appendix C); the evaluator merges them without letting either override `OUTCOME`.

Appendix A code is bound by this prereg; EXECUTE records its sha256 in `provenance.json`. Any deviation from Appendix A must be reported in `result.json.validity_notes`.

## Appendix B — design-time probe log (non-outcome-bearing)

| probe | result |
|---|---|
| Python / Chrome / nproc / RAM / disk | present as in section 10.1 |
| GBNF rule parse | 7/7 rules defined/referenced; string sha256 `16c9877c…` |
| GBNF success-path feasibility | `strchar ::= [^"\\]` admits `-`/digits/uppercase ⇒ `"text":"TARGET-42"` and `"selector":"#reveal-btn"` grammar-admissible (no floor degeneracy) |
| Prompt leakage check | P-TREAT-GOAL-SCHEMA does not contain `#reveal-btn` or `TARGET-42` |
| M-14B-QWEN URL + digest | HTTP 200; 8988110976 bytes; sha256 `d989c91d…` == HF LFS OID |
| M-8B-LLAMA URL + digest | HTTP 200; 4920739232 bytes; sha256 `85450612…` == HF LFS OID |
| Random-baseline analytic | p=0.04992; P(≥3/5)≈1.15e-3 |
| Endpoint reachability probes | OpenAI 401, Anthropic 401, Groq 401, Pollinations /models 200, OpenRouter /models 200; no credential env var present |
| **PC-ORACLE-EPISODE canary** (real Playwright+Chrome+real frozen `run_episode`; scripted string-returning producer per A.3) | 5/5 `task_success`; each episode revealed TARGET-42 and answered it |
| **NC-NO-MODEL-ACTION canary** (real scorer, served page) | parseable_action_rate_step1=0.0, task_success_rate=0.0 |
| **B-RANDOM-ACTION canary** (real scorer, served page, repaired navigation) | parseable_action_rate_step1=1.0, task_success_rate=0.2 (< 0.6) |

**Canary disclosure.** The canary ran at DESIGN time as a cheap non-outcome-bearing satisfiability probe (allowed by the DESIGN contract: no model was under test, no confirmatory measurement was taken). It used a **name-only `llama_cpp` import stub** (no GGUF load, no model inference) so the frozen parent runner could be imported without a multi-GB build — different from the parent prereg's canary only in that the stub was applied here by the DESIGN agent; the REAL Playwright/Chromium browser and the REAL frozen `run_episode`/`parse_action`/`make_*_producer` scoring code were used. It lives outside the repo (`/tmp/opencode/canary.py`, not a repo artifact), is NOT augmented into the evidence chain as model-behavior evidence, and is cited only to certify: (a) the positive completion path is registerable by the frozen scorer; (b) the null is rejected; (c) the repaired random baseline stays below the bar; (d) the Appendix A.3 producer contract (string-returning `step_producer`) is executable.

No confirmatory or outcome-bearing measurement was run during DESIGN.

## Appendix C — census and comparator-table driver spec (thin, new, bounded)

**C.1 Endpoint census — `research/intel/exp_38175568787_census.py`.** For each provider in `spec.endpoint_census.providers`, check `os.environ` for the credential variable(s), then issue an unauthenticated `GET` to the provider's model-list URL with a short timeout (no API key, no model invocation), recording `credential_present`, `reachability_http_status` (or the exact connection error), `classification` and `blocker`. Classification is mechanical: credential present ⇒ `PROVISIONABLE_CREDENTIATED`; no credential and HTTP 401/403 ⇒ `CREDENTIAL_REQUIRED`; connection failure ⇒ `UNREACHABLE`; the Pollinations path is `CREDENTIAL_FREE_OPERATIONALLY_CAPPED` with the carried operational blocker. Writes `raw/endpoint_census.json`. Non-outcome-bearing and non-gating.

**C.2 External-comparator readiness table — `research/intel/exp_38175568787_comparators.py`.** For each entry in `spec.external_comparators.required_entries`, resolve the pinned source (arXiv `abs` HTML with meta tags for `2608.12847` and `2604.09718`; a soft search for site-memory/ColorBrowserAgent), and emit `{system, arxiv_id, title, reported_numbers_with_denominators, reproduction_prerequisites, evidence_label: CANDIDATE_NOT_EVIDENCE}`. If a primary pinned source cannot be located, emit `NOT_PINNED` and do not use that system's numbers. Writes `raw/external_comparators.json`. Non-outcome-bearing and non-gating.

Appendix C code is bound by this prereg; EXECUTE records its sha256 in `provenance.json`.
