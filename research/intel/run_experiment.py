#!/usr/bin/env python3
"""
EXP-INTEL-33925056324 Experiment Runner

Generates synthetic WebArena accessibility tree observations, runs the adapter,
and computes element_recall, attribute_preservation, hierarchy_preservation metrics.

Standard library only. No Docker, no browser, no LLM calls. Offline computation.
"""

from __future__ import annotations

import base64
import json
import os
import random
import statistics
import sys
from dataclasses import dataclass, field, asdict
from typing import Any

# Add parent to path for import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webarena_adapter import ExtractedElement, extract_fragments_from_observation, normalize_role


# ---------------------------------------------------------------------------
# Synthetic data generation
# ---------------------------------------------------------------------------

SEED = 42

# Element type templates for each site type
SITE_TEMPLATES = {
    "ecommerce": {
        "links": [
            ("link", "Product Title: {name}"),
            ("link", "Category: {name}"),
            ("link", "View Details"),
            ("link", "Add to Wishlist"),
            ("link", "Compare"),
        ],
        "buttons": [
            ("button", "Add to Cart"),
            ("button", "Buy Now"),
            ("button", "Wishlist"),
            ("button", "Compare Products"),
            ("button", "Filter"),
            ("button", "Sort by Price"),
            ("button", "Sort by Rating"),
            ("button", "Clear Filters"),
            ("button", "Apply"),
            ("button", "Next Page"),
        ],
        "textboxes": [
            ("textbox", "Search products"),
            ("textbox", "Quantity"),
            ("textbox", "Min Price"),
            ("textbox", "Max Price"),
            ("textbox", "Filter by brand"),
            ("textbox", "Enter coupon code"),
            ("textbox", "Shipping zip code"),
            ("textbox", "Product search"),
            ("textbox", "Review search"),
            ("textbox", "Sort keywords"),
        ],
    },
    "social_forum": {
        "links": [
            ("link", "User Profile: {name}"),
            ("link", "Reply to Post"),
            ("link", "Quote Post"),
            ("link", "View Thread"),
            ("link", "Member List"),
        ],
        "buttons": [
            ("button", "Like"),
            ("button", "Report"),
            ("button", "Follow"),
            ("button", "Subscribe"),
            ("button", "Bookmark"),
            ("button", "Share"),
            ("button", "Flag"),
            ("button", "Collapse"),
            ("button", "Expand"),
            ("button", "Reply"),
        ],
        "textboxes": [
            ("textbox", "Write a comment"),
            ("textbox", "Reply to thread"),
            ("textbox", "Search forum"),
            ("textbox", "New post title"),
            ("textbox", "Tag post"),
            ("textbox", "Filter by date"),
            ("textbox", "User search"),
            ("textbox", "Private message"),
            ("textbox", "Edit signature"),
            ("textbox", "Report reason"),
        ],
    },
    "coding": {
        "links": [
            ("link", "File: {name}"),
            ("link", "Directory: {name}"),
            ("link", "Commit: {name}"),
            ("link", "Branch: {name}"),
            ("link", "Pull Request"),
        ],
        "buttons": [
            ("button", "Expand"),
            ("button", "Collapse"),
            ("button", "Rename"),
            ("button", "Delete"),
            ("button", "New File"),
            ("button", "New Directory"),
            ("button", "Commit"),
            ("button", "Push"),
            ("button", "Pull"),
            ("button", "Merge"),
        ],
        "textboxes": [
            ("textbox", "File search"),
            ("textbox", "Commit message"),
            ("textbox", "Branch name"),
            ("textbox", "Search code"),
            ("textbox", "File path"),
            ("textbox", "Grep pattern"),
            ("textbox", "Replace text"),
            ("textbox", "Find in files"),
            ("textbox", "Terminal command"),
            ("textbox", "PR description"),
        ],
    },
}

# Hierarchy templates: each site type has a tree structure
# Format: (depth, role, name_template, prop_keys)
HIERARCHY_TEMPLATES = {
    "ecommerce": [
        (0, "RootWebArea", "Online Store", []),
        (1, "navigation", "Main Navigation", []),
        (2, "link", "Home", []),
        (2, "link", "Products", []),
        (2, "link", "Cart", []),
        (1, "group", "Product Listing", []),
        (2, "group", "Product Card 1", []),
        (3, "img", "Product Image", []),
        (3, "link", "Product Title", []),
        (3, "button", "Add to Cart", []),
        (3, "textbox", "Quantity", []),
        (2, "group", "Product Card 2", []),
        (3, "img", "Product Image", []),
        (3, "link", "Product Title", []),
        (3, "button", "Add to Cart", []),
        (3, "textbox", "Quantity", []),
        (1, "group", "Filters", []),
        (2, "textbox", "Search products", []),
        (2, "button", "Apply Filters", []),
        (2, "button", "Clear Filters", []),
        (1, "group", "Pagination", []),
        (2, "button", "Previous Page", []),
        (2, "button", "Next Page", []),
        (2, "textbox", "Page Number", []),
    ],
    "social_forum": [
        (0, "RootWebArea", "Community Forum", []),
        (1, "navigation", "Forum Navigation", []),
        (2, "link", "Home", []),
        (2, "link", "Categories", []),
        (2, "link", "Members", []),
        (1, "group", "Thread View", []),
        (2, "group", "Post 1", []),
        (3, "link", "User Profile", []),
        (3, "text", "Post content text", []),
        (3, "button", "Like", []),
        (3, "button", "Reply", []),
        (2, "group", "Post 2", []),
        (3, "link", "User Profile", []),
        (3, "text", "Post content text", []),
        (3, "button", "Like", []),
        (3, "button", "Reply", []),
        (1, "group", "Reply Box", []),
        (2, "textbox", "Write a reply", []),
        (2, "button", "Submit Reply", []),
        (1, "group", "Sidebar", []),
        (2, "link", "Forum Rules", []),
        (2, "link", "Online Users", []),
    ],
    "coding": [
        (0, "RootWebArea", "Code Repository", []),
        (1, "navigation", "File Tree", []),
        (2, "tree", "Root Directory", []),
        (3, "treeitem", "src", []),
        (4, "treeitem", "main.py", []),
        (4, "treeitem", "utils.py", []),
        (3, "treeitem", "tests", []),
        (4, "treeitem", "test_main.py", []),
        (3, "treeitem", "README.md", []),
        (1, "group", "File Content", []),
        (2, "text", "Source code content", []),
        (1, "group", "Actions", []),
        (2, "button", "Commit", []),
        (2, "button", "Push", []),
        (2, "button", "New File", []),
        (2, "textbox", "Commit message", []),
        (2, "textbox", "Branch name", []),
        (1, "group", "Search", []),
        (2, "textbox", "Search code", []),
        (2, "button", "Search", []),
    ],
}


@dataclass
class SyntheticElement:
    """Ground truth element for synthetic observation."""
    element_id: int
    role: str
    name: str
    properties: dict[str, str]
    parent_id: int | None
    children_ids: list[int] = field(default_factory=list)
    backend_id: int = 0
    union_bound: list[float] = field(default_factory=list)
    text: str = ""
    depth: int = 0


def generate_synthetic_observation(
    site_type: str,
    rng: random.Random,
    num_elements: int = 100,
) -> tuple[str, dict[int, dict[str, Any]], list[SyntheticElement]]:
    """
    Generate a synthetic WebArena accessibility tree observation.

    Returns:
        (formatted_text, obs_nodes_info, ground_truth_elements)
    """
    templates = SITE_TEMPLATES[site_type]
    hierarchy = HIERARCHY_TEMPLATES[site_type]

    elements: list[SyntheticElement] = []
    current_id = 0

    # Build elements from hierarchy template, filling remaining from type templates
    prop_choices = ["focused", "expanded", "required", "hasPopup", "selected", "checked"]

    for depth, role, name, prop_keys in hierarchy:
        if current_id >= num_elements:
            break

        # Assign properties probabilistically
        properties = {}
        if rng.random() < 0.3:
            prop = rng.choice(prop_choices)
            properties[prop] = str(rng.choice([True, False]))

        elem = SyntheticElement(
            element_id=current_id,
            role=role,
            name=name,
            properties=properties,
            parent_id=None,  # Will be set below
            backend_id=rng.randint(1000, 9999),
            union_bound=[round(rng.uniform(0, 800), 1) for _ in range(4)],
            text=name,
            depth=depth,
        )
        elements.append(elem)
        current_id += 1

    # Fill remaining elements from type-specific templates
    link_templates = templates["links"]
    button_templates = templates["buttons"]
    textbox_templates = templates["textboxes"]
    all_templates = (
        [(t[0], t[1]) for t in link_templates] +
        [(t[0], t[1]) for t in button_templates] +
        [(t[0], t[1]) for t in textbox_templates]
    )

    names_pool = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"]
    idx = 0
    while current_id < num_elements:
        role, name_tmpl = all_templates[idx % len(all_templates)]
        name = name_tmpl.replace("{name}", rng.choice(names_pool))
        idx += 1

        properties = {}
        if rng.random() < 0.25:
            prop = rng.choice(prop_choices)
            properties[prop] = str(rng.choice([True, False]))

        # Remaining elements get depth 2 (inside groups)
        elem = SyntheticElement(
            element_id=current_id,
            role=role,
            name=name,
            properties=properties,
            parent_id=None,
            backend_id=rng.randint(1000, 9999),
            union_bound=[round(rng.uniform(0, 800), 1) for _ in range(4)],
            text=name,
            depth=2,
        )
        elements.append(elem)
        current_id += 1

    # Assign parent-child relationships based on hierarchy template
    # Use depth to determine parent
    depth_stack: list[tuple[int, int]] = []  # (depth, element_id)
    for elem in elements:
        # Find parent based on depth
        while depth_stack and depth_stack[-1][0] >= elem.depth:
            depth_stack.pop()
        if depth_stack:
            parent_id = depth_stack[-1][1]
            elem.parent_id = parent_id
        depth_stack.append((elem.depth, elem.element_id))

    # Populate children_ids
    parent_to_children: dict[int | None, list[int]] = {}
    for elem in elements:
        parent_to_children.setdefault(elem.parent_id, []).append(elem.element_id)
    for elem in elements:
        elem.children_ids = parent_to_children.get(elem.element_id, [])

    # Generate formatted text string (WebArena format)
    lines = []
    for elem in elements:
        indent = "  " * elem.depth
        props_str = ""
        if elem.properties:
            props_str = " " + " ".join(f"{k}: {v}" for k, v in elem.properties.items())
        # Escape quotes in name
        safe_name = elem.name.replace('"', '\\"')
        lines.append(f'{indent}[{elem.element_id}] {elem.role} "{safe_name}"{props_str}')
    formatted_text = "\n".join(lines)

    # Generate obs_nodes_info
    obs_nodes_info = {}
    for elem in elements:
        obs_nodes_info[elem.element_id] = {
            "backend_id": elem.backend_id,
            "union_bound": elem.union_bound,
            "text": elem.text,
        }

    return formatted_text, obs_nodes_info, elements


def generate_null_control() -> tuple[str, dict[int, dict[str, Any]]]:
    """Null control: observation with only screenshot, no DOM elements."""
    # Simulate obs with empty text and no obs_nodes_info
    return "", {}


def generate_positive_control() -> tuple[str, dict[int, dict[str, Any]], list[SyntheticElement]]:
    """Positive control: exactly 100 elements with known structure."""
    rng = random.Random(SEED + 999)  # Deterministic but distinct from main runs
    return generate_synthetic_observation("ecommerce", rng, num_elements=100)


# ---------------------------------------------------------------------------
# Metrics computation
# ---------------------------------------------------------------------------

@dataclass
class MetricResult:
    value: float
    num_expected: int
    num_extracted: int
    num_correct: int
    details: list[dict[str, Any]] = field(default_factory=list)


def compute_element_recall(
    ground_truth: list[SyntheticElement],
    extracted: list[ExtractedElement],
) -> MetricResult:
    """Fraction of ground truth elements successfully extracted (by ID + role + name)."""
    gt_map = {e.element_id: e for e in ground_truth}
    ext_map = {e.element_id: e for e in extracted}

    correct = 0
    details = []
    for eid, gt_elem in gt_map.items():
        ext_elem = ext_map.get(eid)
        # Normalize ground truth role to match adapter's normalization
        gt_role_normalized = normalize_role(gt_elem.role)
        match = (
            ext_elem is not None
            and ext_elem.role == gt_role_normalized
            and ext_elem.name == gt_elem.name
        )
        if match:
            correct += 1
        details.append({
            "element_id": eid,
            "expected_role": gt_elem.role,
            "expected_name": gt_elem.name,
            "extracted_role": ext_elem.role if ext_elem else None,
            "extracted_name": ext_elem.name if ext_elem else None,
            "match": match,
        })

    recall = correct / len(ground_truth) if ground_truth else 0.0
    return MetricResult(
        value=recall,
        num_expected=len(ground_truth),
        num_extracted=len(extracted),
        num_correct=correct,
        details=details,
    )


def compute_attribute_preservation(
    ground_truth: list[SyntheticElement],
    extracted: list[ExtractedElement],
) -> MetricResult:
    """Fraction of ground truth elements with properties that are correctly preserved in extraction."""
    gt_map = {e.element_id: e for e in ground_truth}
    ext_map = {e.element_id: e for e in extracted}

    # Count ground truth elements that have properties
    gt_with_props = [eid for eid, e in gt_map.items() if e.properties]
    correct = 0
    details = []

    for eid in gt_with_props:
        gt_elem = gt_map[eid]
        ext_elem = ext_map.get(eid)
        gt_props = gt_elem.properties

        if ext_elem is None:
            # Element not extracted at all
            details.append({
                "element_id": eid,
                "expected_props": gt_props,
                "extracted_props": None,
                "match": False,
            })
            continue

        ext_props = ext_elem.properties
        # Check all expected properties are present and correct
        props_match = all(
            ext_props.get(k) == v for k, v in gt_props.items()
        )
        if props_match:
            correct += 1
        details.append({
            "element_id": eid,
            "expected_props": gt_props,
            "extracted_props": ext_props,
            "match": props_match,
        })

    # Preserve rate: correct / total ground truth elements that have properties
    total_with_props = len(gt_with_props)
    preservation = correct / total_with_props if total_with_props > 0 else 1.0

    return MetricResult(
        value=preservation,
        num_expected=total_with_props,
        num_extracted=len([eid for eid in ext_map if eid in gt_map]),
        num_correct=correct,
        details=details,
    )


def compute_hierarchy_preservation(
    ground_truth: list[SyntheticElement],
    extracted: list[ExtractedElement],
) -> MetricResult:
    """Fraction of extracted elements with correct parent-child relationships."""
    gt_map = {e.element_id: e for e in ground_truth}
    ext_map = {e.element_id: e for e in extracted}

    candidates = [eid for eid in ext_map if eid in gt_map]
    correct = 0
    details = []

    for eid in candidates:
        gt_elem = gt_map[eid]
        ext_elem = ext_map[eid]
        parent_match = ext_elem.parent_id == gt_elem.parent_id
        children_match = set(ext_elem.children_ids) == set(gt_elem.children_ids)
        match = parent_match and children_match
        if match:
            correct += 1
        details.append({
            "element_id": eid,
            "expected_parent": gt_elem.parent_id,
            "extracted_parent": ext_elem.parent_id,
            "expected_children": gt_elem.children_ids,
            "extracted_children": ext_elem.children_ids,
            "match": match,
        })

    preservation = correct / len(candidates) if candidates else 0.0
    return MetricResult(
        value=preservation,
        num_expected=len(ground_truth),
        num_extracted=len(candidates),
        num_correct=correct,
        details=details,
    )


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment() -> dict[str, Any]:
    """Run the full experiment and return raw results."""
    results = {
        "site_types": {},
        "positive_control": {},
        "null_control": {},
        "aggregate": {},
    }

    # --- Site type runs ---
    for site_type in ["ecommerce", "social_forum", "coding"]:
        rng = random.Random(SEED)
        formatted_text, obs_nodes_info, ground_truth = generate_synthetic_observation(
            site_type, rng, num_elements=100
        )

        # Extract using adapter
        extracted = extract_fragments_from_observation(formatted_text, obs_nodes_info)

        # Compute metrics
        recall = compute_element_recall(ground_truth, extracted)
        attr_pres = compute_attribute_preservation(ground_truth, extracted)
        hier_pres = compute_hierarchy_preservation(ground_truth, extracted)

        # Store raw results (without full details to keep manageable)
        results["site_types"][site_type] = {
            "num_ground_truth": len(ground_truth),
            "num_extracted": len(extracted),
            "element_recall": recall.value,
            "element_recall_correct": recall.num_correct,
            "attribute_preservation": attr_pres.value,
            "attribute_preservation_correct": attr_pres.num_correct,
            "hierarchy_preservation": hier_pres.value,
            "hierarchy_preservation_correct": hier_pres.num_correct,
            "formatted_text_preview": formatted_text[:500],
            "sample_ground_truth": [
                {"id": e.element_id, "role": e.role, "name": e.name, "props": e.properties, "parent": e.parent_id}
                for e in ground_truth[:5]
            ],
            "sample_extracted": [
                {"id": e.element_id, "role": e.role, "name": e.name, "props": e.properties, "parent": e.parent_id}
                for e in extracted[:5]
            ],
        }

    # --- Positive control ---
    pos_text, pos_info, pos_gt = generate_positive_control()
    pos_extracted = extract_fragments_from_observation(pos_text, pos_info)
    pos_recall = compute_element_recall(pos_gt, pos_extracted)
    pos_attr = compute_attribute_preservation(pos_gt, pos_extracted)
    pos_hier = compute_hierarchy_preservation(pos_gt, pos_extracted)

    results["positive_control"] = {
        "num_ground_truth": len(pos_gt),
        "num_extracted": len(pos_extracted),
        "element_recall": pos_recall.value,
        "attribute_preservation": pos_attr.value,
        "hierarchy_preservation": pos_hier.value,
        "pass": pos_recall.value >= 0.9,
    }

    # --- Null control ---
    null_text, null_info = generate_null_control()
    null_extracted = extract_fragments_from_observation(null_text, null_info)

    results["null_control"] = {
        "num_extracted": len(null_extracted),
        "element_recall": 0.0 if len(null_extracted) == 0 else -1.0,  # -1.0 signals failure
        "pass": len(null_extracted) == 0,
    }

    # --- Aggregate metrics ---
    all_recalls = [results["site_types"][st]["element_recall"] for st in ["ecommerce", "social_forum", "coding"]]
    all_attrs = [results["site_types"][st]["attribute_preservation"] for st in ["ecommerce", "social_forum", "coding"]]
    all_hiers = [results["site_types"][st]["hierarchy_preservation"] for st in ["ecommerce", "social_forum", "coding"]]

    results["aggregate"] = {
        "mean_element_recall": statistics.mean(all_recalls),
        "stdev_element_recall": statistics.stdev(all_recalls) if len(all_recalls) > 1 else 0.0,
        "min_element_recall": min(all_recalls),
        "max_element_recall": max(all_recalls),
        "mean_attribute_preservation": statistics.mean(all_attrs),
        "stdev_attribute_preservation": statistics.stdev(all_attrs) if len(all_attrs) > 1 else 0.0,
        "min_attribute_preservation": min(all_attrs),
        "mean_hierarchy_preservation": statistics.mean(all_hiers),
        "stdev_hierarchy_preservation": statistics.stdev(all_hiers) if len(all_hiers) > 1 else 0.0,
        "min_hierarchy_preservation": min(all_hiers),
        "all_thresholds_met": (
            min(all_recalls) >= 0.90
            and min(all_attrs) >= 0.80
            and min(all_hiers) >= 0.80
        ),
        "any_falsifier_triggered": (
            min(all_recalls) < 0.50 or min(all_attrs) < 0.50
        ),
    }

    # --- Adapter cost ---
    adapter_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webarena_adapter.py")
    adapter_lines = 0
    if os.path.exists(adapter_path):
        with open(adapter_path, "r") as f:
            adapter_lines = len(f.readlines())

    results["transformation_cost"] = {
        "adapter_lines_of_code": adapter_lines,
        "dependencies_added": 0,  # standard library only
        "external_api_calls": 0,
    }

    return results


if __name__ == "__main__":
    results = run_experiment()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Raw results written to {output_path}")
    print(json.dumps(results["aggregate"], indent=2))
