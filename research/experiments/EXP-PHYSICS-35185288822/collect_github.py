#!/usr/bin/env python3
"""Collect GitHub transitions."""
import json, time, random
from urllib.parse import urlparse, urljoin
from playwright.sync_api import sync_playwright

rng = random.Random(42)

def extract_state(page):
    return {'url': page.url, 'title': (page.title() or '')[:100]}

def find_actions(page, domain):
    actions = []
    try:
        for link in page.query_selector_all('a[href]:visible'):
            try:
                href = link.get_attribute('href') or ''
                if not href or href.startswith('#') or href.startswith('javascript:'): continue
                if not href.startswith('http'): href = urljoin(page.url, href)
                if urlparse(href).netloc == domain:
                    text = (link.inner_text() or '')[:30].strip()
                    if text and len(text) > 1:
                        actions.append({'type': 'link', 'href': href, 'el': link})
            except: continue
    except: pass
    return actions

transitions = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
    ctx = browser.new_context(viewport={'width': 1280, 'height': 720}, user_agent='Mozilla/5.0 Chrome/120')
    page = ctx.new_page()
    domain = 'github.com'
    for traj in range(15):
        try:
            page.goto('https://github.com', timeout=12000, wait_until='domcontentloaded')
            time.sleep(0.8)
            for step in range(8):
                sb = extract_state(page)
                acts = find_actions(page, domain)
                if not acts: break
                a = rng.choice(acts)
                try: a['el'].click()
                except: break
                time.sleep(0.8)
                sa = extract_state(page)
                transitions.append({'trajectory_id': traj, 'step': step, 'state_before': sb, 'action': {'action_type': a['type'], 'target_href': a['href']}, 'state_after': sa})
                time.sleep(0.5)
        except Exception as e:
            print(f'traj {traj}: {e}')
            continue
    ctx.close()
    browser.close()

nl = [t for t in transitions if t['action']['target_href'] != t['state_after']['url']]
titles = set(t['state_before']['title'] for t in nl)
print(f'GitHub: raw={len(transitions)}, NL={len(nl)}, titles={len(titles)}')
with open('research/experiments/EXP-PHYSICS-35185288822/github_transitions.json', 'w') as f:
    json.dump(transitions, f, indent=2, default=str)
