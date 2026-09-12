#!/usr/bin/env node
/**
 * Stateful Wizard SPA — Same URL, different API calls per step
 * 
 * A multi-step wizard where each step's API calls include the current
 * step number in the request body, creating distinct network signatures.
 */

const http = require('http');
const url = require('url');

const PORT = process.env.PORT || 3850;

const STEPS = ['personal_info', 'address', 'payment', 'review'];
const STEP_APIS = {
  personal_info: [
    { endpoint: '/api/wizard/validate', method: 'POST', status: 200, bodyPrefix: '{"step":"personal_info","fields":["name","email"]}' },
    { endpoint: '/api/wizard/suggest', method: 'GET', status: 200 },
  ],
  address: [
    { endpoint: '/api/wizard/validate', method: 'POST', status: 200, bodyPrefix: '{"step":"address","fields":["street","city","zip"]}' },
    { endpoint: '/api/geocode', method: 'POST', status: 200, bodyPrefix: '{"step":"address"}' },
  ],
  payment: [
    { endpoint: '/api/wizard/validate', method: 'POST', status: 200, bodyPrefix: '{"step":"payment","fields":["card","expiry"]}' },
    { endpoint: '/api/payment/tokenize', method: 'POST', status: 201, bodyPrefix: '{"step":"payment"}' },
    { endpoint: '/api/tax/calculate', method: 'POST', status: 200, bodyPrefix: '{"step":"payment"}' },
  ],
  review: [
    { endpoint: '/api/wizard/validate', method: 'POST', status: 200, bodyPrefix: '{"step":"review"}' },
    { endpoint: '/api/order/preview', method: 'GET', status: 200 },
  ],
};

const sessions = {};

function getSession(req) {
  const cookies = req.headers.cookie || '';
  const match = cookies.match(/session=([^;]+)/);
  let sid = match ? match[1] : null;
  if (!sid || !sessions[sid]) {
    sid = 'sess_' + Math.random().toString(36).slice(2, 10);
    sessions[sid] = { step: 0 };
  }
  return sid;
}

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);
  const path = parsed.pathname;
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  
  const sid = getSession(req);
  const session = sessions[sid];
  res.setHeader('Set-Cookie', `session=${sid}; Path=/`);
  
  // Serve SPA HTML
  if (path === '/' || path === '/wizard') {
    const stepName = STEPS[session.step] || 'personal_info';
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`<!DOCTYPE html>
<html>
<head><title>Wizard - Step ${session.step + 1}</title></head>
<body>
<div id="app">
  <h1>Wizard</h1>
  <div id="progress">${STEPS.map((s, i) => `<span class="step ${i === session.step ? 'active' : ''}">${s}</span>`).join(' → ')}</div>
  <p>Step: <span id="current-step">${stepName}</span></p>
  <div id="actions">
    ${session.step > 0 ? '<button id="prev-btn">← Back</button>' : ''}
    ${session.step < STEPS.length - 1 ? '<button id="next-btn">Next →</button>' : '<button id="submit-btn">Submit</button>'}
  </div>
</div>
<script>
async function doStep(action) {
  const resp = await fetch('/api/wizard/' + action, { method: 'POST' });
  const data = await resp.json();
  history.pushState({ step: data.step }, '', '/wizard');
  location.reload();
}
document.getElementById('next-btn')?.addEventListener('click', () => doStep('next'));
document.getElementById('prev-btn')?.addEventListener('click', () => doStep('prev'));
document.getElementById('submit-btn')?.addEventListener('click', () => doStep('submit'));
history.replaceState({ step: ${session.step} }, '', '/wizard');
</script>
</body>
</html>`);
    return;
  }
  
  // Wizard step APIs
  if (path === '/api/wizard/next' && req.method === 'POST') {
    if (session.step < STEPS.length - 1) session.step++;
    const stepName = STEPS[session.step];
    const apis = STEP_APIS[stepName];
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ step: session.step, stepName, apis: apis.map(a => a.endpoint) }));
    return;
  }
  
  if (path === '/api/wizard/prev' && req.method === 'POST') {
    if (session.step > 0) session.step--;
    const stepName = STEPS[session.step];
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ step: session.step, stepName }));
    return;
  }
  
  if (path === '/api/wizard/submit' && req.method === 'POST') {
    res.writeHead(201, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ orderId: 'WIZ-' + Date.now(), status: 'submitted' }));
    return;
  }
  
  // Generic API
  const apiMatch = path.match(/^\/api\/(.+)/);
  if (apiMatch) {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ api: apiMatch[1], body: body || null, timestamp: Date.now() }));
    });
    return;
  }
  
  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`Stateful Wizard SPA running on http://localhost:${PORT}`);
  console.log(`All steps at /wizard URL`);
});
