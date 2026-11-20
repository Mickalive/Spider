"""Small opt-in bridge between an existing Web agent and vetted Spider mechanisms.

This module does NOT induce mechanisms, drive a browser, or promote research claims.
The caller supplies an agent fallback, a narrowly authorized executor, and a
post-action observation. An uncertain attempted execution is never retried blindly.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .kernel import SpiderKernel
from .models import ResolutionStatus


@dataclass(frozen=True)
class BridgeResult:
    path: str  # "agent", "inheritance", or "unknown"
    value: Any = None
    reason: str = ""
    mechanism_id: str | None = None


class AgentBridge:
    """Use inheritance only when preconditions, safety and verification are explicit."""

    def __init__(self, kernel: SpiderKernel):
        self.kernel = kernel

    def run(
        self,
        intent: str,
        context: dict[str, Any],
        params: dict[str, Any],
        *,
        fallback: Callable[[], Any],
        execute: Callable[[dict[str, Any]], Any],
        read_state: Callable[[], dict[str, Any]],
        authorize: Callable[[dict[str, Any]], bool],
    ) -> BridgeResult:
        resolution = self.kernel.resolve(intent, context, params)
        if resolution.status != ResolutionStatus.EXECUTABLE:
            return BridgeResult("agent", fallback(), resolution.reason)

        mechanism = next(
            (m for m in self.kernel.registry.all() if m.mechanism_id == resolution.mechanism_id),
            None,
        )
        if mechanism is None or mechanism.invalidated:
            return BridgeResult("agent", fallback(), "mechanism disappeared before execution")
        if mechanism.auth_scope is not None and context.get("auth_scope") != mechanism.auth_scope:
            return BridgeResult("agent", fallback(), "auth scope not verified")
        if mechanism.freshness:
            return BridgeResult("agent", fallback(), "freshness conditions not implemented")
        if not mechanism.postconditions:
            return BridgeResult("agent", fallback(), "no verifiable postcondition")
        if mechanism.verification_rule.get("replay_safe") is not True:
            return BridgeResult("agent", fallback(), "replay safety not attested")

        action = resolution.bound_action
        if not isinstance(action, dict) or not authorize(action):
            # Authorization denial must not be bypassed via the fallback agent.
            return BridgeResult("unknown", reason="execution not authorized", mechanism_id=mechanism.mechanism_id)

        try:
            value = execute(action)
            observed_state = read_state()
        except Exception as error:
            # An action may already have changed external state. No automatic retry.
            return BridgeResult("unknown", reason=f"attempted action unverified ({type(error).__name__})", mechanism_id=mechanism.mechanism_id)

        if not self.kernel.verify(mechanism.mechanism_id, observed_state):
            return BridgeResult("unknown", reason="postcondition not verified; no blind retry", mechanism_id=mechanism.mechanism_id)

        return BridgeResult("inheritance", value, "postcondition verified", mechanism.mechanism_id)
