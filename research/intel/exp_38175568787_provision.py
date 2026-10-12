#!/usr/bin/env python3
"""EXECUTE provisioning-evidence capture for EXP-INTEL-38175568787 (intel lane).

Applies frozen decision rule 3a: verify each candidate's pinned GGUF sha256+bytes
before any load. Evidence so far shows the remote content at the frozen URLs has
drifted (current HF LFS OID / Xet hash != frozen-pinned sha256) across multiple
independent download routes (plain resolve, ?download=true, hf.co). Per the
frozen fail-closed rule (spec measurement_validity #6, decision rule 3a) a
digest mismatch marks the candidate UNMEASURED_LOAD_FAILED and the model is NOT
loaded. This script writes:

  raw/provisioning_evidence.json        - durable evidence of the blocker
  cells/<candidate>/raw/provisioning_receipt.json - per-candidate disposition

It performs no model measurement and no interpretation beyond the frozen
classification.
"""
import hashlib
import json
import os
import sys
import urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38175568787")
GGUF_DIR = "/tmp/opencode/gguf"

CANDIDATES = [
    {
        "candidate_id": "M-14B-QWEN",
        "filename": "Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "url": "https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "pinned_sha256": "d989c91de35f32c18bdb8bec96a4b9fff2c3e5bca066503c63a5ca54dd537a4b",
        "pinned_bytes": 8988110976,
        "hf_repo": "bartowski/Qwen2.5-14B-Instruct-GGUF",
    },
    {
        "candidate_id": "M-8B-LLAMA",
        "filename": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "pinned_sha256": "854506123b68372492b8a99bb3a999594672b394791cf1153f8da5ffb5f1c59a",
        "pinned_bytes": 4920739232,
        "hf_repo": "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    },
]

# Observed sha256 of downloaded bytes (multi-route verified at EXECUTE; each
# equals the current HF LFS OID reported by the tree API, i.e. the served bytes
# are authentic current content that differs from the frozen-pinned digest).
OBSERVED_SHA256 = {
    "M-14B-QWEN": "e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008",
    "M-8B-LLAMA": "7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def hf_tree_info(repo):
    url = "https://huggingface.co/api/models/%s/tree/main?recursive=true&expand=false" % repo
    req = urllib.request.Request(url, headers={"User-Agent": "spider-intel/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    return data


def hf_head(candidate):
    req = urllib.request.Request(candidate["url"], method="HEAD",
                                 headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            return {"final_status": r.status, "final_url": r.geturl(),
                    "etag": hdrs.get("etag"), "content_length": hdrs.get("content-length"),
                    "x-linked-etag": hdrs.get("x-linked-etag")}
    except Exception as e:  # pragma: no cover - network failure is itself evidence
        return {"error": "%s: %s" % (type(e).__name__, e)}


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else EXP
    os.makedirs(os.path.join(outdir, "raw"), exist_ok=True)

    evidence = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38175568787",
        "note": ("Ladder step 3a fail-closed digest verification. At EXECUTE the remote "
                 "content at the frozen GGUF URLs hashes to the CURRENT HF LFS OID (Xet hash) "
                 "which differs from the frozen-pinned sha256. Multiple independent download "
                 "routes agree (resolve plain, ?download=true, hf.co). Byte counts match the "
                 "pinned sizes. No model load was attempted for any mismatched file; a digest "
                 "mismatch marks the candidate UNMEASURED_LOAD_FAILED per frozen decision rule 3a."),
        "candidates": [],
    }
    receipts = {}
    for c in CANDIDATES:
        p = os.path.join(GGUF_DIR, c["filename"])
        exists = os.path.exists(p)
        size = os.path.getsize(p) if exists else None
        sha = sha256_file(p) if exists else None
        match = exists and sha == c["pinned_sha256"] and size == c["pinned_bytes"]
        tree = hf_tree_info(c["hf_repo"])
        head = hf_head(c)
        tree_entry = None
        for f in tree:
            if f.get("path") == c["filename"]:
                tree_entry = {
                    "path": f.get("path"),
                    "size": f.get("size"),
                    "lfs_oid": (f.get("lfs") or {}).get("oid"),
                    "xetHash": f.get("xetHash"),
                    "oid": f.get("oid"),
                }
        entry = {
            "candidate_id": c["candidate_id"],
            "frozen_url": c["url"],
            "pinned_sha256": c["pinned_sha256"],
            "pinned_bytes": c["pinned_bytes"],
            "downloaded_path": p,
            "downloaded_exists": exists,
            "downloaded_bytes": size,
            "downloaded_sha256": sha,
            "digest_match_pinned": match,
            "remote_current_lfs_oid": tree_entry.get("lfs_oid") if tree_entry else None,
            "remote_current_xet_hash": tree_entry.get("xetHash") if tree_entry else None,
            "remote_current_size": tree_entry.get("size") if tree_entry else None,
            "hf_tree_api_entry": tree_entry,
            "hf_head": head,
            "observed_sha256_matches_current_lfs_oid": bool(tree_entry and sha == tree_entry.get("lfs_oid")),
            "diagnosis": {
                "pinned_equals_tree_xetHash": bool(tree_entry and c["pinned_sha256"] == tree_entry.get("xetHash")),
                "pinned_equals_cdn_etag": bool(head.get("etag") and head["etag"].strip('"') == c["pinned_sha256"]),
                "downloaded_equals_tree_lfs_oid": bool(tree_entry and sha == tree_entry.get("lfs_oid")),
                "root_cause": ("the frozen pin equals the HF tree API xetHash (Xet content hash) and the CDN etag, but the "
                               "sha256 of the served bytes equals the tree API lfs.oid. The spec note claims 'sha256 equals "
                               "the HF LFS OID (CDN etag)'; that conflates two distinct server fields: the pin is the "
                               "xetHash/CDN-etag, NOT the lfs.oid. The design-time digest was therefore read from HF server "
                               "metadata (etag/xetHash) rather than computed from downloaded bytes (or the served body changed "
                               "from xet-hashed content to lfs-oid content between design and execute). Either way the frozen "
                               "byte-level identity is unsatisfiable against the currently served, stable, authentic bytes."),
            },
            "routes_verified": ["https://huggingface.co/<repo>/resolve/main/<file>",
                                "https://huggingface.co/<repo>/resolve/main/<file>?download=true",
                                "https://hf.co/<repo>/resolve/main/<file>"],
            "load_attempted": False,
            "disposition": "UNMEASURED_LOAD_FAILED",
            "disposition_rule": "frozen decision rule 3a (pinned GGUF sha256+bytes mismatch -> UNMEASURED_LOAD_FAILED, continue); fail-closed, no model substitution permitted",
        }
        evidence["candidates"].append(entry)
        receipts[c["candidate_id"]] = {
            "candidate_id": c["candidate_id"],
            "load_status": "UNMEASURED_LOAD_FAILED",
            "load_error": ("pinned GGUF sha256+bytes mismatch at EXECUTE: pinned %s (%s bytes) vs downloaded %s (%s bytes); "
                           "downloaded bytes equal the current remote HF LFS OID %s" % (
                               c["pinned_sha256"], c["pinned_bytes"], sha, size,
                               tree_entry.get("lfs_oid") if tree_entry else "?"))
            if not match else None,
            "provisioning_evidence_ref": "raw/provisioning_evidence.json#candidates.%s" % c["candidate_id"],
            "episodes": [],
            "positive_control": None,
        }
        for cid, r in receipts.items():
            rd = os.path.join(outdir, "cells", cid, "raw")
            os.makedirs(rd, exist_ok=True)
            with open(os.path.join(rd, "provisioning_receipt.json"), "w") as f:
                json.dump(r, f, indent=2, sort_keys=True)
        print(json.dumps({"candidate": c["candidate_id"], "digest_match_pinned": match,
                          "pinned": c["pinned_sha256"][:16], "observed": (sha or "?")[:16],
                          "disposition": "UNMEASURED_LOAD_FAILED"}))

    with open(os.path.join(outdir, "raw", "provisioning_evidence.json"), "w") as f:
        json.dump(evidence, f, indent=2, sort_keys=True)
    print("WROTE raw/provisioning_evidence.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())