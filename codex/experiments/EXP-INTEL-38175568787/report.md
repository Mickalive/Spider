# EXP-INTEL-38175568787 — EXECUTE report

**Lane:** intel · **Claim:** `C-LLM-INHERIT` · **Status:** `MEASUREMENT_INVALID` · **Outcome:** `INCONCLUSIVE` · **B3_STATUS:** `UNRESOLVED`

Frozen experiment: a two-candidate capability ladder (`M-14B-QWEN` primary, `M-8B-LLAMA` secondary) under the audited single-factor minimal Web-agent protocol, plus an independent 12-provider hosted-endpoint census and a 3-entry external-comparator readiness table. All frozen inputs (`request.json`, `spec.json`, `prereg.md`, `design_review.json`) and all three `freeze.json` artifact hashes were re-verified on disk and match.

This transaction is a **measurement failure (substrate/provisioning)**, not a scientific negative. No model was loaded and no capability was observed. No claim was promoted, weakened or falsified.

## 1. Question and decision rule

The frozen rule (`spec.json#decision_rule`) is: step 1 PREFLIGHT once; step 2 endpoint census (non-gating); step 3 capability ladder over `[M-14B-QWEN, M-8B-LLAMA]`, where step **3a** byte-verifies each candidate's pinned GGUF sha256+bytes and records `UNMEASURED_LOAD_FAILED` on any mismatch **without loading**; step **3d** requires `COMPLETE` and a clearing bar (`task_success_rate ≥ 0.6` and `parseable_action_rate_step1 ≥ 0.6`) to `SUPPORT`; step **4** maps the post-ladder state: no `COMPLETE` cell ⇒ `MEASUREMENT_INVALID` / `B3_STATUS=UNRESOLVED`; else `FALSIFIES`. Canonical packet mapping: `MEASUREMENT_INVALID → status=MEASUREMENT_INVALID, outcome=INCONCLUSIVE`.

## 2. Measurement validity / controls

Step 1 PREFLIGHT **PASSED** all five frozen checks through the real frozen scorer and a served page:

| Control | Expected | Observed | Verdict |
|---|---|---|---|
| `PC-ORACLE-EPISODE` | 5/5 `task_success=true` | 5/5 `task_success=true` (identical episode records to the audited parent; `raw/controls.json` sha256 `b0120e61…`) | PASS |
| `NC-NO-MODEL-ACTION` | parseable 0.0, success 0.0 | parseable 0.0, success 0.0 | PASS |
| `B-RANDOM-ACTION` | parseable 1.0, success < 0.6 | parseable 1.0, success 0.2 | PASS |
| freeze artifact hashes | all match | 3/3 match | PASS |
| required stack imports | OK | `llama_cpp`, `playwright`, frozen producer symbols present | PASS |

The per-candidate `PC-JSON-CONSTRAINED-DECODING` 10-probe gate (the other member of `PC-SUITE-EXP-INTEL-38175568787`) is `NOT_APPLICABLE` here because no candidate reached the load/episode stage; the parent's carried 10/10 is recorded as context only and is not treated as this experiment's evidence. Carried baselines (`B-UNDERSPECIFIED-PROMPT-7B`, `B-0.5B-QWEN-LOCAL`, `B-POLLINATIONS-PROXY`) are `CARRIED_NOT_RERUN` and did not influence the decision.

## 3. Results — the ladder failed at step 3a

Both candidates matched the frozen **byte counts** but **not** the frozen **sha256**, so per frozen rule 3a each was recorded `UNMEASURED_LOAD_FAILED` and **no model was loaded**:

| Candidate | Pinned sha256 / bytes | Downloaded sha256 / bytes | Match |
|---|---|---|---|
| `M-14B-QWEN` | `d989c91d…` / 8 988 110 976 | `e47ad95d…` / 8 988 110 976 | **no** |
| `M-8B-LLAMA` | `85450612…` / 4 920 739 232 | `7b064f58…` / 4 920 739 232 | **no** |

Ladder outcome: 0 `COMPLETE` cells. Frozen rule 4, no-`COMPLETE` branch → `OUTCOME=MEASUREMENT_INVALID`, `B3_STATUS=UNRESOLVED`, STOP.

### Root cause of the digest mismatch (raw evidence fully preserved)

The frozen pins are not corrupted and the downloads are not corrupted. HF's own metadata and CDN expose **two different hashes for the same file**, and the frozen pin selected one of them:

- HF tree API: `lfs.oid = e47ad95d…` (resp. `7b064f58…`) — and this equals the sha256 of the bytes actually served;
- HF tree API: `xetHash = d989c91d…` (resp. `85450612…`) — and this equals the frozen pin;
- CDN `HEAD`: the redirect path segment and the `etag` header both carry the **pinned** xet hash, while the response **body** hashes to the `lfs.oid`.

The frozen spec note states *"sha256 equals the HF LFS OID (CDN etag)"*; the evidence shows that claim **conflated** the `xetHash`/CDN-`etag` with the `lfs.oid`. The design-time pin was therefore taken from HF server **metadata**, not from downloaded bytes (or the served body changed between design and execute). Three independent routes (plain `resolve`, `?download=true`, `hf.co`) produced identical body hashes and byte counts, so the served content is stable and authentic and the frozen byte-level identity is unsatisfiable against it.

### Endpoint census (step 2, non-gating)

12 providers: `PROVISIONABLE_CREDENTIATED=0`, `CREDENTIAL_REQUIRED=10` (OpenAI 401, Anthropic 401, Google Gemini 403, Mistral 401, Groq 401, Together 401, OpenRouter 200, DeepSeek 401, Fireworks 401, Cohere 401), `CREDENTIAL_FREE_OPERATIONALLY_CAPPED=1` (Pollinations, HTTP 200), `UNREACHABLE=1` (HuggingFace Inference). `any_provisionable_credentialed=false`. No provider model was invoked (reachability/credential check only).

### External comparator readiness table (non-gating)

3/3 entries enumerated and 3/3 primary sources pinned, all labelled `CANDIDATE_NOT_EVIDENCE`: QCR (`arXiv:2608.12847`), Agentic Compilation (`arXiv:2604.09718`), site-memory/ColorBrowserAgent (`arXiv:2601.07262`). Reported numbers are recorded with denominators and reproduction prerequisites; none is used in the decision.

## 4. Interpretation (bounded)

1. The frozen test of whether a 14B-class or a non-Qwen 8B-class model clears the minimal Web-agent bar under the frozen protocol **was not run**, because the frozen substrate could not be obtained in its frozen byte identity. The result says nothing about the capability of these model classes.
2. The finding that **is** established at the operational level is a freeze-process failure mode: an HF GGUF digest pinned from server metadata (`etag`/`xetHash`) can differ from the sha256 of the served bytes (`lfs.oid`) while byte counts match, silently defeating a byte-identity gate. This is an operational diagnostic, not a capability result, and it is not promoted to a claim.
3. This is explicitly **not** `FALSIFIES` and not a downgrade of `C-LLM-INHERIT`; its inherited Codex effective event remains the parent's `FALSIFIES`.

## 5. Smallest unblocking action

Re-pin each candidate to the byte-level sha256 actually served (verified by full download) and re-freeze — keeping the same candidate identities (model, quant, `chat_format`, URL) and correcting only the digest/bytes binding; or vendor the exact GGUF bytes keyed by byte sha256; or, at DESIGN time, compute candidate digests from downloaded bytes rather than from HF server metadata. Downstream experiments pinning HF GGUFs should byte-verify at freeze.

## 6. Cost

One PREFLIGHT pass (oracle 5 + null 5 + random 5 episodes through the real scorer, plus a live served page and Chrome), a 12-provider unauthenticated reachability sweep, a 3-entry comparator fetch, and two GGUF downloads (≈13.9 GB total, multiple routes for the 14B). **Zero** candidate model inferences. No hosted-provider inference. Runtime dominated by GGUF downloads and the single preflight browser batch.

## 7. Artifacts and provenance

Raw evidence (immutable): `raw/preflight.json`, `raw/controls.json`, `raw/materialized_configs.json`, `raw/endpoint_census.json`, `raw/external_comparators.json`, `raw/provisioning_evidence.json`, `raw/decision.json`, and `cells/*/raw/{harness_config.json,provisioning_receipt.json}`. Derived: `raw/decision.json`. Authored code: `research/intel/exp_38175568787_{materialize,controls,census,comparators,provision,eval}.py`. Frozen runner `research/intel/run_exp_37982024058.py` was import-checked but not invoked for candidates. Full hashes, commands, environment and frozen-input verification are in `provenance.json`.

## 8. Unresolved

Whether the frozen pin was wrong at DESIGN time (metadata-only read) or became stale between design (`2026-10-11`) and execute (`2026-10-12`); whether the origin bytes matching the frozen pins remain retrievable anywhere; the capability of the `M-14B-QWEN` and `M-8B-LLAMA` classes under the frozen protocol (entirely unmeasured); and whether the HF Xet-bridge metadata/body mismatch affects pinned GGUFs used by other lanes (not surveyed here).
