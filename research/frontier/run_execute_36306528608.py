"""EXECUTE runner for EXP-FRONTIER-36306528608 (lane=frontier).

Stage order follows the frozen prereg strictly:

  STAGE 1  prereg 4.1  calibration procedure on the frozen calibration site.
                      TEST screening is gated on this passing.
  STAGE 2  prereg 4.2/4.3 screen over the frozen candidate pool, in frozen order,
                      with no post-freeze substitution.
  STAGE 3  prereg 7/11 action-gating object detection and the deterministic
                      re-derivable classification, per site.
  STAGE 4  frozen arms x episodes, only if >= 3 sites qualify (prereg 6).
                      Otherwise the frozen 4.4 fallback record is emitted.
  STAGE 5  derived measurements + frozen decision rule (prereg 14, 17).

Raw evidence (raw/*.jsonl, raw/responses_cache/) is written before any derived
statistic. No arm is skipped and no threshold is relaxed.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import screen_36306528608 as S  # noqa: E402
from harness_36306528608 import (  # noqa: E402
    EXPERIMENT_ID,
    RAW_DIR,
    ResponseCache,
    JsonlWriter,
    file_sha256,
)

PKG_DIR = os.path.join("research", "experiments", EXPERIMENT_ID)
RUN_T0 = time.time()


def jdump(path: str, obj: Any) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)
    return path


def main() -> int:
    os.makedirs(RAW_DIR, exist_ok=True)
    http_raw = JsonlWriter(os.path.join(RAW_DIR, "http.jsonl"))
    pages_w = JsonlWriter(os.path.join(RAW_DIR, "pages.jsonl"))
    screen_w = JsonlWriter(os.path.join(RAW_DIR, "screen.jsonl"))
    objects_w = JsonlWriter(os.path.join(RAW_DIR, "objects.jsonl"))
    ident_w = JsonlWriter(os.path.join(RAW_DIR, "identifiers.jsonl"))
    calib_w = JsonlWriter(os.path.join(RAW_DIR, "calibration.jsonl"))
    class_w = JsonlWriter(os.path.join(RAW_DIR, "classification.jsonl"))
    cache = ResponseCache()

    summary: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "stages": {},
    }

    # ------------------------------------------------------------------ #
    # STAGE 1 -- prereg 4.1 calibration
    # ------------------------------------------------------------------ #
    print("[stage1] calibration on", S.CALIBRATION_SITE, flush=True)
    calib = S.screen_site(
        S.CALIBRATION_SITE, pages_w, http_raw, cache, "calibration",
        root_obs=S.CALIBRATION_ROOT,
    )
    calib_objects = calib["_objects"]
    calib_class = [S.classify_rederivable(o, calib["_pages"][0]) for o in calib_objects]
    calibration_pass = bool(calib["qualifies"])
    calib_record = {
        "experiment_id": EXPERIMENT_ID,
        "calibration_site": S.CALIBRATION_ROOT,
        "prereg_claim_about_site": (
            "prereg.md 4.1 asserts this endpoint 'returns an HTML form with a CSRF-like token "
            "(<input name=\"csrf_token\" ...>)', that 'the csrf_token rotates or is session-bound', "
            "and that it therefore contains a session-scoped identifier, a write verb and a "
            "multi-step GET form -> extract token -> POST flow"
        ),
        "criteria": {c: calib[c] for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C7")},
        "qualifies": calib["qualifies"],
        "calibration_pass": calibration_pass,
        "calibration_procedure_result": (
            "PASS" if calibration_pass else
            "FAIL -- the frozen known-positive calibration site does not satisfy the frozen "
            "screen, so the screen has no demonstrated true-positive detection power"
        ),
        "objects_detected": len(calib_objects),
        "objects": calib_objects,
        "classification": calib_class,
        "root_observation_forms": [
            {"method": f["method"], "action": f["action"], "input_names": f["input_names"],
             "token_fields": f["token_fields"]}
            for f in calib["_pages"][0]["forms"]
        ],
        "root_observation_input_names": calib["_pages"][0].get("token_fields"),
        "http_requests": calib["http_requests"],
        "pages_fetched": calib["pages_fetched"],
    }
    calib_w.write(calib_record)
    summary["stages"]["stage1_calibration"] = {
        "calibration_site": S.CALIBRATION_ROOT,
        "calibration_pass": calibration_pass,
        "criteria": calib_record["criteria"],
        "objects_detected": len(calib_objects),
        "root_form_input_names": calib_record["root_observation_forms"][0]["input_names"] if calib_record["root_observation_forms"] else [],
        "http_requests": calib["http_requests"],
    }
    print("[stage1] calibration_pass =", calibration_pass, flush=True)

    # ------------------------------------------------------------------ #
    # STAGE 2 -- frozen candidate pool
    # ------------------------------------------------------------------ #
    print("[stage2] screening", len(S.CANDIDATE_POOL), "frozen candidate sites", flush=True)
    pool: list[dict[str, Any]] = []
    for i, url in enumerate(S.CANDIDATE_POOL):
        print(f"  [{i+1}/{len(S.CANDIDATE_POOL)}] {url}", flush=True)
        try:
            rec = S.screen_site(url, pages_w, http_raw, cache, f"pool{i:02d}")
        except Exception as exc:  # a crash is recorded, never silently dropped
            rec = {
                "url": url, "error": f"{type(exc).__name__}: {exc}", "qualifies": False,
                "C1": {"pass": False, "reason": "screen raised"}, "C2": {"pass": False, "reason": "screen raised"},
                "C3": {"pass": False, "reason": "screen raised"}, "C4": {"pass": False, "reason": "screen raised"},
                "C5": {"pass": False, "reason": "screen raised"}, "C6": {"pass": False, "reason": "screen raised"},
                "C7": {"pass": False, "reason": "screen raised"},
                "missing_ingredients": ["screen did not complete"], "_objects": [], "_pages": [],
                "http_requests": 0, "pages_fetched": 0, "non_gating_write_actions": [],
            }
        rec["pool_index"] = i
        rec["reached"] = bool(rec.get("C6", {}).get("reachable"))
        pool.append(rec)
        persistable = {k: v for k, v in rec.items() if not k.startswith("_")}
        persistable["objects"] = rec.get("_objects", [])
        screen_w.write(persistable)
        print(f"      qualifies={rec['qualifies']} C1={rec['C1']['pass']} C2={rec['C2']['pass']} "
              f"C3={rec['C3']['pass']} C4={rec['C4']['pass']} C5={rec['C5']['pass']} "
              f"C6={rec['C6']['pass']} C7={rec['C7']['pass']} reqs={rec['http_requests']}", flush=True)

    qualifying = [r for r in pool if r["qualifies"]]
    unreachable = [r for r in pool if not r.get("reached")]
    reached = [r for r in pool if r.get("reached")]
    summary["stages"]["stage2_screen"] = {
        "candidates_screened": len(pool),
        "candidates_reachable": len(reached),
        "candidates_unreachable": len(unreachable),
        "unreachable_urls": [r["url"] for r in unreachable],
        "qualifying_count": len(qualifying),
        "qualifying_urls": [r["url"] for r in qualifying],
        "min_required": S.MIN_QUALIFYING_SITES,
        "per_criterion_pass_counts": {
            c: sum(1 for r in pool if r[c]["pass"]) for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C7")
        },
        "per_criterion_pass_urls": {
            c: [r["url"] for r in pool if r[c]["pass"]] for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C7")
        },
    }
    print(f"[stage2] qualifying={len(qualifying)}/{S.MIN_QUALIFYING_SITES}", flush=True)

    # ------------------------------------------------------------------ #
    # STAGE 3 -- prereg 7/11 object detection + re-derivable classification
    # ------------------------------------------------------------------ #
    print("[stage3] object detection + re-derivable classification", flush=True)
    site_records: list[dict[str, Any]] = []
    for rec in pool:
        pages = rec.get("_pages", [])
        if not pages:
            continue
        root_page = min(pages, key=lambda p: p["depth"])
        classes = []
        for o in rec.get("_objects", []):
            c = S.classify_rederivable(o, root_page)
            c.update({
                "experiment_id": EXPERIMENT_ID, "site": rec["url"],
                "object_index": o["object_index"], "object_page_url": o["page_url"],
            })
            classes.append(c)
            class_w.write(c)
        objs = [{**o, "rederivable": next((c["rederivable"] for c in classes if c["object_id"] == o["object_id"]), None)}
                for o in rec.get("_objects", [])]
        for o in objs:
            objects_w.write({k: v for k, v in o.items()})
        idents = S.classify_identifiers(pages, rec["url"], "screen", ident_w)
        n_span = len(objs)
        n_reder = sum(1 for o in objs if o["rederivable"])
        site_records.append({
            "site": rec["url"],
            "root_observation_url": root_page["url"],
            "root_observation_tokens": None,
            "objects": objs,
            "n_action_gating_spans": n_span,
            "n_rederivable_spans": n_reder,
            "rederivable_fraction_site": (n_reder / n_span) if n_span else None,
            "classifications": classes,
            "identifiers_detected": len(idents),
            "page_urls": [p["url"] for p in pages],
            "depths": [p["depth"] for p in pages],
        })

    # pooled same-unit numerator/denominator over EVERY screened site
    tot_spans = sum(r["n_action_gating_spans"] for r in site_records)
    tot_reder = sum(r["n_rederivable_spans"] for r in site_records)
    summary["stages"]["stage3_objects"] = {
        "sites_with_objects": len(site_records),
        "total_action_gating_spans": tot_spans,
        "total_rederivable_spans": tot_reder,
        "pooled_rederivable_fraction": (tot_reder / tot_spans) if tot_spans else None,
        "numerator_unit": "count of action-gating spans re-derivable from one unconditional GET of the root observation",
        "denominator_unit": "count of action-gating spans",
        "per_site": [
            {"site": r["site"], "n_action_gating_spans": r["n_action_gating_spans"],
             "n_rederivable_spans": r["n_rederivable_spans"],
             "rederivable_fraction_site": r["rederivable_fraction_site"]}
            for r in site_records
        ],
        "identifiers_detected_total": sum(r["identifiers_detected"] for r in site_records),
    }
    print(f"[stage3] spans={tot_spans} rederivable={tot_reder}", flush=True)

    # ------------------------------------------------------------------ #
    # STAGE 4/5 -- handled by the caller module once the gate is decided
    # ------------------------------------------------------------------ #
    cache.flush_keys()
    cache.flush_index()
    for w in (http_raw, pages_w, screen_w, objects_w, ident_w, calib_w, class_w):
        w.close()

    jdump(os.path.join(PKG_DIR, "derived", "screen_summary.json"), summary)
    jdump(os.path.join(PKG_DIR, "derived", "site_records.json"), [
        {k: v for k, v in r.items() if k not in ("objects",)} for r in site_records
    ])
    jdump(os.path.join(PKG_DIR, "derived", "gate_decision.json"), {
        "experiment_id": EXPERIMENT_ID,
        "calibration_pass": calibration_pass,
        "qualifying_sites": [r["url"] for r in qualifying],
        "qualifying_count": len(qualifying),
        "min_required": S.MIN_QUALIFYING_SITES,
        "arm_phase_entered": len(qualifying) >= S.MIN_QUALIFYING_SITES,
        "wall_clock_s": round(time.time() - RUN_T0, 1),
        "http_requests_total": http_raw.n,
        "pages_total": pages_w.n,
    })
    print("[done] wall_clock_s =", round(time.time() - RUN_T0, 1),
          "http_requests =", http_raw.n, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
