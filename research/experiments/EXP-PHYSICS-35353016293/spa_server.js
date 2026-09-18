#!/usr/bin/env node
/**
 * EXP-PHYSICS-35353016293 — Locally-hosted production-like SPA simulation.
 *
 * 12 states, hash-based routing, stochastic transitions conditioned on
 * previous 2 states (K=2).  This creates genuine beyond-Markov structure:
 * (url_before, H_K=3) does NOT fully determine url_after because the
 * transition depends on url_{t-2} which is outside H_K=3 when H_K=3
 * only contains actions.
 *
 * Actions: form_submit, button_click, js_navigate, menu_select
 *
 * Transition design:
 *   For each state s, there are 4 possible successor states for each action.
 *   Which successor is chosen depends on the previous-2-state pair
 *   (prev1, prev2).  Different (prev1, prev2) contexts select different
 *   successors with probability, creating stochastic beyond-Markov transitions.
 */

const http = require("http");
const crypto = require("crypto");

const PORT = 18973;

// ── State definitions ──────────────────────────────────────────────
// 12 unique hash routes.  Multiple states share the same base path
// but differ in hash fragments, testing fragment-aware PMI.
const STATES = {
  0:  { path: "/",          hash: "home",        label: "Home" },
  1:  { path: "/app",       hash: "dashboard",   label: "Dashboard" },
  2:  { path: "/app",       hash: "analytics",   label: "Analytics" },
  3:  { path: "/user",      hash: "profile",     label: "Profile" },
  4:  { path: "/user",      hash: "settings",    label: "Settings" },
  5:  { path: "/app",       hash: "search",      label: "Search" },
  6:  { path: "/app",       hash: "notifications", label: "Notifications" },
  7:  { path: "/admin",     hash: "users",       label: "Admin Users" },
  8:  { path: "/admin",     hash: "reports",     label: "Admin Reports" },
  9:  { path: "/docs",      hash: "getting-started", label: "Docs Start" },
  10: { path: "/docs",      hash: "api-ref",     label: "Docs API" },
  11: { path: "/docs",      hash: "changelog",   label: "Docs Changelog" },
};

const ACTIONS = ["form_submit", "button_click", "js_navigate", "menu_select"];

// ── Transition table ────────────────────────────────────────────────
// For each (current_state, action) pair, we define 4 candidate successor
// states.  The actual successor chosen at runtime depends on the pair
// (prev1_state, prev2_state) — the two states immediately before current.
// This creates genuine beyond-Markov structure: same (url, action) can
// lead to different next states depending on where you came from.
//
// Selection: hash of (prev1, prev2, current, action, salt) mod 4 → index
// into candidates list.  This is deterministic given full history but
// stochastic from the perspective of an observer who only sees the
// current URL and recent action history.
const CANDIDATES = {
  // State 0: /#home
  0: {
    form_submit:   [1, 5, 3, 9],
    button_click:  [2, 6, 4, 10],
    js_navigate:   [3, 7, 5, 11],
    menu_select:   [4, 8, 1, 6],
  },
  // State 1: /app#dashboard
  1: {
    form_submit:   [2, 5, 7, 3],
    button_click:  [4, 0, 8, 10],
    js_navigate:   [6, 3, 9, 1],
    menu_select:   [5, 7, 11, 4],
  },
  // State 2: /app#analytics
  2: {
    form_submit:   [1, 6, 0, 8],
    button_click:  [3, 5, 9, 4],
    js_navigate:   [7, 1, 10, 2],
    menu_select:   [0, 8, 3, 11],
  },
  // State 3: /user#profile
  3: {
    form_submit:   [4, 0, 6, 10],
    button_click:  [1, 7, 5, 11],
    js_navigate:   [2, 8, 0, 9],
    menu_select:   [5, 9, 4, 1],
  },
  // State 4: /user#settings
  4: {
    form_submit:   [3, 1, 8, 0],
    button_click:  [6, 2, 7, 11],
    js_navigate:   [5, 0, 3, 10],
    menu_select:   [7, 10, 6, 2],
  },
  // State 5: /app#search
  5: {
    form_submit:   [0, 3, 11, 6],
    button_click:  [1, 4, 8, 2],
    js_navigate:   [9, 6, 0, 7],
    menu_select:   [10, 2, 5, 3],
  },
  // State 6: /app#notifications
  6: {
    form_submit:   [2, 8, 0, 4],
    button_click:  [3, 9, 7, 1],
    js_navigate:   [4, 10, 1, 5],
    menu_select:   [1, 11, 3, 8],
  },
  // State 7: /admin#users
  7: {
    form_submit:   [8, 1, 3, 5],
    button_click:  [9, 0, 6, 2],
    js_navigate:   [10, 4, 0, 8],
    menu_select:   [11, 5, 7, 1],
  },
  // State 8: /admin#reports
  8: {
    form_submit:   [7, 2, 0, 6],
    button_click:  [10, 3, 1, 9],
    js_navigate:   [11, 5, 4, 0],
    menu_select:   [9, 0, 8, 3],
  },
  // State 9: /docs#getting-started
  9: {
    form_submit:   [10, 0, 2, 7],
    button_click:  [11, 1, 5, 3],
    js_navigate:   [0, 4, 8, 6],
    menu_select:   [1, 6, 10, 4],
  },
  // State 10: /docs#api-ref
  10: {
    form_submit:   [11, 4, 1, 9],
    button_click:  [0, 5, 3, 8],
    js_navigate:   [1, 6, 7, 2],
    menu_select:   [3, 7, 11, 5],
  },
  // State 11: /docs#changelog
  11: {
    form_submit:   [9, 3, 5, 1],
    button_click:  [10, 2, 6, 0],
    js_navigate:   [0, 7, 4, 8],
    menu_select:   [2, 8, 10, 3],
  },
};

// State to track sessions (prev1, prev2) for each session ID
const sessions = {};

function getUrl(state) {
  const s = STATES[state];
  return `${s.path}#${s.hash}`;
}

function getStateFromUrl(url) {
  for (const [id, s] of Object.entries(STATES)) {
    if (`${s.path}#${s.hash}` === url) return parseInt(id);
  }
  return null;
}

function chooseNext(current, action, prev1, prev2) {
  const candidates = CANDIDATES[current][action];
  // Deterministic but history-dependent selection
  const hash = crypto
    .createHash("sha256")
    .update(`${prev1}:${prev2}:${current}:${action}`)
    .digest("hex");
  const idx = parseInt(hash.substring(0, 8), 16) % candidates.length;
  return candidates[idx];
}

const SPA_HTML = `<!DOCTYPE html>
<html>
<head>
<title>SPA Simulation</title>
<style>
  body { font-family: sans-serif; margin: 20px; }
  .state-info { padding: 10px; border: 1px solid #ccc; margin: 10px 0; }
  button { margin: 5px; padding: 8px 16px; }
  form { margin: 10px 0; }
  .actions { margin: 10px 0; }
  .status { color: #666; font-size: 0.9em; }
</style>
</head>
<body>
<div id="app">
  <div class="state-info">
    <strong>State:</strong> <span id="state-label">Loading...</span><br>
    <span class="status">URL: <span id="url-display"></span></span>
  </div>
  <div class="actions">
    <h3>Actions</h3>
    <button id="btn-form" onclick="doAction('form_submit')">Form Submit</button>
    <button id="btn-click" onclick="doAction('button_click')">Button Click</button>
    <button id="btn-nav" onclick="doAction('js_navigate')">JS Navigate</button>
    <button id="btn-menu" onclick="doAction('menu_select')">Menu Select</button>
  </div>
  <div id="content"></div>
  <div class="status" id="transition-log"></div>
</div>
<script>
function getStateFromHash() {
  const hash = window.location.hash.substring(1);
  const path = window.location.pathname;
  const stateMap = {
    '/#home': 0, '/app#dashboard': 1, '/app#analytics': 2,
    '/user#profile': 3, '/user#settings': 4, '/app#search': 5,
    '/app#notifications': 6, '/admin#users': 7, '/admin#reports': 8,
    '/docs#getting-started': 9, '/docs#api-ref': 10, '/docs#changelog': 11
  };
  return stateMap[path + '#' + hash] !== undefined ? stateMap[path + '#' + hash] : 0;
}

function updateUI() {
  const state = getStateFromHash();
  const labels = ['Home','Dashboard','Analytics','Profile','Settings',
                  'Search','Notifications','Admin Users','Admin Reports',
                  'Docs Start','Docs API','Docs Changelog'];
  document.getElementById('state-label').textContent = labels[state] + ' (State ' + state + ')';
  document.getElementById('url-display').textContent = window.location.href;
  document.getElementById('content').innerHTML =
    '<div class="state-info"><p>Current state: ' + state + '</p>' +
    '<p>URL: ' + window.location.pathname + '#' + window.location.hash.substring(1) + '</p></div>';
}

function doAction(action) {
  // Store current URL before navigating
  const beforeUrl = window.location.pathname + '#' + window.location.hash.substring(1);
  document.cookie = 'spider_before_url=' + encodeURIComponent(beforeUrl) + ';path=/';

  // Store action in cookie
  document.cookie = 'spider_action=' + action + ';path=/';

  // Navigate to a random state (the server will handle the actual transition logic)
  // We use hash-based navigation to stay within the SPA
  const currentState = getStateFromHash();
  const randomNext = Math.floor(Math.random() * 12);
  const paths = ['/', '/app', '/app', '/user', '/user', '/app', '/app', '/admin', '/admin', '/docs', '/docs', '/docs'];
  const hashes = ['home', 'dashboard', 'analytics', 'profile', 'settings', 'search', 'notifications', 'users', 'reports', 'getting-started', 'api-ref', 'changelog'];

  // Actually, we should let the server control transitions for beyond-Markov structure.
  // Use XHR to get the next state from the server.
  const xhr = new XMLHttpRequest();
  xhr.open('GET', '/api/transition?state=' + currentState + '&action=' + action, false);
  xhr.send();
  if (xhr.status === 200) {
    const resp = JSON.parse(xhr.responseText);
    window.location.href = paths[resp.next_state] + '#' + hashes[resp.next_state];
  }
  updateUI();
}

window.addEventListener('hashchange', updateUI);
window.addEventListener('load', updateUI);
updateUI();
</script>
</body>
</html>`;

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (url.pathname === "/api/transition") {
    // API endpoint: given current state and action, return next state
    const state = parseInt(url.searchParams.get("state"));
    const action = url.searchParams.get("action");
    const sessionId = url.searchParams.get("session") || "default";

    if (isNaN(state) || !ACTIONS.includes(action)) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Invalid state or action" }));
      return;
    }

    // Initialize session
    if (!sessions[sessionId]) {
      sessions[sessionId] = { prev1: state, prev2: state };
    }

    const sess = sessions[sessionId];
    const next_state = chooseNext(state, action, sess.prev1, sess.prev2);

    // Update history
    sess.prev2 = sess.prev1;
    sess.prev1 = state;

    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      next_state,
      url_before: getUrl(state),
      url_after: getUrl(next_state),
      action_primitive: action,
      session: sessionId,
    }));
  } else if (url.pathname === "/api/reset") {
    // Reset session
    const sessionId = url.searchParams.get("session") || "default";
    delete sessions[sessionId];
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
  } else if (url.pathname === "/api/state") {
    // Return current state info
    const sessionId = url.searchParams.get("session") || "default";
    const sess = sessions[sessionId];
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      session: sessionId,
      prev1: sess ? sess.prev1 : null,
      prev2: sess ? sess.prev2 : null,
    }));
  } else {
    // Serve SPA HTML
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(SPA_HTML);
  }
});

server.listen(PORT, () => {
  console.log(`SPA simulation server running on http://localhost:${PORT}`);
  console.log(`States: ${Object.keys(STATES).length}`);
  console.log(`Actions: ${ACTIONS.join(", ")}`);
});
