#!/usr/bin/env node
/**
 * Multi-Step Form SPA — Genuine-like SPA with URL ambiguity
 * 
 * A realistic multi-step form wizard where the same URL (/checkout)
 * hosts different states at different form steps, each triggering
 * different API calls. This simulates a real SPA checkout flow.
 */

const http = require('http');
const url = require('url');

const PORT = process.env.PORT || 3848;

// 4-step checkout flow, all on /checkout URL
const STEPS = ['shipping', 'payment', 'review', 'confirmation'];
const STEP_API_CALLS = {
  shipping: [
    { endpoint: '/api/shipping/methods', method: 'GET', status: 200 },
    { endpoint: '/api/shipping/address/validate', method: 'POST', status: 200 },
  ],
  payment: [
    { endpoint: '/api/payment/methods', method: 'GET', status: 200 },
    { endpoint: '/api/payment/token', method: 'POST', status: 201 },
    { endpoint: '/api/tax/calculate', method: 'POST', status: 200 },
  ],
  review: [
    { endpoint: '/api/order/preview', method: 'GET', status: 200 },
    { endpoint: '/api/promo/validate', method: 'POST', status: 200 },
  ],
  confirmation: [
    { endpoint: '/api/order/submit', method: 'POST', status: 201 },
    { endpoint: '/api/confirmation/send', method: 'POST', status: 202 },
  ],
};

const sessions = {};

function getSession(req) {
  const cookies = req.headers.cookie || '';
  const match = cookies.match(/session=([^;]+)/);
  let sid = match ? match[1] : null;
  if (!sid || !sessions[sid]) {
    sid = 'sess_' + Math.random().toString(36).slice(2, 10);
    sessions[sid] = { step: 0, data: {} };
  }
  return sid;
}

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);
  const path = parsed.pathname;
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  const sid = getSession(req);
  const session = sessions[sid];
  res.setHeader('Set-Cookie', `session=${sid}; Path=/`);
  
  // Serve SPA HTML
  if (path === '/' || path === '/index.html' || path === '/checkout') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    const stepName = STEPS[session.step] || 'shipping';
    res.end(`<!DOCTYPE html>
<html>
<head><title>Checkout - Step ${session.step + 1}</title></head>
<body>
<div id="app">
  <h1>Checkout</h1>
  <div id="progress">
    ${STEPS.map((s, i) => `<span class="step ${i === session.step ? 'active' : ''} ${i < session.step ? 'done' : ''}">${s}</span>`).join(' → ')}
  </div>
  <div id="step-content">
    <h2>Step ${session.step + 1}: ${stepName}</h2>
    <p>Current URL: /checkout (same for all steps)</p>
    <p>API calls for this step: ${STEP_API_CALLS[stepName].map(a => a.endpoint).join(', ')}</p>
  </div>
  <div id="actions">
    ${session.step > 0 ? '<button id="prev-btn">← Previous</button>' : ''}
    ${session.step < STEPS.length - 1 ? '<button id="next-btn">Next →</button>' : '<button id="submit-btn">Submit Order</button>'}
  </div>
</div>
<script>
// Client-side routing: all on /checkout
document.getElementById('next-btn')?.addEventListener('click', async () => {
  const resp = await fetch('/api/checkout/next', { method: 'POST' });
  const data = await resp.json();
  // Push state (same URL!)
  history.pushState({ step: data.step }, '', '/checkout');
  location.reload();
});

document.getElementById('prev-btn')?.addEventListener('click', async () => {
  const resp = await fetch('/api/checkout/prev', { method: 'POST' });
  const data = await resp.json();
  history.pushState({ step: data.step }, '', '/checkout');
  location.reload();
});

document.getElementById('submit-btn')?.addEventListener('click', async () => {
  const resp = await fetch('/api/order/submit', { method: 'POST' });
  const data = await resp.json();
  alert('Order submitted!');
});

history.replaceState({ step: ${session.step} }, '', '/checkout');
</script>
</body>
</html>`);
    return;
  }
  
  // API: next step
  if (path === '/api/checkout/next' && req.method === 'POST') {
    if (session.step < STEPS.length - 1) {
      session.step++;
      const stepName = STEPS[session.step];
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ step: session.step, stepName, apis: STEP_API_CALLS[stepName] }));
    } else {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Already at last step' }));
    }
    return;
  }
  
  // API: prev step
  if (path === '/api/checkout/prev' && req.method === 'POST') {
    if (session.step > 0) {
      session.step--;
      const stepName = STEPS[session.step];
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ step: session.step, stepName, apis: STEP_API_CALLS[stepName] }));
    } else {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Already at first step' }));
    }
    return;
  }
  
  // API: order submit
  if (path === '/api/order/submit' && req.method === 'POST') {
    res.writeHead(201, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ orderId: 'ORD-' + Date.now(), status: 'submitted' }));
    return;
  }
  
  // API: step-specific endpoints
  const apiMatch = path.match(/^\/api\/(.+)/);
  if (apiMatch) {
    const apiName = apiMatch[1];
    // Return a generic response for any API call
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ api: apiName, status: 'ok', timestamp: Date.now() }));
    return;
  }
  
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
  console.log(`Multi-Step Form SPA running on http://localhost:${PORT}`);
  console.log(`All steps served at /checkout URL`);
});
