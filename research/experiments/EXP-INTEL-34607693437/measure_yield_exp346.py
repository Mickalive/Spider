#!/usr/bin/env python3
"""
EXP-INTEL-34607693437 — Frozen measurement script (v2)
Measures yield_locatable under frozen FUNC-INTERACTIVE-V2 definition across
randomized shopping page types including checkout.

Uses CDP for total node count, Playwright locators for viewport/locatable counts.
"""

import asyncio
import hashlib
import json
import os
import random
import statistics
import sys
import time
from pathlib import Path

# Output directory
OUTPUT_DIR = Path("/home/runner/work/Spider/Spider/research/experiments/EXP-INTEL-34607693437/artifacts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Frozen seed for reproducibility
FROZEN_SEED = 34607693437

# Viewport dimensions
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720

# Frozen definition: interactive element roles
INTERACTIVE_ROLES = {
    "button", "link", "textbox", "checkbox", "radio", "combobox",
    "listbox", "menuitem", "tab", "slider", "spinbutton", "searchbox", "switch",
    "a", "input", "select", "textarea"
}

# Shopping site pages
SHOPPING_PAGES = {
    "product-listing": [
        {"url": "http://localhost:8080/electronics.html", "label": "electronics"},
        {"url": "http://localhost:8080/beauty-personal-care.html", "label": "beauty"},
        {"url": "http://localhost:8080/home-kitchen.html", "label": "home-kitchen"},
        {"url": "http://localhost:8080/books.html", "label": "books"},
        {"url": "http://localhost:8080/shoes.html", "label": "shoes"},
        {"url": "http://localhost:8080/jewelry.html", "label": "jewelry"},
    ],
    "detail": [
        {"url": "http://localhost:8080/headphones/17.html", "label": "headphones"},
        {"url": "http://localhost:8080/cameras/15.html", "label": "cameras"},
        {"url": "http://localhost:8080/cells/12.html", "label": "cells"},
        {"url": "http://localhost:8080/watches/19.html", "label": "watches"},
    ],
    "cart": [
        {"url": "http://localhost:8080/checkout/cart/", "label": "cart"},
    ],
    "checkout": [
        # Checkout pages require items in cart; use placeholder pages
        {"url": "http://localhost:8080/customer/account/login/", "label": "login"},
        {"url": "http://localhost:8080/catalogsearch/result/?q=phone", "label": "search-phone"},
    ],
}


def sha256_of_file(filepath):
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


async def measure_task(page, task_info, task_idx):
    """Measure a single task using Playwright locators and CDP."""
    url = task_info["url"]
    label = task_info["label"]
    
    print(f"  [{task_idx}] Measuring: {label} ({url})")
    
    try:
        # Navigate
        resp = await page.goto(url, wait_until="networkidle", timeout=60000)
        if resp and resp.status >= 400:
            print(f"    WARNING: HTTP {resp.status}")
        await asyncio.sleep(2)
        
        viewport_w = VIEWPORT_WIDTH
        viewport_h = VIEWPORT_HEIGHT
        
        # === CDP: total node count ===
        cdp = await page.context.new_cdp_session(page)
        await cdp.send("Accessibility.enable")
        result = await cdp.send("Accessibility.getFullAXTree")
        cdp_nodes = result.get("nodes", [])
        total_cdp = len(cdp_nodes)
        await cdp.detach()
        
        # === Playwright: count elements using JavaScript ===
        # This gives us accurate counts with bounding boxes
        counts = await page.evaluate("""() => {
            const vw = window.innerWidth || 1280;
            const vh = window.innerHeight || 720;
            
            // Get all elements
            const allElements = document.querySelectorAll('*');
            let total_elements = allElements.length;
            
            // Viewport elements: elements with bbox intersection > 50%
            let viewport_count = 0;
            let viewport_samples = [];
            let all_bboxes = [];
            
            for (const el of allElements) {
                const rect = el.getBoundingClientRect();
                if (rect.width <= 0 || rect.height <= 0) continue;
                
                // Compute intersection
                const ix1 = Math.max(rect.left, 0);
                const iy1 = Math.max(rect.top, 0);
                const ix2 = Math.min(rect.right, vw);
                const iy2 = Math.min(rect.bottom, vh);
                const intersection = Math.max(0, ix2 - ix1) * Math.max(0, iy2 - iy1);
                const element_area = rect.width * rect.height;
                
                if (element_area > 0 && (intersection / element_area) >= 0.5) {
                    viewport_count++;
                    if (viewport_samples.length < 20) {
                        viewport_samples.push({
                            tag: el.tagName.toLowerCase(),
                            role: el.getAttribute('role') || '',
                            id: el.id || '',
                            classes: (el.className || '').toString().substring(0, 80),
                            ariaLabel: el.getAttribute('aria-label') || '',
                            bbox: {x: Math.round(rect.left), y: Math.round(rect.top), 
                                    w: Math.round(rect.width), h: Math.round(rect.height)}
                        });
                    }
                }
            }
            
            // Locatable elements: frozen FUNC-INTERACTIVE-V2 definition
            // Elements with non-null bbox (w>0, h>0) AND:
            //   role in interactive set OR has onclick/onsubmit OR is in form OR has aria-label/aria-describedby
            const INTERACTIVE_ROLES = new Set([
                'button', 'link', 'textbox', 'checkbox', 'radio', 'combobox',
                'listbox', 'menuitem', 'tab', 'slider', 'spinbutton', 'searchbox',
                'switch', 'a', 'input', 'select', 'textarea'
            ]);
            
            let locatable_count = 0;
            let locatable_samples = [];
            
            for (const el of allElements) {
                const rect = el.getBoundingClientRect();
                if (rect.width <= 0 || rect.height <= 0) continue;
                
                let is_locatable = false;
                
                // Check role
                const role = (el.getAttribute('role') || '').toLowerCase();
                const tag = el.tagName.toLowerCase();
                
                if (INTERACTIVE_ROLES.has(role) || INTERACTIVE_ROLES.has(tag)) {
                    is_locatable = true;
                }
                
                // Check onclick/onsubmit handler
                if (!is_locatable && (el.onclick || el.onsubmit || 
                    el.getAttribute('onclick') || el.getAttribute('onsubmit'))) {
                    is_locatable = true;
                }
                
                // Check if within a form element
                if (!is_locatable && el.closest('form')) {
                    is_locatable = true;
                }
                
                // Check aria-label or aria-describedby
                if (!is_locatable && (
                    el.getAttribute('aria-label') || 
                    el.getAttribute('aria-describedby') ||
                    el.getAttribute('aria-labelledby')
                )) {
                    is_locatable = true;
                }
                
                // Check for contenteditable
                if (!is_locatable && el.getAttribute('contenteditable') === 'true') {
                    is_locatable = true;
                }
                
                if (is_locatable) {
                    locatable_count++;
                    if (locatable_samples.length < 20) {
                        locatable_samples.push({
                            tag: tag,
                            role: role,
                            id: el.id || '',
                            ariaLabel: el.getAttribute('aria-label') || '',
                            bbox: {x: Math.round(rect.left), y: Math.round(rect.top),
                                    w: Math.round(rect.width), h: Math.round(rect.height)}
                        });
                    }
                }
            }
            
            return {
                total_elements: total_elements,
                viewport_count: viewport_count,
                locatable_count: locatable_count,
                viewport_samples: viewport_samples,
                locatable_samples: locatable_samples,
                viewport_width: vw,
                viewport_height: vh
            };
        }""")
        
        total_elements = counts["total_elements"]
        viewport_elements = counts["viewport_count"]
        locatable_elements = counts["locatable_count"]
        
        # Yield calculations
        yield_cdp = viewport_elements / total_cdp if total_cdp > 0 else 0
        yield_locatable = viewport_elements / locatable_elements if locatable_elements > 0 else 0
        yield_elements = viewport_elements / total_elements if total_elements > 0 else 0
        
        # Method1 comparison
        method1_yield = 0.365
        method1_delta = abs(yield_locatable - method1_yield) * 100
        
        # Heuristic comparison
        heuristic_yield = 0.65
        heuristic_delta = abs(yield_locatable - heuristic_yield) * 100
        
        result = {
            "task_idx": task_idx,
            "url": url,
            "label": label,
            "page_type": task_info.get("page_type", "unknown"),
            "viewport_width": counts["viewport_width"],
            "viewport_height": counts["viewport_height"],
            "total_cdp_elements": total_cdp,
            "total_elements": total_elements,
            "viewport_elements": viewport_elements,
            "locatable_elements": locatable_elements,
            "yield_cdp": round(yield_cdp, 6),
            "yield_locatable": round(yield_locatable, 6),
            "yield_elements": round(yield_elements, 6),
            "method1_delta_pp": round(method1_delta, 2),
            "heuristic_delta_pp": round(heuristic_delta, 2),
            "viewport_sample": counts["viewport_samples"],
            "locatable_sample": counts["locatable_samples"],
        }
        
        # Save viewport sample
        sample_path = OUTPUT_DIR / f"viewport_sample_{label}.json"
        with open(sample_path, "w") as f:
            json.dump(counts["viewport_samples"], f, indent=2)
        
        # Save raw CDP tree (compact)
        raw_path = OUTPUT_DIR / f"raw_cdp_tree_{label}.json"
        with open(raw_path, "w") as f:
            # Save just node IDs and roles for size
            compact = [{"id": n.get("nodeId"), "role": n.get("role"), "name": str(n.get("name", ""))[:50]} 
                      for n in cdp_nodes[:200]]  # First 200 nodes
            json.dump(compact, f, indent=2, default=str)
        result["raw_cdp_path"] = str(raw_path)
        result["raw_cdp_sha256"] = sha256_of_file(raw_path)
        
        print(f"    total={total_elements}, cdp={total_cdp}, viewport={viewport_elements}, "
              f"locatable={locatable_elements}, yield_cdp={yield_cdp:.4f}, yield_loc={yield_locatable:.4f}")
        
        return result
        
    except Exception as e:
        import traceback
        print(f"    ERROR: {e}")
        traceback.print_exc()
        return {
            "task_idx": task_idx,
            "url": url,
            "label": label,
            "page_type": task_info.get("page_type", "unknown"),
            "error": str(e),
            "total_cdp_elements": 0,
            "total_elements": 0,
            "viewport_elements": 0,
            "locatable_elements": 0,
            "yield_cdp": 0,
            "yield_locatable": 0,
            "yield_elements": 0,
        }


async def measure_external_task(page, url, label, site_type, task_idx):
    """Measure a GitLab or Reddit task."""
    print(f"  [{task_idx}] Measuring {site_type}: {label} ({url})")
    
    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(2)
        
        cdp = await page.context.new_cdp_session(page)
        await cdp.send("Accessibility.enable")
        result = await cdp.send("Accessibility.getFullAXTree")
        cdp_nodes = result.get("nodes", [])
        total_cdp = len(cdp_nodes)
        await cdp.detach()
        
        counts = await page.evaluate("""() => {
            const vw = window.innerWidth || 1280;
            const vh = window.innerHeight || 720;
            const allElements = document.querySelectorAll('*');
            let total_elements = allElements.length;
            let viewport_count = 0;
            let viewport_samples = [];
            
            for (const el of allElements) {
                const rect = el.getBoundingClientRect();
                if (rect.width <= 0 || rect.height <= 0) continue;
                const ix1 = Math.max(rect.left, 0);
                const iy1 = Math.max(rect.top, 0);
                const ix2 = Math.min(rect.right, vw);
                const iy2 = Math.min(rect.bottom, vh);
                const intersection = Math.max(0, ix2 - ix1) * Math.max(0, iy2 - iy1);
                const area = rect.width * rect.height;
                if (area > 0 && (intersection / area) >= 0.5) {
                    viewport_count++;
                    if (viewport_samples.length < 20) {
                        viewport_samples.push({
                            tag: el.tagName.toLowerCase(),
                            role: el.getAttribute('role') || '',
                            bbox: {x: Math.round(rect.left), y: Math.round(rect.top),
                                    w: Math.round(rect.width), h: Math.round(rect.height)}
                        });
                    }
                }
            }
            
            const INTERACTIVE_ROLES = new Set([
                'button', 'link', 'textbox', 'checkbox', 'radio', 'combobox',
                'listbox', 'menuitem', 'tab', 'slider', 'spinbutton', 'searchbox',
                'switch', 'a', 'input', 'select', 'textarea'
            ]);
            
            let locatable_count = 0;
            for (const el of allElements) {
                const rect = el.getBoundingClientRect();
                if (rect.width <= 0 || rect.height <= 0) continue;
                const role = (el.getAttribute('role') || '').toLowerCase();
                const tag = el.tagName.toLowerCase();
                if (INTERACTIVE_ROLES.has(role) || INTERACTIVE_ROLES.has(tag) ||
                    el.onclick || el.onsubmit || el.getAttribute('onclick') || el.getAttribute('onsubmit') ||
                    el.closest('form') || el.getAttribute('aria-label') || el.getAttribute('aria-describedby') ||
                    el.getAttribute('contenteditable') === 'true') {
                    locatable_count++;
                }
            }
            
            return {
                total_elements, viewport_count, locatable_count, viewport_samples,
                viewport_width: vw, viewport_height: vh
            };
        }""")
        
        viewport_elements = counts["viewport_count"]
        locatable_elements = counts["locatable_count"]
        total_elements = counts["total_elements"]
        
        yield_cdp = viewport_elements / total_cdp if total_cdp > 0 else 0
        yield_locatable = viewport_elements / locatable_elements if locatable_elements > 0 else 0
        
        result = {
            "task_idx": task_idx,
            "url": url,
            "label": label,
            "page_type": site_type,
            "site_type": site_type,
            "total_cdp_elements": total_cdp,
            "total_elements": total_elements,
            "viewport_elements": viewport_elements,
            "locatable_elements": locatable_elements,
            "yield_cdp": round(yield_cdp, 6),
            "yield_locatable": round(yield_locatable, 6),
            "viewport_sample": counts["viewport_samples"],
        }
        
        sample_path = OUTPUT_DIR / f"viewport_sample_{site_type}_{label}.json"
        with open(sample_path, "w") as f:
            json.dump(counts["viewport_samples"], f, indent=2)
        
        print(f"    total={total_elements}, cdp={total_cdp}, viewport={viewport_elements}, "
              f"locatable={locatable_elements}, yield_cdp={yield_cdp:.4f}, yield_loc={yield_locatable:.4f}")
        
        return result
        
    except Exception as e:
        import traceback
        print(f"    ERROR: {e}")
        traceback.print_exc()
        return {
            "task_idx": task_idx, "url": url, "label": label,
            "page_type": site_type, "site_type": site_type,
            "error": str(e), "total_cdp_elements": 0, "total_elements": 0,
            "viewport_elements": 0, "locatable_elements": 0,
            "yield_cdp": 0, "yield_locatable": 0,
        }


def randomize_tasks(seed):
    """Randomize task selection from SHOPPING_PAGES, 2 per page type."""
    rng = random.Random(seed)
    selected = []
    for page_type, pages in SHOPPING_PAGES.items():
        n = min(2, len(pages))
        chosen = rng.sample(pages, n)
        for c in chosen:
            c["page_type"] = page_type
        selected.extend(chosen)
    rng.shuffle(selected)
    return selected


async def main():
    from playwright.async_api import async_playwright
    
    print("=" * 70)
    print("EXP-INTEL-34607693437 — Yield Measurement (Frozen FUNC-INTERACTIVE-V2)")
    print("=" * 70)
    
    shopping_tasks = randomize_tasks(FROZEN_SEED)
    print(f"\nSelected {len(shopping_tasks)} shopping tasks (seed={FROZEN_SEED}):")
    for i, t in enumerate(shopping_tasks):
        print(f"  {i}: [{t['page_type']}] {t['label']} -> {t['url']}")
    
    all_results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        # Shopping tasks - fresh context per task
        print("\n--- Shopping Tasks ---")
        for i, task in enumerate(shopping_tasks):
            context = await browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            result = await measure_task(page, task, i)
            result["site_type"] = "shopping"
            all_results.append(result)
            await context.close()
        
        # GitLab - fresh context
        print("\n--- GitLab Tasks ---")
        context = await browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        result = await measure_external_task(
            page, "http://localhost:8888/users/sign_in", "gitlab-login", "gitlab", len(shopping_tasks))
        all_results.append(result)
        await context.close()
        
        # Reddit - fresh context
        print("\n--- Reddit Tasks ---")
        context = await browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        result = await measure_external_task(
            page, "http://localhost:9999/", "reddit-home", "reddit", len(shopping_tasks) + 1)
        all_results.append(result)
        result2 = await measure_external_task(
            page, "http://localhost:9999/f/random", "reddit-random-sub", "reddit", len(shopping_tasks) + 2)
        all_results.append(result2)
        await context.close()
        
        await browser.close()
    
    # Save all results
    raw_results_path = OUTPUT_DIR / "exp346_raw_results.json"
    with open(raw_results_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\n\nRaw results saved to {raw_results_path}")
    print(f"SHA256: {sha256_of_file(raw_results_path)}")
    
    return all_results


if __name__ == "__main__":
    results = asyncio.run(main())
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    shopping_results = [r for r in results if r.get("site_type") == "shopping" and "error" not in r]
    if shopping_results:
        yields_cdp = [r["yield_cdp"] for r in shopping_results]
        yields_loc = [r["yield_locatable"] for r in shopping_results]
        vp_counts = [r["viewport_elements"] for r in shopping_results]
        loc_counts = [r["locatable_elements"] for r in shopping_results]
        cdp_counts = [r["total_cdp_elements"] for r in shopping_results]
        
        print(f"\nShopping tasks measured: {len(shopping_results)}")
        print(f"  yield_cdp: mean={statistics.mean(yields_cdp):.4f}, stdev={statistics.stdev(yields_cdp) if len(yields_cdp) > 1 else 0:.4f}")
        print(f"  yield_locatable: mean={statistics.mean(yields_loc):.4f}, stdev={statistics.stdev(yields_loc) if len(yields_loc) > 1 else 0:.4f}")
        print(f"  viewport_elements: {vp_counts}")
        print(f"  locatable_elements: {loc_counts}")
        print(f"  cdp_elements: {cdp_counts}")
        
        if statistics.mean(yields_loc) > 0 and len(yields_loc) > 1:
            cv = statistics.stdev(yields_loc) / statistics.mean(yields_loc)
            print(f"  yield_locatable_cv: {cv:.4f}")
        
        # Page type breakdown
        page_types = {}
        for r in shopping_results:
            pt = r.get("page_type", "unknown")
            if pt not in page_types:
                page_types[pt] = []
            page_types[pt].append(r)
        
        print("\n  Page type breakdown:")
        for pt, tasks in sorted(page_types.items()):
            locs = [t["yield_locatable"] for t in tasks]
            vps = [t["viewport_elements"] for t in tasks]
            print(f"    {pt} (n={len(tasks)}): yield_loc={statistics.mean(locs):.4f}, viewport={vps}")
    
    external_results = [r for r in results if r.get("site_type") in ("gitlab", "reddit") and "error" not in r]
    if external_results:
        print(f"\nExternal site tasks measured: {len(external_results)}")
        for r in external_results:
            print(f"  [{r['site_type']}] {r['label']}: viewport={r['viewport_elements']}, "
                  f"locatable={r['locatable_elements']}, yield_cdp={r['yield_cdp']:.4f}, "
                  f"yield_loc={r['yield_locatable']:.4f}")
    
    errors = [r for r in results if "error" in r]
    if errors:
        print(f"\nErrors: {len(errors)}")
        for r in errors:
            print(f"  {r['label']}: {r['error'][:100]}")
