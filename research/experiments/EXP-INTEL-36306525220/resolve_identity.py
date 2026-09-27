#!/usr/bin/env python3
"""EXP-INTEL-36306525220 :: Stage 1 -- deterministic identity resolution.

Implements the FROZEN matching rule of prereg.md Section 4.1 / Section 4.2 verbatim.
No outcome-bearing field extraction happens in this stage. No scoring happens here.

Transport note: the frozen prereg Section 4.2 step 1 says "Query arXiv API with exact
arXiv ID". export.arxiv.org/api and arxiv.org/api both return HTTP 406 from arXiv's
own varnish for this runner's egress IP (recorded in raw/search_log.jsonl as
transport_probe entries). The arXiv abstract landing page https://arxiv.org/abs/<id>
and the PDF at https://arxiv.org/pdf/<id> return HTTP 200 and carry the same
authoritative citation_* metadata. This stage therefore retrieves by exact arXiv ID
over the abs/PDF transport. The identity assertions are unchanged.

Raw evidence written to raw/ ; nothing here is interpreted.
"""

from __future__ import annotations

import hashlib
import html as html_mod
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

EXPERIMENT_ID = "EXP-INTEL-36306525220"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
HTML_DIR = os.path.join(RAW, "html")
ART_DIR = os.path.join(RAW, "artifacts")
SEARCH_LOG = os.path.join(RAW, "search_log.jsonl")

USER_AGENT = "SPIDER-Research-2.0/1.0 (EXP-INTEL-36306525220; arXiv identity resolution; python-urllib)"

# Frozen implementation decisions, declared BEFORE any field extraction or outcome
# was observed. Recorded in provenance.json -> frozen_implementation_decisions.
TITLE_JACCARD_THRESHOLD = 0.85          # prereg 4.1(2)
TITLE_COVERAGE_THRESHOLD = 0.85         # prereg 4.1(2) substring reading
RETRIES = 3
SLEEP_S = 2.0


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def jlog(rec: dict) -> None:
    rec = dict(rec)
    rec.setdefault("ts", now())
    with open(SEARCH_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


def http_get(url: str, dest: str | None = None) -> tuple[int, bytes, str]:
    last = None
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read()
                if dest:
                    with open(dest, "wb") as fh:
                        fh.write(body)
                jlog({
                    "stage": "http_get", "url": url, "attempt": attempt,
                    "http_status": r.status, "bytes": len(body),
                    "sha256": sha256_bytes(body), "dest": dest,
                })
                return r.status, body, ""
        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()
            except Exception:
                pass
            msg = f"HTTPError {e.code}"
            jlog({
                "stage": "http_get", "url": url, "attempt": attempt,
                "http_status": e.code, "bytes": len(body), "error": msg,
                "response_body_head": body[:200].decode("utf-8", "replace"),
            })
            last = msg
            if e.code in (400, 404, 406):
                return e.code, b"", msg
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            jlog({"stage": "http_get", "url": url, "attempt": attempt, "error": last})
        time.sleep(SLEEP_S)
    return 0, b"", last or "unknown"


TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html_mod.unescape(s)
    return WS.sub(" ", s).strip()


TOKEN = re.compile(r"[a-z0-9]+")


def toks(s: str) -> set[str]:
    return set(TOKEN.findall(s.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def coverage(need: set[str], have: set[str]) -> float:
    if not need:
        return 0.0
    return len(need & have) / len(need)


def parse_abs_page(body: str) -> dict:
    def meta(name: str) -> list[str]:
        pats = [
            r'<meta\s+name="%s"\s+content="([^"]*)"' % re.escape(name),
            r'<meta\s+content="([^"]*)"\s+name="%s"' % re.escape(name),
        ]
        out = []
        for p in pats:
            out.extend(html_mod.unescape(m) for m in re.findall(p, body))
        return out

    title = (meta("citation_title") or [""])[0]
    authors = meta("citation_author")
    arxid = (meta("citation_arxiv_id") or [""])[0]
    date = (meta("citation_date") or [""])[0]
    abstract = ""
    m = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', body, re.S)
    if m:
        abstract = clean(m.group(1))
        abstract = re.sub(r"^Abstract:\s*", "", abstract)
    if not abstract:
        m = re.search(r'name="citation_abstract"\s+content="([^"]*)"', body)
        if m:
            abstract = clean(html_mod.unescape(m.group(1)))
    # submission history -> available versions
    versions = []
    mh = re.search(r"Submission history(.*?)</div>", body, re.S)
    if mh:
        for v in re.findall(r"\[v(\d+)\]", mh.group(1)):
            versions.append(int(v))
    # journal / comments
    comments = ""
    mc = re.search(r'<td class="tablecell comments[^"]*">(.*?)</td>', body, re.S)
    if mc:
        comments = clean(mc.group(1))
    return {
        "title": title,
        "authors": authors,
        "arxiv_id_returned": arxid,
        "citation_date": date,
        "abstract": abstract,
        "available_versions": sorted(set(versions)),
        "comments": comments,
    }


def classify(target: dict, rec: dict | None, transport_status: int, error: str) -> dict:
    """Apply prereg 4.1 matching rule deterministically. No scoring, no extraction."""
    expected = target["expected_title"]
    exp_authors = target["expected_authors"]
    kw = target["domain_keywords"]
    cid = target["arxiv_id"]

    out = {
        "target_system": target["system"],
        "target_arxiv_id": cid,
        "transport_status": transport_status,
        "transport_error": error or None,
        "returned_arxiv_id": None,
        "returned_title": None,
        "returned_authors": None,
        "checks": {},
        "failed_conditions": [],
        "resolution_status": "NOT_LOCATED",
    }
    if rec is None:
        out["failed_conditions"] = ["C0_no_artifact_retrieved"]
        out["resolution_status"] = "NOT_LOCATED"
        return out

    out["returned_arxiv_id"] = rec["arxiv_id_returned"]
    out["returned_title"] = rec["title"]
    out["returned_authors"] = rec["authors"]

    # C1 exact arXiv ID agreement (base id; version fidelity reported separately)
    base_want = cid.split("v")[0]
    base_got = (rec["arxiv_id_returned"] or "").split("v")[0]
    c1 = base_want == base_got and base_want != ""
    out["checks"]["C1_exact_arxiv_id"] = {
        "pass": c1, "expected_base": base_want, "returned_base": base_got,
        "frozen_version_requested": cid,
        "available_versions": rec["available_versions"],
        "frozen_version_exists": (
            int(cid.split("v")[1]) in rec["available_versions"] if "v" in cid and rec["available_versions"] else None
        ),
    }
    if not c1:
        out["failed_conditions"].append("C1_arxiv_id_mismatch")

    # C2 title match -- both readings logged; substring/coverage is the primary test
    # because prereg 4.1(2) states "matches the expected title substring ... fuzzy
    # threshold".  The full-set Jaccard is logged so an auditor can recompute.
    et, at = toks(expected), toks(rec["title"] or "")
    jf = jaccard(et, at)
    cov = coverage(et, at)
    sub = expected.lower() in (rec["title"] or "").lower()
    c2 = bool(sub and cov >= TITLE_COVERAGE_THRESHOLD)
    out["checks"]["C2_title"] = {
        "pass": c2, "expected_title": expected, "returned_title": rec["title"],
        "jaccard_full_title_tokens": round(jf, 6),
        "expected_token_coverage_in_title": round(cov, 6),
        "expected_title_is_substring": sub,
        "jaccard_threshold": TITLE_JACCARD_THRESHOLD,
        "coverage_threshold": TITLE_COVERAGE_THRESHOLD,
        "primary_reading": "substring_and_token_coverage",
    }
    if not c2:
        out["failed_conditions"].append("C2_title_mismatch")

    # C3 author substring match
    authors_lc = " | ".join(rec["authors"]).lower()
    matched_authors = [a for a in exp_authors if a.lower() in authors_lc]
    author_list_is_tbd = any(str(a).strip().upper() == "TBD" for a in exp_authors)
    if author_list_is_tbd:
        c3 = None
        out["checks"]["C3_author"] = {
            "pass": None, "expected_authors": exp_authors, "matched": [],
            "unevaluable_reason": "frozen expected_authors == ['TBD']; condition not evaluable",
        }
        out["failed_conditions"].append("C3_author_unevaluable_TBD")
    else:
        c3 = len(matched_authors) > 0
        out["checks"]["C3_author"] = {
            "pass": c3, "expected_authors": exp_authors, "matched": matched_authors,
            "returned_authors": rec["authors"],
        }
        if not c3:
            out["failed_conditions"].append("C3_author_mismatch")

    # C4 domain keyword in abstract
    abstract_lc = (rec["abstract"] or "").lower()
    matched_kw = [k for k in kw if k.lower() in abstract_lc]
    c4 = len(matched_kw) > 0
    out["checks"]["C4_domain_keyword"] = {
        "pass": c4, "domain_keywords": kw, "matched": matched_kw,
        "abstract_available": bool(rec["abstract"]),
    }
    if not c4:
        out["failed_conditions"].append("C4_domain_keyword_absent")

    if c1 and c2 and c3 is True and c4:
        out["resolution_status"] = "CORRECTLY_RESOLVED"
    elif rec["abstract"] or rec["title"]:
        out["resolution_status"] = "AMBIGUOUS"
    else:
        out["resolution_status"] = "NOT_LOCATED"
    return out


def resolve(target: dict) -> dict:
    cid = target["arxiv_id"]
    html_path = os.path.join(HTML_DIR, cid + ".html")
    status, body, err = http_get(f"https://arxiv.org/abs/{cid}", dest=html_path)
    rec = None
    if status == 200 and body:
        rec = parse_abs_page(body.decode("utf-8", "replace"))
        rec["sha256_abs_page"] = sha256_bytes(body)
        with open(os.path.join(ART_DIR, cid + ".json"), "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
    verdict = classify(target, rec, status, err)
    jlog({"stage": "resolve", "target": target, "verdict": verdict})
    return verdict


def main() -> int:
    os.makedirs(HTML_DIR, exist_ok=True)
    os.makedirs(ART_DIR, exist_ok=True)

    spec = json.load(open(os.path.join(HERE, "spec.json"), encoding="utf-8"))
    frozen = spec["identity_resolution"]["frozen_target_list"]

    # ---- transport probe, recorded as raw evidence of the substrate condition ----
    probes = []
    for label, url in [
        ("arxiv_atom_api_export", "https://export.arxiv.org/api/query?id_list=2207.01206v4&max_results=1"),
        ("arxiv_atom_api_www", "https://arxiv.org/api/query?id_list=2207.01206v4&max_results=1"),
        ("arxiv_abs_page", "https://arxiv.org/abs/2207.01206v4"),
        ("semantic_scholar", "https://api.semanticscholar.org/graph/v1/paper/arXiv:2207.01206?fields=title"),
    ]:
        st, bd, er = http_get(url)
        probes.append({"label": label, "url": url, "http_status": st, "error": er or None, "bytes": len(bd)})
    jlog({"stage": "transport_probe", "probes": probes})

    results = {}
    for name, tgt in frozen.items():
        tgt = dict(tgt)
        tgt["system"] = name
        results[name] = resolve(tgt)
        print(f"{name:16s} {tgt['arxiv_id']:16s} -> {results[name]['resolution_status']}", flush=True)

    out = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "stage": "identity_resolution",
        "frozen_matching_rule_source": "prereg.md Section 4.1/4.2, spec.json identity_resolution.matching_rule",
        "title_jaccard_threshold": TITLE_JACCARD_THRESHOLD,
        "title_coverage_threshold": TITLE_COVERAGE_THRESHOLD,
        "transport_probes": probes,
        "targets": results,
    }
    with open(os.path.join(RAW, "identity_resolution.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
