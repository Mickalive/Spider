# EXP-INTEL-38106207218 preregistration (intel lane)

**Experiment ID**: EXP-INTEL-38106207218
**Lane**: intel
**Target Claim**: C-LLM-INHERIT
**Design contract version**: 2 (binding transmission contract: research/EXPERIMENT_PACKET.md)
**Director mandate**: global-director-PIVOT, cycle_id=38105755182, claim C-LLM-INHERIT, parent_handoff_disposition=SUPERSEDE, cognitive_reset=true
**Parent handoff**: EXP-INTEL-37982024058 (sha256 b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55)
**Status**: DESIGN NOT YET FROZEN (this file is the frozen-at-freeze protocol text; the deterministic freezer hashes request.json, spec.json, this file and design_review.json into freeze.json)

---

## 1. Strategic context

The Global Research Director has mandated a **PIVOT** on claim **C-LLM-INHERIT** with cognitive reset, superseding the
parent handoff (SUPERSEDE). The binding question (request.json director_mandate.allocation.question, verbatim):

> Would supplying the task goal/schema in the system prompt (as the parent harness's SYS prompt did) convert the
> step-0 reveal-click into a full click-then-answer completion for M-7B-QWEN or M-3B-QWEN under the same
> credential-free CPU-quantized constraints?

The mandate's rationale: Intel focuses on baselines/prior art that materially alter SPIDER decisions; this is a cheap,
targeted diagnostic that directly interrogates the C-LLM-INHERIT failure mode (missing goal/schema in system prompt
could explain the step-0 reveal-click outcome), distinguishing "missing instruction context" from "deeper inheritance
issue", and supporting readiness condition (3) understanding. The mandate's comparative_reasoning explicitly frames it as
"a small diagnostic test varying a single prompt factor under identical constraints. Not a rerun of economics; it's
baseline verification", with no duplicate prior found, and cites the bounded legacy findings P2-REPLAY-COST
(sha 9687ff787f2d74460bb7006826008852f5b4416b), P2-BLIND-COMPOSITION (sha 017a80aeb9a6759c8f6913a37031ff1616ec1bda) and
P2-MIND2WEB (Codex archive blob 9bb76113aeaf46d9aecdd8a38349a3a7741e57c3) as warnings against naive censuses — this
design is a single-factor ablation, not a census rerun.

**Prior failed design attempts (must not be repeated)**: EXP-INTEL-38013769440 carried the same mandate question but
broadened it into a capability-ceiling census (added M-0.5B-QWEN, the anonymous gpt-oss-20b proxy, a time-boxed external
check and a close/re-scope recommendation); its design review failed substantively and it never froze. The first design
attempt of THIS experiment produced a substantive spec.json but a non-substantive preregistration (6-line stub), so the
reviewer could not verify protocol, probes or artifact binding; it failed substantively. This design differs materially:
(i) strictly the PIVOT question — two prompt conditions x the two mandate candidates, no ceiling census, no proxy, no
external check, no pre-decided re-scope; (ii) a fully self-contained preregistration with byte-exact frozen per-condition
configs (section 4.5), a frozen repaired-controls driver (Appendix A), recorded pre-freeze satisfiability probes
(section 10), and fail-closed replication-anchor logic; (iii) all freeze_eligibility evidence is self-contained or cites
accepted parent evidence — never a failed sibling's prereg.

---

## 2. Inherited evidence (exact carry-forward from parent handoff)

Parent: EXP-INTEL-37982024058, audit PASS, producer_claim_supported=true, outcome FALSIFIES, verdict FALSIFIES with
C-LLM-INHERIT retained HYPOTHESIS (canonical event, in_frozen_scope, lane_eligible). Handoff carry_forward preserved
verbatim:

**established**
- Under frozen protocol (no goal/schema in system prompt, constrained GBNF, temp=0, seeds 42-46, CPU-only llama.cpp 0.2.90,
  Qwen2.5 3B/7B Q4_K_M via huggingface.co resolve-redirect), no credential-free model cleared the minimal Web-agent
  capability bar (task_success_rate>=0.6 and parseable_action_rate_step1>=0.6); M-7B-QWEN 0/5, M-3B-QWEN 0/5.
- Constrained decoding verified working: PC-JSON-CONSTRAINED-DECODING PASS 10/10 for both models; task failure is
  reasoning/planning under frozen prompt, not formatting.
- Verification logic sound: NC-NO-MODEL-ACTION 0/5 parseable, 0/5 success; B-RANDOM-ACTION produces valid JSON 5/5 but
  0/5 success (chance-consistent).
- Prompt-sensitive failure mode: step-0 reveal-click succeeds (revealed_value TARGET-42 present in PAGE_TEXT) and both
  models re-emit hidden-button click for remaining steps; no answer action emitted (VF-01).

**rejected**
- Bounded to the frozen 3B-8B Qwen class under the frozen underspecified prompt: no general rejection of credential-free
  path (prompt ablation needed).
- Bounded to the frozen minimal synthetic task and Qwen family (not generality claim).

**unknown**
- Whether parent-style goal/schema prompt converts step-0 click to full click-then-answer (audit U-01) — NOT tested
  post-freeze; THIS experiment tests it.
- Whether failure is general small-model multi-step planning or prompt-specific (audit U-02) — this experiment
  discriminates.
- Whether 14B+ or non-Qwen GGUFs clear the bar (audit U-03) — out of frozen scope.
- Provisioning stability of 7B split shards across HuggingFace repo revisions (audit U-04).

**do_not_assume**
- Frozen protocol ceiling only: FALSIFIES at that ceiling; do not generalize to other prompts/architectures/models.
- 7B primary packaging deviated (single-file URL 404) — same-model, same-quant split shards used and recorded; not a
  model substitution (VF-02).
- Deterministic protocol (temp=0, fixed seeds) produces 5/5 uniform traces — no variance estimate; 3/5 adequacy rule is
  pre-declared, not statistical (VF-03).
- Task failure not due to missing page text: after reveal, PAGE_TEXT contains TARGET-42 (VF-04).
- C-LLM-INHERIT remains HYPOTHESIS (claim not globally rejected); Gate 2 remains FAIL under frozen protocol.

**Frozen parent metrics (replication anchors for the comparator cells)**:

| Cell (parent) | positive_control_pass_rate | parseable_action_rate_step1 | task_success_rate | mean_inference_latency_s | mean_completion_tokens |
|---|---|---|---|---|---|
| M-7B-QWEN | 1.0 (10/10) | 1.0 (5/5) | 0.0 (0/5) | 5.065 | 17.0 |
| M-3B-QWEN | 1.0 (10/10) | 1.0 (5/5) | 0.0 (0/5) | 2.154 | 13.0 |
| NC-NO-MODEL-ACTION | - | 0.0 (0/5) | 0.0 (0/5) | - | - |
| B-RANDOM-ACTION | - | 1.0 (5/5) | 0.0 (0/5) | - | - |

Audit VF-01 (material, prompt_underspecification): the frozen system prompt enumerated neither the action schema nor the
task goal; the parent harness's SYS prompt (grandparent min_webagent.py) contained both. VF-02 (minor, packaging):
7B primary single-file URL 404 -> same-repo same-quant split shards used, hash-recorded. VF-03 (material, determinism):
5/5 uniform traces; no variance estimate. Provenance: research/experiments/EXP-INTEL-37982024058/{result.json, audit.json,
handoff.json, verdict.json, raw/*}.

---

## 3. Hypothesis, falsifier, decision consequences

**H1 (capability)**: at least one of M-7B-QWEN (primary, evaluated first) or M-3B-QWEN (fallback) clears the
pre-declared capability bar — task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6 over the 5 frozen seeded
episodes (seeds 42-46) — under the treatment prompt P-TREAT-GOAL-SCHEMA.

**H1b (attribution)**: for each clearing candidate, the within-experiment paired comparator cell under
P-COMP-UNDERSPECIFIED fails the bar (frozen anchor: 0/5), so the goal/schema prompt is identified as the driver
(PROMPT_ATTRIBUTED), resolving audit U-01/U-02 toward "missing instruction context".

**H0 (falsifier)**: neither candidate clears the bar under P-TREAT-GOAL-SCHEMA; the audited failure mode (step-0 reveal
click, re-click loop, zero answer actions) recurs under the enriched prompt. Then the VF-01 instruction-context
explanation is rejected for this model class at this protocol ceiling (the loop is a capability/planning deficit), and
the credential-free four-arm benchmark path stays DESIGN_COMPROMISED.

**Both-directions consequences**:
- SUPPORTS (PROMPT_ATTRIBUTED): readiness condition (3) satisfied at mechanism level; the four-arm benchmark becomes
  executable with the verified prompt; C-LLM-INHERIT may advance from HYPOTHESIS on Director adjudication.
- FALSIFIES: capability ceiling real at the prompt-ablated protocol; Director's re-scope set (drop Gate-3 external
  same-model anchor; internally re-run comparators on a dynamic-range task bank; orthogonal mechanisms) becomes actionable.
- MEASUREMENT_INVALID: no claim change; the recorded repair (preflight/drift/provisioning/incompleteness) must be fixed
  and the packet re-run.

---

## 4. Frozen protocol

### 4.1 Task and fixture (identical to parent)

- Task id: **MIN-WEBAGENT-CLICK-REVEAL-ANSWER** (parent task.name): single synthetic HTML page served locally via
  python http.server on 127.0.0.1:randomport (harness function start_page_server). Button `#reveal-btn` ("Reveal") and
  hidden `#target` ("TARGET-42"); clicking the button shows the target and hides the button. max_steps_per_episode=5,
  threshold_target_text="TARGET-42". Full page_html is in the frozen template cfg["task"]["page_html"].
- Fixture template (frozen artifact): `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json`
  (sha256 7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb).
- Harness (frozen artifact): `research/intel/run_exp_37982024058.py`
  (sha256 2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00); loads cfg from `<outdir>/raw/harness_config.json`.

### 4.2 Action schema, parsing, episode semantics (identical to parent)

- click requires {action:"click", selector:"<str>"}; answer requires {action:"answer", text:"<str>"}. Any parse error,
  schema violation or missing required field = parse failure (strict json.loads of the full completion).
- Episode loop: observe page (PAGE_TEXT/ELEMENTS/HISTORY), render user_template, produce action; execute via Playwright
  (click prefix-selector with "#" if absent; answer ends the episode; parse failure ends the episode). Max 5 steps.
- **task_success** = clicked_reveal AND revealed_value == "TARGET-42" AND final_answer exists AND final_answer.strip()
  == "TARGET-42" (exactly the parent's definition; answering without revealing does NOT count as success).
- GBNF grammar: frozen in the template (cfg["gbnf_grammar"]); constructible at DESIGN time (probe P-1).

### 4.3 Sampling and decoding (identical to parent)

temperature=0.0, max_tokens=512, base_seed=42, episode seed = 42 + episode_idx, n_ctx=2048, chat_format="qwen",
llama_seed=42, n_threads=4, CPU-only. GBNF-constrained sampling via llama_cpp LlamaGrammar.

### 4.4 Prompt conditions (the ONLY varied dimension)

| stable_id | field | verbatim |
|---|---|---|
| **P-TREAT-GOAL-SCHEMA** | prompts.system | `You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<id>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.` |
| **P-COMP-UNDERSPECIFIED** | prompts.system | `You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.` |

Treatment provenance: grandparent harness SYS constant (research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py,
bound in freeze_artifacts) with the single adaptation ref -> selector required by the parent schema; adds the schema
enumeration and the goal sentence VF-01 identified as missing; leaks neither `#reveal-btn` nor `TARGET-42` (probe P-2).
Comparator provenance: byte-identical to the audited parent system prompt.

### 4.5 Per-condition configs (BYTE-EXACT, materialized at EXECUTE from this section)

Serialization rule: `json.dumps(cfg, indent=2, sort_keys=True).encode() + b"\n"` (Python 3.12) applied to a deep copy of
the frozen template with ONLY the permitted differences (fixture_id, source, and — for the treatment config —
prompts.system := P-TREAT-GOAL-SCHEMA.verbatim). **Materialization rule (unambiguous)**: for each block below, take the
code-fenced lines strictly between the opening and closing fence lines, join them with `\n`, append exactly one `\n`, and
encode UTF-8; that byte string is the frozen file and its sha256 MUST equal the digest in the block heading. The
equivalent one-liner is
`b = (body + "\n").encode()` where `body` is the fence content with no trailing newline. EXECUTE MUST assert the sha256
immediately after materialization; any mismatch -> provisioning_failure -> MEASUREMENT_INVALID.

**FIX-CFG-EXP-INTEL-38106207218-CONTROLS** — sha256 `aa6f7b8d3c0eaf8464133f0d7200c014f5e68e9193fa358b8b0d44b7dc1a41f0` (controls config for the preflight driver; prompts
unused by scripted producers):
```json controls-config
{
  "action_schema": {
    "answer": {
      "action_value": "answer",
      "required": [
        "action",
        "text"
      ]
    },
    "click": {
      "action_value": "click",
      "required": [
        "action",
        "selector"
      ]
    },
    "description": "Valid actions; any parse error, schema violation, or missing required field = parse failure"
  },
  "candidate_models_frozen": [
    {
      "candidate_id": "M-7B-QWEN",
      "frozen_url": "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf",
      "model": "Qwen2.5-7B-Instruct",
      "note": "Frozen URL returns HTTP 404; same-repo same-quant weights exist only as split shards qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf + -00002-of-00002.gguf; shard load attempted before fallback per prereg section 8",
      "quant": "Q4_K_M",
      "role": "primary"
    },
    {
      "candidate_id": "M-3B-QWEN",
      "frozen_url": "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf",
      "model": "Qwen2.5-3B-Instruct",
      "note": "single-file Q4_K_M confirmed present (2,104,932,768 bytes)",
      "quant": "Q4_K_M",
      "role": "fallback"
    }
  ],
  "clearing_threshold": {
    "episodes": 5,
    "parseable_action_rate_step1_min": 0.6,
    "task_success_rate_min": 0.6
  },
  "fixture_id": "FIX-CFG-EXP-INTEL-38106207218-CONTROLS",
  "gbnf_grammar": "root ::= ws \"{\" ws \"\\\"action\\\"\" ws \":\" ws action ws \",\" ws field ws \"}\" ws\nws ::= [ \\t\\n]*\naction ::= \"\\\"click\\\"\" | \"\\\"answer\\\"\"\nfield ::= \"\\\"selector\\\"\" ws \":\" ws string | \"\\\"text\\\"\" ws \":\" ws string\nstring ::= \"\\\"\" strchars \"\\\"\"\nstrchars ::= strchar strchars | strchar\nstrchar ::= [^\"\\\\] | \"\\\\\" ([\"\\\\/bfnrt] | \"u\" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])\n",
  "metrics_stable_ids": [
    "parseable_action_rate_step1",
    "task_success_rate",
    "mean_inference_latency_s",
    "mean_completion_tokens",
    "positive_control_pass_rate"
  ],
  "null_control": {
    "episodes": 5,
    "fixed_invalid_content": "I will click the button",
    "id": "NC-NO-MODEL-ACTION",
    "success_criterion": "0% parseable JSON actions, 0% task completion"
  },
  "positive_control": {
    "id": "PC-JSON-CONSTRAINED-DECODING",
    "probes": 10,
    "success_criterion": "10/10 syntactically valid JSON matching action schema"
  },
  "prompts": {
    "positive_control_probe": "Emit exactly: {\"action\":\"click\",\"selector\":\"#test\"}",
    "system": "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.",
    "user_template": "PAGE_TEXT: {page_text}\nELEMENTS: {elements_json}\nHISTORY: {history}\nNext action (JSON only): "
  },
  "random_baseline": {
    "action_space": [
      {
        "action": "click",
        "selector": "#reveal-btn"
      },
      {
        "action": "answer",
        "text": "TARGET-41"
      },
      {
        "action": "answer",
        "text": "TARGET-42"
      },
      {
        "action": "answer",
        "text": "TARGET-43"
      },
      {
        "action": "answer",
        "text": "unknown"
      }
    ],
    "episodes": 5,
    "id": "B-RANDOM-ACTION"
  },
  "sampling": {
    "base_seed": 42,
    "chat_format": "qwen",
    "episode_seed_offset": "42 + episode_idx",
    "llama_seed": 42,
    "max_tokens": 512,
    "n_ctx": 2048,
    "temperature": 0.0
  },
  "source": "frozen prereg.md sections 4-7 and spec.json measurement_validity; constructed before any outcome-bearing measurement",
  "task": {
    "description": "Click #reveal-btn then answer TARGET-42 (identical semantic task to parent EXP-INTEL-37973264582 Gate 2)",
    "max_steps_per_episode": 5,
    "name": "MIN-WEBAGENT-CLICK-REVEAL-ANSWER",
    "page_html": "<!DOCTYPE html>\n<html>\n<body>\n  <button id=\"reveal-btn\">Reveal</button>\n  <div id=\"target\" style=\"display:none\">TARGET-42</div>\n  <script>\n    document.getElementById('reveal-btn').onclick = () => {\n      document.getElementById('target').style.display = 'block';\n      document.getElementById('reveal-btn').style.display = 'none';\n    };\n  </script>\n</body>\n</html>\n",
    "served_via": "local python http.server on 127.0.0.1 random port",
    "threshold_target_text": "TARGET-42"
  }
}
```
**FIX-CFG-EXP-INTEL-38106207218-TREAT** — sha256 `c4c825cf2b909310e4db2e1fbe15c886ac6744f3fb66e7241f26b6c5eb9a881a` (treatment cells):
```json treatment-config
{
  "action_schema": {
    "answer": {
      "action_value": "answer",
      "required": [
        "action",
        "text"
      ]
    },
    "click": {
      "action_value": "click",
      "required": [
        "action",
        "selector"
      ]
    },
    "description": "Valid actions; any parse error, schema violation, or missing required field = parse failure"
  },
  "candidate_models_frozen": [
    {
      "candidate_id": "M-7B-QWEN",
      "frozen_url": "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf",
      "model": "Qwen2.5-7B-Instruct",
      "note": "Frozen URL returns HTTP 404; same-repo same-quant weights exist only as split shards qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf + -00002-of-00002.gguf; shard load attempted before fallback per prereg section 8",
      "quant": "Q4_K_M",
      "role": "primary"
    },
    {
      "candidate_id": "M-3B-QWEN",
      "frozen_url": "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf",
      "model": "Qwen2.5-3B-Instruct",
      "note": "single-file Q4_K_M confirmed present (2,104,932,768 bytes)",
      "quant": "Q4_K_M",
      "role": "fallback"
    }
  ],
  "clearing_threshold": {
    "episodes": 5,
    "parseable_action_rate_step1_min": 0.6,
    "task_success_rate_min": 0.6
  },
  "fixture_id": "FIX-CFG-EXP-INTEL-38106207218-TREAT",
  "gbnf_grammar": "root ::= ws \"{\" ws \"\\\"action\\\"\" ws \":\" ws action ws \",\" ws field ws \"}\" ws\nws ::= [ \\t\\n]*\naction ::= \"\\\"click\\\"\" | \"\\\"answer\\\"\"\nfield ::= \"\\\"selector\\\"\" ws \":\" ws string | \"\\\"text\\\"\" ws \":\" ws string\nstring ::= \"\\\"\" strchars \"\\\"\"\nstrchars ::= strchar strchars | strchar\nstrchar ::= [^\"\\\\] | \"\\\\\" ([\"\\\\/bfnrt] | \"u\" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])\n",
  "metrics_stable_ids": [
    "parseable_action_rate_step1",
    "task_success_rate",
    "mean_inference_latency_s",
    "mean_completion_tokens",
    "positive_control_pass_rate"
  ],
  "null_control": {
    "episodes": 5,
    "fixed_invalid_content": "I will click the button",
    "id": "NC-NO-MODEL-ACTION",
    "success_criterion": "0% parseable JSON actions, 0% task completion"
  },
  "positive_control": {
    "id": "PC-JSON-CONSTRAINED-DECODING",
    "probes": 10,
    "success_criterion": "10/10 syntactically valid JSON matching action schema"
  },
  "prompts": {
    "positive_control_probe": "Emit exactly: {\"action\":\"click\",\"selector\":\"#test\"}",
    "system": "You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {\"action\":\"click\",\"selector\":\"<id>\"} or {\"action\":\"answer\",\"text\":\"<code>\"}. Click the button to reveal the code, then answer it.",
    "user_template": "PAGE_TEXT: {page_text}\nELEMENTS: {elements_json}\nHISTORY: {history}\nNext action (JSON only): "
  },
  "random_baseline": {
    "action_space": [
      {
        "action": "click",
        "selector": "#reveal-btn"
      },
      {
        "action": "answer",
        "text": "TARGET-41"
      },
      {
        "action": "answer",
        "text": "TARGET-42"
      },
      {
        "action": "answer",
        "text": "TARGET-43"
      },
      {
        "action": "answer",
        "text": "unknown"
      }
    ],
    "episodes": 5,
    "id": "B-RANDOM-ACTION"
  },
  "sampling": {
    "base_seed": 42,
    "chat_format": "qwen",
    "episode_seed_offset": "42 + episode_idx",
    "llama_seed": 42,
    "max_tokens": 512,
    "n_ctx": 2048,
    "temperature": 0.0
  },
  "source": "frozen prereg.md sections 4-7 and spec.json measurement_validity; constructed before any outcome-bearing measurement",
  "task": {
    "description": "Click #reveal-btn then answer TARGET-42 (identical semantic task to parent EXP-INTEL-37973264582 Gate 2)",
    "max_steps_per_episode": 5,
    "name": "MIN-WEBAGENT-CLICK-REVEAL-ANSWER",
    "page_html": "<!DOCTYPE html>\n<html>\n<body>\n  <button id=\"reveal-btn\">Reveal</button>\n  <div id=\"target\" style=\"display:none\">TARGET-42</div>\n  <script>\n    document.getElementById('reveal-btn').onclick = () => {\n      document.getElementById('target').style.display = 'block';\n      document.getElementById('reveal-btn').style.display = 'none';\n    };\n  </script>\n</body>\n</html>\n",
    "served_via": "local python http.server on 127.0.0.1 random port",
    "threshold_target_text": "TARGET-42"
  }
}
```
**FIX-CFG-EXP-INTEL-38106207218-COMP** — sha256 `1ed06df9fd2000079451ff4145dac7e02b711643a5da29e876f9801b8aca3ab4` (comparator cells; byte-identical to the template except
fixture_id/source):
```json comparator-config
{
  "action_schema": {
    "answer": {
      "action_value": "answer",
      "required": [
        "action",
        "text"
      ]
    },
    "click": {
      "action_value": "click",
      "required": [
        "action",
        "selector"
      ]
    },
    "description": "Valid actions; any parse error, schema violation, or missing required field = parse failure"
  },
  "candidate_models_frozen": [
    {
      "candidate_id": "M-7B-QWEN",
      "frozen_url": "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf",
      "model": "Qwen2.5-7B-Instruct",
      "note": "Frozen URL returns HTTP 404; same-repo same-quant weights exist only as split shards qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf + -00002-of-00002.gguf; shard load attempted before fallback per prereg section 8",
      "quant": "Q4_K_M",
      "role": "primary"
    },
    {
      "candidate_id": "M-3B-QWEN",
      "frozen_url": "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf",
      "model": "Qwen2.5-3B-Instruct",
      "note": "single-file Q4_K_M confirmed present (2,104,932,768 bytes)",
      "quant": "Q4_K_M",
      "role": "fallback"
    }
  ],
  "clearing_threshold": {
    "episodes": 5,
    "parseable_action_rate_step1_min": 0.6,
    "task_success_rate_min": 0.6
  },
  "fixture_id": "FIX-CFG-EXP-INTEL-38106207218-COMP",
  "gbnf_grammar": "root ::= ws \"{\" ws \"\\\"action\\\"\" ws \":\" ws action ws \",\" ws field ws \"}\" ws\nws ::= [ \\t\\n]*\naction ::= \"\\\"click\\\"\" | \"\\\"answer\\\"\"\nfield ::= \"\\\"selector\\\"\" ws \":\" ws string | \"\\\"text\\\"\" ws \":\" ws string\nstring ::= \"\\\"\" strchars \"\\\"\"\nstrchars ::= strchar strchars | strchar\nstrchar ::= [^\"\\\\] | \"\\\\\" ([\"\\\\/bfnrt] | \"u\" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])\n",
  "metrics_stable_ids": [
    "parseable_action_rate_step1",
    "task_success_rate",
    "mean_inference_latency_s",
    "mean_completion_tokens",
    "positive_control_pass_rate"
  ],
  "null_control": {
    "episodes": 5,
    "fixed_invalid_content": "I will click the button",
    "id": "NC-NO-MODEL-ACTION",
    "success_criterion": "0% parseable JSON actions, 0% task completion"
  },
  "positive_control": {
    "id": "PC-JSON-CONSTRAINED-DECODING",
    "probes": 10,
    "success_criterion": "10/10 syntactically valid JSON matching action schema"
  },
  "prompts": {
    "positive_control_probe": "Emit exactly: {\"action\":\"click\",\"selector\":\"#test\"}",
    "system": "You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.",
    "user_template": "PAGE_TEXT: {page_text}\nELEMENTS: {elements_json}\nHISTORY: {history}\nNext action (JSON only): "
  },
  "random_baseline": {
    "action_space": [
      {
        "action": "click",
        "selector": "#reveal-btn"
      },
      {
        "action": "answer",
        "text": "TARGET-41"
      },
      {
        "action": "answer",
        "text": "TARGET-42"
      },
      {
        "action": "answer",
        "text": "TARGET-43"
      },
      {
        "action": "answer",
        "text": "unknown"
      }
    ],
    "episodes": 5,
    "id": "B-RANDOM-ACTION"
  },
  "sampling": {
    "base_seed": 42,
    "chat_format": "qwen",
    "episode_seed_offset": "42 + episode_idx",
    "llama_seed": 42,
    "max_tokens": 512,
    "n_ctx": 2048,
    "temperature": 0.0
  },
  "source": "frozen prereg.md sections 4-7 and spec.json measurement_validity; constructed before any outcome-bearing measurement",
  "task": {
    "description": "Click #reveal-btn then answer TARGET-42 (identical semantic task to parent EXP-INTEL-37973264582 Gate 2)",
    "max_steps_per_episode": 5,
    "name": "MIN-WEBAGENT-CLICK-REVEAL-ANSWER",
    "page_html": "<!DOCTYPE html>\n<html>\n<body>\n  <button id=\"reveal-btn\">Reveal</button>\n  <div id=\"target\" style=\"display:none\">TARGET-42</div>\n  <script>\n    document.getElementById('reveal-btn').onclick = () => {\n      document.getElementById('target').style.display = 'block';\n      document.getElementById('reveal-btn').style.display = 'none';\n    };\n  </script>\n</body>\n</html>\n",
    "served_via": "local python http.server on 127.0.0.1 random port",
    "threshold_target_text": "TARGET-42"
  }
}
```

### 4.6 Candidate models (remote; target identifiers + digests frozen)

Verified at DESIGN time (URL HEAD probes, section 10): 3B single-file 200; 7B shard1 200; 7B shard2 200; 7B single-file
404 (parent-documented packaging deviation, raw/provisioning_evidence.json). EXECUTE downloads via huggingface.co
resolve-redirect ONLY, verifies sha256 against raw/gguf_sha256.txt (frozen artifact, sha256 93836c2594b0c156c0fa913fb384e913586cb03adbd501773fdf6fd450176dbd) BEFORE loading; digest mismatch -> provisioning_failure ->
MEASUREMENT_INVALID (recorded; not a scientific negative).

- M-7B-QWEN (primary): qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf (3,993,201,344 B, dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db) + -00002-of-00002.gguf (689,872,288 B, 539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a).
- M-3B-QWEN (fallback): qwen2.5-3b-instruct-q4_k_m.gguf (2,104,932,768 B, 626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d).

### 4.7 Environment (verified at DESIGN time; probe P-0)

Python 3.12.15; llama-cpp-python==0.2.90 (parent-verified version); playwright (parent used 1.63.0); Chrome 154.0.8037.97
headless at /usr/bin/google-chrome; CPU-only nproc=4; ~14 GB available RAM (7B and 3B load sequentially; adequate).
EXECUTE installs these exact versions if absent (parent precedent: the audited parent run assembled this stack in-factory
and produced raw/model_receipts.json; probes P-0/P-1 confirm they assemble in this factory NOW).

### 4.8 Controls driver: REPAIRED NAVIGATION (Appendix A, frozen source)

The parent's harness null-random mode never called page.goto to the served port (controls ran on about:blank; B-RANDOM
task_success was structurally 0). This design repairs the defect: the frozen controls driver (Appendix A, sha256
`494926c4e52235bd6dbfb7bbd8338895700083abf148566a51b6100084d85837`) navigates to the served task URL before episodes and then uses the harness's own run_episode scorer for
PC-ORACLE-EPISODE (5/5), NC-NO-MODEL-ACTION and B-RANDOM-ACTION, writing `<controls_outdir>/raw/control_episodes.json`.
Repair verified at DESIGN time by running the frozen driver (section 10, P-3).

### 4.9 Execution procedure (EXECUTE)

1. Verify freeze.json artifact_hashes (five bound files) and prereg/spec/request hashes; mismatch -> provisioning_failure.
2. Install/locate llama-cpp-python==0.2.90, playwright, chrome (P-0-style import checks).
3. Write three per-condition configs under separate outdirs — `raw_controls/raw/harness_config.json`,
   `raw_treat/raw/harness_config.json`, `raw_comp/raw/harness_config.json` — from the byte blocks in 4.5; assert sha256.
   (Separate outdirs are REQUIRED: the harness receipt writer dedupes model_receipts.json by candidate_id, so a single
   outdir would overwrite the TREAT receipt with the COMP receipt.)
4. Write the controls driver (Appendix A) into the experiment dir; assert its sha256; run it with `--outdir raw_controls`;
   assert oracle_success_rate==1.0, NC (0.0,0.0), RANDOM (1.0, 0.2). Any deviation -> preflight failure -> MEASUREMENT_INVALID.
5. Provision M-7B-QWEN (download+digest-verify+load; receipt with load_time and n_vocab like parent).
6. Run the TREAT cell: `python3 run_exp_37982024058.py --mode probe-candidate --outdir raw_treat --candidate M-7B-QWEN
   --gguf <shard1> <shard2> --chrome /usr/bin/google-chrome --n-threads 4`. Harness runs PC-JSON (10 probes) then 5
   episodes (if PC passes), appending a model receipt.
7. Run the COMP cell for M-7B-QWEN identically with `--outdir raw_comp`.
8. Apply decision rule (section 7). If the TREAT cell cleared -> SUPPORTS -> STOP (M-3B not evaluated).
9. Else provision M-3B-QWEN and repeat steps 6-7 for it (TREAT then COMP).
10. Aggregate raw evidence into result.json (per-cell metrics keyed M-7B-QWEN-TREAT / M-7B-QWEN-COMP / M-3B-QWEN-TREAT /
    M-3B-QWEN-COMP; controls under their stable ids), report.md, provenance.json per the packet contract. No prompt
    tuning, no model substitution, no new candidates post-freeze.

---

## 5. Metrics (stable ids; definitions; downstream transmission)

| stable id | definition | unit |
|---|---|---|
| parseable_action_rate_step1 | fraction of episodes whose step-0 action parsed as schema-valid JSON (k/5) | fraction |
| task_success_rate | fraction of episodes with task_success=true (k/5) | fraction |
| answer_action_emission_rate | fraction of episodes in which ANY step produced a parseable answer action | fraction |
| mean_inference_latency_s | mean wall-time per model call (cell-level mean over call records) | s |
| mean_completion_tokens | mean completion_tokens per model call | tokens |
| positive_control_pass_rate | fraction of PC-JSON probes with valid schema-conforming JSON (k/10) | fraction |

Bar: cell clears iff task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6 (>=3/5 each; pre-declared adequacy
rule, identical to parent).

---

## 6. Controls and baselines (stable ids; expected values)

| control/baseline id | role | protocol | expected (frozen) | evidence |
|---|---|---|---|---|
| PC-JSON-CONSTRAINED-DECODING | positive control (per cell) | 10 probes per cell under the cell's own prompts.system with the frozen grammar | 10/10 valid schema-conforming JSON | parent 10/10 precedent (both models); re-verified per cell at EXECUTE |
| PC-ORACLE-EPISODE | positive control (preflight canary) | 5 scripted episodes (click #reveal-btn, answer TARGET-42) through the REAL run_episode scorer on the served page (Appendix A) | 5/5 task_success=true | probe P-3 and frozen driver run: oracle_success_rate=1.0 |
| NC-NO-MODEL-ACTION | null control | 5 episodes of fixed non-JSON "I will click the button" on the served page | parseable 0.0, success 0.0 | probe P-3: (0.0, 0.0) |
| B-RANDOM-ACTION | negative baseline | 5 episodes, uniform draws from the frozen 5-action space, seed 42 single RNG, served page | parseable 1.0, success exactly 1/5 (0.2) < 0.6 | probe P-3 / frozen driver: (1.0, 0.2), episode success vector [T,F,F,F,F]. A-priori per-episode p = 1/16 = 0.0625 (see below); P(>=3/5) ~= 3.6e-3, so the bar is arithmetically unreachable by this baseline |
| B-UNDERSPECIFIED-PROMPT-7B | within-experiment protocol comparator (replication anchor) | M-7B-QWEN under P-COMP-UNDERSPECIFIED, seeds 42-46, identical artifacts | exactly (task_success_rate, parseable_action_rate_step1, answer_action_emission_rate) = (0.0, 1.0, 0.0); ANY deviation -> MEASUREMENT_INVALID | parent result.json#metrics |
| B-UNDERSPECIFIED-PROMPT-3B | within-experiment protocol comparator (replication anchor) | M-3B-QWEN under P-COMP-UNDERSPECIFIED | (0.0, 1.0, 0.0); deviation -> MEASUREMENT_INVALID | parent result.json#metrics |
| B-0.5B-QWEN-LOCAL / B-POLLINATIONS-PROXY | carried reference baselines (NOT re-run) | from parent result.json#controls | not re-run (UNKNOWN_NOT_RERUN) | parent result.json#controls |

B-RANDOM per-episode success probability (analytic): success requires a `click #reveal-btn` draw before any answer draw,
then a terminating answer draw with text TARGET-42. With 5 equally likely actions: P(click before first answer) = 1/4
(p = (1/5)/(1 - 1/5) truncated at 5 steps is 1/4); P(terminating answer = TARGET-42 | an answer terminates) = 1/4
(one of the four answer values ultimately terminates the episode); p = 1/16 = 0.0625 per episode (i.i.d. approximation;
exact seeded stream is deterministic and measured: 1/5).

---

## 7. Decision rule (formal; precedence; reachability proof)

OUTCOME in {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}; status=COMPLETE unless infrastructure blocks the packet.
Bar: cell clears iff task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6 over its 5 episodes.

Precedence (first matching rule wins):
1. **PREFLIGHT**: PC-ORACLE-EPISODE == 5/5 AND NC == (parseable 0.0, success 0.0) AND B-RANDOM == (parseable 1.0,
   success == 1/5 frozen deterministic value) AND all freeze artifact hashes match AND stack imports OK; else
   OUTCOME=MEASUREMENT_INVALID (preflight failure).
2. **REPLICATION-ANCHOR**: any evaluated comparator cell with (task_success_rate, parseable_action_rate_step1,
   answer_action_emission_rate) != (0.0, 1.0, 0.0) -> OUTCOME=MEASUREMENT_INVALID (deterministic protocol: deviation
   = drift; attribution impossible).
3. **INCOMPLETE**: if both candidate pairs are incomplete (PC failure or run error in either cell of a pair) ->
   OUTCOME=MEASUREMENT_INVALID. (A single incomplete pair -> that candidate skipped.)
4. **M-7B-QWEN pair**: PC-JSON-TREAT (10/10 else pair incomplete), 5 TREAT episodes; then PC-JSON-COMP (10/10 else
   comparator cell incomplete), 5 COMP episodes. If the TREAT cell clears -> OUTCOME=SUPPORTS, attribution =
   PROMPT_ATTRIBUTED (COMP cell fails bar, per the frozen anchor) or UNDETERMINED (COMP cell incomplete/missing);
   STOP.
5. **M-3B-QWEN pair**: evaluated only if rule 4 did not fire. Same structure. If its TREAT cell clears ->
   OUTCOME=SUPPORTS with the same attribution rule; STOP.
6. **FALSIFIES**: no TREAT cell cleared and at least one pair complete -> OUTCOME=FALSIFIES (valid scientific negative;
   status=COMPLETE). Record the failure-mode descriptor per treatment cell (re-click loop / answer-without-click / no
   parseable step-0) in observations.

Reachability proof (pre-freeze, non-outcome-bearing):
- SUPPORTS branch non-empty: the success path is mechanically registerable — PC-ORACLE 5/5 through the real scorer
  (probe P-3 / frozen driver). A TREAT cell reaching >=3/5 is a possible measurement outcome by construction.
- FALSIFIES branch non-empty: the parent produced exactly 0/5 under identical mechanics/artifacts/seeds in this harness
  (result.json#metrics); the TREAT cells run the same mechanics, so all-TREAT-below-bar is an attainable state.
- MEASUREMENT_INVALID branch non-empty: preflight failure (e.g., B-RANDOM stream deviation), replication-anchor
  deviation (any COMP cell not (0,1,0)), or cell incompleteness are all real, detected conditions.
- Thresholds attainable: 0.6 over 5 episodes = k>=3, k in {0..5}; no empty arithmetic.
- Precedence shadowing: rule (4) fires only when rules (1)-(3) did not; rule (6) fires only when no TREAT cell cleared;
  the comparator cell is collected unconditionally per candidate BEFORE the decision, so early-stop (rule 4) cannot
  shadow the anchor rule (2).

---

## 8. Validity threats and mitigations

| Threat | Mitigation |
|---|---|
| Deterministic protocol has zero within-condition variance (VF-03) | Retained deliberately: the comparator cell must EXACTLY replicate the parent anchor, making drift detectable; 3/5 is the pre-declared adequacy rule; no p-values/CI are claimed; result validity_notes restate VF-03. |
| Controls previously ran on about:blank (parent null-random mode) | Repaired controls driver pre-navigates to the served page (section 4.8, Appendix A); verified by P-3 at DESIGN time; expected values frozen (oracle 1.0, NC 0/0, RANDOM 1.0/0.2). |
| Harness drift between parent and this packet | Replication-anchor rule: any COMP cell deviation from (0,1,0) -> MEASUREMENT_INVALID (fail-closed). Freeze artifact hashes verified at EXECUTE. |
| Prompt leakage of #reveal-btn / TARGET-42 in treatment | Probe P-2: neither string appears in P-TREAT-GOAL-SCHEMA. |
| Treatment/comparator differ beyond the prompt | Probe P-2 byte-diff: only fixture_id/source/prompts.system differ; config serialization rule frozen. |
| Small n / single synthetic task / single model family | Capability gate, not generality claim (parent-scoped); scope boundaries in section 13. |
| 7B packaging instability (VF-02) | Same-repo same-quant split shards, digest-pinned (raw/gguf_sha256.txt) and load-tested before fallback; provisioning evidence kept. |
| Model download flakiness | Retry with exponential backoff (parent precedent); digest mismatch after retries -> provisioning_failure -> MEASUREMENT_INVALID. |
| Answer-without-click or click-without-answer as separate failure modes | task_success requires click THEN answer with exact TARGET-42 (parent definition); per-step records let EXECUTE classify failure modes in observations. |
| Chrome/Playwright flakiness | Parent-verified versions; synthetic page has no network dependencies; headless with --no-sandbox. |
| State representation loss (VF-04) | Identical observe() to parent; after reveal PAGE_TEXT contains TARGET-42, so re-click loop cannot be attributed to missing page text; acknowledged, not re-litigated. |

---

## 9. Measurement prerequisites (verified, fail-closed)

Verified at DESIGN time (this run, section 10): Python 3.12.15; llama-cpp-python==0.2.90 importable; playwright
importable; Chrome 154.0.8037.97 at /usr/bin/google-chrome; GBNF grammar constructible; GGUF URLs resolve (3B 200,
7B shard1 200, shard2 200; 7B single-file 404 as parent-documented); CPU nproc=4; RAM ~14 GB; harness + fixture +
provenance files exist with recorded sha256 (freeze_artifacts). Controls canary ran end-to-end (P-3 / frozen driver:
oracle 5/5, NC 0/0, RANDOM 1.0/0.2).

Fail-closed rules at EXECUTE: stack import failure / hash mismatch / digest mismatch / URL non-resolution (after
retries) / grammar construction failure / canary deviation -> provisioning_failure recorded -> OUTCOME=MEASUREMENT_INVALID
with the exact next-action to unblock. Nothing missing is silently converted into a scientific negative.

Note on "will be created during EXECUTE": the only EXECUTE-time creations are (a) re-download of the three GGUF files —
created by the audited parent before, targets+d igests frozen in 4.6, feasibility shown by parent receipts and DESIGN-time
URL probes; and (b) materialization of the per-condition configs and controls driver from frozen byte blocks (4.5,
Appendix A) whose content and sha256 are bound before freeze. Both are deterministic, digest-verified transcriptions of
frozen content, not uncommitted prerequisites.

---

## 10. Pre-freeze non-outcome-bearing satisfiability probes (recorded; reviewer may re-run)

All probes ran in this DESIGN run. None loaded a model; none ran a treatment/comparator episode (no outcome-bearing
measurement). Reproducibility: the three config byte blocks (4.5) and the driver source (Appendix A) are embedded
verbatim with sha256; the reviewer can re-run the driver and re-derive P-1/P-2 statically.

- **P-0 (stack)**: `pip install llama-cpp-python==0.2.90 playwright==1.63.0` succeeded; `import llama_cpp` OK
  (version 0.2.90); `import playwright` OK; python 3.12.15; `/usr/bin/google-chrome` exists
  (Chrome 154.0.8037.97). Result: PASS.
- **P-1 (grammar)**: `LlamaGrammar.from_string(cfg["gbnf_grammar"])` succeeds (type LlamaGrammar). Result: PASS.
- **P-2 (config transcription + liveness)**: three configs transcribed by the frozen serialization rule from the frozen
  template; all JSON-valid; byte-diff vs template shows exactly {fixture_id, source} (comparator/controls) and
  additionally prompts.system (treatment). TREAT contains the goal sentence and schema tokens ("action","click",
  "selector","answer","text") and contains NEITHER "#reveal-btn" NOR "TARGET-42". Frozen sha256s as in 4.5
  (controls aa6f7b8d3c0eaf8464133f0d7200c014f5e68e9193fa358b8b0d44b7dc1a41f0, treatment c4c825cf2b909310e4db2e1fbe15c886ac6744f3fb66e7241f26b6c5eb9a881a, comparator 1ed06df9fd2000079451ff4145dac7e02b711643a5da29e876f9801b8aca3ab4). Result: PASS.
- **P-3 (scorer canary + controls sensitivity, through the REAL run_episode scorer on the served page)** — the frozen
  driver (Appendix A) was run end-to-end in this factory: PC-ORACLE-EPISODE task_success_rate=1.0 (5/5, each 2 steps);
  NC-NO-MODEL-ACTION = (parseable 0.0, success 0.0); B-RANDOM-ACTION = (parseable 1.0, success 0.2 exactly 1/5,
  episode success vector [T,F,F,F,F]). Result: PASS — the scorer registers the full completion path (oracle), rejects
  non-JSON (null), and the seeded random baseline deterministically sits below the bar.
- **P-4 (remote targets)**: HEAD/GET probes at DESIGN time: 3B URL 200 (redirect via xet-bridge CDN); 7B shard-1 200;
  7B shard-2 200; 7B single-file 404 (parent-documented). Sizes/URLs matched raw/provisioning_evidence.json. PASS.
- **P-5 (decision arithmetic)**: bar k>=3 attainable (k in 0..5); oracle path (5/5) and parent path (0/5) both
  registerable; B-RANDOM P(>=3/5) ~= 3.6e-3 under i.i.d. p=1/16 — bar unreachable by the negative baseline. PASS.

---

## 11. Artifacts and evidence layout

Raw evidence (per-cell, immutable): `raw_treat/raw/{harness_config.json, model_receipts.json}`,
`raw_comp/raw/{harness_config.json, model_receipts.json}`, `raw_controls/raw/{harness_config.json,
control_episodes.json}`, plus provisioning receipts (gguf sha256 verification) and `raw/controls_driver.py`
(sha `494926c4e52235bd6dbfb7bbd8338895700083abf148566a51b6100084d85837`). result.json maps cells to metrics (keys M-7B-QWEN-TREAT, M-7B-QWEN-COMP, M-3B-QWEN-TREAT,
M-3B-QWEN-COMP), controls under stable ids (PC-JSON-CONSTRAINED-DECODING per cell, PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION,
B-RANDOM-ACTION, B-UNDERSPECIFIED-PROMPT-7B, B-UNDERSPECIFIED-PROMPT-3B), capability_bar (thresholds + cleared_by_any:
false), observations (failure-mode descriptors per treatment cell: re-click loop / answer-without-click / no-parseable-step-0),
validity_notes (determinism VF-03 read, about:blank repair, anchor logic, small-n, single-family, packaging deviation
VF-02), unresolved (14B+/non-Qwen; generality; HF repo revision stability). result.json MUST include schema_version,
experiment_id, lane, status, outcome, metrics, controls, artifacts, observations, validity_notes, unresolved (packet
contract). Provenance records hash chain (freeze.json + per-cell raw hashes + config/driver hashes).

---

## 12. Consequences and handoff preparation

- **SUPPORTS (PROMPT_ATTRIBUTED)**: handoff carry_forward.established = ["goal/schema system prompt (schema enumeration +
  goal sentence) converts step-0 reveal-click into full click-then-answer for <candidate> under the frozen protocol;
  parent FALSIFIES explained by VF-01 prompt underspecification (audit hypothesis confirmed); readiness condition (3)
  mechanism-level satisfied"]. next_question suggestion for Director: "Run the four-arm benchmark (cold vs instructions vs
  retrieval vs SPIDER) with the verified goal/schema prompt on the validated candidate endpoint."
- **FALSIFIES**: carry_forward.established = ["goal/schema prompt does not convert step-0 reveal-click under identical
  constraints for 3B/7B Qwen; failure is a capability/planning deficit at this protocol ceiling, not instruction
  context"]; carry_forward.do_not_assume = ["FALSIFIES is bounded to this task/harness/model class; generality and
  14B+/non-Qwen remain open"]. Director's re-scope set becomes actionable; this packet does NOT decide it.
- **MEASUREMENT_INVALID**: no claim update; next action is the recorded repair (preflight / anchor drift / provisioning /
  incompleteness) and re-run.
Claim updates in verdict.json must use the canonical status vocabulary; the DIRECTOR decides status transitions; EXECUTE
records outcome + observations only.

---

## 13. Scope boundaries (what this experiment does NOT do)

- Does NOT run the four-arm C-LLM-INHERIT benchmark.
- Does NOT test M-0.5B-QWEN, 14B+, non-Qwen families, the gpt-oss-20b proxy, or any endpoint census (mandate: smallest
  diagnostic; legacy guards P2-* apply).
- Does NOT perform an external literature check or close/re-scope recommendation (Director decision).
- Does NOT measure economics, freshness, delta repair, cross-site, semantic resolution or product metrics.
- Does NOT add models, prompts or candidate endpoints post-freeze; does NOT tune prompts after freeze.
- Does NOT claim generality beyond the frozen minimal task and Qwen 3B/7B class.

---

## 14. Transmission identity table (stable ids for downstream reuse)

| kind | stable id |
|---|---|
| claim | C-LLM-INHERIT |
| treatment condition | P-TREAT-GOAL-SCHEMA |
| comparator condition | P-COMP-UNDERSPECIFIED |
| candidate (primary) | M-7B-QWEN |
| candidate (fallback) | M-3B-QWEN |
| config (controls) | FIX-CFG-EXP-INTEL-38106207218-CONTROLS (sha aa6f7b8d3c0eaf8464133f0d7200c014f5e68e9193fa358b8b0d44b7dc1a41f0) |
| config (treatment) | FIX-CFG-EXP-INTEL-38106207218-TREAT (sha c4c825cf2b909310e4db2e1fbe15c886ac6744f3fb66e7241f26b6c5eb9a881a) |
| config (comparator) | FIX-CFG-EXP-INTEL-38106207218-COMP (sha 1ed06df9fd2000079451ff4145dac7e02b711643a5da29e876f9801b8aca3ab4) |
| controls driver | APPENDIX-A-CONTROLS-DRIVER (sha 494926c4e52235bd6dbfb7bbd8338895700083abf148566a51b6100084d85837) |
| positive controls | PC-JSON-CONSTRAINED-DECODING, PC-ORACLE-EPISODE (suite PC-SUITE-EXP-INTEL-38106207218) |
| null control | NC-NO-MODEL-ACTION |
| negative baseline | B-RANDOM-ACTION |
| protocol comparators | B-UNDERSPECIFIED-PROMPT-7B, B-UNDERSPECIFIED-PROMPT-3B |
| carried references | B-0.5B-QWEN-LOCAL, B-POLLINATIONS-PROXY |
| metrics | parseable_action_rate_step1, task_success_rate, answer_action_emission_rate, mean_inference_latency_s, mean_completion_tokens, positive_control_pass_rate |
| outcomes | SUPPORTS / FALSIFIES / MEASUREMENT_INVALID (status COMPLETE unless infra-blocked) |
| attribution | PROMPT_ATTRIBUTED / UNDETERMINED / (PROMPT NOT A DRIVER under FALSIFIES) |

---

## 15. Freeze contract

This preregistration, spec.json, request.json and design_review.json are hashed into freeze.json by the deterministic
freezer before EXECUTE. Immutability: no edits after freeze; no prompt tuning; no model substitution; no new candidates;
no baseline rescoring; no threshold changes. The freezing of this text binds the byte blocks in 4.5 and Appendix A (their
content is interpretation-bound via prereg.md's own hash in freeze.json). Any deviation discovered at EXECUTE is recorded
as provisioning_failure / preflight failure / replication-anchor deviation with the exact next action, never silently
absorbed. DESIGN NOT YET FROZEN — this sentence is replaced by freeze.json's existence.

---

## Appendix A — controls driver source (FROZEN text; sha256 `494926c4e52235bd6dbfb7bbd8338895700083abf148566a51b6100084d85837`)

EXECUTE writes this text to `<exp_dir>/controls_driver.py` using the same materialization rule as section 4.5 (fenced
lines joined with `
` plus exactly one terminating `
`), verifies its sha256, and runs it with `--outdir raw_controls`
BEFORE any candidate inference. It imports the frozen harness functions
from run_exp_37982024058.py; runs scripted producers only (NO model inference); pre-navigates to the served task URL
(REPAIRED navigation); writes raw_controls/raw/control_episodes.json.

```
#!/usr/bin/env python3
"""EXP-INTEL-38106207218 preflight controls driver (FROZEN text, Appendix A of
prereg.md). Reuses the frozen harness functions from run_exp_37982024058.py.
REPAIRED NAVIGATION vs parent null-random mode: the page is navigated to the
served task URL before episodes, so controls and the PC-ORACLE canary run
against the actual task page through the real run_episode scorer.
No model inference is performed; scripted producers only.
Writes <controls_outdir>/raw/control_episodes.json and prints the frozen
expected values for mechanical verification.
"""
import argparse, json, os, random, sys

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = _here
while ROOT and not os.path.exists(os.path.join(ROOT, "research", "intel", "run_exp_37982024058.py")):
    parent = os.path.dirname(ROOT)
    if parent == ROOT:
        raise SystemExit("repo root not found above %s" % _here)
    ROOT = parent
sys.path.insert(0, os.path.join(ROOT, "research", "intel"))
import run_exp_37982024058 as h  # frozen harness code (freeze_artifacts[0])

def oracle_producer(obs, step):
    if step == 0:
        return json.dumps({"action": "click", "selector": "#reveal-btn"}), 0.0, 0, {"kind": "oracle"}
    return json.dumps({"action": "answer", "text": "TARGET-42"}), 0.0, 0, {"kind": "oracle"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--chrome", default="/usr/bin/google-chrome")
    args = ap.parse_args()
    cfg = h.load_config(args.outdir)
    rawdir = os.path.join(args.outdir, "raw")
    os.makedirs(rawdir, exist_ok=True)
    srv, port = h.start_page_server(cfg["task"]["page_html"])
    out = {}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=args.chrome, headless=True, args=["--no-sandbox"])
            page = b.new_page()
            page.goto("http://127.0.0.1:%d/" % port, timeout=20000)  # REPAIRED navigation
            max_steps = cfg["task"]["max_steps_per_episode"]
            threshold = cfg["task"]["threshold_target_text"]
            # PC-ORACLE-EPISODE: 5/5 scripted click-then-answer through the REAL scorer
            orac = [h.run_episode(page, "", "", max_steps, oracle_producer, threshold=threshold)
                    for _ in range(5)]
            out["PC-ORACLE-EPISODE"] = {
                "control_id": "PC-ORACLE-EPISODE",
                "episodes": orac,
                "task_success_rate": sum(1 for e in orac if e["task_success"]) / len(orac),
                "expected": "1.0 (5/5)",
            }
            # NC-NO-MODEL-ACTION
            nc = cfg["null_control"]
            nc_eps = [h.run_episode(page, "", "", max_steps, h.make_null_producer(nc["fixed_invalid_content"]), threshold=threshold)
                      for _ in range(nc["episodes"])]
            out["NC-NO-MODEL-ACTION"] = {
                "control_id": nc["id"],
                "episodes": nc_eps,
                "parseable_action_rate_step1": sum(1 for e in nc_eps if e["step1_parse_ok"]) / len(nc_eps),
                "task_success_rate": sum(1 for e in nc_eps if e["task_success"]) / len(nc_eps),
                "criterion": nc["success_criterion"],
                "expected": "parseable 0.0, success 0.0",
            }
            # B-RANDOM-ACTION (frozen seeded stream, single RNG as in harness)
            rb = cfg["random_baseline"]
            rng = random.Random(cfg["sampling"]["base_seed"])
            rand_eps = [h.run_episode(page, "", "", max_steps, h.make_random_producer(rb["action_space"], rng), threshold=threshold)
                        for _ in range(rb["episodes"])]
            out["B-RANDOM-ACTION"] = {
                "baseline_id": rb["id"],
                "episodes": rand_eps,
                "parseable_action_rate_step1": sum(1 for e in rand_eps if e["step1_parse_ok"]) / len(rand_eps),
                "task_success_rate": sum(1 for e in rand_eps if e["task_success"]) / len(rand_eps),
                "expected": "parseable 1.0, success 0.2 (exactly 1/5, P-3 frozen value)",
            }
            b.close()
        with open(os.path.join(rawdir, "control_episodes.json"), "w") as f:
            json.dump(out, f, indent=2, sort_keys=True)
        print(json.dumps({
            "oracle_success_rate": out["PC-ORACLE-EPISODE"]["task_success_rate"],
            "NC_parseable_step1": out["NC-NO-MODEL-ACTION"]["parseable_action_rate_step1"],
            "NC_success": out["NC-NO-MODEL-ACTION"]["task_success_rate"],
            "RANDOM_parseable_step1": out["B-RANDOM-ACTION"]["parseable_action_rate_step1"],
            "RANDOM_success": out["B-RANDOM-ACTION"]["task_success_rate"],
        }))
    finally:
        srv.shutdown()
    return 0

if __name__ == "__main__":
    sys.exit(main())
```
