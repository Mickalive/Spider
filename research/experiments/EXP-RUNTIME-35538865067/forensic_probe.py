#!/usr/bin/env python3
"""EXP-RUNTIME-35538865067 forensic probe (diagnostic, post-frozen-matrix).

Re-serves the identical deterministic payload builders through a fresh
cloudflared quick tunnel and captures DELIVERED BYTES for byte-level
transform forensics. JSON/HTML builders are cross-process deterministic
(uuid5/sha-seeded); BINARY is rebuilt in-session and compared against
in-session origin bytes, so PYTHONHASHSEED dependence is moot.

Writes forensic_rows.json (raw delivered bytes as hex-sha + decode attempts).
"""
import gzip
import hashlib
import http.client
import http.server
import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import time
import urllib.parse

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_experiment as R

ORIGIN_PORT = 18792
OUT_PATH = HERE / "forensic_rows.json"


def raw_get(url, accept_encoding=None, timeout=30):
    pu = urllib.parse.urlparse(url)
    t0 = time.monotonic()
    conn = http.client.HTTPSConnection(pu.hostname, pu.port or 443, timeout=timeout)
    path = pu.path or "/"
    if pu.query:
        path += "?" + pu.query
    headers = {"Host": pu.hostname, "Connection": "close",
               "User-Agent": "SPIDER-FORENSIC-35538865067"}
    if accept_encoding is not None:
        headers["Accept-Encoding"] = accept_encoding
    try:
        conn.request("GET", path, headers=headers)
        resp = conn.getresponse()
        status = resp.status
        h = {k.lower(): v for k, v in resp.getheaders()}
        chunks = []
        while True:
            b = resp.read(8192)
            if not b:
                break
            chunks.append(b)
        body = b"".join(chunks)
        err = None
    except Exception as e:
        status, h, body, err = None, {}, b"", f"{type(e).__name__}: {e}"
    finally:
        try:
            conn.close()
        except Exception:
            pass
    return {"status": status, "headers": h, "body": body,
            "error": err, "rt_ms": round((time.monotonic() - t0) * 1000.0, 1)}


def try_decodes(body):
    out = {}
    try:
        out["gzip_dc_sha"] = hashlib.sha256(gzip.decompress(body)).hexdigest()
    except Exception as e:
        out["gzip_dc_sha"] = None
        out["gzip_dc_err"] = f"{type(e).__name__}"
    try:
        import brotli
        out["br_dc_sha"] = hashlib.sha256(brotli.decompress(body)).hexdigest()
    except Exception as e:
        out["br_dc_sha"] = None
        out["br_dc_err"] = f"{type(e).__name__}"
    try:
        out["iter_dc_sha"] = hashlib.sha256(R.fullbody_decompress(body)).hexdigest()
    except Exception as e:
        out["iter_dc_sha"] = None
        out["iter_dc_err"] = f"{type(e).__name__}"
    return out


def main():
    print("building payloads", flush=True)
    for ct in R.CONTENT_TYPES:
        body = R.BODY_GENERATORS[ct](R.AUTH_STATE, R.TARGET_SIZE)
        for order_key, (layers, served_ce) in R.ORDERS.items():
            comp = R.compress_layers(body, layers)
            pkey = f"{ct}_{order_key}"
            R.SERVE[pkey] = {"body": comp, "ce": served_ce,
                             "ctype": R.CONTENT_TYPES[ct]}
        pkey = f"{ct}_IDENTITY"
        R.SERVE[pkey] = {"body": body, "ce": None, "ctype": R.CONTENT_TYPES[ct]}
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", ORIGIN_PORT), R.OriginHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print("origin up", flush=True)
    with open(HERE / "forensic_tunnel.log", "w") as fl:
        tun = subprocess.Popen(
            [R.CLOUDFLARED_BIN, "tunnel", "--url",
             f"http://127.0.0.1:{ORIGIN_PORT}", "--no-autoupdate"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        import select
        fd = tun.stdout.fileno()
        buf, cdn_base, t0 = "", None, time.time()
        while time.time() - t0 < 90:
            r, _, _ = select.select([fd], [], [], 5.0)
            if not r:
                if cdn_base and "Registered tunnel connection" in buf:
                    break
                continue
            chunk = os.read(fd, 65536).decode("utf-8", "replace")
            if not chunk:
                break
            fl.write(chunk)
            fl.flush()
            buf += chunk
            m = re.search(r"https://[A-Za-z0-9-]+\.trycloudflare\.com", buf)
            if m and not cdn_base:
                cdn_base = m.group(0)
            if cdn_base and "Registered tunnel connection" in buf:
                break
        if not cdn_base:
            print("FORENSIC BLOCKED: no tunnel", flush=True)
            tun.terminate()
            return 3
    print(f"tunnel {cdn_base}", flush=True)
    ok = False
    for i in range(30):
        r = raw_get(cdn_base + "/health", timeout=20)
        if r["status"] == 200 and r["body"] == b"OK":
            ok = True
            break
        time.sleep(2)
    if not ok:
        print("FORENSIC BLOCKED: unreachable", flush=True)
        tun.terminate()
        return 3
    print("reachable", flush=True)
    rows = []
    combos = []
    for ct in R.CONTENT_TYPES:
        for order_key in list(R.ORDERS) + ["IDENTITY"]:
            for ae in ["both", "gzip", "br", "none"]:
                combos.append((f"{ct}_{order_key}", ae))
    import uuid as _uuid
    for pkey, ae in combos:
        tok = f"F{_uuid.uuid4().hex[:12]}"
        R.SERVE[tok] = R.SERVE[pkey]
        served = R.SERVE[pkey]["body"]
        ae_send = R.AE_VARIANTS[ae]
        got = raw_get(f"{cdn_base}/m/{tok}", accept_encoding=ae_send)
        body = got.pop("body")
        dec = try_decodes(body)
        rows.append({
            "payload_key": pkey, "accept_encoding": ae,
            "served_len": len(served),
            "served_sha256": hashlib.sha256(served).hexdigest(),
            "served_ce": R.SERVE[pkey]["ce"],
            "delivered_len": len(body),
            "delivered_sha256": hashlib.sha256(body).hexdigest(),
            "bytes_identical": hashlib.sha256(body).hexdigest() == hashlib.sha256(served).hexdigest(),
            "delivered_ce": got["headers"].get("content-encoding"),
            "cf_cache": got["headers"].get("cf-cache-status"),
            "server_hdr": got["headers"].get("server"),
            "status": got["status"], "rt_ms": got["rt_ms"],
            "decode_attempts": dec,
        })
        print(f"  {pkey} ae={ae}: identical={rows[-1]['bytes_identical']} "
              f"ce={rows[-1]['delivered_ce']} dlen={len(body)}", flush=True)
        time.sleep(0.4)
    with open(OUT_PATH, "w") as f:
        json.dump({"tunnel_url": cdn_base, "rows": rows}, f, indent=2)
    print(f"wrote {len(rows)} forensic rows", flush=True)
    tun.terminate()
    try:
        srv.shutdown()
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
