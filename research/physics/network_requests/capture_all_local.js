#!/usr/bin/env node
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const EXPERIMENT_ID = 'EXP-PHYSICS-34674671762';
const OUTPUT_DIR = path.join(__dirname, '..', '..', 'experiments', EXPERIMENT_ID);
const SCRIPT_DIR = __dirname;

function startServer(script, port) {
  return new Promise((resolve) => {
    const server = spawn('node', [path.join(SCRIPT_DIR, script)], {
      env: { ...process.env, PORT: port.toString() },
      stdio: ['ignore', 'pipe', 'pipe']
    });
    let started = false;
    server.stdout.on('data', (data) => {
      if (!started && data.toString().includes('running on')) {
        started = true;
        resolve(server);
      }
    });
    setTimeout(() => { if (!started) { started = true; resolve(server); } }, 3000);
  });
}

function isStaticAsset(url) { return /\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|ttf|map|font)(\?|$)/i.test(url); }

async function captureSPA(name, serverUrl, nTrajectories, stepsPerTraj, interactionFn) {
  console.log(`\n[${name}] Capturing from ${serverUrl}`);
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
        const entry = { endpoint_url: request.url(), http_method: request.method(), timestamp: Date.now(), request_body: '' };
        if (request.method() === 'POST' || request.method() === 'PUT') {
          try { entry.request_body = request.postData() || ''; } catch(e) {}
        }
        capturedRequests.push(entry);
        await route.continue();
      };
      await page.route('**/*', routeHandler);
      
      try {
        const interaction = await interactionFn(page, step, traj);
        if (!interaction) { await page.goto(serverUrl, { waitUntil: 'domcontentloaded' }); currentUrl = page.url(); await page.unroute('**/*', routeHandler); break; }
        await page.waitForTimeout(500);
        const newUrl = page.url();
        const responses = await page.evaluate(() => performance.getEntriesByType('resource').filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest').slice(-10).map(r => ({ name: r.name, responseStatus: r.responseStatus || 200 })));
        const enrichedRequests = capturedRequests.filter(r => !isStaticAsset(r.endpoint_url)).map(r => {
          const resp = responses.find(res => r.endpoint_url === res.name);
          return { ...r, status_code: resp ? resp.responseStatus : 200, content_type: 'application/json' };
        });
        transitions.push({ trajectory_id: `${name}_${traj}`, state_before: { url: currentUrl }, action: interaction, state_after: { url: newUrl }, network_requests: enrichedRequests, step, url_changed: currentUrl.split('#')[0] !== newUrl.split('#')[0] });
        currentUrl = newUrl;
      } catch (e) {}
      await page.unroute('**/*', routeHandler);
    }
    if (traj % 5 === 4) process.stdout.write(`  [${name}] ${traj+1} trajectories done\r`);
  }
  await browser.close();
  console.log(`  [${name}] ${transitions.length} transitions`);
  return transitions;
}

async function main() {
  console.log('='.repeat(70));
  console.log(`${EXPERIMENT_ID} — Combined Local SPA Capture`);
  console.log('='.repeat(70));
  
  const servers = [
    startServer('synthetic_spa_server.js', 3847),
    startServer('multistep_form_server.js', 3848),
    startServer('dashboard_spa_server.js', 3849),
    startServer('wizard_spa_server.js', 3850),
  ];
  const [s1, s2, s3, s4] = await Promise.all(servers);
  await new Promise(r => setTimeout(r, 2000));
  
  const ACTIONS = ['act_a', 'act_b', 'act_c', 'act_d'];
  const TABS = ['overview', 'analytics', 'users', 'settings'];
  
  const allData = {};
  
  allData.synthetic = await captureSPA('synthetic', 'http://localhost:3847', 10, 25, async (page) => {
    const action = ACTIONS[Math.floor(Math.random() * ACTIONS.length)];
    await page.click(`[data-action="${action}"]`);
    return { type: 'button_click', target_href: action };
  });
  
  allData.multistep_form = await captureSPA('multistep_form', 'http://localhost:3848', 10, 12, async (page, step) => {
    if (step % 3 === 0 && step > 0) {
      const btn = await page.$('#prev-btn');
      if (btn) { await btn.click(); return { type: 'button_click', href: 'prev' }; }
    }
    const btn = await page.$('#next-btn') || await page.$('#submit-btn');
    if (btn) { await btn.click(); return { type: 'button_click', href: 'next' }; }
    return null;
  });
  
  allData.dashboard = await captureSPA('dashboard', 'http://localhost:3849', 10, 16, async (page) => {
    const tab = TABS[Math.floor(Math.random() * TABS.length)];
    await page.click(`[data-tab="${tab}"]`);
    return { type: 'tab_click', target_href: tab };
  });
  
  allData.wizard = await captureSPA('wizard', 'http://localhost:3850', 10, 12, async (page, step) => {
    if (step % 4 === 3 && step > 0) {
      const btn = await page.$('#prev-btn');
      if (btn) { await btn.click(); return { type: 'button_click', href: 'prev' }; }
    }
    const btn = await page.$('#next-btn') || await page.$('#submit-btn');
    if (btn) { await btn.click(); return { type: 'button_click', href: 'next' }; }
    return null;
  });
  
  [s1, s2, s3, s4].forEach(s => { if (s && !s.killed) s.kill('SIGTERM'); });
  
  const outputPath = path.join(OUTPUT_DIR, 'raw_network_captures.json');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(allData, null, 2));
  
  console.log('\n' + '='.repeat(70));
  console.log('CAPTURE SUMMARY');
  console.log('='.repeat(70));
  let total = 0;
  for (const [key, trans] of Object.entries(allData)) {
    console.log(`  ${key}: ${trans.length} transitions`);
    total += trans.length;
  }
  console.log(`  TOTAL: ${total} transitions`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
