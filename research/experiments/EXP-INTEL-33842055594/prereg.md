# EXP-INTEL-33842055594 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-INTEL-33842055594
- **Lane**: Intel
- **Claim IDs**: C-CROSSSITE, C-LLM-INHERIT
- **Date**: 2026-09-04
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-INTEL-33528832113 (Structured Reconnaissance of Web-Agent Benchmarks)
- **Parent Verdict**: SUPPORTS

## 2. Scientific Question

Can WebArena's Docker-based self-hosting provide HTML/DOM accessibility trees compatible with SPIDER's fragment-reuse observation format?

## 3. Motivation

EXP-INTEL-33528832113 identified WebArena as the only STRONGLY RECOMMENDED benchmark (5/5 on structural proxies S1-S5). The parent handoff's primary unresolved question is whether this structural compatibility translates to observation-format compatibility.

SPIDER's fragment-reuse model requires observation data that preserves:
- Element identity (tag, id, classes, attributes)
- Element hierarchy (parent-child relationships)
- Text content
- Interactive state (form values, enabled/disabled, visibility)

The parent experiment scored WebArena 5/5 on structural proxies but explicitly noted: "A 5/5 score does not guarantee experimental suitability; suitability requires a separate integration experiment."

This experiment fills that gap for the observation format specifically, before committing to a full integration experiment.

## 4. What This Experiment Is NOT

- This is NOT a Docker deployment test. No containers will be run.
- This is NOT an integration experiment. No SPIDER code will execute against WebArena.
- This is NOT a benchmark evaluation. No tasks will be solved.
- This IS a source-code inspection to determine observation-format compatibility.

## 5. Hypotheses

### H1: DOM Accessibility
WebArena's agent interface provides access to page HTML/DOM content through Playwright's browser automation API. Specifically, the agent observation includes at least one of: raw HTML (page.content()), accessibility tree (page.accessibility.snapshot()), or DOM element queries (page.query_selector_all()).

### H2: Structural Preservation
The DOM/HTML data provided by WebArena preserves the structural information SPIDER needs for fragment extraction: element type, attributes, hierarchy, and text content. This means the data is not serialized into a flat string without parseable structure.

### H3: Cross-Site Consistency
DOM/HTML access is available across all 4 of WebArena's self-hosted website types (e-commerce, social forum, collaborative coding, CMS), not just a subset.

### H4: SPIDER Format Mapping
WebArena's observation data can be mapped into SPIDER's Observation.state dict format (dict[str, Any]) without destroying the structural information needed for fragment identification.

## 6. Methodology

### 6.1 Repository Inspection

Clone or inspect the WebArena GitHub repository (github.com/web-arena-x/webarena). Examine:
1. The agent/environment interaction layer
2. The observation/state extraction functions
3. What data the agent receives per environment step
4. How observations are structured and passed to the agent

### 6.2 Observation Format Extraction

For each of the 4 website types, determine:
- What raw data is available (HTML, accessibility tree, screenshots, API responses)
- How the data is structured (nested dict, flat string, binary image)
- Whether element hierarchy is preserved
- Whether the data can be parsed without external tools

### 6.3 SPIDER Compatibility Mapping

Map extracted observation data to SPIDER's Observation model:
- Observation.state dict must receive structured page data
- Observation.action dict must receive the action taken
- Observation.next_state dict must receive the resulting page state
- The mapping must preserve element identity, hierarchy, attributes, and text

### 6.4 Cross-Site Verification

Check observation availability for each website type:
1. E-commerce ( Shopping site)
2. Social forum (Reddit-like)
3. Collaborative coding (GitLab-like)
4. CMS (Wikipedia-like)

## 7. Controls

### 7.1 Positive Control
WebArena uses Playwright for browser automation. Playwright provides:
- `page.content()` — returns raw HTML string
- `page.accessibility.snapshot()` — returns accessibility tree dict
- `page.query_selector_all()` — returns DOM element handles
- `page.evaluate()` — can execute任意 JS to extract DOM data

If the codebase inspection cannot locate Playwright usage, the methodology is broken.

### 7.2 Null Control
If WebArena's agent interface returns only:
- Screenshots (base64 PNG/JPEG)
- API JSON responses (REST endpoint payloads)
- Action logs without page state

Then DOM/HTML is absent and the observation format is INCOMPATIBLE.

### 7.3 Baseline: SPIDER's Current Format
SPIDER's Observation.state is `dict[str, Any]`. The only constraint is that the dict preserves structural information. Currently tested on quotes.toscrape.com and books.toscrape.com with raw HTML pages.

## 8. Measurement Validity

### 8.1 Source Citation Requirement
Every claim about WebArena's observation interface must cite:
- Specific file path in the repository
- Function/class name
- Line number or code snippet
- The actual data structure returned

### 8.2 No Documentation-Only Claims
Claims must be grounded in source code, not README or paper text. Documentation may state intentions; source code reveals actual behavior.

### 8.3 Three-Level Outcome
The assessment must distinguish:
1. **DIRECTLY_USABLE**: DOM/HTML is present, parseable, and preserves structure
2. **REQUIRES_TRANSFORM**: DOM/HTML is present but needs conversion (e.g., accessibility tree to flat dict)
3. **ABSENT**: DOM/HTML is not available to the agent

These are different outcomes with different product consequences.

## 9. Decision Rules

### 9.1 COMPATIBLE
If ALL of:
1. WebArena's agent interface provides DOM/HTML content (page.content() or accessibility tree or DOM queries)
2. The content preserves element hierarchy (parent-child, not flat string)
3. At least 3 of 4 website types provide DOM/HTML access
4. The data can be mapped to Observation.state dict without losing structural information

Verdict: SUPPORTS. WebArena is observation-compatible with SPIDER.

### 9.2 PARTIALLY_COMPATIBLE
If ANY of:
1. DOM/HTML is present but only for some website types (< 3 of 4)
2. DOM/HTML is present but requires non-trivial transformation that may lose information
3. DOM is accessible but some page elements (iframes, shadow DOM, canvas) are excluded

Verdict: MIXED. WebArena may be usable with limitations. Integration experiment should test specific website types.

### 9.3 INCOMPATIBLE
If ANY of:
1. Agent receives only screenshots without DOM/HTML
2. Agent receives only API JSON responses without page content
3. DOM/HTML is present but fully serialized into flat string without parseable structure
4. None of the 4 website types provide DOM/HTML access

Verdict: FALSIFIES. WebArena cannot serve as SPIDER testbed despite 5/5 structural score.

### 9.4 MEASUREMENT_INVALID
If:
1. Repository is inaccessible or code is obfuscated
2. Observation interface cannot be located in the codebase
3. Source code inspection is ambiguous (multiple possible observation formats)

## 10. Expected Outcomes

### 10.1 COMPATIBLE (most likely)
- WebArena uses Playwright, which provides full DOM access
- Graph lane can design C-CROSSSITE integration experiment
- Product lane can design C-LLM-INHERIT experiment
- Fragment extraction code can target a concrete DOM format
- The 2-site corpus limitation is resolved

### 10.2 PARTIALLY_COMPATIBLE
- Some website types may use iframes, shadow DOM, or canvas
- Integration experiment should be scoped to compatible website types first
- VisualWebArena may fill gaps for visual-only tasks

### 10.3 INCOMPATIBLE (unlikely given Playwright usage)
- WebArena's agent interface abstracts away DOM access
- SPIDER would need a custom observation layer on top of WebArena
- Or SPIDER would need to use VisualWebArena's visual modality instead
- The structural proxy S1-S5 is shown to be necessary but not sufficient

### 10.4 MEASUREMENT_INVALID
- Repository structure is too complex to inspect in bounded time
- Multiple observation formats exist with no clear primary format
- Requires full deployment to determine actual observation data

## 11. Validity Threats

### 11.1 Multiple Observation Formats
WebArena may provide different observation data depending on the agent configuration (e.g., whether the agent uses accessibility tree vs. raw HTML vs. screenshots). The inspection must identify the DEFAULT observation format, not just possible formats.

### 11.2 Code Evolution
WebArena's codebase may have changed since the paper was published. The inspection must use the current HEAD of the repository, not paper-described architecture.

### 11.3 Abstraction Layers
WebArena may abstract browser interaction behind a wrapper that hides DOM access. The inspection must trace through abstraction layers to determine what data is actually available to the agent.

### 11.4 SPIDER Format Underspecification
SPIDER's Observation.state is dict[str, Any] — extremely generic. The compatibility assessment requires an assumption about what structural information SPIDER's fragment extraction WILL need. This assumption is based on the parent handoff's mention of "HTML/DOM accessibility trees" and SPIDER Master Prompt §17 (Raw Observation First).

## 12. Analysis Plan

1. Clone WebArena repository at current HEAD
2. Identify the primary agent-environment interaction file(s)
3. Trace observation extraction from browser to agent
4. For each website type, verify DOM/HTML availability
5. Map observation data to SPIDER's Observation.state format
6. Assess compatibility level (DIRECTLY_USABLE / REQUIRES_TRANSFORM / ABSENT)
7. Write result.json with findings and evidence citations
