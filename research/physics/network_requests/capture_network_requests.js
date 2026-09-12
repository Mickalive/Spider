#!/usr/bin/env node
/**
 * Playwright Network-Request Capture — Master Script
 * 
 * Captures network requests via page.route() interception on:
 * 1. Synthetic SPA positive control (8 states, 4 actions)
 * 2. Multi-step form SPA (4-step checkout, same URL)
 * 3. Public API playground sites (HTTPBin, JSONPlaceholder)
 * 
 * Output: raw_network_captures.json with all transitions
 */

const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const EXPERIMENT_ID = 'EXP-PHYSICS-34674671762';
const OUTPUT_DIR = path.join(__dirname, '..', '..', 'experiments', EXPERIMENT_ID);
const SCRIPT_DIR = __dirname;

// ─── Server Management ────────────────────────────────────────────────────

function startServer(script, port) {
  return new Promise((resolve, reject) => {
    const server = spawn('node', [path.join(SCRIPT_DIR, script)], {
      env: { ...process.env, PORT: port.toString() },
      stdio: ['ignore', 'pipe', 'pipe']
    });
    
    let started = false;
    server.stdout.on('data', (data) => {
      const msg = data.toString();
      console.log(`  [${script}] ${msg.trim()}`);
      if (!started && msg.includes('running on')) {
        started = true;
        resolve(server);
      }
    });
    
    server.stderr.on('data', (data) => {
      console.error(`  [${script}] ERROR: ${data.toString().trim()}`);
    });
    
    setTimeout(() => {
      if (!started) {
        started = true;
        resolve(server); // Assume started after timeout
      }
    }, 3000);
    
    server.on('error', reject);
  });
}

function stopServer(server) {
  if (server && !server.killed) {
    server.kill('SIGTERM');
  }
}

// ─── Capture Helpers ──────────────────────────────────────────────────────

function normalizeUrl(urlStr) {
  if (!urlStr) return urlStr;
  try {
    const u = new URL(urlStr);
    let p = u.pathname;
    if (p.endsWith('/') && p.length > 1) p = p.slice(0, -1);
    return `${u.origin}${p}`;
  } catch {
    return urlStr;
  }
}

function isStaticAsset(url) {
  return /\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|ttf|map|font)(\?|$)/i.test(url);
}

// ─── Synthetic SPA Capture ───────────────────────────────────────────────

async function captureSyntheticSPA(serverUrl, nTrajectories = 10, stepsPerTraj = 25) {
  console.log(`\n[Synthetic SPA] Capturing from ${serverUrl} (${nTrajectories} trajectories x ${stepsPerTraj} steps)`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const transitions = [];
  const ACTIONS = ['act_a', 'act_b', 'act_c', 'act_d'];
  
  for (let traj = 0; traj < nTrajectories; traj++) {
    await page.goto(serverUrl, { waitUntil: 'domcontentloaded' });
    let currentUrl = page.url();
    
    for (let step = 0; step < stepsPerTraj; step++) {
      const capturedRequests = [];
      
      const routeHandler = async (route) => {
        const request = route.request();
        const entry = {
          endpoint_url: request.url(),
          http_method: request.method(),
          timestamp: Date.now(),
          request_body: ''
        };
        // Capture POST/PUT body
        if (request.method() === 'POST' || request.method() === 'PUT') {
          try {
            entry.request_body = request.postData() || '';
          } catch(e) {}
        }
        capturedRequests.push(entry);
        await route.continue();
      };
      
      await page.route('**/*', routeHandler);
      
      const action = ACTIONS[Math.floor(Math.random() * ACTIONS.length)];
      
      try {
        await page.click(`[data-action="${action}"]`);
        await page.waitForTimeout(300);
        
        const newUrl = page.url();
        
        // Get response info
        const responses = await page.evaluate(() => {
          return performance.getEntriesByType('resource').slice(-10).map(r => ({
            name: r.name,
            responseStatus: r.responseStatus || 200
          }));
        });
        
        const enrichedRequests = capturedRequests
          .filter(r => !isStaticAsset(r.endpoint_url))
          .map(r => {
            const resp = responses.find(res => r.endpoint_url === res.name);
            return {
              ...r,
              status_code: resp ? resp.responseStatus : 200,
              content_type: 'application/json'
            };
          });
        
        transitions.push({
          trajectory_id: `synthetic_${traj}`,
          state_before: { url: currentUrl },
          action: { type: 'button_click', target_href: action },
          state_after: { url: newUrl },
          network_requests: enrichedRequests,
          step: step,
          url_changed: normalizeUrl(currentUrl) !== normalizeUrl(newUrl)
        });
        
        currentUrl = newUrl;
      } catch (e) {
        // Silently continue
      }
      
      await page.unroute('**/*', routeHandler);
    }
    
    if (traj % 5 === 4) process.stdout.write(`  Completed ${traj + 1} trajectories\r`);
  }
  
  await browser.close();
  console.log(`  [Synthetic SPA] Captured ${transitions.length} transitions total`);
  return transitions;
}

// ─── Multi-Step Form SPA Capture ─────────────────────────────────────────

async function captureMultistepFormSPA(serverUrl, nTrajectories = 10, stepsPerTraj = 12) {
  console.log(`\n[Multi-Step Form SPA] Capturing from ${serverUrl} (${nTrajectories} trajectories x ${stepsPerTraj} steps)`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const transitions = [];
  
  for (let traj = 0; traj < nTrajectories; traj++) {
    // Fresh session for each trajectory
    await context.clearCookies();
    await page.goto(serverUrl, { waitUntil: 'domcontentloaded' });
    let currentUrl = page.url();
    
    for (let step = 0; step < stepsPerTraj; step++) {
      const capturedRequests = [];
      
      const routeHandler = async (route) => {
        const request = route.request();
        const entry = {
          endpoint_url: request.url(),
          http_method: request.method(),
          timestamp: Date.now(),
          request_body: ''
        };
        if (request.method() === 'POST' || request.method() === 'PUT') {
          try { entry.request_body = request.postData() || ''; } catch(e) {}
        }
        capturedRequests.push(entry);
        await route.continue();
      };
      
      await page.route('**/*', routeHandler);
      
      try {
        // Alternate between next and prev buttons
        let interaction;
        if (step % 3 === 0 && step > 0) {
          // Go back sometimes
          const prevBtn = await page.$('#prev-btn');
          if (prevBtn) {
            interaction = { type: 'button_click', href: 'prev' };
            await prevBtn.click();
          } else {
            const nextBtn = await page.$('#next-btn') || await page.$('#submit-btn');
            if (nextBtn) {
              interaction = { type: 'button_click', href: 'next' };
              await nextBtn.click();
            }
          }
        } else {
          const nextBtn = await page.$('#next-btn') || await page.$('#submit-btn');
          if (nextBtn) {
            interaction = { type: 'button_click', href: 'next' };
            await nextBtn.click();
          }
        }
        
        await page.waitForTimeout(500);
        
        const newUrl = page.url();
        
        const responses = await page.evaluate(() => {
          return performance.getEntriesByType('resource')
            .filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest')
            .slice(-10)
            .map(r => ({
              name: r.name,
              responseStatus: r.responseStatus || 200
            }));
        });
        
        const enrichedRequests = capturedRequests
          .filter(r => !isStaticAsset(r.endpoint_url))
          .map(r => {
            const resp = responses.find(res => r.endpoint_url === res.name);
            return {
              ...r,
              status_code: resp ? resp.responseStatus : 200,
              content_type: 'application/json'
            };
          });
        
        transitions.push({
          trajectory_id: `multistep_${traj}`,
          state_before: { url: currentUrl },
          action: interaction || { type: 'unknown', href: '' },
          state_after: { url: newUrl },
          network_requests: enrichedRequests,
          step: step,
          url_changed: normalizeUrl(currentUrl) !== normalizeUrl(newUrl)
        });
        
        currentUrl = newUrl;
      } catch (e) {
        // Continue
      }
      
      await page.unroute('**/*', routeHandler);
    }
    
    if (traj % 5 === 4) process.stdout.write(`  Completed ${traj + 1} trajectories\r`);
  }
  
  await browser.close();
  console.log(`  [Multi-Step Form SPA] Captured ${transitions.length} transitions total`);
  return transitions;
}

// ─── Public SPA Capture (HTTPBin) ────────────────────────────────────────

async function captureHTTPBin(nTrajectories = 5, stepsPerTraj = 15) {
  console.log(`\n[HTTPBin] Capturing from httpbin.org (${nTrajectories} trajectories x ${stepsPerTraj} steps)`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();
  
  const transitions = [];
  const ENDPOINTS = [
    { path: '/get', type: 'navigation' },
    { path: '/post', type: 'navigation' },
    { path: '/put', type: 'navigation' },
    { path: '/delete', type: 'navigation' },
    { path: '/status/200', type: 'navigation' },
    { path: '/status/201', type: 'navigation' },
    { path: '/json', type: 'navigation' },
    { path: '/html', type: 'navigation' },
    { path: '/ip', type: 'navigation' },
    { path: '/user-agent', type: 'navigation' },
    { path: '/headers', type: 'navigation' },
    { path: '/encoding/utf8', type: 'navigation' },
  ];
  
  for (let traj = 0; traj < nTrajectories; traj++) {
    await page.goto('https://httpbin.org', { waitUntil: 'networkidle', timeout: 30000 });
    let currentUrl = page.url();
    
    for (let step = 0; step < stepsPerTraj; step++) {
      const capturedRequests = [];
      
      const routeHandler = async (route) => {
        const request = route.request();
        const entry = {
          endpoint_url: request.url(),
          http_method: request.method(),
          timestamp: Date.now(),
          request_body: ''
        };
        if (request.method() === 'POST' || request.method() === 'PUT') {
          try { entry.request_body = request.postData() || ''; } catch(e) {}
        }
        capturedRequests.push(entry);
        await route.continue();
      };
      
      await page.route('**/*', routeHandler);
      
      const ep = ENDPOINTS[step % ENDPOINTS.length];
      
      try {
        await page.goto(`https://httpbin.org${ep.path}`, { waitUntil: 'networkidle', timeout: 15000 });
        const newUrl = page.url();
        
        const responses = await page.evaluate(() => {
          return performance.getEntriesByType('resource')
            .filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest' || r.initiatorType === 'other')
            .slice(-10)
            .map(r => ({
              name: r.name,
              responseStatus: r.responseStatus || 200
            }));
        });
        
        const enrichedRequests = capturedRequests
          .filter(r => !isStaticAsset(r.endpoint_url))
          .map(r => {
            const resp = responses.find(res => r.endpoint_url === res.name);
            return {
              ...r,
              status_code: resp ? resp.responseStatus : 200,
              content_type: 'application/json'
            };
          });
        
        transitions.push({
          trajectory_id: `httpbin_${traj}`,
          state_before: { url: currentUrl },
          action: { type: 'navigation', target_href: ep.path },
          state_after: { url: newUrl },
          network_requests: enrichedRequests,
          step: step,
          url_changed: normalizeUrl(currentUrl) !== normalizeUrl(newUrl)
        });
        
        currentUrl = newUrl;
      } catch (e) {
        // Continue
      }
      
      await page.unroute('**/*', routeHandler);
    }
    
    if (traj % 2 === 1) process.stdout.write(`  Completed ${traj + 1} trajectories\r`);
  }
  
  await browser.close();
  console.log(`  [HTTPBin] Captured ${transitions.length} transitions total`);
  return transitions;
}

// ─── Dashboard SPA Capture ───────────────────────────────────────────────

async function captureDashboardSPA(serverUrl, nTrajectories = 10, stepsPerTraj = 16) {
  console.log(`\n[Dashboard SPA] Capturing from ${serverUrl} (${nTrajectories} trajectories x ${stepsPerTraj} steps)`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const transitions = [];
  const TABS = ['overview', 'analytics', 'users', 'settings'];
  
  for (let traj = 0; traj < nTrajectories; traj++) {
    await context.clearCookies();
    await page.goto(serverUrl, { waitUntil: 'domcontentloaded' });
    let currentUrl = page.url();
    
    for (let step = 0; step < stepsPerTraj; step++) {
      const capturedRequests = [];
      
      const routeHandler = async (route) => {
        const request = route.request();
        const entry = {
          endpoint_url: request.url(),
          http_method: request.method(),
          timestamp: Date.now(),
          request_body: ''
        };
        if (request.method() === 'POST' || request.method() === 'PUT') {
          try { entry.request_body = request.postData() || ''; } catch(e) {}
        }
        capturedRequests.push(entry);
        await route.continue();
      };
      
      await page.route('**/*', routeHandler);
      
      try {
        // Random tab selection
        const tab = TABS[Math.floor(Math.random() * TABS.length)];
        
        // Click tab button
        await page.click(`[data-tab="${tab}"]`);
        await page.waitForTimeout(500);
        
        const newUrl = page.url();
        
        const responses = await page.evaluate(() => {
          return performance.getEntriesByType('resource')
            .filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest')
            .slice(-10)
            .map(r => ({
              name: r.name,
              responseStatus: r.responseStatus || 200
            }));
        });
        
        const enrichedRequests = capturedRequests
          .filter(r => !isStaticAsset(r.endpoint_url))
          .map(r => {
            const resp = responses.find(res => r.endpoint_url === res.name);
            return {
              ...r,
              status_code: resp ? resp.responseStatus : 200,
              content_type: 'application/json'
            };
          });
        
        transitions.push({
          trajectory_id: `dashboard_${traj}`,
          state_before: { url: currentUrl },
          action: { type: 'tab_click', target_href: tab },
          state_after: { url: newUrl },
          network_requests: enrichedRequests,
          step: step,
          url_changed: normalizeUrl(currentUrl) !== normalizeUrl(newUrl)
        });
        
        currentUrl = newUrl;
      } catch (e) {
        // Continue
      }
      
      await page.unroute('**/*', routeHandler);
    }
    
    if (traj % 5 === 4) process.stdout.write(`  Completed ${traj + 1} trajectories\r`);
  }
  
  await browser.close();
  console.log(`  [Dashboard SPA] Captured ${transitions.length} transitions total`);
  return transitions;
}

// ─── Wizard SPA Capture ──────────────────────────────────────────────────

async function captureWizardSPA(serverUrl, nTrajectories = 10, stepsPerTraj = 12) {
  console.log(`\n[Wizard SPA] Capturing from ${serverUrl} (${nTrajectories} trajectories x ${stepsPerTraj} steps)`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const transitions = [];
  
  for (let traj = 0; traj < nTrajectories; traj++) {
    await context.clearCookies();
    await page.goto(serverUrl, { waitUntil: 'domcontentloaded' });
    let currentUrl = page.url();
    
    for (let step = 0; step < stepsPerTraj; step++) {
      const capturedRequests = [];
      
      const routeHandler = async (route) => {
        const request = route.request();
        const entry = {
          endpoint_url: request.url(),
          http_method: request.method(),
          timestamp: Date.now(),
          request_body: ''
        };
        if (request.method() === 'POST' || request.method() === 'PUT') {
          try { entry.request_body = request.postData() || ''; } catch(e) {}
        }
        capturedRequests.push(entry);
        await route.continue();
      };
      
      await page.route('**/*', routeHandler);
      
      try {
        let interaction;
        if (step % 4 === 3 && step > 0) {
          const prevBtn = await page.$('#prev-btn');
          if (prevBtn) {
            interaction = { type: 'button_click', href: 'prev' };
            await prevBtn.click();
          } else {
            const btn = await page.$('#next-btn') || await page.$('#submit-btn');
            if (btn) { interaction = { type: 'button_click', href: 'next' }; await btn.click(); }
          }
        } else {
          const btn = await page.$('#next-btn') || await page.$('#submit-btn');
          if (btn) { interaction = { type: 'button_click', href: 'next' }; await btn.click(); }
        }
        
        await page.waitForTimeout(500);
        
        const newUrl = page.url();
        
        const responses = await page.evaluate(() => {
          return performance.getEntriesByType('resource')
            .filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest')
            .slice(-10)
            .map(r => ({ name: r.name, responseStatus: r.responseStatus || 200 }));
        });
        
        const enrichedRequests = capturedRequests
          .filter(r => !isStaticAsset(r.endpoint_url))
          .map(r => {
            const resp = responses.find(res => r.endpoint_url === res.name);
            return {
              ...r,
              status_code: resp ? resp.responseStatus : 200,
              content_type: 'application/json'
            };
          });
        
        transitions.push({
          trajectory_id: `wizard_${traj}`,
          state_before: { url: currentUrl },
          action: interaction || { type: 'unknown', href: '' },
          state_after: { url: newUrl },
          network_requests: enrichedRequests,
          step: step,
          url_changed: normalizeUrl(currentUrl) !== normalizeUrl(newUrl)
        });
        
        currentUrl = newUrl;
      } catch (e) {
        // Continue
      }
      
      await page.unroute('**/*', routeHandler);
    }
    
    if (traj % 5 === 4) process.stdout.write(`  Completed ${traj + 1} trajectories\r`);
  }
  
  await browser.close();
  console.log(`  [Wizard SPA] Captured ${transitions.length} transitions total`);
  return transitions;
}

// ─── Main ────────────────────────────────────────────────────────────────

async function main() {
  console.log('='.repeat(70));
  console.log(`${EXPERIMENT_ID} — Network-Request Capture`);
  console.log('='.repeat(70));
  
  const mode = process.argv[2] || 'all';
  const allTransitions = {};
  
  // Start local servers
  let syntheticServer = null;
  let multistepServer = null;
  let dashboardServer = null;
  let wizardServer = null;
  
  if (mode === 'all' || mode === 'synthetic' || mode === 'multistep' || mode === 'dashboard' || mode === 'wizard') {
    console.log('\nStarting local servers...');
    syntheticServer = await startServer('synthetic_spa_server.js', 3847);
    multistepServer = await startServer('multistep_form_server.js', 3848);
    dashboardServer = await startServer('dashboard_spa_server.js', 3849);
    wizardServer = await startServer('wizard_spa_server.js', 3850);
    // Wait for servers to start
    await new Promise(r => setTimeout(r, 2000));
  }
  
  try {
    // Capture synthetic SPA
    if (mode === 'all' || mode === 'synthetic') {
      allTransitions.synthetic = await captureSyntheticSPA('http://localhost:3847');
    }
    
    // Capture multi-step form SPA
    if (mode === 'all' || mode === 'multistep') {
      allTransitions.multistep_form = await captureMultistepFormSPA('http://localhost:3848');
    }
    
    // Capture dashboard SPA
    if (mode === 'all' || mode === 'dashboard') {
      allTransitions.dashboard = await captureDashboardSPA('http://localhost:3849');
    }
    
    // Capture wizard SPA
    if (mode === 'all' || mode === 'wizard') {
      allTransitions.wizard = await captureWizardSPA('http://localhost:3850');
    }
    
    // Capture public SPAs
    if (mode === 'all' || mode === 'genuine') {
      allTransitions.httpbin = await captureHTTPBin();
    }
  } finally {
    // Stop servers
    stopServer(syntheticServer);
    stopServer(multistepServer);
    stopServer(dashboardServer);
    stopServer(wizardServer);
  }
  
  // Save all transitions
  const outputPath = path.join(OUTPUT_DIR, 'raw_network_captures.json');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(allTransitions, null, 2));
  console.log(`\nSaved raw captures to ${outputPath}`);
  
  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('CAPTURE SUMMARY');
  console.log('='.repeat(70));
  let total = 0;
  for (const [key, trans] of Object.entries(allTransitions)) {
    console.log(`  ${key}: ${trans.length} transitions`);
    total += trans.length;
  }
  console.log(`  TOTAL: ${total} transitions`);
  console.log('='.repeat(70));
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
