#!/usr/bin/env python3
"""EXECUTE external-comparator readiness table for EXP-INTEL-38175568787 (intel lane).

Implements prereg.md Appendix C.2. For each entry in
spec.external_comparators.required_entries, resolve the pinned primary source
(arXiv abs HTML for 2608.12847 and 2604.09718; soft-search-resolved primary
source arXiv 2601.07262 for ColorBrowserAgent) and emit
{system, arxiv_id, title, reported_numbers_with_denominators,
 reproduction_prerequisites, evidence_label: CANDIDATE_NOT_EVIDENCE}.

If a primary pinned source cannot be located, emit NOT_PINNED and do not use that
system's numbers. Non-outcome-bearing and non-gating. No vendor number is SPIDER
evidence; everything here is CANDIDATE_NOT_EVIDENCE.
"""
import json
import os
import re
import sys
import urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38175568787")

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154 Safari/537.36"}


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def citation_title(html):
    m = re.search(r'<meta name="citation_title" content="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    return m.group(1).strip() if m else None


def arxiv_abs(aid):
    url = "https://arxiv.org/abs/%s" % aid
    html = fetch(url)
    return {"url": url, "title": citation_title(html)}


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else EXP
    os.makedirs(os.path.join(outdir, "raw"), exist_ok=True)

    entries = []
    issues = []

    # 1) QCR (target-bound reuse notes) - arXiv 2608.12847
    try:
        qcr = arxiv_abs("2608.12847")
        entries.append({
            "system": "QCR (target-bound reuse notes)",
            "arxiv_id": "2608.12847",
            "primary_source_pinned": True,
            "primary_source_url": qcr["url"],
            "title": qcr["title"],
            "reported_numbers_with_denominators": [
                "+10.7 pts success vs full-trajectory injection (denominator: reported benchmark success-rate points)",
                "-48.9% tokens vs full-trajectory injection (denominator: reported token counts)",
                "2,391 instances across WebArena/WorkArena/AppWorld (denominator: task instances)",
                "stale-binding errors 46.9% -> 10.9% (reported; denominator: error-class counts over stated instance set)"
            ],
            "reproduction_prerequisites": "datasets (WebArena/WorkArena/AppWorld) + base model family + tool set + token-budget denominator + success-rate definition",
            "evidence_label": "CANDIDATE_NOT_EVIDENCE",
        })
    except Exception as e:
        issues.append({"system": "QCR (target-bound reuse notes)", "status": "NOT_PINNED", "error": str(e)[:300]})
        entries.append({
            "system": "QCR (target-bound reuse notes)", "arxiv_id": "2608.12847",
            "primary_source_pinned": False, "title": None,
            "reported_numbers_with_denominators": [], "reproduction_prerequisites": [],
            "evidence_label": "CANDIDATE_NOT_EVIDENCE", "note": "NOT_PINNED: primary source could not be resolved at EXECUTE; numbers not used"
        })

    # 2) compile-and-execute - arXiv 2604.09718
    try:
        ce = arxiv_abs("2604.09718")
        entries.append({
            "system": "compile-and-execute (Agentic Compilation)",
            "arxiv_id": "2604.09718",
            "primary_source_pinned": True,
            "primary_source_url": ce["url"],
            "title": ce["title"],
            "reported_numbers_with_denominators": [
                "5-step workflow, 500 iterations: ~$150 -> <$0.10 (denominator: 500 iterations of the stated 5-step workflow; pricing model)"
            ],
            "reproduction_prerequisites": "workflow/task identity + pricing model + iteration denominator + execution environment",
            "evidence_label": "CANDIDATE_NOT_EVIDENCE",
        })
    except Exception as e:
        issues.append({"system": "compile-and-execute", "status": "NOT_PINNED", "error": str(e)[:300]})
        entries.append({
            "system": "compile-and-execute (Agentic Compilation)", "arxiv_id": "2604.09718",
            "primary_source_pinned": False, "title": None,
            "reported_numbers_with_denominators": [], "reproduction_prerequisites": [],
            "evidence_label": "CANDIDATE_NOT_EVIDENCE", "note": "NOT_PINNED: primary source could not be resolved at EXECUTE; numbers not used"
        })

    # 3) site-memory / ColorBrowserAgent - arXiv 2601.07262 (soft-search-resolved primary source)
    try:
        cb = arxiv_abs("2601.07262")
        title = cb["title"] or "ColorBrowserAgent: Complex Long-Horizon Browser Agent with Adaptive Knowledge Evolution"
        entries.append({
            "system": "site-memory / ColorBrowserAgent",
            "arxiv_id": "2601.07262",
            "primary_source_pinned": True,
            "primary_source_url": cb["url"],
            "title": title,
            "also_published": "ACL 2026 industry track (aclanthology.org/2026.acl-industry.46)",
            "reported_numbers_with_denominators": [
                "71.2% success rate on WebArena (denominator: reported WebArena task set; 812 tasks in the reference benchmark)",
                "47.4% performance under zero-shot transfer on WebChoreArena (denominator: reported WebChoreArena task set)",
                "19.3% relative user-satisfaction improvement in commercial deployment (denominator: reported deployment user-satisfaction metric)",
                "52 distilled site-level rules from <1 person-day (denominator: 52 rules across GitLab 13/Map 7/Reddit 5/Shopping 9/Admin 18)"
            ],
            "reproduction_prerequisites": "primary source identity (arXiv 2601.07262 / ACL 2026.acl-industry.46) + task/site denominators (WebArena/WebChoreArena) + base VLM family + budget + knowledge-adaptation protocol",
            "evidence_label": "CANDIDATE_NOT_EVIDENCE",
        })
    except Exception as e:
        issues.append({"system": "site-memory/ColorBrowserAgent", "status": "NOT_PINNED", "error": str(e)[:300]})
        entries.append({
            "system": "site-memory / ColorBrowserAgent", "arxiv_id": None,
            "primary_source_pinned": False, "title": None,
            "reported_numbers_with_denominators": [], "reproduction_prerequisites": [],
            "evidence_label": "CANDIDATE_NOT_EVIDENCE", "note": "NOT_PINNED: no primary pinned source located at EXECUTE; numbers not used"
        })

    doc = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38175568787",
        "purpose": "Conditional, non-gating deliverable of the Director mandate: enumerate the strongest externally published inheritance/memory systems as candidate fair comparators whose numbers and denominators must be reproduced before use. CANDIDATE_NOT_EVIDENCE; no vendor number is SPIDER evidence.",
        "entries": entries,
        "resolution_issues": issues,
        "comparators_enumerated": sum(1 for e in entries if e.get("primary_source_pinned")),
        "comparators_not_pinned": sum(1 for e in entries if not e.get("primary_source_pinned")),
    }
    with open(os.path.join(outdir, "raw", "external_comparators.json"), "w") as f:
        json.dump(doc, f, indent=2, sort_keys=True)
    print(json.dumps({"enumerated": doc["comparators_enumerated"], "not_pinned": doc["comparators_not_pinned"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())