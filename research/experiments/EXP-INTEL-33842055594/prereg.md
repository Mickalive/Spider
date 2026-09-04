# EXP-INTEL-33842055594 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-33842055594
- **Lane**: Intel
- **Claim IDs**: C-CROSSSITE, C-LLM-INHERIT
- **Date**: 2026-09-04
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-INTEL-33528832113 (Structured Reconnaissance of Web-Agent Benchmarks)
- **Parent Verdict**: SUPPORTS
- **Request Reason**: pulse (inherited next_question from parent handoff)

## 2. Inherited State (from EXP-INTEL-33528832113 handoff.json)

### Established
- WebArena (2024) is a public benchmark with 812 long-horizon tasks, 4 website types (e-commerce, social forum, collaborative coding, CMS), Docker self-hosting, public trajectory replay infrastructure, and scores 5/5 on structural proxies S1-S5.
- VisualWebArena (2024) likely meets all five structural proxies but requires visual modality compatibility check.
- Six to nine additional benchmarks (Mind2Web, AssistantBench, WebBench, WorkArena, WebMall, Explorer, WebLINX, AgentBench) meet S1+S2+S3+S4>=3 but lack self-hosting or single-domain diversity, making them RECOMMENDED only as proxies.

### Rejected
- (none from parent)

### Unknown
- Whether WebArena's Docker environment provides HTML/DOM accessibility trees compatible with SPIDER's fragment-reuse observation format. **(This experiment addresses this.)**
- Whether VisualWebArena's visual emphasis (screenshots + SoM annotations) conflicts with SPIDER's text-based fragment model.
- Whether WebBench's live-website evaluation model could be adapted for SPIDER testing.
- Whether WorkArena's ServiceNow developer instance satisfies spec S4 definition (self-hostable or API replay).
- Whether WebShop's trajectory data availability (S2) should be 1, which would raise it to RECOMMENDED.
- Whether Explorer's synthetic tasks align with SPIDER action-oriented navigation or are QA/information-seeking.
- Whether QWeb or AWM benchmarks, if located, would alter the candidate set.

### Do Not Assume
- Do not assume that structural compatibility (S1-S5) equals SPIDER fragment-reuse suitability.
- Do not assume that C-CROSSSITE or C-LLM-INHERIT are unblocked; they remain bounded to 2-site corpus until integration experiment.
- Do not assume that WebArena's Docker environment provides HTML/DOM accessibility trees compatible with SPIDER.
- Do not assume that VisualWebArena's visual modality is compatible with SPIDER's text-based fragment model.
- Do not assume that the audit's metric inconsistencies affect the core finding about WebArena's existence.
- Do not assume that the null control failure invalidates the entire audit; it indicates measurement incompleteness, not falsification.
- Do not assume that any benchmark is experimentally suitable without a separate integration experiment.

## 3. Scientific Question

Can WebArena's Docker-based self-hosting provide HTML/DOM accessibility trees compatible with SPIDER's fragment-reuse observation format?

## 4. What This Experiment Is NOT

- This is NOT a Docker deployment test. No containers will be run.
- This is NOT an integration experiment. No SPIDER code will execute against WebArena.
- This is NOT a benchmark evaluation. No tasks will be solved.
- This IS a source-code inspection to determine observation-format compatibility.

## 5. Motivation

The parent experiment identified WebArena as the only STRONGLY RECOMMENDED benchmark (5/5 on structural proxies S1-S5). The parent handoff's primary unresolved question is whether this structural compatibility translates to observation-format compatibility.

SPIDER's fragment-reuse model requires observation data that preserves:
- Element identity (tag, id, classes, attributes)
- Element hierarchy (parent-child relationships)
- Text content
- Interactive state (form values, enabled/disabled, visibility)

From `src/spider/models.py`:
```python
@dataclass(frozen=True)
class Observation:
    intent: str
    state: dict[str, Any]   # <-- must hold structured page data
    action: dict[str, Any]
    next_state: dict[str, Any]
    success: bool
    provenance: dict[str, Any] = field(default_factory=dict)
```

The `state` dict is `dict[str, Any]` — generic enough to hold any structured data. The question is whether WebArena provides structured data (not just screenshots or flat strings) that can populate this dict.

## 6. Hypotheses

### H1: DOM Accessibility
WebArena's agent interface provides access to page HTML/DOM content through Playwright's browser automation API. Specifically, the agent observation includes at least one of: raw HTML (`page.content()`), accessibility tree (`page.accessibility.snapshot()`), or DOM element queries (`page.query_selector_all()`).

### H2: Structural Preservation
The DOM/HTML data provided by WebArena preserves the structural information SPIDER needs for fragment extraction: element type, attributes, hierarchy, and text content. The data is not serialized into a flat string without parseable structure.

### H3: Cross-Site Consistency
DOM/HTML access is available across all 4 of WebArena's self-hosted website types (e-commerce, social forum, collaborative coding, CMS), not just a subset.

### H4: SPIDER Format Mapping
WebArena's observation data can be mapped into SPIDER's Observation.state dict format (`dict[str, Any]`) without destroying the structural information needed for fragment identification.

## 7. Methodology

### 7.1 Repository Access

Access the WebArena GitHub repository (github.com/web-arena-x/webarena). Use webfetch or websearch to inspect the repository structure, README, and key source files. No cloning required.

### 7.2 Agent-Environment Interaction Layer

Identify the primary file(s) that implement the agent-environment interface. Look for:
- How the browser/page object is created and managed
- What API calls are made to interact with the page
- What data is extracted from the page after each action

Key search targets:
- Files containing `playwright`, `page.`, `browser.`, `accessibility`, `content()`, `query_selector`
- Agent wrapper classes or environment classes
- Observation extraction or state capture functions

### 7.3 Observation Format Extraction

For each identified observation extraction point, determine:
1. **What data type is returned**: HTML string, accessibility tree dict, DOM element list, screenshot, API response, or combination
2. **What structure the data has**: nested dict (hierarchical), flat string, binary, list of objects
3. **Whether element hierarchy is preserved**: parent-child relationships, nesting depth, attribute access
4. **Whether the data can be parsed**: standard formats (HTML, JSON) vs proprietary/binary

### 7.4 SPIDER Compatibility Mapping

Map extracted observation data to SPIDER's Observation model:
- `Observation.state` dict must receive structured page data
- `Observation.action` dict must receive the action taken
- `Observation.next_state` dict must receive the resulting page state
- The mapping must preserve element identity, hierarchy, attributes, and text

### 7.5 Cross-Site Verification

Check observation availability for each website type by examining:
1. E-commerce (Shopping site)
2. Social forum (Reddit-like)
3. Collaborative coding (GitLab-like)
4. CMS (Wikipedia-like)

Determine whether the observation format is uniform across site types or varies.

## 8. Controls

### 8.1 Positive Control
WebArena is documented as using Playwright for browser automation. Playwright natively provides:
- `page.content()` — returns raw HTML string
- `page.accessibility.snapshot()` — returns accessibility tree as nested dict
- `page.query_selector_all()` — returns DOM element handles
- `page.evaluate()` — can execute arbitrary JavaScript to extract DOM data

If the codebase inspection cannot locate ANY Playwright API usage, the methodology is broken.

### 8.2 Null Control
If WebArena's agent interface returns only:
- Screenshots (base64 PNG/JPEG)
- API JSON responses (REST endpoint payloads)
- Action logs without page state

Then DOM/HTML is absent and the observation format is INCOMPATIBLE.

### 8.3 Baseline: SPIDER's Current Format
SPIDER's Observation.state is `dict[str, Any]`. The only constraint is that the dict preserves structural information. Currently tested on quotes.toscrape.com and books.toscrape.com with raw HTML pages.

## 9. Measurement Validity

### 9.1 Source Citation Requirement
Every claim about WebArena's observation interface must cite:
- Specific file path in the repository
- Function/class name
- Line number or code snippet
- The actual data structure returned

### 9.2 No Documentation-Only Claims
Claims must be grounded in source code, not README or paper text. Documentation may state intentions; source code reveals actual behavior.

### 9.3 Three-Level Outcome
The assessment must distinguish:
1. **DIRECTLY_USABLE**: DOM/HTML is present, parseable, and preserves element hierarchy. Can be mapped to Observation.state without information loss.
2. **REQUIRES_TRANSFORM**: DOM/HTML is present but needs conversion (e.g., accessibility tree nested dict to flat dict, or HTML string to parsed tree). Structural information is recoverable but requires processing.
3. **ABSENT**: DOM/HTML is not available to the agent. Agent receives only screenshots, API responses, or action logs.

These are different outcomes with different product consequences.

## 10. Decision Rules

### 10.1 COMPATIBLE
If ALL of:
1. WebArena's agent interface provides DOM/HTML content (via page.content(), accessibility tree, or DOM queries)
2. The content preserves element hierarchy (parent-child relationships, not flat string)
3. The data can be mapped to Observation.state dict without losing structural information

Verdict: SUPPORTS. WebArena is observation-compatible with SPIDER.

### 10.2 PARTIALLY_COMPATIBLE
If ANY of:
1. DOM/HTML is present but only for some website types (< 3 of 4)
2. DOM/HTML is present but requires non-trivial transformation that may lose information
3. DOM is accessible but some page elements (iframes, shadow DOM, canvas) are excluded

Verdict: MIXED. WebArena may be usable with limitations. Integration experiment should test specific website types.

### 10.3 INCOMPATIBLE
If ANY of:
1. Agent receives only screenshots without DOM/HTML
2. Agent receives only API JSON responses without page content
3. DOM/HTML is present but fully serialized into flat string without parseable structure
4. None of the 4 website types provide DOM/HTML access

Verdict: FALSIFIES. WebArena cannot serve as SPIDER testbed despite 5/5 structural score.

### 10.4 MEASUREMENT_INVALID
If:
1. Repository is inaccessible or code is obfuscated
2. Observation interface cannot be located in the codebase
3. Source code inspection is ambiguous (multiple possible observation formats with no clear primary)

## 11. Validity Threats

### 11.1 Multiple Observation Formats
WebArena may provide different observation data depending on agent configuration (e.g., accessibility tree vs. raw HTML vs. screenshots). The inspection must identify the DEFAULT observation format, not just possible formats. If multiple formats coexist, report all and identify which is primary.

### 11.2 Code Evolution
WebArena's codebase may have changed since the paper was published. The inspection must use the current HEAD of the repository (verified via GitHub), not paper-described architecture.

### 11.3 Abstraction Layers
WebArena may abstract browser interaction behind a wrapper that hides DOM access. The inspection must trace through abstraction layers to determine what data is actually available to the agent at the outermost interface.

### 11.4 SPIDER Format Underspecification
SPIDER's Observation.state is `dict[str, Any]` — extremely generic. The compatibility assessment requires an assumption about what structural information SPIDER's fragment extraction WILL need. This assumption is based on the parent handoff's mention of "HTML/DOM accessibility trees" and SPIDER Master Prompt §17 (Raw Observation First).

### 11.5 WebFetch Limitations
Using webfetch to inspect GitHub repositories returns rendered HTML, not raw source. Key files may be truncated or require navigating multiple pages. Mitigation: use websearch to identify key file paths, then webfetch specific raw file URLs.

## 12. Expected Outcomes

### 12.1 COMPATIBLE (most likely, given Playwright usage)
- WebArena uses Playwright, which provides full DOM access
- Graph lane can design C-CROSSSITE integration experiment
- Product lane can design C-LLM-INHERIT experiment
- Fragment extraction code can target a concrete DOM format
- The 2-site corpus limitation is resolved

### 12.2 PARTIALLY_COMPATIBLE
- Some website types may use iframes, shadow DOM, or canvas
- Integration experiment should be scoped to compatible website types first
- VisualWebArena may fill gaps for visual-only tasks

### 12.3 INCOMPATIBLE (unlikely given Playwright usage)
- WebArena's agent interface abstracts away DOM access
- SPIDER would need a custom observation layer on top of WebArena
- Or SPIDER would need to use VisualWebArena's visual modality instead
- The structural proxy S1-S5 is shown to be necessary but not sufficient

### 12.4 MEASUREMENT_INVALID
- Repository structure too complex to inspect via webfetch in bounded time
- Multiple observation formats with no clear primary
- Requires full deployment to determine actual observation data

## 13. Analysis Plan

1. **Repository Access**: Fetch WebArena GitHub repository structure and README
2. **Key File Identification**: Search for agent-environment interaction files containing Playwright API calls
3. **Observation Extraction Trace**: Follow the code path from browser interaction to agent observation
4. **Data Type Classification**: For each observation point, classify the data type (HTML string, accessibility tree, DOM elements, screenshot, API response)
5. **Structure Assessment**: Determine whether the data preserves element hierarchy or is flat
6. **Cross-Site Check**: Verify observation format consistency across 4 website types
7. **SPIDER Mapping**: Map observation data to Observation.state dict format
8. **Compatibility Verdict**: Apply decision rules to determine COMPATIBLE / PARTIALLY_COMPATIBLE / INCOMPATIBLE / MEASUREMENT_INVALID
9. **Evidence Documentation**: Record file paths, function names, line numbers, and code snippets for all findings

## 14. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 15. Freeze Statement

This preregistration is frozen BEFORE any source code inspection begins. The experiment will be executed exactly as described here.
