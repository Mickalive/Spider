"""Arm CROSS_EPISODE_COMPILED_BINDING of EXP-FRONTIER-36287182510 (new treatment arm).

Frozen-design provenance: ``spec.json`` ``measurement_validity.arms`` and
``prereg.md`` sections 5, 6.2, 11 and 14.

The scientific question this arm exists to answer
------------------------------------------------
prereg.md section 1 asks whether a cross-episode compiled arm whose cache key
*includes the induced binding* closes what a within-episode scratchpad leaves, so
that the minimum persistent state required to close the residual is quantified
rather than asserted.

Mechanism, exactly as preregistered
-----------------------------------
  * A cross-episode compiled replay cache. The cache key is

        (observable_state_sig, binding_key)

    where ``binding_key`` is the capability handle the arm currently holds, i.e.
    the value it induced by reading ``capability_handle`` out of one of its own
    earlier response bodies (prereg.md 6.2: "the capability handle value induced
    from a prior response in the same or earlier episode"). ``binding_key`` is
    ``None`` when the arm holds no handle.
  * A span is compiled after 2 witnesses that map the same key to the same
    action, and the compiled spans are RETAINED ACROSS EPISODES (the cache and
    the induced binding both live on the instance, which the runner creates once
    per novelty rate and reuses for all 50 episodes).
  * On a cache hit the arm replays the bound action *including* the binding key,
    so a class-(iii) span can only ever be replayed with the handle that the key
    itself names. A state key that maps to two different actions under two
    different handles is therefore two keys, not one, which is exactly the defect
    the parent packet measured in B-NO-MEMORY-DETERMINISTIC.
  * The conflict guard is inherited verbatim from ``deopt_ratchet``: a key that
    ever maps to two different actions is marked ambiguous and is never served
    from the cache again. It is retained because it is the parent's mechanism
    under characterisation, and because removing it would let this arm silently
    replay wrong actions for reasons unrelated to the binding key.
  * On a miss the arm deopts to the model oracle, which is the parent's oracle:
    ``ModelOracle.decide(plan, index, store)`` returns the declared plan action
    as bound at execution time.

The identity question this arm makes measurable
-----------------------------------------------
Because the handle is a pure function of (MINT_SALT, episode counter) it is
EPISODE-VARYING, so a cache key that contains its VALUE cannot be shared across
episodes. This arm therefore measures, rather than assumes, the price of soundness:
soundness here is bought with a model call on every span whose correct action
depends on a fresh binding, and the arm's cache fragments at every mint.

Cost model (prereg.md sections 6.2 and 11)
-----------------------------------------
Parent-identical ledger plus the declared machinery term:
  * 1 compile unit per unique ``(state_sig, binding_key)`` compiled,
  * 1 machinery unit per span served from the cache (resolve+bind+verify),
  * 1 execution unit per span,
  * 0 model units for spans served from the cache; 1 model unit per deopt.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from ..substrate_deterministic_http import DeterministicHTTPSubstrate, KeepAliveClient, sha256_hex, span_signature
from ..taskplan import EXPECTED_CODES, Step
from .common import Ledger, ModelOracle, SpanRecord, observable_state_sig

#: prereg.md 6.2: "compiles a span after 2 witnesses". Inherited from the parent
#: arm (``deopt_ratchet.WITNESS_THRESHOLD``); identical value on purpose.
WITNESS_THRESHOLD = 2

CacheKey = tuple[str, str | None]


@dataclass
class BindingCacheEntry:
    state_sig: str
    binding_key: str | None
    request: dict[str, Any]
    witnesses: int = 0
    ambiguous: bool = False
    first_witnessed_episode: int = -1
    compiled_at_episode: int = -1
    bound_handle: str | None = None


@dataclass
class CrossEpisodeCompiledBinding:
    """Compiled replay cache keyed on (observable state, induced binding)."""

    arm: str = "CROSS_EPISODE_COMPILED_BINDING"
    oracle: ModelOracle = field(default_factory=ModelOracle)
    ledger: Ledger = field(default_factory=Ledger)
    #: PERSISTENT ACROSS EPISODES -- the whole point of the arm.
    cache: dict[CacheKey, BindingCacheEntry] = field(default_factory=dict)
    #: PERSISTENT ACROSS EPISODES: the induced binding store.
    induced_bindings: dict[str, str] = field(default_factory=dict)
    current_binding: str | None = None
    # -- operational counters (never read by the decision procedure) --------
    conflicts_detected: int = 0
    deopt_compile_misses: int = 0
    deopt_no_entry: int = 0
    compiled_replays: int = 0
    bound_replays: int = 0

    # -- ratchet internals, inherited verbatim except for the key -----------
    def _witness(self, key: CacheKey, step: Step, episode: int) -> None:
        request = {"method": step.method, "path": step.path, "body": step.body}
        entry = self.cache.get(key)
        if entry is None:
            self.cache[key] = BindingCacheEntry(
                state_sig=key[0],
                binding_key=key[1],
                request=request,
                witnesses=1,
                first_witnessed_episode=episode,
                bound_handle=key[1] if ("?t=" in step.path or "?view=" in step.path) else None,
            )
            return
        if entry.request != request:
            if not entry.ambiguous:
                self.conflicts_detected += 1
                self.ledger.bump("cache_key_conflicts")
            entry.ambiguous = True
            return
        entry.witnesses += 1
        if not entry.ambiguous and entry.witnesses >= WITNESS_THRESHOLD and entry.compiled_at_episode < 0:
            entry.compiled_at_episode = episode
            self.ledger.charge("compile")
            self.ledger.bump("spans_compiled")

    def _lookup(self, key: CacheKey) -> BindingCacheEntry | None:
        entry = self.cache.get(key)
        if entry is None:
            self.deopt_no_entry += 1
            return None
        if entry.ambiguous or entry.compiled_at_episode < 0:
            self.deopt_compile_misses += 1
            return None
        return entry

    # -- one episode --------------------------------------------------------
    def run_episode(
        self,
        substrate: DeterministicHTTPSubstrate,
        client: KeepAliveClient,
        episode: int,
        plan: Any,
        records: list[SpanRecord],
    ) -> dict[str, Any]:
        substrate.reset()  # fresh world + advanced episode counter, as the reference arm does
        store_snapshot: dict[str, Any] = dict(substrate.store)
        last_request: tuple[str, str] | None = None
        code_ok = True
        compiled_hits = 0
        model_calls_this_episode = 0
        store_empty_at_start = len(substrate.store) == 0
        n = len(plan)

        for index in range(n):
            state_sig = observable_state_sig(store_snapshot, last_request)
            # prereg.md 6.2: "binding_key is the capability handle value (or
            # None for non-gated spans)". Gatedness is read from the plan step
            # the arm is already REQUIRED to materialise (the parent arm contract
            # is ``for index, expected in enumerate(plan)``: it consumes the step
            # for the expected role and expected status code). The arm reads
            # only the BOOLEAN "is this step capability-gated" -- the presence of
            # a ?t= / ?view= parameter -- and never the handle value inside it.
            # The handle it keys on is the one it induced from its own response
            # body, so a stale handle can never be replayed for a fresh episode:
            # the fresh handle is a different key.
            expected = plan[index]
            gated = ("?t=" in expected.path) or ("?view=" in expected.path)
            binding_key = self.current_binding if gated else None
            key: CacheKey = (state_sig, binding_key)
            entry = self._lookup(key)
            if entry is not None:
                # Cross-episode resolution: resolve + bind + verify.
                self.ledger.charge("machinery")
                self.ledger.bump("machinery_resolve_bind_verify")
                step = Step(
                    expected.role,
                    entry.request["method"],
                    entry.request["path"],
                    entry.request["body"],
                    EXPECTED_CODES[expected.role],
                )
                decision_path = "COMPILED_REPLAY_BOUND"
                compiled_hits += 1
                self.compiled_replays += 1
                if "?t=" in step.path or "?view=" in step.path:
                    self.ledger.bump("compiled_replays_carrying_a_bound_handle")
                    self.bound_replays += 1
            else:
                decision_path = "DEOPT_TO_MODEL"
                step = self.oracle.decide(plan, index, store_snapshot)
                self.ledger.charge("model")
                model_calls_this_episode += 1

            self._witness(key, step, episode)

            code, raw, sent = client.request(step.method, step.path, step.body)
            self.ledger.charge("execution")
            ok = code == EXPECTED_CODES[step.role]
            code_ok = code_ok and ok

            # The arm induces its binding from its OWN response body.
            observed_handle: str | None = None
            observed_rid: str | None = None
            try:
                parsed = json.loads(raw.decode("utf-8"))
            except Exception:  # pragma: no cover - every substrate response is JSON
                parsed = None
            if isinstance(parsed, dict):
                observed_handle = parsed.get("capability_handle")
                observed_rid = parsed.get("rid")
            if observed_handle:
                self.induced_bindings[str(observed_rid)] = observed_handle
                self.current_binding = observed_handle
                self.ledger.bump("handles_induced_from_response_bodies")

            cached = self.cache.get(key)
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
                        "gated_span": gated,
                        "binding_key_in_cache_key": binding_key,
                        "cache_key": f"{state_sig}|{binding_key}",
                        "witnesses_after": cached.witnesses if cached else 0,
                        "compiled": bool(cached and cached.compiled_at_episode >= 0),
                        "cache_ambiguous": bool(cached and cached.ambiguous),
                        "replayed_handle": entry.bound_handle if entry is not None else None,
                        "handle_induced_this_span": observed_handle,
                        "persistent_bindings_size": len(self.induced_bindings),
                        # Audit-only, computed after the decision was taken and
                        # never read by it: does the arm's own induced binding
                        # equal the handle the plan bound for this span?
                        "audit_plan_bound_handle": _bound_handle(expected.path),
                        "audit_binding_matches_plan": (not gated)
                        or (self.current_binding == _bound_handle(expected.path)),
                    },
                )
            )
            store_snapshot = dict(substrate.store)
            last_request = (step.method, step.path)

        return {
            "episode": episode,
            "spans": n,
            "model_calls": model_calls_this_episode,
            "compiled_replays": compiled_hits,
            "compile_events": 0,
            "final_store_empty": len(substrate.store) == 0,
            "store_empty_at_episode_start": store_empty_at_start,
            "code_ok": code_ok,
            "current_binding_at_episode_end": self.current_binding,
            "cache_size": len(self.cache),
            "persistent_bindings": len(self.induced_bindings),
        }


def _bound_handle(path: str) -> str | None:
    """The handle a materialised plan path carries, or None. Audit use only."""
    for marker in ("?t=", "?view="):
        if marker in path:
            tail = path.split(marker, 1)[1]
            return tail.split("&", 1)[0] or None
    return None


def _decl_headers(body: Any) -> dict[str, str]:
    return {"Content-Type": "application/json"} if body is not None else {}


__all__ = ["BindingCacheEntry", "CrossEpisodeCompiledBinding", "WITNESS_THRESHOLD"]
