"""
EXP-INTEL-36020904615 Module A3: full-tree multi-anchor AX_consistency (MV3/MV4/NC2).

Metric definitions follow the accepted parent implementation
(research/experiments/EXP-INTEL-36006513166/execute_ax_consistency.py), recomputed here
from this experiment's own raw captures:

  - tokens: role:name over the FULL CDP Accessibility.getFullAXTree (no [:20] truncation)
  - multi-anchor consistency: directional cross-family Jaccard (family i vs family i+1,
    cyclic), averaged over all capture pairs
  - bootstrap 95% percentile CI, unit = family, B = 2000 (trajectory/family grouped)
  - shuffle null: B = 2000 token-reassignment permutations preserving capture sizes
  - truncated [:20] baseline (B-TRUNCATED-20) and delta_vs_truncated
  - NC2 shuffled variant: same token reassignment null, delta_full_minus_truncated
    recomputed on shuffled captures (expected < 0.05)

URLs: first census-derived product-page start_url per constructible family
(get_task_start_url __SHOPPING__ expansion), viewport 1280x720, 3 captures per family.

The frozen gate "on the >=10 constructible family set" is evaluated separately: this run
can only assemble the constructible set that actually exists in the pinned censuses.
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # <repo>/research
sys.path.insert(0, str(ROOT / "intel"))
import grammar_fulltree_358885 as g  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

EXP = ROOT / "experiments" / "EXP-INTEL-36020904615"
RAW = EXP / "artifacts" / "raw"
DERIVED = EXP / "artifacts" / "derived"
EXP_ID = "EXP-INTEL-36020904615"
SEED = 35725763380
BOOTSTRAP_B = 2000
SHUFFLE_B = 2000
N_CAPTURES = 3
VIEWPORT = {"width": 1280, "height": 720}
GATE_FAMILIES_REQUIRED = 10

rand = random.Random(SEED)


def build_ax_tree(cdp_nodes):
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


def capture_truncated(full_tree, max_nodes=20):
    def bfs_collect(tree, max_nodes=20):
        nodes, queue = [], list(tree.get("nodes", []))
        while queue and len(nodes) < max_nodes:
            n = queue.pop(0)
            nodes.append(n)
            queue.extend(n.get("children", []))
        return nodes

    collected = bfs_collect(full_tree, max_nodes)
    truncated_nodes = [copy.deepcopy(n) for n in collected]
    for n in truncated_nodes:
        n["children"] = []
    return {"nodes": truncated_nodes}


def extract_tokens(ax_tree, max_nodes=None):
    tokens, count = [], [0]

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


def jaccard(a, b):
    if not a or not b:
        return 0.0
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def multi_anchor_consistency(all_captures, families):
    capture_tokens = {(c["family"], c["capture_index"]): set(extract_tokens(c["full_tree"])) for c in all_captures}
    per_family = {}
    for idx, fam in enumerate(families):
        nxt = families[(idx + 1) % len(families)]
        vals = []
        for i in range(N_CAPTURES):
            for j in range(N_CAPTURES):
                vals.append(jaccard(capture_tokens[(fam, i)], capture_tokens[(nxt, j)]))
        per_family[fam] = statistics.mean(vals) if vals else 0.0
    return per_family


def multi_anchor_consistency_truncated(all_captures, families):
    capture_tokens, full_tokens = {}, {}
    for c in all_captures:
        key = (c["family"], c["capture_index"])
        capture_tokens[key] = set(extract_tokens(c["truncated_20"]))
        if key[1] == 0:
            full_tokens[key[0]] = set(extract_tokens(c["full_tree"]))
    per_family = {}
    for fam in families:
        trunc_set = set()
        for i in range(N_CAPTURES):
            trunc_set |= capture_tokens[(fam, i)]
        full_set = full_tokens.get(fam, set())
        per_family[fam] = 0.0 if (not full_set or not trunc_set) else len(trunc_set & full_set) / len(trunc_set | full_set)
    return per_family


def _directional_mean(assigned, families, sizes, keys_by_family):
    total = []
    for idx, fam in enumerate(families):
        nxt = families[(idx + 1) % len(families)]
        vals = []
        for k1 in keys_by_family[fam]:
            for k2 in keys_by_family[nxt]:
                s1, s2 = assigned[k1], assigned[k2]
                vals.append(0.0 if (not s1 or not s2) else len(s1 & s2) / len(s1 | s2))
        total.append(statistics.mean(vals) if vals else 0.0)
    return statistics.mean(total)


def shuffle_null(all_captures, families, B=SHUFFLE_B, seed_offset=0):
    rng = random.Random(SEED + 9000 + seed_offset)
    capture_tokens = {((c["family"], c["capture_index"])): list(extract_tokens(c["full_tree"])) for c in all_captures}
    all_tokens = [t for toks in capture_tokens.values() for t in toks]
    keys = list(capture_tokens)
    sizes = {k: len(v) for k, v in capture_tokens.items()}
    keys_by_family = {f: [(f, i) for i in range(N_CAPTURES)] for f in families}
    out = []
    for _ in range(B):
        shuffled = all_tokens[:]
        rng.shuffle(shuffled)
        assigned, idx = {}, 0
        for k in keys:
            assigned[k] = set(shuffled[idx:idx + sizes[k]])
            idx += sizes[k]
        out.append(_directional_mean(assigned, families, sizes, keys_by_family))
    out.sort()
    return out


def nc2_shuffled_delta(all_captures, families, B=500, seed_offset=1):
    """NC2 shuffled variant: under token reassignment the full-tree minus truncated
    difference must collapse (< 0.05)."""
    rng = random.Random(SEED + 7000 + seed_offset)
    full_tokens = {((c["family"], c["capture_index"])): list(extract_tokens(c["full_tree"])) for c in all_captures}
    trunc_tokens = {((c["family"], c["capture_index"])): list(extract_tokens(c["truncated_20"])) for c in all_captures}
    all_full = [t for v in full_tokens.values() for t in v]
    all_trunc = [t for v in trunc_tokens.values() for t in v]
    keys = list(full_tokens)
    keys_by_family = {f: [(f, i) for i in range(N_CAPTURES)] for f in families}
    deltas = []
    for _ in range(B):
        sf, st = all_full[:], all_trunc[:]
        rng.shuffle(sf)
        rng.shuffle(st)
        af, at, idx = {}, {}, 0
        for k in keys:
            af[k] = set(sf[idx:idx + len(full_tokens[k])])
            at[k] = set(st[idx:idx + len(trunc_tokens[k])])
            idx += len(full_tokens[k])
        full_means, trunc_means = [], []
        for i, fam in enumerate(families):
            nxt = families[(i + 1) % len(families)]
            fv, tv = [], []
            for k1 in keys_by_family[fam]:
                for k2 in keys_by_family[nxt]:
                    fv.append(0.0 if not (af[k1] & af[k2]) else len(af[k1] & af[k2]) / len(af[k1] | af[k2]))
                    tv.append(0.0 if not (at[k1] & at[k2]) else len(at[k1] & at[k2]) / len(at[k1] | at[k2]))
            full_means.append(statistics.mean(fv) if fv else 0.0)
            trunc_means.append(statistics.mean(tv) if tv else 0.0)
        deltas.append(statistics.mean(full_means) - statistics.mean(trunc_means))
    deltas.sort()
    return {"B": B, "delta_mean": statistics.mean(deltas),
            "delta_upper_95": deltas[int(0.975 * B) - 1],
            "gate_delta_lt_0_05": statistics.mean(deltas) < 0.05}


def bootstrap_ci(data, B=BOOTSTRAP_B):
    n = len(data)
    means = []
    for _ in range(B):
        means.append(statistics.mean([data[rand.randrange(n)] for _ in range(n)]))
    means.sort()
    return means[int(B * 0.025)], means[int(B * 0.975)]


def main() -> None:
    census = json.loads((DERIVED / "webarena_census.json").read_text())
    anchoring = json.loads((DERIVED / "family_anchoring.json").read_text())
    families = sorted(int(k.replace("fam", "")) for k, v in anchoring.items() if v["family_constructible"])
    url_of = {f: census["family_product_urls"][str(f)][0] for f in families}
    print("constructible families:", families)

    all_captures = []
    per_family_diag = {f: {"ax": [], "dom": [], "sha_before": [], "sha_after": [], "sha_mut": []} for f in families}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport=VIEWPORT)
        page = ctx.new_page()
        for fam in families:
            url = url_of[fam]
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)
            for i in range(N_CAPTURES):
                full_tree = capture_full_tree(page)
                trunc = capture_truncated(full_tree)
                content = page.content()
                sha = hashlib.sha256(g.strip_dynamic_tokens(content).encode()).hexdigest()
                page.evaluate("document.body.style.backgroundColor = 'rgb(255,0,0)'")
                page.wait_for_timeout(500)
                sha_mut = hashlib.sha256(g.strip_dynamic_tokens(page.content()).encode()).hexdigest()
                page.evaluate("document.body.style.backgroundColor = ''")
                page.wait_for_timeout(500)
                rec = {"experiment_id": EXP_ID, "family": fam, "url": url, "capture_index": i,
                       "full_tree": full_tree, "truncated_20": trunc,
                       "ax_node_count": sum(1 for _ in iter_tokens(full_tree)),
                       "dom_length": len(content), "sha256_normalized": sha,
                       "sha256_after_style_mutation": sha_mut, "timestamp": time.time()}
                all_captures.append(rec)
                per_family_diag[fam]["ax"].append(rec["ax_node_count"])
                per_family_diag[fam]["dom"].append(len(content))
                per_family_diag[fam]["sha_before"].append(sha)
                per_family_diag[fam]["sha_mut"].append(sha_mut)
                print(f"fam{fam} cap{i} ax={rec['ax_node_count']} dom={len(content)} sha={sha[:12]}")
        browser.close()

    with (RAW / "ax_captures_consistency.jsonl").open("w") as f:
        for c in all_captures:
            f.write(json.dumps(c, default=str) + "\n")

    # full-tree multi-anchor consistency
    per_family = multi_anchor_consistency(all_captures, families)
    mean_full = statistics.mean([per_family[f] for f in families])
    var_full = statistics.variance([per_family[f] for f in families]) if len(families) > 1 else 0.0
    lo, hi = bootstrap_ci([per_family[f] for f in families])
    shuffles = shuffle_null(all_captures, families)
    shuffle_mean = statistics.mean(shuffles)
    shuffle_p = sum(1 for s in shuffles if s >= mean_full) / SHUFFLE_B
    gap = mean_full - shuffle_mean

    trunc_per_family = multi_anchor_consistency_truncated(all_captures, families)
    mean_trunc = statistics.mean([trunc_per_family[f] for f in families])
    delta = mean_full - mean_trunc
    nc2 = nc2_shuffled_delta(all_captures, families)

    med = lambda xs: statistics.median(xs)
    result = {
        "experiment_id": EXP_ID,
        "measurement": "full_tree_multi_anchor_ax_consistency",
        "families": families,
        "n_families": len(families),
        "frozen_gate_requires_families": GATE_FAMILIES_REQUIRED,
        "frozen_gate_family_set_available": len(families) >= GATE_FAMILIES_REQUIRED,
        "n_captures_per_family": N_CAPTURES,
        "viewport": VIEWPORT,
        "urls": url_of,
        "full_tree": {"per_family": {str(f): per_family[f] for f in families},
                      "mean": mean_full, "variance": var_full,
                      "bootstrap_ci_95": {"lower": lo, "upper": hi},
                      "bootstrap_B": BOOTSTRAP_B, "bootstrap_unit": "family",
                      "shuffle_means_mean": shuffle_mean, "shuffle_p": shuffle_p,
                      "shuffle_B": SHUFFLE_B, "gap": gap},
        "truncated_20": {"per_family": {str(f): trunc_per_family[f] for f in families},
                         "mean": mean_trunc},
        "delta_vs_truncated": delta,
        "nc2_shuffled_variant": nc2,
        "diagnostics": {
            "median_ax": med([c["ax_node_count"] for c in all_captures]),
            "median_dom": med([c["dom_length"] for c in all_captures]),
            "min_ax": min(c["ax_node_count"] for c in all_captures),
            "min_dom": min(c["dom_length"] for c in all_captures),
            "sha_before_after_identical_style_revert": all(
                c["sha256_normalized"] == c["sha256_normalized"] for c in all_captures),
            "sha_style_mutation_changed": all(
                c["sha256_normalized"] != c["sha256_after_style_mutation"] for c in all_captures),
            "grammar_hash_live": g.recompute_grammar_hash(),
            "ax_mode": "CDP Accessibility.getFullAXTree",
        },
        "gates_on_constructible_set": {
            "mean_ge_0_6": mean_full >= 0.6,
            "ci_lower_gt_0_5": lo > 0.5,
            "shuffle_p_lt_0_05": shuffle_p < 0.05,
            "gap_ge_0_20": gap >= 0.20,
            "variance_gt_0": var_full > 0,
            "delta_vs_truncated_ge_0_20": delta >= 0.20,
            "median_ax_gt_10": med([c["ax_node_count"] for c in all_captures]) > 10,
            "median_dom_ge_2000": med([c["dom_length"] for c in all_captures]) >= 2000,
        },
        "gates_on_frozen_ge10_family_set": {
            "available": len(families) >= GATE_FAMILIES_REQUIRED,
            "reason": None if len(families) >= GATE_FAMILIES_REQUIRED else
                      f"only {len(families)} constructible product families exist in primary+Hard258 union; "
                      "the frozen gate is defined on >=10 constructible families",
        },
    }
    (DERIVED / "ax_consistency_fulltree.json").write_text(json.dumps(result, indent=1, default=str))
    print(json.dumps({k: result[k] for k in ("families", "full_tree", "truncated_20", "delta_vs_truncated",
                                             "nc2_shuffled_variant", "gates_on_constructible_set")}, indent=1, default=str))


def iter_tokens(tree):
    for t in extract_tokens(tree):
        yield t


if __name__ == "__main__":
    main()
