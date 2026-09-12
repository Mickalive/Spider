#!/usr/bin/env python3
"""
EXP-INTEL-34607693437 Frozen Measurement Script
Measures fragment yield under frozen fallback definition (interactive elements with bbox)
 across randomized shopping page types + gitlab + reddit.
"""

import asyncio
import json
import hashlib
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

# Frozen seed for reproducible randomization
FROZEN_SEED = 34607693437

# Viewport dimensions
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
INTERSECTION_THRESHOLD = 0.5

# Frozen canonical definition: interactive elements with bounding box
INTERACTIVE_ROLES = {
    "button", "link", "textbox", "checkbox", "radio",
    "combobox", "listbox", "menuitem", "tab", "slider",
    "spinbutton", "searchbox", "switch"
}

# Output directory
OUTPUT_DIR = Path("/home/runner/work/Spider/Spider/research/experiments/EXP-INTEL-34607693437/artifacts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def sha256_file(path):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def is_in_viewport(box, vw=VIEWPORT_WIDTH, vh=VIEWPORT_HEIGHT, threshold=INTERSECTION_THRESHOLD):
    """Check if bounding box intersects viewport with threshold."""
    if not box or box.get("width", 0) <= 0 or box.get("height", 0) <= 0:
        return False
    # Viewport rect: (0, 0, vw, vh)
    x1 = max(box.get("x", 0), 0)
    y1 = max(box.get("y", 0), 0)
    x2 = min(box.get("x", 0) + box.get("width", 0), vw)
    y2 = min(box.get("y", 0) + box.get("height", 0), vh)
    if x1 >= x2 or y1 >= y2:
        return False
    intersection_area = (x2 - x1) * (y2 - y1)
    box_area = box.get("width", 0) * box.get("height", 0)
    if box_area <= 0:
        return False
    return (intersection_area / box_area) >= threshold


def has_bbox(node):
    """Check if node has non-null bounding box with width > 0 and height > 0."""
    bbox = node.get("boundingBox") or node.get("bounding_box") or node.get("bbox")
    if not bbox:
        return False
    return bbox.get("width", 0) > 0 and bbox.get("height", 0) > 0


def is_interactive(node):
    """Check if node matches frozen canonical definition of interactive element."""
    role = (node.get("role") or "").lower()
    
    # Check role-based matching
    if role in INTERACTIVE_ROLES:
        return True
    
    # Check form membership
    if role == "form":
        return True
    
    # Check aria attributes
    aria_label = node.get("aria-label") or node.get("ariaLabel") or ""
    aria_describedby = node.get("aria-describedby") or node.get("ariaDescribedby") or ""
    if (aria_label and aria_label.strip()) or (aria_describedby and aria_describedby.strip()):
        return True
    
    # Check event handlers (if available in accessibility tree)
    # Note: CDP accessibility tree may not expose onclick directly
    # We rely on role and aria attributes primarily
    
    return False


def count_elements(ax_tree):
    """
    Count elements under frozen definition.
    Returns (viewport_elements, locatable_elements, total_elements, viewport_sample).
    """
    viewport_count = 0
    locatable_count = 0
    total_count = 0
    viewport_sample = []
    
    def traverse(node):
        nonlocal viewport_count, locatable_count, total_count, viewport_sample
        
        total_count += 1
        
        # Check if element matches frozen definition (locatable)
        has_box = has_bbox(node)
        is_inter = is_interactive(node)
        
        if has_box and is_inter:
            locatable_count += 1
            
            # Check viewport intersection
            bbox = node.get("boundingBox") or node.get("bounding_box") or node.get("bbox")
            if bbox and is_in_viewport(bbox):
                viewport_count += 1
                if len(viewport_sample) < 20:
                    viewport_sample.append({
                        "role": node.get("role", ""),
                        "name": (node.get("name") or "")[:100],
                        "bbox": bbox
                    })
        
        # Traverse children
        for child in node.get("children", []):
            traverse(child)
    
    if ax_tree:
        traverse(ax_tree)
    
    return viewport_count, locatable_count, total_count, viewport_sample


async def measure_task(page, task_url, task_id, site_type, page_type, output_dir):
    """Measure a single task page."""
    print(f"  Measuring task {task_id}: {task_url}")
    
    result = {
        "task_id": task_id,
        "url": task_url,
        "site_type": site_type,
        "page_type": page_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": None
    }
    
    try:
        # Navigate to page
        response = await page.goto(task_url, wait_until="networkidle", timeout=30000)
        result["status_code"] = response.status if response else None
        
        # Wait for page to settle
        await asyncio.sleep(2)
        
        # Get page title
        result["page_title"] = await page.title()
        
        # Get CDP accessibility tree
        cdp_session = await page.context.new_cdp_session(page)
        
        # Get full accessibility tree
        ax_tree_result = await cdp_session.send("Accessibility.getFullAXTree")
        ax_tree = ax_tree_result.get("nodes", [])
        
        # Build tree structure from flat list
        # CDP returns flat list with backendNodeId references
        node_map = {}
        roots = []
        
        for node in ax_tree:
            backend_id = node.get("backendDOMNodeId") or node.get("backendNodeId")
            if backend_id:
                node_map[backend_id] = {
                    "role": node.get("role", ""),
                    "name": node.get("name", {}).get("value", "") if isinstance(node.get("name"), dict) else str(node.get("name", "")),
                    "description": node.get("description", {}).get("value", "") if isinstance(node.get("description"), dict) else str(node.get("description", "")),
                    "children": [],
                    "properties": node.get("properties", []),
                    "parentId": node.get("parentId"),
                }
        
        # Build parent-child relationships
        for backend_id, node in node_map.items():
            parent_id = node.pop("parentId", None)
            if parent_id and parent_id in node_map:
                node_map[parent_id]["children"].append(node)
            elif parent_id is None:
                roots.append(node)
        
        # Get bounding boxes via DOM.getBoxModel for each node
        # This is expensive, so we sample
        dom_nodes = await cdp_session.send("DOM.getDocument", {"depth": -1, "pierce": True})
        
        # Get bounding boxes via page evaluation (faster than CDP for many nodes)
        bbox_data = await page.evaluate("""
            () => {
                const results = {};
                // Get all elements with bounding boxes
                const allElements = document.querySelectorAll('*');
                for (const el of allElements) {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        // Get role from aria or tag
                        let role = el.getAttribute('role') || '';
                        if (!role) {
                            const tag = el.tagName.toLowerCase();
                            const roleMap = {
                                'a': 'link', 'button': 'button', 'input': 'textbox',
                                'select': 'combobox', 'textarea': 'textbox',
                                'checkbox': 'checkbox', 'radio': 'radio',
                                'li': 'listitem', 'ul': 'list', 'ol': 'list',
                                'h1': 'heading', 'h2': 'heading', 'h3': 'heading',
                                'h4': 'heading', 'h5': 'heading', 'h6': 'heading',
                                'img': 'image', 'nav': 'navigation', 'main': 'main',
                                'header': 'banner', 'footer': 'contentinfo',
                                'aside': 'complementary', 'section': 'region',
                                'article': 'article', 'form': 'form',
                                'table': 'table', 'td': 'cell', 'th': 'columnheader',
                                'tr': 'row', 'thead': 'rowgroup', 'tbody': 'rowgroup',
                                'div': 'generic', 'span': 'generic', 'p': 'text',
                                'label': 'text', 'option': 'option'
                            };
                            role = roleMap[tag] || tag;
                        }
                        
                        // Check aria attributes
                        const ariaLabel = el.getAttribute('aria-label') || '';
                        const ariaDescribedby = el.getAttribute('aria-describedby') || '';
                        
                        // Check form membership
                        const inForm = el.closest('form') !== null;
                        
                        // Check event handlers
                        const hasOnclick = el.onclick !== null || el.hasAttribute('onclick');
                        const hasOnsubmit = el.onsubmit !== null || el.hasAttribute('onsubmit');
                        
                        const classNameStr = typeof el.className === 'string' ? el.className : (el.className.baseVal || '');
                        results[el.tagName + '_' + classNameStr.substring(0, 50)] = {
                            x: rect.x, y: rect.y, width: rect.width, height: rect.height,
                            role: role, name: (el.textContent || '').substring(0, 100),
                            ariaLabel: ariaLabel, ariaDescribedby: ariaDescribedby,
                            inForm: inForm, hasOnclick: hasOnclick, hasOnsubmit: hasOnsubmit,
                            tagName: el.tagName, className: classNameStr.substring(0, 100)
                        };
                    }
                }
                return results;
            }
        """)
        
        # Count elements using frozen definition
        viewport_count = 0
        locatable_count = 0
        viewport_sample = []
        
        for key, data in bbox_data.items():
            role = data.get("role", "").lower()
            has_box = data.get("width", 0) > 0 and data.get("height", 0) > 0
            
            if not has_box:
                continue
            
            # Check interactive criteria
            is_inter = False
            if role in INTERACTIVE_ROLES:
                is_inter = True
            elif role == "form":
                is_inter = True
            elif data.get("ariaLabel", "").strip():
                is_inter = True
            elif data.get("ariaDescribedby", "").strip():
                is_inter = True
            elif data.get("inForm", False) and role in ("textbox", "button", "link", "checkbox", "radio", "combobox", "listbox", "menuitem"):
                is_inter = True
            elif data.get("hasOnclick", False) or data.get("hasOnsubmit", False):
                is_inter = True
            
            if is_inter:
                locatable_count += 1
                
                # Check viewport
                bbox = {"x": data["x"], "y": data["y"], "width": data["width"], "height": data["height"]}
                if is_in_viewport(bbox):
                    viewport_count += 1
                    if len(viewport_sample) < 20:
                        viewport_sample.append({
                            "role": data.get("role", ""),
                            "name": data.get("name", "")[:100],
                            "bbox": bbox,
                            "tag": data.get("tagName", ""),
                            "class": data.get("className", "")[:50]
                        })
        
        result["total_cdp_elements"] = len(bbox_data)
        result["locatable_elements"] = locatable_count
        result["viewport_elements"] = viewport_count
        result["viewport_sample"] = viewport_sample
        
        # Save raw accessibility tree
        raw_path = output_dir / f"raw_ax_tree_{task_id}_initial.json"
        with open(raw_path, "w") as f:
            json.dump({"url": task_url, "cdp_tree": ax_tree, "bbox_data": bbox_data}, f)
        result["raw_ax_tree_path"] = str(raw_path)
        result["raw_ax_tree_sha256"] = sha256_file(raw_path)
        
        # Save viewport sample
        sample_path = output_dir / f"viewport_sample_{task_id}.json"
        with open(sample_path, "w") as f:
            json.dump(viewport_sample, f)
        result["viewport_sample_path"] = str(sample_path)
        
        # Compute yields
        if result["total_cdp_elements"] > 0:
            result["yield_cdp"] = viewport_count / result["total_cdp_elements"]
        else:
            result["yield_cdp"] = 0.0
        
        if result["locatable_elements"] > 0:
            result["yield_locatable"] = viewport_count / result["locatable_elements"]
        else:
            result["yield_locatable"] = 0.0
        
        # Method1 deltas
        result["method1_yield"] = 0.365
        result["method1_delta_pp"] = abs(result["yield_locatable"] - 0.365) * 100
        result["method1_within_15pp"] = result["method1_delta_pp"] <= 15.0
        
        # CDP baseline delta
        result["cdp_baseline_yield"] = 0.0426
        result["cdp_delta_pp"] = abs(result["yield_cdp"] - 0.0426) * 100
        
        print(f"    viewport={viewport_count}, locatable={locatable_count}, cdp={result['total_cdp_elements']}")
        print(f"    yield_cdp={result['yield_cdp']:.4f}, yield_locatable={result['yield_locatable']:.4f}")
        
    except Exception as e:
        result["error"] = str(e)
        print(f"    ERROR: {e}")
    
    return result


async def main():
    """Main measurement routine."""
    print(f"EXP-INTEL-34607693437 Frozen Measurement")
    print(f"Frozen seed: {FROZEN_SEED}")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()
    
    # Define task URLs by page type
    # Shopping tasks from WebArena-Verified (Magento 2 site)
    shopping_tasks = {
        "product_listing": [
            ("shop_listing_001", "http://localhost:8080/beauty-personal-care.html", "Beauty & Personal Care"),
            ("shop_listing_002", "http://localhost:8080/electronics.html", "Electronics"),
            ("shop_listing_003", "http://localhost:8080/home-kitchen.html", "Home & Kitchen"),
            ("shop_listing_004", "http://localhost:8080/clothing.html", "Clothing"),
            ("shop_listing_005", "http://localhost:8080/beauty-personal-care/makeup.html", "Makeup"),
            ("shop_listing_006", "http://localhost:8080/beauty-personal-care/hair-care.html", "Hair Care"),
        ],
        "product_detail": [
            ("shop_detail_001", "http://localhost:8080/beauty-personal-care/hair-care/shampoo-conditioner.html", "Shampoo & Conditioner"),
            ("shop_detail_002", "http://localhost:8080/beauty-personal-care/makeup/eyes.html", "Eye Makeup"),
            ("shop_detail_003", "http://localhost:8080/beauty-personal-care/fragrance/women-s.html", "Women's Fragrance"),
            ("shop_detail_004", "http://localhost:8080/beauty-personal-care/skin-care.html", "Skin Care"),
        ],
        "cart": [
            ("shop_cart_001", "http://localhost:8080/checkout/cart/", "Shopping Cart"),
        ],
        "checkout": [
            # Checkout requires items in cart - mark as BLOCKED
            # ("shop_checkout_001", "http://localhost:8080/checkout/", "Checkout"),
        ],
    }
    
    # GitLab tasks
    gitlab_tasks = [
        ("gitlab_001", "http://localhost:8081/", "GitLab Home"),
    ]
    
    # Reddit tasks
    reddit_tasks = [
        ("reddit_001", "http://localhost:8082/", "Reddit Home"),
    ]
    
    # Randomize shopping task selection
    rng = random.Random(FROZEN_SEED)
    
    selected_shopping = []
    for page_type, tasks in shopping_tasks.items():
        # Select 2 tasks from each page type (or all if fewer)
        n_select = min(2, len(tasks))
        selected = rng.sample(tasks, n_select)
        selected_shopping.extend([(t[0], t[1], t[2], "shopping", page_type) for t in selected])
    
    # Add gitlab and reddit tasks
    all_tasks = selected_shopping + [
        (t[0], t[1], t[2], "gitlab", "home") for t in gitlab_tasks
    ] + [
        (t[0], t[1], t[2], "reddit", "home") for t in reddit_tasks
    ]
    
    print(f"Selected {len(all_tasks)} tasks:")
    for task_id, url, name, site, ptype in all_tasks:
        print(f"  {task_id}: {name} ({site}/{ptype})")
    print()
    
    # Launch Playwright
    from playwright.async_api import async_playwright
    
    all_results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for task_id, url, name, site_type, page_type in all_tasks:
            print(f"Task: {task_id} ({site_type}/{page_type})")
            
            # Fresh browser context per task
            context = await browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            result = await measure_task(page, url, task_id, site_type, page_type, OUTPUT_DIR)
            all_results.append(result)
            
            await page.close()
            await context.close()
            
            print()
        
        await browser.close()
    
    # Save all results
    results_path = OUTPUT_DIR / "exp346_raw_results.json"
    with open(results_path, "w") as f:
        json.dump({
        "experiment_id": "EXP-INTEL-34607693437",
        "frozen_seed": FROZEN_SEED,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "frozen_definition": {
            "type": "interactive_with_bbox",
            "roles": sorted(INTERACTIVE_ROLES),
            "viewport": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT, "threshold": INTERSECTION_THRESHOLD}
        },
        "measurements": all_results
    }, f, indent=2)
    
    print(f"Results saved to {results_path}")
    print(f"Results SHA256: {sha256_file(results_path)}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    shopping_results = [r for r in all_results if r.get("site_type") == "shopping" and not r.get("error")]
    if shopping_results:
        viewport_elements = [r["viewport_elements"] for r in shopping_results]
        locatable_elements = [r["locatable_elements"] for r in shopping_results]
        cdp_elements = [r["total_cdp_elements"] for r in shopping_results]
        yield_cdp = [r["yield_cdp"] for r in shopping_results]
        yield_locatable = [r["yield_locatable"] for r in shopping_results]
        
        import statistics
        print(f"Shopping tasks measured: {len(shopping_results)}")
        print(f"Viewport elements: mean={statistics.mean(viewport_elements):.1f}, stdev={statistics.stdev(viewport_elements) if len(viewport_elements) > 1 else 0:.1f}")
        print(f"Locatable elements: mean={statistics.mean(locatable_elements):.1f}, stdev={statistics.stdev(locatable_elements) if len(locatable_elements) > 1 else 0:.1f}")
        print(f"CDP elements: mean={statistics.mean(cdp_elements):.1f}, stdev={statistics.stdev(cdp_elements) if len(cdp_elements) > 1 else 0:.1f}")
        print(f"Yield CDP: mean={statistics.mean(yield_cdp):.4f}, cv={statistics.stdev(yield_cdp)/statistics.mean(yield_cdp) if statistics.mean(yield_cdp) > 0 else 0:.4f}")
        print(f"Yield Locatable: mean={statistics.mean(yield_locatable):.4f}, cv={statistics.stdev(yield_locatable)/statistics.mean(yield_locatable) if statistics.mean(yield_locatable) > 0 else 0:.4f}")
    
    # Non-shopping results
    for r in all_results:
        if r.get("site_type") != "shopping" and not r.get("error"):
            print(f"\n{r['task_id']} ({r['site_type']}): viewport={r['viewport_elements']}, locatable={r['locatable_elements']}, cdp={r['total_cdp_elements']}")
            print(f"  yield_cdp={r['yield_cdp']:.4f}, yield_locatable={r['yield_locatable']:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
