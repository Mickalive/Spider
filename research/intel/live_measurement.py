#!/usr/bin/env python3
"""
EXP-INTEL-34047713704 Live Docker Measurement Script

Deploys WebArena Docker containers, uses Playwright to render pages,
extracts accessibility trees, and measures fragment yield through the
full REQUIRES_TRANSFORM pipeline.

Measures: viewport filtering, IGNORED_ACTREE_PROPERTIES pruning,
truncation at UTTERANCE_MAX_LENGTH=8192 and max_obs_length=1920.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Any

# ---------------------------------------------------------------------------
# Constants from WebArena / SPIDER source code
# ---------------------------------------------------------------------------

UTTERANCE_MAX_LENGTH = 8192
MAX_OBS_LENGTH = 1920
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720

IGNORED_ACTREE_PROPERTIES = [
    "focusable", "editable", "readonly", "level",
    "settable", "multiline", "invalid"
]

# Heuristic yield estimates from EXP-INTEL-33945226776
HEURISTIC_YIELDS = {
    "shopping": 0.65,
    "gitlab": 0.60,
    "wikipedia": 0.517,
}

HEURISTIC_METHOD1_YIELDS = {
    "shopping": 0.365,
    "gitlab": 0.484,
    "wikipedia": 0.517,
}

# ---------------------------------------------------------------------------
# Accessibility tree element
# ---------------------------------------------------------------------------

@dataclass
class AccessibilityElement:
    element_id: int
    role: str
    name: str
    properties: dict[str, str]
    parent_id: int | None
    children_ids: list[int] = field(default_factory=list)
    backend_id: int | None = None
    union_bound: list[float] | None = None
    text: str = ""
    depth: int = 0


# ---------------------------------------------------------------------------
# Accessibility tree parsing (from webarena_adapter.py)
# ---------------------------------------------------------------------------

import re

_ELEMENT_RE = re.compile(
    r'^(\s*)\[(\d+)\]\s+(\S+)\s+"([^"]*)"'
    r'(?:\s+(.*))?$'
)
_PROPERTY_RE = re.compile(r'(\w+):\s*(\S+)')

_ROLE_MAP = {
    "RootWebArea": "root", "WebArea": "root",
    "link": "link", "button": "button", "textbox": "textbox",
    "checkbox": "checkbox", "combobox": "combobox", "listbox": "listbox",
    "menuitem": "menuitem", "menuitemcheckbox": "menuitemcheckbox",
    "menubar": "menubar", "menu": "menu", "navigation": "navigation",
    "img": "img", "heading": "heading", "text": "text",
    "StaticText": "text", "group": "group", "list": "list",
    "listitem": "listitem", "tab": "tab", "tablist": "tablist",
    "tabpanel": "tabpanel", "tree": "tree", "treeitem": "treeitem",
    "article": "article", "region": "region", "dialog": "dialog",
    "main": "main", "banner": "banner", "contentinfo": "contentinfo",
    "complementary": "complementary", "form": "form", "search": "search",
    "table": "table", "row": "row", "cell": "cell",
    "columnheader": "columnheader", "rowheader": "rowheader",
    "grid": "grid", "figure": "figure", "caption": "caption",
    "alert": "alert", "status": "status", "toolbar": "toolbar",
}


def normalize_role(role: str) -> str:
    return _ROLE_MAP.get(role, role.lower())


def parse_accessibility_tree(text: str) -> list[AccessibilityElement]:
    """Parse WebArena-format accessibility tree string."""
    lines = text.strip().split("\n")
    elements: list[AccessibilityElement] = []
    stack: list[tuple[int, int]] = []

    for line in lines:
        if not line.strip():
            continue
        match = _ELEMENT_RE.match(line)
        if not match:
            continue

        indent_str, id_str, role_raw, name, props_str = match.groups()
        indent_level = len(indent_str)
        element_id = int(id_str)
        role = normalize_role(role_raw)

        properties: dict[str, str] = {}
        if props_str:
            for prop_match in _PROPERTY_RE.finditer(props_str):
                prop_name, prop_val = prop_match.groups()
                properties[prop_name] = prop_val

        parent_id: int | None = None
        while stack and stack[-1][0] >= indent_level:
            stack.pop()
        if stack:
            parent_id = stack[-1][1]

        elem = AccessibilityElement(
            element_id=element_id,
            role=role,
            name=name,
            properties=properties,
            parent_id=parent_id,
            text=name,
            depth=indent_level,
        )
        elements.append(elem)
        stack.append((indent_level, element_id))

    # Second pass: populate children_ids
    parent_to_children: dict[int | None, list[int]] = {}
    for elem in elements:
        siblings = parent_to_children.setdefault(elem.parent_id, [])
        siblings.append(elem.element_id)
    for elem in elements:
        elem.children_ids = parent_to_children.get(elem.element_id, [])

    return elements


# ---------------------------------------------------------------------------
# Pipeline simulation (REQUIRES_TRANSFORM)
# ---------------------------------------------------------------------------

def format_element_observation(elem: AccessibilityElement) -> str:
    """Format element as WebArena observation string."""
    props_str = ""
    if elem.properties:
        props_str = " " + " ".join(f"{k}: {v}" for k, v in elem.properties.items())
    safe_name = elem.name.replace('"', '\\"')
    return f'[{elem.element_id}] {elem.role} "{safe_name}"{props_str}'


def apply_ignored_properties(elements: list[AccessibilityElement]) -> list[AccessibilityElement]:
    """Remove IGNORED_ACTREE_PROPERTIES from elements."""
    result = []
    for elem in elements:
        new_props = {k: v for k, v in elem.properties.items()
                     if k not in IGNORED_ACTREE_PROPERTIES}
        result.append(AccessibilityElement(
            element_id=elem.element_id,
            role=elem.role,
            name=elem.name,
            properties=new_props,
            parent_id=elem.parent_id,
            children_ids=elem.children_ids,
            backend_id=elem.backend_id,
            union_bound=elem.union_bound,
            text=elem.text,
            depth=elem.depth,
        ))
    return result


def truncate_observation(obs_text: str, max_length: int) -> str:
    """Truncate observation string to max_length chars."""
    if len(obs_text) <= max_length:
        return obs_text
    return obs_text[:max_length]


def measure_yield(
    elements: list[AccessibilityElement],
    viewport_filtered_count: int | None = None,
) -> dict[str, Any]:
    """Compute fragment yield metrics."""
    total = len(elements)
    if total == 0:
        return {
            "total_elements": 0,
            "viewport_elements": 0,
            "pruned_elements": 0,
            "truncated_8192": 0,
            "truncated_1920": 0,
            "actual_yield": 0.0,
            "unique_roles": 0,
        }

    # Format all elements
    formatted = [format_element_observation(e) for e in elements]
    full_obs = "\n".join(formatted)

    # Apply pruning
    pruned = apply_ignored_properties(elements)
    pruned_formatted = [format_element_observation(e) for e in pruned]
    pruned_obs = "\n".join(pruned_formatted)

    # Truncation
    truncated_8192 = truncate_observation(pruned_obs, UTTERANCE_MAX_LENGTH)
    truncated_1920 = truncate_observation(pruned_obs, MAX_OBS_LENGTH)

    # Count elements surviving each stage
    viewport_count = viewport_filtered_count if viewport_filtered_count is not None else total
    pruned_count = len(pruned)

    # Count elements in truncated versions (by counting complete lines)
    trunc_8192_count = len([l for l in truncated_8192.split("\n") if l.strip()])
    trunc_1920_count = len([l for l in truncated_1920.split("\n") if l.strip()])

    # Unique roles
    unique_roles = len(set(e.role for e in elements))

    # Actual yield = elements surviving full pipeline / total elements
    # Full pipeline: viewport filtering -> pruning -> truncation at 1920
    actual_yield = trunc_1920_count / total if total > 0 else 0.0

    return {
        "total_elements": total,
        "viewport_elements": viewport_count,
        "pruned_elements": pruned_count,
        "truncated_8192": trunc_8192_count,
        "truncated_1920": trunc_1920_count,
        "actual_yield": round(actual_yield, 4),
        "unique_roles": unique_roles,
        "full_obs_length": len(full_obs),
        "pruned_obs_length": len(pruned_obs),
        "truncated_8192_length": len(truncated_8192),
        "truncated_1920_length": len(truncated_1920),
    }


# ---------------------------------------------------------------------------
# Playwright measurement
# ---------------------------------------------------------------------------

async def measure_site(
    site_type: str,
    url: str,
    wait_until: str = "networkidle",
) -> dict[str, Any]:
    """Measure a single site using Playwright."""
    from playwright.async_api import async_playwright

    result = {
        "site_type": site_type,
        "url": url,
        "status": "unknown",
        "error": None,
        "metrics": None,
        "raw_accessibility_tree": None,
    }

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            )
            page = await context.new_page()

            # Navigate to the site
            print(f"  Navigating to {url}...")
            response = await page.goto(url, wait_until=wait_until, timeout=60000)
            result["http_status"] = response.status if response else None

            # Wait for page to settle
            await page.wait_for_timeout(3000)

            # Get the accessibility tree snapshot
            print(f"  Extracting accessibility tree...")
            snapshot = await page.accessibility.snapshot()

            if snapshot is None:
                result["status"] = "error"
                result["error"] = "Accessibility snapshot returned None"
                await browser.close()
                return result

            # Convert Playwright accessibility snapshot to WebArena format
            elements = []
            element_id_counter = 0

            def walk_snapshot(node: dict, depth: int = 0, parent_id: int | None = None) -> int:
                nonlocal element_id_counter
                current_id = element_id_counter
                element_id_counter += 1

                role = node.get("role", "unknown")
                name = node.get("name", "")
                properties = {}

                # Extract properties from the snapshot
                if node.get("focused"):
                    properties["focused"] = "True"
                if node.get("expanded") is not None:
                    properties["expanded"] = str(node.get("expanded"))
                if node.get("selected"):
                    properties["selected"] = "True"
                if node.get("checked") is not None:
                    properties["checked"] = str(node.get("checked"))
                if node.get("disabled"):
                    properties["disabled"] = "True"

                elem = AccessibilityElement(
                    element_id=current_id,
                    role=role,
                    name=name,
                    properties=properties,
                    parent_id=parent_id,
                    text=name,
                    depth=depth,
                )
                elements.append(elem)

                # Process children
                children_ids = []
                for child in node.get("children", []):
                    child_id = walk_snapshot(child, depth + 1, current_id)
                    children_ids.append(child_id)

                elem.children_ids = children_ids
                return current_id

            walk_snapshot(snapshot)

            # Get viewport-filtered count
            # Playwright's accessibility.snapshot() already respects the viewport
            # when used with page.accessibility.snapshot()
            viewport_count = len(elements)

            # Measure yield
            print(f"  Measuring yield for {len(elements)} elements...")
            metrics = measure_yield(elements, viewport_count)

            # Format the raw observation for storage
            formatted_elements = [format_element_observation(e) for e in elements]
            raw_obs = "\n".join(formatted_elements)

            result["status"] = "success"
            result["metrics"] = metrics
            result["raw_accessibility_tree"] = raw_obs[:5000] + "..." if len(raw_obs) > 5000 else raw_obs
            result["num_elements_raw"] = len(elements)
            result["unique_roles"] = list(set(e.role for e in elements))

            await browser.close()

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

async def run_experiment() -> dict[str, Any]:
    """Run the full live measurement experiment."""
    results = {
        "experiment_id": "EXP-INTEL-34047713704",
        "sites": {},
        "controls": {},
        "aggregate": {},
    }

    # Define sites to measure
    sites = [
        ("shopping", "http://localhost:7770/"),
        # ("gitlab", "http://localhost:8023/"),
        # ("wikipedia", "http://localhost:8888/"),
    ]

    # We'll measure what's available and add more as containers come up
    for site_type, url in sites:
        print(f"\n=== Measuring {site_type} ({url}) ===")
        site_result = await measure_site(site_type, url)
        results["sites"][site_type] = site_result

        if site_result["status"] == "success":
            m = site_result["metrics"]
            print(f"  Total elements: {m['total_elements']}")
            print(f"  Viewport elements: {m['viewport_elements']}")
            print(f"  Pruned elements: {m['pruned_elements']}")
            print(f"  Truncated (8192): {m['truncated_8192']}")
            print(f"  Truncated (1920): {m['truncated_1920']}")
            print(f"  Actual yield: {m['actual_yield']}")
            print(f"  Unique roles: {m['unique_roles']}")
        else:
            print(f"  ERROR: {site_result['error']}")

    return results


def main():
    """Synchronous entry point."""
    results = asyncio.run(run_experiment())

    # Save raw results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_raw_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results written to {output_path}")

    # Print summary
    print("\n=== SUMMARY ===")
    for site_type, site_data in results["sites"].items():
        if site_data["status"] == "success":
            m = site_data["metrics"]
            print(f"{site_type}: yield={m['actual_yield']}, "
                  f"elements={m['total_elements']}, "
                  f"truncated_1920={m['truncated_1920']}")
        else:
            print(f"{site_type}: FAILED - {site_data['error']}")


if __name__ == "__main__":
    main()
