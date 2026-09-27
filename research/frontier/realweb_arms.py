"""Arms for EXP-FRONTIER-36293269574 - Real Web cross-site transfer experiment.

Arms:
- INHERITED_PARAMETERIZED (Treatment) - UNAVAILABLE (no distill_parameterized in kernel)
- NULL_STATE_KEYED (Mandatory Null Control) - state-keyed cache omitting gating object identity
- COLD_REEXPLORATION (Baseline) - fresh exploration each episode
- NO_MEMORY_DETERMINISTIC (Baseline) - re-derive from observation each episode
- WITHIN_EPISODE_SCRATCHPAD (Reference) - within-episode propagation only
- ORACLE_PERFECT_TRANSFER (Positive Control) - perfect identifier knowledge
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .realweb_substrate import (
    RealWebClient,
    RealHTTPResponse,
    MinimalObservation,
    extract_minimal_observation,
    detect_identifiers,
    TEST_SITES,
    TRAIN_SITES,
    INTENTS,
    TOKENIZER,
)
from .realweb_substrate import check_site_reachable


# Cost ledger components
@dataclass
class CostLedger:
    """Cost ledger for real Web experiment."""
    observation_tokens: int = 0
    requests: int = 0
    verification_calls: int = 0
    repair_events: int = 0

    def charge_observation(self, tokens: int) -> None:
        self.observation_tokens += tokens

    def charge_request(self) -> None:
        self.requests += 1

    def charge_verification(self) -> None:
        self.verification_calls += 1

    def charge_repair(self) -> None:
        self.repair_events += 1

    def total_cost(self) -> int:
        return self.observation_tokens + self.requests + self.verification_calls + self.repair_events

    def amortized_cost(self, episodes: int) -> float:
        return self.total_cost() / episodes if episodes else float("nan")

    def as_dict(self, episodes: int) -> dict[str, Any]:
        return {
            "episodes": episodes,
            "observation_tokens": self.observation_tokens,
            "requests": self.requests,
            "verification_calls": self.verification_calls,
            "repair_events": self.repair_events,
            "total_cost": self.total_cost(),
            "amortized_cost_per_episode": self.amortized_cost(episodes),
        }


@dataclass
class SpanRecord:
    """Raw span record for evidence."""
    arm: str
    site: str
    episode: int
    span_index: int
    intent: str
    method: str
    url: str
    response_code: int
    response_body_hash: str
    observation_tokens: int
    decision_path: str
    correct: bool
    detail: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "arm": self.arm,
            "site": self.site,
            "episode": self.episode,
            "span_index": self.span_index,
            "intent": self.intent,
            "method": self.method,
            "url": self.url,
            "response_code": self.response_code,
            "response_body_hash": self.response_body_hash,
            "observation_tokens": self.observation_tokens,
            "decision_path": self.decision_path,
            "correct": self.correct,
            "detail": self.detail,
        }


class ArmBase:
    """Base class for all arms."""

    def __init__(self, arm_id: str):
        self.arm_id = arm_id
        self.ledger = CostLedger()
        self.records: list[SpanRecord] = []
        self.episodes_run = 0

    def run_episode(self, site: str, episode: int, client: RealWebClient) -> dict[str, Any]:
        raise NotImplementedError

    def get_metrics(self) -> dict[str, Any]:
        total_spans = len(self.records)
        correct_spans = sum(1 for r in self.records if r.correct)
        abstentions = sum(1 for r in self.records if r.decision_path == "ABSTAIN")
        false_replays = sum(1 for r in self.records if r.decision_path == "FALSE_REPLAY")

        return {
            "arm": self.arm_id,
            "episodes": self.episodes_run,
            "total_spans": total_spans,
            "correct_spans": correct_spans,
            "span_level_action_correctness": correct_spans / total_spans if total_spans else 0.0,
            "abstention_rate": abstentions / total_spans if total_spans else 0.0,
            "false_replay_rate": false_replays / total_spans if total_spans else 0.0,
            "cost": self.ledger.as_dict(self.episodes_run),
            "records": [r.as_dict() for r in self.records],
        }


# ============================================================================
# NULL_STATE_KEYED - Mandatory Null Control
# ============================================================================
class NullStateKeyedArm(ArmBase):
    """State-keyed cache that OMITS the gating object's identity.

    This is exactly the shape of SPIDER's incumbent state-keyed cache
    that produced 80/600 silent false compiled replays in EXP-FRONTIER-36287182510.

    Cache key = observable state signature only (world store snapshot + last request).
    """

    def __init__(self):
        super().__init__("NULL_STATE_KEYED")
        self.cache: dict[str, dict[str, Any]] = {}  # state_sig -> {intent: action}
        self.site_stores: dict[str, dict] = {}  # site -> store snapshot

    def _state_signature(self, store: dict, last_request: tuple[str, str] | None) -> str:
        """Observable state key available without model call."""
        payload = {
            "store_keys": sorted(store.keys()) if store else [],
            "last_method": last_request[0] if last_request else None,
            "last_path": last_request[1] if last_request else None,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]

    def _make_request(self, client: RealWebClient, intent: str, site: str, resource_id: str | None) -> tuple[RealHTTPResponse, MinimalObservation]:
        """Execute request for intent on site."""
        self.ledger.charge_request()

        if intent == "list_resources":
            resp = client.get(site)
        elif intent == "read_resource" and resource_id:
            resp = client.get(f"{site}/{resource_id}")
        else:
            # For unsupported intents on read-only APIs, use base endpoint
            resp = client.get(site)

        obs = extract_minimal_observation(resp)
        self.ledger.charge_observation(obs.tokens)
        return resp, obs

    def run_episode(self, site: str, episode: int, client: RealWebClient) -> dict[str, Any]:
        self.episodes_run += 1
        store = self.site_stores.get(site, {})
        last_request: tuple[str, str] | None = None
        correct = 0
        total = 0

        # For read-only APIs, we test list_resources and read_resource
        intents_to_test = ["list_resources", "read_resource"]

        for span_idx, intent in enumerate(intents_to_test):
            state_sig = self._state_signature(store, last_request)

            # Check cache
            cached_action = self.cache.get(state_sig, {}).get(intent)

            if cached_action:
                # Replay from cache - this is where false replays happen
                # when observable state is same but gating object differs
                self.ledger.charge_verification()
                resp, obs = self._make_request(client, intent, site, cached_action.get("resource_id"))
                self.records.append(SpanRecord(
                    arm=self.arm_id, site=site, episode=episode, span_index=span_idx,
                    intent=intent, method=cached_action["method"], url=cached_action["url"],
                    response_code=resp.status_code, response_body_hash=hashlib.sha256(resp.body).hexdigest()[:16],
                    observation_tokens=obs.tokens, decision_path="CACHE_REPLAY",
                    correct=resp.status_code == 200,
                    detail={"cached": True, "resource_id": cached_action.get("resource_id")}
                ))
                if resp.status_code == 200:
                    correct += 1
                else:
                    # False replay - cache served wrong action
                    self.records[-1].decision_path = "FALSE_REPLAY"
            else:
                # Cold - explore
                resource_id = None
                if intent == "read_resource" and store:
                    # Try to read first resource
                    resource_id = list(store.keys())[0] if store else None

                resp, obs = self._make_request(client, intent, site, resource_id)

                # Learn from successful response
                if resp.status_code == 200 and intent == "list_resources":
                    try:
                        data = json.loads(resp.body_text)
                        # Extract resource IDs from response
                        if isinstance(data, dict) and "message" in data:
                            # dog.ceo format
                            for breed in data["message"]:
                                store[breed] = {"breed": breed}
                        elif isinstance(data, list):
                            # Generic list
                            for i, item in enumerate(data):
                                if isinstance(item, dict) and "id" in item:
                                    store[str(item["id"])] = item
                    except Exception:
                        pass

                self.records.append(SpanRecord(
                    arm=self.arm_id, site=site, episode=episode, span_index=span_idx,
                    intent=intent, method=resp.method, url=resp.url,
                    response_code=resp.status_code, response_body_hash=hashlib.sha256(resp.body).hexdigest()[:16],
                    observation_tokens=obs.tokens, decision_path="COLD_EXPLORE",
                    correct=resp.status_code == 200,
                    detail={"cached": False}
                ))
                if resp.status_code == 200:
                    correct += 1
                    # Cache the action
                    self.cache.setdefault(state_sig, {})[intent] = {
                        "method": resp.method,
                        "url": resp.url,
                        "resource_id": resource_id,
                    }

            total += 1
            last_request = (resp.method, resp.url)
            store = self.site_stores.get(site, {})

        self.site_stores[site] = store

        return {
            "episode": episode,
            "spans": total,
            "correct": correct,
            "cost": self.ledger.as_dict(self.episodes_run),
        }


# ============================================================================
# COLD_REEXPLORATION - Baseline
# ============================================================================
class ColdReexplorationArm(ArmBase):
    """Fresh exploration each episode. No memory inheritance."""

    def __init__(self):
        super().__init__("COLD_REEXPLORATION")

    def _make_request(self, client: RealWebClient, intent: str, site: str, resource_id: str | None) -> tuple[RealHTTPResponse, MinimalObservation]:
        self.ledger.charge_request()
        if intent == "list_resources":
            resp = client.get(site)
        elif intent == "read_resource" and resource_id:
            resp = client.get(f"{site}/{resource_id}")
        else:
            resp = client.get(site)
        obs = extract_minimal_observation(resp)
        self.ledger.charge_observation(obs.tokens)
        return resp, obs

    def run_episode(self, site: str, episode: int, client: RealWebClient) -> dict[str, Any]:
        self.episodes_run += 1
        correct = 0
        total = 0
        intents_to_test = ["list_resources", "read_resource"]

        for span_idx, intent in enumerate(intents_to_test):
            resource_id = None
            resp, obs = self._make_request(client, intent, site, resource_id)

            self.records.append(SpanRecord(
                arm=self.arm_id, site=site, episode=episode, span_index=span_idx,
                intent=intent, method=resp.method, url=resp.url,
                response_code=resp.status_code, response_body_hash=hashlib.sha256(resp.body).hexdigest()[:16],
                observation_tokens=obs.tokens, decision_path="COLD_EXPLORE",
                correct=resp.status_code == 200,
                detail={}
            ))
            if resp.status_code == 200:
                correct += 1
            total += 1

        return {"episode": episode, "spans": total, "correct": correct, "cost": self.ledger.as_dict(self.episodes_run)}


# ============================================================================
# NO_MEMORY_DETERMINISTIC - Baseline
# ============================================================================
class NoMemoryDeterministicArm(ArmBase):
    """No persistent memory. Re-derives action from observation each episode."""

    def __init__(self):
        super().__init__("NO_MEMORY_DETERMINISTIC")

    def _make_request(self, client: RealWebClient, intent: str, site: str, resource_id: str | None) -> tuple[RealHTTPResponse, MinimalObservation]:
        self.ledger.charge_request()
        if intent == "list_resources":
            resp = client.get(site)
        elif intent == "read_resource" and resource_id:
            resp = client.get(f"{site}/{resource_id}")
        else:
            resp = client.get(site)
        obs = extract_minimal_observation(resp)
        self.ledger.charge_observation(obs.tokens)
        return resp, obs

    def run_episode(self, site: str, episode: int, client: RealWebClient) -> dict[str, Any]:
        self.episodes_run += 1
        correct = 0
        total = 0
        intents_to_test = ["list_resources", "read_resource"]

        for span_idx, intent in enumerate(intents_to_test):
            # Re-derive from observation: first list, then read first item
            if intent == "list_resources":
                resp, obs = self._make_request(client, intent, site, None)
                resource_id = None
                if resp.status_code == 200:
                    try:
                        data = json.loads(resp.body_text)
                        if isinstance(data, dict) and "message" in data:
                            resource_id = list(data["message"].keys())[0] if data["message"] else None
                        elif isinstance(data, list) and data:
                            if isinstance(data[0], dict) and "id" in data[0]:
                                resource_id = str(data[0]["id"])
                    except Exception:
                        pass
            else:
                resp, obs = self._make_request(client, intent, site, resource_id)

            self.records.append(SpanRecord(
                arm=self.arm_id, site=site, episode=episode, span_index=span_idx,
                intent=intent, method=resp.method, url=resp.url,
                response_code=resp.status_code, response_body_hash=hashlib.sha256(resp.body).hexdigest()[:16],
                observation_tokens=obs.tokens, decision_path="RE_DERIVE",
                correct=resp.status_code == 200,
                detail={"resource_id": resource_id}
            ))
            if resp.status_code == 200:
                correct += 1
            total += 1

        return {"episode": episode, "spans": total, "correct": correct, "cost": self.ledger.as_dict(self.episodes_run)}


# ============================================================================
# WITHIN_EPISODE_SCRATCHPAD - Reference
# ============================================================================
class WithinEpisodeScratchpadArm(ArmBase):
    """Within-episode value propagation only. Zero cross-episode retention."""

    def __init__(self):
        super().__init__("WITHIN_EPISODE_SCRATCHPAD")

    def _make_request(self, client: RealWebClient, intent: str, site: str, resource_id: str | None) -> tuple[RealHTTPResponse, MinimalObservation]:
        self.ledger.charge_request()
        if intent == "list_resources":
            resp = client.get(site)
        elif intent == "read_resource" and resource_id:
            resp = client.get(f"{site}/{resource_id}")
        else:
            resp = client.get(site)
        obs = extract_minimal_observation(resp)
        self.ledger.charge_observation(obs.tokens)
        return resp, obs

    def run_episode(self, site: str, episode: int, client: RealWebClient) -> dict[str, Any]:
        self.episodes_run += 1
        correct = 0
        total = 0
        intents_to_test = ["list_resources", "read_resource"]
        scratchpad: dict[str, Any] = {"resource_ids": []}

        for span_idx, intent in enumerate(intents_to_test):
            resource_id = None
            if intent == "read_resource" and scratchpad["resource_ids"]:
                resource_id = scratchpad["resource_ids"][0]

            resp, obs = self._make_request(client, intent, site, resource_id)

            # Propagate within episode
            if resp.status_code == 200 and intent == "list_resources":
                try:
                    data = json.loads(resp.body_text)
                    if isinstance(data, dict) and "message" in data:
                        scratchpad["resource_ids"] = list(data["message"].keys())
                    elif isinstance(data, list):
                        scratchpad["resource_ids"] = [str(item.get("id", i)) for i, item in enumerate(data) if isinstance(item, dict)]
                except Exception:
                    pass

            self.records.append(SpanRecord(
                arm=self.arm_id, site=site, episode=episode, span_index=span_idx,
                intent=intent, method=resp.method, url=resp.url,
                response_code=resp.status_code, response_body_hash=hashlib.sha256(resp.body).hexdigest()[:16],
                observation_tokens=obs.tokens, decision_path="SCRATCHPAD_PROPAGATED" if resource_id else "SCRATCHPAD_EMPTY",
                correct=resp.status_code == 200,
                detail={"scratchpad_size": len(scratchpad["resource_ids"]), "resource_id": resource_id}
            ))
            if resp.status_code == 200:
                correct += 1
            total += 1

        return {"episode": episode, "spans": total, "correct": correct, "cost": self.ledger.as_dict(self.episodes_run)}


# ============================================================================
# ORACLE_PERFECT_TRANSFER - Positive Control
# ============================================================================
class OraclePerfectTransferArm(ArmBase):
    """Oracle that knows the correct stable identifier for every action-gating object."""

    def __init__(self):
        super().__init__("ORACLE_PERFECT_TRANSFER")
        self.known_resources: dict[str, list[str]] = {}  # site -> [resource_ids]

    def _make_request(self, client: RealWebClient, intent: str, site: str, resource_id: str | None) -> tuple[RealHTTPResponse, MinimalObservation]:
        self.ledger.charge_request()
        if intent == "list_resources":
            resp = client.get(site)
        elif intent == "read_resource" and resource_id:
            resp = client.get(f"{site}/{resource_id}")
        else:
            resp = client.get(site)
        obs = extract_minimal_observation(resp)
        self.ledger.charge_observation(obs.tokens)
        return resp, obs

    def run_episode(self, site: str, episode: int, client: RealWebClient) -> dict[str, Any]:
        self.episodes_run += 1
        correct = 0
        total = 0
        intents_to_test = ["list_resources", "read_resource"]

        # Oracle knows all resources from first episode
        if site not in self.known_resources:
            resp = client.get(site)
            self.ledger.charge_request()
            self.ledger.charge_observation(extract_minimal_observation(resp).tokens)
            if resp.status_code == 200:
                try:
                    data = json.loads(resp.body_text)
                    if isinstance(data, dict) and "message" in data:
                        self.known_resources[site] = list(data["message"].keys())
                    elif isinstance(data, list):
                        self.known_resources[site] = [str(item.get("id", i)) for i, item in enumerate(data) if isinstance(item, dict)]
                except Exception:
                    self.known_resources[site] = []

        for span_idx, intent in enumerate(intents_to_test):
            resource_id = None
            if intent == "read_resource" and self.known_resources.get(site):
                resource_id = self.known_resources[site][0]

            resp, obs = self._make_request(client, intent, site, resource_id)

            self.records.append(SpanRecord(
                arm=self.arm_id, site=site, episode=episode, span_index=span_idx,
                intent=intent, method=resp.method, url=resp.url,
                response_code=resp.status_code, response_body_hash=hashlib.sha256(resp.body).hexdigest()[:16],
                observation_tokens=obs.tokens, decision_path="ORACLE_PERFECT",
                correct=resp.status_code == 200,
                detail={"resource_id": resource_id, "known_count": len(self.known_resources.get(site, []))}
            ))
            if resp.status_code == 200:
                correct += 1
            total += 1

        return {"episode": episode, "spans": total, "correct": correct, "cost": self.ledger.as_dict(self.episodes_run)}


# ============================================================================
# INHERITED_PARAMETERIZED - Treatment (UNAVAILABLE)
# ============================================================================
class InheritedParameterizedArm(ArmBase):
    """Parameterized mechanism from C-PARAM-INHERIT product kernel.

    UNAVAILABLE: src/spider/kernel.py has no distill_parameterized method.
    Only distill() exists with hardcoded confidence=0.5.
    """

    def __init__(self):
        super().__init__("INHERITED_PARAMETERIZED")
        self.available = False
        self.reason = "distill_parameterized not implemented in src/spider/kernel.py; distill() hardcodes confidence=0.5 < min_confidence=0.8"

    def run_episode(self, site: str, episode: int, client: RealWebClient) -> dict[str, Any]:
        self.episodes_run += 1
        # Record unavailability
        self.records.append(SpanRecord(
            arm=self.arm_id, site=site, episode=episode, span_index=0,
            intent="N/A", method="N/A", url="N/A",
            response_code=0, response_body_hash="",
            observation_tokens=0, decision_path="UNAVAILABLE",
            correct=False,
            detail={"reason": self.reason}
        ))
        return {"episode": episode, "spans": 0, "correct": 0, "cost": self.ledger.as_dict(self.episodes_run)}

    def get_metrics(self) -> dict[str, Any]:
        base = super().get_metrics()
        base["available"] = False
        base["unavailability_reason"] = self.reason
        return base


# ============================================================================
# Arm Factory
# ============================================================================
def create_arms() -> dict[str, ArmBase]:
    """Create all arms for the experiment."""
    return {
        "INHERITED_PARAMETERIZED": InheritedParameterizedArm(),
        "NULL_STATE_KEYED": NullStateKeyedArm(),
        "COLD_REEXPLORATION": ColdReexplorationArm(),
        "NO_MEMORY_DETERMINISTIC": NoMemoryDeterministicArm(),
        "WITHIN_EPISODE_SCRATCHPAD": WithinEpisodeScratchpadArm(),
        "ORACLE_PERFECT_TRANSFER": OraclePerfectTransferArm(),
    }


if __name__ == "__main__":
    # Quick test
    arms = create_arms()
    client = RealWebClient()
    for name, arm in arms.items():
        print(f"Testing {name}...")
        result = arm.run_episode("https://dog.ceo", 1, client)
        print(f"  {result}")