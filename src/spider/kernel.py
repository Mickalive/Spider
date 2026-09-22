from __future__ import annotations

import collections
import hashlib
import json
import logging
import re
import time
from typing import Any

import requests as _requests

from .models import FreshnessResult, Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry

logger = logging.getLogger(__name__)

# Thresholds from validated C-FRESHNESS architecture
THRESHOLD_BEHAVIORAL = 0.25
THRESHOLD_STRUCTURAL = 0.15  # informational only, no gating

# Window size for structural fingerprint history (for entropy computation)
STRUCTURAL_WINDOW = 20


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _matches(required: dict[str, Any], actual: dict[str, Any]) -> bool:
    return all(actual.get(k) == v for k, v in required.items())


def _template_slots(value: Any) -> set[str]:
    if isinstance(value, str):
        return set(_PARAMETER.findall(value))
    if isinstance(value, dict):
        out: set[str] = set()
        for item in value.values():
            out.update(_template_slots(item))
        return out
    if isinstance(value, list):
        out: set[str] = set()
        for item in value:
            out.update(_template_slots(item))
        return out
    return set()


def _bind(value: Any, params: dict[str, Any]) -> Any:
    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            return params[full.group(1)]

        def replace(match: re.Match[str]) -> str:
            return str(params[match.group(1)])

        return _PARAMETER.sub(replace, value)
    if isinstance(value, dict):
        return {k: _bind(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [_bind(v, params) for v in value]
    return value


class SpiderKernel:
    """Conservative first execution-inheritance kernel.

    This kernel is deliberately not a browser agent. It stores and resolves validated mechanisms.
    It abstains when applicability is not demonstrated.
    """

    def __init__(self, registry: MechanismRegistry, min_confidence: float = 0.8):
        self.registry = registry
        self.min_confidence = min_confidence
        self._freshness_enabled = True
        # Track structural fingerprints per mechanism for entropy computation
        self._structural_history: dict[str, collections.deque] = {}

    @property
    def freshness_enabled(self) -> bool:
        return self._freshness_enabled

    @freshness_enabled.setter
    def freshness_enabled(self, value: bool) -> None:
        self._freshness_enabled = value

    def observe(self, observation: Observation) -> str:
        raw = json.dumps({
            "intent": observation.intent,
            "state": observation.state,
            "action": observation.action,
            "next_state": observation.next_state,
            "success": observation.success,
            "provenance": observation.provenance,
        }, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(raw).hexdigest()

    def freshness_check(self, mechanism: Mechanism, context: dict[str, Any]) -> FreshnessResult:
        """Probe mechanism endpoint via HTTP and compute freshness scores.

        Uses HTTP requests to extract:
        - behavioral_score: token validation failure, session state change, auth boundary shift
        - structural_score: ETag/Cache-Control header cardinality, request_id entropy

        Returns FreshnessResult(behavioral_score, structural_score, is_stale, latency_ms)
        """
        probe_url = mechanism.freshness.get("probe_url")
        if not probe_url:
            # No probe URL configured — return fresh (no signal)
            return FreshnessResult(
                behavioral_score=0.0,
                structural_score=0,
                is_stale=False,
                latency_ms=0.0,
            )

        # Determine token to use based on auth_scope
        auth_scope = mechanism.auth_scope or ""
        token = context.get("auth_token", "")

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        start = time.perf_counter()
        try:
            resp = _requests.get(probe_url, headers=headers, timeout=5.0)
            latency_ms = (time.perf_counter() - start) * 1000

            # --- Behavioral signal ---
            # HTTP status anomaly: 401/403 for valid credentials = drift
            status_code = resp.status_code
            behavioral_score = 0.0

            if status_code in (401, 403):
                # If we sent a token and got auth failure, that's behavioral drift
                if token:
                    behavioral_score = 0.8  # strong signal
                else:
                    behavioral_score = 0.0  # expected: no token = no auth
            elif status_code >= 500:
                behavioral_score = 0.3  # server error is moderate signal
            else:
                # Successful response — check response body for auth signals
                try:
                    body = resp.json()
                    if body.get("error") and "expired" in str(body.get("error", "")).lower():
                        behavioral_score = 0.9
                    elif body.get("error") and "invalid" in str(body.get("error", "")).lower():
                        behavioral_score = 0.7
                except (ValueError, KeyError):
                    pass

            # --- Structural signal ---
            # Headers-only: ETag, Cache-Control, X-Request-Id
            # Structural score = cardinality of unique fingerprints across recent probes
            resp_headers = dict(resp.headers)

            etag = resp_headers.get("ETag", "")
            cache_control = resp_headers.get("Cache-Control", "")
            request_id = resp_headers.get("X-Request-Id", "")

            # Compute structural fingerprint (hash of header values)
            fp_raw = f"{etag}|{cache_control}"
            fingerprint = hashlib.md5(fp_raw.encode()).hexdigest()

            # Track in history for this mechanism
            mech_id = mechanism.mechanism_id
            if mech_id not in self._structural_history:
                self._structural_history[mech_id] = collections.deque(maxlen=STRUCTURAL_WINDOW)
            self._structural_history[mech_id].append(fingerprint)

            # Structural score = number of unique fingerprints in recent window
            history = list(self._structural_history[mech_id])
            structural_score = len(set(history))

            is_stale = behavioral_score > THRESHOLD_BEHAVIORAL

            return FreshnessResult(
                behavioral_score=behavioral_score,
                structural_score=structural_score,
                is_stale=is_stale,
                latency_ms=latency_ms,
                status_code=status_code,
                headers=resp_headers,
            )

        except _requests.RequestException as e:
            latency_ms = (time.perf_counter() - start) * 1000
            # Connection failure is a moderate behavioral signal
            return FreshnessResult(
                behavioral_score=0.5,
                structural_score=0,
                is_stale=True,
                latency_ms=latency_ms,
                status_code=None,
                headers=None,
            )

    def distill(self, observation: Observation) -> Mechanism | None:
        """Create only a literal candidate mechanism.

        Generalization/parameter induction is intentionally not guessed here; Research 2.0 must
        earn that capability through C-PARAM-INHERIT and related gates.
        """
        if not observation.success:
            return None
        oid = self.observe(observation)[:16]
        return Mechanism(
            mechanism_id=f"obs-{oid}",
            intent=observation.intent,
            preconditions=dict(observation.state),
            action_template=dict(observation.action),
            postconditions=dict(observation.next_state),
            evidence=[oid],
            confidence=0.5,
        )

    def resolve(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None) -> Resolution:
        params = params or {}
        candidates = []
        for m in self.registry.all():
            if m.invalidated or m.intent != intent:
                continue
            if not _matches(m.preconditions, context):
                continue
            if not _matches(m.applicability_guards, context):
                continue

            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            if any(slot not in params for slot in required_slots):
                continue
            candidates.append(m)

        if not candidates:
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        # Freshness gate: check each candidate before confidence thresholding
        if self._freshness_enabled:
            for m in candidates:
                freshness_result = self.freshness_check(m, context)
                if freshness_result.is_stale:
                    return Resolution(
                        ResolutionStatus.STALE,
                        m.mechanism_id,
                        f"freshness gate: auth/session drift detected (behavioral_score={freshness_result.behavioral_score:.3f})",
                        confidence=m.confidence,
                    )
                if freshness_result.structural_score > THRESHOLD_STRUCTURAL:
                    logger.warning(
                        "Structural drift detected for %s: score=%d (informational, not gating)",
                        m.mechanism_id,
                        freshness_result.structural_score,
                    )

        candidates.sort(key=lambda m: m.confidence, reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            return Resolution(ResolutionStatus.EXPLORE, best.mechanism_id, "candidate exists but confidence is below execution threshold", confidence=best.confidence)

        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=best.confidence,
        )

    def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        return _matches(mechanism.postconditions, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)
