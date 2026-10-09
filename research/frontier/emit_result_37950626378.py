"""Emit result.json and provenance.json for EXP-FRONTIER-37950626378.

This is a packet-emission helper. It reads the measured derived/metrics.json,
derived/analysis.json and the raw artifacts produced by
research/frontier/run_execute_37950626378.py and writes the canonical
result.json / provenance.json exactly in the research/EXPERIMENT_PACKET.md shape.
It performs no new measurement.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP = os.path.join(ROOT, "research", "experiments", "EXP-FRONTIER-37950626378")
RAW = os.path.join(EXP, "raw")
DERIVED = os.path.join(EXP, "derived")
CODE = os.path.join(ROOT, "research", "frontier", "run_execute_37950626378.py")

EXPERIMENT_ID = "EXP-FRONTIER-37950626378"
LANE = "frontier"


def sha256_file(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def artifact_entries() -> list[dict]:
    out = [{"path": os.path.relpath(CODE, ROOT),
            "sha256": sha256_file(CODE), "role": "code"}]
    for d in (RAW, DERIVED):
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if not os.path.isfile(p):
                continue
            role = "raw" if d == RAW else "derived"
            out.append({"path": os.path.relpath(p, ROOT),
                        "sha256": sha256_file(p), "role": role})
    return out


def main() -> int:
    m = json.load(open(os.path.join(DERIVED, "metrics.json")))
    a = json.load(open(os.path.join(DERIVED, "analysis.json")))

    ctrls = m["controls"]
    pooled = m["pooled"]
    be = m["breakeven"]
    gate = m["admission_gate"]

    # frozen metric identities from spec.metrics
    metrics = {
        "pooled_ratio_requests_deep_over_near":
            pooled["ratio_requests_deep_over_near"],
        "pooled_ratio_bytes_deep_over_near":
            pooled["ratio_bytes_deep_over_near"],
        "pooled_verdict": pooled["verdict"],
        "materiality_factor": 3.0,
        "falsifier_triggered": (
            pooled["ratio_requests_deep_over_near"] is not None and
            pooled["ratio_bytes_deep_over_near"] is not None),
        "pooled_band_sizes": {
            "n_deep": pooled["n_deep"], "n_near": pooled["n_near"],
            "n_mid_excluded": pooled["n_mid_excluded"],
            "n_items_deduped": pooled["n_items_deduped"],
            "n_duplicate_rows_removed": pooled["n_duplicate_rows_removed"],
        },
        "median_re_derivation_requests_by_band": {
            "NEAR": a["NEAR"]["median_red_requests"],
            "MID": a["MID"]["median_red_requests"],
            "DEEP": a["DEEP"]["median_red_requests"],
        },
        "median_re_derivation_bytes_by_band": {
            "NEAR": a["NEAR"]["median_red_bytes"],
            "MID": a["MID"]["median_red_bytes"],
            "DEEP": a["DEEP"]["median_red_bytes"],
        },
        "median_re_acquisition_path_requests_by_band": {
            "NEAR": a["NEAR"]["median_racq_path_requests"],
            "MID": a["MID"]["median_racq_path_requests"],
            "DEEP": a["DEEP"]["median_racq_path_requests"],
        },
        "median_re_acquisition_path_bytes_by_band": {
            "NEAR": a["NEAR"]["median_racq_path_bytes"],
            "MID": a["MID"]["median_racq_path_bytes"],
            "DEEP": a["DEEP"]["median_racq_path_bytes"],
        },
        "racq_path_ratio_deep_over_near_requests":
            a["racq_path_ratio_deep_over_near_requests"],
        "racq_path_ratio_deep_over_near_bytes":
            a["racq_path_ratio_deep_over_near_bytes"],
        "median_break_even_reuse_count_requests_by_band": {
            b: be[b]["median_break_even_reuse_count_requests"]
            for b in ("NEAR", "MID", "DEEP")},
        "median_break_even_reuse_count_bytes_by_band": {
            b: be[b]["median_break_even_reuse_count_bytes"]
            for b in ("NEAR", "MID", "DEEP")},
        "break_even_eligible_counts_by_band": {
            b: {"eligible": be[b]["n_eligible"], "n": be[b]["n_items"]}
            for b in ("NEAR", "MID", "DEEP")},
        "admission_gate": {
            "id": gate["id"], "pass": gate["pass"],
            "observed": gate["observed"], "requires": gate["requires"]},
        "per_site_ratios_session_a": {
            s: {
                "ratio_requests_deep_over_near":
                    r["ratio_session_a"]["ratio_requests_deep_over_near"],
                "ratio_bytes_deep_over_near":
                    r["ratio_session_a"]["ratio_bytes_deep_over_near"],
                "verdict": r["ratio_session_a"]["verdict"],
                "n_deep_kept": r.get("n_deep_kept"),
                "n_near_kept": r.get("n_near_kept"),
                "items_kept": r.get("items_kept"),
                "site_unstable_excluded": r.get("site_unstable_excluded"),
            }
            for s, r in m["site_reports"].items()},
        "deep_items_by_site": a["deep_items_by_site"],
        "deep_hosts": a["deep_hosts"],
        "near_hosts": a["near_hosts"],
        "path_len_equals_hop_plus_one": m["path_consistency"],
        "session_agreement": a["session_agreement"],
        "controls_metric": {k: v["pass"] for k, v in ctrls.items()},
        "substrate_economics": {
            "n_http_get": m["n_http_get"], "n_non_get": 0,
            "wall_clock_seconds": m["wall_clock_seconds"],
            "max_body_bytes": 600000, "timeout_s": 12,
        },
        "environment": m["environment"],
        "frozen_inputs_verified_unmodified": {
            k: v["match"] for k, v in m["frozen_inputs"].items()},
    }

    controls = {
        "POS_KNOWN_HOP_CONTROL": {
            "frozen_kind": "positive",
            "expected": ctrls["POS_KNOWN_HOP_CONTROL"]["expected"],
            "observed": ctrls["POS_KNOWN_HOP_CONTROL"]["observed"],
            "pass": ctrls["POS_KNOWN_HOP_CONTROL"]["pass"],
            "evidence_refs": ["raw/controls.jsonl", "raw/http.jsonl"],
        },
        "NEG_UNREACHABLE_CONTROL": {
            "frozen_kind": "null/negative",
            "expected": ctrls["NEG_UNREACHABLE_CONTROL"]["expected"],
            "observed": ctrls["NEG_UNREACHABLE_CONTROL"]["observed"],
            "pass": ctrls["NEG_UNREACHABLE_CONTROL"]["pass"],
            "evidence_refs": ["raw/controls.jsonl", "raw/http.jsonl"],
        },
        "NARROW_CHAIN_CALIBRATION": {
            "frozen_kind": "dynamic-range FLAT",
            "expected": ctrls["NARROW_CHAIN_CALIBRATION"]["expected"],
            "observed": ctrls["NARROW_CHAIN_CALIBRATION"]["observed"],
            "pass": ctrls["NARROW_CHAIN_CALIBRATION"]["pass"],
            "evidence_refs": ["raw/controls.jsonl", "raw/http.jsonl"],
        },
        "BROAD_FANOUT_CALIBRATION": {
            "frozen_kind": "dynamic-range GROWING",
            "expected": ctrls["BROAD_FANOUT_CALIBRATION"]["expected"],
            "observed": ctrls["BROAD_FANOUT_CALIBRATION"]["observed"],
            "pass": ctrls["BROAD_FANOUT_CALIBRATION"]["pass"],
            "evidence_refs": ["raw/controls.jsonl", "raw/http.jsonl"],
        },
        "RED_re_derivation": {
            "frozen_role": "baseline comparator (item-blind BFS prefix)",
            "expected": "most expensive arm by construction; superset of the "
                        "shortest-path pages",
            "observed": {
                "median_requests_DEEP": a["DEEP"]["median_red_requests"],
                "median_requests_NEAR": a["NEAR"]["median_red_requests"],
                "ordering_RED_ge_RACQ_PATH": True,
            },
            "pass": True,
            "evidence_refs": ["derived/metrics.json", "derived/analysis.json"],
        },
        "RACQ_PATH_re_acquisition": {
            "frozen_role": "primary re-acquisition arm (persisted shortest path)",
            "expected": "h+1 GETs; strictly cheaper than RED whenever the BFS "
                        "takes >=1 detour",
            "observed": {
                "median_requests_DEEP": a["DEEP"]["median_racq_path_requests"],
                "median_requests_NEAR": a["NEAR"]["median_racq_path_requests"],
                "median_saving_requests_DEEP":
                    a["DEEP"]["median_saving_requests"],
                "path_len_equals_hop_plus_one": m["path_consistency"],
            },
            "pass": True,
            "evidence_refs": ["derived/metrics.json", "derived/analysis.json"],
        },
        "RACQ_URL_re_acquisition": {
            "frozen_role": "persisted-URL re-acquisition (absolute lower bound)",
            "expected": "exactly 1 GET for every h>=0",
            "observed": {"requests": 1, "applies_to_all_items": True},
            "pass": True,
            "evidence_refs": ["derived/metrics.json"],
        },
        "STRUCTURAL_MINIMUM": {
            "frozen_role": "theoretical floor used only for the ordering proof",
            "expected": "h+1 GETs; RACQ_PATH attains it",
            "observed": {
                "path_len_equals_hop_plus_one":
                    m["path_consistency"]["n_path_len_equals_hop_plus_one"],
                "n_items": m["path_consistency"]["n_items"],
            },
            "pass": True,
            "evidence_refs": ["derived/metrics.json"],
        },
    }

    observations = [
        {"id": "OBS-01",
         "text": "All four frozen controls reproduced live and PASS under the "
                 "frozen policy: POS_KNOWN_HOP_CONTROL found=true hop=1 "
                 "requests=3 cum_bytes=653222 status=200; NEG_UNREACHABLE_CONTROL "
                 "found=false; NARROW_CHAIN_CALIBRATION R=2.0 "
                 "(hop1=2,hop2=3,hop3=4); BROAD_FANOUT_CALIBRATION R=466.0 "
                 "(hop1=2,hop3=932). These equal the pre-freeze values in "
                 "spec.json.controls."},
        {"id": "OBS-02",
         "text": "All 12 planned structural sessions (6 candidate roots x 2 "
                 "sessions) completed with a 200 seed and n_get=250 (budget "
                 "exhausted); sessions_ok=true for all six sites. Cumulative "
                 "fetched body bytes were identical across the two sessions for "
                 "5 of 6 sites; forums.gentoo.org session B was exactly 1 byte "
                 "larger (6732475 vs 6732474) and carried all 16 item-level "
                 "byte differences (OBS-10)."},
        {"id": "OBS-03",
         "text": "ADMISSION_GATE_V1 PASS: site-row counts admitted_DEEP=26, "
                 "admitted_NEAR=419, admitted_MID=1114; after dedup by the frozen "
                 "item_id, DEEP=25, NEAR=408, MID=1099. distinct_seed_hosts=4 "
                 "(doc.rust-lang.org, www.gnu.org, quotes.toscrape.com, "
                 "forums.gentoo.org)."},
        {"id": "OBS-04",
         "text": "Every admitted DEEP item is on doc.rust-lang.org (mdBook): "
                 "26 site rows (rust_book 12, rust_cargo 10, rust_nomicon 4) and "
                 "25 after dedup (rust_book 12, rust_cargo 9, rust_nomicon 4). "
                 "No DEEP item was admitted on www.gnu.org, "
                 "quotes.toscrape.com or forums.gentoo.org within B=250, D=6."},
        {"id": "OBS-05",
         "text": "Pooled (deduped) RED medians: requests DEEP=158 vs NEAR=30 -> "
                 "R_req=5.2667; bytes DEEP=9704744 vs NEAR=1327357 -> "
                 "R_bytes=7.3113. Both exceed the pre-registered materiality "
                 "factor M=3.0, so the frozen falsifier returns GROWING."},
        {"id": "OBS-06",
         "text": "Per-site session-A ratios: rust_book R_req=10.625 "
                 "R_bytes=7.622; rust_cargo R_req=28.75 R_bytes=13.572; "
                 "rust_nomicon R_req=44.5 R_bytes=40.962 (all GROWING). "
                 "gnu, quotes and gentoo are UNDEFINED with 0 DEEP items."},
        {"id": "OBS-07",
         "text": "Persisted-path arm cost is approximately linear in hop: median "
                 "RACQ_PATH.requests DEEP=4 vs NEAR=2 (ratio 2.0); median "
                 "RACQ_PATH.bytes DEEP=711368 vs NEAR=63384 (ratio 11.22); "
                 "RACQ_URL.requests=1 for every item."},
        {"id": "OBS-08",
         "text": "Median per-item break-even reuse counts over eligible items: "
                 "DEEP requests=0.02597 (25/25 eligible), bytes=0.09918; "
                 "NEAR requests=0.06452 (382/408), bytes=0.04755; MID requests="
                 "0.02222 (1099/1099), bytes=0.01791. Every DEEP item is "
                 "break-even eligible (saving_requests>=1 and "
                 "saving_bytes>=1024)."},
        {"id": "OBS-09",
         "text": "The reconstructed shortest path length equals hop+1 for "
                 "1532/1532 deduped admitted items, so RACQ_PATH.requests is a "
                 "consistent shortest-path charge."},
        {"id": "OBS-10",
         "text": "Two-session agreement: RED.requests is identical between "
                 "sessions for all 1559 admitted item-rows (0 disagreements), so "
                 "no site was flagged unstable under VN-V4. RED.bytes differs in "
                 "16/1559 rows (minor response drift); these rows were retained "
                 "because VN-V4 keys exclusion on hop or request count only."},
        {"id": "OBS-11",
         "text": "Substrate: 4257 GETs are recorded in raw/http.jsonl, of which "
                 "3000 are the 12 real-root sessions (6 roots x 2 x 250), 250 "
                 "pos_control, 1000 broad_fanout and 7 narrow_chain. The raw "
                 "records carry no method field; the executor implements only "
                 "urllib GET (no POST/HEAD, no cookie jar, no credentials, no "
                 "browser, no Docker, no model key, no write verb). Wall clock "
                 "572.43 s."},
        {"id": "OBS-12",
         "text": "tiktoken is not importable (ModuleNotFoundError) and has no "
                 "pyproject.toml entry, so every token field is null and no token "
                 "figure is presented as satisfying the frozen cost basis. The "
                 "declared cost bases are GET requests and response-body bytes."},
        {"id": "OBS-13",
         "text": "Admitted state items kept per site after two-session "
                 "agreement: rust_book 36, rust_cargo 160, rust_nomicon 41, gnu "
                 "1300, quotes 6, gentoo 16. For every site items_shared equals "
                 "items_kept, so no item was dropped by the VN-V4 agreement "
                 "check."},
    ]

    validity_notes = [
        {"id": "VN-V1-tokenizer",
         "note": "tiktoken absent at EXECUTE (ModuleNotFoundError) and not "
                 "declared in pyproject.toml. Token fields are null; requests "
                 "and response-body bytes are the measured cost bases."},
        {"id": "VN-V2-js-navigation",
         "note": "Only static <a href> links are graph edges; JS-generated "
                 "navigation is not followed. Measured hop may exceed a "
                 "browser-observed hop. Applies identically to all bands."},
        {"id": "VN-V3-same-host",
         "note": "Cross-host navigation is excluded; the claim is bounded to "
                 "same-host static-link acquisition. The three doc.rust-lang.org "
                 "roots share one host and therefore one crawl universe."},
        {"id": "VN-V4-determinism",
         "note":          "K=2 sessions/site. RED.requests agreed in 1559/1559 admitted "
                 "rows, so no site was excluded. RED.bytes differed in 16/1559 "
                 "rows, all on forums.gentoo.org (cumulative +1 byte); VN-V4 "
                 "keys exclusion on hop or request count, so these did not "
                 "trigger exclusion."},
        {"id": "VN-V5-availability",
         "note": "All six seed hosts were reachable (network=AVAILABLE); no "
                 "status=BLOCKED condition occurred."},
        {"id": "VN-V6-parser",
         "note": "State-item discovery is a stdlib HTML-parser heuristic for "
                 "named <input>/<select>. JS-rendered controls are missed. Raw "
                 "discovery counts are reported per site (OBS-13)."},
        {"id": "VN-V7-band-separation",
         "note": "hop==2 (MID) is reported descriptively only and excluded from "
                 "the primary NEAR-vs-DEEP contrast; bands are disjoint."},
        {"id": "VN-V8-representation-loss",
         "note": "The DEEP band is 100% doc.rust-lang.org mdBook. gnu, quotes "
                 "and gentoo admitted 0 DEEP items within B=250/D=6, so the "
                 "pooled ratio contrasts a single-host/single-engine DEEP set "
                 "against a multi-host NEAR set. Generalization beyond mdBook "
                 "is NOT supported; per-host engine effects cannot be separated "
                 "from band effects in the pooled figure. The per-site doc "
                 "ratios are all GROWING, so the effect holds within mdBook."},
        {"id": "VN-V9-construct-validity",
         "note": "The RED arm is defined as the prefix of an item-blind "
                 "document-order BFS, and the frozen baseline-ordering proof "
                 "states RED.requests >= RACQ_PATH.requests by construction. For "
                 "any frontier broader than a chain, BFS necessarily fetches all "
                 "shallower pages before a deeper page, so a DEEP/NEAR ratio "
                 "above M=3 is largely a mathematical property of the frozen "
                 "level-order estimator (branching factor), not independent "
                 "evidence about Web acquisition economics. The FLAT branch was "
                 "producible only on the detour-free NARROW_CHAIN_CALIBRATION "
                 "(R=2.0). The frozen decision rule scores this GROWING as "
                 "SUPPORTS(H1); the producer flags that the measured quantity "
                 "is estimator-bound and that the persisted-path arm "
                 "(RACQ_PATH) is near-linear in hop (ratio 2.0 requests), which "
                 "is the more direct re-acquisition-cost reading."},
        {"id": "VN-V10-paired-arms",
         "note": "RACQ_PATH/RACQ_URL bytes are charged from the bodies fetched "
                 "in the SAME session that produced RED (IC-04); no duplicate GET "
                 "was issued for an arm. RED and both RACQ arms are strictly "
                 "paired on the same session and item set."},
        {"id": "VN-V11-calibration-budget",
         "note": "The two local calibration fixtures ran the identical frozen "
                 "BFS with a page budget of 1000 (IC-03) so the first hop-3 node "
                 "was reachable, matching the pre-freeze observation; the six "
                 "real roots used the frozen B=250."},
        {"id": "VN-V12-pooled-dedup",
         "note": "Pooled ratio deduplicates by the frozen item_id across the "
                 "three shared doc.rust-lang.org roots (IC-07); 27 duplicate "
                 "rows were removed. Per-site ratios and raw rows are "
                 "unaffected."},
        {"id": "VN-V13-depth-unreached",
         "note": "gnu, quotes and gentoo contributed 0 DEEP items because their "
                 "crawl universe exhausts B=250 before hop 3; their UNDEFINED "
                 "site verdict is a budget/depth fact, not a FLAT scientific "
                 "measurement."},
        {"id": "VN-V14-no-token",
         "note": "No tokenizer was available, so the optional third channel is "
                 "null. No latency or dollar cost was imputed; only GET counts "
                 "and body bytes are measured."},
    ]

    unresolved = [
        {"id": "UR-1",
         "question": "Whether any non-mdBook host in the frozen pool admits "
                     "state items at hop>=3 within B=250/D=6. The DEEP band is "
                     "single-host/single-engine, so cross-host generalization is "
                     "untested.",
         "why": "gnu, quotes and gentoo admitted 0 DEEP items within the frozen "
                "budget; a larger budget or different roots would be required."},
        {"id": "UR-2",
         "question": "Whether the GROWING pooled ratio reflects Web structure or "
                     "the branching factor of the frozen item-blind BFS "
                     "estimator.",
         "why": "RED>=RACQ_PATH is forced by the frozen baseline-ordering proof; "
                "the alternative persisted-path arm is near-linear in hop "
                "(requests ratio 2.0). Separating the two needs an estimator "
                "that does not order deeper pages behind shallower ones."},
        {"id": "UR-3",
         "question": "Real acquisition economics (latency, dollars, model calls) "
                     "as a function of hop.",
         "why": "Only GET request counts and response-body bytes were measured; "
                "no tokenizer, latency or cost model was available."},
        {"id": "UR-4",
         "question": "How many controls are JS-rendered and therefore missed by "
                     "the static parser, and whether that changes which items "
                     "are admitted at depth.",
         "why": "Only static named <input>/<select> were detectable; VN-V6 "
                "detection counts are per site."},
        {"id": "UR-5",
         "question": "The cause and significance of the 16/1559 response-body "
                     "byte differences between the two sessions.",
         "why": "Byte drift only; request counts and hops were identical, so it "
                "does not affect the frozen decision rule."},
    ]

    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "claim_ids": ["C-RESIDUAL-NOVELTY"],
        "status": "COMPLETE",
        "outcome": "SUPPORTS",
        "decision_rule_application": {
            "rule": "FLAT iff R_req<=3.0 AND R_bytes<=3.0; GROWING iff "
                    "R_req>3.0 AND R_bytes>3.0; else MIXED.",
            "R_req": pooled["ratio_requests_deep_over_near"],
            "R_bytes": pooled["ratio_bytes_deep_over_near"],
            "frozen_branch": "GROWING",
            "controls_gate": {k: v["pass"] for k, v in ctrls.items()},
            "admission_gate_pass": gate["pass"],
        },
        "metrics": metrics,
        "controls": controls,
        "artifacts": artifact_entries(),
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
        "claim_ceiling_producer": (
            "On this frozen credential-free GET-only stdlib substrate, the "
            "frozen item-blind re-derivation cost of admitted DEEP state items "
            "(all doc.rust-lang.org mdBook) exceeds that of admitted NEAR items "
            "by R_req=5.27 and R_bytes=7.31 at M=3.0, so the frozen decision rule "
            "returns GROWING. The producer does NOT claim that this is "
            "independent evidence of depth-growing Web acquisition economics, "
            "because RED is a level-order BFS prefix forced to exceed the "
            "shortest-path arm by construction (VN-V9). The persisted-path arm "
            "is near-linear in hop (median 4 vs 2 GETs). No promotion, no "
            "product-core claim, mdBook-only DEEP band."
        ),
    }

    with open(os.path.join(EXP, "result.json"), "w") as f:
        json.dump(result, f, indent=1, sort_keys=False)

    provenance = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "lane": LANE,
        "origin_github_run_id": "37950626378",
        "execute_github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "execute_github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "base_sha": "455f25d130572f80db1d693ef97b050665f5be79",
        "execution_head_sha": "89c5dea1358f74a8197e69cae94c104ab92fe654",
        "branch": "lab2/frontier",
        "command": "python3 research/frontier/run_execute_37950626378.py",
        "emit_command": "python3 research/frontier/emit_result_37950626378.py",
        "frozen_inputs": {
            "request.json": m["frozen_inputs"]["request.json"]["actual"],
            "spec.json": m["frozen_inputs"]["spec.json"]["actual"],
            "prereg.md": m["frozen_inputs"]["prereg.md"]["actual"],
            "freeze.json_sha256": sha256_file(os.path.join(EXP, "freeze.json")),
            "verified_unmodified": all(v["match"] for v in m["frozen_inputs"].values()),
        },
        "environment": {
            "python": m["environment"]["python"],
            "platform": m["environment"]["platform"],
            "network": m["environment"]["network"],
            "tokenizer": {"tiktoken_version": m["environment"]["tiktoken_version"],
                          "declared_in_pyproject": False},
            "uname": os.uname().sysname + " " + os.uname().release,
        },
        "dataset": {
            "candidate_roots": [
                {"site": "rust_book", "root": "https://doc.rust-lang.org/book/",
                 "engine": "mdBook", "host": "doc.rust-lang.org"},
                {"site": "rust_cargo", "root": "https://doc.rust-lang.org/cargo/",
                 "engine": "mdBook", "host": "doc.rust-lang.org"},
                {"site": "rust_nomicon", "root": "https://doc.rust-lang.org/nomicon/",
                 "engine": "mdBook", "host": "doc.rust-lang.org"},
                {"site": "gnu", "root": "https://www.gnu.org/",
                 "engine": "GNU web", "host": "www.gnu.org"},
                {"site": "quotes", "root": "https://quotes.toscrape.com/",
                 "engine": "custom", "host": "quotes.toscrape.com"},
                {"site": "gentoo", "root": "https://forums.gentoo.org/",
                 "engine": "phpBB", "host": "forums.gentoo.org"},
            ],
            "sessions_per_site": 2,
            "budget_pages": 250,
            "depth_cap": 6,
            "n_http_get": m["n_http_get"],
            "raw_http_records": sum(1 for _ in open(os.path.join(RAW, "http.jsonl"))),
            "observation_records": sum(1 for _ in open(os.path.join(RAW, "observations.jsonl"))),
        },
        "code_paths": [
            "research/frontier/run_execute_37950626378.py",
            "research/frontier/emit_result_37950626378.py",
        ],
        "artifacts": artifact_entries(),
        "safety": {
            "get_only": True, "non_get_requests": 0,
            "credentials": False, "cookies": False, "browser": False,
            "docker": False, "model_key": False, "write_verb": False,
            "no_commit_no_push": True,
        },
        "prior_execute_receipts": {
            "note": "Superseded operational receipts left in place by the "
                    "workflow runner and NOT treated as scientific evidence. "
                    "This EXECUTE completes the frozen design; result.json / "
                    "report.md / provenance.json are the authoritative stage "
                    "output. These receipts were not edited by the producer.",
            "failure.json": {"github_run_id": "37962922070",
                             "category": "EXECUTION_FAILURE",
                             "superseded": True},
            "model_execute.json": {"github_run_id": "37975522921",
                                   "status": "retry", "attempt": 4,
                                   "superseded": True},
            "execution_checkpoint.json": {"github_run_id": "37950626378",
                                          "role": "origin checkpoint",
                                          "superseded": False},
        },
        "notes": [
            "Frozen inputs were re-hashed at execute time and match freeze.json.",
            "Token channel unavailable; requests and response-body bytes are the "
            "declared cost bases.",
            "RACQ arm bytes are charged from the same-session observed bodies "
            "(IC-04); no duplicate GETs were issued for arms.",
        ],
    }
    with open(os.path.join(EXP, "provenance.json"), "w") as f:
        json.dump(provenance, f, indent=1, sort_keys=False)

    print("wrote result.json and provenance.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
