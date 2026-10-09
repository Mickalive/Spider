# EXECUTE Report: EXP-INTEL-37973264582

**Lane:** intel
**Claim:** C-LLM-INHERIT (HYPOTHESIS)
**Status:** COMPLETE
**Outcome:** FALSIFIES (frozen label: **DESIGN_COMPROMISED**)
**Frozen inputs:** request.json `455427c8…`, spec.json `36f1b4e8…`, prereg.md `98cf2603…` (unchanged; verified against freeze.json)

This packet answers the Director mandate's endpoint/comparator question and states, per mandate part (c), whether the finding changes the frozen four-arm design. It does **not** run the four-arm benchmark, does not implement comparators, and does not evaluate kernel execution (prereg.md §11).

---

## 1. Decision rule result

| Gate | Frozen test | Result |
|------|-------------|--------|
| **Gate 0** Endpoint attainability | ≥1 candidate produces a valid `PC-ENDPOINT-LIVE` receipt | **PASS** |
| **Gate 1** Comparator obtainability | ≥1 comparator obtainable + runnable under identical model/tools/budget + published numbers with denominators | **PASS** (framework reading) |
| **Gate 2** Four-arm viability | design executable with attained endpoint + comparators **without weakening** | **FAIL** |
| **Gate 3** Publication audit | ≥1 comparator's published numbers survive the 5-criterion audit | **FAIL (zero pass)** |

**Frozen outcome → DESIGN_COMPROMISED** ("Gates 0–1 PASS but Gate 2 FAIL; endpoint+comparators exist but the four-arm design requires weakening"). Gate 3 zero-pass corroborates.

The canonical `result.json` outcome enum has no `DESIGN_COMPROMISED`; because the frozen hypothesis H1 requires the design to *remain valid and executable* and that conjunct is not met, `outcome=FALSIFIES` is recorded, with the frozen label preserved in `metrics.frozen_outcome_label`.

---

## 2. Gate 0 — endpoint attainability (PASS)

Two credential-free endpoints produced valid, non-error completions with usage and response hashes:

- **E-LOCAL-LLAMA** — `llama-cpp-python 0.2.90`, `qwen2.5-0.5b-instruct-q4_k_m.gguf` (491,400,032 bytes, sha256 `74a4da8c…d7a9db`). Valid completion `SPIDER-PING`, usage 28/4/32 tokens, both in-process and through the OpenAI-compatible server at `127.0.0.1:8081/v1/chat/completions`. Fully offline and reproducible after the one-time GGUF download.
- **E-POLLINATIONS-OPENAI** — `https://text.pollinations.ai/openai`, no credential, anonymous tier, model resolved to **gpt-oss-20b** (`GET /models`). Returned HTTP 200 with usage and `user_tier: anonymous` (6/6 in the final probe).

Credential-required / invalid (recorded as provisioning receipts): OpenAI, Anthropic, Groq, Together, Cerebras, Replicate (401/403); `api-inference.huggingface.co` and `cdn-lfs.huggingface.co` unresolvable; Ollama binary absent; vLLM/TGI require a GPU (none). **`models.github.ai` is intercepted**: every path, including a bogus one, returns HTTP 200 `text/plain` body `OK` — it is not a model completion and was excluded.

`PC-ENDPOINT-LIVE` = **PASS**; `NC-NO-ENDPOINT` correctly does **not** hold. The two are mutually exclusive and collectively exhaustive over the tested set.

---

## 3. Gate 1 — comparator obtainability (PASS, with a documented limitation)

All 14 candidate packages were retrievable with `pip download --no-deps` (exit 0): `langchain`, `langchain-community`, `chromadb`, `faiss-cpu`, `llama-index`, `browser-use`, `langgraph`, `pyautogen`, `crewai`, `dspy-ai`, `letta`, `zep-python`, `playwright`, `stagehand-py`.

Runnability under the **same model endpoint** was demonstrated for the compiled-workflow category: a **LangGraph** graph executed against both credential-free endpoints and returned `SPIDER-PING` (local 0.144 s; proxy 3.793 s; identical output hash `507fea36…c90d777`). The browser tool substrate is present: **Playwright drove system Chrome** (chromium `154.0.8037.97`) to open a page and read title/text.

However, a **minimal Web-agent task** (click `#reveal-btn`, then answer `TARGET-42`) did **not** complete under either credential-free endpoint:

| Endpoint | Model | Steps | Result | Tokens |
|----------|-------|-------|--------|--------|
| E-LOCAL-LLAMA | qwen2.5-0.5b-instruct | 1 | emitted prose, no parseable JSON action | 150 |
| E-POLLINATIONS-OPENAI | gpt-oss-20b | 1 | empty content, reasoning-only, ~197-token completion cap despite `max_tokens=1200` | 197 |

The proxy also intermittently returned **HTTP 402 Payment Required**, and the OpenAI Python client received HTTP 400 ("unexpected tokens remaining in message header") for a request shape that equivalent raw HTTP accepted. It has no SLA and no model pinning.

Published comparator numbers with denominators exist (retrieval/workflow/memory; see §4), which is why Gate 1 passes under the obtainability reading. Under a stricter reading of "runnable under identical model/tools/budget" as *a completed Web-agent task*, Gate 1 would instead FAIL → `UNRESOLVABLE_COMPARATOR`. Both readings converge on **not VIABLE**; the discrepancy is recorded in `unresolved[0]`.

---

## 4. Gate 2/3 — why the design requires weakening (FAIL)

**Gate 2.** The only fully offline, reproducible credential-free endpoint (local Qwen2.5-0.5B) cannot act as a Web agent; the only stronger credential-free endpoint (anonymous gpt-oss-20b) is unstable, token-capped, and unpinned. Running the four arms under the frozen same-model/tools/budget constraint therefore requires substituting a different/stronger model or a differently provisioned endpoint — a material weakening. The exact compromises are recorded in `raw/gate_evaluation.json:gate_2_four_arm_viability.required_compromises`.

**Gate 3 (publication audit).** No comparator's published numbers survive the same-model/tools/budget audit:

| Comparator | Published number (source, external landscape evidence) | Model family | Audit |
|------------|--------------------------------------------------------|--------------|-------|
| B-RETRIEVAL | LRAT, +27% task success | 4B–358B backbones | UNAUDITED (different model; no token budget) |
| B-SELECTOR-CACHE | browser-use, WebVoyager 89.1% (586 tasks) | gpt-4o | UNAUDITED (different model; no token budget) |
| B-COMPILED-WORKFLOW | AWM/ASI/ReasoningBank, WebArena SR + tokens/task | Gemini 3 Flash / GPT-5.4-mini / Qwen 3.6-27B | UNAUDITED (different model) |
| B-MEMORY-AGENT | Letta, LoCoMo 74.0% (10 conv / 1,540 QA) | gpt-4o-mini, filesystem tools (no browser) | UNAUDITED (different model, non-Web task, no token budget) |

**Zero comparators pass the audit.** No comparator publishes Web-agent success/cost numbers on Qwen2.5-0.5B-Instruct, gpt-oss-20b, or any credential-free endpoint model. The selector/action-cache category has no success/cost benchmark with denominators under any model. Consequently the externally auditable baseline the frozen design requires does not exist.

Per mandate part (c): **yes, the finding changes the frozen four-arm design** — the same-model/tools/budget requirement, paired with a published-baseline audit, is unsatisfiable on current assets until either (i) a stable credential-free endpoint able to drive a Web agent is provisioned, or (ii) the design is re-scoped to internally re-run comparators without an external published anchor.

---

## 5. Controls

- `PC-ENDPOINT-LIVE` — **PASS** (two valid receipts).
- `NC-NO-ENDPOINT` — **does not hold** (mutually exclusive with PC).
- `B-COLD`, `B-INSTRUCTIONS` — internal arms; not run in scope (obtainability/test only).
- `B-RETRIEVAL`, `B-COMPILED-WORKFLOW` — obtainable/partially runnable; Gate 3 UNAUDITED.
- `B-SELECTOR-CACHE`, `B-MEMORY-AGENT` — obtainable but Gate 3 UNAUDITED (no same-model number / no token budget).

## 6. Consequence

C-LLM-INHERIT remains **HYPOTHESIS**. The frozen four-arm benchmark is **not executable as specified on current assets**: the endpoint gap is partly closed (two credential-free endpoints exist), but the same-model published-baseline anchor and a budget-stable Web-agent-capable credential-free model do not. The next step is a Director/prereg decision: provision a stable endpoint or re-scope the design, and note the contradiction with accepted codex evidence (EXP-PRODUCT-37950607128) which treats the four-arm benchmark as executable "pending a model credential" (see `unresolved[4]`). Intel's external-baseline search thread is bounded by this result.

## 7. Validity threats

- Comparator numbers are external landscape evidence, not independently reproduced.
- The minimal Web-agent failure uses one synthetic page, one prompt, one parser; a better harness could raise the local action rate.
- The pollinations proxy is unstable and unpinned; receipts are timestamp-bound.
- No WebArena/WebVoyager task population was provisioned.
- Scope excludes SPIDER kernel execution and the four-arm benchmark itself.

Full detail: `raw/endpoint_receipts.json`, `raw/comparator_obtainability.json`, `raw/gate_evaluation.json`, `raw/provisioning_receipts.json`, and `provenance.json`.
