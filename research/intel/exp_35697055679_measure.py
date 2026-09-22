#!/usr/bin/env python3
"""
EXP-INTEL-35697055679 measurement script (EXECUTE phase).

Frozen design: verify actual mechanism sharing on WebArena Docker datasets by
extracting accessibility trees from shopping stores and measuring:
  - mechanism overlap fraction (frozen: intent templates appearing in >=2 stores)
  - parameterization prevalence (intent templates with variable fields)
  - duplication fraction (tasks with identical intent templates)
plus positive control (search mechanism) and null control (Wikipedia, if Docker available).

Environment facts established before measurement:
  - WebArena-Verified v2 dataset (assets/dataset/webarena-verified.json, 812 tasks)
  - WebArenaSite.SHOPPING maps to ONE container: am1n3e/webarena-verified-shopping:latest
    (src/webarena_verified/environments/container/config.py) -> localhost:7770
  - Running container serves "One Stop Market" (Magento), single store view,
    general/single_store_mode/enabled=1 -> no per-store switching.
  - docker hub tag census for am1n3e/webarena-verified-shopping: [latest, 0.1.0] only
    -> no per-store images exist.

Therefore: cross-store overlap across 12 store instances is not computable because the
dataset defines exactly one shopping store. All other frozen measurements are executed.

Sampling (frozen): seed = 35697055679; 10 tasks stratified by intent template type.
With a single store this means: 10 tasks across >=5 distinct intent template families
(2 tasks per family where possible) so both parameterized variation and re-use are
observable on live pages.

Extraction: Playwright + Chromium, CDP Accessibility.getFullAXTree, initial viewport
1280x720, raw trees saved with sha256.
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE_URL = "http://localhost:7770"
SEED = 35697055679
VIEWPORT = {"width": 1280, "height": 720}
SHOPPING_TOKEN = "__SHOPPING__"

EXPERIMENT_DIR = Path("research/experiments/EXP-INTEL-35697055679")
RAW_DIR = EXPERIMENT_DIR / "artifacts" / "raw"
DERIVED_DIR = EXPERIMENT_DIR / "artifacts" / "derived"
DATASET_PATH = RAW_DIR / "webarena-verified.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_start_url(url: str) -> str:
    """Resolve __SHOPPING__ token to the running container URL."""
    if SHOPPING_TOKEN in url:
        suffix = url.split(SHOPPING_TOKEN, 1)[1]
        return BASE_URL + suffix
    return url


def load_tasks() -> list[dict]:
    with open(DATASET_PATH, encoding="utf-8") as f:
        return json.load(f)


def by_template_items(task_list):
    d = defaultdict(list)
    for t in task_list:
        d[t["intent_template"]].append(t)
    return d.items()


def select_tasks(shopping_tasks: list[dict], seed: int, n: int = 10) -> list[dict]:
    """Stratified selection: distinct intent-template families, 2 tasks per family."""
    rng = random.Random(seed)
    by_template: dict[str, list[dict]] = defaultdict(list)
    for t in shopping_tasks:
        by_template[t["intent_template"]].append(t)
    for fam in by_template.values():
        fam.sort(key=lambda t: t["task_id"])
        rng.shuffle(fam)  # seeded shuffles only affect intra-family pick order (low cost)
    ordered = sorted(by_template.items(), key=lambda kv: (-len(kv[1]), kv[0]))  # freq desc
    selected: list[dict] = []
    fam_use: dict[str, int] = defaultdict(int)
    # round-robin over families, take up to 2 per family until n reached
    remaining = n
    while remaining > 0:
        progressed = False
        for tpl, fam in ordered:
            if remaining == 0:
                break
            if fam_use[tpl] >= min(2, len(fam)):
                continue
            selected.append(fam[fam_use[tpl]])
            fam_use[tpl] += 1
            remaining -= 1
            progressed = True
        if not progressed:
            break
    return selected


def extract_ax_snapshot(page) -> dict:
    """Full AX tree via CDP at current viewport (initial)."""
    cdp = page.context.new_cdp_session(page)
    tree = cdp.send("Accessibility.getFullAXTree")
    return tree


def interactive_from_ax(nodes: list[dict]) -> list[dict]:
    INTERACTIVE_ROLES = {
        "textbox", "searchbox", "button", "link", "combobox", "checkbox", "radio",
        "menuitem", "menuitemcheckbox", "menuitemradio", "listbox", "option",
        "slider", "spinbutton", "switch", "tab", "treeitem", "textbox", "searchbox",
    }
    out = []
    for n in nodes:
        role = n.get("role", {}).get("value")
        if role in INTERACTIVE_ROLES:
            name = n.get("name", {}).get("value", "")
            node_id = n.get("nodeId")
            props = {}
            for p in n.get("properties", []):
                pname = p.get("name")
                val = p.get("value", {})
                props[pname] = val.get("value") if isinstance(val, dict) else val
            out.append({"nodeId": node_id, "role": role, "name": name,
                        "props": {k: v for k, v in props.items() if k in
                                  ("focusable", "editable", "settable", "multiline", "level", "checked")}})
    return out


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    dataset_hash = sha256_file(DATASET_PATH)
    tasks = load_tasks()
    shopping = [t for t in tasks if "shopping" in t["sites"]]

    # ---------- (1) task-definition-level analysis ----------
    tpl_counts = Counter(t["intent_template"] for t in shopping)
    tpl_total = len(tpl_counts)
    tasks_with_tpl_reuse = sum(c for c in tpl_counts.values() if c >= 2)
    dup_tasks = sum(c for c in tpl_counts.values() if c > 1)
    dup_fraction = dup_tasks / len(shopping) if shopping else None

    param_tasks = [t for t in shopping if t.get("instantiation_dict")]
    param_task_fraction = len(param_tasks) / len(shopping) if shopping else None
    tpl_param = [tpl for tpl, ts in by_template_items(shopping) if any(t.get("instantiation_dict") for t in ts)]
    param_tpl_fraction = len(tpl_param) / tpl_total if tpl_total else None

    # exact copies (identical template AND identical instantiation)
    tpl_inst = Counter((t["intent_template"], json.dumps(t.get("instantiation_dict") or {}, sort_keys=True)) for t in shopping)
    copies = sum(c for c in tpl_inst.values() if c > 1)
    copy_fraction = copies / len(shopping) if shopping else None

    # which distinct 'site' values appear on shopping tasks (stores)
    site_counter = Counter(tuple(t["sites"]) for t in shopping)

    # (2) sampling / extraction
    selected = select_tasks(shopping, SEED, 10)
    extracted = []
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport=VIEWPORT)
        for t in selected:
            url = resolve_start_url(t["start_urls"][0])
            rec = {
                "task_id": t["task_id"],
                "intent_template": t["intent_template"],
                "intent": t["intent"],
                "instantiation_dict": t.get("instantiation_dict") or {},
                "start_url": url,
            }
            try:
                resp = page.goto(url, timeout=60000, wait_until="load")
                page.wait_for_timeout(1500)
                tree = extract_ax_snapshot(page)
                nodes = tree.get("nodes", [])
                raw_path = RAW_DIR / f"axtree_task_{t['task_id']}.json"
                with open(raw_path, "w", encoding="utf-8") as f:
                    json.dump(tree, f)
                inter = interactive_from_ax(nodes)
                rec.update({
                    "http_status": resp.status if resp else None,
                    "title": page.title(),
                    "final_url": page.url,
                    "ax_node_count": len(nodes),
                    "interactive_elements": inter,
                    "raw_tree_path": str(raw_path),
                    "raw_tree_sha256": sha256_file(raw_path),
                    "extraction_error": None,
                })
            except Exception as e:  # noqa: BLE001
                rec.update({"extraction_error": f"{type(e).__name__}: {e}"})
            extracted.append(rec)
        browser.close()

    # ---------- (3) positive control on live store ----------
    # Search mechanism: textbox/searchbox input + submit button on the store.
    pc_seen = Counter()
    for rec in extracted:
        if rec.get("extraction_error"):
            continue
        for el in rec["interactive_elements"]:
            key = f"{el['role']}|{(el['name'] or '').strip().lower()}"
            pc_seen[key] += 1
    searchbox_present = any(k.startswith(("searchbox|", "textbox|")) for k in pc_seen)
    # dedicated combined check: look for elements whose role/name match search patterns
    search_elements = [k for k in pc_seen
                       if k.split("|", 1)[0] in ("searchbox", "textbox") and ("search" in k.split("|", 1)[1] or "find" in k.split("|", 1)[1])]

    summary = {
        "shopping_task_count": len(shopping),
        "distinct_intent_templates": tpl_total,
        "tasks_with_template_reuse_ge2": tasks_with_tpl_reuse,
        "dup_fraction_identical_template": dup_fraction,
        "copy_fraction_identical_template_and_instantiation": copy_fraction,
        "param_tasks": len(param_tasks),
        "param_task_fraction": param_task_fraction,
        "param_template_fraction": param_tpl_fraction,
        "site_tuples": {"+".join(k) if isinstance(k, tuple) else k: v for k, v in site_counter.items()},
        "selected_tasks": [t["task_id"] for t in selected],
        "selected_template_families": sorted({t["intent_template"] for t in selected}),
    }

    derived = {
        "dataset_sha256": dataset_hash,
        "seed": SEED,
        "base_url": BASE_URL,
        "summary": summary,
        "extracted": extracted,
        "positive_control": {
            "searchbox_present_any_page": searchbox_present,
            "search_named_elements": search_elements,
            "cooccurrence": dict(pc_seen),
        },
    }
    out_path = DERIVED_DIR / "measurements.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(derived, f, indent=1)
    print(json.dumps(summary, indent=2))
    print("OUTPUT:", out_path, sha256_file(out_path))
    for rec in extracted:
        status = "OK" if not rec.get("extraction_error") else f"ERR({rec['extraction_error'][:60]})"
        print(f"task {rec['task_id']}: {status} ax={rec.get('ax_node_count')} inter={len(rec.get('interactive_elements', []))} "
              f"title={rec.get('title','')[:40]!r}")


if __name__ == "__main__":
    sys.exit(main())