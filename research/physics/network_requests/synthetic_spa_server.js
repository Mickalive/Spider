#!/usr/bin/env node
/**
 * Synthetic SPA Positive Control Server
 * 
 * 8 states, 4 actions, each (state, action) triggers a distinct
 * endpoint+method+status combination.
 * 
 * This verifies the PMI computation pipeline correctly detects
 * network-request structure when present.
 */

const http = require('http');
const url = require('url');

const PORT = process.env.PORT || 3847;

// State machine: 8 states, 4 actions
// Each (state, action) pair triggers a distinct endpoint+method+status
const STATES = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'];
const ACTIONS = ['act_a', 'act_b', 'act_c', 'act_d'];

// Deterministic transition table: state_machine[state][action] = next_state
const STATE_MACHINE = {
  'S0': { 'act_a': 'S1', 'act_b': 'S2', 'act_c': 'S3', 'act_d': 'S4' },
  'S1': { 'act_a': 'S2', 'act_b': 'S3', 'act_c': 'S4', 'act_d': 'S5' },
  'S2': { 'act_a': 'S3', 'act_b': 'S4', 'act_c': 'S5', 'act_d': 'S6' },
  'S3': { 'act_a': 'S4', 'act_b': 'S5', 'act_c': 'S6', 'act_d': 'S7' },
  'S4': { 'act_a': 'S5', 'act_b': 'S6', 'act_c': 'S7', 'act_d': 'S0' },
  'S5': { 'act_a': 'S6', 'act_b': 'S7', 'act_c': 'S0', 'act_d': 'S1' },
  'S6': { 'act_a': 'S7', 'act_b': 'S0', 'act_c': 'S1', 'act_d': 'S2' },
  'S7': { 'act_a': 'S0', 'act_b': 'S1', 'act_c': 'S2', 'act_d': 'S3' },
};

// Network request signature for each (state, action) pair
// Each triggers a distinct endpoint+method+status
const NETWORK_SIGNATURES = {};
for (const state of STATES) {
  NETWORK_SIGNATURES[state] = {};
  for (const action of ACTIONS) {
    const next_state = STATE_MACHINE[state][action];
    const state_idx = parseInt(state.slice(1));
    const action_idx = ACTIONS.indexOf(action);
    // Each combination gets a unique endpoint, method, and status
    const methods = ['GET', 'POST', 'PUT', 'DELETE'];
    const statuses = [200, 201, 202, 204];
    const method = methods[action_idx];
    const status = statuses[(state_idx + action_idx) % 4];
    const endpoint = `/api/state/${state_idx}/action/${action_idx}/next/${parseInt(next_state.slice(1))}`;
    
    NETWORK_SIGNATURES[state][action] = {
      endpoint,
      method,
      status,
      contentType: 'application/json',
      body: JSON.stringify({ from: state, action, to: next_state })
    };
  }
}

// Current state tracking (per session via cookie)
const sessions = {};

function getOrCreateSession(req) {
  const cookies = req.headers.cookie || '';
  const match = cookies.match(/session=([^;]+)/);
  let sid = match ? match[1] : null;
  if (!sid || !sessions[sid]) {
    sid = 'sess_' + Math.random().toString(36).slice(2, 10);
    sessions[sid] = { state: 'S0' };
  }
  return sid;
}

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);
  const path = parsed.pathname;
  
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  const sid = getOrCreateSession(req);
  const session = sessions[sid];
  res.setHeader('Set-Cookie', `session=${sid}; Path=/`);
  
  // Serve SPA HTML
  if (path === '/' || path === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`<!DOCTYPE html>
<html>
<head><title>Synthetic SPA Control</title></head>
<body>
<div id="app">
  <p>State: <span id="current-state">${session.state}</span></p>
  <div id="actions">
    ${ACTIONS.map(a => `<button class="action-btn" data-action="${a}">${a}</button>`).join('\n    ')}
  </div>
  <div id="history"></div>
</div>
<script>
// Client-side routing with history API
window.addEventListener('popstate', (e) => {
  if (e.state && e.state.state) {
    updateUI(e.state.state);
  }
});

function updateUI(state) {
  document.getElementById('current-state').textContent = state;
}

document.querySelectorAll('.action-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const action = btn.dataset.action;
    // Trigger network request (simulated SPA action)
    const resp = await fetch('/api/action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    });
    const data = await resp.json();
    // Push state (client-side route)
    history.pushState({ state: data.to }, '', '#state/' + data.to);
    updateUI(data.to);
  });
});

// Initialize from current state
history.replaceState({ state: '${session.state}' }, '', '#state/${session.state}');
</script>
</body>
</html>`);
    return;
  }
  
  // API endpoint: perform action
  if (path === '/api/action' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { action } = JSON.parse(body);
        const current = session.state;
        
        if (!ACTIONS.includes(action)) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Invalid action' }));
          return;
        }
        
        const sig = NETWORK_SIGNATURES[current][action];
        const next_state = STATE_MACHINE[current][action];
        
        // Update session state
        session.state = next_state;
        
        // Return the response with the network signature
        res.writeHead(sig.status, { 'Content-Type': sig.contentType });
        res.end(sig.body);
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }
  
  // State-specific API endpoints (for observation)
  const stateMatch = path.match(/^\/api\/state\/(\d+)/);
  if (stateMatch && req.method === 'GET') {
    const stateIdx = parseInt(stateMatch[1]);
    const state = 'S' + stateIdx;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ state, actions: ACTIONS }));
    return;
  }
  
  // 404
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
  console.log(`Synthetic SPA server running on http://localhost:${PORT}`);
  console.log(`States: ${STATES.join(', ')}`);
  console.log(`Actions: ${ACTIONS.join(', ')}`);
});
