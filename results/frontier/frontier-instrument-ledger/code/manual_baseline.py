#!/usr/bin/env python3
"""frontier-instrument-ledger — manual-baseline vs ledger lookup comparison (PREREG sect.7).

Manual policy (frozen): iterative grep over accepted mounts' state/docs/results,
then open up to MAX_OPEN candidate files reading +/-CONTEXT chars around hits.
Every grep/open is logged as a step. Ledger policy: ONE load+filter of the
built ledger/flags JSONs. Correctness adjudication is recorded separately
(manual_vs_ledger_adjudication.json) BEFORE computing the D4 dimension.
"""
import json, os, re, subprocess, sys

TEAM = sys.argv[1]
MOUNTS = ["/tmp/spider_graph", "/tmp/spider_physics", "/tmp/spider_intel",
          "/tmp/spider_product", "/tmp/spider_runtime"]
SUBDIRS = ["state", "docs", "results"]
MAX_OPEN = 6
CONTEXT = 400

QUESTIONS = {
    "M1": {"text": "Spentness/discipline status of the V31 addressing instrument; what does any future quantitative claim require?",
            "terms": ["V31"]},
    "M2": {"text": "Has the books composite evaluation fixture been adapted since creation, pre- or post-evaluation?",
            "terms": ["books instrument defect", "books instrument"]},
    "M3": {"text": "Which lanes reference PhysicsLeakageGuardTests and what status does each record?",
            "terms": ["PhysicsLeakageGuardTests"]},
    "M4": {"text": "Is the Intel unbrowse route-ladder eligible for further confirmatory use under its own CAP/final-round rules?",
            "terms": ["unbrowse", "CAP extended", "final round"]},
    "M5": {"text": "Were WP-006 collector instruments repaired before outcomes, compliantly documented?",
            "terms": ["collector_wp006", "pre-outcome instrument repairs", "WP-006.*repair"]},
    "M6": {"text": "Does SGDR fused-scoring carry binding caveats that must travel into Graph integration?",
            "terms": ["SGDR", "R-1", "caveats travel"]},
}


def manual_search(terms):
    trace, steps, files_hits = [], 0, {}
    seen_terms = []
    for t in terms:
        seen_terms.append(t)
        steps += 1
        cmd = ["grep", "-rInE", t] + [f"{m}/{d}" for m in MOUNTS for d in SUBDIRS if os.path.isdir(f"{m}/{d}")]
        r = subprocess.run(cmd, capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines() if l]
        trace.append({"step": steps, "op": "grep", "pattern": t, "hits": len(lines)})
        for l in lines:
            path = l.split(":", 1)[0]
            files_hits.setdefault(path, []).append(l.split(":", 1)[1][:200] if ":" in l else "")
    opened, snippets = 0, []
    ranked = sorted(files_hits, key=lambda p: -len(files_hits[p]))
    ambiguous_candidates = len(ranked)
    for p in ranked[:MAX_OPEN]:
        opened += 1
        steps += 1
        try:
            content = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        best = None
        for t in seen_terms:
            for m in re.finditer(t, content, re.I):
                best = content[max(0, m.start() - CONTEXT):m.start() + CONTEXT]
                break
            if best:
                break
        snippets.append({"file": p, "excerpt": (best or "")[:600]})
    return {"steps": steps, "files_opened": opened,
            "ambiguous_candidates": ambiguous_candidates, "trace": trace, "snippets": snippets}


def ledger_lookup(qid):
    L = json.load(open(f"{TEAM}/ledger/instrument_ledger.json"))
    Fl = json.load(open(f"{TEAM}/ledger/hazard_flags.json"))["flags"]
    steps = 1  # one structured query over two local JSON artifacts
    key = {"M1": "graph-arm-V31", "M2": "fixture-books-composite",
           "M3": "shared-fixture-PhysicsLeakageGuardTests",
           "M4": "unbrowse-route-capture-replay-ladder",
           "M5": "collector_wp006", "M6": "SGDR-fused-retrieval"}[qid]
    recs = [r for r in L["records"] if r["instrument_id"] == key]
    fls = [f for f in Fl if f["instrument_id"] == key]
    return {"steps": steps, "record_found": bool(recs),
            "record": recs[0] if recs else None, "flags": fls}


if __name__ == "__main__":
    out = {}
    for qid, q in QUESTIONS.items():
        man = manual_search(q["terms"])
        led = ledger_lookup(qid)
        out[qid] = {"question": q["text"],
                    "manual": man,
                    "ledger": {"steps": led["steps"], "record_found": led["record_found"],
                               "spentness": (led["record"] or {}).get("spentness"),
                               "flags_summary": [(f["check"], f["level"]) for f in led["flags"]],
                               "adaptation_timings": [(a["kind"], a["timing"]) for a in (led["record"] or {}).get("adaptation_events", [])],
                               "lanes_seen": (led["record"] or {}).get("lanes_seen")}}
    json.dump(out, open(f"{TEAM}/ledger/manual_vs_ledger.json", "w"), indent=1)
    for qid, o in out.items():
        print(f"{qid}: manual_steps={o['manual']['steps']} manual_ambiguous={o['manual']['ambiguous_candidates']} "
              f"ledger_steps={o['ledger']['steps']} found={o['ledger']['record_found']}")
