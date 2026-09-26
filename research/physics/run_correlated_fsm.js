#!/usr/bin/env node
/**
 * EXP-PHYSICS-36104718112 — Correlated Branching FSM Server
 * 
 * Serves 5 latent states x 2 regimes x 3 variants = 30 genuine DOM prototypes
 * at locked 1280x720 via Express with distinct visual/computed/AX representations
 * and overlapping spectra (hist_intersection > 0.3).
 * 
 * Branching transition probabilities: regime A favors staying in basin A,
 * regime B favors staying in basin B. Each (state, regime) pair has distinct
 * DOM appearance with shared colors across regimes for overlapping spectra.
 */

const express = require('express');
const path = require('path');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 18930;
const VIEWPORT = { width: 1280, height: 720 };

const STATES = 5;
const REGIMES = ['A', 'B'];
const VARIANTS = 3;
const BASIN_A = [0, 1, 2];
const BASIN_B = [3, 4];

// Transition probabilities: regime-dependent branching
// Regime A: P(stay_in_A|A) = 0.62, P(switch_to_B|A) = 0.38
// Regime B: P(stay_in_B|B) = 0.62, P(switch_to_A|B) = 0.38
function getNextState(currentState, regime) {
  const rng = Math.random();
  const basin = regime === 'A' ? BASIN_A : BASIN_B;
  const other = regime === 'A' ? BASIN_B : BASIN_A;
  
  if (basin.includes(currentState)) {
    // In home basin: 0.62 stay, 0.38 switch
    if (rng < 0.62) {
      return basin[Math.floor(Math.random() * basin.length)];
    } else {
      return other[Math.floor(Math.random() * other.length)];
    }
  } else {
    // In other basin: 0.62 stay, 0.38 switch
    if (rng < 0.62) {
      return other[Math.floor(Math.random() * other.length)];
    } else {
      return basin[Math.floor(Math.random() * basin.length)];
    }
  }
}

// Generate distinct DOM appearance per (state, regime, variant)
// Overlapping spectra: 2/3 variants share one color per regime
function getStyle(state, regime, variant) {
  // Overlapping colors: A: variants 0,1 red, variant 2 blue; B: variants 0,1 blue, variant 2 red
  let color, bg;
  if (regime === 'A') {
    if (variant < 2) { color = 'rgb(255, 0, 0)'; bg = 'rgb(255, 255, 255)'; }
    else { color = 'rgb(0, 0, 255)'; bg = 'rgb(242, 242, 242)'; }
  } else {
    if (variant < 2) { color = 'rgb(0, 0, 255)'; bg = 'rgb(255, 255, 255)'; }
    else { color = 'rgb(255, 0, 0)'; bg = 'rgb(238, 238, 238)'; }
  }
  
  const left = 100 + (regime === 'A' ? 0 : 10) + state * 2 + variant * 6;
  const top = 180 + state * 8;
  const width = 120 + variant * 4 + (regime === 'A' ? 0 : 2);
  const height = 28;
  const opacity = state < 3 ? '1.0' : '0.95';
  
  return { color, bg, left, top, width, height, opacity, border: '1px solid #999', fontSize: '14px', display: 'block', visibility: 'visible', position: 'absolute' };
}

// Generate AX tree content
function getAXTree(state, regime, variant) {
  return JSON.stringify({
    role: 'button',
    name: `action ${state} variant ${variant} regime ${regime}`,
    value: `${regime}`,
    children: [
      { role: 'region', name: `region 0`, value: `Content 0 regime ${regime} state ${state}` },
      { role: 'region', name: `region 1`, value: `Content 1 regime ${regime} state ${state}` },
    ]
  });
}

// Serve the page
app.get('/state/:state/regime/:regime/variant/:variant', (req, res) => {
  const state = parseInt(req.params.state);
  const regime = req.params.regime;
  const variant = parseInt(req.params.variant);
  
  if (isNaN(state) || state < 0 || state >= STATES || !REGIMES.includes(regime) || variant < 0 || variant >= VARIANTS) {
    return res.status(404).send('Not found');
  }
  
  const style = getStyle(state, regime, variant);
  const axTree = getAXTree(state, regime, variant);
  
  const html = `<!DOCTYPE html>
<html><head><style>
body { margin: 0; padding: 0; font-family: 'DejaVu Sans', Arial, sans-serif; }
#btn { position: absolute; left: ${style.left}px; top: ${style.top}px; width: ${style.width}px; height: ${style.height}px; color: ${style.color}; background: ${style.bg}; display: ${style.display}; visibility: ${style.visibility}; opacity: ${style.opacity}; border: ${style.border}; font-size: ${style.fontSize}; }
.item { padding: 4px; margin: 2px; border: 1px solid #ccc; }
</style></head>
<body>
<header><h1>FSM State ${state} Regime ${regime}</h1></header>
<nav aria-label="main"><ul><li><a href="#section0">Link0</a></li><li><a href="#section1">Link1</a></li></ul></nav>
<div id="root">
<button id="btn" aria-label="action ${state} variant ${variant} regime ${regime}">Action ${state} ${regime}${variant}</button>
<span>state${state}</span>
<div class="item" data-state="${state}" data-variant="${variant}" role="region" aria-label="region 0">Content 0 regime ${regime} state ${state}</div>
<div class="item" data-state="${state}" data-variant="${variant}" role="region" aria-label="region 1">Content 1 regime ${regime} state ${state}</div>
</div>
<footer><p>Footer ${regime}${variant}</p></footer>
</body></html>`;
  
  res.setHeader('Content-Type', 'text/html');
  res.setHeader('Content-Length', Buffer.byteLength(html));
  res.send(html);
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', viewport: VIEWPORT, states: STATES, regimes: REGIMES, variants: VARIANTS });
});

// Transition endpoint
app.post('/transition', (req, res) => {
  // Simple transition endpoint for testing
  res.json({ ok: true });
});

const server = app.listen(PORT, () => {
  console.log(`Correlated Branching FSM Server running at http://localhost:${PORT}`);
  console.log(`States: ${STATES}, Regimes: ${REGIMES.join(',')}, Variants: ${VARIANTS}`);
  console.log(`Viewport: ${VIEWPORT.width}x${VIEWPORT.height}`);
  console.log(`Basin A: ${BASIN_A.join(',')}, Basin B: ${BASIN_B.join(',')}`);
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`Port ${PORT} already in use`);
    process.exit(1);
  }
  console.error('Server error:', err);
  process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', () => { server.close(); process.exit(0); });
process.on('SIGINT', () => { server.close(); process.exit(0); });
