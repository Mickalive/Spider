# EXP-INTEL-38194362040 preregistration

Lane: `intel` — design_contract_version 2
Status: **DESIGN — NOT YET FROZEN**

Director mandate: `research/experiments/EXP-INTEL-38194362040/request.json#director_mandate` (typed `allocation_directive`; `allocation: NEW`; `parent_handoff_disposition: USE`; binding target claim `C-LLM-INHERIT`; `comparative_reasoning.legacy_classification: REPLICATION (corrected) plus DISTINCT_EXTENSION`). The mandate's binding requirement is: **re-pin each candidate GGUF to the byte-level sha256 of the actually served body (verified by full download, NOT HF etag/xetHash tree-API metadata), re-freeze, and re-run the already-frozen two-candidate ladder**, additionally recording the exact credential/operational blocker and, non-gating, external-comparator reproducibility. This packet is that corrected probe; it is **not** a re-run of the spent 3B–8B prompt ablation and **not** a substitute objective.

Predecessor chain: EXP-INTEL-37973264582 (grandparent; endpoint/comparator obtainability, Gate 2 FAIL, `DESIGN_COMPROMISED`) → EXP-INTEL-37982024058 (frozen runner + base fixture; FALSIFIES; audit PASS) → EXP-INTEL-38164607941 (goal/schema prompt ablation; FALSIFIES; audit PASS) → EXP-INTEL-38175568787 (parent; metadata-pinned ladder; **MEASUREMENT_INVALID**, audit MEASUREMENT_INVALID, `required_fixes` issued) → this packet (corrected freeze).
Superseded/near siblings (NOT evidence): EXP-INTEL-38123995594 (spent 3B–8B prompt ablation, executed as EXP-INTEL-38164607941) and EXP-INTEL-38013769440 (broadened capability-ceiling census). Neither froze; neither is cited as evidence.
Product/runtime context (parallel, not a dependency): `research/portfolio/PROGRAM_AUDIT_2026-10-10.md` — B1 (shipped carrier) and B2 (non-ceiling dynamic-range task bank) are open; **B3** (a capable same-model endpoint for the gated four-arm benchmark COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER) is the target of this packet.

---

## 1. Question

After each candidate GGUF is re-pinned to the byte-level sha256 of the **actually served body** (verified by a full DESIGN-time download, NOT HF `etag`/`xetHash` tree-API metadata) and re-frozen with a revision-pinned URL, does either **M-14B-QWEN** or **M-8B-LLAMA** clear the frozen minimal multi-step Web-agent bar (`task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6` over the 5 frozen seeded episodes) — and if not, what is the exact credential/operational blocker that must be removed to run a same-model/tools/budget hosted capability test?

Three components, one decision:

1. **Capability ladder (primary, gating).** Measure the two predeclared credential-free local classes the parent left untested (U-03): a larger same-family class (M-14B-QWEN) and a different-family class (M-8B-LLAMA), under the byte-frozen minimal protocol and the frozen P-TREAT-GOAL-SCHEMA prompt, against the inherited bar.
2. **Provisioning census (secondary, non-gating).** Record, per predeclared hosted provider, whether a same-protocol endpoint is provisionable and if not the exact credential/operational blocker (missing environment variable / HTTP status / operational cap).
3. **External-comparator readiness + reproducibility table (conditional, non-gating).** Enumerate the strongest externally published inheritance/memory systems (QCR arXiv:2608.12847; compile-and-execute arXiv:2604.09718; site-memory/ColorBrowserAgent arXiv:2601.07262) as `CANDIDATE_NOT_EVIDENCE`, and record mechanically whether each is reproducible under this protocol in this factory.

The Director's binding strategic question is component (1) plus the blocker clause (2); component (3) is the mandate's explicitly required conditional deliverable. No external vendor number is used as SPIDER evidence.

## 2. Hypotheses

- **H1 (capability).** At least one predeclared credential-free candidate class not previously tested — M-14B-QWEN (scale beyond the tested 8B ceiling) or M-8B-LLAMA (non-Qwen family) — clears the inherited bar under the frozen minimal protocol and P-TREAT-GOAL-SCHEMA, thereby satisfying readiness condition (3) at mechanism level with a factory-provisionable credential-free local endpoint.
- **H2 (provisioning).** No hosted same-protocol model endpoint is provisionable in this factory without a human-issued credential: every predeclared hosted provider is credential-gated (exact missing environment variable recorded) or unreachable, and the only reachable credential-free hosted path (Pollinations gpt-oss-20b) is operationally capped.
- **H3 (freeze-process repair; operational, not scientific).** The prior `MEASUREMENT_INVALID` was a freeze-process defect, not model behaviour: the served-body sha256 of both candidates (obtained by full download) equals the HF tree-API `lfs.oid`, while the previously pinned `xetHash`/`etag` differs from it. Re-pinning to served-body bytes and folding a full-download byte-verification step into frozen rule 3a and into `freeze_eligibility.freeze_artifacts_bound` makes the frozen content identity satisfiable against authentic served content.

## 3. Falsifier

**H0 (bounded negative).** No predeclared credential-free candidate clears the bar — every COMPLETE candidate cell has `task_success_rate < 0.6` — AND the census finds no `PROVISIONABLE_CREDENTIATED` hosted provider, so no currently-provisionable same-protocol endpoint can drive the minimal multi-step Web-agent test and readiness condition (3) is `NOT_SATISFIED`. The gated four-arm benchmark must then be re-scoped (drop the same-model external published-baseline anchor in favour of internally re-run comparators on a task bank with a dynamic-range certificate, or obtain a hosted credential with pinning/SLA, or pursue a different model class).

FALSIFIES is asserted only over the COMPLETE, predeclared credential-free local candidate set; it is a **capability bound on the tested classes and quantisation**, not a global rejection of `C-LLM-INHERIT` and not a closure of hosted frontier classes (which remain `UNRESOLVED`-by-blocker). A candidate whose GGUF fails the byte-level content-identity verification or load is `UNMEASURED_LOAD_FAILED`; a candidate whose treatment PC gate fails is `UNMEASURED_TREATMENT_PC_FAILED`; neither is counted as a capability failure. If no candidate is COMPLETE, the packet is `MEASUREMENT_INVALID`, not a scientific negative.

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

**Materialization path (binding).** The frozen runner's `load_config(outdir)` reads exactly `os.path.join(outdir, "raw", "harness_config.json")`. Each per-candidate config is materialized at **`<per-candidate-outdir>/raw/harness_config.json`**, where `<per-candidate-outdir>` is the `--outdir` passed to the frozen runner for that candidate. A provenance mirror is recorded at `configs/config_<candidate_id>.json` (both sha256 recorded in `provenance.json`). EXECUTE must verify the object-level diff between the materialized config and the frozen base config is confined to the 3 keys above.

The section-4.2 overlay materializer is provided by the thin driver `research/intel/exp_38194362040_materialize.py` (Authored-at-EXECUTE; bound by this section; sha256 recorded in `provenance.json`; parent precedents: `exp_38164607941_materialize.py`, `exp_38175568787_materialize.py`).

**Prompt provenance.** The treatment string is the grandparent harness goal/schema prompt (derived from `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`, file sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`, with the single `ref`→`selector` schema alignment already frozen by the parent). It does **not** contain the substrings `#reveal-btn` or `TARGET-42` (design-time verified), so a positive outcome cannot be attributed to answer leakage.

### 4.3 Candidate ladder, ordering and engine

Model cells are executed by the **frozen parent runner** `research/intel/run_exp_37982024058.py` (sha256 `2b5d5bb5…`), invoked once per candidate:

```
python research/intel/run_exp_37982024058.py --mode probe-candidate \
  --outdir <per-candidate-dir> --candidate <candidate_id> --gguf <pinned gguf path> \
  --chrome /usr/bin/google-chrome --n-threads 4
```

`<per-candidate-dir>/raw/harness_config.json` is the section-4.2 overlay. `mode_probe_candidate` runs the frozen `PC-JSON-CONSTRAINED-DECODING` gate (10 probes), then — only if it passes — the 5 frozen seeded episodes against the served task page, writing `raw/model_receipts.json`. No new model-path or scoring code is authored. The **content-identity verification of step 3a (section 4.5) is performed by the thin provisioning driver before the frozen runner is invoked**, because the frozen runner itself only records the local file's sha256 in its receipt and does not gate on the pin.

Ladder order and early stop (frozen): `[M-14B-QWEN, M-8B-LLAMA]`. M-14B-QWEN is tested first because the leading general prior is that quantisation/scale dominates small-model capability; if it CLEARS, the ladder stops (SUPPORTS) before testing the second family, saving its download. If it does not clear, M-8B-LLAMA tests the family dimension at the same size band as the failed Qwen 7B. Content-identity failure, load failure or PC failure for a candidate is non-terminal: record and continue.

The three mechanical controls (`PC-ORACLE-EPISODE`, `NC-NO-MODEL-ACTION`, `B-RANDOM-ACTION`) and the evaluator are provided by the thin driver specified in **Appendix A**. That driver must import the frozen parent primitives (`run_episode`, `make_null_producer`, `make_random_producer`, `parse_action`, `start_page_server`) rather than re-implement them, and must navigate the page to the served task URL before running any episode (repairing the parent's `mode_null_random` about:blank defect, Appendix A.2).

### 4.4 Corrected frozen candidate table (served-body pins)

| candidate_id | role | model | quant | chat_format | bytes | served_body_sha256 (PIN) |
|---|---|---|---|---|---|---|
| `M-14B-QWEN` | primary | Qwen2.5-14B-Instruct | Q4_K_M | `qwen` | 8988110976 | `e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008` |
| `M-8B-LLAMA` | secondary | Meta-Llama-3.1-8B-Instruct | Q4_K_M | `llama-3` | 4920739232 | `7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c` |

Revision-pinned URLs (frozen; `resolve/<revision_sha>/<file>`, verified at DESIGN to serve the identical body as the concurrent `main` ref):

- `https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/05244aa5d871c661c80082a15d3bce44714d068d/Qwen2.5-14B-Instruct-Q4_K_M.gguf` (`revision_sha = 05244aa5d871c661c80082a15d3bce44714d068d`)
- `https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/bf5b95e96dac0462e2a09145ec66cae9a3f12067/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` (`revision_sha = bf5b95e96dac0462e2a09145ec66cae9a3f12067`)

Concurrent `main`-ref URLs (recorded for drift observation only, NOT the pin):
- `https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/Qwen2.5-14B-Instruct-Q4_K_M.gguf`
- `https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`

**Superseded (rejected) pins — recorded so they cannot be reused.** The parent pinned `d989c91de35f32c18bdb8bec96a4b9fff2c3e5bca066503c63a5ca54dd537a4b` (M-14B-QWEN) and `854506123b68372492b8a99bb3a999594672b394791cf1153f8da5ffb5f1c59a` (M-8B-LLAMA). Those values are the HF tree-API `xetHash` / CDN `etag` and are **explicitly NOT pin sources** here. The served-body sha256 values above equal the HF tree-API `lfs.oid` and the parent's EXECUTE-observed body hashes.

**Independent GGUF header fingerprints (secondary identity anchor; parsed at DESIGN from the downloaded files).**

| candidate_id | gguf_version | tensor_count | kv_count | general.architecture | general.name | general.file_type | block_count | embedding_length | context_length | tokenizer.chat_template |
|---|---|---|---|---|---|---|---|---|---|---|
| `M-14B-QWEN` | 3 | 579 | 38 | `qwen2` | `Qwen2.5 14B Instruct` | 15 | 48 | 5120 | 32768 | present |
| `M-8B-LLAMA` | 3 | 292 | 33 | `llama` | `Meta Llama 3.1 8B Instruct` | 15 | 32 | 4096 | 131072 | present |

**Leading general prior (theory, not factory evidence).** The largest credential-free same-protocol hosted chat surfaces are credential-gated; the reachable credential-free hosted path is operationally capped; and sub-30B quantised local models rarely complete multi-step Web tasks reliably. This prior predicts a likely bounded negative. It is declared here so that a confirmatory SUPPORTS is not post-hoc. The ladder is a mechanism test of one variable that existed before any decision — model capacity (scale and family).

### 4.5 Content-identity verification (the correction; frozen rule 3a)

This is the specific repair the parent audit demanded (`EXP-INTEL-38175568787/audit.json#required_fixes`). At frozen ladder step 3a, before any load, EXECUTE:

1. Streams the **revision-pinned URL** to a temp path with no size cap; computes byte count and sha256 of the downloaded body (never reads a server metadata field as the pin).
2. Parses the GGUF header (magic `GGUF`, version, tensor_count, kv_count, and the metadata keys `general.architecture`, `general.name`, `general.file_type`, block_count, embedding_length, context_length, and presence of `tokenizer.chat_template`).
3. **IDENTITY-PASS** iff `bytes == pinned bytes` AND `sha256 == served_body_sha256` AND `fingerprint == pinned fingerprint`.
4. On mismatch, permits **one** re-download to distinguish transient transport corruption from a stable served-body drift; both attempts and observed values are logged.
5. If it still mismatches: record observed `bytes`/`sha256`/`fingerprint` (durable diagnostic), mark the candidate `UNMEASURED_LOAD_FAILED`, and continue. **A differing body is never substituted for the frozen content identity.**

Pin-source discipline is frozen in `spec.remote_artifact_pin_policy`: forbidden pin sources are HF tree-API `xetHash`, CDN `etag`, and `lfs.oid` used without a full-download confirmation. This makes EXECUTE-supplied `local_copy_sha256` equal the pin by construction, and makes a metadata-vs-body mismatch fail loudly at DESIGN/EXECUTE instead of silently passing freeze as it did in EXP-INTEL-38175568787.

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
| `served_body_digest_verified` | **new**: candidates whose EXECUTE full-download byte sha256 matched the frozen `served_body_sha256` | count (0–2) |
| `gguf_metadata_fingerprint_matched` | **new**: candidates whose parsed GGUF header fingerprint matched the frozen fingerprint | count (0–2) |
| `b3_status` | derived readiness-condition-(3) status `SATISFIED` / `NOT_SATISFIED` / `UNRESOLVED` | enum |
| `providers_credential_required` | census count of providers classified `CREDENTIAL_REQUIRED` | count |
| `providers_credential_free_operationally_capped` | census count classified `CREDENTIAL_FREE_OPERATIONALLY_CAPPED` | count |
| `providers_provisionable_credentialed` | census count classified `PROVISIONABLE_CREDENTIATED` | count |
| `candidates_measured_complete` | candidate cells that are COMPLETE | count |
| `comparators_enumerated` | external-comparator readiness-table entries emitted | count |

`answer_action_emission_rate` is inherited from the parent (where the zero-answer fact had to be inferred from raw traces). `served_body_digest_verified` and `gguf_metadata_fingerprint_matched` are new and make the content-identity repair directly measurable. `b3_status` and the census counts are the mandate's decision-facing outputs; they do not override the frozen `OUTCOME`. `metrics_stable_ids` in spec.json is the frozen identity list for EXECUTE/AUDIT.

## 6. Controls (stable ids)

- **PC-SUITE-EXP-INTEL-38194362040** (positive-control suite)
  - `PC-JSON-CONSTRAINED-DECODING`: 10 probes per candidate of the frozen probe string `Emit exactly: {"action":"click","selector":"#test"}` under P-TREAT-GOAL-SCHEMA with the frozen grammar (string sha256 `16c9877c0829b2099bd7180c212f28d8c545b095e9a4411afa7cabccd3fa6a65`). Success 10/10; a failing candidate is EXCLUDED (no episodes) and recorded `UNMEASURED_TREATMENT_PC_FAILED`.
  - `PC-ORACLE-EPISODE`: 5 scripted episodes (`click #reveal-btn`; `answer TARGET-42`) driven through the **real** frozen `run_episode` scorer against the served page. Success 5/5 `task_success=true`. Failure ⇒ preflight MEASUREMENT_INVALID.
- **NC-NO-MODEL-ACTION** (null control): 5 episodes of the fixed non-JSON content `I will click the button` through the real scorer against the served page. Expected `parseable_action_rate_step1=0.0` AND `task_success_rate=0.0`; anything else ⇒ verification broken ⇒ MEASUREMENT_INVALID.
- **B-RANDOM-ACTION** (chance baseline): uniform action from the frozen 5-action space, 5 episodes, `random.Random(42)` created once and reused (as the frozen `make_random_producer` does), run against the served page. Expected `parseable_action_rate_step1=1.0` (valid JSON by construction) and `task_success_rate < 0.6`. Analytic per-episode success probability is `sum_{j=1..4}(1/5)^(j+1) = 0.04992`, so `P(task_success_rate >= 3/5) = P(Binomial(5,0.04992) >= 3) ≈ 1.15e-3`; the bar is effectively unreachable by chance. If `task_success_rate >= 0.6` ⇒ MEASUREMENT_INVALID.
- **B-CARRIED-3B-8B-QWEN-GOAL-SCHEMA** (carried reference baseline, NOT re-run): parent's M-7B-QWEN 0/5 and M-3B-QWEN 0/5 with `parseable_action_rate_step1=1.0`. Reserved as the protocol-hardness anchor only, never as a within-run comparator arm.
- **B-POLLINATIONS-CARRIED** (carried reference baseline, NOT re-run): grandparent endpoint receipt for the anonymous Pollinations gpt-oss-20b path (reasoning-only, ~197-token cap, intermittent 402, no pinning/SLA). Recorded in the census as `CREDENTIAL_FREE_OPERATIONALLY_CAPPED`.

Control-sensitivity repair: this design runs all mechanical controls against the served page (Appendix A.2), so a positive is registerable and a null cannot be an artifact of broken navigation. The digest correction does not alter the controls.

## 7. Decision rule (frozen)

`OUTCOME ∈ {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}`; `B3_STATUS ∈ {SATISFIED, NOT_SATISFIED, UNRESOLVED}` is a separate derived field. `status=COMPLETE` for SUPPORTS/FALSIFIES; `status=MEASUREMENT_INVALID` for the invalid branches.

**Definitions.** A **cell** is one candidate = PC-JSON gate (10 probes; passed iff `positive_control_pass_rate == 1.0`) + an episode batch (`clearing_threshold.episodes = 5`). A cell is **COMPLETE** iff `load_status == LOADED` AND its PC gate passed AND it recorded exactly 5 episode records; **EXCLUDED** iff loaded and its PC gate did not pass (no episodes); **UNMEASURED_LOAD_FAILED** iff the byte-level content-identity verification at 3a failed or the model failed to load; **PARTIAL** iff its PC gate passed but it recorded fewer than 5 episode records; **CLEARS** iff COMPLETE and `task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6`.

**Precedence (first matching rule wins).**

1. **PREFLIGHT** (executed once, before the ladder). `PC-ORACLE-EPISODE == 5/5` AND `NC-NO-MODEL-ACTION == (parseable 0.0, success 0.0)` AND `B-RANDOM-ACTION == (parseable 1.0, task_success_rate < 0.6)` AND all `freeze_artifact` hash checks match AND required stack imports OK; else `OUTCOME=MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP.
2. **ENDPOINT CENSUS** (executed independently; non-gating for OUTCOME). For each predeclared provider: record `credential_env`, `credential_present`, unauthenticated `reachability_http_status`, and `classification ∈ {PROVISIONABLE_CREDENTIATED, CREDENTIAL_REQUIRED, CREDENTIAL_FREE_OPERATIONALLY_CAPPED, UNREACHABLE}` plus the exact `blocker`. No model is invoked.
3. **CAPABILITY LADDER** over `[M-14B-QWEN, M-8B-LLAMA]` in order; for each candidate `c`:
   - **3a. Byte-level content-identity verification** (section 4.5). IDENTITY-PASS iff `bytes == pin` AND `sha256 == served_body_sha256` AND `fingerprint == pin`; allow one re-download on mismatch. Any persistent mismatch ⇒ record observed values, `UNMEASURED_LOAD_FAILED`, continue (no substitution).
   - 3b. Load the model. Load failure ⇒ `UNMEASURED_LOAD_FAILED`, continue.
   - 3c. Run the PC gate, then the 5 episodes. If EXCLUDED ⇒ `UNMEASURED_TREATMENT_PC_FAILED`, continue. If PARTIAL ⇒ record and continue.
   - 3d. If COMPLETE and CLEARS ⇒ `OUTCOME=SUPPORTS`, `B3_STATUS=SATISFIED`, **STOP** (early stop on the first clearing candidate).
   - 3e. If COMPLETE and does not CLEAR ⇒ record `TREATMENT_FAILS_BAR`, continue.
4. **AFTER THE LADDER** (no candidate cleared). Let `measured = { c in ladder : CELL(c) COMPLETE and not CLEARS }`.
   - If `measured` is empty (no candidate COMPLETE) ⇒ `OUTCOME=MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP.
   - Else ⇒ `OUTCOME=FALSIFIES` and `B3_STATUS = NOT_SATISFIED` iff every predeclared hosted provider is `CREDENTIAL_REQUIRED` / `UNREACHABLE` / `CREDENTIAL_FREE_OPERATIONALLY_CAPPED`, else `UNRESOLVED` (a credentialed hosted provider is provisionable, so a hosted capability test remains the smallest next action).

A candidate identity/load failure or PC failure is never encoded as a capability failure.

**Canonical packet mapping.** `SUPPORTS` → `result.outcome=SUPPORTS`, `result.status=COMPLETE`. `FALSIFIES` → `result.outcome=FALSIFIES`, `result.status=COMPLETE`. `MEASUREMENT_INVALID` → `result.status=MEASUREMENT_INVALID`, `result.outcome=INCONCLUSIVE`. `B3_STATUS`, the census records and the external-comparator readiness/reproducibility table are written in `result.metrics` / `result.observations` and do not override the frozen `OUTCOME`.

## 8. Validity threats and limitations

- **Bounded negative scope.** FALSIFIES is bounded to the predeclared credential-free local Q4_K_M classes tested (Qwen2.5-14B, Llama-3.1-8B) plus the carried Qwen 3B–8B anchors and the recorded non-provisionable hosted census. It does not close hosted frontier classes (blocked, not tested), other quantisations, other tasks or other domains, and it does not globally reject `C-LLM-INHERIT`.
- **Served-body temporal drift (the residual substrate risk).** The frozen content identity is a remote body; if HF re-serves different bytes at the same revision between DESIGN and EXECUTE, step 3a fails closed and the packet is `MEASUREMENT_INVALID` again. Mitigations: (i) the pin equals the parent's prior-day EXECUTE-observed body hash, so the body has already been stable across ≥1 day; (ii) the URL is revision-pinned to a repo commit; (iii) DESIGN verified byte-identity across two routes; (iv) any drift is recorded with observed `bytes`/`sha256`/`fingerprint`, which is itself a durable substrate finding. This is disclosed as the keep-or-kill risk of the repair.
- **Task-bank granularity.** The frozen task is a single near-deterministic page; clearing the bar is necessary but **not sufficient** for Gate-3 readiness (comparator-at-ceiling and dynamic range are B2-owned).
- **No embedded comparator cell.** There is no COLD/INSTRUCTIONS/RETRIEVAL/SPIDER comparator cell inside this packet, by mandate. It probes obtainability of a capable, fair-comparator-capable subject model only.
- **Scale vs family are not separated within a candidate.** A SUPPORTS by M-14B-QWEN does not attribute causation to scale vs any Qwen-14B-specific property, and the early stop may leave the family dimension untested (recorded as unknown).
- **Provisioning deviations.** The 14B GGUF (~9.0 GB) may fail to load on a 15 GB box; if so it is `UNMEASURED_LOAD_FAILED` (operational, not capability) and the 8B Llama (~4.9 GB) is comfortably loadable. Both candidate `chat_format` paths were verified to exist in llama-cpp-python 0.2.90 at DESIGN.
- **Grammar admission vs parse acceptance.** The frozen GBNF admits any single-field object whose keys are `selector` or `text` independent of the `click`/`answer` action, so grammar-feasible completions include schema-mismatched objects the frozen `parse_action` rejects. Liveness rests on the empirically verified PC 10/10 and carried 5/5 step-1 parseable behaviour; a candidate with `parseable_action_rate_step1 < 0.6` cannot clear the bar, so this residual cannot manufacture a false SUPPORTS.
- **Deterministic protocol / no variance.** `temperature=0.0` + fixed seeds. The 3/5 rule is the pre-declared adequacy rule for a capability gate, not a statistical threshold; no variance estimate is possible. n=5 per candidate and n=5 controls, per the frozen adequacy rule.
- **Representation loss (inherited).** State is a simplified text observation (`PAGE_TEXT` 300 chars, `ELEMENTS`, `HISTORY`), not a full accessibility tree; after the reveal `PAGE_TEXT` contains `TARGET-42` and `ELEMENTS` still lists the (now hidden) reveal button. This packet changes only the model class, not the observation representation.
- **Observation-only census.** The census is env-var presence + unauthenticated HTTP status/reachability + carried receipts; it cannot prove a credentialed provider would clear the bar — only that it is provisionable.
- **CANDIDATE_NOT_EVIDENCE comparators.** The external-comparator table is a literature-identity enumeration; no vendor number is SPIDER evidence and no external number is reproduced by this packet.
- **Scorer scope.** Mechanical verification only (DOM + JSON schema); no LLM grading.

## 9. Consequences

- **Positive (SUPPORTS, B3_STATUS=SATISFIED).** A factory-provisionable credential-free local endpoint (the clearing candidate's GGUF + llama.cpp) satisfies readiness condition (3) at mechanism level. The gated four-arm benchmark becomes executable at that model class with the verified goal/schema prompt, subject to B1 and B2 (parallel, not dependent). Whether `C-LLM-INHERIT` advances from HYPOTHESIS toward EXPERIMENTAL is a DIRECTOR adjudication.
- **Negative (FALSIFIES, B3_STATUS=NOT_SATISFIED).** No credential-free Q4_K_M local class tested up to 14B and a non-Qwen 8B family clears the minimal multi-step bar, and the only reachable credential-free hosted path is operationally capped; readiness condition (3) is not satisfied. The recorded exact blocker per hosted provider and the census classification become decision inputs for the Global Research Director, who owns the re-scope choice. This packet does not pre-decide the re-scope.
- **MEASUREMENT_INVALID.** No claim changes; the recorded repair must precede any re-run. A third `MEASUREMENT_INVALID` would specifically indicate served-body drift or an environment regression, and would be recorded with the observed byte evidence rather than as a capability result.

## 10. Prerequisites and DESIGN-time satisfiability probes (non-outcome-bearing)

Design-time probes performed (allowed: cheap, non-outcome-bearing) and their results:

1. **Stack.** `python 3.12.15`; `nproc=4`; 15 GB total RAM (~14 GB available); 85 GB free disk; `/usr/bin/google-chrome`, `curl`, `wget`, `git` present; `huggingface.co` reachable (~127 MB/s in the DESIGN probe). `llama-cpp-python`, `playwright` and `openai` are NOT preinstalled ⇒ EXECUTE installs/builds them.
2. **chat_format support.** Downloaded `llama_cpp_python-0.2.90.tar.gz` from PyPI and inspected `llama_cpp/llama_chat_format.py`: `@register_chat_format("llama-3")` (line 975) and `@register_chat_format("qwen")` (line 1006) are both present ⇒ both candidate load paths exist. (Removes the parent's residual "chat_format may be unsupported" uncertainty for M-8B-LLAMA.)
3. **Candidate content identity (the correction).** FULL DOWNLOAD (not metadata) of each candidate at DESIGN time:
   - M-14B-QWEN revision-pinned URL: 8,988,110,976 bytes, sha256 `e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008`; `main`-ref URL: identical bytes and sha256.
   - M-8B-LLAMA revision-pinned URL: 4,920,739,232 bytes, sha256 `7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c`; `main`-ref URL: identical bytes and sha256.
   - Both served-body hashes equal the HF tree-API `lfs.oid` and the parent EXECUTE-observed body hashes; the parent-pinned `xetHash`/`etag` values are rejected as pins.
4. **GGUF header fingerprints.** Parsed from the downloaded files (section 4.4): both are GGUF v3 with the expected architectures, tensor counts, `file_type=15`, and an embedded `tokenizer.chat_template`.
5. **Freeze artifacts.** Re-hashed at DESIGN: runner `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`, base fixture `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`, prompt provenance `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862` — all match the parent `freeze.json.artifact_hashes`.
6. **Grammar.** `raw/harness_config.json#gbnf_grammar` rule set (7 rules) and success-path feasibility are inherited from the audited parent (string sha256 `16c9877c…`; `strchar ::= [^"\\]` admits `-`, digits and uppercase ⇒ `"text":"TARGET-42"` and `"selector":"#reveal-btn"` are grammar-admissible).
7. **Chance baseline.** Analytic result in section 6 (non-outcome-bearing).
8. **Endpoint census method.** Probed live at predecessor design time: `api.openai.com/v1/models` HTTP 401, `api.anthropic.com/v1/models` HTTP 401, `api.groq.com/openai/v1/models` HTTP 401, `text.pollinations.ai/models` HTTP 200, `openrouter.ai/api/v1/models` HTTP 200; no credential exists in the environment.
9. **Control/scorer canary (carried, predecessor).** The three mechanical controls were driven through the REAL frozen `run_episode` scorer with a REAL browser against the served task page with a name-only `llama_cpp` stub (prereg of EXP-INTEL-38175568787, Appendix B): PC-ORACLE-EPISODE 5/5, NC 0.0/0.0, B-RANDOM parseable 1.0 / success 0.2. No confirmatory model measurement was run during DESIGN.

Provisioning plan: download the pinned GGUF for the next unresolved candidate (step-3a byte-verified, fail-closed), build `llama-cpp-python==0.2.90`, install `playwright`, then run preflight controls.

## 11. Cost and information gain

CPU-only, up to 2 candidates × (10 PC probes + up to 5 episodes × up to 5 steps) llama.cpp inferences. Frozen runner per-call latency measured by the parent: 6.22 s (7B, 35 calls), 2.73 s (3B, 35 calls); scaling to ~10–12 s/call for 14B gives ~5–15 min inference per candidate (early stop after the first clearing candidate). Downloads ~13.9 GB worst case (M-14B 9.0 GB + M-8B 4.9 GB; the DESIGN-time full downloads consumed this once; early stop may avoid the second at EXECUTE). `llama-cpp-python` build ~5–15 min; `playwright` <5 min; census <5 min. No external API spend. Wall-clock estimate 60–180 min.

Information gain is high and decision-changing in both directions, and strictly higher than re-running the invalid parent because the one blocking substrate defect is repaired and independently verified at DESIGN time. SUPPORTS unblocks the flagship four-arm benchmark with a factory-provisionable credential-free endpoint. FALSIFIES closes the credential-free Q4_K_M local path up to 14B/non-Qwen-8B as a capability result, records the exact hosted-credential blocker per provider, sets B3_STATUS=NOT_SATISFIED, and hands the Director a concrete re-scope set plus a bounded external-comparator table. It directly tests the parent handoff's declared unknown U-03 and the mandate's hosted-provisioning clause, and it does NOT re-run the spent 3B–8B prompt ablation or the spent Pollinations agent attempt.

## 12. Inherited state from the parent handoff (four-way, preserved)

From EXP-INTEL-38175568787 handoff (the exact `parent_handoff` referenced by `request.json`, sha256 `df1150468c97dee8fd002d60fcd97fbbc96434cbc97749e0428325c58e0af942`):

- **established**: (i) the generic freeze-process defect — for both frozen HF GGUFs the pinned sha256 equals the HF tree-API `xetHash` / CDN `etag` while the sha256 of the served bytes equals the tree-API `lfs.oid`; byte counts match; three independent routes reproduce identical body hashes; (ii) the measurement substrate is live and deterministic (PREFLIGHT 5/5, NC 0/0, random 1.0/0.2, `raw/controls.json` byte-identical to the audited parent); (iii) both candidates were `UNMEASURED_LOAD_FAILED` at frozen step 3a, fail-closed, no byte substitution; (iv) census snapshot 0 provisionable-credentialed / 10 credential-required / 1 capped / 1 unreachable; (v) external-comparator table 3/3 enumerated, all `CANDIDATE_NOT_EVIDENCE`; (vi) packet disposition MEASUREMENT_INVALID/INCONCLUSIVE, audit confirms substrate failure not scientific negative, `C-LLM-INHERIT` neither promoted nor weakened.
- **rejected**: (i) the hypothesis that the metadata-derived pins identify the served body; (ii) transport corruption / corrupted local copy / byte-count change as the cause (three routes agree); (iii) treating the step-3a mismatch as a capability failure of either candidate.
- **unknown**: whether the pins were wrong at DESIGN (metadata-only read) or became stale; whether origin bytes matching the old `xetHash` remain retrievable; the capability of M-14B-QWEN and M-8B-LLAMA under the frozen protocol (entirely unmeasured); whether the Xet metadata/body mismatch affects other lanes' pinned GGUFs; whether a re-pinned re-freeze would produce COMPLETE cells; the capability of any hosted provider (census is credential/reachability only).
- **do_not_assume**: do not encode the parent packet as FALSIFIES or as capability evidence; do not promote/downgrade/globally reject `C-LLM-INHERIT`; do not re-run the spent 3B–8B ablation; do not pin HF GGUF digests from server metadata; do not generalize the inherited 3B–8B ceiling to 14B/non-Qwen; do not treat the census or the external-comparator table as capability evidence; do not treat a successful corrected re-run as established inheritance capability at product scale.

From EXP-INTEL-38164607941 handoff (inherited by the parent): the prompt-sensitive failure mode (step-0 reveal succeeds, then hidden-button re-click loop, no answer action); the bounded 3B–8B Qwen FALSIFIES. From EXP-INTEL-37973264582 handoff: Pollinations gpt-oss-20b receipts; the endpoint obtainability census; Gate 3 FAIL_ZERO_PASS.

## 13. Non-duplication

`spec.comparative_reasoning` records the Director's `REPLICATION (corrected) plus DISTINCT_EXTENSION` classification and why this probe is distinct: (1) the one-time freeze/byte-identity repair demanded by the parent audit's `required_fixes` (served-body sha256 pin verified by full download + revision-pinned URL + GGUF fingerprint + a full-download verification step in frozen rule 3a and in `freeze_eligibility.freeze_artifacts_bound`); (2) the two capacity axes the parent handoff left open (U-03: >8B scale and non-Qwen family); (3) a provisioning census answering the mandate's exact hosted credential/operational blocker clause; (4) a conditional external-comparator readiness/reproducibility table. Nearest substantive precedents, not duplicates: P2-REPLAY-COST (sha `9687ff787f2d74460bb7006826008852f5b4416b`) and P2-BLIND-COMPOSITION (sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`) concern replay/composition economics, and the grandparent EXP-INTEL-37973264582 concerns obtainability; this packet extends to byte-identity-corrected capability.

## 14. Freeze artifacts

Every existing mutable local code/data/fixture dependency whose identity can change the interpretation:

- `research/intel/run_exp_37982024058.py` (sha256 `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`)
- `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`)
- `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py` (sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`)

All six `freeze_eligibility` checks are PASS with evidence refs in `spec.json`. The per-candidate configs are deterministic transformations of the bound base config (section 4.2) and therefore need no separate local file at freeze time; EXECUTE records their materialized sha256 in `provenance.json`. The thin materializer/provisioning/controls/census/comparators/evaluator drivers are authored at EXECUTE and fully specified by Appendices A and C; their behaviour is a deterministic function of the frozen base fixture, the pinned candidate digests and the frozen thresholds, and EXECUTE records their sha256 in `provenance.json`. Remote GGUFs are frozen as **revision-pinned URLs + served-body sha256 digests**, not bytes; the byte-verification requirement is recorded in `spec.remote_artifact_pin_policy` and `freeze_eligibility.freeze_artifacts_bound`. `prereg.md` (this file) is hashed into `freeze.json`.

---

## Appendix A — controls & evaluator driver spec (thin, new, bounded)

The driver is the only new outcome-adjacent code. It must be minimal and must import, not re-implement, the frozen parent primitives.

**A.1 CLI.** `research/intel/exp_38194362040_controls.py` with a single mode `preflight-and-controls`:
`--outdir <dir> --config <config.json> --chrome /usr/bin/google-chrome`.
`<config.json>` may be the frozen base config or any per-candidate overlay: all controls-relevant keys (`task`, `null_control`, `random_baseline`, `sampling`) are inherited byte-for-byte and identical across candidates (section 4.2). It writes `raw/controls.json` (PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION, B-RANDOM-ACTION records) and `raw/preflight.json`.

**A.2 Server + navigation repair.** Start the page server via the frozen `start_page_server(cfg["task"]["page_html"])`; launch Chromium with `executable_path=--chrome, headless=True, args=["--no-sandbox"]`; **explicitly `page.goto("http://127.0.0.1:<port>/")` before any episode** (repair of the parent's `mode_null_random` about:blank defect). `run_episode` re-navigates to `page.url`, so the served page persists across episodes.

**A.3 Imported frozen primitives (no reimplementation).** From `run_exp_37982024058.py`: `run_episode`, `make_null_producer`, `make_random_producer`, `start_page_server`, and (for sanity) `parse_action`.

**Producer contract (binding).** The frozen `step_producer(obs, step) -> (raw, latency_s, completion_tokens, producer_meta)` passes `raw` directly to the frozen `parse_action`, which requires the completion **string**. Every step producer therefore returns `raw` as a **string**: `json.dumps(...)` of the action object. Returning a dict is a contract violation.

- For **PC-ORACLE-EPISODE** the step producer returns `json.dumps({"action":"click","selector":"#reveal-btn"})` on step 0 and `json.dumps({"action":"answer","text":"TARGET-42"})` on steps ≥ 1, fed through the real `run_episode`.
- For **NC** use `make_null_producer(cfg["null_control"]["fixed_invalid_content"])`.
- For **B-RANDOM** use `make_random_producer(cfg["random_baseline"]["action_space"], random.Random(cfg["sampling"]["base_seed"]))`.

**A.4 Preflight outputs.** `PC-ORACLE-EPISODE` = 5/5 `task_success`; `NC` = parseable 0.0 & success 0.0; `B-RANDOM` = parseable 1.0 & `task_success_rate < 0.6`. Any deviation ⇒ `preflight.json.pass=false` ⇒ section 7 rule 1.

**A.5 Provisioning driver (new; implements section 4.5).** `research/intel/exp_38194362040_provision.py` streams each candidate's revision-pinned URL to a local temp path, computes byte count + sha256, parses the GGUF header fingerprint, allows one re-download on mismatch, writes `raw/provisioning_receipt.json` per candidate (observed bytes/sha256/fingerprint, `identity_pass`, and — on mismatch — the durable observed-value diagnostic), and prints the local GGUF path only when IDENTITY-PASS is true. It never substitutes a differing body.

**A.6 Evaluator.** `research/intel/exp_38194362040_eval.py` aggregates each candidate's `raw/model_receipts.json`, the provisioning receipts and the controls into `result.json` metrics/controls using the section-5 metric ids, computes the section-7 decision and the derived `b3_status`, and never inspects outcomes during DESIGN. It records raw evidence paths/hashes in `result.json.artifacts`. The endpoint census is produced by `research/intel/exp_38194362040_census.py` (Appendix C) and the external-comparator table by `research/intel/exp_38194362040_comparators.py` (Appendix C); the evaluator merges them without letting either override `OUTCOME`.

Appendix A code is bound by this prereg; EXECUTE records its sha256 in `provenance.json`. Any deviation from Appendix A must be reported in `result.json.validity_notes`.

## Appendix B — DESIGN-time probe log (non-outcome-bearing)

| probe | result |
|---|---|
| Python / Chrome / curl / wget / git / nproc / RAM / disk | Python 3.12.15, `/usr/bin/google-chrome` present, curl/wget/git present, nproc=4, 15 GB RAM (~14 GB avail), 85 GB free |
| HF network | reachable; ~127 MB/s in the DESIGN full-download probe |
| `llama-cpp-python` 0.2.90 chat formats | sdist `llama_cpp/llama_chat_format.py` registers `llama-3` (line 975) and `qwen` (line 1006) ⇒ both candidate load paths exist |
| M-14B-QWEN revision-pinned FULL download | 8,988,110,976 bytes; sha256 `e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008`; equals `main`-ref body and tree `lfs.oid` |
| M-8B-LLAMA revision-pinned FULL download | 4,920,739,232 bytes; sha256 `7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c`; equals `main`-ref body and tree `lfs.oid` |
| Rejected pin sources | M-14B `xetHash`/`etag` = `d989c91d…`; M-8B `xetHash`/`etag` = `85450612…` — explicitly NOT used as pins |
| GGUF header fingerprints | M-14B: v3, tensors 579, kv 38, arch `qwen2`, file_type 15, block 48, emb 5120, ctx 32768, chat_template present. M-8B: v3, tensors 292, kv 33, arch `llama`, file_type 15, block 32, emb 4096, ctx 131072, chat_template present |
| Freeze artifact hashes | runner `2b5d5bb5…`, base fixture `7aba9dc8…`, prompt provenance `4e2b6710…` — all match parent `freeze.json.artifact_hashes` |
| Prompt leakage check | P-TREAT-GOAL-SCHEMA does not contain `#reveal-btn` or `TARGET-42` |
| GBNF rule parse | 7/7 rules defined/referenced; string sha256 `16c9877c…` (inherited frozen fixture) |
| GBNF success-path feasibility | `strchar ::= [^"\\]` admits `-`/digits/uppercase ⇒ `"text":"TARGET-42"` and `"selector":"#reveal-btn"` grammar-admissible |
| Random-baseline analytic | p=0.04992; P(≥3/5)≈1.15e-3 |
| Endpoint reachability probes | OpenAI 401, Anthropic 401, Groq 401, Pollinations /models 200, OpenRouter /models 200; no credential env var present |
| Control/scorer canary (carried predecessor, real Playwright+Chrome+real frozen `run_episode`) | PC-ORACLE 5/5; NC parseable 0.0/success 0.0; B-RANDOM parseable 1.0/success 0.2 |

**Canary disclosure.** The control/scorer canary was executed at predecessor DESIGN time as a cheap non-outcome-bearing satisfiability probe; it used a name-only `llama_cpp` import stub (no model inference) with the REAL Playwright/Chromium browser and the REAL frozen scoring code, and is cited here only as carried, audited liveness evidence. The DESIGN probes performed by this packet (full downloads, GGUF header parse, chat_format inspection, freeze-artifact hashing) are all non-outcome-bearing and are recorded in the table above. **No confirmatory or outcome-bearing model measurement was run during DESIGN.**

## Appendix C — census and comparator-table driver spec (thin, new, bounded)

**C.1 Endpoint census — `research/intel/exp_38194362040_census.py`.** For each provider in `spec.endpoint_census.providers`, check `os.environ` for the credential variable(s), then issue an unauthenticated `GET` to the provider's model-list URL with a short timeout (no API key, no model invocation), recording `credential_present`, `reachability_http_status` (or the exact connection error), `classification` and `blocker`. Classification is mechanical: credential present ⇒ `PROVISIONABLE_CREDENTIATED`; no credential and HTTP 401/403 ⇒ `CREDENTIAL_REQUIRED`; connection failure ⇒ `UNREACHABLE`; the Pollinations path is `CREDENTIAL_FREE_OPERATIONALLY_CAPPED` with the carried operational blocker. Writes `raw/endpoint_census.json`. Non-outcome-bearing and non-gating.

**C.2 External-comparator readiness + reproducibility table — `research/intel/exp_38194362040_comparators.py`.** For each entry in `spec.external_comparators.required_entries`, resolve the pinned source (arXiv `abs` HTML with meta tags for `2608.12847` and `2604.09718`; a soft search for site-memory/ColorBrowserAgent), and emit `{system, arxiv_id, title, reported_numbers_with_denominators, reproduction_prerequisites, reproducibility_feasibility, evidence_label: CANDIDATE_NOT_EVIDENCE}`. `reproducibility_feasibility ∈ {FEASIBLE_WITH_CREDENTIALS, NOT_FEASIBLE_MISSING_SUBSTRATE, UNKNOWN}` is decided mechanically from whether the required substrate (datasets / base model family / tool set / budget denominator) is obtainable in this factory without credentials. If a primary pinned source cannot be located, emit `NOT_PINNED` and do not use that system's numbers. Writes `raw/external_comparators.json`. Non-outcome-bearing and non-gating.

Appendix C code is bound by this prereg; EXECUTE records its sha256 in `provenance.json`.
