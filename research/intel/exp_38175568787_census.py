#!/usr/bin/env python3
"""EXECUTE endpoint census for EXP-INTEL-38175568787 (intel lane, frozen design).

Implements prereg.md Appendix C.1. For each provider in
spec.endpoint_census.providers: check credential env-var presence, issue an
unauthenticated GET to the provider model-list URL with a short timeout (no API
key, no model invocation), and record credential_present,
reachability_http_status (or exact connection error), classification and the
exact blocker. Writes <outdir>/raw/endpoint_census.json.

Non-outcome-bearing and non-gating for OUTCOME. No interpretation.
"""
import json
import os
import sys
import urllib.error
import urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38175568787")
SPEC = os.path.join(EXP, "spec.json")

# Frozen provider table (spec.endpoint_census.providers).
PROVIDERS = [
    {"provider": "OpenAI", "credential_env": "OPENAI_API_KEY", "reachability_url": "https://api.openai.com/v1/models"},
    {"provider": "Anthropic", "credential_env": "ANTHROPIC_API_KEY", "reachability_url": "https://api.anthropic.com/v1/models"},
    {"provider": "Google Gemini", "credential_env": "GEMINI_API_KEY|GOOGLE_API_KEY", "reachability_url": "https://generativelanguage.googleapis.com/v1beta/models"},
    {"provider": "Mistral", "credential_env": "MISTRAL_API_KEY", "reachability_url": "https://api.mistral.ai/v1/models"},
    {"provider": "Groq", "credential_env": "GROQ_API_KEY", "reachability_url": "https://api.groq.com/openai/v1/models"},
    {"provider": "Together", "credential_env": "TOGETHER_API_KEY", "reachability_url": "https://api.together.xyz/v1/models"},
    {"provider": "OpenRouter", "credential_env": "OPENROUTER_API_KEY", "reachability_url": "https://openrouter.ai/api/v1/models"},
    {"provider": "DeepSeek", "credential_env": "DEEPSEEK_API_KEY", "reachability_url": "https://api.deepseek.com/v1/models"},
    {"provider": "HuggingFace Inference", "credential_env": "HF_TOKEN|HUGGINGFACEHUB_API_TOKEN", "reachability_url": "https://api-inference.huggingface.co/models"},
    {"provider": "Fireworks", "credential_env": "FIREWORKS_API_KEY", "reachability_url": "https://api.fireworks.ai/inference/v1/models"},
    {"provider": "Cohere", "credential_env": "COHERE_API_KEY", "reachability_url": "https://api.cohere.com/v1/models"},
    {"provider": "Pollinations", "credential_env": None, "reachability_url": "https://text.pollinations.ai/models",
     "expected_classification": "CREDENTIAL_FREE_OPERATIONALLY_CAPPED",
     "blocker": "reasoning-only content + ~197 completion-token cap + intermittent HTTP 402 + no model pinning/SLA (carried from EXP-INTEL-37973264582; not re-run as an agent)"},
]


def env_present(credential_env):
    if not credential_env:
        return False, []
    names = credential_env.split("|")
    present = [n for n in names if os.environ.get(n)]
    return bool(present), names


def probe(url, timeout=10):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "spider-intel-census/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, None
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, "%s: %s" % (type(e).__name__, str(e)[:200])


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else EXP
    os.makedirs(os.path.join(outdir, "raw"), exist_ok=True)

    records = []
    for p in PROVIDERS:
        present, names = env_present(p.get("credential_env"))
        status, conn_err = probe(p["reachability_url"])
        rec = {
            "provider": p["provider"],
            "credential_env": p.get("credential_env"),
            "credential_env_names": names,
            "credential_present": present,
            "reachability_url": p["reachability_url"],
            "reachability_http_status": status,
            "connection_error": conn_err,
        }
        if p.get("expected_classification") == "CREDENTIAL_FREE_OPERATIONALLY_CAPPED":
            rec["classification"] = "CREDENTIAL_FREE_OPERATIONALLY_CAPPED"
            rec["blocker"] = p.get("blocker")
        elif present:
            rec["classification"] = "PROVISIONABLE_CREDENTIATED"
            rec["blocker"] = None
        elif conn_err is not None:
            rec["classification"] = "UNREACHABLE"
            rec["blocker"] = "connection error: %s" % conn_err
        elif status in (401, 403):
            rec["classification"] = "CREDENTIAL_REQUIRED"
            rec["blocker"] = "missing credential env var %s (unauthenticated model-list returned HTTP %s)" % (p.get("credential_env"), status)
        elif status == 200:
            # Public model list reachable but inference still requires a credential.
            rec["classification"] = "CREDENTIAL_REQUIRED"
            rec["blocker"] = "public model list reachable (HTTP 200) but inference requires missing credential env var %s" % (p.get("credential_env"))
        else:
            rec["classification"] = "UNREACHABLE"
            rec["blocker"] = "unexpected unauthenticated HTTP status %s" % status
        records.append(rec)
        print(json.dumps({k: rec[k] for k in ("provider", "credential_present", "reachability_http_status", "classification")}))

    counts = {
        "PROVISIONABLE_CREDENTIATED": sum(1 for r in records if r["classification"] == "PROVISIONABLE_CREDENTIATED"),
        "CREDENTIAL_REQUIRED": sum(1 for r in records if r["classification"] == "CREDENTIAL_REQUIRED"),
        "CREDENTIAL_FREE_OPERATIONALLY_CAPPED": sum(1 for r in records if r["classification"] == "CREDENTIAL_FREE_OPERATIONALLY_CAPPED"),
        "UNREACHABLE": sum(1 for r in records if r["classification"] == "UNREACHABLE"),
    }
    doc = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38175568787",
        "method": "env-var presence + unauthenticated GET to model-list endpoint; no API key, no model invocation",
        "providers": records,
        "counts": counts,
        "any_provisionable_credentialed": counts["PROVISIONABLE_CREDENTIATED"] > 0,
    }
    with open(os.path.join(outdir, "raw", "endpoint_census.json"), "w") as f:
        json.dump(doc, f, indent=2, sort_keys=True)
    print(json.dumps({"counts": counts}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
