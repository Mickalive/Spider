# EXP-INTEL-33842055594 — Execution Report

## Executive Summary

**Verdict: COMPATIBLE (DIRECTLY_USABLE)**

WebArena's Docker-based self-hosting provides HTML/DOM accessibility trees that are fully compatible with SPIDER's fragment-reuse observation format. The agent observation interface exposes structured DOM data through Chrome DevTools Protocol, preserving element identity, hierarchy, attributes, and text content. No transformation is required to map this data to SPIDER's Observation.state dict.

## What Was Executed

Source-code inspection of the WebArena GitHub repository (github.com/web-arena-x/webarena, main branch). No Docker deployment, no browser execution, no live task solving. The experiment determined what data the code reveals is available to the agent.

## Key Findings

### 1. Observation Types (browser_env/envs.py, processors.py)

WebArena provides **three observation types** via the `observation_type` parameter:

| Type | API Used | Data Returned | Default |
|------|----------|---------------|---------|
| `accessibility_tree` | CDP `Accessibility.getFullAXTree` | Structured accessibility tree nodes | **Yes** |
| `html` | CDP `DOMSnapshot.captureSnapshot` | DOM tree with HTML attributes | No |
| `image` | `page.screenshot()` | Numpy array (PNG) | No |

The **default observation type is `accessibility_tree`**, which provides the richest structured DOM data.

### 2. Accessibility Tree Node Structure

Each accessibility tree node contains (browser_env/utils.py `AccessibilityTreeNode`):

```
{
  "nodeId": str,           # Unique element identifier
  "role": {"value": str},  # Element role: link, button, textbox, etc.
  "name": {"value": str},  # Element text content
  "properties": [          # Additional attributes
    {"name": str, "value": {"value": Any}}
  ],
  "childIds": [str],       # Children element IDs
  "parentId": str,         # Parent element ID
  "backendDOMNodeId": str, # Chrome DOM backend ID
  "union_bound": [x, y, w, h]  # Bounding box
}
```

### 3. Observation Output

The agent receives `obs["text"]` containing a formatted string like:

```
[4] RootWebArea 'Projects · Dashboard · GitLab' focused: True
        [12] link 'Skip to content'
        [28] link 'Dashboard'
        [2266] button '' hasPopup: menu expanded: False
        [63] textbox 'Search GitLab' required: False
```

Additionally, `obs_nodes_info` provides structured metadata mapping each element ID to `{backend_id, union_bound, text}`.

### 4. SPIDER Compatibility Mapping

SPIDER's `Observation.state` is `dict[str, Any]`. WebArena's data maps directly:

```python
state = {
    "accessibility_tree": accessibility_tree_nodes,  # Full node list
    "obs_nodes_info": obs_nodes_info,                # Element ID → metadata
    "browser_config": browser_config,                # Viewport info
    "url": page.url,                                 # Current page URL
}
```

All structural information needed for fragment extraction is preserved:
- **Element identity**: nodeId, role, name
- **Element hierarchy**: parentId, childIds (tree structure)
- **Element attributes**: properties list (focused, expanded, required, etc.)
- **Text content**: name.value contains visible text
- **Spatial information**: union_bound provides bounding boxes

### 5. Cross-Site Consistency

The `observation_type` is configured at the environment level (not per-site). All 4 website types use the same `ScriptBrowserEnv` class and the same observation pipeline:
- E-commerce (Shopping site)
- Social forum (Reddit-like)
- Collaborative coding (GitLab-like)
- CMS (Wikipedia-like)

**The observation format is uniform across all site types.**

### 6. Positive Control Verification

- **Playwright usage**: Confirmed. `browser_env/envs.py` imports `sync_playwright` and calls `self.playwright.chromium.launch()`.
- **CDP Accessibility**: Confirmed. `processors.py` calls `client.send("Accessibility.getFullAXTree", {})` and `client.send("Accessibility.enable")`.
- **DOM API calls**: Confirmed. `page.content()` is used in `DetachedPage` for trajectory saving. `page.evaluate()` is used for viewport bounds. `page.screenshot()` is used for image observations.

### 7. Null Control Result

The null control (screenshots-only interface) does **NOT** pass because WebArena's default observation type provides structured DOM data, not just screenshots. This is the expected positive outcome — it confirms DOM availability.

## Compatibility Assessment

| Criterion | Status | Evidence |
|-----------|--------|----------|
| DOM/HTML content accessible | ✅ Yes | CDP Accessibility.getFullAXTree and DOMSnapshot.captureSnapshot |
| Element hierarchy preserved | ✅ Yes | parentId/childIds in node structure, indentation in formatted output |
| Element identity preserved | ✅ Yes | nodeId, role, name in each node |
| Element attributes preserved | ✅ Yes | properties list with key-value pairs |
| Text content preserved | ✅ Yes | name.value contains visible text |
| Parseable format | ✅ Yes | Standard CDP JSON structure, not proprietary |
| Cross-site consistent | ✅ Yes | Same environment class for all 4 site types |
| Maps to SPIDER Observation.state | ✅ Yes | dict[str, Any] can hold full tree structure |

**Verdict: DIRECTLY_USABLE** — No transformation required. WebArena's observation data can be placed directly into SPIDER's Observation.state dict.

## Product Consequences

### If COMPATIBLE (this experiment)
- **Graph lane**: Can design C-CROSSSITE integration experiment using WebArena
- **Product lane**: Can design C-LLM-INHERIT experiment
- **Fragment extraction code**: Can target a concrete, well-documented DOM format
- **2-site corpus limitation**: Resolved — WebArena provides 812 tasks across 4 website types

### What This Unblocks
1. C-CROSSSITE claim: Testing cross-site fragment inheritance on a real multi-site corpus
2. C-LLM-INHERIT claim: Testing LLM-based parameter inheritance on diverse websites
3. Integration experiment: Can now design a concrete experiment testing SPIDER's fragment mechanism against WebArena's DOM

## Validity Threats

1. **Source inspection only**: No live execution. The observation format is as documented in code, but actual runtime behavior may differ (e.g., if CDP fails silently).
2. **Viewport filtering**: Default `current_viewport_only=True` means off-screen elements are not observed. SPIDER can override this.
3. **Observation truncation**: `max_obs_length=1920` truncates observations before LLM input. This is an agent-side constraint, not an environment limitation.
4. **Code evolution**: WebArena's codebase may change. Evidence is from the main branch as of 2026-09-04.
5. **Shadow DOM/iframe**: Not verified whether `Accessibility.getFullAXTree` traverses shadow DOM and iframes completely. Likely yes based on CDP documentation, but unconfirmed in live execution.
