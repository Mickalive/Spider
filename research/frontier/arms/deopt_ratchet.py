"""Arm A of EXP-FRONTIER-36249071934: B-NO-MEMORY-DETERMINISTIC (deopt ratchet).

Frozen-design provenance: prereg.md sections 6.1, 7.1, 7.2.

Mechanism, exactly as preregistered:
  1. cold episode: execute every span via the model oracle;
  2. compile a span once its ``(world state, own last request)`` key has been
     witnessed with the same next-action at least twice;
  3. deopt any span that is not compiled to the model oracle (1 unit);
  4. ratchet: replay compiled spans directly (1 unit execution, 0 model calls),
     recompile newly-witnessed-deterministic keys;
  5. amortisation: 1 unit per unique span compiled, 1 unit per deopt, 1 unit per
     span executed.

No registry, no distillation, no resolution, no freshness guard, no parameter
induction -- this arm accumulates no cross-episode knowledge beyond a
state -> next-action table rebuilt from the current episode's own observations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..substrate_deterministic_http import DeterministicHTTPSubstrate, KeepAliveClient, sha256_hex, span_signature
from ..taskplan import EXPECTED_CODES, Step
from .common import Ledger, ModelOracle, SpanRecord, observable_state_sig

#: prereg.md 6.1 step 2 -- "spans that have been witnessed >=2 times".
WITNESS_THRESHOLD = 2


@dataclass
class CacheEntry:
    state_sig: str
    request: dict[str, Any]
    witnesses: int = 0
    ambiguous: bool = False
    first_witnessed_episode: int = -1
    compiled_at_episode: int = -1


@dataclass
class DeoptRatchet:
    arm: str = "B-NO-MEMORY-DETERMINISTIC"
    oracle: ModelOracle = field(default_factory=ModelOracle)
    ledger: Ledger = field(default_factory=Ledger)
    cache: dict[str, CacheEntry] = field(default_factory=dict)
    model_calls_after_compile_complete: int = 0
    compiled_complete_at_episode: int | None = None
    compile_events_this_episode: list[dict[str, Any]] = field(default_factory=list)
    conflicts_detected: int = 0
    deopt_compile_misses: int = 0
    deopt_no_entry: int = 0

    # -- ratchet internals -------------------------------------------------
    def _witness(self, state_sig: str, step: Step, episode: int) -> None:
        request = {"method": step.method, "path": step.path, "body": step.body}
        entry = self.cache.get(state_sig)
        if entry is None:
            self.cache[state_sig] = CacheEntry(
                state_sig=state_sig, request=request, witnesses=1, first_witnessed_episode=episode
            )
            return
        if entry.request != request:
            # Conservative guard: a state key that ever maps to two different
            # correct actions is never compiled; the span is deopted instead.
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
            self.compile_events_this_episode.append(
                {
                    "episode": episode,
                    "state_sig": state_sig,
                    "method": step.method,
                    "path": step.path,
                    "witnesses": entry.witnesses,
                }
            )
            if self.compiled_complete_at_episode is None:
                self.compiled_complete_at_episode = episode

    def _lookup(self, state_sig: str) -> CacheEntry | None:
        entry = self.cache.get(state_sig)
        if entry is None:
            self.deopt_no_entry += 1
            return None
        if entry.ambiguous or entry.compiled_at_episode < 0:
            self.deopt_compile_misses += 1
            return None
        return entry

    # -- one episode -------------------------------------------------------
    def run_episode(
        self,
        substrate: DeterministicHTTPSubstrate,
        client: KeepAliveClient,
        episode: int,
        plan: list[Step],
        records: list[SpanRecord],
    ) -> dict[str, Any]:
        substrate.reset()
        self.compile_events_this_episode = []
        store_snapshot: dict[str, Any] = dict(substrate.store)
        last_request: tuple[str, str] | None = None
        model_calls_this_episode = 0
        code_ok = True
        compiled_hits = 0

        for index, expected in enumerate(plan):
            state_sig = observable_state_sig(store_snapshot, last_request)
            entry = self._lookup(state_sig)
            if entry is not None:
                decision_path = "COMPILED_REPLAY"
                step = Step(
                    expected.role,
                    entry.request["method"],
                    entry.request["path"],
                    entry.request["body"],
                    EXPECTED_CODES[expected.role],
                )
                compiled_hits += 1
                self.ledger.bump("compiled_replays")
            else:
                decision_path = "DEOPT_TO_MODEL"
                step = self.oracle.decide(plan, index, store_snapshot)
                self.ledger.charge("model")
                model_calls_this_episode += 1

            self._witness(state_sig, step, episode)

            code, raw, sent = client.request(step.method, step.path, step.body)
            self.ledger.charge("execution")
            ok = code == EXPECTED_CODES[step.role]
            code_ok = code_ok and ok

            cached = self.cache.get(state_sig)
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
                    signature=span_signature(
                        step.method, step.path, _decl_headers(step.body), step.body, code, raw
                    ),
                    state_sig=state_sig,
                    decision_path=decision_path,
                    detail={
                        "expected_code": EXPECTED_CODES[step.role],
                        "code_ok": ok,
                        "witnesses_after": cached.witnesses if cached else 0,
                        "compiled": bool(cached and cached.compiled_at_episode >= 0),
                        "cache_ambiguous": bool(cached and cached.ambiguous),
                    },
                )
            )

            store_snapshot = dict(substrate.store)
            last_request = (step.method, step.path)

        if self.compiled_complete_at_episode is not None and episode > self.compiled_complete_at_episode:
            self.model_calls_after_compile_complete += model_calls_this_episode

        return {
            "episode": episode,
            "spans": len(plan),
            "model_calls": model_calls_this_episode,
            "compiled_replays": compiled_hits,
            "compile_events": len(self.compile_events_this_episode),
            "final_store_empty": len(substrate.store) == 0,
            "code_ok": code_ok,
        }


def _decl_headers(body: Any) -> dict[str, str]:
    """Declared request headers, matching what the substrate client sends.

    prereg.md 12 normalizes headers inside the span signature; the volatile
    transport headers are excluded inside ``normalize_headers``.
    """
    return {"Content-Type": "application/json"} if body is not None else {}
