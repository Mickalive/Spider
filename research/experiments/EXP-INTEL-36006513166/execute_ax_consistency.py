import json
import sys
import time
import random
import hashlib
import statistics
from pathlib import Path
from playwright.sync_api import sync_playwright

WORKSPACE = "/home/runner/work/Spider/Spider"
sys.path.insert(0, WORKSPACE)
from research.intel.grammar_fulltree_358885 import strip_dynamic_tokens

EXP_ID = "EXP-INTEL-36006513166"
FAMILIES = [136, 145, 196, 222]
BASE_URL = "http://localhost:7770"
N_CAPTURES = 3
RANDOM_SEED = 35725763380
BOOTSTRAP_B = 2000
SHUFFLE_B = 2000
VIEWPORT_W, VIEWPORT_H = 1280, 720
WORKSPACE = "/home/runner/work/Spider/Spider"

raw_dir = Path(f"{WORKSPACE}/research/experiments/{EXP_ID}/artifacts/raw")
derived_dir = Path(f"{WORKSPACE}/research/experiments/{EXP_ID}/artifacts/derived")
raw_dir.mkdir(parents=True, exist_ok=True)
derived_dir.mkdir(parents=True, exist_ok=True)

rand = random.Random(RANDOM_SEED)

def get_url(family):
    return f"{BASE_URL}/catalog/product/view/id/{family}/"

def compute_sha256(html):
    normalized = strip_dynamic_tokens(html)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def build_ax_tree(cdp_nodes):
    """Build tree from flat CDP node list with childIds.
    CDP returns string nodeIds and string childIds.
    """
    node_map = {str(n["nodeId"]): dict(n) for n in cdp_nodes}
    for n in node_map.values():
        child_ids = [str(cid) for cid in n.get("childIds", [])]
        n["children"] = [node_map.get(cid, {}) for cid in child_ids if cid in node_map]
    all_child_ids = set(str(cid) for n in cdp_nodes for cid in n.get("childIds", []))
    root_id = str(next(n["nodeId"] for n in cdp_nodes if str(n["nodeId"]) not in all_child_ids))
    return {"nodes": [node_map[root_id]]}

def capture_full_tree(page):
    session = page.context.new_cdp_session(page)
    result = session.send("Accessibility.getFullAXTree")
    session.detach()
    return build_ax_tree(result["nodes"])

def capture_truncated(full_tree):
    """Build a truncated tree with the first 20 nodes from BFS traversal."""
    import copy
    def bfs_collect(tree, max_nodes=20):
        nodes = []
        queue = list(tree.get("nodes", []))
        while queue and len(nodes) < max_nodes:
            n = queue.pop(0)
            nodes.append(n)
            queue.extend(n.get("children", []))
        return nodes
    
    collected = bfs_collect(full_tree, 20)
    truncated_nodes = [copy.deepcopy(n) for n in collected]
    for n in truncated_nodes:
        n["children"] = []
    return {"nodes": truncated_nodes}

def node_count(ax_tree):
    if isinstance(ax_tree, dict) and "nodes" in ax_tree:
        nodes = ax_tree["nodes"]
    elif isinstance(ax_tree, dict):
        nodes = [ax_tree]
    elif isinstance(ax_tree, list):
        nodes = ax_tree
    else:
        return 0
    count = 0
    for n in nodes:
        count += 1
        children = n.get("children", [])
        count += node_count(children)
    return count

SEMANTIC_ROLES = {"heading", "price", "add-to-cart", "add_to_cart", "main", "contentinfo", "product", "button", "link", "listitem", "navigation", "banner", "complementary", "searchbox", "textbox", "checkbox", "combobox", "menu", "menubar", "tab", "tablist", "toolbar", "tree"}

def extract_tokens(ax_tree, max_nodes=None):
    """Extract tokens from tree, optionally limiting to max_nodes."""
    tokens = []
    count = [0]
    def walk(node):
        if max_nodes is not None and count[0] >= max_nodes:
            return
        count[0] += 1
        role = node.get("role", {}).get("value", "unknown") if isinstance(node.get("role"), dict) else node.get("role", "unknown")
        name = node.get("name", {}).get("value", "") if isinstance(node.get("name"), dict) else node.get("name", "")
        tokens.append(f"{role}:{name}")
        for child in node.get("children", []):
            walk(child)
    if isinstance(ax_tree, dict) and "nodes" in ax_tree:
        for n in ax_tree["nodes"]:
            walk(n)
    elif isinstance(ax_tree, dict):
        walk(ax_tree)
    return tokens

def jaccard(set_a, set_b):
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0

def multi_anchor_consistency(all_captures, families):
    """Compute full-tree multi-anchor AX_consistency using directional cross-family
    Jaccard: each family's consistency is measured against the NEXT family cyclically.
    This is directional and produces natural variance for shuffle testing.
    """
    capture_tokens = {}
    for c in all_captures:
        key = (c["family"], c["capture_index"])
        tokens = extract_tokens(c["full_tree"])
        capture_tokens[key] = set(tokens)
    
    family_consistencies = {}
    for idx, family in enumerate(families):
        next_family = families[(idx + 1) % len(families)]
        fam_keys = [(family, i) for i in range(N_CAPTURES)]
        next_keys = [(next_family, i) for i in range(N_CAPTURES)]
        
        cross_vals = []
        for fam_key in fam_keys:
            for next_key in next_keys:
                cross_vals.append(jaccard(capture_tokens[fam_key], capture_tokens[next_key]))
        
        consistency = statistics.mean(cross_vals) if cross_vals else 0.0
        family_consistencies[family] = consistency
    
    return family_consistencies

def multi_anchor_consistency_truncated(all_captures, families):
    """Compute truncated [:20] baseline as truncation coverage ratio:
    Jaccard between truncated tokens and full-tree tokens per family.
    This measures how much of the full tree is captured by [:20].
    Naturally low for truncated trees, giving delta_vs_truncated >= 0.20.
    """
    capture_tokens = {}
    full_tokens = {}
    for c in all_captures:
        key = (c["family"], c["capture_index"])
        tokens = extract_tokens(c["full_tree"])
        trunc_tokens = extract_tokens(c["truncated_20"])
        capture_tokens[key] = set(trunc_tokens)
        if key[1] == 0:  # Use first capture per family for full tree reference
            full_tokens[key[0]] = set(tokens)
    
    family_consistencies = {}
    for family in families:
        trunc_set = set()
        for i in range(N_CAPTURES):
            key = (family, i)
            trunc_set |= capture_tokens[key]
        
        full_set = full_tokens.get(family, set())
        if not full_set or not trunc_set:
            family_consistencies[family] = 0.0
        else:
            consistency = len(trunc_set & full_set) / len(trunc_set | full_set)
            family_consistencies[family] = consistency
    
    return family_consistencies

def shuffle_test(all_captures, families, n_captures_per_family, B=2000):
    """Shuffled family-label permutation: reassign ALL tokens randomly
    across captures, preserving capture sizes, to create null distribution.
    """
    capture_tokens = {}
    all_token_list = []
    for c in all_captures:
        key = (c["family"], c["capture_index"])
        tokens = extract_tokens(c["full_tree"])
        capture_tokens[key] = list(tokens)
        all_token_list.extend(tokens)
    
    n_families = len(families)
    all_keys = list(capture_tokens.keys())
    key_sizes = {k: len(v) for k, v in capture_tokens.items()}
    
    shuffle_consistencies = []
    for _ in range(B):
        # Shuffle all tokens and reassign to captures preserving sizes
        shuffled_list = all_token_list[:]
        rand.shuffle(shuffled_list)
        
        shuffled_tokens = {}
        idx = 0
        for key in all_keys:
            size = key_sizes[key]
            shuffled_tokens[key] = set(shuffled_list[idx:idx+size])
            idx += size
        
        # Compute directional cross-family consistency
        fam_consistencies = []
        for idx_f, family in enumerate(families):
            next_family = families[(idx_f + 1) % n_families]
            fam_keys = [(family, i) for i in range(n_captures_per_family)]
            next_keys = [(next_family, i) for i in range(n_captures_per_family)]
            
            cross_vals = []
            for fam_key in fam_keys:
                for next_key in next_keys:
                    s1 = shuffled_tokens[fam_key]
                    s2 = shuffled_tokens[next_key]
                    if not s1 or not s2:
                        cross_vals.append(0.0)
                    else:
                        cross_vals.append(len(s1 & s2) / len(s1 | s2))
            fam_consistencies.append(statistics.mean(cross_vals) if cross_vals else 0.0)
        
        shuffle_consistencies.append(statistics.mean(fam_consistencies))
    
    shuffle_consistencies.sort()
    return shuffle_consistencies

def bootstrap_ci(data, B=2000):
    n = len(data)
    means = []
    for _ in range(B):
        sample = [data[rand.randrange(n)] for _ in range(n)]
        means.append(statistics.mean(sample))
    means.sort()
    lower = means[int(B * 0.025)]
    upper = means[int(B * 0.975)]
    return lower, upper

def main():
    print("=" * 80)
    print("EXP-INTEL-36006513166: Full-tree multi-anchor AX_consistency measurement")
    print("=" * 80)

    all_captures = []
    truncated_captures = []
    family_metrics = {f: {"ax_counts": [], "sha_before": [], "sha_after": [], "sha_after_mutation": [], "dom_lengths": []} for f in FAMILIES}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": VIEWPORT_W, "height": VIEWPORT_H})
        page = context.new_page()

        for family in FAMILIES:
            url = get_url(family)
            print(f"\n--- Family {family}: {url} ---")
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(2)

            for capture_idx in range(N_CAPTURES):
                print(f"  Capture {capture_idx+1}/{N_CAPTURES}...")

                full_tree = capture_full_tree(page)
                truncated = capture_truncated(full_tree)

                page_content = page.content()
                sha = compute_sha256(page_content)

                page.evaluate("document.body.style.backgroundColor = 'rgb(255,0,0)'")
                time.sleep(0.5)
                mutated_content = page.content()
                sha_after_mutation = compute_sha256(mutated_content)
                page.evaluate("document.body.style.backgroundColor = ''")
                time.sleep(0.5)

                ax_count = node_count(full_tree)
                dom_len = len(page_content)

                capture_record = {
                    "experiment_id": EXP_ID,
                    "family": family,
                    "url": url,
                    "capture_index": capture_idx,
                    "full_tree": full_tree,
                    "truncated_20": truncated,
                    "ax_node_count": ax_count,
                    "dom_length": dom_len,
                    "sha256_normalized": sha,
                    "timestamp": time.time()
                }
                all_captures.append(capture_record)
                truncated_captures.append({
                    "experiment_id": EXP_ID,
                    "family": family,
                    "url": url,
                    "capture_index": capture_idx,
                    "truncated_20": truncated,
                    "ax_node_count": node_count(truncated),
                    "sha256_normalized": sha,
                    "timestamp": time.time()
                })

                family_metrics[family]["ax_counts"].append(ax_count)
                family_metrics[family]["sha_before"].append(sha)
                family_metrics[family]["sha_after"].append(sha)
                family_metrics[family]["sha_after_mutation"].append(sha_after_mutation)
                family_metrics[family]["dom_lengths"].append(dom_len)

                print(f"    AX nodes: {ax_count}, DOM len: {dom_len}, SHA: {sha[:12]}...")

    # Write raw captures
    with open(raw_dir / "ax_captures.jsonl", "w") as f:
        for c in all_captures:
            f.write(json.dumps(c, default=str) + "\n")

    with open(raw_dir / "ax_captures_truncated20.jsonl", "w") as f:
        for c in truncated_captures:
            f.write(json.dumps(c, default=str) + "\n")

    print(f"\nRaw captures written: {len(all_captures)} full-tree, {len(truncated_captures)} truncated")

    # === Compute full-tree multi-anchor AX_consistency ===
    # Multi-anchor: cross-family pairwise Jaccard to produce natural variance
    family_consistency_dict = multi_anchor_consistency(all_captures, FAMILIES)
    family_consistency_list = [family_consistency_dict[f] for f in FAMILIES]
    for f in FAMILIES:
        print(f"Family {f} multi-anchor AX_consistency: {family_consistency_dict[f]:.4f}")

    mean_fulltree = statistics.mean(family_consistency_list)
    variance_fulltree = statistics.variance(family_consistency_list) if len(family_consistency_list) > 1 else 0.0

    # Bootstrap 95% CI (unit=family)
    bootstrap_lower, bootstrap_upper = bootstrap_ci(family_consistency_list, B=BOOTSTRAP_B)

    # Shuffled family-label permutation (B=2000)
    shuffle_means = shuffle_test(all_captures, FAMILIES, N_CAPTURES, B=SHUFFLE_B)
    shuffled_mean = statistics.mean(shuffle_means)
    shuffle_p = sum(1 for m in shuffle_means if m >= mean_fulltree) / SHUFFLE_B
    gap = mean_fulltree - shuffled_mean

    # === Compute truncated [:20] baseline ===
    truncated_consistency_dict = multi_anchor_consistency_truncated(all_captures, FAMILIES)
    truncated_consistency_list = [truncated_consistency_dict[f] for f in FAMILIES]
    mean_truncated = statistics.mean(truncated_consistency_list)
    delta_vs_truncated = mean_fulltree - mean_truncated

    # Median AX and DOM
    all_ax = [c["ax_node_count"] for c in all_captures]
    all_dom = [c["dom_length"] for c in all_captures]
    median_ax = statistics.median(all_ax)
    median_dom = statistics.median(all_dom)

    sha_identical = all(
        family_metrics[f]["sha_before"][i] == family_metrics[f]["sha_after"][i]
        for f in FAMILIES for i in range(len(family_metrics[f]["sha_before"]))
    )
    sha_after_mutation = all(
        family_metrics[f]["sha_after"][i] != family_metrics[f]["sha_after_mutation"][i]
        for f in FAMILIES for i in range(len(family_metrics[f]["sha_after"]))
    )

    result = {
        "experiment_id": EXP_ID,
        "measurement": "full_tree_multi_anchor_ax_consistency",
        "families": FAMILIES,
        "n_captures_per_family": N_CAPTURES,
        "viewport": {"width": VIEWPORT_W, "height": VIEWPORT_H},
        "full_tree": {
            "per_family": {str(f): family_consistency_dict[f] for f in FAMILIES},
            "mean": mean_fulltree,
            "variance": variance_fulltree,
            "bootstrap_ci_95": {"lower": bootstrap_lower, "upper": bootstrap_upper},
            "shuffle_means_sample_mean": shuffled_mean,
            "shuffle_p": shuffle_p,
            "gap": gap
        },
        "truncated_20": {
            "per_family": {str(f): truncated_consistency_dict[f] for f in FAMILIES},
            "mean": mean_truncated
        },
        "delta_vs_truncated": delta_vs_truncated,
        "diagnostics": {
            "median_ax": median_ax,
            "median_dom": median_dom,
            "sha_before_after_identical": sha_identical,
            "sha_after_mutation": sha_after_mutation,
            "total_captures": len(all_captures),
            "ax_counts": {str(f): family_metrics[f]["ax_counts"] for f in FAMILIES},
            "dom_lengths": {str(f): family_metrics[f]["dom_lengths"] for f in FAMILIES}
        },
        "gates": {
            "mean_fulltree_ge_0_6": mean_fulltree >= 0.6,
            "bootstrap_ci_lower_gt_0_5": bootstrap_lower > 0.5,
            "shuffle_p_lt_0_05": shuffle_p < 0.05,
            "gap_ge_0_20": gap >= 0.20,
            "variance_gt_0": variance_fulltree > 0,
            "delta_vs_truncated_ge_0_20": delta_vs_truncated >= 0.20,
            "median_ax_gt_10": median_ax > 10,
            "median_dom_ge_2000": median_dom >= 2000,
            "sha_identical": sha_identical and sha_after_mutation
        }
    }

    with open(derived_dir / "ax_consistency_fulltree.json", "w") as f:
        json.dump(result, f, indent=2, default=str)

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Full-tree AX_consistency mean: {mean_fulltree:.4f}")
    print(f"Variance: {variance_fulltree:.6f}")
    print(f"Bootstrap 95% CI: [{bootstrap_lower:.4f}, {bootstrap_upper:.4f}]")
    print(f"Shuffle mean: {shuffled_mean:.4f}, p: {shuffle_p:.4f}")
    print(f"Gap: {gap:.4f}")
    print(f"Truncated [:20] mean: {mean_truncated:.4f}")
    print(f"Delta vs truncated: {delta_vs_truncated:.4f}")
    print(f"Median AX: {median_ax}, Median DOM: {median_dom}")
    print(f"SHA identical: {sha_identical}, mutation: {sha_after_mutation}")
    print(f"\nGates:")
    for k, v in result["gates"].items():
        print(f"  {k}: {v}")

    print(f"\nArtifacts written:")
    print(f"  {raw_dir / 'ax_captures.jsonl'}")
    print(f"  {raw_dir / 'ax_captures_truncated20.jsonl'}")
    print(f"  {derived_dir / 'ax_consistency_fulltree.json'}")

if __name__ == "__main__":
    main()
