#!/usr/bin/env python3
"""
Step 2: Collect browser transitions from real SPA sites.
"""

import json
import time
import os
from playwright.sync_api import sync_playwright

EXPERIMENT_ID = "EXP-PHYSICS-34348438464"
SEED = 42
N_TRAJECTORIES = 20
TRAJECTORY_LENGTH = 8
POLITE_DELAY = 1.0
STATE_CAPTURE_DELAY = 1.0

SITES = {
    "github": {
        "name": "GitHub",
        "entry_url": "https://github.com",
    },
    "mdn": {
        "name": "MDN Web Docs",
        "entry_url": "https://developer.mozilla.org",
    },
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
    from urllib.parse import urlparse, urljoin
    actions = []
    entry_domain = urlparse(entry_url).netloc
    
    # Buttons
    buttons = page.query_selector_all("button:visible, [role=button]:visible")
    for btn in buttons:
        try:
            text = btn.inner_text()[:50] if btn.inner_text() else ""
            is_enabled = btn.is_enabled()
            if is_enabled and text:
                btn_id = btn.get_attribute("id") or ""
                btn_class = btn.get_attribute("class") or ""
                btn_href = f"button://{btn_class}/{btn_id}/{text[:20]}"
                actions.append({
                    "type": "button_click",
                    "href": btn_href,
                    "element": btn,
                })
        except:
            continue
    
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
    
    # Inputs
    inputs = page.query_selector_all("input:not([type=hidden]):visible, textarea:visible")
    for inp in inputs:
        try:
            input_type = inp.get_attribute("type") or "text"
            placeholder = inp.get_attribute("placeholder") or ""
            inp_id = inp.get_attribute("id") or ""
            inp_name = inp.get_attribute("name") or ""
            if input_type in ["text", "email", "password", "search", "url", "tel", "number", "textarea"]:
                inp_href = f"input://{inp_id}/{inp_name}/{placeholder[:20]}"
                actions.append({
                    "type": "input_submit",
                    "href": inp_href,
                    "element": inp,
                })
        except:
            continue
    
    # Checkboxes
    toggles = page.query_selector_all("input[type=checkbox]:visible, [role=checkbox]:visible, [role=switch]:visible")
    for toggle in toggles:
        try:
            toggle_id = toggle.get_attribute("id") or ""
            toggle_label = toggle_id or "toggle"
            toggle_href = f"toggle://{toggle_id}/{toggle_label[:20]}"
            actions.append({
                "type": "toggle",
                "href": toggle_href,
                "element": toggle,
            })
        except:
            continue
    
    return actions


def execute_action(page, action):
    import random
    try:
        element = action["element"]
        if action["type"] == "button_click":
            element.click()
        elif action["type"] == "link_nav":
            element.click()
        elif action["type"] == "input_submit":
            element.fill("")
            element.type(f"test_{random.randint(0, 999)}")
            element.press("Enter")
        elif action["type"] == "toggle":
            element.click()
        else:
            return {"success": False}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def collect_site_transitions(page, site_config, n_trajectories, trajectory_length):
    import random
    rng = random.Random(SEED)
    transitions = []
    
    for traj_id in range(n_trajectories):
        try:
            page.goto(site_config["entry_url"], timeout=20000, wait_until="domcontentloaded")
            time.sleep(STATE_CAPTURE_DELAY)
            
            for step in range(trajectory_length):
                state_before = extract_browser_state(page)
                actions = find_available_actions(page, site_config["entry_url"])
                
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
    
    return transitions


def main():
    print("=" * 70)
    print("BROWSER DATA COLLECTION")
    print("=" * 70)
    
    all_site_data = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for site_key, site_config in SITES.items():
            print(f"\nCollecting from: {site_config['name']}")
            print(f"Entry: {site_config['entry_url']}")
            
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )
            page = context.new_page()
            
            try:
                raw_transitions = collect_site_transitions(
                    page, site_config, N_TRAJECTORIES, TRAJECTORY_LENGTH)
                print(f"  Collected {len(raw_transitions)} raw transitions")
                
                # Classify non-leakage
                non_leakage = []
                leakage_count = 0
                for t in raw_transitions:
                    target = t["action"]["target_href"]
                    actual_url = t["state_after"]["url"]
                    if target == actual_url:
                        leakage_count += 1
                    else:
                        non_leakage.append(t)
                
                print(f"  Non-leakage: {len(non_leakage)}")
                print(f"  Leakage: {leakage_count}")
                
                # Title analysis
                titles = [t["state_before"]["title"] for t in non_leakage]
                unique_titles = len(set(titles))
                print(f"  Unique titles: {unique_titles}/{len(titles)}")
                
                all_site_data[site_key] = {
                    "name": site_config["name"],
                    "entry_url": site_config["entry_url"],
                    "raw_transitions": raw_transitions,
                    "non_leakage": non_leakage,
                    "n_leakage": leakage_count,
                    "unique_titles": unique_titles,
                }
                
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
            finally:
                context.close()
        
        browser.close()
    
    # Save results
    out_dir = "research/experiments/EXP-PHYSICS-34348438464"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "browser_transitions.json")
    with open(out_path, "w") as f:
        json.dump(all_site_data, f, indent=2, default=str)
    print(f"\nBrowser transitions saved to {out_path}")


if __name__ == "__main__":
    main()
