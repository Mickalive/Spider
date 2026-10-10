# EXP-INTEL-38013769440 Preregistration

- Experiment: `EXP-INTEL-38013769440`
- Lane: `intel`
- Claim: `C-LLM-INHERIT` (status HYPOTHESIS; current effective event EXP-INTEL-37982024058 FALSIFIES)
- Design contract version: 2 (freeze_eligibility + freeze_artifacts in spec.json)
- Request: `research/experiments/EXP-INTEL-38013769440/request.json` (contains `director_mandate`, cycle `38013054267`, action REOPEN, parent_handoff disposition USE)
- Parent packet: `research/experiments/EXP-INTEL-37982024058` (handoff sha256 `b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55`)
- Canonical machine state: `spec.json` (this file is the human-readable supporting preregistration and the byte-authority for the frozen prompt strings).

## 0. Status

`DESIGN NOT YET FROZEN` (DESIGN complete and self-attacked; six `freeze_eligibility` checks: five PASS, one NOT_APPLICABLE; awaiting independent pre-freeze design review and the deterministic freezer). No confirmatory measurement has been executed.

---

## 1. Strategic Context

The mandate (Global Research Director, cycle 38013054267) asks one decision-changing question (B3): under the same credential-free, CPU-quantized constraints, does supplying the task goal/schema in the system prompt — removing the underspecification the parent harness did not have — convert the step-0 reveal-click into a full multi-step click-then-answer completion for the largest obtainable credential-free models; if not, what is the demonstrable capability ceiling for the minimal Web-agent task across ALL credential-free endpoints and local models actually available to the factory; and return an explicit close/re-scope recommendation for readiness condition (3) of the four-arm C-LLM-INHERIT benchmark, including a bounded external check of the published capability envelope for comparably sized local models. Both directions are decision-changing deliverables (mandate escape clause): a proven same-model driver (SUPPORTS) OR an explicit close/re-scope recommendation (FALSIFIES/MIXED/MEASUREMENT_INVALID).

Parent handoff (EXP-INTEL-37982024058) carry-forward — preserved in intent:

**Established**
- M-7B-QWEN and M-3B-QWEN (Qwen2.5-7B/3B-Instruct Q4_K_M via llama.cpp 0.2.90 constrained decoding, CPU-only, nproc=4) both pass PC-JSON-CONSTRAINED-DECODING 10/10.
- Both fail the frozen minimal Web-agent task 0/5, 0/5 (task_success_rate 0.0) with parseable_action_rate_step1 1.0 — schema-valid JSON actions every episode, never completed.
- Trace: step-0/step-1 reveal-click occurs; revealed value TARGET-42 surfaces in PAGE_TEXT; models re-click hidden elements and never emit the answer action (reveal-click loop). Success mechanics are mechanical: clicked_reveal=True AND revealed_value==TARGET-42 AND final answer text == `TARGET-42`; a bare answer cannot register (B-RANDOM: 5/5 valid JSON, 0/5 success).
- Audit PASS with material finding VF-01: system-prompt underspecification bounds the parent negative to the frozen prompt; the falsifier's generality is NOT established — a prompt ablation is required.
- Null/random controls behave as designed (NC 0 parseable / 0 success; B-RANDOM 5/5 valid JSON / 0/5 success).

**Rejected**
- Under the parent's frozen underspecified-prompt protocol, no 3B-8B Qwen cleared the bar (bounded to that protocol; not a general rejection of the credential-free path).
- M-0.5B-QWEN-LOCAL emits prose under the CENSUS's UNCONSTRAINED decoding protocol, 0% parseable (EXP-INTEL-37973264582 Gate 2). This finding is retained under ITS protocol and is NOT re-litigated, but it does NOT determine the outcome under this experiment's frozen GBNF protocol (which forces valid JSON); M-0.5B-QWEN is therefore measured here as a census-completeness candidate (see section 2 / SA-07).
- gpt-oss-20b via the Pollinations anonymous proxy can drive the task: empty/reasoning-only content, ~197-token cap, intermittent HTTP 402; receipts timestamp-bound, not reproducible contracts; not re-measured.

**Unknown**
- Whether 3B/7B failure is a model-capability ceiling or a prompt-underspecification artifact (VF-01) — this packet measures it.
- Whether larger obtainable local models (14B) fail or pass under identical constraints.
- Whether M-0.5B-QWEN clears under the frozen GBNF protocol (census result was unconstrained-decoding; measured here as a new candidate).
- Provisioning stability of the 7B split shards across HuggingFace repo revisions.
- The published capability envelope for comparably sized local models on multi-step browser/tool tasks (only pre-2.0 PAPER_EVIDENCE exists, NOT reproduced by SPIDER).

**Do not assume**
- Do not assume the parent's 0/5 transfers to a different (specified) system prompt — that is exactly what this experiment measures.
- Do not assume the parent's 0/5 transfers to 14B — forked sample, not tested there; 14B is the escalation arm.
- Do not assume the census 0.5B/proxy negatives transfer to THIS frozen protocol (different decoding regime); exhaustion claims here rest only on frozen-protocol measurements plus carried endpoint-layer evidence explicitly labelled as such.
- Do not assume non-Qwen open-weight models (e.g., Llama-3.2-3B, Gemma-2-9B) are in the obtainable set — they are out of scope via the confirmed route without new provisioning.
- Do not assume Pollinations receipts are reproducible contracts (timestamp-bound); do not promote them.
- Do not assume answer-action emission is a completion: completion requires answer text exactly `TARGET-42` preceded by the mechanical reveal click.
- Do not treat NOT_ATTEMPTED/NOT_MEASURED records as scientific negatives.
- Do not assume this packet promotes any endpoint into Product Core or changes C-LLM-INHERIT's claim status (DIRECTOR decision).

---

## 2. Hypothesis and Falsifier

**Hypothesis (H1).** Under the same credential-free, CPU-quantized constraints, the parent-era 0/5 negatives for M-7B-QWEN and M-3B-QWEN are caused at least partly by system-prompt underspecification (audit finding VF-01), not by an immutable model-capability ceiling. Under a parent-style system prompt that states the goal and enumerates the action schema (PR-SPECIFIED below; grand-parent census SYS structure), the models' step-0 reveal-click (observed 5/5 in the parent) converts into a full click-then-answer completion: at least one candidate in the primary obtainable set {M-7B-QWEN, M-3B-QWEN, M-14B-QWEN} clears the frozen capability bar (`task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6`, i.e. >= 3/5 episodes both), all other frozen constraints byte-identical to the parent (same GBNF grammar, user template, task HTML, seeds 42-46, temperature 0.0, max_tokens 512, n_ctx 2048, chat_format qwen, same GGUF shards, CPU-only). M-0.5B-QWEN is additionally MEASURED under the same frozen protocol as a census-completeness candidate (the census's unconstrained-decoding prose finding is a different protocol and does not determine this one; the mandate's ceiling question requires protocol-grounded exhaustion). If M-0.5B-QWEN alone clears while the primary set fails, the outcome is still SUPPORTS with the clearing candidate explicitly recorded as the driver (the mandate requires a proven same-model driver without a size floor).

**Falsifier (F1).** Under the same constraints and PR-SPECIFIED, no model in the obtainable set measured under the frozen protocol {M-0.5B-QWEN, M-3B-QWEN, M-7B-QWEN, M-14B-QWEN} clears the bar, while the within-experiment replication control CV-UNDERSPEC-REPLICATION confirms behavioral continuity with the parent (0/5 + reveal-click loop on both 7B and 3B under PR-UNDERSPEC) and PC-SCRIPTED-ORACLE confirms the task/verifier can reward a correct click-then-answer (5/5). Exhaustion of the obtainable credential-free range under identical frozen constraints, together with the carried endpoint-layer negative B-POLLINATIONS-PROXY, closes the credential-free external-agent path: readiness condition (3) is NOT satisfied by any credential-free same-model driver, and the four-arm C-LLM-INHERIT benchmark must be explicitly re-scoped off the credential-free path (drop Gate 3's same-model external anchor; re-anchor on internally re-run comparators with a dynamic-range task bank per EXP-PRODUCT-37973256064 / EXP-PRODUCT-37950607128).

---

## 3. Frozen Environment and Substrate (verified at DESIGN time)

Verified live by non-outcome-bearing probes (recorded in `spec.pre_freeze_satisfiability_dry_run.environment_probes`; all PASS):

- Python 3.12.15 (runner toolchain).
- `llama-cpp-python==0.2.90` primary: no cp312 binary wheel; sdist `llama_cpp_python-0.2.90.tar.gz` (63,762,953 bytes, PyPI-verified at DESIGN) downloads; source-build toolchain present (gcc 13.3.0, cmake 3.31.6, make) and `scikit_build_core-1.1.1-py3-none-any.whl` (293,450 bytes) backend verified. This exact 0.2.90 source build already completed successfully in the parent EXECUTE, so it is a proven-reachable step. Fallback ONLY if the sdist build fails: documented newest 0.3.x wheel; continuity gated by CV-UNDERSPEC-REPLICATION.
- `playwright==1.63.0` (wheel PyPI-verified); system `google-chrome` 154.0.8037.97 at `/usr/bin/google-chrome` (identical to parent); `executable_path` used; no browser install step.
- Network: huggingface.co `resolve-redirect` route verified live for all model URLs below (HTTP 200/206/302); content-lengths match parent `raw/gguf_sha256.txt` receipts byte-for-byte where pinned.
- Hardware: nproc=4, CPU-only; RAM 15989 MiB total / 14475 MiB available / ~11185 MiB free at DESIGN; disk 85.0 GiB free. The 14B arm is gated on available memory (>= ~11 GiB) and falls to `NOT_ATTEMPTED-RAM` (=> MIXED, 14B UNRESOLVED) if unmet. 0.5B/3B/7B have no RAM gate.
- Pre-probed and recorded so EXECUTE does NOT retry: the 7B single-file URL (`qwen2.5-7b-instruct-q4_k_m.gguf`) returns HTTP 404 — only split-shard packaging exists (parent's VF-02 packaging deviation, not model unavailability). EXECUTE uses only the pinned split-shard URLs.

Candidates with pinned identities (URLs verified at DESIGN; shas from parent/census receipts or computed at download and recorded in provenance):

| candidate_id | model / quant | files | bytes | sha256 (source) | URL (resolve-redirect) |
|---|---|---|---|---|---|
| M-7B-QWEN | Qwen2.5-7B-Instruct Q4_K_M | 00001-of-00002, 00002-of-00002 | 3,993,201,344 / 689,872,288 | dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db, 539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a (parent raw/gguf_sha256.txt) | https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf (+ -00002-of-00002.gguf) |
| M-3B-QWEN | Qwen2.5-3B-Instruct Q4_K_M | single | 2,104,932,768 | 626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d (parent raw/gguf_sha256.txt) | https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf |
| M-14B-QWEN (conditional escalation) | Qwen2.5-14B-Instruct Q4_K_M | 00001-of-00003, 00002-of-00003, 00003-of-00003 | 3,991,999,872 / 3,989,373,504 / 1,006,737,120 | computed at download, recorded in provenance | https://huggingface.co/Qwen/Qwen2.5-14B-Instruct-GGUF/resolve/main/qwen2.5-14b-instruct-q4_k_m-00001-of-00003.gguf (+ -00002-of-00003.gguf, -00003-of-00003.gguf) |
| M-0.5B-QWEN (census-completeness) | Qwen2.5-0.5B-Instruct Q4_K_M | single | 491,400,032 | 74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db (pinned from census endpoint_receipts.json; recomputed at download) | https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf |

A shard hash mismatch at download => `NOT_MEASURED-SHA-MISMATCH`, never a silent substitution.

---

## 4. Frozen Task and Prompts (single-variable ablation)

Task: `MIN-WEBAGENT-CLICK-REVEAL-ANSWER` — synthetic page served via local python http.server on 127.0.0.1 random port. Page HTML byte-identical to the parent fixture (`harness_config.json` task page):

```html
<!DOCTYPE html>
<html>
<body>
  <button id="reveal-btn">Reveal</button>
  <div id="target" style="display:none">TARGET-42</div>
  <script>
    document.getElementById('reveal-btn').onclick = () => {
      document.getElementById('target').style.display = 'block';
      document.getElementById('reveal-btn').style.display = 'none';
    };
  </script>
</body>
</html>
```

Max steps per episode: 5. Threshold: final answer text == `TARGET-42`. Success requires clicked_reveal=True AND revealed_value==TARGET-42 AND final answer text == `TARGET-42`.

Action schema (frozen, identical to parent): `click` requires `action` + `selector`; `answer` requires `action` + `text`. Any parse error, schema violation, or missing required field = parse failure (regex-parse recorded alongside as raw evidence only).

GBNF grammar (byte-identical to parent fixture):

```
root ::= ws "{" ws "\"action\"" ws ":" ws action ws "," ws field ws "}" ws
ws ::= [ \t\n]*
action ::= "\"click\"" | "\"answer\""
field ::= "\"selector\"" ws ":" ws string | "\"text\"" ws ":" ws string
string ::= "\"" strchars "\""
strchars ::= strchar strchars | strchar
strchar ::= [^"\\] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])
```

User template (byte-identical to parent):

```
PAGE_TEXT: {page_text}
ELEMENTS: {elements_json}
HISTORY: {history}
Next action (JSON only): 
```

**Comparator system prompt (PR-UNDERSPEC)** — byte-identical to the parent fixture `prompts.system`:

```
You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.
```

**Treatment system prompt (PR-SPECIFIED, parent-style)** — the single-variable change; byte-frozen to the grand-parent census harness SYS structure (`EXP-INTEL-37973264582/raw/code/min_webagent.py`), with the ONLY adaptation being the action examples switched from the census's `ref`-based schema to THIS experiment's frozen `selector`-based schema (the frozen GBNF grammar accepts only keys `selector`/`text`). The goal sentence is VERBATIM from the census SYS:

```
You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<css selector>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.
```

Leak guard (P2-BLIND-COMPOSITION): neither PR-SPECIFIED nor PR-UNDERSPEC contains the exact selector `#reveal-btn` nor the answer string `TARGET-42`.

Sampling (identical to parent): temperature=0.0, max_tokens=512, n_ctx=2048, chat_format=`qwen`, llama_seed=42, base_seed=42, episode seed = 42 + episode_idx, 5 episodes per arm per model. CPU threads: 4.

The EXECUTE harness must construct its fixture such that the PR-UNDERSPEC and PR-SPECIFIED strings above are reproduced byte-for-byte (AUDIT-verifiable against this prereg), and all other fixture fields are byte-identical to the parent `harness_config.json`.

---

## 5. Controls and Baselines (stable identifiers)

- **PC-SCRIPTED-ORACLE** (positive control, task/verifier ceiling; NEW): deterministic NON-MODEL scripted policy emits `{"action":"click","selector":"#reveal-btn"}` then `{"action":"answer","text":"TARGET-42"}` through the identical episode pipeline (same page server, Playwright/chrome, parser, verifier), 5 episodes. Requirement: `scripted_oracle_task_success_rate` = 5/5. < 5/5 => `MEASUREMENT_INVALID` (the task/verifier cannot reward a correct click-then-answer; no candidate 0/5 would be interpretable). Certifies the ceiling at 1.0.
- **PC-JSON-CONSTRAINED-DECODING** (positive control, per candidate): 10/10 probes `Emit exactly: {"action":"click","selector":"#test"}` through the identical LlamaGrammar path; success = 10/10 syntactically valid JSON matching the action schema, per candidate, before that candidate's task episodes. PC-fail => candidate `NOT_MEASURED-PC-FAIL`; fail on BOTH 7B and 3B => `MEASUREMENT_INVALID` (decoding infrastructure).
- **NC-NO-MODEL-ACTION** (null control, 5 episodes): fixed invalid content producer (`I will click the button`); success criterion = 0% parseable, 0% completion (reproduction of parent).
- **B-RANDOM-ACTION** (random-baseline null, 5 episodes): uniform random from frozen action space `[click #reveal-btn, answer TARGET-41, answer TARGET-42, answer TARGET-43, answer unknown]`; expectation = chance-level success (~0%: success requires clicked_reveal=True AND exact answer), valid-JSON rate ~1.0 (parent observed 5/5 valid JSON, 0/5 success).
- **CV-UNDERSPEC-REPLICATION** (within-experiment replication control, PRIMARY continuity gate): M-7B-QWEN and M-3B-QWEN under PR-UNDERSPEC in THIS harness. PASS iff for EACH of the two models: `task_success_rate == 0/5` AND `step0_reveal_click_rate >= 0.8` (>= 4/5 episodes with a step-0/step-1 reveal-click) AND >= 1 loop-signature episode (post-reveal hidden-element click, or answer-without-reveal with final answer != TARGET-42) AND confirmational `parseable_action_rate_step1 >= 0.8`. ANY unmet condition on either model (including any clear under PR-UNDERSPEC, any task success > 0/5, click rate < 4/5, absent loop signature, or parseable rate < 0.8) => `MEASUREMENT_INVALID` with reason `REPLICATION-DEVIATION` (environment not byte-continuous with parent; ablation unidentifiable). All-or-nothing by design (SA-06).
- **B-0.5B-QWEN-LOCAL** (carried, DIFFERENT-protocol contextual baseline ONLY): Qwen2.5-0.5B-Instruct Q4_K_M, 0% parseable under UNCONSTRAINED decoding (EXP-INTEL-37973264582 Gate 2). Retained, NOT re-litigated, and does NOT determine M-0.5B-QWEN's outcome under this experiment's frozen GBNF protocol — M-0.5B-QWEN is measured as a candidate.
- **B-POLLINATIONS-PROXY** (carried negative, timestamp-bound): gpt-oss-20b via Pollinations anonymous proxy, empty/reasoning-only content, ~197-token cap, intermittent HTTP 402 (EXP-INTEL-37973264582; not re-measured; endpoint-layer evidence only).
- **B-UNDERSPEC-CARRIED** (comparator baseline): the parent's published 0/5 + 1.0 parseable numbers; re-anchored in-experiment by CV-UNDERSPEC-REPLICATION.

---

## 6. Measurement Protocol

Preamble (once, before any model episode): (0) PC-SCRIPTED-ORACLE 5 episodes; must be 5/5 or the experiment is `MEASUREMENT_INVALID`.

Candidate order (frozen): M-7B-QWEN -> M-3B-QWEN -> (conditional) M-14B-QWEN -> (census-completeness) M-0.5B-QWEN.

Per candidate: (1) model load + receipt; (2) PC-JSON-CONSTRAINED-DECODING (10/10); (3) 5 episodes under PR-UNDERSPEC — M-7B-QWEN and M-3B-QWEN only (this is the CV-UNDERSPEC-REPLICATION arm); (4) 5 episodes under PR-SPECIFIED (treatment) for every measured candidate. M-14B-QWEN and M-0.5B-QWEN run PC then PR-SPECIFIED (treatment) only — they have no parent/underspecified-protocol receipt under this frozen protocol, so no replication arm. Early stop on first clear under PR-SPECIFIED (remaining candidates recorded `NOT_ATTEMPTED-EARLY-STOP`; never negatives).

Per episode: render user prompt; produce one action (model / null-random producer); parse (JSON schema + regex fallback both recorded as raw evidence); execute click (Playwright `eval_on_selector_all`, record clicked selector and target visibility after) or answer (record answer text); repeat up to 5 steps or completion; record final answer, seed, mean inference latency, mean completion tokens. Raw evidence per episode preserved (all parent episode fields), appended to per-experiment artifacts.

Metrics (stable identifiers):

- `parseable_action_rate_step1` — fraction of episodes whose step-1 action parsed to valid schema JSON (bar >= 0.6)
- `task_success_rate` — fraction of episodes with clicked_reveal=True AND revealed_value==TARGET-42 AND final answer == `TARGET-42` (bar >= 0.6)
- `positive_control_pass_rate` — PC-JSON-CONSTRAINED-DECODING 10/10 required pre-task per candidate
- `scripted_oracle_task_success_rate` — NEW: PC-SCRIPTED-ORACLE task successes / 5 (must be 5/5; failure => MEASUREMENT_INVALID)
- `answer_action_emission_rate` — NEW: fraction of episodes emitting >= 1 parseable `answer` action (the click-then-answer conversion metric named by the mandate)
- `step0_reveal_click_rate` — fraction of episodes with a `click` on `#reveal-btn` at step 1 (parent observed 5/5)
- `loop_signature_rate` — fraction of episodes with >= 1 post-reveal hidden-element click, or an answer-without-reveal whose final answer != TARGET-42
- `mean_inference_latency_s`, `mean_completion_tokens` — economics/cost records per candidate
- `candidate_cleared_bar` (derived bool), `census_completed` (derived bool)

Success threshold (per candidate): cleared bar iff `parseable_action_rate_step1 >= 0.6` AND `task_success_rate >= 0.6` over the frozen 5-episode arm (equivalently, >= 3/5 episodes parsed at step 1 AND >= 3/5 episodes completed; success mechanically requires clicked_reveal==True and exact answer TARGET-42).

---

## 7. Formal Decision Rule

Run arms in order; evaluate in the order below. Exactly one outcome is written to `result.json.outcome` ∈ {SUPPORTS, FALSIFIES, MIXED, MEASUREMENT_INVALID}; `status` ∈ {COMPLETE, BLOCKED, MEASUREMENT_INVALID}.

1. If PC-SCRIPTED-ORACLE != 5/5 => `MEASUREMENT_INVALID` (task/verifier cannot reward success). If PC-JSON fails on BOTH M-7B-QWEN and M-3B-QWEN => `MEASUREMENT_INVALID` (decoding infrastructure). A candidate whose PC-JSON fails is `NOT_MEASURED-PC-FAIL`.
2. Run CV-UNDERSPEC-REPLICATION (7B, 3B under PR-UNDERSPEC). Replication PASS iff for EACH of M-7B-QWEN and M-3B-QWEN: `task_success_rate == 0/5` AND `step0_reveal_click_rate >= 0.8` AND >= 1 loop-signature episode AND `parseable_action_rate_step1 >= 0.8`. If replication does NOT PASS (any condition unmet on either model — including a candidate clearing the bar under PR-UNDERSPEC, any task success > 0/5, click rate < 4/5, absent loop signature, or parseable rate < 0.8) => `MEASUREMENT_INVALID` with reason `REPLICATION-DEVIATION` (environment not byte-continuous with the parent; ablation unidentifiable). Raw observations still reported.
3. Run treatment (PR-SPECIFIED) for the next candidate in order. If any measured candidate clears the bar under PR-SPECIFIED => `SUPPORTS` (early stop; remaining candidates `NOT_ATTEMPTED-EARLY-STOP`, never negatives). The clearing candidate(s) are recorded with full receipts as the proven same-model driver (readiness condition (3) satisfied); the benchmark is executable as frozen with that driver.
4. If replication passed and every measured candidate failed under PR-SPECIFIED:
   - a. If M-14B-QWEN was attained and measured and failed AND M-0.5B-QWEN was measured and failed => `FALSIFIES`. Demonstrable ceiling = {M-0.5B-QWEN, M-3B-QWEN, M-7B-QWEN, M-14B-QWEN measured under the frozen protocol} + {B-POLLINATIONS-PROXY carried, timestamp-bound endpoint-layer negative} = the full credential-free endpoint/model set actually available (E-LOCAL-LLAMA GGUF range + E-POLLINATIONS-OPENAI; models.github.ai is an interception, not an endpoint, per census receipts). Issue the explicit close/re-scope recommendation.
   - b. If M-14B-QWEN and/or M-0.5B-QWEN was NOT attempted or failed attainment/measurement (`NOT_ATTEMPTED-URL` / `NOT_ATTEMPTED-RAM` / `NOT_ATTEMPTED-DISK` / `NOT_MEASURED-RUN-ERROR` / `NOT_MEASURED-PC-FAIL` / `NOT_MEASURED-SHA-MISMATCH`) => `MIXED`. Negative bounded strictly to the measured set; any unresolved arm explicitly `UNRESOLVED`; close/re-scope recommendation issued with a strength caveat.
5. Infrastructure failures (build failure without acceptable fallback, playwright/chrome failure, server failure) => `MEASUREMENT_INVALID` with the exact failure string; never a scientific negative. `status=BLOCKED` only if the failure precedes any measurement.

Close/re-scope recommendation (deliverable, written to report.md regardless of direction): if SUPPORTS -> benchmark executable as frozen with the proven driver (candidate id + shard hashes recorded); if FALSIFIES/MIXED -> readiness condition (3) is NOT satisfiable on the credential-free path; re-scope the four-arm C-LLM-INHERIT benchmark off the credential-free path: drop Gate 3's same-model external published-baseline anchor; require internally re-run comparators (same harness, frozen seeds) on a task bank with demonstrable dynamic range (cold and retrieval arms must NOT saturate at 1.0 at high novelty, per EXP-PRODUCT-37973256064 / EXP-PRODUCT-37950607128).

---

## 8. Bounded External Published-Envelope Check (Q-EXT-1/2/3)

Purpose: contextualize the close/re-scope recommendation with the published capability envelope for comparably sized (<14B open-weight) models. This is NOT a SPIDER measurement and is NOT reproduced; it cannot alter the packet outcome. Three pre-registered queries, run once during EXECUTE with the available web search tool:

- Q-EXT-1: `open weights small model browser agent task success rate WebArena 3B 7B 8B 14B`
- Q-EXT-2: `Qwen2.5 7B 14B function calling tool use accuracy benchmark BFCL`
- Q-EXT-3: `small local LLM agent success rate Mind2Web WebVoyager 2025 2026 published results`

Source classification per hit: `PAPER_EVIDENCE` (peer-reviewed/arXiv with explicit SR and N), `REPO_EVIDENCE` (official model/benchmark leaderboards with methodology), `BLOG_EVIDENCE` (unstructured claim), `UNAVAILABLE` (search failed). Record the top 3 per query with numbers and denominators. Anchor starting reference from pre-2.0 Codex (PAPER_EVIDENCE, NOT reproduced by SPIDER): WebArena avg success 37.5% GPT-4.1 / 24.3% Qwen3-4B (AWM/ASI/CER-style scaffolding, arXiv:2606.04391). Results appear only in report.md under a labeled external section and `validity_notes`; no citation is transferred to any claim update without DIRECTOR adjudication.

---

## 9. Validity Threats and Mitigations

- **Version drift (llama.cpp/playwright/chrome)**: pinned versions identical to parent (0.2.90, 1.63.0, chrome 154.0.8037.97). Fallback (0.3.x wheel) only on sdist build failure, gated by CV-UNDERSPEC-REPLICATION. Any drift that changes the replication trace => MEASUREMENT_INVALID.
- **Prompt-identity confound**: the treatment prompt is a static string frozen byte-for-byte in this prereg (grand-parent census SYS structure, selector-schema adaptation only, goal sentence verbatim); the harness constructs it with no discretion; AUDIT re-verifies byte equality. The ablation is single-variable by construction (all other fixture fields byte-identical to the bound parent fixture).
- **Protocol-mismatched carried negative (SA-07)**: the census 0.5B negative was measured under UNCONSTRAINED decoding; it does not determine the outcome under this experiment's frozen GBNF protocol. M-0.5B-QWEN is therefore measured as a candidate; the census finding is retained as a different-protocol contextual baseline only and is NOT re-litigated. If M-0.5B-QWEN cannot be measured, census completeness fails => MIXED with 0.5B UNRESOLVED, never FALSIFIES.
- **Uncertified ceiling (SA-02)**: PC-SCRIPTED-ORACLE (5/5 required) certifies that a correct click-then-answer is rewarded at 1.0, so a universal candidate 0/5 cannot be an unpassable-task or verifier artifact; its failure routes to MEASUREMENT_INVALID.
- **Determinism/randomness**: temp=0, fixed seeds (42-46); the parent showed 5/5 uniform traces; any non-determinism appears as mixed traces, recorded as observation, not used to rescue an outcome.
- **Census completeness**: NOT_ATTEMPTED/NOT_MEASURED are records with reasons (URL/RAM/DISK/RUN-ERROR/PC-FAIL/SHA-MISMATCH/EARLY-STOP), never negatives. 14B and/or 0.5B unresolved => MIXED, not FALSIFIES.
- **Chance-level success**: B-RANDOM-ACTION establishes the chance floor; success additionally requires clicked_reveal=True, so bare chance answers cannot register; bar thresholds (0.6) are above any plausible chance rate.
- **Verification tautology**: success requires `TARGET-42` extracted from the actual page after the reveal click; answering from prior knowledge without the click yields the wrong context (target hidden => not in PAGE_TEXT/ELEMENTS).
- **Carried evidence decay**: Pollinations receipts are timestamp-bound; this design does not rely on them beyond the negative baseline already established by the audit.
- **Measurement vs infrastructure failure**: all failure modes map to explicit categories per the decision rule; infrastructure failure is never encoded as a scientific negative.

---

## 10. Representation Loss Disclosure

- The synthetic two-step page is an extreme minimal instance of the Web-agent task class; results do not generalize to arbitrary multi-step web tasks (no claim beyond the minimal task is intended).
- Only the Qwen2.5 family via E-LOCAL-LLAMA and the gpt-oss-20b proxy are in the obtainable credential-free set; "all credential-free models" means all obtainable via the confirmed route, not all open-weight models ever published.
- Constrained decoding forces JSON structure; the measured ability is reasoning+task completion under grammar constraints, not free-form formatting.
- The 14B and 0.5B arms, if unattainable, bound the census to the measured set and are so labeled (MIXED/UNRESOLVED).
- External published-envelope numbers carry their own publication context and are labeled NOT reproduced.

---

## 11. Scope Boundaries (Explicitly NOT Done)

- No new endpoint provisioning, Docker/ollama routes, GPU, paid APIs, or human-issued credentials.
- No candidate/prompt/grammar/seed additions after freeze.
- No measurement of C-PRODUCT-ECON economics, no kernel promotion, no four-arm benchmark execution (downstream, gated on this result).
- No re-litigation of the audited carried negatives under their own protocols (0.5B census result, Pollinations proxy); M-0.5B-QWEN is measured here under the frozen protocol as a new candidate required by the mandate's ceiling question.
- No re-run of the bounded endpoint/comparator census (EXP-INTEL-37973264582).
- No promotion of any endpoint into Product Core.

---

## 12. Dependencies on Frozen Upstream Evidence

- Parent packet `EXP-INTEL-37982024058` spec/prereg/result/audit/provenance/raw — immutable external evidence referenced by path+sha256 in `spec.code_binding` (not mutable local `freeze_artifact`; see section 16).
- `research/intel/run_exp_37982024058.py` (sha256 `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`) — audited ancestor harness; the EXECUTE harness for this experiment is a minimal parameterized fork constrained to: (a) same parse/verification/page-server logic (success mechanics verified at DESIGN from lines 131-211), (b) parameterization of the system prompt per arm and per-candidate URL shards, (c) outdir = this experiment's dir. Other logic byte-preserved unless removal is required for parameterization and is documented in provenance. The derived EXECUTE harness (`research/intel/run_exp_38013769440.py`) and its derived fixture are bound at EXECUTE by sha256 into `result.json.artifacts` (roles `code`/`fixture`) and `provenance.json`.
- Parent fixture `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`) — task HTML, GBNF grammar, prompts.system=PR-UNDERSPEC, user template, sampling, action schema, clearing threshold.
- GGUF receipts `raw/gguf_sha256.txt` (sha256 `93836c2594b0c156c0fa913fb384e913586cb03adbd501773fdf6fd450176dbd`) — 3B/7B GGUF identities.
- Census receipts `research/experiments/EXP-INTEL-37973264582/raw/endpoint_receipts.json` (sha256 `b7f5c850c4cee3dbac892e28188c1ef18b32c44dc926cf42de121e731db294e9`) — 0.5B GGUF sha256/bytes pinning, proxy operating characteristics, github-models interception control.
- Pre-2.0 Codex PAPER_EVIDENCE (WebArena numbers) as external-check anchor only; `codex/claim_state.json.effective_event_by_claim` — C-LLM-INHERIT HYPOTHESIS (current effective event: EXP-INTEL-37982024058 FALSIFIES).

---

## 13. Pre-Registered Analysis Plan (No Post-Hoc Changes)

- All rates computed as simple fractions over the frozen 5-episode arm; no ad-hoc filtering of episodes.
- Bar clearing threshold fixed (>= 3/5 both metrics) before results are read.
- Outcome selected by the formal rule in section 7; no post-hoc branch invention, no weakening of the falsifier after seeing outcomes.
- report.md may interpret but must not silently contradict result.json or exceed the frozen claim.

---

## 14. Artifacts to Produce (Raw Evidence)

Under `research/experiments/EXP-INTEL-38013769440/`:

- `raw/harness_config.json` — this experiment's fixture (must equal the parent fixture byte-for-byte except `prompts.system` per arm, plus candidate URLs/shas for 14B and 0.5B; AUDIT-verifiable against this prereg).
- `raw/model_receipts.json` — per candidate: load time, gguf sha256 (all shards), positive-control result.
- `raw/task_episodes.json` — per candidate per arm per episode: full trace (prompt, raw completion, parsed action, regex action, clicked selector, visibility, token/latency stats, final answer, seed).
- `raw/control_episodes.json` — PC-SCRIPTED-ORACLE + NC-NO-MODEL-ACTION + B-RANDOM-ACTION episodes.
- `raw/provisioning_evidence.json` — download attrs (URL, bytes, sha256) and attainment-gate records for 14B and 0.5B (reason codes NOT_ATTEMPTED-URL/RAM/DISK, NOT_MEASURED-SHA-MISMATCH if any).
- `raw/code_manifest.json` — sha256 of the EXECUTE harness (`research/intel/run_exp_38013769440.py`) and the derived fixture, for `result.json.artifacts` (roles `code`/`fixture`).
- `result.json` (packet schema v1), `report.md`, `provenance.json`.

---

## 15. Handoff Preparation

`handoff.json` will preserve: established (prompt ablation outcome per candidate; PC-SCRIPTED-ORACLE/PC-JSON/NC/random/replication control results; census completeness incl. 0.5B/14B; cost records), rejected (any re-scope assumptions invalidated), unknown (14B and/or 0.5B if unmeasured; external envelope classification), and do_not_assume (no cross-model generalization, no endpoint promotion, no four-arm benchmark execution authorization, carried negatives not protocol-transferable).

---

## 16. Pre-Freeze Self-Attack (design_contract_version 2) and Code/Artifact Binding

DESIGN actively tried to disprove its own satisfiability before freeze. Findings (mirrored in `spec.pre_freeze_satisfiability_dry_run.self_attack_findings`):

- **SA-01 (BLOCKING, fixed)**: first draft marked `freeze_artifacts_bound` PASS against three pre-existing parent files while the actual EXECUTE harness (the true interpretation dependency) cannot pre-exist at DESIGN freeze time. Reclassified to `NOT_APPLICABLE` with `freeze_artifacts: []`, mirroring the only accepted v2 precedent (`EXP-GRAPH-37992949248`, freeze.json artifact_hashes=[]); the EXECUTE harness is bound at EXECUTE by sha256 into `result.json.artifacts` and `provenance.json`.
- **SA-02 (BLOCKING, fixed)**: no control proved the task/verifier can register success, so a universal 0/5 would be uninterpretable. Added **PC-SCRIPTED-ORACLE** (5/5 required; failure => MEASUREMENT_INVALID).
- **SA-03 (MAJOR, fixed)**: the 14B RAM precondition was stated as "14 GiB free"; actual free RAM is ~10.9 GiB (~14.1 GiB available). The 14B arm is now explicitly attainability-gated on available memory (>= ~11 GiB); non-attainment => `NOT_ATTEMPTED-RAM` and `MIXED` (14B UNRESOLVED), never `FALSIFIES`.
- **SA-04 (MINOR, fixed)**: the 7B single-file URL 404s; only split shards exist. Recorded as a pre-freeze probe result so EXECUTE does not retry it or record a spurious provisioning failure.
- **SA-05 (MINOR, fixed)**: first draft's FALSIFIES implicitly assumed 14B attainment; the decision rule now separates FALSIFIES (14B measured-and-failed AND 0.5B measured-and-failed) from MIXED (either unresolved).
- **SA-06 (BLOCKING, fixed)**: first-drafted replication gate had an undefined middle (e.g., 1/5 task success under PR-UNDERSPEC matched no branch). Replication is now an all-or-nothing gate (PASS requires the full conjunction per model; ANY unmet condition => `MEASUREMENT_INVALID` / `REPLICATION-DEVIATION`).
- **SA-07 (MAJOR, fixed)**: first-drafted FALSIFIER treated M-0.5B-QWEN as a carried negative from the census, but that census measured 0.5B under UNCONSTRAINED decoding — protocol-mismatched with this experiment's GBNF protocol (grammar forces valid JSON; success additionally demands clicked_reveal==True), so an exhaustion claim resting on it would be protocol-mismatched, and the 0.5B outcome is genuinely unknown under GBNF. M-0.5B-QWEN is promoted to a MEASURED census-completeness candidate under the identical frozen protocol (PC then PR-SPECIFIED; no replication arm, since the parent never ran 0.5B under the underspecified prompt), cost trivial (~491 MB). The census finding is retained as a different-protocol contextual baseline (B-0.5B-QWEN-LOCAL), explicitly NOT re-litigated. If 0.5B cannot be measured => MIXED with 0.5B UNRESOLVED, never FALSIFIES. Serves the mandate's "across ALL credential-free endpoints and local models actually available" ceiling clause.
- **SA-08 (MINOR, fixed)**: the treatment prompt as first drafted said "Click the reveal button ...", not byte-faithful to the grand-parent census SYS. PR-SPECIFIED is now frozen byte-by-byte to the census SYS structure with the ONLY adaptation `ref`->`selector` (frozen grammar accepts only keys `selector`/`text`); goal sentence verbatim ("Click the button to reveal the code, then answer it."). Leak guard: neither prompt contains `#reveal-btn` nor `TARGET-42`.

### Branch-reachability matrix (every branch reachable; no empty class)

| branch | reachable when |
|---|---|
| SUPPORTS | any measured candidate (0.5B/3B/7B/14B) clears the bar under PR-SPECIFIED (early stop; driver recorded) |
| FALSIFIES | PC-SCRIPTED-ORACLE 5/5, replication PASS, and ALL of M-0.5B-QWEN/M-3B-QWEN/M-7B-QWEN/M-14B-QWEN measured under PR-SPECIFIED and failing |
| MIXED | replication PASS and measured candidates fail, but M-14B-QWEN and/or M-0.5B-QWEN is NOT_ATTEMPTED/NOT_MEASURED (URL/RAM/DISK/RUN-ERROR/PC-FAIL/SHA-MISMATCH) — missing arm(s) explicitly UNRESOLVED; negative bounded to the measured set |
| MEASUREMENT_INVALID | scripted-oracle < 5/5; or PC-JSON fails on both 7B and 3B; or replication not PASS (any deviation from the parent's deterministic 0/5 + reveal-click-loop pattern on either model, incl. a clear under PR-UNDERSPEC); or playwright/chrome/server/build failure |

### Code/artifact binding (v2)

`freeze_artifacts` is empty and `freeze_artifacts_bound` is `NOT_APPLICABLE`: no mutable local code/data/task-bank/fixture dependency exists at freeze time, because the DESIGN write scope (`scripts/check_scope.py`) permits only spec.json/prereg.md/failure.json/model_design.json/model_design_review.json and `scripts/freeze_experiment.py` cannot hash non-existent files. The immutable pre-existing evidence is referenced by path+sha256 in `spec.code_binding` (ancestor harness `2b5d5bb5...`, parent fixture `7aba9dc8...`, GGUF receipts `93836c25...`, census receipts `b7f5c850...`), not as mutable local fixtures. The EXECUTE-written harness and derived fixture are bound at EXECUTE by sha256 into `result.json.artifacts` (roles `code`/`fixture`) and `provenance.json`; AUDIT re-verifies the derived fixture and the PR-UNDERSPEC/PR-SPECIFIED strings byte-for-byte against this prereg.

---

## 17. Signatures

- Design: big-pickle (opencode/big-pickle), DESIGN mode, lane intel.
- No outcome-bearing measurements were performed during DESIGN; all environment probes were non-outcome-bearing satisfiability checks recorded in `spec.pre_freeze_satisfiability_dry_run.environment_probes` and sections 3 and 9.
- Fidelity notes: parent/census fixture hashes re-verified at DESIGN; PR-SPECIFIED byte-compared against the grand-parent census SYS source (`min_webagent.py` lines 16-18) with only the schema-key adaptation.