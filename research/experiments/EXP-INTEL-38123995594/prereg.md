# PRE-REGISTRATION: EXP-INTEL-38123995594 (INTEL, design_contract_version=2)

Title: Prompt ablation: does supplying task goal+schema in the system prompt convert the step-0 reveal-click into a full click-then-answer completion for M-7B-QWEN / M-3B-QWEN under the same credential-free CPU-quantized constraints as EXP-INTEL-37982024058?

Experiment ID: EXP-INTEL-38123995594 | Lane: intel | Claim IDs: ["C-LLM-INHERIT"]
Status: DESIGN (pre-freeze; DESIGN ONLY). No outcome-bearing measurements performed.
Request reference: research/experiments/EXP-INTEL-38123995594/request.json
Parent handoff (continuity, not authorization): research/experiments/EXP-INTEL-37982024058/handoff.json (sha256 b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55)

## 1) Rationale and Context (binding)

- Director mandate (binding): action CONTINUE, claim C-LLM-INHERIT, cognitive_reset true, parent_handoff_disposition SUPERSEDE. Question verbatim: "Would supplying the task goal/schema in the system prompt (as the parent harness's SYS prompt did) convert the step-0 reveal-click into a full click-then-answer completion for M-7B-QWEN or M-3B-QWEN under the same credential-free CPU-quantized constraints?"
- Parent result (frozen evidence): EXP-INTEL-37982024058 produced an audited FALSIFIES on C-LLM-INHERIT (audit status PASS, producer_claim_supported=true, VF-01 material). Both models emitted a valid click at step 0 (parseable_action_rate_step1=1.0, 5/5), the target was revealed (revealed_value='TARGET-42'), then both re-emitted {"action":"click","selector":"#reveal-btn"} for steps 1-4 and never emitted an answer action (task_success_rate=0.0, 5/5). Constrained decoding PC 10/10 both models; NC 0/5 parseable; B-RANDOM 5/5 parseable, 0/5 success.
- Mechanistic hypothesis (audit VF-01): prompt underspecification. The parent system prompt states neither the action schema nor the terminal goal. The grandparent harness (EXP-INTEL-37973264582) SYS constant contained both. The treatment is that prompt, recovered exactly, with one disclosed adjustment.
- Epistemic boundary: the parent handoff is continuity evidence only and MUST NOT silently override the Director's SUPERSEDE/CONTINUE decision. Its established/rejected/unknown/do_not_assume distinctions are preserved in section 11 and are not treated as an agenda.

## 2) Non-duplication and Legacy Check

- POLICY.md requires non-duplication: targeted reads of codex/legacy_brief.json, codex/legacy_artifact_index.json and codex/index.json (Research 2.0 section) show no material legacy hits for local CPU-quantized small-model capability probing or programmatic credential-free endpoints ("qwen", "capability", "endpoint"). Nearest legacy: P2-REPLAY-COST (sha 9687ff787f...) guard applies downstream to replay/economics (not this capability probe); P2-BLIND-COMPOSITION (sha 017a80ae...) out of scope; P2-MIND2WEB out of scope.
- The Director mandate's own comparative_reasoning records "LEGACY: NO_MATCH, with an explicit search limitation" and states this probe is NOT a rerun of EXP-INTEL-37982024058: it adds the goal/schema system prompt and isolates prompt-underspecification from capability.
- Siblings that never froze are NOT evidence sources: EXP-INTEL-38013769440, EXP-INTEL-38106207218, EXP-INTEL-38110512532, EXP-INTEL-38121203425. The last three share the design-review control-plane failure fingerprint 3b9ff5e4e9e73f23e368efb4 (model opencode/exo-free, exit_code 1, category substantive) documented by the Director as a shared outage, not a scientific design verdict.

## 3) Design: Only One Varied Dimension

- Candidate models: M-7B-QWEN (Qwen2.5-7B-Instruct-Q4_K_M split shards, digests pinned) evaluated first; M-3B-QWEN (Qwen2.5-3B-Instruct-Q4_K_M single file, digest pinned) evaluated only if M-7B-QWEN treatment does NOT clear (early stop on first clearing treatment).
- Task, fixture, grammar, sampling, seeds, harness code path, model artifacts and environment identical across cells.
- Prompt conditions (ONLY prompts.system varies):

P-COMP-UNDERSPECIFIED (comparator; frozen expected anchor):
  "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown."
  Provenance: byte-identical to EXP-INTEL-37982024058 raw/harness_config.json#prompts.system (sha256 7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb).

P-TREAT-GOAL-SCHEMA (treatment):
  "You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {\"action\":\"click\",\"selector\":\"<id>\"} or {\"action\":\"answer\",\"text\":\"<code>\"}. Click the button to reveal the code, then answer it."
  Provenance: grandparent raw/code/min_webagent.py SYS (sha256 4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862) with the single ref->selector schema alignment. Justification: the frozen GBNF admits only the keys "selector" and "text"; the grandparent prompt's "ref" key is not in the grammar, so aligning the prompt's named schema to the grammar-enforced schema ensures the treatment measures the goal+schema content rather than a prompt/grammar key mismatch. No '#reveal-btn' or 'TARGET-42' leakage (design-time verified).

## 4) Protocol, Controls, and Comparator Validity

4.1 Deterministic protocol (inherited)
- temperature=0.0, max_tokens=512, n_ctx=2048, chat_format=qwen, llama_seed=42, episode_seed_offset="42 + episode_idx", seeds 42..46 for episodes 0..4 (base 42). max_steps_per_episode=5.

4.2 Task fixture (inherited)
- Identical minimal page from EXP-INTEL-37982024058 raw/harness_config.json: button #reveal-btn reveals div #target containing "TARGET-42". Scorer identical (Playwright DOM assertions + strict JSON parse against the frozen GBNF/action schema). run_episode calls page.goto(page.url) at the start of each episode, so the model episodes and all repaired controls run against the served page.

4.3 Positive controls
- PC-JSON-CONSTRAINED-DECODING: 10 probes per cell ("Emit exactly: {\"action\":\"click\",\"selector\":\"#test\"}") under that cell's prompts.system + frozen GBNF. Must be 10/10 before the cell's episodes; if both candidates' treatment-cell PCs fail -> OUTCOME=MEASUREMENT_INVALID.
- PC-ORACLE-EPISODE: 5 scripted click-then-answer episodes (click #reveal-btn then answer TARGET-42) through the real run_episode scorer against the served page. Must be 5/5 at preflight; <5/5 -> MEASUREMENT_INVALID (scorer broken, not model behavior).

4.4 Null/negative controls
- NC-NO-MODEL-ACTION: 5 episodes of fixed non-JSON content ("I will click the button") through the real scorer against the SERVED page. Must be parseable 0.0 and success 0.0; any parseable/success -> MEASUREMENT_INVALID.
- B-RANDOM-ACTION: seeded RNG random.Random(42) created once and reused across episodes (as in the parent), run against the SERVED page (navigation repaired vs the parent's about:blank defect), 5-action uniform space, valid JSON by construction. Must be parseable_action_rate_step1 == 1.0 and task_success_rate < 0.6 (per-episode success probability <= 1/25, so P(bar cleared by chance) < 4e-4). If task_success_rate >= 0.6 -> MEASUREMENT_INVALID (control broken).

4.5 Comparator validity (fail-closed, refined anchor policy)
- For each evaluated candidate, the P-COMP comparator cell is collected unconditionally BEFORE any outcome decision, in the same run as the treatment cell. The identification contrast is this contemporaneous within-run pair (same model, same harness, same sampling schedule, same environment; only prompts.system differs).
- HARD INVALIDATION (MEASUREMENT_INVALID): a comparator cell that CLEARS the capability bar (task_success_rate >= 0.6) makes the prompt effect non-identifiable; a comparator cell with parseable_action_rate_step1 < 0.6 indicates protocol/decoding drift.
- EXPECTED ANCHOR: the frozen parent tuple (task_success_rate=0.0, parseable_action_rate_step1=1.0, answer_action_emission_rate=0.0) from EXP-INTEL-37982024058 result.json#metrics. Exact match -> record REPLICATION_ANCHOR_EXACT. A bar-failing deviation that preserves parseability -> record REPLICATION_ANCHOR_DRIFT as a validity note; the paired contrast remains identifiable and the packet need not be invalidated, but the report must state that the historical parent anchor was not exactly reproduced.
- Rationale: the comparator's role is a contemporaneous control, not a byte-replay of history; historical exactness is a drift monitor. This prevents a spurious infrastructure invalidation (e.g., a rebuild producing minor floating-point drift) while preserving attribution.

4.6 Byte-exact frozen blocks (bound for EXECUTE materialization)

Per-condition config blocks (identical structure to the parent harness_config; only prompts.system differs).

Config P-COMP-UNSPEC (byte-exact reference string content):
```
{
  "gbnf_grammar": "root ::= ws \"{\" ws \"\\\"action\\\"\" ws \":\" ws action ws \",\" ws field ws \"}\" ws\nws ::= [ \\t\\n]*\naction ::= \"\\\"click\\\"\" | \"\\\"answer\\\"\"\nfield ::= \"\\\"selector\\\"\" ws \":\" ws string | \"\\\"text\\\"\" ws \":\" ws string\nstring ::= \"\\\"\" strchars \"\\\"\"\nstrchars ::= strchar strchars | strchar\nstrchar ::= [^\"\\\\] | \"\\\\\" ([\"\\\\/bfnrt] | \"u\" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])\n",
  "prompts": {
    "system": "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.",
    "user_template": "PAGE_TEXT: {page_text}\nELEMENTS: {elements_json}\nHISTORY: {history}\nNext action (JSON only): "
  },
  "sampling": {
    "temperature": 0.0,
    "max_tokens": 512,
    "base_seed": 42,
    "episode_seed_offset": "42 + episode_idx",
    "n_ctx": 2048,
    "chat_format": "qwen",
    "llama_seed": 42
  },
  "task": {"max_steps_per_episode": 5},
  "clearing_threshold": {"task_success_rate_min": 0.6, "parseable_action_rate_step1_min": 0.6, "episodes": 5}
}
```

Config P-TREAT-GOAL-SCHEMA (only system differs):
```
{
  "gbnf_grammar": "root ::= ws \"{\" ws \"\\\"action\\\"\" ws \":\" ws action ws \",\" ws field ws \"}\" ws\nws ::= [ \\t\\n]*\naction ::= \"\\\"click\\\"\" | \"\\\"answer\\\"\"\nfield ::= \"\\\"selector\\\"\" ws \":\" ws string | \"\\\"text\\\"\" ws \":\" ws string\nstring ::= \"\\\"\" strchars \"\\\"\"\nstrchars ::= strchar strchars | strchar\nstrchar ::= [^\"\\\\] | \"\\\\\" ([\"\\\\/bfnrt] | \"u\" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])\n",
  "prompts": {
    "system": "You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {\"action\":\"click\",\"selector\":\"<id>\"} or {\"action\":\"answer\",\"text\":\"<code>\"}. Click the button to reveal the code, then answer it.",
    "user_template": "PAGE_TEXT: {page_text}\nELEMENTS: {elements_json}\nHISTORY: {history}\nNext action (JSON only): "
  },
  "sampling": {"temperature": 0.0, "max_tokens": 512, "base_seed": 42, "episode_seed_offset": "42 + episode_idx", "n_ctx": 2048, "chat_format": "qwen", "llama_seed": 42},
  "task": {"max_steps_per_episode": 5},
  "clearing_threshold": {"task_success_rate_min": 0.6, "parseable_action_rate_step1_min": 0.6, "episodes": 5}
}
```

Controls driver requirements (EXECUTE materialization): random baseline and NC must navigate to the served page before selecting actions (fix parent about:blank defect); PC-ORACLE runs through the real scorer; all controls use the same run_episode scorer as the candidates.

Harness delta: new runner `research/intel/run_exp_38123995594.py` (thin; imports parse_action / regex_parse_action / run_episode / control producers from the frozen `research/intel/run_exp_37982024058.py`, accepts per-cell config path and model paths, enforces digest checks, runs PC gates, collects comparator unconditionally, runs repaired controls, applies precedence 1..6). Its content is bound by Appendix A; EXECUTE records its sha256.

## 5) Metrics and Stable IDs

- positive_control_pass_rate: fraction of the 10 per-cell JSON-decode probes that produce schema-valid JSON.
- parseable_action_rate_step1: fraction of episodes whose step-0 completion is a strict-parseable schema-conforming action (>=0.6 required to clear).
- answer_action_emission_rate: fraction of episodes containing at least one strict-parseable action with action=="answer" (0.0 expected for the comparator anchor; descriptive otherwise).
- task_success_rate: fraction of episodes where the reveal click executed, revealed_value == "TARGET-42", and the terminal answer stripped == "TARGET-42" within 5 steps (>=0.6 required to clear).
- mean_inference_latency_s: mean wall-clock seconds per model call over episode steps (descriptive).
- mean_completion_tokens: mean completion tokens per model call over episode steps (descriptive).

## 6) Decision Rule (exact precedence)

OUTCOME in {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}; status COMPLETE unless operational blockers preclude any cell. A cell clears iff task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6 over its 5 episodes. Precedence (first matching rule wins):

1. PREFLIGHT: PC-ORACLE-EPISODE == 5/5 AND NC-NO-MODEL-ACTION == (parseable 0.0, success 0.0) AND B-RANDOM-ACTION == (parseable 1.0, task_success_rate < 0.6) AND all freeze_artifact hash checks match AND required stack imports OK AND GGUF digest checks PASS. Else OUTCOME=MEASUREMENT_INVALID.
2. COMPARATOR VALIDITY: for any evaluated comparator cell, if task_success_rate >= 0.6 OR parseable_action_rate_step1 < 0.6 -> OUTCOME=MEASUREMENT_INVALID. Else record the tuple: exact (0.0, 1.0, 0.0) -> REPLICATION_ANCHOR_EXACT; any other bar-failing value -> REPLICATION_ANCHOR_DRIFT validity note.
3. INCOMPLETE: if both candidate pairs are incomplete (fewer than 5 episode records in any evaluated cell) -> OUTCOME=MEASUREMENT_INVALID.
4. Evaluate the M-7B-QWEN pair (COMP: PC-JSON 10/10 then 5 episodes; TREAT: PC-JSON 10/10 then 5 episodes; comparator collected unconditionally). If the TREAT cell clears -> OUTCOME=SUPPORTS, attribution=PROMPT_ATTRIBUTED. STOP (M-3B-QWEN not evaluated).
5. Else evaluate the M-3B-QWEN pair identically. If its TREAT cell clears -> OUTCOME=SUPPORTS with the same attribution. STOP.
6. Else (no TREAT cell cleared, at least one pair complete and comparator-valid) -> OUTCOME=FALSIFIES (Director's bounded negative).

report.md must record, per evaluated candidate, the failure-mode descriptor (answer_action_emission_rate, click loop count, step-0 reveal success) and the bounded-negative wording exactly.

## 7) Reachability Proof (non-outcome-bearing)

- SUPPORTS reachable: PC-ORACLE-EPISODE 5/5 proves the scorer registers the full click-then-answer path; the treatment prompt is feasible under the frozen GBNF. Comparator expected to fail the bar preserves attribution.
- FALSIFIES reachable: the parent already realized 0/5 under the comparator prompt; the treatment may also fail (recurring loop, zero answer action) with at most 2 candidates evaluated under early stop.
- MEASUREMENT_INVALID reachable via preflight failure, comparator clearing the bar / losing parseability, cell incompleteness, freeze-artifact hash mismatch, GGUF digest mismatch, provisioning failure, or PC failure. No rule shadows another: comparator cells are collected unconditionally before (4); (6) fires only when complete, comparator-valid, and no treatment cleared.
- Threshold 0.6 over 5 episodes (>=3/5) is attainable for both extremes; the random baseline is strictly below the bar by construction (P(chance clearance) < 4e-4).

## 8) Non-Outcome-Bearing Satisfiability Probes (design-contract v2)

Performed at DESIGN (logged for EXECUTE preflight):
- P-0 Env/importability: cmake 3.31.6, gcc/g++ 13.3.0, Python.h (Python 3.12.15), pip 26.2.1 present; llama-cpp-python 0.2.90 sdist published on PyPI, no cp312 wheel -> sdist build feasible; playwright 1.63.0 installable; /usr/bin/google-chrome present. PASS.
- P-1 Grammar well-formedness: the parent GBNF defines and references all 7 rules (root, ws, action, field, string, strchars, strchar); constructible by the parent-executed grammar path. PASS.
- P-2 Prompt non-leakage / byte-identity: P-TREAT-GOAL-SCHEMA contains neither "#reveal-btn" nor "TARGET-42"; P-COMP-UNDERSPECIFIED is byte-identical to parent harness_config.json#prompts.system. PASS.
- P-3 Provisioning liveness: 3B resolve URL HTTP 302, 7B shard1 302, shard2 302, 7B single-file 404 (documented deviation); digests pinned from raw/gguf_sha256.txt. PASS.
- P-4 Task/scorer/oracle path: the parent executed the served-page oracle/scorer end-to-end (task_episodes.json); the controls driver's navigation repair is a mechanical requirement specified in 4.5/Appendix A. PASS.

## 9) Validity Threats and Mitigations

- Comparator drift: comparator cells are collected unconditionally and compared to the frozen parent anchor; hard invalidation if the comparator clears the bar or loses parseability; lesser drift recorded as a validity note (4.5).
- Prompt leakage: treatment must not name specific selectors/targets (explicit non-leakage check); GBNF keys restricted to selector/text.
- Control sensitivity: random/NC/oracle run against the served page (navigation repaired) via the same scorer, so a null cannot be a navigation artifact and a positive is registerable.
- Provisioning: GGUF digest checks against raw/gguf_sha256.txt; URL route confirmed live; 7B split shards pinned (single-file 404 known). Mismatch -> MEASUREMENT_INVALID.
- Decoder-capability conflation: comparator re-measured in the same run for each model; only prompts.system changes, so a treatment clearance with a bar-failing comparator is attributable to the prompt.
- Early-stop bias: M-7B-QWEN pair is fully evaluated first; M-3B-QWEN is evaluated only if 7B does not clear. The negative is therefore not overstated across both models unless both treatment cells were actually measured.
- Build chain: llama-cpp-python 0.2.90 sdist build (no cp312 wheel) - cmake+gcc present; if the build fails at EXECUTE -> provisioning_failure -> MEASUREMENT_INVALID (not a model result).
- Bundled treatment: the treatment bundles the goal sentence, the schema enumeration, and the prompt wording. If it clears, the decomposition (goal vs schema enumeration vs generic longer instruction) is NOT identified; this is recorded as unresolved and bounded in report.md.

## 9.1) Design-time self-attack (constructibility, recorded before freeze)

Each named v2 DESIGN-failure class was actively attacked and resolved:

- Empty/unreachable branches: precedence 1..6 is fully enumerated; SUPPORTS needs >=3/5 in a treatment cell (registerable per PC-ORACLE), FALSIFIES needs all treatment cells <0.6 (parent realized this), MEASUREMENT_INVALID is reachable via preflight/comparator/incompleteness. No rule is shadowed; comparator cells are collected before any decision. (Section 7.)
- Arithmetic impossibility: threshold 3/5 over 5 episodes is attainable for both extremes; early stop means at most 2 candidates are evaluated; no branch requires more episodes than the frozen 5.
- Ceiling/floor baselines: comparator sits at the realized floor (0/5), PC-ORACLE at the ceiling (5/5); dynamic range is full, so a treatment effect is identifiable. The random control is strictly below the bar (P(clearance) < 4e-4), so the bar cannot be cleared by chance.
- Treatment/comparator identity: byte-diffed at design time; only prompts.system changes; all other outcome-relevant config keys are byte-identical to the parent fixture (verified by parsing both section 4.5 blocks). No leakage of the selector or the answer text into the treatment.
- Insensitive controls: PC-JSON fires 10/10 (parent-verified) and PC-ORACLE fires 5/5; NC stays 0/0; B-RANDOM cannot reach 0.6. Each control has a distinct, attainable expected value.
- Missing prerequisites: Python 3.12.15, cmake 3.31.6, gcc/g++ 13.3, Python.h, pip 26.2.1, /usr/bin/google-chrome verified; llama-cpp-python 0.2.90 sdist present on PyPI (no cp312 wheel) so the build path is required and feasible; playwright 1.63.0 installable; all three GGUF resolve URLs verified live (7B single-file 404 documented); parent end-to-end execution proves the task/scorer path.
- Unbound mutable artifacts: five existing freeze_artifacts hashed; the outcome-determining parsing/scoring/episode code is bound by importing the frozen parent runner (no re-implementation); the only EXECUTE-created files (per-cell configs, thin driver) are bound by byte-exact prereg section 4.5 / Appendix A and their sha256 recorded in provenance.json.

Residual risks (documented, not hidden): (R1) a rebuilt llama.cpp could produce minor floating-point drift from the parent build - handled by the comparator policy (drift note vs hard invalidation), not by changing the science; (R2) the thin driver itself is not a freeze artifact (it cannot exist at freeze time) - mitigated by the import binding and Appendix A; (R3) a treatment clearance would not decompose goal-sentence vs schema-enumeration vs generic longer instruction - recorded as unresolved; (R4) the split-shard 7B packaging could change in future repo revisions - the current digests pin the exact artifacts.

## 10) Prerequisites, Costs, and Expected Information Gain

- Prerequisites: CPU-only, 4 cores, ~15 GB RAM, /usr/bin/google-chrome, Python 3.12.15, pip 26.2.1, cmake 3.31.6, gcc 13.3, Python.h. GGUFs are NOT present in /tmp/opencode/gguf/ and llama-cpp-python/playwright are not installed in this factory, so EXECUTE must re-download (~6.8 GB) and install/build.
- Cost estimate: 45-150 min wall-clock; inference ~10-25 min worst case; provisioning/build 25-60 min. No external API spend.
- Information gain: High and decision-changing in both directions. SUPPORTS unblocks the four-arm benchmark with a verified goal/schema prompt and bounds the parent FALSIFIES to the underspecified-prompt ceiling. FALSIFIES (bounded negative) closes the credential-free local 3B-8B Qwen path as a capability result (not a prompt artifact) and records the receipts for a hosted-endpoint / different-model-class re-scope. This is readiness-condition-(3) work allocated by the Director (agent_priors_used: a cheap probe that separates two competing explanations is higher decision value than another benchmark run on an unverified endpoint).

## 11) Inherited State (parent_handoff preserved, not treated as agenda)

- established: under the frozen underspecified-prompt protocol, no credential-free model cleared the bar (M-7B-QWEN 0/5, M-3B-QWEN 0/5, audit PASS); constrained decoding PC 10/10; NC 0/5 parseable; B-RANDOM 5/5 parseable, 0/5 success; step-0 reveal succeeds and both models re-click the hidden button, never emitting an answer.
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
- Frozen artifacts: see spec.freeze_artifacts

## 13) v2 Freeze Eligibility (recorded)

All six required checks PASS with concrete evidence_refs in spec.freeze_eligibility:
decision_rule_reachability PASS; measurement_prerequisites PASS; baseline_identifiability PASS; control_sensitivity PASS; treatment_liveness PASS; freeze_artifacts_bound PASS.
Before freezing, EXECUTE must verify hash equality of freeze_artifacts and byte-exact equality of the two per-condition configs materialized from section 4.5/Appendix A.

## 14) Execution Procedure (EXECUTE-time, not performed in DESIGN)

1. Verify sha256 of the five spec.freeze_artifacts against freeze.json.artifact_hashes. Materialize the per-cell configs from section 4.5 (byte-exact) and verify their sha256 against the frozen blocks recorded in freeze.json/provenance.
2. Provision GGUFs: download the M-7B-QWEN split shards (00001/00002) and the M-3B-QWEN single file to /tmp/opencode/gguf/, verify sha256 against the pinned values; the 7B single-file URL is expected to 404 and must not be used. On mismatch -> provisioning_failure -> MEASUREMENT_INVALID.
3. Build/install llama-cpp-python 0.2.90 from sdist (cmake+gcc present); install playwright 1.63.0 and confirm Chrome at /usr/bin/google-chrome.
4. PREFLIGHT: PC-ORACLE-EPISODE 5/5, NC (parseable 0.0, success 0.0), B-RANDOM (parseable 1.0, success < 0.6), stack imports OK, digest checks PASS. Else MEASUREMENT_INVALID.
5. For each evaluated candidate, run the P-COMP cell (unconditionally) with PC-JSON 10/10 first, then 5 episodes; apply comparator-validity rule 2.
6. Evaluate M-7B-QWEN TREAT (PC-JSON 10/10, 5 episodes). If it clears -> SUPPORTS (PROMPT_ATTRIBUTED), STOP. Else evaluate M-3B-QWEN pair identically. If it clears -> SUPPORTS, STOP. Else FALSIFIES.
7. Write result.json, report.md, provenance.json per EXPERIMENT_PACKET.md. Keep RAW EVIDENCE / OBSERVATIONS / DERIVED MEASUREMENTS / INTERPRETATION distinct; record the materialized driver/config sha256 in provenance.json; do not self-promote claims.

## 15) Compliance Notes

- DESIGN ONLY: no outcome-bearing measurements performed. Cheap non-outcome-bearing satisfiability probes P-0..P-4 allowed and recorded.
- Treatment/comparator identity: only prompts.system varies; no post-freeze design changes.
- Parent handoff distinctions preserved; Director mandate binding; parent_handoff_disposition=SUPERSEDE respected.
- v2 contract satisfied: six freeze_eligibility checks complete, freeze_artifacts bound, stable metric/control IDs, explicit precedence, both-outcome consequences stated.

## Appendix A: Byte-exact materialization notes (EXECUTE)

- Config files to materialize (deterministic names): `configs/exp_38123995594_pcomp_unspec.json`, `configs/exp_38123995594_ptreat_goalschema.json` - content must equal the JSON blocks in section 4.5 byte-for-byte (including whitespace/quotes). sha256 computed at freeze time; re-verified at EXECUTE and recorded in provenance.json.
- Harness delta `research/intel/run_exp_38123995594.py` must: (a) import parse_action / regex_parse_action / run_episode / make_null_producer / make_random_producer / make_model_producer / start_page_server from `research/intel/run_exp_37982024058.py` (the frozen parent runner) and MUST NOT copy or re-implement that logic (the file is a freeze artifact, so the parsing/scoring/episode semantics are bound to its sha256), (b) accept `--config`, `--model` (model paths list for 7B shards), `--cell` (comp|treat|random|nc|pc_oracle), `--episodes`, `--out`, (c) enforce GGUF digest checks against the pinned map, (d) implement navigation-repaired controls, (e) collect the comparator cell unconditionally before any treatment decision, (f) enforce the PC gates, (g) apply decision precedence 1..6 and write packet artifacts to the experiment dir, (h) compute answer_action_emission_rate from raw steps.
- Navigation repair is mandatory and explicit: the repaired controls driver MUST call `page.goto("http://127.0.0.1:<served_port>/")` on the Playwright page before each control episode (the frozen run_episode opens with `page.goto(page.url)`; if the page were left at about:blank - the parent's defect - the control would be structurally zeroed). The candidate cells inherit the frozen parent runner's own correct navigation and are unaffected. After running, verify the control's terminal page state (`final_target_visible` for NC must be false) as an additional mechanical check.
- EXECUTE must record the materialized sha256 of the driver and of both per-cell configs (and of the parent runner re-verified to its freeze hash) in provenance.json#code / provenance.json#fixtures.
- No other behavioral changes; the new driver only orchestrates config materialization, digest checks, control execution, aggregation and the decision rule. It performs no outcome interpretation and self-promotes no claim.
