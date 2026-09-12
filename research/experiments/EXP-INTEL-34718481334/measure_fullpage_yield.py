#!/usr/bin/env python3
"""
EXP-INTEL-34718481334 Frozen Measurement Script
Measures full-page interactive fraction (locatable/total_dom) using frozen DEF-FALLBACK-INTERACTIVE.
No viewport filtering. Uses DOM queries via page.evaluate().
"""

import asyncio
import json
import hashlib
import os
import random
import statistics
from datetime import datetime, timezone
from pathlib import Path

# Frozen constants
EXPERIMENT_ID = "EXP-INTEL-34718481334"
FROZEN_SEED = 99
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
INTERSECTION_THRESHOLD = 0.5

# Frozen definition: DEF-FALLBACK-INTERACTIVE
# Elements with non-null bounding box (width > 0 AND height > 0) AND
# (role in interactive_roles OR onclick/onsubmit handler OR within form OR aria-label/aria-describedby)
INTERACTIVE_ROLES = {
    "button", "link", "textbox", "checkbox", "radio",
    "combobox", "listbox", "menuitem", "tab", "slider",
    "spinbutton", "searchbox", "switch"
}

# Docker image info
DOCKER_IMAGE = "am1n3e/webarena-verified-shopping:latest"
DOCKER_DIGEST = "sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb"

# Output directory
OUTPUT_DIR = Path(__file__).parent

# JavaScript for full-page DOM measurement (no viewport filtering)
MEASURE_JS = """
() => {
    const allElements = document.querySelectorAll('*');
    let totalDom = 0;
    let elementsWithBbox = 0;
    let locatableElements = 0;
    let viewportElements = 0;
    
    const locatableSample = [];
    const viewportSample = [];
    
    const interactiveRoles = new Set([
        'button','link','textbox','checkbox','radio',
        'combobox','listbox','menuitem','tab','slider',
        'spinbutton','searchbox','switch'
    ]);
    
    const viewportRect = {x: 0, y: 0, width: 1280, height: 720};
    
    for (const el of allElements) {
        totalDom++;
        const rect = el.getBoundingClientRect();
        const hasBbox = rect.width > 0 && rect.height > 0;
        
        if (hasBbox) {
            elementsWithBbox++;
        }
        
        // Full-page locatable: apply DEF-FALLBACK-INTERACTIVE to entire DOM
        if (hasBbox) {
            const role = (el.getAttribute('role') || el.tagName.toLowerCase());
            let isInteractive = interactiveRoles.has(role);
            
            if (!isInteractive) {
                const hasOnclick = el.onclick !== null || el.hasAttribute('onclick');
                const hasOnsubmit = el.onsubmit !== null || el.hasAttribute('onsubmit');
                const inForm = el.closest('form') !== null;
                const ariaLabel = (el.getAttribute('aria-label') || '').trim();
                const ariaDescribedby = (el.getAttribute('aria-describedby') || '').trim();
                
                if (hasOnclick || hasOnsubmit || inForm || ariaLabel || ariaDescribedby) {
                    isInteractive = true;
                }
            }
            
            if (isInteractive) {
                locatableElements++;
                
                if (locatableSample.length < 20) {
                    locatableSample.push({
                        tag: el.tagName,
                        role: el.getAttribute('role') || el.tagName.toLowerCase(),
                        ariaLabel: (el.getAttribute('aria-label') || '').substring(0, 100),
                        inForm: el.closest('form') !== null,
                        x: rect.x, y: rect.y, w: rect.width, h: rect.height
                    });
                }
                
                // Viewport check (for cross-denominator comparison)
                const x1 = Math.max(rect.x, 0);
                const y1 = Math.max(rect.y, 0);
                const x2 = Math.min(rect.x + rect.width, viewportRect.width);
                const y2 = Math.min(rect.y + rect.height, viewportRect.height);
                if (x1 < x2 && y1 < y2) {
                    const intersectionArea = (x2 - x1) * (y2 - y1);
                    const boxArea = rect.width * rect.height;
                    if (boxArea > 0 && (intersectionArea / boxArea) > 0.5) {
                        viewportElements++;
                        if (viewportSample.length < 20) {
                            viewportSample.push({
                                tag: el.tagName,
                                role: el.getAttribute('role') || el.tagName.toLowerCase(),
                                ariaLabel: (el.getAttribute('aria-label') || '').substring(0, 100),
                                x: rect.x, y: rect.y, w: rect.width, h: rect.height
                            });
                        }
                    }
                }
            }
        }
    }
    
    return {
        totalDom: totalDom,
        elementsWithBbox: elementsWithBbox,
        locatableElements: locatableElements,
        viewportElements: viewportElements,
        locatableSample: locatableSample,
        viewportSample: viewportSample
    };
}
"""

# Accessibility snapshot JS
A11Y_SNAPSHOT_JS = """
() => {
    try {
        // Playwright's accessibility.snapshot() is called from the test runner
        // This is a fallback that counts ARIA roles in the DOM
        const ariaRoles = document.querySelectorAll('[role]');
        const ariaLabels = document.querySelectorAll('[aria-label]');
        const ariaDescribed = document.querySelectorAll('[aria-describedby]');
        const inputs = document.querySelectorAll('input, select, textarea, button');
        const links = document.querySelectorAll('a[href]');
        
        return {
            ariaRolesCount: ariaRoles.length,
            ariaLabelsCount: ariaLabels.length,
            ariaDescribedCount: ariaDescribed.length,
            inputsCount: inputs.length,
            linksCount: links.length,
            // Sample of ARIA roles
            ariaRoleSample: Array.from(ariaRoles).slice(0, 20).map(el => ({
                role: el.getAttribute('role'),
                tag: el.tagName,
                ariaLabel: (el.getAttribute('aria-label') || '').substring(0, 50)
            }))
        };
    } catch(e) {
        return {error: e.message};
    }
}
"""


def sha256_file(path):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data):
    """Compute SHA256 of bytes/string."""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


async def measure_task(page, task_url, task_id, page_type):
    """Measure a single task page using full-page DOM enumeration."""
    print(f"  [{task_id}] Navigating to {task_url}")
    
    result = {
        "task_id": task_id,
        "url": task_url,
        "page_type": page_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": None,
        "http_status": None
    }
    
    try:
        # Navigate to page
        response = await page.goto(task_url, wait_until="networkidle", timeout=30000)
        result["http_status"] = response.status if response else None
        
        # Wait for page to settle
        await asyncio.sleep(2)
        
        # Get page title
        result["page_title"] = await page.title()
        
        # Primary measurement: full-page DOM enumeration via page.evaluate()
        dom_data = await page.evaluate(MEASURE_JS)
        
        result["total_dom_elements"] = dom_data["totalDom"]
        result["elements_with_bbox"] = dom_data["elementsWithBbox"]
        result["locatable_elements"] = dom_data["locatableElements"]
        result["viewport_elements"] = dom_data["viewportElements"]
        result["locatable_sample"] = dom_data["locatableSample"]
        result["viewport_sample"] = dom_data["viewportSample"]
        
        # Compute derived metrics
        if result["total_dom_elements"] > 0:
            result["interactive_fraction"] = result["locatable_elements"] / result["total_dom_elements"]
            result["cdp_yield"] = result["viewport_elements"] / result["total_dom_elements"]
        else:
            result["interactive_fraction"] = 0.0
            result["cdp_yield"] = 0.0
        
        if result["locatable_elements"] > 0:
            result["viewport_locatable_yield"] = result["viewport_elements"] / result["locatable_elements"]
        else:
            result["viewport_locatable_yield"] = 0.0
        
        # Accessibility snapshot (secondary method)
        try:
            a11y_snapshot = await page.accessibility.snapshot()
            if a11y_snapshot:
                # Count nodes in the accessibility tree
                def count_nodes(node):
                    count = 1
                    for child in node.get("children", []):
                        count += count_nodes(child)
                    return count
                
                result["a11y_node_count"] = count_nodes(a11y_snapshot)
                result["a11y_root_role"] = a11y_snapshot.get("role", "")
                result["a11y_sample"] = {
                    "role": a11y_snapshot.get("role", ""),
                    "name": (a11y_snapshot.get("name", "") or "")[:100],
                    "children_count": len(a11y_snapshot.get("children", []))
                }
                # Save full snapshot
                a11y_path = OUTPUT_DIR / f"a11y_snapshot_{task_id}.json"
                with open(a11y_path, "w") as f:
                    json.dump(a11y_snapshot, f, indent=2)
                result["a11y_snapshot_path"] = str(a11y_path)
                result["a11y_snapshot_sha256"] = sha256_file(a11y_path)
            else:
                result["a11y_node_count"] = 0
                result["a11y_sample"] = None
        except Exception as e:
            result["a11y_error"] = str(e)
            result["a11y_node_count"] = 0
            result["a11y_sample"] = None
        
        # Additional DOM statistics via page.evaluate
        dom_stats = await page.evaluate("""
            () => {
                const all = document.querySelectorAll('*');
                const tags = {};
                for (const el of all) {
                    const tag = el.tagName.toLowerCase();
                    tags[tag] = (tags[tag] || 0) + 1;
                }
                return {
                    tagCounts: tags,
                    formsCount: document.querySelectorAll('form').length,
                    inputsCount: document.querySelectorAll('input, select, textarea').length,
                    linksCount: document.querySelectorAll('a[href]').length,
                    buttonsCount: document.querySelectorAll('button').length
                };
            }
        """)
        result["dom_stats"] = dom_stats
        
        print(f"    total_dom={result['total_dom_elements']}, bbox={result['elements_with_bbox']}, "
              f"locatable={result['locatable_elements']}, viewport={result['viewport_elements']}")
        print(f"    interactive_fraction={result['interactive_fraction']:.6f}, "
              f"cdp_yield={result['cdp_yield']:.6f}, a11y_nodes={result.get('a11y_node_count', 'N/A')}")
        
    except Exception as e:
        result["error"] = str(e)
        print(f"    ERROR: {e}")
    
    return result


async def main():
    """Main measurement routine."""
    print(f"EXP-INTEL-34718481334 Full-Page Yield Measurement")
    print(f"Frozen seed: {FROZEN_SEED}")
    print(f"Docker image: {DOCKER_IMAGE}")
    print(f"Docker digest: {DOCKER_DIGEST}")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()
    
    # Task selection with frozen seed
    rng = random.Random(FROZEN_SEED)
    
    # Define candidate tasks by page type
    listing_urls = [
        ("electronics.html", "http://localhost:8080/electronics.html"),
        ("home-kitchen.html", "http://localhost:8080/home-kitchen.html"),
        ("tools-home-improvement.html", "http://localhost:8080/tools-home-improvement.html"),
        ("clothing-shoes-jewelry.html", "http://localhost:8080/clothing-shoes-jewelry.html"),
        ("beauty-personal-care.html", "http://localhost:8080/beauty-personal-care.html"),
    ]
    
    detail_urls = [
        ("detail_vr_bag", "http://localhost:8080/navitech-black-hard-carry-bag-case-cover-with-shoulder-strap-compatible-with-the-vr-virtual-reality-3d-headsets-including-the-crypto-vr-150-virtual-reality-headset-3d-glasses.html"),
        ("detail_camera", "http://localhost:8080/zosi-h-265-poe-home-security-camera-system-outdoor-indoor-8-channel-5mp-poe-nvr-recorder-4pcs-wired-2mp-1080p-surveillance-bullet-poe-ip-cameras-no-hard-drive-renewed.html"),
        ("detail_pet_camera", "http://localhost:8080/indoor-pet-camera-hd-1080p-no-wifi-security-camera-with-night-vision-no-built-in-baterry.html"),
        ("detail_car_audio", "http://localhost:8080/rockville-ch103sp-chuchero-car-audio-enclosure-for-2-10-mids-2-3-tweeter.html"),
    ]
    
    cart_urls = [
        ("cart_1", "http://localhost:8080/checkout/cart/"),
    ]
    
    checkout_urls = [
        ("checkout_1", "http://localhost:8080/checkout/"),
    ]
    
    # Select tasks per frozen stratification
    listing_sel = rng.sample(listing_urls, 3)
    detail_sel = rng.sample(detail_urls, 3)
    cart_sel = rng.choices(cart_urls, k=2)
    checkout_sel = rng.choices(checkout_urls, k=2)
    
    # Build final task list with stable IDs
    all_tasks = []
    for name, url in listing_sel:
        all_tasks.append((f"listing_{name.replace('.html','')}", url, "product_listing"))
    for name, url in detail_sel:
        all_tasks.append((name, url, "detail"))
    for name, url in cart_sel:
        all_tasks.append((name, url, "cart"))
    for name, url in checkout_sel:
        all_tasks.append((name, url, "checkout"))
    
    print(f"Selected {len(all_tasks)} tasks:")
    for task_id, url, ptype in all_tasks:
        print(f"  {task_id}: {ptype} -> {url}")
    print()
    
    # Launch Playwright
    from playwright.async_api import async_playwright
    
    all_results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for task_id, url, page_type in all_tasks:
            print(f"Task: {task_id} ({page_type})")
            
            # Fresh browser context per task (no shared cookies/session)
            context = await browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            result = await measure_task(page, url, task_id, page_type)
            all_results.append(result)
            
            # Save per-task raw measurement
            raw_path = OUTPUT_DIR / f"raw_measurement_{task_id}.json"
            with open(raw_path, "w") as f:
                json.dump(result, f, indent=2)
            
            await page.close()
            await context.close()
            
            print()
        
        await browser.close()
    
    # Save all raw results
    raw_results_path = OUTPUT_DIR / "exp347_raw_results.json"
    with open(raw_results_path, "w") as f:
        json.dump({
            "experiment_id": EXPERIMENT_ID,
            "frozen_seed": FROZEN_SEED,
            "docker_image": DOCKER_IMAGE,
            "docker_digest": DOCKER_DIGEST,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "measurements": all_results
        }, f, indent=2)
    
    print(f"Raw results saved to {raw_results_path}")
    print(f"Raw results SHA256: {sha256_file(raw_results_path)}")
    
    # Compute statistics
    print("\n=== STATISTICS ===")
    
    successful = [r for r in all_results if r.get("error") is None]
    errors = [r for r in all_results if r.get("error") is not None]
    
    print(f"Total tasks: {len(all_results)}")
    print(f"Successful: {len(successful)}")
    print(f"Errors: {len(errors)}")
    
    if errors:
        for e in errors:
            print(f"  ERROR: {e['task_id']}: {e['error']}")
    
    if len(successful) < 8:
        print("WARNING: Fewer than 8 successful measurements - may be MEASUREMENT_INVALID")
    
    # Compute per-type and overall statistics
    types = {}
    for r in successful:
        pt = r["page_type"]
        if pt not in types:
            types[pt] = []
        types[pt].append(r)
    
    print("\nPer-type breakdown:")
    all_if = []
    all_cdp = []
    for pt, tasks in types.items():
        ifs = [t["interactive_fraction"] for t in tasks]
        cdps = [t["cdp_yield"] for t in tasks]
        doms = [t["total_dom_elements"] for t in tasks]
        locs = [t["locatable_elements"] for t in tasks]
        vps = [t["viewport_elements"] for t in tasks]
        
        all_if.extend(ifs)
        all_cdp.extend(cdps)
        
        n = len(tasks)
        print(f"  {pt} (n={n}):")
        print(f"    total_dom: mean={statistics.mean(doms):.1f}, stdev={statistics.stdev(doms) if n > 1 else 0:.1f}")
        print(f"    locatable: mean={statistics.mean(locs):.1f}, stdev={statistics.stdev(locs) if n > 1 else 0:.1f}")
        print(f"    viewport:  mean={statistics.mean(vps):.1f}, stdev={statistics.stdev(vps) if n > 1 else 0:.1f}")
        print(f"    interactive_fraction: mean={statistics.mean(ifs):.6f}, cv={statistics.stdev(ifs)/statistics.mean(ifs) if n > 1 and statistics.mean(ifs) > 0 else 0:.6f}")
        print(f"    cdp_yield: mean={statistics.mean(cdps):.6f}, cv={statistics.stdev(cdps)/statistics.mean(cdps) if n > 1 and statistics.mean(cdps) > 0 else 0:.6f}")
    
    if all_if:
        overall_cv = statistics.stdev(all_if) / statistics.mean(all_if) if statistics.mean(all_if) > 0 else 0
        print(f"\nOverall interactive_fraction: mean={statistics.mean(all_if):.6f}, stdev={statistics.stdev(all_if) if len(all_if) > 1 else 0:.6f}, cv={overall_cv:.6f}")
    
    # Between-type vs within-type variance
    if len(types) >= 2:
        type_means = {pt: statistics.mean([t["interactive_fraction"] for t in tasks]) 
                      for pt, tasks in types.items() if len(tasks) >= 1}
        
        between_var = statistics.variance(list(type_means.values())) if len(type_means) > 1 else 0
        
        within_vars = []
        for pt, tasks in types.items():
            if len(tasks) > 1:
                within_vars.append(statistics.variance([t["interactive_fraction"] for t in tasks]))
        within_var = statistics.mean(within_vars) if within_vars else 0
        
        print(f"\nBetween-type variance: {between_var:.10f}")
        print(f"Within-type variance: {within_var:.10f}")
        print(f"Discrimination ratio: {between_var / within_var if within_var > 0 else 'inf':.4f}")
    
    # A11y snapshot summary
    a11y_counts = [r.get("a11y_node_count", 0) for r in successful]
    print(f"\nA11y snapshot nodes: {[r.get('a11y_node_count', 'N/A') for r in successful]}")
    
    print(f"\nAll results saved. SHA256: {sha256_file(raw_results_path)}")


if __name__ == "__main__":
    asyncio.run(main())
