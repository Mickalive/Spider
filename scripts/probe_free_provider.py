#!/usr/bin/env python3
"""Zero-priced OpenCode availability/credential preflight.

Runs in GitHub Actions *before* dispatching expensive scientific stages.
Attempts only explicitly allowlisted, documented-free models. Receipts have
no raw provider text (which could contain credentials or task data).
A green CI proves the classifier, not that an external provider is healthy.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROBE_TOKEN = "SPIDER_FREE_PROVIDER_READY"
AUTH = re.compile(
    r"invalid credential|invalid api.?key|missing api.?key|authentication failed|"
    r"unauthori[sz]ed|invalid token|status[^0-9]*401|http[^0-9]*401",
    re.I,
)
DENIED = re.compile(
    r"the user rejected permission|the user has specified a rule which prevents|"
    r"permission denied|requires permission approval", re.I
)
OUTAGE = re.compile(
    r"model is unavailable|model.*(not found|deprecated)|unexpected server error|"
    r"upstream.*(overload|unavailable|error)|503|429|rate.?limit|fetch failed|"
    r"network error|timed out|connection reset|unknownerror", re.I,
)


def classify(output: str, returncode: int, timeout: bool = False) -> str:
    """Auth/security failures take precedence; never hide them behind a 503."""
    output = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", output)
    if AUTH.search(output):
        return "AUTH_INVALID"
    if DENIED.search(output):
        return "PERMISSION_DENIED"
    if timeout:
        return "TIMEOUT"
    if returncode == 0 and re.search(rf"(?m)^\s*{PROBE_TOKEN}\s*$", output):
        return "READY"
    if OUTAGE.search(output):
        return "SERVICE_UNAVAILABLE"
    return "NO_ATTESTED_OUTPUT"


def run_probe(binary: str, model: str, deadline: int) -> str:
    # Never give a probe access to the filesystem or any GitHub/model secrets
    # except the authentication the chosen OpenCode provider itself requires.
    prompt = f"Reply with EXACTLY the single string {PROBE_TOKEN}. No tools, no explanation."
    argv = [binary, "run", "--model", model, "--agent", "spider_provider_probe", prompt]
    try:
        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, errors="replace", start_new_session=True)
    except OSError:
        return "BINARY_UNAVAILABLE"
    try:
        stdout, stderr = proc.communicate(timeout=deadline)
        return classify((stdout or "") + "\n" + (stderr or ""), proc.returncode)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.communicate()
        return "TIMEOUT"


def allowed_candidates(config: dict, limit: int) -> list[str]:
    if config.get("free_only") is not True:
        raise ValueError("paid model configuration forbidden")
    approved = set(config["free_only_allowed_models"])
    if not approved:
        raise ValueError("no verified free models available")
    models = []
    # Two roles/families to distinguish a model outage from auth-wide failure.
    for role in ("scout", "director", "research"):
        for model in config["roles"][role]:
            if model not in approved or not model.startswith("opencode/"):
                raise ValueError("model outside reviewed no-payment allowlist")
            if model not in models:
                models.append(model)
    return models[:limit]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config/models.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bin", default=str(Path.home() / ".opencode/bin/opencode"))
    parser.add_argument("--max-models", type=int, default=3)
    parser.add_argument("--per-model-seconds", type=int, default=45)
    args = parser.parse_args()
    if not (1 <= args.max_models <= 3 and 5 <= args.per_model_seconds <= 90):
        parser.error("bounded free model preflight only: <=3 models, 5–90 seconds each")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    choices = allowed_candidates(config, args.max_models)
    policy_path = Path(".github/scripts/opencode-ci-permissions.json")
    if not policy_path.is_file():
        raise SystemExit("SPIDER_PREFLIGHT_NO_HEADLESS_POLICY")
    os.environ["OPENCODE_CONFIG_CONTENT"] = policy_path.read_text(encoding="utf-8")
    attempts = []
    for model in choices:
        status = run_probe(args.bin, model, args.per_model_seconds)
        attempts.append({"model": model, "status": status})
        print(f"SPIDER_PROVIDER_CHECK model={model} category={status}", flush=True)
        if status == "READY":
            break
    ready = any(item["status"] == "READY" for item in attempts)
    reasons = [a["status"] for a in attempts]
    if ready:
        category = "READY"
    elif "AUTH_INVALID" in reasons:
        category = "AUTH_INVALID"
    elif "PERMISSION_DENIED" in reasons:
        category = "PERMISSION_DENIED"
    elif "TIMEOUT" in reasons:
        category = "TIMEOUT"
    else:
        category = "SERVICE_UNAVAILABLE"
    result = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "ready": ready,
        "category": category,
        "attempts": attempts,
        "free_only": True,
        "no_paid_fallback": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(f"SPIDER_PROVIDER_PREFLIGHT_{'READY' if ready else 'BLOCKED'} category={category}")
    # A blocked provider is *operationally* recorded but must not cause
    # factory-recovery to dispatch another costly cycle every 30 minutes.


if __name__ == "__main__":
    main()
