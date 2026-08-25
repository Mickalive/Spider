# PB-001 INTERFACES — Frozen module contracts for the Builder — v2

Beta: **PB-001** · These interfaces are frozen at architect time (2026-08-25, v2). The Builder
implements them; semantic changes require a prereg amendment BEFORE any outcome (disclosed).
v2 delta vs v1: new §3bis contracts for the vendored SGDR fusion stack (`hash_embed`,
`state_summarizer`, `frag_describe`, `fusion_scorer`); §3 goalsig restated as eligibility GATE;
§8.3 row schema gains descriptive retrieval-internals fields. Everything else unchanged.
All paths relative to `product-beta/PB-001/`. Python 3.11+, Playwright/Chromium (vendored
`shared/browser.py` lineage).

---

## 1. `spider_mem/store.py` — MemoryStore (vendored, G-H1) — unchanged

Reuse `graph/store.py` @ lab/graph `d41fe9bfdfc41176cd0dd9607db29dbff0ced9ec` verbatim semantics:
tables `sites/states/actions/transitions/fragments/runs`; `target_sig()` canonical signatures;
`fingerprint()` structural identity; `save_fragment()` with explicit column mapping +
`_assert_fragment_invariants()`; `confidence()` engineering score (UNCALIBRATED — must never be
presented as calibrated).

Additional beta-only methods (additive only, no semantic change):

```python
class Store:
    # ... vendored API unchanged ...
    def all_fragments(self, site: str | None = None) -> list[dict]:
        """[{id, site, goal_sig, steps:[{kind,target_sig,value?}], success_count,
            failure_count, created, last_validated}] — retrieval input."""

    def dump(self) -> dict:
        """Full JSON-serializable KB extract (all tables)."""
```

## 2. `spider_mem/kbfile.py` — KB byte-restore and hashing — unchanged

```python
def kb_sha256(path: str) -> str
def snapshot_kb(src_db: str, dst_path: str) -> str          # returns sha256
def restore_kb(frozen_copy: str, dst_db: str) -> str        # byte-exact copy + wal checkpoint; returns sha256
def assert_write_suppressed(h_before: str, h_after: str) -> None   # raises WriteSuppressionError
def counts(db_path: str) -> dict   # {states, transitions, actions, fragments} for row records
```

Contract: every evaluation row begins with `restore_kb` and ends with
`assert_write_suppressed`. A violation aborts the batch as MEASUREMENT_INVALID.

## 3. `spider_mem/goalsig.py` — blind content addressing — v2 ROLE: ELIGIBILITY GATE ONLY

Constants frozen: `SEED=20260824 TAU=0.30 MIN_MATCH=2 TOPK=3 DF_KEEP=0.6 MIN_SITE_FRAGS=3
COV_CAP=6`. Functions reused verbatim: `tokenize`, `slug_tokens`, `describe_steps`,
`url_title_tokens`, `matched_pairs`, `coverage`, `prune_boilerplate`.

**v2 change of role (not of code)**: the goalsig scorer decides ONLY candidate ELIGIBILITY
(OK|UNKNOWN): a fragment is gate-passing iff `matched_pairs >= MIN_MATCH AND coverage >= TAU`
under DF-pruning/COV_CAP, exactly as in v1. It no longer determines ordering; ranking among
gate-passers is `fusion_scorer`'s job (§3bis). TOPK=3 remains the number of candidates returned.
Threshold constants are UNTOUCHED (prereg §0 delta).

```python
@dataclass
class FragmentCandidate:
    fragment_id: int
    site: str
    description_text: str        # v2: C16 mechanical description (rendering + embedding input)
    description_tokens_used: list[str]
    coverage: float
    matched: int
    fused_score: float           # v2: populated by fusion_scorer after ranking
    steps: list[dict]            # executable primitive steps
    kind: str                    # "procedure" | "pager" | "single"
    provenance: dict             # success_count, failure_count, last_validated, confidence

def gate_candidates(query_text: str, fragments: list[dict], site: str | None,
                    equipment: Literal["v31", "legacy_v00"] = "v31",
                    seed: int = goalsig.SEED) -> GateResult:
    """Applies V31 descriptor + symmetric closed-class canonicalization when equipment="v31"
    (preprocessing only), then the FROZEN eligibility gates.
    Returns {status: "OK"|"UNKNOWN", passing: [fragment_rows], query_tokens,
             timings_ms_perf: float}. UNKNOWN ⇔ zero candidates clear thresholds.
    NO goal_sig lookup path exists in this module (blind discipline asserted by test)."""
```

V31 equipment (`equipment_v31.py`) extracted from `graph/score_variants.py` @ `d41fe9b` winning
arm (descriptor `d3_pagelist`: page-anchor + depth-digit ⇒ pagination-affordance token;
canonicalization `q1_canon`: symmetric closed synonym classes GO/NEXT/CAT/LIST/AUTH/HOME applied to
BOTH query and descriptor sides). Thresholds untouched. Regression fixture unchanged: offline
scoring of the committed G-H4 fresh-set paraphrases must reproduce the committed confirm-scores
verdict pattern (6/8 positives, 0/2 false accepts for V31 vs 3/8 baseline) using the committed
cycle-3 KB dump as inert test fixture. **No quantitative V31 claim may be quoted in beta outputs.**

## 3bis. Vendored SGDR fusion stack — NEW in v2 (the directed change)

All four modules vendor from `intel/experiments/sgdr_repro/` @ lab/intel
`fca0acbc0aa56af2ad2e83538661b5dc86644c5d` (audit gate CYCLE_32800296360: PASS /
VALIDATED_USEFUL / PROOF_OF_CONCEPT ceiling). Clean-room lineage only; NEVER copy CC BY-SA
reference source. Numeric behavior must be preserved EXACTLY (fixture WP-0 proves it).

### 3bis.1 `spider_mem/hash_embed.py` (vendored `embedder.py`, verbatim)

```python
DIM = 512
def tokenize(text: str) -> list[str]          # [a-z0-9']+ over lowered text
def embed(text: str) -> dict[int, float]      # sparse L2-normalized vector;
                                              # word unigrams + adjacent bigrams;
                                              # sublinear tf (1+ln c); sha1-bucketed features
def cosine(a: dict, b: dict) -> float         # sparse dot product
```

Determinism: sha1 bucketing only — PYTHONHASHSEED-independent (constitution §30). Unit test:
identical outputs across `PYTHONHASHSEED={0,1,random}`; known-value cosine fixtures committed.

### 3bis.2 `spider_mem/state_summarizer.py` (vendored `summarizer.py`, verbatim)

```python
MAX_VERBS = 15
def cache_key(snap: dict) -> str              # sha256 over url_shape/title/element sigs/forms
def summarize(snap: dict, cache: dict | None = None,
              stats: dict | None = None) -> tuple[str, str, Literal["hit","miss","fallback"]]
```

Contract-faithful operational summary: page kind (login form | link listing page | content detail
page | general page; frozen first-match rules), title, url_shape, ≤15 enabled-action verb phrases
("open '…'", "type into '…'", "type password", "tick '…'", "choose '…'"). Deterministic URL/title
stub fallback on failure. Verb vocabulary is SHARED with frag_describe by construction (audited
property; do not alter either side). `stats` accumulates {hits, misses, fallbacks}; misses count
would-be LLM calls DESCRIPTIVELY ONLY — they are never billed into `llm_calls` or token totals
(fairness floor: provider accounting exclusively).

### 3bis.3 `spider_mem/frag_describe.py` (vendored `descriptions.py`, verbatim)

```python
def humanize_sig(sig: str) -> str
def describe_fragment(frag_row: dict) -> str
#   => f"On {site} ({humanize_sig}): open 'x'; type 'y' into field; ..." per frozen verb map
```

The single description channel for BOTH rendering (memory block text shown to the planner LLM) and
embedding (fusion score input). Store-derived tokens inside descriptions are NOT lookup keys; blind
discipline is asserted by test (no equality path from goal text to goal_sig anywhere in the
consumer).

### 3bis.4 `spider_mem/fusion_scorer.py` (adapted `retriever.py`) — THE changed component

```python
TOP_K = 3                     # = goalsig.TOPK
MMR_LAMBDA = 0.7
ALPHA = 0.4                   # directed value (audited C_a04)
TOP_M = max(3 * TOP_K, 20)    # = 20, reference formula

@dataclass
class FusionResult:
    status: Literal["OK", "UNKNOWN"]      # inherited verbatim from the goalsig gate
    candidates: list[FragmentCandidate]   # ranked, len <= TOP_K, fused_score populated
    diagnostics: dict   # {n_gate_pass, pool_size, alpha_used, mmr_lambda_used,
                        #  summary_status, selected_scores:[float], summary_stats:{...}}

def retrieve_fused(goal_text: str, state_snapshot: dict, gate_passing: list[dict],
                   summary_cache: dict, summary_stats: dict,
                   seed: int = 20260824) -> FusionResult:
    """Ranks gate-passing fragments by the audited fused score:
       rel(f) = ALPHA*cos(E(goal_text), E(desc_f))
              + (1-ALPHA)*cos(E(summarizer(state_snapshot)), E(desc_f))
       Pool = gate_passing sorted by (-rel, id), truncated to TOP_M;
       greedy MMR (lambda=MMR_LAMBDA) selects min(TOP_K, len(pool)); ties break to LOWER id.
    Preconditions: gate_passing non-empty (caller returns UNKNOWN otherwise);
    descriptions via frag_describe.describe_fragment ONLY; embeddings cached per bank load."""
```

Adaptation rules (exhaustive): strip conditions A_native/A_free_text/B_plain/B_mmr/C_a05/D_random
and their machinery; keep `FragmentBank` embed-cache pattern, `rel_fused` formula, `mmr_rerank`
ordering semantics (sort key `(-rel, -id)` internally ⇒ tie→lower id), and site scoping via the
vendored `site_key()` normalization (netloc-style rows vs short runtime keys). Any other change is
FORBIDDEN without a prereg amendment. Fixture (WP-0): offline recomputation over the COMMITTED
cycle-1 artifacts (`results/intel/reproductions/cycle1/*` + vendored `stimuli.py` bank inputs)
must reproduce hard@1 {B_plain 25/74, B_mmr 25/74, C_a04 36/74} and pairwise C-vs-B 11 wins / 0
reversals EXACTLY; mismatch ⇒ BLOCKED (never approximate). These fixture numbers are reproduction-
integrity targets INSIDE WP-0 only; quoting them as product performance claims is forbidden
(Intel wording constraints travel; PoC tier; no GENERALIZATION language).

Cost accounting contract: summarize/embed/MMR run harness-side; wall-clock lands in SPIDER
`stage_ms_perf.retrieval`; ZERO provider calls issued; would-be-miss counters descriptive only.

## 4. `spider_mem/accept.py` — anchored predicates (vendored, G-H3 E4) — unchanged

`norm_path`, `url_matches_anchor` verbatim. Task predicates are data (§8 registry schema); the
evaluator is harness-side:

```python
def evaluate_predicate(pred: dict, final_snap: dict, nav_chain: list[str]) -> PredicateEval:
    """Checks host allowlist, url_anchor(s) via url_matches_anchor, required element/text anchors
    on final snapshot, neg_url substring rejections, AND nav-chain integrity (final URL reachable
    through recorded navigation history). Returns {passed: bool, checks: [{name, ok, detail}]}.
    Harness-judged ONLY."""
```

## 5. `runtime/session.py` — browser observation/action surface (vendored shared/browser.py) — unchanged

Unchanged public surface: `Session(headless=True)` with `.goto(url, site) -> snap`,
`.snapshot(site, settle_ms=350) -> snap`, `.act(snap, action) -> post_snap`, `.close()`.
Health floors: `dom_bytes ≥ 2000`, `len(elements) ≥ 5` → else `HealthGateError`. Snapshots carry
`elements[]` (index-addressable), `forms[]`, `page_text`, `url`, `url_shape`, `dom_sha256`,
`dom_bytes`. Row init MUST use a fresh incognito context (cookies/storage empty). Snapshot shape is
directly consumable by `state_summarizer` (elements/forms/url/title/url_shape keys present).

## 6. `runtime/react.py` — frozen reference ReAct loop (new, hash-pinned) — unchanged

```python
class ReactAgent:
    def __init__(self, llm: LLMAdapter, session: Session, budgets: Budgets,
                 obs_serializer: ObsSerializer, logger: EventLogger): ...
    def run(self, task: TaskView) -> RunRecord:
        """Observe→decide→act loop until done-action / budget exhausted. The agent NEVER sees the
        predicate result; it may stop via done(reason). Termination: MAX_STEPS=30 actions,
        MAX_LLM_CALLS=60, WALL_S=600s, MAX_ROW_TOKENS=200_000."""
```

- Observation format (identical all arms): numbered interactive-element list rendered from the
  snapshot (`i, tag, type, role, name, aria, placeholder, text, href-path`), current URL, page
  title, ≤600 tokens of page_text head.
- Action schema (JSON mode): `{"action": "click"|"fill"|"select"|"press"|"goto"|"wait"|"done",
  "element": <int>, "value": "<str>", "thought": "<str>"}` mapped onto Session primitives
  (`fill` requires target element; `select` value=label; `press` value=key name; `goto` value=URL).
- Malformed model output: 1 structured-repair attempt, then counted as a failed call and the step
  retried once; both calls billed to the arm's totals.

## 7. `runtime/llm.py` — provider adapter contract (new) — unchanged

```python
class LLMAdapter(Protocol):
    model_id: str                      # pinned at F1, identical across arms
    def chat(self, messages: list[dict], *, temperature: float = 0.0,
             max_tokens: int = 700, json_schema: dict | None = None,
             seed: int | None = 20260825) -> LLMResponse

@dataclass
class LLMResponse:
    text: str
    usage_prompt_tokens: int           # MANDATORY from provider usage fields
    usage_completion_tokens: int       # MANDATORY; no estimate allowed
    latency_ms_perf: float             # perf_counter
    raw_call_index: int                # links to event log entry
```

Policy: temperature=0 everywhere; provider seed passed when supported (recorded either way);
1 retry on transport/5xx errors (both attempts logged+billed); no caching of responses across arms
or rows. If no authenticated endpoint exists in the build environment ⇒ build status BLOCKED with
reason `no_backbone_available` (never fabricate accounting).

## 8. Harness contracts

### 8.1 Panel file `harness/panel.json` (frozen at F1) — unchanged

```json
{
  "seed_schedule": 20260825,
  "passes": 2,
  "tasks": [{
     "task_id": "E_R1_auth_quotes",
     "regime": "R1",
     "site": "quotes",
     "start_url": "https://quotes.toscrape.com/",
     "goal_text": "...authored independently, committed at F1...",
     "fills": [{"field_hint": "username", "value_env": "PB_QUOTES_USER"},
               {"field_hint": "password", "value_env": "PB_QUOTES_PASS"}],
     "predicate": {"host_allowlist": ["quotes.toscrape.com"],
                    "elem_text_any": ["logout"],
                    "url_anchor": null},
     "subgoal_anchors": [...]
  }],
  "reserve_pool": [...],
  "pilot_smoke": [...],
  "b2_sanity_routes": [...]
}
```

Credentials resolve from environment at run time; values appear in event logs REDACTED except
inside `fill` action values needed for replay audit (demo-site practice credentials are already
public in repo history; disclosure stands).

### 8.2 Row lifecycle `harness/driver.py`

```python
def run_row(task, arm, pass_idx, frozen_kb_copy, llm, schedule_rng) -> RowRecord
```

Order: seeded interleave (arm round-robin within pass; pass2 order reversed; sites alternating);
KB restore → health gate → execute → harness-judged outcome → write-suppression assert →
artifacts. INFRA rerun: max 1 per cell, only on HEALTH_TRIP/provider-outage classes; original row
preserved with `rerun_of`; >10% infra-rerun rate ⇒ batch MEASUREMENT_INVALID.

### 8.3 Row record schema (JSONL `results/product-beta/PB-001/raw_rows.jsonl`) — v2 adds fields marked

```json
{
  "row_id": "P02-E_R2_pag_books_7-pass1",
  "arm": "SPIDER|B0|B1", "task_id": "...", "regime": "R1|R2|R3", "pass": 1,
  "status": "SUCCESS|FAILURE|TIMEOUT|INFRA_EXCLUDED|RERUN",
  "predicate_eval": {"passed": true, "checks": []},
  "fabrication_violations": [],
  "counters": {"browser_actions": 0, "novel_actions": 0, "reused_actions": 0,
               "loads": 0, "llm_calls": 0},
  "tokens": {"prompt": 0, "completion": 0},
  "wall_ms_perf": 0.0,
  "stage_ms_perf": {"retrieval": 0.0, "llm": 0.0, "browser": 0.0},
  "action_mix": {"memory_procedure": 0, "memory_guided": 0, "exploration": 0},
  "memory_events": [{"subgoal": "", "event": "retrieved|applied|verified|reset|unknown|
                      false_accept|fallback_explore", "candidates": 0}],
  "fused_retrieval_diagnostics": {
      "n_gate_pass": 0, "pool_size": 0, "alpha_used": 0.4, "mmr_lambda_used": 0.7,
      "selected_scores": [], "summary_status": "hit|miss|fallback|null",
      "summary_stats": {"hits": 0, "misses": 0, "fallbacks": 0}
  },
  "first_failure_class": "null|RETRIEVER_MISS|RETRIEVER_FALSE_ACCEPT|PLANNER_MISPLAN|
                          PROCEDURE_EXEC_FAIL|PRECONDITION_MISMATCH|VERIFY_FAIL|
                          RESET_EXHAUSTED|EXPLORE_BUDGET_EXHAUSTED|PROVIDER_ERROR|HEALTH_TRIP",
  "kb_sha256_before": "...", "kb_sha256_after": "...",
  "health": {"http_probes": {}, "dom_floor_ok": true},
  "env": {"model_id": "...", "temperature": 0, "code_version": "..."}
}
```

(`fused_retrieval_diagnostics` present on SPIDER rows only; null elsewhere. Descriptive only —
no win-rule clause reads it.)

Per-event JSONL (`events/<row_id>.jsonl`): every LLM call (messages hash, usage, latency), every
action (kind, target index/sig, ok/error, pre/post URL), every memory event, with
`perf_counter_ns` timestamps. Enough to recompute all counters independently (auditor duty).

### 8.4 Manifest `results/product-beta/PB-001/MANIFEST.json` (freeze artifact)

F1 section: env record (python/playwright versions, OS, model id/version, endpoint family),
dependency lockfile hashes, vendored-file sha256 table (Graph `d41fe9b` + Intel `fca0acb`
lineages), panel.json+paraphrases sha256, prompt template hashes, seeds. F2 section: KB dump
sha256 + counts, B1 corpus sha256, route-absence records, B2 sanity results, analysis-code hash,
freeze UTC timestamps. Commit order enforced: F1 before Phase A; F2 before Phase B; outcomes begin
only after the F2 commit.

## 9. Arm adapters (`arms/`) — unchanged

```python
class Arm(Protocol):
    name: str
    def build(self, llm, session, budgets, task: TaskView, memory: MemoryView) -> ReactAgent
```

- `MemoryView.none` (B0): system prompt P0 verbatim from prereg Appendix P; no memory block.
- `MemoryView.trajectories(k=3)` (B1): lexical-overlap top-k successful producer trajectories
  (tokenized goal text + site match; same tokenizer family as goalsig) rendered via template T-B1
  (≤1200 tokens each, total block ≤1800 tokens) into the system prompt. Corpus frozen at F2.
- `MemoryView.procedure_store()` (SPIDER): ARCHITECTURE.md §5 flow — whole-goal retrieval
  (goalsig gate → fusion_scorer ranking), LLM plan JSON (schema in Appendix P3), procedure
  application with verification/reset caps, residual exploration; every stage billed to the arm.

Ablation flag (diagnostic slice only): `memory.mode=edge_iter` renders the SAME retrieved
knowledge as an unordered edge list (graph_iter-style) instead of packaged procedures — isolates
A3's packaging claim. Never enters the win-rule panel.

## 10. Analysis contract `analysis/compute_verdict.py` — unchanged

Input: raw_rows.jsonl (+ events dir). Output `results/product-beta/PB-001/VERDICT.json`:

```json
{
  "aggregates": {"per_arm_regime": {}, "paired_reductions": {}},
  "win_rule_evaluation": {
    "success_noninferior_full_panel": {"clause": "...", "value": 0.0, "threshold": -0.10, "pass": true},
    "r1r2_median_action_reduction_ge_50": {"pass": false},
    "r1r2_median_token_reduction_ge_40": {"pass": false},
    "r1r2_median_wall_reduction_ge_30": {"pass": false},
    "zero_fabricated_success_spider": {"pass": true},
    "two_pass_replication": {"pass": true},
    "spider_r3_not_behind_b0_by_more_than_1_row": {"pass": true},
    "comparator": "B1"},
  "verdict": "BEATS_BASELINE|PARITY|LOSES|INCONCLUSIVE|MEASUREMENT_INVALID",
  "exclusions": [], "notes": []
}
```

Mechanical formulas (frozen): success rate over rows per arm on full panel incl. R3; paired
per-task reductions on R1+R2 = median over tasks of `(comparator_t − spider_t)/comparator_t` with
pass-averaged per-task costs; comparator = higher-success baseline (tie→B1); replication =
per-cell status equality across passes for ALL arms. Script is deterministic, stdlib-only where
possible, hash-pinned at F2, and must run unchanged on auditor recomputation.
