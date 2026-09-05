# EXP-INTEL-33925056324 — Execution Report

## Experiment Summary

**Question**: Can SPIDER's fragment extraction logic be adapted to extract reusable fragments from WebArena's accessibility tree observation format, and what is the transformation cost?

**Verdict**: SUPPORTS — The transformation cost is low. A 224-line adapter (zero external dependencies) successfully extracts elements with identity, hierarchy, attributes, and text from synthetic WebArena accessibility tree observations across all three site types.

## Results

### Primary Metrics

| Metric | Threshold | E-commerce | Social Forum | Coding | Mean | Min |
|--------|-----------|-----------|-------------|--------|------|-----|
| Element Recall | >= 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Attribute Preservation | >= 0.80 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Hierarchy Preservation | >= 0.80 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

All three metrics exceed their thresholds across all site types with zero variance.

### Controls

- **Positive control** (100 known elements): PASS — all elements extracted with correct attributes and hierarchy.
- **Null control** (screenshots only, no DOM): PASS — zero elements extracted.

### Transformation Cost

- Adapter: 224 lines of Python (standard library only)
- Dependencies added: 0
- External API calls: 0

## Interpretation

### What This Means

The adapter successfully recomposes WebArena's split observation channels (formatted indented string + obs_nodes_info metadata) into structured fragments. The transformation logic is:

1. **Parse formatted string**: Regex extraction of element IDs, roles, names, and ARIA properties from indented text lines.
2. **Reconstruct hierarchy**: Indentation-based parent-child relationship inference via a stack algorithm.
3. **Recompose metadata**: Mapping element IDs to obs_nodes_info for backend_id, union_bound, and text.
4. **Role normalization**: Mapping ARIA role names (e.g., RootWebArea → root) for consistency with SPIDER's fragment model.

### Product Consequence

The SUPPORTS verdict means:
- **Transformation cost is low** — 224 lines, zero dependencies, offline computation.
- **WebArena's 812-task corpus expansion is worth the REQUIRES_TRANSFORM overhead.**
- **C-CROSSSITE and C-LLM-INHERIT can proceed with an integration experiment** in the graph lane.

### What This Does NOT Mean

This experiment tested synthetic observations only. The following unknowns remain:

1. **Real WebArena Docker output** may present edge cases not captured in synthetic data (truncation, shadow DOM, iframes, viewport filtering).
2. **html mode** (DOMSnapshot with HTML attributes) may yield different results than accessibility_tree mode.
3. **UTTERANCE_MAX_LENGTH=8192 truncation** may discard fragments on large pages.
4. **End-to-end integration** with SPIDER's fragment reuse pipeline is untested.

### Validity Threats

1. **Synthetic-to-real gap**: The most significant threat. Synthetic observations mimic WebArena's format but are not generated from live Docker. Success on synthetic is necessary but not sufficient for real WebArena DOM.
2. **Sample size**: 300 elements across 3 site types. Sufficient for large effects, may miss rare edge cases.
3. **Element diversity**: Synthetic elements may not capture all real WebArena element patterns (complex ARIA trees, deeply nested iframes, dynamic content).
4. **Adapter scope**: Minimal adapter covers core extraction. Viewport override, truncation handling, shadow DOM traversal are out of scope.

## Decision Rule Evaluation

Per the frozen spec:
- element_recall >= 0.90 across all site types: **YES** (1.00)
- attribute_preservation >= 0.80 across all site types: **YES** (1.00)
- hierarchy_preservation >= 0.80 across all site types: **YES** (1.00)
- Positive control passes: **YES**
- Null control passes: **YES**
- No pipeline errors: **YES**

**Verdict: SUPPORTS**
