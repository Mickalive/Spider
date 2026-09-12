#!/usr/bin/env node
/**
 * EXP-PHYSICS-34719136202 — DOM Feature Capture Script
 *
 * Captures DOM structural features at each transition point on locally-hosted SPAs.
 * Based on capture_response_side.js but adds page.evaluate() DOM extraction.
 *
 * DOM Features extracted per spec:
 *   - element_count: document.querySelectorAll('*').length
 *   - tree_depth: computeMaxDepth(document.body)
 *   - interactive_density: interactiveElements.length / totalElements
 *   - form_count: document.querySelectorAll('form').length
 *   - input_count: document.querySelectorAll('input, select, textarea').length
 *   - button_count: document.querySelectorAll('button, [role="button"]').length
 *   - visible_text_hash: SHA-256(document.body.innerText.trim().substring(0, 2000))
 *   - attribute_pattern_hash: SHA-256(sorted attribute names from interactive elements)
 *
 * Output: raw_dom_captures.json with DOM features per transition.
 */

const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const EXPERIMENT_ID = 'EXP-PHYSICS-34719136202';
const OUTPUT_DIR = path.join(__dirname);
const SERVERS_DIR = path.join(__dirname, '..', '..', 'physics', 'network_requests');

function startServer(script, port) {
  return new Promise((resolve) => {
    const server = spawn('node', [path.join(SERVERS_DIR, script)], {
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
    setTimeout(() => { if (!started) { started = true; resolve(server); } }, 4000);
  });
}

function sha256(str) {
  return crypto.createHash('sha256').update(str).digest('hex');
}

function saveData(allData, filename) {
  const outputPath = path.join(OUTPUT_DIR, filename);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(allData, null, 2));
}

/**
 * Extract DOM structural features via page.evaluate().
 * This function runs IN the browser context — passed as a function reference, not a string.
 */
function domExtractionFn() {
  function computeMaxDepth(el) {
    if (!el || !el.children || el.children.length === 0) return 1;
    let maxChild = 0;
    for (let i = 0; i < el.children.length; i++) {
      const d = computeMaxDepth(el.children[i]);
      if (d > maxChild) maxChild = d;
    }
    return 1 + maxChild;
  }

  const allElements = document.querySelectorAll('*');
  const interactiveElements = document.querySelectorAll(
    'button, a, input, select, textarea, [role="button"]'
  );

  // Visible text content (first 2000 chars)
  const visibleText = (document.body.innerText || '').trim().substring(0, 2000);

  // Attribute pattern hash: collect sorted attribute names from interactive elements
  const attrNames = [];
  interactiveElements.forEach(el => {
    for (let i = 0; i < el.attributes.length; i++) {
      attrNames.push(el.attributes[i].name);
    }
  });
  attrNames.sort();

  return {
    element_count: allElements.length,
    tree_depth: computeMaxDepth(document.body),
    interactive_density: interactiveElements.length / Math.max(allElements.length, 1),
    form_count: document.querySelectorAll('form').length,
    input_count: document.querySelectorAll('input, select, textarea').length,
    button_count: document.querySelectorAll('button, [role="button"]').length,
    visible_text_raw: visibleText,
    attribute_names: attrNames
  };
}

function hashStr(str) {
  return sha256(str).slice(0, 16);
}

async function extractDOMFeatures(page) {
  try {
    const rawFeatures = await page.evaluate(domExtractionFn);
    return {
      element_count: rawFeatures.element_count,
      tree_depth: rawFeatures.tree_depth,
      interactive_density: rawFeatures.interactive_density,
      form_count: rawFeatures.form_count,
      input_count: rawFeatures.input_count,
      button_count: rawFeatures.button_count,
      visible_text_hash: hashStr(rawFeatures.visible_text_raw || ''),
      attribute_pattern_hash: hashStr((rawFeatures.attribute_names || []).join('|'))
    };
  } catch (e) {
    console.log(`    [DOM] evaluate error: ${e.message.substring(0, 100)}`);
    return { element_count: 0, tree_depth: 0, interactive_density: 0,
      form_count: 0, input_count: 0, button_count: 0,
      visible_text_hash: 'error', attribute_pattern_hash: 'error' };
  }
}

async function captureSPA(name, serverUrl, nTrajectories, stepsPerTraj, interactionFn) {
  console.log(`\n[${name}] Capturing DOM features from ${serverUrl}`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  const transitions = [];
  let errorCount = 0;

  try {
    for (let traj = 0; traj < nTrajectories; traj++) {
      await context.clearCookies();
      await page.goto(serverUrl, { waitUntil: 'load' });
      // Wait for JS to execute and DOM to render
      await page.waitForTimeout(1000);
      let currentUrl = page.url();

      // Capture initial DOM state before any interaction
      let prevDomFeatures = await extractDOMFeatures(page);

      for (let step = 0; step < stepsPerTraj; step++) {
        try {
          // Perform the interaction
          const interaction = await interactionFn(page, step, traj);
          if (!interaction) break;

          // Wait for DOM to stabilize: networkidle with fallback timeout
          try {
            await page.waitForLoadState('networkidle', { timeout: 3000 });
          } catch (e) {}
          await page.waitForTimeout(600);

          const newUrl = page.url();

          // Extract DOM features AFTER interaction
          let domFeatures = await extractDOMFeatures(page);

          transitions.push({
            trajectory_id: `${name}_${traj}`,
            state_before: { url: currentUrl, dom_features: prevDomFeatures },
            action: interaction,
            state_after: { url: newUrl, dom_features: domFeatures },
            step,
            url_changed: currentUrl.split('#')[0] !== newUrl.split('#')[0]
          });

          prevDomFeatures = domFeatures;
          currentUrl = newUrl;
        } catch (e) {
          errorCount++;
          console.log(`  [${name}] step ${step} error: ${e.message.substring(0, 80)}`);
        }
      }
      if (traj % 5 === 4) process.stdout.write(`  [${name}] ${traj + 1} done\r`);
    }
  } catch (e) {
    console.log(`  [${name}] FATAL: ${e.message.substring(0, 100)}`);
  }
  await browser.close().catch(() => {});
  console.log(`  [${name}] ${transitions.length} transitions captured (${errorCount} errors)`);
  return transitions;
}

async function main() {
  console.log('='.repeat(70));
  console.log(`${EXPERIMENT_ID} — DOM Feature Capture`);
  console.log('='.repeat(70));

  // Start all 4 servers sequentially with longer waits
  console.log('Starting servers...');
  const s1 = await startServer('synthetic_spa_server.js', 3847);
  console.log('  synthetic on 3847');
  await new Promise(r => setTimeout(r, 500));
  const s2 = await startServer('multistep_form_server.js', 3848);
  console.log('  multistep_form on 3848');
  await new Promise(r => setTimeout(r, 500));
  const s3 = await startServer('dashboard_spa_server.js', 3849);
  console.log('  dashboard on 3849');
  await new Promise(r => setTimeout(r, 500));
  const s4 = await startServer('wizard_spa_server.js', 3850);
  console.log('  wizard on 3850');
  await new Promise(r => setTimeout(r, 3000));

  const ACTIONS = ['act_a', 'act_b', 'act_c', 'act_d'];
  const TABS = ['overview', 'analytics', 'users', 'settings'];

  const allData = {};

  // 1. Synthetic — deterministic DOM per (state, action)
  // 10 trajectories x 25 steps = ~250 transitions (positive control)
  allData.synthetic = await captureSPA('synthetic', 'http://localhost:3847', 10, 25, async (page) => {
    const action = ACTIONS[Math.floor(Math.random() * ACTIONS.length)];
    await page.click(`[data-action="${action}"]`);
    return { type: 'button_click', target_href: action };
  });
  saveData(allData, 'raw_dom_captures.json');

  // 2. Multistep form — 25 trajectories x 8 steps = ~200 transitions
  allData.multistep_form = await captureSPA('multistep_form', 'http://localhost:3848', 25, 8, async (page, step) => {
    if (step % 3 === 0 && step > 0) {
      const btn = await page.$('#prev-btn');
      if (btn) { await btn.click(); return { type: 'button_click', target_href: 'prev' }; }
    }
    const btn = await page.$('#next-btn') || await page.$('#submit-btn');
    if (btn) { await btn.click(); return { type: 'button_click', target_href: 'next' }; }
    return null;
  });
  saveData(allData, 'raw_dom_captures.json');

  // 3. Dashboard — 25 trajectories x 8 steps = ~200 transitions
  allData.dashboard = await captureSPA('dashboard', 'http://localhost:3849', 25, 8, async (page) => {
    const tab = TABS[Math.floor(Math.random() * TABS.length)];
    await page.click(`[data-tab="${tab}"]`);
    return { type: 'tab_click', target_href: tab };
  });
  saveData(allData, 'raw_dom_captures.json');

  // 4. Wizard — 25 trajectories x 8 steps = ~200 transitions
  allData.wizard = await captureSPA('wizard', 'http://localhost:3850', 25, 8, async (page, step) => {
    if (step % 4 === 3 && step > 0) {
      const btn = await page.$('#prev-btn');
      if (btn) { await btn.click(); return { type: 'button_click', target_href: 'prev' }; }
    }
    const btn = await page.$('#next-btn') || await page.$('#submit-btn');
    if (btn) { await btn.click(); return { type: 'button_click', target_href: 'next' }; }
    return null;
  });
  saveData(allData, 'raw_dom_captures.json');

  // Kill servers
  [s1, s2, s3, s4].forEach(s => { try { if (s && !s.killed) s.kill('SIGTERM'); } catch (e) {} });

  console.log('\\n' + '='.repeat(70));
  console.log('CAPTURE SUMMARY');
  console.log('='.repeat(70));
  let total = 0;
  for (const [key, trans] of Object.entries(allData)) {
    const uniqueStates = new Set(trans.map(t => t.state_after.dom_features.visible_text_hash));
    console.log(`  ${key}: ${trans.length} transitions, ${uniqueStates.size} unique visible-text-hash states`);
    total += trans.length;
  }
  console.log(`  TOTAL: ${total} transitions`);
  console.log('Output: raw_dom_captures.json');
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
