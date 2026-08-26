"""AUDIT round-3 session (run 32800296360): re-derive the two cited ablation
controls with own scoring logic over committed evidence + frozen embedder.

  WRONGCTX: fused alpha=0.4, but state term = a DIFFERENT context's summary,
            rotated within the same site (never the query's own page).
  SUMONLY : score = cos(state_summary, desc) only, same pool+MMR machinery.
Expected if the report's attribution is right: both ~24/74 hard@1.
"""
import json, sys
sys.path.insert(0, "/tmp/opencode/audit3/intel/experiments")
sys.path.insert(0, "/tmp/opencode/audit3")
from sgdr_repro import stimuli as S
from sgdr_repro import embedder as E
from sgdr_repro.retriever import FragmentBank
from sgdr_repro.summarizer import summarize

R = "/tmp/opencode/audit3/results/intel/reproductions/cycle1/"
lib = json.load(open(R + "manifest_library.json"))
mc = json.load(open(R + "manifest_contexts.json"))
ev = json.load(open(R + "retrieval_eval.json"))

bank = FragmentBank(lib["fragments"])
stats = {"hits": 0, "misses": 0, "fallbacks": 0}
summaries = {}
for rec in mc["contexts"]:
    if rec["status"] == "ok":
        text, _, _st = summarize(rec["snapshot"], {}, stats)
        summaries[rec["qid"]] = (text, rec["site"])

# deterministic rotation of summaries within each site (never self)
by_site = {}
for qid, (txt, site) in sorted(summaries.items()):
    by_site.setdefault(site, []).append(qid)
rotated = {}
for site, qs in by_site.items():
    n = len(qs)
    for i, q in enumerate(qs):
        rotated[q] = summaries[qs[(i + 1) % n]][0]

def mmr_top1(scored):
    """Greedy MMR identical to frozen spec; returns chosen[0]."""
    rel = dict(scored)
    pool = [fid for fid, _ in sorted(scored, key=lambda t: (-t[1], t[0]))][:S.TOP_M]
    if not pool:
        return None
    chosen = [max(pool, key=lambda fid: (rel[fid], -fid))]
    rest = [f for f in pool if f != chosen[0]]
    while len(chosen) < min(S.TOP_K, len(pool)) and rest:
        def m(fid):
            redundancy = max(bank.desc_sim(fid, c) for c in chosen)
            return S.MMR_LAMBDA * rel[fid] - (1 - S.MMR_LAMBDA) * redundancy
        nxt = max(rest, key=lambda fid: (m(fid), -fid))
        chosen.append(nxt)
        rest.remove(nxt)
    return chosen[0]

rows = [r for r in ev["per_query"] if r["hard"]]
qsite = {c["qid"]: c["site"] for c in mc["contexts"] if c["status"] == "ok"}
res = {"WRONGCTX": 0, "SUMONLY": 0}
for r in rows:
    truth = set(r["truth"])
    frags = bank.site_frags(qsite[r["qid"]])
    task_emb = E.embed(S.FORMULATIONS[r["sig"]][r["form"]])
    # WRONGCTX: alpha*cos(task) + (1-alpha)*cos(wrong summary)
    wrong_emb = E.embed(rotated[r["qid"]])
    sc_w = [(f["id"], 0.4 * bank.rel_task(f["id"], task_emb)
             + 0.6 * E.cosine(wrong_emb, bank.emb[f["id"]])) for f in frags]
    res["WRONGCTX"] += int(mmr_top1(sc_w) in truth)
    # SUMONLY: cos(own summary) only
    own_emb = E.embed(summaries[r["qid"]][0])
    sc_s = [(f["id"], E.cosine(own_emb, bank.emb[f["id"]])) for f in frags]
    res["SUMONLY"] += int(mmr_top1(sc_s) in truth)

print("hard n =", len(rows))
print("WRONGCTX:", f"{res['WRONGCTX']}/{len(rows)}", "| SUMONLY:", f"{res['SUMONLY']}/{len(rows)}")
