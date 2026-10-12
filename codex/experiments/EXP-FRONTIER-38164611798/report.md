# EXP-FRONTIER-38164611798 — Execution Report

**Lane:** frontier | **Claim:** C-CROSSSITE | **Status:** MEASUREMENT_INVALID | **Outcome:** NOT_APPLICABLE

---

## 1. Summary

This experiment attempted to measure whether site-native discovery channels (sitemaps, feeds, on-site search, JSON-LD) make deep (shortest-path hop ≥ 3) state-carrying item acquisition O(1) within K = 3 fresh-agent GETs, on a credential-free GET-only stdlib-HTTP substrate over a frozen 20-host pool.

**The experiment could not complete its outcome stages (Q2/Q3) due to a defect in the frozen outcome-bearing code.** The frozen module (prereg.md section 16, CODE_SHA256 `75a01d490ec81609cbf87a606f8cfa9227d07f07765b2eb4fd876fef2c8ff53a`) contains a bug where `v.get('controls_seen', 0) > 0` raises `TypeError` when `controls_seen` is `None` (the key exists with null value for pages discovered but not fetched due to budget limits). This occurs at two locations in the discovery stage: host census computation and item list comprehension.

All measurement validity gates passed:
- **V1 Code Canary:** Transcribed module hash matches frozen CODE_SHA256 ✓
- **V2 Controls Gate:** 15/15 control rows (13 distinct identities) PASS ✓
- **V3 Inventory/Seed Gate:** 20/20 frozen seeds returned HTTP 200 ✓

The structural pass (Q1) completed successfully for all 20 hosts. The Q1 census is reported below. Q2 (per-channel discovery reachability) and Q3 (materiality threshold ≥ 0.50 on ≥ 2 engines) could not be measured.

---

## 2. Q1 Structural Census (Attainability Measurement)

### 2.1 Per-Engine DEEP Items with Observed Controls

| Engine Class | Hosts | DEEP (hop≥3) with Controls | DEEP Total in Graph | Hop Distribution |
|--------------|-------|---------------------------|---------------------|------------------|
| **Sphinx-RTD** | docs.readthedocs.io, docs.pytest.org | **32** | 196 | hop3: 94, hop4: 101, hop5: 1 |
| mdBook | doc.rust-lang.org | 0 | 220 | hop3: 220 |
| custom | quotes.toscrape.com | 0 | 99 | hop3: 75, hop4: 24 |
| Sphinx | docs.python.org, numpy.org, pandas.pydata.org | 0 | 9 | hop3: 9 |
| Jekyll | jekyllrb.com | 0 | 24 | hop3: 24 |
| Docusaurus | docusaurus.io, react.dev | 0 | 8 | hop3: 8 |
| GNU-web | www.gnu.org | 0 | 0 | — |
| GitBook | docs.gitbook.com | 0 | 0 | — |
| GitHubDocs | docs.github.com | 0 | 0 | — |
| Hugo | gohugo.io | 0 | 0 | — |
| Hugo-k8s | kubernetes.io | 0 | 0 | — |
| MDN-Yari | developer.mozilla.org | 0 | 0 | — |
| MediaWiki | en.wikipedia.org, www.mediawiki.org | 0 | 0 | — |
| WordPress | blog.wordpress.org | 0 | 0 | — |
| phpBB | forums.gentoo.org | 0 | 0 | — |

**Key finding:** Only **one engine class (Sphinx-RTD)** yielded any DEEP state-carrying items that were both reached *and fetched* within the BFS budget of 250 pages. All other engines either had no DEEP items in the graph, or their DEEP items were not fetched (controls_seen = null) because the budget was exhausted on shallower pages.

### 2.2 Host-Level Census

| Host | Engine | DEEP with Controls | DEEP in Graph | Notes |
|------|--------|-------------------|---------------|-------|
| docs.readthedocs.io | Sphinx-RTD | 28 | 36 | hop3: 31, hop4: 4, hop5: 1 |
| docs.pytest.org | Sphinx-RTD | 4 | 160 | hop3: 63, hop4: 97 |
| doc.rust-lang.org | mdBook | 0 | 220 | All 220 DEEP items unfetched (budget) |
| quotes.toscrape.com | custom | 0 | 99 | All unfetched (budget) |
| docs.python.org | Sphinx | 0 | 0 | No DEEP items in graph |
| numpy.org | Sphinx | 0 | 0 | No DEEP items in graph |
| pandas.pydata.org | Sphinx | 0 | 9 | All unfetched (budget) |
| jekyllrb.com | Jekyll | 0 | 24 | All unfetched (budget) |
| react.dev | Docusaurus | 0 | 8 | All unfetched (budget) |
| docusaurus.io | Docusaurus | 0 | 0 | No DEEP items in graph |
| (11 other hosts) | — | 0 | 0 | No DEEP items in graph |

### 2.3 Engines with Zero DEEP (with Controls)

14 of 15 engine classes have **zero DEEP items with observed controls**. For most, this is because the BFS budget of 250 pages was exhausted before reaching hop ≥ 3 pages and fetching them to check for controls. The budget cap is enforced *inside the link loop* — even a single page with thousands of links cannot push discovery past 250.

---

## 3. Channel Inventory (Discovery Substrate)

All five frozen discovery channels are live on ≥1 host (per DESIGN certificate, re-verified at EXECUTE):

| Channel | Live Hosts | Example Endpoints |
|---------|-----------|-------------------|
| ROBOTS_SITEMAP | 7 | doc.rust-lang.org, docs.python.org, docs.readthedocs.io, ... |
| SITEMAP_XML | 9 | docs.python.org, numpy.org, docusaurus.io, ... |
| ON_SITE_SEARCH | 10 | docs.python.org, numpy.org, docs.readthedocs.io, ... |
| RSS_ATOM | 7 | jekyllrb.com, developer.mozilla.org, www.gnu.org, ... |
| JSON_LD | 6 | docusaurus.io, jekyllrb.com, kubernetes.io, ... |

ON_SITE_SEARCH is probeable on 10 hosts (search form with named text-like input found). Notably, `blog.wordpress.org` has a search form but its action is cross-host (`wordpress.org/search/do-search.php`), which is disclosed but not followed as a membership shortcut per frozen protocol.

---

## 4. Controls Certificate (V2 Gate)

All 15 control rows passed (13 distinct control identities):

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| NC_BFS_CALIBRATION_FLAT | R ≤ 3.0 | R = 2.0 | ✓ |
| NC_BFS_CALIBRATION_GROWING | R > 3.0 | R = 6.5 | ✓ |
| PC_PARSER_CANARY_sitemap_xml | urls=[a], not index | PASS | ✓ |
| PC_PARSER_CANARY_sitemap_index | is_index, children=[s1.xml] | PASS | ✓ |
| PC_PARSER_CANARY_sitemap_txt | urls=[a,b] | PASS | ✓ |
| PC_PARSER_CANARY_robots | lines=[s.xml] | PASS | ✓ |
| PC_PARSER_CANARY_feed_rss | urls=[p1] | PASS | ✓ |
| PC_PARSER_CANARY_feed_atom | urls=[p2] | PASS | ✓ |
| PC_PARSER_CANARY_jsonld | urls=[p3] | PASS | ✓ |
| PC_REACHABILITY_LISTED_LIVE | listed+live reachable | 3/3 True | ✓ |
| NC_REACHABILITY_UNLISTED_OR_DEAD | unlisted/dead NOT reachable | both False | ✓ |
| PC_ENV | Python 3.12, stdlib urllib | 3.12.15 | ✓ |
| NC_SYNTHETIC_UNREACHABLE_ITEM_direct ×3 | HTTP ≥ 400 | 404 on 3 hosts | ✓ |

The two BFS calibration controls certify the instrument's dynamic range in both directions (flat R=2.0 vs growing R=6.5). The reachability fixture controls drive the actual `evaluate_items` scoring path. Two DESIGN-time bugs were caught by these controls pre-freeze (PC_PARSER_CANARY_jsonld extraction bug; NC_SYNTHETIC_UNREACHABLE_ITEM_direct HTTPError collapse), demonstrating sensitivity.

---

## 5. Frozen Code Defect (Root Cause of MEASUREMENT_INVALID)

### 5.1 The Bug

In prereg.md section 16 (frozen outcome-bearing module), two locations use:

```python
v.get("controls_seen", 0) > 0
```

When a page is discovered but not fetched (due to budget/depth limits), its entry has `"controls_seen": null` (key exists, value explicitly null). Python's `dict.get(key, default)` returns the **actual value** (None) when the key exists, not the default. Thus `None > 0` raises `TypeError`.

**Locations:**
1. Line ~995 (host_census computation)
2. Line ~1208-1212 (items list comprehension for evaluate_items)

### 5.2 Impact

- Structural pass (Q1) and inventory completed successfully
- Discovery stage (Q2/Q3) crashes before any per-item evaluation
- No per-channel coverage, reachability fractions, or Q3 decision can be produced
- The frozen code hash (V1) matches — the defect is in the *frozen design itself*

### 5.3 Why This Was Not Caught at DESIGN

The DESIGN-stage certificate ran only `--stage controls` and `--stage inventory`. The `--stage structural` and `--stage discovery` (which contains the bug) were not executed at DESIGN. The design review correctly validated the six freeze_eligibility checks but could not catch a runtime bug in code that wasn't exercised.

---

## 6. Validity Threats & Measurement Notes

| ID | Threat | Impact |
|----|--------|--------|
| VN-FROZEN-CODE-BUG | Frozen code TypeError on None comparison | **Blocks Q2/Q3 measurement entirely** |
| VN-BUDGET-LIMIT | BFS budget 250 hard cap | Only 1/15 engines yielded observable DEEP controls; most DEEP items unfetched |
| VN-UNIT-REDUCTION | Page-level vs control-triple unit | Conservative for item counts; does not inflate reachability |
| VN-REPRESENTATION | Body cap 600KB, sitemap index→first child, robots→first line | Partial graph for large sites (docs.gitbook.com truncated) |
| VN-AMORTIZATION | Charged ≤K=3 vs actual GETs | Actual vs charged ledger not generated (discovery stage failed) |
| VN-SEARCH-SEMANTICS | Slug query, first GET form, cross-host disclosed | May underestimate search coverage for some engines |
| VN-ENGINE-IDENTITY | Generator meta or DESIGN platform | 7/20 hosts had generator meta; 13 used documented platform |
| VN-DRIFT | Live Web changes between freeze/execute | Controls + inventory re-run as gates; all passed |

---

## 7. Decision Rule Evaluation (Frozen)

Per prereg.md section 10 / spec.json decision_rule:

- **G1 Validity (V1/V2/V3):** All PASSED → would proceed to G2
- **G2 Seed Signature:** 0/20 seed failures → would proceed to G3
- **G3 Attainability:** ≥1 engine with DEEP items (Sphinx-RTD has 32) → would proceed to G4
- **G4 Limited-Only:** 0 engines limited (>10% death) → would proceed to G5
- **G5 Materiality:** Requires ≥2 engines with fraction ≥ 0.50 → **CANNOT EVALUATE** (discovery stage failed)
- **G6 Otherwise:** Would be FALSIFIES (only 1 eligible engine) → **CANNOT EVALUATE**

Because the outcome stage code crashes, the decision rule cannot be fully evaluated. Per EXPERIMENT_PACKET.md: "Any FAIL [of measurement validity] → status=MEASUREMENT_INVALID, outcome=NOT_APPLICABLE; never a scientific answer."

---

## 8. Product Consequences

| Scenario | Consequence |
|----------|-------------|
| **If SUPPORTS** (Q3 holds) | C-CROSSSITE → EXPERIMENTAL; effort moves to discovery-channel coverage & substrate expansion; C-FRESHNESS/C-PRODUCT-ECON becomes scheduled mandate |
| **If FALSIFIES** (Q3 fails) | Engine-stratified bounded negative; discovery axis closed on this substrate; persistence-maintenance (re-validation GETs/bytes + stale-replay false-accept rate vs re-derivation cost) handed to Graph/Product |
| **INCONCLUSIVE** (zero DEEP or all-LIMITED) | Q1 attainability census + zero-admission channel ledger = durable deliverable; no claim update; future design re-targets pools from census |
| **MEASUREMENT_INVALID (actual)** | **No claim update.** Q1 census delivered as partial evidence. Frozen code defect must be fixed and experiment re-run under new design to measure Q2/Q3. |

---

## 9. Artifacts

| Path | SHA256 | Role |
|------|--------|------|
| raw/controls.jsonl | fddd9e429d27792527e0e580585270a875fc1e0ebc286edb109d31db5cd99672 | raw |
| raw/channel_docs.jsonl | b42798c3cd285dda9f06fd87f5a09a6890e6aae53dc0126a73c21c5c23b979cc | raw |
| raw/structural.jsonl | 2afe65b63f751ef0d25578b02c9a667d43f866a0ac54504ebe1e1f4db839d747 | raw |
| execute_module.py | 75a01d490ec81609cbf87a606f8cfa9227d07f07765b2eb4fd876fef2c8ff53a | code (frozen transcript) |

---

## 10. Unresolved Questions

1. **Q2/Q3 unmeasured:** What fraction of the 32 Sphinx-RTD DEEP items is reachable via the five frozen channels within K=3 GETs?
2. **Per-channel coverage:** Which channels cover which items? Which channels admit zero DEEP items?
3. **Budget sensitivity:** Would a larger BFS budget (or different crawl policy) yield DEEP controls on other engines (mdBook, custom, Sphinx, Jekyll, Docusaurus)?
4. **Threshold attainability:** Can any second engine reach the 0.50 threshold on this pool/substrate?
5. **Code fix required:** The frozen code bug must be corrected (change `v.get('controls_seen', 0)` to `(v.get('controls_seen') or 0)`) and the experiment re-run under a new DESIGN.

---

*Generated 2026-10-11 | SPIDER Research 2.0 | Frontier Lane | EXP-FRONTIER-38164611798*