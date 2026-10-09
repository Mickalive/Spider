import json, time
from playwright.sync_api import sync_playwright
out={}
try:
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=["--no-sandbox"])
            out["launch_channel"]="executable_path:/usr/bin/google-chrome"
        except Exception as e1:
            out["launch_exec_error"]=str(e1)[:300]
            b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
            out["launch_channel"]="channel:chrome"
        pg = b.new_page()
        t0=time.time()
        pg.goto("data:text/html,<title>SPIDER</title><h1 id=x>hello</h1>", timeout=20000)
        title=pg.title(); txt=pg.inner_text("#x")
        out.update({"title":title,"text":txt,"latency_s":round(time.time()-t0,3),"browser":b.browser_type.name,"version":b.version})
        b.close()
except Exception as e:
    out["error"]=str(e)[:500]
print(json.dumps(out))
