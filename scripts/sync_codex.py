#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from research2_contract import (
    AUDIT_STATUSES,
    CLAIM_STATUSES,
    DIRECTOR_CLAIM_STATUSES,
    LANES,
    PACKET_FILES,
    RESULT_OUTCOMES,
    RESULT_STATUSES,
)

ROOT = Path(__file__).resolve().parents[1]


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check).stdout


def show(ref, path):
    p = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return None if p.returncode else p.stdout


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def parse_json(raw: bytes, label: str):
    try:
        obj = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise ValueError(f"{label} invalid JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise ValueError(f"{label} must be a JSON object")
    return obj


def require(obj, keys, label):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValueError(f"{label} missing keys: {missing}")


def require_list(obj, key: str, label: str):
    if not isinstance(obj.get(key), list):
        raise ValueError(f"{label} {key} must be a list")


def identity(obj, exp_id: str, lane: str, label: str):
    require(obj, ["schema_version", "experiment_id", "lane"], label)
    if obj["schema_version"] != 1 or obj["experiment_id"] != exp_id or obj["lane"] != lane:
        raise ValueError(f"{label} identity mismatch")


def experiment_sort_key(item):
    exp_id, entry = item
    created = entry.get("created_at") or ""
    m = re.search(r"-(\d+)$", exp_id)
    run_id = int(m.group(1)) if m else 0
    return (created, run_id, exp_id)


def validate_packet(
    exp_id: str,
    lane: str,
    source_commit: str,
    raw: dict[str, bytes],
    known_claims: set[str],
    lane_claims: set[str],
):
    req = parse_json(raw["request.json"], "request")
    require(req, ["schema_version", "experiment_id", "lane", "request_id", "request_hash", "base_sha", "claim_registry_sha256"], "request")
    if req["schema_version"] != 1 or req["experiment_id"] != exp_id or req["lane"] != lane:
        raise ValueError("request identity mismatch")
    expected_request_hash = sha256(canonical({k: v for k, v in req.items() if k != "request_hash"}))
    if req["request_hash"] != expected_request_hash:
        raise ValueError("request_hash mismatch")

    base_sha = str(req.get("base_sha") or "")
    if not base_sha or base_sha == "unknown":
        raise ValueError("request base_sha is not immutable")
    base_claims = show(base_sha, "research/claims/registry.json")
    if base_claims is None:
        raise ValueError("request base_sha cannot be resolved for claim registry validation")
    if sha256(base_claims) != req["claim_registry_sha256"]:
        raise ValueError("claim_registry_sha256 does not match request base_sha")

    parent = req.get("parent_handoff")
    if parent is not None:
        if not isinstance(parent, dict):
            raise ValueError("parent_handoff must be an object")
        require(parent, ["experiment_id", "path", "sha256"], "parent_handoff")
        parent_raw = show(source_commit, parent["path"])
        if parent_raw is None:
            raise ValueError("parent_handoff path is not present at child finalization commit")
        if sha256(parent_raw) != parent["sha256"]:
            raise ValueError("parent_handoff sha256 mismatch")
        parent_obj = parse_json(parent_raw, "parent_handoff artifact")
        if parent_obj.get("experiment_id") != parent["experiment_id"]:
            raise ValueError("parent_handoff experiment_id mismatch")

    spec = parse_json(raw["spec.json"], "spec")
    require(spec, ["experiment_id", "lane", "claim_ids", "question"], "spec")
    if spec["experiment_id"] != exp_id or spec["lane"] != lane:
        raise ValueError("spec identity mismatch")
    if not isinstance(spec["claim_ids"], list) or not spec["claim_ids"] or any(c not in known_claims for c in spec["claim_ids"]):
        raise ValueError("spec contains empty/invalid/unknown claim_ids")
    if not isinstance(spec["question"], str) or not spec["question"].strip():
        raise ValueError("spec question is empty")

    freeze = parse_json(raw["freeze.json"], "freeze")
    require(freeze, ["schema_version", "experiment_id", "hashes"], "freeze")
    if freeze["schema_version"] != 1 or freeze["experiment_id"] != exp_id or not isinstance(freeze["hashes"], dict):
        raise ValueError("freeze identity/shape mismatch")
    for name, expected in freeze["hashes"].items():
        if name not in raw:
            raise ValueError(f"frozen packet file missing from canonical raw set: {name}")
        if expected != sha256(raw[name]):
            raise ValueError(f"freeze hash mismatch: {name}")

    artifact_hashes = freeze.get("artifact_hashes", {})
    if not isinstance(artifact_hashes, dict):
        raise ValueError("freeze artifact_hashes must be an object")
    for rel, expected in artifact_hashes.items():
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts:
            raise ValueError(f"unsafe frozen artifact path: {rel}")
        pinned_artifact = show(source_commit, rel)
        if pinned_artifact is None:
            raise ValueError(f"frozen artifact absent at finalization commit: {rel}")
        if sha256(pinned_artifact) != expected:
            raise ValueError(f"frozen artifact hash mismatch: {rel}")

    if len(raw["prereg.md"].strip()) < 100 or len(raw["report.md"].strip()) < 20:
        raise ValueError("prereg/report is structurally empty")

    result = parse_json(raw["result.json"], "result")
    identity(result, exp_id, lane, "result")
    require(result, ["status", "outcome", "metrics", "controls", "artifacts", "observations", "validity_notes", "unresolved"], "result")
    if result["status"] not in RESULT_STATUSES or result["outcome"] not in RESULT_OUTCOMES:
        raise ValueError("result status/outcome invalid")
    if not isinstance(result["metrics"], dict) or not isinstance(result["controls"], dict):
        raise ValueError("result metrics/controls must be objects")
    for key in ("artifacts", "observations", "validity_notes", "unresolved"):
        require_list(result, key, "result")

    provenance = parse_json(raw["provenance.json"], "provenance")
    if provenance.get("experiment_id", exp_id) != exp_id or provenance.get("lane", lane) != lane:
        raise ValueError("provenance identity mismatch")

    audit = parse_json(raw["audit.json"], "audit")
    identity(audit, exp_id, lane, "audit")
    require(audit, ["status", "producer_claim_supported", "required_fixes", "validity_findings", "baseline_findings", "recomputed_metrics", "claim_ceiling", "evidence_refs", "unresolved"], "audit")
    if audit["status"] not in AUDIT_STATUSES or not isinstance(audit["producer_claim_supported"], bool):
        raise ValueError("audit status/producer_claim_supported invalid")
    if not isinstance(audit["recomputed_metrics"], dict):
        raise ValueError("audit recomputed_metrics must be an object")
    if not isinstance(audit["claim_ceiling"], str) or not audit["claim_ceiling"].strip():
        raise ValueError("audit claim_ceiling must be non-empty")
    for key in ("required_fixes", "validity_findings", "baseline_findings", "evidence_refs", "unresolved"):
        require_list(audit, key, "audit")

    verdict = parse_json(raw["verdict.json"], "verdict")
    identity(verdict, exp_id, lane, "verdict")
    require(verdict, ["decision", "claim_updates", "product_action", "promote_to_product", "continue", "next_question", "reason", "evidence_refs"], "verdict")
    if not isinstance(verdict["claim_updates"], list) or not isinstance(verdict["promote_to_product"], bool) or not isinstance(verdict["continue"], bool):
        raise ValueError("verdict shape invalid")
    if verdict["next_question"] is not None and not isinstance(verdict["next_question"], str):
        raise ValueError("verdict next_question must be string or null")
    if not isinstance(verdict["reason"], str) or not verdict["reason"].strip():
        raise ValueError("verdict reason must be non-empty")
    require_list(verdict, "evidence_refs", "verdict")
    if verdict["promote_to_product"] and (lane != "product" or audit["status"] != "PASS"):
        raise ValueError("unauthorized product promotion verdict")
    design_contract_version = int(req.get("design_contract_version", 1))
    frozen_claims = set(spec["claim_ids"])
    for event in verdict["claim_updates"]:
        if not isinstance(event, dict):
            raise ValueError("claim update must be an object")
        if event.get("claim_id") not in known_claims or event.get("status") not in DIRECTOR_CLAIM_STATUSES or not event.get("reason"):
            raise ValueError("invalid Director claim update")
        if design_contract_version >= 2:
            if event.get("claim_id") not in frozen_claims:
                raise ValueError(f"v2 claim update outside frozen spec.claim_ids: {event.get('claim_id')}")
            if event.get("claim_id") not in lane_claims:
                raise ValueError(f"v2 claim update outside lane charter: {event.get('claim_id')}")
            if event.get("status") in {"MEASUREMENT_INVALID", "BLOCKED"}:
                raise ValueError("v2 packet/operational status may not replace epistemic claim status")
        if event.get("status") == "VALIDATED" and audit["status"] != "PASS":
            raise ValueError("VALIDATED claim without PASS audit")
        if event.get("status") == "PRODUCT_CORE" and (lane != "product" or audit["status"] != "PASS" or not verdict["promote_to_product"]):
            raise ValueError("PRODUCT_CORE without audited Product promotion gate")

    handoff = parse_json(raw["handoff.json"], "handoff")
    identity(handoff, exp_id, lane, "handoff")
    require(handoff, ["target_lane", "next_question", "why_next", "carry_forward", "dependencies", "evidence_refs", "recommended_action"], "handoff")
    if handoff["target_lane"] is not None and handoff["target_lane"] not in LANES:
        raise ValueError("invalid handoff target_lane")
    if handoff["next_question"] != verdict["next_question"]:
        raise ValueError("handoff/verdict next_question mismatch")
    if not isinstance(handoff["why_next"], str) or not isinstance(handoff["recommended_action"], str):
        raise ValueError("handoff text fields must be strings")
    carry = handoff.get("carry_forward")
    if not isinstance(carry, dict) or any(not isinstance(carry.get(k), list) for k in ("established", "rejected", "unknown", "do_not_assume")):
        raise ValueError("handoff carry_forward invalid")
    for key in ("dependencies", "evidence_refs"):
        require_list(handoff, key, "handoff")

    return req, spec, audit, verdict


def main():
    refs = [x.strip() for x in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/lab2").splitlines() if x.strip()]
    dest_root = ROOT / "codex/experiments"
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    claims_registry = json.loads((ROOT / "research/claims/registry.json").read_text())
    known_claims = {c["id"] for c in claims_registry["claims"]}
    registry_status = {c["id"]: c["status"] for c in claims_registry["claims"]}
    lanes_registry = json.loads((ROOT / "research/lanes/registry.json").read_text())["lanes"]

    # SPIDER has one cumulative scientific history, not two Codices.
    # The original archive blob is materialized losslessly on main.
    legacy_index = json.loads((ROOT / "codex/legacy_artifact_index.json").read_text(encoding="utf-8"))
    legacy_brief = json.loads((ROOT / "codex/legacy_brief.json").read_text(encoding="utf-8"))
    historical_source = "codex/sources/0000-historical-evidence.md"
    historical_raw = (ROOT / historical_source).read_bytes()
    historical_blob = hashlib.sha1(
        b"blob " + str(len(historical_raw)).encode() + b"\0" + historical_raw
    ).hexdigest()
    if historical_blob != legacy_index["source"]["blob_sha"] or historical_blob != legacy_brief["source"]["blob_sha"]:
        raise ValueError("historical source hash mismatch")
    if len(legacy_index["artifacts"]) != legacy_index["count"] or legacy_index["count"] != legacy_brief["source"]["artifact_count"]:
        raise ValueError("historical artifact coverage mismatch")
    historical_manifest = {
        "period": "historical research (before autonomous Research 2.0)",
        "source_path": historical_source,
        "source_blob_sha": historical_blob,
        "original_archive": "archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md",
        "artifact_count": len(legacy_index["artifacts"]),
        "counting_rule": "unique source artifacts, NOT independent experiment count",
        "artifacts": legacy_index["artifacts"],
    }
    historical_claim_map = {
        "C-MEAS-VALID": ["P2-WP003", "P2-AUTOMATION"],
        "C-PARAM-INHERIT": ["P2-BLIND-COMPOSITION", "P2-REPLAY-COST", "P2-MIND2WEB"],
        "C-FRESHNESS": ["P2-AUTOMATION"],
        "C-DELTA-REPAIR": ["P2-AUTOMATION"],
        "C-RESIDUAL-NOVELTY": ["P2-REPLAY-COST", "P2-BLIND-COMPOSITION", "P2-MIND2WEB"],
        "C-LLM-INHERIT": ["P2-REPLAY-COST", "P2-BLIND-COMPOSITION", "P2-MIND2WEB"],
        "C-PRODUCT-ECON": ["P2-REPLAY-COST"],
        "C-CROSSSITE": ["P2-WP002B", "P2-WP003", "P2-WP003B"],
        "C-SEMANTIC-RESOLVE": ["P2-MIND2WEB", "P2-BLIND-COMPOSITION"],
        "C-WEB-DYNAMICS": ["P2-WP002B", "P2-WP003", "P2-WP003B"],
    }
    historic_precedents = {
        claim_id: [
            {key: finding[key] for key in ("key", "source", "status", "fact", "guard")}
            for finding in legacy_brief["findings"]
            if finding["key"] in historical_claim_map.get(claim_id, [])
        ]
        for claim_id in sorted(known_claims)
    }
    gaps: list[dict] = []
    scope_warnings: list[dict] = []
    quarantine: list[dict] = []
    entries: dict[str, dict] = {}
    claim_events: dict[str, list] = {}

    for ref in refs:
        lane = ref.split("origin/lab2/", 1)[-1]
        if lane not in LANES:
            quarantine.append({"lane": lane, "ref": ref, "error": "unknown lab2 lane ref"})
            continue
        ref_head = git("rev-parse", ref).strip()
        paths = git("ls-tree", "-r", "--name-only", ref, "research/experiments", check=False).splitlines()
        exp_ids = sorted({p.split("/")[2] for p in paths if p.startswith("research/experiments/") and len(p.split("/")) >= 4})
        for exp_id in exp_ids:
            verdict_path = f"research/experiments/{exp_id}/verdict.json"
            if show(ref, verdict_path) is None:
                continue
            missing = [name for name in PACKET_FILES if show(ref, f"research/experiments/{exp_id}/{name}") is None]
            if missing:
                gaps.append({"lane": lane, "experiment_id": exp_id, "ref": ref, "missing": missing})
                continue

            # Canonical finalization point is the commit that first ADDED verdict.json.
            # The previous "latest commit touching verdict" rule could bless a later
            # mutation as if it were the original Director decision.
            source_commit = git("log", "--diff-filter=A", "-1", "--format=%H", ref, "--", verdict_path, check=False).strip()
            if not source_commit:
                quarantine.append({"lane": lane, "experiment_id": exp_id, "ref": ref, "error": "cannot pin original verdict creation commit"})
                continue

            try:
                raw: dict[str, bytes] = {}
                packet_hashes: dict[str, str] = {}
                for name in PACKET_FILES:
                    path = f"research/experiments/{exp_id}/{name}"
                    pinned = show(source_commit, path)
                    current = show(ref, path)
                    if pinned is None:
                        raise ValueError(f"packet file absent at verdict creation commit: {name}")
                    if current != pinned:
                        raise ValueError(f"post-finalization mutation detected: {name}")
                    raw[name] = pinned
                    packet_hashes[name] = sha256(pinned)

                # Design-contract v2 adds an independently produced design review
                # to the immutable freeze set without making it mandatory for legacy packets.
                req_preview = parse_json(raw["request.json"], "request preview")
                if int(req_preview.get("design_contract_version", 1)) >= 2:
                    review_path = f"research/experiments/{exp_id}/design_review.json"
                    pinned_review = show(source_commit, review_path)
                    current_review = show(ref, review_path)
                    if pinned_review is None:
                        raise ValueError("v2 packet missing design_review.json at finalization")
                    if current_review != pinned_review:
                        raise ValueError("post-finalization mutation detected: design_review.json")
                    raw["design_review.json"] = pinned_review
                    packet_hashes["design_review.json"] = sha256(pinned_review)

                lane_claims = set(lanes_registry[lane].get("priority_claims", []))
                req, spec, audit, verdict = validate_packet(
                    exp_id, lane, source_commit, raw, known_claims, lane_claims
                )
                if exp_id in entries:
                    raise ValueError(f"duplicate experiment id already ingested from {entries[exp_id]['source_ref']}")

                out = dest_root / exp_id
                out.mkdir(parents=True, exist_ok=True)
                for name, content in raw.items():
                    (out / name).write_bytes(content)

                entry = {
                    "lane": lane,
                    "request_id": req["request_id"],
                    "created_at": req.get("created_at"),
                    "claim_ids": spec["claim_ids"],
                    "question": spec["question"],
                    "audit_status": audit["status"],
                    "decision": verdict["decision"],
                    "promote_to_product": verdict["promote_to_product"],
                    "source_ref": ref,
                    "source_ref_head": ref_head,
                    "source_commit": source_commit,
                    "hashes": packet_hashes,
                }
                entries[exp_id] = entry
                for event in verdict.get("claim_updates", []):
                    claim_id = event["claim_id"]
                    in_frozen_scope = claim_id in set(spec["claim_ids"])
                    lane_eligible = claim_id in set(lanes_registry[lane].get("priority_claims", []))
                    enriched = {
                        "experiment_id": exp_id,
                        "lane": lane,
                        "created_at": req.get("created_at"),
                        "decision": verdict["decision"],
                        "next_question": verdict.get("next_question"),
                        "source_commit": source_commit,
                        "in_frozen_scope": in_frozen_scope,
                        "lane_eligible": lane_eligible,
                        **event,
                    }
                    claim_events.setdefault(claim_id, []).append(enriched)
                    if not in_frozen_scope or not lane_eligible:
                        scope_warnings.append({
                            "claim_id": claim_id,
                            "experiment_id": exp_id,
                            "lane": lane,
                            "in_frozen_scope": in_frozen_scope,
                            "lane_eligible": lane_eligible,
                            "status": event.get("status"),
                            "reason": "historical claim update preserved but excluded from effective claim state",
                        })
            except Exception as exc:
                quarantine.append({"lane": lane, "experiment_id": exp_id, "ref": ref, "source_commit": source_commit, "error": str(exc)})

    # Stable chronological event ordering across lanes; ref iteration order is not
    # scientific chronology.
    entry_order = dict(sorted(entries.items(), key=experiment_sort_key))
    for claim_id, events in claim_events.items():
        events.sort(key=lambda e: ((e.get("created_at") or ""), e["experiment_id"]))
    latest_event = {claim_id: events[-1] for claim_id, events in claim_events.items() if events}

    # Effective claim state is epistemic, not merely chronological. Preserve all
    # raw events, but do not let packet/operational statuses or historical
    # out-of-scope updates erase accepted scientific state.
    non_epistemic = {"MEASUREMENT_INVALID", "BLOCKED"}
    effective_event: dict[str, dict] = {}
    for claim_id in sorted(known_claims):
        effective: dict = {
            "claim_id": claim_id,
            "status": registry_status[claim_id],
            "reason": "base status from research/claims/registry.json; no later admissible epistemic event",
            "source": "registry",
        }
        for event in claim_events.get(claim_id, []):
            if not event.get("in_frozen_scope", False) or not event.get("lane_eligible", False):
                continue
            if event.get("status") in non_epistemic:
                continue
            effective = dict(event)
            effective["source"] = "canonical_event"
        effective_event[claim_id] = effective

    codex_dir = ROOT / "codex"
    (codex_dir / "coverage_gaps.json").write_text(json.dumps(gaps, indent=2) + "\n")
    (codex_dir / "quarantine.json").write_text(json.dumps(quarantine, indent=2) + "\n")
    (codex_dir / "claim_scope_warnings.json").write_text(json.dumps(scope_warnings, indent=2) + "\n")
    (codex_dir / "index.json").write_text(json.dumps({"schema_version": 3, "historical": historical_manifest, "experiments": entry_order}, indent=2) + "\n")
    (codex_dir / "claim_state.json").write_text(json.dumps({
        "schema_version": 4,
        "historical_precedents_by_claim": historic_precedents,
        "events_by_claim": claim_events,
        "latest_event_by_claim": latest_event,
        "effective_event_by_claim": effective_event,
    }, indent=2) + "\n")

    # SPIDER_CODEX.md is an index, not a second multi-megabyte copy of every packet.
    # Full canonical evidence remains losslessly available under codex/experiments/.
    lines = [
        "# SPIDER CODEX — cumulative scientific record",
        "",
        "One SPIDER program, one continuous scientific history; Research 2.0 extends earlier experiments.",
        "Original evidence is kept byte-for-byte on main at codex/sources/0000-historical-evidence.md.",
        "The single codex/index.json combines original source artifact locations and subsequent experiment packets.",
        "The same codex/claim_state.json records bounded historical precedents and subsequent audited claim events.",
        "",
        "## Earlier research — preserved source, indexed into the same Codex",
        "",
        f"Unique historical evidence artifacts: **{len(legacy_index['artifacts'])}** (source documents, NOT independent experiments).",
        f"Immutable original Git blob: {historical_blob}.",
        "Search codex/index.json.historical.artifacts by original path, lane and line interval.",
        "Historical PASS tags are hints, not automatically validated scientific claims.",
        "",
        "| Historical evidence | Original reference | Bounded finding |",
        "|---|---|---|",
    ]
    for finding in legacy_brief["findings"]:
        fact = finding["fact"].replace("|", "/").replace("\n", " ")
        lines.append(f"| {finding['key']} | {finding['source']} | {fact} |")
    lines += [
        "",
        "## Subsequent finalized experiments — Research 2.0",
        "",
        "Canonical subsequent evidence is in codex/experiments/<experiment_id>/.",
        "Use the same codex/index.json and codex/claim_state.json across both periods.",
        f"Finalized subsequent packets: **{len(entry_order)}**. Coverage gaps: **{len(gaps)}**. Quarantined packets: **{len(quarantine)}**.",
        "",
        "## Experiment index",
        "| Experiment | Lane | Audit | Verdict | Claims | Source commit |",
        "|---|---|---|---|---|---|",
    ]
    for exp_id, e in entry_order.items():
        lines.append(f"| {exp_id} | {e['lane']} | {e['audit_status']} | {e['decision']} | {', '.join(e['claim_ids'])} | `{e['source_commit'][:12]}` |")
    if effective_event:
        lines += ["", "## Effective claim state", "", "This table is the state used for research direction. Packet-level MEASUREMENT_INVALID/BLOCKED events and historical out-of-scope claim updates remain in claim_state history but do not erase accepted epistemic state.", "", "| Claim | Status | Source |", "|---|---|---|"]
        for claim_id in sorted(effective_event):
            e = effective_event[claim_id]
            source = e.get("experiment_id") or e.get("source", "registry")
            lines.append(f"| {claim_id} | {e['status']} | {source} |")
    if latest_event:
        lines += ["", "## Latest raw claim events", "", "Chronological event stream for auditability; not an automatic truth ranking.", "", "| Claim | Status | Experiment | Lane |", "|---|---|---|---|"]
        for claim_id in sorted(latest_event):
            e = latest_event[claim_id]
            lines.append(f"| {claim_id} | {e['status']} | {e['experiment_id']} | {e['lane']} |")
    if gaps or quarantine:
        lines += ["", "## Integrity accounting", "", "See `codex/coverage_gaps.json` and `codex/quarantine.json`; incomplete or invalid finalized packets are never silently ingested."]
    (ROOT / "SPIDER_CODEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"SPIDER_CODEX_SYNC_OK experiments={len(entry_order)} gaps={len(gaps)} quarantine={len(quarantine)} scope_warnings={len(scope_warnings)} refs={len(refs)}")


if __name__ == "__main__":
    main()
