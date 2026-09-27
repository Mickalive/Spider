# Preregistration: EXP-INTEL-36287179392

## 1. Experiment Identity
- **Experiment ID**: EXP-INTEL-36287179392
- **Lane**: intel
- **Claim ID**: C-CROSSSITE
- **Director Mandate**: REOPEN with cognitive reset (request.json director_mandate.allocation.action = REOPEN, claim_id = C-CROSSSITE, cognitive_reset = true)
- **Parent Handoff Disposition**: SUPERSEDE (parent_handoff = EXP-INTEL-36272389571; its next_question is advisory only)

## 2. Question (from Director Mandate)
> Without any third-party dataset credential, container registry authentication, browser binary or model API key, what is the measured cross-site structural prevalence and per-observation cost floor in real Web data — on a pre-registered sample of real public sites, plus whatever task manifest is genuinely obtainable credential-free, what fraction of observed navigational and interaction structure is alias-generalizable across distinct eTLD+1 hosts, reported against a shuffled-host null of demonstrated power with bootstrap intervals of nonzero width, and what does one observation of such a site actually cost in bytes and in tokens-equivalent compared with full-DOM and accessibility-tree style representations — so that SPIDER's addressable market and its external baseline set are set by measurement rather than by reported numbers?

## 3. Hypothesis
**H1 (Prevalence)**: Real public websites contain a measurable fraction of alias-generalizable navigational/interaction structure (reusable across eTLD+1 via parameterized identifiers) that exceeds a shuffled-host null.

**H2 (Cost)**: The per-observation cost using a minimal HTTP+HTML-structural representation is strictly lower than full-DOM or accessibility-tree representations.

**H3 (Measurability)**: The measurement produces bootstrap confidence intervals of nonzero width (non-degenerate inference).

## 4. Falsifiers
The hypothesis is falsified if ANY of the following holds:
- **F1**: Alias-generalizable fraction (AGF) point estimate ≤ shuffled-host null 95th percentile, OR bootstrap 95% CI lower bound ≤ null 95th percentile.
- **F2**: Minimal representation tokens-per-observation ≥ B-FULL-DOM tokens-per-observation OR ≥ B-A11Y-TREE tokens-per-observation (paired bootstrap 95% CI for difference includes or exceeds zero).
- **F3**: Bootstrap CI width = 0 for AGF (degenerate), OR fewer than 10 eTLD+1 hosts with ≥2 pages each, OR shuffled null distribution degenerate (std = 0).

## 5. Pre-Registered Site Sample
### 5.1 Selection Criteria
- Publicly accessible via HTTP/HTTPS GET without authentication, cookies, or JavaScript execution
- robots.txt permits crawling (User-Agent: SPIDER-Research/1.0)
- Distinct eTLD+1 (effective top-level domain + 1)
- At least 2 discoverable pages per site (homepage + at least one linked page)
- Diverse categories: e-commerce, documentation, news, reference, social, search, developer tools

### 5.2 Fixed Sample (20 eTLD+1 hosts)
| # | eTLD+1 | Base URL | Category | Rationale |
|---|--------|----------|----------|-----------|
| 1 | github.com | https://github.com | Developer platform | Forms, navigation, lists, search |
| 2 | docs.python.org | https://docs.python.org | Documentation | Navigation, sidebar, content structure |
| 3 | en.wikipedia.org | https://en.wikipedia.org | Reference | Links, tables, search, navigation |
| 4 | news.ycombinator.com | https://news.ycombinator.com | News aggregator | Lists, pagination, links |
| 5 | stackoverflow.com | https://stackoverflow.com | Q&A | Forms, lists, tags, navigation |
| 6 | developer.mozilla.org | https://developer.mozilla.org | Documentation | Navigation, sidebar, code examples |
| 7 | pypi.org | https://pypi.org | Package registry | Search, forms, lists, detail pages |
| 8 | npmjs.com | https://www.npmjs.com | Package registry | Search, forms, lists, detail pages |
| 9 | crates.io | https://crates.io | Package registry | Search, forms, lists, detail pages |
| 10 | rubygems.org | https://rubygems.org | Package registry | Search, forms, lists, detail pages |
| 11 | gitlab.com | https://gitlab.com | Developer platform | Forms, navigation, lists, CI/CD |
| 12 | bitbucket.org | https://bitbucket.org | Developer platform | Forms, navigation, lists |
| 13 | sourceforge.net | https://sourceforge.net | Developer platform | Navigation, lists, downloads |
| 14 | dockerhub.io | https://hub.docker.com | Container registry | Search, forms, lists, tags |
| 15 | readthedocs.io | https://readthedocs.io | Documentation hosting | Navigation, sidebar, search |
| 16 | git-scm.com | https://git-scm.com | Documentation | Navigation, sidebar, content |
| 17 | linuxfoundation.org | https://linuxfoundation.org | Organization | Navigation, news, resources |
| 18 | apache.org | https://apache.org | Organization | Navigation, projects, downloads |
| 19 | gnu.org | https://www.gnu.org | Organization | Navigation, software, manuals |
| 20 | kernel.org | https://kernel.org | Reference | Navigation, downloads, mirrors |

**Note**: Sample is FIXED before any measurement. No adaptive addition/removal based on outcomes.

### 5.3 Page Discovery per Site
- Start at base URL (homepage)
- Extract all same-origin links (href starting with / or base URL)
- Filter: exclude logout, login, account, admin, API, static assets (.css, .js, .png, .jpg, .svg, .woff, .ico)
- Limit: maximum 10 pages per site (homepage + 9 discovered)
- Minimum: 2 pages per site (if fewer discovered, site retained but noted)

## 6. Structural Extraction Pipeline
### 6.1 Raw Observation (per page)
- HTTP GET with headers: `User-Agent: SPIDER-Research/1.0`, `Accept: text/html`
- Record: status code, response headers, response body (raw HTML), bytes received, latency
- Respect robots.txt (checked once per host before any requests)
- Rate limit: 1 request/second per host (token bucket)
- Timeout: 10 seconds connect, 30 seconds read

### 6.2 Structural Representation (Minimal)
From parsed HTML (BeautifulSoup4), extract:
1. **Forms**: `<form>` elements with action, method, and all `<input>`, `<select>`, `<textarea>` with name, type, placeholder, required
2. **Navigation**: `<nav>`, `<header>`, `<footer>`, elements with role="navigation", links with `rel="prev/next/first/last"`, breadcrumb structures
3. **Lists/Repeating Structures**: `<ul>`, `<ol>`, `<table>`, elements with >3 same-tag children with similar class patterns
4. **Search**: `<form>` with type="search" or input name containing "search"/"query"/"q"
5. **Pagination**: Links with rel="next/prev", text matching "next|previous|page \d+", query params like `page=`, `p=`, `offset=`
6. **Detail/Entity Pages**: Links with patterns like `/item/`, `/product/`, `/article/`, `/post/`, `/question/`, `/issue/`, `/pr/`, `/package/`, `/crate/`, `/gem/`, `/project/`
7. **Buttons/Actions**: `<button>`, `<input type="submit/button">`, `<a class*="btn">`, role="button"

**Parameterization Rule**: For each structural element type, identify varying attributes (href paths, input names/values, IDs in URLs, query parameters) and abstract to a template with typed slots (e.g., `/search?q={query}`, `/item/{id}`, `input[name={field}]`).

### 6.3 Baseline Representations
- **B-RAW-HTML**: Raw response body bytes and tokens (cl100k_base)
- **B-FULL-DOM**: Full serialized DOM (outerHTML of documentElement) bytes and tokens
- **B-A11Y-TREE**: Approximated from semantic HTML (`<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`, `<header>`, `<footer>`, `[role]`, `[aria-*]`, heading hierarchy) — serialized as structured JSON, then bytes and tokens

### 6.4 Minimal Representation (Test)
- Only the extracted structural elements from 6.2, serialized as compact JSON
- Tokens = cl100k_base encoding of this JSON

## 7. Alias-Generalizable Fraction (AGF) Computation
### 7.1 Structural Signature per Page
Each page → set of structural signatures:
- Form signature: `(action_template, method, field_names_sorted)`
- Nav signature: `(nav_type, link_templates_sorted)`
- List signature: `(container_type, item_template, item_count)`
- Search signature: `(action_template, param_name)`
- Pagination signature: `(base_template, param_name)`
- Detail signature: `(list_template, detail_template)`
- Action signature: `(action_type, target_template)`

Templates have typed slots: `{id}`, `{slug}`, `{query}`, `{page}`, `{category}`, `{token}`, etc.

### 7.2 Cross-Site Matching
For each pair of distinct eTLD+1 (A, B):
- Match signatures by type and template structure (ignoring slot values)
- A match = same signature type + identical template structure (same slot names/types in same positions)
- Count matched signatures per site pair

### 7.3 AGF Metric
```
AGF = (Total matched signatures across all eTLD+1 pairs) / (Total signatures across all pages)
```
Alternative (per-site-pair): Mean Jaccard similarity of signature sets across all eTLD+1 pairs.

Primary metric: **AGF (global fraction)**. Secondary: **Mean pairwise Jaccard**.

## 8. Null Control: Shuffled-Host
### 8.1 Procedure
1. Take the observed signature sets per eTLD+1
2. Randomly permute eTLD+1 labels (1,000 permutations)
3. For each permutation, recompute AGF and pairwise Jaccard
4. Build empirical null distribution

### 8.2 Null Power Check
- Verify null distribution std > 0 (non-degenerate)
- Verify null 95th percentile < observed AGF point estimate (for positive control validation)

## 9. Bootstrap Inference
### 9.1 Resampling Unit
**eTLD+1 host** (not page, not signature). This preserves within-site correlation.

### 9.2 Procedure (10,000 replicates)
1. Sample 20 eTLD+1 with replacement
2. Compute AGF and cost metrics on resampled set
3. Record replicate statistics

### 9.3 Confidence Intervals
- Percentile 95% CI (2.5th, 97.5th percentiles)
- Report: point estimate, CI lower, CI upper, CI width
- **Validity gate**: CI width > 0 for AGF

## 10. Cost Metrics
Per observation (per page):
- `bytes_raw` = len(response.content)
- `bytes_minimal` = len(json.dumps(minimal_structure).encode())
- `bytes_full_dom` = len(full_dom_serialized.encode())
- `bytes_a11y` = len(a11y_json.encode())
- `tokens_raw` = len(tiktoken.encode(response.text))
- `tokens_minimal` = len(tiktoken.encode(json.dumps(minimal_structure)))
- `tokens_full_dom` = len(tiktoken.encode(full_dom_serialized))
- `tokens_a11y` = len(tiktoken.encode(json.dumps(a11y_structure)))

Paired comparison: For each page, compute differences (minimal - full_dom), (minimal - a11y). Bootstrap CI for mean difference.

## 11. Positive Control: Synthetic Alias
### 11.1 Construction
Two synthetic HTML pages with identical template structure, different slot values:
- Page A: `/search?q=python` form, `/item/123` detail links, pagination `?page=1`
- Page B: `/search?q=rust` form, `/item/456` detail links, pagination `?page=1`

### 11.2 Expected Outcome
AGF > 0.8 against shuffled null (which should be ~0 for 2 sites). Confirms pipeline sensitivity.

## 12. Decision Rule (Frozen)
| Condition | Threshold |
|-----------|-----------|
| **Primary (Prevalence)** | AGF_point > null_p95 AND AGF_CI_lower > null_p95 |
| **Cost** | mean(tokens_minimal - tokens_full_dom) < 0 AND mean(tokens_minimal - tokens_a11y) < 0 (paired bootstrap 95% CI upper < 0) |
| **Validity** | AGF_CI_width > 0 AND n_eTLD1_ge2pages >= 10 AND null_std > 0 |

### Outcome Mapping
| Outcome | Criteria |
|---------|----------|
| **SUPPORTS** | Primary ∧ Cost ∧ Validity |
| **FALSIFIES** | ¬Primary ∨ ¬Cost ∨ ¬Validity |
| **MIXED** | (Primary ∧ ¬Cost) ∨ (¬Primary ∧ Cost) ∨ (Validity partially failed but some metrics valid) |
| **INCONCLUSIVE** | ¬Validity (degenerate CI, insufficient sample) |

## 13. Validity Threats & Mitigations
| Threat | Mitigation |
|--------|------------|
| JS-rendered content missed | Accepted limitation: HTTP-only extraction; documented in validity_notes |
| robots.txt blocks key pages | Pre-check robots.txt; if blocked, note in observations; site still counted if ≥2 pages accessible |
| Site structure changes during run | Single snapshot per site; record timestamp; no re-fetching |
| Template extraction heuristics miss structures | Positive control validates pipeline; false negatives possible but bounded |
| eTLD+1 not true organizational boundary | Using public suffix list (publicsuffix2 library); documented |
| Tokenizer not matching target model | cl100k_base is standard for GPT-4/3.5; reported as convention |
| Bootstrap CI degenerate (width=0) | Validity gate catches this → INCONCLUSIVE |

## 14. Artifacts to Produce
Raw evidence (immutable):
- `raw_responses.jsonl`: One line per request: `{url, status, headers, body_sha256, bytes, latency_ms, timestamp}`
- `extracted_structures.jsonl`: One line per page: `{url, eTLD1, signatures, minimal_json, full_dom_sha256, a11y_json}`

Derived measurements:
- `metrics.json`: `{AGF, AGF_CI, pairwise_jaccard_mean, pairwise_jaccard_CI, null_distribution, cost_metrics, bootstrap_replicates_summary}`

Provenance:
- `provenance.json`: Git commit, Python version, package versions, site sample hash, random seeds

## 15. Software Environment
- Python 3.11+
- `requests>=2.31`
- `beautifulsoup4>=4.12`
- `tiktoken>=0.7`
- `publicsuffix2>=2.2023`
- `numpy>=1.24` (for bootstrap)
- All pure Python or manylinux wheels; no system dependencies

## 16. Random Seeds
- Bootstrap: `seed=36287179392` (experiment_id)
- Shuffled null permutations: `seed=36287179392 + 1`
- Positive control: `seed=36287179392 + 2`

## 17. Pre-Registration Freeze
This prereg.md and spec.json are frozen before any HTTP requests are made. The freeze.json will contain SHA256 hashes of both files. No changes to design, sample, or decision rule after freeze.

## 18. Consequences
- **Positive (SUPPORTS)**: C-CROSSSITE moves from HYPOTHESIS to EXPERIMENTAL with measured prevalence and cost floor. Graph/Product/Frontier receive measured baselines.
- **Negative (FALSIFIES)**: C-CROSSSITE remains HYPOTHESIS or moves to REJECTED with bounded evidence. Cross-site inheritance deprioritized; per-observation cost floor becomes new baseline.
- **Mixed**: Partial evidence; specific components (prevalence vs cost) inform lane re-scoping.
- **Inconclusive (MEASUREMENT_INVALID)**: Measurement infrastructure issue; retry with larger sample or fixed extraction.

---

**End of Preregistration**