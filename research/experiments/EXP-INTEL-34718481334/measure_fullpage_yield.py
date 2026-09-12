#!/usr/bin/env python3
"""
EXP-INTEL-34718481334: Full-page DOM element enumeration yield measurement.
Frozen spec: use DEF-FALLBACK-INTERACTIVE on entire page DOM (no viewport filtering).
Seed=99 for task selection.
"""

import json
import hashlib
import time
import math
import random
import os
import sys
from datetime import datetime, timezone

# ── Task pool (from WebArena-Verified shopping site on localhost:8080) ──

TASK_POOL = {
    "product_listing": [
        "http://localhost:8080/electronics.html",
        "http://localhost:8080/home-kitchen.html",
        "http://localhost:8080/sports-outdoors.html",
        "http://localhost:8080/tools-home-improvement.html",
        "http://localhost:8080/clothing-shoes-jewelry.html",
    ],
    "detail": [
        "http://localhost:8080/zosi-h-265-poe-home-security-camera-system-outdoor-indoor-8-channel-5mp-poe-nvr-recorder-4pcs-wired-2mp-1080p-surveillance-bullet-poe-ip-cameras-no-hard-drive-renewed.html",
        "http://localhost:8080/navitech-black-hard-carry-bag-case-cover-with-shoulder-strap-compatible-with-the-vr-virtual-reality-3d-headsets-including-the-crypto-vr-150-virtual-reality-headset-3d-glasses.html",
        "http://localhost:8080/intel-nuc-kit-nuc6i7kyk-mini-pc-no-power-cord.html",
        "http://localhost:8080/indoor-pet-camera-hd-1080p-no-wifi-security-camera-with-night-vision-no-built-in-baterry.html",
        "http://localhost:8080/150ft-quad-shield-solid-copper-3ghz-rg-6-coaxial-cable-75-ohm-directv-satellite-tv-or-broadband-internet-anti-corrosion-brass-connector-rg6-fittings-assembled-in-usa-by-phat-satellite-intl.html",
    ],
    "cart": [
        "http://localhost:8080/checkout/cart/",
    ],
    "checkout": [
        "http://localhost:8080/checkout/",
        "http://localhost:8080/checkout/cart/",
    ],
}

# Selection counts per type per frozen spec
SELECTION = {
    "product_listing": 3,
    "detail": 3,
    "cart": 2,
    "checkout": 2,
}

SEED = 99

# ── Frozen DEF-FALLBACK-INTERACTIVE definition (from parent) ──

INTERACTIVE_ROLES = {
    'button', 'link', 'textbox', 'checkbox', 'radio',
    'combobox', 'listbox', 'menuitem', 'tab', 'slider',
    'spinbutton', 'searchbox', 'switch'
}

# ── DOM enumeration JavaScript ──

DOM_ENUM_JS = """
() => {
    // Total DOM elements
    const totalDom = document.querySelectorAll('*').length;
    
    // Elements with bounding box (width > 0 && height > 0)
    const allElements = [...document.querySelectorAll('*')];
    const elementsWithBbox = allElements.filter(el => {
        const rect = el.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
    }).length;
    
    // Interactive elements (DEF-FALLBACK-INTERACTIVE applied to full page)
    const interactiveRoles = new Set(['button','link','textbox','checkbox','radio','combobox','listbox','menuitem','tab','slider','spinbutton','searchbox','switch']);
    const locatableElements = allElements.filter(el => {
        const rect = el.getBoundingClientRect();
        const hasBbox = rect.width > 0 && rect.height > 0;
        if (!hasBbox) return false;
        const role = el.getAttribute('role') || el.tagName.toLowerCase();
        if (interactiveRoles.has(role)) return true;
        if (el.onclick || el.onsubmit) return true;
        if (el.closest('form')) return true;
        if (el.getAttribute('aria-label') || el.getAttribute('aria-describedby')) return true;
        return false;
    }).length;
    
    // Viewport elements (for cross-denominator comparison)
    // Viewport rect: (0, 0, 1280, 720)
    const VP_W = 1280, VP_H = 720;
    const viewportElements = allElements.filter(el => {
        const rect = el.getBoundingClientRect();
        if (rect.width <= 0 || rect.height <= 0) return false;
        // Intersection with viewport (0,0,1280,720)
        const ix = Math.max(0, Math.min(rect.right, VP_W) - Math.max(rect.left, 0));
        const iy = Math.max(0, Math.min(rect.bottom, VP_H) - Math.max(rect.top, 0));
        const intersection = ix * iy;
        const area = rect.width * rect.height;
        return (intersection / area) > 0.5;
    }).length;
    
    return JSON.stringify({totalDom, elementsWithBbox, locatableElements, viewportElements});
}
"""


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_bytes(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def select_tasks(seed):
    """Select tasks using frozen seed=99, stratified by page type."""
    rng = random.Random(seed)
    selected = []
    for page_type, count in SELECTION.items():
        pool = TASK_POOL[page_type]
        # Sample without replacement
        chosen = rng.sample(pool, min(count, len(pool)))
        for url in chosen:
            slug = url.split('/')[-1].replace('.html', '')[:40] if url.endswith('.html') else url.split('/')[-1][:40]
            task_name = f"{page_type}_{slug}"
            selected.append({
                "page_type": page_type,
                "url": url,
                "task_name": task_name,
            })
    return selected


def measure_task(page, task):
    """Measure a single task: navigate, enumerate DOM, snapshot accessibility."""
    url = task["url"]
    task_name = task["task_name"]
    page_type = task["page_type"]
    
    result = {
        "task_name": task_name,
        "url": url,
        "page_type": page_type,
        "success": False,
        "error": None,
        "http_status": None,
    }
    
    try:
        # Navigate
        response = page.goto(url, wait_until="networkidle", timeout=30000)
        result["http_status"] = response.status if response else None
        
        # Handle redirect for checkout
        current_url = page.url
        if current_url != url:
            result["redirected_to"] = current_url
            if "7770" in current_url:
                result["checkout_proxy"] = True
                result["page_type"] = "cart"  # checkout proxies to cart
        
        # Wait a bit for dynamic content
        time.sleep(1)
        
        # Full-page DOM enumeration
        dom_data_str = page.evaluate(DOM_ENUM_JS)
        dom_data = json.loads(dom_data_str)
        
        result["total_dom_elements"] = dom_data["totalDom"]
        result["elements_with_bbox"] = dom_data["elementsWithBbox"]
        result["locatable_elements"] = dom_data["locatableElements"]
        result["viewport_elements"] = dom_data["viewportElements"]
        
        # Yield calculations
        if dom_data["totalDom"] > 0:
            result["interactive_fraction"] = dom_data["locatableElements"] / dom_data["totalDom"]
            result["cdp_yield"] = dom_data["viewportElements"] / dom_data["totalDom"]
        else:
            result["interactive_fraction"] = 0
            result["cdp_yield"] = 0
        
        # Accessibility snapshot (secondary)
        try:
            a11y_snapshot = page.accessibility.snapshot()
            if a11y_snapshot:
                node_count = _count_a11y_nodes(a11y_snapshot)
                result["accessibility_snapshot_nodes"] = node_count
            else:
                result["accessibility_snapshot_nodes"] = 0
        except Exception as e:
            result["accessibility_snapshot_nodes"] = 0
            result["a11y_error"] = str(e)
        
        result["success"] = True
        result["error"] = None
        
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
    
    return result


def _count_a11y_nodes(node, count=0):
    """Count nodes in accessibility tree snapshot."""
    count += 1
    for child in node.get("children", []):
        count = _count_a11y_nodes(child, count)
    return count


def compute_statistics(measurements):
    """Compute derived metrics from raw measurements."""
    successful = [m for m in measurements if m.get("success", False)]
    n = len(successful)
    
    stats = {
        "total_tasks_attempted": len(measurements),
        "total_tasks_measured": n,
        "successful_tasks": n,
    }
    
    if n == 0:
        return stats
    
    # Basic stats for each metric
    for metric in ["total_dom_elements", "locatable_elements", "viewport_elements", 
                    "interactive_fraction", "cdp_yield"]:
        values = [m[metric] for m in successful if metric in m]
        if values:
            mean = sum(values) / len(values)
            stdev = math.sqrt(sum((v - mean) ** 2 for v in values) / len(values)) if len(values) > 1 else 0
            cv = stdev / mean if mean != 0 else 0
            stats[f"{metric}_mean"] = round(mean, 6)
            stats[f"{metric}_stdev"] = round(stdev, 6)
            stats[f"{metric}_cv"] = round(cv, 6)
            stats[f"{metric}_min"] = round(min(values), 6)
            stats[f"{metric}_max"] = round(max(values), 6)
            stats[f"{metric}_values"] = [round(v, 6) for v in values]
    
    # Page type breakdown
    type_breakdown = {}
    for m in successful:
        pt = m["page_type"]
        if pt not in type_breakdown:
            type_breakdown[pt] = {"count": 0, "if_values": [], "td_values": [], "loc_values": []}
        type_breakdown[pt]["count"] += 1
        type_breakdown[pt]["if_values"].append(m.get("interactive_fraction", 0))
        type_breakdown[pt]["td_values"].append(m.get("total_dom_elements", 0))
        type_breakdown[pt]["loc_values"].append(m.get("locatable_elements", 0))
    
    for pt, data in type_breakdown.items():
        if data["count"] > 0:
            data["mean_interactive_fraction"] = round(sum(data["if_values"]) / len(data["if_values"]), 6)
            if data["count"] > 1:
                mean_if = data["mean_interactive_fraction"]
                data["if_stdev"] = round(math.sqrt(sum((v - mean_if) ** 2 for v in data["if_values"]) / len(data["if_values"])), 6)
                data["if_cv"] = round(data["if_stdev"] / mean_if, 6) if mean_if > 0 else 0
            else:
                data["if_stdev"] = 0
                data["if_cv"] = 0
            data["mean_total_dom"] = round(sum(data["td_values"]) / len(data["td_values"]), 1)
            data["mean_locatable"] = round(sum(data["loc_values"]) / len(data["loc_values"]), 1)
        # Remove raw arrays
        del data["if_values"]
        del data["td_values"]
        del data["loc_values"]
    
    stats["page_type_breakdown"] = type_breakdown
    
    # Between-type vs within-type variance
    type_means = [d["mean_interactive_fraction"] for d in type_breakdown.values() if d["count"] > 0]
    if len(type_means) > 1:
        grand_mean = sum(type_means) / len(type_means)
        between_type_var = sum((m - grand_mean) ** 2 for m in type_means) / len(type_means)
        
        within_type_variances = []
        for d in type_breakdown.values():
            if d["count"] > 1:
                within_type_variances.append(d["if_stdev"] ** 2)
        within_type_var = sum(within_type_variances) / len(within_type_variances) if within_type_variances else 0
        
        stats["between_type_variance"] = round(between_type_var, 8)
        stats["within_type_variance"] = round(within_type_var, 8)
        stats["discrimination_ratio"] = round(between_type_var / within_type_var, 4) if within_type_var > 0 else float('inf')
    else:
        stats["between_type_variance"] = 0
        stats["within_type_variance"] = 0
        stats["discrimination_ratio"] = 0
    
    # Within-type CVs for types with n >= 2
    within_type_cvs = {}
    for pt, data in type_breakdown.items():
        if data["count"] >= 2:
            within_type_cvs[pt] = data["if_cv"]
    stats["within_type_cvs"] = within_type_cvs
    
    return stats


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting EXP-INTEL-34718481334 measurement")
    
    # Select tasks
    tasks = select_tasks(SEED)
    print(f"Selected {len(tasks)} tasks:")
    for t in tasks:
        print(f"  {t['page_type']}: {t['task_name']}")
    
    measurements = []
    
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for task in tasks:
            print(f"\n--- Measuring: {task['task_name']} ({task['url']}) ---")
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            
            result = measure_task(page, task)
            measurements.append(result)
            
            if result["success"]:
                print(f"  OK: total_dom={result['total_dom_elements']}, "
                      f"locatable={result['locatable_elements']}, "
                      f"viewport={result['viewport_elements']}, "
                      f"interactive_fraction={result['interactive_fraction']:.4f}")
            else:
                print(f"  FAIL: {result['error']}")
            
            context.close()
            time.sleep(0.5)
        
        browser.close()
    
    # Compute statistics
    stats = compute_statistics(measurements)
    
    # Save raw results
    raw_output = {
        "experiment_id": "EXP-INTEL-34718481334",
        "measurements": measurements,
        "statistics": stats,
        "frozen_definition": {
            "type": "functional_fallback",
            "definition": "Elements with non-null bounding box (width > 0 AND height > 0) AND (role in interactive_roles OR onclick/onsubmit handler OR form membership OR aria-label/aria-describedby)",
            "interactive_roles": sorted(INTERACTIVE_ROLES),
            "maps_to": "Definition 2 (interactive-only)",
        },
        "docker_image_digest": "sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb",
        "frozen_seed": SEED,
        "selected_tasks": [[t["page_type"], t["url"].split("/")[-1], t["task_name"]] for t in tasks],
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "exp347_raw_results.json")
    with open(output_path, 'w') as f:
        json.dump(raw_output, f, indent=2)
    
    print(f"\n[{datetime.now(timezone.utc).isoformat()}] Raw results saved to {output_path}")
    print(f"Tasks measured: {stats['total_tasks_measured']}/{stats['total_tasks_attempted']}")
    
    return raw_output


if __name__ == "__main__":
    main()
