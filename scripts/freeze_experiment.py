#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def under(path: str, root: str) -> bool:
    root = root.rstrip("/")
    return path == root or path.startswith(root + "/")


def prereg_is_substantive(path: Path, experiment_id: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    # The DESIGN agent may legitimately retain a human-readable status line such as
    # "DESIGN NOT YET FROZEN" until this deterministic freezer runs. Reject only the
    # untouched scaffold / trivially incomplete prereg, not that phrase by itself.
    scaffold = f"# {experiment_id} preregistration\n\nDESIGN NOT YET FROZEN.".strip()
    if text == scaffold:
        return False
    if len(text) < 500:
        return False
    if experiment_id not in text:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_id")
    args = ap.parse_args()
    exp = ROOT / "research/experiments" / args.experiment_id
    if (exp / "freeze.json").exists():
        print("SPIDER_ALREADY_FROZEN")
        return

    req = json.loads((exp / "request.json").read_text())
    spec = json.loads((exp / "spec.json").read_text())
    required = [
        "experiment_id", "lane", "claim_ids", "question", "hypothesis", "falsifier",
        "baselines", "positive_control", "null_control", "measurement_validity",
        "decision_rule", "product_consequence_positive", "product_consequence_negative",
        "estimated_cost", "expected_information_gain",
    ]
    missing = [k for k in required if k not in spec or spec[k] in ("", None, [])]
    if missing:
        raise SystemExit(f"cannot freeze incomplete spec: {missing}")
    if spec["experiment_id"] != args.experiment_id or spec["lane"] != req["lane"]:
        raise SystemExit("spec/request identity mismatch")

    mandate = req.get("director_mandate")
    if mandate is not None:
        if not isinstance(mandate, dict) or not isinstance(mandate.get("allocation"), dict):
            raise SystemExit("invalid director_mandate in request")
        allocation = mandate["allocation"]
        target_claim = allocation.get("claim_id")
        if target_claim not in spec["claim_ids"]:
            raise SystemExit(
                f"spec claim_ids {spec['claim_ids']} do not include Director target claim {target_claim}"
            )
        if allocation.get("action") not in {"CONTINUE", "PIVOT", "REOPEN"}:
            raise SystemExit("Director mandate action does not authorize a new experiment")
    if not prereg_is_substantive(exp / "prereg.md", args.experiment_id):
        raise SystemExit("preregistration remains scaffold or is structurally incomplete")

    if "build_required" not in spec or "freeze_artifacts" not in spec:
        raise SystemExit("spec must declare build_required and freeze_artifacts")
    build_required = spec["build_required"]
    freeze_artifacts = spec["freeze_artifacts"]
    if not isinstance(build_required, bool):
        raise SystemExit("spec.build_required must be boolean")
    if not isinstance(freeze_artifacts, list) or any(
        not isinstance(x, str) or not x.strip() for x in freeze_artifacts
    ):
        raise SystemExit("spec.freeze_artifacts must be a list of non-empty paths")
    if len(freeze_artifacts) != len(set(freeze_artifacts)):
        raise SystemExit("spec.freeze_artifacts contains duplicates")
    if build_required and not freeze_artifacts:
        raise SystemExit("build_required=true requires freeze_artifacts")

    receipt_path = exp / "build_receipt.json"
    if not receipt_path.exists():
        raise SystemExit("build_receipt.json missing; pre-freeze build receipt is mandatory")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("experiment_id") != args.experiment_id or receipt.get("lane") != req["lane"]:
        raise SystemExit("build receipt identity mismatch")
    receipt_artifacts = receipt.get("artifacts")
    if not isinstance(receipt_artifacts, dict):
        raise SystemExit("build receipt artifacts must be an object")

    lanes = json.loads((ROOT / "research/lanes/registry.json").read_text())
    roots = lanes["lanes"][req["lane"]].get("allowed_code_roots", [])
    exp_root = f"research/experiments/{args.experiment_id}"
    artifact_hashes = {}
    for rel in freeze_artifacts:
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts:
            raise SystemExit(f"unsafe freeze artifact path: {rel}")
        if not (under(rel, exp_root) or any(under(rel, root) for root in roots)):
            raise SystemExit(f"freeze artifact outside lane-authorized roots: {rel}")
        full = ROOT / rel
        if not full.is_file():
            raise SystemExit(f"freeze artifact missing: {rel}")
        digest = sha(full)
        if receipt_artifacts.get(rel) != digest:
            raise SystemExit(f"build receipt mismatch: {rel}")
        artifact_hashes[rel] = digest

    claims = json.loads((ROOT / "research/claims/registry.json").read_text())
    known = {c["id"] for c in claims["claims"]}
    unknown = set(spec["claim_ids"]) - known
    if unknown:
        raise SystemExit(f"unknown claim ids: {sorted(unknown)}")

    freeze = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "hashes": {
            "request.json": sha(exp / "request.json"),
            "spec.json": sha(exp / "spec.json"),
            "prereg.md": sha(exp / "prereg.md"),
            "build_receipt.json": sha(exp / "build_receipt.json"),
        },
        "artifact_commit": git_head(),
        "artifact_hashes": artifact_hashes,
    }
    (exp / "freeze.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
    print(f"SPIDER_FROZEN {args.experiment_id}")


if __name__ == "__main__":
    main()
