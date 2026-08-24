"""SPIDER TEAM GRAPH — strong memory baselines for blind inheritance.

Both baselines produce routes consumed by the IDENTICAL replay+fallback
machinery as SPIDER fragments (graph.consumer), so method comparisons differ
only in the memory representation consulted:

  nearest_trajectory : retrieve the stored trajectory whose bounded text
                       profile best matches the consumer query (a concrete
                       stand-in for nearest-successful-trajectory /
                       trajectory-RAG memory).
  graph_bfs          : plan over the concrete state-transition graph with
                       keyword-scored goal states (no fragment abstraction).

Neither baseline reads the fragment table; the SPIDER strategy does not read
trajectories. All methods write to their own private copy of the same
post-production store.
"""
from graph.explorer import _slug_tokens

TRAJ_MIN_HITS = 1      # preregistered: >=1 profile-token overlap required
BFS_MAX_DEPTH = 3      # preregistered planning depth
BFS_FRONTIER_CAP = 60  # bound on expanded nodes


def nearest_trajectory_route(store, query_kws, site):
    qtoks = sorted({t for k in query_kws for t in _slug_tokens(k)})
    if not qtoks:
        return None, {"reason": "empty_query"}
    best, best_hits = None, 0
    n_trajs = 0
    for traj in store.iter_trajectories(site=site):
        n_trajs += 1
        prof = set(traj["profile"])
        hits = sum(1 for t in qtoks if t in prof)
        if hits > best_hits:
            best, best_hits = traj, hits
    diag = {"trajectories_considered": n_trajs, "best_hits": best_hits}
    if not best or best_hits < TRAJ_MIN_HITS or not best["steps"]:
        diag["reason"] = "no_trajectory_above_threshold"
        return None, diag
    diag["source_task"] = best["task_id"]
    steps = [{"kind": s["kind"], "target_sig": s["target_sig"],
              **({"value": s["value"]} if s.get("value") else {})}
             for s in best["steps"]]
    return {"steps": steps, "confidence": 1.0,
            "goal_sig": f"traj:{best['task_id']}"}, diag


def _state_tokens(store, sid):
    raw = store.state_raw(sid)
    if not raw:
        return set()
    return set(_slug_tokens(raw.get("url_shape", ""))) | \
        set(_slug_tokens(raw.get("page_text", "")[:1500]))


def graph_bfs_route(store, snap, query_kws, fingerprint_fn):
    """BFS from the current structural state toward keyword-matching states."""
    qtoks = sorted({t for k in query_kws for t in _slug_tokens(k)})
    if not qtoks:
        return None, {"reason": "empty_query"}
    start_sid = store.state_id_by_fingerprint(fingerprint_fn(snap))
    if start_sid is None:
        return None, {"reason": "current_state_unknown_to_graph"}
    from collections import deque
    q = deque([(start_sid, [])])
    seen = {start_sid}
    best = None   # (score, depth, path)
    expanded = 0
    while q and expanded < BFS_FRONTIER_CAP:
        sid, path = q.popleft()
        if len(path) >= BFS_MAX_DEPTH:
            continue
        for kind, target_sig, to_sid in store.out_edges(sid):
            if to_sid in seen:
                continue
            seen.add(to_sid)
            expanded += 1
            new_path = path + [{"kind": kind, "target_sig": target_sig}]
            toks = _state_tokens(store, to_sid)
            hits = sum(1 for t in qtoks if t in toks)
            score = hits / max(1, len(qtoks))
            if hits > 0 and (best is None or (score, -len(new_path)) >
                             (best[0], -len(best[2]))):
                best = (score, len(new_path), new_path)
            q.append((to_sid, new_path))
            if expanded >= BFS_FRONTIER_CAP:
                break
    diag = {"expanded": expanded, "visited_states": len(seen)}
    if not best:
        diag["reason"] = "no_keyword_matching_state_within_depth"
        return None, diag
    return {"steps": best[2], "confidence": 1.0, "goal_sig": "graph:bfs"}, diag
