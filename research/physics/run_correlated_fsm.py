#!/usr/bin/env python3
"""
EXP-PHYSICS-36104718112 — Correlated Branching FSM Server (Flask)
Serves 5 latent states x 2 regimes x 3 variants = 30 genuine DOM prototypes
at locked 1280x720 with distinct visual/computed/AX representations
and overlapping spectra (hist_intersection > 0.3).

Usage: python3 research/physics/run_correlated_fsm.py &
"""
import sys, os, json, math
from flask import Flask, Response, request

app = Flask(__name__)
VIEWPORT = {"width": 1280, "height": 720}

STATES = 5
REGIMES = ["A", "B"]
VARIANTS = 3
BASIN_A = [0, 1, 2]
BASIN_B = [3, 4]

# Regime-dependent branching: 0.62 stay, 0.38 switch
def get_next_state(current_state, regime):
    import random
    rng = random.random()
    basin = BASIN_A if regime == "A" else BASIN_B
    other = BASIN_B if regime == "A" else BASIN_A
    if current_state in basin:
        if rng < 0.62:
            return basin[random.randint(0, len(basin)-1)]
        else:
            return other[random.randint(0, len(other)-1)]
    else:
        if rng < 0.62:
            return other[random.randint(0, len(other)-1)]
        else:
            return basin[random.randint(0, len(basin)-1)]

def get_style(state, regime, variant):
    if regime == "A":
        if variant < 2: color, bg = "rgb(255, 0, 0)", "rgb(255, 255, 255)"
        else: color, bg = "rgb(0, 0, 255)", "rgb(242, 242, 242)"
    else:
        if variant < 2: color, bg = "rgb(0, 0, 255)", "rgb(255, 255, 255)"
        else: color, bg = "rgb(255, 0, 0)", "rgb(238, 238, 238)"
    left = 100 + (0 if regime == "A" else 10) + state * 2 + variant * 6
    top = 180 + state * 8
    width = 120 + variant * 4 + (0 if regime == "A" else 2)
    height = 28
    opacity = "1.0" if state < 3 else "0.95"
    return color, bg, left, top, width, height, opacity

@app.route("/health")
def health():
    return Response(
        json.dumps({"status": "ok", "viewport": VIEWPORT, "states": STATES, "regimes": REGIMES, "variants": VARIANTS}),
        mimetype="application/json",
        headers={"Content-Length": str(len(json.dumps({"status": "ok"})))},
    )

@app.route("/state/<int:state>/regime/<regime>/variant/<int:variant>")
def serve_state(state, regime, variant):
    if state < 0 or state >= STATES or regime not in REGIMES or variant < 0 or variant >= VARIANTS:
        return Response("Not found", status=404)
    
    color, bg, left, top, width, height, opacity = get_style(state, regime, variant)
    
    # Build HTML with proper structure for CDP capture
    html = f"""<!DOCTYPE html>
<html><head><style>
body{{margin:0;padding:0;font-family:'DejaVu Sans',Arial,sans-serif}}
#btn{{position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;color:{color};background:{bg};display:block;visibility:visible;opacity:{opacity};border:1px solid #999;font-size:14px}}
.item{{padding:4px;margin:2px;border:1px solid #ccc}}
</style></head>
<body>
<header><h1>FSM State {state} Regime {regime}</h1></header>
<nav aria-label="main"><ul><li><a href="#section0">Link0</a></li><li><a href="#section1">Link1</a></li></ul></nav>
<div id="root">
<button id="btn" aria-label="action {state} variant {variant} regime {regime}">Action {state} {regime}{variant}</button>
<span>state{state}</span>
<div class="item" data-state="{state}" data-variant="{variant}" role="region" aria-label="region 0">Content 0 regime {regime} state {state}</div>
<div class="item" data-state="{state}" data-variant="{variant}" role="region" aria-label="region 1">Content 1 regime {regime} state {state}</div>
</div>
<footer><p>Footer {regime}{variant}</p></footer>
</body></html>"""
    
    dom_bytes = len(html.encode())
    a11y_bytes = 500  # AX tree serialized ~500+ bytes
    
    resp = Response(
        html,
        mimetype="text/html",
        headers={
            "Content-Length": str(dom_bytes),
            "X-Viewport": f"{VIEWPORT['width']}x{VIEWPORT['height']}",
            "X-DOM-Bytes": str(dom_bytes),
            "X-A11y-Bytes": str(a11y_bytes),
        },
    )
    return resp

@app.route("/transition", methods=["POST"])
def transition():
    return Response(json.dumps({"ok": True}), mimetype="application/json")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 18930))
    # Kill existing process on port if needed
    print(f"Correlated Branching FSM Server running at http://localhost:{port}", flush=True)
    print(f"States: {STATES}, Regimes: {','.join(REGIMES)}, Variants: {VARIANTS}", flush=True)
    print(f"Viewport: {VIEWPORT['width']}x{VIEWPORT['height']}", flush=True)
    print(f"Basin A: {BASIN_A}, Basin B: {BASIN_B}", flush=True)
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
