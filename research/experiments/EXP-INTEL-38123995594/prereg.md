# PRE-REGISTRATION: EXP-INTEL-38123995594 (INTEL, design_contract_version=2)

Title: Prompt ablation: does supplying task goal+schema in the system prompt convert the step-0 reveal-click into a full click-then-answer completion for M-7B-QWEN / M-3B-QWEN under the same credential-free CPU-quantized constraints as EXP-INTEL-37982024058?

Experiment ID: EXP-INTEL-38123995594 | Lane: intel | Claim IDs: ["C-LLM-INHERIT"]
Status: DESIGN (pre-freeze; DESIGN ONLY). No outcome-bearing measurements performed.
Request reference: research/experiments/EXP-INTEL-38123995594/request.json (sha256 fa2fab71042e21422b7ceaa2f79abdcd352d1b739ac19a556f9f657800b4324d; request_hash ed8e64b8a504d11da95f0b260ab0a28787ed8aa169f74c19489d20fbe0bc5cce)
Parent handoff (continuity, not authorization): research/experiments/EXP-INTEL-37982024058/handoff.json (sha256 b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55)

## 1) Rationale and Context (binding)

- Director mandate (binding): action CONTINUE, claim C-LLM-INHERIT, cognitive_reset true, parent_handoff_disposition SUPERSEDE. Question verbatim: "Would supplying the task goal/schema in the system prompt (as the parent harness's SYS prompt did) convert the step-0 reveal-click into a full click-then-answer completion for M-7B-QWEN or M-3B-QWEN under the same credential-free CPU-quantized constraints?"
- Parent result (frozen evidence): EXP-INTEL-37982024058 produced an audited FALSIFIES on C-LLM-INHERIT (audit status PASS, producer_claim_supported=true, VF-01 material). Both models emitted a valid click at step 0 (parseable_action_rate_step1=1.0, 5/5), the target was revealed (revealed_value='TARGET-42'), then both re-emitted {"action":"click","selector":"#reveal-btn"} for steps 1-4 and never emitted an answer action (task_success_rate=0.0, 5/5; parent result.json#observations establishes zero terminal answer actions in all 10 episodes - the parent metric field answer_action_emission_rate was null). Constrained decoding PC 10/10 both models; NC 0/5 parseable; B-RANDOM 5/5 parseable, 0/5 success (the 0/5 was structural: the parent control ran on about:blank).
- Mechanistic hypothesis (audit VF-01): prompt underspecification. The parent system prompt states neither the action schema nor the terminal goal. The grandparent harness (EXP-INTEL-37973264582) SYS constant contained both. The treatment is that prompt, recovered exactly, with one disclosed adjustment.
- Epistemic boundary: the parent handoff is continuity evidence only and MUST NOT silently override the Director's SUPERSEDE/CONTINUE decision. Its established/rejected/unknown/do_not_assume distinctions are preserved in section 11 and are not treated as an agenda.

## 2) Non-duplication and Legacy Check

- POLICY.md requires non-duplication. The Director mandate records "LEGACY: NO_MATCH, with an explicit search limitation": no existing artifact tests local CPU-quantized small-model capability probing or a credential-free programmatic endpoint readiness gate. A targeted re-read of codex/legacy_artifact_index.json and the mounted pre-2.0 Codex archive confirms NO_MATCH but finds three literal near-hit clusters, explicitly classified here as non-matches rather than hidden:
  - (1) "qwen" / "llama" WebArena paper numbers (37.5% GPT-4.1 / 24.3% Qwen3-4B) are HOSTED-LLM PAPER EVIDENCE, marked "NOT reproduced by SPIDER" (archived Codex section, WebArena/AWM rows). Different substrate (hosted API) and different benchmark (WebArena) from this local CPU-quantized minimal-task gate.
  - (2) Pre-2.0 operational notes "NO local inference capability exists in this environment (no ollama/vllm/llama servers, ports 11434/8000/8080/1234 closed; no openai/vllm/transformers/torch packages)" are environment-infrastructure DIAGNOSTICS of the pre-2.0 factory. They are SUPERSEDED for this transaction by the audited parent's proven local llama.cpp+GGUF provisioning (parent loaded Qwen2.5-7B split shards on this CPU-only factory, n_vocab=152064). They are not experiments on local model capability.
  - (3) "credential-free" hits concern billed-token budgets and Product closure-hygiene duties, not capability probes.
- Nearest substantive legacy precedents (accepted bounded findings, not duplicates): P2-REPLAY-COST (sha 9687ff787f...) guard applies downstream to replay/economics, not to this capability probe; P2-BLIND-COMPOSITION (sha 017a80ae...) out of scope; P2-MIND2WEB (blob sha 9bb76113...) out of scope.
- Siblings that never froze are NOT evidence sources: EXP-INTEL-38013769440, EXP-INTEL-38106207218, EXP-INTEL-38110512532, EXP-INTEL-38121203425. The last three (and four other lanes) share the design-review control-plane failure fingerprint 3b9ff5e4e9e73f23e368efb4 (model opencode/exo-free, exit_code 1, category substantive), documented by the Director as a shared outage, not a scientific design verdict.

## 3) Design: Only One Varied Dimension

- Candidate models: M-7B-QWEN (Qwen2.5-7B-Instruct-Q4_K_M split shards, digests pinned) evaluated first; M-3B-QWEN (Qwen2.5-3B-Instruct-Q4_K_M single file, digest pinned) evaluated only if M-7B-QWEN treatment does NOT clear (early stop on first clearing treatment).
- Task, fixture, grammar, sampling, seeds, harness code path, model artifacts and environment identical across cells.
- Prompt conditions (ONLY prompts.system varies):

P-COMP-UNDERSPECIFIED (comparator; frozen expected anchor):
  "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown."
  Provenance: byte-identical to EXP-INTEL-37982024058 raw/harness_config.json#prompts.system (parent file sha256 7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb; prompts.system string sha256 1294954da7b1d6b9570b07e1e39cb48515b925355d0f33d5fabf72c8e8ce3876).

P-TREAT-GOAL-SCHEMA (treatment):
  "You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<id>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it."
  Provenance: grandparent raw/code/min_webagent.py SYS (file sha256 4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862; SYS string sha256 742e5aae5b5ffd72ccb43cb18658a14483660e7659640df651e91011e9b6dc12; adapted treatment string sha256 36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716) with the single ref->selector schema alignment. Justification: the frozen GBNF admits only the keys "selector" and "text"; the grandparent prompt's "ref" key is not in the grammar, so aligning the prompt's named schema to the grammar-enforced schema ensures the treatment measures the goal+schema content rather than a prompt/grammar key mismatch. No '#reveal-btn' or 'TARGET-42' leakage (design-time verified).

## 4) Protocol, Controls, and Comparator Validity

4.1 Deterministic protocol (inherited)
- temperature=0.0, max_tokens=512, n_ctx=2048, chat_format=qwen, llama_seed=42, episode_seed_offset="42 + episode_idx", seeds 42..46 for episodes 0..4 (base 42). max_steps_per_episode=5.

4.2 Task fixture (inherited)
- Identical minimal page from EXP-INTEL-37982024058 raw/harness_config.json: button #reveal-btn reveals div #target containing "TARGET-42" (JS sets #target display:block and hides #reveal-btn). Scorer identical (Playwright DOM assertions + strict JSON parse against the frozen GBNF/action schema). run_episode calls page.goto(page.url) at the start of each episode, so the model episodes and all repaired controls run against the served page.

4.3 Positive controls
- PC-JSON-CONSTRAINED-DECODING: 10 probes per cell ("Emit exactly: {"action":"click","selector":"#test"}") under that cell's prompts.system + frozen GBNF. Must be 10/10 before the cell's episodes; a cell whose PC fails is EXCLUDED (no episodes). If both candidates' treatment-cell PCs fail -> OUTCOME=MEASUREMENT_INVALID.
- PC-ORACLE-EPISODE: 5 scripted click-then-answer episodes (click #reveal-btn then answer TARGET-42) through the real run_episode scorer against the served page. Must be 5/5 at preflight; <5/5 -> MEASUREMENT_INVALID (scorer broken, not model behavior).

4.4 Null/negative controls
- NC-NO-MODEL-ACTION: 5 episodes of fixed non-JSON content ("I will click the button") through the real scorer against the SERVED page. Must be parseable 0.0 and success 0.0; any parseable/success -> MEASUREMENT_INVALID.
- B-RANDOM-ACTION: seeded RNG random.Random(42) created once and reused across episodes (exactly the parent's make_random_producer/mode_null_random stream: one rng.choice per step), run against the SERVED page (navigation repaired vs the parent's about:blank defect), 5-action uniform space, valid JSON by construction. Analytic per-episode success probability = sum_{j=1..4} (1/5)^(j+1) = 0.04992, so P(bar cleared by chance) ~ 1.15e-3. Deterministic seed-42 realization (design-time simulation of the parent's exact stream, re-derived at EXECUTE): episode 0 = click, click(hidden), answer TARGET-42 (success); episodes 1-3 = answer TARGET-41; episode 4 = click, answer unknown -> task_success_rate = 1/5 = 0.2, parseable_action_rate_step1 = 1.0. Must be parseable 1.0 and success < 0.6; if task_success_rate >= 0.6 -> MEASUREMENT_INVALID (control broken). A realization different from (1.0, 0.2) signals a driver/RNG-stream mismatch and is recorded explicitly.

4.5 Comparator validity (fail-closed, refined anchor policy)
- For each evaluated candidate, the P-COMP comparator cell is collected unconditionally BEFORE any outcome decision, in the same run as the treatment cell. The identification contrast is this contemporaneous within-run pair (same model, same harness, same sampling schedule, same environment; only prompts.system differs).
- HARD INVALIDATION (MEASUREMENT_INVALID): a comparator cell that CLEARS the capability bar (task_success_rate >= 0.6) makes the prompt effect non-identifiable; a comparator cell with parseable_action_rate_step1 < 0.6 indicates protocol/decoding drift; a partial pair (either cell with fewer than 5 episode records) cannot decide a clearance or a confound.
- EXPECTED ANCHOR: the frozen parent tuple (task_success_rate=0.0, parseable_action_rate_step1=1.0, zero answer actions) from EXP-INTEL-37982024058 result.json#metrics and #observations. Exact match -> record REPLICATION_ANCHOR_EXACT. A bar-failing deviation that preserves parseability -> record REPLICATION_ANCHOR_DRIFT as a validity note; the paired contrast remains identifiable and the packet need not be invalidated, but the report must state that the historical parent anchor was not exactly reproduced.
- Rationale: the comparator's role is a contemporaneous control, not a byte-replay of history; historical exactness is a drift monitor. This prevents a spurious infrastructure invalidation (e.g., a rebuild producing minor floating-point drift) while preserving attribution.

4.6 Per-cell config materialization (bound for EXECUTE)

The per-cell config is NOT re-authored. EXECUTE deterministically materializes it by loading the frozen parent fixture `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (file sha256 7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb) and replacing ONLY `prompts.system` with the condition string below; every other key is inherited byte-for-byte from the parent file. This binds every outcome-relevant key the parent runner consumes, including:

- `prompts.positive_control_probe` = "Emit exactly: {"action":"click","selector":"#test"}"; `positive_control` = {"id":"PC-JSON-CONSTRAINED-DECODING","probes":10,...}
- `null_control` = {"id":"NC-NO-MODEL-ACTION","episodes":5,"fixed_invalid_content":"I will click the button",...}
- `random_baseline` = {"id":"B-RANDOM-ACTION","episodes":5,"action_space":[click #reveal-btn; answer TARGET-41; answer TARGET-42; answer TARGET-43; answer unknown]}
- `task.page_html`, `gbnf_grammar` (string sha256 16c9877c0829b2099bd7180c212f28d8c545b095e9a4411afa7cabccd3fa6a65), `sampling`, `clearing_threshold`, `action_schema`, `metrics_stable_ids`.

Condition strings (the ONLY `prompts.system` override):

- P-COMP-UNDERSPECIFIED `prompts.system` (string sha256 1294954da7b1d6b9570b07e1e39cb48515b925355d0f33d5fabf72c8e8ce3876):
  "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown."
- P-TREAT-GOAL-SCHEMA `prompts.system` (string sha256 36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716):
  "You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<id>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it."

The two materialized configs therefore differ from each other ONLY in `prompts.system`; their sha256 is recorded in provenance.json. EXECUTE must NOT hand-author a reduced config (a partial config omitting positive_control/null_control/random_baseline would crash the imported `run_positive_control` and the control driver); the overlay rule removes that failure mode.

Controls driver requirements (EXECUTE materialization): random baseline and NC must navigate to the served page before selecting actions (fix parent about:blank defect); PC-ORACLE-EPISODE runs through the real scorer; all controls use the same run_episode scorer as the candidates.

Harness delta: new runner `research/intel/run_exp_38123995594.py` (thin; imports parse_action / regex_parse_action / run_episode / make_null_producer / make_random_producer / make_model_producer / start_page_server from the frozen `research/intel/run_exp_37982024058.py`, accepts per-cell config path and model paths, enforces digest checks, runs PC gates, collects comparator unconditionally, runs repaired controls, applies precedence 1..4). Its content is bound by Appendix A; EXECUTE records its sha256.

## 5) Metrics and Stable IDs

- positive_control_pass_rate: fraction of the 10 per-cell JSON-decode probes that produce schema-valid JSON.
- parseable_action_rate_step1: fraction of episodes whose step-0 completion is a strict-parseable schema-conforming action (>=0.6 required to clear).
- answer_action_emission_rate: fraction of episodes containing at least one strict-parseable action with action=="answer" (0.0 expected for the comparator anchor; descriptive otherwise).
- task_success_rate: fraction of episodes where the reveal click executed, revealed_value == "TARGET-42", and the terminal answer stripped == "TARGET-42" within 5 steps (>=0.6 required to clear).
- mean_inference_latency_s: mean wall-clock seconds per model call over episode steps (descriptive).
- mean_completion_tokens: mean completion tokens per model call over episode steps (descriptive).

## 6) Decision Rule (exact precedence)

OUTCOME in {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}; status COMPLETE unless operational blockers prevent every cell.

Definitions:
- A CELL is one (candidate, prompt-condition) unit = PC-JSON gate (10 probes; passed iff positive_control_pass_rate == 1.0) + an episode batch (clearing_threshold.episodes = 5).
- A cell is COMPLETE iff its PC gate passed AND it recorded exactly 5 episode records.
- A cell is EXCLUDED iff its PC gate did not pass (no episodes run).
- A cell CLEARS iff COMPLETE and task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6.
- A comparator cell is VALID iff COMPLETE and task_success_rate < 0.6 AND parseable_action_rate_step1 >= 0.6.

Precedence (first matching rule wins):

1. PREFLIGHT: PC-ORACLE-EPISODE == 5/5 AND NC-NO-MODEL-ACTION == (parseable 0.0, success 0.0) AND B-RANDOM-ACTION == (parseable 1.0, task_success_rate < 0.6) AND all freeze_artifact hash checks match AND required stack imports OK AND GGUF digest checks PASS. Else OUTCOME=MEASUREMENT_INVALID.
2. CANDIDATE LOOP over [M-7B-QWEN, M-3B-QWEN] in order, each candidate measured in ONE run:
   a. Run the candidate's TREAT cell (PC-JSON gate then 5 episodes) and its COMP cell (PC-JSON gate then 5 episodes) unconditionally as a contemporaneous pair.
   b. If the TREAT cell is EXCLUDED, the candidate yields no capability measurement: record it UNMEASURED_TREATMENT_PC_FAILED and continue to the next candidate (unresolved, NOT a failure).
   c. If either cell of the pair is COMPLETE-but-partial (fewer than 5 episode records) -> a partial pair cannot decide a clearance or a confound -> OUTCOME=MEASUREMENT_INVALID, STOP.
   d. If the COMP cell CLEARS (task_success_rate >= 0.6) or has parseable_action_rate_step1 < 0.6 -> prompt effect not identifiable -> OUTCOME=MEASUREMENT_INVALID, STOP. Otherwise record the comparator disposition: COMPLETE-and-VALID with task_success_rate=0.0, parseable_action_rate_step1=1.0 and zero answer actions -> REPLICATION_ANCHOR_EXACT; any other VALID value -> REPLICATION_ANCHOR_DRIFT validity note.
   e. If the TREAT cell CLEARS -> OUTCOME=SUPPORTS (attribution=PROMPT_ATTRIBUTED, candidate=c), STOP.
3. FALSIFIES: the loop completed, at least one TREAT cell was COMPLETE (measurable), no TREAT cell cleared, and every evaluated COMP cell was COMPLETE-and-VALID -> SUPPORTS is not observed for the measured candidate set (Director's bounded negative). Candidates with an EXCLUDED treatment cell are listed in unresolved, not counted as failures.
4. Otherwise (no TREAT cell was measurable, e.g. all treatment PCs failed) -> OUTCOME=MEASUREMENT_INVALID.

report.md must record, per evaluated candidate, the failure-mode descriptor (answer_action_emission_rate, click loop count, step-0 reveal success) and the bounded-negative wording exactly.

## 7) Reachability Proof (non-outcome-bearing)

- SUPPORTS reachable: PC-ORACLE-EPISODE 5/5 proves the scorer registers the full click-then-answer path; the treatment prompt is feasible under the frozen GBNF and the audited parent's PC is 10/10, so a treatment clearance is a genuinely open empirical outcome. A comparator that fails the bar preserves attribution.
- FALSIFIES reachable: the parent already realized 0/5 task success under the comparator prompt; the treatment may also fail (recurring loop, zero answer action), with at most 2 candidates evaluated under early stop, and the branch requires only that at least one treatment cell be COMPLETE.
- MEASUREMENT_INVALID reachable via preflight failure, comparator clearing the bar / losing parseability, a partial pair, no measurable treatment cell, freeze-artifact hash mismatch, GGUF digest mismatch, provisioning failure, or PC failure. No rule shadows another: comparator cells are collected unconditionally before (2e); (3) fires only when a treatment cell completed, none cleared, and all evaluated comparators were complete and valid; (4) covers the residual.
- Threshold 0.6 over 5 episodes (>=3/5) is attainable for both extremes; the random baseline is strictly below the bar by construction (deterministic seed-42 realization 0.2 success / 1.0 parseable; analytic per-episode probability 0.04992; P(chance clearance) ~ 1.15e-3).

## 8) Non-Outcome-Bearing Satisfiability Probes (design-contract v2)

Performed at DESIGN (logged for EXECUTE preflight):

- P-0 Environment/importability: cmake 3.31.6, gcc/g++ 13.3.0, Python 3.12.15, pip 26.2.1, Python.h present; /usr/bin/google-chrome present; nproc=4, ~15 GB total RAM; llama_cpp and playwright NOT preinstalled (EXECUTE installs/builds). PASS.
- P-1 Grammar well-formedness: the parent GBNF defines and references all 7 rules (root, ws, action, field, string, strchars, strchar); constructible by the parent-executed grammar path. PASS. (Recorded caveat: the grammar admits schema-mismatched action/field combos that parse_action rejects; liveness rests on verified empirical decoding + the 0.6 parseability bar, not on a syntactic claim.)
- P-2 Prompt non-leakage / byte-identity: P-TREAT-GOAL-SCHEMA contains neither "#reveal-btn" nor "TARGET-42"; P-COMP-UNDERSPECIFIED is byte-identical to parent harness_config.json#prompts.system (both string sha256 re-verified). PASS.
- P-3 Provisioning liveness: 3B resolve URL HTTP 302, 7B shard1 302, shard2 302, 7B single-file 404 (documented deviation); digests pinned from raw/gguf_sha256.txt. PASS.
- P-4 Task/scorer/oracle path: the parent executed the served-page oracle/scorer end-to-end (task_episodes.json); the controls driver's navigation repair is a mechanical requirement specified in 4.4/Appendix A. PASS.
- P-5 B-RANDOM deterministic realizability: simulated the parent's exact stream (rng=random.Random(42) created once, one rng.choice per step over the frozen 5-action space, reused across 5 episodes) -> expected (parseable 1.0, success 0.2) < 0.6, so the control is realizable and non-tautological and cannot accidentally clear the bar. PASS.
- P-6 Legacy non-duplication: targeted reads of codex/legacy_artifact_index.json and the mounted pre-2.0 Codex archive classify the "qwen"/"llama"/"credential-free" literal hits as hosted-LLM paper evidence, pre-2.0 environment diagnostics, and Product budget notes respectively (section 2); no existing artifact tests this local CPU-quantized capability gate. PASS.

## 9) Validity Threats and Mitigations

- Comparator drift: comparator cells are collected unconditionally and compared to the frozen parent anchor; hard invalidation if the comparator clears the bar or loses parseability; lesser drift recorded as a validity note (4.5).
- Prompt leakage: treatment must not name specific selectors/targets (explicit non-leakage check); GBNF keys restricted to selector/text.
- Control sensitivity: random/NC/oracle run against the served page (navigation repaired) via the same scorer, so a null cannot be a navigation artifact and a positive is registerable. The random control's true chance realization (0.2) is pinned deterministically, not assumed.
- Provisioning: GGUF digest checks against raw/gguf_sha256.txt; URL route confirmed live; 7B split shards pinned (single-file 404 known). Mismatch -> MEASUREMENT_INVALID.
- Decoder-capability conflation: comparator re-measured in the same run for each model; only prompts.system changes, so a treatment clearance with a bar-failing comparator is attributable to the prompt.
- Cell completeness vs scientific result: partial cells and PC-excluded treatment cells are MEASUREMENT_INVALID/unresolved, never encoded as capability failures (rules 2b/2c/4).
- Grammar admission vs parse acceptance: the GBNF admits mismatched action/field combos that parse_action rejects; the treatment cannot clear the bar unless >=3/5 step-1 completions are genuinely parseable, so this cannot manufacture a false SUPPORTS.
- Early-stop bias: M-7B-QWEN pair is fully evaluated first; M-3B-QWEN is evaluated only if 7B does not clear. The negative is therefore not overstated across both models unless both treatment cells were actually measured (rule 3 lists any unresolved candidate explicitly).
- Build chain: llama-cpp-python 0.2.90 sdist build (no cp312 wheel) - cmake+gcc present; if the build fails at EXECUTE -> provisioning_failure -> MEASUREMENT_INVALID (not a model result).
- Bundled treatment: the treatment bundles the goal sentence, the schema enumeration, and the prompt wording. If it clears, the decomposition (goal vs schema enumeration vs generic longer instruction) is NOT identified; this is recorded as unresolved and bounded in report.md.

## 9.1) Design-time self-attack (constructibility, recorded before freeze)

Each named v2 DESIGN-failure class was actively attacked and resolved:

- Empty/unreachable branches: precedence 1..4 is fully enumerated; SUPPORTS needs >=3/5 in a COMPLETE treatment cell (registerable per PC-ORACLE-EPISODE), FALSIFIES needs at least one COMPLETE treatment cell clearing nothing with all evaluated comparators valid (parent realized the comparator behavior), MEASUREMENT_INVALID is reachable via preflight/comparator/partial-pair/no-measurable-treatment. No rule is shadowed; comparator cells are collected before any decision. (Section 7.)
- Arithmetic impossibility: threshold 3/5 over 5 episodes is attainable for both extremes; early stop means at most 2 candidates are evaluated; no branch requires more episodes than the frozen 5. The random control's deterministic realization (0.2) is strictly below 0.6.
- Ceiling/floor baselines: comparator sits at the realized floor (0/5 task success), PC-ORACLE-EPISODE at the ceiling (5/5); dynamic range is full, so a treatment effect is identifiable. The random control is strictly below the bar.
- Treatment/comparator identity: byte-identified at design time (prompt string sha256s in section 3); the two per-cell configs are materialized by the section 4.6 overlay and differ ONLY in prompts.system, so all other outcome-relevant config keys are inherited byte-for-byte from the parent fixture. No leakage of the selector or the answer text into the treatment.
- Insensitive controls: PC-JSON fires 10/10 (parent-verified) and PC-ORACLE-EPISODE fires 5/5; NC stays 0/0; B-RANDOM realizes (1.0, 0.2) and cannot reach 0.6. Each control has a distinct, attainable expected value.
- Missing prerequisites: Python 3.12.15, cmake 3.31.6, gcc/g++ 13.3, Python.h, pip 26.2.1, /usr/bin/google-chrome verified; llama-cpp-python 0.2.90 sdist present on PyPI (no cp312 wheel) so the build path is required and feasible; playwright installable; all three GGUF resolve URLs verified live (7B single-file 404 documented); parent end-to-end execution proves the task/scorer path.
- Unbound mutable artifacts: five existing freeze_artifacts hashed; the outcome-determining parsing/scoring/episode code is bound by importing the frozen parent runner (no re-implementation); the only EXECUTE-created files (per-cell configs, thin driver) are bound by the deterministic prereg section 4.6 overlay rule / Appendix A and their sha256 recorded in provenance.json.

Residual risks (documented, not hidden): (R1) a rebuilt llama.cpp could produce minor floating-point drift from the parent build - handled by the comparator policy (drift note vs hard invalidation), not by changing the science; (R2) the thin driver itself is not a freeze artifact (it cannot exist at freeze time) - mitigated by the import binding and Appendix A; (R3) a treatment clearance would not decompose goal-sentence vs schema-enumeration vs generic longer instruction - recorded as unresolved; (R4) the split-shard 7B packaging could change in future repo revisions - the current digests pin the exact artifacts; (R5) the GBNF admits schema-mismatched combos - the parseability bar (and the audited PC 10/10) prevents a false SUPPORTS.

## 10) Prerequisites, Costs, and Expected Information Gain

- Prerequisites: CPU-only, 4 cores, ~15 GB total RAM, /usr/bin/google-chrome, Python 3.12.15, pip 26.2.1, cmake 3.31.6, gcc/g++ 13.3, Python.h. GGUFs are NOT present in /tmp/opencode/gguf/ and llama-cpp-python/playwright are not installed in this factory, so EXECUTE must re-download (~6.8 GB) and install/build.
- Cost estimate: 45-150 min wall-clock; inference ~10-25 min worst case (parent mean 5.065 s/call 7B, 2.154 s/call 3B at 13-17 completion tokens); provisioning/build 25-60 min. No external API spend.
- Information gain: High and decision-changing in both directions. SUPPORTS unblocks the four-arm benchmark with a verified goal/schema prompt and bounds the parent FALSIFIES to the underspecified-prompt ceiling. FALSIFIES (bounded negative) closes the credential-free local 3B-8B Qwen path as a capability result (not a prompt artifact) and records the receipts for a hosted-endpoint / different-model-class re-scope. This is readiness-condition-(3) work allocated by the Director (agent_priors_used: a cheap probe that separates two competing explanations is higher decision value than another benchmark run on an unverified endpoint).

## 11) Inherited State (parent_handoff preserved, not treated as agenda)

- established: under the frozen underspecified-prompt protocol, no credential-free model cleared the bar (M-7B-QWEN 0/5, M-3B-QWEN 0/5, audit PASS); constrained decoding PC 10/10; NC 0/5 parseable; B-RANDOM 5/5 parseable, 0/5 success (structural about:blank artifact); step-0 reveal succeeds and both models re-click the hidden button, never emitting an answer.
- rejected (bounded): no general rejection of the credential-free path (prompt ablation needed); no generality beyond the frozen minimal synthetic task and Qwen family.
- unknown: whether the parent-style goal/schema prompt converts step-0 click to full completion (audit U-01) - this experiment tests exactly this; whether the failure is general small-model planning or prompt-specific (U-02); whether 14B+/non-Qwen GGUFs clear (U-03, out of scope); 7B split-shard packaging stability over time (U-04).
- do_not_assume: frozen-prompt ceiling only; 7B packaging deviation is not a model substitution (VF-02); deterministic protocol yields uniform traces - no variance estimate and the 3/5 rule is pre-declared, not statistical (VF-03); task failure not due to missing page text after reveal (VF-04); C-LLM-INHERIT remains HYPOTHESIS (not globally rejected) and Gate 2 remains FAIL under the frozen protocol.

## 12) Transmission Identity (for downstream agents)

Stable IDs to reuse across EXECUTE/AUDIT/DIRECTOR:
- Experiment: EXP-INTEL-38123995594 (lane=intel, design_contract_version=2)
- Claim: C-LLM-INHERIT
- Candidates: M-7B-QWEN, M-3B-QWEN
- Prompt conditions: P-COMP-UNDERSPECIFIED, P-TREAT-GOAL-SCHEMA
- Controls: PC-JSON-CONSTRAINED-DECODING, PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION, B-RANDOM-ACTION, B-0.5B-QWEN-LOCAL (carried), B-POLLINATIONS-PROXY (carried)
- Baselines: B-UNDERSPECIFIED-PROMPT-7B, B-UNDERSPECIFIED-PROMPT-3B, B-RANDOM-ACTION
- Metrics: positive_control_pass_rate, parseable_action_rate_step1, answer_action_emission_rate, task_success_rate, mean_inference_latency_s, mean_completion_tokens
- Comparator disposition flags: REPLICATION_ANCHOR_EXACT, REPLICATION_ANCHOR_DRIFT
- Treatment disposition flags: UNMEASURED_TREATMENT_PC_FAILED
- Frozen artifacts: see spec.freeze_artifacts

## 13) v2 Freeze Eligibility (recorded)

All six required checks PASS with concrete evidence_refs in spec.freeze_eligibility:
decision_rule_reachability PASS; measurement_prerequisites PASS; baseline_identifiability PASS; control_sensitivity PASS; treatment_liveness PASS; freeze_artifacts_bound PASS.
Before freezing, EXECUTE must verify hash equality of freeze_artifacts and confirm that the two per-cell configs materialized by the section 4.6 overlay differ ONLY in `prompts.system` (their sha256 is recorded in provenance.json).

## 14) Execution Procedure (EXECUTE-time, not performed in DESIGN)

1. Verify sha256 of the five spec.freeze_artifacts against freeze.json.artifact_hashes. Materialize the per-cell configs by the section 4.6 overlay rule (load the frozen parent harness_config.json; replace ONLY prompts.system with the condition string) and record their sha256 in provenance.json.
2. Provision GGUFs: download the M-7B-QWEN split shards (00001/00002) and the M-3B-QWEN single file to /tmp/opencode/gguf/, verify sha256 against the pinned values; the 7B single-file URL is expected to 404 and must not be used. On mismatch -> provisioning_failure -> MEASUREMENT_INVALID.
3. Build/install llama-cpp-python 0.2.90 from sdist (cmake+gcc present); install playwright and confirm Chrome at /usr/bin/google-chrome.
4. PREFLIGHT: PC-ORACLE-EPISODE 5/5, NC (parseable 0.0, success 0.0), B-RANDOM (parseable 1.0, success < 0.6), stack imports OK, digest checks PASS. Else MEASUREMENT_INVALID.
5. For M-7B-QWEN: run the P-COMP cell (unconditionally) and the P-TREAT cell, each with PC-JSON 10/10 first then 5 episodes; apply rules 2b-2d. If the TREAT cell clears -> SUPPORTS (PROMPT_ATTRIBUTED), STOP.
6. Otherwise evaluate M-3B-QWEN identically; if its TREAT cell clears -> SUPPORTS, STOP; else apply rule 3 (FALSIFIES) or rule 4 (MEASUREMENT_INVALID).
7. Write result.json, report.md, provenance.json per EXPERIMENT_PACKET.md. Keep RAW EVIDENCE / OBSERVATIONS / DERIVED MEASUREMENTS / INTERPRETATION distinct; record the materialized driver/config sha256 in provenance.json; do not self-promote claims.

## 15) Compliance Notes

- DESIGN ONLY: no outcome-bearing measurements performed. Cheap non-outcome-bearing satisfiability probes P-0..P-6 allowed and recorded.
- Treatment/comparator identity: only prompts.system varies; no post-freeze design changes.
- Parent handoff distinctions preserved; Director mandate binding; parent_handoff_disposition=SUPERSEDE respected.
- v2 contract satisfied: six freeze_eligibility checks complete, freeze_artifacts bound, stable metric/control IDs, explicit precedence, both-outcome consequences stated.

## Appendix A: Byte-exact materialization notes (EXECUTE)

- Config files to materialize (deterministic names): `configs/exp_38123995594_pcomp_unspec.json`, `configs/exp_38123995594_ptreat_goalschema.json`. Each is produced by loading the frozen parent fixture `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (file sha256 7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb), deep-copying it, replacing ONLY `prompts.system` with the condition string from section 4.6, and serializing deterministically (json.dumps with sort_keys=True). All other keys (positive_control probe string/count, null_control content, random_baseline action space, task.page_html, gbnf_grammar, sampling, clearing_threshold) are thereby inherited byte-for-byte. Verify at EXECUTE that the two materialized configs differ ONLY in prompts.system, and record each sha256 in provenance.json.
- Harness delta `research/intel/run_exp_38123995594.py` must: (a) import parse_action / regex_parse_action / run_episode / make_null_producer / make_random_producer / make_model_producer / start_page_server from `research/intel/run_exp_37982024058.py` (the frozen parent runner) and MUST NOT copy or re-implement that logic (the file is a freeze artifact, so the parsing/scoring/episode semantics are bound to its sha256), (b) accept `--config`, `--model` (model paths list for 7B shards), `--cell` (comp|treat|random|nc|pc_oracle), `--episodes`, `--out`, (c) enforce GGUF digest checks against the pinned map, (d) implement navigation-repaired controls, (e) collect the comparator cell unconditionally before any treatment decision, (f) enforce the PC gates, (g) apply decision precedence 1..4 and write packet artifacts to the experiment dir, (h) compute answer_action_emission_rate from raw steps.
- Navigation repair is mandatory and explicit: the repaired controls driver MUST call `page.goto("http://127.0.0.1:<served_port>/")` on the Playwright page before each control episode (the frozen run_episode opens with `page.goto(page.url)`; if the page were left at about:blank - the parent's defect - the control would be structurally zeroed). The candidate cells inherit the frozen parent runner's own correct navigation and are unaffected. After running, verify the control's terminal page state (`final_target_visible` for NC must be false) as an additional mechanical check.
- EXECUTE must record the materialized sha256 of the driver and of both per-cell configs (and of the parent runner re-verified to its freeze hash) in provenance.json#code / provenance.json#fixtures.
- No other behavioral changes; the new driver only orchestrates config materialization, digest checks, control execution, aggregation and the decision rule. It performs no outcome interpretation and self-promotes no claim.
