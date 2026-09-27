#!/usr/bin/env python3
"""EXP-INTEL-36306525220 :: Stage 1b -- transport-fidelity re-probe.

Stage 1 requested exactly the versioned identifiers frozen in spec.json
(e.g. 1802.08827v3).  arXiv's abs endpoint returns HTTP 404 for a version suffix
that does not exist, which is a transport-fidelity artifact rather than an
identity result.  This stage re-probes ONLY the targets Stage 1 marked NOT_LOCATED
using the base identifier (same frozen base arXiv ID, no version selector) and
records the outcome.  It cannot change an identity verdict to CORRECTLY_RESOLVED
unless the base-ID artifact satisfies all four frozen conditions of prereg 4.1.

It also harvests the reference list of the PC artifact arXiv:2608.05784v1 for the
bounded 1-hop snowball of prereg 4.4, and freezes the snowball selection rule and
the snowball candidate list (path+hash) BEFORE any snowball content is read.
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_identity import (  # noqa: E402
    ART_DIR, HTML_DIR, RAW, classify, http_get, jlog, now, parse_abs_page, sha256_bytes,
)

HERE = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.join(RAW, "references")

SNOWBALL_RULE = (
    "Declared at EXECUTE stage 1b, before any snowball artifact was fetched or read. "
    "Source: the reference list of the positive-control artifact arXiv:2608.05784v1, "
    "taken in document order. Inclusion: reference strings that contain an arXiv "
    "identifier (abs/YYMM.NNNNN form). Cap: first 25 such references, no reordering, "
    "no content-based filtering, no cherry-picking. Each included reference is then "
    "identity-resolved under the frozen prereg 4.1 rule with its OWN frozen expected "
    "identity taken verbatim from the citing paper's own reference string "
    "(expected_title = title substring as printed in the reference, expected_authors = "
    "[] -> condition C3 skipped with reason 'snowball reference carries no author "
    "string', domain_keywords = the frozen global domain keyword list). prereg 4.4 caps "
    "the snowball at 50; this run takes 25."
)
FROZEN_GLOBAL_KEYWORDS = [
    "web", "agent", "browser", "automation", "llm", "e-commerce", "benchmark",
    "environment", "multimodal", "replay", "compilation", "memory", "cache",
    "cost", "token", "screen", "workflow", "gui", "interface",
]


def pdf_text(pdf_path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    return "\n".join((p.extract_text() or "") for p in reader.pages)


def main() -> int:
    os.makedirs(REF_DIR, exist_ok=True)
    idr = json.load(open(os.path.join(RAW, "identity_resolution.json"), encoding="utf-8"))

    # ---- (a) base-ID re-probe for NOT_LOCATED targets only ----
    recheck = {}
    for name, v in idr["targets"].items():
        if v["resolution_status"] != "NOT_LOCATED":
            continue
        base = v["target_arxiv_id"].split("v")[0]
        st, body, err = http_get(f"https://arxiv.org/abs/{base}",
                                 dest=os.path.join(HTML_DIR, base + "_base.html"))
        rec = None
        if st == 200 and body:
            rec = parse_abs_page(body.decode("utf-8", "replace"))
            rec["sha256_abs_page"] = sha256_bytes(body)
            with open(os.path.join(ART_DIR, base + "_base.json"), "w", encoding="utf-8") as fh:
                json.dump(rec, fh, indent=1, sort_keys=True)
        target = {
            "system": name,
            "arxiv_id": base,
            "expected_title": None,       # filled below
            "expected_authors": [],
            "domain_keywords": FROZEN_GLOBAL_KEYWORDS,
        }
        spec = json.load(open(os.path.join(HERE, "spec.json"), encoding="utf-8"))
        ft = spec["identity_resolution"]["frozen_target_list"][name]
        target["expected_title"] = ft["expected_title"]
        # C3 must not be silently satisfied by an empty author list for a frozen
        # target whose authors were frozen as real names: keep the frozen authors.
        target["expected_authors"] = ft["expected_authors"]
        verdict = classify(target, rec, st, err)
        verdict["recheck_note"] = (
            f"Stage-1 request for versioned id {v['target_arxiv_id']} returned HTTP 404; "
            f"re-probed base id {base}."
        )
        recheck[name] = verdict
        print(f"RECHECK {name:12s} {v['target_arxiv_id']} -> base {base} -> {verdict['resolution_status']}")

    jlog({"stage": "base_id_recheck", "targets": recheck})

    # ---- (b) harvest PC artifact reference list, freeze snowball candidate list ----
    pc = "2608.05784v1"
    pdf_path = os.path.join(RAW, "pdf", pc + ".pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    st, body, err = http_get(f"https://arxiv.org/pdf/{pc}", dest=pdf_path)
    refs = []
    if st == 200 and body:
        txt = pdf_text(pdf_path)
        with open(os.path.join(REF_DIR, pc + "_fulltext.txt"), "w", encoding="utf-8") as fh:
            fh.write(txt)
        # arXiv-style reference strings: find "... arXiv:YYMM.NNNNN [cs.AI] ..." patterns
        # and take the line-ish window around each.
        raw_refs = []
        for m in re.finditer(r"arXiv:\d{4}\.\d{4,5}", txt):
            s = max(0, m.start() - 400)
            e = min(len(txt), m.end() + 120)
            window = re.sub(r"\s+", " ", txt[s:e]).strip()
            if window not in raw_refs:
                raw_refs.append(window)
        refs = raw_refs
    with open(os.path.join(REF_DIR, "snowball_candidates.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "schema_version": 1,
            "experiment_id": "EXP-INTEL-36306525220",
            "declared_at": now(),
            "selection_rule": SNOWBALL_RULE,
            "frozen_global_domain_keywords": FROZEN_GLOBAL_KEYWORDS,
            "pdf_status": st,
            "pdf_sha256": sha256_bytes(body) if body else None,
            "n_reference_strings_found": len(refs),
            "references": refs[:25],
        }, fh, indent=1, sort_keys=True)
    print(f"SNOWBALL candidates: {len(refs)} found, {min(len(refs),25)} frozen")

    out = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-36306525220",
        "stage": "base_id_recheck",
        "targets": recheck,
        "snowball": {
            "selection_rule": SNOWBALL_RULE,
            "n_candidates_frozen": min(len(refs), 25),
            "path": os.path.join(REF_DIR, "snowball_candidates.json"),
        },
    }
    with open(os.path.join(RAW, "base_id_recheck.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
