# Preregistration: EXP-FRONTIER-38013774272
## Site-Native Discovery vs Link-Following for Deep-Item Acquisition

**Experiment ID:** EXP-FRONTIER-38013774272
**Lane:** frontier
**Claim IDs:** C-RESIDUAL-NOVELTY
**Date:** 2026-10-10
**Status:** PREREGISTERED (pre-freeze)
**Design Contract Version:** 2

---

## 1. Scientific Question

On the credential-free GET-only stdlib-HTTP substrate established by EXP-FRONTIER-37950626378, does changing the acquisition **MECHANISM** from same-host link-following BFS to **SITE-NATIVE DISCOVERY CHANNELS** (robots.txt sitemap directives, sitemap.xml, on-site search/query URLs, RSS/Atom feeds, JSON-LD/structured-data enumeration) allow a fresh agent to reach **DEEP (hop≥3) state items in ≤K=3 GETs** (one discovery GET + item-page GET + one spare for redirect/validation) on a frozen multi-host pool **separately confirmed** to contain DEEP items on at least three distinct hosts/engines?

---

## 2. Hypothesis

**Primary Hypothesis (H1):** Site-native discovery channels provide ≤K=3 GET reachability for a material fraction (≥50%) of DEEP state items on at least two distinct hosts/engines. This would demonstrate that shortest-path hop is **not a fundamental acquisition-cost barrier** for discovery-enabled acquisition. Consequently, persistent path/procedure caching is not the primary optimization target; research and product effort should shift to discovery-channel coverage and substrate expansion.

**Alternative Hypothesis (H0):** Even with site-native discovery, fresh deep-instance acquisition remains **path-bound** (≤K=3 reachability fraction <50% on fewer than two engines). Persistence of paths/procedures retains a measurable, depth-dependent amortization surface whose break-even can be computed from real re-derivation cost.

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

## 4. Substrate & Constraints (Identical to Parent EXP-FRONTIER-37950626378)

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
3. Fetch each sitemap URL (handle `.gz` with stdlib `gzip`)
4. Parse XML for `<url><loc>` entries
5. Match against admitted DEEP item URLs (exact match)

### 5.2 SITEMAP_XML
1. Directly fetch `/sitemap.xml`, `/sitemap_index.xml`
2. Parse XML (handle sitemap index recursion, handle `.gz`)
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
3. Parse JSON-LD for `@type` in `Product`, `Article`, `WebPage`, `ItemPage`, `Dataset`, `SoftwareSourceCode`, `TechArticle`, `BlogPosting`, etc.
4. Extract `url`, `mainEntityOfPage`, `@id`, or similar URL properties
5. Match against admitted DEEP item URLs (self-discovery validation)

---

## 6. Target Pool & Admission Gate (ADMISSION_GATE_V2)

### 6.1 Pool Construction (During DESIGN, Before Freeze)
1. **Candidate seeds:** Three curated public documentation sites with different engines, confirmed during DESIGN to have DEEP items and working discovery channels:
   - `https://docs.python.org/3/` (Sphinx)
   - `https://developer.mozilla.org/en-US/` (Yari/MDN)
   - `https://redis.io/docs/latest/` (Docusaurus)

2. **Hop-confirmation crawl:** For each seed, run link-following BFS (static `<a href>`, same-host, depth≤6, budget 250 GETs) — **identical to EXP-FRONTIER-37950626378 RED arm**.

3. **DEEP admission:** Items at hop≥3 are "admitted DEEP items".

4. **Pool freeze:** The set of seeds, admitted DEEP items, and their hop depths are frozen in `spec.json.target_pool.confirmed_deep_items` and recorded in `pre_freeze_evidence/pool_deep_confirmation.json`.

### 6.2 Admission Gate Criteria (Must Pass Before Freeze)
- **Total admitted DEEP items ≥ 10** across all hosts (actual: 18,471)
- **≥3 distinct hosts/engines** each with **≥3 admitted DEEP items** (actual: 3 hosts, min 590)
- If gate fails: cross-engine contrast reported as **unmeasured**, not FLAT. Experiment proceeds only if gate passes.

### 6.3 Engine/Host Definition
- "Distinct host/engine" = distinct base domain (e.g., `docs.python.org` vs `developer.mozilla.org`) OR distinct generator fingerprint (Sphinx vs Yari vs Docusaurus) on same domain.
- Determined by: generator meta tag, HTML structure fingerprint, or manual classification during DESIGN.
- Frozen in `spec.json.target_pool.engine_map`.

---

## 7. Measurement Procedure (EXECUTE Phase)

For each **admitted DEEP item** in the frozen pool:

### 7.1 Hop Confirmation (Baseline)
- Re-run the link-following BFS from the seed to confirm hop depth (must match DESIGN value ±0).
- Record: `hop_depth`, `shortest_path_urls`, `RED_requests`, `RED_bytes`.

### 7.2 Discovery Probing (Per Channel)
For each of the 5 discovery channels:
1. Execute channel-specific discovery steps ( §5 )
2. Count GETs used: `discovery_GETs` (sitemap/feed/search/JSON-LD fetch) + `item_page_GET` (1) + `redirect_validation_GETs` (0-1, followed automatically by urllib)
3. **Success criterion:** Item URL discovered **AND** item page fetched with 2xx status within **K=3 total GETs**.
4. Record per-channel: `channel_success[bool]`, `channel_GETs_used[int]`, `channel_bytes[int]`, `discovered_via[channel_name]`.

### 7.3 Aggregation
- `item_reachable_via_discovery = OR(channel_success across 5 channels)`
- `item_discovery_GETs = min(channel_GETs_used where success) if any_success else null`
- `item_discovery_bytes = corresponding bytes`

### 7.4 Null Control
- For each channel, probe 2 synthetic item identifiers per host ( §Null Control )
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
| VN-V11 | sitemap.gz handling | Stdlib gzip decompression; frozen in VN-V11 |
| VN-V12 | Redirect accounting | Each redirect = 1 GET; final 2xx = 1 GET; frozen in VN-V12 |
| VN-V13 | Engine definition | Distinct domain or generator fingerprint; frozen in VN-V13 |
| VN-V14 | Search parameter mapping | Per-host `input name` inspection; frozen in VN-V14 |
| VN-V15 | JSON-LD vocabulary | Product, Article, WebPage, ItemPage, Dataset, SoftwareSourceCode, TechArticle, BlogPosting; frozen in VN-V15 |
| VN-V16 | Synthetic ID format | `spider-nonexistent-item-{8_char_hex}`; frozen in VN-V16 |

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
| HTTP GETs | 1,000–3,000 (pool: ~50–150 DEEP × 5 channels × ≤3 GETs + hop confirmation) |
| Wall time | ~45 minutes (sequential, polite) |
| Compute | Negligible (stdlib only) |
| External deps | Public HTTP endpoints only; no keys/credentials |

**Expected Information Gain: HIGH.** This experiment directly tests the **depth-cost premise** motivating SPIDER's entire persistence architecture. A positive result redirects the program from path persistence → discovery/substrate. A negative result validates persistence and provides a real break-even surface. Either outcome changes a program-level architectural decision.

---

## 14. Pre-Freeze Control Certificate (Completed During DESIGN)

The following **have been verified live and recorded in `spec.json.pre_freeze_control_certificate`** before `freeze.json` creation:

1. **Pool DEEP confirmation:** Hop-confirmation crawl on frozen seeds admits 18,471 DEEP items total, with 3 hosts having ≥3 DEEP each (docs.python.org: 16,190; developer.mozilla.org: 2,291; redis.io: 590). Evidence: `pre_freeze_evidence/pool_deep_confirmation.json`.
2. **Discovery channel probe:** At least 3 channels probeable on each host (docs.python.org: ROBOTS_SITEMAP, SITEMAP_XML, ON_SITE_SEARCH; developer.mozilla.org: ROBOTS_SITEMAP, SITEMAP_XML, RSS_ATOM; redis.io: ROBOTS_SITEMAP, SITEMAP_XML, ON_SITE_SEARCH, JSON_LD). Evidence: `pre_freeze_evidence/channel_probes.json`.
3. **Null control:** Synthetic item probes return 0 reachable URLs on all channels across all hosts. Evidence: `pre_freeze_evidence/null_control.json`.

**All three verified. Freeze proceeds.**

---

## 15. Inherited State from Parent (EXP-FRONTIER-37984242167)

Per `handoff.json` four-way distinction:

### Established (Carry Forward)
- The site-native-discovery question remains **entirely unmeasured**; neither a positive nor negative answer exists.
- The v1 freeze committed an empty sampling frame (0 seeds, 0 DEEP items, 0 hosts), absent pre-freeze control certificate, and 0/0 primary metric unreachable in both falsifier directions.
- The failure is a **control-plane defect with a known repair** (design-contract v2 with freeze_eligibility checks), not a scientific negative.
- Parent EXP-FRONTIER-37950626378 validly measured: persisted-path re-acquisition near-linear (hop+1), direct URL replay = 1 GET, GROWING ratio (R_req=5.27, R_bytes=7.31 at M=3.0) but construct-validity-bounded by BFS estimator.
- DEEP band in parent was single-host/single-engine mdBook; this experiment requires ≥2 engines.

### Rejected (Do Not Re-litigate)
- Reading BLOCKED/NOT_APPLICABLE as a scientific FALSIFIES of the discovery hypothesis.
- Any post-freeze construction of the target pool as a confirmatory measurement.
- The parent's single-engine mdBook DEEP band as a substitute for the required ≥2-engine pool.

### Unknown (Open Questions)
- Whether site-native discovery channels reach ≥50% of DEEP items in ≤K=3 GETs on ≥2 engines — **THIS EXPERIMENT**.
- Whether any non-mdBook host admits DEEP items at larger budget (now resolved: 3 hosts confirmed).
- The maintenance/invalidation axis (re-validation GETs/bytes plus stale-replay false-accept rate vs re-derivation cost) — recorded alternative.

### Do Not Assume (Dangerous Non-Conclusions)
- Do NOT treat this DESIGN as pre-judging the outcome; the falsifier is arithmetically satisfiable in both directions.
- Do NOT assume discovery channels work on all engines; per-channel coverage is measured and reported.
- Do NOT import agent priors / Scout brief / portfolio assessment as SPIDER evidence.

---

## 16. Dependencies & Prerequisites

1. **Global Research Director mandate** (present in `request.json.director_mandate`, action=REOPEN on C-RESIDUAL-NOVELTY).
2. **Frozen target pool** with confirmed DEEP items on ≥3 hosts/engines (built during DESIGN, evidence in `pre_freeze_evidence/`).
3. **Pre-freeze control certificate** with live evidence references in `spec.json`.
4. **No new infrastructure:** Credential-free GET-only stdlib HTTP (already established).
5. **Mutable local code dependency:** `run_experiment.py` (bound in `freeze_artifacts`).

---

## 17. Evidence References (To Be Populated by EXECUTE)

| Artifact | Path Pattern |
|----------|--------------|
| Raw HTTP logs | `raw/http.jsonl` |
| Raw hop confirmation | `raw/hop_confirmation.jsonl` |
| Raw discovery probes | `raw/discovery_probes.jsonl` |
| Raw null control | `raw/null_control.jsonl` |
| Derived metrics | `derived/metrics.json` |
| Per-item results | `derived/per_item_results.json` |
| Controls verification | `derived/controls.json` |

---

## 18. Freeze-Eligibility Checks (Design Contract v2)

All six checks **PASS** with justification recorded in `spec.json.freeze_eligibility`:

1. **decision_rule_reachability**: PASS — Denominator ≥10 confirmed; both falsifier branches arithmetically satisfiable.
2. **measurement_prerequisites**: PASS — Substrate available, pool confirmed, channels defined, controls verified, all VN-V* resolved.
3. **baseline_identifiability**: PASS — Three baselines carried from parent with stable identifiers, computable on same item set.
4. **control_sensitivity**: PASS — Positive control verified live on 3 hosts; null control verified live yielding 0 FP.
5. **treatment_liveness**: PASS — Treatment executable on frozen pool with stdlib HTTP; no browser/Docker/model key needed.
6. **freeze_artifacts_bound**: PASS — All mutable dependencies listed in `spec.json.freeze_artifacts` (pool/crawl/certificate evidence + run_experiment.py).

---

## 19. Commitment

This preregistration is **frozen** upon creation of `freeze.json`. No changes to hypothesis, channels, K, threshold, pool, decision rule, or metrics are permitted after freeze. Any post-freeze analysis changes render the confirmatory claim exploratory.

**Next step:** Deterministic freezer creates `freeze.json` with hashes of `request.json`, `spec.json`, `prereg.md`, and all `freeze_artifacts`.