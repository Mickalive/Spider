#!/usr/bin/env python3
"""EXP-INTEL-36306525220 :: Stage 3a -- deterministic pattern sweep (RAW EVIDENCE).

For every artifact that reached at least CORRECTLY_RESOLVED or is a control, sweep a
frozen pattern list over the retrieved text (full text when the PDF was retrievable,
otherwise the arXiv abstract) and write every matching verbatim window to
raw/spans.json.  This stage makes NO determination.  A field is later declared
EXTRACTED / NOT_REPORTED_IN_RETRIEVED_TEXT only after a human-readable reading of
these windows, and every quoted string is machine-verified to be a verbatim substring
of the retrieved text by verify_quotes.py.
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_identity import RAW, now  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TXT_DIR = os.path.join(RAW, "fulltext")
ART_DIR = os.path.join(RAW, "artifacts")
HTML_DIR = os.path.join(RAW, "html")

WIN = 320

# Frozen field pattern list.  Patterns are applied case-insensitively; the emitted
# window is verbatim source text, never paraphrased.
PATTERNS: dict[str, list[str]] = {
    # ---- prereg 5.1 Part 1 cost accounting ----
    "Routine_Overhead_Ratio_R": [r"Routine\s*Overhead\s*Ratio", r"Rinject", r"Rinfo",
                                 r"C\s*agent\s*\(", r"=\s*C\s*agent"],
    "delegable_recurrence_h": [r"delegable\s+recurrence", r"recurrence\s*h", r"h\s*specific",
                               r"h\s*raw", r"h\s*=\s*9", r"h\s*=\s*7"],
    "break_even_reuse_count_fstar": [r"break[-\s]?even", r"breakeven", r"break\s+even\s+reuse",
                                     r"reuse\s+count", r"payback", r"amorti[sz]ation\s+point",
                                     r"f\s*\*"],
    "marginal_cost_cached_vs_derived": [r"marginal\s+cost", r"per[-\s]occurrence\s+reduction",
                                        r"re[-\s]?deriv", r"replay\s+instead\s+of", r"cach"],
    "staleness_forgetting_maintenance_cost": [r"stale", r"staleness", r"forget", r"forgetting",
                                              r"drift", r"invalidat", r"refresh",
                                              r"maintenance\s+cost", r"maintain"],
    "real_cost_advantage_persistence": [r"billed", r"in[-\s]loop", r"real\s+usage",
                                        r"wall[-\s]clock", r"live\s+(?:run|execution|compar)"],
    "denominator": [r"per\s+step", r"per\s+occurrence", r"per\s+routine", r"per\s+action",
                    r"per\s+task", r"per\s+episode", r"denominator", r"per\s+visit",
                    r"per\s+screen", r"per\s+1,?000", r"per\s+frame", r"per\s+day"],
    "accounting_convention": [r"input\s*\+\s*output", r"cl100k", r"tiktoken", r"list\s+rates?",
                              r"Mtok", r"wall[-\s]clock\s+second", r"modeled\s+upper\s+bound",
                              r"upper\s+bound", r"token", r"image[-\s]token"],
    "stated_uncertainty": [r"95%\s*CI", r"confidence\s+interval", r"interquartile", r"\bIQR\b",
                           r"Wilson", r"standard\s+error", r"±", r"min\s*[–-]\s*max",
                           r"no\s+.{0,30}uncertain"],
    "modeled_vs_measured": [r"modeled", r"measured", r"not\s+billed", r"billed"],
    # ---- prereg 5.2 Part 2 performance envelope ----
    "success_rate": [r"success\s+rate", r"task\s+success", r"overall\s+success",
                     r"\d+\.\d+%", r"step\s+success\s+rate"],
    "evaluation_convention": [r"success\s+rate", r"task\s+completion", r"step\s+success\s+rate",
                              r"pass@\d", r"evaluation\s+protocol", r"evaluation\s+metric",
                              r"we\s+(?:report|evaluate|measure)"],
    "benchmark_split": [r"task\s+instances", r"\d{2,4}\s+tasks?\b", r"\d{2,4}\s+(?:websites?|sites?)",
                        r"train(?:ing)?\s+split", r"test\s+split", r"held[-\s]out", r"cross[-\s]site",
                        r"episodes?\b"],
    # ---- prereg 5.3 Part 3 retrieval vs write ----
    "retrieval_quality_metric": [r"recall@\d+", r"precision@\d+", r"nDCG", r"hit\s+rate",
                                 r"retrieval\s+accuracy", r"retrieval\s+quality", r"MRR",
                                 r"context\s+recall", r"relevant\s+context"],
    "write_pipeline_type": [r"raw\s+(?:chunk|row|log|trajector)", r"chunking", r"chunked",
                            r"summari[sz]ation", r"summary\s+of\s+the\s+same", r"extract(?:ion|ive)",
                            r"episodic\s+memory", r"written?\s+memory", r"memory\s+construction"],
    "downstream_accuracy": [r"downstream\s+(?:accuracy|task|performance)", r"question[-\s]answering",
                            r"end[-\s]to[-\s]end\s+(?:accuracy|success)", r"accuracy"],
    "ablation_result": [r"ablat", r"variance", r"explains?\s+more", r"dominant\s+driver",
                        r"attribut", r"contribution\s+of", r"we\s+compare"],
    # ---- construct-presence probe for Part 1 (declared at execute stage 3a) ----
    "persistent_state_construct": [r"persist", r"across\s+sessions?", r"cross[-\s]episode",
                                   r"episodic\s+memory", r"workflow\s+memory", r"replay"],
    # ---- null-control behaviour probe ----
    "NOT_FOUND_token": [r"NOT_FOUND", r"NOT\s+FOUND"],
}


def load_text(cid: str) -> dict:
    p = os.path.join(TXT_DIR, cid.split("v")[0] + ".txt")
    if not os.path.exists(p):
        p = os.path.join(TXT_DIR, cid + ".txt")
    if os.path.exists(p):
        t = open(p, encoding="utf-8", errors="replace").read()
        return {"scope": "full_text", "text": t, "chars": len(t), "path": os.path.relpath(p, HERE)}
    for cand in (os.path.join(ART_DIR, cid + ".json"), os.path.join(ART_DIR, cid.split("v")[0] + "_base.json"),
                 os.path.join(ART_DIR, "ctrl_" + cid + ".json")):
        if os.path.exists(cand):
            rec = json.load(open(cand, encoding="utf-8"))
            t = (rec.get("title") or "") + " " + (rec.get("abstract") or "")
            return {"scope": "abstract_only", "text": t, "chars": len(t), "path": os.path.relpath(cand, HERE)}
    return {"scope": "none", "text": "", "chars": 0, "path": None}


def sweep(cid: str) -> dict:
    src = load_text(cid)
    text = src["text"]
    out = {
        "arxiv_id": cid, "scope": src["scope"], "chars": src["chars"], "source": src["path"],
        "fields": {},
    }
    for field, pats in PATTERNS.items():
        hits = []
        seen = set()
        for pat in pats:
            for m in re.finditer(pat, text, flags=re.I):
                s = max(0, m.start() - WIN // 2)
                e = min(len(text), m.end() + WIN // 2)
                w = re.sub(r"\s+", " ", text[s:e]).strip()
                key = w[:120]
                if key in seen:
                    continue
                seen.add(key)
                hits.append({"pattern": pat, "offset": m.start(), "window": w})
                if len(hits) >= 40:
                    break
            if len(hits) >= 40:
                break
        out["fields"][field] = hits
    return out


def main() -> int:
    spec = json.load(open(os.path.join(HERE, "spec.json"), encoding="utf-8"))
    frozen = spec["identity_resolution"]["frozen_target_list"]
    ctrl = json.load(open(os.path.join(RAW, "controls_result.json"), encoding="utf-8"))

    ids = {}
    for name, t in frozen.items():
        ids[f"target:{name}"] = t["arxiv_id"]
    for k, v in ctrl["controls"].items():
        ids[f"control:{k}"] = v["frozen_definition"]["arxiv_id"]
        if v["frozen_definition"]["arxiv_id"].split("v")[0] not in {i.split("v")[0] for i in ids.values()}:
            ids[f"control-base:{k}"] = v["frozen_definition"]["arxiv_id"].split("v")[0]

    res = {k: sweep(v) for k, v in ids.items()}
    path = os.path.join(RAW, "spans.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"schema_version": 1, "experiment_id": "EXP-INTEL-36306525220",
                   "generated_at": now(), "window_chars": WIN, "spans": res}, fh, indent=1, sort_keys=True)
    for k, v in res.items():
        print(f"{k:34s} {v['arxiv_id']:16s} scope={v['scope']:14s} chars={v['chars']}")
    print("wrote", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
