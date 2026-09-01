#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "# SPIDER CODEX — RESEARCH 2.0 CONTINUATION"
REQUIRED = [
    "request.json",
    "spec.json",
    "prereg.md",
    "freeze.json",
    "result.json",
    "report.md",
    "provenance.json",
    "audit.json",
    "verdict.json",
    "handoff.json",
]
EMBED = [
    "spec.json",
    "prereg.md",
    "result.json",
    "report.md",
    "provenance.json",
    "audit.json",
    "verdict.json",
    "handoff.json",
]


def git(*args: str, check: bool = True) -> bytes:
    p = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode:
        raise RuntimeError(p.stderr.decode("utf-8", errors="replace"))
    return p.stdout


def text(*args: str, check: bool = True) -> str:
    return git(*args, check=check).decode("utf-8", errors="replace")


def show(ref: str, path: str) -> bytes | None:
    p = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else None


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fenced(label: str, raw: bytes) -> list[str]:
    body = raw.decode("utf-8", errors="replace").rstrip()
    return [f"### {label}", "", "~~~~text", body, "~~~~", ""]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive-dir", required=True)
    args = ap.parse_args()
    archive = Path(args.archive_dir).resolve()
    codex = archive / "SPIDER_CODEX_ULTIME.md"
    if not codex.exists():
        raise SystemExit("canonical SPIDER_CODEX_ULTIME.md missing")

    current = codex.read_text(encoding="utf-8", errors="replace")
    # Pre-2.0 bytes are immutable. Every sync regenerates only the continuation.
    base = current.split("\n" + MARKER, 1)[0].rstrip()

    refs = [
        r.strip()
        for r in text("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/lab2").splitlines()
        if r.strip()
    ]
    experiments: dict[str, dict] = {}
    coverage_gaps: list[dict] = []
    collisions: list[dict] = []

    for ref in refs:
        lane = ref.split("origin/lab2/", 1)[-1]
        paths = text("ls-tree", "-r", "--name-only", ref, "research/experiments", check=False).splitlines()
        ids = sorted({
            p.split("/")[2]
            for p in paths
            if p.startswith("research/experiments/") and len(p.split("/")) >= 4
        })
        for exp_id in ids:
            prefix = f"research/experiments/{exp_id}"
            verdict_raw = show(ref, f"{prefix}/verdict.json")
            if verdict_raw is None:
                continue
            packet = {name: show(ref, f"{prefix}/{name}") for name in REQUIRED}
            missing = [name for name, raw in packet.items() if raw is None]
            if missing:
                coverage_gaps.append({"experiment_id": exp_id, "lane": lane, "source_ref": ref, "missing": missing})
                continue

            hashes = {name: sha256(packet[name]) for name in REQUIRED}  # type: ignore[arg-type]
            fingerprint = sha256(json.dumps(hashes, sort_keys=True).encode())
            if exp_id in experiments:
                if experiments[exp_id]["fingerprint"] != fingerprint:
                    collisions.append({"experiment_id": exp_id, "first_ref": experiments[exp_id]["source_ref"], "second_ref": ref})
                continue

            request = json.loads(packet["request.json"])  # type: ignore[arg-type]
            spec = json.loads(packet["spec.json"])  # type: ignore[arg-type]
            audit = json.loads(packet["audit.json"])  # type: ignore[arg-type]
            verdict = json.loads(packet["verdict.json"])  # type: ignore[arg-type]
            freeze = json.loads(packet["freeze.json"])  # type: ignore[arg-type]
            experiments[exp_id] = {
                "experiment_id": exp_id,
                "lane": lane,
                "source_ref": ref,
                "fingerprint": fingerprint,
                "packet": packet,
                "meta": {
                    "request_id": request.get("request_id"),
                    "request_hash": request.get("request_hash"),
                    "created_at": request.get("created_at"),
                    "origin_github_run_id": request.get("origin_github_run_id"),
                    "base_sha": request.get("base_sha"),
                    "claim_ids": spec.get("claim_ids", []),
                    "question": spec.get("question"),
                    "freeze_hashes": freeze.get("hashes", {}),
                    "audit_status": audit.get("status"),
                    "decision": verdict.get("decision"),
                    "promote_to_product": verdict.get("promote_to_product", False),
                    "content_hashes": hashes,
                },
            }

    if collisions:
        raise SystemExit("experiment-id collision with divergent content: " + json.dumps(collisions, sort_keys=True))

    ordered = sorted(experiments.values(), key=lambda e: (str(e["meta"].get("created_at") or ""), e["experiment_id"]))
    lines = [
        base,
        "",
        MARKER,
        "",
        "This continuation is generated from complete finalized Research 2.0 packets on `lab2/*` branches.",
        "The pre-2.0 corpus above this marker is preserved byte-for-byte by the generator.",
        "Each Research 2.0 experiment appears exactly once. GitHub Actions logs and duplicate packet copies are not embedded.",
        "",
        f"Finalized Research 2.0 experiments: **{len(ordered)}**.",
        f"Finalized-packet coverage gaps: **{len(coverage_gaps)}**.",
        "",
        "## R2 normalized experiment index",
        "",
        "| Experiment | Lane | Audit | Verdict | Claims |",
        "|---|---|---|---|---|",
    ]
    for e in ordered:
        m = e["meta"]
        lines.append(f"| {e['experiment_id']} | {e['lane']} | {m.get('audit_status')} | {m.get('decision')} | {', '.join(m.get('claim_ids') or [])} |")

    lines += ["", "## R2 normalized experiment records", ""]
    for e in ordered:
        m = e["meta"]
        packet = e["packet"]
        lines += [f"## {e['experiment_id']}", "", "### normalized_metadata", "", "~~~~json", json.dumps(m, indent=2, sort_keys=True), "~~~~", ""]
        for name in EMBED:
            lines += fenced(name, packet[name])  # type: ignore[arg-type]

    if coverage_gaps:
        lines += ["## R2 coverage gaps", "", "A finalized verdict exists for these experiments, but the canonical packet is incomplete. They are explicitly reported rather than silently omitted.", "", "~~~~json", json.dumps(coverage_gaps, indent=2, sort_keys=True), "~~~~", ""]

    new_text = "\n".join(lines).rstrip() + "\n"
    codex.write_text(new_text, encoding="utf-8")
    print(f"SPIDER_CODEX_ULTIMATE_SYNC_OK experiments={len(ordered)} gaps={len(coverage_gaps)} refs={len(refs)} bytes={len(new_text.encode())}")


if __name__ == "__main__":
    main()
