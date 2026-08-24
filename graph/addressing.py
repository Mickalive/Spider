"""SPIDER TEAM GRAPH — content-derived fragment addressing.

Cycle 32670239235: replaces the run-1 hand-authored `goal_sig` equality
lookup with an addressing layer over AUTO-DERIVED fragment metadata:

  content channel  : URL-shape tokens of the fragment's recorded entry state
                     plus text/href tokens of the elements actually clicked
                     during acquisition (recorded by graph.explorer._ctx_of).
  provenance chan. : the producing agent's own goal keywords, kept as a
                     lower-weight secondary signal (0.4x). This is disclosed
                     hand-authored material on the PRODUCER side only.

The consumer addresses memory with its own task keywords. Exact goal_sig
strings are never used for retrieval here; they remain provenance/debug
labels. If no candidate passes the gates the layer returns UNKNOWN and the
caller must explore — UNKNOWN is never filled from ground truth.

Token weighting: IDF computed from the fragment store itself (no external
corpus, no hand lists). Smoke validation BEFORE the recorded run showed that
unweighted matching let boilerplate tokens (e.g. 'catalogue', present in
almost every books-site context) drive confident but cross-purpose
retrievals; IDF demotes such tokens automatically. Gate constants unchanged.

Preregistered constants (frozen before any recorded cycle-2 outcome):
  CONTENT_W = 1.0, PROVENANCE_W = 0.4,
  MIN_CONTENT_HITS = 1, TAU = 0.25, WEIGHT_CAP = 3.0.
"""
import math
from collections import Counter

from graph.explorer import _slug_tokens

CONTENT_W = 1.0
PROVENANCE_W = 0.4
MIN_CONTENT_HITS = 1
TAU = 0.25
WEIGHT_CAP = 3.0


def _fragment_content_tokens(frag):
    toks = set()
    meta = frag.get("meta") or {}
    toks.update(_slug_tokens(meta.get("entry_url_shape", "")))
    for ctx in meta.get("steps_ctx", []):
        toks.update(ctx.get("text_tokens", []))
        toks.update(ctx.get("href_tokens", []))
    return toks


def _fragment_provenance_tokens(frag):
    meta = frag.get("meta") or {}
    return set(_slug_tokens(" ".join(meta.get("kws_producer", []))))


def _idf_weights(all_frags, query_tokens):
    """Store-computed inverse document frequency over fragment vocabulary."""
    n = max(1, len(all_frags))
    df = Counter()
    for f in all_frags:
        seen = _fragment_content_tokens(f) | _fragment_provenance_tokens(f)
        for t in seen:
            df[t] += 1
    w = {}
    for t in query_tokens:
        w[t] = min(WEIGHT_CAP, math.log(1.0 + n / (1 + df.get(t, 0))))
    return w


def address_fragments(store, query_kws, site=None, tau=TAU,
                      min_content_hits=MIN_CONTENT_HITS):
    """Rank stored fragments against a consumer-side keyword query.

    Returns dict:
      candidates: [{frag_id, goal_sig(provenance), score, content_hits,
                    provenance_hits, success_count}] sorted by score desc
      unknown: True if no candidate passes the gates
      diagnostics are returned even when unknown (for honest reporting).
    """
    qtoks = sorted({t for k in query_kws for t in _slug_tokens(k)})
    pool = store.iter_fragments(site=site)
    iw = _idf_weights(pool, qtoks)
    denom = sum(iw.values()) or 1.0
    cands = []
    for frag in pool:
        if not frag["steps"]:
            continue
        content = _fragment_content_tokens(frag)
        prov = _fragment_provenance_tokens(frag)
        chits = sum(1 for t in qtoks if t in content)
        phits = sum(1 for t in qtoks if t in prov)
        s_content = sum(iw[t] for t in qtoks if t in content)
        s_prov = sum(PROVENANCE_W * iw[t] for t in qtoks if t in prov)
        score = min(1.0, (CONTENT_W * s_content + s_prov) / denom)
        cands.append({"frag_id": frag["id"],
                      "goal_sig": frag["goal_sig"],   # provenance label only
                      "score": round(score, 4),
                      "content_hits": chits,
                      "provenance_hits": phits,
                      "success_count": frag["success_count"],
                      "n_steps": len(frag["steps"])})
    passed = [c for c in cands
              if c["content_hits"] >= min_content_hits and c["score"] >= tau]
    passed.sort(key=lambda c: (-c["score"], -c["success_count"]))
    return {"candidates": passed, "all_scored": len(cands),
            "unknown": len(passed) == 0}
