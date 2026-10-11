#!/usr/bin/env python3
"""EXECUTE materializer for EXP-INTEL-38164607941 (intel lane, frozen design).

Implements prereg.md section 4.2: for every (candidate, prompt-condition) cell,
load the frozen parent harness_config.json and replace ONLY prompts.system with
the verbatim frozen condition string. Verifies the byte-difference (as an
object) is confined to prompts.system. Writes the per-cell overlay to the exact
path the frozen parent runner reads: <per-cell-outdir>/raw/harness_config.json,
plus a provenance mirror at configs/config_<candidate>_<condition>.json.

This script performs no measurement and no interpretation.
"""
import hashlib
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38164607941")
PARENT_CFG = os.path.join(REPO, "research", "experiments", "EXP-INTEL-37982024058", "raw", "harness_config.json")

PARENT_CFG_SHA256 = "7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb"

P_COMP_UNDERSPECIFIED = (
    "You are a web agent. Reply with ONLY a valid JSON action per the schema. "
    "No prose, no reasoning, no markdown."
)
P_TREAT_GOAL_SCHEMA = (
    'You are a web agent. Reply ONLY with one JSON object per turn, no prose. '
    'Actions available: {"action":"click","selector":"<id>"} or '
    '{"action":"answer","text":"<code>"}. '
    "Click the button to reveal the code, then answer it."
)

CONDITIONS = {
    "P-COMP-UNDERSPECIFIED": P_COMP_UNDERSPECIFIED,
    "P-TREAT-GOAL-SCHEMA": P_TREAT_GOAL_SCHEMA,
}
EXPECTED_STR_SHA = {
    "P-COMP-UNDERSPECIFIED": "1294954da7b1d6b9570b07e1e39cb48515b925355d0f33d5fabf72c8e8ce3876",
    "P-TREAT-GOAL-SCHEMA": "36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716",
}
CANDIDATES = ["M-7B-QWEN", "M-3B-QWEN"]


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def cell_dir(candidate, condition):
    return os.path.join(EXP, "cells", candidate, condition)


def main():
    with open(PARENT_CFG, "rb") as f:
        raw = f.read()
    parent_sha = sha256_bytes(raw)
    assert parent_sha == PARENT_CFG_SHA256, "frozen parent config sha mismatch: %s" % parent_sha
    parent = json.loads(raw.decode())

    materialized = {}
    for candidate in CANDIDATES:
        for cond, system_str in CONDITIONS.items():
            assert sha256_bytes(system_str.encode()) == EXPECTED_STR_SHA[cond], "condition string sha mismatch for %s" % cond
            cfg = json.loads(raw.decode())  # fresh deep copy from frozen bytes
            cfg["prompts"]["system"] = system_str
            # verify: the ONLY difference is prompts.system (the comparator overlay
            # is byte-identical to the parent and therefore has no diff at all)
            diffs = [k for k in set(list(cfg.keys()) + list(parent.keys())) if cfg.get(k) != parent.get(k)]
            assert diffs in ([], ["prompts"]), "unexpected top-level diff for %s/%s: %s" % (candidate, cond, diffs)
            pp = dict(parent["prompts"]); cp = dict(cfg["prompts"])
            pk = [k for k in set(list(pp.keys()) + list(cp.keys())) if pp.get(k) != cp.get(k)]
            assert pk in ([], ["system"]), "prompts diff not confined to system for %s/%s: %s" % (candidate, cond, pk)
            if cond == "P-TREAT-GOAL-SCHEMA":
                assert diffs == ["prompts"] and pk == ["system"], "treatment overlay must differ only in prompts.system"
            else:
                assert diffs == [] and pk == [], "comparator overlay must be byte-identical to the parent"
            # no answer leakage
            assert "#reveal-btn" not in system_str and "TARGET-42" not in system_str, "leakage in %s" % cond

            cd = cell_dir(candidate, cond)
            os.makedirs(os.path.join(cd, "raw"), exist_ok=True)
            overlay_path = os.path.join(cd, "raw", "harness_config.json")
            overlay_bytes = json.dumps(cfg, indent=2, sort_keys=True).encode()
            with open(overlay_path, "wb") as f:
                f.write(overlay_bytes)
            mirr_dir = os.path.join(EXP, "configs")
            os.makedirs(mirr_dir, exist_ok=True)
            mirror_path = os.path.join(mirr_dir, "config_%s_%s.json" % (candidate, cond))
            with open(mirror_path, "wb") as f:
                f.write(overlay_bytes)
            materialized["%s|%s" % (candidate, cond)] = {
                "candidate": candidate,
                "condition": cond,
                "cell_dir": os.path.relpath(cd, REPO),
                "overlay_path": os.path.relpath(overlay_path, REPO),
                "mirror_path": os.path.relpath(mirror_path, REPO),
                "overlay_sha256": sha256_bytes(overlay_bytes),
                "overlay_is_parent_byte_identical": (overlay_bytes == raw),
                "system_string_sha256": sha256_bytes(system_str.encode()),
                "system_string": system_str,
                "diff_confined_to_prompts_system": True,
                "leakage_reveal_selector": ("#reveal-btn" in system_str),
                "leakage_target_value": ("TARGET-42" in system_str),
            }
            print(json.dumps({"materialized": "%s|%s" % (candidate, cond), "overlay_sha256": materialized["%s|%s" % (candidate, cond)]["overlay_sha256"]}))

    manifest = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38164607941",
        "parent_config_path": os.path.relpath(PARENT_CFG, REPO),
        "parent_config_sha256": parent_sha,
        "cells": materialized,
    }
    out = os.path.join(EXP, "raw", "materialized_configs.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print("WROTE %s" % os.path.relpath(out, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
