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


def validate_packet(exp_id: str, lane: str, source_commit: str, raw: dict[str, bytes], known_claims: set[str]):
    req = parse_json(raw["request.json"], "request")
    require(req, ["schema_version", "experiment_id", "lane", "request_id", "request_hash", "base_sha", "claim_registry_sha256"], "request")
    if req["schema_version"] != 1 or req["experiment_id"] != exp_id or req["lane"] != lane:
        raise ValueError("request identity mismatch")
    expected_request_hash = sha256(canonical({k: v for k, v in req.items() if k != "request_hash"}))
    if req["request_hash"] != expected_request_hash:
        raise ValueError("request_hash mismatch")

    base_claims = show(str(req.get("base_sha")), "research/claims/registry.json") if req.get("base_sha") else None
    if base_claims is not None and sha256(base_claims) != req["claim_registry_sha256"]:
        raise ValueError("claim_registry_sha256 does not match request base_sha")

    spec = parse_json(raw["spec.json"], "spec")
    require(spec, ["experiment_id", "lane", "claim_ids", "question"], "spec")
    if spec["experiment_id"] != exp_id or spec["lane"] != lane:
        raise ValueError("spec identity mismatch")
    if not isinstance(spec["claim_ids"], list) or any(c not in known_claims for c in spec["claim_ids"]):
        raise ValueError("spec contains invalid/unknown claim_ids")
    if not isinstance(spec["question"], str) or not spec["question"].strip():
        raise ValueError("spec question is empty")

    freeze = parse_json(raw["freeze.json"], "freeze")
    require(freeze, ["schema_version", "experiment_id", "hashes"], "freeze")
    if freeze["schema_version"] != 1 or freeze["experiment_id"] != exp_id or not isinstance(freeze["hashes"], dict):
        raise ValueError("freeze identity/shape mismatch")
    for name in ("request.json", "spec.json", "prereg.md"):
        if freeze["hashes"].get(name) != sha256(raw[name]):
            raise ValueError(f"freeze hash mismatch: {name}")

    if len(raw["prereg.md"].strip()) < 100 or len(raw["report.md"].strip()) < 20:
        raise ValueError("prereg/report is structurally empty")

    result = parse_json(raw["result.json"], "result")
    identity(result, exp_id, lane, "result")
    require(result, ["status", "outcome", "metrics", "controls", "artifacts", "observations", "validity_notes", "unresolved"], "result")
    if result["status"] not in RESULT_STATUSES or result["outcome"] not in RESULT_OUTCOMES:
        raise ValueError("result status/outcome invalid")
    if not isinstance(result["metrics"], dict) or not isinstance(result["controls"], dict):
        raise ValueError("result metrics/controls must be objects")

    provenance = parse_json(raw["provenance.json"], "provenance")
    if provenance.get("experiment_id", exp_id) != exp_id or provenance.get("lane", lane) != lane:
        raise ValueError("provenance identity mismatch")

    audit = parse_json(raw["audit.json"], "audit")
    identity(audit, exp_id, lane, "audit")
    require(audit, ["status", "producer_claim_supported", "required_fixes", "validity_findings", "baseline_findings", "recomputed_metrics", "claim_ceiling", "evidence_refs", "unresolved"], "audit")
    if audit["status"] not in AUDIT_STATUSES or not isinstance(audit["producer_claim_supported"], bool):
        raise ValueError("audit status/producer_claim_supported invalid")

    verdict = parse_json(raw["verdict.json"], "verdict")
    identity(verdict, exp_id, lane, "verdict")
    require(verdict, ["decision", "claim_updates", "product_action", "promote_to_product", "continue", "next_question", "reason", "evidence_refs"], "verdict")
    if not isinstance(verdict["claim_updates"], list) or not isinstance(verdict["promote_to_product"], bool) or not isinstance(verdict["continue"], bool):
        raise ValueError("verdict shape invalid")
    if verdict["promote_to_product"] and (lane != "product" or audit["status"] != "PASS"):
        raise ValueError("unauthorized product promotion verdict")
    for event in verdict["claim_updates"]:
        if not isinstance(event, dict):
            raise ValueError("claim update must be an object")
        if event.get("claim_id") not in known_claims or event.get("status") not in CLAIM_STATUSES or not event.get("reason"):
            raise ValueError("invalid claim update")
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
    carry = handoff.get("carry_forward")
    if not isinstance(carry, dict) or any(not isinstance(carry.get(k), list) for k in ("established", "rejected", "unknown", "do_not_assume")):
        raise ValueError("handoff carry_forward invalid")

    return req, spec, audit, verdict


def main():
    refs = [x.strip() for x in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/lab2").splitlines() if x.strip()]
    dest_root = ROOT / "codex/experiments"
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    claims_registry = json.loads((ROOT / "research/claims/registry.json").read_text())
    known_claims = {c["id"] for c in claims_registry["claims"]}
    gaps: list[dict] = []
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

            source_commit = git("log", "-1", "--format=%H", ref, "--", verdict_path, check=False).strip()
            if not source_commit:
                quarantine.append({"lane": lane, "experiment_id": exp_id, "ref": ref, "error": "cannot pin verdict commit"})
                continue

            try:
                raw: dict[str, bytes] = {}
                packet_hashes: dict[str, str] = {}
                for name in PACKET_FILES:
                    path = f"research/experiments/{exp_id}/{name}"
                    pinned = show(source_commit, path)
                    current = show(ref, path)
                    if pinned is None:
                        raise ValueError(f"packet file absent at verdict commit: {name}")
                    if current != pinned:
                        raise ValueError(f"post-finalization mutation detected: {name}")
                    raw[name] = pinned
                    packet_hashes[name] = sha256(pinned)

                req, spec, audit, verdict = validate_packet(exp_id, lane, source_commit, raw, known_claims)
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
                    claim_events.setdefault(event["claim_id"], []).append({
                        "experiment_id": exp_id,
                        "lane": lane,
                        "created_at": req.get("created_at"),
                        "decision": verdict["decision"],
                        "source_commit": source_commit,
                        **event,
                    })
            except Exception as exc:
                quarantine.append({"lane": lane, "experiment_id": exp_id, "ref": ref, "source_commit": source_commit, "error": str(exc)})

    # Stable chronological event ordering across lanes; ref iteration order is not
    # scientific chronology.
    entry_order = dict(sorted(entries.items(), key=experiment_sort_key))
    for claim_id, events in claim_events.items():
        events.sort(key=lambda e: ((e.get("created_at") or ""), e["experiment_id"]))
    latest_event = {claim_id: events[-1] for claim_id, events in claim_events.items() if events}

    codex_dir = ROOT / "codex"
    (codex_dir / "coverage_gaps.json").write_text(json.dumps(gaps, indent=2) + "\n")
    (codex_dir / "quarantine.json").write_text(json.dumps(quarantine, indent=2) + "\n")
    (codex_dir / "index.json").write_text(json.dumps({"schema_version": 2, "experiments": entry_order}, indent=2) + "\n")
    (codex_dir / "claim_state.json").write_text(json.dumps({"schema_version": 2, "events_by_claim": claim_events, "latest_event_by_claim": latest_event}, indent=2) + "\n")

    # SPIDER_CODEX.md is an index, not a second 7MB copy of every packet. Full
    # canonical evidence remains losslessly available under codex/experiments/.
    lines = [
        "# SPIDER CODEX — Research 2.0",
        "",
        "Pre-2.0 canonical memory remains frozen at `archive/spider-codex-ultimate:SPIDER_CODEX_ULTIME.md`.",
        "",
        "Canonical Research 2.0 evidence lives in `codex/experiments/<experiment_id>/`.",
        "Use `codex/index.json` and `codex/claim_state.json` to locate relevant packets; do not load all experiment bodies by default.",
        f"Validated experiments: **{len(entry_order)}**. Coverage gaps: **{len(gaps)}**. Quarantined packets: **{len(quarantine)}**.",
        "",
        "## Experiment index",
        "",
        "| Experiment | Lane | Audit | Verdict | Claims | Source commit |",
        "|---|---|---|---|---|---|",
    ]
    for exp_id, e in entry_order.items():
        lines.append(f"| {exp_id} | {e['lane']} | {e['audit_status']} | {e['decision']} | {', '.join(e['claim_ids'])} | `{e['source_commit'][:12]}` |")
    if latest_event:
        lines += ["", "## Latest recorded claim events", "", "These are chronological latest events, not an automatic truth ranking.", "", "| Claim | Status | Experiment | Lane |", "|---|---|---|---|"]
        for claim_id in sorted(latest_event):
            e = latest_event[claim_id]
            lines.append(f"| {claim_id} | {e['status']} | {e['experiment_id']} | {e['lane']} |")
    if gaps or quarantine:
        lines += ["", "## Integrity accounting", "", "See `codex/coverage_gaps.json` and `codex/quarantine.json`; incomplete or invalid finalized packets are never silently ingested."]
    (ROOT / "SPIDER_CODEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"SPIDER_CODEX_SYNC_OK experiments={len(entry_order)} gaps={len(gaps)} quarantine={len(quarantine)} refs={len(refs)}")


if __name__ == "__main__":
    main()
