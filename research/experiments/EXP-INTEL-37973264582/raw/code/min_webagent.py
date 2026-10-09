import json, re, sys, time, hashlib
from openai import OpenAI
from playwright.sync_api import sync_playwright

base, model = sys.argv[1], sys.argv[2]
max_steps = int(sys.argv[3]) if len(sys.argv) > 3 else 4
client = OpenAI(base_url=base, api_key="sk-noauth", timeout=90)

PAGE = """data:text/html,<html><body>
<h1>Vault</h1>
<button id='reveal-btn'>Reveal code</button>
<div id='code'></div>
<script>document.getElementById('reveal-btn').onclick=function(){document.getElementById('code').textContent='TARGET-42';};</script>
</body></html>"""

SYS = ("You are a web agent. Reply ONLY with one JSON object per turn, no prose. "
       "Actions available: {\"action\":\"click\",\"ref\":\"<id>\"} or "
       "{\"action\":\"answer\",\"text\":\"<code>\"}. Click the button to reveal the code, then answer it.")

def parse(txt):
    m = re.search(r'\{.*\}', txt, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def obs(page, history):
    els = page.eval_on_selector_all("button, a, input", "els => els.map(e => ({tag:e.tagName, id:e.id||'', text:(e.innerText||'').slice(0,40)}))")
    body = page.inner_text("body")[:300]
    return f"PAGE_TEXT: {body}\nELEMENTS: {json.dumps(els)}\nHISTORY: {history}"

receipt = {"base_url": base, "model": model, "max_steps": max_steps, "turns": [], "success_condition": "final answer == TARGET-42"}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=["--no-sandbox"])
        page = b.new_page(); page.goto(PAGE, timeout=20000)
        history=[]; final=None; t0=time.time(); tot_tok=0
        for step in range(max_steps):
            o = obs(page, history)
            r = client.chat.completions.create(model=model,
                messages=[{"role":"system","content":SYS},{"role":"user","content":o}],
                temperature=0, max_tokens=120)
            txt = r.choices[0].message.content or ""
            tok = getattr(r.usage,"total_tokens",0) or 0
            tot_tok += tok
            act = parse(txt)
            receipt["turns"].append({"step":step,"raw":txt[:400],"action":act,"tokens":tok})
            if not act: break
            if act.get("action")=="click":
                try: page.click(f"#{act['ref']}" if not str(act['ref']).startswith('#') else act['ref'], timeout=8000); history.append(f"clicked {act['ref']}")
                except Exception as e: history.append(f"click error {str(e)[:80]}")
            elif act.get("action")=="answer":
                final = str(act.get("text","")); break
            else: break
        receipt["final_answer"] = final
        receipt["success"] = (final=="TARGET-42")
        receipt["latency_s"] = round(time.time()-t0,3)
        receipt["total_tokens"] = tot_tok
        b.close()
except Exception as e:
    receipt["error"] = str(e)[:500]
receipt["receipt_sha256"] = hashlib.sha256(json.dumps(receipt,sort_keys=True).encode()).hexdigest()
print(json.dumps(receipt))
