# PRE-REGISTRATION: EXP-INTEL-38121203425 (INTEL, design_contract_version=2)

Title: Prompt ablation: does supplying task goal+schema in the system prompt convert the step-0 reveal-click into a full click-then-answer completion for M-7B-QWEN and M-3B-QWEN under the same credential-free CPU-quantized constraints as EXP-INTEL-37982024058?

Experiment ID: EXP-INTEL-38121203425 | Lane: intel | Claim IDs: ["C-LLM-INHERIT"]
Status: DESIGN (pre-freeze; DESIGN ONLY). No outcome-bearing measurements performed.
Request reference: research/experiments/EXP-INTEL-38121203425/request.json

## 1) Rationale and Context (binding)

- Director mandate (binding): action CONTINUE, claim C-LLM-INHERIT, cognitive_reset true. Question verbatim: "Would supplying the task goal/schema in the system prompt (as the parent harness's SYS prompt did) convert the step-0 reveal-click into a full click-then-answer completion for M-7B-QWEN or M-3B-QWEN under the same credential-free CPU-quantized constraints?"
- Parent result (frozen evidence): EXP-INTEL-37982024058 produced an audited FALSIFIES on C-LLM-INHERIT (audit PASS, VF-01 material). Both models emitted valid click at step 0 (parseable_action_rate_step1=1.0, 5/5), revealed TARGET-42, then re-emitted {"action":"click","selector":"#reveal-btn"} and never emitted an answer action (task_success_rate=0.0, 5/5). Constrained decoding PC 10/10; NC/B-RANDOM behaved as expected.
- Epistemic boundary: parent_handoff from EXP-INTEL-37982024058 is continuity evidence only and MUST NOT silently override a SUPERSEDE/PIVOT/REOPEN Director decision. Established/rejected/unknown/do_not_assume are preserved; the Director's CONTINUE target claim/strategic question are binding.
- Mechanistic hypothesis: audit VF-01 identifies prompt underspecification (omitted goal+schema). Grandparent (EXP-INTEL-37973264582) used a richer SYS prompt including action schema enumeration and the goal sentence; the parent task's frozen GBNF grammar uses "selector"/"text" (not "ref"), so treatment must adapt ref->selector.

## 2) Non-duplication and Legacy Check

- POLICY.md requires non-duplication: targeted reads of codex/legacy_brief.json, codex/legacy_artifact_index.json, .spider-runtime/pre2/SPIDER_CODEX_ULTIME.md show no material legacy hits for local CPU-quantized small-model capability probing or programmatic credential-free endpoints ("qwen", "capability", "endpoint"); nearest legacy: P2-REPLAY-COST (9687ff787f...) guard applies downstream to replay/economics (not this capability probe), P2-BLIND-COMPOSITION (017a80ae...) out of scope, P2-MIND2WEB out of scope.
- Siblings EXP-INTEL-38106207218/38110512532 failed at design stage (fingerprint 3b9ff5e4e9e73f23e368efb4), never froze; this design uses the Director CONTINUE mandate with paired-comparator fail-closed anchor, navigation-repaired controls, digest-pinned provisioning.

## 3) Design: Only One Varied Dimension

- Candidate models: M-7B-QWEN (Qwen2.5-7B-Instruct-Q4_K_M split shards, digests pinned) evaluated first; M-3B-QWEN (Qwen2.5-3B-Instruct-Q4_K_M single file, digest pinned) evaluated only if M-7B-QWEN treatment does NOT clear (early stop on first clearing treatment).
- Task, fixture, grammar, sampling, seeds, harness code path, model artifacts identical across cells.
- Prompt conditions (ONLY prompts.system varies):

P-COMP-UNDERSPECIFIED (comparator, replication anchor):
  "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown."
  Provenance: byte-identical to EXP-INTEL-37982024058 raw/harness_config.json#prompts.system.

P-TREAT-GOAL-SCHEMA (treatment):
  "You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {\"action\":\"click\",\"selector\":\"<id>\"} or {\"action\":\"answer\",\"text\":\"<code>\"}. Click the button to reveal the code, then answer it."
  Provenance: grandparent raw/code/min_webagent.py SYS with ref->selector adaptation required by frozen GBNF (only selector/text keys). No '#reveal-btn' or 'TARGET-42' leakage (design-time verified).

## 4) Protocol, Controls, and Replication Anchor

4.1 Deterministic protocol (inherited)
- temperature=0.0, max_tokens=512, n_ctx=2048, chat_format=qwen, llama_seed=42, episode_seed_offset="42 + episode_idx", seeds 42..46 for episodes 0..4 (base 42). max_steps_per_episode=5.

4.2 Task fixture (inherited)
- Identical minimal page from EXP-INTEL-37982024058 raw/harness_config.json; #reveal-btn reveals #target containing TARGET-42. Scorer identical (Playwright DOM assertions + JSON parse against frozen GBNF/action schema).

4.3 Positive controls
- PC-JSON-CONSTRAINED-DECODING: 10 probes per cell ("Emit exactly: {\"action\":\"click\",\"selector\":\"#test\"}") under that cell's prompts.system + frozen GBNF. Must be 10/10 before cell's episodes; if both candidates' treatment cells fail -> OUTCOME=MEASUREMENT_INVALID.
- PC-ORACLE-EPISODE: 5 scripted click-then-answer episodes via real run_episode scorer against served page. Must be 5/5 at preflight; <5/5 -> MEASUREMENT_INVALID.

4.4 Null/negative controls
- NC-NO-MODEL-ACTION: 5 episodes fixed non-JSON content -> parseable 0.0, success 0.0; any parseable/success -> MEASUREMENT_INVALID.
- B-RANDOM-ACTION: seeded RNG random.Random(42) reused across episodes, run against SERVED page (navigation repaired vs about:blank defect), valid JSON by construction. parseable_action_rate_step1==1.0, task_success_rate < 0.6 (per-episode success probability <= 1/25, seed 42 expected 0/5). If task_success_rate >= 0.6 -> MEASUREMENT_INVALID (control broken).

4.5 Replication anchor (fail-closed)
- For each evaluated candidate, comparator cell P-COMP collected unconditionally before treatment decision. Must match frozen parent exactly: task_success_rate=0.0, parseable_action_rate_step1=1.0, answer_action_emission_rate=0.0 (from EXP-INTEL-37982024058 result.json#metrics). Any deviation -> MEASUREMENT_INVALID.

4.6 Byte-exact frozen blocks (bound for EXECUTE materialization)

Per-condition config blocks (identical structure to parent harness_config, only prompts.system differs):

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

Controls driver requirements (EXECUTE materialization; navigation repaired): random baseline must navigate to served page before selecting actions (fix parent about:blank defect); NC must use real scorer against served page; PC-ORACLE runs through real scorer.

Harness delta: new runner `research/intel/run_exp_38121203425.py` (thin, reuses parsing/scorer/episode logic from `research/intel/run_exp_37982024058.py`, accepts per-cell config path and model paths, enforces digest checks, runs PC gates, collects comparator unconditionally, applies precedence 1..6). Content of delta frozen conceptually by Appendix A; materialized at EXECUTE.

## 5) Metrics and Stable IDs

- positive_control_pass_rate (per cell and overall preflight)
- parseable_action_rate_step1 (>=0.6 required in decision rule)
- answer_action_emission_rate (0.0 expected for comparator anchor; descriptive for treatment/failures)
- task_success_rate (>=0.6 required; success = reached revealed target and emitted correct answer within 5 steps)
- mean_inference_latency_s (descriptive)
- mean_completion_tokens (descriptive)

## 6) Decision Rule (exact precedence)

OUTCOME in {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}, status COMPLETE unless operational blockers preclude any cell. Cell clears iff task_success_rate>=0.6 AND parseable_action_rate_step1>=0.6 over 5 episodes. Precedence (first matching wins):
1. PREFLIGHT: PC-ORACLE 5/5 AND NC (parseable 0.0, success 0.0) AND B-RANDOM (parseable 1.0, task_success_rate < 0.6) AND all freeze_artifact hash checks match AND required stack imports OK AND GGUF digest checks PASS -> else MEASUREMENT_INVALID.
2. REPLICATION-ANCHOR: any evaluated comparator cell != (task_success_rate=0.0, parseable_action_rate_step1=1.0, answer_action_emission_rate=0.0) -> MEASUREMENT_INVALID.
3. INCOMPLETE: if both candidate pairs incomplete (<5 episode records in any evaluated cell) -> MEASUREMENT_INVALID.
4. Evaluate M-7B-QWEN pair (COMP: PC-JSON 10/10 then 5 episodes; TREAT: PC-JSON 10/10 then 5 episodes; comparator collected unconditionally). If TREAT clears -> OUTCOME=SUPPORTS; attribution PROMPT_ATTRIBUTED if COMP failed bar per anchor (expected), else UNDETERMINED. STOP (do not evaluate M-3B-QWEN).
5. Else evaluate M-3B-QWEN pair identically. If TREAT clears -> OUTCOME=SUPPORTS with same attribution; STOP.
6. Else (no TREAT cleared, at least one pair complete) -> OUTCOME=FALSIFIES (Director's bounded negative).

report.md must record failure-mode descriptor per candidate (answer_action_emission_rate, click loop count, step-0 reveal success) and the bounded-negative wording exactly.

## 7) Reachability Proof (non-outcome-bearing)

- SUPPORTS reachable: PC-ORACLE 5/5 proves scorer registers full click-then-answer; treatment prompt is feasible under frozen GBNF (ref->selector verified). Comparator expected 0/5 preserves attribution.
- FALSIFIES reachable: parent already realized 0/5 under comparator; treatment may also fail (recurring loop, zero answer). With early stop after first clearing treatment, at most 2 candidates evaluated.
- MEASUREMENT_INVALID reachable via preflight, anchor deviation, incompleteness, GGUF digest mismatch, provisioning failure, PC failures. No rule shadows: comparator collected unconditionally before (4); (6) fires only when complete and no clearance.
- Threshold 0.6 over 5 episodes (>=3/5) is attainable for both extremes; random < 0.6 guaranteed (p<=1/25 per episode).

## 8) Non-Outcome-Bearing Satisfiability Probes (design-contract v2)

These are cheap checks to be performed at DESIGN/pre-freeze validation (and logged at EXECUTE preflight):
- P-0 Env/importability: cmake/gcc/g++/Python.h present; pip available; check llama-cpp-python==0.2.90 availability (wheel absent, sdist present) -> build feasible.
- P-1 Grammar compile: parent GBNF parses/validates (all rules referenced defined) under the parent parser logic; grammar bytes stable.
- P-2 Prompt non-leakage: P-TREAT-GOAL-SCHEMA contains neither "#reveal-btn" nor "TARGET-42" (verified). Comparator byte-identical to parent.
- P-3 Page serve/oracle: PC-ORACLE 5/5 against served page via real scorer (navigation repaired).
- P-4 Random determinism: B-RANDOM with seed 42 on served page -> parseable 1.0, task_success_rate < 0.6, reproducible.

All P-0..P-4 PASS at design time (see evidence_refs).

## 9) Validity Threats and Mitigations

- Replication drift: comparator collected unconditionally, must equal frozen anchor -> fail-closed MEASUREMENT_INVALID.
- Prompt leakage: treatment must not name specific selectors/targets (explicit non-leakage check). Grammar keys restricted to selector/text.
- Control sensitivity: random/NC run against served page (navigation repaired) via same scorer.
- Provisioning: GGUF digest checks against raw/gguf_sha256.txt; URL route confirmed live; 7B split shards pinned (single-file 404 known). Mismatch -> MEASUREMENT_INVALID.
- Decoder capability ceiling conflation: comparator replicates parent (0/5) for both models; only prompt changes, so attribution PROMPT_ATTRIBUTED if treatment clears while comparator fails.
- Early stop bias: early stop at first clearing treatment (evaluate M-7B-QWEN pair fully; only if no clearance evaluate M-3B-QWEN). This is conservative (does not overstate FALSIFIES across both models unless necessary).
- Build chain: llama-cpp-python 0.2.90 sdist build (no cp312 wheel) — cmake+gcc present; if build fails at EXECUTE -> provisioning_failure -> MEASUREMENT_INVALID.

## 10) Prerequisites, Costs, and Expected Information Gain

- Prerequisites: CPU-only, 4 cores, ~14GB RAM, /usr/bin/google-chrome, Python 3.12.15, pip 26.2.1, cmake 3.31.6, gcc 13.3, Python.h. GGUFs not present in /tmp/opencode/gguf/ -> re-download required at EXECUTE (~6.8GB).
- Cost estimate: 45-120 min wall-clock; inference ~15-25 min worst case; provisioning/build 25-55 min. No external API spend.
- Information gain: High and decision-changing in both directions. SUPPORTS unblocks four-arm benchmark with verified goal/schema prompt. FALSIFIES (bounded negative) closes credential-free local 3B-8B path as capability result (not prompt artifact) and records receipts for hosted-endpoint re-scope. This is readiness-condition-(3) allocated by Director.

## 11) Product Consequences (per outcome)

- SUPPORTS: prompt underspecification confirmed as driver (audit VF-01); C-LLM-INHERIT may advance from HYPOTHESIS toward EXPERIMENTAL under Director adjudication; verified goal/schema prompt becomes in-prompt task specification for frozen four-arm benchmark.
- FALSIFIES (bounded negative): step-0-reveal re-click loop not due to missing instruction context for 3B-8B class; capability ceiling real for credential-free CPU-quantized local models under this task; readiness condition (3) not satisfied by this model class. Director inputs recorded (E-LOCAL-LLAMA, E-POLLINATIONS-PROXY receipts) for re-scope (hosted endpoint with pinning/SLA, different model class, or dynamic-range task bank). Packet does not pre-decide.
- MEASUREMENT_INVALID: no claim change; repair required before re-run.

## 12) Transmission Identity (for downstream agents)

Stable IDs to reuse across EXECUTE/AUDIT/DIRECTOR:
- Experiment: EXP-INTEL-38121203425 (lane=intel)
- Claim: C-LLM-INHERIT
- Candidates: M-7B-QWEN, M-3B-QWEN
- Prompt conditions: P-COMP-UNDERSPECIFIED (stable_id), P-TREAT-GOAL-SCHEMA (stable_id)
- Controls: PC-JSON-CONSTRAINED-DECODING, PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION, B-RANDOM-ACTION, B-0.5B-QWEN-LOCAL (carried), B-POLLINATIONS-PROXY (carried)
- Metrics: positive_control_pass_rate, parseable_action_rate_step1, answer_action_emission_rate, task_success_rate, mean_inference_latency_s, mean_completion_tokens
- Baselines: B-UNDERSPECIFIED-PROMPT-7B, B-UNDERSPECIFIED-PROMPT-3B, B-RANDOM-ACTION
- Artifacts (frozen set): see spec.freeze_artifacts

## 13) v2 Freeze Eligibility (recorded)

All six required checks: decision_rule_reachability PASS, measurement_prerequisites PASS, baseline_identifiability PASS, control_sensitivity PASS, treatment_liveness PASS, freeze_artifacts_bound PASS (with concrete evidence_refs in spec). Before freezing, EXECUTE must verify hash equality of freeze_artifacts and byte-exact equality of the two per-condition configs materialized from section 4.5/Appendix A.

## 14) Execution Procedure (EXECUTE-time, not performed in DESIGN)

1. Pre-freeze hash check of freeze_artifacts listed in spec. Materialize per-cell configs from section 4.5 (byte-exact) to disk; verify sha256 against frozen blocks.
2. Provision GGUFs: download M-7B-QWEN shards 00001/00002 and M-3B-QWEN single file to /tmp/opencode/gguf/ (or configured cache), verify sha256 against pinned values; if 7B single-file returns 404 (expected), use shards. On mismatch -> provisioning_failure -> MEASUREMENT_INVALID.
3. Build/install llama-cpp-python 0.2.90 from sdist (cmake+gcc present); playwright install if needed; Chrome present.
4. PREFLIGHT: PC-ORACLE 5/5, NC (0.0,0.0), B-RANDOM (parseable 1.0, success<0.6), stack imports OK, digest checks PASS. Else MEASUREMENT_INVALID.
5. Replication-anchor path: for each candidate, run P-COMP cell (unconditionally) with PC-JSON 10/10 first, then 5 episodes; verify anchor match (0.0,1.0,0.0). Any deviation -> MEASUREMENT_INVALID.
6. Decision: evaluate M-7B-QWEN TREAT (PC-JSON 10/10, 5 episodes). If clears -> SUPPORTS (PROMPT_ATTRIBUTED), STOP. Else evaluate M-3B-QWEN pair identically. If clears -> SUPPORTS, STOP. Else FALSIFIES.
7. Write result.json, report.md, provenance.json per EXPERIMENT_PACKET.md. Keep RAW EVIDENCE/OBSERVATIONS/DERIVED/INTERPRETATION distinct; do not self-promote claims.

## 15) Compliance Notes

- DESIGN ONLY: no outcome-bearing measurements performed. Cheap non-outcome-bearing satisfiability probes P-0..P-4 allowed.
- Treatment/comparator identity: only prompts.system varies. No post-freeze changes.
- Parent handoff distinctions preserved; Director mandate binding.
- v2 contract satisfied: freeze_eligibility complete, freeze_artifacts bound, metrics/controls stable IDs, precedence explicit.

## Appendix A: Byte-exact materialization notes (EXECUTE)

- Config files to materialize (names deterministic): `configs/exp_38121203425_pcomp_unspec.json`, `configs/exp_38121203425_ptreat_goalschema.json` — content must equal the JSON blocks in 4.5 byte-for-byte (including whitespace/quotes). sha256 computed at freeze time.
- Harness delta `research/intel/run_exp_38121203425.py` must: (a) reuse parse_action/regex_parse_action and run_episode/scorer from parent (or import them), (b) accept `--config`, `--model` (or model paths list for 7B shards), `--cell` (comp|treat|random|nc|pc_oracle), `--episodes`, (c) enforce GGUF digest checks against pinned map, (d) implement navigation-repaired controls (B-RANDOM/NC/PC-ORACLE against served page), (e) collect comparator unconditionally before treatment, (f) enforce PC gates, (g) apply decision precedence 1..6 and write packet artifacts to experiment dir. No other behavioral changes.
