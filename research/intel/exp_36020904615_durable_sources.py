"""
EXP-INTEL-36020904615 Module A1: durable-source acquisition attempts (MV1/MV2).

Every required durable source receives >=2 genuine attempts with canonical logging:
attempt URL / command, HTTP status or returncode, bytes, sha256 hex, 64-char digest
substring check, configured timeout >=300s, stdout/stderr tails.

Sources
  SRC-HF-WEBARENA      HF raw + Hub API tree for ServiceNow/WebArena-Verified
  SRC-HF-HARD258       HF raw + Hub API tree for webarna-verfied-hard.json
  SRC-HF-WEBGYM        HF raw + Hub API tree for OpenEnv/WebGym (292k/127k)
  SRC-GHCR-BROWSERGYM  GHCR registry v2 token+manifest x2 AND docker pull x2
  SRC-DOCKER-HUB       Hub API tags x2 AND docker pull --digests x2
  SRC-GITHUB-CROSS     raw.githubusercontent x2 (webarena-verified.json byte identity)
                       + x2 (webarna-verfied-hard.json Hard258 census source)

HF_TOKEN presence is logged (true/false). GHCR uses GH_TOKEN (repository bearer) only
for the registry API probe; absence/failure is recorded as evidence, never as a
scientific negative.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments" / "EXP-INTEL-36020904615"
RAW = EXP / "artifacts" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

EXP_ID = "EXP-INTEL-36020904615"
TIMEOUT_S = 300
MANIFEST_SHA_EXPECTED = "d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30"
DOCKER_DIGEST_EXPECTED = "sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb"
GHCR_REF = "ghcr.io/servicenow/browsergym:0.14.3"
HUB_REF = "am1n3e/webarena-verified-shopping"


def hf_token_present() -> bool:
    return bool(os.environ.get("HF_TOKEN"))


def http_attempt(label: str, url: str, headers: dict | None = None, accept: str | None = None) -> dict:
    rec = {
        "attempt_label": label,
        "url": url,
        "timeout_configured_s": TIMEOUT_S,
        "hf_token_present": hf_token_present(),
    }
    hdrs = dict(headers or {})
    if accept:
        hdrs["Accept"] = accept
    req = urllib.request.Request(url, headers=hdrs)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            body = resp.read()
            rec.update(
                status=resp.status,
                bytes=len(body),
                sha256=hashlib.sha256(body).hexdigest(),
                digest_header=resp.headers.get("Docker-Content-Digest"),
                elapsed_s=round(time.time() - t0, 3),
                error=None,
            )
    except urllib.error.HTTPError as e:
        rec.update(status=e.code, bytes=0, sha256=None, digest_header=None,
                   elapsed_s=round(time.time() - t0, 3),
                   error=f"HTTPError {e.code}: {e.reason}")
    except Exception as e:  # noqa: BLE001
        rec.update(status=None, bytes=0, sha256=None, digest_header=None,
                   elapsed_s=round(time.time() - t0, 3),
                   error=f"{type(e).__name__}: {e}")
    return rec


def docker_attempt(cmd: list[str], timeout: int = TIMEOUT_S) -> dict:
    rec = {"cmd": " ".join(cmd), "timeout_configured_s": timeout}
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        rec.update(returncode=p.returncode,
                   stdout_tail=p.stdout[-4000:],
                   stderr_tail=p.stderr[-4000:],
                   elapsed_s=round(time.time() - t0, 3),
                   error=None)
    except subprocess.TimeoutExpired as e:
        rec.update(returncode=None,
                   stdout_tail=(e.stdout or b"")[-4000:].decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")[-4000:],
                   stderr_tail=(e.stderr or b"")[-4000:].decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")[-4000:],
                   elapsed_s=round(time.time() - t0, 3),
                   error=f"TimeoutExpired after {timeout}s")
    except Exception as e:  # noqa: BLE001
        rec.update(returncode=None, stdout_tail="", stderr_tail="",
                   elapsed_s=round(time.time() - t0, 3),
                   error=f"{type(e).__name__}: {e}")
    return rec


def digest_check(digest: str | None) -> dict:
    if not digest:
        return {"digest": None, "digest_64hex": None, "digest_64hex_len": 0, "digest_64hex_valid": False}
    d = digest.split(":", 1)[-1] if ":" in digest else digest
    valid = len(d) == 64 and all(c in "0123456789abcdef" for c in d)
    return {"digest": digest if digest.startswith("sha256:") else f"sha256:{digest}",
            "digest_64hex": d, "digest_64hex_len": len(d), "digest_64hex_valid": valid}


def main() -> None:
    out: dict = {"experiment_id": EXP_ID, "hf_token_present": hf_token_present(),
                 "gh_token_present": bool(os.environ.get("GH_TOKEN")),
                 "timeout_configured_s": TIMEOUT_S}

    # ---------------- HF: WebArena-Verified manifest ----------------
    hf_attempts = [
        http_attempt("webarena-verified.json raw",
                     "https://huggingface.co/datasets/ServiceNow/WebArena-Verified/resolve/main/webarena-verified.json"),
        http_attempt("WebArena Hub API tree",
                     "https://huggingface.co/api/datasets/ServiceNow/WebArena-Verified/tree/main"),
    ]
    (RAW / "hf_manifest_attempts.json").write_text(json.dumps({
        "experiment_id": EXP_ID, "source": "SRC-HF-WEBARENA",
        "hf_token_present": hf_token_present(),
        "expected_sha256": MANIFEST_SHA_EXPECTED,
        "attempts": hf_attempts,
        "n_attempts": len(hf_attempts),
        "n_genuine_attempts": len(hf_attempts),
    }, indent=1))

    # ---------------- HF: Hard258 census file ----------------
    hard_attempts = [
        http_attempt("webarna-verfied-hard.json raw",
                     "https://huggingface.co/datasets/ServiceNow/WebArena-Verified/resolve/main/assets/dataset/webarna-verfied-hard.json"),
        http_attempt("Hard258 Hub API tree",
                     "https://huggingface.co/api/datasets/ServiceNow/WebArena-Verified/tree/main/assets/dataset"),
    ]
    (RAW / "hf_hard258_attempts.json").write_text(json.dumps({
        "experiment_id": EXP_ID, "source": "SRC-HF-HARD258",
        "hf_token_present": hf_token_present(),
        "attempts": hard_attempts,
        "n_attempts": len(hard_attempts),
        "fallback_source": "raw.githubusercontent.com/ServiceNow/WebArena-Verified (documented, NOT HF)",
    }, indent=1))

    # ---------------- HF: WebGym 292k ----------------
    webgym_attempts = [
        http_attempt("WebGym Hub API tree",
                     "https://huggingface.co/api/datasets/OpenEnv/WebGym/tree/main"),
        http_attempt("WebGym README probe",
                     "https://huggingface.co/datasets/OpenEnv/WebGym/resolve/main/README.md"),
    ]
    (RAW / "hf_webgym_manifest_attempts.json").write_text(json.dumps({
        "experiment_id": EXP_ID, "source": "SRC-HF-WEBGYM",
        "hf_token_present": hf_token_present(),
        "attempts": webgym_attempts,
        "n_attempts": len(webgym_attempts),
        "note": "WebGym 292k tasks/127k sites manifest is HF-gated; MV5: >=2 genuine attempts "
                ">=300s configured; if 401 after 2 attempts diverse count is UNAVAILABLE not zero.",
    }, indent=1))

    # ---------------- GHCR BrowserGym 0.14.3 ----------------
    ghcr_attempts = []
    tok_url = ("https://ghcr.io/token?service=ghcr.io&scope=repository:servicenow/browsergym:pull")
    tok_rec = http_attempt("GHCR anonymous token", tok_url)
    ghcr_attempts.append(tok_rec)
    token = None
    if os.environ.get("GH_TOKEN"):
        authed = http_attempt("GHCR token with GH_TOKEN basic auth", tok_url,
                              headers={"Authorization": "Basic " + __import__("base64").b64encode(
                                  f"x-access-token:{os.environ['GH_TOKEN']}".encode()).decode()})
        ghcr_attempts.append(authed)
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    tok_url, headers={"Authorization": "Basic " + __import__("base64").b64encode(
                        f"x-access-token:{os.environ['GH_TOKEN']}".encode()).decode()}),
                    timeout=TIMEOUT_S) as r:
                token = json.loads(r.read()).get("token")
        except Exception:  # noqa: BLE001
            token = None
    for i in (1, 2):
        hdrs = {"Authorization": f"Bearer {token}"} if token else {}
        ghcr_attempts.append(http_attempt(
            f"GHCR manifest GET attempt {i}",
            "https://ghcr.io/v2/servicenow/browsergym/manifests/0.14.3",
            headers=hdrs,
            accept=("application/vnd.oci.image.index.v1+json,"
                    "application/vnd.docker.distribution.manifest.list.v2+json,"
                    "application/vnd.docker.distribution.manifest.v2+json")))
    pull_attempts = []
    for i in (1, 2):
        pull_attempts.append(docker_attempt(["docker", "pull", GHCR_REF], TIMEOUT_S))
    (RAW / "ghcr_browsergym_attempts.json").write_text(json.dumps({
        "experiment_id": EXP_ID, "source": "SRC-GHCR-BROWSERGYM",
        "reference": GHCR_REF,
        "api_attempts": ghcr_attempts,
        "docker_pull_attempts": pull_attempts,
        "n_genuine_attempts": len(ghcr_attempts) + len(pull_attempts),
        "digest": next((a.get("digest_header") for a in ghcr_attempts if a.get("digest_header")), None),
        "note": "2 registry-API attempts + 2 docker pull attempts, each timeout 300s configured.",
    }, indent=1))

    # ---------------- Docker Hub shopping image ----------------
    hub_attempts = []
    for i in (1, 2):
        hub_attempts.append(http_attempt(
            f"Hub API tags attempt {i}",
            f"https://hub.docker.com/v2/repositories/{HUB_REF}/tags"))
    hub_digest = None
    for a in hub_attempts:
        if a["status"] == 200 and a.get("sha256"):
            # re-parse digest from a fresh fetch body (body not retained) -> second GET
            pass
    # capture digest body explicitly
    body_rec = http_attempt("Hub API tags digest capture",
                            f"https://hub.docker.com/v2/repositories/{HUB_REF}/tags")
    try:
        with urllib.request.urlopen(f"https://hub.docker.com/v2/repositories/{HUB_REF}/tags",
                                    timeout=TIMEOUT_S) as r:
            data = json.loads(r.read())
            results = data.get("results") or []
            if results:
                hub_digest = results[0].get("digest") or results[0].get("images", [{}])[0].get("digest")
    except Exception:  # noqa: BLE001
        hub_digest = None
    hub_pulls = []
    for i in (1, 2):
        hub_pulls.append(docker_attempt(
            ["docker", "pull", f"{HUB_REF}@{DOCKER_DIGEST_EXPECTED}"], TIMEOUT_S))
    docker_images = docker_attempt(["docker", "images", "--digests", HUB_REF], 120)
    (RAW / "docker_hub_api_attempts.json").write_text(json.dumps({
        "experiment_id": EXP_ID, "source": "SRC-DOCKER-HUB-API",
        "expected_digest": DOCKER_DIGEST_EXPECTED,
        "hub_api_attempts": hub_attempts,
        "hub_digest_capture": body_rec,
        "hub_latest_digest": hub_digest,
        **digest_check(hub_digest or DOCKER_DIGEST_EXPECTED),
        "digest_expected_match": (hub_digest == DOCKER_DIGEST_EXPECTED) if hub_digest else None,
        "n_genuine_attempts": len(hub_attempts) + len(hub_pulls),
    }, indent=1))
    (RAW / "docker_pull_attempts.json").write_text(json.dumps({
        "experiment_id": EXP_ID, "source": "SRC-DOCKER-PULL",
        "pull_attempts": hub_pulls,
        "docker_images_digests": docker_images,
    }, indent=1))

    # ---------------- GitHub cross-source (byte identity + Hard258 source) ----------------
    gh_wa = [http_attempt(f"GitHub raw webarena-verified.json attempt {i}",
                          "https://raw.githubusercontent.com/ServiceNow/WebArena-Verified/main/assets/dataset/webarena-verified.json")
             for i in (1, 2)]
    gh_hard = [http_attempt(f"GitHub raw webarna-verfied-hard.json attempt {i}",
                            "https://raw.githubusercontent.com/ServiceNow/WebArena-Verified/main/assets/dataset/webarna-verfied-hard.json")
               for i in (1, 2)]
    (RAW / "github_cross_source_attempts.json").write_text(json.dumps({
        "experiment_id": EXP_ID, "source": "SRC-GITHUB-CROSS-SOURCE",
        "expected_sha256": MANIFEST_SHA_EXPECTED,
        "webarena_attempts": gh_wa,
        "hard258_attempts": gh_hard,
        "byte_identity_match": [a.get("sha256") == MANIFEST_SHA_EXPECTED for a in gh_wa],
        "cross_source_note": ("GitHub raw is an ADDITIONAL independent source, not HuggingFace. "
                              "Per MV2, HF cross-source equality stays UNAVAILABLE when HF 401; "
                              "GitHub equality is reported separately and never relabeled as HF."),
        "n_genuine_attempts": len(gh_wa) + len(gh_hard),
    }, indent=1))

    # save fetched hard file for census derivation
    for i, a in enumerate(gh_hard, 1):
        if a["status"] == 200 and a["bytes"]:
            with urllib.request.urlopen(a["url"], timeout=TIMEOUT_S) as r:
                (RAW / "webarena_verfied_hard.json").write_bytes(r.read())
            break

    out["files"] = sorted(p.name for p in RAW.glob("*attempts*.json")) + ["docker_pull_attempts.json"]
    (RAW / "durable_sources_index.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    for p in sorted(RAW.glob("*.json")):
        print("--", p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
