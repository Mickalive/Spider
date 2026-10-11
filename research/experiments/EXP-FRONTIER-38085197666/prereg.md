# Preregistration: EXP-FRONTIER-38085197666

**Lane**: frontier
**Target Claims**: C-CROSSSITE, C-RESIDUAL-NOVELTY, C-WEB-DYNAMICS
**Design Contract Version**: 2
**Director Mandate**: PIVOT to site-native discovery acquisition-cost question (cycle 38084662468)

---

## 1. Scientific Question

On the credential-free GET-only stdlib-HTTP substrate, over a frozen multi-host pool confirmed during DESIGN by a pre-freeze attainability certificate to contain DEEP (hop>=3) state-carrying items on at least two distinct hosts/engines (>=10 total, >=3 per engine) via the frozen same-host static-`<a>` BFS (depth<=6, budget 250), what fraction of those DEEP items is reachable in <=K=3 fresh-agent GETs (one discovery GET + item-page GET + one spare) using ANY of the five frozen discovery channels (ROBOTS_SITEMAP, SITEMAP_XML, ON_SITE_SEARCH, RSS_ATOM, JSON_LD) — with the preregistered materiality threshold 0.50 on >=2 engines deciding whether shortest-path hop is NOT a fundamental acquisition-cost barrier (persistent path caching is not the optimization target; effort moves to discovery and substrate expansion) versus fresh deep-instance acquisition remaining path-bound with a computable persistence break-even surface?

---

## 2. Hypothesis

Site-native discovery channels (robots.txt/sitemap directives, sitemap.xml, on-site search, RSS/Atom feeds, JSON-LD structured data) enable a fresh agent to reach DEEP (hop>=3) state items in O(1) GETs (K<=3) on at least two distinct engines, demonstrating that shortest-path hop is not a fundamental acquisition-cost barrier. If true, persistent path caching is not the primary optimization target and effort should shift to discovery-channel procedure caching and substrate expansion. If false, fresh deep-instance acquisition remains path-bound and persistence retains a measurable, depth-dependent amortization surface.

---

## 3. Falsifier (Two-Sided, Arithmetically Checkable Before Freeze, Satisfiable in Both Directions)

Let D_e be the set of confirmed DEEP items on engine e, and R_e ⊆ D_e the subset reachable in <=K=3 GETs via ANY frozen discovery channel.

**Primary Metric**: `discovery_reachable_fraction_e = |R_e| / |D_e|` for each engine e with |D_e| >= 3.

**Decision Rule**:
- If `discovery_reachable_fraction_e >= 0.50` for at least two distinct engines e → **verdict = FLAT** (hop is NOT a fundamental barrier)
- Else → **verdict = GROWING** (fresh acquisition remains path-bound)

**Satisfiability Justification**:
- The pre-freeze attainability certificate guarantees denominator > 0 (|D_e| >= 3 for >=2 engines)
- The positive control guarantees numerator CAN be > 0
- The negative/null controls guarantee numerator CAN be < denominator
- The 0.50 threshold is strictly interior to [0,1]
- Both FLAT and GROWING branches are arithmetically reachable

---

## 4. Substrate & Operational Definitions

### 4.1 Substrate
- **Protocol**: Credential-free GET-only Python stdlib HTTP (`urllib.request`)
- **TLS**: Verified (default system CA bundle)
- **User-Agent**: `SPIDER-frontier-38085197666/1.0`
- **Timeout**: 15 seconds per request
- **Max Body**: 1 MB (1,048,576 bytes)
- **Redirects**: Followed (max 10, stdlib default)
- **No**: Browser, Docker, model API key, credentials, cookies, write verbs, third-party state mutation

### 4.2 Hop Confirmation (Frozen Policy — Identical to EXP-FRONTIER-37950626378)
- **Algorithm**: Same-host static `<a href>` BFS, FIFO, document order
- **Budget**: 250 pages per seed per session
- **Depth Cap**: 6 hops
- **Host Constraint**: Exact hostname equality against seed's final URL (no eTLD+1 expansion)
- **Asset Exclusion**: Standard extensions (png, jpg, css, js, pdf, etc.) excluded
- **Session Count**: 2 independent sessions per seed (for session agreement)
- **Admission**: Items must appear in BOTH sessions with identical hop and RED.requests

### 4.3 DEEP / NEAR / MID Bands (Frozen)
- **NEAR**: hop ∈ {0, 1}
- **MID**: hop = 2
- **DEEP**: hop ∈ {3, 4, 5, 6}

### 4.4 State-Carrying Item Definition
A state-carrying item is a page containing at least one named `<input>` or `<select>` control (HTML form control with a `name` attribute), as detected by the frozen stdlib `HTMLParser`. This matches EXP-FRONTIER-37950626378 exactly.

---

## 5. Discovery Channels (Five Frozen Channels)

Each channel is a deterministic stdlib-HTTP procedure. Channels are tried in the fixed order below; the first channel that yields a valid item URL within the K=3 budget counts as success for that item.

### 5.1 ROBOTS_SITEMAP
1. Fetch `/robots.txt` from seed host
2. Extract all `Sitemap:` directive URLs (case-insensitive)
3. For each sitemap URL: fetch, decompress if `.gz`, parse XML `urlset/url/loc`
4. Filter URLs for state-item patterns (see Section 5.6)

### 5.2 SITEMAP_XML
1. Fetch standard sitemap locations in order: `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap.gz`, `/sitemap_index.gz`
2. For each: fetch, decompress if `.gz`, parse XML `urlset/url/loc` (or `sitemapindex/sitemap/loc` for index)
3. If index: recurse into referenced sitemaps (max depth 2)
4. Filter URLs for state-item patterns

### 5.3 ON_SITE_SEARCH
1. Identify search endpoint: parse seed page for `<form>` with `action` containing `search`/`query`/`q`, or well-known paths `/search`, `/query`, `/search/`, OpenSearch description document
2. Extract query parameter name (from form `input[name]` or URL pattern)
3. For each DEEP item: construct query from item's identifier (title, path segment, control name)
4. Issue GET to search endpoint with query parameter
5. Parse results page for links (static `<a href>`), filter for state-item patterns
6. Verify candidate by fetching (counts as item-page GET)

### 5.4 RSS_ATOM
1. Fetch standard feed locations: `/feed`, `/rss`, `/atom.xml`, `/rss.xml`, `/feed.xml`, `/index.xml`
2. Parse as RSS 2.0 (`channel/item/link`, `channel/item/guid`) or Atom (`feed/entry/link/@href`, `feed/entry/id`)
3. Filter URLs for state-item patterns

### 5.5 JSON_LD
1. Fetch seed homepage and top-level section pages (discovered in hop-confirmation crawl, max 10 pages)
2. Extract all `<script type="application/ld+json">` blocks
3. Parse JSON; traverse `@graph` (array) or root object for `@id`, `url`, `mainEntityOfPage`, `itemListElement` entries
4. Filter URLs for state-item patterns

### 5.6 State-Item URL Pattern Filtering (Frozen)
A candidate URL is a **state-item candidate** iff:
- Same hostname as seed (exact equality)
- Path contains at least one segment matching: `item`, `product`, `page`, `post`, `article`, `doc`, `guide`, `tutorial`, `reference`, `api`, `resource`, `entry`, `node`, `entity`, `object`, `record`, `detail`, `view`, `show`, `display`
- OR path ends with `.html`, `.htm`, `.php`, `.asp`, `.aspx`, `.jsp` (common dynamic page extensions)
- OR query string contains `id=`, `item=`, `product=`, `page=`, `slug=`, `path=`
- **Exclusion**: Asset extensions (Section 4.2), fragment-only (`#`), mailto:, javascript:, tel:, data:, ftp:, file:

### 5.7 K=3 GET Budget Breakdown (Frozen)
- **GET 1**: Discovery channel fetch (robots.txt, sitemap.xml, search results, feed, or JSON-LD page)
- **GET 2**: Item-page fetch (candidate URL from discovery)
- **GET 3**: Spare (redirect follow, validation re-fetch, or second discovery channel if first yields no candidates)
- **Hard Cap**: No item may consume more than 3 GETs total across all channels combined

### 5.8 Channel Execution Order (Frozen)
For each DEEP item, channels are attempted in order: ROBOTS_SITEMAP → SITEMAP_XML → ON_SITE_SEARCH → RSS_ATOM → JSON_LD. The first channel that yields a verified reachable item page (HTTP 200, contains named form control) within the remaining K budget wins. Channels exhausted without success = item not discovery-reachable.

---

## 6. Baselines (Frozen Identities for Downstream Transmission)

| Baseline ID | Description | Expected DEEP Reachability | Cost Model |
|-------------|-------------|---------------------------|------------|
| `COLD_BASELINE` | Fresh agent, no discovery, direct URL only if known a priori | 0% (URL unknown) | 1 GET if URL provided, else ∞ |
| `SHORTEST_PATH_BASELINE` | Link-following BFS (frozen policy, Section 4.2) | 100% (by admission definition) | hop+1 GETs |
| `RANDOM_DISCOVERY_BASELINE` | Discovery channel assignment shuffled across items (null) | ≈0% | ≤3 GETs (wasted) |

---

## 7. Treatment Arm

**DISCOVERY_TREATMENT**: Site-native discovery channels (Section 5) with K=3 GET budget per item. Acquisition mechanism is fundamentally different from link-following: uses site-provided structured navigation (sitemaps, feeds, search, structured data) rather than graph traversal.

---

## 8. Controls (Frozen Identities, Must PASS During DESIGN for Freeze)

### 8.1 POS_DISCOVERY_REACHABLE (Positive Control)
- **Definition**: A DEEP item confirmed during DESIGN to be reachable in <=K=3 GETs via at least one frozen discovery channel on at least one engine.
- **Verification**: Live probe during pre-freeze attainability certificate construction.
- **Pass Criterion**: `reachable_in_k == true AND k_used <= 3`
- **Required for Freeze**: YES — freeze proceeds ONLY if this control passes.

### 8.2 NEG_DISCOVERY_UNREACHABLE (Negative Control)
- **Definition**: Synthetic item URL known not to exist on any target host (e.g., `/__spider_nonexistent_38085197666__.html`).
- **Verification**: Discovery channels probed during DESIGN; must NOT report it as reachable.
- **Pass Criterion**: `reachable_in_k == false`
- **Required for Freeze**: YES

### 8.3 CALIBRATION_NEAR (Dynamic-Range Control: FLAT)
- **Definition**: NEAR (hop<=1) items from the admitted pool. These should have high discovery reachability because they are prominent/linked from homepage.
- **Expected**: `discovery_reachable_fraction_NEAR >= 0.80` on >=2 engines
- **Purpose**: Fires if discovery systematically fails even for easy items.
- **Required for Freeze**: YES (recorded in certificate, not a freeze gate)

### 8.4 CALIBRATION_DEEP_LINK (Dynamic-Range Control: GROWING)
- **Definition**: DEEP items from the admitted pool, measured via SHORTEST_PATH_BASELINE (link-following BFS).
- **Expected**: 100% reachable at cost = hop+1 GETs (by admission gate definition).
- **Purpose**: Fires if hop confirmation is wrong or BFS policy changed.
- **Required for Freeze**: YES (recorded in certificate)

### 8.4 RANDOM_DISCOVERY_BASELINE (Null Control)
- **Definition**: Discovery channel assignment randomly permuted across DEEP items (same channels, same K budget, wrong item-channel pairing).
- **Expected**: Near-zero reachability.
- **Purpose**: Measures chance alignment; must be << treatment effect.
- **Required for Freeze**: YES (recorded in certificate)

---

## 9. Pre-Freeze Attainability Certificate (Mandatory for Freeze)

The following **MUST** be verified and recorded in `spec.json#pre_freeze_attainability_certificate` with evidence refs BEFORE `freeze.json` is created. Freeze proceeds ONLY if all items are verified.

| Certificate Item | Verification Method | Evidence Ref |
|------------------|---------------------|--------------|
| `candidate_seeds_curated` | Manual curation of >=10 candidate seeds spanning >=4 distinct hosts/engines | `seeds.json` |
| `hop_confirmation_crawl_run` | Execute frozen same-host BFS (depth<=6, budget 250, 2 sessions) on all seeds | `raw/hop_confirmation.jsonl` |
| `deep_items_admitted_per_engine` | Count admitted DEEP items per engine (session-agreed) | `derived/admission.json` |
| `distinct_engines_with_deep_ge_3` | Count engines with |D_e| >= 3 | `derived/admission.json` |
| `total_deep_items_ge_10` | Sum |D_e| across engines >= 10 | `derived/admission.json` |
| `probeable_discovery_channel_per_engine` | For each engine with |D_e|>=3, at least 1 channel yields >=1 candidate URL | `raw/discovery_probes.jsonl` |
| `positive_control_verified` | POS_DISCOVERY_REACHABLE passes live probe | `raw/controls.jsonl` |
| `negative_control_verified` | NEG_DISCOVERY_UNREACHABLE passes live probe | `raw/controls.jsonl` |
| `null_control_verified` | RANDOM_DISCOVERY_BASELINE probed | `raw/controls.jsonl` |
| `prereg_section_18_decisions_resolved` | All 7 decisions resolved and frozen in spec.json | `spec.json#prereg_section_18_decisions` |

**Admission Gate for Freeze** (ADMISSION_GATE_V2):
- `admitted_DEEP_items >= 10`
- `distinct_engines_with_deep_ge_3 >= 2`
- `positive_control_verified == true`
- `negative_control_verified == true`
- All 7 prereg section 18 decisions resolved

---

## 10. Prereg Section 18 Design Decisions (Resolved During DESIGN, Frozen in spec.json)

1. **final_seed_list_with_hostnames**: Exact list of (seed_label, seed_url, engine_name, hostname) tuples. Frozen in `seeds.json`.
2. **synthetic_identifier_format_for_search_queries**: Format: `{control_name}_{page_path_segment}`. For items without controls: `{page_title_slug}`. Frozen in `spec.json#identifier_format`.
3. **search_query_parameter_mapping_per_site**: Per-site mapping of search endpoint URL and query parameter name. Discovered during DESIGN, frozen in `seeds.json#search_config`.
4. **json_ld_vocabulary_scope**: Accept `@type` ∈ {Product, Article, WebPage, ItemPage, Dataset, SoftwareApplication, Course, HowTo, FAQPage, QAPage, ItemList}. Reject others. Frozen in `spec.json#json_ld_vocabulary`.
5. **sitemap_gz_handling**: Decompress via `gzip.GzipFile`; parse as XML; on parse error, skip that sitemap (record as channel-unavailable for that seed). Frozen in `spec.json#sitemap_gz_policy`.
6. **redirect_accounting_in_k_budget**: Redirects followed automatically by stdlib count as 0 additional GETs (single `urlopen` call). Only explicit re-fetch for validation counts as spare GET. Frozen in `spec.json#redirect_policy`.
7. **engine_definition_and_distinctness_criterion**: Engine = (CMS/platform fingerprint, e.g., mdBook, WordPress, custom, phpBB, Hugo, Sphinx, Jekyll, Docusaurus, GitBook, MkDocs). Distinctness = different engine_name string. Hostname may be shared (e.g., doc.rust-lang.org hosts mdBook only). Frozen in `seeds.json#engine_definitions`.

---

## 11. Metrics (Stable Identities for Downstream Transmission)

### 11.1 Primary Metric
- `discovery_reachable_fraction_per_engine`: Object mapping engine_name → fraction (|R_e| / |D_e|)
- `primary_verdict`: "FLAT" or "GROWING" (per decision rule)
- `engines_meeting_threshold`: List of engine names where fraction >= 0.50

### 11.2 Secondary Metrics
- `discovery_reachable_fraction_overall`: Total reachable DEEP / total DEEP across all engines
- `acquisition_cost_per_hop_discovery`: For each hop band, median GETs and bytes via discovery treatment
- `acquisition_cost_per_hop_shortest_path`: For each hop band, median GETs and bytes via SHORTEST_PATH_BASELINE
- `acquisition_cost_per_hop_cold`: For each hop band, median GETs and bytes via COLD_BASELINE
- `discovery_channel_effectiveness`: Per-channel reachability count and fraction
- `k_get_distribution`: Histogram of GETs used per successful discovery (1, 2, or 3)
- `session_agreement`: Fraction of items with identical reachability verdict across 2 sessions
- `admission_gate`: Copy of ADMISSION_GATE_V2 observed values

### 11.3 Control Metrics
- `controls.POS_DISCOVERY_REACHABLE.pass`: boolean
- `controls.NEG_DISCOVERY_UNREACHABLE.pass`: boolean
- `controls.CALIBRATION_NEAR.fraction`: float
- `controls.CALIBRATION_DEEP_LINK.fraction`: float
- `controls.RANDOM_DISCOVERY_BASELINE.fraction`: float

---

## 12. Validity Threats & Representation Losses (Explicit)

1. **Static Parser Only**: JavaScript-rendered links, SPA routes, dynamic sitemaps, and JS-based search are invisible. This systematically *underestimates* discovery reachability (conservative for FLAT verdict).
2. **No Authentication**: Gated/private content inaccessible. Items behind login are not in the admitted pool (hop confirmation would not reach them).
3. **robots.txt Compliance**: Discovery channels respect `Disallow`; crawl policy follows same-host `<a>` only. If a site blocks sitemap/feed discovery but allows crawling, discovery is disadvantaged.
4. **Sitemap.gz Errors**: Parse errors cause channel skip for that sitemap (recorded as unavailable).
5. **On-Site Search Limitations**: Sites without identifiable search forms, with opaque JS search, or requiring POST are channel-unavailable (not a failure).
6. **JSON-LD Scope**: Only inline `<script type="application/ld+json">` on fetched pages; external references (`@id` URLs) not followed.
7. **K=3 Budget Rigidity**: Some discoveries may need 4 GETs (e.g., sitemap index → sitemap → item page → validation). These count as failures (conservative).
8. **Single-Hop Discovery**: Chained discovery (discovery channel → intermediate page → another discovery channel) not allowed within K=3.
9. **Engine Fingerprinting Heuristic**: Engine detection via meta tags, generator headers, path patterns. May misclassify. Distinctness by engine_name string is the frozen criterion.

---

## 13. Execution Phases (Frozen)

### Phase 0: Preflight (Immutable)
- Verify frozen input hashes (`request.json`, `spec.json`, `prereg.md`, `freeze.json`)
- Record environment (Python version, platform, network reachability to all seeds)
- Verify pre-freeze attainability certificate matches spec.json

### Phase 1: Controls (Live Verification)
- Execute all 5 controls (POS, NEG, CAL_NEAR, CAL_DEEP_LINK, RANDOM)
- Record pass/fail with evidence refs
- **Any control FAIL → status=BLOCKED, outcome=NOT_APPLICABLE** (design defect, not measurement)

### Phase 2: Structural Crawl (Hop Confirmation — Re-Run)
- Re-run frozen same-host BFS on all admitted seeds (2 sessions each)
- Verify session agreement on admitted DEEP/NEAR items
- Items without session agreement → excluded (recorded)

### Phase 3: Discovery Treatment
- For each admitted DEEP item: attempt 5 discovery channels in fixed order within K=3 budget
- Record: channel used, GETs consumed, success/failure, final URL, response status
- For NEAR items: same procedure (for CALIBRATION_NEAR)

### Phase 4: Baseline Measurements
- SHORTEST_PATH_BASELINE: cost = hop+1 GETs (from Phase 2 parent pointers)
- COLD_BASELINE: 0 GETs (URL unknown by construction)
- RANDOM_DISCOVERY_BASELINE: permuted channel assignment

### Phase 5: Metrics Computation
- Compute all metrics in Section 11
- Apply decision rule → primary_verdict
- Write `derived/metrics.json`, `derived/implementation_choices.json`

---

## 14. Decision Rule Application (Frozen, No Discretion)

```python
def apply_decision_rule(metrics):
    fractions = metrics["discovery_reachable_fraction_per_engine"]
    engines_meeting = [e for e, f in fractions.items() if f >= 0.50]
    if len(engines_meeting) >= 2:
        return "FLAT"
    else:
        return "GROWING"
```

**No post-hoc analysis, no threshold adjustment, no engine redefinition after seeing outcomes.**

---

## 15. Outcome Consequences (Pre-Registered)

| Verdict | Claim Update | Product Action | Next Question |
|---------|-------------|----------------|---------------|
| FLAT | C-CROSSSITE: EXPERIMENTAL (survives cross-engine test)<br>C-RESIDUAL-NOVELTY: EXPERIMENTAL (discovery enables O(1) deep acquisition)<br>C-WEB-DYNAMICS: HYPOTHESIS (site-provided structure is a dynamical regularity) | Shift architecture from path-persistence to discovery-persistence.<br>Invest in: discovery procedure caching, substrate expansion, cross-episode freshness. | How does discovery freshness/invalidation cost scale with hop and elapsed time? (Maintenance/invalidation axis) |
| GROWING | C-CROSSSITE: HYPOTHESIS (cross-engine discovery not sufficient)<br>C-RESIDUAL-NOVELTY: EXPERIMENTAL (path-bound confirmed)<br>C-WEB-DYNAMICS: HYPOTHESIS (no new dynamical structure) | Validate path-persistence investment.<br>Prioritize: delta repair, freshness guards, break-even from real re-derivation costs. | What is the persistence break-even surface (re-validation cost + stale-replay false-accept rate vs. re-derivation cost) as a function of hop and time? |

---

## 16. Cheap Pre-Freeze Satisfiability Probes (Design-Contract v2 Requirement)

The following probes are executed **during DESIGN** (before spec.json is finalized) to verify the design is satisfiable. They are NOT outcome-bearing measurements.

1. **Seed Reachability Probe**: TCP/HTTPS connectivity to all candidate seeds (4s timeout). All must succeed.
2. **Hop Confirmation Probe**: Run frozen BFS on 2 candidate seeds (1 session each) to confirm DEEP items exist and session agreement works.
3. **Discovery Channel Probe**: For 2 candidate seeds, probe all 5 channels; confirm at least 1 channel yields candidates per engine.
4. **Positive Control Probe**: Verify POS_DISCOVERY_REACHABLE item is actually reachable in <=3 GETs.
5. **Negative Control Probe**: Verify NEG_DISCOVERY_UNREACHABLE is not reachable.
6. **Code Path Probe**: Import all freeze_artifacts modules; verify no syntax errors, no missing stdlib dependencies.
7. **Arithmetic Probe**: Confirm decision rule denominator > 0 for >=2 engines with current admitted DEEP counts.

**All probes must PASS for DESIGN to finalize.** Any FAIL → DESIGN revision required (not a scientific result).

---

## 17. Independent Design Review (Design-Contract v2 Requirement)

Before freeze, an independent DESIGN REVIEW agent must emit `design_review.json` attacking the six freeze_eligibility checks and the satisfiability of the design. The review must confirm:
- No empty/unreachable decision branches
- No missing prerequisites
- No treatment/comparator identity
- No ceiling/floor baselines
- No insensitive controls
- No unbound mutable artifacts
- The pre-freeze attainability certificate is constructible with current infrastructure

The DESIGN agent does not proceed to freeze until `design_review.json` exists and all checks are PASS.

---

## 18. Comparison with Pre-2.0 Precedents (LEGACY: DISTINCT_EXTENSION)

Per `codex/legacy_brief.json` and Director mandate comparative reasoning:

- **P2-MIND2WEB** (retrieval 47/176 = 26.7%): Measures *retrieval* from human demonstrations, not *site-native discovery reachability* or *acquisition cost vs hop depth*. Different substrate, different mechanism, different metric.
- **P2-WP002B** (no website-holdout result): Measures next-state prediction accuracy, not discovery-channel reachability.
- **Intel discovery artifacts** (cycle5 `discovery_checks.json`, cycle6 manifests): Reproduction/route captures on specific sites, not a controlled multi-engine DEEP pool with frozen discovery channels and a two-sided hop-cost falsifier.
- **EXP-FRONTIER-37950626378**: Measured link-following acquisition cost (GROWING, but estimator-bound). This experiment changes the *acquisition mechanism* to site-native discovery — orthogonal and decision-changing.
- **EXP-FRONTIER-37984242167**: Same mandate, but v1 freeze committed empty sampling frame (0 seeds, 0 DEEP, 0 hosts). This v2 redesign adds the pre-freeze attainability certificate and six freeze_eligibility checks to make the question falsifiable in both directions.

**This is a DISTINCT_EXTENSION**: new mechanism (discovery vs. link-following), new metric (discovery_reachable_fraction vs. RED/RACQ ratio), new falsifier (two-sided materiality threshold on multi-engine DEEP pool), and a v2 design-contract that prevents the empty-frame control-plane defect.

---

## 19. Post-Freeze Change Prohibition

Per `research/EXPERIMENT_PACKET.md` Section 19 and SPIDER_MASTER_PROMPT.md Section 19: **No confirmatory analysis may change after seeing outcomes.** Any post-freeze modification to the decision rule, threshold, channel definitions, K budget, engine definitions, or admission criteria renders confirmatory claims exploratory. A new confirmatory claim requires a new preregistration and untouched evidence.

---

## 20. Evidence References (For Downstream Transmission)

All raw evidence will be written to `research/experiments/EXP-FRONTIER-38085197666/raw/`:
- `http.jsonl`: Every HTTP GET with metadata (URL, status, bytes, headers, hash, elapsed)
- `controls.jsonl`: Control execution records
- `hop_confirmation.jsonl`: Phase 2 BFS crawl records
- `discovery_probes.jsonl`: Phase 3 discovery channel attempts
- `observations.jsonl`: Admitted items with hop, band, engine, session agreement

All derived evidence to `derived/`:
- `metrics.json`: All metrics (Section 11)
- `implementation_choices.json`: Ambiguity resolutions
- `admission.json`: Admission gate details

Provenance to `provenance.json`: Git commit, run ID, environment, code paths, artifact hashes.

---

**End of Preregistration**