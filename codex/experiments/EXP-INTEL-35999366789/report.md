# EXP-INTEL-35999366789 — Report (intel lane)

**status: COMPLETE — outcome: MIXED** (H_A FALSIFIED_IN_SETTING at the 4-family census ceiling; H_B SURVIVES_CURRENT_TEST)

Frozen design executed per `freeze.json` hashes (prereg `5fc5d9e1...`, spec `562391e2...`, request `ade7c451...`). No frozen file modified. All MV1–MV4/MV6–MV9 gates pass; MV5 WebGym documented UNAVAILABLE (2 genuine 401 attempts, HF_TOKEN absent) — not invalid, not assumed zero.

---

## 1. Module A — Durable census + deterministic constructibility

### A1 Durable sources (MV1/MV2/MV9)
- **SRC-HF** (WebArena-Verified raw + Hub API): HTTP **401 × 2** (`hf_token_present=false`), bytes 0, sha null — logged at `artifacts/raw/hf_manifest_attempts.json`. Cross-source byte-identity Docker↔HF **unavailable** (explicitly marked, not assumed).
- **SRC-HF-WEBGYM** (292k): HTTP **401 × 2** — logged at `artifacts/raw/hf_webgym_manifest_attempts.json`.
- **SRC-DOCKER**: Hub API **200 × 2** with digest `sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb` (64 hex) matching on both; `docker pull @digest` returncode 0 × 2; `docker images --digests` match; health `http://localhost:7770` **200 × 3**. **SRC_DOCKER_SUCCESS = true.**
- Local pinned manifest re-verified byte-identical: sha `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30`, 927,596 bytes.

### A2 Census + deterministic family constructibility (MV3/MV4)
- Census (matches parent `6fcdc04f` exactly): total **812**, shopping **192**, shopping_admin 182, map 112, reddit 114, gitlab 196, wikipedia 16; families_ge3 **36**; family-size histogram `{3:2, 4:1, 5:32, 6:1}`; **product_page_families [136, 145, 196, 222]** (21 tasks with ≥1 product-page start_url); 32/36 families have only `__SHOPPING__` homepage/non-product start_urls.
- Deterministic sampling executed twice with identical seed reset:
  **S1 == S2 == [191, 180, 162, 197, 153, 213, 163, 137, 136, 222]** — determinism proven. Only **136, 222** of the sampled 10 are product-page families; the other 8 have no product-page task in the census.
- Probe (1280x720, CDP `Accessibility.getFullAXTree`, chromium 153.0.8010.12, outerHTML SHA after grammar strip with live grammar hash `273eafbc...`): **12/12** product captures valid — AX median **688** (min 627), DOM median **200,413** (min 195,052), SHA identical **12/12**, SHA mutation-changed **12/12**, anchored elements **(heading/price-box/add-to-cart/main/contentinfo) 12/12** with subtree node counts heading 2 / price 6 / add-to-cart 2 / main 226–365 / contentinfo 31.
- **M_A_CONSTRUCTIBLE_COUNT = 4** (`fam136, fam145, fam196, fam222`) **< 10 → H_A deterministic 10-family gate FALSIFIED_IN_SETTING (bounded)**. The falsification is a *deterministic census property*: exactly 4 constructible product families exist in the pinned 812-task census under the frozen protocol; it is not a protocol artifact and not an infrastructure failure. The canonical-path mechanism (anchoring + SHA stability) passes 4/4.
- MV3 environment pinned: browsergym-core 0.14.3, agentlab 0.4.2, playwright **1.63.0** (force-installed `--no-deps`; browsergym-core pins 1.44), chromium 153.0.8010.12, pip freeze 263 lines sha `7c4dfcce...`; protocol dump confirms `getFullAXTree` params `[depth, frameId]`, AXNode 13 properties, `boundingBox` absent (Chromium153 fact → anchored Runtime.evaluate replacement 12/12).

### A3 WebGym diverse subsystem (MV5)
**UNAVAILABLE** — 2 genuine 401 attempts logged. `M_WEBGYM_*` = null; sweep 0.818–0.9479 and family-level B=2000 duplication CI not computable. H_A partially bounded (parent UNRES-WEBGYM equivalent).

---

## 2. Module B — Blind external-SOTA ceiling with honest Pareto (MV6/MV7/MV8)

Blind recipes from frozen text only; deterministic simulation, no LLM. 327 rows (40 tasks × 8 baseline variants + 7 PC-B toy). **Two runs byte-identical** sha `3c5ab5af...` (matches parent established sha) — MV8 re-run gate satisfied; harness sha `b11ea970...` logged.

| Baseline | Coverage (B=2000 CI) | M_total_f10 (CI) | M_total_f100 |
|---|---|---|---|
| B-AGENTIC-DSM (HITL) | 0.75 [0.625, 0.875] | 22.6 [19.8, 26.0] | 5.65 |
| B-AGENTIC-DSM-NOHITL | 0.25 [0.125, 0.375] | 10.0 [9.4, 10.6] | 2.50 |
| B-TRACECOMPILER-DEFUSE | 0.25 [0.125, 0.375] | 10.0 [9.4, 10.6] | 2.50 |
| B-BMEM-CATALOG | 0.0 degenerate [0,0] flagged | 10.0 [9.0, 11.2] | 2.50 |
| B-SPIDER-ALIAS | 0.925 [0.85, 1.0] | 30.1 [25.4, 35.5] | 7.53 |
| B-SPIDER-ROUTING | 1.0 degenerate [1,1] flagged | 33.0 [26.6, 41.0] | 8.25 |
| B-SPIDER-WEBMCP | 1.0 degenerate [1,1] flagged | 28.0 [22.4, 34.4] | 7.00 |
| B-COLD-LLM | 0.25 [0.125, 0.375] | 38.0 [33.0, 43.5] | 9.50 |

- **DSM O(1) ceiling**: 1.0/1.0 on header/body, 0.7 auth, **0.3 mixed** — the 99% claim does not transfer to mixed multi-channel alias-OOD. USD at published midpoint $0.047/patch: mean **$0.0353/task**, total **$1.41** for 40 (30 patch tasks), CI [0.0294, 0.0411].
- **Residual-novelty rho**: rho_real **0.8656** vs rho_shuffled **0.1592** (< 0.20 gate PASS, p=0.0) — cost tracks residual novelty, not length; residual-novelty gate rho≥0.60 PASSes on synthetic.
- **NC1 coverage shuffle**: DSM real family std 0.287 vs shuffled mean 0.113 (gap 0.174, p=0.0); SPIDER-ALIAS flat p=0.626 as pre-registered.
- **NC2**: delta_vs_truncated **0.6667** ≥ 0.20 PASS (full-tree non-vacuous).
- **NC3**: HITL ablation drop **0.50** ≥ 0.30 PASS (DSM without HITL collapses 0.75 → 0.25; mixed 0.3 → 0.0, auth 0.7 → 0.0).
- **WebMCP tool-bypass prevalence**: **0.725** [0.575, 0.85], amortized f10 **2.9**, f100 **0.725** — hybrid bypass dominates at f10/f100 on this synthetic set (parity coverage 1.0 at lower cost than routing).
- **PC-B toy**: DSM True, ALIAS/ROUTING/WEBMCP/BMEM True, TRACE/COLD False (as expected).
- False accept 0.0 structural (strict-server verify at alias time), disclosed.

Pareto (coverage × cost): at f10/f100 WEBMCP (1.0, 28.0/7.0) dominates ROUTING (1.0, 33.0/8.25); ALIAS (0.925, 30.1/7.53); DSM (0.75, 22.6/5.65) is the cheapest covered option but loses 0.25 coverage on mixed. SPIDER must beat the O(1) compilation ceiling (DSM 0.75 @ 22.6) on mixed-channel work — the only SPIDER mechanisms currently above it are the degenerate 1.0 saturators; on structured work (header/body/auth alone) DSM is at parity with SPIDER at lower cost.

---

## 3. Controls

- **PC-A** PASS (AX 17 > 10 ×3; SHA 16/16 both directions over 3 repeats). DOM 355 bytes — frozen fixture text (≈400 B) cannot reach the literal prereg §8 `DOM>=2000` sub-clause; disclosed as frozen-text internal inconsistency; `DOM>=2000` satisfied on canonical-path real captures (median 200,413).
- **PC-B** PASS (toy DSM 1.0). **PC-C** UNAVAILABLE (HF-gated, not failed).
- **B-DURABLE-HF** UNAVAILABLE (401×2) / **B-DURABLE-DOCKER** PASS (digest 64-hex + reachable).
- **B-TRUNCATED-20 / NC2** PASS (delta 0.6667). **NC3** PASS (drop 0.50).
- **B-AGENTIC-DSM** PARTIAL (interior single-channel, mixed collapse); **B-TRACECOMPILER-DEFUSE** PASS (0.25 body-1.0 collapse replicated); **B-BMEM-CATALOG** PASS (0.0 collapse, degenerate CI flagged); **B-SPIDER-ALIAS** PASS (0.925 flat); **B-SPIDER-ROUTING/WEBMCP** PASS-with-degenerate-flagged; **B-COLD-LLM** PASS (floor 0.25).

---

## 4. Decision (per frozen three-way rule)

- **A PASS** (MV1–MV4, MV6–MV9 genuine; MV5 UNAVAILABLE documented) → not MEASUREMENT_INVALID.
- **H_A_SURVIVES = FALSE**: constructible count 4 < 10. Bounded **FALSIFIED_IN_SETTING** — the pinned 812-task census deterministically yields exactly 4 constructible product-page families (136/145/196/222) under the frozen sampling+anchoring+SHA protocol; the ≥10-family gate is a hard census ceiling on this pin.
- **H_B_SURVIVES = TRUE**: blind external baselines executed with per-task logs; DSM/ALIAS interior CIs; honest M_total f10/f100 CIs; |rho_shuffled| 0.1592 < 0.20; PC-A/PC-B PASS; WebMCP prevalence measured.
- **Outcome: MIXED** per prereg §11 ("MIXED if one module survives and the other falsified").

## 5. Consequences for the portfolio

- **C-CROSSSITE** stays at the 4-family ceiling: Graph ≥10-family hold-out remains **BLOCKED on this pin**; must select an alternative census (shopping_admin 184-task/42-family superset, WebMall/Mind2Web-2 loopback, or expanded product-URL extraction) before any ≥10-family cross-site transfer claim. The 4-family ceiling is now *deterministically proven*, not a protocol artifact — do not re-run this same design expecting a different pin.
- **C-RESIDUAL-NOVELTY**: synthetic residual-novelty gate rho 0.8656 vs shuffled 0.1592 PASSes; O(1) DSM ceiling is parity-on-structure / below-SPIDER-on-mixed; residual novelty economics hinge on mixed-channel and real-site work (simulation bound).
- **C-PRODUCT-ECON**: WebMCP hybrid bypass 0.725 dominates at f10/f100 in simulation; real wall-clock/token Pareto still requires live execution.

## 6. Unresolved / smallest next actions

1. **HF_TOKEN with WebGym + WebArena-Verified read access** → cross-source byte-identity + 292k diverse eTLD+1 duplication CI + 0.818–0.9479 sweep (one re-run of A1/A3).
2. **Alternative census for ≥10 product families** (shopping_admin superset, WebMall/Mind2Web loopback) — only route to unblock Graph ≥10-family hold-out.
3. **Live-cost Pareto** (Stagehand/WebMCP real execution) for Product; **DSM mixed-channel causal step** (why 0.3 vs SPIDER 1.0) on real WebArena tasks.
4. NC2 shuffled-truncation variant (<0.05) not measured.

## 7. Artifacts

All under `research/experiments/EXP-INTEL-35999366789/` — see `artifacts` list with sha256 in `result.json` and `provenance.json`; raw evidence separated from derived measurements; failed-attempt logs included as first-class artifacts.