#!/usr/bin/env python3
"""Verify ACTUAL no-charge OpenCode tool use, as in the working LexMachina repo.

The previous plain-text-only probe labelled genuinely working free agents
NO_ATTESTED_OUTPUT, blocked all six scientific lanes and discarded why.
We run a disposable *real* bash-tool marker test, without loading Spider,
accepting an arbitrary printed string, or giving an LLM repository access.
No paid models are ever tried.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROBE_TOKEN = "SPIDER_FREE_TOOL_OK"
AUTH = re.compile(
    r"invalid credential|invalid api.?key|missing api.?key|authentication failed|"
    r"unauthori[sz]ed|invalid token|status[^0-9]*401|http[^0-9]*401",
    re.I,
)
DENIED = re.compile(
    r"the user rejected permission|the user has specified a rule which prevents|"
    r"permission denied|requires permission approval", re.I,
)
OUTAGE = re.compile(
    r"model is unavailable|model.*(not found|deprecated)|unexpected server error|"
    r"upstream.*(overload|unavailable|error)|503|429|rate.?limit|fetch failed|"
    r"network error|timed out|connection reset|unknownerror", re.I,
)
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
MODEL_ID = re.compile(r"opencode/[A-Za-z0-9._-]+\Z")


def classify(output: str, returncode: int, *, marker_ok: bool = False,
             timeout: bool = False) -> str:
    """Never confuse model text (or a role banner) with performed work."""
    output = ANSI.sub("", output)
    if AUTH.search(output):
        return "AUTH_INVALID"
    if DENIED.search(output):
        return "PERMISSION_DENIED"
    if timeout:
        return "TIMEOUT"
    if returncode == 0 and marker_ok:
        return "READY"
    if OUTAGE.search(output):
        return "SERVICE_UNAVAILABLE"
    return "NO_TOOL_ATTESTATION"


def clean_environment() -> dict[str, str]:
    """Keep OpenCode provider authentication, never the GitHub app token."""
    env = os.environ.copy()
    for name in ("GH_TOKEN", "GITHUB_TOKEN", "ACTIONS_RUNTIME_TOKEN",
                 "ACTIONS_ID_TOKEN_REQUEST_TOKEN", "ACTIONS_RUNTIME_URL",
                 "GIT_ASKPASS", "BROWSERBASE_API_KEY"):
        env.pop(name, None)
    # Unlike Spider's research runner, the working Lex model-health test
    # does not inject a repo-specific permission overlay. The disposable
    # probe agent owns its permissions; the repo policy may misconfigure it.
    env.pop("OPENCODE_CONFIG_CONTENT", None)
    return env


def query_catalog(binary: str, *, deadline: int = 25) -> tuple[set[str] | None, str]:
    """Use the real CLI catalog, not a stale GitHub pricing snapshot."""
    try:
        proc = subprocess.run(
            [binary, "models", "opencode"],
            text=True, errors="replace", capture_output=True,
            timeout=deadline, env=clean_environment(), check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None, "UNAVAILABLE"
    if proc.returncode != 0:
        return None, "UNAVAILABLE"
    models = {line.strip() for line in proc.stdout.splitlines()
              if MODEL_ID.fullmatch(line.strip())}
    return (models, "OK") if models else (None, "EMPTY")


def run_probe(binary: str, model: str, deadline: int) -> str:
    """The proof is a real tool-created marker, NOT assistant output text."""
    if not MODEL_ID.fullmatch(model):
        return "UNAPPROVED_MODEL"
    source = Path(__file__).resolve().parents[1] / ".opencode/agents/spider_provider_probe.md"
    with tempfile.TemporaryDirectory(prefix="spider-provider-") as root:
        scratch = Path(root)
        agent = scratch / ".opencode/agents/spider_provider_probe.md"
        agent.parent.mkdir(parents=True, exist_ok=True)
        agent.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        marker = scratch / "marker.txt"
        command = f"printf {PROBE_TOKEN} > marker.txt"
        prompt = ("Use the bash tool exactly once to run: " + command
                  + ". Do not merely print or echo the token. Stop when done.")
        try:
            proc = subprocess.Popen(
                [binary, "run", "--dir", str(scratch), "--model", model,
                 "--agent", "spider_provider_probe", prompt],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, errors="replace", start_new_session=True,
                cwd=scratch, env=clean_environment(),
            )
        except OSError:
            return "BINARY_UNAVAILABLE"
        try:
            stdout, stderr = proc.communicate(timeout=deadline)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.communicate()
            return "TIMEOUT"
        passed = marker.is_file() and marker.read_bytes() == PROBE_TOKEN.encode()
        combined = (stdout or "") + "\n" + (stderr or "")
        category = classify(combined, proc.returncode, marker_ok=passed)
        if category == "NO_TOOL_ATTESTATION":
            # This is the precise class Spider previously swallowed for almost
            # every FREE model. Probe runs in an isolated empty directory with
            # a fixed prompt. Print only a short sanitized fragment, never
            # provider credentials, complete model output or user files.
            safe = ANSI.sub("", combined)
            safe = re.sub(r"(?:gh[pousr]_[A-Za-z0-9]{12,}|sk-[A-Za-z0-9_-]{12,}|"
                          r"Bearer\\s+\\S+)", "[REDACTED]", safe, flags=re.I)
            safe = " ".join(safe.split())[:450]
            print(f"SPIDER_PROBE_FAILURE_DETAIL model={model} rc={proc.returncode} "
                  f"diagnostic={safe!r}", flush=True)
        return category


def allowed_candidates(config: dict, limit: int) -> list[str]:
    if config.get("free_only") is not True:
        raise ValueError("paid model configuration forbidden")
    allowed = config.get("free_only_allowed_models") or []
    if not allowed or len(set(allowed)) != len(allowed):
        raise ValueError("missing or duplicate zero-price allowlist")
    if any(not MODEL_ID.fullmatch(m) for m in allowed):
        raise ValueError("invalid provider-model syntax")
    return allowed[:limit]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config/models.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bin", default=str(Path.home() / ".opencode/bin/opencode"))
    parser.add_argument("--max-models", type=int, default=12)
    parser.add_argument("--per-model-seconds", type=int, default=90)
    args = parser.parse_args()
    if not (1 <= args.max_models <= 12 and 10 <= args.per_model_seconds <= 120):
        parser.error("only reviewed free models, 10–120 seconds per probe")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    choices = allowed_candidates(config, args.max_models)
    catalog, catalog_status = query_catalog(args.bin)
    print("SPIDER_PROVIDER_CATALOG status=" + catalog_status
          + " curated_present=" + str(len(set(choices) & catalog) if catalog is not None else "UNKNOWN"),
          flush=True)
    attempts = []
    for model in choices:
        if catalog is not None and model not in catalog:
            status = "SKIPPED_ABSENT"
        else:
            status = run_probe(args.bin, model, args.per_model_seconds)
        attempts.append({"model": model, "status": status})
        print(f"SPIDER_PROVIDER_CHECK model={model} category={status}", flush=True)
        if status == "READY" or status == "BINARY_UNAVAILABLE":
            break
    selected = next((item["model"] for item in attempts if item["status"] == "READY"), None)
    statuses = {a["status"] for a in attempts}
    category = ("READY" if selected else
                "BINARY_UNAVAILABLE" if "BINARY_UNAVAILABLE" in statuses else
                "AUTH_INVALID" if "AUTH_INVALID" in statuses else
                "PERMISSION_DENIED" if "PERMISSION_DENIED" in statuses else
                "TIMEOUT" if "TIMEOUT" in statuses else
                "MODEL_CATALOG_EMPTY" if catalog is not None and not
                (set(choices) & catalog) else
                "SERVICE_UNAVAILABLE")
    report = {
        "schema_version": 2,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "ready": selected is not None,
        "category": category,
        "selected_model": selected,
        "catalog_status": catalog_status,
        "catalog_present_count": len(set(choices) & catalog) if catalog is not None else None,
        "attestation": "real_tool_wrote_marker_in_isolated_scratch",
        "attempts": attempts,
        "free_only": True,
        "no_paid_fallback": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    print(f"SPIDER_PROVIDER_PREFLIGHT_{'READY' if selected else 'BLOCKED'} category={category}",
          flush=True)


if __name__ == "__main__":
    main()
