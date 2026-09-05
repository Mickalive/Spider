#!/usr/bin/env python3
"""
EXP-INTEL-33945226776: WebArena Task Distribution Analysis

Estimates page complexity, truncation risk, and fragment yield across
WebArena site types to determine corpus suitability for C-CROSSSITE/
C-LLM-INHERIT integration experiments.

Three independent estimation methods:
1. Element-count-based: estimate DOM element count per page type
2. Char-length-based: estimate formatted observation string length
3. Task-type-based: URL-pattern complexity within site types
"""

import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ============================================================
# Constants from WebArena source code
# ============================================================
UTTERANCE_MAX_LENGTH = 8192  # observation_space truncation
MAX_OBS_LENGTH = 1920         # LLM input truncation
IN_VIEWPORT_RATIO_THRESHOLD = 0.6
IGNORED_ACTREE_PROPERTIES = ("focusable", "editable", "readonly", "level",
                              "settable", "multiline", "invalid")

# Estimated chars per element in formatted accessibility tree
# Format: [id] role "name" prop1: val1 prop2: val2
CHARS_PER_ELEMENT_MIN = 25   # [0] root "" (minimal)
CHARS_PER_ELEMENT_TYPICAL = 65  # [123] button "Submit" focused: True
CHARS_PER_ELEMENT_MAX = 120  # [456] combobox "Search products..." focused: True expanded: True selected: False


@dataclass
class TaskDef:
    task_id: int
    site: str  # shopping, shopping_admin, reddit, gitlab, map, misc
    intent: str
    intent_template_id: int | None
    eval_types: list[str]
    require_login: bool
    has_reference_url: bool
    intent_length: int  # chars


@dataclass
class SiteTypeStats:
    site_type: str
    task_count: int
    intent_lengths: list[int] = field(default_factory=list)
    eval_types: Counter = field(default_factory=Counter)
    intent_template_ids: set[int] = field(default_factory=set)
    unique_url_patterns: int = 0
    has_login: int = 0
    has_reference_url: int = 0


# ============================================================
# Element count estimation by page type
# ============================================================
# Based on domain knowledge of typical web pages
ELEMENT_COUNT_ESTIMATES = {
    # shopping (consumer-facing): product listings, product detail, cart, search, reviews
    "shopping": {
        "product_listing": {"min": 80, "typical": 150, "max": 300, "weight": 0.30},
        "product_detail": {"min": 60, "typical": 120, "max": 250, "weight": 0.25},
        "cart": {"min": 30, "typical": 60, "max": 120, "weight": 0.10},
        "search": {"min": 80, "typical": 160, "max": 350, "weight": 0.15},
        "reviews": {"min": 40, "typical": 80, "max": 150, "weight": 0.10},
        "account_orders": {"min": 20, "typical": 50, "max": 100, "weight": 0.10},
    },
    # shopping_admin (merchant admin): dashboard, product management, order management, analytics
    "shopping_admin": {
        "dashboard": {"min": 40, "typical": 80, "max": 150, "weight": 0.20},
        "product_list": {"min": 50, "typical": 100, "max": 200, "weight": 0.25},
        "order_list": {"min": 40, "typical": 80, "max": 160, "weight": 0.25},
        "analytics": {"min": 30, "typical": 60, "max": 120, "weight": 0.15},
        "settings": {"min": 20, "typical": 40, "max": 80, "weight": 0.15},
    },
    # reddit (self-hosted forum): subreddits, threads, comments, user profiles
    "reddit": {
        "subreddit_home": {"min": 60, "typical": 120, "max": 250, "weight": 0.20},
        "post_thread": {"min": 40, "typical": 100, "max": 300, "weight": 0.25},
        "comment_section": {"min": 50, "typical": 120, "max": 350, "weight": 0.25},
        "user_profile": {"min": 30, "typical": 60, "max": 120, "weight": 0.10},
        "search_results": {"min": 40, "typical": 80, "max": 180, "weight": 0.10},
        "settings": {"min": 15, "typical": 30, "max": 60, "weight": 0.10},
    },
    # gitlab (self-hosted): projects, repos, issues, merge requests, pipelines
    "gitlab": {
        "project_list": {"min": 40, "typical": 80, "max": 160, "weight": 0.15},
        "repo_file_tree": {"min": 50, "typical": 100, "max": 200, "weight": 0.15},
        "code_view": {"min": 30, "typical": 70, "max": 150, "weight": 0.15},
        "issue_list": {"min": 30, "typical": 60, "max": 120, "weight": 0.15},
        "merge_request": {"min": 40, "typical": 80, "max": 160, "weight": 0.15},
        "pipeline": {"min": 25, "typical": 50, "max": 100, "weight": 0.10},
        "settings": {"min": 20, "typical": 40, "max": 80, "weight": 0.05},
        "dashboard": {"min": 30, "typical": 60, "max": 120, "weight": 0.10},
    },
    # map (OpenStreetMap-based): map views, search, directions, place details
    "map": {
        "map_view": {"min": 30, "typical": 60, "max": 120, "weight": 0.30},
        "search_results": {"min": 20, "typical": 40, "max": 80, "weight": 0.25},
        "place_detail": {"min": 25, "typical": 50, "max": 100, "weight": 0.25},
        "directions": {"min": 15, "typical": 30, "max": 60, "weight": 0.20},
    },
    # wikipedia (CMS-like): article pages, edit pages, talk pages
    "wikipedia": {
        "article": {"min": 20, "typical": 45, "max": 90, "weight": 0.40},
        "article_list": {"min": 15, "typical": 35, "max": 70, "weight": 0.20},
        "talk_page": {"min": 10, "typical": 25, "max": 50, "weight": 0.15},
        "search": {"min": 15, "typical": 30, "max": 60, "weight": 0.15},
        "user_page": {"min": 10, "typical": 20, "max": 40, "weight": 0.10},
    },
}

# Typical roles per page type (for element diversity estimation)
ROLE_DISTRIBUTION = {
    "shopping": {
        "root": 1, "navigation": 1, "banner": 1, "main": 1,
        "link": 25, "button": 15, "img": 20, "heading": 5,
        "text": 30, "list": 8, "listitem": 15, "group": 10,
        "textbox": 3, "combobox": 2, "checkbox": 2,
        "table": 2, "row": 5, "cell": 15, "form": 3,
        "search": 1, "region": 5,
    },
    "shopping_admin": {
        "root": 1, "navigation": 1, "banner": 1, "main": 1,
        "link": 15, "button": 12, "img": 8, "heading": 6,
        "text": 20, "list": 5, "listitem": 10, "group": 6,
        "textbox": 4, "table": 4, "row": 10, "cell": 20,
        "form": 3, "tab": 3, "tablist": 1, "tabpanel": 3,
        "checkbox": 3, "combobox": 2,
    },
    "reddit": {
        "root": 1, "navigation": 1, "banner": 1, "main": 1,
        "link": 20, "button": 10, "img": 8, "heading": 8,
        "text": 35, "list": 3, "listitem": 8, "group": 5,
        "textbox": 3, "checkbox": 2, "region": 5,
        "article": 3, "form": 2,
    },
    "gitlab": {
        "root": 1, "navigation": 1, "banner": 1, "main": 1,
        "link": 18, "button": 10, "img": 5, "heading": 6,
        "text": 25, "list": 5, "listitem": 12, "group": 5,
        "textbox": 3, "table": 2, "row": 5, "cell": 10,
        "form": 2, "tab": 3, "tablist": 1, "tabpanel": 3,
        "code": 3,
    },
    "map": {
        "root": 1, "navigation": 1, "banner": 1, "main": 1,
        "link": 8, "button": 12, "img": 5, "heading": 3,
        "text": 15, "list": 3, "listitem": 5, "group": 5,
        "textbox": 3, "combobox": 2, "region": 5,
        "dialog": 1,
    },
    "wikipedia": {
        "root": 1, "navigation": 1, "main": 1, "banner": 1,
        "link": 15, "button": 3, "img": 5, "heading": 8,
        "text": 40, "list": 5, "listitem": 8, "group": 3,
        "table": 3, "row": 5, "cell": 10, "region": 5,
        "form": 1,
    },
}

# Viewport coverage estimate (fraction of elements visible)
VIEWPORT_COVERAGE = {
    "shopping": 0.45,       # product listings extend beyond viewport
    "shopping_admin": 0.55,  # admin dashboards somewhat more compact
    "reddit": 0.50,         # threads extend beyond viewport
    "gitlab": 0.55,         # code views somewhat more compact
    "map": 0.65,            # map views are mostly viewport-contained
    "wikipedia": 0.55,      # article pages are mostly viewport-contained
}

# Node pruning fraction (elements matching IGNORED_ACTREE_PROPERTIES)
NODE_PRUNING_FRACTION = {
    "shopping": 0.12,       # many focusable/readonly elements
    "shopping_admin": 0.15,  # more form elements with readonly
    "reddit": 0.10,         # fewer ignored properties
    "gitlab": 0.12,         # similar to shopping
    "map": 0.08,            # fewer form properties
    "wikipedia": 0.06,      # minimal interactive elements
}


def parse_tasks_from_file(filepath: str) -> list[TaskDef]:
    """Parse task definitions from WebArena test.raw.json"""
    with open(filepath) as f:
        tasks_raw = json.load(f)

    tasks = []
    for t in tasks_raw:
        # Support both 'site' (extracted) and 'sites' (raw) formats
        if "site" in t:
            site = t["site"]
        elif "sites" in t:
            sites = t["sites"]
            site = sites[0] if sites else "unknown"
        else:
            site = "unknown"
        intent = t.get("intent", "")
        eval_types = t.get("eval_types", t.get("eval", {}).get("eval_types", []))
        has_ref_url = t.get("has_reference_url", bool(t.get("eval", {}).get("reference_url", "")))

        tasks.append(TaskDef(
            task_id=t.get("task_id", -1),
            site=site,
            intent=intent,
            intent_template_id=t.get("intent_template_id"),
            eval_types=eval_types,
            require_login=t.get("require_login", False),
            has_reference_url=has_ref_url,
            intent_length=len(intent),
        ))
    return tasks


def compute_site_stats(tasks: list[TaskDef]) -> dict[str, SiteTypeStats]:
    """Compute per-site-type statistics"""
    stats = {}
    for task in tasks:
        site = task.site
        if site not in stats:
            stats[site] = SiteTypeStats(site_type=site, task_count=0)
        s = stats[site]
        s.task_count += 1
        s.intent_lengths.append(task.intent_length)
        for et in task.eval_types:
            s.eval_types[et] += 1
        if task.intent_template_id is not None:
            s.intent_template_ids.add(task.intent_template_id)
        if task.require_login:
            s.has_login += 1
        if task.has_reference_url:
            s.has_reference_url += 1

    # Estimate unique URL patterns per site type
    for site, s in stats.items():
        s.unique_url_patterns = len(s.intent_template_ids)

    return stats


# ============================================================
# Estimation Method 1: Element-Count-Based
# ============================================================
def estimate_fragment_yield_element_count(site_type: str) -> dict[str, Any]:
    """
    Estimate fragment yield based on typical DOM element counts
    per page type within each site type.
    """
    page_types = ELEMENT_COUNT_ESTIMATES.get(site_type, {})
    if not page_types:
        return {"error": f"Unknown site type: {site_type}"}

    results = {}
    for page_type, params in page_types.items():
        est_elements = params["typical"]
        weight = params["weight"]

        # Truncation: elements beyond UTTERANCE_MAX_LENGTH chars
        chars_per_elem = CHARS_PER_ELEMENT_TYPICAL
        total_chars = est_elements * chars_per_elem
        truncation_yield = min(1.0, UTTERANCE_MAX_LENGTH / total_chars) if total_chars > 0 else 0

        # Viewport filtering
        viewport_frac = VIEWPORT_COVERAGE.get(site_type, 0.5)
        viewport_yield = viewport_frac

        # Node pruning
        prune_frac = NODE_PRUNING_FRACTION.get(site_type, 0.10)
        pruning_yield = 1.0 - prune_frac

        # Combined yield
        combined_yield = truncation_yield * viewport_yield * pruning_yield

        # LLM input truncation (max_obs_length=1920)
        llm_truncation_yield = min(1.0, MAX_OBS_LENGTH / total_chars) if total_chars > 0 else 0

        results[page_type] = {
            "estimated_elements": est_elements,
            "estimated_chars": total_chars,
            "weight": weight,
            "truncation_yield": round(truncation_yield, 3),
            "viewport_yield": round(viewport_yield, 3),
            "pruning_yield": round(pruning_yield, 3),
            "combined_yield": round(combined_yield, 3),
            "llm_truncation_yield": round(llm_truncation_yield, 3),
        }

    # Weighted average yield
    weighted_yield = sum(
        r["combined_yield"] * r["weight"] for r in results.values()
    )
    weighted_llm_yield = sum(
        r["llm_truncation_yield"] * r["weight"] for r in results.values()
    )

    return {
        "page_types": results,
        "weighted_median_yield": round(weighted_yield, 3),
        "weighted_llm_yield": round(weighted_llm_yield, 3),
    }


# ============================================================
# Estimation Method 2: Char-Length-Based
# ============================================================
def estimate_fragment_yield_char_length(site_type: str) -> dict[str, Any]:
    """
    Estimate fragment yield based on formatted observation string length.
    """
    page_types = ELEMENT_COUNT_ESTIMATES.get(site_type, {})
    if not page_types:
        return {"error": f"Unknown site type: {site_type}"}

    results = {}
    for page_type, params in page_types.items():
        est_elements = params["typical"]
        weight = params["weight"]

        # Estimate total chars at different chars-per-element rates
        chars_min = est_elements * CHARS_PER_ELEMENT_MIN
        chars_typical = est_elements * CHARS_PER_ELEMENT_TYPICAL
        chars_max = est_elements * CHARS_PER_ELEMENT_MAX

        # Yield at UTTERANCE_MAX_LENGTH
        yield_at_utterance = min(1.0, UTTERANCE_MAX_LENGTH / chars_typical) if chars_typical > 0 else 0
        yield_at_utterance_min = min(1.0, UTTERANCE_MAX_LENGTH / chars_max) if chars_max > 0 else 0
        yield_at_utterance_max = min(1.0, UTTERANCE_MAX_LENGTH / chars_min) if chars_min > 0 else 0

        # Yield at MAX_OBS_LENGTH
        yield_at_llm = min(1.0, MAX_OBS_LENGTH / chars_typical) if chars_typical > 0 else 0
        yield_at_llm_min = min(1.0, MAX_OBS_LENGTH / chars_max) if chars_max > 0 else 0
        yield_at_llm_max = min(1.0, MAX_OBS_LENGTH / chars_min) if chars_min > 0 else 0

        # Max elements surviving
        max_elems_at_utterance = min(est_elements, int(UTTERANCE_MAX_LENGTH / CHARS_PER_ELEMENT_TYPICAL))
        max_elems_at_llm = min(est_elements, int(MAX_OBS_LENGTH / CHARS_PER_ELEMENT_TYPICAL))

        results[page_type] = {
            "estimated_elements": est_elements,
            "chars_range": [chars_min, chars_typical, chars_max],
            "yield_at_utterance_8192": round(yield_at_utterance, 3),
            "yield_range_at_utterance": [round(yield_at_utterance_min, 3), round(yield_at_utterance, 3), round(yield_at_utterance_max, 3)],
            "yield_at_llm_1920": round(yield_at_llm, 3),
            "yield_range_at_llm": [round(yield_at_llm_min, 3), round(yield_at_llm, 3), round(yield_at_llm_max, 3)],
            "max_elements_at_utterance": max_elems_at_utterance,
            "max_elements_at_llm": max_elems_at_llm,
            "weight": weight,
        }

    weighted_yield = sum(r["yield_at_utterance_8192"] * r["weight"] for r in results.values())
    weighted_llm_yield = sum(r["yield_at_llm_1920"] * r["weight"] for r in results.values())

    return {
        "page_types": results,
        "weighted_median_yield": round(weighted_yield, 3),
        "weighted_llm_yield": round(weighted_llm_yield, 3),
    }


# ============================================================
# Estimation Method 3: Task-Type-Based (URL pattern complexity)
# ============================================================
def estimate_fragment_yield_task_type(site_type: str, stats: SiteTypeStats) -> dict[str, Any]:
    """
    Estimate fragment yield based on task URL patterns and intent complexity.
    Uses intent length as a proxy for page complexity.
    """
    if not stats.intent_lengths:
        return {"error": "No tasks for site type"}

    import statistics
    median_intent_len = statistics.median(stats.intent_lengths)
    mean_intent_len = statistics.mean(stats.intent_lengths)
    max_intent_len = max(stats.intent_lengths)
    min_intent_len = min(stats.intent_lengths)

    # Map intent length to complexity
    # Longer intents often visit more complex pages
    if median_intent_len > 80:
        complexity_class = "high"
        base_yield = 0.65
    elif median_intent_len > 50:
        complexity_class = "moderate"
        base_yield = 0.55
    else:
        complexity_class = "low"
        base_yield = 0.45

    # Adjust by site type baseline complexity
    site_complexity_adjustment = {
        "shopping": 0.10,       # product pages are element-dense
        "shopping_admin": 0.05,  # admin pages are structured but dense
        "reddit": 0.0,          # baseline
        "gitlab": -0.05,        # code views are somewhat simpler
        "map": -0.10,           # map views are simpler
        "wikipedia": -0.15,     # article pages are simplest
    }

    adjusted_yield = base_yield + site_complexity_adjustment.get(site_type, 0)
    adjusted_yield = max(0.1, min(0.95, adjusted_yield))

    # Evaluate diversity
    unique_templates = len(stats.intent_template_ids)
    eval_diversity = len(stats.eval_types)

    return {
        "task_count": stats.task_count,
        "median_intent_length": round(median_intent_len, 1),
        "mean_intent_length": round(mean_intent_len, 1),
        "min_intent_length": min_intent_len,
        "max_intent_length": max_intent_len,
        "complexity_class": complexity_class,
        "estimated_yield": round(adjusted_yield, 3),
        "unique_template_ids": unique_templates,
        "eval_type_diversity": eval_diversity,
        "eval_types": dict(stats.eval_types),
        "fraction_requiring_login": round(stats.has_login / stats.task_count, 3) if stats.task_count > 0 else 0,
        "fraction_with_reference_url": round(stats.has_reference_url / stats.task_count, 3) if stats.task_count > 0 else 0,
    }


# ============================================================
# Statistical tests
# ============================================================
def spearman_rank_correlation(x: list[float], y: list[float]) -> float:
    """Compute Spearman rank correlation between two lists."""
    n = len(x)
    if n < 3:
        return 0.0

    # Rank the values
    def rank_data(data):
        sorted_indices = sorted(range(n), key=lambda i: data[i])
        ranks = [0.0] * n
        for rank, idx in enumerate(sorted_indices, 1):
            ranks[idx] = rank
        return ranks

    rank_x = rank_data(x)
    rank_y = rank_data(y)

    # Compute d^2
    d_sq = sum((rx - ry) ** 2 for rx, ry in zip(rank_x, rank_y))

    return 1.0 - (6 * d_sq) / (n * (n * n - 1))


def kruskal_wallis_test(groups: list[list[float]]) -> dict[str, Any]:
    """Simplified Kruskal-Wallis H test."""
    all_data = []
    for g in groups:
        all_data.extend(g)
    N = len(all_data)
    k = len(groups)

    if N == 0 or k < 2:
        return {"H": 0, "df": k - 1, "p_approx": 1.0}

    # Rank all data
    sorted_data = sorted(enumerate(all_data), key=lambda x: x[1])
    ranks = [0.0] * N
    for rank, (orig_idx, _) in enumerate(sorted_data, 1):
        ranks[orig_idx] = rank

    # Compute H
    rank_sums = []
    start = 0
    for g in groups:
        end = start + len(g)
        rank_sums.append(sum(ranks[start:end]))
        start = end

    H = (12 / (N * (N + 1))) * sum(rs**2 / len(g) for rs, g in zip(rank_sums, groups)) - 3 * (N + 1)

    # Approximate p-value using chi-squared with k-1 df
    # For small samples, this is approximate
    import math
    df = k - 1
    if df <= 0:
        p_approx = 1.0
    else:
        # Rough chi-squared approximation
        if H > 0:
            # Use Wilson-Hilferty approximation
            z = (H / df) ** (1/3) - (1 - 2 / (9 * df))
            z /= math.sqrt(2 / (9 * df))
            # Rough normal CDF approximation
            p_approx = 0.5 * math.erfc(z / math.sqrt(2))
        else:
            p_approx = 1.0

    return {"H": round(H, 4), "df": df, "p_approx": round(min(1.0, max(0.0, p_approx)), 4)}


# ============================================================
# Main analysis
# ============================================================
def run_analysis(tasks_file: str) -> dict[str, Any]:
    """Run the full analysis pipeline."""
    # Parse tasks
    tasks = parse_tasks_from_file(tasks_file)
    stats = compute_site_stats(tasks)

    # Site types observed
    site_types = sorted(stats.keys())

    # Run three estimation methods
    method1_results = {}  # element-count
    method2_results = {}  # char-length
    method3_results = {}  # task-type

    for site in site_types:
        method1_results[site] = estimate_fragment_yield_element_count(site)
        method2_results[site] = estimate_fragment_yield_char_length(site)
        method3_results[site] = estimate_fragment_yield_task_type(site, stats[site])

    # Aggregate yields per site type across methods
    aggregated = {}
    for site in site_types:
        yields = []
        if "weighted_median_yield" in method1_results.get(site, {}):
            yields.append(method1_results[site]["weighted_median_yield"])
        if "weighted_median_yield" in method2_results.get(site, {}):
            yields.append(method2_results[site]["weighted_median_yield"])
        if "estimated_yield" in method3_results.get(site, {}):
            yields.append(method3_results[site]["estimated_yield"])

        import statistics
        median_yield = statistics.median(yields) if yields else 0
        mean_yield = statistics.mean(yields) if yields else 0

        # Element diversity (unique roles per page)
        roles = ROLE_DISTRIBUTION.get(site, {})
        element_diversity = len(roles)

        aggregated[site] = {
            "median_yield": round(median_yield, 3),
            "mean_yield": round(mean_yield, 3),
            "method_yields": yields,
            "element_diversity": element_diversity,
            "task_count": stats[site].task_count,
            "unique_templates": len(stats[site].intent_template_ids),
        }

    # Method agreement (Spearman correlation)
    # Use the 3 method yields across site types
    site_yields_m1 = [aggregated[s]["method_yields"][0] for s in site_types if len(aggregated[s]["method_yields"]) > 0]
    site_yields_m2 = [aggregated[s]["method_yields"][1] for s in site_types if len(aggregated[s]["method_yields"]) > 1]
    site_yields_m3 = [aggregated[s]["method_yields"][2] for s in site_types if len(aggregated[s]["method_yields"]) > 2]

    min_len = min(len(site_yields_m1), len(site_yields_m2), len(site_yields_m3))
    if min_len >= 3:
        rho_m1_m2 = spearman_rank_correlation(site_yields_m1[:min_len], site_yields_m2[:min_len])
        rho_m1_m3 = spearman_rank_correlation(site_yields_m1[:min_len], site_yields_m3[:min_len])
        rho_m2_m3 = spearman_rank_correlation(site_yields_m2[:min_len], site_yields_m3[:min_len])
    else:
        rho_m1_m2 = rho_m1_m3 = rho_m2_m3 = None

    method_agreement = {
        "spearman_m1_m2": rho_m1_m2,
        "spearman_m1_m3": rho_m1_m3,
        "spearman_m2_m3": rho_m2_m3,
    }

    # Kruskal-Wallis test (are yields different across site types?)
    kw_groups = [aggregated[s]["method_yields"] for s in site_types if aggregated[s]["method_yields"]]
    kw_result = kruskal_wallis_test(kw_groups) if len(kw_groups) >= 2 else {"H": 0, "df": 0, "p_approx": 1.0}

    # Threshold tests
    sites_above_50 = [s for s in site_types if aggregated[s]["median_yield"] > 0.50]
    sites_below_30 = [s for s in site_types if aggregated[s]["median_yield"] < 0.30]

    # Decision
    support_count = len(sites_above_50)
    falsify_count = len(sites_below_30)

    # Positive control: shopping should be highest
    shopping_yield = aggregated.get("shopping", {}).get("median_yield", 0)
    shopping_admin_yield = aggregated.get("shopping_admin", {}).get("median_yield", 0)
    shopping_is_high = shopping_yield > 0.50 or shopping_admin_yield > 0.50

    # Null control: wikipedia should be lowest
    wikipedia_yield = aggregated.get("wikipedia", {}).get("median_yield", 1.0)
    site_yields_for_wiki = [aggregated[s]["median_yield"] for s in site_types if s != "wikipedia"]
    wikipedia_is_lowest = wikipedia_yield <= min(site_yields_for_wiki) if site_yields_for_wiki else False

    # Method agreement check
    method_agreement_ok = True
    if rho_m1_m2 is not None:
        method_agreement_ok = (
            (rho_m1_m2 is None or rho_m1_m2 > 0.3) and
            (rho_m1_m3 is None or rho_m1_m3 > 0.3) and
            (rho_m2_m3 is None or rho_m2_m3 > 0.3)
        )

    # Overall verdict
    if support_count >= 2 and shopping_is_high and method_agreement_ok:
        verdict = "SUPPORTS"
    elif falsify_count == len(site_types) or (support_count == 0 and falsify_count >= 2):
        verdict = "FALSIFIES"
    else:
        verdict = "MIXED"

    # Truncation sensitivity
    truncation_sensitivity = {}
    for site in site_types:
        m2 = method2_results.get(site, {})
        if "page_types" in m2:
            yields_at_8192 = [pt["yield_at_utterance_8192"] for pt in m2["page_types"].values()]
            yields_at_1920 = [pt["yield_at_llm_1920"] for pt in m2["page_types"].values()]
            if yields_at_8192 and yields_at_1920:
                truncation_sensitivity[site] = {
                    "yield_at_8192": round(statistics.mean(yields_at_8192), 3),
                    "yield_at_1920": round(statistics.mean(yields_at_1920), 3),
                    "sensitivity_ratio": round(statistics.mean(yields_at_1920) / statistics.mean(yields_at_8192), 3) if statistics.mean(yields_at_8192) > 0 else 0,
                }

    return {
        "total_tasks": len(tasks),
        "site_types": site_types,
        "site_stats": {s: {
            "task_count": stats[s].task_count,
            "unique_templates": len(stats[s].intent_template_ids),
            "eval_types": dict(stats[s].eval_types),
            "fraction_login_required": round(stats[s].has_login / stats[s].task_count, 3) if stats[s].task_count > 0 else 0,
            "median_intent_length": round(statistics.median(stats[s].intent_lengths), 1) if stats[s].intent_lengths else 0,
        } for s in site_types},
        "method1_element_count": method1_results,
        "method2_char_length": method2_results,
        "method3_task_type": method3_results,
        "aggregated": aggregated,
        "method_agreement": method_agreement,
        "kruskal_wallis": kw_result,
        "threshold_tests": {
            "sites_above_50pct": sites_above_50,
            "sites_below_30pct": sites_below_30,
            "support_count": support_count,
            "falsify_count": falsify_count,
        },
        "controls": {
            "positive_control_shopping_high": shopping_is_high,
            "positive_control_shopping_yield": shopping_yield,
            "null_control_wikipedia_lowest": wikipedia_is_lowest,
            "null_control_wikipedia_yield": wikipedia_yield,
            "method_agreement_ok": method_agreement_ok,
        },
        "truncation_sensitivity": truncation_sensitivity,
        "verdict": verdict,
    }


if __name__ == "__main__":
    tasks_file = sys.argv[1] if len(sys.argv) > 1 else "/tmp/webarena_tasks.json"
    result = run_analysis(tasks_file)
    print(json.dumps(result, indent=2))
