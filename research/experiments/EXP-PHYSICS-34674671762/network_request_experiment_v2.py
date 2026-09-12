#!/usr/bin/env python3
"""
EXP-PHYSICS-34674671762 — Network Request PMI Experiment (v2)
Tests whether network requests and API calls captured via Playwright route
interception on genuine client-side-routed SPAs provide predictive state
information beyond URL.

v2: Fixed synthetic SPA positive control using local HTTP server.
"""

import json
import math
import random
import collections
import os
import sys
import hashlib
import time
import traceback
import re
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

import numpy as np

# ─── Configuration (frozen from spec.json) ───────────────────────────────────

EXPERIMENT_ID = "EXP-PHYSICS-34674671762"
SEED = 42
N_PERMUTATIONS = 1000
ALPHA = 1.0  # Laplace smoothing
BONFERRONI_COMPARISONS = 3  # 3 sites maximum
ALPHA_BONFERRONI = 0.05 / BONFERRONI_COMPARISONS  # 0.0167

# ─── Synthetic SPA Configuration ──────────────────────────────────────────────

# 8 states with same URL but different network-request patterns
# Each (state, action) triggers distinct endpoint+method+status
SYNTHETIC_STATES = {
    0: {"name": "Checkout Step 1", "api_calls": [
        {"endpoint": "/api/shipping/validate", "method": "POST", "status": 200},
        {"endpoint": "/api/cart/summary", "method": "GET", "status": 200}
    ]},
    1: {"name": "Checkout Step 2", "api_calls": [
        {"endpoint": "/api/payment/methods", "method": "GET", "status": 200},
        {"endpoint": "/api/shipping/cost", "method": "POST", "status": 200}
    ]},
    2: {"name": "Checkout Step 3", "api_calls": [
        {"endpoint": "/api/payment/process", "method": "POST", "status": 200},
        {"endpoint": "/api/order/create", "method": "POST", "status": 201}
    ]},
    3: {"name": "Dashboard Overview", "api_calls": [
        {"endpoint": "/api/dashboard/stats", "method": "GET", "status": 200},
        {"endpoint": "/api/dashboard/recent", "method": "GET", "status": 200}
    ]},
    4: {"name": "Dashboard Analytics", "api_calls": [
        {"endpoint": "/api/analytics/summary", "method": "GET", "status": 200},
        {"endpoint": "/api/analytics/chart", "method": "POST", "status": 200}
    ]},
    5: {"name": "Dashboard Settings", "api_calls": [
        {"endpoint": "/api/settings/user", "method": "GET", "status": 200},
        {"endpoint": "/api/settings/preferences", "method": "PUT", "status": 200}
    ]},
    6: {"name": "Profile View", "api_calls": [
        {"endpoint": "/api/profile/info", "method": "GET", "status": 200},
        {"endpoint": "/api/profile/activity", "method": "GET", "status": 200}
    ]},
    7: {"name": "Profile Edit", "api_calls": [
        {"endpoint": "/api/profile/update", "method": "POST", "status": 200},
        {"endpoint": "/api/profile/avatar", "method": "POST", "status": 200}
    ]}
}

# Transition matrix
SYNTHETIC_TRANSITIONS = {
    0: {"form_submit": 3, "button_click": 4, "link_nav": 6, "menu_select": 7},
    1: {"form_submit": 5, "button_click": 3, "link_nav": 4, "menu_select": 6},
    2: {"form_submit": 3, "button_click": 5, "link_nav": 7, "menu_select": 4},
    3: {"form_submit": 0, "button_click": 1, "link_nav": 2, "menu_select": 6},
    4: {"form_submit": 1, "button_click": 2, "link_nav": 0, "menu_select": 7},
    5: {"form_submit": 2, "button_click": 0, "link_nav": 1, "menu_select": 6},
    6: {"form_submit": 3, "button_click": 4, "link_nav": 5, "menu_select": 0},
    7: {"form_submit": 5, "button_click": 3, "link_nav": 6, "menu_select": 1}
}


# ─── Local HTTP Server for Synthetic SPA ──────────────────────────────────────

class SyntheticSPAHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves SPA HTML and API endpoints."""
    
    current_state = 0
    
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(SYNTHETIC_SPA_HTML.encode())
        elif self.path.startswith('/api/'):
            # API endpoint - return JSON
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"state": self.current_state, "endpoint": self.path}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            self.send_response(201 if 'create' in self.path else 200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"state": self.current_state, "endpoint": self.path, "method": "POST"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_PUT(self):
        if self.path.startswith('/api/'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"state": self.current_state, "endpoint": self.path, "method": "PUT"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress server logs


SYNTHETIC_SPA_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Synthetic SPA - Network Request Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .state { display: none; }
        .state.active { display: block; }
        button { margin: 5px; padding: 10px; }
        .form-group { margin: 10px 0; }
        label { display: block; margin-bottom: 5px; }
        input, select { padding: 5px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>Synthetic SPA State Machine</h1>
    <p>Current State: <span id="state-display">0</span></p>
    
    <!-- State 0: Checkout Step 1 -->
    <div id="state-0" class="state active">
        <h2>Checkout Step 1</h2>
        <form>
            <div class="form-group">
                <label for="shipping-name">Shipping Name</label>
                <input type="text" id="shipping-name" name="shipping-name">
            </div>
            <div class="form-group">
                <label for="shipping-address">Shipping Address</label>
                <input type="text" id="shipping-address" name="shipping-address">
            </div>
        </form>
    </div>
    
    <!-- State 1: Checkout Step 2 -->
    <div id="state-1" class="state">
        <h2>Checkout Step 2</h2>
        <form>
            <div class="form-group">
                <label for="card-number">Card Number</label>
                <input type="text" id="card-number" name="card-number">
            </div>
        </form>
    </div>
    
    <!-- State 2: Checkout Step 3 -->
    <div id="state-2" class="state">
        <h2>Checkout Step 3</h2>
        <p>Confirm your order</p>
    </div>
    
    <!-- State 3: Dashboard Overview -->
    <div id="state-3" class="state">
        <h2>Dashboard Overview</h2>
        <p>Statistics and recent activity</p>
    </div>
    
    <!-- State 4: Dashboard Analytics -->
    <div id="state-4" class="state">
        <h2>Dashboard Analytics</h2>
        <p>Charts and analytics</p>
    </div>
    
    <!-- State 5: Dashboard Settings -->
    <div id="state-5" class="state">
        <h2>Dashboard Settings</h2>
        <form>
            <div class="form-group">
                <label for="display-name">Display Name</label>
                <input type="text" id="display-name" name="display-name">
            </div>
        </form>
    </div>
    
    <!-- State 6: Profile View -->
    <div id="state-6" class="state">
        <h2>Profile View</h2>
        <p>User profile information</p>
    </div>
    
    <!-- State 7: Profile Edit -->
    <div id="state-7" class="state">
        <h2>Profile Edit</h2>
        <form>
            <div class="form-group">
                <label for="edit-email">Email</label>
                <input type="email" id="edit-email" name="edit-email">
            </div>
        </form>
    </div>
    
    <!-- Navigation Buttons -->
    <div id="navigation">
        <h3>Actions:</h3>
        <button type="button" id="btn-form-submit" onclick="takeAction('form_submit')">Form Submit</button>
        <button type="button" id="btn-button-click" onclick="takeAction('button_click')">Button Click</button>
        <button type="button" id="btn-link-nav" onclick="takeAction('link_nav')">Link Navigation</button>
        <button type="button" id="btn-menu-select" onclick="takeAction('menu_select')">Menu Select</button>
    </div>
    
    <script>
        const states = {
            0: { name: "Checkout Step 1", api: ["/api/shipping/validate", "/api/cart/summary"] },
            1: { name: "Checkout Step 2", api: ["/api/payment/methods", "/api/shipping/cost"] },
            2: { name: "Checkout Step 3", api: ["/api/payment/process", "/api/order/create"] },
            3: { name: "Dashboard Overview", api: ["/api/dashboard/stats", "/api/dashboard/recent"] },
            4: { name: "Dashboard Analytics", api: ["/api/analytics/summary", "/api/analytics/chart"] },
            5: { name: "Dashboard Settings", api: ["/api/settings/user", "/api/settings/preferences"] },
            6: { name: "Profile View", api: ["/api/profile/info", "/api/profile/activity"] },
            7: { name: "Profile Edit", api: ["/api/profile/update", "/api/profile/avatar"] }
        };
        
        const transitions = {
            0: { form_submit: 3, button_click: 4, link_nav: 6, menu_select: 7 },
            1: { form_submit: 5, button_click: 3, link_nav: 4, menu_select: 6 },
            2: { form_submit: 3, button_click: 5, link_nav: 7, menu_select: 4 },
            3: { form_submit: 0, button_click: 1, link_nav: 2, menu_select: 6 },
            4: { form_submit: 1, button_click: 2, link_nav: 0, menu_select: 7 },
            5: { form_submit: 2, button_click: 0, link_nav: 1, menu_select: 6 },
            6: { form_submit: 3, button_click: 4, link_nav: 5, menu_select: 0 },
            7: { form_submit: 5, button_click: 3, link_nav: 6, menu_select: 1 }
        };
        
        let currentState = 0;
        
        async function makeApiCall(endpoint, method) {
            try {
                const options = {
                    method: method,
                    headers: { 'Content-Type': 'application/json' }
                };
                if (method !== 'GET') {
                    options.body = JSON.stringify({ state: currentState });
                }
                const response = await fetch(endpoint, options);
                return { endpoint, method, status: response.status };
            } catch (e) {
                console.error('API call failed:', e);
                return { endpoint, method, status: 500, error: e.message };
            }
        }
        
        async function takeAction(action) {
            const nextState = transitions[currentState][action];
            console.log(`Action: ${action}, Current: ${currentState}, Next: ${nextState}`);
            
            // Make API calls for the next state
            const apiCalls = states[nextState].api;
            const results = [];
            for (const endpoint of apiCalls) {
                const method = endpoint.includes('validate') || endpoint.includes('process') || 
                              endpoint.includes('create') || endpoint.includes('update') || 
                              endpoint.includes('chart') ? 'POST' : 
                              endpoint.includes('preferences') ? 'PUT' : 'GET';
                const result = await makeApiCall(endpoint, method);
                results.push(result);
            }
            
            // Hide current state
            document.getElementById(`state-${currentState}`).classList.remove('active');
            
            // Update state
            currentState = nextState;
            
            // Show new state
            document.getElementById(`state-${currentState}`).classList.add('active');
            
            // Update display
            document.getElementById('state-display').textContent = currentState;
            
            // Log transition
            console.log(`TRANSITION:${JSON.stringify({
                from: currentState,
                to: nextState,
                action: action,
                api_calls: results
            })}`);
        }
        
        // Initial state display
        document.getElementById('state-display').textContent = currentState;
    </script>
</body>
</html>'''


def start_server(port=8765):
    """Start local HTTP server for synthetic SPA."""
    server = HTTPServer(('127.0.0.1', port), SyntheticSPAHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


# ─── Network Request Processing ───────────────────────────────────────────────

def compute_request_hash(endpoint, method, status):
    """Compute deterministic hash of a network request."""
    sig = f"{endpoint}|{method}|{status}"
    return hashlib.sha256(sig.encode()).hexdigest()[:16]


def compute_network_state_hash(request_hashes):
    """Compute deterministic hash of network request state (sorted tuple of hashes)."""
    if not request_hashes:
        return "empty"
    sorted_hashes = sorted(request_hashes)
    sig = "|".join(sorted_hashes)
    return hashlib.sha256(sig.encode()).hexdigest()[:16]


# ─── PMI Computation ─────────────────────────────────────────────────────────

def compute_pmi_stats(triples):
    """Compute PMI statistics for a set of triples.
    
    PMI(s, a, s') = log2[ P(a, s' | s) / (P(a | s) * P(s' | s)) ]
    """
    N = len(triples)
    if N == 0:
        return {"mean_pmi": 0.0, "pmi_values": [], "N": 0,
                "unique_states": 0, "unique_actions": 0, "unique_sa_pairs": 0}

    state_counts = collections.Counter()
    state_action_counts = collections.Counter()
    state_next_counts = collections.Counter()
    triple_counts = collections.Counter()

    for s, a, s_next in triples:
        state_counts[s] += 1
        state_action_counts[(s, a)] += 1
        state_next_counts[(s, s_next)] += 1
        triple_counts[(s, a, s_next)] += 1

    pmi_values = []

    for s, a, s_next in triples:
        count_s = state_counts[s]
        count_sa = state_action_counts[(s, a)]
        count_ss_next = state_next_counts[(s, s_next)]
        count_sas_next = triple_counts[(s, a, s_next)]

        distinct_actions_s = sum(1 for (si, ai) in state_action_counts if si == s)
        distinct_next_s = sum(1 for (si, sni) in state_next_counts if si == s)

        p_a_given_s = (count_sa + ALPHA) / (count_s + ALPHA * distinct_actions_s)
        p_s_next_given_s = (count_ss_next + ALPHA) / (count_s + ALPHA * distinct_next_s)
        p_joint_given_s = count_sas_next / count_s

        denom = p_a_given_s * p_s_next_given_s
        if denom > 0 and p_joint_given_s > 0:
            pmi = math.log2(p_joint_given_s / denom)
        else:
            pmi = 0.0

        pmi_values.append(pmi)

    mean_pmi = sum(pmi_values) / len(pmi_values)

    return {
        "mean_pmi": mean_pmi,
        "pmi_values": pmi_values,
        "N": N,
        "unique_states": len(state_counts),
        "unique_actions": len(set(a for _, a, _ in triples)),
        "unique_sa_pairs": len(state_action_counts),
    }


# ─── Permutation Test ────────────────────────────────────────────────────────

def permutation_test(triples, observed_mean_pmi, n_permutations, seed):
    """Permutation test for PMI significance."""
    rng = random.Random(seed)
    
    states = [t[0] for t in triples]
    actions = [t[1] for t in triples]
    next_states = [t[2] for t in triples]
    
    shuffled_means = []
    for _ in range(n_permutations):
        shuffled_next = next_states.copy()
        rng.shuffle(shuffled_next)
        shuffled_triples = list(zip(states, actions, shuffled_next))
        stats = compute_pmi_stats(shuffled_triples)
        shuffled_means.append(stats["mean_pmi"])
    
    count_gt = sum(1 for m in shuffled_means if m > observed_mean_pmi)
    p_value = (count_gt + 1) / (n_permutations + 1)
    
    null_mean = float(np.mean(shuffled_means))
    null_std = float(np.std(shuffled_means))
    effect_d = float((observed_mean_pmi - null_mean) / null_std) if null_std > 0 else 0.0
    
    return {
        "p_value": p_value,
        "shuffled_means": shuffled_means,
        "observed_mean_pmi": observed_mean_pmi,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size_d": effect_d,
    }


def null_control_permutation_test(triples, n_permutations, seed):
    """Null control: shuffle network-request labels and check PMI is not significant."""
    rng = random.Random(seed)
    
    source_hashes = [t[0] for t in triples]
    target_hashes = [t[2] for t in triples]
    actions = [t[1] for t in triples]
    
    shuffled_source = source_hashes.copy()
    shuffled_target = target_hashes.copy()
    rng.shuffle(shuffled_source)
    rng.shuffle(shuffled_target)
    
    shuffled_triples = list(zip(shuffled_source, actions, shuffled_target))
    shuffled_stats = compute_pmi_stats(shuffled_triples)
    shuffled_pmi = shuffled_stats["mean_pmi"]
    
    perm = permutation_test(shuffled_triples, shuffled_pmi, min(n_permutations, 200), seed + 1000)
    
    return {
        "shuffled_pmi": shuffled_pmi,
        "shuffled_n_transitions": len(shuffled_triples),
        "shuffled_unique_states": shuffled_stats["unique_states"],
        "permutation_p": perm["p_value"],
        "permutation_null_mean": perm["null_mean"],
        "passes": perm["p_value"] > 0.01,
    }


def compute_entropy(values):
    """Compute Shannon entropy of a list of values."""
    counts = collections.Counter(values)
    N = len(values)
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / N
            entropy -= p * math.log2(p)
    return entropy


# ─── Synthetic SPA Experiment (Positive Control) ──────────────────────────────

def run_synthetic_experiment():
    """Run experiment on synthetic SPA with deterministic network-request evolution."""
    print("=" * 70)
    print(f"SYNTHETIC SPA EXPERIMENT (Network Requests) — {EXPERIMENT_ID}")
    print("=" * 70)
    
    try:
        from playwright.sync_api import sync_playwright
        
        # Start local server
        PORT = 8765
        server = start_server(PORT)
        base_url = f"http://127.0.0.1:{PORT}"
        print(f"\n[1/6] Server started on {base_url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # Capture network requests
            captured_requests = []
            
            def handle_route(route):
                """Capture the request and let it continue."""
                request = route.request
                captured_requests.append({
                    "url": request.url,
                    "method": request.method,
                    "resource_type": request.resource_type,
                    "timestamp": time.time()
                })
                route.continue_()
            
            # Intercept all network requests
            page.route("**/*", handle_route)
            
            # Navigate to synthetic SPA
            print("\n[2/6] Navigating to synthetic SPA...")
            page.goto(base_url)
            page.wait_for_load_state("networkidle")
            captured_requests.clear()  # Clear navigation requests
            
            # Collect transitions
            transitions = []
            n_trajectories = 25
            trajectory_length = 20
            
            print(f"\n[3/6] Collecting {n_trajectories} trajectories of length {trajectory_length}...")
            
            rng = random.Random(SEED)
            actions = list(SYNTHETIC_TRANSITIONS[0].keys())
            
            for traj_id in range(n_trajectories):
                # Start at random state
                current_state = rng.choice(list(SYNTHETIC_STATES.keys()))
                
                # Navigate to initial state
                for _ in range(5):
                    action = rng.choice(actions)
                    page.evaluate(f"takeAction('{action}')")
                    page.wait_for_timeout(100)
                
                captured_requests.clear()
                # Capture initial network state
                initial_request_hashes = []
                for req in captured_requests:
                    if req["resource_type"] in ["xhr", "fetch"] or "/api/" in req["url"]:
                        parsed = urllib.parse.urlparse(req["url"])
                        req_hash = compute_request_hash(parsed.path, req["method"], 200)
                        initial_request_hashes.append(req_hash)
                prev_net_hash = compute_network_state_hash(initial_request_hashes)
                prev_url = page.url
                captured_requests.clear()
                
                # Collect transitions
                for step in range(trajectory_length):
                    url_before = prev_url
                    net_hash_before = prev_net_hash
                    captured_requests.clear()
                    
                    # Take action
                    action = rng.choice(actions)
                    page.evaluate(f"takeAction('{action}')")
                    page.wait_for_timeout(300)
                    
                    # Get captured network requests (AFTER action)
                    url_after = page.url
                    
                    request_hashes_after = []
                    for req in captured_requests:
                        if req["resource_type"] in ["xhr", "fetch"] or "/api/" in req["url"]:
                            parsed = urllib.parse.urlparse(req["url"])
                            req_hash = compute_request_hash(parsed.path, req["method"], 200)
                            request_hashes_after.append(req_hash)
                    
                    net_hash_after = compute_network_state_hash(request_hashes_after)
                    
                    transitions.append({
                        "trajectory_id": traj_id,
                        "state_before": {"url": url_before, "net_hash": net_hash_before},
                        "action": action,
                        "state_after": {"url": url_after, "net_hash": net_hash_after},
                        "n_api_calls": len(request_hashes_after)
                    })
                    
                    prev_url = url_after
                    prev_net_hash = net_hash_after
            
            print(f"  Collected {len(transitions)} transitions")
            
            # Analyze transitions
            print("\n[4/6] Analyzing transitions...")
            
            within_url_transitions = [t for t in transitions if t["state_before"]["url"] == t["state_after"]["url"]]
            all_non_leakage = transitions
            
            print(f"  Total: {len(transitions)}, Non-leakage: {len(all_non_leakage)}, Within-URL: {len(within_url_transitions)}")
            
            # Compute PMI for different state representations
            print("\n[5/6] Computing PMI...")
            
            url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in all_non_leakage]
            net_triples = [(t["state_before"]["net_hash"], t["action"], t["state_after"]["net_hash"]) for t in all_non_leakage]
            
            url_stats = compute_pmi_stats(url_triples)
            net_stats = compute_pmi_stats(net_triples)
            
            within_url_url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in within_url_transitions]
            within_url_net_triples = [(t["state_before"]["net_hash"], t["action"], t["state_after"]["net_hash"]) for t in within_url_transitions]
            
            within_url_url_stats = compute_pmi_stats(within_url_url_triples)
            within_url_net_stats = compute_pmi_stats(within_url_net_triples)
            
            print(f"  URL-only PMI (all): {url_stats['mean_pmi']:.6f} bits")
            print(f"  Net-only PMI (all): {net_stats['mean_pmi']:.6f} bits")
            print(f"  URL-only PMI (within-URL): {within_url_url_stats['mean_pmi']:.6f} bits")
            print(f"  Net-only PMI (within-URL): {within_url_net_stats['mean_pmi']:.6f} bits")
            
            # Permutation tests
            print("\n[6/6] Running permutation tests...")
            
            url_perm = permutation_test(url_triples, url_stats["mean_pmi"], N_PERMUTATIONS, SEED)
            net_perm = permutation_test(net_triples, net_stats["mean_pmi"], N_PERMUTATIONS, SEED)
            within_url_net_perm = permutation_test(within_url_net_triples, within_url_net_stats["mean_pmi"],
                                                    N_PERMUTATIONS, SEED)
            
            # Null control: shuffle network-request labels
            null_ctrl = null_control_permutation_test(net_triples, N_PERMUTATIONS, SEED)
            
            print(f"  URL-only permutation p: {url_perm['p_value']:.6f}")
            print(f"  Net-only permutation p: {net_perm['p_value']:.6f}")
            print(f"  Within-URL Net permutation p: {within_url_net_perm['p_value']:.6f}")
            print(f"  Null control shuffled PMI: {null_ctrl['shuffled_pmi']:.6f}")
            print(f"  Null control permutation p: {null_ctrl['permutation_p']:.6f}")
            print(f"  Null control passes: {null_ctrl['passes']}")
            
            # Decision evaluation
            print(f"\n{'=' * 70}")
            print("DECISION EVALUATION")
            print(f"{'=' * 70}")
            
            # Condition 1: Net PMI >= 0.5 bits (positive control)
            condition_1 = net_stats["mean_pmi"] >= 0.5
            print(f"  Condition 1: Net PMI >= 0.5 bits: {net_stats['mean_pmi']:.6f} >= 0.5 = {condition_1}")
            
            # Condition 2: Net permutation p < 0.001 (positive control)
            condition_2 = net_perm["p_value"] < 0.001
            print(f"  Condition 2: Net perm p < 0.001: {net_perm['p_value']:.6f} < 0.001 = {condition_2}")
            
            # Condition 3: Null control passes (shuffled p > 0.01)
            condition_3 = null_ctrl["passes"]
            print(f"  Condition 3: Null control (shuffled perm p > 0.01): {null_ctrl['permutation_p']:.6f} > 0.01 = {condition_3}")
            
            # Condition 4: Net state varies (entropy > 0)
            net_hashes = [t["state_before"]["net_hash"] for t in transitions]
            unique_net = len(set(net_hashes))
            net_entropy = compute_entropy(net_hashes) if net_hashes else 0.0
            condition_4 = unique_net > 1
            print(f"  Condition 4: Net state varies: {unique_net} unique hashes, entropy={net_entropy:.4f} bits > 0 = {condition_4}")
            
            # Condition 5: Data sufficiency
            condition_5 = len(all_non_leakage) >= 50
            print(f"  Condition 5: Data sufficiency: {len(all_non_leakage)} >= 50 = {condition_5}")
            
            # Overall decision
            survives = all([condition_1, condition_2, condition_3, condition_4, condition_5])
            outcome = "SUPPORTS" if survives else "FALSIFIES"
            
            print(f"\n  POSITIVE CONTROL PASSES: {survives}")
            print(f"  OUTCOME: {outcome}")
            
            # Entropy analysis
            url_entropy = compute_entropy([t["state_before"]["url"] for t in transitions])
            
            results = {
                "experiment_id": EXPERIMENT_ID,
                "synthetic_spa": {
                    "n_transitions": len(transitions),
                    "n_trajectories": n_trajectories,
                    "trajectory_length": trajectory_length,
                    "within_url_transitions": len(within_url_transitions),
                    "unique_net_hashes": unique_net,
                    "unique_urls": len(set(t["state_before"]["url"] for t in transitions)),
                },
                "pmi_results": {
                    "url_only_all": url_stats["mean_pmi"],
                    "net_only_all": net_stats["mean_pmi"],
                    "url_only_within_url": within_url_url_stats["mean_pmi"],
                    "net_only_within_url": within_url_net_stats["mean_pmi"],
                },
                "permutation_tests": {
                    "url_only": {"p_value": url_perm["p_value"], "null_mean": url_perm["null_mean"], "effect_d": url_perm["effect_size_d"]},
                    "net_only": {"p_value": net_perm["p_value"], "null_mean": net_perm["null_mean"], "effect_d": net_perm["effect_size_d"]},
                    "within_url_net": {"p_value": within_url_net_perm["p_value"], "null_mean": within_url_net_perm["null_mean"]},
                },
                "null_control": {
                    "shuffled_pmi": null_ctrl["shuffled_pmi"],
                    "permutation_p": null_ctrl["permutation_p"],
                    "permutation_null_mean": null_ctrl["permutation_null_mean"],
                    "passes": null_ctrl["passes"],
                },
                "entropy_analysis": {
                    "url_entropy": url_entropy,
                    "net_entropy": net_entropy,
                },
                "decision_conditions": {
                    "net_pmi_bits": net_stats["mean_pmi"],
                    "condition_1_net_pmi_ge_0.5": condition_1,
                    "condition_2_net_perm_p": net_perm["p_value"],
                    "condition_2_passes": condition_2,
                    "condition_3_null_control_p": null_ctrl["permutation_p"],
                    "condition_3_passes": condition_3,
                    "condition_4_net_unique_hashes": unique_net,
                    "condition_4_net_entropy_bits": net_entropy,
                    "condition_4_passes": condition_4,
                    "condition_5_data_sufficiency": len(all_non_leakage),
                    "condition_5_passes": condition_5,
                },
                "positive_control_passes": survives,
                "outcome": outcome,
                "status": "COMPLETE",
            }
            
            server.shutdown()
            return results, transitions
            
    except Exception as e:
        print(f"Synthetic SPA experiment failed: {e}")
        traceback.print_exc()
        raise


# ─── Real Site Experiment ─────────────────────────────────────────────────────

def try_dismiss_overlays(page):
    """Try to dismiss common overlay/modal elements."""
    overlay_selectors = [
        '[class*="modal"] button[class*="close"]',
        '[class*="overlay"] button[class*="close"]',
        '[class*="dialog"] button[class*="close"]',
        'button[aria-label="Close"]',
        'button[aria-label="Dismiss"]',
        '[class*="cookie"] button',
        '[class*="consent"] button',
        '[class*="banner"] button',
        '[data-testid*="close"]',
        '[class*="popup"] button',
    ]
    dismissed = 0
    for sel in overlay_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click(force=True)
                page.wait_for_timeout(300)
                dismissed += 1
        except:
            pass
    return dismissed


def try_interact_with_page(page):
    """Try various strategies to interact with the page and advance state."""
    # Strategy 1: Try Next/Continue/Submit buttons
    for text in ["Next", "Continue", "Submit", "Continue to next step", "Next step", "next"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn and btn.is_visible():
                btn.click(force=True, timeout=3000)
                return f"click_{text.lower()}"
        except:
            pass
    
    # Strategy 2: Try primary/submit buttons
    for sel in ['button[type="submit"]', 'button.primary', 'button.btn-primary', 
                'button[data-testid*="next"]', 'button[data-testid*="continue"]',
                'button[class*="next"]', 'button[class*="continue"]']:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click(force=True, timeout=2000)
                return f"click_{sel}"
        except:
            pass
    
    # Strategy 3: Try any visible button
    try:
        buttons = page.query_selector_all("button")
        for btn in buttons:
            if btn.is_visible():
                btn.click(force=True, timeout=2000)
                return "click_button"
    except:
        pass
    
    # Strategy 4: Try links
    try:
        links = page.query_selector_all("a[href]")
        for link in links:
            if link.is_visible():
                link.click(force=True, timeout=2000)
                return "click_link"
    except:
        pass
    
    # Strategy 5: Fill input and submit form
    try:
        inputs = page.query_selector_all("input:visible")
        if inputs:
            inputs[0].fill("test_value")
            inputs[0].press("Enter")
            return "fill_and_submit"
    except:
        pass
    
    return "no_action"


def run_real_site_experiment(site_name, site_url, max_steps=30):
    """Run experiment on a real form-heavy SPA with network-request interception."""
    print(f"\n{'=' * 70}")
    print(f"REAL SITE EXPERIMENT — {site_name}")
    print(f"URL: {site_url}")
    print(f"{'=' * 70}")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # Capture network requests
            captured_requests = []
            
            def handle_route(route):
                """Capture request and continue."""
                request = route.request
                captured_requests.append({
                    "url": request.url,
                    "method": request.method,
                    "resource_type": request.resource_type,
                    "timestamp": time.time()
                })
                route.continue_()
            
            page.route("**/*", handle_route)
            
            # Navigate to site
            print(f"\n[1/4] Navigating...")
            try:
                page.goto(site_url, timeout=30000, wait_until="networkidle")
            except:
                try:
                    page.goto(site_url, timeout=30000, wait_until="domcontentloaded")
                    page.wait_for_timeout(3000)
                except Exception as e:
                    print(f"  Failed to navigate: {e}")
                    return None
            
            # Dismiss overlays
            time.sleep(2)
            dismissed = try_dismiss_overlays(page)
            if dismissed:
                print(f"  Dismissed {dismissed} overlays")
            
            # Get initial URL
            initial_url = page.url
            print(f"  Initial URL: {initial_url}")
            captured_requests.clear()
            
            # Collect transitions
            transitions = []
            prev_url = initial_url
            
            for step in range(max_steps):
                # Try to interact with the page
                action = try_interact_with_page(page)
                page.wait_for_timeout(1500)
                
                # Try dismissing overlays again
                try_dismiss_overlays(page)
                
                url = page.url
                
                # Discretize network request state
                request_hashes = []
                for req in captured_requests:
                    if req["resource_type"] in ["xhr", "fetch"] or "/api/" in req["url"]:
                        parsed = urllib.parse.urlparse(req["url"])
                        req_hash = compute_request_hash(
                            parsed.path,
                            req["method"],
                            200
                        )
                        request_hashes.append(req_hash)
                
                net_state_hash = compute_network_state_hash(request_hashes)
                
                transitions.append({
                    "step": step,
                    "state_before": {"url": prev_url, "net_hash": net_state_hash},
                    "action": action,
                    "state_after": {"url": url, "net_hash": net_state_hash},
                    "n_api_calls": len(request_hashes),
                    "api_endpoints": list(set(urllib.parse.urlparse(r["url"]).path for r in captured_requests 
                                             if r["resource_type"] in ["xhr", "fetch"] or "/api/" in r["url"]))
                })
                
                captured_requests.clear()
                
                if step % 10 == 0:
                    print(f"  Step {step}: action={action}, url_changed={url != prev_url}")
                
                prev_url = url
            
            print(f"\n  Collected {len(transitions)} transitions")
            
            # Analyze
            within_url = [t for t in transitions if t["state_before"]["url"] == t["state_after"]["url"]]
            non_leakage = [t for t in transitions if t["action"] not in ["no_action"]]
            
            print(f"  Non-leakage: {len(non_leakage)}, Within-URL: {len(within_url)}")
            
            if len(non_leakage) < 10:
                print("  Insufficient transitions for reliable PMI")
                return {"site_name": site_name, "site_url": site_url, "status": "INSUFFICIENT_DATA",
                        "n_transitions": len(transitions), "n_non_leakage": len(non_leakage)}
            
            # Compute PMI
            url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in non_leakage]
            net_triples = [(t["state_before"]["net_hash"], t["action"], t["state_after"]["net_hash"]) for t in non_leakage]
            
            url_stats = compute_pmi_stats(url_triples)
            net_stats = compute_pmi_stats(net_triples)
            
            within_url_url_triples = [(t["state_before"]["url"], t["action"], t["state_after"]["url"]) for t in within_url]
            within_url_net_triples = [(t["state_before"]["net_hash"], t["action"], t["state_after"]["net_hash"]) for t in within_url]
            
            within_url_url_stats = compute_pmi_stats(within_url_url_triples) if within_url_url_triples else {"mean_pmi": 0.0}
            within_url_net_stats = compute_pmi_stats(within_url_net_triples) if within_url_net_triples else {"mean_pmi": 0.0}
            
            # Permutation tests
            url_perm = permutation_test(url_triples, url_stats["mean_pmi"], N_PERMUTATIONS, SEED) if len(url_triples) >= 10 else None
            net_perm = permutation_test(net_triples, net_stats["mean_pmi"], N_PERMUTATIONS, SEED) if len(net_triples) >= 10 else None
            within_url_net_perm = permutation_test(within_url_net_triples, within_url_net_stats["mean_pmi"], N_PERMUTATIONS, SEED) if len(within_url_net_triples) >= 10 else None
            
            # Null control
            null_ctrl = null_control_permutation_test(net_triples, N_PERMUTATIONS, SEED) if len(net_triples) >= 10 else None
            
            # Entropy
            url_entropy = compute_entropy([t["state_before"]["url"] for t in transitions])
            net_entropy = compute_entropy([t["state_before"]["net_hash"] for t in transitions])
            unique_net = len(set(t["state_before"]["net_hash"] for t in transitions))
            unique_urls = len(set(t["state_before"]["url"] for t in transitions))
            
            # Decision: does net PMI exceed URL-only by >= 0.1 bits on within-URL transitions?
            gain_within_url = within_url_net_stats["mean_pmi"] - within_url_url_stats["mean_pmi"]
            decision_condition_1 = gain_within_url >= 0.1
            decision_condition_2 = (within_url_net_perm["p_value"] < ALPHA_BONFERRONI) if within_url_net_perm else False
            
            print(f"\n  Results:")
            print(f"    URL-only PMI: {url_stats['mean_pmi']:.6f} bits")
            print(f"    Net-only PMI: {net_stats['mean_pmi']:.6f} bits")
            print(f"    URL-only PMI (within-URL): {within_url_url_stats['mean_pmi']:.6f} bits")
            print(f"    Net-only PMI (within-URL): {within_url_net_stats['mean_pmi']:.6f} bits")
            print(f"    Gain within-URL: {gain_within_url:.6f} bits")
            print(f"    Unique URLs: {unique_urls}, Unique net hashes: {unique_net}")
            print(f"    URL entropy: {url_entropy:.4f}, Net entropy: {net_entropy:.4f}")
            if url_perm:
                print(f"    URL permutation p: {url_perm['p_value']:.6f}")
            if net_perm:
                print(f"    Net permutation p: {net_perm['p_value']:.6f}")
            if within_url_net_perm:
                print(f"    Within-URL Net perm p: {within_url_net_perm['p_value']:.6f}")
            if null_ctrl:
                print(f"    Null control shuffled PMI: {null_ctrl['shuffled_pmi']:.6f}, p: {null_ctrl['permutation_p']:.6f}, passes: {null_ctrl['passes']}")
            
            results = {
                "site_name": site_name,
                "site_url": site_url,
                "status": "COMPLETE",
                "n_transitions": len(transitions),
                "n_non_leakage": len(non_leakage),
                "n_within_url": len(within_url),
                "unique_net_hashes": unique_net,
                "unique_urls": unique_urls,
                "pmi_results": {
                    "url_only_all": url_stats["mean_pmi"],
                    "net_only_all": net_stats["mean_pmi"],
                    "url_only_within_url": within_url_url_stats["mean_pmi"],
                    "net_only_within_url": within_url_net_stats["mean_pmi"],
                },
                "permutation_tests": {
                    "url_only": {"p_value": url_perm["p_value"], "null_mean": url_perm["null_mean"]} if url_perm else None,
                    "net_only": {"p_value": net_perm["p_value"], "null_mean": net_perm["null_mean"]} if net_perm else None,
                    "within_url_net": {"p_value": within_url_net_perm["p_value"], "null_mean": within_url_net_perm["null_mean"]} if within_url_net_perm else None,
                },
                "null_control": {
                    "shuffled_pmi": null_ctrl["shuffled_pmi"],
                    "permutation_p": null_ctrl["permutation_p"],
                    "passes": null_ctrl["passes"],
                } if null_ctrl else None,
                "entropy_analysis": {
                    "url_entropy": url_entropy,
                    "net_entropy": net_entropy,
                },
                "decision_conditions": {
                    "gain_within_url_bits": gain_within_url,
                    "condition_1_gain_ge_0.1": decision_condition_1,
                    "condition_2_permutation_p": within_url_net_perm["p_value"] if within_url_net_perm else None,
                    "condition_2_passes": decision_condition_2,
                },
                "raw_transitions": transitions,
            }
            
            browser.close()
            return results
            
    except Exception as e:
        print(f"  Experiment failed: {e}")
        traceback.print_exc()
        return {"site_name": site_name, "site_url": site_url, "status": "EXCEPTION", "error": str(e)}


# ─── Main Experiment ─────────────────────────────────────────────────────────

def main():
    """Run the full network request PMI experiment."""
    os.environ["PYTHONHASHSEED"] = "0"
    
    print("=" * 70)
    print(f"NETWORK REQUEST PMI EXPERIMENT — {EXPERIMENT_ID}")
    print("=" * 70)
    
    # 1. Synthetic SPA experiment (positive control)
    synthetic_results, synthetic_transitions = run_synthetic_experiment()
    
    # Save raw results
    out_dir = Path(__file__).parent
    raw_results_path = out_dir / "raw_results_network_v2.json"
    with open(raw_results_path, "w") as f:
        json.dump(synthetic_results, f, indent=2, default=str)
    print(f"\nRaw results saved to {raw_results_path}")
    
    transitions_path = out_dir / "synthetic_transitions_network_v2.json"
    with open(transitions_path, "w") as f:
        json.dump(synthetic_transitions, f, indent=2, default=str)
    
    # 2. Real site experiments (best effort, multiple candidates)
    real_site_configs = [
        ("tally_form", "https://tally.so/r/wAqjQj"),
        ("typeform", "https://form.typeform.com/to/sample"),
        ("github_new_repo", "https://github.com/new"),
    ]
    
    real_site_results = []
    for name, url in real_site_configs:
        result = run_real_site_experiment(name, url, max_steps=30)
        if result:
            real_site_results.append(result)
    
    # Save real site results
    if real_site_results:
        real_results_path = out_dir / "real_site_results_network_v2.json"
        with open(real_results_path, "w") as f:
            json.dump(real_site_results, f, indent=2, default=str)
        print(f"\nReal site results saved to {real_results_path}")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("EXPERIMENT SUMMARY")
    print(f"{'=' * 70}")
    print(f"Synthetic SPA: {synthetic_results['outcome']} (positive_control_passes={synthetic_results['positive_control_passes']})")
    print(f"Real sites tested: {len(real_site_results)}")
    for r in real_site_results:
        print(f"  {r.get('site_name', '?')}: {r.get('status', '?')}")
    
    return synthetic_results, real_site_results


if __name__ == "__main__":
    main()
