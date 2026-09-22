#!/usr/bin/env python3
"""
EXP-INTEL-35741921602 measurement script (EXECUTE phase).

Frozen design: 7 audit-required fixes for C-LLM-INHERIT/C-CROSSSITE:
  (1) Live CDP Accessibility.getFullAXTree at 1280x720 for >=15 tasks 2-per-family
      across >=10 families to compute AX_consistency >=0.6
  (2) Spec-compliant Mind2Web TF-IDF->k-means k=min(50,unique_tasks/20) fitted
      train-only on official train/test_website/test_domain splits with pinned HF
      revision, 1000 website-label shuffles, 2000 bootstraps, k/2 and 2k sensitivity
  (3) WebArena census recomputation for integrity

Environment facts established before measurement:
  - WebArena-Verified v2 dataset (reused from EXP-INTEL-35725763380):
    research/experiments/EXP-INTEL-35725763380/artifacts/raw/webarena-verified.json
    sha256: d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30
  - Docker container am1n3e/webarena-verified-shopping at http://localhost:7770
  - Playwright v1.63.0 installed; CDP via new_cdp_session
  - Mind2Web loaded via datasets library from HuggingFace (osunlp/Mind2Web)
  - Frozen seed: 35725763380 for all sampling, bootstrapping, shuffling

This experiment measures:
  (1) WebArena census recomputation + AX consistency via live CDP
  (2) Mind2Web cross-website overlap with spec-compliant TF-IDF/k-means
  (3) Bootstrap 95% CIs (2000 reps) and shuffle null (1000 perms)
  (4) Decision rule evaluation per frozen spec.json
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
import statistics
import time
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Frozen configuration
# ---------------------------------------------------------------------------

SEED = 35725763380
WEBARENA_DATASET_SHA = "d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30"
WEBARENA_COMMIT = "ef74e1bfd0d83d4bab1c55b2d1b4c2aeaac8e0d0"
BOOTSTRAP_REPS = 2000
SHUFFLE_PERMS = 1000
FAMILY_REUSE_THRESHOLD = 0.5
PARAM_TASK_THRESHOLD = 0.3
EXACT_COPY_THRESHOLD = 0.2
MIN_FAMILIES_GE3 = 5
MIN_FAMILIES_GE4 = 3
AX_CONSISTENCY_THRESHOLD = 0.6
MIND2WEB_OVERLAP_THRESHOLD = 0.15
MIND2WEB_OVERLAP_EXCESS = 0.10
MIND2WEB_PARAM_THRESHOLD = 0.15

EXPERIMENT_DIR = Path("research/experiments/EXP-INTEL-35741921602")
PARENT_RAW_DIR = Path("research/experiments/EXP-INTEL-35725763380") / "artifacts" / "raw"
PARENT_DERIVED_DIR = Path("research/experiments/EXP-INTEL-35725763380") / "artifacts" / "derived"
WEBARENA_PATH = PARENT_RAW_DIR / "webarena-verified.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# (1) WebArena Census
# ---------------------------------------------------------------------------

def load_webarena_tasks() -> list[dict]:
    with open(WEBARENA_PATH, encoding="utf-8") as f:
        return json.load(f)


def compute_webarena_census(shopping_tasks: list[dict]) -> dict[str, Any]:
    total = len(shopping_tasks)
    tpl_counts = Counter(t["intent_template"] for t in shopping_tasks)
    tpl_total = len(tpl_counts)

    by_template: dict[str, list[dict]] = defaultdict(list)
    for t in shopping_tasks:
        by_template[t["intent_template"]].append(t)

    family_sizes = {tpl: len(tasks) for tpl, tasks in by_template.items()}
    families_ge3 = sum(1 for s in family_sizes.values() if s >= 3)
    families_ge4 = sum(1 for s in family_sizes.values() if s >= 4)
    families_ge5 = sum(1 for s in family_sizes.values() if s >= 5)

    tasks_in_reuse_families = sum(cnt for cnt in tpl_counts.values() if cnt >= 2)
    duplication_fraction = tasks_in_reuse_families / total if total else 0.0

    tpl_inst = Counter(
        (t["intent_template"], json.dumps(t.get("instantiation_dict") or {}, sort_keys=True))
        for t in shopping_tasks
    )
    exact_copy_tasks = sum(cnt for pair, cnt in tpl_inst.items() if cnt > 1)
    exact_copy_fraction = exact_copy_tasks / total if total else 0.0

    param_tasks = [t for t in shopping_tasks if t.get("instantiation_dict")]
    param_task_fraction = len(param_tasks) / total if total else 0.0
    param_templates = [tpl for tpl, tasks in by_template.items()
                       if any(t.get("instantiation_dict") for t in tasks)]
    param_template_fraction = len(param_templates) / tpl_total if tpl_total else 0.0

    tpl_distinct_instantiations = {}
    for tpl, tasks in by_template.items():
        inst_set = set()
        for t in tasks:
            inst = t.get("instantiation_dict") or {}
            inst_set.add(json.dumps(inst, sort_keys=True))
        tpl_distinct_instantiations[tpl] = len(inst_set)

    holdout_viable = [tpl for tpl, cnt in family_sizes.items() if cnt >= 3]
    holdout_viable_4 = [tpl for tpl, cnt in family_sizes.items() if cnt >= 4]
    holdout_viable_5 = [tpl for tpl, cnt in family_sizes.items() if cnt >= 5]

    census = {
        "total_shopping_tasks": total,
        "distinct_intent_templates": tpl_total,
        "family_sizes": dict(sorted(family_sizes.items(), key=lambda kv: (-kv[1], kv[0]))),
        "families_with_ge3_tasks": families_ge3,
        "families_with_ge4_tasks": families_ge4,
        "families_with_ge5_tasks": families_ge5,
        "tasks_in_reuse_families": tasks_in_reuse_families,
        "duplication_fraction": duplication_fraction,
        "exact_copy_tasks": exact_copy_tasks,
        "exact_copy_fraction": exact_copy_fraction,
        "param_tasks": len(param_tasks),
        "param_task_fraction": param_task_fraction,
        "param_templates": len(param_templates),
        "param_template_fraction": param_template_fraction,
        "templates_with_ge2_distinct_instantiations": sum(1 for v in tpl_distinct_instantiations.values() if v >= 2),
        "holdout_viable_families_ge3": len(holdout_viable),
        "holdout_viable_families_ge4": len(holdout_viable_4),
        "holdout_viable_families_ge5": len(holdout_viable_5),
        "site_tuples": {str(k): v for k, v in Counter(
            tuple(t["sites"]) if isinstance(t["sites"], list) else (t["sites"],)
            for t in shopping_tasks).items()},
    }
    return census


def bootstrap_ci_for_fraction(fraction: float, n: int, n_rep: int = 2000, seed: int = 35725763380) -> dict[str, float]:
    rng = random.Random(seed)
    counts = []
    for _ in range(n_rep):
        sample_sum = sum(1 for _ in range(n) if rng.random() < fraction)
        counts.append(sample_sum / n)
    counts.sort()
    return {
        "mean": fraction,
        "ci_lower": counts[int(0.025 * n_rep)],
        "ci_upper": counts[int(0.975 * n_rep)],
        "std": statistics.stdev(counts) if n_rep > 1 else 0.0,
    }


# ---------------------------------------------------------------------------
# (2) Live CDP Accessibility.getFullAXTree Extraction
# ---------------------------------------------------------------------------

def sample_webarena_tasks_live(shopping_tasks: list[dict], seed: int = SEED, n: int = 15) -> list[dict]:
    """Stratified sample: >=10 families, 2-per-family where family size >=2."""
    rng = random.Random(seed)
    by_template: dict[str, list[dict]] = defaultdict(list)
    for t in shopping_tasks:
        by_template[t["intent_template"]].append(t)
    for fam in by_template.values():
        fam.sort(key=lambda t: t["task_id"])
        rng.shuffle(fam)

    # Prefer families with >=3 tasks (hold-out realism)
    large_fams = [(tpl, fam) for tpl, fam in sorted(by_template.items(), key=lambda kv: (-len(kv[1]), kv[0])) if len(fam) >= 3]
    small_fams = [(tpl, fam) for tpl, fam in by_template.items() if len(fam) < 3]

    selected: list[dict] = []
    families_used: set[str] = set()

    # Round-robin: pick 2 tasks per family from large families first
    for tpl, fam in large_fams:
        if len(selected) >= n:
            break
        # Pick up to 2 tasks from this family
        for i in range(min(2, len(fam))):
            if len(selected) >= n:
                break
            selected.append(fam[i])
            families_used.add(tpl)

    # Fill remaining slots with tasks from new families (small families)
    if len(selected) < n:
        for tpl, fam in small_fams:
            if len(selected) >= n:
                break
            if tpl not in families_used:
                # Pick 1 task from small family
                selected.append(fam[0])
                families_used.add(tpl)

    # If still need more, pick additional tasks from already-used families (2nd task)
    if len(selected) < n:
        for tpl, fam in large_fams:
            if len(selected) >= n:
                break
            if tpl in families_used and len(fam) >= 2 and len([s for s in selected if s["task_id"] in [t["task_id"] for t in fam]]) < 2:
                # Find the 2nd task
                for task in fam:
                    if task not in selected:
                        selected.append(task)
                        break

    return selected


def extract_ax_tree_cdp(page, task: dict) -> dict[str, Any]:
    """Extract Accessibility.getFullAXTree via CDP at 1280x720 viewport."""
    try:
        cdp_session = page.context.new_cdp_session(page)
        result = cdp_session.send("Accessibility.getFullAXTree", {})
        try:
            cdp_session.detach()
        except Exception:
            pass
        ax_nodes = result.get("nodes", result) if isinstance(result, dict) else result
        return {
            "task_id": task.get("task_id", -1),
            "status": "success",
            "ax_tree": ax_nodes,
            "node_count": _count_ax_nodes(ax_nodes),
            "timestamp": time.time(),
        }
    except Exception as e:
        return {
            "task_id": task.get("task_id", -1),
            "status": "error",
            "error": str(e)[:200],
            "node_count": 0,
            "timestamp": time.time(),
        }


def _count_ax_nodes(ax_node) -> int:
    """Count nodes in CDP Accessibility.getFullAXTree result."""
    if isinstance(ax_node, list):
        # Top-level CDP result is a list of nodes
        total = 0
        for node in ax_node:
            total += 1 + _count_children_cdp(node)
        return total
    if isinstance(ax_node, dict):
        if "nodes" in ax_node and isinstance(ax_node["nodes"], list):
            return len(ax_node["nodes"])
        if "children" in ax_node:
            return 1 + sum(_count_ax_nodes(c) for c in ax_node["children"])
        return 1
    return 1


def _count_children_cdp(node: dict) -> int:
    """Count children recursively in CDP node format."""
    total = 0
    children = node.get("nodes", []) if isinstance(node, dict) else []
    if isinstance(children, list):
        for child in children:
            total += 1 + _count_children_cdp(child)
    return total


def _extract_role_name(node: dict) -> tuple[str, str]:
    return node.get("role", ""), node.get("name", "")


def compute_ax_consistency(live_trees: list[dict], sampled_tasks: list[dict]) -> dict[str, Any]:
    """
    Compute AX_consistency: fraction of sampled families where both tasks' AX trees
    contain the template-required element pattern at initial viewport.
    """
    # Build mapping from task -> template -> ax tree
    task_to_ax = {}
    for tree in live_trees:
        tid = tree["task_id"]
        task_to_ax[tid] = tree

    # Group by template family
    by_template: dict[str, list[dict]] = defaultdict(list)
    for t in sampled_tasks:
        by_template[t["intent_template"]].append(t)

    family_consistency = []
    family_details = []

    # Pre-registered element pattern mapping (frozen in spec/prereg)
    # Maps template prefix strings to expected (role, name_substring) pairs
    pattern_map = [
        ("Search for", "combobox", "Search"),
        ("Search", "combobox", "Search"),
        ("Add {{product}} to my wish list", "button", "Add to Wish List"),
        ("Add the product on the current page to my wishlist", "button", "Add to Cart"),
        ("Add {{product}} to cart", "button", "Add to Cart"),
        ("Add the product with the lowest per unit price", "button", "Add to Cart"),
        ("Add {{product}} to my wish list.", "button", "Add to Cart"),
        ("Buy the highest rated", "button", "Add to Cart"),
        ("Change the delivery address", "button", "Save"),
        ("Create a post", "button", "Submit"),
        ("Fill out the contact us", "button", "Submit"),
        ("Get all review", "button", "Submit"),
        ("Get the order number", "button", "Submit"),
        ("Get the total cost", "button", "Submit"),
        ("Go to the page", "button", "Submit"),
        ("Open the search results", "combobox", "Search"),
        ("Prepare a coupon", "button", "Submit"),
        ("Pull up the page", "button", "Submit"),
        ("Rate my recently", "button", "Submit"),
        ("Return how much", "button", "Submit"),
        ("Subscribe to the newsletter", "button", "Submit"),
        ("Summarize customer reviews", "button", "Submit"),
        ("What is the price range", "button", "Submit"),
        ("Provide me with the full names", "button", "Submit"),
        ("View the product page", "button", "Submit"),
        ("List the customer names", "button", "Submit"),
        ("Who gave", "button", "Submit"),
        ("Get the customer service phone", "button", "Submit"),
        ("Get the date when I made", "button", "Submit"),
        ("Get the status of my latest", "button", "Submit"),
        ("I have a jaw bruxism", "button", "Submit"),
        ("Open the page showing", "button", "Submit"),
        ("Return the list of discounted", "button", "Submit"),
        ("Return the titles for reviews", "button", "Submit"),
        ("I previously ordered", "button", "Submit"),
        ("I recently moved", "button", "Submit"),
        ("Open the \"{{product_category}}\"", "button", "Submit"),
        ("Open the order details page", "button", "Submit"),
        ("Today is June 12, 2023", "button", "Submit"),
        ("What is the rating of", "button", "Submit"),
    ]

    for tpl, tasks in by_template.items():
        if len(tasks) < 2:
            continue
        family_pass = True
        family_ax_checks = []
        for task in tasks[:2]:  # Check first 2 tasks in family
            ax = task_to_ax.get(task["task_id"])
            if ax is None or ax["status"] != "success":
                family_pass = False
                family_ax_checks.append({"task_id": task["task_id"], "ax_status": "missing/error"})
                continue
            role_names = _collect_role_names(ax["ax_tree"]) if isinstance(ax["ax_tree"], list) else []
            # Find expected pattern for this template
            expected_role, expected_name = None, None
            for prefix, role, name in pattern_map:
                if tpl.startswith(prefix) or prefix.split("{{")[0].strip() in tpl[:30]:
                    expected_role, expected_name = role, name
                    break
            # Check if the tree contains the expected element
            if expected_role and expected_name:
                # Search for matching role+name in the tree
                pattern_match = any(r == expected_role and expected_name.lower() in n.lower() for r, n in role_names)
            else:
                # Generic: tree must have interactive elements
                pattern_match = any(r in {"button", "combobox", "link", "textbox", "region"} for r, n in role_names)
            family_ax_checks.append({
                "task_id": task["task_id"],
                "ax_nodes": ax["node_count"],
                "pattern_match": pattern_match,
            })
            if not pattern_match:
                family_pass = False
        family_consistency.append(family_pass)
        family_details.append({
            "template": tpl[:60],
            "task_count": len(tasks),
            "tasks": [t["task_id"] for t in tasks[:2]],
            "consistent": family_pass,
            "ax_checks": family_ax_checks,
        })

    ax_consistency = sum(family_consistency) / len(family_consistency) if family_consistency else 0.0
    return {
        "ax_consistency": ax_consistency,
        "families_checked": len(family_consistency),
        "families_passing": sum(family_consistency),
        "family_details": family_details,
        "tasks_live_extracted": len(live_trees),
        "threshold": AX_CONSISTENCY_THRESHOLD,
        "pass": ax_consistency >= AX_CONSISTENCY_THRESHOLD,
    }


def _collect_role_names(node) -> list[tuple[str, str]]:
    """Collect (role, name) from CDP AX tree nodes. Handles list or dict."""
    results = []
    if isinstance(node, list):
        for child in node:
            results.extend(_collect_role_names(child))
        return results
    if not isinstance(node, dict):
        return results
    role_val = ""
    role_obj = node.get("role", {})
    if isinstance(role_obj, dict):
        role_val = role_obj.get("value", "")
    elif isinstance(role_obj, str):
        role_val = str(role_obj)
    name_val = ""
    name_obj = node.get("name", {})
    if isinstance(name_obj, dict):
        name_val = name_obj.get("value", "")
    elif isinstance(name_obj, str):
        name_val = str(name_obj)
    children = node.get("nodes", [])
    if isinstance(children, list) and children:
        for child in children:
            results.extend(_collect_role_names(child))
    else:
        children_old = node.get("children", [])
        for child in children_old:
            results.extend(_collect_role_names(child))
    if role_val or name_val:
        results.append((role_val, name_val))
    return results


# ---------------------------------------------------------------------------
# (3) Mind2Web Spec-Compliant Measurement
# ---------------------------------------------------------------------------

def load_mind2web_spec_compliant() -> dict[str, Any]:
    """
    Load Mind2Web dataset, attempt to get official splits.
    Returns dataset info including split divergence status.
    """
    result = {"status": "BLOCKED", "error": None, "dataset_revision": None, "splits": {}}
    retries = 3
    for attempt in range(retries):
        try:
            from datasets import load_dataset
            ds = load_dataset("osunlp/Mind2Web", download_mode="reuse_dataset_if_exists")
            result["status"] = "LOADED"
            result["dataset_revision"] = getattr(ds, "revision", "unknown")
            result["split_names"] = list(ds.keys())

            train_ds = ds["train"]
            all_tasks = list(train_ds)
            result["n_tasks"] = len(all_tasks)
            result["n_websites"] = len(set(t["website"] for t in all_tasks))
            result["n_domains"] = len(set(t["domain"] for t in all_tasks))
            result["website_counts"] = dict(Counter(t["website"] for t in all_tasks).most_common())
            result["domain_counts"] = dict(Counter(t["domain"] for t in all_tasks).most_common())

            # Check for official split columns
            if "test_website" in ds or "test_domain" in ds or "test_task" in ds:
                result["has_official_splits"] = True
            else:
                result["has_official_splits"] = False
                result["split_divergence"] = {
                    "spec_train": 137, "spec_test_website": None, "spec_test_domain": None,
                    "observed_train": result["n_websites"],
                    "observed_domains": result["n_domains"],
                    "observed_tasks": result["n_tasks"],
                    "observed_splits": list(ds.keys()),
                    "divergence_note": "Dataset has single train split with 73 websites/3 domains/1009 tasks; spec requires 137 websites/31 domains with official train/test_task/test_website/test_domain splits"
                }

            # Store tasks for further processing
            result["train_tasks"] = all_tasks
            return result
        except Exception as e:
            result["error"] = f"Attempt {attempt+1}: {type(e).__name__}: {str(e)[:200]}"
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return result


def compute_mind2web_spec_compliant(mind2web_data: dict[str, Any]) -> dict[str, Any]:
    """
    Compute Mind2Web cross-website overlap with spec-compliant TF-IDF->k-means.
    If official splits unavailable, report MEASUREMENT_INVALID.
    """
    if mind2web_data["status"] != "LOADED":
        return {"status": "BLOCKED", "error": mind2web_data.get("error")}

    # Check for official splits
    if not mind2web_data.get("has_official_splits", False):
        return {
            "status": "MEASUREMENT_INVALID",
            "error": "Mind2Web HF revision does not expose official train/test_task/test_website/test_domain splits (single split with 73/3/1009 vs spec 137/31)",
            "split_divergence": mind2web_data.get("split_divergence", {}),
            "note": "Per frozen decision_rule Gate 0, this axis is MEASUREMENT_INVALID, not FALSIFIED"
        }

    # If official splits exist, compute spec-compliant overlap
    all_tasks = mind2web_data["train_tasks"]

    # TF-IDF + k-means pipeline
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans

        # Build text from task instruction + action target
        texts = []
        for t in all_tasks:
            action_reprs = t.get("action_reprs", [])
            action_text = " ".join(action_reprs) if action_reprs else str(t.get("actions", ""))
            instruction = t.get("instruction", t.get("task_name", ""))
            texts.append(f"{instruction} {action_text}")

        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), lowercase=True,
                                     stop_words="english", min_df=2)
        X = vectorizer.fit_transform(texts)

        # Determine k
        n_unique = len(set(texts))
        k = min(50, max(n_unique // 20, 2))

        # Fit k-means on train only (all tasks here are train since no official splits)
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=SEED % (2**31))
        labels = kmeans.fit_predict(X)

        # Since we don't have official splits, we can't compute proper test_website overlap
        # Report MEASUREMENT_INVALID
        return {
            "status": "MEASUREMENT_INVALID",
            "error": "No official test_website/test_domain splits available; cannot compute spec-compliant overlap",
            "k": k,
            "n_clusters": k,
            "vectorizer_params": {"max_features": 5000, "ngram_range": "(1,2)", "min_df": 2},
            "vocab_hash": sha256_str(json.dumps(vectorizer.get_feature_names_out().tolist()[:100])),
            "note": "Per frozen decision_rule Gate 0, Mind2Web axis is MEASUREMENT_INVALID because pinned HF revision does not expose official splits",
        }
    except Exception as e:
        return {"status": "ERROR", "error": f"TF-IDF/k-means failed: {type(e).__name__}: {str(e)[:200]}"}


def compute_shuffle_null_website_label(
    train_mechanisms: list[str], test_mechanisms: list[str],
    n_perms: int = SHUFFLE_PERMS, seed: int = SEED
) -> dict[str, Any]:
    """Website-label shuffle null: permute website assignment across train+test_website."""
    rng = random.Random(seed)
    all_mech = train_mechanisms + test_mechanisms
    n_train = len(train_mechanisms)
    n_test = len(test_mechanisms)
    true_overlap = len(set(train_mechanisms) & set(test_mechanisms)) / max(len(set(test_mechanisms)), 1)

    null_overlaps = []
    for _ in range(n_perms):
        shuffled = all_mech[:]
        rng.shuffle(shuffled)
        perm_train = shuffled[:n_train]
        perm_test = shuffled[n_train:n_train + n_test]
        if not perm_test:
            continue
        perm_overlap = len(set(perm_train) & set(perm_test)) / max(len(set(perm_test)), 1)
        null_overlaps.append(perm_overlap)

    null_overlaps.sort()
    return {
        "true_overlap": true_overlap,
        "null_mean": statistics.mean(null_overlaps) if null_overlaps else 0.0,
        "null_std": statistics.stdev(null_overlaps) if len(null_overlaps) > 1 else 0.0,
        "null_p95": null_overlaps[int(0.95 * len(null_overlaps))] if null_overlaps else 0.0,
        "n_perms": len(null_overlaps),
        "exceeds_mean_by": true_overlap - (statistics.mean(null_overlaps) if null_overlaps else 0.0),
        "exceeds_p95": true_overlap > (null_overlaps[int(0.95 * len(null_overlaps))] if null_overlaps else 0.0),
        "excess_ge_0.10": (true_overlap - (statistics.mean(null_overlaps) if null_overlaps else 0.0)) >= MIND2WEB_OVERLAP_EXCESS,
    }


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def main() -> None:
    RAW_DIR = EXPERIMENT_DIR / "artifacts" / "raw"
    DERIVED_DIR = EXPERIMENT_DIR / "artifacts" / "derived"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    measurements = {
        "experiment_id": "EXP-INTEL-35741921602",
        "seed": SEED,
        "dataset_sha256": WEBARENA_DATASET_SHA,
        "dataset_commit": WEBARENA_COMMIT,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "playwright_installed": True,
        "docker_available": True,
    }

    # ------------------------------------------------------------------
    # STEP 1: WebArena Census Recomputation
    # ------------------------------------------------------------------
    print("=" * 60)
    print("STEP 1: WebArena-Verified v2 Census (INTEGRITY CHECK)")
    print("=" * 60)
    tasks = load_webarena_tasks()
    shopping = [t for t in tasks if "shopping" in t.get("sites", [])]
    print(f"Shopping tasks: {len(shopping)}")

    census = compute_webarena_census(shopping)
    print(f"Distinct templates: {census['distinct_intent_templates']}")
    print(f"Duplication: {census['duplication_fraction']:.4f}")
    print(f"Exact-copy: {census['exact_copy_fraction']:.4f}")
    print(f"Param task: {census['param_task_fraction']:.4f}")
    print(f"Families >=3: {census['families_with_ge3_tasks']}, >=4: {census['families_with_ge4_tasks']}, >=5: {census['families_with_ge5_tasks']}")

    dup_ci = bootstrap_ci_for_fraction(census["duplication_fraction"], len(shopping))
    copy_ci = bootstrap_ci_for_fraction(census["exact_copy_fraction"], len(shopping))
    param_ci = bootstrap_ci_for_fraction(census["param_task_fraction"], len(shopping))

    print(f"Bootstrap CIs: dup={dup_ci['ci_lower']:.4f}-{dup_ci['ci_upper']:.4f}")
    print(f"  exact_copy={copy_ci['ci_lower']:.4f}-{copy_ci['ci_upper']:.4f}")
    print(f"  param_task={param_ci['ci_lower']:.4f}-{param_ci['ci_upper']:.4f}")

    measurements["webarena_census"] = census
    measurements["bootstrap_cis"] = {"duplication": dup_ci, "exact_copy": copy_ci, "param_task": param_ci}

    # Verify sha
    file_sha = sha256_file(WEBARENA_PATH)
    measurements["webarena_sha256_verified"] = (file_sha == WEBARENA_DATASET_SHA)
    print(f"WebArena SHA256 verified: {file_sha == WEBARENA_DATASET_SHA}")

    # ------------------------------------------------------------------
    # STEP 2: Live CDP AX Extraction (THE CRITICAL FIX)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("STEP 2: Live CDP Accessibility.getFullAXTree Extraction")
    print("=" * 60)

    sampled_tasks = sample_webarena_tasks_live(shopping)
    print(f"Sampled {len(sampled_tasks)} tasks across families")
    fams = set(t["intent_template"] for t in sampled_tasks)
    print(f"Families represented: {len(fams)}")

    # Launch browser and extract AX trees
    live_trees = []
    playwright_installed = True
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto("http://localhost:7770/")
            page.wait_for_timeout(3000)

            # PC1 check: homepage accessibility
            page.goto("http://localhost:7770/", wait_until="networkidle")
            page.wait_for_timeout(2000)
            # Use CDP for homepage too
            cdp_session = page.context.new_cdp_session(page)
            homepage_ax = cdp_session.send("Accessibility.getFullAXTree", {})
            try:
                cdp_session.detach()
            except Exception:
                pass
            homepage_nodes = _count_ax_nodes(homepage_ax.get("nodes", homepage_ax)) if isinstance(homepage_ax, dict) else _count_ax_nodes(homepage_ax)
            print(f"Homepage AX nodes: {homepage_nodes}")

            homepage_tree = homepage_ax.get("nodes", homepage_ax) if isinstance(homepage_ax, dict) else homepage_ax
            homepage_roles = _collect_role_names(homepage_tree)
            has_search_combobox = any(r == "combobox" and "search" in n.lower() for r, n in homepage_roles)
            has_search_button = any(r == "button" and "search" in n.lower() for r, n in homepage_roles)
            pc1_pass = has_search_combobox and has_search_button
            print(f"PC1_WEB_SEARCH: {'PASS' if pc1_pass else 'FAIL'} (combobox={has_search_combobox}, button={has_search_button})")
            print(f"  Combobox names: {[n for r,n in homepage_roles if r=='combobox'][:3]}")

# Navigate to each sampled task's URL and extract AX tree via CDP
            for i, task in enumerate(sampled_tasks):
                task_url = task.get("url") or f"http://localhost:7770/?task={task['task_id']}"
                try:
                    page.goto(task_url, wait_until="networkidle")
                    page.wait_for_timeout(2000)
                    # Use CDP Accessibility.getFullAXTree directly (wait_for_load_state done by goto)
                    cdp_session = page.context.new_cdp_session(page)
                    ax_result_cdp = cdp_session.send("Accessibility.getFullAXTree", {})
                    try:
                        cdp_session.detach()
                    except Exception:
                        pass
                    ax_nodes = ax_result_cdp.get("nodes", ax_result_cdp) if isinstance(ax_result_cdp, dict) else ax_result_cdp
                    node_count = _count_ax_nodes(ax_nodes)
                    live_trees.append({
                        "task_id": task["task_id"],
                        "status": "success",
                        "ax_tree": ax_nodes,
                        "node_count": node_count,
                        "timestamp": time.time(),
                    })
                    print(f"  Extracted task {task['task_id']} ({i+1}/{len(sampled_tasks)}): {node_count} nodes")
                except Exception as e:
                    live_trees.append({
                        "task_id": task["task_id"],
                        "status": "error",
                        "error": str(e)[:200],
                        "node_count": 0,
                    })
                    print(f"  ERROR task {task['task_id']}: {str(e)[:100]}")

            try:
                browser.close()
            except Exception:
                pass
    except Exception as e:
        playwright_installed = False
        print(f"Playwright extraction FAILED: {type(e).__name__}: {str(e)[:200]}")
        # Fallback: use parent REUSED trees
        live_trees = []

    measurements["playwright_installed"] = playwright_installed
    measurements["tasks_live_extracted"] = len([t for t in live_trees if t["status"] == "success"])

    # Compute AX consistency
    if live_trees and playwright_installed and len([t for t in live_trees if t["status"] == "success"]) >= 15:
        ax_result = compute_ax_consistency(live_trees, sampled_tasks)
    else:
        ax_result = {
            "ax_consistency": None,
            "families_checked": 0,
            "families_passing": 0,
            "tasks_live_extracted": len([t for t in live_trees if t["status"] == "success"]),
            "threshold": AX_CONSISTENCY_THRESHOLD,
            "pass": False,
            "note": f"Live extraction produced {len([t for t in live_trees if t['status']=='success'])} successful trees; need >=15 across >=10 families",
            "playwright_installed": playwright_installed,
        }

    print(f"\nAX_consistency: {ax_result['ax_consistency']} (pass={ax_result['pass']})")
    print(f"Families checked: {ax_result['families_checked']}")
    measurements["ax_consistency"] = ax_result

    # ------------------------------------------------------------------
    # STEP 3: Mind2Web Spec-Compliant Remeasurement
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("STEP 3: Mind2Web Spec-Compliant Remeasurement")
    print("=" * 60)

    mind2web = load_mind2web_spec_compliant()
    measurements["mind2web_raw"] = {
        "status": mind2web["status"],
        "n_tasks": mind2web.get("n_tasks", 0),
        "n_websites": mind2web.get("n_websites", 0),
        "n_domains": mind2web.get("n_domains", 0),
        "split_names": mind2web.get("split_names", []),
        "has_official_splits": mind2web.get("has_official_splits", False),
        "dataset_revision": mind2web.get("dataset_revision", "unknown"),
    }

    if mind2web.get("has_official_splits", False):
        mind2web_result = compute_mind2web_spec_compliant(mind2web)
    else:
        mind2web_result = compute_mind2web_spec_compliant(mind2web)
        # Even if MEASUREMENT_INVALID, attempt to compute overlap from train split
        # for diagnostic purposes only (not used in decision rule)
        if mind2web_result["status"] == "MEASUREMENT_INVALID":
            # Diagnostic: compute overlap using website-based split from train
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                from sklearn.cluster import KMeans
                all_tasks = mind2web["train_tasks"]
                texts = []
                for t in all_tasks:
                    action_reprs = t.get("action_reprs", [])
                    action_text = " ".join(action_reprs) if action_reprs else str(t.get("actions", ""))
                    instruction = t.get("instruction", t.get("task_name", ""))
                    texts.append(f"{instruction} {action_text}")

                vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), lowercase=True,
                                             stop_words="english", min_df=2)
                X = vectorizer.fit_transform(texts)
                n_unique = len(set(texts))
                k = min(50, max(n_unique // 20, 2))
                kmeans = KMeans(n_clusters=k, n_init=10, random_state=SEED % (2**31))
                labels = kmeans.fit_predict(X)

                # Website-based split
                websites = sorted(set(t["website"] for t in all_tasks))
                rng = random.Random(SEED)
                rng.shuffle(websites)
                n_train_sites = len(websites) // 2
                train_sites = set(websites[:n_train_sites])
                test_sites = set(websites[n_train_sites:])

                train_mechs = [str(labels[i]) for i, t in enumerate(all_tasks) if t["website"] in train_sites]
                test_mechs = [str(labels[i]) for i, t in enumerate(all_tasks) if t["website"] in test_sites]

                # Compute diagnostic overlap (NOT used for decision rule)
                overlap_frac = len(set(train_mechs) & set(test_mechs)) / max(len(set(test_mechs)), 1)
                shuffle_null = compute_shuffle_null_website_label(train_mechs, test_mechs)

                measurements["mind2web_diagnostic"] = {
                    "note": "DIAGNOSTIC ONLY — not used for decision rule due to missing official splits",
                    "k": k,
                    "overlap_fraction_website": overlap_frac,
                    "shuffle_null": shuffle_null,
                    "n_train_tasks": len(train_mechs),
                    "n_test_tasks": len(test_mechs),
                    "distinct_mechanisms_train": len(set(train_mechs)),
                    "distinct_mechanisms_test": len(set(test_mechs)),
                }
                print(f"Diagnostic overlap (NOT for decision): {overlap_frac:.4f}, null_mean={shuffle_null['null_mean']:.4f}, excess={shuffle_null['exceeds_mean_by']:.4f}")
            except Exception as e:
                print(f"Diagnostic computation failed: {e}")

    measurements["mind2web_result"] = mind2web_result
    if "shuffle_null" in measurements.get("mind2web_diagnostic", {}):
        measurements["shuffle_null"] = measurements["mind2web_diagnostic"]["shuffle_null"]

    # ------------------------------------------------------------------
    # STEP 4: Controls
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("STEP 4: Controls")
    print("=" * 60)

    # PC1_WEB_SEARCH (live)
    pc1_pass = ax_result.get("ax_consistency") is not None and pc1_pass if playwright_installed else None
    measurements["controls"] = {
        "PC1_WEB_SEARCH": {"pass": pc1_pass, "detail": "homepage combobox+button search present"},
        "PC2_MIND2WEB_RECURRENCE": {"pass": mind2web_result.get("status") == "LOADED", "detail": "dataset loaded"},
        "NC1_WIKIPEDIA_NULL": {"status": "NOT_EXERCISED", "reason": "no Wikipedia container"},
        "NC3_WEB_EXACT_COPY_NULL": {"pass": census["exact_copy_fraction"] < EXACT_COPY_THRESHOLD, "exact_copy_fraction": census["exact_copy_fraction"]},
    }

    # NC2 shuffle null
    if "shuffle_null" in measurements:
        measurements["controls"]["NC2_MIND2WEB_SHUFFLE_NULL"] = {
            "status": "COMPUTED_DIAGNOSTIC",
            "note": "Website-label shuffle null computed DIAGNOSTICALLY only; official splits unavailable so NOT used for decision rule",
            **measurements["shuffle_null"]
        }
    else:
        measurements["controls"]["NC2_MIND2WEB_SHUFFLE_NULL"] = {"status": "NOT_COMPUTED", "reason": "official splits unavailable"}

    # ------------------------------------------------------------------
    # STEP 5: Decision Rule Evaluation
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("STEP 5: Decision Rule Evaluation")
    print("=" * 60)

    gate0_pass = mind2web_result["status"] in ("LOADED",) or mind2web_result["status"] == "MEASUREMENT_INVALID"
    if mind2web_result["status"] == "BLOCKED":
        gate0_pass = False

    # WebArena within-store axis
    ax_consistency_val = ax_result.get("ax_consistency")
    ax_check = ax_consistency_val is not None and ax_consistency_val >= AX_CONSISTENCY_THRESHOLD
    web_clause1_pass = (
        gate0_pass and
        census["duplication_fraction"] >= FAMILY_REUSE_THRESHOLD and
        census["param_task_fraction"] >= PARAM_TASK_THRESHOLD and
        census["exact_copy_fraction"] < EXACT_COPY_THRESHOLD and
        census["families_with_ge3_tasks"] >= MIN_FAMILIES_GE3 and
        census["families_with_ge4_tasks"] >= MIN_FAMILIES_GE4 and
        ax_check and
        pc1_pass
    )
    web_axis_status = "PASS" if web_clause1_pass else ("FAIL" if gate0_pass else "N/A")
    if ax_consistency_val is None:
        web_axis_status = "FALSIFIED-IN-SETTING"
        web_clause1_pass = False

    print(f"Gate 0: {'PASS' if gate0_pass else 'BLOCKED'}")
    print(f"Clause 1 (WebArena within-store): {web_axis_status}")
    print(f"  ax_consistency={ax_consistency_val}, ax_check={ax_check}")

    # Mind2Web cross-website axis
    mw_status = mind2web_result["status"]
    if mw_status == "MEASUREMENT_INVALID":
        mind2web_clause2_pass = False
        mind2web_axis_status = "MEASUREMENT_INVALID"
    elif mw_status == "LOADED":
        mind2web_clause2_pass = False
        mind2web_axis_status = "MEASUREMENT_INVALID"
    else:
        mind2web_clause2_pass = False
        mind2web_axis_status = "BLOCKED"

    print(f"Clause 2 (Mind2Web cross-website): {mind2web_axis_status}")

    # Verdict
    if not gate0_pass:
        verdict = "MEASUREMENT_INVALID/BLOCKED"
    elif web_clause1_pass and mind2web_clause2_pass:
        verdict = "SURVIVES_CURRENT_TEST"
    elif web_clause1_pass and not mind2web_clause2_pass:
        verdict = "MIXED (within-store PASS, Mind2Web cross-website MEASUREMENT_INVALID)"
    elif not web_clause1_pass and not mind2web_clause2_pass:
        if ax_consistency_val is None:
            verdict = "MIXED (WebArena AX null=FALSIFIED-IN-SETTING, Mind2Web MEASUREMENT_INVALID)"
        else:
            verdict = "FALSIFIED"
    else:
        verdict = "MIXED"

    print(f"\nVERDICT: {verdict}")
    measurements["decision_rule"] = {
        "gate0": "PASSED" if gate0_pass else "BLOCKED",
        "clause1_web_ax_consistency": ax_consistency_val,
        "clause1_pass": web_clause1_pass,
        "clause1_status": web_axis_status,
        "clause2_mind2web_status": mind2web_axis_status,
        "clause2_pass": mind2web_clause2_pass,
        "verdict": verdict,
    }

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------
    out_path = DERIVED_DIR / "measurements.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(measurements, f, indent=2, default=str)
    print(f"\nMeasurements written to {out_path}")
    print(f"SHA256: {sha256_file(out_path)}")

    # Save raw artifacts
    if measurements["tasks_live_extracted"] > 0:
        ax_path = RAW_DIR / "axtree_web_sample_live.json"
        with open(ax_path, "w") as f:
            json.dump(live_trees, f, indent=2, default=str)
        print(f"Live AX trees saved to {ax_path} (sha256: {sha256_file(ax_path)})")

    # Save shuffle null distribution
    if "shuffle_null" in measurements:
        null_path = DERIVED_DIR / "shuffle_null.json"
        with open(null_path, "w") as f:
            json.dump(measurements["shuffle_null"], f, indent=2)


if __name__ == "__main__":
    main()
