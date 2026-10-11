#!/usr/bin/env python3
"""EXECUTE controls driver for EXP-INTEL-38164607941 (intel lane, frozen design).

Implements prereg.md Appendix A. Single mode `preflight-and-controls`:

    --outdir <dir> --config <config.json> --chrome /usr/bin/google-chrome [--gguf-dir <dir>]

It imports the frozen parent primitives (run_episode, make_null_producer,
make_random_producer, start_page_server, parse_action) from
research/intel/run_exp_37982024058.py rather than re-implementing them, starts
the frozen page server, launches Chromium and explicitly navigates to the
served page BEFORE any episode (repairing the parent's about:blank control
defect; Appendix A.2). It writes <outdir>/raw/controls.json and
<outdir>/raw/preflight.json. No interpretation.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import sys
import traceback

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RUNNER = os.path.join(HERE, "run_exp_37982024058.py")
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38164607941")
FREEZE = os.path.join(EXP, "freeze.json")

PINNED_GGUF = {
    "qwen2.5-3b-instruct-q4_k_m.gguf": ("626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d", 2104932768),
    "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf": ("dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db", 3993201344),
    "qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf": ("539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a", 689872288),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def load_parent_module():
    spec = importlib.util.spec_from_file_location("parentrunner_37982024058", RUNNER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def make_oracle_producer():
    def producer(obs, step):
        act = {"action": "click", "selector": "#reveal-btn"} if step == 0 else {"action": "answer", "text": "TARGET-42"}
        return json.dumps(act), 0.0, 0, {"kind": "oracle"}

    return producer


def verify_freeze_artifacts():
    with open(FREEZE) as f:
        fr = json.load(f)
    out = {}
    ok = True
    for rel, want in fr["artifact_hashes"].items():
        p = os.path.join(REPO, rel)
        exists = os.path.exists(p)
        got = sha256_file(p) if exists else None
        match = (got == want)
        ok = ok and match
        out[rel] = {"exists": exists, "expected_sha256": want, "observed_sha256": got, "match": match}
    return ok, out


def verify_gguf_digests(gguf_dir):
    out = {}
    ok = True
    for name, (want_sha, want_bytes) in PINNED_GGUF.items():
        p = os.path.join(gguf_dir, name)
        exists = os.path.exists(p)
        got_sha = sha256_file(p) if exists else None
        got_bytes = os.path.getsize(p) if exists else None
        match = exists and (got_sha == want_sha) and (got_bytes == want_bytes)
        ok = ok and match
        out[name] = {"exists": exists, "expected_sha256": want_sha, "observed_sha256": got_sha,
                     "expected_bytes": want_bytes, "observed_bytes": got_bytes, "match": match}
    return ok, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--chrome", default="/usr/bin/google-chrome")
    ap.add_argument("--gguf-dir", default="/tmp/opencode/gguf")
    args = ap.parse_args()

    os.makedirs(os.path.join(args.outdir, "raw"), exist_ok=True)
    with open(args.config) as f:
        cfg = json.load(f)

    preflight = {"checks": {}, "freeze_artifact_hashes": {}, "gguf_digests": {}, "stack_imports": {}}

    # stack imports
    try:
        m = load_parent_module()
        preflight["stack_imports"] = {
            "parent_runner_import": True,
            "playwright": True,
            "llama_cpp": True,
            "has_parse_action": hasattr(m, "parse_action"),
            "has_start_page_server": hasattr(m, "start_page_server"),
            "has_make_null_producer": hasattr(m, "make_null_producer"),
            "has_make_random_producer": hasattr(m, "make_random_producer"),
            "has_run_episode": hasattr(m, "run_episode"),
        }
        stack_ok = all([preflight["stack_imports"]["parent_runner_import"],
                        preflight["stack_imports"]["playwright"],
                        preflight["stack_imports"]["llama_cpp"],
                        preflight["stack_imports"]["has_parse_action"],
                        preflight["stack_imports"]["has_start_page_server"],
                        preflight["stack_imports"]["has_make_null_producer"],
                        preflight["stack_imports"]["has_make_random_producer"],
                        preflight["stack_imports"]["has_run_episode"]])
    except Exception as e:
        preflight["stack_imports"] = {"error": str(e)[:500], "traceback": traceback.format_exc()[-1500:]}
        stack_ok = False

    freeze_ok, freeze_detail = verify_freeze_artifacts()
    preflight["freeze_artifact_hashes"] = freeze_detail
    gguf_ok, gguf_detail = verify_gguf_digests(args.gguf_dir)
    preflight["gguf_digests"] = gguf_detail

    controls = {}
    run_error = None
    if stack_ok:
        try:
            srv, port = m.start_page_server(cfg["task"]["page_html"])
            try:
                with sync_playwright() as p:
                    b = p.chromium.launch(executable_path=args.chrome, headless=True, args=["--no-sandbox"])
                    page = b.new_page()
                    page.goto("http://127.0.0.1:%d/" % port, timeout=20000)  # Appendix A.2 navigation repair

                    # PC-ORACLE-EPISODE
                    oracle = []
                    op = make_oracle_producer()
                    for ep in range(5):
                        r = m.run_episode(page, "", "", cfg["task"]["max_steps_per_episode"], op)
                        r["episode"] = ep
                        oracle.append(r)
                    controls["PC-ORACLE-EPISODE"] = {
                        "control_id": "PC-ORACLE-EPISODE",
                        "role": "positive_control_episode",
                        "criterion": "5/5 task_success=true",
                        "episodes": oracle,
                        "task_success_rate": sum(1 for e in oracle if e["task_success"]) / len(oracle),
                        "parseable_action_rate_step1": sum(1 for e in oracle if e["step1_parse_ok"]) / len(oracle),
                    }

                    # NC-NO-MODEL-ACTION
                    nc = cfg["null_control"]
                    np_ = m.make_null_producer(nc["fixed_invalid_content"])
                    nc_eps = []
                    for ep in range(nc["episodes"]):
                        r = m.run_episode(page, "", "", cfg["task"]["max_steps_per_episode"], np_)
                        r["episode"] = ep
                        nc_eps.append(r)
                    controls["NC-NO-MODEL-ACTION"] = {
                        "control_id": nc["id"],
                        "role": "null_control",
                        "criterion": nc["success_criterion"],
                        "episodes": nc_eps,
                        "parseable_action_rate_step1": sum(1 for e in nc_eps if e["step1_parse_ok"]) / len(nc_eps),
                        "task_success_rate": sum(1 for e in nc_eps if e["task_success"]) / len(nc_eps),
                    }

                    # B-RANDOM-ACTION
                    rb = cfg["random_baseline"]
                    rng = random.Random(cfg["sampling"]["base_seed"])
                    rp = m.make_random_producer(rb["action_space"], rng)
                    rand_eps = []
                    for ep in range(rb["episodes"]):
                        r = m.run_episode(page, "", "", cfg["task"]["max_steps_per_episode"], rp)
                        r["episode"] = ep
                        rand_eps.append(r)
                    controls["B-RANDOM-ACTION"] = {
                        "baseline_id": rb["id"],
                        "role": "negative_baseline",
                        "criterion": "parseable_action_rate_step1==1.0 AND task_success_rate<0.6",
                        "episodes": rand_eps,
                        "parseable_action_rate_step1": sum(1 for e in rand_eps if e["step1_parse_ok"]) / len(rand_eps),
                        "task_success_rate": sum(1 for e in rand_eps if e["task_success"]) / len(rand_eps),
                    }
                    b.close()
            finally:
                srv.shutdown()
        except Exception as e:
            run_error = {"error": str(e)[:800], "traceback": traceback.format_exc()[-2500:]}

    pc = controls.get("PC-ORACLE-EPISODE", {})
    nc = controls.get("NC-NO-MODEL-ACTION", {})
    rb = controls.get("B-RANDOM-ACTION", {})
    checks = {
        "PC_ORACLE_EPISODE_5of5": pc.get("task_success_rate") == 1.0,
        "NC_parseable_0_and_success_0": (nc.get("parseable_action_rate_step1") == 0.0 and nc.get("task_success_rate") == 0.0),
        "B_RANDOM_parseable_1_and_success_lt_0.6": (rb.get("parseable_action_rate_step1") == 1.0 and (rb.get("task_success_rate") is not None and rb.get("task_success_rate") < 0.6)),
        "freeze_artifact_hashes_match": bool(freeze_ok),
        "required_stack_imports_ok": bool(stack_ok),
        "gguf_digest_checks_pass": bool(gguf_ok),
    }
    preflight["checks"] = checks
    preflight["run_error"] = run_error
    preflight["pass"] = all(checks.values())

    with open(os.path.join(args.outdir, "raw", "controls.json"), "w") as f:
        json.dump(controls, f, indent=2, sort_keys=True)
    with open(os.path.join(args.outdir, "raw", "preflight.json"), "w") as f:
        json.dump(preflight, f, indent=2, sort_keys=True)

    print(json.dumps({"pass": preflight["pass"], "checks": checks}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
