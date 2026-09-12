#!/usr/bin/env node
/**
 * EXP-PHYSICS-34695057869 — Response-Side Capture Script
 * 
 * Based on capture_all_local_v2.js but captures response bodies via
 * Playwright's page.on('response', ...) event instead of relying on
 * performance.getEntriesByType('resource').
 * 
 * For each API/XHR response, captures:
 *   - response.status()
 *   - response.headers()['content-type']
 *   - SHA-256(response.body()[:500])
 *   - response.body() fragment (first 500 chars)
 * 
 * Output: raw_network_captures_response_side.json with same structure
 * as parent but with additional response-side fields.
 */

const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const EXPERIMENT_ID = 'EXP-PHYSICS-34695057869';
const OUTPUT_DIR = path.join(__dirname, '..', '..', 'experiments', EXPERIMENT_ID);

function startServer(script, port) {
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
      // Some servers print to stderr
      if (!started && (data.toString().includes('running on') || data.toString().includes('listening'))) {
        started = true;
        resolve(server);
      }
    });
    setTimeout(() => { if (!started) { started = true; resolve(server); } }, 4000);
  });
}

function isStaticAsset(url) {
  return /\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|ttf|map|font)(\?|$)/i.test(url);
}

function sha256(str) {
  return crypto.createHash('sha256').update(str).digest('hex');
}

function saveData(allData, filename) {
  const outputPath = path.join(OUTPUT_DIR, filename);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(allData, null, 2));
}

async function captureSPA(name, serverUrl, nTrajectories, stepsPerTraj, interactionFn) {
  console.log(`\n[${name}] Capturing response-side data from ${serverUrl}`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  const transitions = [];
  let totalResponses = 0;
  let capturedResponses = 0;

  try {
    for (let traj = 0; traj < nTrajectories; traj++) {
      await context.clearCookies();
      await page.goto(serverUrl, { waitUntil: 'domcontentloaded' });
      let currentUrl = page.url();

      for (let step = 0; step < stepsPerTraj; step++) {
        const capturedRequests = [];
        const capturedResponsesMap = new Map(); // url -> response-side data
        let routeHandler;
        let responseHandler;

        try {
          // Set up route interception to capture requests
          routeHandler = async (route) => {
            const request = route.request();
            const entry = {
              endpoint_url: request.url(),
              http_method: request.method(),
              timestamp: Date.now(),
              request_body: ''
            };
            if (request.method() === 'POST' || request.method() === 'PUT') {
              try { entry.request_body = request.postData() || ''; } catch (e) {}
            }
            capturedRequests.push(entry);
            await route.continue();
          };
          await page.route('**/*', routeHandler);

          // Set up response interception to capture response bodies
          responseHandler = async (response) => {
            const url = response.url();
            if (isStaticAsset(url)) return;
            totalResponses++;
            try {
              const body = await response.body();
              const bodyStr = body.toString('utf-8').slice(0, 500);
              const bodyHash = sha256(bodyStr).slice(0, 16);
              const contentType = response.headers()['content-type'] || 'unknown';
              const status = response.status();

              capturedResponsesMap.set(url, {
                status_code: status,
                content_type: contentType,
                response_body_hash: bodyHash,
                response_body_fragment: bodyStr,
                response_timing_ms: Date.now() // approximate
              });
              capturedResponses++;
            } catch (e) {
              // Response body unavailable (streaming, redirect, etc.)
              try {
                const contentType = response.headers()['content-type'] || 'unknown';
                const status = response.status();
                capturedResponsesMap.set(url, {
                  status_code: status,
                  content_type: contentType,
                  response_body_hash: 'unavailable',
                  response_body_fragment: '',
                  response_timing_ms: Date.now()
                });
              } catch (e2) {}
            }
          };
          page.on('response', responseHandler);

          // Perform the interaction
          const interaction = await interactionFn(page, step, traj);
          if (!interaction) {
            page.off('response', responseHandler);
            try { await page.unroute('**/*', routeHandler); } catch (e) {}
            break;
          }

          // Wait for responses to arrive
          await page.waitForTimeout(600);

          const newUrl = page.url();

          // Merge captured requests with response-side data
          const enrichedRequests = capturedRequests
            .filter(r => !isStaticAsset(r.endpoint_url))
            .map(r => {
              const respData = capturedResponsesMap.get(r.endpoint_url) || {};
              return {
                endpoint_url: r.endpoint_url,
                http_method: r.http_method,
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
            state_before: { url: currentUrl },
            action: interaction,
            state_after: { url: newUrl },
            network_requests: enrichedRequests,
            step,
            url_changed: currentUrl.split('#')[0] !== newUrl.split('#')[0],
            response_capture_stats: {
              total_responses: capturedResponsesMap.size,
              with_body: [...capturedResponsesMap.values()].filter(r => r.response_body_hash !== 'unavailable').length
            }
          });

          currentUrl = newUrl;
        } catch (e) {
          console.log(`  [${name}] step ${step} error: ${e.message.substring(0, 80)}`);
        }

        // Cleanup handlers
        page.off('response', responseHandler);
        try { if (routeHandler) await page.unroute('**/*', routeHandler); } catch (e) {}
      }
      if (traj % 5 === 4) process.stdout.write(`  [${name}] ${traj + 1} done\r`);
    }
  } catch (e) {
    console.log(`  [${name}] FATAL: ${e.message.substring(0, 100)}`);
  }
  await browser.close().catch(() => {});
  console.log(`  [${name}] ${transitions.length} transitions, ${capturedResponses}/${totalResponses} responses captured`);
  return transitions;
}

async function main() {
  console.log('='.repeat(70));
  console.log(`${EXPERIMENT_ID} — Response-Side Capture`);
  console.log('='.repeat(70));

  const s1 = await startServer('synthetic_spa_server.js', 3847);
  const s2 = await startServer('multistep_form_server.js', 3848);
  const s3 = await startServer('dashboard_spa_server.js', 3849);
  const s4 = await startServer('wizard_spa_server.js', 3850);
  await new Promise(r => setTimeout(r, 2500));

  const ACTIONS = ['act_a', 'act_b', 'act_c', 'act_d'];
  const TABS = ['overview', 'analytics', 'users', 'settings'];

  const allData = {};

  // 1. Synthetic — deterministic response bodies per (state, action)
  allData.synthetic = await captureSPA('synthetic', 'http://localhost:3847', 10, 25, async (page) => {
    const action = ACTIONS[Math.floor(Math.random() * ACTIONS.length)];
    await page.click(`[data-action="${action}"]`);
    return { type: 'button_click', target_href: action };
  });
  saveData(allData, 'raw_network_captures_response_side.json');

  // 2. Multistep form — response bodies vary by step
  allData.multistep_form = await captureSPA('multistep_form', 'http://localhost:3848', 10, 12, async (page, step) => {
    if (step % 3 === 0 && step > 0) {
      const btn = await page.$('#prev-btn');
      if (btn) { await btn.click(); return { type: 'button_click', href: 'prev' }; }
    }
    const btn = await page.$('#next-btn') || await page.$('#submit-btn');
    if (btn) { await btn.click(); return { type: 'button_click', href: 'next' }; }
    return null;
  });
  saveData(allData, 'raw_network_captures_response_side.json');

  // 3. Dashboard — response bodies vary by tab
  allData.dashboard = await captureSPA('dashboard', 'http://localhost:3849', 10, 16, async (page) => {
    const tab = TABS[Math.floor(Math.random() * TABS.length)];
    await page.click(`[data-tab="${tab}"]`);
    return { type: 'tab_click', target_href: tab };
  });
  saveData(allData, 'raw_network_captures_response_side.json');

  // 4. Wizard — response bodies vary by step
  allData.wizard = await captureSPA('wizard', 'http://localhost:3850', 10, 12, async (page, step) => {
    if (step % 4 === 3 && step > 0) {
      const btn = await page.$('#prev-btn');
      if (btn) { await btn.click(); return { type: 'button_click', href: 'prev' }; }
    }
    const btn = await page.$('#next-btn') || await page.$('#submit-btn');
    if (btn) { await btn.click(); return { type: 'button_click', href: 'next' }; }
    return null;
  });
  saveData(allData, 'raw_network_captures_response_side.json');

  // Kill servers
  [s1, s2, s3, s4].forEach(s => { try { if (s && !s.killed) s.kill('SIGTERM'); } catch (e) {} });

  console.log('\n' + '='.repeat(70));
  console.log('CAPTURE SUMMARY');
  console.log('='.repeat(70));
  let total = 0;
  for (const [key, trans] of Object.entries(allData)) {
    const withBody = trans.reduce((acc, t) => {
      return acc + t.network_requests.filter(r => r.response_body_hash !== 'missing' && r.response_body_hash !== 'unavailable').length;
    }, 0);
    const totalReqs = trans.reduce((acc, t) => acc + t.network_requests.length, 0);
    console.log(`  ${key}: ${trans.length} transitions, ${withBody}/${totalReqs} responses with body`);
    total += trans.length;
  }
  console.log(`  TOTAL: ${total} transitions`);
  console.log('Output: raw_network_captures_response_side.json');
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
