#!/usr/bin/env python3
"""
EXP-PHYSICS-35353016293 — Playwright browser collection on locally-hosted SPA.

Collects transitions by navigating the SPA simulation via Playwright,
extracting action primitives and URL transitions.  Uses the server's
/api/transition endpoint to get the actual next state (beyond-Markov
structure is server-controlled).
"""

import json
import random
import hashlib
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

EXPERIMENT_ID = "EXP-PHYSICS-35353016293"
SEED = 42
SPA_URL = "http://localhost:18973"
N_SESSIONS = 20
STEPS_PER_SESSION = 50
TARGET_RAW_TRANSITIONS = 500  # >= 200 required for pilot

# Actions mapping: button IDs → action primitives
ACTION_BUTTONS = {
    "btn-form": "form_submit",
    "btn-click": "button_click",
    "btn-nav": "js_navigate",
    "btn-menu": "menu_select",
}


def collect_transitions():
    """Collect transitions via Playwright browser automation."""
    rng = random.Random(SEED)
    all_transitions = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for session_id in range(N_SESSIONS):
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent=f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 SpiderBot/{session_id}",
            )
            page = context.new_page()
            
            try:
                # Navigate to SPA
                page.goto(SPA_URL, wait_until="networkidle", timeout=10000)
                time.sleep(0.2)
                
                # Get initial state
                initial_url = page.url
                session_trans = []
                
                for step in range(STEPS_PER_SESSION):
                    # Get current URL before action
                    url_before = page.url
                    
                    # Choose random action
                    action = rng.choice(list(ACTION_BUTTONS.keys()))
                    action_primitive = ACTION_BUTTONS[action]
                    
                    # Click the action button
                    try:
                        page.click(f"#{action}", timeout=3000)
                        time.sleep(0.1)
                    except Exception as e:
                        # If click fails, try JS navigation
                        try:
                            page.evaluate(f"doAction('{action_primitive}')")
                            time.sleep(0.1)
                        except Exception:
                            continue
                    
                    # Get new URL after action
                    url_after = page.url
                    
                    # Parse hash fragments for state identification
                    trans = {
                        "session": f"session_{session_id}",
                        "step": step,
                        "url_before": url_before.split("#")[0] + "#" + url_before.split("#")[1] if "#" in url_before else url_before,
                        "url_after": url_after.split("#")[0] + "#" + url_after.split("#")[1] if "#" in url_after else url_after,
                        "action_primitive": action_primitive,
                        "error": None,
                    }
                    session_trans.append(trans)
                
                all_transitions.extend(session_trans)
                print(f"Session {session_id}: {len(session_trans)} transitions collected")
                
            except Exception as e:
                print(f"Session {session_id} failed: {e}")
            finally:
                context.close()
        
        browser.close()
    
    return all_transitions


def collect_api_transitions():
    """Collect transitions directly via the server API (bypassing browser)."""
    import urllib.request
    import urllib.parse
    
    rng = random.Random(SEED)
    all_transitions = []
    actions = ["form_submit", "button_click", "js_navigate", "menu_select"]
    
    for session_id in range(N_SESSIONS):
        # Reset session
        try:
            urllib.request.urlopen(f"{SPA_URL}/api/reset?session=session_{session_id}")
        except Exception:
            pass
        
        # Start at state 0 (home)
        current_state = 0
        
        for step in range(STEPS_PER_SESSION):
            action = rng.choice(actions)
            
            # Get transition from server
            params = urllib.parse.urlencode({
                "state": current_state,
                "action": action,
                "session": f"session_{session_id}",
            })
            
            try:
                resp = urllib.request.urlopen(f"{SPA_URL}/api/transition?{params}")
                data = json.loads(resp.read().decode())
                
                trans = {
                    "session": f"session_{session_id}",
                    "step": step,
                    "url_before": data["url_before"],
                    "url_after": data["url_after"],
                    "action_primitive": data["action_primitive"],
                    "error": None,
                }
                all_transitions.append(trans)
                current_state = data["next_state"]
                
            except Exception as e:
                print(f"  Session {session_id} step {step} failed: {e}")
                continue
        
        print(f"Session {session_id}: collected via API")
    
    return all_transitions


def save_raw_data(transitions):
    """Save raw transition data."""
    out_dir = Path("research/experiments") / EXPERIMENT_ID
    out_dir.mkdir(parents=True, exist_ok=True)
    
    raw_path = out_dir / "raw_transitions.json"
    with open(raw_path, "w") as f:
        json.dump(transitions, f, indent=2)
    
    sha = hashlib.sha256(json.dumps(transitions, sort_keys=True).encode()).hexdigest()
    print(f"Saved {len(transitions)} transitions to {raw_path}")
    print(f"SHA256: {sha}")
    
    return raw_path, sha


if __name__ == "__main__":
    print("Collecting transitions via API...")
    transitions = collect_api_transitions()
    
    raw_path, sha = save_raw_data(transitions)
    
    print(f"\nTotal transitions: {len(transitions)}")
    print(f"Sessions: {len(set(t['session'] for t in transitions))}")
    print(f"Target: >= {TARGET_RAW_TRANSITIONS}")
    print(f"Pilot pass: {len(transitions) >= 200}")
