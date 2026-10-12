#!/usr/bin/env python3
"""EXECUTE provisioning driver for EXP-INTEL-38194362040 (intel lane, frozen design).

Implements prereg.md Appendix A.5 / section 4.5 (frozen ladder step 3a):
for each predeclared candidate, stream the revision-pinned URL to a local temp
path with no size cap, compute byte count + sha256 of the downloaded body
(NOT any server metadata field), parse the GGUF header fingerprint, and require

    IDENTITY-PASS  iff  bytes == pinned bytes
                   AND  sha256 == served_body_sha256 (PIN)
                   AND  fingerprint == pinned fingerprint

One re-download is permitted on mismatch to distinguish transient transport
corruption from stable served-body drift. On persistent mismatch the candidate is
recorded UNMEASURED_LOAD_FAILED with observed bytes/sha256/fingerprint as a
durable diagnostic; a differing body is NEVER substituted for the frozen content.

Writes raw/provisioning_evidence.json and per-candidate
cells/<candidate>/raw/provisioning_receipt.json. Prints each IDENTITY-PASS GGUF
path. Performs no model measurement and no interpretation.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38194362040")
GGUF_DIR = "/tmp/opencode/gguf"

CANDIDATES = [
    {
        "candidate_id": "M-14B-QWEN",
        "filename": "Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "frozen_url": "https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/05244aa5d871c661c80082a15d3bce44714d068d/Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "main_ref_url": "https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "revision_sha": "05244aa5d871c661c80082a15d3bce44714d068d",
        "pinned_sha256": "e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008",
        "pinned_bytes": 8988110976,
        "hf_repo": "bartowski/Qwen2.5-14B-Instruct-GGUF",
        "gguf_fingerprint": {
            "gguf_version": 3, "tensor_count": 579, "kv_count": 38,
            "general.architecture": "qwen2", "general.name": "Qwen2.5 14B Instruct",
            "general.file_type": 15, "block_count": 48, "embedding_length": 5120,
            "context_length": 32768, "has_tokenizer_chat_template": True,
        },
    },
    {
        "candidate_id": "M-8B-LLAMA",
        "filename": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "frozen_url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/bf5b95e96dac0462e2a09145ec66cae9a3f12067/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "main_ref_url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "revision_sha": "bf5b95e96dac0462e2a09145ec66cae9a3f12067",
        "pinned_sha256": "7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c",
        "pinned_bytes": 4920739232,
        "hf_repo": "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
        "gguf_fingerprint": {
            "gguf_version": 3, "tensor_count": 292, "kv_count": 33,
            "general.architecture": "llama", "general.name": "Meta Llama 3.1 8B Instruct",
            "general.file_type": 15, "block_count": 32, "embedding_length": 4096,
            "context_length": 131072, "has_tokenizer_chat_template": True,
        },
    },
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


# --- minimal GGUF metadata reader -------------------------------------------
SCALAR = {0: ("<B", 1), 1: ("<b", 1), 2: ("<H", 2), 3: ("<h", 2),
          4: ("<I", 4), 5: ("<i", 4), 6: ("<f", 4), 7: ("<B", 1),
          10: ("<Q", 8), 11: ("<q", 8), 12: ("<d", 8)}


def _read_exact(f, n):
    b = f.read(n)
    if len(b) != n:
        raise EOFError("short read: wanted %d got %d" % (n, len(b)))
    return b


def _read_string(f):
    n = struct.unpack("<Q", _read_exact(f, 8))[0]
    return _read_exact(f, n).decode("utf-8", "replace")


def _skip_array_payload(f, etype, count):
    """Consume `count` array elements of `etype`, leaving the file positioned
    immediately after the array payload (arrays are not materialized)."""
    if etype == 9:  # nested array
        for _ in range(count):
            n_etype = struct.unpack("<I", _read_exact(f, 4))[0]
            n_count = struct.unpack("<Q", _read_exact(f, 8))[0]
            _skip_array_payload(f, n_etype, n_count)
        return
    if etype == 8:  # array of strings
        for _ in range(count):
            n = struct.unpack("<Q", _read_exact(f, 8))[0]
            _read_exact(f, n)
        return
    if etype not in SCALAR:
        raise ValueError("unknown gguf array element type %d" % etype)
    _, size = SCALAR[etype]
    _read_exact(f, size * count)


def _read_value(f, vtype):
    if vtype == 8:
        return _read_string(f)
    if vtype == 9:
        etype = struct.unpack("<I", _read_exact(f, 4))[0]
        count = struct.unpack("<Q", _read_exact(f, 8))[0]
        _skip_array_payload(f, etype, count)
        return None
    if vtype not in SCALAR:
        raise ValueError("unknown gguf metadata value type %d" % vtype)
    fmt, size = SCALAR[vtype]
    return struct.unpack(fmt, _read_exact(f, size))[0]


def parse_gguf_fingerprint(path, max_kv=200000):
    with open(path, "rb") as f:
        magic = _read_exact(f, 4)
        if magic != b"GGUF":
            raise ValueError("not a GGUF file (magic=%r)" % magic)
        version = struct.unpack("<I", _read_exact(f, 4))[0]
        tensor_count = struct.unpack("<Q", _read_exact(f, 8))[0]
        kv_count = struct.unpack("<Q", _read_exact(f, 8))[0]
        meta = {}
        for _ in range(min(kv_count, max_kv)):
            key = _read_string(f)
            vtype = struct.unpack("<I", _read_exact(f, 4))[0]
            val = _read_value(f, vtype)
            meta[key] = val
    arch = meta.get("general.architecture")
    fp = {
        "gguf_version": version,
        "tensor_count": tensor_count,
        "kv_count": kv_count,
        "general.architecture": arch,
        "general.name": meta.get("general.name"),
        "general.file_type": meta.get("general.file_type"),
        "block_count": meta.get("%s.block_count" % arch) if arch else None,
        "embedding_length": meta.get("%s.embedding_length" % arch) if arch else None,
        "context_length": meta.get("%s.context_length" % arch) if arch else None,
        "has_tokenizer_chat_template": bool(meta.get("tokenizer.chat_template")),
    }
    return fp


# --- download ----------------------------------------------------------------
def download(url, dest):
    tmp = dest + ".part"
    if os.path.exists(tmp):
        os.remove(tmp)
    cmd = ["curl", "-sSL", "--fail", "--retry", "3", "--retry-delay", "2",
           "-o", tmp, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("curl failed rc=%d stderr=%s" % (r.returncode, r.stderr[-400:]))
    if os.path.exists(dest):
        os.remove(dest)
    os.rename(tmp, dest)


def hf_tree_lfs_oid(repo, filename):
    url = "https://huggingface.co/api/models/%s/tree/main?recursive=true&expand=false" % repo
    req = urllib.request.Request(url, headers={"User-Agent": "spider-intel/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    for e in data:
        if e.get("path") == filename:
            return {"lfs_oid": (e.get("lfs") or {}).get("oid"), "xetHash": e.get("xetHash"),
                    "size": e.get("size")}
    return None


def attempt(c, path):
    size = os.path.getsize(path)
    sha = sha256_file(path)
    fp = parse_gguf_fingerprint(path)
    identity = (size == c["pinned_bytes"] and sha == c["pinned_sha256"]
                and fp == c["gguf_fingerprint"])
    return {"bytes": size, "sha256": sha, "fingerprint": fp, "identity_pass": identity}


def main():
    os.makedirs(GGUF_DIR, exist_ok=True)
    os.makedirs(os.path.join(EXP, "raw"), exist_ok=True)
    evidence = {"schema_version": 1, "experiment_id": "EXP-INTEL-38194362040",
                "method": "full-download served body; compute byte count + sha256 + GGUF header fingerprint; IDENTITY-PASS iff all three equal the frozen pins",
                "pin_policy": "sha256 of fully downloaded served body (NOT HF etag/xetHash metadata)",
                "candidates": []}
    for c in CANDIDATES:
        path = os.path.join(GGUF_DIR, c["filename"])
        attempts = []
        # Reuse an already-present correct body; otherwise (re)download.
        if os.path.exists(path):
            try:
                attempts.append(attempt(c, path))
            except Exception as e:
                attempts.append({"error": "%s: %s" % (type(e).__name__, e), "identity_pass": False})
        if not attempts or not attempts[-1].get("identity_pass"):
            for _ in range(2):  # initial download + at most one re-download
                try:
                    download(c["frozen_url"], path)
                    attempts.append(attempt(c, path))
                except Exception as e:
                    attempts.append({"error": "%s: %s" % (type(e).__name__, e), "identity_pass": False})
                if attempts[-1].get("identity_pass"):
                    break
        final = attempts[-1]
        ident = bool(final.get("identity_pass"))
        entry = {
            "candidate_id": c["candidate_id"],
            "frozen_url": c["frozen_url"],
            "revision_sha": c["revision_sha"],
            "main_ref_url": c["main_ref_url"],
            "pinned_sha256": c["pinned_sha256"],
            "pinned_bytes": c["pinned_bytes"],
            "pinned_fingerprint": c["gguf_fingerprint"],
            "local_path": path if ident else None,
            "attempts": attempts,
            "observed_bytes": final.get("bytes"),
            "observed_sha256": final.get("sha256"),
            "observed_fingerprint": final.get("fingerprint"),
            "identity_pass": ident,
            "n_download_attempts": len(attempts),
            "load_attempted": False,
            "disposition": "IDENTITY_PASS" if ident else "UNMEASURED_LOAD_FAILED",
            "disposition_rule": "frozen rule 3a: IDENTITY-PASS iff bytes+sha256+fingerprint all equal frozen pins; persistent mismatch -> UNMEASURED_LOAD_FAILED (no substitution)",
        }
        if not ident:
            try:
                entry["remote_tree_api"] = hf_tree_lfs_oid(c["hf_repo"], c["filename"])
            except Exception as e:
                entry["remote_tree_api"] = {"error": "%s: %s" % (type(e).__name__, e)}
        evidence["candidates"].append(entry)

        rd = os.path.join(EXP, "cells", c["candidate_id"], "raw")
        os.makedirs(rd, exist_ok=True)
        receipt = {
            "candidate_id": c["candidate_id"],
            "identity_pass": ident,
            "observed_bytes": final.get("bytes"),
            "observed_sha256": final.get("sha256"),
            "observed_fingerprint": final.get("fingerprint"),
            "attempts": attempts,
            "local_path": path if ident else None,
            "load_status": "PROVISIONED" if ident else "UNMEASURED_LOAD_FAILED",
            "load_error": None if ident else "served-body content identity did not match the frozen pins (see attempts)",
            "provisioning_evidence_ref": "raw/provisioning_evidence.json#candidates.%s" % c["candidate_id"],
            "episodes": [],
            "positive_control": None,
        }
        with open(os.path.join(rd, "provisioning_receipt.json"), "w") as f:
            json.dump(receipt, f, indent=2, sort_keys=True)
        print(json.dumps({"candidate": c["candidate_id"], "identity_pass": ident,
                          "observed_sha256": (final.get("sha256") or "?")[:16],
                          "local_path": path if ident else None}))

    with open(os.path.join(EXP, "raw", "provisioning_evidence.json"), "w") as f:
        json.dump(evidence, f, indent=2, sort_keys=True)
    n_pass = sum(1 for e in evidence["candidates"] if e["identity_pass"])
    print(json.dumps({"identity_pass_candidates": n_pass, "total": len(evidence["candidates"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
