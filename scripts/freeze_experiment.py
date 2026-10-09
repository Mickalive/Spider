#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ELIGIBILITY_CHECKS = (
    "decision_rule_reachability",
    "measurement_prerequisites",
    "baseline_identifiability",
    "control_sensitivity",
    "treatment_liveness",
    "freeze_artifacts_bound",
)
PRODUCT_TREATMENT_CLAIMS = {
    "C-PARAM-INHERIT",
    "C-RESIDUAL-NOVELTY",
    "C-LLM-INHERIT",
    "C-PRODUCT-ECON",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_repo_file(rel: str) -> Path:
    if not isinstance(rel, str) or not rel.strip():
        raise SystemExit("freeze_artifact path must be a non-empty string")
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts:
        raise SystemExit(f"unsafe freeze_artifact path: {rel}")
    full = ROOT / p
    if not full.exists() or not full.is_file():
        raise SystemExit(f"freeze_artifact must be an existing file: {rel}")
    return full


def validate_v2_design(req: dict, spec: dict, exp: Path) -> dict[str, str]:
    eligibility = spec.get("freeze_eligibility")
    if not isinstance(eligibility, dict) or set(eligibility) != set(ELIGIBILITY_CHECKS):
        raise SystemExit("design contract v2 requires exact freeze_eligibility checks")

    for name in ELIGIBILITY_CHECKS:
        item = eligibility[name]
        if not isinstance(item, dict):
            raise SystemExit(f"freeze_eligibility.{name} must be an object")
        status = item.get("status")
        reason = item.get("reason")
        refs = item.get("evidence_refs")
        if status not in {"PASS", "NOT_APPLICABLE"}:
            raise SystemExit(f"freeze_eligibility.{name} is not freeze-eligible: {status}")
        if not isinstance(reason, str) or not reason.strip():
            raise SystemExit(f"freeze_eligibility.{name} requires a non-empty reason")
        if not isinstance(refs, list):
            raise SystemExit(f"freeze_eligibility.{name}.evidence_refs must be a list")

    review_path = exp / "design_review.json"
    if not review_path.exists():
        raise SystemExit("design contract v2 requires design_review.json")
    review = json.loads(review_path.read_text(encoding="utf-8"))
    if (
        review.get("schema_version") != 1
        or review.get("experiment_id") != req["experiment_id"]
        or review.get("lane") != req["lane"]
        or review.get("status") != "PASS"
    ):
        raise SystemExit("design review did not PASS for this experiment")

    if req["lane"] == "product" and PRODUCT_TREATMENT_CLAIMS.intersection(spec.get("claim_ids", [])):
        if eligibility["treatment_liveness"]["status"] != "PASS":
            raise SystemExit("Product inheritance/economics design requires treatment_liveness PASS before freeze")

    artifacts = spec.get("freeze_artifacts")
    if not isinstance(artifacts, list) or any(not isinstance(x, str) for x in artifacts):
        raise SystemExit("design contract v2 requires freeze_artifacts list")
    if len(artifacts) != len(set(artifacts)):
        raise SystemExit("freeze_artifacts contains duplicates")

    bound_status = eligibility["freeze_artifacts_bound"]["status"]
    if bound_status == "PASS" and not artifacts:
        raise SystemExit("freeze_artifacts_bound PASS requires at least one bound artifact")
    if bound_status == "NOT_APPLICABLE" and artifacts:
        raise SystemExit("freeze_artifacts must be empty when freeze_artifacts_bound is NOT_APPLICABLE")

    return {rel: sha(safe_repo_file(rel)) for rel in artifacts}


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

    claims = json.loads((ROOT / "research/claims/registry.json").read_text())
    known = {c["id"] for c in claims["claims"]}
    unknown = set(spec["claim_ids"]) - known
    if unknown:
        raise SystemExit(f"unknown claim ids: {sorted(unknown)}")

    design_contract_version = int(req.get("design_contract_version", 1))
    artifact_hashes: dict[str, str] = {}
    if design_contract_version >= 2:
        artifact_hashes = validate_v2_design(req, spec, exp)

    hashes = {
        "request.json": sha(exp / "request.json"),
        "spec.json": sha(exp / "spec.json"),
        "prereg.md": sha(exp / "prereg.md"),
    }
    if design_contract_version >= 2:
        hashes["design_review.json"] = sha(exp / "design_review.json")

    freeze = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "design_contract_version": design_contract_version,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "hashes": hashes,
        "artifact_hashes": artifact_hashes,
    }
    (exp / "freeze.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
    print(f"SPIDER_FROZEN {args.experiment_id}")


if __name__ == "__main__":
    main()
