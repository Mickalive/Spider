# Preregistration: EXP-FRONTIER-37984242167
## Site-Native Discovery vs Link-Following for Deep-Item Acquisition

**Experiment ID:** EXP-FRONTIER-37984242167
**Lane:** frontier
**Claim IDs:** C-RESIDUAL-NOVELTY, C-WEB-DYNAMICS
**Date:** 2026-10-09
**Status:** PREREGISTERED (pre-freeze)

---

## 1. Scientific Question

On the credential-free GET-only stdlib-HTTP substrate established by EXP-FRONTIER-37950626378, does changing the acquisition **MECHANISM** from same-host link-following BFS to **SITE-NATIVE DISCOVERY CHANNELS** (robots.txt sitemap directives, sitemap.xml, on-site search/query URLs, RSS/Atom feeds, JSON-LD/structured-data enumeration) allow a fresh agent to reach **DEEP (hop≥3) state items in O(1) GETs** (K≤3: one discovery GET + item-page GET + one spare for redirect/validation) on a frozen multi-host pool **separately confirmed** to contain DEEP items on at least two distinct hosts/engines?

---

## 2. Hypothesis

**Primary Hypothesis (H1):** Site-native discovery channels provide O(1) reachability for a material fraction (≥50%) of DEEP state items on at least two distinct hosts/engines. This would demonstrate that shortest-path hop is **not a fundamental acquisition-cost barrier** for discovery-enabled acquisition. Consequently, persistent path/procedure caching is not the primary optimization target; research and product effort should shift to discovery-channel coverage and substrate expansion.

**Alternative Hypothesis (H0):** Even with site-native discovery, fresh deep-instance acquisition remains **path-bound** (O(1) reachability fraction <50% on fewer than two engines). Persistence of paths/procedures retains a measurable, depth-dependent amortization surface whose break-even can be computed from real re-derivation cost.

---

## 3. Falsifier (Two-Sided, Arithmetically Checkable Before Freeze)

| Condition | Outcome | Interpretation |
|-----------|---------|----------------|
| `discovery_reachable_fraction ≥ 0.50` on **≥2 distinct hosts/engines** | **SUPPORTS (H1)** | Depth is not a fundamental barrier. Discovery collapses acquisition cost. Persistence is not the optimization target. |
| `discovery_reachable_fraction < 0.50` on **≥2 distinct hosts/engines** | **FALSIFIES (H0)** | Depth remains a barrier even with discovery. Path persistence has a real amortization surface. |
| Threshold met on exactly 1 engine, or pool has <2 engines with DEEP items | **MIXED** | Cross-engine contrast unmeasured. Inconclusive for program-level decision. |
| Admission gate fails (<10 total DEEP items) or validity gates fail | **INCONCLUSIVE** | Measurement invalid; no claim update. |

**Key Parameters (Frozen at Design):**
- Materiality threshold: **0.50** (50% of DEEP items)
- Minimum engines: **2** distinct hosts/engines
- K-GET budget: **3** (1 discovery + 1 item-page + 1 spare)
- Discovery channels: **5** (defined in §5)

**Per-Channel Disclosure Requirement:** Must report `discovery_reachable_fraction_per_channel[channel]` for each of the 5 channels, and explicitly list any channel yielding **zero admitted DEEP items** (not counted as null).

---

## 4. Substrate & Constraints (Identical to Parent)

| Constraint | Value |
|------------|-------|
| Protocol | Credential-free GET-only, stdlib HTTP (`urllib`/`requests`) |
| No browser | No Playwright, Selenium, Docker |
| No auth | No cookies, tokens, API keys, write verbs |
| No tokenizer | `tiktoken` not available; token fields = `null` |
| Cost bases | GET request count + response-body bytes only |
| Parser | Stdlib `html.parser` / regex only; **no JS rendering** |
| Concurrency | Sequential, polite (respect `robots.txt` crawl-delay) |
| Episode isolation | Fresh episode per item-channel probe (no cross-item caching) |

---

## 5. Discovery Channels (Frozen Definitions)

### 5.1 ROBOTS_SITEMAP
1. Fetch `robots.txt` from host root
2. Extract `Sitemap:` directive URLs
3. Fetch each sitemap URL
4. Parse XML for `<url><loc>` entries
5. Match against admitted DEEP item URLs (exact or prefix match)

### 5.2 SITEMAP_XML
1. Directly fetch `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap.gz`
2. Parse XML (handle sitemap index recursion)
3. Extract `<url><loc>` entries
4. Match against admitted DEEP item URLs

### 5.3 ON_SITE_SEARCH
1. Fetch host root HTML
2. Locate `<form>` with search-like attributes (`action` containing `search`, `query`, `q`; `<input name=q|query|search>`)
3. Construct query URL: `action?param=ITEM_IDENTIFIER` (identifier = last path segment of DEEP item URL)
4. Fetch results page
5. Parse `<a href>` links from results
6. Match against admitted DEEP item URLs

### 5.4 RSS_ATOM
1. Fetch host root HTML
2. Find `<link rel="alternate" type="application/rss+xml|application/atom+xml" href="...">`
3. Fetch feed URL
4. Parse XML for `<item><link>` or `<entry><link href="...">`
5. Match against admitted DEEP item URLs

### 5.5 JSON_LD
1. For each admitted DEEP item URL, fetch the item page HTML
2. Find `<script type="application/ld+json">` blocks
3. Parse JSON-LD for `@type` in `Product`, `Article`, `WebPage`, `ItemPage`, `Dataset`, etc.
4. Extract `url`, `mainEntityOfPage`, `@id`, or similar URL properties
5. Match against admitted DEEP item URLs (self-discovery validation)

---

## 6. Target Pool & Admission Gate (ADMISSION_GATE_V2)

### 6.1 Pool Construction (During DESIGN, Before Freeze)
1. **Candidate seeds:** Curated list of public documentation/sites known to have deep hierarchical structure (e.g., multiple mdBook/Sphinx/Docusaurus sites, large wikis, API references).
2. **Hop-confirmation crawl:** For each seed, run link-following BFS (static `<a href>`, same-host, depth≤6, budget 250 GETs) — **identical to EXP-FRONTIER-37950626378 RED arm**.
3. **DEEP admission:** Items at hop≥3 are "admitted DEEP items".
4. **Pool freeze:** The set of seeds, admitted DEEP items, and their hop depths are frozen in `spec.json.target_pool.confirmed_deep_items`.

### 6.2 Admission Gate Criteria (Must Pass Before Freeze)
- **Total admitted DEEP items ≥ 10** across all hosts
- **≥2 distinct hosts/engines** each with **≥3 admitted DEEP items**
- If gate fails: cross-engine contrast reported as **unmeasured**, not FLAT. Experiment proceeds only if gate passes.

### 6.3 Engine/Host Definition
- "Distinct host/engine" = distinct base domain (e.g., `doc.rust-lang.org` vs `docs.python.org`) OR distinct generator fingerprint (mdBook vs Sphinx vs Docusaurus) on same domain.
- Determined by: generator meta tag, HTML structure fingerprint, or manual classification during DESIGN.

---

## 7. Measurement Procedure (EXECUTE Phase)

For each **admitted DEEP item** in the frozen pool:

### 7.1 Hop Confirmation (Baseline)
- Re-run the link-following BFS from the seed to confirm hop depth (must match DESIGN value ±0).
- Record: `hop_depth`, `shortest_path_urls`, `RED_requests`, `RED_bytes`.

### 7.2 Discovery Probing (Per Channel)
For each of the 5 discovery channels:
1. Execute channel-specific discovery steps ( §5 )
2. Count GETs used: `discovery_GETs` (sitemap/feed/search/JSON-LD fetch) + `item_page_GET` (1) + `redirect_validation_GETs` (0-1)
3. **Success criterion:** Item URL discovered **AND** item page fetched with 2xx status within **K=3 total GETs**.
4. Record per-channel: `channel_success[bool]`, `channel_GETs_used[int]`, `channel_bytes[int]`, `discovered_via[channel_name]`.

### 7.3 Aggregation
- `item_reachable_via_discovery = OR(channel_success across 5 channels)`
- `item_discovery_GETs = min(channel_GETs_used where success) if any_success else null`
- `item_discovery_bytes = corresponding bytes`

### 7.4 Null Control
- For each channel, probe 2 synthetic item identifiers ( §Null Control )
- Record: `null_channel_success[bool]` (expected: all false)

---

## 8. Metrics (Stable Identifiers for Downstream)

| Metric ID | Definition | Unit |
|-----------|------------|------|
| `discovery_reachable_fraction` | `count(items with item_reachable_via_discovery=true) / count(admitted DEEP items)` | proportion [0,1] |
| `discovery_reachable_fraction_per_engine[host]` | Same fraction computed per distinct host/engine | proportion [0,1] |
| `discovery_reachable_fraction_per_channel[channel]` | Fraction reachable via each specific channel | proportion [0,1] |
| `median_discovery_GETs_reachable` | Median `item_discovery_GETs` over reachable items | GETs |
| `median_discovery_bytes_reachable` | Median `item_discovery_bytes` over reachable items | bytes |
| `hop_depth_distribution` | Distribution of confirmed hop depths for admitted DEEP items | hop (int) |
| `RED_requests_vs_discovery_GETs` | Paired comparison: `RED_requests` vs `item_discovery_GETs` for same items | GETs ratio |
| `channels_with_zero_deep[channel]` | Boolean: channel yielded 0 admitted DEEP items | bool |
| `null_control_false_positive_rate[channel]` | `count(null_success=true) / count(null_probes)` per channel | proportion [0,1] |

---

## 9. Controls (Stable Identifiers)

| Control ID | Type | Pass Criterion |
|------------|------|----------------|
| `PC_DISCOVERY_CHANNEL_REACHABILITY` | Positive | ≥1 channel probeable on ≥1 host (live evidence in `pre_freeze_control_certificate`) |
| `NC_SYNTHETIC_UNREACHABLE_ITEM` | Null | All channels return 0 reachable URLs for synthetic items |
| `B_LINK_FOLLOWING_BFS` | Baseline | Hop depths match DESIGN confirmation crawl |
| `B_PERSISTED_PATH_REACQUISITION` | Baseline | `RACQ_PATH.requests ≈ hop+1` (from parent) |
| `B_DIRECT_URL_REPLAY` | Baseline | `RACQ_URL.requests = 1` (from parent) |

---

## 10. Measurement Validity Threats (Disclosed)

| ID | Threat | Mitigation / Disclosure |
|----|--------|-------------------------|
| VN-V1 | Substrate limited to static GET | Declared scope; no browser/JS/auth |
| VN-V2 | Pool may not yield ≥2 engines with DEEP | Admission gate; report unmeasured if fails |
| VN-V3 | Channels miss JS-rendered discovery | Static parser only; disclosed as representation loss |
| VN-V4 | K=3 may be too tight/loose | Preregistered; sensitivity in `unresolved` |
| VN-V5 | Hop confirmation uses same BFS as parent | Identical code path; distinct observable |
| VN-V6 | Channels not independent (e.g., sitemap in robots.txt) | Report per-channel + union; disclose overlap |
| VN-V7 | No token/latency/$ cost | Only GETs + bytes measured; tokens=null |
| VN-V8 | Single-episode (no cross-item caching) | Measures fresh-agent cost; amortization separate |
| VN-V9 | Attainability certificate required pre-freeze | `pre_freeze_control_certificate` in spec.json |
| VN-V10 | Synthetic items may accidentally exist | Use randomized suffixes; verify 404 on item page |

---

## 11. Decision Rule (Formal)

```python
def apply_decision_rule(metrics, admission_gate_pass):
    if not admission_gate_pass:
        return "INCONCLUSIVE", "admission_gate_failed"
    
    engines_meeting_threshold = sum(
        1 for host, frac in metrics["discovery_reachable_fraction_per_engine"].items()
        if frac >= 0.50
    )
    
    if engines_meeting_threshold >= 2:
        return "SUPPORTS", f"{engines_meeting_threshold} engines >= 0.50"
    elif engines_meeting_threshold == 1:
        return "MIXED", "threshold met on exactly 1 engine"
    else:
        return "FALSIFIES", f"{engines_meeting_threshold} engines >= 0.50"
```

**Admission Gate (ADMISSION_GATE_V2):**
- `total_deep_items >= 10`
- `len(hosts_with_deep >= 3) >= 2`

---

## 12. Product Consequences

### If SUPPORTS (Discovery Collapses Depth Cost)
1. **Architectural pivot:** SPIDER's memory layer should optimize for **discovery-channel coverage** and **substrate expansion**, not path/procedure persistence.
2. **C-RESIDUAL-NOVELTY** gains support: "pay for novelty" applies to acquisition — deep novelty can be O(1) if discovery works.
3. **Frontier priority:** Discovery-channel generalization, cross-engine substrate scaling, hybrid discovery+traversal for uncovered items.
4. **Graph/Runtime/Product:** Freshness (C-FRESHNESS) and delta repair (C-DELTA-REPAIR) become lower priority for acquisition; shift to discovery freshness.

### If FALSIFIES (Depth Remains a Barrier)
1. **Architectural validation:** Path/procedure persistence **is** the correct optimization target.
2. **Break-even surface:** Compute real re-derivation cost from `RACQ_PATH` vs `discovery_GETs` — provides quantitative amortization economics.
3. **C-RESIDUAL-NOVELTY** supported for the *execution* phase (novelty = residual after discovery), but acquisition cost scales with depth.
4. **Frontier priority:** Improve discovery recall, hybrid strategies, or accept depth-cost as fundamental.
5. **Graph/Runtime/Product:** Freshness guards and delta repair remain high priority for persisted paths.

### If MIXED / INCONCLUSIVE
- No program-level decision change. Next experiment must resolve the cross-engine contrast (larger pool, different sites) or improve discovery-channel coverage.

---

## 13. Estimated Cost & Information Gain

| Resource | Estimate |
|----------|----------|
| HTTP GETs | 500–2,000 (pool: ~50–100 DEEP × 5 channels × ≤3 GETs + hop confirmation) |
| Wall time | ~30 minutes (sequential, polite) |
| Compute | Negligible (stdlib only) |
| External deps | Public HTTP endpoints only; no keys/credentials |

**Expected Information Gain: HIGH.** This experiment directly tests the **depth-cost premise** motivating SPIDER's entire persistence architecture. A positive result redirects the program from path persistence → discovery/substrate. A negative result validates persistence and provides a real break-even surface. Either outcome changes a program-level architectural decision.

---

## 14. Pre-Freeze Control Certificate (Must Be Completed During DESIGN)

The following **must be verified live and recorded in `spec.json.pre_freeze_control_certificate`** before `freeze.json` is created:

1. **Pool DEEP confirmation:** Hop-confirmation crawl on frozen seeds admits ≥10 DEEP items total, with ≥2 hosts having ≥3 DEEP each. Evidence: raw crawl logs, admitted item list.
2. **Discovery channel probe:** At least one channel ( §5 ) returns 200 + parsable content with ≥1 URL entry on at least one host. Evidence: HTTP response, parsed entry count.
3. **Null control:** Synthetic item probes return 0 reachable URLs on all channels. Evidence: probe results.

**Freeze proceeds ONLY if all three are verified.** If any fails, DESIGN must revise pool/channels or report INCONCLUSIVE.

---

## 15. Inherited State from Parent (EXP-FRONTIER-37950626378)

Per `handoff.json` four-way distinction:

### Established (Carry Forward)
- Frozen measurement transaction valid; GROWING branch returned (R_req=5.27, R_bytes=7.31 at M=3.0)
- All four controls live-PASS; admission gate PASS (26 DEEP / 419 NEAR / 4 hosts)
- Persisted-path re-acquisition near-linear (hop+1); direct URL replay = 1 GET
- GROWING ratio is **estimator-forced** (RED ≥ RACQ_PATH by construction; VF-03)
- DEEP band is **single-host/single-engine** (doc.rust-lang.org mdBook only)
- No token/latency/$ cost measured (tiktoken absent)
- Break-even counts <<1 are ordering proof, not economics (VF-04)

### Rejected (Do Not Re-litigate)
- GROWING ratio as independent Web-economics evidence
- FLAT branch as established (only on detour-free chain R=2.0)
- Break-even counts as economics
- Generalization beyond mdBook, static <a href>, GET-only, B=250/D=6
- This result closes C-RESIDUAL-NOVELTY, C-FRESHNESS, C-WEB-DYNAMICS, or persistence architecture

### Unknown (Open Questions)
- Whether GROWING reflects Web structure or BFS estimator branching factor
- Whether non-mdBook hosts admit DEEP items at larger budget
- Real acquisition economics (latency, $, model calls)
- **Whether site-native discovery reaches DEEP in O(1) GETs on ≥2 engines** ← **THIS EXPERIMENT**
- Maintenance/invalidation cost scaling with hop/time
- Cause of Gentoo 1-byte session differences

### Do Not Assume (Dangerous Non-Conclusions)
- Audit PASS ≠ validation of C-RESIDUAL-NOVELTY or depth-growing economics
- GROWING ratio ≠ independent of frozen BFS estimator
- gnu/quotes/gentoo UNDEFINED ≠ FLAT or negative result
- Break-even <<1 ≠ real economics
- No generalization beyond mdBook/static-link/GET-only/B-250/D-6
- No re-run of frozen DEEP/NEAR level-order-BFS ratio as discriminating test
- Handoff/next_question ≠ authorization for child experiment (Global Director mandate required)
- Agent priors / Scout brief / portfolio assessment ≠ SPIDER evidence
- Registry claim status (HYPOTHESIS) ≠ overrides Codex running state (EXPERIMENTAL)

---

## 16. Dependencies & Prerequisites

1. **Global Research Director mandate** (present in `request.json.director_mandate`).
2. **Frozen target pool** with confirmed DEEP items on ≥2 hosts/engines (built during DESIGN).
3. **Pre-freeze control certificate** with live evidence references in `spec.json`.
4. **No new infrastructure:** Credential-free GET-only stdlib HTTP (already established).
5. **Cross-lane:** Graph/Runtime/Product C-FRESHNESS work is adjacent but not a hard dependency (maintenance/invalidation axis is the alternative question).

---

## 17. Evidence References (To Be Populated by EXECUTE)

| Artifact | Path Pattern |
|----------|--------------|
| Raw HTTP logs | `raw/http.jsonl` |
| Raw discovery probes | `raw/discovery_probes.jsonl` |
| Raw hop confirmation | `raw/hop_confirmation.jsonl` |
| Raw null control | `raw/null_control.jsonl` |
| Derived metrics | `derived/metrics.json` |
| Analysis | `derived/analysis.json` |
| Implementation choices | `derived/implementation_choices.json` |
| Controls verification | `raw/controls.jsonl` |

---

## 18. Unresolved / Open Design Decisions (To Be Closed Before Freeze)

- [ ] Final seed URL list for target pool (must yield ≥2 engines with DEEP)
- [ ] Exact synthetic item identifier format (randomized suffix strategy)
- [ ] Search query parameter mapping per host (may need host-specific tuning)
- [ ] JSON-LD @type vocabulary to match (Product, Article, ItemPage, etc.)
- [ ] Handling of sitemap.gz (gzip decompression in stdlib)
- [ ] Redirect handling in K=3 budget (count as 1 GET or 2?)
- [ ] Definition of "distinct engine" for multi-generator same-domain sites

**All must be resolved and frozen in `spec.json` before `freeze.json` is created.**

---

## 19. Commitment

This preregistration is **frozen** upon creation of `freeze.json`. No changes to hypothesis, channels, K, threshold, pool, decision rule, or metrics are permitted after freeze. Any post-freeze analysis changes render the confirmatory claim exploratory.

**Next step:** Complete DESIGN by populating `spec.json.target_pool`, `spec.json.pre_freeze_control_certificate`, and resolving §18 open decisions. Then deterministic freezer creates `freeze.json`.