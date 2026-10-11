# EXP-INTEL-38013769440 Preregistration

**Experiment ID**: EXP-INTEL-38013769440
**Lane**: intel
**Target Claim**: C-LLM-INHERIT
**Director Mandate**: REOPEN (global-director-REOPEN, cycle_id=38013054267)
**Parent Handoff**: EXP-INTEL-37982024058 (sha256: b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55)
**Design Contract Version**: 2

---

## 1. Strategic Context

The Global Research Director has mandated REOPEN on claim C-LLM-INHERIT (readiness condition (3) / blocker B3). The parent experiment EXP-INTEL-37982024058 (audit PASS, outcome FALSIFIES) established under the frozen underspecified protocol:

- **Gate 0 PASS**: Credential-free endpoints exist (local GGUF via huggingface.co resolve-redirect; anonymous proxy).
- **Gate 1 PASS**: Constrained decoding infrastructure verified (PC-JSON-CONSTRAINED-DECODING 10/10 for both M-7B-QWEN and M-3B-QWEN).
- **Gate 2 FAIL**: Neither model cleared the minimal Web-agent capability bar (task_success_rate=0.0, 0/5 each). Both models executed the step-0 reveal-click successfully (clicked_reveal=True, revealed_value='TARGET-42' in 10/10 episodes), then entered a re-click loop on the now-hidden button and never emitted an answer action.
- **Audit VF-01 (material)**: The frozen system prompt enumerated neither the action schema nor the task goal, unlike the grandparent harness (EXP-INTEL-37973264582 `min_webagent.py`), whose SYS prompt contained both ("Actions available: {\"action\":\"click\",\"ref\":\"<id>\"} or {\"action\":\"answer\",\"text\":\"<code>\"}. Click the button to reveal the code, then answer it."). The audit bounds the FALSIFIES outcome to that specific underspecified prompt.
- **Audit U-01/U-02**: The single highest-value follow-up is a NEW experiment with an amended prompt as the treatment variable, isolating prompt sensitivity from model planning capacity.

The Director's question (verbatim from request.json `director_mandate.allocation.question`):

> Under the same credential-free, CPU-quantized constraints, does supplying the task goal/schema in the system prompt (removing the underspecification the parent harness did not have) convert the step-0 reveal-click into a full multi-step click-then-answer completion for the largest obtainable credential-free models, and if not, what is the demonstrable capability ceiling for the minimal Web-agent task across ALL credential-free endpoints and local models actually available to the factory? Return an explicit close/re-scope recommendation so that readiness condition (3) is either satisfied by a proven same-model driver or the four-arm C-LLM-INHERIT benchmark is re-scoped off the credential-free path. Include a bounded external check of the published capability envelope for comparably sized local models.

This experiment is a **bounded within-experiment prompt ablation** (treatment = goal/schema-enriched system prompt; comparator = frozen underspecified prompt re-run in the same packet) plus a **bounded, non-gating external capability envelope check**, executed with the **same harness, same models, same task, same seeds and same infrastructure as the audited parent**. Both decision branches are pre-declared and decision-changing.

---

## 2. Hypothesis and Falsifier

**Hypothesis (H1)**: At least one of M-7B-QWEN or M-3B-QWEN will clear the minimal Web-agent capability bar (task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6 over 5 seeded episodes) when the system prompt enumerates the task goal and the action schema (without leaking the literal answer TARGET-42), converting the parent's FALSIFIES (bounded by VF-01 to the underspecified prompt) to SUPPORTS and unblocking the frozen four-arm benchmark as specified.

**Falsifier (H0)**: Even with the goal/schema-enriched prompt, neither candidate clears the bar (task_success_rate < 0.6 for each — i.e. <= 2/5 under the deterministic protocol), and the within-experiment comparator re-run reproduces the parent's failure mode (0/5 success, re-click loop, answer_action_emission_rate = 0.0), confirming the deficit sits below the prompt ceiling. Then the demonstrable capability ceiling for the minimal Web-agent task across ALL credential-free endpoints/models actually available (0.5B/3B/7B local GGUFs + anonymous proxy, plus the bounded external envelope for comparably sized local models) is below the bar, and the packet delivers the pre-declared close/re-scope recommendation (Section 8.3).

**Both-directions**: SUPPORTS unblocks the flagship benchmark at zero new infrastructure cost. FALSIFIES closes the credential-free path with an accountable re-scope recommendation. There is no third outcome determined by the external check: the envelope is informational evidence for the recommendation only (the local measurement is the sole arbiter of OUTCOME).

---

## 3. Candidate Model Set and Provisioning (FROZEN — No Post-Freeze Additions)

| Candidate ID | Role | Model / Quant | Artifacts (sha256-pinned) | Serving |
|--------------|------|----------------|---------------------------|---------|
| **M-7B-QWEN** | primary | Qwen2.5-7B-Instruct Q4_K_M | shard1 `dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db` (3,993,201,344 B), shard2 `539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a` (689,872,288 B) | llama-cpp-python 0.2.90, chat_format=qwen, n_ctx=2048, seed 42 |
| **M-3B-QWEN** | fallback | Qwen2.5-3B-Instruct Q4_K_M | single file `626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d` (2,104,932,768 B) | same stack |

**Route constraints (established by parent, do not re-derive)**:
- Download ONLY via `huggingface.co` resolve-redirect (302 -> `us.aws.cdn.hf.co`). `cdn-lfs.huggingface.co` and `api-inference.huggingface.co` do NOT resolve in this factory.
- No GPU: CPU-only, nproc=4, ~14 GB RAM (parent ran the 7B Q4_K_M identically).
- The 7B single-file URL 404s; the packaging is two split shards (parent VF-02 — packaging deviation, NOT model substitution). The frozen primary definition for this experiment is the shard pair with pinned digests above.

### 3.1 Provisioning Protocol (frozen)
1. If `/tmp/opencode/gguf/` on the EXECUTE runner still contains files whose sha256 match ALL pinned digests above, reuse them (record reuse in `raw/provisioning_evidence.json`).
2. Otherwise download each artifact via `https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-0000N-of-00002.gguf` (N=1,2) and `https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf`.
3. Verify sha256 of every downloaded file against the pinned digests BEFORE loading. Any mismatch or download failure = `provisioning_failure` for that candidate (recorded; never silently substituted): continue with the remaining candidate; if both fail -> OUTCOME=MEASUREMENT_INVALID.
4. Record download URLs, bytes, digests and load status in `raw/provisioning_evidence.json` and `raw/model_receipts.json` (mirroring the parent's structure).

---

## 4. System Prompts (FROZEN, verbatim)

### 4.1 Treatment Prompt P_treat (goal/schema-enriched; mirrors the grandparent harness structure)
```
You are a web agent. Your task: click the button that reveals the target value, then answer with the revealed value.
Valid actions (emit exactly one JSON object, no prose, no reasoning, no markdown):
- click:  {"action": "click", "selector": "<element id starting with #>"}    e.g. {"action": "click", "selector": "#reveal-btn"}
- answer: {"action": "answer", "text": "<the revealed value>"}
Reply with ONLY a valid JSON action.
```
Intentionally does NOT contain the literal answer `TARGET-42` (beyond the mechanical `#reveal-btn` click example that the element list makes redundant): the model must observe the revealed value in the page observation and echo it, preserving step-2 identifiability. This is the faithful adaptation of the grandparent SYS structure (`schema enumeration + goal sentence`) to the frozen harness action schema (`selector`/`text` instead of `ref`/`text`).

### 4.2 Comparator Prompt P_comp (frozen underspecified, byte-identical to parent)
```
You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.
```

Both prompts are embedded verbatim in this packet; EXECUTE must reproduce them byte-for-byte in the per-condition config files (see Section 5.1).

---

## 5. Minimal Web-Agent Task, Harness and Config Transcription

### 5.1 Harness (REUSED UNMODIFIED, hash-bound)
All measurement runs through the audited frozen harness `research/intel/run_exp_37982024058.py` (sha256 `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`, from parent result.json artifacts) via its config-driven modes:
- `probe-candidate --candidate <ID> --outdir <outdir> --gguf <paths> --chrome /usr/bin/google-chrome --n-threads 4` → runs PC-JSON-CONSTRAINED-DECODING and 5 task episodes from `<outdir>/raw/harness_config.json`.
- `null-random --outdir <outdir>` → runs NC-NO-MODEL-ACTION and B-RANDOM-ACTION from the same config.

This script is **not modified**. Per-condition evaluation = the same script pointed at per-condition outdirs (`raw_treatment/`, `raw_comparator/`), whose config files are byte-identical transcriptions of the frozen parent fixture `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`) with the single field `prompts.system` (and only `prompts.system`) replaced by the verbatim strings of Section 4.1 / 4.2. `prompts.user_template`, `task.page_html`, `gbnf_grammar`, `sampling`, `candidate_models_frozen`, `clearing_threshold`, `positive_control`, `null_control`, `random_baseline` are copied unchanged. Both transcriptions plus the source fixture digests go into `raw/harness_config_transcription.json` and result.json `artifacts` (sha256 of every file), so any transcription drift is diff-checkable against this packet and the bound fixture.

### 5.2 Episode protocol (identical to parent, Section 4/6 of parent prereg)
1. Episode i (i=0..4) uses seed 42+i, temperature 0.0, max_tokens 512, GBNF grammar from config.
2. Per step: observe page (PAGE_TEXT/ELEMENTS/HISTORY via the harness's text-DOM observer), render `user_template`, one constrained model completion, strict parse, Playwright execution.
3. Repeat until a valid `answer` action or 5 steps.
4. `task_success = clicked_reveal AND revealed_value == "TARGET-42" AND final_answer == "TARGET-42"`, plus terminal page-state re-verification (harness built-in).

### 5.3 Baseline/random action space (identical to parent `random_baseline`)
`[{"action":"click","selector":"#reveal-btn"}, {"action":"answer","text":"TARGET-41"}, {"action":"answer","text":"TARGET-42"}, {"action":"answer","text":"TARGET-43"}, {"action":"answer","text":"unknown"}]`, 5 episodes, `random.Random(42)`.

---

## 6. Controls and Baselines (stable IDs)

### 6.1 PC-JSON-CONSTRAINED-DECODING (gate; ID inherited from parent)
- 10 probes per model per prompt condition: system = the condition's prompt, user = `Emit exactly: {"action":"click","selector":"#test"}`.
- Criterion: 10/10 schema-valid JSON. Per-condition `positive_control_pass_rate` reported.
- Failure policy: candidate with treatment-PC < 1.0 is EXCLUDED from treatment evaluation (decoding_infrastructure_failure); its treatment metrics do not exist and are not interpreted as capability.

### 6.2 PC-ORACLE-EPISODE (NEW — scorer-path positive control)
- 5 episodes, scripted producer: step 0 emits `{"action":"click","selector":"#reveal-btn"}`, then emits `{"action":"answer","text":"TARGET-42"}` on the next step, driven through the EXACT `run_episode` scorer (imported from the bound harness) and page server used for candidates.
- Criterion: 5/5 `task_success=true` with `revealed_value='TARGET-42'`.
- Purpose: proves the full scoring path (click → reveal detection → answer registration → terminal re-verification) can fire under the identical implementation that will score candidates. A score below 5/5 → OUTCOME=MEASUREMENT_INVALID (scorer cannot register success), regardless of candidate results.
- Implementation: EXECUTE writes `research/intel/run_exp_38013769440_oracle.py` whose complete behavior is specified here: `import` the harness module by repo path; `start_page_server(task_page_html)`; open Playwright Chromium at `/usr/bin/google-chrome`; for ep in range(5): `run_episode(page, P_treat, user_template, max_steps_per_episode, oracle_producer)` with `oracle_producer(obs, step) -> json.dumps(click action if step==0 else answer action)`, fixed seed irrelevant (scripted), recording per-episode records; write `raw/control_episodes.json#PC-ORACLE-EPISODE`. The file's sha256 is recorded in result.json `artifacts` and provenance.

### 6.3 NC-NO-MODEL-ACTION (inherited ID)
- 5 episodes, fixed invalid content `"I will click the button"`, same scorer (harness `null-random` mode; the producers are prompt-independent, so either per-condition outdir yields identical records — use the treatment outdir for uniformity). Criterion: 0% parseable, 0% success.

### 6.4 B-RANDOM-ACTION (inherited ID)
- 5 episodes, uniform random selection from the Section 5.3 space, seeded RNG (`random.Random(42)`, harness `null-random` mode, same prompt-independence note as 6.3). Expected: parseable_action_rate_step1=1.0, task_success_rate≈0; per-episode success probability p=(1/5)·(1/5)=0.04, so P(>=3/5) ≈ 6.0e-4 (exact arithmetic; see Section 10). The 3/5 bar is unreachable by chance.

### 6.5 B-UNDERSPECIFIED-PROMPT-7B / B-UNDERSPECIFIED-PROMPT-3B (within-experiment protocol comparators)
- M-7B-QWEN and M-3B-QWEN under P_comp (Section 4.2), 5 episodes each, seeds 42-46, in the comparator phase (Section 9, Phase B). Parent-expected replication: task_success_rate=0.0, answer_action_emission_rate=0.0, parseable_action_rate_step1=1.0. NON-replication is a validity signal (harness/provisioning drift) to be flagged loudly, not explained away.

### 6.6 Carried reference baselines (NOT re-run; for the 'ALL endpoints available' ceiling statement)
- **B-0.5B-QWEN-LOCAL** (parent E-LOCAL-LLAMA): prose, no parseable JSON; 0% task success.
- **B-POLLINATIONS-PROXY** (parent E-POLLINATIONS-OPENAI): empty/reasoning-only content, ~197-token cap, HTTP 402; timestamp-bound, not reproducible — do not assume re-runnable.

---

## 7. Measurement Protocol

Per candidate (M-7B-QWEN first, early-success stop; M-3B-QWEN second only if needed):
1. Provision per Section 3.1 (reuse or download + sha256 verify + load test).
2. Treatment phase (Phase A): PC-JSON-CONSTRAINED-DECODING under P_treat (10 probes); if pass → 5 task episodes under P_treat (seeds 42-46).
3. If the candidate clears the bar → SUPPORTS, stop the whole experiment.
4. Comparator phase (Phase B, only when the experiment converges to the negative branch): for EVERY candidate that was evaluated on task under treatment: PC + 5 episodes under P_comp (same seeds 42-46).
5. Controls (oracle, NC, B-RANDOM) run via `null-random` mode + oracle driver, at EXECUTE start before any candidate arm (scorer/canary ordering: oracle first so a broken scorer invalidates the run before compute is spent).

**Metrics (stable IDs; parent set + one diagnostic)**
- `parseable_action_rate_step1`: fraction of episodes where the step-1 action is schema-valid JSON (k/n).
- `task_success_rate`: fraction of the 5 episodes completing the full task.
- `answer_action_emission_rate` (NEW): fraction of episodes in which at least one valid `answer` action is emitted (quantifies the VF-01 click→answer transition).
- `positive_control_pass_rate`, `mean_inference_latency_s`, `mean_completion_tokens` (inherited).
- `external_capability_envelope` (informational, Section 8.2).

**Bar (per model under P_treat)**: CLEARS iff `task_success_rate >= 0.6` (>=3/5) AND `parseable_action_rate_step1 >= 0.6` (>=3/5).

**Threshold rationale (corrected from the parent draft)**: 3/5 is the pre-declared **operational adequacy rule** for a deterministic capability gate (5 seeded episodes at temperature 0.0 produce uniform traces; parent audit VF-03/VF-05 endorse this framing). It is NOT a significance claim: under binomial p=0.5, P(X>=3 | n=5)=0.5, and no p-value is reported anywhere in this packet. Its discriminating power is anchored instead to the random baseline: with per-episode success p=0.04, P(>=3/5) ≈ 0.000602 (exact: 5.99e-4 + 1.23e-5 + 1.02e-7), so a 3/5-or-better cell cannot arise from chance in the same scorer.

---

## 8. Bounded External Capability Check (informational)

### 8.1 Protocol (time-boxed <= 30 min, then stop)
Search the following bounded, named source set for published, reproducible numeric results of the listed local-class models on multi-step Web-agent or tool-use tasks (success rates, pass@k, task completion):
- Sources: WebArena/WebArena-Lite leaderboards and papers; Mind2Web leaderboard and papers; MiniWoB++ papers; τ-bench papers; AgentBench (Web/Tool subsets); ToolBench/API-Bank/BMTools small-model results; GAIA small-model submissions; WebShop small-model results; HuggingFace model cards / Open LLM leaderboard function-calling subsets; arXiv 2024-2026 small-model web-agent papers.
- Models: Qwen2.5-3B/7B, Llama-3.2-3B/8B, Gemma-2-2B/9B, Phi-3.5-mini (or directly comparable successors published through 2026).
- Each finding records: source URL, access date, benchmark, model, task subset, metric, numeric value, and whether inference was credential-free/local (no cloud API key).
- Ceiling criterion per finding: success >= 0.6 on a multi-step task of complexity >= MIN-WEBAGENT-CLICK-REVEAL-ANSWER.

### 8.2 Output
`metrics.external_capability_envelope = {search_timestamp, sources_searched[], findings[], ceiling_above_bar (bool|null), search_exhaustive (bool), ceiling_summary}`. `ceiling_above_bar` is informational; if the 30-min bound expires before all sources, `search_exhaustive=false` and `ceiling_above_bar=null` if no finding qualified (absence of evidence ≠ evidence of absence).

### 8.3 Recommendation mapping (pre-declared; the packet's explicit close/re-scope deliverable)
- OUTCOME=SUPPORTS → recommendation: "Run the frozen four-arm C-LLM-INHERIT benchmark on the verified same-model driver (exact model + P_treat + harness config from this packet)."
- OUTCOME=FALSIFIES and envelope contains >= 1 credible qualifying finding → recommendation: "Bounded follow-up before closing: verify that specific external model+provisioning path in the factory under this packet's protocol; if unprovisionable, re-scope."
- OUTCOME=FALSIFIES and envelope has no qualifying finding (or not exhaustive) → recommendation: "Re-scope the four-arm benchmark off the credential-free path: drop Gate 3's same-model external published anchor; require internally re-run comparators with retrieval-quality metrics (precision@5, recall@5, mean_similarity) on a dynamic-range task bank where cold and retrieval arms are not at ceiling (B2 mandate precedent)."

---

## 9. Decision Rule (Formal; FSM with 3 outcomes)

Let M1=M-7B-QWEN, M2=M-3B-QWEN; P_treat=§4.1, P_comp=§4.2.

**PROVISIONING** (once, before any arm): if both candidates unprovisionable (all digest-verified artifacts unavailable) → OUTCOME=MEASUREMENT_INVALID. Missing/undigest-matching artifact for one candidate → that candidate is `provisioning_failure`, continue with the other.

**PHASE A (treatment)**: for M_i in [M1, M2]:
1. PC under P_treat: `positive_control_pass_rate < 1.0` → EXCLUDE M_i from treatment evaluation (`decoding_infrastructure_failure`); next candidate.
2. 5 episodes under P_treat.
3. `task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6` → **OUTCOME=SUPPORTS, Status=COMPLETE, STOP** (no further candidates, no Phase B, no external check gating).

**PHASE B (convergence)**: entered iff at least one candidate was evaluated on task under treatment and none cleared:
1. Confirm PC-ORACLE-EPISODE (already run at EXECUTE start, Section 7 step 5): if `< 5/5` → **OUTCOME=MEASUREMENT_INVALID** (the scorer can never register success; the run is invalidated regardless of candidate results).
2. Comparator arms: for each candidate evaluated under treatment: PC under P_comp (reference) + 5 episodes under P_comp (seeds 42-46).
3. Bounded external check (§8). Then **OUTCOME=FALSIFIES, Status=COMPLETE**.

**MEASUREMENT_INVALID** only when: both candidates unprovisionable; or zero candidates evaluated on task (all excluded at PC); or oracle < 5/5.

**Reachability audit (pre-freeze)**: SUPPORTS reachable — treatment differs from the parent-failing cell only in the VF-01-identified dimension, and the scorer can register 5/5 (oracle); FALSIFIES reachable — parent already exhibits the full comparator failure mode, treatment may not fix it; MEASUREMENT_INVALID reachable via three enumerated infrastructure conditions. No branch references a value that cannot be computed (the removed MIXED/ceiling branch that depended on an ill-defined external comparison is gone; the envelope is informational only). Thresholds exactly attainable (3/5=0.6). Precedence is strict early-stop; Phase B cannot shadow Phase A.

---

## 10. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| **Constrained decoding masks model reasoning** | PC-JSON isolates decoding (must pass 10/10 under the same prompt), task uses the same GBNF; a PC-pass/task-fail split is a reasoning/planning verdict (parent demonstrated exactly this split). |
| **Scorer cannot register success (latent harness bug)** | NEW PC-ORACLE-EPISODE exercises the full success path through the identical `run_episode` scorer; <5/5 → MEASUREMENT_INVALID regardless of candidates. |
| **Prompt ablation not the true driver** | Within-experiment 2x2: comparator re-run under identical seeds/harness in the same packet; only `prompts.system` differs between cells. |
| **Answer leakage trivializes the task** | P_treat contains no literal `TARGET-42`; the model must observe the revealed value and echo it (step-2 identifiability preserved). The `#reveal-btn` click example is harmless (step-0 clicking already works in the parent). |
| **Determinism hides variance** | Temperature 0.0 + fixed seeds: read as a deterministic-protocol result with zero within-cell variance (parent VF-03); no p-values/CI; 3/5 is an adequacy rule anchored to the random baseline (p=0.04/episode, P(>=3/5)≈6.0e-4 — exact arithmetic, not a binomial 'survival' claim). |
| **Provisioning drift / shard packaging change** | sha256-pinned artifacts (§3); digest mismatch → provisioning_failure → MEASUREMENT_INVALID path, never substitution; parent VF-02 documentation carried. |
| **Harness drift between parent and this run** | Harness hash-bound in freeze_artifacts; comparator cells must replicate parent outcomes (0/5, re-click loop) — non-replication is a loud validity signal. |
| **External check incompleteness** | Bounded source list + 30-min cap, `search_exhaustive` flag, `ceiling_above_bar=null` when unknown; envelope never changes OUTCOME (informational by design). |
| **Prompt-erasure / whitespace drift in transcription** | Both prompts frozen verbatim in §4; EXECUTE transcribes byte-for-byte and records config sha256 in result artifacts for diff against this packet. |
| **Single synthetic task, single model family** | Capability gate, not generality claim (parent VF-04); no architectural-diversity claim; Qwen-class bounded per mandate prior (largest obtainable credential-free models). |
| **CPU latency / runner resource limits** | Parent-verified envelope (7B ~5.1 s/call, 3B ~2.2 s/call, ~14 GB RAM); worst-case 2x2 matrix ≈ 140 calls ≈ 9 min inference + downloads ≤ 6 GB. |

---

## 11. Representation Loss Disclosure

- Text-DOM observation (PAGE_TEXT/ELEMENTS/HISTORY), not full accessibility tree; visual layout, shadow DOM, dynamic attributes lost. After the reveal, PAGE_TEXT contains `TARGET-42` (parent-verified), so failure is not attributable to missing page text.
- Action space limited to click/answer (no type/hover/scroll/navigation); single synthetic page, no auth, no post-load network calls.
- Single model family (Qwen2.5), two sizes; no architectural diversity. 0.5B and proxy are carried references, not re-measured.
- External check bounded to the §8.1 source list; not a literature census.

---

## 12. Artifacts to Produce (Raw Evidence)

| Path (under the experiment dir) | Role | Content |
|---|---|---|
| `raw/model_receipts.json` | raw | Per model per prompt condition: URLs, sha256, bytes, load_time, PC results, episodes, prompt_condition tags |
| `raw/task_episodes.json` | raw | Per-episode: raw completion, parsed action, parse_ok, step_count, click_ok, reveal, final answer, success, answer_action_emitted, tokens, latency, seed, prompt_condition |
| `raw/control_episodes.json` | raw | PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION, B-RANDOM-ACTION (inherited structure + oracle block) |
| `raw/harness_config_transcription.json` | fixture | Both per-condition configs, transcriptions with source-fixture digest + target prompt digest |
| `raw/provisioning_evidence.json` | raw | Reuse/download decisions, digests, load outcomes |
| `raw/external_capability_envelope.json` | raw | §8.2 structured findings |
| `result.json`, `report.md`, `provenance.json` | derived | Per EXPERIMENT_PACKET.md top-level shapes; sha256 of every raw artifact |

---

## 13. Scope Boundaries (What This Experiment Does NOT Do)

- Does NOT run the four-arm C-LLM-INHERIT benchmark (that is the downstream consumer).
- Does NOT add candidate models post-freeze (no census; mandate B2/B3 anti-pattern).
- Does NOT re-run B-0.5B-QWEN-LOCAL / B-POLLINATIONS-PROXY (carried reference baselines; proxy is timestamp-bound).
- Does NOT measure C-CROSSSITE / C-PARAM-INHERIT / C-FRESHNESS / C-DELTA-REPAIR / C-WEB-DYNAMICS / C-SEMANTIC-RESOLVE / C-PRODUCT-ECON.
- Does NOT use GPU, ollama, vLLM, TGI, cloud credentials, or any route beyond huggingface.co resolve-redirect + the verified local stack.
- Does NOT let the external envelope decide the outcome (informational only).

---

## 14. Dependencies on Frozen Upstream Evidence (do not re-derive)

- Parent task definition + page HTML + GBNF grammar + user_template + sampling (frozen fixture, hash-bound).
- Parent environment facts: CPU-only nproc=4, ~14 GB RAM, llama-cpp-python 0.2.90, playwright 1.63.0, Chrome 154.0.8037.97, Python 3.12.15, resolve-redirect route, cdn-lfs/api-inference non-resolution.
- Parent control outcomes (PC 10/10 both models; NC and B-RANDOM verdicts) — controls are re-run here, so they also act as harness-drift checks.
- Parent analysis: VF-01 (prompt underspecification), U-01/U-02 (prompt-ablation value), VF-03 (determinism), VF-05 (adequacy-rule framing).
- Grandparent harness SYS structure (min_webagent.py style) as the treatment template.
- C-LLM-INHERIT registry: HYPOTHESIS, next_gate = same model/tools/budget four-arm.
- Product committed kernel blob b15ed848 as the treatment carrier for any downstream benchmark (not re-verified here).

---

## 15. Pre-registered Analysis Plan (No Post-Hoc Changes)

1. Apply §9 FSM; report exactly one of {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID} with Status=COMPLETE (unless infrastructure aborted the run, which is an operational failure and must be reported as such — not as an outcome).
2. Report per-cell metrics with exact k/n; both prompt conditions labeled; compute the treatment−comparator delta in `answer_action_emission_rate` and `task_success_rate` per model.
3. Replicate-check: comparator cells vs parent outcomes; PC-ORACLE vs 5/5; NC vs 0/0; B-RANDOM vs chance bound.
4. No statistical testing beyond the adequacy rule (no p-values, CIs, or model comparisons anywhere).
5. Validity notes classify every deviation as infrastructure vs capability; unresolved lists what EXECUTE cannot settle.

---

## 16. Handoff Preparation

**If SUPPORTS**: `established` = ["Credential-free 3B-8B GGUF clears the minimal Web-agent capability bar under the goal/schema prompt (exact P_treat in spec/prereg)", "Gate 2 converts to PASS; VF-01 confirmed as the actionable underspecification", "Four-arm C-LLM-INHERIT benchmark unblocked as specified on the verified same-model driver (model + prompt + harness config)"]. `next_question` = "Run the frozen four-arm benchmark."

**If FALSIFIES**: `established` = ["Credential-free 3B-8B GGUF path exhausted under factory constraints even with a goal/schema prompt (within-experiment comparator replicates parent VF-01 mode)", "Demonstrable minimal-task capability ceiling across ALL endpoints/models actually available sits below the 3/5 bar", "Four-arm benchmark DESIGN_COMPROMISED confirmed protocol-stable"]. `rejected` = ["credential-free path viable without a model credential (within the parent bounded scope)", "prompt underspecification alone can unblock Gate 2 for the Qwen 3B/7B class (per this measurement)"]. `do_not_assume` = ["absence of an external envelope finding is evidence of absence (bounded search)", "a qualifying external finding is provisionable in this factory (unverified until a follow-up)", "0.5B/proxy characteristics are re-runnable (carried, timestamp-bound)"]. `next_question` = "Accept the §8.3 recommendation: bounded verification follow-up if a concrete external model was flagged, else explicit re-scope of the four-arm benchmark (drop Gate 3 anchor; internally re-run comparators with retrieval-quality metrics on a dynamic-range task bank)."

**If MEASUREMENT_INVALID**: `do_not_assume` = ["decoding/scoring infrastructure failure == model capability failure"]. `next_question` = "Repair the failing prerequisite (decoder, scorer canary, or provisioning route) once at the substrate level and re-run the frozen protocol."

---

## 17. Freeze Eligibility Justifications (v2 Design Contract)

Each check mirrors `spec.freeze_eligibility` (machine-validated by `scripts/freeze_experiment.py`); the spec is the machine source of truth, this section is the human-readable argument.

| Check | Verdict | Justification (summary) |
|-------|---------|-------------------------|
| **decision_rule_reachability** | PASS | 3-outcome FSM; SUPPORTS reachable (scorer can register 5/5 via oracle; treatment cell open), FALSIFIES reachable (parent exhibits the comparator failure mode), MEASUREMENT_INVALID reachable via 3 enumerated infrastructure conditions; thresholds exactly attainable; early-stop precedence means no shadowing; no ill-defined external-gated branch (removed MIXED). |
| **measurement_prerequisites** | PASS | All hard prerequisites verified-available by the audit-PASS parent packet (models+digests, llama-cpp-python 0.2.90, playwright, Chrome, CPU-only envelope, resolve-redirect route) or carry a frozen failure path (§3.1). No 'will be created during EXECUTE' prerequisite: the only EXECUTE materializations are byte-determined transcriptions of frozen packet content. |
| **baseline_identifiability** | PASS | Treatment vs comparator differ in exactly one variable (prompts.system); same task/grammar/seeds/harness; parent pins comparator expectations (0/5, step-1 parse 1.0) so the cells can differ; neither arm at ceiling (5/5 max, 3/5 not a floor) nor floor (0/5 already observed; oracle proves 5/5 possible); carried references clearly labeled non-re-run; no hidden cost dimension. |
| **control_sensitivity** | PASS | PC-JSON (decoder gate, 10/10, parent-demonstrated discrimination), NEW PC-ORACLE (scorer success path, must be 5/5), NC (must stay 0/0), B-RANDOM (chance bound p=0.04/episode, P(>=3/5)≈6.0e-4 — the 3/5 bar is unreachable by chance); all pre-declared, none tautological beyond the inherited decoder gate, none impossible. |
| **treatment_liveness** | PASS | Treatment = prompt-string variant on the audited config-driven harness; config transcription is a single-field replacement; oracle canary proves the scorer carries click→answer to success before any candidate compute; no harness modification (hash-bound). |
| **freeze_artifacts_bound** | PASS | freeze_artifacts = [research/intel/run_exp_37982024058.py, research/experiments/EXP-INTEL-37982024058/raw/harness_config.json] — both EXIST and are the experiment's operative code+fixture (hash-pinned). New config transcriptions and the oracle driver are EXECUTE-time artifacts fully determined by frozen strings here (§4, §5.1, §6.2), hash-recorded in result/provenance — they cannot change interpretation. GGUFs are remote content pinned by URLs+sha256 (§3.1), which the packet contract treats as frozen identifiers, not bindable files. |

---

## 18. Freeze Artifacts (mutable local dependencies, bound)

1. `research/intel/run_exp_37982024058.py` — audited parent harness, reused unmodified for all measurement (sha256 pinned at freeze).
2. `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` — frozen comparator fixture, byte-template for both per-condition configs (sha256 pinned at freeze).

Post-freeze EXECUTE materializations (per-condition configs, oracle driver) are deterministic transcriptions of frozen packet content with behavioral pseudocode specified in §5.1/§6.2 and are submitted to result.json `artifacts`/provenance with sha256. GGUF content is identified by frozen URL + pinned digest (§3.1).

---

## 19. Legacy Comparative Reasoning (POLICY.md Section 48)

**LEGACY: DISTINCT_EXTENSION** — extends the audited parent by: (1) a goal/schema treatment prompt as the single experimental variable (direct, bounded test of audit VF-01 and U-01/U-02 — the mandate's exact question), (2) within-experiment comparator re-run (2x2 evidence matrix + harness-drift check), (3) NEW scorer-path positive control (PC-ORACLE-EPISODE; the parent's control suite never exercised full task_success), (4) a bounded, explicitly non-gating external capability envelope whose only role is the pre-declared close/re-scope recommendation.

**Pre-2.0 artifacts checked** (against `codex/legacy_brief.json` and `codex/legacy_artifact_index.json`):
- P2-MIND2WEB (HISTORICAL_BOUNDED): route/compositionality analysis over a Mind2Web-derived task-route extraction (176 routes, 6766 actions) — a dataset-level task-route study, NOT an LLM emission capability gate; its guard ("distinguish retrieval, operation overlap, causal composition") is respected by keeping this experiment to a pure prompt ablation with a scripted-scorer oracle.
- P2-REPLAY-COST (HISTORICAL_AUDITED_BOUNDED): withdrawn 8.5x cost claim; guard (matched tasks, no scripted-replay economics) respected — this experiment measures capability, not economics.
- P2-BLIND-COMPOSITION (HISTORICAL_BOUNDED_NEEDS_EXACT_PRIMARY_CHECK): keyword/oracle-guided stopping artifact; guard respected — our oracle is a scorer canary, never a component of the measurement the candidates are scored on.
- P2-WP002B (HISTORICAL_BOUNDED), P2-WP003 (MEASUREMENT_INVALID leakage lesson): no next-state prediction is made here; no leakage-prone bootstrap design is used.
- `legacy_artifact_index.json` intel-lane browser pilot: `results/intel/reproductions/cycle6/pre_freeze_pilot/pilot_browser.json` (507 B, sha `8908cdb4b2917ed42ecd7b1da50ab951babd84ed`, archived out of the working tree): a pre-freeze reproduction pilot under the old intel program — no prompt-ablation capability gate exists in the pre-2.0 corpus; nothing identical or degenerate is repeated.

**Justification for proceeding**: minimal high-information packet named by the mandate and the parent audit's priority unresolved; both branches change the C-LLM-INHERIT decision; no identical pre-2.0 or Research-2.0 design exists.

---

## 20. Signatures

This preregistration is frozen before EXECUTE begins. The deterministic freezer hashes `request.json`, `spec.json`, this `prereg.md`, `design_review.json` and the two `freeze_artifacts` into `freeze.json`. No changes to hypothesis, candidate set, task, prompts, harness, metrics, decision rule, success thresholds, external-check protocol or controls after freeze. DESIGN performs no outcome-bearing measurement; the pre-freeze satisfiability probes actually run (exact-arithmetic chance bounds, machine-contract validation, freeze-file existence and shas) are recorded in the design loop evidence, not as experiment outcomes.