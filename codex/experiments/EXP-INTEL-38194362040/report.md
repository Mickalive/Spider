# EXP-INTEL-38194362040 — Byte-verified credential-free capable-endpoint capability ladder (corrected freeze) + hosted-provisioning census

- **Lane:** intel
- **Claim:** `C-LLM-INHERIT` (single claim id; per frozen `spec.claim_ids`)
- **Status:** `COMPLETE`
- **Outcome:** `FALSIFIES`
- **B3_STATUS:** `NOT_SATISFIED`
- **Design contract:** v2 (`freeze.json.design_contract_version`), `design_review.json` = PASS
- **Frozen packet:** `request.json` `38039a17…`, `spec.json` `2f787080…`, `prereg.md` `f1429eaa…`, `design_review.json` `6a84d75b…` (all re-verified on disk at EXECUTE)
- **Freeze artifacts:** all three hashes in `freeze.json.artifact_hashes` MATCH (`raw/preflight.json.freeze_artifact_hashes`)

This packet is the corrected continuation of `EXP-INTEL-38175568787` (MEASUREMENT_INVALID — a
substrate/provisioning identity defect, **not** a capability result). Its purpose was to repair the
content-identity freeze defect and then run the frozen capability ladder. It does **not** re-run the
spent 3B–8B Qwen prompt ablation (`EXP-INTEL-38164607941`) or the spent Pollinations agent attempt.

---

## 1. What was done (method, as frozen)

1. **Preflight** (rule 1), once, against the frozen runner and the frozen served page.
2. **Endpoint census** (rule 2), independently and non-gating: credential env-var presence +
   unauthenticated reachability + classification for each predeclared hosted provider.
3. **Capability ladder** (rule 3) over `[M-14B-QWEN, M-8B-LLAMA]` in order:
   byte-level content-identity verification → load → `PC-JSON-CONSTRAINED-DECODING` gate (10 probes) →
   5 seeded episodes (seeds 42–46) under the frozen runner.

Only the model GGUF (and the family `chat_format` needed to load it) differs between cells. The task
page, user template, system prompt `P-TREAT-GOAL-SCHEMA` (string sha `36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716`),
GBNF grammar, sampling (`temperature=0.0`, `max_tokens=512`, `n_ctx=2048`, seeds, `n_threads=4`),
strict `parse_action` and the mechanical `run_episode` scorer are identical for every cell.

**Frozen bar:** `task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6` over 5 episodes.

---

## 2. Raw evidence produced

Artifacts (with sha256 in `result.json.artifacts`) are under
`research/experiments/EXP-INTEL-38194362040/`:

| Artifact | Role |
|---|---|
| `raw/preflight.json` | raw — preflight checks + freeze-artifact hash verification |
| `raw/controls.json` | raw — PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION, B-RANDOM-ACTION episode logs |
| `raw/materialized_configs.json` | raw — overlay/mirror sha256 + diff-path confinement |
| `raw/provisioning_evidence.json` | raw — byte/sha256/fingerprint identity receipts |
| `raw/endpoint_census.json` | raw — 12-provider credential/reachability classification |
| `raw/external_comparators.json` | raw — 3-entry comparator readiness table (`CANDIDATE_NOT_EVIDENCE`) |
| `raw/decision.json` | derived — frozen-rule decision + trace |
| `cells/M-14B-QWEN/raw/{harness_config,provisioning_receipt,model_receipts}.json` | fixture/raw/raw |
| `cells/M-8B-LLAMA/raw/{harness_config,provisioning_receipt,model_receipts}.json` | fixture/raw/raw |
| `configs/config_{M-14B-QWEN,M-8B-LLAMA}.json` | fixture (mirrors) |

Per-candidate runner config overlays are deterministic transformations of the frozen base fixture
(`7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`). The object-level diff is
confined to `prompts.system`, `sampling.chat_format`, `candidate_models_frozen`
(`raw/materialized_configs.json.diff_confined_to_allowed_keys = true` for both cells).

---

## 3. Observations (direct, no interpretation)

### 3.1 Preflight — PASS (all five checks true)

`raw/preflight.json.checks`: `PC_ORACLE_EPISODE_5of5=true`, `NC_parseable_0_and_success_0=true`,
`B_RANDOM_parseable_1_and_success_lt_0.6=true`, `freeze_artifact_hashes_match=true`,
`required_stack_imports_ok=true`.

### 3.2 Content-identity repair — CONFIRMED (IDENTITY-PASS on both)

At EXECUTE each candidate’s revision-pinned served body was streamed in full and hashed. Observed
`sha256` equals the frozen `served_body_sha256` pin (which equals the HF tree-API `lfs.oid`), at equal
byte count; the parsed GGUF header fingerprint also equals the frozen fingerprint:

| Candidate | Observed bytes | Observed sha256 | Fingerprint | Identity |
|---|---|---|---|---|
| M-14B-QWEN | 8,988,110,976 | `e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008` | qwen2 / tensor 579 / file_type 15 | **PASS** |
| M-8B-LLAMA | 4,920,739,232 | `7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c` | llama / tensor 292 / file_type 15 | **PASS** |

`n_download_attempts = 1` for both. The parent’s metadata-vs-body mismatch did **not** recur.

### 3.3 Controls

| Control | Expected | Observed | Verdict |
|---|---|---|---|
| `PC-ORACLE-EPISODE` | 5/5 task_success | 5/5, parse step1 = 1.0 | PASS |
| `NC-NO-MODEL-ACTION` | parse step1 = 0.0 AND tsr = 0.0 | 0.0 / 0.0 | PASS |
| `B-RANDOM-ACTION` | parse step1 = 1.0 AND tsr < 0.6 | 1.0 / 0.2 (1/5) | PASS |
| `PC-JSON-CONSTRAINED-DECODING` | 10/10 per cell | 10/10 both cells | PASS |

### 3.4 Capability ladder

| Metric | M-14B-QWEN | M-8B-LLAMA | Bar |
|---|---|---|---|
| `positive_control_pass_rate` | 1.0 (10/10) | 1.0 (10/10) | 1.0 |
| `parseable_action_rate_step1` | 1.0 (5/5) | 1.0 (5/5) | ≥ 0.6 |
| `answer_action_emission_rate` | 0.0 (0/5) | 0.0 (0/5) | — |
| **`task_success_rate`** | **0.0 (0/5)** | **0.0 (0/5)** | **≥ 0.6** |
| cell state | COMPLETE | COMPLETE | — |
| CLEARS | no | no | — |
| load_time_s | 0.543 | 15.1 | — |
| max RSS | ~9.4 GB | ~5.2 GB | — |
| mean inference latency | 12.535 s/call (n=35) | 5.726 s/call (n=35) | — |
| mean completion tokens | 15.0 | 10.57 | — |

**Behavioural trace (identical shape in every one of the 10 episodes):** the model emits
`{"action":"click","selector":"#reveal-btn"}` at step 0 (the button click succeeds; `TARGET-42` is
revealed and `PAGE_TEXT` then contains it), then keeps clicking `#reveal-btn` for the remaining four
steps (`click_ok=false` after the first, since the button is hidden) and never emits a terminal
`answer` action. `clicked_reveal=true` and `revealed_value="TARGET-42"` in all episodes;
`final_answer=null` in all episodes.

### 3.5 Endpoint census (non-gating)

`raw/endpoint_census.json.counts`: `PROVISIONABLE_CREDENTIATED = 0`, `CREDENTIAL_REQUIRED = 10`,
`CREDENTIAL_FREE_OPERATIONALLY_CAPPED = 1`, `UNREACHABLE = 1`. No credential environment variable
was present. The one reachable credential-free path, Pollinations, is operationally capped.

### 3.6 External comparators (non-gating, `CANDIDATE_NOT_EVIDENCE`)

`raw/external_comparators.json`: 3/3 entries enumerated with pinned primary sources, 0 unhpin­nable.
No external vendor number is reproduced or used as evidence.

---

## 4. Derived measurement

Applying the frozen decision rule (`raw/decision.json.trace`):

```
rule1_preflight_pass
rule2_endpoint_census_recorded_non_gating:providers=12 provisionable_credentialed=0
rule3c_complete:M-14B-QWEN tsr=0.0 parse=1.0 clears=False
rule3e_fails_bar:M-14B-QWEN=TREATMENT_FAILS_BAR
rule3c_complete:M-8B-LLAMA tsr=0.0 parse=1.0 clears=False
rule3e_fails_bar:M-8B-LLAMA=TREATMENT_FAILS_BAR
rule4_complete_cells_no_clear->FALSIFIES b3=NOT_SATISFIED
```

- No candidate CLEARS; both COMPLETE cells fail the bar → `measured` is non-empty.
- Every predeclared hosted provider is `CREDENTIAL_REQUIRED` / `UNREACHABLE` /
  `CREDENTIAL_FREE_OPERATIONALLY_CAPPED` → `B3_STATUS = NOT_SATISFIED`.
- Therefore `OUTCOME = FALSIFIES`, canonical mapping `result.status = COMPLETE`.

---

## 5. Interpretation (bounded)

The corrected substrate executed cleanly and produced a **valid scientific negative**: neither
predeclared credential-free candidate clears the frozen minimal multi-step Web-agent bar, and no
currently-provisionable credential-free same-protocol endpoint (local or hosted) can drive the test,
so readiness condition (3) / blocker B3 is **NOT_SATISFIED**.

The failure is **not** a decoding failure — constrained decoding is live (`PC 10/10`, step-1 parse
5/5). It is a **control/behavioural** failure under the frozen simplified observation: both classes
perform the reveal and then loop on the hidden reveal button instead of emitting the answer they can
see in `PAGE_TEXT`. This reproduces, at 14B Qwen and at a non-Qwen 8B family, the same failure mode
carried from the 3B–8B Qwen anchors.

The recorded exact blocker per hosted provider (missing credential env var / unreachable endpoint)
and the bounded comparator-readiness table are the decision inputs for the Global Research Director;
this packet does not pre-decide the re-scope.

**This FALSIFIES is bounded** to the predeclared credential-free local Q4_K_M classes tested
(Qwen2.5-14B, Llama-3.1-8B) plus the carried Qwen 3B–8B anchors and the recorded non-provisionable
hosted census. It does **not** globally reject `C-LLM-INHERIT`, does **not** close hosted frontier
classes (blocked, not tested), and says nothing about other quantisations, tasks or domains.

---

## 6. Consequences (both directions, as predeclared)

- **Positive branch (`SUPPORTS`), not taken:** a clearing credential-free candidate would make B3
  satisfiable with a factory-provisionable local endpoint and unblock the gated four-arm benchmark at
  that class (subject to B1 shipped carrier and B2 non-ceiling task bank, owned by Product/Runtime).
- **Negative branch (`FALSIFIES`, taken):** readiness condition (3) is NOT_SATISFIED. The Director
  owns the re-scope: obtain a hosted credential (pinning/SLA), or drop Gate 3’s same-model external
  published-baseline anchor in favour of internally re-run comparators on a dynamic-range task bank,
  or provision a different model class.

No claim is promoted or weakened by this transaction; `C-LLM-INHERIT` keeps its prior effective
status pending DIRECTOR adjudication.

---

## 7. Validity threats and limitations

See `result.json.validity_notes` for the full list. Key points:

- **Representation loss (inherited):** text observation (`PAGE_TEXT` 300 chars, `ELEMENTS`, `HISTORY`),
  not a full accessibility tree; after reveal, `ELEMENTS` still lists the hidden button. This packet
  changes only the model class, so it cannot separate raw control capacity from
  representation/affordance effects.
- **No variance estimate:** `temperature=0.0` + fixed seeds; `0.6` is a pre-declared adequacy rule,
  not a statistical threshold; n=5 per cell. `B-RANDOM-ACTION` analytic `P(tsr>=3/5) ≈ 1.15e-3`.
- **Scale vs family not separated:** both classes failed, so each result bounds its tested class; no
  interaction claim is made.
- **Census is observational**, not a capability test of credentialed providers.
- **External comparators are literature identities only** (`CANDIDATE_NOT_EVIDENCE`).
- **Residual grammar-admission risk** cannot manufacture a false SUPPORTS (a cell with parse step1
  < 0.6 cannot clear).

---

## 8. Provenance

`provenance.json` records the GitHub run id (`38212976602`, attempt 1), repo HEAD
`50bc0c511cdc81e8100857903d428d780328c930` (`lab2/intel`) and env `GITHUB_SHA`
`239c934b3c30e867bb221489ec10d0b570cbc690`, the frozen-input hashes, the freeze-artifact hash
verification, the prompt/overlay hashes, model pins and observed identity, the environment
(Python, llama-cpp-python 0.2.90, Playwright 1.63.0, `/usr/bin/google-chrome`, CPU/RAM) and the exact
executed commands.

Prior EXECUTE attempts failed with exit code 75 (agent model-pool exhaustion,
`model_execute.json` attempt 4 `transient-pool-exhausted`) before producing evidence; this
transaction ran the frozen design to completion.
