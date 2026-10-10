#!/usr/bin/env python3
"""EXECUTE harness for EXP-INTEL-37982024058 (intel lane, frozen design).

Frozen design: research/experiments/EXP-INTEL-37982024058/{spec.json,prereg.md,freeze.json}
Harness fixture: research/experiments/EXP-INTEL-37982024058/raw/harness_config.json

Modes:
  probe-candidate  : load one candidate GGUF, run PC-JSON-CONSTRAINED-DECODING and
                     5 minimal-Web-agent episodes; append a model receipt.
  null-random      : run NC-NO-MODEL-ACTION and B-RANDOM-ACTION controls.

Raw evidence is written under <outdir>/raw/. This script performs no scientific
interpretation; it records raw completions, parsed actions and mechanical outcomes.
"""
import argparse
import hashlib
import json
import os
import random
import re
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from llama_cpp import Llama, LlamaGrammar
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_DIR_DEFAULT = os.path.abspath(os.path.join(HERE, "..", "experiments", "EXP-INTEL-37982024058"))


def load_config(outdir):
    with open(os.path.join(outdir, "raw", "harness_config.json")) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# HTTP server for the frozen synthetic page
# ---------------------------------------------------------------------------
def start_page_server(page_html):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = page_html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, srv.server_address[1]


# ---------------------------------------------------------------------------
# Frozen parsing / schema validation
# ---------------------------------------------------------------------------
def parse_action(raw):
    """Strict parse: the full completion must be valid JSON (prereg section 4).

    Returns (action_or_None, parse_ok, detail).
    """
    if raw is None:
        return None, False, "no_content"
    text = raw.strip()
    if text == "":
        return None, False, "empty"
    try:
        obj = json.loads(text)
    except Exception as e:
        return None, False, "json_error: %s" % (str(e)[:120])
    if not isinstance(obj, dict):
        return None, False, "not_object"
    act = obj.get("action")
    if act == "click":
        sel = obj.get("selector")
        if not isinstance(sel, str) or sel.strip() == "":
            return None, False, "click_missing_selector"
        return {"action": "click", "selector": sel}, True, "ok"
    if act == "answer":
        txt = obj.get("text")
        if not isinstance(txt, str):
            return None, False, "answer_missing_text"
        return {"action": "answer", "text": txt}, True, "ok"
    return None, False, "bad_action_value:%r" % (act,)


def regex_parse_action(raw):
    """Secondary observation only (not used for any metric)."""
    try:
        m = re.search(r"\{.*\}", raw or "", re.S)
        if not m:
            return None
        return json.loads(m.group(0))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Page observation (identical style to parent EXP-INTEL-37973264582 harness)
# ---------------------------------------------------------------------------
def observe(page, history):
    els = page.eval_on_selector_all(
        "button, a, input",
        "els => els.map(e => ({tag:e.tagName, id:e.id||'', text:(e.innerText||'').slice(0,40)}))",
    )
    body = page.inner_text("body")[:300]
    return {
        "page_text": body,
        "elements": els,
        "history": list(history),
    }


def render_user_prompt(tpl, obs):
    return tpl.format(
        page_text=obs["page_text"],
        elements_json=json.dumps(obs["elements"]),
        history=json.dumps(obs["history"]),
    )


# ---------------------------------------------------------------------------
# Episode runner (works for model, null-control and random-baseline producers)
# ---------------------------------------------------------------------------
def run_episode(page, system_prompt, user_tpl, max_steps, step_producer, threshold="TARGET-42"):
    """step_producer(obs, step_idx) -> (raw_completion, latency_s, completion_tokens, producer_meta)

    Returns an episode record with raw evidence and mechanical outcome.
    """
    page.goto(page.url, timeout=20000)
    history = []
    revealed_value = None
    clicked_reveal = False
    final_answer = None
    steps = []
    step1_parse_ok = None
    for step in range(max_steps):
        obs = observe(page, history)
        prompt = render_user_prompt(user_tpl, obs)
        raw, latency, tokens, meta = step_producer(obs, step)
        action, parse_ok, detail = parse_action(raw)
        rec = {
            "step": step,
            "raw": raw,
            "action": action,
            "parse_ok": parse_ok,
            "parse_detail": detail,
            "regex_action": regex_parse_action(raw),
            "latency_s": latency,
            "completion_tokens": tokens,
            "producer_meta": meta,
        }
        if step == 0:
            step1_parse_ok = parse_ok
        if not parse_ok:
            steps.append(rec)
            break
        if action["action"] == "click":
            sel = action["selector"].strip()
            if not sel.startswith("#"):
                sel = "#" + sel
            try:
                page.click(sel, timeout=8000)
                rec["click_ok"] = True
                rec["click_selector"] = sel
                # mechanical reveal detection
                try:
                    if page.locator("#target").is_visible():
                        revealed_value = page.locator("#target").inner_text().strip()
                        clicked_reveal = True
                except Exception:
                    pass
                history.append("clicked %s" % sel)
            except Exception as e:
                rec["click_ok"] = False
                rec["click_selector"] = sel
                history.append("click error %s" % str(e)[:80])
            steps.append(rec)
        elif action["action"] == "answer":
            final_answer = action["text"]
            rec["answer_text"] = final_answer
            steps.append(rec)
            break
    success = (
        clicked_reveal
        and revealed_value == threshold
        and final_answer is not None
        and final_answer.strip() == threshold
    )
    # mechanical re-verification of the terminal page state
    try:
        final_target_visible = page.locator("#target").is_visible()
        final_target_text = page.locator("#target").inner_text().strip() if final_target_visible else None
    except Exception:
        final_target_visible = None
        final_target_text = None
    return {
        "steps": steps,
        "step_count": len(steps),
        "step1_parse_ok": bool(step1_parse_ok),
        "clicked_reveal": clicked_reveal,
        "revealed_value": revealed_value,
        "final_answer": final_answer,
        "final_target_visible": final_target_visible,
        "final_target_text": final_target_text,
        "task_success": bool(success),
    }


# ---------------------------------------------------------------------------
# Model-backed producers
# ---------------------------------------------------------------------------
def make_model_producer(llm, system_prompt, grammar, seed_base, meta):
    calls = {"n": 0}

    def producer(obs, step):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": render_user_prompt(meta["user_tpl"], obs)},
        ]
        t0 = time.time()
        resp = llm.create_chat_completion(
            messages=messages,
            temperature=meta["temperature"],
            max_tokens=meta["max_tokens"],
            seed=seed_base,
            grammar=grammar,
        )
        latency = round(time.time() - t0, 3)
        raw = (resp["choices"][0]["message"].get("content") or "")
        usage = resp.get("usage", {}) or {}
        calls["n"] += 1
        return raw, latency, int(usage.get("completion_tokens", 0) or 0), {"call": calls["n"]}

    return producer


def make_null_producer(fixed_invalid):
    def producer(obs, step):
        return fixed_invalid, 0.0, 0, {"kind": "null_control"}

    return producer


def make_random_producer(action_space, rng):
    def producer(obs, step):
        action = dict(rng.choice(action_space))
        return json.dumps(action), 0.0, 0, {"kind": "random_baseline"}

    return producer


# ---------------------------------------------------------------------------
# Positive control
# ---------------------------------------------------------------------------
def run_positive_control(llm, cfg, grammar, model_meta):
    probes = []
    pc = cfg["positive_control"]
    sys_p = cfg["prompts"]["system"]
    probe_p = cfg["prompts"]["positive_control_probe"]
    for i in range(pc["probes"]):
        t0 = time.time()
        resp = llm.create_chat_completion(
            messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": probe_p}],
            temperature=cfg["sampling"]["temperature"],
            max_tokens=cfg["sampling"]["max_tokens"],
            seed=cfg["sampling"]["llama_seed"],
            grammar=grammar,
        )
        latency = round(time.time() - t0, 3)
        raw = (resp["choices"][0]["message"].get("content") or "")
        usage = resp.get("usage", {}) or {}
        action, parse_ok, detail = parse_action(raw)
        probes.append({
            "probe": i,
            "raw": raw,
            "action": action,
            "parse_ok": parse_ok,
            "parse_detail": detail,
            "latency_s": latency,
            "completion_tokens": int(usage.get("completion_tokens", 0) or 0),
        })
    n_pass = sum(1 for p in probes if p["parse_ok"])
    return {
        "control_id": pc["id"],
        "probes": probes,
        "n_pass": n_pass,
        "n_total": pc["probes"],
        "pass_rate": n_pass / pc["probes"],
        "criterion": pc["success_criterion"],
        "pass": n_pass == pc["probes"],
    }


# ---------------------------------------------------------------------------
# Model load
# ---------------------------------------------------------------------------
def load_model(paths, chat_format, base_seed, n_ctx, n_threads):
    t0 = time.time()
    llm = Llama(
        model_path=paths[0],
        n_ctx=n_ctx,
        n_threads=n_threads,
        verbose=False,
        chat_format=chat_format,
        seed=base_seed,
    )
    return llm, round(time.time() - t0, 3)


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------
def mode_probe_candidate(args):
    outdir = args.outdir
    cfg = load_config(outdir)
    rawdir = os.path.join(outdir, "raw")
    os.makedirs(rawdir, exist_ok=True)
    cand = next(c for c in cfg["candidate_models_frozen"] if c["candidate_id"] == args.candidate)
    receipt = {
        "candidate_id": args.candidate,
        "role": cand["role"],
        "model": cand["model"],
        "quant": cand["quant"],
        "frozen_url": cand["frozen_url"],
        "gguf_paths": args.gguf,
        "gguf_bytes": [os.path.getsize(p) for p in args.gguf],
        "gguf_sha256": [hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.getsize(p) < 3_000_000_000 else sha256_file(p) for p in args.gguf],
        "load_time_s": None,
        "load_status": "NOT_ATTEMPTED",
        "load_error": None,
        "positive_control": None,
        "episodes": [],
        "config_sampling": cfg["sampling"],
    }
    grammar = LlamaGrammar.from_string(cfg["gbnf_grammar"])
    try:
        llm, load_t = load_model(
            args.gguf, cfg["sampling"]["chat_format"], cfg["sampling"]["llama_seed"],
            cfg["sampling"]["n_ctx"], args.n_threads,
        )
        receipt["load_time_s"] = load_t
        receipt["load_status"] = "LOADED"
        receipt["load_meta"] = {
            "n_ctx": cfg["sampling"]["n_ctx"],
            "chat_format": cfg["sampling"]["chat_format"],
            "llama_seed": cfg["sampling"]["llama_seed"],
            "n_threads": args.n_threads,
        }
    except Exception as e:
        receipt["load_status"] = "LOAD_FAILED"
        receipt["load_error"] = str(e)[:800]
        _append_json_list(os.path.join(rawdir, "model_receipts.json"), receipt)
        print(json.dumps({"candidate": args.candidate, "load_status": "LOAD_FAILED",
                          "load_error": receipt["load_error"]}))
        return 0

    # Positive control + episodes; crash-safe so partial raw evidence is preserved.
    receipt["run_status"] = "COMPLETE"
    try:
        # Positive control
        receipt["positive_control"] = run_positive_control(llm, cfg, grammar, receipt)
        print(json.dumps({"candidate": args.candidate, "positive_control_pass_rate":
                          receipt["positive_control"]["pass_rate"]}))

        # Episodes (only if positive control passes, per frozen decision rule step 1)
        if receipt["positive_control"]["pass"]:
            srv, port = start_page_server(cfg["task"]["page_html"])
            try:
                with sync_playwright() as p:
                    b = p.chromium.launch(executable_path=args.chrome, headless=True, args=["--no-sandbox"])
                    page = b.new_page()
                    page.goto("http://127.0.0.1:%d/" % port, timeout=20000)
                    meta = {
                        "user_tpl": cfg["prompts"]["user_template"],
                        "temperature": cfg["sampling"]["temperature"],
                        "max_tokens": cfg["sampling"]["max_tokens"],
                    }
                    n_ep = cfg["clearing_threshold"]["episodes"]
                    for ep in range(n_ep):
                        seed = cfg["sampling"]["base_seed"] + ep
                        prod = make_model_producer(llm, cfg["prompts"]["system"], grammar, seed, meta)
                        ep_rec = run_episode(page, cfg["prompts"]["system"], cfg["prompts"]["user_template"],
                                             cfg["task"]["max_steps_per_episode"], prod)
                        ep_rec["episode"] = ep
                        ep_rec["seed"] = seed
                        receipt["episodes"].append(ep_rec)
                        print(json.dumps({"candidate": args.candidate, "episode": ep,
                                          "step1_parse_ok": ep_rec["step1_parse_ok"],
                                          "task_success": ep_rec["task_success"],
                                          "steps": ep_rec["step_count"]}))
                        if ep_rec["task_success"]:
                            pass  # no early stop within a model; all 5 episodes are the frozen unit
                    b.close()
            finally:
                srv.shutdown()
        else:
            receipt["episodes"] = []
            receipt["positive_control_excluded"] = True
    except Exception as e:
        import traceback
        receipt["run_status"] = "RUN_ERROR"
        receipt["run_error"] = str(e)[:800]
        receipt["run_traceback"] = traceback.format_exc()[-3000:]
        _append_json_list(os.path.join(rawdir, "model_receipts.json"), receipt)
        print(json.dumps({"candidate": args.candidate, "run_error": receipt["run_error"]}))
        return 1

    _append_json_list(os.path.join(rawdir, "model_receipts.json"), receipt)
    return 0


def mode_null_random(args):
    outdir = args.outdir
    cfg = load_config(outdir)
    rawdir = os.path.join(outdir, "raw")
    os.makedirs(rawdir, exist_ok=True)
    srv, port = start_page_server(cfg["task"]["page_html"])
    out = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=args.chrome, headless=True, args=["--no-sandbox"])
            page = b.new_page()
            # NC-NO-MODEL-ACTION
            nc = cfg["null_control"]
            nc_eps = []
            null_prod = make_null_producer(nc["fixed_invalid_content"])
            for ep in range(nc["episodes"]):
                r = run_episode(page, "", "", cfg["task"]["max_steps_per_episode"], null_prod)
                r["episode"] = ep
                nc_eps.append(r)
            out["NC-NO-MODEL-ACTION"] = {
                "control_id": nc["id"],
                "episodes": nc_eps,
                "parseable_action_rate_step1": sum(1 for e in nc_eps if e["step1_parse_ok"]) / len(nc_eps),
                "task_success_rate": sum(1 for e in nc_eps if e["task_success"]) / len(nc_eps),
                "criterion": nc["success_criterion"],
            }
            # B-RANDOM-ACTION
            rb = cfg["random_baseline"]
            rng = random.Random(cfg["sampling"]["base_seed"])
            rand_eps = []
            rand_prod = make_random_producer(rb["action_space"], rng)
            for ep in range(rb["episodes"]):
                r = run_episode(page, "", "", cfg["task"]["max_steps_per_episode"], rand_prod)
                r["episode"] = ep
                rand_eps.append(r)
            out["B-RANDOM-ACTION"] = {
                "baseline_id": rb["id"],
                "episodes": rand_eps,
                "parseable_action_rate_step1": sum(1 for e in rand_eps if e["step1_parse_ok"]) / len(rand_eps),
                "task_success_rate": sum(1 for e in rand_eps if e["task_success"]) / len(rand_eps),
            }
        with open(os.path.join(rawdir, "control_episodes.json"), "w") as f:
            json.dump(out, f, indent=2, sort_keys=True)
        print(json.dumps({
            "NC_parseable_step1": out["NC-NO-MODEL-ACTION"]["parseable_action_rate_step1"],
            "NC_success": out["NC-NO-MODEL-ACTION"]["task_success_rate"],
            "RANDOM_parseable_step1": out["B-RANDOM-ACTION"]["parseable_action_rate_step1"],
            "RANDOM_success": out["B-RANDOM-ACTION"]["task_success_rate"],
        }))
    finally:
        srv.shutdown()
    return 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _append_json_list(path, entry):
    data = []
    if os.path.exists(path):
        with open(path) as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
    data = [d for d in data if d.get("candidate_id") != entry.get("candidate_id")]
    data.append(entry)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["probe-candidate", "null-random"])
    ap.add_argument("--outdir", default=EXP_DIR_DEFAULT)
    ap.add_argument("--candidate", default=None)
    ap.add_argument("--gguf", nargs="+", default=None)
    ap.add_argument("--chrome", default="/usr/bin/google-chrome")
    ap.add_argument("--n-threads", type=int, default=4)
    args = ap.parse_args()
    if args.mode == "probe-candidate":
        return mode_probe_candidate(args)
    return mode_null_random(args)


if __name__ == "__main__":
    sys.exit(main())
