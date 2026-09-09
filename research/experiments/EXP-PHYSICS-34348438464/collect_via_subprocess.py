#!/usr/bin/env python3
"""
Collect browser transitions using subprocess to avoid Playwright timeout issues.
"""

import json
import subprocess
import sys
import time

def run_collection():
    """Run the Playwright collection in a subprocess."""
    script = '''
import json
import time
import random
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urljoin

SEED = 42
rng = random.Random(SEED)
transitions = []

print("Starting Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    
    for traj_id in range(5):
        print(f"Trajectory {traj_id}...")
        page.goto("https://github.com", timeout=15000, wait_until="domcontentloaded")
        time.sleep(1)
        
        for step in range(3):
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
            for link in links:
                try:
                    href = link.get_attribute("href") or ""
                    if href.startswith("#") or href.startswith("javascript:"):
                        continue
                    if not href.startswith("http"):
                        href = urljoin(url, href)
                    parsed = urlparse(href)
                    if parsed.netloc == "github.com":
                        actions.append({"element": link, "href": href})
                except:
                    continue
            
            if not actions:
                break
            
            action = rng.choice(actions)
            try:
                action["element"].click()
                time.sleep(1)
                
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
                time.sleep(0.5)
            except Exception as e:
                print(f"  Action failed: {e}")
                break
    
    browser.close()

print(f"Collected {len(transitions)} transitions")

with open("research/experiments/EXP-PHYSICS-34348438464/github_transitions.json", "w") as f:
    json.dump(transitions, f, indent=2, default=str)
print("Saved")
'''
    
    # Write script to temp file
    script_path = "/tmp/collect_github.py"
    with open(script_path, "w") as f:
        f.write(script)
    
    # Run subprocess
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        timeout=120,
        cwd="/home/runner/work/Spider/Spider"
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    return result.returncode == 0


if __name__ == "__main__":
    success = run_collection()
    print(f"Collection {'succeeded' if success else 'failed'}")
