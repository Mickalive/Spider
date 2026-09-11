#!/usr/bin/env python3
"""
EXP-INTEL-34607693437: Frozen Measurement Script (v2 - DOM-based)
Implements fallback definition of locatable_elements:
  Elements with non-null bounding box (width > 0 AND height > 0)
  AND (role is interactive OR has aria-label/aria-describedby OR is within a form)
  
NOTE: CDP Accessibility.getFullAXTree returns only 1 node in headless Chromium shell.
This script uses DOM element counts instead, which are the true element counts.
The CDP accessibility tree limitation is an infrastructure constraint, not a scientific finding.
"""

import asyncio
import hashlib
import json
import os
import random
import statistics
import sys
import time
from typing import Any

# === FROZEN CONSTANTS ===
FROZEN_SEED = 34607693437
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
BBOX_INTERSECTION_THRESHOLD = 0.5

# Interactive roles for fallback locatable definition
INTERACTIVE_ROLES = ["button", "link", "textbox", "checkbox", "radio",
    "combobox", "listbox", "menuitem", "tab", "slider",
    "spinbutton", "searchbox", "switch"]

# Shopping page URLs classified by page type
SHOPPING_URLS = {
    "product_listing": [
        ("electronics.html", "listing_electronics"),
        ("beauty-personal-care.html", "listing_beauty"),
        ("home-kitchen.html", "listing_home_kitchen"),
        ("clothing-shoes-jewelry.html", "listing_clothing"),
        ("sports-outdoors.html", "listing_sports"),
        ("tools-home-improvement.html", "listing_tools"),
    ],
    "detail": [
        ("navitech-black-hard-carry-bag-case-cover-with-shoulder-strap-compatible-with-the-vr-virtual-reality-3d-headsets-including-the-crypto-vr-150-virtual-reality-headset-3d-glasses.html", "detail_vr_bag"),
        ("zosi-h-265-poe-home-security-camera-system-outdoor-indoor-8-channel-5mp-poe-nvr-recorder-4pcs-wired-2mp-1080p-surveillance-bullet-poe-ip-cameras-no-hard-drive-renewed.html", "detail_camera"),
        ("indoor-pet-camera-hd-1080p-no-wifi-security-camera-with-night-vision-no-built-in-baterry.html", "detail_pet_camera"),
        ("rockville-ch103sp-chuchero-car-audio-enclosure-for-2-10-mids-2-3-tweeter.html", "detail_audio"),
        ("150ft-quad-shield-solid-copper-3ghz-rg-6-coaxial-cable-75-ohm-directv-satellite-tv-or-broadband-internet-anti-corrosion-brass-connector-rg6-fittings-assembled-in-usa-by-phat-satellite-intl.html", "detail_cable"),
        ("jsy-foldable-bath-body-brush-portable-massager-brush-with-long-handle-for-wet-dry-brush-bath-body-brushes-color-green.html", "detail_brush"),
    ],
    "cart": [
        ("checkout/cart/", "cart_1"),
    ],
    "checkout": [
        ("checkout/cart/", "checkout_cart_1"),
        ("checkout/cart/", "checkout_cart_2"),
    ],
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


JS_EXTRACT_ELEMENTS = """() => {
    const interactiveRoles = new Set(%s);
    const allElements = document.querySelectorAll('*');
    const viewport = {width: %d, height: %d};
    const threshold = %f;
    
    let total_dom = allElements.length;
    let with_bbox = 0;
    let viewport_elements = 0;
    let locatable_elements = 0;
    let locatable_interactive = 0;
    let locatable_aria = 0;
    let locatable_form = 0;
    let locatable_onclick = 0;
    
    const viewport_sample = [];
    const locatable_sample = [];
    const role_counts = {};
    
    for (const el of allElements) {
        const role = el.getAttribute('role') || el.tagName.toLowerCase();
        role_counts[role] = (role_counts[role] || 0) + 1;
        
        try {
            const rect = el.getBoundingClientRect();
            if (!rect || rect.width <= 0 || rect.height <= 0) continue;
            with_bbox++;
            
            // Viewport intersection
            const ix = Math.max(0, Math.min(rect.right, viewport.width) - Math.max(rect.left, 0));
            const iy = Math.max(0, Math.min(rect.bottom, viewport.height) - Math.max(rect.top, 0));
            const intersectionArea = ix * iy;
            const elemArea = rect.width * rect.height;
            
            if (elemArea > 0 && (intersectionArea / elemArea) >= threshold) {
                viewport_elements++;
                if (viewport_sample.length < 20) {
                    viewport_sample.push({tag: el.tagName, role: role, text: (el.textContent || '').substring(0, 40)});
                }
            }
            
            // Locatable check (fallback definition)
            const isInteractive = interactiveRoles.has(role);
            const hasAriaLabel = !!el.getAttribute('aria-label');
            const hasAriaDescribedby = !!el.getAttribute('aria-describedby');
            const isInForm = !!el.closest('form');
            const hasOnclick = !!el.onclick || !!el.getAttribute('onclick');
            
            if (isInteractive || hasAriaLabel || hasAriaDescribedby || isInForm || hasOnclick) {
                locatable_elements++;
                if (isInteractive) locatable_interactive++;
                if (hasAriaLabel || hasAriaDescribedby) locatable_aria++;
                if (isInForm) locatable_form++;
                if (hasOnclick) locatable_onclick++;
                if (locatable_sample.length < 20) {
                    locatable_sample.push({tag: el.tagName, role: role, ariaLabel: el.getAttribute('aria-label') || ''});
                }
            }
        } catch(e) {}
    }
    
    return {
        total_dom: total_dom,
        with_bbox: with_bbox,
        viewport_elements: viewport_elements,
        locatable_elements: locatable_elements,
        locatable_interactive: locatable_interactive,
        locatable_aria: locatable_aria,
        locatable_form: locatable_form,
        locatable_onclick: locatable_onclick,
        viewport_sample: viewport_sample,
        locatable_sample: locatable_sample,
        role_counts: role_counts,
    };
}""" % (
    json.dumps(INTERACTIVE_ROLES),
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
    BBOX_INTERSECTION_THRESHOLD,
)


async def measure_task(page, url: str, task_name: str, output_dir: str) -> dict:
    """Measure a single task page."""
    result = {
        "task_name": task_name,
        "url": url,
        "success": False,
        "total_dom_elements": 0,
        "elements_with_bbox": 0,
        "viewport_elements": 0,
        "locatable_elements": 0,
        "yield_cdp": 0.0,
        "yield_locatable": 0.0,
        "locatable_interactive": 0,
        "locatable_aria": 0,
        "locatable_form": 0,
        "locatable_onclick": 0,
        "role_counts": {},
        "viewport_sample": [],
        "locatable_sample": [],
        "error": None,
    }
    
    try:
        print(f"  Navigating to {url}...", flush=True)
        response = await page.goto(url, wait_until="networkidle", timeout=30000)
        if response:
            result["http_status"] = response.status
        
        await asyncio.sleep(3)
        
        # Extract all element data via JS
        data = await page.evaluate(JS_EXTRACT_ELEMENTS)
        
        result["total_dom_elements"] = data["total_dom"]
        result["elements_with_bbox"] = data["with_bbox"]
        result["viewport_elements"] = data["viewport_elements"]
        result["locatable_elements"] = data["locatable_elements"]
        result["locatable_interactive"] = data["locatable_interactive"]
        result["locatable_aria"] = data["locatable_aria"]
        result["locatable_form"] = data["locatable_form"]
        result["locatable_onclick"] = data["locatable_onclick"]
        result["role_counts"] = data["role_counts"]
        result["viewport_sample"] = data["viewport_sample"]
        result["locatable_sample"] = data["locatable_sample"]
        
        # Compute yields
        # yield_cdp = viewport_elements / total_dom_elements (DOM-based equivalent)
        if data["total_dom"] > 0:
            result["yield_cdp"] = round(data["viewport_elements"] / data["total_dom"], 6)
        # yield_locatable = viewport_elements / locatable_elements
        if data["locatable_elements"] > 0:
            result["yield_locatable"] = round(data["viewport_elements"] / data["locatable_elements"], 6)
        
        result["success"] = True
        print(f"  OK: dom={data['total_dom']}, bbox={data['with_bbox']}, viewport={data['viewport_elements']}, locatable={data['locatable_elements']}, yield_cdp={result['yield_cdp']:.4f}, yield_loc={result['yield_locatable']:.4f}")
        
    except Exception as e:
        result["error"] = str(e)
        print(f"  ERROR: {e}", flush=True)
    
    return result


async def main():
    output_dir = "/tmp/opencode"
    os.makedirs(output_dir, exist_ok=True)
    
    # === FROZEN TASK SELECTION ===
    rng = random.Random(FROZEN_SEED)
    
    selected_tasks = []
    for page_type in ["product_listing", "detail", "cart", "checkout"]:
        urls = SHOPPING_URLS[page_type]
        n = 2
        selected = rng.sample(urls, min(n, len(urls)))
        for url_tuple in selected:
            selected_tasks.append((page_type, url_tuple[0], url_tuple[1]))
    
    print("Selected tasks:")
    for pt, url, name in selected_tasks:
        print(f"  {pt}: {name}")
    
    all_results = []
    
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for page_type, url, task_name in selected_tasks:
            print(f"\nMeasuring {task_name} ({page_type})...")
            
            context = await browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            )
            page = await context.new_page()
            
            full_url = f"http://localhost:8080/{url}"
            result = await measure_task(page, full_url, task_name, output_dir)
            result["page_type"] = page_type
            
            # Save per-task artifacts
            if result["success"]:
                # Save viewport sample
                vp_path = os.path.join(output_dir, f"viewport_sample_{task_name}.json")
                with open(vp_path, "w") as f:
                    json.dump(result["viewport_sample"], f, indent=2)
                
                # Save locatable sample
                loc_path = os.path.join(output_dir, f"locatable_sample_{task_name}.json")
                with open(loc_path, "w") as f:
                    json.dump(result["locatable_sample"], f, indent=2)
            
            all_results.append(result)
            await context.close()
            
            # Small delay between tasks
            await asyncio.sleep(1)
        
        await browser.close()
    
    # === COMPUTE AGGREGATE STATISTICS ===
    successful = [r for r in all_results if r["success"]]
    
    if not successful:
        print("ERROR: No successful measurements!")
        sys.exit(1)
    
    # Per-page-type statistics
    page_type_stats = {}
    for pt in ["product_listing", "detail", "cart", "checkout"]:
        pt_results = [r for r in successful if r["page_type"] == pt]
        if pt_results:
            yields_cdp = [r["yield_cdp"] for r in pt_results]
            yields_loc = [r["yield_locatable"] for r in pt_results]
            viewport_counts = [r["viewport_elements"] for r in pt_results]
            locatable_counts = [r["locatable_elements"] for r in pt_results]
            dom_counts = [r["total_dom_elements"] for r in pt_results]
            
            page_type_stats[pt] = {
                "count": len(pt_results),
                "mean_yield_cdp": round(statistics.mean(yields_cdp), 6),
                "mean_yield_locatable": round(statistics.mean(yields_loc), 6),
                "mean_viewport_elements": round(statistics.mean(viewport_counts), 2),
                "mean_locatable_elements": round(statistics.mean(locatable_counts), 2),
                "mean_dom_elements": round(statistics.mean(dom_counts), 2),
            }
    
    # Overall statistics
    all_yields_cdp = [r["yield_cdp"] for r in successful]
    all_yields_loc = [r["yield_locatable"] for r in successful]
    all_viewport = [r["viewport_elements"] for r in successful]
    all_locatable = [r["locatable_elements"] for r in successful]
    all_dom = [r["total_dom_elements"] for r in successful]
    
    viewport_set = set(all_viewport)
    
    stats = {
        "total_tasks_measured": len(successful),
        "total_tasks_attempted": len(all_results),
        "successful_tasks": len(successful),
        "yield_cdp_mean": round(statistics.mean(all_yields_cdp), 6),
        "yield_cdp_stdev": round(statistics.stdev(all_yields_cdp), 6) if len(all_yields_cdp) > 1 else 0.0,
        "yield_cdp_cv": round(statistics.stdev(all_yields_cdp) / statistics.mean(all_yields_cdp), 6) if len(all_yields_cdp) > 1 and statistics.mean(all_yields_cdp) > 0 else 0.0,
        "yield_cdp_min": min(all_yields_cdp),
        "yield_cdp_max": max(all_yields_cdp),
        "yield_locatable_mean": round(statistics.mean(all_yields_loc), 6),
        "yield_locatable_stdev": round(statistics.stdev(all_yields_loc), 6) if len(all_yields_loc) > 1 else 0.0,
        "yield_locatable_cv": round(statistics.stdev(all_yields_loc) / statistics.mean(all_yields_loc), 6) if len(all_yields_loc) > 1 and statistics.mean(all_yields_loc) > 0 else 0.0,
        "yield_locatable_min": min(all_yields_loc),
        "yield_locatable_max": max(all_yields_loc),
        "viewport_elements_mean": round(statistics.mean(all_viewport), 2),
        "viewport_elements_stdev": round(statistics.stdev(all_viewport), 4) if len(all_viewport) > 1 else 0.0,
        "viewport_elements_values": all_viewport,
        "viewport_constancy": len(viewport_set) == 1,
        "viewport_unique_values": sorted(viewport_set),
        "locatable_elements_mean": round(statistics.mean(all_locatable), 2),
        "locatable_elements_stdev": round(statistics.stdev(all_locatable), 2) if len(all_locatable) > 1 else 0.0,
        "dom_elements_mean": round(statistics.mean(all_dom), 2),
        "dom_elements_stdev": round(statistics.stdev(all_dom), 2) if len(all_dom) > 1 else 0.0,
        "method1_yield": 0.365,
        "method1_delta_pp": round(abs(statistics.mean(all_yields_loc) - 0.365) * 100, 2),
        "method1_within_15pp": abs(statistics.mean(all_yields_loc) - 0.365) <= 0.15,
        "method1_within_10pp": abs(statistics.mean(all_yields_loc) - 0.365) <= 0.10,
        "page_type_breakdown": page_type_stats,
    }
    
    # Save raw results
    raw_results = {
        "measurements": all_results,
        "statistics": stats,
        "frozen_definition": {
            "type": "functional_fallback",
            "rationale": "Forensic analysis of Method1 derivation (analyze.py) showed 150-element estimate is hand-estimated typical DOM node count (line 70: 'Based on domain knowledge of typical web pages'). Derivation never defines what constitutes an element or locatable element. Functional fallback captures interactive elements an agent can use for inheritance.",
            "definition": "Elements with non-null bounding box (width > 0 AND height > 0) AND (role is interactive OR has aria-label/aria-describedby OR is within a form OR has onclick handler)",
            "interactive_roles": INTERACTIVE_ROLES,
            "maps_to": "Definition 2 (interactive-only)",
            "expected_yield_range": [0.25, 0.45],
        },
        "frozen_seed": FROZEN_SEED,
        "selected_tasks": [(pt, url, name) for pt, url, name in selected_tasks],
        "infrastructure_notes": [
            "CDP Accessibility.getFullAXTree returns only 1 node in headless Chromium shell - DOM-based counting used instead",
            "Checkout page (checkout/) redirects to localhost:7770 (internal port) - checkout/cart/ used as checkout proxy",
        ],
    }
    
    raw_path = os.path.join(output_dir, "exp346_raw_results.json")
    with open(raw_path, "w") as f:
        json.dump(raw_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to {raw_path}")
    print(f"\n=== SUMMARY ===")
    print(f"Tasks measured: {stats['total_tasks_measured']}")
    print(f"Yield CDP (viewport/dom): {stats['yield_cdp_mean']:.4f} (CV={stats['yield_cdp_cv']:.4f})")
    print(f"Yield Locatable (viewport/locatable): {stats['yield_locatable_mean']:.4f} (CV={stats['yield_locatable_cv']:.4f})")
    print(f"Viewport elements: {stats['viewport_elements_mean']:.1f} (stdev={stats['viewport_elements_stdev']:.4f}, values={stats['viewport_unique_values']})")
    print(f"Locatable elements: {stats['locatable_elements_mean']:.1f}")
    print(f"DOM elements: {stats['dom_elements_mean']:.1f}")
    print(f"Method1 delta: {stats['method1_delta_pp']:.2f}pp")
    print(f"Page type breakdown:")
    for pt, s in page_type_stats.items():
        print(f"  {pt}: n={s['count']}, yield_cdp={s['mean_yield_cdp']:.4f}, yield_loc={s['mean_yield_locatable']:.4f}, viewport={s['mean_viewport_elements']:.0f}, locatable={s['mean_locatable_elements']:.0f}, dom={s['mean_dom_elements']:.0f}")
    
    return raw_results


if __name__ == "__main__":
    asyncio.run(main())
