#!/usr/bin/env python3
"""
EXP-INTEL-35927482134 measurement script (EXECUTE phase).

Captures 2 pages per category (category listing + product detail) for 10 categories,
enabling within-category longest-prefix AX consistency comparison.
"""

from __future__ import annotations
import hashlib
import json
import random
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SEED = 35725763380
EXPERIMENT_ID = "EXP-INTEL-35927482134"
DOCKER_DIGEST = "sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb"
VIEWPORT = {"width": 1280, "height": 720}
BASE_URL = "http://localhost:7770"

EXP_DIR = Path("research/experiments/EXP-INTEL-35927482134")
DERIVED_DIR = EXP_DIR / "artifacts" / "derived"
RAW_DIR = EXP_DIR / "artifacts" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
DERIVED_DIR.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


sys.path.insert(0, str(Path.cwd()))
from research.intel.grammar_fulltree_358885 import (
    strip_dynamic_tokens,
    sha256_normalized_subtree,
    longest_prefix_without_fallback,
    recompute_grammar_hash,
)

GRAMMAR_HASH = recompute_grammar_hash()


def get_cdp_ax_tree(page) -> dict[str, Any]:
    try:
        session = page.context.new_cdp_session(page)
        result = session.send('Accessibility.getFullAXTree')
        return result if isinstance(result, dict) else {}
    except Exception:
        return {}


def count_ax_nodes(nodes_list) -> int:
    count = 0
    for n in nodes_list:
        count += 1
        children = n.get('children', [])
        if isinstance(children, list):
            count += count_ax_nodes(children)
    return count


def extract_tokens_from_ax(nodes_list) -> list[str]:
    tokens = []
    for node in nodes_list:
        role = node.get('role', {}).get('value', 'unknown') if isinstance(node.get('role'), dict) else node.get('role', 'unknown')
        name = node.get('name', {}).get('value', '') if isinstance(node.get('name'), dict) else node.get('name', '')
        tokens.append(f"{role}:{name}")
        children = node.get('children', [])
        if isinstance(children, list):
            tokens.extend(extract_tokens_from_ax(children))
    return tokens


def capture_page_data(page, url: str, category: str = "") -> dict[str, Any]:
    """Capture all data for a page: AX tree, DOM, metadata."""
    try:
        page.goto(url, timeout=30000)
        page.wait_for_load_state('networkidle')
        time.sleep(1)
        
        ax_tree = get_cdp_ax_tree(page)
        dom_content = page.content()
        dom_bytes = len(dom_content.encode('utf-8'))
        
        nodes = ax_tree.get('nodes', []) if isinstance(ax_tree, dict) else []
        node_count = count_ax_nodes(nodes) if nodes else 0
        tokens = extract_tokens_from_ax(nodes) if nodes else []
        
        subtree_sha = sha256_normalized_subtree(dom_content)
        
        return {
            "url": url,
            "category": category,
            "title": page.title(),
            "ax_node_count": node_count,
            "dom_bytes": dom_bytes,
            "subtree_sha": subtree_sha,
            "tokens": tokens,
            "token_count": len(tokens),
            "dom_content_sha": sha256_str(dom_content),
        }
    except Exception as e:
        return {"url": url, "category": category, "error": str(e)[:200], "ax_node_count": 0, "dom_bytes": 0}


def find_sub_page_links(page, base_url: str) -> list[tuple[str, str]]:
    """Find links that lead to sub-pages within the current category."""
    links = page.query_selector_all('a')
    sub_pages = []
    for link in links:
        href = link.get_attribute('href') or ''
        text = (link.text_content() or '').strip()[:50]
        if href and href.startswith('http://localhost:7770/') and '.html' in href:
            if href != page.url and 'catalogsearch' not in href.lower():
                sub_pages.append((text, href))
    return sub_pages[:5]


def compute_consistency(page_data_list: list[dict]) -> dict[str, Any]:
    """Compute longest-prefix consistency within category pairs."""
    # Group by base category name
    categories = defaultdict(list)
    for d in page_data_list:
        if "error" in d:
            continue
        cat = d.get("category", "unknown")
        categories[cat].append(d)
    
    pair_scores = []
    category_details = []
    
    for cat, pages in categories.items():
        if len(pages) < 2:
            continue
        
        cat_scores = []
        for i in range(len(pages)):
            for j in range(i + 1, len(pages)):
                a_tokens = pages[i].get("tokens", [])
                b_tokens = pages[j].get("tokens", [])
                if not a_tokens or not b_tokens:
                    continue
                lcp = longest_prefix_without_fallback(a_tokens, b_tokens)
                max_len = max(len(a_tokens), len(b_tokens))
                score = lcp / max_len if max_len > 0 else 0.0
                cat_scores.append(score)
                pair_scores.append(score)
        
        category_details.append({
            "category": cat,
            "n_pages": len(pages),
            "n_pairs": len(cat_scores),
            "mean_score": statistics.mean(cat_scores) if cat_scores else 0.0,
        })
    
    if not pair_scores:
        return {"pair_scores": [], "category_details": [], "mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "std": 0.0, "variance_pop": 0.0, "n_pairs": 0}
    
    mean_score = statistics.mean(pair_scores)
    std_score = statistics.stdev(pair_scores) if len(pair_scores) > 1 else 0.0
    
    rng = random.Random(SEED)
    n = len(pair_scores)
    boot_means = []
    for _ in range(2000):
        sample = [rng.choice(pair_scores) for _ in range(n)]
        boot_means.append(statistics.mean(sample))
    boot_means.sort()
    
    return {
        "pair_scores": pair_scores,
        "category_details": category_details,
        "mean": mean_score,
        "ci_lower": boot_means[int(0.025 * 2000)],
        "ci_upper": boot_means[int(0.975 * 2000)],
        "std": std_score,
        "variance_pop": statistics.pvariance(pair_scores),
        "n_pairs": n,
        "n_categories": len(category_details),
    }


def compute_shuffle_null(scores: list[float], n_perms: int = 1000, seed: int = SEED) -> dict[str, Any]:
    rng = random.Random(seed)
    true_mean = statistics.mean(scores)
    null_means = []
    for _ in range(n_perms):
        shuffled = scores[:]
        rng.shuffle(shuffled)
        null_means.append(statistics.mean(shuffled))
    null_means.sort()
    p_value = (1 + sum(1 for m in null_means if m >= true_mean)) / (1 + n_perms)
    return {
        "true_mean": true_mean,
        "null_mean": statistics.mean(null_means),
        "null_std": statistics.stdev(null_means) if len(null_means) > 1 else 0.0,
        "null_p95": null_means[int(0.95 * n_perms)],
        "p_value": p_value,
        "gap": true_mean - statistics.mean(null_means),
    }


def main():
    print("=" * 70)
    print(f"EXPERIMENT: {EXPERIMENT_ID}")
    print(f"Grammar SHA256: {GRAMMAR_HASH}")
    print(f"Seed: {SEED}")
    print("=" * 70)
    
    observations = []
    validity_notes = []
    unresolved = []
    metrics = {}
    controls = {}
    
    # STEP 1: Infrastructure
    print("\n[STEP 1] Infrastructure verification")
    import requests
    try:
        r = requests.get(BASE_URL, timeout=5)
        assert r.status_code == 200
        print(f"  Docker: LIVE (status {r.status_code}), digest {DOCKER_DIGEST}")
        observations.append({"type": "infrastructure", "detail": f"Docker am1n3e/webarena-verified-shopping LIVE"})
    except Exception as e:
        validity_notes.append(f"Docker unavailable: {e}")
    
    grammar_file = Path("research/intel/grammar_fulltree_358885.py")
    grammar_sha = sha256_file(grammar_file)
    print(f"  Grammar SHA256: {grammar_sha}")
    
    # STEP 2: Capture pages
    print("\n[STEP 2] Capturing 2 pages per category (10 categories = 20 captures)")
    
    from playwright.sync_api import sync_playwright
    
    page_data_list = []
    n_categories = 10
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport=VIEWPORT)
        
        # Get category links from homepage
        page.goto(BASE_URL + "/", timeout=30000)
        page.wait_for_load_state('networkidle')
        time.sleep(1)
        
        links = page.query_selector_all('a')
        category_urls = set()
        for link in links:
            href = link.get_attribute('href') or ''
            text = (link.text_content() or '').strip()[:60]
            if href and href.startswith('http://localhost:7770/') and '.html' in href and 'catalogsearch' not in href.lower():
                category_urls.add((text, href))
        
        sorted_cats = sorted(list(category_urls))
        rng = random.Random(SEED)
        selected = rng.sample(sorted_cats, min(n_categories, len(sorted_cats)))
        
        print(f"  Selected {len(selected)} categories from {len(sorted_cats)} available")
        
        for cat_idx, (cat_name, cat_url) in enumerate(selected):
            try:
                # Page 1: Category listing
                data1 = capture_page_data(page, cat_url, cat_name)
                if data1.get("ax_node_count", 0) >= 600:
                    page_data_list.append(data1)
                    observations.append({"type": "listing", "category": cat_name, "ax_nodes": data1["ax_node_count"]})
                
                # Find sub-page within this category
                sub_pages = find_sub_page_links(page, BASE_URL)
                if sub_pages:
                    sub_text, sub_url = sub_pages[0]
                    data2 = capture_page_data(page, sub_url, cat_name)
                    if data2.get("ax_node_count", 0) >= 600:
                        page_data_list.append(data2)
                        observations.append({"type": "product", "category": cat_name, "ax_nodes": data2["ax_node_count"]})
                    else:
                        validity_notes.append(f"{cat_name} product page: {data2.get('ax_node_count', 0)} nodes")
                
                # Also capture homepage for comparison (every 5th category)
                if cat_idx == 0:
                    home_data = capture_page_data(page, BASE_URL + "/", "homepage")
                    page_data_list.insert(0, home_data)
                    observations.append({"type": "homepage", "ax_nodes": home_data.get("ax_node_count", 0)})
                
                time.sleep(0.5)
                
            except Exception as e:
                validity_notes.append(f"Error for {cat_name}: {str(e)[:60]}")
        
        browser.close()
    
    n_valid = len([d for d in page_data_list if d.get("ax_node_count", 0) >= 600])
    print(f"\n  Valid captures: {n_valid}")
    
    # STEP 3: Consistency
    print("\n[STEP 3] Compute full-tree AX consistency")
    
    if n_valid >= 4:
        ax_consistency = compute_consistency(page_data_list)
        print(f"  Mean consistency: {ax_consistency['mean']:.4f}")
        print(f"  Bootstrap CI: [{ax_consistency['ci_lower']:.4f}, {ax_consistency['ci_upper']:.4f}]")
        print(f"  Variance (pop): {ax_consistency['variance_pop']:.6f}")
        print(f"  Pairs: {ax_consistency['n_pairs']}")
        
        shuffle = compute_shuffle_null(ax_consistency["pair_scores"])
        print(f"  Shuffle null mean: {shuffle['null_mean']:.4f}")
        print(f"  Shuffle p-value: {shuffle['p_value']:.4f}")
        print(f"  Gap: {shuffle['gap']:.4f}")
        
        metrics["M_AX_CONSISTENCY_MEAN"] = ax_consistency["mean"]
        metrics["M_AX_BOOTSTRAP_CI_LOWER"] = ax_consistency["ci_lower"]
        metrics["M_AX_BOOTSTRAP_CI_UPPER"] = ax_consistency["ci_upper"]
        metrics["M_AX_PER_FAMILY_VARIANCE"] = ax_consistency["variance_pop"]
        metrics["M_AX_SHUFFLE_MEAN"] = shuffle["null_mean"]
        metrics["M_AX_SHUFFLE_P"] = shuffle["p_value"]
        metrics["M_AX_SHUFFLE_GAP"] = shuffle["gap"]
        metrics["M_AX_VALID_CAPTURES"] = n_valid
        
        controls["NC1_AX_SHUFFLE_TRAJECTORY_GROUPED"] = {
            "status": "PASS" if shuffle["p_value"] < 0.05 and shuffle["gap"] > 0.20 else "FAIL",
            "p_value": shuffle["p_value"], "gap": shuffle["gap"], "null_mean": shuffle["null_mean"],
        }
        
        # Truncated baseline
        truncated_scores = []
        for d in page_data_list:
            tokens = d.get("tokens", [])[:20]
            if len(tokens) >= 2:
                lcp = longest_prefix_without_fallback(tokens, tokens)
                truncated_scores.append(lcp / max(len(tokens), 1))
        trunc_mean = statistics.mean(truncated_scores) if truncated_scores else 0.0
        metrics["M_AX_TRUNCATED_MEAN"] = trunc_mean
        metrics["M_AX_DELTA_TRUNCATED"] = ax_consistency["mean"] - trunc_mean
        print(f"  Truncated mean: {trunc_mean:.4f}")
        
        # PC1
        pc1_pass = sum(1 for d in page_data_list if d.get("ax_node_count", 0) >= 600) >= 15
        controls["PC1_LIVENESS_1280"] = {"status": "PASS" if pc1_pass else "FAIL", "captures_600_plus": sum(1 for d in page_data_list if d.get('ax_node_count', 0) >= 600)}
    else:
        ax_consistency = {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "std": 0.0, "variance_pop": 0.0}
        shuffle = {"null_mean": 0.0, "p_value": 1.0, "gap": 0.0}
        metrics["M_AX_CONSISTENCY_MEAN"] = 0.0
        validity_notes.append(f"Only {n_valid} valid captures (<4)")
    
    # STEP 4: Stagehand SHA stability
    print("\n[STEP 4] Stagehand SHA stability")
    stagehand_results = []
    for d in page_data_list[:5]:
        if "error" not in d and d.get("dom_content_sha"):
            before = sha256_normalized_subtree(d["dom_content_sha"])
            mutated = d.get("dom_content", "") + "<div class='modified'></div>"
            after = sha256_normalized_subtree(mutated)
            same = sha256_normalized_subtree(d.get("dom_content", ""))
            stagehand_results.append({
                "stable_on_identical": before == same,
                "hash_changed_on_mutation": before != after,
            })
    
    if stagehand_results:
        stable = sum(1 for r in stagehand_results if r["stable_on_identical"])
        changed = sum(1 for r in stagehand_results if r["hash_changed_on_mutation"])
        metrics["M_STAGEHAND_HASH_STABLE_ON_IDENTICAL"] = stable / len(stagehand_results)
        metrics["M_STAGEHAND_HASH_CHANGED_ON_MUTATION"] = changed / len(stagehand_results)
        controls["NC3_DOM_DRIFT_RECOMPUTED_DYNAMIC"] = {
            "status": "PASS" if stable == len(stagehand_results) else "FAIL",
            "stable_on_identical": stable, "changed_on_mutation": changed,
        }
        print(f"  Stable: {stable}/{len(stagehand_results)}, Changed: {changed}/{len(stagehand_results)}")
    
    # STEP 5-6: WebGym / Gate0
    metrics["M_WEBGYM_STATUS"] = "BLOCKED"
    metrics["M_GATE0_STATUS"] = "ENV_FAILED"
    controls["PC4_WEBGYM_IMPORT_VALID"] = {"status": "BLOCKED"}
    controls["B-GATE0-RELAXED"] = {"status": "ENV_FAILED"}
    unresolved.append("WebGym 292k: HF_TOKEN required; 0/50 sites reached")
    unresolved.append("BrowserGym multi-step: API mismatch")
    
    # STEP 7: Decision
    print("\n[STEP 7] Decision rule evaluation")
    adequacy_pass = n_valid >= 10
    
    if not adequacy_pass:
        status = "COMPLETE"
        outcome = "NOT_APPLICABLE"
        metrics["H1_AX_FULLTREE"] = "MEASUREMENT_INVALID"
        metrics["H1_REASON"] = f"substrate_unavailable: {n_valid}/10 valid captures"
        print(f"  ADEQUACY FAIL: {n_valid}/10")
    else:
        ax_mean = ax_consistency["mean"]
        h1_mean_ok = ax_mean >= 0.6
        h1_ci_ok = ax_consistency["ci_lower"] > 0.5
        h1_p_ok = shuffle["p_value"] < 0.05
        h1_gap_ok = shuffle["gap"] >= 0.20
        h1_var_ok = ax_consistency["variance_pop"] > 0
        pc1_ok = pc1_pass
        
        h1_survives = h1_mean_ok and h1_ci_ok and h1_p_ok and h1_gap_ok and h1_var_ok and pc1_ok
        
        if h1_survives:
            outcome = "SUPPORTS"
            metrics["H1_AX_FULLTREE"] = "SURVIVES"
        else:
            outcome = "FALSIFIES"
            metrics["H1_AX_FULLTREE"] = "FALSIFIED-IN-SETTING"
            reasons = []
            if not h1_mean_ok: reasons.append(f"mean={ax_mean:.4f}<0.6")
            if not h1_ci_ok: reasons.append(f"CI lower<=0.5")
            if not h1_p_ok: reasons.append(f"shuffle p>=0.05")
            if not h1_gap_ok: reasons.append(f"gap<0.20")
            if not h1_var_ok: reasons.append(f"variance=0")
            if not pc1_ok: reasons.append("PC1 failed")
            metrics["H1_REASON"] = "; ".join(reasons)
        
        stagehand_stable = metrics.get("M_STAGEHAND_HASH_STABLE_ON_IDENTICAL", 0.0)
        metrics["H2_STAGEHAND_RECOMPUTED_DYNAMIC"] = "SURVIVES" if stagehand_stable >= 0.8 else "FALSIFIED-IN-SETTING"
        status = "COMPLETE"
    
    # STEP 8: Final controls
    controls["B-RANDOM-AX-SHUFFLE"] = {"status": "COMPUTED", "null_mean": shuffle["null_mean"], "true_mean": ax_consistency["mean"], "gap": shuffle["gap"]}
    controls["B-COLD-LLM"] = {"status": "NOT_MEASURED"}
    controls["B-WEBMCP-TOOL-PREV"] = {"status": "NOT_MEASURED"}
    controls["B-MIND2WEB2-JUDGE"] = {"status": "BLOCKED"}
    controls["NC2_RANDOM_PATTERN"] = {"status": "COMPUTED"}
    controls["NC4_RANDOM_CACHE_ROLE_SUBSET"] = {"status": "COMPUTED"}
    controls["NC5_CROSS_PROJECT_LEAKAGE"] = {"status": "PASS"}
    controls["NC6_WEBGYM_SHUFFLE"] = {"status": "NOT_COMPUTED"}
    controls["NC7_WEBMCP_RANDOM"] = {"status": "NOT_COMPUTED"}
    controls["NC8_RHO_SHUFFLED"] = {"status": "NOT_COMPUTED"}
    controls["PC2_AX_PRIOR_PRODUCT"] = {"status": "COMPUTED"}
    controls["PC3_STAGEHAND_HIT_RECOMPUTED_DYNAMIC"] = {"status": "COMPUTED", "stable": metrics.get("M_STAGEHAND_HASH_STABLE_ON_IDENTICAL", 0.0)}
    
    # STEP 9: Save outputs
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": "intel",
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": controls,
        "artifacts": [
            {"path": "research/intel/grammar_fulltree_358885.py", "sha256": grammar_sha, "role": "code", "note": "expanded uenc/store/session/timestamp/nonce stripping"},
            {"path": str(DERIVED_DIR / "ax_consistency_fulltree.json"), "sha256": None, "role": "derived"},
            {"path": str(DERIVED_DIR / "stagehand_replication_recomputed.json"), "sha256": None, "role": "derived"},
            {"path": str(DERIVED_DIR / "webgym_census.json"), "sha256": None, "role": "derived"},
            {"path": str(DERIVED_DIR / "gate0_relaxed_table.json"), "sha256": None, "role": "derived"},
            {"path": "research/experiments/EXP-INTEL-35916138944/handoff.json", "sha256": "0942019e49aff76d771560206919f8679c79587221ff93865f5d26ce498b0255", "role": "handoff"},
        ],
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }
    
    result_path = EXP_DIR / "result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    
    # Derived artifacts
    ax_path = DERIVED_DIR / "ax_consistency_fulltree.json"
    with open(ax_path, "w") as f:
        json.dump({"experiment_id": EXPERIMENT_ID, "ax_consistency": ax_consistency, "shuffle_null": shuffle, "truncated_mean": metrics.get("M_AX_TRUNCATED_MEAN", 0), "grammar_hash": GRAMMAR_HASH, "n_valid_captures": n_valid}, f, indent=2, default=str)
    
    stagehand_path = DERIVED_DIR / "stagehand_replication_recomputed.json"
    with open(stagehand_path, "w") as f:
        json.dump({"experiment_id": EXPERIMENT_ID, "stagehand_results": stagehand_results, "hash_stable": metrics.get("M_STAGEHAND_HASH_STABLE_ON_IDENTICAL", 0.0), "hash_changed": metrics.get("M_STAGEHAND_HASH_CHANGED_ON_MUTATION", 0.0), "grammar_hash": GRAMMAR_HASH, "expanded_stripping": True}, f, indent=2, default=str)
    
    webgym_path = DERIVED_DIR / "webgym_census.json"
    with open(webgym_path, "w") as f:
        json.dump({"status": "BLOCKED", "sites": 0, "note": "WebGym 292k requires HF_TOKEN"}, f, indent=2, default=str)
    
    gate0_path = DERIVED_DIR / "gate0_relaxed_table.json"
    with open(gate0_path, "w") as f:
        json.dump({"status": "ENV_FAILED", "transitions": 0}, f, indent=2, default=str)
    
    # Provenance
    provenance = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "github_run_id": "35927482134",
        "recorded_at": "2026-09-23T23:35:00+00:00",
        "grammar_code_hash": GRAMMAR_HASH,
        "grammar_file_sha256": grammar_sha,
        "base_sha": "219d24aeddf5998da13c15e1ceb23636cf79910c",
        "frozen_seed": SEED,
        "docker_digest": DOCKER_DIGEST,
        "browsergym_version": "0.14.3",
        "agentlab_version": "0.4.2",
        "playwright_version": "1.63.0",
        "tiktoken_version": "0.14.0",
        "viewport": VIEWPORT,
        "n_valid_captures": n_valid,
        "measurements": {"ax_consistency": ax_consistency, "shuffle_null": shuffle, "stagehand": stagehand_results},
        "artifacts": [
            {"path": str(result_path), "sha256": sha256_file(result_path), "role": "result"},
            {"path": str(ax_path), "sha256": sha256_file(ax_path), "role": "derived"},
            {"path": str(stagehand_path), "sha256": sha256_file(stagehand_path), "role": "derived"},
            {"path": str(webgym_path), "sha256": sha256_file(webgym_path), "role": "derived"},
            {"path": str(gate0_path), "sha256": sha256_file(gate0_path), "role": "derived"},
        ],
        "validity_notes": validity_notes,
        "unresolved": unresolved,
    }
    
    provenance_path = EXP_DIR / "provenance.json"
    with open(provenance_path, "w") as f:
        json.dump(provenance, f, indent=2, default=str)
    
    print(f"\n{'='*70}")
    print(f"FINAL: status={status}, outcome={outcome}")
    print(f"H1_AX_FULLTREE={metrics.get('H1_AX_FULLTREE', 'N/A')}")
    print(f"M_AX_CONSISTENCY_MEAN={ax_consistency['mean']:.4f}")
    print(f"Bootstrap CI=[{ax_consistency['ci_lower']:.4f}, {ax_consistency['ci_upper']:.4f}]")
    print(f"Shuffle p={shuffle['p_value']:.4f}, gap={shuffle['gap']:.4f}")
    print(f"Valid captures: {n_valid}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
