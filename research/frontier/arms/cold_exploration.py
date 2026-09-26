"""Arm C of EXP-FRONTIER-36249071934: B-COLD-EXPLORATION (mandatory null control).

Frozen-design provenance: prereg.md section 6.3.

"Same substrate, same tasks, **empty registry**. Every span resolved as UNKNOWN
-> deopt to model oracle. No compilation, no caching, no inheritance. Cost = 1
unit per model call per span per episode."

The arm is deliberately kept as a *controlled* comparison against Arm B: it
performs the identical ``SpiderKernel.resolve()`` call on the identical
(identically empty) registry and receives the identical UNKNOWN resolution, so
the only difference between Arm B and Arm C after episode 1 is that Arm B holds
a populated-but-unusable registry. prereg.md 6.3 calls this "the absolute
floor"; because the frozen cost model charges a resolve step to any arm that
performs one, Arm C's realised cost is reported as measured and the inherited
arm is not credited for a mechanism it cannot execute.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..substrate_deterministic_http import DeterministicHTTPSubstrate, KeepAliveClient, sha256_hex, span_signature
from ..taskplan import EXPECTED_CODES, Step
from .common import Ledger, ModelOracle, SpanRecord, ensure_src_on_path, observable_state_sig

ensure_src_on_path()

from spider.kernel import SpiderKernel  # noqa: E402
from spider.models import ResolutionStatus  # noqa: E402
from spider.registry import MechanismRegistry  # noqa: E402


@dataclass
class ColdExploration:
    arm: str = "B-COLD-EXPLORATION"
    oracle: ModelOracle = field(default_factory=ModelOracle)
    ledger: Ledger = field(default_factory=Ledger)
    registry_dir: str = field(default_factory=lambda: tempfile.mkdtemp(prefix="spider-cold-"))
    kernel_config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.registry_path = Path(self.registry_dir) / "registry.jsonl"
        self.registry = MechanismRegistry(self.registry_path)
        # Inheritance ablation: the registry is emptied and stays empty.
        self.registry.replace([])
        self.kernel = SpiderKernel(self.registry, min_confidence=0.8)
        self.kernel_config = {
            "kernel_class": type(self.kernel).__name__,
            "min_confidence": self.kernel.min_confidence,
            "registry_path": str(self.registry_path),
            "registry_size": len(self.registry.all()),
        }

    def run_episode(
        self,
        substrate: DeterministicHTTPSubstrate,
        client: KeepAliveClient,
        episode: int,
        plan: list[Step],
        records: list[SpanRecord],
    ) -> dict[str, Any]:
        substrate.reset()
        store_snapshot: dict[str, Any] = dict(substrate.store)
        last_request: tuple[str, str] | None = None
        model_calls = 0
        code_ok = True

        for index, expected in enumerate(plan):
            state_sig = observable_state_sig(store_snapshot, last_request)
            context = {
                "store_size": len(store_snapshot),
                "store_keys": sorted(store_snapshot.keys()),
                "last_method": last_request[0] if last_request else None,
                "last_path": last_request[1] if last_request else None,
            }
            self.ledger.charge("machinery")
            self.ledger.bump("resolve_calls")
            resolution = self.kernel.resolve(expected.role, context)
            self.ledger.bump(f"resolve_{resolution.status.value.lower()}")

            if resolution.status is ResolutionStatus.EXECUTABLE and resolution.bound_action is not None:
                decision_path = "INHERITED_EXECUTABLE"
                step = Step(
                    expected.role,
                    resolution.bound_action["method"],
                    resolution.bound_action["path"],
                    resolution.bound_action.get("body"),
                    EXPECTED_CODES[step.role],
                )
            else:
                decision_path = f"DEOPT_TO_MODEL_{resolution.status.value}"
                step = self.oracle.decide(plan, index, store_snapshot)
                self.ledger.charge("model")
                model_calls += 1

            code, raw, sent = client.request(step.method, step.path, step.body)
            self.ledger.charge("execution")
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
                    },
                )
            )

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


def _decl_headers(body: Any) -> dict[str, str]:
    """Declared request headers, matching what the substrate client sends.

    prereg.md 12 normalizes headers inside the span signature; the volatile
    transport headers are excluded inside ``normalize_headers``.
    """
    return {"Content-Type": "application/json"} if body is not None else {}
