#!/usr/bin/env python3
"""
Collect browser transitions for both sites using subprocess.
"""

import json
import subprocess
import sys
import os

WORK_DIR = "/home/runner/work/Spider/Spider"

def run_collection():
    """Run Playwright collection for both sites."""
    script = '''
import json
import time
import random
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urljoin

SEED = 42
rng = random.Random(SEED)
N_TRAJECTORIES = 15
TRAJECTORY_LENGTH = 6

SITES = {
    "github": {"name": "GitHub", "entry_url": "https://github.com"},
    "mdn": {"name": "MDN Web Docs", "entry_url": "https://developer.mozilla.org"},
}

all_results = {}

print("Starting Playwright collection...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for site_key, site_config in SITES.items():
        print(f"\\nCollecting from: {site_config['name']}")
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        
        transitions = []
        
        for traj_id in range(N_TRAJECTORIES):
            try:
                page.goto(site_config["entry_url"], timeout=15000, wait_until="domcontentloaded")
                time.sleep(0.5)
                
                for step in range(TRAJECTORY_LENGTH):
                    url = page.url
                    title = page.title()[:100]
                    
                    state_before = {
                        "url": url,
                        "title": title,
                        "form_signals": [
                            len(page.query_selector_all("form")) > 0,
                            len(page.query_selector_all("input:not([type=hidden])")) > 0,
                            len(page.query_selector_all("select")) > 0,
                            len(page.query_selector_all("textarea")) > 0,
                        ],
                    }
                    
                    links = page.query_selector_all("a[href]:visible")
                    actions = []
                    entry_domain = urlparse(site_config["entry_url"]).netloc
                    
                    for link in links:
                        try:
                            href = link.get_attribute("href") or ""
                            if href.startswith("#") or href.startswith("javascript:"):
                                continue
                            if not href.startswith("http"):
                                href = urljoin(url, href)
                            parsed = urlparse(href)
                            if parsed.netloc == entry_domain or parsed.netloc == "":
                                actions.append({"element": link, "href": href})
                        except:
                            continue
                    
                    if not actions:
                        break
                    
                    action = rng.choice(actions)
                    try:
                        action["element"].click()
                        time.sleep(0.5)
                        
                        state_after = {
                            "url": page.url,
                            "title": page.title()[:100],
                            "form_signals": [
                                len(page.query_selector_all("form")) > 0,
                                len(page.query_selector_all("input:not([type=hidden])")) > 0,
                                len(page.query_selector_all("select")) > 0,
                                len(page.query_selector_all("textarea")) > 0,
                            ],
                        }
                        
                        transitions.append({
                            "trajectory_id": traj_id,
                            "step": step,
                            "state_before": state_before,
                            "action": {"action_type": "link_nav", "target_href": action["href"]},
                            "state_after": state_after,
                        })
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"  Action failed: {e}")
                        break
                
            except Exception as e:
                print(f"  Trajectory {traj_id} failed: {e}")
                continue
        
        context.close()
        
        # Classify non-leakage
        non_leakage = []
        leakage_count = 0
        for t in transitions:
            target = t["action"]["target_href"]
            actual_url = t["state_after"]["url"]
            if target == actual_url:
                leakage_count += 1
            else:
                non_leakage.append(t)
        
        titles = [t["state_before"]["title"] for t in non_leakage]
        unique_titles = len(set(titles))
        
        print(f"  Raw transitions: {len(transitions)}")
        print(f"  Non-leakage: {len(non_leakage)}")
        print(f"  Leakage: {leakage_count}")
        print(f"  Unique titles: {unique_titles}/{len(titles)}")
        
        all_results[site_key] = {
            "name": site_config["name"],
            "raw_transitions": transitions,
            "non_leakage": non_leakage,
            "n_leakage": leakage_count,
            "unique_titles": unique_titles,
        }
    
    browser.close()

# Save results
with open("research/experiments/EXP-PHYSICS-34348438464/all_browser_transitions.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)

print("\\nAll data saved to all_browser_transitions.json")
'''
    
    script_path = "/tmp/full_collection.py"
    with open(script_path, "w") as f:
        f.write(script)
    
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        timeout=600,  # 10 minutes
        cwd=WORK_DIR
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR (last 500 chars):")
        print(result.stderr[-500:])
    
    return result.returncode == 0


if __name__ == "__main__":
    success = run_collection()
    print(f"Collection {'succeeded' if success else 'failed'}")
