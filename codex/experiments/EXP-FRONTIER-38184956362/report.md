# EXP-FRONTIER-38184956362 — EXECUTE REPORT (FALSIFIES)

- **Lane**: frontier
- **Outcome**: `FALSIFIES` (engine-stratified bounded negative, frozen decision rule G6)
- **Status**: `COMPLETE` — measurement transaction valid; all frozen gates V1..V5 passed; result is a valid scientific negative, not an infrastructure failure.
- **EXECUTE date**: 2026-10-12 (UTC), run on GitHub Actions runner `runnervmmprz5` (Linux, x86_64)
- **Determinism**: frozen `request.json` / `spec.json` / `prereg.md` / `freeze.json` / `design_review.json` immutable; executed code identity bound by hash (V1 gate, sha256 `b9b2efdc…`); the reconstructed module was executed with its embedded LOCKED checksum values from the freeze.

---

## 1. Executive summary

On the credential-free GET-only stdlib-HTTP substrate, using the frozen 20-host pool and the bounds emitted by the parent discovery expedition (EXP-FRONTIER-38164611798), the O(1)-cost "site-native discovery channel" hypothesis (C-CROSSSITE: a fresh agent can reach deep state-carrying pages in ≤3 GETs via sitemap/robots/search/feed/JSON-LD enumerated by the site itself) is **falsified on this frame**:

- **Q1 (census)**: 556 discovered DEEP (hop 3..6) pages across 20 hosts; each was fetched once (556/556, full census, no censoring). 208 pages (37.4%) carry ≥1 named control — 13 on **mdBook** (doc.rust-lang.org), 187 on **Sphinx-RTD** (docs.pytest.org 159 + docs.readthedocs.io 28), 8 on **Sphinx** (pandas.pydata.org). Three engines host state-carrying DEEP pages (≥2 required; PC-2/PC-3 PASS).
- **Q2 (discovery)**: **0 of 208** admitted items (0.0%) are reachable within the charged ≤K=3 fresh-agent GETs through **any** of the five frozen channels (robots→sitemap, sitemap.xml, on-site search, RSS/Atom, JSON-LD). Per-engine fractions: mdBook 0.0 (CI95 [0.0, 0.247]), Sphinx 0.0 (CI95 [0.0, 0.369]), Sphinx-RTD 0.0 (CI95 [0.0, 0.0195]). No engine is LIMITED; 0/208 admitted items were dead.
- **Q3 (materiality)**: 0 of 3 DEEP-admitting engines reach the 0.50 threshold → **G6 FALSIFIES** with a decision-reason string "fewer than 2 engines reach 0.5: none over 3 DEEP-admitting engine(s), limited=[] (engine-stratified bounded negative)".

The zero is *not* an instrument artifact: all four DEEP-admitting hosts' channel documents were fetched live and parsed by canary-verified extractors (the sitemaps demonstrably contain only version roots; the search endpoints demonstrably return 200 with JS-rendered results), the reachability scorer demonstrably returns True for listed+live fixture items and False for unlisted/dead ones on the same code path, and an independent recomputation of membership under the frozen equality semantics reproduces the module's verdict for all 208 items (with even a V7-relaxed cross-host path comparison finding zero path-equivalent matches).

**Consequences (per frozen product_consequence_negative).** The short-horizon self-hosted discovery axis is closed on this substrate class and frame: no O(1) site-native discovery shortcut is promoted into Product Core, and C-CROSSSITE stays at HYPOTHESIS. Mandate options for the Global Research Director: (1) refit discovery to the runner-up RACQ candidates of the experimental parent (URI/title-probe/URL-pattern search at O(hops) cost) and (2) authorize an out-of-substrate (JS/browser) pool for ON_SITE_SEARCH coverage — each bounded, cheap, and independently decisive.

---

## 2. Evidence chain (RAW → OBSERVATION → DERIVED → INTERPRETATION)

1. **RAW** (frozen inputs): `research/experiments/EXP-FRONTIER-38164611798/raw/structural.jsonl` (bound frame; sha256 `2afe65b6…`), `research/experiments/EXP-FRONTIER-38164611798/execute_module.py` (base; sha256 `75a01d49…`), `freeze.json` hash table.
2. **RAW** (execution, `--out research/experiments/EXP-FRONTIER-38184956362`):
   - `raw/controls.jsonl` — 15/15 control rows PASS.
   - `raw/channel_docs.jsonl` — per-host channel documents; 20/20 seeds HTTP 200.
   - `raw/census.jsonl` — Q1 census separation per host.
   - `raw/structural.jsonl` — censused frame (frame + census backfill of `controls_seen`).
   - `raw/items.jsonl` — 208 admitted items, per-channel membership, liveness.
3. **DERIVED**: `derived/metrics.json` — frozen `compute_metrics` output incl. per-engine fractions, CI95, decision.
4. **OBSERVATION** (selected, full ledger in `result.json`):
   - census: 556 discovered, 556 fetched, 208 with controls (mdBook 13, Sphinx-RTD 187, Sphinx 8, 12 engines zero-deep);
   - liveness: 208/208 admitted items HTTP 200;
   - membership: 0/208 items in any of the five channels;
   - search probes: 208/208 HTTP 200 result pages, 0 static links to the queried item;
   - channel documents: doc.rust-lang.org robots→sitemap.txt = 3 version roots; docs.pytest.org sitemap.xml = 15 version roots; docs.readthedocs.io = 1 loc; pandas.pydata.org = no sitemap endpoints.
5. **INTERPRETATION**: the site-native discovery channels of this pool's hosts do not enumerate their own deep control-bearing pages; with the empirical tilt (deep-static-index hosts carry no named DEEP controls here), the ≤3-GET discovery claim is falsified engine-stratified on this frame. Bounded: substrate class (credential-free static GET), pool (20 hosts), frame (556 DEEP items), channels (five), K=3.

---

## 3. Gates

| Gate | Frozen criterion | Result | Evidence |
|---|---|---|---|
| V1 code identity | sha256(module C) = `b9b2efdc…` (+3 audit repairs) | **PASS** | byte-identical strip of prereg §7 block; `py_compile` 0 |
| V2 controls | 15/15 rows PASS, exit 0 | **PASS** | `raw/controls.jsonl` (sha256 `fddd9e42…`) |
| V3 inventory | 20/20 seeds HTTP 200 | **PASS** | `raw/channel_docs.jsonl`; `seed_error_hosts=[]` |
| V4 frame fidelity | 20 hosts, 556 DEEP, frame hash `2afe65b6…` | **PASS** | `--stage structural --frame …` |
| V5 census completeness | `deep_fetched == deep_discovered` per host; ≥2 engines with controls | **PASS** | 556/556; mdBook 13, Sphinx-RTD 187, Sphinx 8 → 3 engines |
| PC-SEED-LIVENESS | 20/20 seeds HTTP 200 at inventory | **PASS** | `raw/channel_docs.jsonl` |

Decision rule execution (frozen, §8.3): `engines_at_or_above_threshold=[]` ⊂ `engines_census_with_any_deep={mdBook,Sphinx,Sphinx-RTD}` (nonempty) and `engines_limited=[]` → **G6 FALSIFIES**.

---

## 4. Q1 census (measurement)

| Host | Engine | DEEP discovered | DEEP fetched | with controls |
|---|---|---|---|---|
| doc.rust-lang.org | mdBook | 220 | 220 | **13** |
| docs.pytest.org | Sphinx-RTD | 160 | 160 | **159** |
| quotes.toscrape.com | custom | 99 | 99 | 0 |
| docs.readthedocs.io | Sphinx-RTD | 36 | 36 | **28** |
| jekyllrb.com | Jekyll | 24 | 24 | 0 |
| pandas.pydata.org | Sphinx | 9 | 9 | **8** |
| react.dev | Docusaurus | 8 | 8 | 0 |
| other 13 hosts | — | 0 | 0 | 0 |
| **Total** | — | **556** | **556** | **208** (37.4%) |

Per-engine admitted pools: mdBook n=13 (hop 3: 13), Sphinx n=8 (hop 3: 8), Sphinx-RTD n=187 (hop 3: 88, hop 4: 99; consistency of the two hosts' hop sums verified — class of AUDIT-VF-04).

---

## 5. Q2 discovery coverage (measurement) and Q3 decision

Charged cost per channel (all ≤ K=3): robots→sitemap 3 GETs, sitemap.xml 2, on-site search 3, RSS/Atom 3, JSON-LD 2. Item liveness GET charged per channel. All protocol costs within K; no engine LIMITED (0 dead / 0 excluded).

| Engine | admitted | items in robots/sitemap | items in sitemap.xml | items via search | items in RSS/Atom | items in JSON-LD | reachable any | fraction (CI95) |
|---|---|---|---|---|---|---|---|---|
| mdBook | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 (0.0–0.2471) |
| Sphinx | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 (0.0–0.3694) |
| Sphinx-RTD | 187 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 (0.0–0.0195) |
| **All** | **208** | 0 | 0 | 0 | 0 | 0 | **0** | **0.0** |

Q3: threshold 0.50 on ≥2 distinct engines; `engines_at_or_above_threshold=[]` → **FALSIFIES**.

**Channel-document ground truth** (why 0 is real, not a parse failure):
- doc.rust-lang.org: robots.txt → sitemap.txt with 3 URLs (`/beta/`, `/nightly/`, `/stable/` roots); `/sitemap.xml` and `/sitemap_index.xml` 404; no feed; no JSON-LD URLs. (mdBook uses a client-side searchbar; results are JS-rendered.)
- docs.pytest.org: robots → same 15 URLs as `/sitemap.xml`; all are version roots (`en/4.6.x … en/9.0.x`, `en/latest`, `en/stable`); no deep page is listed. Search action `/en/stable/search.html` input `q`; results JS-rendered.
- docs.readthedocs.io: sitemap documents 1 loc (`https://docs.readthedocs.com/`; plus `/platform/stable/` via the .com sitemap); the 28 admitted items all live on `docs.readthedocs.com/dev/latest/…` (no match; item URLs are on the readthedocs.com base host per V7 exact-host semantics).
- pandas.pydata.org: robots has no Sitemap lines; `/sitemap.xml` and `/sitemap_index.xml` 404; only a GET search form (`search.html`, input `q`) with JS-rendered results.

Independent V7 recomputation (outside the module, using the module's frozen `norm_eq`) reproduced `reachable_any=False` for all 208 items; even relaxing V7 to cross-host path comparison yields 0 path-equivalent matches.

---

## 6. Baseline contrast (frozen baselines)

| Baseline | Definition | Value vs discovery |
|---|---|---|
| B-SAME-HOST-BFS-PATH-COST | 1-based BFS discovery/fetch ordinal of each admitted item in the bound frame (the a-priori acquisition cost to beat) | 208/208 within the bound frame; ordinal min 31, max 250, **mean 166.0**; discovery reached **0/208** at charged ≤3 |
| B-PERSISTED-PATH-REACQUISITION (RACQ_PATH) | ~hop+1 fresh GETs per item (experimental parent) | inherited context, not re-measured here |
| B-DIRECT-URL-REPLAY (RACQ_URL) | 1 fresh GET per item | inherited context, not re-measured here |

The contrast is discriminating: the same frame's BFS acquisition obtained all 208 items at mean path cost 166, while the O(1) claim obtained 0. **GET ledger (actual network):** inventory 108 + census 556 + search probes 208 + liveness 208 + synthetic-null 3 = **≈1083 GETs**; zero model calls, zero credentials, zero persistence (hourglass policy).

---

## 7. Controls (all PASS; `raw/controls.jsonl`)

- **NC_BFS_CALIBRATION_FLAT** R=2.0 (expected ≤3.0) and **NC_BFS_CALIBRATION_GROWING** R=6.5, nodes_fetched=250 (expected >3.0) — hop-cost model of the census/depth logic.
- **Parser canaries** (8): sitemap.xml exact URL set, sitemap index→child, sitemap.txt, robots FIRST-Sitemap-line, RSS first-link, Atom first-link, JSON-LD seed URL — all exact-match.
- **Reachability semantics**: PC_REACHABILITY_LISTED_LIVE 3/3 True (sitemap/jsonld/search) and NC_REACHABILITY_UNLISTED_OR_DEAD (unlisted-live False; listed-404 False) — the *same* `evaluate_items` path that scored the 208 items demonstrably produces True and False correctly.
- **NC_SYNTHETIC_UNREACHABLE_ITEM_direct** (3×): synthetic URLs on frozen hosts return real HTTP 404 — network reality check.
- **PC_ENV**: Python 3.12.15, stdlib urllib, ssl default True.

---

## 8. Validity, threats, disclosure

- **Valid transaction (VN-1)**: all gates passed; FALSIFIES is the frozen decision rule's output for a live, fully-fetched, fully-listed pool.
- **Construct degeneracy (VN-3, disclosed pre-hoc in prereg §14.1)**: "state-carrying" includes theme chrome (`searchbar`, `q`); not narrowed post-hoc. The zero holds even with the inflated construct; a chrome-stripped construct would not change the decision.
- **Empirical tilt (VN-4, prereg §14.2 + design_review finding 1)**: hosts with static named search forms expose shallow indexes (version roots only); hosts with deep indexes (Docusaurus, Hugo, Jekyll…) carry no named DEEP controls on this frame. Zero is consistent with the tilt. **Bounded scope**: this result says nothing about (a) JS/browser substrates, (b) pools built around in-substrate positive poles such as docs.djangoproject.com (prereg §11e, deliberately excluded from the frozen frame), (c) channels ≠ the five frozen ones.
- **Coverage gap (VN-5, §14.6)**: search results JS-rendered → ON_SITE_SEARCH scored under static-HTTP semantics (200 responses, no static links) and recorded as a disclosed gap, not a null.
- **Staleness (VN-6)**: 208/208 live at EXECUTE → not a confound.
- **Redirect-domain frame property (VN-7)**: docs.readthedocs.io items live on docs.readthedocs.com (frozen parent-frame property); V7 exact-host semantics prevent cross-host matching; disclosed, not silently ignored.
- **Single vantage (VN-8)**: one runner egress; cross-vantage stationarity untested (→ U-3).
- **Representation (VN-10)**: MAX_BODY=600000 truncation flags; no scored channel document truncated.

## 9. Unresolved (→ handoff)

U-1 JS/browser-substrate search coverage (out of mandate scope); U-2 a rebuilt pool containing the static-index×named-deep-controls conjunction (prereg §11e pole; SUPPORTS is a real, unmeasured state for this instrument — EXP-FRONTIER-38164611798's Q1 measures it, this design re-measures it on the frozen frame only); U-3 cross-vantage stationarity; U-4 named-control-type (chrome/content) split not recorded by the frozen module; U-5 docs.readthedocs.io/docs.readthedocs.com share the RTD platform (engine-class distinctness per frozen V12 is base-host distinctness, not server-origin independence).

## 10. Artifacts (hashes)

| File | sha256 |
|---|---|
| `execute_module.py` (code) | `b9b2efdc78266717946022002eb3bef301979ac6fc0967254202747037c5956f` |
| `raw/controls.jsonl` | `fddd9e429d27792527e0e580585270a875fc1e0ebc286edb109d31db5cd99672` |
| `raw/channel_docs.jsonl` | `4ed67c117687d3eb75bb2c2dd97379b18ffea726232eaecf33ebaa2e875f1bb0` |
| `raw/census.jsonl` | `8b7a5f919143ac1ae3c0a91c282d848a83c493656524bb0583e360225c38b40f` |
| `raw/structural.jsonl` (censused) | `95a3f15f9e7164096cf6c18fc3b6b1212c91caad88d741020ec885f0b520fd45` |
| `raw/items.jsonl` | `c8215d69fbc4f230bd7087773c44aeecd68021a8b3349666adc5c19b0ed26ec5` |
| `derived/metrics.json` | `d51568c56de800fb4bd3d5aec748a625edd8c15e69fbdacfc57215f0e5b6c17d` |
| bound frame (fixture) | `2afe65b63f751ef0d25578b02c9a667d43f866a0ac54504ebe1e1f4db839d747` |
| bound base module (fixture) | `75a01d490ec81609cbf87a606f8cfa9227d07f07765b2eb4fd876fef2c8ff53a` |