# EXP-INTEL-38110512532 preregistration (design-contract v2)

- **experiment_id**: `EXP-INTEL-38110512532`
- **lane**: intel
- **claim_ids**: [`C-LLM-INHERIT`] (registry id; registry sha256 `3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b`)
- **request**: `research/experiments/EXP-INTEL-38110512532/request.json` (request_hash `0e7eac9014a7dd5ab4a1a64ff52c5ebd753c3eaabfa8a091131727bc6d7407b5`), immutable
- **design_contract_version**: 2
- **status**: DESIGN COMPLETE — all six `freeze_eligibility` checks PASS (see `spec.json#freeze_eligibility`); no outcome-bearing measurement performed

---

## 1. Overview

This is the mandated goal/schema **system-prompt specification ablation** on the
two live credential-free CPU-quantized endpoints of the C-LLM-INHERIT readiness
sequence. It reuses, byte-for-byte where possible, the accepted machinery of
`EXP-INTEL-37982024058` (frozen harness `research/intel/run_exp_37982024058.py`,
frozen task config `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json`,
frozen GBNF grammar, sampling, seeds and model artifacts). The **single
manipulated variable** is the value of `prompts.system`:

- `P-TREAT-GOAL-SCHEMA` (treatment): goal + action-schema prompt, adapted from the
  grandparent harness SYS prompt (`EXP-INTEL-37973264582/raw/code/min_webagent.py`);
- `P-COMP-UNDERSPECIFIED` (comparator): byte-identical to the audited parent anchor
  prompt, re-run **within this packet** as a matched paired comparator.

A bounded negative here is the mandate's decision-changing exit: it retires the
CPU-quantized local endpoint plan for the four-arm benchmark and forces the
provisioning decision (stronger local model vs stable proxy vs credential
acquisition).

## 2. Inherited state (parent handoff, sibling, mandate)

Source: `research/experiments/EXP-INTEL-37982024058/handoff.json` (sha256
`b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55`) and
`research/experiments/EXP-INTEL-38106207218/request.json` + `failure.json`.

**Parent handoff four-way distinction (preserved):**
- `established`: under the frozen protocol with the underspecified system prompt,
  M-7B-QWEN and M-3B-QWEN both achieve task_success_rate 0/5 with
  parseable_action_rate_step1 1.0 (audit PASS, producer_claim_supported=true);
  constrained decoding works (PC-JSON-CONSTRAINED-DECODING 10/10 both models);
  verifier sound (NC 0/5 parseable, 0/5 success); the failure mode is prompt-sensitive:
  step-0 reveal-click succeeds (revealed_value TARGET-42) but answer is never emitted.
- `rejected`: the 0/5 outcome at the frozen ceiling as a claim about *any other*
  prompt/model/environment; C-LLM-INHERIT is NOT globally rejected.
- `unknown`: whether 3B/7B Qwen2.5 Q4_K_M can clear the minimal bar under a
  properly specified goal/schema prompt (this experiment); any endpoint-capability
  statement; variance of the deterministic protocol.
- `do_not_assume`: (a) no generalization beyond the frozen ceiling; (b) 7B
  single-file URL 404 -> split shards are a packaging, not model, substitution
  (VF-02); (c) temp=0 fixed seeds give no variance estimate; 3/5 rule is
  pre-declared adequacy, not statistics (VF-03); (d) task failure is not due to
  missing page text (VF-04); (e) the parent B-RANDOM-ACTION (measured on
  about:blank) is structurally insensitive and is **not reused** as evidence.

**Sibling `EXP-INTEL-38106207218`** (same mandate question): passed `model_design`
but never froze; blocked by the shared design-review model routing failure
(fingerprint `3b9ff5e4e9e73f23e368efb4`, control_revision
`bfa3c519a2a0e6fa67418a49021072b9b7d8b316fb68952420df800a2e6c6801`, stage=design,
exit 1, retryable=false). Its spec/prereg are unfrozen templates only; this packet
is a fresh design under the same mandate, not an adoption of sibling files.

**Director mandate** (in request.json#director_mandate, action CONTINUE,
parent_handoff_disposition **SUPERSEDE**, cognitive_reset=true, claim
C-LLM-INHERIT): the strategic question quoted verbatim in section 3 is binding
direction; the parent handoff is continuity evidence only and does not override
the SUPERSEDE disposition.

## 3. Question, hypothesis, falsifier

**Question (verbatim from mandate strategic_question field):** "Would supplying
the task goal/schema in the system prompt (as the parent harness's SYS prompt did)
convert the step-0 reveal-click into a full click-then-answer completion for
M-7B-QWEN or M-3B-QWEN under the same credential-free CPU-quantized constraints -
i.e., is the accepted 0/5 falsification of EXP-INTEL-37982024058 attributable to
prompt underspecification rather than to model capability, thereby separating the
two failure modes and determining whether ANY local CPU-quantized 3B-8B endpoint
can clear the minimal multi-step Web-agent capability bar (valid parseable JSON
action + completion) required for readiness condition (3) of the gated four-arm
benchmark, with the exact provisioning receipt recorded and a bounded negative (no
endpoint in the tested class can complete the task even with a properly specified
goal/schema) as the decision-changing exit?"

**Hypothesis H1 (prompt-specification attribution):** at least one of M-7B-QWEN
(primary, evaluated first) or M-3B-QWEN (fallback) clears the pre-declared bar
(task_success_rate >= 0.6 AND parseable_action_rate_step1 >= 0.6 over the 5 frozen
seeded episodes) under P-TREAT-GOAL-SCHEMA, while its within-experiment paired
comparator cell under P-COMP-UNDERSPECIFIED stays below the bar with a material
lift (TREAT success count − COMP success count >= 2). I.e., the parent's
step-0-click-only failure mode (VF-01) converts to full click-then-answer
completion exactly when the goal/schema is supplied.

**Falsifier H0:** neither M-7B-QWEN nor M-3B-QWEN clears the bar under
P-TREAT-GOAL-SCHEMA (all evaluated treatment cells < 0.6 task_success_rate) under
a measurement-valid packet. This yields the mandate's bounded negative: the parent
0/5 is attributable to model/endpoint capability (or a joint prompt-effectiveness
floor of the tested class), not to prompt underspecification alone; no local
CPU-quantized Qwen2.5 3B/7B Q4_K_M endpoint completes the minimal multi-step
Web-agent capability test even with a properly specified goal/schema.

## 4. Prompt conditions and config transcription (content-pinned)

Two condition strings; both leak neither `#reveal-btn` nor `TARGET-42`
(probe P-2 leakage check scoped to prompts.system):

| id | role | exact string |
|---|---|---|
| `P-TREAT-GOAL-SCHEMA` | treatment | `You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<id>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.` |
| `P-COMP-UNDERSPECIFIED` | comparator | `You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.` |

The treatment is the grandparent harness SYS prompt
(`research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`, sha256
`4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`) with the
**sole documented adaptation** `ref` -> `selector`, which is *required* for
conformance with the frozen GBNF grammar and `action_schema` (keys `selector`/`text`
only). The comparator is the byte-identical parent anchor prompt (project copy in
the frozen template).

**Config transcription rule (frozen, deterministic):** ECXUTE deep-copies the
frozen template `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json`
(sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`) and
applies EXACTLY these edits, then serializes with
`json.dumps(cfg, indent=2, sort_keys=True).encode() + b"\n"`:

1. `fixture_id` := per-config id below;
2. `source` := "frozen EXP-INTEL-38110512532 prereg.md sections 4-6 and spec.json measurement_validity; constructed before any outcome-bearing measurement";
3. for `P-TREAT-GOAL-SCHEMA` configs only: `prompts.system` := the treatment string above.

Expected bytes (probe P-2, byte-verified at DESIGN):

| config id | fixture_id | sha256 | bytes |
|---|---|---|---|
| `CFG-TREAT` | `FIX-CFG-EXP-INTEL-38110512532-TREAT` | `988751c6b607f6b5b76cdbce569db066faec5b56cb2aef00f44570d9526ec8fb` | 4491 |
| `CFG-COMP` | `FIX-CFG-EXP-INTEL-38110512532-COMP` | `4a2ef4be897b8de96be930e59b1471ca8c02ae7a147858a13060ed952ed88daa` | 4362 |
| `CFG-CONTROLS` | `FIX-CFG-EXP-INTEL-38110512532-CONTROLS` | `14589f7cdf9fffcfac016de0bea8f076cf6e51518d6affd7b6779b1388c30cdd` | 4366 |

The COMP config differs from the template only in `fixture_id`/`source`
(byte-identical prompts.system to the parent anchor); the TREAT config differs in
`fixture_id`/`source`/`prompts.system` only. Minimum editor: a `python3` one-liner
using `json.load`/`json.dump`; byte-identity of the generated config with the
pinned sha256 is a mandatory EXECUTE verification step (mismatch = stop and
investigate, do not proceed; see section 11).

## 5. Candidates and provisioning (receipt to be recorded exactly)

| candidate_id | role | model | quant | GGUF files (local dir `/tmp/opencode/gguf/`) | sha256 (frozen manifest `raw/gguf_sha256.txt`) |
|---|---|---|---|---|---|
| `M-7B-QWEN` | primary | Qwen2.5-7B-Instruct | Q4_K_M | `qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf` (+3993201344 B) | `dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db` |
| | | | | `qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf` (+689872288 B) | `539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a` |
| `M-3B-QWEN` | fallback | Qwen2.5-3B-Instruct | Q4_K_M | `qwen2.5-3b-instruct-q4_k_m.gguf` (+2104932768 B) | `626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d` |

- Frozen primary 7B single-file URL (`.../qwen2.5-7b-instruct-q4_k_m.gguf`) returns
  HTTP 404 (VF-02, established); the same-repo same-quant split shards are used and
  the deviation is recorded (packaging, not model, substitution).
- Download at EXECUTE via `urllib` GET on the `resolve/main` URLs (probe P-4: all
  return 302 to the Xet CDN today); verify sha256 (streaming) against the manifest;
  reuse existing files if and only if the hash matches (files are already present
  from the DESIGN probes).
- Harness load path: `Llama(model_path=paths[0], n_ctx=2048, n_threads=4,
  verbose=False, chat_format="qwen", seed=42)`; llama.cpp auto-locates the
  companion shard from the `-NNNNN-of-NNNNN` naming pattern (probe P-5, re-verified
  on DESIGN re-dispatch: 7B load 0.433 s, 3B load 0.316 s; load time is
  host-state-dependent, while the sha256 and grammar-valid emission pins are stable).
- The provisioning receipt to record at EXECUTE: URLs, byte sizes, sha256,
  load_time_s, load_status, chat_format, n_ctx, n_threads, llama_seed — per cell in
  `raw/model_receipts.json` (the harness already emits this).

## 6. Metrics, controls, stable identifiers

**Metrics (stable ids, reused from parent where they exist):**
`positive_control_pass_rate`, `parseable_action_rate_step1`, `task_success_rate`,
`click_reveal_rate` (fraction of episodes with `clicked_reveal` true — derived from
episode records), `answer_action_emission_rate` (fraction of episodes containing at
least one answer action in `steps` — derived), `mean_inference_latency_s`,
`mean_completion_tokens`, `capability_bar`.

**Bar (capability_bar):** a cell clears iff `task_success_rate >= 0.6` (>=3/5)
AND `parseable_action_rate_step1 >= 0.6` (>=3/5) — identical to the parent.

**Controls (stable ids):**

| control_id | role | expected | failure policy |
|---|---|---|---|
| `PC-JSON-CONSTRAINED-DECODING` | mechanism positive control (per cell) | 10/10 valid schema-conforming JSON under the cell's own prompts.system | cell EXCLUDED if < 10/10; both treatment cells excluded -> MEASUREMENT_INVALID/INCONCLUSIVE |
| `PC-ORACLE-EPISODE` | scorer/reachability positive control (preflight) | 5/5 scripted click-then-answer episodes through the real `run_episode` on the served page | <5/5 -> MEASUREMENT_INVALID/INCONCLUSIVE |
| `NC-NO-MODEL-ACTION` | verifier null control (preflight) | 0.0 parseable, 0.0 success | any parse/success -> MEASUREMENT_INVALID/INCONCLUSIVE |
| `B-RANDOM-ACTION` | chance negative baseline (preflight, REPAIRED navigation) | parseable 1.0; success exactly 0.2 with vector [T,F,F,F,F] | mismatch -> MEASUREMENT_INVALID/INCONCLUSIVE |
| `B-CELL-COMP-UNDERSPECIFIED` | matched comparator pair (per candidate cell cell `COMP-M7B`/`COMP-M3B`) | task_success_rate < 0.6 (frozen anchor: 0/5); parseable >= 0.6 | COMP >= 0.6 -> ANCHOR rule -> MEASUREMENT_INVALID/INCONCLUSIVE |
| `B-0.5B-QWEN-LOCAL` | carried reference (NOT re-run) | 0/0/0 per EXP-INTEL-37973264582 | n/a (recorded reference) |
| `B-POLLINATIONS-PROXY` | carried reference (NOT re-run) | 0% success, ~197-token cap, 402s | n/a (recorded reference) |

## 7. Decision rule (full precedence; first matching rule wins)

Outcome taxonomy: `SUPPORTS | FALSIFIES | MIXED | INCONCLUSIVE`; status:
`COMPLETE | MEASUREMENT_INVALID | BLOCKED`. A valid scientific negative is
`status=COMPLETE, outcome=FALSIFIES`. `infrastructure/substrate failure is never
encoded as scientific falsification`.

- **(1) PREFLIGHT** — run once before any model cell: `PC-ORACLE-EPISODE == 5/5`
  AND `NC-NO-MODEL-ACTION == (0.0, 0.0)` AND `B-RANDOM-ACTION == (parseable 1.0,
  success_rate 0.2, success_vector [True,False,False,False,False])`. Any mismatch
  -> `status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE` (record the deviation in
  validity_notes; repair and re-preflight if possible).
- **(2) MECHANISM (per cell)** — cell valid iff `PC-JSON == 10/10` AND
  `load_status == LOADED` AND `run_status == COMPLETE`. Invalid cell = EXCLUDED
  (no episodes interpreted). Both treatment cells excluded -> `MEASUREMENT_INVALID`
  / `INCONCLUSIVE`.
- **(3) ANCHOR** — any measured COMP cell with `task_success_rate >= 0.6` -> the
  parent 0/5 anchor is not reproduced and paired prompt attribution is confounded
  -> `status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE` (raw comparator kept as a
  drift observation; it is NOT falsification and NOT promotion).
- **(4) SUPPORTS** — exists candidate c with measured TREAT_c clearing the bar AND
  measured COMP_c below the bar AND `lift(c) = TREAT_c.success_count -
  COMP_c.success_count >= 2`. Claim bounded to the clearing candidate(s). Early
  stop: if TREAT(M-7B) clears, M-3B cells are not run.
- **(5) MIXED** — no SUPPORTS AND at least one measured TREAT cell clears the bar
  but has lift < 2 (partial/ambiguous evidence: treatment reaches the bar yet the
  matched comparator is too close to attribute the conversion to the prompt).
  -> `status=COMPLETE, outcome=MIXED`.
- **(6) FALSIFIES** — no SUPPORTS and all measured TREAT cells fail the bar (packet
  otherwise valid) -> bounded negative per section 3 (`status=COMPLETE,
  outcome=FALSIFIES`).
- **(7) FALLBACK** — any other combination reachable under exclusions -> `status=
  MEASUREMENT_INVALID, outcome=INCONCLUSIVE` with an explicit reason.

**Reachability arithmetic (probe P-4, DESIGN-time):** success counts are integers
0..5; the bar is k>=3 on 5 episodes. (TREAT, COMP) pair outcomes under the ANCHOR
rule (COMP <= 2): T=0,1,2 -> FALSIFIES-class; T>=3 with (T-C)>=2 -> SUPPORTS-class;
T>=3 with (T-C)<2 and COMP<=2 -> exactly (T,C)=(3,2) (lift 1; T=4,C=2 already has
lift 2) -> MIXED-class. No branch is empty:
T5C0 (SUPPORTS), T3C2 (MIXED), T2C0 (FALSIFIES), T3C? with C>=3 (ANCHOR invalidation)
are all constructible integer outcomes, and PC-ORACLE 5/5 (probe P-3) demonstrates
the scorer can register T=5.

## 8. Validity and threats

Measurement-validity commitments (full list in `spec.json#measurement_validity`):

1. **Single variable**: only `prompts.system` varies between TREAT and COMP cells
   (probe P-2 byte-diff). All else identical to the parent packet.
2. **Deterministic protocol**: temp=0, llama_seed=42, per-episode seeds 42..46,
   max_tokens=512, n_ctx=2048, chat_format=qwen; identical to the parent. The
   anchor rule is COMP-below-bar (not exact replication) precisely because small
   residual nondeterminism is possible; a below-bar drift is disclosed as an
   observation in validity_notes.
3. **Falsifier reachable**: PC-ORACLE-EPISODE 5/5 (probe P-3) -> the scorer
   registers a full click-then-answer completion; no mechanical ceiling on SUPPORTS.
4. **Sensitive controls**: repaired B-RANDOM-ACTION on the served page leaves
   dynamic range (0.2 vs 0.6 bar); the parent about:blank baseline is retired.
5. **Packaging deviation (VF-02)** and **observation adequacy (VF-04)** inherited
   and unchanged (see section 2).
6. **Leakage**: neither condition string contains the selector or target.
7. **No outcome-bearing DESIGN measurement**: probes exercised stack, grammar,
   configs, controls and model load/liveness only (section 10).

**Threat register** (pre-declared; each mapped to a gate):

| threat | existence | control/gate |
|---|---|---|
| Scorer cannot register success | impossible (P-3 5/5) | PC-ORACLE-EPISODE == 5/5 else INCONCLUSIVE |
| Verifier false-accepts random/noise | impossible (P-3 0/0) | NC-NO-MODEL-ACTION |
| Chance baseline at/above bar (ceiling) | retired about:blank; 0.2 measured | B-RANDOM-ACTION pin |
| Environment drift vs parent anchor | possible | COMP below bar else INCONCLUSIVE (ANCHOR) |
| Decoding failure masquerading as task failure | possible | per-cell PC-JSON 10/10 |
| Prompt leakage of target/selector | ruled out (P-2) | leakage check |
| Model substitution/packaging artifact | ruled out (hashes) | sha256 pins + provisioning receipt |
| Small-n interpretation | pre-declared adequacy (3/5), no variance claim | spec section 7 / VF-03 inherited |

## 9. Legacy divergence / replication statement

- `codex/legacy_brief.json` and the pre-2.0 archive were screened (targeted reads
  only; `SPIDER_CODEX.md` was NOT ingested wholesale). **No minimal-capability
  model-endpoint probe** exists in the legacy archive: the closest pins
  (P2-WP002B next-state prediction mechanics; P2-MIND2WEB route-reuse rates) concern
  different mechanics and are NOT baselines here — recorded as NO_MATCH (consistent
  with the mandate's comparative_reasoning).
- This experiment is a **single-variable ablation on the accepted parent
  EXP-INTEL-37982024058** (a Research 2.0 FALSIFIES, not a legacy artifact): it
  reuses the frozen harness/config/grammar/sampling and changes only the system
  prompt, per the mandate's explicit authorization ("not a pointless repetition
  of the falsified setup"). No pre-2.0 method is replayed.
- `EXP-INTEL-38106207218` (same mandate) is a blocked sibling, not a precedent:
  its spec/prereg never froze and its probes were never recorded as artifacts; this
  packet's probes (section 10) are first-hand.
- Pre-2.0 divergence: the parent measured B-RANDOM-ACTION on about:blank (defect);
  here the control is repaired by pre-navigating to the served task page (probe P-3),
  and the PC-ORACLE reachability canary is added. PG1: no pre-2.0 finding is
  contradicted; the pre-2.0 assumption "0/N under underspecified prompt = capability"
  is explicitly rejected in favor of the mandate's separation principle.

## 10. Pre-freeze satisfiability probes (DESIGN-time, non-outcome-bearing)

All probes were re-run and re-verified on the DESIGN re-dispatch (fresh runner:
the pinned packages were re-installed from the frozen versions and the GGUF files
re-downloaded with streaming sha256 verification against the manifest). Raw probe
values are recorded here as frozen expectations for EXECUTE/AUDIT.

| probe | what | result (evidence) |
|---|---|---|
| P-0 stack | python 3.12.15; llama-cpp-python 0.2.90; playwright 1.63.0 (both re-installed and import-verified on DESIGN re-dispatch); `/usr/bin/google-chrome` present; 4 cores; 15 GB RAM | PASS |
| P-1 grammar | `LlamaGrammar.from_string(frozen gbnf_grammar)` compiles; fields restrict to click/answer x selector/text | PASS |
| P-2 configs | deterministic transcription of CFG-TREAT/COMP/CONTROLS; sha256 988751c6..., 4a2ef4be..., 14589f7c...; TREAT top-level diff = {fixture_id, prompts, source}; COMP diff = {fixture_id, source}; leakage scoped to prompts.system = none | PASS (hashes pinned section 4) |
| P-3 controls | Appendix-A driver through the REAL `run_episode` on the served page: oracle_success_rate=1.0 (5/5); NC=[0.0,0.0]; RANDOM=[1.0, 0.2], vector [True,False,False,False,False]; `raw/control_episodes.json` schema conforms | PASS |
| P-4 URLs | 7B shard1/shard2 resolve -> Xet CDN (HEAD final 200; Content-Length 3993201344/689872288 matches manifest); 7B single-file 404 (documented, VF-02); 3B resolve -> Xet CDN (final 200; 2104932768) | PASS (VF-02 intact) |
| P-5 load+liveness | GGUF sha256 all match manifest (fresh download on DESIGN re-dispatch, streaming verify: dfce12e3..., 539cf93f..., 626b4a66...); `load_model` 7B 0.433 s (split-shard auto-locate), 3B 0.316 s (load time host-state-dependent); under P-TREAT-GOAL-SCHEMA both models emit grammar-valid `{"action":"click","selector":"#reveal-btn"}` (M-7B emit 10.5 s, M-3B emit 4.3 s) — mechanism alive, outcome not measured | PASS |

The byte-level diff is verified by re-deriving each config from the frozen
template and exercising the pinned sha256 from section 4 as the authoritative
check — see spec `baseline_identifiability`.

## 11. EXECUTE protocol (frozen steps)

Directory layout under `research/experiments/EXP-INTEL-38110512532/`:

```
preflight/raw/harness_config.json        <- CFG-CONTROLS bytes
cells/COMP-M7B/raw/harness_config.json   <- CFG-COMP bytes
cells/TREAT-M7B/raw/harness_config.json  <- CFG-TREAT bytes
cells/COMP-M3B/raw/harness_config.json   <- CFG-COMP bytes
cells/TREAT-M3B/raw/harness_config.json  <- CFG-TREAT bytes
preflight/controls_driver.py             <- Appendix A bytes (sha256 fdbcdc28...)
```

1. **Generate + verify configs** (P-2 rule, section 4): write the five config
   files; verify each sha256 equals the pinned value; mismatch -> STOP (do not
   proceed; record in `raw/` and mark BLOCKED, not a scientific result).
2. **Write controls driver** from Appendix A verbatim; verify sha256
   `fdbcdc28f9f4231278ac4ce4dca2593acbf9f0205cd5dbbad11b5a160bb8f5bb`.
3. **Prep models**: for the candidates needed, download GGUF(s) to
   `/tmp/opencode/gguf/` (reuse if sha256 matches the manifest) — 7B: shard pair;
   3B: single file. Record download/verify evidence in `provenance.json`.
4. **PREFLIGHT (gate 1)** — `python3 preflight/controls_driver.py --outdir
   preflight --chrome /usr/bin/google-chrome`; assert printed values equal the
   P-3 pin (rule 1). Mismatch -> MEASUREMENT_INVALID/INCONCLUSIVE.
5. **Cells in order** — for each needed cell, `python3 research/intel/
   run_exp_37982024058.py --mode probe-candidate --outdir <cell dir> --candidate
   <M-7B-QWEN|M-3B-QWEN> --gguf <local paths> --chrome /usr/bin/google-chrome
   --n-threads 4`. Order: COMP-M7B, TREAT-M7B; early stop after a clearing TREAT
   cell (M-3B cells skipped). Validate rule 2 per cell (PC 10/10, LOADED,
   COMPLETE).
6. **Derive metrics** — the harness writes episode records inside
   `raw/model_receipts.json` (per-candidate `episodes` arrays, each with `steps`,
   `step1_parse_ok`, `clicked_reveal`, `revealed_value`, `final_answer`,
   `task_success`, `seed`); EXECUTE extracts them into a derived convenience file
   `raw/task_episodes.json` (`{"experiment_id", "candidates", "controls"}`, per the
   parent precedent) and computes the metrics with the stable ids of section 6
   (incl. derived click_reveal_rate and answer_action_emission_rate from episode
   `steps`).
7. **Apply decision rule** (section 7, precedence) -> `result.json`,
   `report.md`, `provenance.json` (packet shapes per EXPERIMENT_PACKET.md),
   preserving control identifiers and evidence paths.
8. **Preserve raw evidence**: `raw/harness_config.json` (per cell),
   `raw/control_episodes.json`, `raw/model_receipts.json` (authoritative episode
   source), derived `raw/task_episodes.json` (step 6), episode traces, receipts,
   command logs.

**Failure policy:** a LOAD_FAILED/Load error in a cell, download mismatch, or any
runtime harness error is an infrastructure event: record it in `result.json`
(status MEASUREMENT_INVALID or BLOCKED with reason; never FALSIFIES). PC/control
failures are measurement-validity events per rules 1-2.

## 12. Consequences (summary — full text in spec.json)

- **SUPPORTS**: four-arm benchmark may proceed on the local Qwen class with the
  goal/schema-specified system prompt; provisioning receipt recorded; readiness
  condition (3) cleared on the local class (DIRECTOR adjudicates the claim update).
- **FALSIFIES**: bounded negative retires the CPU-quantized local endpoint plan;
  forces the provisioning decision (stronger local model vs stable proxy vs
  credential acquisition); the four-arm benchmark is not funded on the tested local
  class.
- **MIXED**: ambiguous lift; publish as bounded partial evidence; recommend a
  power-bumped focused replication (more episodes) before any provisioning decision.
- **MEASUREMENT_INVALID/INCONCLUSIVE**: packet-level outcome only; no claim change;
  record exact repair needed.

## 13. File inventory (evidence refs used above)

- Harness: `research/intel/run_exp_37982024058.py` (sha256 `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`)
- Frozen task/template config: `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`)
- Grandparent prompt source: `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py` (sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`)
- gguf manifest: `research/experiments/EXP-INTEL-37982024058/raw/gguf_sha256.txt` (sha256 `93836c2594b0c156c0fa913fb384e913586cb03adbd501773fdf6fd450176dbd`)
- Provisioning evidence: `research/experiments/EXP-INTEL-37982024058/raw/provisioning_evidence.json` (sha256 `7b1e50436e75292baa88029264938773342b99785536a94c185d8371b74693f0`)
- Parent packet: `research/experiments/EXP-INTEL-37982024058/{result.json,audit.json,handoff.json}` (audit PASS, producer_claim_supported=true)

---

## Appendix A — preflight controls driver (FROZEN text)

sha256 of the file bytes below: `fdbcdc28f9f4231278ac4ce4dca2593acbf9f0205cd5dbbad11b5a160bb8f5bb`
(4637 bytes). EXECUTE writes this file verbatim (fenced content only, no leading/
trailing whitespace beyond the fence) as `<experiment_dir>/preflight/
controls_driver.py`, verifies the sha256, then runs it. It reuses frozen harness
functions; it adds ONLY the repaired served-page navigation and the oracle canary;
it performs no model inference.

```python
#!/usr/bin/env python3
"""EXP-INTEL-38110512532 preflight controls driver (FROZEN text, Appendix A of
prereg.md). Reuses the frozen harness functions from run_exp_37982024058.py.

REPAIRED NAVIGATION vs the parent harness null-random mode: the page is navigated
to the served task URL before episodes, so the PC-ORACLE canary, NC-NO-MODEL-ACTION
and B-RANDOM-ACTION all run against the actual task page through the real
run_episode scorer. No model inference is performed; scripted producers only.

Writes <outdir>/raw/control_episodes.json and prints the preflight values.
"""
import argparse, json, os, random, sys

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SPIDER_ROOT") or _here
while ROOT and not os.path.exists(os.path.join(ROOT, "research", "intel", "run_exp_37982024058.py")):
    parent = os.path.dirname(ROOT)
    if parent == ROOT:
        raise SystemExit("repo root not found above %s" % _here)
    ROOT = parent
sys.path.insert(0, os.path.join(ROOT, "research", "intel"))
import run_exp_37982024058 as h  # frozen harness code (freeze_artifacts)

def oracle_producer(obs, step):
    if step == 0:
        return json.dumps({"action": "click", "selector": "#reveal-btn"}), 0.0, 0, {"kind": "oracle"}
    return json.dumps({"action": "answer", "text": "TARGET-42"}), 0.0, 0, {"kind": "oracle"}

def rate(eps, key):
    return sum(1 for e in eps if e[key]) / len(eps)

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

            oracle_eps = []
            for ep in range(5):
                r = h.run_episode(page, "", "", max_steps, oracle_producer)
                r["episode"] = ep
                oracle_eps.append(r)
            out["PC-ORACLE-EPISODE"] = {
                "control_id": "PC-ORACLE-EPISODE", "episodes": oracle_eps,
                "task_success_rate": rate(oracle_eps, "task_success"),
            }

            nc = cfg["null_control"]
            nc_eps = []
            null_prod = h.make_null_producer(nc["fixed_invalid_content"])
            for ep in range(nc["episodes"]):
                r = h.run_episode(page, "", "", max_steps, null_prod)
                r["episode"] = ep
                nc_eps.append(r)
            out["NC-NO-MODEL-ACTION"] = {
                "control_id": nc["id"], "episodes": nc_eps,
                "parseable_action_rate_step1": rate(nc_eps, "step1_parse_ok"),
                "task_success_rate": rate(nc_eps, "task_success"),
                "criterion": nc["success_criterion"],
            }

            rb = cfg["random_baseline"]
            rng = random.Random(cfg["sampling"]["base_seed"])
            rand_eps = []
            rand_prod = h.make_random_producer(rb["action_space"], rng)
            for ep in range(rb["episodes"]):
                r = h.run_episode(page, "", "", max_steps, rand_prod)
                r["episode"] = ep
                rand_eps.append(r)
            out["B-RANDOM-ACTION"] = {
                "baseline_id": rb["id"], "episodes": rand_eps,
                "parseable_action_rate_step1": rate(rand_eps, "step1_parse_ok"),
                "task_success_rate": rate(rand_eps, "task_success"),
                "success_vector": [bool(e["task_success"]) for e in rand_eps],
            }
            b.close()
    finally:
        srv.shutdown()
    with open(os.path.join(rawdir, "control_episodes.json"), "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps({
        "oracle_success_rate": out["PC-ORACLE-EPISODE"]["task_success_rate"],
        "NC": [out["NC-NO-MODEL-ACTION"]["parseable_action_rate_step1"],
               out["NC-NO-MODEL-ACTION"]["task_success_rate"]],
        "RANDOM": [out["B-RANDOM-ACTION"]["parseable_action_rate_step1"],
                   out["B-RANDOM-ACTION"]["task_success_rate"]],
        "RANDOM_success_vector": out["B-RANDOM-ACTION"]["success_vector"],
    }))

if __name__ == "__main__":
    main()
```

## Appendix B — config transcription snippet (frozen rule, section 4)

Non-outcome-bearing construction helper; the authoritative artifacts are the pinned
sha256 values in section 4, and EXECUTE must verify bytes against them.

```python
import json, hashlib
TEMPLATE = "research/experiments/EXP-INTEL-37982024058/raw/harness_config.json"
SOURCE = ("frozen EXP-INTEL-38110512532 prereg.md sections 4-6 and spec.json "
          "measurement_validity; constructed before any outcome-bearing measurement")
TREAT_SYS = ("You are a web agent. Reply ONLY with one JSON object per turn, no prose. "
             "Actions available: {\"action\":\"click\",\"selector\":\"<id>\"} or "
             "{\"action\":\"answer\",\"text\":\"<code>\"}. Click the button to reveal the code, then answer it.")
def build(fixture_id, system=None):
    c = json.loads(json.dumps(json.load(open(TEMPLATE))))
    c["fixture_id"] = fixture_id
    c["source"] = SOURCE
    if system is not None:
        c["prompts"]["system"] = system
    return json.dumps(c, indent=2, sort_keys=True).encode() + b"\n"
# CFG-TREAT = build("FIX-CFG-EXP-INTEL-38110512532-TREAT", TREAT_SYS)   # expect 988751c6...
# CFG-COMP  = build("FIX-CFG-EXP-INTEL-38110512532-COMP")               # expect 4a2ef4be...
# CFG-CONTROLS = build("FIX-CFG-EXP-INTEL-38110512532-CONTROLS")        # expect 14589f7c...
```