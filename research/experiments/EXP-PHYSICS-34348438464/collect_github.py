#!/usr/bin/env python3
"""
Collect data from a single site with minimal parameters.
"""

import json
import time
import os
import random
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urljoin

SEED = 42
N_TRAJECTORIES = 10
TRAJECTORY_LENGTH = 4
POLITE_DELAY = 0.5
STATE_CAPTURE_DELAY = 0.5

SITE_KEY = "github"
SITE_CONFIG = {
    "name": "GitHub",
    "entry_url": "https://github.com",
}


def extract_browser_state(page):
    url = page.url
    title = page.title()[:100]
    has_form = len(page.query_selector_all("form")) > 0
    has_input = len(page.query_selector_all("input:not([type=hidden])")) > 0
    has_select = len(page.query_selector_all("select")) > 0
    has_textarea = len(page.query_selector_all("textarea")) > 0
    return {
        "url": url,
        "title": title,
        "form_signals": [has_form, has_input, has_select, has_textarea],
    }


def find_available_actions(page, entry_url):
    actions = []
    entry_domain = urlparse(entry_url).netloc
    
    # Links
    links = page.query_selector_all("a[href]:visible")
    for link in links:
        try:
            href = link.get_attribute("href") or ""
            if not href or href.startswith("#") or href.startswith("javascript:"):
                text = link.inner_text()[:30] if link.inner_text() else ""
                if text:
                    actions.append({
                        "type": "link_nav",
                        "href": href,
                        "element": link,
                    })
                continue
            if not href.startswith("http"):
                href = urljoin(page.url, href)
            parsed = urlparse(href)
            if parsed.netloc == entry_domain or parsed.netloc == "":
                text = link.inner_text()[:30] if link.inner_text() else ""
                actions.append({
                    "type": "link_nav",
                    "href": href,
                    "element": link,
                })
        except:
            continue
    
    return actions


def execute_action(page, action):
    try:
        element = action["element"]
        if action["type"] == "link_nav":
            element.click()
        else:
            return {"success": False}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    rng = random.Random(SEED)
    transitions = []
    
    print(f"Collecting from {SITE_CONFIG['name']}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        
        for traj_id in range(N_TRAJECTORIES):
            try:
                page.goto(SITE_CONFIG["entry_url"], timeout=15000, wait_until="domcontentloaded")
                time.sleep(STATE_CAPTURE_DELAY)
                
                for step in range(TRAJECTORY_LENGTH):
                    state_before = extract_browser_state(page)
                    actions = find_available_actions(page, SITE_CONFIG["entry_url"])
                    
                    if not actions:
                        break
                    
                    action = rng.choice(actions)
                    action_result = execute_action(page, action)
                    
                    if not action_result["success"]:
                        break
                    
                    time.sleep(STATE_CAPTURE_DELAY)
                    state_after = extract_browser_state(page)
                    
                    transition = {
                        "trajectory_id": traj_id,
                        "step": step,
                        "state_before": state_before,
                        "action": {
                            "action_type": action["type"],
                            "target_href": action["href"],
                        },
                        "state_after": state_after,
                    }
                    transitions.append(transition)
                    time.sleep(POLITE_DELAY)
                    
            except Exception as e:
                print(f"  Trajectory {traj_id} failed: {e}")
                continue
        
        browser.close()
    
    print(f"Collected {len(transitions)} transitions")
    
    # Save
    out_path = "research/experiments/EXP-PHYSICS-34348438464/github_transitions.json"
    with open(out_path, "w") as f:
        json.dump(transitions, f, indent=2, default=str)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
