# EXP-INTEL-38234107074 preregistration

Lane: `intel` — design_contract_version 2
Request: `research/experiments/EXP-INTEL-38234107074/request.json` (immutable; `base_sha=4e6d7ef451eb38e0f0f1c82960f6833e466d2a6a`, chain_depth=0, reason `global-director-PIVOT`)
Director mandate: PIVOT on claim `C-LLM-INHERIT` (binding direction). Parent handoff: `research/experiments/EXP-INTEL-38194362040/handoff.json` (sha256 `b23deed94c4c843aeddd8d4510096673ebad51473435f04bee9973389ec3938f`, verified at DESIGN).
Status: pre-freeze DESIGN; no outcome-bearing measurement was taken.

> **Design contract note.** `director_mandate.allocation.question` is the binding research
> direction. This prereg refines it into the smallest rigorous falsifiable experiment
> (a single-factor observation-representation discriminator on the two already-tested
> byte-verified classes) and does not drift back to the parent handoff's local
> `next_question`, which is advisory continuity state only.

---

## 1. Question

On the byte-verified credential-free local models (M-14B-QWEN, M-8B-LLAMA) and the
frozen minimal multi-step Web-agent protocol, does the audited failure mode — step-0 reveal
succeeds and `PAGE_TEXT` contains the target, yet the model emits a hidden-button re-click
loop with zero answer actions — **resolve when the observation/action representation is the
single varied factor** (suppress the hidden reveal button from the `ELEMENTS` observation;
and/or present a full accessibility-tree observation), so that representation failure is
separated from raw multi-step control capacity; i.e. do either local class reach
`answer_action_emission_rate > 0` and `task_success_rate >= 0.6`, or does the failure persist
across observation changes — in which case B3 is credential-gated and the exact human-issued
credential/endpoint blocker is recorded instead of another ladder re-run?

The experiment varies **one** factor (`SPIDER_OBS_MODE`) while holding the runner (outside the
frozen patch region), fixture, system prompt, grammar, sampling, seeds, scorer and GGUF bodies
byte-identical to the parent.

## 2. Hypotheses

- **H1 (representation, primary).** The audited failure is an observation-representation
  defect, not a multi-step control-capacity ceiling. The frozen `observe()` calls
  `page.eval_on_selector_all("button, a, input", ...)` which **ignores visibility**, so after
  the step-0 click reveals `TARGET-42` and hides `#reveal-btn`, `ELEMENTS` still lists
  `#reveal-btn` and the model re-clicks a non-actionable affordance. Under an otherwise
  byte-identical protocol, an observation that does not list the hidden affordance
  (`OBS-VISIBLE`) and/or a full accessibility-tree observation (`OBS-A11Y`) will let at least
  one tested class reach `task_success_rate >= 0.6` **and**
  `parseable_action_rate_step1 >= 0.6`, with `answer_action_emission_rate > 0`.
- **H0 (bounded negative / falsifier).** See section 3.
- **H-partial (predeclared decision branch, not a separate claim).** A representation change
  alters behaviour (`answer_action_emission_rate > 0` or `task_success_rate > base`) but does
  not clear the bar; the representation is then necessary-but-insufficient.

## 3. Falsifier

**H0.** Under **every** treatment observation mode (`OBS-VISIBLE`, and `OBS-A11Y` where run),
both tested credential-free classes reproduce the parent failure signature —
`answer_action_emission_rate == 0.0` **and** `task_success_rate == 0.0` **and**
`step0_reveal_click_rate == 1.0` — while their in-run `CELL-BASE-*` cells reproduce the parent
failure exactly. Hence the audited failure mode is **not** an observation-representation defect
and readiness condition (3) / blocker **B3 is credential-gated**.

`FALSIFIES` is asserted only over the **COMPLETE, predeclared** treatment cells at the two
tested classes; it is a bounded capability/representation bound, not a global rejection of
`C-LLM-INHERIT` and not a closure of hosted frontier classes. A cell whose GGUF fails
byte-level content-identity verification, whose load fails, or whose positive-control gate
fails is `UNMEASURED_*` (operational) and is **not** counted as a capability failure; if no
treatment cell is `COMPLETE` the packet is `MEASUREMENT_INVALID`, not a scientific negative.

## 4. Substrate, task and protocol

### 4.1 Frozen task and harness (inherited byte-for-byte; NOT varied)

| item | frozen value |
|---|---|
| Runner | `research/intel/run_exp_37982024058.py`, file sha256 `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00` |
| Base fixture | `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json`, file sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb` |
| Prompt provenance | `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`, file sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862` |
| Task | `MIN-WEBAGENT-CLICK-REVEAL-ANSWER`: `<button id="reveal-btn">Reveal</button>` reveals `<div id="target">TARGET-42</div>` and hides `#reveal-btn`; `max_steps_per_episode=5`; threshold text `TARGET-42`; served on `127.0.0.1` by the frozen `start_page_server`; Playwright + `/usr/bin/google-chrome` |
| System prompt | `P-TREAT-GOAL-SCHEMA`, string sha256 `36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716` |
| GBNF grammar | string sha256 `16c9877c0829b2099bd7180c212f28d8c545b095e9a4411afa7cabccd3fa6a65` |
| Sampling | `temperature=0.0`, `max_tokens=512`, `n_ctx=2048`, `llama_seed=42`, episode seeds `42..46`, `n_threads=4` |
| Parse / scorer | frozen strict `parse_action` (whole completion is JSON) and mechanical `run_episode` (reveal + terminal answer == `TARGET-42`) |
| Bar | `task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6` over 5 episodes |

Per-cell config overlays are deterministic transformations of the frozen base config: only
`prompts.system` (P-TREAT-GOAL-SCHEMA), `sampling.chat_format` (family chat format) and
`candidate_models_frozen` (single candidate) are replaced. **Every other key — including
`prompts.user_template` and the task page — is inherited byte-for-byte.** Overlays are written
to `<cell-outdir>/raw/harness_config.json`; EXECUTE records each overlay's sha256 and verifies
the object-level diff is confined to those three keys.

### 4.2 The single manipulated factor: the observation patch

`SPIDER_OBS_MODE` selects the observation produced by the frozen runner's single
`observe(page, history)` hook: `base` (verbatim frozen), `visible` (primary treatment),
`a11y` (secondary conditional treatment). **The ENTIRE runner change is the frozen patch in
Appendix A.** The patch is embedded in this prereg (which the freezer hashes into
`freeze.json.hashes`); EXECUTE reconstructs the runner from the frozen runner bytes plus this
patch and never authors new code. The default value is `base`, so an unset variable cannot
silently become a treatment.

### 4.3 Arms, ordering and early stop

| # | cell_id | model | `SPIDER_OBS_MODE` | role | conditional |
|---|---|---|---|---|---|
| 1 | `CELL-BASE-M-14B-QWEN` | M-14B-QWEN | `base` | comparator + reproduction | no |
| 2 | `CELL-VISIBLE-M-14B-QWEN` | M-14B-QWEN | `visible` | primary treatment | no |
| 3 | `CELL-BASE-M-8B-LLAMA` | M-8B-LLAMA | `base` | comparator + reproduction | no |
| 4 | `CELL-VISIBLE-M-8B-LLAMA` | M-8B-LLAMA | `visible` | primary treatment | no |
| 5 | `CELL-A11Y-M-14B-QWEN` | M-14B-QWEN | `a11y` | secondary treatment | yes |
| 6 | `CELL-A11Y-M-8B-LLAMA` | M-8B-LLAMA | `a11y` | secondary treatment | yes |

Execution order (frozen): `PREFLIGHT` → 1 → 2 → 3 → 4 → (5, 6 conditional). Each model is run
`base` **before** its treatment so any gain is attributable to the observation. A11Y cells run
only if no `VISIBLE` cell `CLEARS`, the model's `BASE` cell is `COMPLETE` and `REPRO_OK`, and
the a11y API is available (mandate: accessibility-tree arm included only if cheap).

**Early stop.** As soon as any treatment cell `CLEARS`, `OUTCOME=SUPPORTS`,
`B3_STATUS=SATISFIED` and EXECUTE stops (no further cells, no further downloads). A `BASE` cell
that `CLEARS` stops the run with `OUTCOME=MIXED` (reproduction anomaly, rule 3).

### 4.4 Candidate table (served-body pins)

| candidate_id | model / quant | chat_format | revision-pinned URL | bytes | served_body_sha256 |
|---|---|---|---|---|---|
| `M-14B-QWEN` | Qwen2.5-14B-Instruct Q4_K_M | `qwen` | `.../bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/05244aa5d871c661c80082a15d3bce44714d068d/Qwen2.5-14B-Instruct-Q4_K_M.gguf` | 8,988,110,976 | `e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008` |
| `M-8B-LLAMA` | Meta-Llama-3.1-8B-Instruct Q4_K_M | `llama-3` | `.../bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/bf5b95e96dac0462e2a09145ec66cae9a3f12067/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` | 4,920,739,232 | `7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c` |

GGUF header fingerprints (version / tensors / kv / architecture / file_type / block_count /
embedding_length / context_length / chat_template-present) are inherited verbatim from the
parent `spec.json#candidates` and re-checked at EXECUTE.

### 4.5 Content-identity verification (fail-closed, non-substituting)

At frozen rule (2), before any load: stream the revision-pinned URL to a temp path with no size
cap, compute byte count + sha256, parse the GGUF header fingerprint. `IDENTITY-PASS` iff
`bytes == pin` AND `sha256 == served_body_sha256` AND `fingerprint == pin`. `HF xetHash`/CDN
`etag` are explicitly **not** pin sources. On mismatch: one re-download; persistent mismatch →
`UNMEASURED_LOAD_FAILED` with observed bytes/sha256/fingerprint recorded, never a substituted
body. The downloaded GGUFs live outside the repo (`/tmp/opencode/gguf`) and are ephemeral.

## 5. Measurements (stable ids)

| metric id | definition |
|---|---|
| `positive_control_pass_rate` | per cell: `n_pass / 10` for `PC-JSON-CONSTRAINED-DECODING` |
| `parseable_action_rate_step1` | fraction of episodes whose **step-0** completion is valid JSON matching the schema |
| `answer_action_emission_rate` | fraction of episodes emitting at least one `answer` action at any step |
| `task_success_rate` | fraction of episodes with mechanical reveal AND a terminal `answer` == `TARGET-42` |
| `step0_reveal_click_rate` | fraction of episodes whose step-0 action is `click #reveal-btn` |
| `mean_inference_latency_s` | mean per-call latency over the cell's model calls |
| `mean_completion_tokens` | mean `completion_tokens` over the cell's model calls |
| `hidden_affordance_listed_post_reveal` | per mode (PC-OBSERVATION-CONTRAST): does the post-reveal observation list `id == 'reveal-btn'` |
| `target_text_present_post_reveal` | per mode: does `page_text` contain `TARGET-42` after reveal |
| `served_body_digest_verified` | bool per candidate from rule (2) |
| `gguf_metadata_fingerprint_matched` | bool per candidate from rule (2) |
| `reconstructed_runner_sha256_verified` | bool: reconstructed runner == `b2e3b7f9a1411176d66ba21f03659d9d21372fef5fa5b3ecad3ffd40dc7c0cd3` |
| `cells_complete` | count of `COMPLETE` cells |
| `b3_status` | derived `SATISFIED` / `NOT_SATISFIED` / `UNRESOLVED` |
| `observation_mode` | categorical cell metadata (`base`/`visible`/`a11y`) |

## 6. Controls (stable ids)

- **`PC-ORACLE-EPISODE`** — 5 scripted episodes (click then answer) through the REAL frozen
  scorer against the served page; criterion **5/5** `task_success`. Proves the scorer registers
  the full completion path. `<5/5` → `MEASUREMENT_INVALID`.
- **`PC-OBSERVATION-CONTRAST`** — the manipulation check (real page, scripted reveal, no model):
  (a) `OBS-BASE` post-reveal `ELEMENTS` **still contains** `id == 'reveal-btn'` (defect present);
  (b) `OBS-VISIBLE` pre-reveal **contains** `#reveal-btn`; (c) `OBS-VISIBLE` post-reveal does
  **not** contain it; (d) `OBS-A11Y` post-reveal exposes no clickable control named `Reveal`;
  (e) `page_text` contains `TARGET-42` post-reveal in every mode. Any false assertion → the
  varied factor is not live → `MEASUREMENT_INVALID` (never a capability result).
- **`PC-JSON-CONSTRAINED-DECODING`** — 10 probes per cell under the frozen grammar; criterion
  **10/10**. A failing cell is `UNMEASURED_TREATMENT_PC_FAILED` (operational).
- **`NC-NO-MODEL-ACTION`** — 5 episodes of fixed non-JSON content against the served page;
  criterion `parseable_action_rate_step1 == 0.0` AND `task_success_rate == 0.0`.
- **`B-RANDOM-ACTION`** — uniform random over the frozen 5-action space, `random.Random(42)`;
  criterion `parseable_action_rate_step1 == 1.0` AND `task_success_rate < 0.6` (analytic chance
  ≈ 0.0499/episode).
- **`B-BASE-OBSERVATION`** — in-run frozen-observation comparator (the `CELL-BASE-*` cells).
- **`B-CARRIED-PARENT-FALSIFIES`**, **`B-POLLINATIONS-CARRIED`** — carried references, not re-run.

## 7. Decision rule (frozen)

`OUTCOME ∈ {SUPPORTS, FALSIFIES, MIXED, MEASUREMENT_INVALID}`; `B3_STATUS ∈ {SATISFIED,
NOT_SATISFIED, UNRESOLVED}` (separate derived field).

Definitions. `CELL(m)` is one cell = a `PC-JSON-CONSTRAINED-DECODING` gate (10 probes) followed
by an episode batch (5). `CELL(m)` is **COMPLETE** iff identity-PASS AND `load_status==LOADED`
AND `positive_control_pass_rate==1.0` AND exactly 5 episode records; **EXCLUDED** iff LOADED and
the PC gate failed (no episodes); **UNMEASURED_LOAD_FAILED** iff identity verification failed or
the model failed to load; **UNMEASURED_OBS_MODE_UNAVAILABLE** iff the observation mode could not
be produced; **PARTIAL** iff the PC gate passed but fewer than 5 episode records.
`CLEARS(m)` iff COMPLETE and `task_success_rate>=0.6` AND `parseable_action_rate_step1>=0.6`.
`REPRO_OK(base)` iff COMPLETE and NOT CLEARS and `answer_action_emission_rate==0.0` and
`step0_reveal_click_rate==1.0`. `PARTIAL_SIGNAL(m)` iff COMPLETE and not CLEARS and
(`answer_action_emission_rate>0` OR `task_success_rate > base.task_success_rate`).

Precedence (first matching rule wins):

1. **PREFLIGHT** (once): `PC-ORACLE-EPISODE==5/5` AND `NC==(0.0,0.0)` AND
   `B-RANDOM==(1.0, <0.6)` AND `PC-OBSERVATION-CONTRAST` passes for every mode that will be run
   AND all freeze-artifact hash checks match AND required stack imports succeed AND
   `reconstructed_runner_sha256_verified` AND base-mode `observe` AST-equivalence to the frozen
   `observe`. Else `OUTCOME=MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP.
2. **CANDIDATE IDENTITY + LOAD** per model at first use (section 4.5). Persistent mismatch or
   load failure → `UNMEASURED_LOAD_FAILED` (operational); the model is dropped and the run
   continues with the remaining model.
3. **BASE REPRODUCTION.** Each model's `BASE` cell must be `REPRO_OK`. If any `BASE` cell
   `CLEARS` → `OUTCOME=MIXED`, `B3_STATUS=UNRESOLVED`, STOP (the parent's deterministic 0/5 did
   not reproduce, so the observation factor cannot be cleanly identified; recorded as a
   reproduction anomaly, not a capability result). If no `BASE` cell is COMPLETE →
   `OUTCOME=MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP.
4. **TREATMENT.** Run `CELL-VISIBLE` for each model whose `BASE` is COMPLETE and `REPRO_OK`, in
   the frozen order. If any `CELL-VISIBLE` `CLEARS` → `OUTCOME=SUPPORTS`,
   `B3_STATUS=SATISFIED`, STOP.
5. **A11Y (conditional).** If no `CELL-VISIBLE` `CLEARS`, run `CELL-A11Y` for each eligible model
   (only if the a11y API is available). If any `CELL-A11Y` `CLEARS` → `OUTCOME=SUPPORTS`,
   `B3_STATUS=SATISFIED`, STOP. A11Y unavailability → `UNMEASURED_OBS_MODE_UNAVAILABLE`
   (operational), not a capability failure.
6. **AFTER all planned cells (no CLEARS).** Let `T = { treatment cells COMPLETE }`. If `T` empty
   → `MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP. Else if any `t ∈ T` has
   `PARTIAL_SIGNAL` → `OUTCOME=MIXED`, `B3_STATUS=NOT_SATISFIED` (representation is
   necessary-but-insufficient; exact effect recorded). Else (every `t ∈ T` COMPLETE, not CLEARS,
   not PARTIAL_SIGNAL, i.e. `answer_action_emission_rate==0.0` and `task_success_rate==0.0`) →
   `OUTCOME=FALSIFIES`, `B3_STATUS=NOT_SATISFIED`, and the exact carried per-provider
   credential/endpoint blocker is recorded in the result.

An identity/load/PC/observation-mode failure is never encoded as a capability failure. Canonical
packet mapping: `SUPPORTS` → `result.outcome=SUPPORTS, status=COMPLETE`; `FALSIFIES` →
`outcome=FALSIFIES, status=COMPLETE`; `MIXED` → `outcome=MIXED, status=COMPLETE`;
`MEASUREMENT_INVALID` → `status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE`. `B3_STATUS`, the
reproduction signature and the manipulation-check records are written in
`result.metrics`/`result.observations`.

## 8. Validity threats and limitations

1. **Not a statistical estimate.** Five deterministic episodes per cell (temperature 0.0, fixed
   seeds); the 0.6 bar is a pre-declared capability-gate adequacy rule, not a significance test.
2. **`MIXED` vs `FALSIFIES` boundary.** Depends on `answer_action_emission_rate`; a treatment
   that emits a *wrong* answer counts as partial (behaviour changed) — which is the intended
   semantics, but it means `MIXED` does not by itself imply the bar is close.
3. **A11Y confounds format and affordance.** The accessibility tree changes both the element
   format and which affordances are exposed; that is why `VISIBLE` (pure affordance suppression)
   is the primary treatment and `A11Y` is secondary/conditional.
4. **A11Y API availability varies by Playwright build.** The mode is fail-closed
   (`UNMEASURED_OBS_MODE_UNAVAILABLE`); the primary contrast does not depend on it.
5. **`VISIBLE` filter is geometry/computed-style based.** It drops zero-area elements and
   `display:none`/`visibility:hidden`/`opacity:0`; a page hiding the button another way (e.g.
   `aria-hidden` with nonzero geometry) would still be listed. This is itself part of what the
   probe tests, and `PC-OBSERVATION-CONTRAST` asserts the exact defect on the real fixture.
6. **Reproduction is asserted, not assumed.** The parent's 0/5 was deterministic, but the BASE
   cells are run in-session and rule 3 guards against a non-reproducing base.
7. **Single task, single page.** `MIN-WEBAGENT-CLICK-REVEAL-ANSWER` is a readiness prerequisite,
   not a product-scale result; clearing it is not evidence for `C-LLM-INHERIT` at product scale.
8. **Environment/model-version drift.** GGUF bodies are content-pinned; `llama-cpp-python` is
   pinned to 0.2.90; Playwright/Chrome versions are recorded in `provenance.json`.
9. **Two `CELL-BASE-*` cells run the frozen observation twice** (M-14B, M-8B) — this is the
   comparator, not a repeated ladder; no pre-2.0 or spent thread is re-run.

## 9. Consequences

- **Positive (`SUPPORTS`).** The audited failure is an observation-representation defect, not a
  capacity ceiling; B3 is satisfied with a factory-provisionable credential-free local endpoint.
  The gated four-arm `C-LLM-INHERIT` benchmark becomes executable at the clearing class (subject
  to B1/B2), and the product gets a concrete observation-layer requirement: suppress
  non-actionable/hidden affordances and/or emit an accessibility-first observation.
- **Negative (`FALSIFIES`).** The failure is not observation-repairable and B3 is
  credential-gated; the exact per-provider blocker becomes the decision input; the program stops
  re-running the local ladder and either obtains a human credential/model class or re-scopes
  Gate 3.
- **`MIXED`.** Representation is a necessary-but-insufficient component; the next step is a
  specified combined representation+task-structure probe, not another identical ladder.
- **No product mechanism is promoted from this packet**; any promotion is a DIRECTOR action.

## 10. Prerequisites and DESIGN-time satisfiability probes (non-outcome-bearing)

Stack: Python 3.12.15, nproc=4, 15 GB RAM (~14 GB available), 85 GB free disk,
`/usr/bin/google-chrome` 154.0.8037.97 present. `llama_cpp` and `playwright` are **not**
preinstalled at DESIGN (parent EXECUTE installed them); `llama-cpp-python==0.2.90` sdist is
present on PyPI and registers both `llama-3` and `qwen` (carried parent DESIGN verification).
No credential is required. All DESIGN probes below are non-outcome-bearing (no model, no
browser, no confirmatory measurement); details in Appendix B.

## 11. Cost and information gain

CPU-only. Downloads worst case ~13.9 GB (M-14B 8,988,110,976 + M-8B 4,920,739,232 bytes;
early stop may avoid the second). Inference: 10 PC probes + up to 25 steps per cell; parent
CPU latency ~11 s/call (14B) and ~6 s/call (8B) ⇒ ~6 min/cell (14B) and ~4 min/cell (8B); 4
unconditional + up to 2 conditional a11y cells ≈ 40–70 min. Build `llama-cpp-python` 5–15 min;
Playwright <5 min. No external API spend. Wall-clock estimate 60–120 min. Information gain is
decision-changing in every branch (section 9); it directly tests the parent handoff's declared
unknown on representation-vs-capacity and the mandate's PIVOT, and re-runs no spent thread.

## 12. Inherited state from the parent handoff (four-way, preserved)

From `research/experiments/EXP-INTEL-38194362040/handoff.json#carry_forward` (read and preserved
verbatim in meaning):

- **established.** Content-identity freeze repair durable (both GGUFs hashed to served-body pins
  at EXECUTE); valid bounded negative at the audited ceiling — M-14B-QWEN and M-8B-LLAMA both
  `task_success_rate=0.0` (0/5), `parseable_action_rate_step1=1.0`, `positive_control_pass_rate=1.0`,
  `answer_action_emission_rate=0.0`; the failure is action-selection/affordance behaviour (step-0
  click reveals `TARGET-42`, then re-clicks the hidden button, no answer action); endpoint census
  0 PROVISIONABLE_CREDENTIATED / 10 CREDENTIAL_REQUIRED / 1 CREDENTIAL_FREE_OPERATIONALLY_CAPPED /
  1 UNREACHABLE; `C-LLM-INHERIT` retains effective status HYPOTHESIS.
- **rejected (bounded).** The tested credential-free local Q4_K_M path (Qwen 3B/7B/14B,
  Llama-3.1 8B) as clearing the frozen bar; constrained-decoding failure as the cause; the
  anonymous Pollinations proxy as a capable credential-free endpoint. Hosted frontier classes
  remain untested, not rejected.
- **unknown.** Whether the failure reflects intrinsic control capacity or the frozen simplified
  observation (ELEMENTS still lists the hidden button after reveal) — **the exact unknown this
  experiment tests**; whether other observation formats/prompts/decoding or other quantisations/
  classes/tasks would change the bounded negative; whether any credentialed provider would clear
  the bar.
- **do_not_assume.** Do NOT encode `FALSIFIES` as a global rejection of `C-LLM-INHERIT`; do NOT
  re-run the same classes/quant/protocol ladder; do NOT treat the census as capability evidence;
  do NOT use external-comparator numbers as SPIDER evidence; do NOT treat clearing the minimal
  single-page task as product-scale inheritance evidence; do NOT generalize the bounded negative
  to other quantisations/classes/observation formats/task banks; do NOT pin HF GGUF digests from
  server metadata (pin the downloaded served body); do NOT read the 0.6 bar as a statistical
  threshold.

## 13. Non-duplication

A DESIGN-time search of `codex/legacy_artifact_index.json` (1401 artifacts) found **0 matches**
for `representation`, `accessibility`, `hidden`, `visibility`, `button`, `screenshot`, `llm`,
`gguf`, `endpoint`, `multistep`, `element`; the pre-2.0 era had no comparable frozen
model-capability protocol. This is not a rerun: the parent ladder held the observation fixed and
varied the model class; this packet holds the byte-verified model classes fixed and varies the
**observation** — a falsifier the parent did not test. It does not repeat the spent 3B–8B prompt
ablation (`EXP-INTEL-37982024058` / `EXP-INTEL-38164607941`), the byte-identity correction
(`EXP-INTEL-38175568787`) or the hosted census; it reuses their frozen runner/fixture and adds
only the frozen observation patch of Appendix A.

## 14. Freeze artifacts and eligibility

`freeze_artifacts` (hashed by the freezer into `freeze.json.artifact_hashes`; immutable
interpretation dependencies):

- `research/intel/run_exp_37982024058.py` — `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`
- `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` — `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`
- `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py` — `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`

The new code (the observation patch) is embedded verbatim in this prereg, which the freezer also
hashes. All six `freeze_eligibility` checks are `PASS` in `spec.json` (reasons there).

---

## Appendix A — observation patch (frozen; the ONLY runner change)

The patch is the ordered exact-string replacement `OLD → NEW` below. `OLD` occurs exactly once in
the frozen runner. EXECUTE must:

1. extract the bytes strictly between the `PATCH-OLD-BEGIN`/`PATCH-OLD-END` marker lines
   (exclusive) of the OLD block and the `PATCH-NEW-BEGIN`/`PATCH-NEW-END` marker lines
   (exclusive) of the NEW block, each with exactly one trailing newline;
2. verify `sha256(OLD) == 183d3c630e661de298567bdd4062a3b3d7cbbd6d2dac345dd2ff6334f4b8d654`
   and `sha256(NEW) == 61d8bf3fa5ec66f77e4157ab103535dc397eacf5e1c447fb5c3d5787ef235a66`;
3. verify `frozen_runner.count(OLD) == 1`; replace once;
4. verify `sha256(reconstructed_runner) == b2e3b7f9a1411176d66ba21f03659d9d21372fef5fa5b3ecad3ffd40dc7c0cd3`,
   that the default `OBS_MODE == "base"`, and that the `base` branch is AST-identical to the
   frozen `observe()` body;
5. fail closed (`MEASUREMENT_INVALID`) on any mismatch — never edit code by hand.

### A.1 `OLD` (frozen runner lines 104–117; sha256 `183d3c63…4b8d654`)

```python
# PATCH-OLD-BEGIN
# ---------------------------------------------------------------------------
# Page observation (identical style to parent EXP-INTEL-37973264582 harness)
# ---------------------------------------------------------------------------
def observe(page, history):
    els = page.eval_on_selector_all(
        "button, a, input",
        "els => els.map(e => ({tag:e.tagName, id:e.id||'', text:(e.innerText||'').slice(0,40)}))",
    )
    body = page.inner_text("body")[:300]
    return {
        "page_text": body,
        "elements": els,
        "history": list(history),
    }
# PATCH-OLD-END
```

### A.2 `NEW` (sha256 `61d8bf3f…f235a66`)

```python
# PATCH-NEW-BEGIN
# ---------------------------------------------------------------------------
# Page observation (identical style to parent EXP-INTEL-37973264582 harness)
# ---------------------------------------------------------------------------
# <<< SPIDER-EXP-INTEL-38234107074 PATCH-BEGIN >>>
# The ONLY factor varied by this experiment: the observation/action
# representation. OBS_MODE is read once at import; the default "base"
# reproduces the frozen observation exactly.
OBS_MODE = os.environ.get("SPIDER_OBS_MODE", "base")


def _flatten_aria(node):
    out = []
    if isinstance(node, dict):
        role = node.get("role") or ""
        name = node.get("name") or ""
        if role or name:
            out.append({"tag": role, "id": "", "text": (name or "")[:40]})
        for ch in (node.get("children") or []):
            out.extend(_flatten_aria(ch))
    elif isinstance(node, list):
        for ch in node:
            out.extend(_flatten_aria(ch))
    return out


def _observe_a11y(page):
    snap = None
    try:
        snap = page.locator("body").aria_snapshot()
    except Exception:
        snap = None
    if snap is None:
        try:
            snap = page.accessibility.snapshot(interesting_only=True)
        except Exception:
            snap = None
    if snap is None:
        raise RuntimeError(
            "SPIDER_OBS_MODE=a11y unavailable: neither Locator.aria_snapshot nor "
            "Page.accessibility.snapshot is present in this Playwright build"
        )
    if isinstance(snap, str):
        els = [{"tag": "aria", "id": "", "text": ln.strip()[:40]}
               for ln in snap.splitlines() if ln.strip()][:60]
    else:
        els = _flatten_aria(snap)
    return els


def observe(page, history):
    if OBS_MODE == "base":
        els = page.eval_on_selector_all(
            "button, a, input",
            "els => els.map(e => ({tag:e.tagName, id:e.id||'', text:(e.innerText||'').slice(0,40)}))",
        )
        body = page.inner_text("body")[:300]
    elif OBS_MODE == "visible":
        els = page.eval_on_selector_all(
            "button, a, input",
            "els => els.filter(e => { const r = e.getBoundingClientRect(); const s = window.getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0'; }).map(e => ({tag:e.tagName, id:e.id||'', text:(e.innerText||'').slice(0,40)}))",
        )
        body = page.inner_text("body")[:300]
    elif OBS_MODE == "a11y":
        els = _observe_a11y(page)
        body = page.inner_text("body")[:300]
    else:
        raise RuntimeError("unknown SPIDER_OBS_MODE: %r" % OBS_MODE)
    return {
        "page_text": body,
        "elements": els,
        "history": list(history),
    }
# <<< SPIDER-EXP-INTEL-38234107074 PATCH-END >>>
# PATCH-NEW-END
```

## Appendix B — DESIGN-time probe log (non-outcome-bearing)

No model inference, no browser launch, no outcome-bearing measurement was performed.

| # | probe | result |
|---|---|---|
| B1 | sha256 of the three freeze artifacts | runner `2b5d5bb5…` fixture `7aba9dc8…` provenance `4e2b6710…` (all match) |
| B2 | patch anchor search in frozen runner | `count(OLD) == 1`; `sha256(OLD)=183d3c63…`, `sha256(NEW)=61d8bf3f…` |
| B3 | reconstruct + `py_compile` | `py_compile OK`; `sha256(reconstructed)=b2e3b7f9…c0cd3` (22,277 bytes) |
| B4 | base-branch AST equivalence vs frozen `observe` | base branch statements `==` frozen `els=`/`body=` statements (True); return expression `==` (True); base JS map string identical (True) |
| B5 | Node semantic probe of the exact two JS element sources | with an element whose computed `display:none` and zero rect: `base` lists it **before and after** reveal; `visible` lists it **before** and **not after** — the treatment predicate does exactly the intended suppression |
| B6 | branch liveness (heavy deps stubbed) | default `OBS_MODE=='base'`; `visible` and `a11y` return well-formed observation dicts; `a11y` falls back from `Locator.aria_snapshot` to `Page.accessibility.snapshot`; unavailable a11y raises an explicit operational `RuntimeError`; unknown mode raises |
| B7 | candidate URL reachability (HEAD) | both revision-pinned URLs HTTP 200, `content-length` equal to the pinned byte counts, `x-linked-etag` equal to the pinned `served_body_sha256` (no download at DESIGN; full-download re-verify at EXECUTE) |
| B8 | `llama-cpp-python==0.2.90` on PyPI | sdist `llama_cpp_python-0.2.90.tar.gz` present |
| B9 | legacy non-duplication search | `codex/legacy_artifact_index.json` (1401 artifacts): 0 matches for the term list in section 13 |
| B10 | environment | Python 3.12.15; nproc 4; ~14 GB available RAM; 85 GB free disk; Chrome 154.0.8037.97; `llama_cpp`/`playwright` not preinstalled (installed at EXECUTE) |

## Appendix C — runner reconstruction & verification procedure (EXECUTE)

1. Re-verify `freeze.json.artifact_hashes` for all three freeze artifacts; fail closed on mismatch.
2. Extract `OLD`/`NEW` from Appendix A per the Appendix A.1 rules; verify their sha256 and
   `count(OLD)==1`; reconstruct the runner; verify the reconstructed sha256, the default mode,
   and base-branch AST equivalence (A.4).
3. Materialize per-cell config overlays and verify the object-level diff is confined to
   `prompts.system`, `sampling.chat_format`, `candidate_models_frozen`.
4. Run `PREFLIGHT` (rule 1) including `PC-OBSERVATION-CONTRAST` on the real served page.
5. Run the frozen cell order for each model with `SPIDER_OBS_MODE` set per cell; preserve all raw
   completions and per-step records under `<cell-outdir>/raw/`.
6. Apply the frozen decision rule (section 7); write `result.json`, `report.md`, `provenance.json`
   with the exact metric/control ids of sections 5–6 and the frozen outcome vocabulary.
