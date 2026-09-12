#!/usr/bin/env node
/**
 * Retry capture for dashboard and multistep_form — more trajectories for data sufficiency.
 * Need >= 150 transitions per site for n_test >= 30 after 80/20 split.
 */
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const EXPERIMENT_ID = 'EXP-PHYSICS-34695057869';
const OUTPUT_DIR = path.join(__dirname, '..', '..', 'experiments', EXPERIMENT_ID);

function sha256(str) { return crypto.createHash('sha256').update(str).digest('hex'); }
function isStaticAsset(url) { return /\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|ttf|map|font)(\?|$)/i.test(url); }

async function startServer(script, port) {
  return new Promise((resolve) => {
    const server = spawn('node', [path.join(__dirname, script)], {
      env: { ...process.env, PORT: port.toString() },
      stdio: ['ignore', 'pipe', 'pipe']
    });
    let started = false;
    server.stdout.on('data', (data) => {
      if (!started && data.toString().includes('running on')) { started = true; resolve(server); }
    });
    server.stderr.on('data', (data) => {
      if (!started && (data.toString().includes('running on') || data.toString().includes('listening'))) {
        started = true; resolve(server);
      }
    });
    setTimeout(() => { if (!started) { started = true; resolve(server); } }, 5000);
  });
}

async function captureSPA(name, serverUrl, nTrajectories, stepsPerTraj, interactionFn) {
  console.log(`\n[${name}] Capturing from ${serverUrl} (${nTrajectories} traj x ${stepsPerTraj} steps)`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  const transitions = [];

  try {
    for (let traj = 0; traj < nTrajectories; traj++) {
      await context.clearCookies();
      await page.goto(serverUrl, { waitUntil: 'domcontentloaded', timeout: 10000 });
      let currentUrl = page.url();

      for (let step = 0; step < stepsPerTraj; step++) {
        const capturedRequests = [];
        const capturedResponsesMap = new Map();
        let routeHandler, responseHandler;

        try {
          routeHandler = async (route) => {
            const request = route.request();
            const entry = { endpoint_url: request.url(), http_method: request.method(), timestamp: Date.now(), request_body: '' };
            if (request.method() === 'POST' || request.method() === 'PUT') {
              try { entry.request_body = request.postData() || ''; } catch(e) {}
            }
            capturedRequests.push(entry);
            await route.continue();
          };
          await page.route('**/*', routeHandler);

          responseHandler = async (response) => {
            const url = response.url();
            if (isStaticAsset(url)) return;
            try {
              const body = await response.body();
              const bodyStr = body.toString('utf-8').slice(0, 500);
              const bodyHash = sha256(bodyStr).slice(0, 16);
              capturedResponsesMap.set(url, {
                status_code: response.status(),
                content_type: response.headers()['content-type'] || 'unknown',
                response_body_hash: bodyHash,
                response_body_fragment: bodyStr,
                response_timing_ms: Date.now()
              });
            } catch(e) {
              try {
                capturedResponsesMap.set(response.url(), {
                  status_code: response.status(),
                  content_type: response.headers()['content-type'] || 'unknown',
                  response_body_hash: 'unavailable',
                  response_body_fragment: '',
                  response_timing_ms: Date.now()
                });
              } catch(e2) {}
            }
          };
          page.on('response', responseHandler);

          const interaction = await interactionFn(page, step, traj);
          if (!interaction) {
            page.off('response', responseHandler);
            try { await page.unroute('**/*', routeHandler); } catch(e) {}
            break;
          }

          await page.waitForTimeout(600);
          const newUrl = page.url();
          const enrichedRequests = capturedRequests
            .filter(r => !isStaticAsset(r.endpoint_url))
            .map(r => {
              const respData = capturedResponsesMap.get(r.endpoint_url) || {};
              return {
                endpoint_url: r.endpoint_url, http_method: r.http_method,
                status_code: respData.status_code || 200,
                content_type: respData.content_type || 'application/json',
                request_body: r.request_body,
                response_body_hash: respData.response_body_hash || 'missing',
                response_body_fragment: respData.response_body_fragment || '',
                response_timing_ms: respData.response_timing_ms || 0
              };
            });

          transitions.push({
            trajectory_id: `${name}_${traj}`,
            state_before: { url: currentUrl }, action: interaction,
            state_after: { url: newUrl }, network_requests: enrichedRequests,
            step, url_changed: currentUrl.split('#')[0] !== newUrl.split('#')[0]
          });
          currentUrl = newUrl;
        } catch (e) {
          console.log(`  [${name}] step ${step} error: ${e.message.substring(0, 60)}`);
        }
        page.off('response', responseHandler);
        try { if (routeHandler) await page.unroute('**/*', routeHandler); } catch(e) {}
      }
      if (traj % 5 === 4) process.stdout.write(`  [${name}] ${traj + 1} done\n`);
    }
  } catch (e) {
    console.log(`  [${name}] FATAL: ${e.message.substring(0, 100)}`);
  }
  await browser.close().catch(() => {});
  console.log(`  [${name}] ${transitions.length} transitions captured`);
  return transitions;
}

async function main() {
  // Start servers
  const dashServer = await startServer('dashboard_spa_server.js', 3849);
  const multiServer = await startServer('multistep_form_server.js', 3848);
  await new Promise(r => setTimeout(r, 2000));

  const TABS = ['overview', 'analytics', 'users', 'settings'];

  // Capture dashboard: 20 trajectories x 16 steps = 320 planned
  const dashboard = await captureSPA('dashboard', 'http://localhost:3849', 20, 16, async (page) => {
    const tab = TABS[Math.floor(Math.random() * TABS.length)];
    await page.click(`[data-tab="${tab}"]`);
    return { type: 'tab_click', target_href: tab };
  });

  // Capture multistep_form: 15 trajectories x 12 steps = 180 planned
  const multistep = await captureSPA('multistep_form', 'http://localhost:3848', 15, 12, async (page, step) => {
    if (step % 3 === 0 && step > 0) {
      const btn = await page.$('#prev-btn');
      if (btn) { await btn.click(); return { type: 'button_click', href: 'prev' }; }
    }
    const btn = await page.$('#next-btn') || await page.$('#submit-btn');
    if (btn) { await btn.click(); return { type: 'button_click', href: 'next' }; }
    return null;
  });

  // Kill servers
  [dashServer, multiServer].forEach(s => { try { if (s && !s.killed) s.kill('SIGTERM'); } catch(e) {} });

  // Merge into existing data
  const existingPath = path.join(OUTPUT_DIR, 'raw_network_captures_response_side.json');
  let allData = {};
  if (fs.existsSync(existingPath)) {
    allData = JSON.parse(fs.readFileSync(existingPath, 'utf-8'));
  }
  allData.dashboard = dashboard;
  allData.multistep_form = multistep;
  fs.writeFileSync(existingPath, JSON.stringify(allData, null, 2));

  console.log('\n' + '='.repeat(60));
  console.log('FINAL CAPTURE SUMMARY');
  console.log('='.repeat(60));
  for (const [k, v] of Object.entries(allData)) {
    const withBody = v.reduce((acc, t) => acc + t.network_requests.filter(r => r.response_body_hash !== 'missing' && r.response_body_hash !== 'unavailable').length, 0);
    const totalReqs = v.reduce((acc, t) => acc + t.network_requests.length, 0);
    const nTest = Math.floor(v.length * 0.2);
    console.log(`  ${k}: ${v.length} transitions, ${withBody}/${totalReqs} with body, n_test=${nTest} ${nTest >= 30 ? 'PASS' : 'FAIL'}`);
  }
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
