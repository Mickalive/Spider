#!/usr/bin/env node
/**
 * Retry capture for wizard only — start server, capture, kill.
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

async function main() {
  console.log('Starting wizard server on port 3850...');
  const wizardServer = await startServer('wizard_spa_server.js', 3850);
  
  // Wait for server to be ready
  await new Promise(r => setTimeout(r, 2000));
  
  // Test connection
  try {
    const http = require('http');
    await new Promise((resolve, reject) => {
      http.get('http://localhost:3850/', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => { console.log('Wizard server OK, got', data.length, 'bytes'); resolve(); });
      }).on('error', reject);
    });
  } catch(e) {
    console.log('Wizard server test failed:', e.message);
    wizardServer.kill('SIGTERM');
    process.exit(1);
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  const transitions = [];

  console.log('Capturing wizard transitions...');

  for (let traj = 0; traj < 15; traj++) {
    await context.clearCookies();
    await page.goto('http://localhost:3850/', { waitUntil: 'domcontentloaded', timeout: 10000 });
    let currentUrl = page.url();

    for (let step = 0; step < 12; step++) {
      const capturedRequests = [];
      const capturedResponsesMap = new Map();
      let routeHandler;
      let responseHandler;

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

        if (step % 4 === 3 && step > 0) {
          const btn = await page.$('#prev-btn');
          if (btn) { await btn.click(); }
        } else {
          const btn = await page.$('#next-btn') || await page.$('#submit-btn');
          if (btn) { await btn.click(); }
        }

        await page.waitForTimeout(600);
        const newUrl = page.url();
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
          trajectory_id: `wizard_${traj}`,
          state_before: { url: currentUrl },
          action: { type: 'button_click', href: 'next' },
          state_after: { url: newUrl },
          network_requests: enrichedRequests,
          step,
          url_changed: currentUrl.split('#')[0] !== newUrl.split('#')[0]
        });
        currentUrl = newUrl;
      } catch (e) {
        console.log(`  step ${step} error: ${e.message.substring(0, 80)}`);
      }
      page.off('response', responseHandler);
      try { if (routeHandler) await page.unroute('**/*', routeHandler); } catch(e) {}
    }
    if (traj % 5 === 4) process.stdout.write(`  ${traj + 1} done\n`);
  }

  await browser.close().catch(() => {});
  wizardServer.kill('SIGTERM');

  console.log(`Wizard: ${transitions.length} transitions captured`);
  
  // Load existing data and merge
  const existingPath = path.join(OUTPUT_DIR, 'raw_network_captures_response_side.json');
  let allData = {};
  if (fs.existsSync(existingPath)) {
    allData = JSON.parse(fs.readFileSync(existingPath, 'utf-8'));
  }
  allData.wizard = transitions;
  fs.writeFileSync(existingPath, JSON.stringify(allData, null, 2));
  console.log('Merged wizard data into raw_network_captures_response_side.json');
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
