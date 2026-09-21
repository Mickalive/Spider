#!/usr/bin/env python3
"""
EXP-INTEL-35572177756 Full-DOM Collection Script
Collects ALL elements with bbox (not truncated-first-20) for the 7 existing Magento tasks.
Based on measure_fullpage_yield.py but removes truncation limit.
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
EXPERIMENT_ID = "EXP-INTEL-35572177756"
FROZEN_SEED = 99
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
INTERSECTION_THRESHOLD = 0.5

# Frozen definition: DEF-FALLBACK-INTERACTIVE
INTERACTIVE_ROLES = {
    "button", "link", "textbox", "checkbox", "radio",
    "combobox", "listbox", "menuitem", "tab", "slider",
    "spinbutton", "searchbox", "switch"
}

# Docker image info
DOCKER_IMAGE = "am1n3e/webarena-verified-shopping:latest"
DOCKER_DIGEST = "sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb"

# Output directory
OUTPUT_DIR = Path(__file__).parent / "raw_evidence"
OUTPUT_DIR.mkdir(exist_ok=True)

# JavaScript for full-page DOM measurement (NO TRUNCATION)
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
                
                // CRITICAL CHANGE: No truncation limit
                locatableSample.push({
                    tag: el.tagName,
                    role: el.getAttribute('role') || el.tagName.toLowerCase(),
                    ariaLabel: (el.getAttribute('aria-label') || '').substring(0, 100),
                    inForm: el.closest('form') !== null,
                    x: rect.x, y: rect.y, w: rect.width, h: rect.height
                });
                
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
                        // Also no truncation for viewport sample
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


def sha256_file(path):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


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
        print(f"    locatable_sample_length={len(result['locatable_sample'])} "
              f"(expected {result['locatable_elements']} from locatable_elements)")
        
    except Exception as e:
        result["error"] = str(e)
        print(f"    ERROR: {e}")
    
    return result


async def main():
    """Main measurement routine."""
    print(f"EXP-INTEL-35572177756 Full-DOM Collection")
    print(f"Frozen seed: {FROZEN_SEED}")
    print(f"Docker image: {DOCKER_IMAGE}")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()
    
    # Fixed task list from parent experiment (7 tasks)
    tasks = [
        ("listing_clothing-shoes-jewelry", "http://localhost:8080/clothing-shoes-jewelry.html", "product_listing"),
        ("listing_beauty-personal-care", "http://localhost:8080/beauty-personal-care.html", "product_listing"),
        ("listing_electronics", "http://localhost:8080/electronics.html", "product_listing"),
        ("detail_camera", "http://localhost:8080/zosi-h-265-poe-home-security-camera-system-outdoor-indoor-8-channel-5mp-poe-nvr-recorder-4pcs-wired-2mp-1080p-surveillance-bullet-poe-ip-cameras-no-hard-drive-renewed.html", "detail"),
        ("detail_vr_bag", "http://localhost:8080/navitech-black-hard-carry-bag-case-cover-with-shoulder-strap-compatible-with-the-vr-virtual-reality-3d-headsets-including-the-crypto-vr-150-virtual-reality-headset-3d-glasses.html", "detail"),
        ("detail_pet_camera", "http://localhost:8080/indoor-pet-camera-hd-1080p-no-wifi-security-camera-with-night-vision-no-built-in-baterry.html", "detail"),
        ("cart_1", "http://localhost:8080/checkout/cart/", "cart"),
    ]
    
    print(f"Collected {len(tasks)} tasks:")
    for task_id, url, ptype in tasks:
        print(f"  {task_id}: {ptype} -> {url}")
    print()
    
    # Launch Playwright
    from playwright.async_api import async_playwright
    
    all_results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for task_id, url, page_type in tasks:
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
    raw_results_path = OUTPUT_DIR / "exp355_fulldom_raw_results.json"
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
    
    # Verify locatable_sample lengths
    print("\n=== LOCATABLE SAMPLE LENGTHS ===")
    for r in all_results:
        if r.get("error") is None:
            sample_len = len(r.get("locatable_sample", []))
            locatable = r.get("locatable_elements", 0)
            print(f"  {r['task_id']}: sample_len={sample_len}, locatable_elements={locatable}, "
                  f"match={'YES' if sample_len == locatable else 'NO'}")
    
    print(f"\nAll results saved. SHA256: {sha256_file(raw_results_path)}")


if __name__ == "__main__":
    asyncio.run(main())