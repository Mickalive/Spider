import json, re, sys, time, hashlib, httpx
from playwright.sync_api import sync_playwright

base, model = sys.argv[1], sys.argv[2]
max_steps = int(sys.argv[3]) if len(sys.argv) > 3 else 4
url = base.rstrip("/") + "/chat/completions"

PAGE = """data:text/html,<html><body>
<h1>Vault</h1>
<button id='reveal-btn'>Reveal code</button>
<div id='code'></div>
<script>document.getElementById('reveal-btn').onclick=function(){document.getElementById('code').textContent='TARGET-42';};</script>
</body></html>"""
SYS = ("You are a web agent. Reply ONLY with one JSON object per turn, no prose. "
       "Actions: {\"action\":\"click\",\"ref\":\"<id>\"} or {\"action\":\"answer\",\"text\":\"<code>\"}. "
       "Click the button to reveal the code, then answer it.")

def parse(txt):
    m = re.search(r'\{.*\}', txt, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def call(messages):
    body = {"model": model, "messages": messages, "temperature": 0, "max_tokens": 1200}
    last = None
    for attempt in range(6):
        try:
            r = httpx.post(url, json=body, timeout=90)
            if r.status_code == 200:
                return r.json()
            last = {"http": r.status_code, "body": r.text[:200]}
        except Exception as e:
            last = {"err": str(e)[:150]}
        time.sleep(6)
    return {"error": last}

def obs(page, history):
    els = page.eval_on_selector_all("button, a, input", "els => els.map(e => ({tag:e.tagName, id:e.id||'', text:(e.innerText||'').slice(0,40)}))")
    body = page.inner_text("body")[:300]
    return f"PAGE_TEXT: {body}\nELEMENTS: {json.dumps(els)}\nHISTORY: {history}"

receipt = {"base_url": base, "model": model, "max_steps": max_steps, "turns": [], "success_condition": "final answer == TARGET-42"}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=["--no-sandbox"])
        page = b.new_page(); page.goto(PAGE, timeout=20000)
        history=[]; final=None; t0=time.time(); tot=0
        for step in range(max_steps):
            o = obs(page, history)
            resp = call([{"role":"system","content":SYS},{"role":"user","content":o}])
            if "error" in resp:
                receipt["turns"].append({"step":step,"error":resp["error"]}); break
            msg = resp["choices"][0]["message"]; txt = (msg.get("content") or "") + ("\n"+(msg.get("reasoning") or "") if msg.get("reasoning") else "")
            tok = (resp.get("usage") or {}).get("total_tokens",0) or 0
            tot += tok
            act = parse(txt)
            receipt["turns"].append({"step":step,"raw":txt[:300],"action":act,"tokens":tok})
            if not act: break
            if act.get("action")=="click":
                try: page.click("#"+str(act["ref"]).lstrip("#"), timeout=8000); history.append("clicked "+str(act["ref"]))
                except Exception as e: history.append("click error "+str(e)[:60])
            elif act.get("action")=="answer":
                final=str(act.get("text","")); break
            else: break
        receipt["final_answer"]=final; receipt["success"]=(final=="TARGET-42")
        receipt["latency_s"]=round(time.time()-t0,3); receipt["total_tokens"]=tot
        b.close()
except Exception as e:
    receipt["error"]=str(e)[:500]
receipt["receipt_sha256"]=hashlib.sha256(json.dumps(receipt,sort_keys=True).encode()).hexdigest()
print(json.dumps(receipt))
