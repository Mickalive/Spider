#!/usr/bin/env python3
"""EXP-INTEL-36306525220 :: Stage 2 -- controls (frozen identities) + full text.

Runs the four controls exactly as frozen in prereg.md Section 6 and re-attaches
the frozen identity rule to each control target.  Emits raw/controls_result.json.

Nothing in this file interprets a scientific outcome.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_identity import (  # noqa: E402
    ART_DIR, HTML_DIR, RAW, classify, http_get, jlog, now, parse_abs_page, sha256_bytes,
)

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(RAW, "pdf")
TXT_DIR = os.path.join(RAW, "fulltext")

# Frozen control definitions, copied from prereg.md Section 6 / spec.json.
CONTROLS = {
    "PC-COST-ACCOUNTING": {
        "role": "positive_control",
        "gates": "prereg.md Section 7 gate 1 -> MEASUREMENT_INVALID for entire experiment",
        "system": "ActivityFrames",
        "arxiv_id": "2608.05784v1",
        "expected_title": "Activity Frames",
        "expected_authors": ["TBD"],
        "domain_keywords": ["activity", "frames", "agent", "memory", "replay", "compilation"],
    },
    "PC-PERFORMANCE-ENVELOPE": {
        "role": "positive_control",
        "gates": "prereg.md Section 7 gate 4 -> MEASUREMENT_INVALID for Part 2 only",
        "system": "WebVoyager",
        "arxiv_id": "2401.13919v4",
        "expected_title": "WebVoyager",
        "expected_authors": ["He", "Zhang", "Yao", "Chen"],
        "domain_keywords": ["web", "voyager", "agent", "multimodal", "browser"],
    },
    "NC-REAL-BUT-WRONG": {
        "role": "null_control",
        "gates": "prereg.md Section 7 gate 2 -> MEASUREMENT_INVALID for entire experiment",
        "system": "WebArena",
        "arxiv_id": "1802.05012v2",
        "expected_title": "WebArena",
        "expected_authors": ["Zhou", "Liu", "Gu", "Chen"],
        "domain_keywords": ["web", "arena", "agent", "benchmark", "environment"],
    },
    "NC-FABRICATED-CLAIM": {
        "role": "null_control_sanity_only",
        "gates": "prereg.md Section 6.4 -> recorded, does NOT trigger MEASUREMENT_INVALID",
        "system": "FabricatedTarget",
        "arxiv_id": "2609.99999",
        "expected_title": "FabricatedTarget",
        "expected_authors": ["Nonexistent"],
        "domain_keywords": ["web", "agent"],
    },
}


def fetch_fulltext(cid: str) -> dict:
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(TXT_DIR, exist_ok=True)
    pdf_path = os.path.join(PDF_DIR, cid + ".pdf")
    txt_path = os.path.join(TXT_DIR, cid + ".txt")
    if os.path.exists(pdf_path) and os.path.exists(txt_path):
        return {
            "arxiv_id": cid, "status": "cached",
            "pdf_sha256": sha256_bytes(open(pdf_path, "rb").read()),
            "text_sha256": sha256_bytes(open(txt_path, "rb").read()),
            "text_chars": len(open(txt_path, encoding="utf-8", errors="replace").read()),
        }
    st, body, err = http_get(f"https://arxiv.org/pdf/{cid}", dest=pdf_path)
    if st != 200 or not body:
        jlog({"stage": "fulltext", "arxiv_id": cid, "http_status": st, "error": err})
        return {"arxiv_id": cid, "status": "unavailable", "http_status": st, "error": err or None}
    try:
        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        txt = "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception as e:  # noqa: BLE001
        jlog({"stage": "fulltext", "arxiv_id": cid, "error": f"{type(e).__name__}: {e}"})
        return {"arxiv_id": cid, "status": "pdf_parse_failed", "error": f"{type(e).__name__}: {e}"}
    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    out = {
        "arxiv_id": cid, "status": "ok",
        "pdf_sha256": sha256_bytes(body),
        "text_sha256": sha256_bytes(txt.encode("utf-8")),
        "text_chars": len(txt),
    }
    jlog({"stage": "fulltext", **out})
    return out


def resolve_control(key: str) -> dict:
    c = CONTROLS[key]
    cid = c["arxiv_id"]
    hp = os.path.join(HTML_DIR, "ctrl_" + cid + ".html")
    st, body, err = http_get(f"https://arxiv.org/abs/{cid}", dest=hp)
    rec = None
    if st == 200 and body:
        rec = parse_abs_page(body.decode("utf-8", "replace"))
        rec["sha256_abs_page"] = sha256_bytes(body)
        with open(os.path.join(ART_DIR, "ctrl_" + cid + ".json"), "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
    target = {
        "system": c["system"], "arxiv_id": cid, "expected_title": c["expected_title"],
        "expected_authors": c["expected_authors"], "domain_keywords": c["domain_keywords"],
    }
    verdict = classify(target, rec, st, err)
    ft = fetch_fulltext(cid) if st == 200 else {"arxiv_id": cid, "status": "not_attempted"}

    # ---- frozen pass/fail determination, per prereg 6.x ----
    observed = {
        "resolution_status": verdict["resolution_status"],
        "failed_conditions": verdict["failed_conditions"],
        "returned_title": verdict["returned_title"],
        "returned_authors": verdict["returned_authors"],
        "returned_arxiv_id": verdict["returned_arxiv_id"],
        "artifact_is_real": bool(rec and rec["title"]),
        "fulltext": ft,
    }
    if key == "NC-REAL-BUT-WRONG":
        # Pass requires: artifact real AND resolver flags identity mismatch AND emits
        # an UNMEASURED-class status (AMBIGUOUS or NOT_LOCATED) rather than NOT_FOUND.
        flagged = verdict["resolution_status"] in ("AMBIGUOUS", "NOT_LOCATED")
        ok = observed["artifact_is_real"] and flagged
        observed["pass_criterion"] = (
            "artifact is REAL, resolver flags identity mismatch, resolver emits "
            "AMBIGUOUS/NOT_LOCATED (-> UNMEASURED row) and does NOT emit NOT_FOUND"
        )
        observed["emitted_row_resolution_status"] = (
            "UNMEASURED" if flagged else "CORRECTLY_RESOLVED"
        )
        observed["pass"] = ok
    elif key == "NC-FABRICATED-CLAIM":
        ok = verdict["resolution_status"] == "NOT_LOCATED"
        observed["pass_criterion"] = "resolver fails to locate artifact and emits NOT_LOCATED"
        observed["emitted_row_resolution_status"] = "UNMEASURED"
        observed["pass"] = ok
    else:
        # positive controls: identity precondition only is evaluated here; the field
        # extraction half of the pass criterion is evaluated in stage 3.
        identity_ok = verdict["resolution_status"] == "CORRECTLY_RESOLVED"
        observed["identity_precondition_pass"] = identity_ok
        observed["pass_criterion"] = (
            "artifact passes prereg 4.1 identity resolution AND all required fields are "
            "extracted with evidence quotes (field half evaluated in stage 3)"
        )
        observed["pass"] = None  # completed in stage 3
    jlog({"stage": "control", "control_id": key, "observed": observed})
    return {"frozen_definition": c, "verdict": verdict, "observed": observed}


def main() -> int:
    os.makedirs(RAW, exist_ok=True)
    out = {"schema_version": 1, "experiment_id": "EXP-INTEL-36306525220",
           "stage": "controls_identity", "generated_at": now(), "controls": {}}
    for k in CONTROLS:
        r = resolve_control(k)
        out["controls"][k] = r
        print(f"{k:26s} -> {r['verdict']['resolution_status']:20s} "
              f"artifact_real={r['observed']['artifact_is_real']} "
              f"failed={r['verdict']['failed_conditions']}", flush=True)

    # full text for every CORRECTLY_RESOLVED frozen target (Part 1/2/3 evidence base)
    idr = json.load(open(os.path.join(RAW, "identity_resolution.json"), encoding="utf-8"))
    out["resolved_target_fulltext"] = {}
    for name, v in idr["targets"].items():
        if v["resolution_status"] == "CORRECTLY_RESOLVED":
            out["resolved_target_fulltext"][name] = fetch_fulltext(v["target_arxiv_id"])
            print(f"FULLTEXT {name:16s} {v['target_arxiv_id']} -> "
                  f"{out['resolved_target_fulltext'][name]['status']}", flush=True)

    with open(os.path.join(RAW, "controls_result.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
