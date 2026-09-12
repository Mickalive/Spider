#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const EXPERIMENT_ID = 'EXP-PHYSICS-34674671762';
const OUTPUT_DIR = path.join(__dirname, '..', '..', 'experiments', EXPERIMENT_ID);

function isStaticAsset(url) { return /\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|ttf|map|font)(\?|$)/i.test(url); }

async function main() {
  console.log('Capturing Wizard SPA...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  const transitions = [];
  
  for (let traj = 0; traj < 10; traj++) {
    await context.clearCookies();
    await page.goto('http://localhost:3850', { waitUntil: 'domcontentloaded' });
    let currentUrl = page.url();
    
    for (let step = 0; step < 12; step++) {
      const capturedRequests = [];
      try {
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
        
        let interaction;
        if (step % 4 === 3 && step > 0) {
          const btn = await page.$('#prev-btn');
          if (btn) { await btn.click(); interaction = { type: 'button_click', href: 'prev' }; }
        }
        if (!interaction) {
          const btn = await page.$('#next-btn') || await page.$('#submit-btn');
          if (btn) { await btn.click(); interaction = { type: 'button_click', href: 'next' }; }
        }
        
        if (!interaction) { break; }
        await page.waitForTimeout(500);
        const newUrl = page.url();
        const responses = await page.evaluate(() => performance.getEntriesByType('resource').filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest').slice(-10).map(r => ({ name: r.name, responseStatus: r.responseStatus || 200 })));
        const enrichedRequests = capturedRequests.filter(r => !isStaticAsset(r.endpoint_url)).map(r => {
          const resp = responses.find(res => r.endpoint_url === res.name);
          return { ...r, status_code: resp ? resp.responseStatus : 200, content_type: 'application/json' };
        });
        transitions.push({ trajectory_id: `wizard_${traj}`, state_before: { url: currentUrl }, action: interaction, state_after: { url: newUrl }, network_requests: enrichedRequests, step, url_changed: currentUrl.split('#')[0] !== newUrl.split('#')[0] });
        currentUrl = newUrl;
      } catch (e) {
        console.log(`  traj=${traj} step=${step}: ${e.message.substring(0, 100)}`);
        break;
      }
      try { await page.unroute('**/*'); } catch(e) {}
    }
    if (traj % 5 === 4) process.stdout.write(`  ${traj+1} trajectories done\r`);
  }
  await browser.close();
  console.log(`  Wizard: ${transitions.length} transitions`);
  
  // Load existing data and merge
  const outputPath = path.join(OUTPUT_DIR, 'raw_network_captures.json');
  let allData = {};
  if (fs.existsSync(outputPath)) {
    allData = JSON.parse(fs.readFileSync(outputPath, 'utf-8'));
  }
  allData.wizard = transitions;
  fs.writeFileSync(outputPath, JSON.stringify(allData, null, 2));
  console.log('  Saved to raw_network_captures.json');
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
