#!/usr/bin/env node
/**
 * Tabbed Dashboard SPA — Client-side routed with different API calls per tab
 * 
 * Same URL (/dashboard) but different tabs trigger different API endpoints.
 * This is a more realistic SPA with genuine within-URL network-request variation.
 */

const http = require('http');
const url = require('url');

const PORT = process.env.PORT || 3849;

const TABS = ['overview', 'analytics', 'users', 'settings'];
const TAB_APIS = {
  overview: [
    { endpoint: '/api/dashboard/stats', method: 'GET', status: 200 },
    { endpoint: '/api/dashboard/recent', method: 'GET', status: 200 },
  ],
  analytics: [
    { endpoint: '/api/analytics/metrics', method: 'GET', status: 200 },
    { endpoint: '/api/analytics/trends', method: 'GET', status: 200 },
    { endpoint: '/api/analytics/segments', method: 'POST', status: 200, body: '{"period":"7d"}' },
  ],
  users: [
    { endpoint: '/api/users/list', method: 'GET', status: 200 },
    { endpoint: '/api/users/roles', method: 'GET', status: 200 },
    { endpoint: '/api/users/permissions', method: 'POST', status: 200, body: '{"resource":"all"}' },
  ],
  settings: [
    { endpoint: '/api/settings/config', method: 'GET', status: 200 },
    { endpoint: '/api/settings/notifications', method: 'GET', status: 200 },
    { endpoint: '/api/settings/audit-log', method: 'POST', status: 201, body: '{"action":"view"}' },
  ],
};

const sessions = {};

function getSession(req) {
  const cookies = req.headers.cookie || '';
  const match = cookies.match(/session=([^;]+)/);
  let sid = match ? match[1] : null;
  if (!sid || !sessions[sid]) {
    sid = 'sess_' + Math.random().toString(36).slice(2, 10);
    sessions[sid] = { currentTab: 'overview' };
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
  if (path === '/' || path === '/dashboard' || path === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
<div id="app">
  <h1>Dashboard</h1>
  <nav id="tabs">
    ${TABS.map(t => `<button class="tab-btn" data-tab="${t}" ${t === session.currentTab ? 'style="font-weight:bold"' : ''}>${t}</button>`).join(' ')}
  </nav>
  <div id="content">
    <p>Current tab: <span id="current-tab">${session.currentTab}</span></p>
    <p>URL: /dashboard (same for all tabs)</p>
  </div>
</div>
<script>
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const tab = btn.dataset.tab;
    // Client-side navigation (same URL)
    history.pushState({ tab }, '', '/dashboard');
    document.getElementById('current-tab').textContent = tab;
    // Trigger tab-specific API calls
    const resp = await fetch('/api/tab/' + tab);
    const data = await resp.json();
  });
});
history.replaceState({ tab: '${session.currentTab}' }, '', '/dashboard');
</script>
</body>
</html>`);
    return;
  }
  
  // Tab switch API
  const tabMatch = path.match(/^\/api\/tab\/(.+)/);
  if (tabMatch && req.method === 'GET') {
    const tab = tabMatch[1];
    session.currentTab = TABS.includes(tab) ? tab : 'overview';
    
    // Return tab-specific data
    const apis = TAB_APIS[session.currentTab];
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ tab: session.currentTab, apis, timestamp: Date.now() }));
    return;
  }
  
  // Generic API endpoint
  const apiMatch = path.match(/^\/api\/(.+)/);
  if (apiMatch) {
    const apiName = apiMatch[1];
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      // Find matching API definition
      let status = 200;
      for (const tab of TABS) {
        for (const api of TAB_APIS[tab]) {
          if (api.endpoint.includes(apiName)) {
            status = api.status;
            break;
          }
        }
      }
      res.writeHead(status, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ api: apiName, status: 'ok', body: body || null, timestamp: Date.now() }));
    });
    return;
  }
  
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
  console.log(`Tabbed Dashboard SPA running on http://localhost:${PORT}`);
  console.log(`All tabs served at /dashboard URL`);
  console.log(`Tabs: ${TABS.join(', ')}`);
});
