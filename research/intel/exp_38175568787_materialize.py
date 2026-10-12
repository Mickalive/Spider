#!/usr/bin/env python3
"""EXECUTE materializer for EXP-INTEL-38175568787 (intel lane, frozen design).

Implements prereg.md section 4.2: for each candidate, load the frozen base
harness_config.json (byte-frozen parent fixture, sha256 pinned) and replace ONLY:

  - prompts.system          <- frozen P-TREAT-GOAL-SCHEMA string
  - sampling.chat_format    <- the candidate's family chat_format
  - candidate_models_frozen <- the single frozen candidate entry

Every other key is inherited byte-for-byte. The overlay is a pure deterministic
transformation of the bound base fixture. The materialized config is written to
the exact path the frozen runner reads (<per-candidate-outdir>/raw/harness_config.json)
plus a provenance mirror at configs/config_<candidate_id>.json.

This script performs no measurement and no interpretation.
"""
import hashlib
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38175568787")
BASE_CFG = os.path.join(REPO, "research", "experiments", "EXP-INTEL-37982024058", "raw", "harness_config.json")

BASE_CFG_SHA256 = "7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb"
SYSTEM_SHA256 = "36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716"

P_TREAT_GOAL_SCHEMA = (
    'You are a web agent. Reply ONLY with one JSON object per turn, no prose. '
    'Actions available: {"action":"click","selector":"<id>"} or '
    '{"action":"answer","text":"<code>"}. '
    "Click the button to reveal the code, then answer it."
)

# Frozen candidate table (spec.json#candidates). frozen_url comes from files[0].url.
CANDIDATES = [
    {
        "candidate_id": "M-14B-QWEN",
        "role": "primary",
        "model": "Qwen2.5-14B-Instruct",
        "quant": "Q4_K_M",
        "chat_format": "qwen",
        "frozen_url": "https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "bytes": 8988110976,
        "sha256": "d989c91de35f32c18bdb8bec96a4b9fff2c3e5bca066503c63a5ca54dd537a4b",
    },
    {
        "candidate_id": "M-8B-LLAMA",
        "role": "secondary",
        "model": "Meta-Llama-3.1-8B-Instruct",
        "quant": "Q4_K_M",
        "chat_format": "llama-3",
        "frozen_url": "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "bytes": 4920739232,
        "sha256": "854506123b68372492b8a99bb3a999594672b394791cf1153f8da5ffb5f1c59a",
    },
]


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def deep_diff(a, b, prefix=""):
    """Return a sorted list of dotted paths whose scalar/object values differ."""
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a.keys()) | set(b.keys())):
            if k not in a or k not in b:
                diffs.append(prefix + k)
            else:
                diffs.extend(deep_diff(a[k], b[k], prefix + k + "."))
    else:
        if a != b:
            diffs.append(prefix.rstrip("."))
    return diffs


def cand_dir(cid):
    return os.path.join(EXP, "cells", cid)


def main():
    with open(BASE_CFG, "rb") as f:
        raw = f.read()
    base_sha = sha256_bytes(raw)
    assert base_sha == BASE_CFG_SHA256, "frozen base config sha mismatch: %s" % base_sha
    base = json.loads(raw.decode())

    assert sha256_bytes(P_TREAT_GOAL_SCHEMA.encode()) == SYSTEM_SHA256, "treatment system prompt sha mismatch"
    assert "#reveal-btn" not in P_TREAT_GOAL_SCHEMA and "TARGET-42" not in P_TREAT_GOAL_SCHEMA, "prompt leakage"

    manifest = {"cells": {}}
    for c in CANDIDATES:
        cfg = json.loads(raw.decode())  # fresh deep copy from frozen bytes
        cfg["prompts"]["system"] = P_TREAT_GOAL_SCHEMA
        cfg["sampling"]["chat_format"] = c["chat_format"]
        cfg["candidate_models_frozen"] = [{
            "candidate_id": c["candidate_id"],
            "role": c["role"],
            "model": c["model"],
            "quant": c["quant"],
            "frozen_url": c["frozen_url"],
            "bytes": c["bytes"],
            "sha256": c["sha256"],
        }]

        diffs = deep_diff(base, cfg)
        allowed = {
            "prompts.system",
            "sampling.chat_format",
            "candidate_models_frozen",
        }
        # The diff must be confined to the allowed keys and must actually change
        # prompts.system and candidate_models_frozen. sampling.chat_format only
        # appears when its value differs from the base (the base is already "qwen",
        # which is exactly the M-14B-QWEN overlay value, so it is a no-op there).
        if not (set(diffs) <= allowed and "prompts.system" in diffs and "candidate_models_frozen" in diffs):
            raise AssertionError("unexpected diff set for %s: %s" % (c["candidate_id"], diffs))

        cd = cand_dir(c["candidate_id"])
        os.makedirs(os.path.join(cd, "raw"), exist_ok=True)
        overlay_path = os.path.join(cd, "raw", "harness_config.json")
        overlay_bytes = json.dumps(cfg, indent=2, sort_keys=True).encode()
        with open(overlay_path, "wb") as f:
            f.write(overlay_bytes)

        mirr_dir = os.path.join(EXP, "configs")
        os.makedirs(mirr_dir, exist_ok=True)
        mirror_path = os.path.join(mirr_dir, "config_%s.json" % c["candidate_id"])
        with open(mirror_path, "wb") as f:
            f.write(overlay_bytes)

        manifest["cells"][c["candidate_id"]] = {
            "candidate_id": c["candidate_id"],
            "cell_dir": os.path.relpath(cd, REPO),
            "overlay_path": os.path.relpath(overlay_path, REPO),
            "mirror_path": os.path.relpath(mirror_path, REPO),
            "overlay_sha256": sha256_bytes(overlay_bytes),
            "diff_paths": diffs,
            "diff_confined_to_allowed_keys": True,
            "system_string_sha256": sha256_bytes(P_TREAT_GOAL_SCHEMA.encode()),
            "chat_format": c["chat_format"],
            "candidate_entry_sha256": sha256_bytes(json.dumps(cfg["candidate_models_frozen"], sort_keys=True).encode()),
            "leakage_reveal_selector": ("#reveal-btn" in P_TREAT_GOAL_SCHEMA),
            "leakage_target_value": ("TARGET-42" in P_TREAT_GOAL_SCHEMA),
        }
        print(json.dumps({"materialized": c["candidate_id"], "overlay_sha256":
                          manifest["cells"][c["candidate_id"]]["overlay_sha256"], "diff_paths": diffs}))

    out = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38175568787",
        "base_config_path": os.path.relpath(BASE_CFG, REPO),
        "base_config_sha256": base_sha,
        "system_string": P_TREAT_GOAL_SCHEMA,
        "system_string_sha256": SYSTEM_SHA256,
        "cells": manifest["cells"],
    }
    op = os.path.join(EXP, "raw", "materialized_configs.json")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    with open(op, "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print("WROTE %s" % os.path.relpath(op, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
