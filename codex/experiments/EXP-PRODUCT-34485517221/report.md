# EXP-PRODUCT-34485517221 Report

## Executive Summary

**Verdict: MIXED** — 4/7 conditions pass, structural generalization rate 60%.

The leaf-path URL-as-string prefix extraction heuristic (rfind('/') based) partially generalizes to structurally different URL patterns. It handles query-string multi-parameter URLs, deep path URLs, and path+query hybrid URLs correctly. However, it fails on three conditions:

1. **G1 (Query String Simple)**: Common suffix extraction captures trailing characters from training values, corrupting the template.
2. **G4 (Multi-Slot)**: The leaf-path model treats URLs as single fields, detecting only 1 slot when 2 vary.
3. **N1 (No Common Prefix)**: The heuristic over-parameterizes URLs that share a short prefix but are structurally different.

## Detailed Findings

### Conditions That Pass

**P1_PATH_PREFIX (Positive Control)**: Replicates the established pattern. slot_count=1, binding_accuracy=1.0. Template: `https://api.example.com/users/${url}`. Verifies pipeline works.

**G2_QUERY_STRING_MULTIPARAM**: The heuristic correctly identifies that only `page` varies while `category=books` is constant. Common prefix: `https://api.example.com/items?category=books&page=`. slot_prefixes={'url': 'items?category=books&page='}. Binding produces correct URLs for unseen page values.

**G3_DEEP_PATH**: The heuristic handles deep path structures correctly. Template: `https://api.example.com/orgs/acme/repos/main/issues/${url}`. The rfind('/') correctly places the slot boundary at the last segment.

**G5_PATH_QUERY_HYBRID**: The heuristic correctly identifies the varying path segment while treating the constant query parameter as part of the URL. Template: `https://api.example.com/users/${url}/items?page=1`. Binding produces correct URLs.

### Conditions That Fail

**G1_QUERY_STRING_SIMPLE**: The rfind('/') heuristic correctly extracts `search?q=` as the slot prefix. However, the common suffix extraction captures trailing 'a' from training values (alpha, beta, delta all end with 'a'). This produces template `search?q=${url}a`, causing binding to produce `search?q=gammaa` instead of `search?q=gamma`.

**Root cause**: The `_find_common_prefix_suffix` function extracts the longest common suffix across all training values. When training values share trailing characters, the suffix is incorrectly included in the template.

**G4_MULTI_SLOT**: The leaf-path model treats the URL as a single field path. It detects only 1 varying slot (expected 2). The template becomes `users/${url}00` due to common suffix '00' from order IDs (100, 200, 300). Multi-segment URL patterns with multiple varying parts cannot be parameterized.

**Root cause**: Architectural limitation. The URL is a single leaf value in the action dict, not a decomposable structure. The leaf-path model cannot split a single URL field into multiple parameter slots.

**N1_NO_COMMON_PREFIX**: The heuristic finds common prefix `https://api.` across URLs from different hosts (api.example.com, api.other.com, api.third.com) and incorrectly parameterizes them. Expected slot_count=0 but observed slot_count=1.

**Root cause**: The heuristic has no similarity threshold or host-awareness. It parameterizes any URLs sharing a common prefix, regardless of structural similarity.

## Product Consequences

### What This Means for C-PARAM-INHERIT

The claim "Mechanisms parameterize to received identifiers" is **partially supported**:
- Path-prefix patterns: SUPPORTED (P1, G3, G5)
- Query-string patterns: MIXED (G2 passes, G1 fails due to suffix extraction)
- Multi-slot patterns: FALSIFIED for leaf-path model (G4)
- Null control: FALSIFIED (N1 over-parameterizes)

### What This Means for C-PRODUCT-ECON

The C-PRODUCT-ECON economics measurement is **blocked** until:
1. The suffix extraction issue is fixed (affects query-string patterns)
2. A decision is made on multi-slot support (architectural change required)
3. The over-parameterization issue is addressed (similarity threshold or host-awareness)

### Recommendation

The kernel requires three targeted fixes before product economics measurement:
1. **Fix suffix extraction**: Exclude common suffix from template when it doesn't represent a structural pattern (e.g., trailing characters from training values)
2. **Add similarity threshold**: Prevent parameterization of structurally different URLs that share short prefixes
3. **Decide on multi-slot**: Either extend the leaf-path model to support multi-slot URLs, or document this as a known limitation

These are bounded fixes that don't require architectural changes. The rfind('/') prefix extraction heuristic itself works correctly for the patterns it was designed to handle.

## Comparison with Parent Experiment

The parent experiment (EXP-PRODUCT-34420092879) established kernel correctness on 10 conditions with binding_accuracy=1.0. This experiment tests the specific V3_REPRESENTATION_LOSS finding from the parent audit. The results show:

- The parent experiment's D2 condition (query string with multiple parameters) worked because the training values had different suffixes (page=1/2/3), avoiding the suffix extraction issue.
- This experiment's G1 condition fails because the training values share a trailing character ('a' from alpha/beta/delta).
- The parent experiment did not test multi-slot or no-common-prefix patterns, so those failures are new findings.

The parent experiment's claim ceiling was "synthetic kernel correctness only." This experiment validates (or invalidates) the heuristic's behavior on structurally different URL patterns, which is a prerequisite for product economics measurement.
