"""Arm B of EXP-FRONTIER-36249071934: B-INHERITED-SPIDER (incumbent shipped kernel).

Frozen-design provenance: prereg.md section 6.2.

This arm imports the ACTUAL shipped kernel ``src/spider/kernel.py`` and the
ACTUAL ``src/spider/registry.py`` with no modification whatsoever. There is no
local re-implementation, no confidence override, no registry surgery:

  * episode 1 runs against an empty registry (every span resolves UNKNOWN);
  * after episode 1 every successful observation is passed through
    ``SpiderKernel.distill()`` into a real on-disk ``MechanismRegistry``;
  * the registry is static thereafter (prereg.md 6.2: "Registry is static
    thereafter (no online learning)");
  * every later span goes through ``SpiderKernel.resolve()`` with the shipped
    default ``min_confidence=0.8`` and ``SpiderKernel.verify()``;
  * cost accounting: 1 unit per resolve+bind+verify+freshness check per span,
    plus 1 unit per span execution, plus 1 unit per deopt-to-model.

The actual counts of resolve / bind / verify / freshness calls are recorded so
the frozen per-span machinery charge can be audited against what the kernel
actually did rather than against what it claims to do.
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..substrate_deterministic_http import DeterministicHTTPSubstrate, KeepAliveClient, sha256_hex, span_signature
from ..taskplan import EXPECTED_CODES, Step
from .common import Ledger, ModelOracle, SpanRecord, ensure_src_on_path, observable_state_sig

ensure_src_on_path()

from spider.kernel import SpiderKernel  # noqa: E402
from spider.models import Observation, ResolutionStatus  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402

STATUS_COUNTS: dict[str, int] = {s.value: 0 for s in ResolutionStatus}


@dataclass
class InheritedSpider:
    arm: str = "B-INHERITED-SPIDER"
    oracle: ModelOracle = field(default_factory=ModelOracle)
    ledger: Ledger = field(default_factory=Ledger)
    registry_dir: str = field(default_factory=lambda: tempfile.mkdtemp(prefix="spider-inherit-"))
    distill_calls: int = 0
    mechanisms_distilled: int = 0
    min_confidence: float = 0.8
    kernel_config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.registry_path = Path(self.registry_dir) / "registry.jsonl"
        self.registry = MechanismRegistry(self.registry_path)
        self.kernel = SpiderKernel(self.registry, min_confidence=self.min_confidence)
        self.kernel_config = {
            "kernel_class": type(self.kernel).__name__,
            "kernel_module": type(self.kernel).__module__,
            "min_confidence": self.kernel.min_confidence,
            "registry_path": str(self.registry_path),
        }

    # -- episode 1: collect observations, then distil exactly as prereg 6.2 --
    def run_episode(
        self,
        substrate: DeterministicHTTPSubstrate,
        client: KeepAliveClient,
        episode: int,
        plan: list[Step],
        records: list[SpanRecord],
        collect: list[Observation] | None = None,
    ) -> dict[str, Any]:
        substrate.reset()
        store_snapshot: dict[str, Any] = dict(substrate.store)
        last_request: tuple[str, str] | None = None
        model_calls = 0
        code_ok = True
        resolutions: list[str] = []

        for index, expected in enumerate(plan):
            state_sig = observable_state_sig(store_snapshot, last_request)
            context = self._context(store_snapshot, last_request)
            self.ledger.charge("machinery")
            self.ledger.bump("resolve_calls")
            resolution = self.kernel.resolve(expected.role, context)
            resolutions.append(resolution.status.value)
            STATUS_COUNTS[resolution.status.value] = STATUS_COUNTS.get(resolution.status.value, 0) + 1
            self.ledger.bump(f"resolve_{resolution.status.value.lower()}")

            if resolution.status is ResolutionStatus.EXECUTABLE and resolution.bound_action is not None:
                decision_path = "INHERITED_EXECUTABLE"
                step = Step(
                    expected.role,
                    resolution.bound_action["method"],
                    resolution.bound_action["path"],
                    resolution.bound_action.get("body"),
                    EXPECTED_CODES[expected.role],
                )
                self.ledger.bump("bind_calls")
                mechanism_id = resolution.mechanism_id
            else:
                decision_path = f"DEOPT_TO_MODEL_{resolution.status.value}"
                step = self.oracle.decide(plan, index, store_snapshot)
                self.ledger.charge("model")
                model_calls += 1
                mechanism_id = None

            code, raw, sent = client.request(step.method, step.path, step.body)
            self.ledger.charge("execution")

            post_state = self._context(dict(substrate.store), (step.method, step.path))
            verified = None
            if mechanism_id is not None:
                self.ledger.bump("bind_calls")
                self.ledger.bump("verify_calls")
                self.ledger.bump("freshness_checks")
                verified = self.kernel.verify(mechanism_id, post_state)

            ok = code == EXPECTED_CODES[step.role]
            code_ok = code_ok and ok

            records.append(
                SpanRecord(
                    arm=self.arm,
                    episode=episode,
                    index=index,
                    role=step.role,
                    work_item=index // 6,
                    method=step.method,
                    path=step.path,
                    body=step.body,
                    declared_headers={"content-type": "application/json"} if step.body is not None else {},
                    request_headers_sent=sent,
                    response_code=code,
                    response_body_hash=sha256_hex(raw),
                    signature=span_signature(step.method, step.path, _decl_headers(step.body), step.body, code, raw),
                    state_sig=state_sig,
                    decision_path=decision_path,
                    detail={
                        "expected_code": EXPECTED_CODES[step.role],
                        "code_ok": ok,
                        "resolution_status": resolution.status.value,
                        "resolution_reason": resolution.reason,
                        "resolution_mechanism_id": resolution.mechanism_id,
                        "resolution_confidence": resolution.confidence,
                        "verified": verified,
                    },
                )
            )

            if collect is not None:
                self.distill_calls += 1
                mechanism = self.kernel.distill(
                    Observation(
                        intent=step.role,
                        state=context,
                        action={"method": step.method, "path": step.path, "body": step.body},
                        next_state=post_state,
                        success=ok,
                        provenance={"arm": self.arm, "episode": episode, "index": index},
                    )
                )
                if mechanism is not None:
                    self.registry.upsert(mechanism)
                    self.mechanisms_distilled += 1
                self.ledger.bump("distill_calls")

            store_snapshot = dict(substrate.store)
            last_request = (step.method, step.path)

        return {
            "episode": episode,
            "spans": len(plan),
            "model_calls": model_calls,
            "compile_events": 0,
            "final_store_empty": len(substrate.store) == 0,
            "code_ok": code_ok,
            "registry_size": len(self.registry.all()),
        }

    @staticmethod
    def _context(store: dict[str, Any], last_request: tuple[str, str] | None) -> dict[str, Any]:
        """Preconditions/postconditions the kernel matches on: observable world state."""
        return {
            "store_size": len(store),
            "store_keys": sorted(store.keys()),
            "last_method": last_request[0] if last_request else None,
            "last_path": last_request[1] if last_request else None,
        }

    def registry_dump(self) -> dict[str, Any]:
        items = self.registry.all()
        return {
            "count": len(items),
            "confidences": sorted({m.confidence for m in items}),
            "min_confidence_gate": self.kernel.min_confidence,
            "any_above_gate": any(m.confidence >= self.kernel.min_confidence for m in items),
            "parameter_slots_nonempty": sum(1 for m in items if m.parameter_slots),
            "freshness_nonempty": sum(1 for m in items if m.freshness),
            "applicability_guards_nonempty": sum(1 for m in items if m.applicability_guards),
            "verification_rule_nonempty": sum(1 for m in items if m.verification_rule),
            "repair_scope_nonempty": sum(1 for m in items if m.repair_scope),
            "failure_boundary_nonempty": sum(1 for m in items if m.failure_boundary),
            "sample": [json.loads(json.dumps(m.as_dict(), sort_keys=True)) for m in items[:2]],
        }


def _decl_headers(body: Any) -> dict[str, str]:
    """Declared request headers, matching what the substrate client sends.

    prereg.md 12 normalizes headers inside the span signature; the volatile
    transport headers are excluded inside ``normalize_headers``.
    """
    return {"Content-Type": "application/json"} if body is not None else {}
