#!/usr/bin/env python3
"""Collect browser transitions from 3 production sites."""
import json, time, random
from urllib.parse import urlparse, urljoin
from playwright.sync_api import sync_playwright

SEED = 42
SITES = {
    'wikipedia': {'name': 'Wikipedia', 'entry_url': 'https://en.wikipedia.org', 'domain': 'en.wikipedia.org'},
    'mdn': {'name': 'MDN', 'entry_url': 'https://developer.mozilla.org', 'domain': 'developer.mozilla.org'},
    'github': {'name': 'GitHub', 'entry_url': 'https://github.com', 'domain': 'github.com'},
}
N_TRAJ = 12
TRAJ_LEN = 8
POLITE = 0.8
CAPTURE_DELAY = 1.2

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
    try:
        for btn in page.query_selector_all('button:visible, [role=button]:visible'):
            try:
                text = (btn.inner_text() or '')[:30].strip()
                if btn.is_enabled() and text and len(text) > 1:
                    actions.append({'type': 'button', 'href': f'btn://{text[:20]}', 'el': btn})
            except: continue
    except: pass
    return actions

rng = random.Random(SEED)
all_data = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
    
    for site_key, sc in SITES.items():
        print(f'\n=== {sc["name"]} ===')
        ctx = browser.new_context(viewport={'width': 1280, 'height': 720}, user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120')
        page = ctx.new_page()
        transitions = []
        
        for traj in range(N_TRAJ):
            try:
                page.goto(sc['entry_url'], timeout=15000, wait_until='domcontentloaded')
                time.sleep(CAPTURE_DELAY)
                for step in range(TRAJ_LEN):
                    sb = extract_state(page)
                    acts = find_actions(page, sc['domain'])
                    if not acts:
                        break
                    a = rng.choice(acts)
                    try:
                        a['el'].click()
                    except:
                        break
                    time.sleep(CAPTURE_DELAY)
                    sa = extract_state(page)
                    transitions.append({
                        'trajectory_id': traj, 'step': step,
                        'state_before': sb,
                        'action': {'action_type': a['type'], 'target_href': a['href']},
                        'state_after': sa
                    })
                    time.sleep(POLITE)
            except Exception as e:
                print(f'  traj {traj}: {e}')
                continue
        
        nl = [t for t in transitions if t['action']['target_href'] != t['state_after']['url']]
        titles = set(t['state_before']['title'] for t in nl)
        print(f'  raw={len(transitions)}, NL={len(nl)}, unique_titles={len(titles)}')
        
        path = f'research/experiments/EXP-PHYSICS-35185288822/{site_key}_transitions.json'
        with open(path, 'w') as f:
            json.dump(transitions, f, indent=2, default=str)
        print(f'  Saved {path}')
        
        all_data[site_key] = {'n_raw': len(transitions), 'n_nl': len(nl), 'unique_titles': len(titles)}
        ctx.close()
    
    browser.close()

with open('research/experiments/EXP-PHYSICS-35185288822/collection_summary.json', 'w') as f:
    json.dump(all_data, f, indent=2)
print('\nAll done.')
